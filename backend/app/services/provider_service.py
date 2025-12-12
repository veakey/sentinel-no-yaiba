"""
Service for loading and managing providers from database
"""
from typing import Dict, Optional
from sqlalchemy.orm import Session

from app.database.models import Provider
from app.database.repositories.provider_repository import ProviderRepository
from app.providers.base import BaseProvider, ProviderConfig
from app.providers.factory import ProviderFactory
from app.auth.encryption import EncryptionService
from app.core.exceptions import ProviderException


class ProviderService:
    """
    Service for loading providers from database and converting them to BaseProvider instances.
    
    Handles:
    - Loading active providers from database
    - Decrypting API keys
    - Creating provider instances via factory
    - Error handling for invalid configurations
    """
    
    def __init__(self, db: Session):
        """
        Initialize ProviderService.
        
        Args:
            db: Database session
        """
        self.db = db
        self.repository = ProviderRepository(db)
    
    def load_all_providers(self, active_only: bool = True) -> Dict[str, BaseProvider]:
        """
        Load all providers from database and convert them to BaseProvider instances.
        
        Args:
            active_only: If True, only load active providers
            
        Returns:
            Dictionary mapping provider names to BaseProvider instances
        """
        providers = {}
        db_providers = self.repository.get_all(active_only=active_only)
        
        for db_provider in db_providers:
            try:
                provider_instance = self._create_provider_instance(db_provider)
                # Use provider name as key (or GUID if name conflicts)
                providers[db_provider.name] = provider_instance
            except Exception as e:
                # Log error but continue with other providers
                # In production, use proper logging here
                print(f"Failed to load provider {db_provider.name} (GUID: {db_provider.guid}): {str(e)}")
                continue
        
        return providers
    
    def load_provider_by_guid(self, guid: str) -> Optional[BaseProvider]:
        """
        Load a specific provider by GUID.
        
        Args:
            guid: Provider GUID
            
        Returns:
            BaseProvider instance if found and valid, None otherwise
        """
        db_provider = self.repository.get_by_guid(guid)
        if not db_provider:
            return None
        
        try:
            return self._create_provider_instance(db_provider)
        except Exception as e:
            # Log error
            print(f"Failed to load provider {db_provider.name} (GUID: {guid}): {str(e)}")
            return None
    
    def _create_provider_instance(self, db_provider: Provider) -> BaseProvider:
        """
        Create a BaseProvider instance from a database Provider model.
        
        Args:
            db_provider: Provider model from database
            
        Returns:
            BaseProvider instance
            
        Raises:
            ProviderException: If provider type is not registered or configuration is invalid
        """
        # Decrypt API key (if present)
        api_key = None
        if db_provider.api_key_encrypted:
            try:
                api_key = EncryptionService.decrypt(db_provider.api_key_encrypted)
            except Exception as e:
                raise ProviderException(f"Failed to decrypt API key for provider {db_provider.name}: {str(e)}")
        
        # Check if provider type is registered
        if not ProviderFactory.is_registered(db_provider.type):
            raise ProviderException(f"Provider type '{db_provider.type}' is not registered")
        
        # Build ProviderConfig
        config_data = {
            "base_url": db_provider.base_url,
            "timeout": 30  # Default timeout
        }
        
        # Add API key if available
        if api_key:
            config_data["api_key"] = api_key
        
        # Merge provider-specific config if available (may contain client_id, client_secret)
        if db_provider.config:
            if isinstance(db_provider.config, dict):
                # Extract OAuth credentials from config if present
                if "client_id" in db_provider.config:
                    config_data["client_id"] = db_provider.config["client_id"]
                if "client_secret" in db_provider.config:
                    # Decrypt client_secret if it's encrypted
                    client_secret = db_provider.config["client_secret"]
                    if isinstance(client_secret, str) and client_secret.startswith("encrypted:"):
                        try:
                            encrypted_value = client_secret.replace("encrypted:", "")
                            config_data["client_secret"] = EncryptionService.decrypt(encrypted_value)
                        except Exception as e:
                            raise ProviderException(
                                f"Failed to decrypt client_secret for provider {db_provider.name}: {str(e)}"
                            )
                    else:
                        # Plain text client_secret (shouldn't happen in production, but handle it)
                        config_data["client_secret"] = client_secret
                
                # Merge other config values
                for key, value in db_provider.config.items():
                    if key not in ["client_id", "client_secret"]:
                        config_data[key] = value
        
        # Override timeout if specified in config
        if db_provider.config and isinstance(db_provider.config, dict):
            if "timeout" in db_provider.config:
                config_data["timeout"] = db_provider.config["timeout"]
        
        # Create ProviderConfig
        try:
            provider_config = ProviderConfig(**config_data)
        except Exception as e:
            raise ProviderException(f"Invalid configuration for provider {db_provider.name}: {str(e)}")
        
        # Create provider instance via factory
        try:
            provider_instance = ProviderFactory.create(db_provider.type, provider_config)
        except Exception as e:
            raise ProviderException(f"Failed to create provider instance for {db_provider.name}: {str(e)}")
        
        return provider_instance
    
    def get_provider_info(self, guid: str) -> Optional[Dict]:
        """
        Get provider information (without decrypting API key).
        
        Args:
            guid: Provider GUID
            
        Returns:
            Dictionary with provider info, or None if not found
        """
        db_provider = self.repository.get_by_guid(guid)
        if not db_provider:
            return None
        
        return {
            "guid": db_provider.guid,
            "name": db_provider.name,
            "type": db_provider.type,
            "base_url": db_provider.base_url,
            "is_active": db_provider.is_active,
            "config": db_provider.config,
            "provider_specific_settings": db_provider.provider_specific_settings,
            "created_at": db_provider.created_at.isoformat() if db_provider.created_at else None,
            "updated_at": db_provider.updated_at.isoformat() if db_provider.updated_at else None
        }

