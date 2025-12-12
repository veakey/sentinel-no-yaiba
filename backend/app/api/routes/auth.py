"""
Authentication API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database.database import get_db
from app.auth.auth_service import AuthService
from app.auth.dependencies import get_current_user
from app.database.models import User


router = APIRouter(prefix="/api/auth", tags=["auth"])


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request model"""
    refresh_token: str


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint to authenticate user and get tokens.
    
    Args:
        form_data: OAuth2 form data with username and password
        db: Database session
        
    Returns:
        TokenResponse with access_token, refresh_token, and token_type
        
    Raises:
        HTTPException: If authentication fails (401 Unauthorized)
    """
    auth_service = AuthService(db)
    
    # Authenticate user
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    tokens = auth_service.create_tokens_for_user(user)
    
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Args:
        request: RefreshTokenRequest with refresh_token
        db: Database session
        
    Returns:
        TokenResponse with new access_token and refresh_token
        
    Raises:
        HTTPException: If refresh token is invalid (401 Unauthorized)
    """
    auth_service = AuthService(db)
    
    # Refresh tokens
    tokens = auth_service.refresh_access_token(request.refresh_token)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return tokens


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user from dependency
        
    Returns:
        User information (without sensitive data)
    """
    return {
        "guid": current_user.guid,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }

