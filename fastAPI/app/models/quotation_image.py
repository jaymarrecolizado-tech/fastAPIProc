"""Quotation Image SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class QuotationImage(Base):
    """Quotation Image model - supporting document images for quotations"""
    
    __tablename__ = "quotation_images"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Reference
    supplier_quotation_id = Column(
        Integer,
        ForeignKey("supplier_quotations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # File Information
    image_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)  # Size in bytes
    
    # Upload Tracking
    uploaded_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    # Relationships
    supplier_quotation = relationship("SupplierQuotation", back_populates="quotation_images")
    
    def __repr__(self) -> str:
        return f"<QuotationImage(id={self.id}, original_filename={self.original_filename})>"
