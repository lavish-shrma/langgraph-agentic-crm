from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class FollowUpCreate(BaseModel):
    interaction_id: int
    hcp_id: int
    follow_up_date: date
    notes: Optional[str] = None
    status: str = "pending"


class FollowUpUpdate(BaseModel):
    follow_up_date: Optional[date] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class FollowUpResponse(BaseModel):
    id: int
    interaction_id: int
    hcp_id: int
    follow_up_date: date
    notes: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
