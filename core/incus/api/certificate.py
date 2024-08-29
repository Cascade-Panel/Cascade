# incus_sdk/api/certificate.py

from ..models.certificate import Certificate
from .base import BaseAPI
from typing import List, Optional

class CertificateAPI(BaseAPI):
    async def create(self, certificate: str, name: Optional[str] = None, type: str = "client") -> Certificate:
        """
        Add a new certificate.

        Args:
            certificate (str): The certificate data.
            name (Optional[str]): A name for the certificate.
            type (str): The type of certificate (default: "client").

        Returns:
            Certificate: The added certificate.
        """
        data = await self._client.request("POST", "/1.0/certificates", json={
            "certificate": certificate,
            "name": name,
            "type": type
        })
        cert = Certificate(**data)
        cert.set_client(self._client)
        return cert

    async def get(self, fingerprint: str) -> Certificate:
        """
        Get a certificate by fingerprint.

        Args:
            fingerprint (str): The fingerprint of the certificate.

        Returns:
            Certificate: The retrieved certificate.
        """
        data = await self._client.request("GET", f"/1.0/certificates/{fingerprint}")
        cert = Certificate(**data)
        cert.set_client(self._client)
        return cert

    async def list(self) -> List[Certificate]:
        """
        List all certificates.

        Returns:
            List[Certificate]: A list of all certificates.
        """
        data = await self._client.request("GET", "/1.0/certificates")
        return [Certificate(**cert_data).set_client(self._client) for cert_data in data]

    async def update(self, fingerprint: str, data: dict) -> dict:
        """
        Update a certificate.

        Args:
            fingerprint (str): The fingerprint of the certificate to update.
            data (dict): The updated certificate data.

        Returns:
            dict: The updated certificate data.
        """
        return await self._client.request("PUT", f"/1.0/certificates/{fingerprint}", json=data)

    async def delete(self, fingerprint: str):
        """
        Delete a certificate.

        Args:
            fingerprint (str): The fingerprint of the certificate to delete.
        """
        await self._client.request("DELETE", f"/1.0/certificates/{fingerprint}")