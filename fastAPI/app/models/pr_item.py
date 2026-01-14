"""PR Item SQLAlchemy model"""

from decimal import Decimal
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class PRItem(Base):
    """Purchase Request Item model - items within a purchase request"""
    
    __tablename__ = "pr_items"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_request_id = Column(
        Integer,
        ForeignKey("purchase_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Item Details
    item_code = Column(String(100), nullable=False)
    item_name = Column(String(500), nullable=False)
    quantity = Column(DECIMAL(10, 2), nullable=False)
    unit_of_measure = Column(String(50), nullable=False)
    estimated_price = Column(DECIMAL(15, 2), nullable=False)
    
    # Relationships
    purchase_request = relationship("PurchaseRequest", back_populates="pr_items")
    quotation_items = relationship(
        "QuotationItem",
        back_populates="pr_item",
        foreign_keys="QuotationItem.pr_item_id"
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_pr_items_purchase_request", "purchase_request_id"),
    )
    
    @property
    def total_estimated_cost(self) -> Decimal:
        """Calculate total estimated cost for this item"""
        return self.quantity * self.estimated_price
    
    def __repr__(self) -> str:
        return f"<PRItem(id={self.id}, item_name={self.item_name}, quantity={self.quantity})>"
