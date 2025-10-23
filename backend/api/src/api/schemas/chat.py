from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    session_id: UUID
    sender_id: UUID
    sender_type: str # 'citizen' or 'official'

class Message(MessageBase):
    id: UUID
    session_id: UUID
    sender_id: UUID
    sender_type: str
    timestamp: datetime

    class Config:
        from_attributes = True