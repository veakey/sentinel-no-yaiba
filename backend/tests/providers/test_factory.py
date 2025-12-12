"""
Tests for Provider Factory pattern
"""
import pytest
from app.providers.factory import ProviderFactory, ProviderType
from app.providers.base import BaseProvider, ProviderConfig
from app.core.exceptions import ProviderException


def test_provider_factory_registers_provider():
    """Test that ProviderFactory can register a provider type"""
    class TestProvider(BaseProvider):
        async def fetch_threats(self, params):
            return {}
    
    ProviderFactory.register("test", TestProvider)
    
    # Verify it's registered
    assert ProviderFactory.is_registered("test")
    assert not ProviderFactory.is_registered("unknown")


def test_provider_factory_creates_provider():
    """Test that ProviderFactory creates provider instances"""
    class TestProvider(BaseProvider):
        async def fetch_threats(self, params):
            return {"test": "data"}
    
    ProviderFactory.register("test", TestProvider)
    
    config = ProviderConfig(api_key="test-key-1234567890")
    provider = ProviderFactory.create("test", config)
    
    assert isinstance(provider, TestProvider)
    assert provider.config == config


def test_provider_factory_raises_for_unknown_type():
    """Test that ProviderFactory raises exception for unknown provider type"""
    config = ProviderConfig(api_key="test-key-1234567890")
    
    with pytest.raises(ProviderException, match="Unknown provider type"):
        ProviderFactory.create("unknown_provider", config)


def test_provider_factory_list_registered():
    """Test that ProviderFactory can list registered providers"""
    class Provider1(BaseProvider):
        async def fetch_threats(self, params):
            return {}
    
    class Provider2(BaseProvider):
        async def fetch_threats(self, params):
            return {}
    
    # Save existing registrations
    original_providers = ProviderFactory._providers.copy()
    
    try:
        # Clear any existing registrations for this test
        ProviderFactory._providers.clear()
        
        ProviderFactory.register("provider1", Provider1)
        ProviderFactory.register("provider2", Provider2)
        
        registered = ProviderFactory.list_registered()
        
        assert "provider1" in registered
        assert "provider2" in registered
        assert len(registered) >= 2
    finally:
        # Restore original registrations
        ProviderFactory._providers.clear()
        ProviderFactory._providers.update(original_providers)


def test_provider_factory_enum_types():
    """Test that ProviderType enum works correctly"""
    # Check that known types exist
    assert hasattr(ProviderType, 'NINJA')
    assert hasattr(ProviderType, 'MALWAREBYTES')
    
    # Check that enum values are strings
    assert isinstance(ProviderType.NINJA.value, str)
    assert isinstance(ProviderType.MALWAREBYTES.value, str)

