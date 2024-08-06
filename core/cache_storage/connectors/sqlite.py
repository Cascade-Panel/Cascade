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

    async def __async__init__(self) -> None:
        """
        Initializes the caching object and creates the cache table if it doesn't exist.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    ttl INTEGER,
                    cached_at INTEGER DEFAULT (strftime('%s', 'now'))
                )
            ''')
            await db.commit()

    async def get(self, key: str) -> str | dict | list | tuple | object | callable:
        """
        Retrieve a value from the cache based on the key.

        Args:
            key (str): The key of the cache.

        Returns:
            The cached value if found, otherwise None.
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT value FROM cache WHERE key = ?', (key,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return pickle.loads(row[0])
                return None

    async def set(self, key: str, value: str | dict | list | tuple | object | callable, ttl=None) -> None:
        """
        Add a value to the cache.

        Args:
            key (str): The key of the cache.
            value: The value to be cached.
            ttl (int, optional): The time-to-live in seconds. Defaults to None.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT OR REPLACE INTO cache (key, value, ttl) VALUES (?, ?, ?)',
                (key, pickle.dumps(value, pickle.HIGHEST_PROTOCOL), ttl)
            )
            await db.commit()

    async def clear_expired(self) -> None:
        """
        Clear expired cache entries from the SQLite database.
        """
        async with aiosqlite.connect(self.db_path) as db:
            current_time = int(datetime.datetime.now().timestamp())
            await db.execute('DELETE FROM cache WHERE ttl IS NOT NULL AND (cached_at + ttl) < ?', (current_time,))
            await db.commit()

    async def delete(self, key: str) -> None:
        """
        Remove a value from the cache based on the key.

        Args:
            key (str): The key of the cache.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM cache WHERE key = ?', (key,))
            await db.commit()
