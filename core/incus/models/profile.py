# incus_sdk/models/profile.py

from .base import BaseModel
from typing import Dict, Any, List

class Profile(BaseModel):
    name: str
    description: str
    config: Dict[str, Any]
    devices: Dict[str, Dict[str, Any]]
    used_by: List[str]

    async def push(self):
        """Update the profile on the server."""
        updated_data = await self._client.profiles.update(self.name, self.to_dict())
        self.__init__(**updated_data)

    async def delete(self):
        """Delete the profile from the server."""
        await self._client.profiles.delete(self.name)