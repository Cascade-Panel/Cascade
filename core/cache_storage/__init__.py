""" The main, public interface to the caching system. """
from core.cache_storage.connectors.base import BaseConnector

class CacheStorageManager:
    """
        The main, public interface to the caching system.

        Attributes:
            connector: The storage connector (e.g., SQLiteConnector, RedisConnector).
    """
    def __init__(self, connector):
        self.connector = connector

    async def get(self, key: str) -> BaseConnector:
        return await self.connector.get(key)

    async def set(self, key: str, value: str, ttl=None) -> None:
        await self.connector.set(key, value, ttl)

    async def delete(self, key: str) -> None:
        await self.connector.delete(key)
