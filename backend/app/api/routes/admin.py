"""
Admin API routes for managing providers
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.database.database import get_db
from app.database.models import Provider, ProviderType
from app.database.repositories.provider_repository import ProviderRepository
from app.services.provider_service import ProviderService
from app.auth.dependencies import require_admin
from app.auth.encryption import EncryptionService
from app.providers.factory import ProviderFactory
from app.core.exceptions import ProviderException


router = APIRouter(prefix="/api/admin/providers", tags=["admin", "providers"])


# Request/Response schemas
class ProviderCreateRequest(BaseModel):
    """Request schema for creating a provider"""
    name: str
    type: str
    api_key: str
    base_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: bool = True
    provider_specific_settings: Optional[Dict[str, Any]] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError("Provider name must be at least 3 characters")
        return v.strip()
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        if not ProviderFactory.is_registered(v):
            raise ValueError(f"Provider type '{v}' is not registered")
        return v
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        if not v or len(v) < 10:
            raise ValueError("API key must be at least 10 characters")
        return v


class ProviderUpdateRequest(BaseModel):
    """Request schema for updating a provider"""
    name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    provider_specific_settings: Optional[Dict[str, Any]] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and (not v or len(v.strip()) < 3):
            raise ValueError("Provider name must be at least 3 characters")
        return v.strip() if v else None
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        if v is not None and (not v or len(v) < 10):
            raise ValueError("API key must be at least 10 characters")
        return v


class ProviderResponse(BaseModel):
    """Response schema for provider"""
    guid: str
    name: str
    type: str
    base_url: Optional[str]
    is_active: bool
    config: Optional[Dict[str, Any]]
    provider_specific_settings: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProviderTestResponse(BaseModel):
    """Response schema for provider test"""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None


@router.get("", response_model=List[ProviderResponse])
async def list_providers(
    active_only: bool = False,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """
    List all providers (admin only).
    
    Args:
        active_only: If True, only return active providers
        db: Database session
        admin_user: Current admin user (from dependency)
        
    Returns:
        List of providers
    """
    repository = ProviderRepository(db)
    providers = repository.get_all(active_only=active_only)
    
    return providers


@router.get("/{guid}", response_model=ProviderResponse)
async def get_provider(
    guid: str,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """
    Get a specific provider by GUID (admin only).
    
    Args:
        guid: Provider GUID
        db: Database session
        admin_user: Current admin user (from dependency)
        
    Returns:
        Provider information
        
    Raises:
        HTTPException: If provider not found (404)
    """
    repository = ProviderRepository(db)
    provider = repository.get_by_guid(guid)
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider with GUID '{guid}' not found"
        )
    
    return provider


@router.post("", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_provider(
    request: ProviderCreateRequest,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """
    Create a new provider (admin only).
    
    Args:
        request: Provider creation request
        db: Database session
        admin_user: Current admin user (from dependency)
        
    Returns:
        Created provider
        
    Raises:
        HTTPException: If validation fails or provider type is invalid
    """
    repository = ProviderRepository(db)
    
    # Encrypt API key
    encrypted_api_key = EncryptionService.encrypt(request.api_key)
    
    # Create provider
    provider = Provider(
        name=request.name,
        type=request.type,
        api_key_encrypted=encrypted_api_key,
        base_url=request.base_url,
        config=request.config,
        is_active=request.is_active,
        provider_specific_settings=request.provider_specific_settings
    )
    
    try:
        created = repository.create(provider)
        return created
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create provider: {str(e)}"
        )


@router.put("/{guid}", response_model=ProviderResponse)
async def update_provider(
    guid: str,
    request: ProviderUpdateRequest,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """
    Update a provider (admin only).
    
    Args:
        guid: Provider GUID
        request: Provider update request
        db: Database session
        admin_user: Current admin user (from dependency)
        
    Returns:
        Updated provider
        
    Raises:
        HTTPException: If provider not found (404) or update fails
    """
    repository = ProviderRepository(db)
    provider = repository.get_by_guid(guid)
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider with GUID '{guid}' not found"
        )
    
    # Update fields
    if request.name is not None:
        provider.name = request.name
    if request.api_key is not None:
        provider.api_key_encrypted = EncryptionService.encrypt(request.api_key)
    if request.base_url is not None:
        provider.base_url = request.base_url
    if request.config is not None:
        provider.config = request.config
    if request.is_active is not None:
        provider.is_active = request.is_active
    if request.provider_specific_settings is not None:
        provider.provider_specific_settings = request.provider_specific_settings
    
    try:
        updated = repository.update(provider)
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update provider: {str(e)}"
        )


@router.delete("/{guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_provider(
    guid: str,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """
    Delete a provider (admin only).
    
    Args:
        guid: Provider GUID
        db: Database session
        admin_user: Current admin user (from dependency)
        
    Raises:
        HTTPException: If provider not found (404)
    """
    repository = ProviderRepository(db)
    provider = repository.get_by_guid(guid)
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider with GUID '{guid}' not found"
        )
    
    repository.delete(provider)
    return None


@router.post("/{guid}/test", response_model=ProviderTestResponse)
async def test_provider(
    guid: str,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    """
    Test provider connection and configuration (admin only).
    
    Args:
        guid: Provider GUID
        db: Database session
        admin_user: Current admin user (from dependency)
        
    Returns:
        Test result with success status and message
        
    Raises:
        HTTPException: If provider not found (404)
    """
    provider_service = ProviderService(db)
    
    # Load provider instance
    provider_instance = provider_service.load_provider_by_guid(guid)
    
    if not provider_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider with GUID '{guid}' not found or invalid"
        )
    
    # Test health check
    try:
        is_healthy = await provider_instance.health_check()
        
        if is_healthy:
            return ProviderTestResponse(
                success=True,
                message="Provider connection test successful",
                details={"health_check": "passed"}
            )
        else:
            return ProviderTestResponse(
                success=False,
                message="Provider health check failed",
                details={"health_check": "failed"}
            )
    except ProviderException as e:
        return ProviderTestResponse(
            success=False,
            message=f"Provider test failed: {str(e)}",
            details={"error": str(e)}
        )
    except Exception as e:
        return ProviderTestResponse(
            success=False,
            message=f"Unexpected error during provider test: {str(e)}",
            details={"error": str(e)}
        )

