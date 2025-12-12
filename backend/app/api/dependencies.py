"""
FastAPI dependencies for route handlers
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.threat_service import ThreatService
from app.services.provider_service import ProviderService
from app.cache.cache_manager import CacheManager
from app.database.database import get_db


def get_cache_manager() -> CacheManager:
    """
    Get or create CacheManager instance.
    
    Returns:
        CacheManager instance
    """
    # For now, create a new instance (in production, use dependency injection)
    # TODO: Integrate with app state/dependency injection container
    return CacheManager(default_ttl=300, enable_db=False)


def get_provider_service(db: Session = Depends(get_db)) -> ProviderService:
    """
    Get ProviderService instance.
    
    Args:
        db: Database session
        
    Returns:
        ProviderService instance
    """
    return ProviderService(db)


def get_threat_service(
    db: Session = Depends(get_db),
    cache_manager: CacheManager = Depends(get_cache_manager)
) -> ThreatService:
    """
    Get or create ThreatService instance with providers loaded from database.
    
    Args:
        db: Database session
        cache_manager: Cache manager instance
        
    Returns:
        ThreatService instance with all active providers from database
    """
    # Load providers from database
    provider_service = ProviderService(db)
    providers = provider_service.load_all_providers(active_only=True)
    
    return ThreatService(cache_manager=cache_manager, providers=providers)

