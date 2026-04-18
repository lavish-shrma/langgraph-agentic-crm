from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Sample(Base):
    """Sample distribution model."""

    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interaction_id = Column(Integer, ForeignKey("interaction.id"), nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    interaction = relationship("Interaction", back_populates="samples")

    def __repr__(self):
        return f"<Sample(id={self.id}, product='{self.product_name}', qty={self.quantity})>"
