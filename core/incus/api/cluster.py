# incus_sdk/api/cluster.py

from ..models.cluster import Cluster, ClusterMember
from .base import BaseAPI

class ClusterAPI(BaseAPI):
    async def get(self) -> Cluster:
        """
        Get the current cluster configuration.

        Returns:
            Cluster: The current cluster configuration.
        """
        data = await self._client.request("GET", "/1.0/cluster")
        cluster = Cluster(**data)
        cluster.set_client(self._client)
        return cluster

    async def update(self, data: dict) -> dict:
        """
        Update the cluster configuration.

        Args:
            data (dict): The updated cluster configuration data.

        Returns:
            dict: The updated cluster configuration.
        """
        return await self._client.request("PUT", "/1.0/cluster", json=data)

    async def leave(self):
        """
        Leave the cluster.
        """
        await self._client.request("POST", "/1.0/cluster/leave")