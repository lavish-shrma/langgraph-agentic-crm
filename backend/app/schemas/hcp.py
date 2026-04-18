from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HCPCreate(BaseModel):
    name: str
    specialty: str
    institution: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None


class HCPResponse(BaseModel):
    id: int
    name: str
    specialty: str
    institution: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HCPWithInteractions(HCPResponse):
    interactions: list = []

    class Config:
        from_attributes = True
