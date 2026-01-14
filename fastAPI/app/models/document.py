"""Document SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import DocumentCategory


class Document(Base):
    """Document model - general document uploads for PRs, RFQs, BAC docs, POs"""
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Document Classification
    document_type = Column(SQLEnum(DocumentCategory), nullable=False, index=True)
    reference_id = Column(Integer, nullable=True, index=True, comment="ID of referenced entity")
    category = Column(String(100), nullable=True, index=True)
    
    # File Information
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(BigInteger, nullable=False, comment="Size in bytes")
    mime_type = Column(String(100), nullable=False)
    
    # Upload Tracking
    uploaded_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    uploaded_by_user = relationship("User", back_populates="uploaded_documents", foreign_keys=[uploaded_by])
    
    # Indexes
    __table_args__ = (
        Index("ix_documents_reference", "document_type", "reference_id"),
    )
    
    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file_name={self.file_name}, document_type={self.document_type})>"
