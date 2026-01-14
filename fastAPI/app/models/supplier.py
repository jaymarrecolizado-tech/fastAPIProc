"""Supplier SQLAlchemy model"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class Supplier(Base):
    """Supplier model - registered suppliers for quotations"""
    
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Company Information
    name = Column(String(500), nullable=False, index=True)
    address = Column(Text, nullable=False)
    
    # Contact Information
    contact_person = Column(String(255), nullable=False)
    contact_number = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    
    # Government Identifiers
    tax_id_number = Column(String(50), nullable=True, index=True)
    philgeps_number = Column(String(100), nullable=True, index=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    quotations = relationship(
        "SupplierQuotation",
        back_populates="supplier",
        foreign_keys="SupplierQuotation.supplier_id"
    )
    purchase_orders = relationship(
        "PurchaseOrder",
        back_populates="supplier",
        foreign_keys="PurchaseOrder.supplier_id"
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_suppliers_name_active", "name", "is_active"),
        Index("ix_suppliers_tax_id", "tax_id_number"),
    )
    
    def __repr__(self) -> str:
        return f"<Supplier(id={self.id}, name={self.name}, is_active={self.is_active})>"
