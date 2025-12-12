"""
Integration tests for cache with database
"""
import pytest
from datetime import datetime, timedelta, timezone
from app.cache.cache_manager import CacheManager
from app.cache.cache_key import generate_cache_key
from app.database.repositories.cache_repository import CacheRepository


@pytest.fixture
def cache_repo(db_session):
    """Fixture for CacheRepository"""
    return CacheRepository(db_session)


@pytest.fixture
def cache_manager_with_db(cache_repo):
    """Fixture for CacheManager with DB enabled"""
    manager = CacheManager(default_ttl=300, enable_db=True)
    manager.db_cache = cache_repo
    return manager


def test_cache_manager_with_db_set_and_get(cache_manager_with_db):
    """Test cache manager with database persistence"""
    cache_key = "test_key_db_12345"
    data = {"test": "data_from_db"}
    
    # Set in cache (should go to both memory and DB)
    cache_manager_with_db.set(cache_key, data, ttl=600)
    
    # Clear memory cache to force DB lookup
    cache_manager_with_db._memory_cache.clear()
    
    # Should retrieve from DB
    result = cache_manager_with_db.get(cache_key)
    
    assert result == data


def test_cache_manager_db_expiration(cache_manager_with_db, db_session):
    """Test that expired DB cache entries are not returned"""
    from app.database.models import CacheEntry
    
    cache_key = "test_key_expired_db"
    expired_time = datetime.now(timezone.utc) - timedelta(seconds=10)
    
    # Create expired entry directly in DB
    entry = CacheEntry(
        cache_key=cache_key,
        response_data={"test": "expired_data"},
        expires_at=expired_time
    )
    db_session.add(entry)
    db_session.commit()
    
    # Should not retrieve expired entry
    result = cache_manager_with_db.get(cache_key)
    
    assert result is None


def test_cache_repository_set_get(cache_repo):
    """Test CacheRepository set and get operations"""
    cache_key = "test_repo_key"
    data = {"test": "repository_data"}
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=300)
    
    # Set
    cache_repo.set(cache_key, data, expires_at)
    
    # Get
    entry = cache_repo.get(cache_key)
    
    assert entry is not None
    assert entry.response_data == data
    assert entry.cache_key == cache_key


def test_cache_repository_update_existing(cache_repo):
    """Test that CacheRepository updates existing entries"""
    cache_key = "test_update_key"
    data1 = {"test": "data1"}
    data2 = {"test": "data2"}
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=300)
    
    # Set first time
    cache_repo.set(cache_key, data1, expires_at)
    entry1 = cache_repo.get(cache_key)
    assert entry1.response_data == data1
    
    # Update
    new_expires_at = datetime.now(timezone.utc) + timedelta(seconds=600)
    cache_repo.set(cache_key, data2, new_expires_at)
    entry2 = cache_repo.get(cache_key)
    
    assert entry2.response_data == data2
    # Compare timestamps (SQLite may return naive datetimes)
    entry_expires = entry2.expires_at
    if entry_expires.tzinfo is None:
        entry_expires = entry_expires.replace(tzinfo=timezone.utc)
    # Allow 1 second tolerance for DB storage
    time_diff = abs((entry_expires - new_expires_at).total_seconds())
    assert time_diff < 2

