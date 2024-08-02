""" This module contains the index view. """

from sanic import Request
from sanic.views import HTTPMethodView
from sanic import text

class IndexView(HTTPMethodView):
    """The index view."""
    uri = '/'

    async def get(self, request: Request):
        """
            Handles GET requests to the index view.
        """
        return await text('I am get method')

    async def post(self, request: Request):
        """
            Handles POST requests to the index view.
        """

        return await text('I am post method')

    async def put(self, request: Request):
        """
            Handles PUT requests to the index view.
        """

        return await text('I am put method')