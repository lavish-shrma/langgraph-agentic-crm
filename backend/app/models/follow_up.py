from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class FollowUp(Base):
    """Follow-up task model."""

    __tablename__ = "follow_up"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interaction_id = Column(Integer, ForeignKey("interaction.id"), nullable=False)
    hcp_id = Column(Integer, ForeignKey("hcp.id"), nullable=False)
    follow_up_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    interaction = relationship("Interaction", back_populates="follow_ups")
    hcp = relationship("HCP", back_populates="follow_ups")

    def __repr__(self):
        return f"<FollowUp(id={self.id}, date={self.follow_up_date}, status='{self.status}')>"
