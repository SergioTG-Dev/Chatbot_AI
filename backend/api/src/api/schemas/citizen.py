from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class CitizenBase(BaseModel):
    dni: str
    first_name: str
    last_name: str
    email: EmailStr

class CitizenCreate(CitizenBase):
    pass

class CitizenUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class Citizen(CitizenBase):
    id: UUID
    created_at: str

    class Config:
        from_attributes = True