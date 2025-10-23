from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None

class Department(DepartmentBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True