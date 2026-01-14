"""Approval Routing SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Index, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import ApprovalStatus


class ApprovalRouting(Base):
    """Approval Routing model - manages sequential approval workflows"""
    
    __tablename__ = "approval_routings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Document Reference (polymorphic - can reference PR, RFQ, or BAC Document)
    document_type = Column(
        String(50),
        nullable=False,
        index=True,
        comment="PURCHASE_REQUEST, RFQ, BAC_DOCUMENT"
    )
    document_id = Column(Integer, nullable=False, index=True, comment="ID of the referenced document")
    
    # Approver
    approver_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Routing Details
    sequence = Column(Integer, nullable=False, index=True, comment="Order in approval chain")
    
    # Status
    status = Column(
        SQLEnum(ApprovalStatus),
        nullable=False,
        index=True,
        default=ApprovalStatus.PENDING
    )
    
    # Timestamps
    routed_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    routed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejected_at = Column(DateTime(timezone=True), nullable=True)
    
    # Comments
    comments = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Relationships
    approver = relationship("User", back_populates="approval_routings_received", foreign_keys=[approver_id])
    routed_by_user = relationship("User", back_populates="approval_routings_created", foreign_keys=[routed_by])
    purchase_request = relationship(
        "PurchaseRequest",
        back_populates="approval_routings",
        foreign_keys=[document_id],
        primaryjoin="and_(ApprovalRouting.document_id==PurchaseRequest.id, ApprovalRouting.document_type=='PURCHASE_REQUEST')"
    )
    bac_document = relationship(
        "BACDocument",
        back_populates="approval_routings",
        foreign_keys=[document_id],
        primaryjoin="and_(ApprovalRouting.document_id==BACDocument.id, ApprovalRouting.document_type=='BAC_DOCUMENT')"
    )
    
    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint("document_type", "document_id", "sequence", name="uq_approval_routing_sequence"),
        Index("ix_approval_routings_document_status", "document_type", "document_id", "status"),
        Index("ix_approval_routings_approver_status", "approver_id", "status"),
        Index("ix_approval_routings_sequence", "document_type", "document_id", "sequence"),
    )
    
    def __repr__(self) -> str:
        return f"<ApprovalRouting(id={self.id}, document_type={self.document_type}, document_id={self.document_id}, sequence={self.sequence})>"
