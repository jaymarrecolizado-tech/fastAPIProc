"""BAC Document SQLAlchemy model"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import BACDocumentType, BACDocumentStatus, ProcurementMode


class BACDocument(Base):
    """BAC Document model - BAC preparation documents (Abstract, Price Matrix, etc.)"""
    
    __tablename__ = "bac_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # BAC Document Number (auto-generated format: BAC-YYYY-####)
    bac_document_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # References
    purchase_request_id = Column(
        Integer,
        ForeignKey("purchase_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    selected_supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )
    
    # Document Details
    procurement_mode = Column(SQLEnum(ProcurementMode), nullable=False)
    document_type = Column(SQLEnum(BACDocumentType), nullable=False, index=True)
    contract_amount = Column(DECIMAL(15, 2), nullable=False)
    delivery_schedule = Column(DateTime(timezone=True), nullable=False)
    payment_terms = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Status
    status = Column(
        SQLEnum(BACDocumentStatus),
        nullable=False,
        index=True,
        default=BACDocumentStatus.DRAFT
    )
    
    # Approval
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    purchase_request = relationship("PurchaseRequest", back_populates="bac_documents")
    selected_supplier = relationship("Supplier")
    approval_routings = relationship(
        "ApprovalRouting",
        back_populates="bac_document",
        foreign_keys="ApprovalRouting.document_id",
        primaryjoin="and_(ApprovalRouting.document_id==BACDocument.id, ApprovalRouting.document_type=='BAC_DOCUMENT')"
    )
    documents = relationship("Document", back_populates="bac_document", foreign_keys="Document.bac_document_id")
    
    # Indexes
    __table_args__ = (
        Index("ix_bac_documents_pr_type", "purchase_request_id", "document_type"),
        Index("ix_bac_documents_status", "status"),
    )
    
    def __repr__(self) -> str:
        return f"<BACDocument(id={self.id}, bac_document_number={self.bac_document_number}, document_type={self.document_type})>"
