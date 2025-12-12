"""
Tests for authentication dependencies
"""
import pytest
from fastapi import HTTPException
from app.auth.dependencies import get_current_user, require_admin
from app.auth.jwt import create_access_token
from app.auth.password import hash_password
from app.database.models import User


@pytest.fixture
def admin_user(db_session):
    """Fixture for admin user"""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        role="admin",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def client_user(db_session):
    """Fixture for client user"""
    user = User(
        username="client",
        email="client@example.com",
        hashed_password=hash_password("client123"),
        role="client",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_get_current_user_valid_token(db_session, admin_user):
    """Test getting current user from valid token"""
    token = create_access_token({"sub": admin_user.guid, "role": "admin"})
    
    user = get_current_user(token, db_session)
    
    assert user is not None
    assert user.username == "admin"
    assert user.guid == admin_user.guid


def test_get_current_user_invalid_token(db_session):
    """Test getting current user with invalid token"""
    with pytest.raises(HTTPException) as exc_info:
        get_current_user("invalid_token", db_session)
    
    assert exc_info.value.status_code == 401


def test_get_current_user_user_not_found(db_session):
    """Test getting current user when user doesn't exist"""
    from app.database.models import User
    from app.auth.jwt import create_access_token
    import uuid
    
    # Create token for non-existent user
    fake_guid = str(uuid.uuid4())
    token = create_access_token({"sub": fake_guid, "role": "admin"})
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token, db_session)
    
    assert exc_info.value.status_code == 401


def test_get_current_user_inactive(db_session, admin_user):
    """Test getting current user when user is inactive"""
    admin_user.is_active = False
    db_session.commit()
    
    token = create_access_token({"sub": admin_user.guid, "role": "admin"})
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token, db_session)
    
    assert exc_info.value.status_code == 401


def test_require_admin_allows_admin(db_session, admin_user):
    """Test that require_admin allows admin users"""
    token = create_access_token({"sub": admin_user.guid, "role": "admin"})
    user = get_current_user(token, db_session)
    
    # Should not raise exception
    require_admin(user)


def test_require_admin_blocks_client(db_session, client_user):
    """Test that require_admin blocks client users"""
    token = create_access_token({"sub": client_user.guid, "role": "client"})
    user = get_current_user(token, db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        require_admin(user)
    
    assert exc_info.value.status_code == 403

