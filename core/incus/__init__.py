import aiohttp
from typing import Optional, Dict, Any
from pydantic import ValidationError
from models import Server, ServerPut, StandardResponse, ErrorResponse
from core.type_hints import Url

class Incus:
    def __init__(self, external_url: Url):
        self.external_url = external_url
        self.session = aiohttp.ClientSession()
        self.base_url = external_url.strip("/")

    async def __aenter__(self):
        await self.__async_init()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def __async_init(self) -> None:
        """
        Initialize the Incus client by retrieving the supported API versions
        and setting the base URL to the latest version.
        """
        async with self.session.get(self.base_url) as response:
            if response.status != 200:
                raise Exception(f"Failed to initialize Incus: {response.status}")
            
            data = await response.json()
            self.incus_versions = data.get('metadata', [])
            if not self.incus_versions:
                raise Exception("No API versions found")
            
            latest_version = self.incus_versions[-1]
            self.base_url += latest_version

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Generalized request method to handle GET, PATCH, PUT requests.
        """
        url = f"{self.base_url}{endpoint}"
        async with getattr(self.session, method)(url, **kwargs) as response:
            response_json = await response.json()
            if response.status == 200:
                try:
                    return StandardResponse(**response_json)
                except ValidationError as e:
                    raise Exception(f"Response validation failed: {e}")
            elif 400 <= response.status < 500:
                try:
                    return ErrorResponse(**response_json)
                except ValidationError as e:
                    raise Exception(f"Error response validation failed: {e}")
            else:
                raise Exception(f"Unexpected status code: {response.status}")

    async def environment(self, target: str, project: Optional[str] = None) -> Server:
        """
        Get the environment of the Incus server.
        """
        params = {'target': target}
        if project:
            params['project'] = project
        
        response = await self._request('get', "/1.0", params=params)
        return Server(**response.metadata)

    async def update_server_configuration(self, target: str, config: ServerPut, patch: bool = False) -> StandardResponse:
        """
        Update the server configuration.
        """
        params = {'target': target}
        method = 'patch' if patch else 'put'
        response = await self._request(method, "/1.0", json=config.dict(), params=params)
        return response