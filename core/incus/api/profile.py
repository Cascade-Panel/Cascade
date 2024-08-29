# incus_sdk/api/profile.py

from ..models.profile import Profile
from .base import BaseAPI
from typing import List

class ProfileAPI(BaseAPI):
    async def create(self, name: str, config: dict) -> Profile:
        """
        Create a new profile.

        Args:
            name (str): The name of the profile.
            config (dict): The profile configuration.

        Returns:
            Profile: The created profile.
        """
        data = await self._client.request("POST", "/1.0/profiles", json={"name": name, **config})
        profile = Profile(**data)
        profile.set_client(self._client)
        return profile

    async def get(self, name: str) -> Profile:
        """
        Get a profile by name.

        Args:
            name (str): The name of the profile.

        Returns:
            Profile: The retrieved profile.
        """
        data = await self._client.request("GET", f"/1.0/profiles/{name}")
        profile = Profile(**data)
        profile.set_client(self._client)
        return profile

    async def list(self) -> List[Profile]:
        """
        List all profiles.

        Returns:
            List[Profile]: A list of all profiles.
        """
        data = await self._client.request("GET", "/1.0/profiles")
        return [Profile(**profile_data).set_client(self._client) for profile_data in data]

    async def update(self, name: str, data: dict) -> dict:
        """
        Update a profile.

        Args:
            name (str): The name of the profile to update.
            data (dict): The updated profile data.

        Returns:
            dict: The updated profile data.
        """
        return await self._client.request("PUT", f"/1.0/profiles/{name}", json=data)

    async def delete(self, name: str):
        """
        Delete a profile.

        Args:
            name (str): The name of the profile to delete.
        """
        await self._client.request("DELETE", f"/1.0/profiles/{name}")