"""
Tests for BaseProvider abstract interface
"""
import pytest
from abc import ABC
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock

from app.providers.base import BaseProvider, ProviderConfig


def test_provider_config_validation():
    """Test that ProviderConfig validates API key"""
    # Valid config
    config = ProviderConfig(api_key="valid-api-key-1234567890")
    assert config.api_key == "valid-api-key-1234567890"
    
    # Invalid config - too short
    with pytest.raises(ValueError, match="API key invalide"):
        ProviderConfig(api_key="short")


def test_base_provider_is_abstract():
    """Test that BaseProvider cannot be instantiated directly"""
    with pytest.raises(TypeError):
        BaseProvider(config=ProviderConfig(api_key="test-key-1234567890"))


def test_base_provider_has_required_methods():
    """Test that BaseProvider defines required abstract methods"""
    # Check that BaseProvider is an ABC
    assert issubclass(BaseProvider, ABC)
    
    # Check that fetch_threats is abstract
    assert hasattr(BaseProvider, 'fetch_threats')
    
    # Check that health_check exists (not abstract, has default implementation)
    assert hasattr(BaseProvider, 'health_check')


def test_base_provider_config_storage():
    """Test that BaseProvider stores configuration"""
    class TestProvider(BaseProvider):
        async def fetch_threats(self, params: Dict[str, Any]) -> Dict[str, Any]:
            return {}
    
    config = ProviderConfig(api_key="test-key-1234567890")
    provider = TestProvider(config)
    
    assert provider.config == config
    assert provider.config.api_key == "test-key-1234567890"


def test_base_provider_validate_config():
    """Test that BaseProvider validates config on initialization"""
    class TestProvider(BaseProvider):
        def validate_config(self):
            if not self.config.api_key.startswith("test-"):
                raise ValueError("API key must start with 'test-'")
        
        async def fetch_threats(self, params: Dict[str, Any]) -> Dict[str, Any]:
            return {}
    
    # Valid config
    config = ProviderConfig(api_key="test-valid-key-1234567890")
    provider = TestProvider(config)
    assert provider is not None
    
    # Invalid config (will fail custom validation)
    config = ProviderConfig(api_key="invalid-key-1234567890")
    with pytest.raises(ValueError, match="API key must start with 'test-'"):
        TestProvider(config)

