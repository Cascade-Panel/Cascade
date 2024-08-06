""" This module provides functions for caching user information in the application. """

from sqlalchemy import Uuid
from core.cache_storage import CacheStorageManager
from core.database.models.user.User import User

class CacheManager:
    def __init__(self, connector_type: str, **kwargs):
        """
            Initialize the cache manager.

            Args:
                connector_type: The type of connector to use.
                kwargs: Additional keyword arguments to pass to the connector.
        """
        if connector_type.lower() == 'sqlite':
            from core.cache_storage.connectors.sqlite import SQLiteConnector
            self.cache = CacheStorageManager(SQLiteConnector(**kwargs))
        elif connector_type.lower() == 'redis':
            from core.cache_storage.connectors.redis import RedisConnector
            self.cache = CacheStorageManager(RedisConnector(**kwargs))
        elif connector_type.lower() == 'system':
            from core.cache_storage.connectors.system import SystemConnector
            self.cache = CacheStorageManager(SystemConnector(**kwargs))
        else:
            raise ValueError('Invalid connector type: {}'.format(connector_type))

    async def __async__init__(self) -> None:
        """
            Initialize the cache manager.
        """
        await self.cache.__async__init__()

    async def get(self, user_uuid: Uuid) -> User:
        """
            Retrieve a user from the cache based on the UUID.

            Args:
                user_uuid: The UUID of the user to retrieve.
            
            Returns:
                The user object if found, otherwise None.
        """
        user = await self.cache.get(str(user_uuid))
        return user
    
    async def add(self, user: User) -> User:
        """
            Add a user to the cache.

            Args:
                user: The user to be cached.
            
            Returns:
                The user object.
        """
        await self.cache.set(str(user.uuid), user)
        return user
    
    async def delete(self, user_uuid: Uuid) -> None:
        """
            Remove a user from the cache based on the UUID.

            Args:
                user_uuid: The UUID of the user to remove.
            
            Returns:
                True if the user was removed, otherwise False.
        """
        await self.cache.delete(str(user_uuid))
    
    async def clear_expired(self) -> None:
        """
            Clear expired cache entries from the storage system.

            Returns:
                True if the cache was cleared.
        """
        await self.cache.clear_expired()
    
    async def update(self, user: User) -> User:
        """
            Update a user in the cache.

            Args:
                user: The user to update.
            
            Returns:
                The updated user object.
        """
        await self.delete(str(user.uuid))
        await self.add(user)
        return user