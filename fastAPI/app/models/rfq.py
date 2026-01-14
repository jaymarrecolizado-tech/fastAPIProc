"""RFQ (Request for Quotation) SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Index, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import RFQStatus


class RFQ(Base):
    """Request for Quotation model - created from approved purchase requests"""
    
    __tablename__ = "rfqs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # RFQ Number (auto-generated format: RFQ-YYYY-####)
    rfq_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # References
    purchase_request_id = Column(
        Integer,
        ForeignKey("purchase_requests.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    procurement_officer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # RFQ Details
    delivery_schedule = Column(DateTime(timezone=True), nullable=False)
    payment_terms = Column(Text, nullable=False)
    canvassing_deadline = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Status
    status = Column(
        SQLEnum(RFQStatus),
        nullable=False,
        index=True,
        default=RFQStatus.PENDING
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    purchase_request = relationship("PurchaseRequest", back_populates="rfq")
    procurement_officer = relationship("User", back_populates="managed_rfqs", foreign_keys=[procurement_officer_id])
    canvasses = relationship(
        "Canvass",
        back_populates="rfq",
        cascade="all, delete-orphan",
        foreign_keys="Canvass.rfq_id"
    )
    documents = relationship("Document", back_populates="rfq", foreign_keys="Document.rfq_id")
    
    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint("purchase_request_id", name="uq_rfqs_purchase_request"),
        Index("ix_rfqs_status_created", "status", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<RFQ(id={self.id}, rfq_number={self.rfq_number}, status={self.status})>"
