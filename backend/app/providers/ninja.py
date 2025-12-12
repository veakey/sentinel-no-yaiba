"""
Ninja One provider implementation
"""
import httpx
from typing import Dict, Any
from app.providers.base import BaseProvider, ProviderConfig
from app.core.exceptions import ProviderException


class NinjaProvider(BaseProvider):
    """
    Provider implementation for Ninja One API.
    
    Documentation: https://app.ninjaone.com/apidocs/?links.active=core
    Base URLs:
    - North America: https://app.ninjarmm.com
    - Europe: https://eu.ninjarmm.com
    - Oceania: https://oc.ninjarmm.com
    """
    
    DEFAULT_BASE_URL = "https://app.ninjarmm.com"
    
    def __init__(self, config: ProviderConfig):
        """
        Initialize Ninja One provider.
        
        Args:
            config: Provider configuration with API key
        """
        # Set default base URL if not provided
        if not config.base_url:
            config.base_url = self.DEFAULT_BASE_URL
        
        super().__init__(config)
    
    def validate_config(self):
        """
        Validate Ninja-specific configuration.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.api_key:
            raise ValueError("Ninja API key is required")
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers for API requests.
        
        Returns:
            Dictionary with authentication headers
        """
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def fetch_threats(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch threat intelligence data from Ninja One API.
        
        Args:
            params: Optional parameters for filtering/pagination
            
        Returns:
            Dictionary containing threat data from Ninja API
            
        Raises:
            ProviderException: If the API request fails
        """
        if params is None:
            params = {}
        
        url = f"{self.config.base_url}/api/v1/threats"
        
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    params=params
                )
                response.raise_for_status()
                return response.json()
        
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code} from Ninja API"
            if e.response.status_code == 401:
                error_msg = "Authentication failed: Invalid API key"
            elif e.response.status_code == 404:
                error_msg = "Resource not found"
            raise ProviderException(f"Failed to fetch threats from Ninja: {error_msg}")
        
        except httpx.TimeoutException as e:
            raise ProviderException(f"Timeout while fetching threats from Ninja: {str(e)}")
        
        except httpx.NetworkError as e:
            raise ProviderException(f"Network error while fetching threats from Ninja: {str(e)}")
        
        except Exception as e:
            raise ProviderException(f"Unexpected error fetching threats from Ninja: {str(e)}")
    
    async def health_check(self) -> bool:
        """
        Check if Ninja One API is accessible.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            # Try a minimal API call (e.g., get account info or health endpoint)
            url = f"{self.config.base_url}/api/v1/account"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    url,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return True
        
        except Exception:
            return False

