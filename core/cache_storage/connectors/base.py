""" The base connector for all storage connectors. """

class BaseConnector:
    """
    The base class for all storage connectors.

    Attributes:
        connection: The connection to the storage system.
    """
    def __init__(self, connection):
        self.connection = connection

    async def get(self, key) -> str | dict | list | tuple | object | callable:
        """
        Retrieve a value from the cache based on the key.

        Attributes:
            key (str): The key of the cache.
        """
        raise NotImplementedError

    async def set(self, key, value, ttl=None) -> None:
        """
        Add a value to the cache.

        Attributes:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        raise NotImplementedError

    async def clear_expired(self) -> None:
        """
        Clear expired cache entries from the storage system

        Attributes:
            key (str): The key of the cache.
        """
        raise NotImplementedError

    async def delete(self, key) -> None:
        """
        Remove a value from the cache based on the key.

        Attributes:
            key (str): The key of the cache.
        """
        raise NotImplementedError