from pydantic import BaseModel
from uuid import UUID
from typing import Union, Dict
from datetime import datetime

class OperationMetadata(BaseModel):
    ## the id is given as a string convert it to uuid
    id: UUID
    _class: str["task" | "websocket" | "token"]
    created_at: datetime
    updated_at: datetime
    status: str
    status_code: int
    resources: Dict
    metadata: Dict
    may_cancel: bool
    err: str