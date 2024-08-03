import aioredis
import pickle
from core.cache_storage.connectors.base import BaseConnector

class RedisConnector(BaseConnector):
    """
    A caching manager that stores cache in a Redis database.

    Attributes:
        redis_url (str): The URL to connect to the Redis database.
    """
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.conn = None

    async def async__init__(self):
        """
        Initializes the Redis connection.
        """
        self.conn = await aioredis.create_redis_pool(self.redis_url)

    async def get(self, key):
        """
        Retrieve a value from the cache based on the key.

        Attributes:
            key (str): The key of the cache.

        Returns:
            The cached value if found, otherwise None.
        """
        value = await self.conn.get(key)
        if value:
            return pickle.loads(value)
        return None

    async def set(self, key, value, ttl=None):
        """
        Add a value to the cache.

        Attributes:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        if ttl:
            await self.conn.setex(key, ttl, value)
        else:
            await self.conn.set(key, value)

    async def clear_expired(self):
        """
        Clear expired cache entries from the Redis database.
        This is typically managed automatically by Redis, so this method is just a placeholder.
        """
        # Redis automatically handles expired keys, but you can run a manual expiration check if needed.
        pass

    async def delete(self, key):
        """
        Remove a value from the cache based on the key.

        Attributes:
            key (str): The key of the cache.
        """
        await self.conn.delete(key)
