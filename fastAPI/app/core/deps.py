"""FastAPI dependencies for authentication and authorization"""

from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_token
from app.core.roles import UserRole
from app.models.user import User


# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extract user ID
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Query user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Get current active user (shortcut for checking is_active).
    
    Raises:
        HTTPException: 400 if user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_role(*allowed_roles: UserRole):
    """
    Dependency factory to require specific user roles.
    
    Usage:
        @app.get("/admin-only")
        async def admin_endpoint(
            user: Annotated[User, Depends(require_role(UserRole.ADMIN))]
        ):
            ...
    
    Raises:
        HTTPException: 403 if user doesn't have required role
    """
    async def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)]
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join([r.value for r in allowed_roles])}"
            )
        return current_user
    
    return role_checker


# Common role-based dependencies
require_admin = require_role(UserRole.ADMIN)
require_procurement_officer = require_role(UserRole.PROCUREMENT_OFFICER, UserRole.ADMIN)
require_end_user = require_role(UserRole.END_USER, UserRole.ADMIN)
require_canvasser = require_role(UserRole.CANVASSER, UserRole.ADMIN)
require_bac_member = require_role(UserRole.BAC_MEMBER, UserRole.BAC_CHAIR, UserRole.ADMIN)
require_bac_secretariat = require_role(UserRole.BAC_SECRETARIAT, UserRole.ADMIN)
require_supplier = require_role(UserRole.SUPPLIER, UserRole.ADMIN)


def require_any_role(*allowed_roles: UserRole):
    """
    Dependency to allow access to users with ANY of the specified roles.
    Similar to require_role but with clearer naming for complex cases.
    """
    return require_role(*allowed_roles)


# Procurement staff dependency (OFFICER, BAC_SECRETARIAT, BAC_MEMBER, BAC_CHAIR)
require_procurement_staff = require_role(
    UserRole.PROCUREMENT_OFFICER,
    UserRole.BAC_SECRETARIAT,
    UserRole.BAC_MEMBER,
    UserRole.BAC_CHAIR,
    UserRole.ADMIN
)


# Approver dependency (users who can approve documents)
require_approver = require_role(
    UserRole.PROCUREMENT_OFFICER,
    UserRole.BAC_MEMBER,
    UserRole.BAC_CHAIR,
    UserRole.ADMIN
)
