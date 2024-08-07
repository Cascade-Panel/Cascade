from inspect import isawaitable
from functools import wraps

from sanic import BadRequest

from core.authentication import get_user, mfa_is_setting_up

def protected(
        inject: bool = True,
        email_unverified_only: bool = False,
        mfa_logging_in_only: bool = False,
        mfa_being_setup_only: bool = False,
    ):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):

            user, session = await get_user(request, include_session=True)

            if email_unverified_only and user.is_email_verified:
                raise BadRequest("User email is verified")
            
            if mfa_logging_in_only and not session.get("is_logging_in_with_mfa"):
                raise BadRequest("MFA is enabled")

            if mfa_being_setup_only and not mfa_is_setting_up(request, user):
                raise BadRequest("MFA is not being setup")

            if inject:
                response = f(request, user, *args, **kwargs)
            else:
                response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response

            return response

        return decorated_function

    return decorator