"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str  # Required - will raise error if not provided
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite:///./sentinel.db"
    
    # Cache
    CACHE_TTL_DEFAULT: int = 300  # 5 minutes
    CACHE_ENABLE_DB: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    
    # Providers
    PROVIDER_REQUEST_TIMEOUT: int = 30
    PROVIDER_MAX_RETRIES: int = 3
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # Encryption
    ENCRYPTION_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

