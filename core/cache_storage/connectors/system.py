import aiosqlite
import pickle
import datetime
from core.cache_storage.connectors.base import BaseConnector

class SystemConnector(BaseConnector):
    """
    A caching manager that stores cache in system memory.
    """
    def __init__(self):
        """
        Initializes the caching object.
        """
        self.store = {}

    async def __async__init__(self) -> None:
        """
        Initialize the caching object.
        """
        pass

    async def get(self, key: str) -> str | dict | list | tuple | object | callable:
        """
        Retrieve a value from the cache based on the key.

        Args:
            key (str): The key of the cache.

        Returns:
            The cached value if found, otherwise None.
        """
        raw_store = self.store.get(key)
        if not raw_store:
            return None
        return pickle.loads(raw_store)['value']

    async def set(self, key: str, value: str | dict | list | tuple | object | callable, ttl=None) -> None:
        """
        Add a value to the cache.

        Args:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        data = {"ttl": ttl, "value": value}
        self.store[key] = pickle.dumps(data)

    async def clear_expired(self) -> None:
        """
        Clear expired cache entries from the SQLite database.
        """
        for item in list(self.store.keys()):
            raw_store = self.store.get(item)
            if not raw_store:
                continue
            data = pickle.loads(raw_store)
            if data['ttl'] is not None and data['ttl'] < datetime.datetime.now().timestamp():
                del self.store[item]

    async def delete(self, key: str) -> None:
        """
        Remove a value from the cache based on the key.

        Args:
            key (str): The key of the cache.
        """
        if key in self.store:
            del self.store[key]
