from pydantic import BaseModel, Field
from core.incus.metadata import OperationMetadata

class StandardResponse(BaseModel):
    type: str
    status: str
    status_code: int = Field(200, const=True)
    metadata: dict = None

class BackgroundOperationResponse(BaseModel):
    type: str
    status: str
    status_code: int = Field(202, const=True)
    operation: str
    metadata: OperationMetadata

class ErrorResponse(BaseModel):
    type: str = "error"
    error: str
    error_code: int = Field(..., const=True, gt=399, lt=600)
    metadata: dict = None
