"""
Repository for cache entries
"""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models import CacheEntry


class CacheRepository:
    """Repository for managing cache entries in database"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, cache_key: str) -> Optional[CacheEntry]:
        """
        Get a cache entry by key if not expired.
        
        Args:
            cache_key: Cache key to retrieve
            
        Returns:
            CacheEntry if found and not expired, None otherwise
        """
        now = datetime.now(timezone.utc)
        entry = self.db.query(CacheEntry).filter(
            CacheEntry.cache_key == cache_key
        ).first()
        
        if entry and entry.expires_at:
            # Ensure expires_at is timezone-aware for comparison
            if entry.expires_at.tzinfo is None:
                # If naive, assume UTC
                expires_at = entry.expires_at.replace(tzinfo=timezone.utc)
            else:
                expires_at = entry.expires_at
            
            if expires_at > now:
                return entry
            else:
                # Expired, delete it
                self.delete(cache_key)
                return None
        
        return None
    
    def set(self, cache_key: str, data: dict, expires_at: datetime):
        """
        Store a cache entry.
        
        Args:
            cache_key: Cache key
            data: Response data to cache
            expires_at: Expiration timestamp
        """
        # Check if entry exists
        existing = self.db.query(CacheEntry).filter(
            CacheEntry.cache_key == cache_key
        ).first()
        
        if existing:
            # Update existing
            existing.response_data = data
            existing.expires_at = expires_at
            existing.updated_at = datetime.now(timezone.utc)
        else:
            # Create new
            entry = CacheEntry(
                cache_key=cache_key,
                response_data=data,
                expires_at=expires_at
            )
            self.db.add(entry)
        
        self.db.commit()
    
    def delete(self, cache_key: str):
        """Delete a cache entry by key."""
        entry = self.db.query(CacheEntry).filter(
            CacheEntry.cache_key == cache_key
        ).first()
        if entry:
            self.db.delete(entry)
            self.db.commit()
    
    def clear_all(self):
        """Clear all cache entries."""
        self.db.query(CacheEntry).delete()
        self.db.commit()
    
    def invalidate_pattern(self, pattern: str):
        """
        Delete cache entries matching a pattern.
        
        Args:
            pattern: Pattern to match in cache_key
        """
        entries = self.db.query(CacheEntry).filter(
            CacheEntry.cache_key.like(f"%{pattern}%")
        ).all()
        for entry in entries:
            self.db.delete(entry)
        self.db.commit()

