"""
Factory pattern for creating provider instances
"""
from enum import Enum
from typing import Dict, Type, List
from app.providers.base import BaseProvider, ProviderConfig
from app.core.exceptions import ProviderException


class ProviderType(str, Enum):
    """Enumeration of supported provider types"""
    NINJA = "ninja"
    MALWAREBYTES = "malwarebytes"


class ProviderFactory:
    """
    Factory for creating provider instances.
    
    Providers must be registered before they can be created.
    """
    
    _providers: Dict[str, Type[BaseProvider]] = {}
    
    @classmethod
    def register(cls, provider_type: str, provider_class: Type[BaseProvider]):
        """
        Register a provider type with its implementation class.
        
        Args:
            provider_type: String identifier for the provider type
            provider_class: Class that implements BaseProvider
        """
        if not issubclass(provider_class, BaseProvider):
            raise ValueError(f"{provider_class.__name__} must be a subclass of BaseProvider")
        
        cls._providers[provider_type] = provider_class
    
    @classmethod
    def create(cls, provider_type: str, config: ProviderConfig) -> BaseProvider:
        """
        Create a provider instance of the specified type.
        
        Args:
            provider_type: String identifier for the provider type
            config: Provider configuration
            
        Returns:
            Instance of the requested provider type
            
        Raises:
            ProviderException: If the provider type is not registered
        """
        if provider_type not in cls._providers:
            raise ProviderException(f"Unknown provider type: {provider_type}")
        
        provider_class = cls._providers[provider_type]
        return provider_class(config)
    
    @classmethod
    def is_registered(cls, provider_type: str) -> bool:
        """
        Check if a provider type is registered.
        
        Args:
            provider_type: String identifier for the provider type
            
        Returns:
            True if registered, False otherwise
        """
        return provider_type in cls._providers
    
    @classmethod
    def list_registered(cls) -> List[str]:
        """
        Get a list of all registered provider types.
        
        Returns:
            List of registered provider type strings
        """
        return list(cls._providers.keys())

