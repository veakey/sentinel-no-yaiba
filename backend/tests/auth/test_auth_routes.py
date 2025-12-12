"""
Tests for authentication API routes
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.password import hash_password
from app.database.models import User


@pytest.fixture
def test_user(db_session):
    """Fixture for test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role="client",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_login_endpoint_exists(client):
    """Test that POST /api/auth/login endpoint exists"""
    response = client.post("/api/auth/login", json={})
    # Should not be 404
    assert response.status_code != 404


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        },
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_email(client, test_user):
    """Test login using email instead of username"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        },
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "wrong_password"
        },
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_login_inactive_user(client, db_session, test_user):
    """Test login with inactive user"""
    test_user.is_active = False
    db_session.commit()
    
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        },
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 401


def test_refresh_endpoint_exists(client):
    """Test that POST /api/auth/refresh endpoint exists"""
    response = client.post("/api/auth/refresh", json={})
    # Should not be 404
    assert response.status_code != 404


def test_refresh_token_success(client, test_user):
    """Test successful token refresh"""
    # First login
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        },
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Refresh
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_invalid(client):
    """Test refresh with invalid token"""
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    
    assert response.status_code == 401

