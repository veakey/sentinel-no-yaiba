"""
Tests for User model
"""
import pytest
from app.database.models import User
from app.database.base import BaseModel
from sqlalchemy import inspect


def test_user_inherits_from_base_model():
    """Test that User model inherits from BaseModel"""
    assert issubclass(User, BaseModel)


def test_user_has_required_fields(db_session):
    """Test that User model has all required fields"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password_here",
        role="client"
    )
    
    db_session.add(user)
    db_session.commit()
    
    # Check that BaseModel fields exist
    assert user.id is not None
    assert user.guid is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    
    # Check User-specific fields
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password_here"
    assert user.role == "client"


def test_user_username_unique(db_session):
    """Test that username must be unique"""
    user1 = User(
        username="duplicate",
        email="user1@example.com",
        hashed_password="hash1",
        role="client"
    )
    user2 = User(
        username="duplicate",
        email="user2@example.com",
        hashed_password="hash2",
        role="client"
    )
    
    db_session.add(user1)
    db_session.commit()
    
    db_session.add(user2)
    with pytest.raises(Exception):  # IntegrityError
        db_session.commit()


def test_user_email_unique(db_session):
    """Test that email must be unique"""
    user1 = User(
        username="user1",
        email="duplicate@example.com",
        hashed_password="hash1",
        role="client"
    )
    user2 = User(
        username="user2",
        email="duplicate@example.com",
        hashed_password="hash2",
        role="client"
    )
    
    db_session.add(user1)
    db_session.commit()
    
    db_session.add(user2)
    with pytest.raises(Exception):  # IntegrityError
        db_session.commit()


def test_user_role_enum_values():
    """Test that role field accepts only 'admin' or 'client'"""
    # Valid roles
    user_admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password="hash",
        role="admin"
    )
    user_client = User(
        username="client",
        email="client@example.com",
        hashed_password="hash",
        role="client"
    )
    
    assert user_admin.role == "admin"
    assert user_client.role == "client"


def test_user_is_active_default(db_session):
    """Test that is_active defaults to True"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hash",
        role="client"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.is_active is True


def test_user_is_active_can_be_set(db_session):
    """Test that is_active can be set to False"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hash",
        role="client",
        is_active=False
    )
    
    assert user.is_active is False

