from datetime import datetime
from typing import Dict, Union
from sqlalchemy import Uuid
from core.cache_storage import CacheStorageManager
from core.database.models.user.User import User

class SessionManager:
    def __init__(self, connector_type: str, **kwargs):
        """
        Initialize the session manager.

        Args:
            connector_type: The type of connector to use.
            kwargs: Additional keyword arguments to pass to the connector.
        """
        if connector_type.lower() == 'sqlite':
            from core.cache_storage.connectors.sqlite import SQLiteConnector
            self.sessions = CacheStorageManager(SQLiteConnector(**kwargs))
        elif connector_type.lower() == 'redis':
            from core.cache_storage.connectors.redis import RedisConnector
            self.sessions = CacheStorageManager(RedisConnector(**kwargs))
        elif connector_type.lower() == 'system':
            from core.cache_storage.connectors.system import SystemConnector
            self.cache = CacheStorageManager(SystemConnector(**kwargs))
        else:
            raise ValueError(f"Invalid connector type: {connector_type}")

    async def __async__init__(self) -> None:
        """
        Initialize the session manager.
        """
        await self.sessions.__async__init__()

    async def get(self, session_id: str) -> Union[Dict[str, Union[Uuid, str, datetime]], None]:
        """
        Retrieve a user session info from the cache based on the session ID.

        Args:
            session_id: The ID of the session to retrieve.

        Returns:
            The user session info if found, otherwise None.
        """
        session_info = await self.sessions.get(session_id)
        return session_info

    async def add(self, session_id: str, user_uuid: Uuid, ip_address: str, ttl: int = None) -> None:
        """
        Add a user session info to the cache.

        Args:
            session_id: The ID of the session.
            user_uuid: The user uuid to be cached.
            ip_address: The IP address where the session was created.
            ttl: The time-to-live in seconds. Defaults to None.
        """
        session_info = {
            'user_uuid': user_uuid,
            'created_at': datetime.now(),
            'ip_address': ip_address
        }
        await self.sessions.set(session_id, session_info, ttl=ttl)

    async def delete(self, session_id: str) -> None:
        """
        Remove a user session info from the cache based on the session ID.

        Args:
            session_id: The ID of the session.
        """
        await self.sessions.delete(session_id)

    async def clear_expired(self) -> None:
        """
        Clear expired sessions from the cache.
        """
        await self.sessions.clear_expired()
