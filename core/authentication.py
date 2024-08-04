""" This module provides core functions for handling authentication. """

from sanic import BadRequest, HTTPResponse, text
from core.cookies import get_cookie, append_cookie, remove_cookie

from core.database.DALs.user.mfa_dal import MfaDAL
from core.database.DALs.user.user_dal import UserDAL
from core.database.models.user.Mfa import Mfa
from core.database.models.user.User import User
from sanic import Request

async def get_session(request: Request) -> str | None:
    """
    Get the user session ID from the request.

    Attributes:
        request (sanic.Request): The request object.
    
    Returns:
        The session ID if found, otherwise None.
    """
    cookie_data = get_cookie(request, request.app.ctx.env_manager.get("COOKIE_IDENTITY"))
    session_id = cookie_data.get("user_uuid") if cookie_data else None

    if not session_id:
        raise BadRequest('Unauthorized')
    
    session_data = request.app.ctx.session_manager.get(session_id)

    if not session_data:
        raise BadRequest('Unauthorized')
    
    return session_id

async def fetch_user(session, user_uuid: str) -> User | None:
    """
    Fetch a user from the database.

    Attributes:
        session: The database session.
        user_uuid: The UUID of the user to fetch.
    
    Returns:
        The user if found, otherwise None.
    """
    user_dal = UserDAL(session)
    return await user_dal.get(user_uuid)

async def fetch_mfa(session, user_uuid: str) -> Mfa | None:
    """
    Fetch an MFA from the database.

    Attributes:
        session: The database session.
        user_uuid: The UUID of the user to fetch the MFA for.

    Returns:
        The MFA if found, otherwise None.
    """
    mfa_dal = MfaDAL(session)
    return await mfa_dal.get(user_uuid)

async def is_authorized(request) -> bool:
    """
    Check if the user is authorized.

    Attributes:
        request (sanic.Request): The request object.

    Returns:
        True if the user is authorized, otherwise False.
    """
    user_uuid = await (request)
    if not user_uuid:
        return False

    async with request.app.db_session() as session:
        async with session.begin():
            user = await fetch_user(session, user_uuid)
            if not user or not user.is_email_verified:
                return False

            mfa = await fetch_mfa(session, user.uuid)
            if mfa and mfa.is_setting_up:
                return False

    return True

async def get_user(request) -> User | None:
    """
    Get the user from the request.

    Attributes:
        request (sanic.Request): The request object.
    
    Returns:
        The user if found, otherwise None.
    """
    user_session = await get_session(request)
    if not user_session:
        raise BadRequest('Unauthorized')

    async with request.app.db_session() as session:
        async with session.begin():
            user = await fetch_user(session, user_session.get("user_uuid"))
            if not user or not user.is_email_verified:
                raise BadRequest('Unauthorized')

            mfa = await fetch_mfa(session, user.uuid)
            if mfa and mfa.is_setting_up:
                raise BadRequest('Forbidden: MFA is being set up')
            
            if mfa and user_session.get("is_logging_in_with_mfa"):
                raise BadRequest('Forbidden: User is currently logging in with MFA')
    return user

async def login(request, user: User) -> HTTPResponse:
    """
    Log the user in.

    Attributes:
        request (sanic.Request): The request object.
        user (User): The user to log in.

    Returns:
        A response with a signed cookie attached
    """
    if await is_authorized(request):
        raise BadRequest('User is already logged in')

    response = text('Logged in')
    response = append_cookie(request, response, request.app.ctx.env_manager.get("COOKIE_IDENTITY"), {"user_uuid": user.uuid})
    return response

async def logout(request) -> HTTPResponse:
    """
    Log the user out.

    Attributes:
        request (sanic.Request): The request object.
    
    Returns:
        A response with the cookie removed
    """
    if not await is_authorized(request):
        raise BadRequest('User is not logged in')

    response = text('Logged out')
    response = remove_cookie(response, request.app.ctx.env_manager.get("COOKIE_IDENTITY"))
    return response

async def restrict_to_mfa_setting_up(request: Request):
    """
    Restrict the route to users setting up MFA.

    Attributes:
        request (sanic.Request): The request object.
    
    Returns:
        The user if found, otherwise raises an exception
    """
    user_session = await get_session(request)
    if not user_session:
        raise BadRequest('Unauthorized')

    async with request.app.db_session() as session:
        async with session.begin():
            user = await fetch_user(session, user_session.get("user_uuid"))
            if not user:
                raise BadRequest('Unauthorized')

            mfa = await fetch_mfa(session, user.uuid)
            if not mfa or not mfa.is_setting_up:
                raise BadRequest('Forbidden: This route is restricted to users setting up MFA')
    return user

async def restrict_to_email_unverified(request: Request):
    """
    Restrict the route to users with unverified emails.

    Attributes:
        request (sanic.Request): The request object.

    Returns:
        The user if found, otherwise raises an exception
    """
    user_session = await get_session(request)
    if not user_session:
        raise BadRequest('Unauthorized')

    async with request.app.db_session() as session:
        async with session.begin():
            user = await fetch_user(session, user_session.get("user_uuid"))
            if not user or user.is_email_verified:
                raise BadRequest('Forbidden: This route is restricted to users with unverified emails')
    return user

async def restrict_to_mfa_logging_in(request: Request):
    """
    Restrict the route to users currently logging in with MFA.

    Attributes:
        request (sanic.Request): The request object.
    
    Returns:
        The user if found, otherwise raises an exception
    """
    user_session = await get_session(request)
    if not user_session:
        raise BadRequest('Unauthorized')

    if not user_session.get("is_logging_in_with_mfa"):
        raise BadRequest('Forbidden: This route is restricted to users currently logging in with MFA')
    
    async with request.app.db_session() as session:
        async with session.begin():
            user = await fetch_user(session, user_session.get("user_uuid"))
            if not user:
                raise BadRequest('Unauthorized')
    return user