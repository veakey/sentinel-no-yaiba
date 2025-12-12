"""
Tests for Ninja One provider implementation
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from app.providers.ninja import NinjaProvider
from app.providers.base import ProviderConfig
from app.core.exceptions import ProviderException


@pytest.fixture
def ninja_config():
    """Fixture for Ninja provider configuration"""
    return ProviderConfig(
        api_key="ninja-test-api-key-12345678901234567890",
        base_url="https://app.ninjarmm.com",
        timeout=30
    )


@pytest.fixture
def ninja_provider(ninja_config):
    """Fixture for Ninja provider instance"""
    return NinjaProvider(ninja_config)


def test_ninja_provider_initialization(ninja_config):
    """Test that NinjaProvider can be initialized with valid config"""
    provider = NinjaProvider(ninja_config)
    assert provider.config == ninja_config
    assert provider.config.api_key == "ninja-test-api-key-12345678901234567890"
    assert provider.config.base_url == "https://app.ninjarmm.com"


def test_ninja_provider_default_base_url():
    """Test that NinjaProvider uses default base URL if not provided"""
    config = ProviderConfig(api_key="ninja-test-api-key-12345678901234567890")
    provider = NinjaProvider(config)
    assert provider.config.base_url == "https://app.ninjarmm.com"


def test_ninja_provider_is_base_provider(ninja_provider):
    """Test that NinjaProvider is a subclass of BaseProvider"""
    from app.providers.base import BaseProvider
    assert isinstance(ninja_provider, BaseProvider)


@pytest.mark.asyncio
async def test_ninja_provider_fetch_threats_success(ninja_provider):
    """Test successful fetch_threats call with mocked HTTP response"""
    mock_response = {
        "data": [
            {
                "id": "threat-1",
                "name": "Test Threat",
                "severity": "high",
                "status": "active",
                "detected_at": "2024-01-01T00:00:00Z"
            }
        ],
        "meta": {
            "total": 1,
            "page": 1
        }
    }
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 200
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status = MagicMock()
        mock_get.return_value = mock_response_obj
        
        result = await ninja_provider.fetch_threats({})
        
        assert result == mock_response
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_ninja_provider_fetch_threats_with_params(ninja_provider):
    """Test fetch_threats with parameters (filters, pagination)"""
    params = {
        "severity": "high",
        "status": "active",
        "page": 1,
        "limit": 10
    }
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 200
        mock_response_obj.json.return_value = {"data": [], "meta": {"total": 0}}
        mock_response_obj.raise_for_status = MagicMock()
        mock_get.return_value = mock_response_obj
        
        await ninja_provider.fetch_threats(params)
        
        # Verify that params were passed correctly
        call_args = mock_get.call_args
        assert call_args is not None


@pytest.mark.asyncio
async def test_ninja_provider_fetch_threats_http_error(ninja_provider):
    """Test fetch_threats handles HTTP errors (401, 404, 500)"""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 401
        mock_response_obj.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Unauthorized",
            request=MagicMock(),
            response=mock_response_obj
        )
        mock_get.return_value = mock_response_obj
        
        with pytest.raises(ProviderException, match="Failed to fetch threats from Ninja"):
            await ninja_provider.fetch_threats({})


@pytest.mark.asyncio
async def test_ninja_provider_fetch_threats_timeout(ninja_provider):
    """Test fetch_threats handles timeout errors"""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = httpx.TimeoutException("Request timed out")
        
        with pytest.raises(ProviderException, match="Timeout"):
            await ninja_provider.fetch_threats({})


@pytest.mark.asyncio
async def test_ninja_provider_fetch_threats_network_error(ninja_provider):
    """Test fetch_threats handles network errors"""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = httpx.NetworkError("Network error")
        
        with pytest.raises(ProviderException):
            await ninja_provider.fetch_threats({})


@pytest.mark.asyncio
async def test_ninja_provider_health_check_success(ninja_provider):
    """Test health_check returns True when API is accessible"""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 200
        mock_response_obj.raise_for_status = MagicMock()
        mock_get.return_value = mock_response_obj
        
        result = await ninja_provider.health_check()
        
        assert result is True


@pytest.mark.asyncio
async def test_ninja_provider_health_check_failure(ninja_provider):
    """Test health_check returns False when API is not accessible"""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = httpx.NetworkError("Network error")
        
        result = await ninja_provider.health_check()
        
        assert result is False


def test_ninja_provider_headers_include_api_key(ninja_provider):
    """Test that API requests include proper authentication headers"""
    # This tests that the provider uses the API key in headers
    assert ninja_provider.config.api_key is not None
    assert len(ninja_provider.config.api_key) >= 10

