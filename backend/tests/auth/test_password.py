"""
Tests for password hashing and verification
"""
import pytest
from app.auth.password import hash_password, verify_password


def test_hash_password():
    """Test hashing a password"""
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert hashed is not None
    assert isinstance(hashed, str)
    assert len(hashed) > 0
    assert hashed != password  # Should be different from plain password


def test_hash_password_different_each_time():
    """Test that hashing the same password produces different hashes (salt)"""
    password = "same_password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    # Should be different due to salt
    assert hash1 != hash2


def test_verify_password_correct():
    """Test verifying a correct password"""
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test verifying an incorrect password"""
    password = "correct_password"
    wrong_password = "wrong_password"
    hashed = hash_password(password)
    
    assert verify_password(wrong_password, hashed) is False


def test_verify_password_empty():
    """Test verifying an empty password"""
    password = "test_password"
    hashed = hash_password(password)
    
    assert verify_password("", hashed) is False


def test_verify_password_empty_hash():
    """Test verifying with empty hash"""
    password = "test_password"
    
    # Empty hash should fail verification
    assert verify_password(password, "") is False

