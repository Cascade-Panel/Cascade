
from datetime import datetime
from sanic import BadRequest, Request
from core.database.DALs.user.mfa_dal import MfaDAL
from core.database.DALs.user.user_dal import UserDAL
from core.database.models.user.User import User
from core.cookies import get_cookie
from core.hashing import check_password
from core.type_hints import Email, Password

async def fetch_cookie(request: Request) -> str:
    """
        Fetch the cookie from the request.

        Args:
            request: The incoming request.

        Returns:
            The cookie value.
    """
    cookie = get_cookie(request, request.app.ctx.env_manager.get("COOKIE_IDENTITY"))
    return cookie

async def get_user(request: Request, include_session: bool = False) -> User:
    """
        Retrieve the user from the request.

        Args:
            request: The incoming request.
            include_session: Whether to include the session alongside the user object.

        Returns:
            The user object.
        
        Raises:
            BadRequest: If the user is not found.
    """
    
    ctx = request.app.ctx

    cookie = await fetch_cookie(request)

    if cookie is None:
        raise BadRequest("Unauthorized")

    session = ctx.session_manager.get(cookie.get("session_id"))

    if session is None:
        raise BadRequest("Unauthorized")
    
    user = ctx.cache_manager.get(session.get("user_uuid"))

    if user is None:
        raise BadRequest("Unauthorized")

    if include_session:
        return (user, session)

    return user

async def mfa_is_setting_up(request, user: User) -> bool:
    """
        Retrieve the MFA setup status of the user from the request.

        Args:
            request: The incoming request.

        Returns:
            The MFA setup status.
    """
    
    async with request.app.ctx.db_session() as session:
        async with session.begin():
            mfa_dal = MfaDAL(session)

            mfa = await mfa_dal.get(user.uuid)

            return mfa.is_setting_up

async def login(request: Request, email: Email, password: Password) -> str:
    """
        Log in a user.

        Args:
            email: The user's email.
            password: The user's password.

        Returns:
            The users session ID.
    """
    app = request.app

    async with app.ctx.db_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = user_dal.get_by_email(email)

            if user is None:
                raise BadRequest("Invalid credentials")

            if not check_password(password, user.password):
                user.failed_login_attempts += 1
                user.last_failed_login = datetime.now()
                user.last_failed_login_ip = request.ip or request.remote_addr
                await user_dal.update(user)
                raise BadRequest("Invalid credentials")
            
            if user.is_mfa_enabled:
                if await mfa_is_setting_up(request, user):
                    raise BadRequest("MFA setup is not complete")
                mfa = True
            
            user.last_login = datetime.now()
            user.last_login_ip = request.ip or request.remote_addr

            len_sessions = 0

            for i in app.ctx.session_manager.get_all_values():
                if i.get("user_uuid") == user.uuid:
                    len_sessions += 1

            if len_sessions > user.max_sessions:
                raise BadRequest("Maximum number of sessions reached")

            session_id = app.ctx.session_manager.gen_session_id()

            await app.ctx.session_manager.add(
                session_id, user.uuid, 
                request.ip or request.remote_addr,
                mfa, ttl=app.ctx.env_manager.get("SESSION_TTL")
            )

            return session_id
    
async def logout(request: Request) -> None:
    """
        Log out a user.

        Args:
            request: The incoming request.
    """
    app = request.app

    user, session = await get_user(request, include_session=True)

    len_sessions = 0
    for i in app.ctx.session_manager.get_all_values():
        if i.get("user_uuid") == user.uuid:
            len_sessions += 1
    
    if len_sessions == 1:
        app.ctx.cache_manager.delete(user.uuid)
    
    app.ctx.session_manager.delete(session.get("session_id"))

    