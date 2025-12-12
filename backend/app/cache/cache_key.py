"""
Cache key generation utilities
"""
import hashlib
import json
from typing import Dict, Any


def generate_cache_key(provider: str, endpoint: str, params: Dict[str, Any]) -> str:
    """
    Generate a unique cache key for a provider request.
    
    Args:
        provider: Provider name (e.g., "ninja", "malwarebytes")
        endpoint: API endpoint (e.g., "threats")
        params: Request parameters dictionary
        
    Returns:
        SHA256 hash of the cache key components (hex string, 64 characters)
    """
    # Normalize params by sorting keys for consistent hashing
    normalized_params = json.dumps(params, sort_keys=True) if params else "{}"
    
    # Create key string
    key_string = f"{provider}:{endpoint}:{normalized_params}"
    
    # Generate SHA256 hash
    return hashlib.sha256(key_string.encode()).hexdigest()

