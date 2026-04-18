from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SampleCreate(BaseModel):
    product_name: str
    quantity: int


class SampleResponse(BaseModel):
    id: int
    interaction_id: int
    product_name: str
    quantity: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
