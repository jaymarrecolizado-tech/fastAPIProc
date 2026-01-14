"""User SQLAlchemy model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.roles import UserRole


class User(Base):
    """User model for authentication and authorization"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    department = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships - Temporarily disabled to avoid SQLAlchemy mapper errors
    # These will be enabled when all related models are properly imported
    # For now, authentication works without these relationships
    # created_prs = relationship(
    #     "PurchaseRequest",
    #     back_populates="end_user",
    #     foreign_keys="PurchaseRequest.end_user_id",
    #     lazy="select"
    # )
    # managed_rfqs = relationship(
    #     "RFQ",
    #     back_populates="procurement_officer",
    #     foreign_keys="RFQ.procurement_officer_id",
    #     lazy="select"
    # )
    # assigned_canvasses = relationship(
    #     "Canvass",
    #     back_populates="canvasser",
    #     foreign_keys="Canvass.canvasser_id",
    #     lazy="select"
    # )
    # uploaded_documents = relationship(
    #     "Document",
    #     back_populates="uploaded_by_user",
    #     foreign_keys="Document.uploaded_by",
    #     lazy="select"
    # )
    # approval_routings_received = relationship(
    #     "ApprovalRouting",
    #     back_populates="approver",
    #     foreign_keys="ApprovalRouting.approver_id",
    #     lazy="select"
    # )
    # approval_routings_created = relationship(
    #     "ApprovalRouting",
    #     back_populates="routed_by_user",
    #     foreign_keys="ApprovalRouting.routed_by",
    #     lazy="select"
    # )
    # activity_logs = relationship(
    #     "ActivityLog",
    #     back_populates="user",
    #     foreign_keys="ActivityLog.user_id",
    #     lazy="select"
    # )
    # notifications = relationship(
    #     "Notification",
    #     back_populates="user",
    #     foreign_keys="Notification.user_id",
    #     lazy="select"
    # )
    
    # Indexes
    __table_args__ = (
        Index("ix_users_role_active", "role", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
