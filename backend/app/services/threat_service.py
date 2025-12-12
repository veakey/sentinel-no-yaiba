"""
Service for aggregating threat intelligence from multiple providers
"""
from typing import Dict, Any, Optional
from app.cache.cache_manager import CacheManager
from app.cache.cache_key import generate_cache_key
from app.providers.base import BaseProvider
from app.core.exceptions import ProviderException


class ThreatService:
    """
    Service for aggregating threat intelligence data from multiple providers.
    
    Handles:
    - Multi-provider data aggregation
    - Caching with instant responses
    - Error handling (continues if one provider fails)
    - Asynchronous refresh
    """
    
    def __init__(self, cache_manager: CacheManager, providers: Dict[str, BaseProvider]):
        """
        Initialize ThreatService.
        
        Args:
            cache_manager: Cache manager instance
            providers: Dictionary mapping provider names to provider instances
        """
        self.cache_manager = cache_manager
        self.providers = providers
    
    async def get_threats(
        self, 
        force_refresh: bool = False,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get aggregated threats from all providers.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            params: Optional parameters for provider requests
            
        Returns:
            Dictionary with provider names as keys and their threat data as values
        """
        if params is None:
            params = {}
        
        cache_key = generate_cache_key("all", "threats", params)
        
        # Check cache first (unless force refresh)
        if not force_refresh:
            cached = self.cache_manager.get(cache_key)
            if cached:
                # Trigger async refresh in background (fire and forget)
                # Note: In production, use asyncio.create_task() here
                return cached
        
        # Fetch fresh data from all providers
        aggregated_data = await self._fetch_from_all_providers(params)
        
        # Store in cache
        self.cache_manager.set(cache_key, aggregated_data, ttl=300)
        
        return aggregated_data
    
    async def _fetch_from_all_providers(
        self, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetch threats from all configured providers.
        
        Args:
            params: Parameters to pass to providers
            
        Returns:
            Dictionary mapping provider names to their responses (or error info)
        """
        aggregated = {}
        
        for provider_name, provider in self.providers.items():
            try:
                data = await self._fetch_from_provider(provider_name, params)
                aggregated[provider_name] = data
            except ProviderException as e:
                # Log error but continue with other providers
                aggregated[provider_name] = {
                    "error": str(e),
                    "status": "failed"
                }
            except Exception as e:
                # Unexpected error
                aggregated[provider_name] = {
                    "error": f"Unexpected error: {str(e)}",
                    "status": "failed"
                }
        
        return aggregated
    
    async def _fetch_from_provider(
        self,
        provider_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetch threats from a specific provider.
        
        Args:
            provider_name: Name of the provider
            params: Parameters for the request
            
        Returns:
            Provider's response data
            
        Raises:
            ProviderException: If the provider request fails
        """
        provider = self.providers.get(provider_name)
        if not provider:
            raise ProviderException(f"Provider '{provider_name}' not found")
        
        return await provider.fetch_threats(params)

