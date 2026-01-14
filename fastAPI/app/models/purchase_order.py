"""Purchase Order SQLAlchemy model"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Enum as SQLEnum, Index, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import PurchaseOrderStatus


class PurchaseOrder(Base):
    """Purchase Order model - final PO generated from BAC-approved documents"""
    
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # PO Number (auto-generated format: PO-YYYY-####)
    po_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # References
    purchase_request_id = Column(
        Integer,
        ForeignKey("purchase_requests.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # PO Details
    contract_amount = Column(DECIMAL(15, 2), nullable=False)
    delivery_instructions = Column(Text, nullable=False)
    payment_terms = Column(Text, nullable=False)
    delivery_deadline = Column(DateTime(timezone=True), nullable=False)
    
    # Status
    status = Column(
        SQLEnum(PurchaseOrderStatus),
        nullable=False,
        index=True,
        default=PurchaseOrderStatus.PENDING
    )
    
    # Conforme (Supplier Acceptance)
    conforme_status = Column(String(50), nullable=True, index=True, comment="ACCEPTED, REJECTED")
    conforme_date = Column(DateTime(timezone=True), nullable=True)
    conforme_signature_path = Column(String(500), nullable=True)
    
    # Timestamps
    disseminated_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    purchase_request = relationship("PurchaseRequest", back_populates="purchase_order")
    supplier = relationship("Supplier", back_populates="purchase_orders")
    documents = relationship("Document", back_populates="purchase_order", foreign_keys="Document.purchase_order_id")
    
    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint("purchase_request_id", name="uq_purchase_orders_purchase_request"),
        Index("ix_purchase_orders_status_created", "status", "created_at"),
        Index("ix_purchase_orders_supplier", "supplier_id"),
    )
    
    def __repr__(self) -> str:
        return f"<PurchaseOrder(id={self.id}, po_number={self.po_number}, status={self.status})>"
