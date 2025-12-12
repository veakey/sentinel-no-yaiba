"""
Multi-level cache manager (memory + SQLite)
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict
from app.cache.cache_key import generate_cache_key


class CacheManager:
    """
    Multi-level cache manager with memory cache and optional database persistence.
    
    Level 1: In-memory cache (fast, lost on restart)
    Level 2: SQLite cache (persistent, slower but survives restarts)
    """
    
    def __init__(self, default_ttl: int = 300, enable_db: bool = False):
        """
        Initialize cache manager.
        
        Args:
            default_ttl: Default TTL in seconds (default: 5 minutes)
            enable_db: Whether to enable SQLite cache layer
        """
        self._memory_cache: Dict[str, tuple] = {}  # {key: (data, expires_at)}
        self.default_ttl = default_ttl
        self.enable_db = enable_db
        self.db_cache = None  # Will be set if enable_db is True
    
    def set(self, cache_key: str, data: Any, ttl: Optional[int] = None):
        """
        Store data in cache (memory + DB if enabled).
        
        Args:
            cache_key: Cache key
            data: Data to cache
            ttl: Time to live in seconds (uses default if not provided)
        """
        ttl = ttl or self.default_ttl
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
        
        # Level 1: Memory cache
        self._memory_cache[cache_key] = (data, expires_at)
        
        # Level 2: DB cache (if enabled)
        if self.enable_db and self.db_cache:
            self.db_cache.set(cache_key, data, expires_at)
    
    def get(self, cache_key: str) -> Optional[Any]:
        """
        Retrieve data from cache (memory first, then DB if enabled).
        
        Args:
            cache_key: Cache key to retrieve
            
        Returns:
            Cached data or None if not found or expired
        """
        now = datetime.now(timezone.utc)
        
        # Level 1: Check memory cache
        if cache_key in self._memory_cache:
            data, expires_at = self._memory_cache[cache_key]
            if now < expires_at:
                return data
            else:
                # Expired, remove from memory
                del self._memory_cache[cache_key]
        
        # Level 2: Check DB cache (if enabled)
        if self.enable_db and self.db_cache:
            db_entry = self.db_cache.get(cache_key)
            if db_entry:
                # Ensure expires_at is timezone-aware for comparison
                expires_at = db_entry.expires_at
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                
                if expires_at > now:
                    # Re-inject into memory cache
                    self.set(
                        cache_key, 
                        db_entry.response_data,
                        ttl=int((expires_at - now).total_seconds())
                    )
                    return db_entry.response_data
                else:
                    # Expired, remove from DB
                    self.db_cache.delete(cache_key)
        
        return None
    
    def clear(self):
        """Clear all cache entries from memory."""
        self._memory_cache.clear()
        if self.enable_db and self.db_cache:
            self.db_cache.clear_all()
    
    def invalidate_pattern(self, pattern: str):
        """
        Invalidate cache entries matching a pattern.
        
        Args:
            pattern: Pattern to match in cache keys
        """
        keys_to_remove = [
            key for key in self._memory_cache.keys()
            if pattern in key
        ]
        for key in keys_to_remove:
            del self._memory_cache[key]
        
        if self.enable_db and self.db_cache:
            self.db_cache.invalidate_pattern(pattern)

