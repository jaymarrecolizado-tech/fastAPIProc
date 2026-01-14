"""
Rate limiting middleware for authentication endpoints.
Prevents brute force attacks by limiting login attempts.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
from collections import defaultdict
import asyncio

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse


class RateLimiter:
    """
    In-memory rate limiter using sliding window algorithm.
    For production, use Redis-based solution for distributed systems.
    """
    
    def __init__(self):
        # Store: {identifier: [(timestamp, success)]}
        self._attempts: Dict[str, list[tuple[datetime, bool]]] = defaultdict(list)
        self._lockouts: Dict[str, datetime] = {}
        
        # Configuration
        self.max_attempts = 5  # Maximum failed attempts
        self.window_seconds = 60  # Time window in seconds
        self.lockout_seconds = 900  # 15 minutes lockout
    
    def _cleanup_old_attempts(self, identifier: str) -> None:
        """Remove attempts outside the time window."""
        cutoff = datetime.now() - timedelta(seconds=self.window_seconds)
        self._attempts[identifier] = [
            (ts, success) for ts, success in self._attempts[identifier]
            if ts > cutoff
        ]
    
    def _get_failed_attempts(self, identifier: str) -> int:
        """Count failed attempts within time window."""
        self._cleanup_old_attempts(identifier)
        return sum(1 for _, success in self._attempts[identifier] if not success)
    
    def is_locked_out(self, identifier: str) -> bool:
        """Check if identifier is currently locked out."""
        if identifier in self._lockouts:
            if datetime.now() < self._lockouts[identifier]:
                return True
            else:
                # Lockout expired
                del self._lockouts[identifier]
        return False
    
    def get_lockout_remaining(self, identifier: str) -> int:
        """Get remaining lockout time in seconds."""
        if identifier in self._lockouts:
            remaining = (self._lockouts[identifier] - datetime.now()).total_seconds()
            return max(0, int(remaining))
        return 0
    
    def record_attempt(self, identifier: str, success: bool) -> None:
        """Record a login attempt."""
        self._attempts[identifier].append((datetime.now(), success))
        
        # If failed attempt, check if should lockout
        if not success:
            failed_count = self._get_failed_attempts(identifier)
            if failed_count >= self.max_attempts:
                # Lockout for specified duration
                self._lockouts[identifier] = datetime.now() + timedelta(seconds=self.lockout_seconds)
    
    def check_rate_limit(self, identifier: str) -> tuple[bool, Optional[int]]:
        """
        Check if request should be rate limited.
        Returns: (allowed, remaining_lockout_seconds)
        """
        # Check if locked out
        if self.is_locked_out(identifier):
            remaining = self.get_lockout_remaining(identifier)
            return False, remaining
        
        # Check rate limit
        failed_count = self._get_failed_attempts(identifier)
        if failed_count >= self.max_attempts:
            self._lockouts[identifier] = datetime.now() + timedelta(seconds=self.lockout_seconds)
            return False, self.lockout_seconds
        
        return True, None
    
    def reset(self, identifier: str) -> None:
        """Reset rate limit for identifier (e.g., after successful login)."""
        if identifier in self._attempts:
            del self._attempts[identifier]
        if identifier in self._lockouts:
            del self._lockouts[identifier]


# Global rate limiter instance
_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    return _rate_limiter


def get_client_identifier(request: Request) -> str:
    """
    Extract client identifier from request.
    Uses IP address, falling back to X-Forwarded-For header.
    """
    # Check for forwarded IP (behind proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Get first IP in list
        return forwarded.split(",")[0].strip()
    
    # Use direct IP
    return str(request.client.host) if request.client else "unknown"


async def check_auth_rate_limit(request: Request) -> None:
    """
    Check rate limit for authentication requests.
    Raises HTTPException if rate limit exceeded.
    """
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
