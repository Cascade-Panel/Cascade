
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine('url', future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

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