"""
Tests for ThreatService WebSocket integration
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.threat_service import ThreatService
from app.cache.cache_manager import CacheManager
from app.websocket.manager import WebSocketManager
from app.providers.base import ProviderConfig
from app.providers.ninja import NinjaProvider


@pytest.fixture
def cache_manager():
    """Fixture for CacheManager"""
    return CacheManager(default_ttl=300, enable_db=False)


@pytest.fixture
def ws_manager():
    """Fixture for WebSocketManager"""
    return WebSocketManager()


@pytest.fixture
def ninja_provider():
    """Fixture for Ninja provider"""
    config = ProviderConfig(api_key="ninja-test-key-12345678901234567890")
    return NinjaProvider(config)


@pytest.fixture
def threat_service_with_ws(cache_manager, ninja_provider, ws_manager):
    """Fixture for ThreatService with WebSocket manager"""
    providers = {"ninja": ninja_provider}
    service = ThreatService(cache_manager=cache_manager, providers=providers)
    service.websocket_manager = ws_manager
    return service


@pytest.mark.asyncio
async def test_threat_service_broadcasts_on_fresh_fetch(threat_service_with_ws, ws_manager):
    """Test that ThreatService broadcasts WebSocket message after fetching fresh data"""
    fresh_data = {
        "ninja": {"data": [{"id": "threat-1"}]}
    }
    
    providers = threat_service_with_ws.providers
    
    with patch.object(providers["ninja"], 'fetch_threats', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = fresh_data["ninja"]
        
        # Mock broadcast to capture calls
        with patch.object(ws_manager, 'broadcast', new_callable=AsyncMock) as mock_broadcast:
            result = await threat_service_with_ws.get_threats(force_refresh=True)
            
            # Should fetch and return data
            assert result == fresh_data
            
            # Should broadcast update via WebSocket
            mock_broadcast.assert_called_once()
            call_args = mock_broadcast.call_args
            broadcast_message = call_args[0][0]
            assert broadcast_message["type"] == "threats_updated"
            assert "data" in broadcast_message


@pytest.mark.asyncio
async def test_threat_service_no_broadcast_on_cached_data(threat_service_with_ws, cache_manager, ws_manager):
    """Test that ThreatService does not broadcast when returning cached data"""
    from app.cache.cache_key import generate_cache_key
    
    cached_data = {
        "ninja": {"data": [{"id": "cached"}]}
    }
    
    # Pre-populate cache
    cache_key = generate_cache_key("all", "threats", {})
    cache_manager.set(cache_key, cached_data, ttl=600)
    
    # Mock broadcast
    with patch.object(ws_manager, 'broadcast', new_callable=AsyncMock) as mock_broadcast:
        result = await threat_service_with_ws.get_threats(force_refresh=False)
        
        # Should return cached data
        assert result == cached_data
        
        # Should NOT broadcast (data is from cache, not fresh)
        mock_broadcast.assert_not_called()


@pytest.mark.asyncio
async def test_threat_service_broadcast_includes_data(threat_service_with_ws, ws_manager):
    """Test that broadcast message includes the threat data"""
    ninja_data = {"data": [{"id": "threat-1", "severity": "high"}]}
    expected_aggregated = {
        "ninja": ninja_data
    }
    
    providers = threat_service_with_ws.providers
    
    with patch.object(providers["ninja"], 'fetch_threats', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = ninja_data
        
        with patch.object(ws_manager, 'broadcast', new_callable=AsyncMock) as mock_broadcast:
            await threat_service_with_ws.get_threats(force_refresh=True)
            
            call_args = mock_broadcast.call_args
            broadcast_message = call_args[0][0]
            
            assert broadcast_message["type"] == "threats_updated"
            assert broadcast_message["data"] == expected_aggregated

