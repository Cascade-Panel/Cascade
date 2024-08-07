
from sanic import BadRequest, Request
from core.database.DALs.user.mfa_dal import MfaDAL
from core.database.models.user.User import User
from core.cookies import get_cookie

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