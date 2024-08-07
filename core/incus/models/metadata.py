from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Union, Dict
from datetime import datetime

class OperationMetadata(BaseModel):
    id: str
    class_: str = Field(..., alias='class')
    created_at: datetime
    updated_at: datetime
    status: str
    status_code: int
    resources: Dict[str, List[str]]
    metadata: Dict[str, Dict[str, str]]
    may_cancel: bool
    err: str