# incus_sdk/api/base.py

from typing import Any

class BaseAPI:
    def __init__(self, client):
        """
        Initialize the Base API.

        Args:
            client: The IncusClient instance.
        """
        self._client = client

    async def _get(self, endpoint: str, **kwargs: Any) -> Any:
        """
        Perform a GET request.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The JSON response from the API.
        """
        return await self._client.request("GET", endpoint, **kwargs)

    async def _post(self, endpoint: str, **kwargs: Any) -> Any:
        """
        Perform a POST request.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The JSON response from the API.
        """
        return await self._client.request("POST", endpoint, **kwargs)

    async def _put(self, endpoint: str, **kwargs: Any) -> Any:
        """
        Perform a PUT request.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The JSON response from the API.
        """
        return await self._client.request("PUT", endpoint, **kwargs)

    async def _delete(self, endpoint: str, **kwargs: Any) -> Any:
        """
        Perform a DELETE request.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The JSON response from the API.
        """
        return await self._client.request("DELETE", endpoint, **kwargs)

    async def _patch(self, endpoint: str, **kwargs: Any) -> Any:
        """
        Perform a PATCH request.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The JSON response from the API.
        """
        return await self._client.request("PATCH", endpoint, **kwargs)