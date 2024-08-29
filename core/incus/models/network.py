# incus_sdk/models/network.py

from .base import BaseModel
from typing import List, Optional, Dict, Any

class NetworkConfig(BaseModel):
    config: Dict[str, Any]
    description: Optional[str]
    name: str
    type: str
    used_by: List[str]

class Network(BaseModel):
    name: str
    description: Optional[str]
    type: str
    config: Dict[str, Any]
    managed: bool
    used_by: List[str]

    async def push(self):
        """Update the network configuration on the server."""
        updated_data = await self._client.networks.update(self.name, self.to_dict())
        self.__init__(**updated_data)

    async def delete(self):
        """Delete the network from the server."""
        await self._client.networks.delete(self.name)