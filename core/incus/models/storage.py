# incus_sdk/models/storage.py

from .base import BaseModel
from typing import Dict, Any, List, Optional

class StoragePool(BaseModel):
    name: str
    driver: str
    used_by: List[str]
    config: Dict[str, Any]
    description: Optional[str]
    status: str
    locations: List[str]

    async def push(self):
        """Update the storage pool on the server."""
        updated_data = await self._client.storage.update_pool(self.name, self.to_dict())
        self.__init__(**updated_data)

    async def delete(self):
        """Delete the storage pool from the server."""
        await self._client.storage.delete_pool(self.name)

class StorageVolume(BaseModel):
    type: str
    name: str
    description: Optional[str]
    config: Dict[str, Any]
    content_type: str
    used_by: List[str]

    async def push(self):
        """Update the storage volume on the server."""
        updated_data = await self._client.storage.update_volume(self.type, self.name, self.to_dict())
        self.__init__(**updated_data)

    async def delete(self):
        """Delete the storage volume from the server."""
        await self._client.storage.delete_volume(self.type, self.name)