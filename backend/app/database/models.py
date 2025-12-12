"""
Database models
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    CLIENT = "client"


class ProviderType(str, enum.Enum):
    """Provider type enumeration"""
    NINJA = "ninja"
    MALWAREBYTES = "malwarebytes"


class User(BaseModel):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.CLIENT.value)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    dashboards = relationship("Dashboard", back_populates="user", cascade="all, delete-orphan")


class Provider(BaseModel):
    """Provider model for storing provider configurations"""
    __tablename__ = "providers"
    
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # ProviderType enum value
    api_key_encrypted = Column(Text, nullable=False)  # Encrypted API key
    base_url = Column(String(500), nullable=True)
    config = Column(JSON, nullable=True)  # Provider-specific configuration
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    provider_specific_settings = Column(JSON, nullable=True)  # Additional settings
    
    # Relationships
    cache_entries = relationship("CacheEntry", back_populates="provider", cascade="all, delete-orphan")


class CacheEntry(BaseModel):
    """Cache entry model for storing API responses"""
    __tablename__ = "cache_entries"
    
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=True, index=True)
    cache_key = Column(String(64), unique=True, nullable=False, index=True)
    response_data = Column(JSON, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Relationships
    provider = relationship("Provider", back_populates="cache_entries")


class Dashboard(BaseModel):
    """Dashboard model for user-specific dashboard configurations"""
    __tablename__ = "dashboards"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    config = Column(JSON, nullable=False)  # Dashboard configuration (widgets, layout, etc.)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="dashboards")

