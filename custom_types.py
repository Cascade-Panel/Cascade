from dataclasses import dataclass
from core.cache import CacheManager
from core.env_manager import EnvManager
from core.sessions import SessionManager
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import ConcreteBase

@dataclass
class DatabaseContext:
    engine: AsyncEngine
    asyncsession: sessionmaker
    Base: ConcreteBase

@dataclass
class MyTypedContext:
    db: DatabaseContext
    env_manager: EnvManager
    session_manager: SessionManager
    cache_manager: CacheManager
