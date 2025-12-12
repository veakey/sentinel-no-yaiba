"""
Tests for Authentication Service token generation
"""
import pytest
from app.auth.auth_service import AuthService
from app.auth.jwt import verify_token, decode_token
from app.auth.password import hash_password
from app.database.models import User


@pytest.fixture
def auth_service(db_session):
    """Fixture for AuthService"""
    return AuthService(db_session)


@pytest.fixture
def test_user(db_session):
    """Fixture for test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role="admin",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_create_access_token_for_user(auth_service, test_user):
    """Test creating access token for authenticated user"""
    tokens = auth_service.create_tokens_for_user(test_user)
    
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"
    
    # Verify access token
    payload = verify_token(tokens["access_token"])
    assert payload["sub"] == test_user.guid
    assert payload["role"] == "admin"


def test_create_refresh_token_for_user(auth_service, test_user):
    """Test that refresh token is valid and contains user info"""
    tokens = auth_service.create_tokens_for_user(test_user)
    
    # Verify refresh token
    payload = verify_token(tokens["refresh_token"])
    assert payload["sub"] == test_user.guid
    assert payload["type"] == "refresh"


def test_refresh_access_token(auth_service, test_user):
    """Test refreshing access token from refresh token"""
    tokens = auth_service.create_tokens_for_user(test_user)
    refresh_token = tokens["refresh_token"]
    
    # Create new access token from refresh token
    new_tokens = auth_service.refresh_access_token(refresh_token)
    
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    
    # Verify new access token
    payload = verify_token(new_tokens["access_token"])
    assert payload["sub"] == test_user.guid


def test_refresh_access_token_invalid(auth_service):
    """Test refreshing with invalid refresh token"""
    result = auth_service.refresh_access_token("invalid_token")
    
    assert result is None


def test_refresh_access_token_expired(auth_service, test_user):
    """Test refreshing with expired refresh token"""
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from app.config import settings
    
    # Create expired refresh token manually
    expired_data = {
        "sub": test_user.guid,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) - timedelta(hours=1)
    }
    expired_token = jwt.encode(expired_data, settings.SECRET_KEY, algorithm="HS256")
    
    result = auth_service.refresh_access_token(expired_token)
    
    assert result is None


def test_refresh_access_token_not_refresh_type(auth_service, test_user):
    """Test that non-refresh tokens cannot be used to refresh"""
    tokens = auth_service.create_tokens_for_user(test_user)
    access_token = tokens["access_token"]  # Not a refresh token
    
    result = auth_service.refresh_access_token(access_token)
    
    assert result is None

