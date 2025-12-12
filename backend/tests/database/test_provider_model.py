"""
Tests for Provider model
"""
import pytest
from app.database.models import Provider, ProviderType, CacheEntry
from app.auth.encryption import EncryptionService


def test_provider_creation(db_session):
    """Test creating a provider"""
    api_key = "test-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Ninja Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        base_url="https://api.ninja.test",
        is_active=True
    )
    
    db_session.add(provider)
    db_session.commit()
    
    assert provider.id is not None
    assert provider.guid is not None
    assert provider.name == "Test Ninja Provider"
    assert provider.type == ProviderType.NINJA.value
    assert provider.api_key_encrypted == encrypted_key
    assert provider.base_url == "https://api.ninja.test"
    assert provider.is_active is True
    assert provider.created_at is not None
    assert provider.updated_at is not None


def test_provider_with_config(db_session):
    """Test creating a provider with JSON config"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    config = {
        "timeout": 60,
        "retries": 3,
        "custom_setting": "value"
    }
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.MALWAREBYTES.value,
        api_key_encrypted=encrypted_key,
        config=config
    )
    
    db_session.add(provider)
    db_session.commit()
    
    assert provider.config == config
    assert provider.config["timeout"] == 60


def test_provider_with_provider_specific_settings(db_session):
    """Test creating a provider with provider-specific settings"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    settings = {
        "organization_id": "org-123",
        "region": "us-east-1"
    }
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        provider_specific_settings=settings
    )
    
    db_session.add(provider)
    db_session.commit()
    
    assert provider.provider_specific_settings == settings


def test_provider_default_is_active(db_session):
    """Test that is_active defaults to True"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    
    db_session.add(provider)
    db_session.commit()
    
    assert provider.is_active is True


def test_provider_relationship_cache_entries(db_session):
    """Test Provider relationship with CacheEntry"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    
    db_session.add(provider)
    db_session.commit()
    
    # Create cache entry linked to provider
    from datetime import datetime, timedelta, timezone
    cache_entry = CacheEntry(
        provider_id=provider.id,
        cache_key="test-cache-key-123",
        response_data={"threats": []},
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    
    db_session.add(cache_entry)
    db_session.commit()
    
    # Test relationship
    assert len(provider.cache_entries) == 1
    assert provider.cache_entries[0].cache_key == "test-cache-key-123"
    assert cache_entry.provider.id == provider.id


def test_provider_api_key_encryption(db_session):
    """Test that API key is properly encrypted"""
    api_key = "super-secret-api-key-12345"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    
    db_session.add(provider)
    db_session.commit()
    
    # Verify encrypted key is different from plaintext
    assert provider.api_key_encrypted != api_key
    assert len(provider.api_key_encrypted) > len(api_key)
    
    # Verify we can decrypt it
    decrypted = EncryptionService.decrypt(provider.api_key_encrypted)
    assert decrypted == api_key


def test_provider_unique_guid(db_session):
    """Test that each provider has a unique GUID"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider1 = Provider(
        name="Provider 1",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    
    provider2 = Provider(
        name="Provider 2",
        type=ProviderType.MALWAREBYTES.value,
        api_key_encrypted=encrypted_key
    )
    
    db_session.add_all([provider1, provider2])
    db_session.commit()
    
    assert provider1.guid != provider2.guid
    assert len(provider1.guid) == 36  # UUID format


def test_provider_cascade_delete_cache_entries(db_session):
    """Test that deleting a provider cascades to cache entries"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    
    db_session.add(provider)
    db_session.commit()
    
    # Create cache entries
    from datetime import datetime, timedelta, timezone
    cache_entry1 = CacheEntry(
        provider_id=provider.id,
        cache_key="cache-1",
        response_data={},
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    cache_entry2 = CacheEntry(
        provider_id=provider.id,
        cache_key="cache-2",
        response_data={},
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    
    db_session.add_all([cache_entry1, cache_entry2])
    db_session.commit()
    
    # Delete provider
    db_session.delete(provider)
    db_session.commit()
    
    # Verify cache entries are deleted
    assert db_session.query(CacheEntry).count() == 0

