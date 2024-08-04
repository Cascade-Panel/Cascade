""" This module contains the index view. """

from dataclasses import dataclass
from sanic import Request
from sanic.views import HTTPMethodView
from sanic import text
from sanic_ext import validate
from sanic.response import HTTPResponse
from core.database.models.user.User import User

class IndexView(HTTPMethodView):
    """The index view."""
    uri = '/'

    
    @dataclass
    class QueryParams:
        q: str

    @dataclass
    class Json:
        text: str

    @validate(query=QueryParams)
    async def get(self, request: Request) -> HTTPResponse:
        """
            Handles GET requests to the index view.
        """
        return await text('I am get method with a query param `q`')

    @validate(json=Json)
    async def post(self, request: Request, user: User) -> HTTPResponse:
        """
            Handles POST requests to the index view.
        """

        return await text('I am a protected post method with json body and user object injected.')

    async def put(self, request: Request) -> HTTPResponse:
        """
            Handles PUT requests to the index view.
        """

        return await text('I am put method')