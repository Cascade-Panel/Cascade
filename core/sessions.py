""" This module provides functions for saving user sessions in the application. """

from sqlalchemy import Uuid
from core.cache_storage import CacheStorageManager
from core.database.models.user.User import User

class SessionManager:
    def __init__(self, connector_type: str, **kwargs):
        """
            Initialize the session manager.

            Attributes:
                connector_type: The type of connector to use.
                kwargs: Additional keyword arguments to pass to the connector.
        """
        if connector_type.lower() == 'sqlite':
            from core.cache_storage.connectors.sqlite import SQLiteConnector
            self.sessions = CacheStorageManager(SQLiteConnector(**kwargs))
        elif connector_type.lower() == 'redis':
            from core.cache_storage.connectors.redis import RedisConnector
            self.sessions = CacheStorageManager(RedisConnector(**kwargs))
        else:
            raise ValueError('Invalid connector type: {}'.format(connector_type))
    
    async def __async__init__(self) -> None:
        """
            Initialize the session manager.
        """
        await self.sessions.__async__init__()
    
    async def get(self, session_id: str) -> User:
        """
            Retrieve a user uuid from the cache based on the session ID.

            Attributes:
                session_id: The ID of the session to retrieve.

            Returns:
                The user uuid if found, otherwise None.
        """
        user_uuid = await self.sessions.get(session_id)
        return user_uuid
    
    async def add(self, session_id: str, user_uuid: Uuid, ttl: int = None) -> None:
        """
            Add a user uuid to the cache.

            Attributes:
                session_id: The ID of the session.
                user_uuid: The user uuid to be cached.
                ttl: The time-to-live in seconds. Defaults to None.
        """
        await self.sessions.set(session_id, user_uuid, ttl=ttl)

    async def delete(self, session_id: str) -> None:
        """
            Remove a user uuid from the cache based on the session ID.

            Attributes:
                session_id: The ID of the session.
        """
        await self.sessions.delete(session_id)
    
    async def clear_expired(self) -> None:
        """
            Clear expired sessions from the cache.
        """
        await self.sessions.clear_expired()