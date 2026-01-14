"""
Authentication service layer.
Handles business logic for user authentication and token management.
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.config import settings
from app.models.user import User
from app.schemas.user import Token, TokenResponse, UserCreate, UserResponse


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password.
        Returns User object if successful, None otherwise.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    async def create_tokens(
        self,
        user: User,
        client_ip: Optional[str] = None
    ) -> TokenResponse:
        """
        Create access and refresh tokens for user.
        """
        # Create access token (short-lived: 2 hours)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )
        
        # Create refresh token (long-lived: 30 days)
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        # Calculate expiration times
        access_expires = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_expires = datetime.now() + timedelta(days=30)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user)
        )
    
    async def refresh_access_token(
        self,
        refresh_token: str
    ) -> Optional[TokenResponse]:
        """
        Create new access token from refresh token.
        Returns None if refresh token is invalid.
        """
        # Decode refresh token
        payload = decode_token(refresh_token)
        if payload is None:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        # Get user
        result = await self.db.execute(
            select(User).where(User.id == int(user_id))
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            return None
        
        # Create new tokens
        return await self.create_tokens(user)
    
    async def get_current_user(
        self,
        user_id: int
    ) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def logout_user(
        self,
        user_id: int
    ) -> bool:
        """
        Logout user (for token invalidation in future).
        Currently a placeholder as we use stateless JWT tokens.
        In production, implement token blacklist using Redis.
        """
        # TODO: Add token to Redis blacklist
        # await redis.setex(f"blacklist:{user_id}", expiry, token)
        return True
