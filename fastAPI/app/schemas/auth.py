"""
Authentication-specific schemas.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.schemas.user import UserResponse


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


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)


class PasswordChange(BaseModel):
    """Schema for changing password"""
    old_password: str
    new_password: str = Field(..., min_length=12, max_length=100)


class PasswordReset(BaseModel):
    """Schema for password reset request"""
    email: EmailStr
