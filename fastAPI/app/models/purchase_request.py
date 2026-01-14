"""Purchase Request SQLAlchemy model"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Boolean, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import PurchaseRequestStatus, UrgencyLevel


class PurchaseRequest(Base):
    """Purchase Request model - the core entity of the procurement workflow"""
    
    __tablename__ = "purchase_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # PR Number (auto-generated format: PR-YYYY-####)
    pr_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Project Information
    project_title = Column(String(500), nullable=False)
    project_description = Column(Text, nullable=False)
    purpose = Column(Text, nullable=False)
    
    # User Reference
    end_user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    # Department Information
    end_user_department = Column(String(255), nullable=False)
    office_name = Column(String(255), nullable=True)
    office_address = Column(Text, nullable=True)
    responsibility_center = Column(String(100), nullable=True)
    
    # Financial Information
    fund_source = Column(String(255), nullable=False, index=True)
    estimated_budget = Column(DECIMAL(15, 2), nullable=False)
    
    # Urgency
    urgency_level = Column(SQLEnum(UrgencyLevel), nullable=False, index=True, default=UrgencyLevel.MEDIUM)
    urgency_timeline = Column(Text, nullable=True)
    
    # Approval Date
    approval_date = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    status = Column(
        SQLEnum(PurchaseRequestStatus),
        nullable=False,
        index=True,
        default=PurchaseRequestStatus.PR_UNDER_REVIEW
    )
    
    # RA 9184 Compliance Checklist
    # Section 1: General Information
    has_unit_price = Column(Boolean, default=False, nullable=True)
    has_market_study = Column(Boolean, default=False, nullable=True)
    has_budget_allocation = Column(Boolean, default=False, nullable=True)
    
    # Section 2: Technical Specifications
    has_technical_specs = Column(Boolean, default=False, nullable=True)
    has_approved_plan = Column(Boolean, default=False, nullable=True)
    
    # Section 3: Procurement Mode Justification
    procurement_mode_justification = Column(Text, nullable=True)
    
    # Signatory Information
    requested_by_name = Column(String(255), nullable=True)
    requested_by_position = Column(String(255), nullable=True)
    approved_by_name = Column(String(255), nullable=True)
    approved_by_position = Column(String(255), nullable=True)
    noted_by_name = Column(String(255), nullable=True)
    noted_by_position = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    end_user = relationship("User", foreign_keys=[end_user_id])
    pr_items = relationship("PRItem", back_populates="purchase_request", cascade="all, delete-orphan")
    rfq = relationship(
        "RFQ",
        back_populates="purchase_request",
        uselist=False,
        foreign_keys="RFQ.purchase_request_id"
    )
    bac_documents = relationship(
        "BACDocument",
        back_populates="purchase_request",
        foreign_keys="BACDocument.purchase_request_id"
    )
    purchase_order = relationship(
        "PurchaseOrder",
        back_populates="purchase_request",
        uselist=False,
        foreign_keys="PurchaseOrder.purchase_request_id"
    )
    approval_routings = relationship(
        "ApprovalRouting",
        back_populates="purchase_request",
        foreign_keys="ApprovalRouting.document_id",
        primaryjoin="and_(ApprovalRouting.document_id==PurchaseRequest.id, ApprovalRouting.document_type=='PURCHASE_REQUEST')"
    )
    
    def __repr__(self) -> str:
        return f"<PurchaseRequest(id={self.id}, pr_number={self.pr_number}, status={self.status})>"
