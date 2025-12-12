"""
Repository for provider configurations
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models import Provider


class ProviderRepository:
    """Repository for managing provider configurations in database"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_guid(self, guid: str) -> Optional[Provider]:
        """
        Get a provider by GUID.
        
        Args:
            guid: Provider GUID
            
        Returns:
            Provider if found, None otherwise
        """
        return self.db.query(Provider).filter(Provider.guid == guid).first()
    
    def get_by_id(self, provider_id: int) -> Optional[Provider]:
        """
        Get a provider by ID.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            Provider if found, None otherwise
        """
        return self.db.query(Provider).filter(Provider.id == provider_id).first()
    
    def get_all(self, active_only: bool = False) -> List[Provider]:
        """
        Get all providers.
        
        Args:
            active_only: If True, only return active providers
            
        Returns:
            List of providers
        """
        query = self.db.query(Provider)
        if active_only:
            query = query.filter(Provider.is_active == True)
        return query.all()
    
    def get_by_type(self, provider_type: str, active_only: bool = False) -> List[Provider]:
        """
        Get providers by type.
        
        Args:
            provider_type: Provider type (e.g., "ninja", "malwarebytes")
            active_only: If True, only return active providers
            
        Returns:
            List of providers of the specified type
        """
        query = self.db.query(Provider).filter(Provider.type == provider_type)
        if active_only:
            query = query.filter(Provider.is_active == True)
        return query.all()
    
    def create(self, provider: Provider) -> Provider:
        """
        Create a new provider.
        
        Args:
            provider: Provider instance to create
            
        Returns:
            Created provider
        """
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return provider
    
    def update(self, provider: Provider) -> Provider:
        """
        Update an existing provider.
        
        Args:
            provider: Provider instance to update
            
        Returns:
            Updated provider
        """
        self.db.commit()
        self.db.refresh(provider)
        return provider
    
    def delete(self, provider: Provider):
        """
        Delete a provider.
        
        Args:
            provider: Provider instance to delete
        """
        self.db.delete(provider)
        self.db.commit()
    
    def exists(self, guid: str) -> bool:
        """
        Check if a provider exists by GUID.
        
        Args:
            guid: Provider GUID
            
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(Provider).filter(Provider.guid == guid).first() is not None

