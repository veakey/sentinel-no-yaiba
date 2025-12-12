"""
Tests for admin provider routes
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.models import Provider, ProviderType, User, UserRole
from app.auth.password import hash_password
from app.auth.encryption import EncryptionService
from app.auth.jwt import create_access_token


@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing"""
    user = User(
        username="admin",
        email="admin@test.com",
        hashed_password=hash_password("admin123"),
        role=UserRole.ADMIN.value,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def client_user(db_session):
    """Create a client user for testing"""
    user = User(
        username="client",
        email="client@test.com",
        hashed_password=hash_password("client123"),
        role=UserRole.CLIENT.value,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_token(admin_user):
    """Create an admin access token"""
    token_data = {"sub": admin_user.guid}
    return create_access_token(token_data)


@pytest.fixture
def client_token(client_user):
    """Create a client access token"""
    token_data = {"sub": client_user.guid}
    return create_access_token(token_data)


@pytest.fixture
def test_provider(db_session):
    """Create a test provider"""
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
    db_session.refresh(provider)
    return provider


def test_list_providers_requires_auth(client):
    """Test that listing providers requires authentication"""
    response = client.get("/api/admin/providers")
    assert response.status_code == 401


def test_list_providers_requires_admin(client, client_token):
    """Test that listing providers requires admin role"""
    headers = {"Authorization": f"Bearer {client_token}"}
    response = client.get("/api/admin/providers", headers=headers)
    assert response.status_code == 403


def test_list_providers_success(client, db_session, admin_token, test_provider):
    """Test successful listing of providers"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/admin/providers", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(p["guid"] == test_provider.guid for p in data)


def test_list_providers_active_only(client, db_session, admin_token, test_provider):
    """Test listing only active providers"""
    # Create inactive provider
    api_key = "test-api-key-2"
    encrypted_key = EncryptionService.encrypt(api_key)
    inactive_provider = Provider(
        name="Inactive Provider",
        type=ProviderType.MALWAREBYTES.value,
        api_key_encrypted=encrypted_key,
        is_active=False
    )
    db_session.add(inactive_provider)
    db_session.commit()
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/admin/providers?active_only=true", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert all(p["is_active"] is True for p in data)
    assert not any(p["guid"] == inactive_provider.guid for p in data)


def test_get_provider_requires_auth(client, test_provider):
    """Test that getting a provider requires authentication"""
    response = client.get(f"/api/admin/providers/{test_provider.guid}")
    assert response.status_code == 401


def test_get_provider_requires_admin(client, client_token, test_provider):
    """Test that getting a provider requires admin role"""
    headers = {"Authorization": f"Bearer {client_token}"}
    response = client.get(f"/api/admin/providers/{test_provider.guid}", headers=headers)
    assert response.status_code == 403


def test_get_provider_success(client, admin_token, test_provider):
    """Test successful retrieval of a provider"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get(f"/api/admin/providers/{test_provider.guid}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["guid"] == test_provider.guid
    assert data["name"] == "Test Provider"
    assert data["type"] == ProviderType.NINJA.value


def test_get_provider_not_found(client, admin_token):
    """Test getting a non-existent provider"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/admin/providers/non-existent-guid", headers=headers)
    assert response.status_code == 404


def test_create_provider_requires_auth(client):
    """Test that creating a provider requires authentication"""
    response = client.post(
        "/api/admin/providers",
        json={
            "name": "New Provider",
            "type": "ninja",
            "api_key": "test-api-key-12345"
        }
    )
    assert response.status_code == 401


def test_create_provider_requires_admin(client, client_token):
    """Test that creating a provider requires admin role"""
    headers = {"Authorization": f"Bearer {client_token}"}
    response = client.post(
        "/api/admin/providers",
        headers=headers,
        json={
            "name": "New Provider",
            "type": "ninja",
            "api_key": "test-api-key-12345"
        }
    )
    assert response.status_code == 403


def test_create_provider_success(client, db_session, admin_token):
    """Test successful creation of a provider"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/api/admin/providers",
        headers=headers,
        json={
            "name": "New Provider",
            "type": "ninja",
            "api_key": "test-api-key-12345",
            "base_url": "https://api.test.com",
            "is_active": True
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Provider"
    assert data["type"] == "ninja"
    assert data["base_url"] == "https://api.test.com"
    assert "guid" in data
    assert "api_key" not in data  # API key should not be in response


def test_create_provider_invalid_type(client, admin_token):
    """Test creating a provider with invalid type"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/api/admin/providers",
        headers=headers,
        json={
            "name": "New Provider",
            "type": "invalid_type",
            "api_key": "test-api-key-12345"
        }
    )
    assert response.status_code == 422  # Validation error


def test_create_provider_short_api_key(client, admin_token):
    """Test creating a provider with too short API key"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/api/admin/providers",
        headers=headers,
        json={
            "name": "New Provider",
            "type": "ninja",
            "api_key": "short"
        }
    )
    assert response.status_code == 422  # Validation error


def test_update_provider_requires_auth(client, test_provider):
    """Test that updating a provider requires authentication"""
    response = client.put(
        f"/api/admin/providers/{test_provider.guid}",
        json={"name": "Updated Name"}
    )
    assert response.status_code == 401


def test_update_provider_requires_admin(client, client_token, test_provider):
    """Test that updating a provider requires admin role"""
    headers = {"Authorization": f"Bearer {client_token}"}
    response = client.put(
        f"/api/admin/providers/{test_provider.guid}",
        headers=headers,
        json={"name": "Updated Name"}
    )
    assert response.status_code == 403


def test_update_provider_success(client, admin_token, test_provider):
    """Test successful update of a provider"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.put(
        f"/api/admin/providers/{test_provider.guid}",
        headers=headers,
        json={
            "name": "Updated Provider Name",
            "is_active": False
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Provider Name"
    assert data["is_active"] is False


def test_update_provider_not_found(client, admin_token):
    """Test updating a non-existent provider"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.put(
        "/api/admin/providers/non-existent-guid",
        headers=headers,
        json={"name": "Updated Name"}
    )
    assert response.status_code == 404


def test_delete_provider_requires_auth(client, test_provider):
    """Test that deleting a provider requires authentication"""
    response = client.delete(f"/api/admin/providers/{test_provider.guid}")
    assert response.status_code == 401


def test_delete_provider_requires_admin(client, client_token, test_provider):
    """Test that deleting a provider requires admin role"""
    headers = {"Authorization": f"Bearer {client_token}"}
    response = client.delete(f"/api/admin/providers/{test_provider.guid}", headers=headers)
    assert response.status_code == 403


def test_delete_provider_success(client, db_session, admin_token, test_provider):
    """Test successful deletion of a provider"""
    provider_guid = test_provider.guid
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete(f"/api/admin/providers/{provider_guid}", headers=headers)
    
    assert response.status_code == 204
    
    # Verify provider is deleted
    from app.database.repositories.provider_repository import ProviderRepository
    repository = ProviderRepository(db_session)
    assert repository.get_by_guid(provider_guid) is None


def test_delete_provider_not_found(client, admin_token):
    """Test deleting a non-existent provider"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete("/api/admin/providers/non-existent-guid", headers=headers)
    assert response.status_code == 404


def test_test_provider_requires_auth(client, test_provider):
    """Test that testing a provider requires authentication"""
    response = client.post(f"/api/admin/providers/{test_provider.guid}/test")
    assert response.status_code == 401


def test_test_provider_requires_admin(client, client_token, test_provider):
    """Test that testing a provider requires admin role"""
    headers = {"Authorization": f"Bearer {client_token}"}
    response = client.post(f"/api/admin/providers/{test_provider.guid}/test", headers=headers)
    assert response.status_code == 403


def test_test_provider_success(client, admin_token, test_provider):
    """Test successful provider test"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(f"/api/admin/providers/{test_provider.guid}/test", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "message" in data
    # Note: The actual success value depends on the provider's health_check implementation


def test_test_provider_not_found(client, admin_token):
    """Test testing a non-existent provider"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/api/admin/providers/non-existent-guid/test", headers=headers)
    assert response.status_code == 404

