"""Activity Log SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.status import ActivityAction


class ActivityLog(Base):
    """Activity Log model - comprehensive audit trail for all system actions"""
    
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User Reference
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Action Details
    action = Column(SQLEnum(ActivityAction), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True, comment="User, PR, RFQ, etc.")
    entity_id = Column(Integer, nullable=True, index=True, comment="ID of the entity")
    
    # Change Tracking (JSON for flexible old/new values)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    
    # Description
    description = Column(Text, nullable=False)
    
    # Request Information
    ip_address = Column(String(45), nullable=True, comment="IPv4 or IPv6")
    user_agent = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="activity_logs", foreign_keys=[user_id])
    purchase_request = relationship("PurchaseRequest", back_populates="activity_logs", foreign_keys=[entity_id], primaryjoin="and_(ActivityLog.entity_id==PurchaseRequest.id, ActivityLog.entity_type=='PurchaseRequest')")
    
    # Indexes
    __table_args__ = (
        Index("ix_activity_logs_user_action", "user_id", "action"),
        Index("ix_activity_logs_entity", "entity_type", "entity_id"),
        Index("ix_activity_logs_created", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<ActivityLog(id={self.id}, action={self.action}, entity_type={self.entity_type})>"
