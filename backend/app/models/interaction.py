from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Interaction(Base):
    """HCP Interaction model."""

    __tablename__ = "interaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hcp_id = Column(Integer, ForeignKey("hcp.id"), nullable=False)
    interaction_type = Column(String, nullable=False)  # Meeting, Call, Email, Conference Visit, Other
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=True)
    attendees = Column(Text, nullable=True)
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(JSONB, nullable=True, default=list)  # Array of strings
    sentiment = Column(String, nullable=True)  # positive, neutral, negative
    outcome = Column(Text, nullable=True)
    follow_up_notes = Column(Text, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    ai_suggested_followups = Column(JSONB, nullable=True, default=list)  # Array of strings
    location = Column(String, nullable=True)
    source = Column(String, nullable=False, default="form")  # form or chat
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    hcp = relationship("HCP", back_populates="interactions")
    samples = relationship("Sample", back_populates="interaction", lazy="selectin", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="interaction", lazy="selectin")

    def __repr__(self):
        return f"<Interaction(id={self.id}, type='{self.interaction_type}', date={self.date})>"
