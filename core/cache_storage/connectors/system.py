""" This module contains the SystemConnector class. """

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

    async def __async__init__(self, instance_name: str) -> None:
        """
        Initialize the caching object.
        """
        self.store[instance_name] = {}

    async def get(self, instance_name: str, key: str):
        """
        Retrieve a value from the cache based on the key.

        Args:
            key (str): The key of the cache.

        Returns:
            The cached value if found, otherwise None.
        """
        raw_store = self.store[instance_name].get(key)
        if not raw_store:
            return None
        return pickle.loads(raw_store)['value']

    async def set(self, instance_name: str, key: str, value, ttl=None) -> None:
        """
        Add a value to the cache.

        Args:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        data = {"ttl": ttl, "value": value}
        self.store[instance_name][key] = pickle.dumps(data)

    async def clear_expired(self, instance_name: str) -> None:
        """
        Clear expired cache entries from the SQLite database.
        """
        for item in list(self.store[instance_name].keys()):
            raw_store = self.store[instance_name].get(item)
            if not raw_store:
                continue
            data = pickle.loads(raw_store)
            if data['ttl'] is not None and data['ttl'] < datetime.datetime.now().timestamp():
                del self.store[instance_name][item]

    async def delete(self, instance_name: str, key: str) -> None:
        """
        Remove a value from the cache based on the key.

        Args:
            key (str): The key of the cache.
        """
        if key in self.store[instance_name]:
            del self.store[instance_name][key]

    async def get_all_values(self, instance_name: str) -> list:
        """
        Retrieve all values from the cache.

        Returns:
            list: All values in the cache.
        """
        return self.store[instance_name].values()