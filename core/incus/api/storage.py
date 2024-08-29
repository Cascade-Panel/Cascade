# incus_sdk/api/storage.py

from ..models.storage import StoragePool, StorageVolume
from .base import BaseAPI
from typing import List

class StorageAPI(BaseAPI):
    async def create_pool(self, name: str, driver: str, config: dict) -> StoragePool:
        """
        Create a new storage pool.

        Args:
            name (str): The name of the storage pool.
            driver (str): The driver for the storage pool.
            config (dict): The storage pool configuration.

        Returns:
            StoragePool: The created storage pool.
        """
        data = await self._client.request("POST", "/1.0/storage-pools", json={"name": name, "driver": driver, **config})
        pool = StoragePool(**data)
        pool.set_client(self._client)
        return pool

    async def get_pool(self, name: str) -> StoragePool:
        """
        Get a storage pool by name.

        Args:
            name (str): The name of the storage pool.

        Returns:
            StoragePool: The retrieved storage pool.
        """
        data = await self._client.request("GET", f"/1.0/storage-pools/{name}")
        pool = StoragePool(**data)
        pool.set_client(self._client)
        return pool

    async def list_pools(self) -> List[StoragePool]:
        """
        List all storage pools.

        Returns:
            List[StoragePool]: A list of all storage pools.
        """
        data = await self._client.request("GET", "/1.0/storage-pools")
        return [StoragePool(**pool_data).set_client(self._client) for pool_data in data]

    async def update_pool(self, name: str, data: dict) -> dict:
        """
        Update a storage pool.

        Args:
            name (str): The name of the storage pool to update.
            data (dict): The updated storage pool data.

        Returns:
            dict: The updated storage pool data.
        """
        return await self._client.request("PUT", f"/1.0/storage-pools/{name}", json=data)

    async def delete_pool(self, name: str):
        """
        Delete a storage pool.

        Args:
            name (str): The name of the storage pool to delete.
        """
        await self._client.request("DELETE", f"/1.0/storage-pools/{name}")

    async def create_volume(self, pool: str, name: str, config: dict) -> StorageVolume:
        """
        Create a new storage volume.

        Args:
            pool (str): The name of the storage pool.
            name (str): The name of the storage volume.
            config (dict): The storage volume configuration.

        Returns:
            StorageVolume: The created storage volume.
        """
        data = await self._client.request("POST", f"/1.0/storage-pools/{pool}/volumes", json={"name": name, **config})
        volume = StorageVolume(**data)
        volume.set_client(self._client)
        return volume

    async def get_volume(self, pool: str, volume_type: str, name: str) -> StorageVolume:
        """
        Get a storage volume by name.

        Args:
            pool (str): The name of the storage pool.
            volume_type (str): The type of the storage volume.
            name (str): The name of the storage volume.

        Returns:
            StorageVolume: The retrieved storage volume.
        """
        data = await self._client.request("GET", f"/1.0/storage-pools/{pool}/volumes/{volume_type}/{name}")
        volume = StorageVolume(**data)
        volume.set_client(self._client)
        return volume

    async def list_volumes(self, pool: str) -> List[StorageVolume]:
        """
        List all storage volumes in a pool.

        Args:
            pool (str): The name of the storage pool.

        Returns:
            List[StorageVolume]: A list of all storage volumes in the pool.
        """
        data = await self._client.request("GET", f"/1.0/storage-pools/{pool}/volumes")
        return [StorageVolume(**volume_data).set_client(self._client) for volume_data in data]

    async def update_volume(self, pool: str, volume_type: str, name: str, data: dict) -> dict:
        """
        Update a storage volume.

        Args:
            pool (str): The name of the storage pool.
            volume_type (str): The type of the storage volume.
            name (str): The name of the storage volume to update.
            data (dict): The updated storage volume data.

        Returns:
            dict: The updated storage volume data.
        """
        return await self._client.request("PUT", f"/1.0/storage-pools/{pool}/volumes/{volume_type}/{name}", json=data)

    async def delete_volume(self, pool: str, volume_type: str, name: str):
        """
        Delete a storage volume.

        Args:
            pool (str): The name of the storage pool.
            volume_type (str): The type of the storage volume.
            name (str): The name of the storage volume to delete.
        """
        await self._client.request("DELETE", f"/1.0/storage-pools/{pool}/volumes/{volume_type}/{name}")