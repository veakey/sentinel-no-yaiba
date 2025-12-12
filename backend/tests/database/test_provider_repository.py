"""
Tests for ProviderRepository
"""
import pytest
from app.database.models import Provider, ProviderType
from app.database.repositories.provider_repository import ProviderRepository
from app.auth.encryption import EncryptionService


def test_provider_repository_get_by_guid(db_session):
    """Test getting a provider by GUID"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    db_session.add(provider)
    db_session.commit()
    
    repository = ProviderRepository(db_session)
    found = repository.get_by_guid(provider.guid)
    
    assert found is not None
    assert found.guid == provider.guid
    assert found.name == "Test Provider"


def test_provider_repository_get_by_guid_not_found(db_session):
    """Test getting a provider by GUID that doesn't exist"""
    repository = ProviderRepository(db_session)
    found = repository.get_by_guid("non-existent-guid")
    
    assert found is None


def test_provider_repository_get_by_id(db_session):
    """Test getting a provider by ID"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    db_session.add(provider)
    db_session.commit()
    
    repository = ProviderRepository(db_session)
    found = repository.get_by_id(provider.id)
    
    assert found is not None
    assert found.id == provider.id


def test_provider_repository_get_all(db_session):
    """Test getting all providers"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider1 = Provider(
        name="Provider 1",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        is_active=True
    )
    provider2 = Provider(
        name="Provider 2",
        type=ProviderType.MALWAREBYTES.value,
        api_key_encrypted=encrypted_key,
        is_active=True
    )
    provider3 = Provider(
        name="Provider 3",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        is_active=False
    )
    
    db_session.add_all([provider1, provider2, provider3])
    db_session.commit()
    
    repository = ProviderRepository(db_session)
    all_providers = repository.get_all()
    
    assert len(all_providers) == 3


def test_provider_repository_get_all_active_only(db_session):
    """Test getting only active providers"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider1 = Provider(
        name="Provider 1",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key,
        is_active=True
    )
    provider2 = Provider(
        name="Provider 2",
        type=ProviderType.MALWAREBYTES.value,
        api_key_encrypted=encrypted_key,
        is_active=False
    )
    
    db_session.add_all([provider1, provider2])
    db_session.commit()
    
    repository = ProviderRepository(db_session)
    active_providers = repository.get_all(active_only=True)
    
    assert len(active_providers) == 1
    assert active_providers[0].name == "Provider 1"


def test_provider_repository_get_by_type(db_session):
    """Test getting providers by type"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider1 = Provider(
        name="Ninja Provider 1",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    provider2 = Provider(
        name="Ninja Provider 2",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    provider3 = Provider(
        name="Malwarebytes Provider",
        type=ProviderType.MALWAREBYTES.value,
        api_key_encrypted=encrypted_key
    )
    
    db_session.add_all([provider1, provider2, provider3])
    db_session.commit()
    
    repository = ProviderRepository(db_session)
    ninja_providers = repository.get_by_type(ProviderType.NINJA.value)
    
    assert len(ninja_providers) == 2
    assert all(p.type == ProviderType.NINJA.value for p in ninja_providers)


def test_provider_repository_create(db_session):
    """Test creating a provider"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="New Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    
    repository = ProviderRepository(db_session)
    created = repository.create(provider)
    
    assert created.id is not None
    assert created.guid is not None
    assert created.name == "New Provider"


def test_provider_repository_update(db_session):
    """Test updating a provider"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Original Name",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    db_session.add(provider)
    db_session.commit()
    
    provider.name = "Updated Name"
    repository = ProviderRepository(db_session)
    updated = repository.update(provider)
    
    assert updated.name == "Updated Name"


def test_provider_repository_delete(db_session):
    """Test deleting a provider"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="To Delete",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    db_session.add(provider)
    db_session.commit()
    provider_id = provider.id
    
    repository = ProviderRepository(db_session)
    repository.delete(provider)
    
    # Verify it's deleted
    found = repository.get_by_id(provider_id)
    assert found is None


def test_provider_repository_exists(db_session):
    """Test checking if a provider exists"""
    api_key = "test-api-key"
    encrypted_key = EncryptionService.encrypt(api_key)
    
    provider = Provider(
        name="Test Provider",
        type=ProviderType.NINJA.value,
        api_key_encrypted=encrypted_key
    )
    db_session.add(provider)
    db_session.commit()
    
    repository = ProviderRepository(db_session)
    
    assert repository.exists(provider.guid) is True
    assert repository.exists("non-existent-guid") is False

