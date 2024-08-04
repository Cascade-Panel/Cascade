from functools import wraps
from sanic import Request, HTTPResponse, BadRequest
from core.authentication import get_session, fetch_user, fetch_mfa

def protected():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            user_session = await get_session(request)
            if not user_session:
                raise BadRequest('Unauthorized')

            async with request.app.db_session() as session:
                async with session.begin():
                    user = await fetch_user(session, user_session.get("user_uuid"))
                    if not user:
                        raise BadRequest('Unauthorized')

                    # Inject the user into the route handler
                    return await f(request, user, *args, **kwargs)
        return decorated_function
    return decorator

