"""Canvass SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import CanvassStatus


class Canvass(Base):
    """Canvass model - canvassing tasks assigned to canvassers"""
    
    __tablename__ = "canvasses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Canvass Number (auto-generated format: CANVASS-YYYY-####)
    canvass_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # References
    rfq_id = Column(
        Integer,
        ForeignKey("rfqs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    canvasser_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Canvass Details
    task_description = Column(Text, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    
    # Status
    status = Column(
        SQLEnum(CanvassStatus),
        nullable=False,
        index=True,
        default=CanvassStatus.PENDING
    )
    
    # Completion
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    rfq = relationship("RFQ", back_populates="canvasses")
    canvasser = relationship("User", back_populates="assigned_canvasses", foreign_keys=[canvasser_id])
    supplier_quotations = relationship(
        "SupplierQuotation",
        back_populates="canvass",
        cascade="all, delete-orphan",
        foreign_keys="SupplierQuotation.canvass_id"
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_canvasses_status_deadline", "status", "deadline"),
        Index("ix_canvasses_canvasser_status", "canvasser_id", "status"),
    )
    
    def __repr__(self) -> str:
        return f"<Canvass(id={self.id}, canvass_number={self.canvass_number}, status={self.status})>"
