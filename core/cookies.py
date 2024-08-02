"""
This module provides functions for handling cookies.
"""

import jwt
from sanic import json, Sanic, response
from sanic.request import Request

secret = "secret"

def append_cookie(request: Request, response: json, key: str, value: str, http_only: bool = False, expires_in: int = 604800, algorithm: str = "HS256") -> response:
    """
        Append a cookie to a response.

        Attributes:
            request (Request): The request object.
            response (json): The response object.
            key (str): The key of the cookie.
            value (str): The value of the cookie.
            http_only (bool): Whether the cookie is HTTP only
            expires_in (int): The number of seconds until the cookie expires.
            algorithm (str): The algorithm to use to encode the cookie.

        Returns:
            Response: The response object with the cookie appended.
    """
    response.add_cookie(
        key,
        jwt.encode(value, 
            secret,
            algorithm=algorithm
        ),
        httponly=http_only,
        secure=True,
        max_age=expires_in,
        path="/"
    )
    return response

def get_cookie(request: Request, key: str, algorithm: str = "HS256") -> str | None:
    """
        Get a cookie from a request.

        Attributes:
            request (Request): The request object.
            key (str): The key of the cookie.
            algorithm (str): The algorithm to use to decode the cookie.

        Returns:
            str: The value of the cookie.
    """
    try:
        return jwt.decode(
            request.cookies[key],
            secret,
            algorithms=[algorithm]
        )
    except jwt.ExpiredSignatureError:
        return None

def remove_cookie(response: json, key: str) -> response:
    """
        Remove a cookie from a response.

        Attributes:
            request (Request): The request object.
            response (json): The response object.
            key (str): The key of the cookie.

        Returns:
            Response: The response object with the cookie removed.
    """
    response.del_cookie(key)
    return response

def update_cookie(request: Request, response: json, key: str, value: str, http_only: bool = False, expires_in: int = 604800, algorithm: str = "HS256") -> response:
    """
        Update a cookie in a response.

        Attributes:
            request (Request): The request object.
            response (json): The response object.
            key (str): The key of the cookie.
            value (str): The value of the cookie.
            http_only (bool): Whether the cookie is HTTP only
            expires_in (int): The number of seconds until the cookie expires.
            algorithm (str): The algorithm to use to encode the cookie.

        Returns:
            Response: The response object with the cookie updated.
    """
    response.del_cookie(key)
    return append_cookie(request, response, key, value, http_only, expires_in, algorithm)