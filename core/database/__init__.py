""" A module to handle the database operations. """

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.env_manager import EnvManager

env_manager = EnvManager()

engine = create_async_engine(env_manager.get("MAIN_DB_URL"), future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

def fetch_encryption_key() -> str:
    """
        Get the encryption key.

        Args:
            None
        
        Returns:
            str: The encryption key.
    """
    return env_manager.get("DB_ENCRYPTION_KEY")

async def gen_tables() -> None:
    """
        Generate (or regenerate) the database tables.

        Args:
            None
        
        Returns:
            None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def init_db(regen=False) -> None:
    """
        Initialize the database.

        Args:
            None
        
        Returns:
            None
    """
    if regen:
        await gen_tables()
    return (engine, async_session, Base)

async def close_db() -> None:
    """
        Close the database.

        Args:
            None
        
        Returns:
            None
    """
    await engine.dispose()

async def get_session() -> AsyncSession: # type: ignore
    """
        Get a new session object.

        Args:
            None
        
        Returns:
            AsyncSession: The session object.
    """
    async with async_session() as session:
        yield session