"""Quotation Item SQLAlchemy model"""

from decimal import Decimal
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Index, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class QuotationItem(Base):
    """Quotation Item model - items within a supplier quotation"""
    
    __tablename__ = "quotation_items"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # References
    supplier_quotation_id = Column(
        Integer,
        ForeignKey("supplier_quotations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    pr_item_id = Column(
        Integer,
        ForeignKey("pr_items.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Item Details (matching PR item but with supplier pricing)
    item_code = Column(String(100), nullable=False)
    item_name = Column(String(500), nullable=False)
    quantity = Column(DECIMAL(10, 2), nullable=False)
    unit_price = Column(DECIMAL(15, 2), nullable=False)
    total_price = Column(DECIMAL(15, 2), nullable=False)  # Generated column equivalent
    
    # Relationships
    supplier_quotation = relationship("SupplierQuotation", back_populates="quotation_items")
    pr_item = relationship("PRItem", back_populates="quotation_items")
    
    # Indexes
    __table_args__ = (
        Index("ix_quotation_items_supplier_quotation", "supplier_quotation_id"),
        Index("ix_quotation_items_pr_item", "pr_item_id"),
    )
    
    def __repr__(self) -> str:
        return f"<QuotationItem(id={self.id}, item_name={self.item_name}, unit_price={self.unit_price})>"
