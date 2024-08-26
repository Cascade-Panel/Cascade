from dataclasses import dataclass
from core.cache import CacheManager
from core.env_manager import EnvManager
from core.sessions import SessionManager
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import ConcreteBase

@dataclass
class DatabaseContext:
    """
        Sub-custom-context for database spesific actions

        Args:
            engine: sqlalchemy.ext.asyncio.AsyncEngine
            asyncsession: sqlalchemy.orm.sessionmaker
            Base: sqlalchemy.ext.declarative.ConcreteBase
    """
    engine: AsyncEngine
    asyncsession: sessionmaker
    Base: ConcreteBase

@dataclass
class MyTypedContext:
    """
        Custom typed context for the app.ctx object

        Args:
            db: DatabaseContext
            env_manager: core.env_manager.EnvManager
            session_manager: core.session_manager.SessionManager
            cache_manager: core.cache_manager.CacheManager
    """
    db: DatabaseContext
    env_manager: EnvManager
    session_manager: SessionManager
    cache_manager: CacheManager
