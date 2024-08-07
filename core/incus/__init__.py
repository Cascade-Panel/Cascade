import aiohttp
from core.type_hints import Url

class Incus:
    def __init__(self, external_url: Url):
        self.external_url = external_url
        self.session = aiohttp.ClientSession()

    async def __async__init__(self) -> None:
        """
            Initialize the Incus client.
        """
        async with self.session.get(self.external_url) as response:
            if response.status != 200:
                raise Exception("Failed to initialize Incus")
            
            self.incus_versions = await response.json()['metadata']

            self.session._base_url = self.external_url.strip("/") + self.incus_versions[-1]

    async def enviroment(self, target: str, ) -> str:
        """
            Get the enviroment of the Incus server.
        """
        async with self.session.get("/") as response:
            return await response.json()['enviroment']

    async def __aenter__(self):
        return self