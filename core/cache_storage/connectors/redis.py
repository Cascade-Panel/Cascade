import aioredis
import pickle
from core.cache_storage.connectors.base import BaseConnector

class RedisConnector(BaseConnector):
    """
    A caching manager that stores cache in a Redis database.

    Args:
        redis_url (str): The URL to connect to the Redis database.
    """
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.conn = None

    async def __async__init__(self, instance_name: str) -> None:
        """
        Initializes the Redis connection.
        """
        self.conn = await aioredis.create_redis_pool(self.redis_url)

    async def get(self, instance_name: str, key: str):
        """
        Retrieve a value from the cache based on the key.

        Args:
            key (str): The key of the cache.

        Returns:
            The cached value if found, otherwise None.
        """
        instance_key = f"{instance_name}:{key}"
        value = await self.conn.get(instance_key)
        if value:
            return pickle.loads(value)
        return None

    async def set(self, instance_name: str, key: str, value, ttl=None):
        """
        Add a value to the cache.

        Args:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        instance_key = f"{instance_name}:{key}"
        value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        if ttl:
            await self.conn.setex(instance_key, ttl, value)
        else:
            await self.conn.set(instance_key, value)

    async def clear_expired(self, instance_name: str) -> None:
        """
        Clear expired cache entries from the Redis database.
        This is typically managed automatically by Redis, so this method is just a placeholder.
        """
        # Redis automatically handles expired keys, but you can run a manual expiration check if needed.
        pass

    async def delete(self, instance_name: str, key: str) -> None:
        """
        Remove a value from the cache based on the key.

        Args:
            key (str): The key of the cache.
        """
        instance_key = f"{instance_name}:{key}"
        await self.conn.delete(instance_key)
