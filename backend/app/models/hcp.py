from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class HCP(Base):
    """Healthcare Professional model."""

    __tablename__ = "hcp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    interactions = relationship("Interaction", back_populates="hcp", lazy="selectin")
    follow_ups = relationship("FollowUp", back_populates="hcp", lazy="selectin")

    def __repr__(self):
        return f"<HCP(id={self.id}, name='{self.name}', specialty='{self.specialty}')>"
