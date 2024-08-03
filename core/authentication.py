""" This module provides functions for handling authentication. """

from sanic import BadRequest, text
from core.cookies import get_cookie, append_cookie, remove_cookie

from core.database.DALs.user.mfa_dal import MfaDAL
from core.database.DALs.user.user_dal import UserDAL
from core.database.models.user.User import User
from core.database.models.user.MfaBackupCodes import MfaBackupCodes
from core.database.models.user.Mfa import Mfa

async def is_authorised(request) -> bool:
    """
        Determine if the user is authorised.

        Attributes:
            request (Request): The request object.

        Returns:
            bool: True if the user is authorised, False otherwise.
    """
    user_uuid = get_cookie(request, request.app.ctx.env_manager.get("COOKIE_IDENTITY"))
    if user_uuid is None:
        return False

    user = await UserDAL(request.app.db_session).get(user_uuid)
    if user is None:
        return False

    ## check that the users email is verified
    if not user.is_email_verified:
        return False
    
    ## check that they are not setting up mfa
    mfa = await MfaDAL(request.app.db_session).get(user.uuid)
    if mfa is not None and mfa.is_setting_up:
        return False

    return True

async def get_user(request) -> User:
    """
        Get the user from the request.
        - Requires the user to be logged in.

        Attributes:
            request (Request): The request object.

        Returns:
            User: The user.
    """
    if not is_authorised(request):
        raise BadRequest('You are not logged in.')

    cookie_data = get_cookie(request, request.app.ctx.env_manager.get("COOKIE_IDENTITY"))
    
    user_uuid = cookie_data.get("user_uuid")

    cached_user = request.app.ctx.cache_manager.get(user_uuid)

    if cached_user is None:
        raise BadRequest('You are not logged in.')
    return cached_user

async def restricted_to_unverified(request) -> bool:
    """
        Determine if the user is allowed to access the endpoint without their email being verified.

        Attributes:
            request (Request): The request object.

        Returns:
            bool: True if the user is allowed to access the endpoint without their email being verified, False otherwise.
    """
    if not is_authorised(request):
        return False
    
    ## check if the users email is verified
    user = await get_user(request)

    return user.is_email_verified

async def restricted_to_mfa_setters(request) -> bool:
    """
        Determine if the user is authorised before MFA has been setup fully.

        Attributes:
            request (Request): The request object.

        Returns:
            bool: True if the user is authorised before MFA, False otherwise.
    """
    user = await get_user(request)
    if user is None:
        return False

    mfa = await MfaDAL(request.app.db_session).get(user.uuid)
    if mfa is None:
        return False

    return mfa.is_setting_up

async def login(request, user: User) -> None:
    """
        Log the user in.

        Attributes:
            request (Request): The request object.
            user (User): The user to log in.

        Raises:
            BadRequest: If the user is already logged in.
    """
    if is_authorised(request):
        raise BadRequest('User is already logged in')

    response = text('Logged in')

    response = append_cookie(request, response, request.app.ctx.env_manager.get("COOKIE_IDENTITY"), {"user_uuid": user.uuid})
    return response

async def logout(request) -> bool:
    """
        Log the user out.

        Attributes:
            request (Request): The request object.

        Returns:
            bool: True if the user was logged out, False otherwise.
    """
    if not is_authorised(request):
        raise BadRequest('User is not logged in')

    response = text('Logged out')

    response = remove_cookie(response, request.app.ctx.env_manager.get("COOKIE_IDENTITY"))
    return response