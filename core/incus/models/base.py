# incus_sdk/models/base.py

from pydantic import BaseModel as PydanticBaseModel
from typing import Any, Dict

class BaseModel(PydanticBaseModel):
    """Base model for all Incus API models."""

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._client = None

    def set_client(self, client):
        """Set the API client for this model instance."""
        self._client = client

    async def push(self):
        """Update the model on the server."""
        if not self._client:
            raise ValueError("API client not set. Use set_client() before calling push().")
        # Implement the update logic here
        raise NotImplementedError("push() method must be implemented in subclasses")

    async def delete(self):
        """Delete the model on the server."""
        if not self._client:
            raise ValueError("API client not set. Use set_client() before calling delete().")
        # Implement the delete logic here
        raise NotImplementedError("delete() method must be implemented in subclasses")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return self.dict(exclude_unset=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create a model instance from a dictionary."""
        return cls(**data)