"""
Database models
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text, Boolean, Enum
import enum
from .base import BaseModel


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    CLIENT = "client"


class User(BaseModel):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.CLIENT.value)
    is_active = Column(Boolean, default=True, nullable=False)


class CacheEntry(BaseModel):
    """Cache entry model for storing API responses"""
    __tablename__ = "cache_entries"
    
    # provider_id will be linked to Provider model in Phase 5
    # For now, it's just an integer field
    provider_id = Column(Integer, nullable=True)
    cache_key = Column(String(64), unique=True, nullable=False, index=True)
    response_data = Column(JSON, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

