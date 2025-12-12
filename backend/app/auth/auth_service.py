"""
Authentication service for user authentication and management
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from jose import JWTError
from app.database.models import User
from app.auth.password import verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token
)


class AuthService:
    """Service for user authentication and token management"""
    
    def __init__(self, db: Session):
        """
        Initialize AuthService.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username/email and password.
        
        Args:
            username_or_email: Username or email address
            password: Plain text password
            
        Returns:
            User object if authentication succeeds, None otherwise
        """
        # Try to find user by username or email
        user = self.db.query(User).filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        ).first()
        
        if not user:
            return None
        
        # Check if user is active
        if not user.is_active:
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_tokens_for_user(self, user: User) -> Dict[str, Any]:
        """
        Create access and refresh tokens for a user.
        
        Args:
            user: User object
            
        Returns:
            Dictionary with access_token, refresh_token, and token_type
        """
        token_data = {
            "sub": user.guid,
            "role": user.role
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": user.guid})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Create a new access token from a refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Dictionary with new access_token and refresh_token, or None if invalid
        """
        try:
            # Verify and decode refresh token
            payload = verify_token(refresh_token)
            
            # Check that it's actually a refresh token
            if payload.get("type") != "refresh":
                return None
            
            # Get user GUID from token
            user_guid = payload.get("sub")
            if not user_guid:
                return None
            
            # Get user from database
            user = self.get_user_by_guid(user_guid)
            if not user or not user.is_active:
                return None
            
            # Create new tokens
            return self.create_tokens_for_user(user)
            
        except JWTError:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: Email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_guid(self, guid: str) -> Optional[User]:
        """
        Get user by GUID.
        
        Args:
            guid: User GUID to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.guid == guid).first()
