# incus_sdk/api/instance.py

from ..models.instance import Instance, InstanceStatus
from .base import BaseAPI
from typing import List, Dict, Any, Optional

class InstanceAPI(BaseAPI):
    async def create(self, name: str, config: dict) -> Instance:
        """
        Create a new instance.

        Args:
            name (str): The name of the instance.
            config (dict): The instance configuration.

        Returns:
            Instance: The created instance.
        """
        data = await self._post("/1.0/instances", json={"name": name, **config})
        instance = Instance(**data)
        instance.set_client(self._client)
        return instance

    async def get(self, name: str) -> Instance:
        """
        Get an instance by name.

        Args:
            name (str): The name of the instance.

        Returns:
            Instance: The retrieved instance.
        """
        data = await self._get(f"/1.0/instances/{name}")
        instance = Instance(**data)
        instance.set_client(self._client)
        return instance

    async def list(self) -> List[Instance]:
        """
        List all instances.

        Returns:
            List[Instance]: A list of all instances.
        """
        data = await self._get("/1.0/instances")
        return [Instance(**instance_data).set_client(self._client) for instance_data in data]

    async def update(self, name: str, data: dict) -> dict:
        """
        Update an instance.

        Args:
            name (str): The name of the instance to update.
            data (dict): The updated instance data.

        Returns:
            dict: The updated instance data.
        """
        return await self._put(f"/1.0/instances/{name}", json=data)

    async def delete(self, name: str):
        """
        Delete an instance.

        Args:
            name (str): The name of the instance to delete.
        """
        await self._delete(f"/1.0/instances/{name}")

    async def start(self, name: str):
        """
        Start an instance.

        Args:
            name (str): The name of the instance to start.
        """
        await self._put(f"/1.0/instances/{name}/state", json={"action": "start"})

    async def stop(self, name: str):
        """
        Stop an instance.

        Args:
            name (str): The name of the instance to stop.
        """
        await self._put(f"/1.0/instances/{name}/state", json={"action": "stop"})

    async def restart(self, name: str):
        """
        Restart an instance.

        Args:
            name (str): The name of the instance to restart.
        """
        await self._put(f"/1.0/instances/{name}/state", json={"action": "restart"})

    async def freeze(self, name: str):
        """
        Freeze an instance.

        Args:
            name (str): The name of the instance to freeze.
        """
        await self._put(f"/1.0/instances/{name}/state", json={"action": "freeze"})

    async def unfreeze(self, name: str):
        """
        Unfreeze an instance.

        Args:
            name (str): The name of the instance to unfreeze.
        """
        await self._put(f"/1.0/instances/{name}/state", json={"action": "unfreeze"})

    async def get_state(self, name: str) -> Dict[str, Any]:
        """
        Get the current state of an instance.

        Args:
            name (str): The name of the instance.

        Returns:
            Dict[str, Any]: The current state of the instance.
        """
        return await self._get(f"/1.0/instances/{name}/state")

    async def execute(self, name: str, command: List[str], environment: Optional[Dict[str, str]] = None):
        """
        Execute a command in an instance.

        Args:
            name (str): The name of the instance.
            command (List[str]): The command to execute.
            environment (Optional[Dict[str, str]]): Environment variables for the command.

        Returns:
            Dict[str, Any]: The result of the command execution.
        """
        payload = {
            "command": command,
            "environment": environment or {},
            "wait-for-websocket": False,
            "record-output": True,
        }
        return await self._post(f"/1.0/instances/{name}/exec", json=payload)

    async def get_files(self, name: str, path: str) -> bytes:
        """
        Get files from an instance.

        Args:
            name (str): The name of the instance.
            path (str): The path of the file or directory to retrieve.

        Returns:
            bytes: The content of the file or directory.
        """
        response = await self._get(f"/1.0/instances/{name}/files", params={"path": path})
        return response.content

    async def put_files(self, name: str, path: str, content: bytes):
        """
        Put files into an instance.

        Args:
            name (str): The name of the instance.
            path (str): The path where to put the file.
            content (bytes): The content of the file.
        """
        await self._post(f"/1.0/instances/{name}/files", params={"path": path}, data=content)