from pydantic import BaseModel
import datetime
from typing import Optional, List

from app.schemas.sample import SampleCreate, SampleResponse


class InteractionCreate(BaseModel):
    hcp_id: int
    interaction_type: str
    date: datetime.date
    time: Optional[datetime.time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = None
    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_notes: Optional[str] = None
    follow_up_date: Optional[datetime.date] = None
    ai_suggested_followups: Optional[List[str]] = None
    location: Optional[str] = None
    source: str = "form"
    samples: Optional[List[SampleCreate]] = None


class InteractionUpdate(BaseModel):
    interaction_type: Optional[str] = None
    date: Optional[datetime.date] = None
    time: Optional[datetime.time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = None
    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_notes: Optional[str] = None
    follow_up_date: Optional[datetime.date] = None
    ai_suggested_followups: Optional[List[str]] = None
    location: Optional[str] = None


class InteractionResponse(BaseModel):
    id: int
    hcp_id: int
    interaction_type: str
    date: datetime.date
    time: Optional[datetime.time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = None
    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_notes: Optional[str] = None
    follow_up_date: Optional[datetime.date] = None
    ai_suggested_followups: Optional[List[str]] = None
    location: Optional[str] = None
    source: str
    samples: List[SampleResponse] = []
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True
