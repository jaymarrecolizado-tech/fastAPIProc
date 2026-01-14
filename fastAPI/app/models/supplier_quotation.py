"""Supplier Quotation SQLAlchemy model"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Boolean, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import ComplianceStatus


class SupplierQuotation(Base):
    """Supplier Quotation model - quotations from suppliers for canvasses"""
    
    __tablename__ = "supplier_quotations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # References
    canvass_id = Column(
        Integer,
        ForeignKey("canvasses.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Supplier Information (snapshot at time of quotation)
    supplier_name = Column(String(500), nullable=False)
    supplier_address = Column(Text, nullable=False)
    supplier_contact_person = Column(String(255), nullable=False)
    supplier_contact_number = Column(String(50), nullable=False)
    supplier_email = Column(String(255), nullable=True)
    
    # Quotation Details
    delivery_days = Column(Integer, nullable=False)
    compliance_status = Column(
        SQLEnum(ComplianceStatus),
        nullable=False,
        index=True,
        default=ComplianceStatus.COMPLIANT
    )
    total_amount = Column(DECIMAL(15, 2), nullable=False)
    
    # Selection
    is_selected = Column(Boolean, default=False, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    canvass = relationship("Canvass", back_populates="supplier_quotations")
    supplier = relationship("Supplier", back_populates="quotations")
    quotation_items = relationship(
        "QuotationItem",
        back_populates="supplier_quotation",
        cascade="all, delete-orphan",
        foreign_keys="QuotationItem.supplier_quotation_id"
    )
    quotation_images = relationship(
        "QuotationImage",
        back_populates="supplier_quotation",
        cascade="all, delete-orphan",
        foreign_keys="QuotationImage.supplier_quotation_id"
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_supplier_quotations_canvass_selected", "canvass_id", "is_selected"),
    )
    
    def __repr__(self) -> str:
        return f"<SupplierQuotation(id={self.id}, supplier_name={self.supplier_name}, is_selected={self.is_selected})>"
