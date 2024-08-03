""" Server events for the application. """
from sanic import Sanic
from asyncio import AbstractEventLoop
from core.database import init_db, close_db
from core.sessions import SessionManager
from core.cache import CacheManager

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

    CACHE_STORAGE_TYPE = app.ctx.env_manager.get("CACHE_STORAGE_TYPE")

    if CACHE_STORAGE_TYPE == "redis":
        REDIS_URL = app.ctx.env_manager.get("REDIS_URL")
        app.ctx.session_manager = SessionManager(connector_type="redis", redis_url=REDIS_URL)
        app.ctx.cache_manager = CacheManager(connector_type="redis", redis_url=REDIS_URL)



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