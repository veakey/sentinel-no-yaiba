"""
Tests for JWT utilities
"""
import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token
)
from app.config import settings


def test_create_access_token():
    """Test creating an access token"""
    data = {"sub": "user123", "role": "admin"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_contains_claims():
    """Test that access token contains correct claims"""
    data = {"sub": "user123", "role": "admin"}
    token = create_access_token(data)
    
    decoded = decode_token(token)
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "admin"


def test_create_access_token_expires_in_future():
    """Test that access token has expiration in the future"""
    data = {"sub": "user123"}
    token = create_access_token(data)
    
    decoded = decode_token(token)
    assert "exp" in decoded
    exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    now = datetime.now(timezone.utc)
    assert exp_time > now


def test_create_refresh_token():
    """Test creating a refresh token"""
    data = {"sub": "user123"}
    token = create_refresh_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token_valid():
    """Test verifying a valid token"""
    data = {"sub": "user123", "role": "admin"}
    token = create_access_token(data)
    
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"


def test_verify_token_invalid():
    """Test verifying an invalid token"""
    invalid_token = "invalid.token.here"
    
    with pytest.raises(JWTError):
        verify_token(invalid_token)


def test_verify_token_expired():
    """Test verifying an expired token"""
    # Create a token with past expiration
    data = {"sub": "user123"}
    expired_data = data.copy()
    expired_data["exp"] = datetime.now(timezone.utc) - timedelta(hours=1)
    
    token = jwt.encode(expired_data, settings.SECRET_KEY, algorithm="HS256")
    
    with pytest.raises(JWTError):
        verify_token(token)


def test_decode_token_valid():
    """Test decoding a valid token"""
    data = {"sub": "user123", "role": "admin"}
    token = create_access_token(data)
    
    decoded = decode_token(token)
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "admin"


def test_decode_token_invalid_signature():
    """Test decoding token with wrong secret"""
    data = {"sub": "user123"}
    token = jwt.encode(data, "wrong-secret", algorithm="HS256")
    
    with pytest.raises(JWTError):
        decode_token(token)

