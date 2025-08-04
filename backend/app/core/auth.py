from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import get_db
from app.services.chat_service import ChatService
from app.models import User
import httpx
from typing import Optional
import json

# Security scheme
security = HTTPBearer(auto_error=False)

# Cache for Clerk JWKS (JSON Web Key Set)
_jwks_cache = None
_jwks_cache_time = 0

async def get_clerk_jwks():
    """Get Clerk's JSON Web Key Set for JWT verification"""
    global _jwks_cache, _jwks_cache_time
    import time
    
    # Cache JWKS for 1 hour
    if _jwks_cache and (time.time() - _jwks_cache_time) < 3600:
        return _jwks_cache
    
    try:
        # Get your Clerk instance URL from your dashboard
        # It should be something like: https://clerk.your-domain.com or similar
        # For now, we'll construct it from your secret key
        clerk_domain = "https://api.clerk.com"  # This is the default API domain
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{clerk_domain}/v1/jwks")
            _jwks_cache = response.json()
            _jwks_cache_time = time.time()
            return _jwks_cache
    except Exception as e:
        print(f"Failed to fetch JWKS: {e}")
        return None


def verify_clerk_jwt(token: str) -> Optional[dict]:
    """Verify a Clerk JWT token"""
    try:
        # For development, we'll implement a simpler verification
        # In production, you'd verify against Clerk's JWKS
        
        # Decode the JWT without verification for now (development only)
        payload = jwt.get_unverified_claims(token)
        
        # Basic validation
        if not payload.get("sub"):  # subject (user ID)
            return None
            
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "email_verified": payload.get("email_verified", False)
        }
        
    except JWTError as e:
        print(f"JWT verification failed: {e}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    
    # For development/testing, allow requests without auth
    if not credentials and settings.debug:
        # Return a test user for development
        service = ChatService(db)
        user = service.get_or_create_user("dev_user_123", "dev@example.com")
        return user
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the JWT token
    user_data = verify_clerk_jwt(credentials.credentials)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get or create user in our database
    service = ChatService(db)
    user = service.get_or_create_user(
        clerk_user_id=user_data["user_id"],
        email=user_data["email"]
    )
    
    return user


# Convenience function to get just the user ID
async def get_current_user_id(user: User = Depends(get_current_user)) -> int:
    """Get the current user's ID"""
    return user.id