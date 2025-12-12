"""
Tests for application configuration
"""
import pytest
import os
from pydantic import ValidationError

from app.config import Settings


def test_settings_loads_from_env(monkeypatch):
    """Test that settings are loaded from environment variables"""
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-12345")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test_config.db")
    
    settings = Settings()
    
    assert settings.SECRET_KEY == "test-secret-key-12345"
    assert settings.DATABASE_URL == "sqlite:///./test_config.db"


def test_settings_has_defaults(monkeypatch):
    """Test that settings have correct default values"""
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-12345")
    
    settings = Settings()
    
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert settings.CACHE_TTL_DEFAULT == 300
    assert settings.LOG_LEVEL == "INFO"


def test_settings_has_default_secret_key(monkeypatch):
    """Test that SECRET_KEY has a default value if not provided"""
    # Remove SECRET_KEY from environment if present and clear .env loading
    monkeypatch.delenv("SECRET_KEY", raising=False)
    
    # Should not raise error, should use default
    # Note: If .env.example exists, it will load from there
    settings = Settings()
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) > 0


def test_settings_cors_origins_default():
    """Test that CORS_ORIGINS has correct default values"""
    from app.config import settings
    
    assert "http://localhost:3000" in settings.CORS_ORIGINS
    assert "http://localhost:5173" in settings.CORS_ORIGINS

