"""
Tests for ProviderService
"""
import pytest
from unittest.mock import MagicMock, AsyncMock
from app.database.models import Provider, ProviderType
from app.services.provider_service import ProviderService
from app.providers.base import BaseProvider
from app.auth.encryption import EncryptionService


def test_provider_service_load_all_providers_empty(db_session):
    """Test loading providers when database is empty"""
    service = ProviderService(db_session)
    providers = service.load_all_providers()
    
    assert providers == {}


def test_provider_service_load_all_providers(db_session):
    """Test loading all active providers from database"""
    api_key = "test-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider1 = Provider(
        name="Ninja Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        base_url="https://api.ninja.test",
        is_active=True
    )
    provider2 = Provider(
        name="Malwarebytes Provider",
        type=ProviderType.MALWAREBYTES.value,
        api_key_encrypted=encrypted_key,
        base_url="https://api.malwarebytes.test",
        is_active=True
    )
    provider3 = Provider(
        name="Inactive Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        is_active=False
    )
    
    db_session.add_all([provider1, provider2, provider3])
    db_session.commit()
    
    service = ProviderService(db_session)
    providers = service.load_all_providers(active_only=True)
    
    # Should only load active providers
    assert len(providers) == 2
    assert "Ninja Provider" in providers
    assert "Malwarebytes Provider" in providers
    assert "Inactive Provider" not in providers
    
    # Verify they are BaseProvider instances
    assert isinstance(providers["Ninja Provider"], BaseProvider)
    assert isinstance(providers["Malwarebytes Provider"], BaseProvider)


def test_provider_service_load_all_providers_including_inactive(db_session):
    """Test loading all providers including inactive ones"""
    api_key = "test-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider1 = Provider(
        name="Active Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        is_active=True
    )
    provider2 = Provider(
        name="Inactive Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        is_active=False
    )
    
    db_session.add_all([provider1, provider2])
    db_session.commit()
    
    service = ProviderService(db_session)
    providers = service.load_all_providers(active_only=False)
    
    assert len(providers) == 2


def test_provider_service_load_provider_by_guid(db_session):
    """Test loading a specific provider by GUID"""
    api_key = "test-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        base_url="https://api.test.com"
    )
    db_session.add(provider)
    db_session.commit()
    
    service = ProviderService(db_session)
    loaded = service.load_provider_by_guid(provider.guid)
    
    assert loaded is not None
    assert isinstance(loaded, BaseProvider)
    assert loaded.config.api_key == api_key
    assert loaded.config.base_url == "https://api.test.com"


def test_provider_service_load_provider_by_guid_not_found(db_session):
    """Test loading a provider that doesn't exist"""
    service = ProviderService(db_session)
    loaded = service.load_provider_by_guid("non-existent-guid")
    
    assert loaded is None


def test_provider_service_load_provider_with_config(db_session):
    """Test loading a provider with custom config"""
    api_key = "test-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    config = {
        "timeout": 60,
        "retries": 5
    }
    
    provider = Provider(
        name="Provider with Config",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        base_url="https://api.test.com",
        config=config
    )
    db_session.add(provider)
    db_session.commit()
    
    service = ProviderService(db_session)
    loaded = service.load_provider_by_guid(provider.guid)
    
    assert loaded is not None
    assert loaded.config.timeout == 60


def test_provider_service_load_provider_invalid_type(db_session):
    """Test loading a provider with unregistered type"""
    api_key = "test-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Invalid Provider",
        type="unknown_type",
        api_key_encrypted=encrypted_key
    )
    db_session.add(provider)
    db_session.commit()
    
    service = ProviderService(db_session)
    providers = service.load_all_providers()
    
    # Should skip invalid provider and continue
    assert "Invalid Provider" not in providers


def test_provider_service_load_provider_decryption_error(db_session):
    """Test handling decryption errors"""
    # Create provider with invalid encrypted key
    provider = Provider(
        name="Bad Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted="invalid-encrypted-data"
    )
    db_session.add(provider)
    db_session.commit()
    
    service = ProviderService(db_session)
    providers = service.load_all_providers()
    
    # Should skip provider with decryption error
    assert "Bad Provider" not in providers


def test_provider_service_get_provider_info(db_session):
    """Test getting provider information without decrypting"""
    api_key = "test-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        base_url="https://api.test.com",
        is_active=True
    )
    db_session.add(provider)
    db_session.commit()
    
    service = ProviderService(db_session)
    info = service.get_provider_info(provider.guid)
    
    assert info is not None
    assert info["guid"] == provider.guid
    assert info["name"] == "Test Provider"
    assert info["type"] == ProviderType.NINJA.value
    assert info["base_url"] == "https://api.test.com"
    assert info["is_active"] is True
    # API key should not be in info
    assert "api_key" not in info
    assert "api_key_encrypted" not in info


def test_provider_service_get_provider_info_not_found(db_session):
    """Test getting info for non-existent provider"""
    service = ProviderService(db_session)
    info = service.get_provider_info("non-existent-guid")
    
    assert info is None

