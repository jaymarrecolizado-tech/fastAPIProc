"""Notification SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import NotificationType


class Notification(Base):
    """Notification model - in-app notifications for users"""
    
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User Reference
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Notification Details
    type = Column(SQLEnum(NotificationType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Action Link
    link = Column(String(500), nullable=True, comment="Deep link to relevant entity")
    entity_type = Column(String(100), nullable=True, index=True)
    entity_id = Column(Integer, nullable=True, index=True)
    
    # Read Status
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications", foreign_keys=[user_id])
    
    # Indexes
    __table_args__ = (
        Index("ix_notifications_user_read", "user_id", "is_read"),
        Index("ix_notifications_user_created", "user_id", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, title={self.title}, is_read={self.is_read})>"
