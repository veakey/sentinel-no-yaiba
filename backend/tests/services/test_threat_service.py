"""
Tests for ThreatService
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.threat_service import ThreatService
from app.cache.cache_manager import CacheManager
from app.cache.cache_key import generate_cache_key
from app.providers.base import ProviderConfig
from app.providers.ninja import NinjaProvider
from app.providers.malwarebytes import MalwarebytesProvider
from app.core.exceptions import ProviderException


@pytest.fixture
def cache_manager():
    """Fixture for CacheManager without DB"""
    return CacheManager(default_ttl=300, enable_db=False)


@pytest.fixture
def ninja_provider():
    """Fixture for Ninja provider"""
    config = ProviderConfig(api_key="ninja-test-key-12345678901234567890")
    return NinjaProvider(config)


@pytest.fixture
def malwarebytes_provider():
    """Fixture for Malwarebytes provider"""
    config = ProviderConfig(api_key="mb-test-key-12345678901234567890")
    return MalwarebytesProvider(config)


@pytest.fixture
def threat_service(cache_manager, ninja_provider, malwarebytes_provider):
    """Fixture for ThreatService"""
    providers = {
        "ninja": ninja_provider,
        "malwarebytes": malwarebytes_provider
    }
    return ThreatService(cache_manager=cache_manager, providers=providers)


@pytest.mark.asyncio
async def test_threat_service_fetch_from_single_provider(threat_service, ninja_provider):
    """Test fetching threats from a single provider"""
    mock_response = {
        "data": [{"id": "threat-1", "name": "Test Threat"}],
        "meta": {"total": 1}
    }
    
    with patch.object(ninja_provider, 'fetch_threats', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_response
        
        result = await threat_service._fetch_from_provider("ninja", {})
        
        assert result == mock_response
        mock_fetch.assert_called_once_with({})


@pytest.mark.asyncio
async def test_threat_service_aggregate_from_multiple_providers(threat_service):
    """Test aggregating threats from multiple providers"""
    ninja_data = {
        "data": [{"id": "n1", "provider": "ninja", "severity": "high"}],
        "meta": {"total": 1}
    }
    mb_data = {
        "results": [{"id": "m1", "provider": "malwarebytes", "severity": "critical"}],
        "count": 1
    }
    
    providers = threat_service.providers
    
    with patch.object(providers["ninja"], 'fetch_threats', new_callable=AsyncMock) as mock_ninja:
        with patch.object(providers["malwarebytes"], 'fetch_threats', new_callable=AsyncMock) as mock_mb:
            mock_ninja.return_value = ninja_data
            mock_mb.return_value = mb_data
            
            result = await threat_service.get_threats()
            
            # Should aggregate both providers
            assert "ninja" in result
            assert "malwarebytes" in result
            assert result["ninja"] == ninja_data
            assert result["malwarebytes"] == mb_data


@pytest.mark.asyncio
async def test_threat_service_uses_cache(threat_service, cache_manager):
    """Test that ThreatService uses cache for instant responses"""
    cache_key = generate_cache_key("all", "threats", {})
    cached_data = {
        "ninja": {"data": [{"id": "cached-1"}]},
        "malwarebytes": {"results": [{"id": "cached-2"}]}
    }
    
    # Pre-populate cache
    cache_manager.set(cache_key, cached_data, ttl=600)
    
    # Should return cached data immediately
    result = await threat_service.get_threats(force_refresh=False)
    
    assert result == cached_data
    
    # Providers should not be called
    with patch.object(threat_service.providers["ninja"], 'fetch_threats') as mock_ninja:
        result = await threat_service.get_threats(force_refresh=False)
        mock_ninja.assert_not_called()


@pytest.mark.asyncio
async def test_threat_service_force_refresh_bypasses_cache(threat_service):
    """Test that force_refresh bypasses cache and fetches fresh data"""
    cache_key = generate_cache_key("all", "threats", {})
    cached_data = {"ninja": {"data": [{"id": "old"}]}}
    
    # Pre-populate cache
    threat_service.cache_manager.set(cache_key, cached_data, ttl=600)
    
    fresh_data = {
        "ninja": {"data": [{"id": "new"}]},
        "malwarebytes": {"results": [{"id": "new2"}]}
    }
    
    providers = threat_service.providers
    
    with patch.object(providers["ninja"], 'fetch_threats', new_callable=AsyncMock) as mock_ninja:
        with patch.object(providers["malwarebytes"], 'fetch_threats', new_callable=AsyncMock) as mock_mb:
            mock_ninja.return_value = fresh_data["ninja"]
            mock_mb.return_value = fresh_data["malwarebytes"]
            
            result = await threat_service.get_threats(force_refresh=True)
            
            # Should return fresh data, not cached
            assert result["ninja"]["data"][0]["id"] == "new"
            mock_ninja.assert_called_once()
            mock_mb.assert_called_once()


@pytest.mark.asyncio
async def test_threat_service_handles_provider_failure(threat_service):
    """Test that ThreatService continues if one provider fails"""
    providers = threat_service.providers
    
    with patch.object(providers["ninja"], 'fetch_threats', new_callable=AsyncMock) as mock_ninja:
        with patch.object(providers["malwarebytes"], 'fetch_threats', new_callable=AsyncMock) as mock_mb:
            # One provider fails
            mock_ninja.side_effect = ProviderException("Provider error")
            mock_mb.return_value = {"results": [{"id": "m1"}]}
            
            result = await threat_service.get_threats()
            
            # Should still return data from working provider
            assert "malwarebytes" in result
            assert "ninja" in result  # But with error info
            assert "error" in result["ninja"] or result["ninja"] is None


@pytest.mark.asyncio
async def test_threat_service_caches_fresh_data(threat_service, cache_manager):
    """Test that fresh data is stored in cache"""
    cache_key = generate_cache_key("all", "threats", {})
    fresh_data = {
        "ninja": {"data": [{"id": "fresh"}]},
        "malwarebytes": {"results": [{"id": "fresh2"}]}
    }
    
    providers = threat_service.providers
    
    with patch.object(providers["ninja"], 'fetch_threats', new_callable=AsyncMock) as mock_ninja:
        with patch.object(providers["malwarebytes"], 'fetch_threats', new_callable=AsyncMock) as mock_mb:
            mock_ninja.return_value = fresh_data["ninja"]
            mock_mb.return_value = fresh_data["malwarebytes"]
            
            # Fetch fresh data
            await threat_service.get_threats(force_refresh=True)
            
            # Verify it's in cache
            cached = cache_manager.get(cache_key)
            assert cached is not None
            assert cached["ninja"] == fresh_data["ninja"]

