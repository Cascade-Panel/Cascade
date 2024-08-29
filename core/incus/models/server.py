# incus_sdk/models/server.py

from .base import BaseModel
from typing import Dict, Any

class Server(BaseModel):
    server_name: str
    config: Dict[str, Any]
    environment: Dict[str, Any]

    async def push(self):
        """Update the server configuration on the API server."""
        updated_data = await self._client.servers.update(self.server_name, self.to_dict())
        self.__init__(**updated_data)