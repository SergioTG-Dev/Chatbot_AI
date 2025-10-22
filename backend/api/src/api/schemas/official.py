from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class OfficialBase(BaseModel):
    full_name: str
    description: Optional[str] = None
    department_id: UUID
    role: str = 'funcionario'

class OfficialCreate(OfficialBase):
    pass

class OfficialCreateWithAuth(OfficialBase):
    email: EmailStr
    password: str

class OfficialUpdate(BaseModel):
    full_name: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[UUID] = None
    role: Optional[str] = None

class Official(OfficialBase):
    id: UUID

    class Config:
        from_attributes = True