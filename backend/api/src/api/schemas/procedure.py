from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProcedureBase(BaseModel):
    name: str
    description: Optional[str] = None
    department_id: UUID
    duration_minutes: int = 30

class ProcedureCreate(ProcedureBase):
    pass

class ProcedureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None

class Procedure(ProcedureBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True