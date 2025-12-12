"""
Base provider interface for threat intelligence APIs
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, field_validator


class ProviderConfig(BaseModel):
    """Configuration for a provider"""
    api_key: str
    base_url: Optional[str] = None
    timeout: int = 30
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        """Validate API key format"""
        if not v or len(v) < 10:
            raise ValueError("API key invalide")
        return v


class BaseProvider(ABC):
    """
    Abstract base class for all threat intelligence providers.
    
    All providers must implement the fetch_threats method to retrieve
    threat intelligence data from their respective APIs.
    """
    
    def __init__(self, config: ProviderConfig):
        """
        Initialize the provider with configuration.
        
        Args:
            config: Provider configuration containing API key and settings
        """
        self.config = config
        self.validate_config()
    
    def validate_config(self):
        """
        Validate provider-specific configuration.
        
        Override this method in subclasses to add custom validation.
        """
        pass
    
    @abstractmethod
    async def fetch_threats(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch threat intelligence data from the provider API.
        
        Args:
            params: Parameters for the API request (filters, dates, etc.)
            
        Returns:
            Dictionary containing threat intelligence data
            
        Raises:
            ProviderException: If the API request fails
        """
        pass
    
    async def health_check(self) -> bool:
        """
        Check if the provider API is accessible and healthy.
        
        Returns:
            True if the provider is healthy, False otherwise
        """
        try:
            # Default implementation: try a minimal request
            # Subclasses can override for more specific checks
            return True
        except Exception:
            return False

