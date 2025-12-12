"""
FastAPI dependencies for authentication and authorization
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import User
from app.auth.jwt import verify_token
from app.core.exceptions import AppException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT access token
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify and decode token
        payload = verify_token(token)
        user_guid = payload.get("sub")
        
        if user_guid is None:
            raise credentials_exception
        
        # Get user from database
        user = db.query(User).filter(User.guid == user_guid).first()
        
        if user is None:
            raise credentials_exception
        
        # Check if user is active
        if not user.is_active:
            raise credentials_exception
        
        return user
        
    except Exception:
        raise credentials_exception


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to require admin role.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if admin
        
    Raises:
        HTTPException: If user is not admin (403 Forbidden)
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )
    
    return current_user

