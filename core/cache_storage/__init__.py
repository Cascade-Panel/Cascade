""" The main, public interface to the caching system. """
from core.cache_storage.connectors.base import BaseConnector

class CacheStorageManager:
    """
    The main, public interface to the caching system.

    Attributes:
        connector: The storage connector (e.g., SQLiteConnector, RedisConnector).
    """
    def __init__(self, connector: BaseConnector, instance_name: str):
        self.connector = connector
        self.instance_name = instance_name

    async def __async__init__(self) -> None:
        """
        Initialize the cache manager.
        """
        await self.connector.__async__init__(self.instance_name)

    async def get(self, key: str):
        return await self.connector.get(self.instance_name, key)

    async def set(self, key: str, value: str, ttl=None) -> None:
        await self.connector.set(self.instance_name, key, value, ttl)

    async def clear_expired(self) -> None:
        await self.connector.clear_expired(self.instance_name)

    async def delete(self, key: str) -> None:
        await self.connector.delete(self.instance_name, key)

    async def get_all_values(self) -> list:
        return await self.connector.get_all_values(self.instance_name)