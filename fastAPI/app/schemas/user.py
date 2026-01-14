"""Pydantic schemas for User model"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.core.roles import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    department: Optional[str] = Field(None, max_length=255)
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=12, max_length=100)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Dela Cruz",
                "email": "juan.delacruz@dict.gov.ph",
                "password": "SecurePass123!@#",
                "department": "Information Technology Service",
                "role": "END_USER"
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserInDB(BaseModel):
    """Schema for user data in database (includes password hash)"""
    id: int
    name: str
    email: str
    password_hash: str
    role: UserRole
    department: Optional[str] = None
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """Schema for user response (excludes password hash)"""
    id: int
    name: str
    email: str
    role: UserRole
    department: Optional[str] = None
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "juan.delacruz@dict.gov.ph",
                "password": "SecurePass123!@#"
            }
        }
    )


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse


class TokenRefresh(BaseModel):
    """Schema for token refresh"""
    refresh_token: str


class PasswordReset(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=12, max_length=100)


class PasswordChange(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=12, max_length=100)


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)
