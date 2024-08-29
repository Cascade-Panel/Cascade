# incus_sdk/client.py

import aiohttp
from typing import Optional
from .exceptions import IncusAPIError
from .api.instance import InstanceAPI
from .api.cluster import ClusterAPI
from .api.certificate import CertificateAPI
from .api.server import ServerAPI
from .api.network import NetworkAPI
from .api.profile import ProfileAPI
from .api.storage import StorageAPI

class IncusClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the Incus API client.

        Args:
            base_url (str): The base URL of the Incus API.
            api_key (Optional[str]): The API key for authentication.
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Initialize API endpoints
        self.instances = InstanceAPI(self)
        self.clusters = ClusterAPI(self)
        self.certificates = CertificateAPI(self)
        self.servers = ServerAPI(self)
        self.networks = NetworkAPI(self)
        self.profiles = ProfileAPI(self)
        self.storage = StorageAPI(self)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """Establish the aiohttp client session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers=self._get_headers())

    async def close(self):
        """Close the aiohttp client session."""
        if self.session and not self.session.closed:
            await self.session.close()

    def _get_headers(self):
        """Get the headers for API requests."""
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def request(self, method: str, endpoint: str, **kwargs):
        """
        Make an HTTP request to the Incus API.

        Args:
            method (str): The HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint (str): The API endpoint.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            IncusAPIError: If the API returns an error.
        """
        if not self.session or self.session.closed:
            await self.connect()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with self.session.request(method, url, **kwargs) as response:
            if response.status >= 400:
                error_message = await response.text()
                raise IncusAPIError(f"API request failed: {response.status} {response.reason}\n{error_message}")
            return await response.json()