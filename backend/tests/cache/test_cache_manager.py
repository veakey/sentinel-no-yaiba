"""
Tests for CacheManager
"""
import pytest
from datetime import datetime, timedelta, timezone
from app.cache.cache_manager import CacheManager
from app.cache.cache_key import generate_cache_key


@pytest.fixture
def cache_manager():
    """Fixture for CacheManager without DB"""
    return CacheManager(default_ttl=300, enable_db=False)


def test_cache_manager_initialization(cache_manager):
    """Test that CacheManager initializes correctly"""
    assert cache_manager.default_ttl == 300
    assert cache_manager._memory_cache == {}


def test_cache_manager_set_and_get(cache_manager):
    """Test setting and getting from cache"""
    cache_key = "test_key_12345"
    data = {"test": "data"}
    
    # Set cache
    cache_manager.set(cache_key, data, ttl=600)
    
    # Get cache
    result = cache_manager.get(cache_key)
    
    assert result == data


def test_cache_manager_get_miss(cache_manager):
    """Test getting non-existent cache entry"""
    result = cache_manager.get("non_existent_key")
    
    assert result is None


def test_cache_manager_ttl_expiration(cache_manager):
    """Test that cache entries expire after TTL"""
    cache_key = "test_key_expired"
    data = {"test": "data"}
    
    # Set with very short TTL
    cache_manager.set(cache_key, data, ttl=1)
    
    # Should be available immediately
    result = cache_manager.get(cache_key)
    assert result == data
    
    # Wait for expiration (in real scenario, we'd mock time)
    # For now, we'll test by manually expiring
    cache_manager._memory_cache[cache_key] = (
        data, 
        datetime.now(timezone.utc) - timedelta(seconds=10)
    )
    
    # Should be None after expiration
    result = cache_manager.get(cache_key)
    assert result is None


def test_cache_manager_default_ttl(cache_manager):
    """Test that default TTL is used when not specified"""
    cache_key = "test_key_default_ttl"
    data = {"test": "data"}
    
    cache_manager.set(cache_key, data)
    
    # Entry should exist
    result = cache_manager.get(cache_key)
    assert result == data
    
    # Check that expiration is set with default TTL
    entry_data, expires_at = cache_manager._memory_cache[cache_key]
    expected_expiry = datetime.now(timezone.utc) + timedelta(seconds=300)
    
    # Allow 1 second tolerance
    time_diff = abs((expires_at - expected_expiry).total_seconds())
    assert time_diff < 2


def test_cache_manager_clear(cache_manager):
    """Test clearing cache"""
    cache_manager.set("key1", {"data": 1})
    cache_manager.set("key2", {"data": 2})
    
    assert cache_manager.get("key1") is not None
    assert cache_manager.get("key2") is not None
    
    cache_manager.clear()
    
    assert cache_manager.get("key1") is None
    assert cache_manager.get("key2") is None


def test_cache_manager_invalidate_pattern(cache_manager):
    """Test invalidating cache entries by pattern"""
    cache_manager.set("ninja_threats", {"data": 1})
    cache_manager.set("ninja_devices", {"data": 2})
    cache_manager.set("malwarebytes_threats", {"data": 3})
    
    # Invalidate all ninja entries
    cache_manager.invalidate_pattern("ninja")
    
    assert cache_manager.get("ninja_threats") is None
    assert cache_manager.get("ninja_devices") is None
    assert cache_manager.get("malwarebytes_threats") is not None

