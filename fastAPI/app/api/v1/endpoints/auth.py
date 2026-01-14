"""
Authentication endpoints.
Provides login, logout, token refresh, and user profile endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.rate_limiter import get_rate_limiter, get_client_identifier
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import (
    UserLogin,
    TokenResponse,
    UserResponse,
    UserCreate,
    PasswordChange,
    PasswordReset
)
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens.
    
    - **email**: User email address
    - **password**: User password
    
    Returns access_token and refresh_token.
    Rate limited: 5 attempts per minute, then 15-minute lockout.
    """
    # Check rate limit
    identifier = get_client_identifier(request)
    limiter = get_rate_limiter()
    
    allowed, lockout_remaining = limiter.check_rate_limit(identifier)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Too many failed attempts. Account locked temporarily.",
                "lockout_remaining_seconds": lockout_remaining,
                "lockout_remaining_minutes": lockout_remaining // 60
            }
        )
    
    # Authenticate
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(
        credentials.email,
        credentials.password
    )
    
    if not user:
        # Record failed attempt
        limiter.record_attempt(identifier, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Reset rate limit on successful login
    limiter.reset(identifier)
    
    # Create tokens
    tokens = await auth_service.create_tokens(user, identifier)
    
    return tokens


@router.post("/login/oauth2", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login_oauth2(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible login endpoint.
    Use this for Swagger UI authentication.
    """
    # Check rate limit
    identifier = get_client_identifier(request)
    limiter = get_rate_limiter()
    
    allowed, lockout_remaining = limiter.check_rate_limit(identifier)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Too many failed attempts. Account locked temporarily.",
                "lockout_remaining_seconds": lockout_remaining
            }
        )
    
    # Authenticate
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(
        form_data.username,  # OAuth2 uses username field for email
        form_data.password
    )
    
    if not user:
        limiter.record_attempt(identifier, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    limiter.reset(identifier)
    tokens = await auth_service.create_tokens(user, identifier)
    
    return tokens


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout current user.
    Note: JWT tokens are stateless, so this mainly serves as a client-side indicator.
    In production, implement token blacklist using Redis.
    """
    auth_service = AuthService(db)
    await auth_service.logout_user(current_user.id)
    
    return {
        "message": "Successfully logged out",
        "detail": "Please delete your tokens from client storage"
    }


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token from login response
    
    Returns new access_token and refresh_token.
    """
    auth_service = AuthService(db)
    tokens = await auth_service.refresh_access_token(refresh_token)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    return tokens


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    Requires valid access token.
    """
    return UserResponse.model_validate(current_user)


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change current user's password.
    
    - **old_password**: Current password
    - **new_password**: New password (min 8 chars, must include uppercase, lowercase, number, special char)
    """
    from app.core.security import verify_password
    
    # Verify old password
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Hash new password
    current_user.password_hash = get_password_hash(password_data.new_password)
    
    await db.commit()
    await db.refresh(current_user)
    
    return {
        "message": "Password changed successfully",
        "detail": "Please login again with your new password"
    }


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset (placeholder for email flow).
    In production, this would:
    1. Validate email exists
    2. Generate reset token
    3. Send email with reset link
    4. User clicks link and submits new password
    """
    # TODO: Implement email-based password reset
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Password reset via email not yet implemented"
    )
