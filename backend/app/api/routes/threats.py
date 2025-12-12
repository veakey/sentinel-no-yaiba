"""
Threat intelligence API routes
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Dict, Any, Optional
from app.services.threat_service import ThreatService
from app.api.dependencies import get_threat_service
from app.core.exceptions import ProviderException


router = APIRouter(prefix="/api/threats", tags=["threats"])


@router.get("")
async def get_threats(
    force_refresh: bool = Query(False, description="Force refresh from providers"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    threat_service: ThreatService = Depends(get_threat_service)
) -> Dict[str, Any]:
    """
    Get aggregated threat intelligence from all configured providers.
    
    Args:
        force_refresh: If True, bypass cache and fetch fresh data
        severity: Optional severity filter
        status: Optional status filter
        threat_service: Injected ThreatService instance
        
    Returns:
        Dictionary with provider names as keys and their threat data as values
    """
    # Build params dict from query parameters
    params: Dict[str, Any] = {}
    if severity:
        params["severity"] = severity
    if status:
        params["status"] = status
    
    try:
        data = await threat_service.get_threats(
            force_refresh=force_refresh,
            params=params
        )
        return data
    except ProviderException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Provider error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

