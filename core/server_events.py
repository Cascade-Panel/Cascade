""" Server events for the application. """
from sanic import Sanic
from asyncio import AbstractEventLoop
from core.database import init_db, close_db
from core.database.models.user.User import User
from core.sessions import SessionManager
from core.cache import CacheManager
from core.authentication import get_user
from core.config import init_config

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

    await init_config(app)

    CACHE_STORAGE_TYPE = app.ctx.env_manager.get("CACHE_STORAGE_TYPE")

    if CACHE_STORAGE_TYPE == "redis":
        REDIS_URL = app.ctx.env_manager.get("REDIS_URL")
        app.ctx.session_manager = SessionManager(connector_type="redis", redis_url=REDIS_URL)
        app.ctx.cache_manager = CacheManager(connector_type="redis", redis_url=REDIS_URL)
    if CACHE_STORAGE_TYPE == "sqlite":
        app.ctx.session_manager = SessionManager(connector_type="sqlite", db_path=app.ctx.env_manager.get("CACHE_STORAGE_DB_PATH"))
        app.ctx.cache_manager = CacheManager(connector_type="sqlite", db_path=app.ctx.env_manager.get("CACHE_STORAGE_DB_PATH"))
    if CACHE_STORAGE_TYPE == "system":
        app.ctx.session_manager = SessionManager(connector_type="system")
        app.ctx.cache_manager = CacheManager(connector_type="system")
    if CACHE_STORAGE_TYPE == "memcached":
        app.ctx.session_manager = SessionManager(connector_type="memcached", memcached_url=app.ctx.env_manager.get("MEMCACHED_URL"))
        app.ctx.cache_manager = CacheManager(connector_type="memcached", memcached_url=app.ctx.env_manager.get("MEMCACHED_URL"))

    # Adding user dependency if it has type hint `: User`
    app.ext.add_dependency(User, get_user)

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