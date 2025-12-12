"""
Tests for cache key generation
"""
import pytest
from app.cache.cache_key import generate_cache_key


def test_generate_cache_key_basic():
    """Test basic cache key generation"""
    provider = "ninja"
    endpoint = "threats"
    params = {}
    
    key = generate_cache_key(provider, endpoint, params)
    
    assert key is not None
    assert isinstance(key, str)
    assert len(key) == 64  # SHA256 hex length


def test_generate_cache_key_with_params():
    """Test cache key generation with parameters"""
    provider = "ninja"
    endpoint = "threats"
    params1 = {"severity": "high", "status": "active"}
    params2 = {"severity": "high", "status": "active"}
    params3 = {"status": "active", "severity": "high"}  # Different order
    
    key1 = generate_cache_key(provider, endpoint, params1)
    key2 = generate_cache_key(provider, endpoint, params2)
    key3 = generate_cache_key(provider, endpoint, params3)
    
    # Same params should generate same key
    assert key1 == key2
    # Different order but same values should generate same key (if sorted)
    assert key1 == key3


def test_generate_cache_key_different_params():
    """Test that different parameters generate different keys"""
    provider = "ninja"
    endpoint = "threats"
    
    key1 = generate_cache_key(provider, endpoint, {"page": 1})
    key2 = generate_cache_key(provider, endpoint, {"page": 2})
    
    assert key1 != key2


def test_generate_cache_key_different_providers():
    """Test that different providers generate different keys"""
    endpoint = "threats"
    params = {}
    
    key1 = generate_cache_key("ninja", endpoint, params)
    key2 = generate_cache_key("malwarebytes", endpoint, params)
    
    assert key1 != key2


def test_generate_cache_key_different_endpoints():
    """Test that different endpoints generate different keys"""
    provider = "ninja"
    params = {}
    
    key1 = generate_cache_key(provider, "threats", params)
    key2 = generate_cache_key(provider, "devices", params)
    
    assert key1 != key2

