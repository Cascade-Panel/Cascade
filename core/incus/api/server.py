# incus_sdk/api/server.py

from ..models.server import Server
from .base import BaseAPI
from typing import List

class ServerAPI(BaseAPI):
    async def get(self, server_name: str = "") -> Server:
        """
        Get server information.

        Args:
            server_name (str): The name of the server (empty for local server).

        Returns:
            Server: The server information.
        """
        data = await self._client.request("GET", f"/1.0/servers/{server_name}")
        server = Server(**data)
        server.set_client(self._client)
        return server

    async def list(self) -> List[Server]:
        """
        List all servers in the cluster.

        Returns:
            List[Server]: A list of all servers.
        """
        data = await self._client.request("GET", "/1.0/servers")
        return [Server(**server_data).set_client(self._client) for server_data in data]

    async def update(self, server_name: str, data: dict) -> dict:
        """
        Update server configuration.

        Args:
            server_name (str): The name of the server to update.
            data (dict): The updated server configuration.

        Returns:
            dict: The updated server data.
        """
        return await self._client.request("PUT", f"/1.0/servers/{server_name}", json=data)