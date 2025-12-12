"""
Integration tests for ProviderFactory with registered providers
"""
import pytest
# Import providers module to trigger registration
import app.providers  # noqa: F401
from app.providers.factory import ProviderFactory, ProviderType
from app.providers.base import ProviderConfig


def test_factory_has_ninja_provider_registered():
    """Test that Ninja provider is registered in the factory"""
    # Re-register in case previous tests cleared it
    import app.providers  # noqa: F401
    assert ProviderFactory.is_registered(ProviderType.NINJA.value)


def test_factory_can_create_ninja_provider():
    """Test that factory can create Ninja provider instance"""
    # Re-register in case previous tests cleared it
    import app.providers  # noqa: F401
    config = ProviderConfig(api_key="ninja-test-key-12345678901234567890")
    
    provider = ProviderFactory.create(ProviderType.NINJA.value, config)
    
    from app.providers.ninja import NinjaProvider
    assert isinstance(provider, NinjaProvider)
    assert provider.config == config

