""" Server events for the application. """
from sanic import Sanic
from asyncio import AbstractEventLoop
from core.database import init_db, close_db

async def before_server_start(app: Sanic, loop: AbstractEventLoop) -> None:
    """
        Run before the server starts.

        Args:
            app (Sanic): The Sanic application.
            loop (asyncio.AbstractEventLoop): The event loop.
    """

    engine, asyncsession, Base = await init_db(True)

    app.ctx.db = type('', (), {})()
    app.ctx.db.engine = engine
    app.ctx.db.asyncsession = asyncsession
    app.ctx.db.Base = Base

async def after_server_start(app: Sanic, loop: AbstractEventLoop) -> None:
    """
        Run after the server starts.

        Args:
            app (Sanic): The Sanic application.
            loop (asyncio.AbstractEventLoop): The event loop.
    """
    pass

async def before_server_stop(app: Sanic, loop: AbstractEventLoop) -> None:
    """
        Run before the server stops.

        Args:
            app (Sanic): The Sanic application.
            loop (asyncio.AbstractEventLoop): The event loop.
    """
    await close_db()