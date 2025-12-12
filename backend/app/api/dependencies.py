"""
FastAPI dependencies for route handlers
"""
from app.services.threat_service import ThreatService
from app.cache.cache_manager import CacheManager
from app.providers.factory import ProviderFactory
from app.providers.base import ProviderConfig
from app.providers.factory import ProviderType


def get_cache_manager() -> CacheManager:
    """
    Get or create CacheManager instance.
    
    Returns:
        CacheManager instance
    """
    # For now, create a new instance (in production, use dependency injection)
    # TODO: Integrate with app state/dependency injection container
    return CacheManager(default_ttl=300, enable_db=False)


def get_threat_service() -> ThreatService:
    """
    Get or create ThreatService instance with configured providers.
    
    Returns:
        ThreatService instance with all registered providers
    """
    cache_manager = get_cache_manager()
    
    # Build providers dictionary from factory
    providers = {}
    # TODO: Load providers from database in Phase 5
    # For now, providers are hardcoded (will be configurable later)
    
    return ThreatService(cache_manager=cache_manager, providers=providers)

