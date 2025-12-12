"""
Database models
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from .base import BaseModel


class CacheEntry(BaseModel):
    """Cache entry model for storing API responses"""
    __tablename__ = "cache_entries"
    
    # provider_id will be linked to Provider model in Phase 5
    # For now, it's just an integer field
    provider_id = Column(Integer, nullable=True)
    cache_key = Column(String(64), unique=True, nullable=False, index=True)
    response_data = Column(JSON, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

