from core.authentication import is_authorised, restricted_to_unverified, restricted_to_mfa_setters
from sanic import BadRequest

def authenticated(func):
    """ 
        Decorator to ensure that the user is authenticated.
        - Forces the user to:
            - Be authenticated.
            - Not be verifying their email.
            - Not be setting up MFA.

        Raises:
            BadRequest: If the user is not authenticated.
    """
    def wrapper(request, *args, **kwargs):
        if not is_authorised(request):
            raise BadRequest("You are not authorised to access this resource.")
        return func(request, *args, **kwargs)
    return wrapper

def restricted_to_unverified(func):
    """
        Decorator to ensure that the user is allowed to access the endpoint without their email being verified.
        - Forces the user to:
            - Be authorised.
            - Have their email verified.

        Raises:
            BadRequest: If the user is not allowed to access the endpoint without their email being verified.
    """
    def wrapper(request, *args, **kwargs):
        if not restricted_to_unverified(request):
            raise BadRequest("You are not authorised to access this resource.")

        return func(request, *args, **kwargs)
    return wrapper

def restricted_to_mfa_setters(func):
    """
        Decorator to ensure that the user is authorised before MFA has been setup fully.
        - Forces the user to:
            - Be authorised.
            - Be setting up MFA.

        Raises:
            BadRequest: If the user is not authorised before MFA.
    """
    def wrapper(request, *args, **kwargs):
        if not restricted_to_mfa_setters(request):
            raise BadRequest("You are not authorised to access this resource.")
        return func(request, *args, **kwargs)
    return wrapper
