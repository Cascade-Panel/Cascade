# incus_sdk/models/instance.py

from .base import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class InstanceStatus(Enum):
    RUNNING = "Running"
    STOPPED = "Stopped"
    FROZEN = "Frozen"
    ERROR = "Error"

class Instance(BaseModel):
    architecture: str
    config: Dict[str, Any]
    devices: Dict[str, Dict[str, Any]]
    ephemeral: bool
    name: str
    description: Optional[str]
    profiles: List[str]
    stateful: bool
    status: InstanceStatus
    status_code: int
    last_used_at: str
    location: str
    type: str
    project: str

    async def push(self):
        """Update the instance on the server."""
        updated_data = await self._client.instances.update(self.name, self.to_dict())
        self.__init__(**updated_data)

    async def delete(self):
        """Delete the instance from the server."""
        await self._client.instances.delete(self.name)

    async def start(self):
        """Start the instance."""
        await self._client.instances.start(self.name)
        self.status = InstanceStatus.RUNNING

    async def stop(self):
        """Stop the instance."""
        await self._client.instances.stop(self.name)
        self.status = InstanceStatus.STOPPED

    async def restart(self):
        """Restart the instance."""
        await self._client.instances.restart(self.name)
        self.status = InstanceStatus.RUNNING

    async def freeze(self):
        """Freeze the instance."""
        await self._client.instances.freeze(self.name)
        self.status = InstanceStatus.FROZEN

    async def unfreeze(self):
        """Unfreeze the instance."""
        await self._client.instances.unfreeze(self.name)
        self.status = InstanceStatus.RUNNING

    async def get_state(self):
        """Get the current state of the instance."""
        state = await self._client.instances.get_state(self.name)
        self.status = InstanceStatus(state['status'])
        self.status_code = state['status_code']
        return state

    async def execute(self, command: List[str], environment: Optional[Dict[str, str]] = None):
        """Execute a command in the instance."""
        return await self._client.instances.execute(self.name, command, environment)

    async def get_files(self, path: str):
        """Get files from the instance."""
        return await self._client.instances.get_files(self.name, path)

    async def put_files(self, path: str, content: bytes):
        """Put files into the instance."""
        return await self._client.instances.put_files(self.name, path, content)