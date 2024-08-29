# incus_sdk/models/certificate.py

from .base import BaseModel
from typing import Optional

class Certificate(BaseModel):
    fingerprint: str
    certificate: str
    name: Optional[str]
    type: str

    async def push(self):
        """Update the certificate on the server."""
        updated_data = await self._client.certificates.update(self.fingerprint, self.to_dict())
        self.__init__(**updated_data)

    async def delete(self):
        """Delete the certificate from the server."""
        await self._client.certificates.delete(self.fingerprint)