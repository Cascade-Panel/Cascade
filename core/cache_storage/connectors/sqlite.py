""" This module contains the SQLiteConnector class. """

import aiosqlite
import pickle
import datetime
from core.cache_storage.connectors.base import BaseConnector

class SQLiteConnector(BaseConnector):
    """
    A caching manager that stores cache in a SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def __async__init__(self, instance_name: str) -> None:
        """
        Initializes the caching object and creates the cache table if it doesn't exist.
        """
        table_name = f"cache_{instance_name}"
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    ttl INTEGER,
                    cached_at INTEGER DEFAULT (strftime('%s', 'now'))
                )
            ''')
            await db.commit()

    async def get(self, instance_name: str, key: str):
        """
        Retrieve a value from the cache based on the key.

        Args:
            key (str): The key of the cache.

        Returns:
            The cached value if found, otherwise None.
        """
        table_name = f"cache_{instance_name}"
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f'SELECT value FROM {table_name} WHERE key = ?', (key,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return pickle.loads(row[0])
                return None

    async def set(self, instance_name: str, key: str, value, ttl=None) -> None:
        """
        Add a value to the cache.

        Args:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        table_name = f"cache_{instance_name}"
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f'INSERT OR REPLACE INTO {table_name} (key, value, ttl) VALUES (?, ?, ?)',
                (key, pickle.dumps(value, pickle.HIGHEST_PROTOCOL), ttl)
            )
            await db.commit()

    async def clear_expired(self, instance_name: str) -> None:
        """
        Clear expired cache entries from the SQLite database.
        """
        table_name = f"cache_{instance_name}"
        async with aiosqlite.connect(self.db_path) as db:
            current_time = int(datetime.datetime.now().timestamp())
            await db.execute(f'DELETE FROM {table_name} WHERE ttl IS NOT NULL AND (cached_at + ttl) < ?', (current_time,))
            await db.commit()

    async def delete(self, instance_name: str, key: str) -> None:
        """
        Remove a value from the cache based on the key.

        Args:
            key (str): The key of the cache.
        """
        table_name = f"cache_{instance_name}"
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'DELETE FROM {table_name} WHERE key = ?', (key,))
            await db.commit()

    async def get_all_values(self, instance_name: str) -> list:
        """
        Retrieve all values from the cache.

        Returns:
            list: All values in the cache.
        """
        table_name = f"cache_{instance_name}"
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f'SELECT value FROM {table_name}') as cursor:
                rows = await cursor.fetchall()
                return [pickle.loads(row[0]) for row in rows] if rows else []