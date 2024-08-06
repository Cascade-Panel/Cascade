""" This module contains the MemcachedConnector class. """

import aiomcache
import pickle
from core.cache_storage.connectors.base import BaseConnector

class MemcachedConnector(BaseConnector):
    """
    A caching manager that stores cache in a Memcached database.

    Args:
        memcached_url (str): The URL to connect to the Memcached server.
    """
    def __init__(self, memcached_url: str):
        self.memcached_url = memcached_url
        self.client = None

    async def __async__init__(self, instance_name: str) -> None:
        """
        Initializes the Memcached connection.
        """
        # Create a Memcached client
        self.client = aiomcache.Client(self.memcached_url)

    async def get(self, instance_name: str, key: str):
        """
        Retrieve a value from the cache based on the key.

        Args:
            key (str): The key of the cache.

        Returns:
            The cached value if found, otherwise None.
        """
        instance_key = f"{instance_name}:{key}".encode()
        value = await self.client.get(instance_key)
        if value:
            return pickle.loads(value)
        return None

    async def set(self, instance_name: str, key: str, value, ttl=None) -> None:
        """
        Add a value to the cache.

        Args:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        instance_key = f"{instance_name}:{key}".encode()
        value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        if ttl:
            await self.client.set(instance_key, value, exptime=ttl)
        else:
            await self.client.set(instance_key, value)

    async def clear_expired(self, instance_name: str) -> None:
        """
        Clear expired cache entries from the Memcached database.
        """
        # Memcached handles expired keys automatically; this method is a placeholder.
        pass

    async def delete(self, instance_name: str, key: str) -> None:
        """
        Remove a value from the cache based on the key.

        Args:
            key (str): The key of the cache.
        """
        instance_key = f"{instance_name}:{key}".encode()
        await self.client.delete(instance_key)
