""" Server events for the application. """
from sanic import Sanic
from asyncio import AbstractEventLoop

async def before_server_start(app: Sanic, loop: AbstractEventLoop) -> None:
    """
        Run before the server starts.

        Args:
            app (Sanic): The Sanic application.
            loop (asyncio.AbstractEventLoop): The event loop.
    """

    ...

async def after_server_start(app: Sanic, loop: AbstractEventLoop) -> None:
    """
        Run after the server starts.

        Args:
            app (Sanic): The Sanic application.
            loop (asyncio.AbstractEventLoop): The event loop.
    """
    ...

async def before_server_stop(app: Sanic, loop: AbstractEventLoop) -> None:
    """
        Run before the server stops.

        Args:
            app (Sanic): The Sanic application.
            loop (asyncio.AbstractEventLoop): The event loop.
    """
    ...