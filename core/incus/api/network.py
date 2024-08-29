# incus_sdk/api/network.py

from ..models.network import Network
from .base import BaseAPI
from typing import List

class NetworkAPI(BaseAPI):
    async def create(self, name: str, config: dict) -> Network:
        """
        Create a new network.

        Args:
            name (str): The name of the network.
            config (dict): The network configuration.

        Returns:
            Network: The created network.
        """
        data = await self._client.request("POST", "/1.0/networks", json={"name": name, **config})
        network = Network(**data)
        network.set_client(self._client)
        return network

    async def get(self, name: str) -> Network:
        """
        Get a network by name.

        Args:
            name (str): The name of the network.

        Returns:
            Network: The retrieved network.
        """
        data = await self._client.request("GET", f"/1.0/networks/{name}")
        network = Network(**data)
        network.set_client(self._client)
        return network

    async def list(self) -> List[Network]:
        """
        List all networks.

        Returns:
            List[Network]: A list of all networks.
        """
        data = await self._client.request("GET", "/1.0/networks")
        return [Network(**network_data).set_client(self._client) for network_data in data]

    async def update(self, name: str, data: dict) -> dict:
        """
        Update a network.

        Args:
            name (str): The name of the network to update.
            data (dict): The updated network data.

        Returns:
            dict: The updated network data.
        """
        return await self._client.request("PUT", f"/1.0/networks/{name}", json=data)

    async def delete(self, name: str):
        """
        Delete a network.

        Args:
            name (str): The name of the network to delete.
        """
        await self._client.request("DELETE", f"/1.0/networks/{name}")