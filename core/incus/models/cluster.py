# incus_sdk/models/cluster.py

from .base import BaseModel
from typing import List, Optional

class ClusterMember(BaseModel):
    server_name: str
    url: str
    database: bool
    status: str
    message: Optional[str]

class Cluster(BaseModel):
    cluster_name: Optional[str]
    enabled: bool
    member_config: List[ClusterMember]

    async def push(self):
        """Update the cluster configuration on the server."""
        updated_data = await self._client.clusters.update(self.to_dict())
        self.__init__(**updated_data)

    async def delete(self):
        """Leave the cluster."""
        await self._client.clusters.leave()