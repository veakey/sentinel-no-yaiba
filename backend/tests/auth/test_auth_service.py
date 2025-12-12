"""
Tests for Authentication Service
"""
import pytest
from unittest.mock import Mock
from app.auth.auth_service import AuthService
from app.auth.password import hash_password
from app.database.models import User
from app.core.exceptions import AppException


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
        role="client",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_authenticate_user_success(auth_service, test_user):
    """Test successful user authentication"""
    user = auth_service.authenticate_user("testuser", "password123")
    
    assert user is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_authenticate_user_wrong_password(auth_service, test_user):
    """Test authentication with wrong password"""
    user = auth_service.authenticate_user("testuser", "wrong_password")
    
    assert user is None


def test_authenticate_user_inactive(auth_service, db_session, test_user):
    """Test authentication with inactive user"""
    test_user.is_active = False
    db_session.commit()
    
    user = auth_service.authenticate_user("testuser", "password123")
    
    assert user is None


def test_authenticate_user_not_found(auth_service):
    """Test authentication with non-existent user"""
    user = auth_service.authenticate_user("nonexistent", "password123")
    
    assert user is None


def test_authenticate_user_by_email(auth_service, test_user):
    """Test authentication using email instead of username"""
    user = auth_service.authenticate_user("test@example.com", "password123")
    
    assert user is not None
    assert user.username == "testuser"


def test_get_user_by_username(auth_service, test_user):
    """Test getting user by username"""
    user = auth_service.get_user_by_username("testuser")
    
    assert user is not None
    assert user.username == "testuser"


def test_get_user_by_email(auth_service, test_user):
    """Test getting user by email"""
    user = auth_service.get_user_by_email("test@example.com")
    
    assert user is not None
    assert user.email == "test@example.com"


def test_get_user_by_id(auth_service, test_user):
    """Test getting user by ID"""
    user = auth_service.get_user_by_id(test_user.id)
    
    assert user is not None
    assert user.id == test_user.id


def test_get_user_by_guid(auth_service, test_user):
    """Test getting user by GUID"""
    user = auth_service.get_user_by_guid(test_user.guid)
    
    assert user is not None
    assert user.guid == test_user.guid


def test_get_user_not_found(auth_service):
    """Test getting non-existent user"""
    user = auth_service.get_user_by_username("nonexistent")
    
    assert user is None

