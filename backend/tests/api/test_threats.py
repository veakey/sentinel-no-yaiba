"""
Tests for /api/threats endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from app.main import app
from app.api.dependencies import get_threat_service
from app.services.threat_service import ThreatService


@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def mock_threat_service():
    """Fixture for mocked ThreatService"""
    service = MagicMock(spec=ThreatService)
    service.get_threats = AsyncMock()
    return service


def test_get_threats_endpoint_exists(client):
    """Test that GET /api/threats endpoint exists"""
    response = client.get("/api/threats")
    # Should not be 404
    assert response.status_code != 404


def test_get_threats_returns_aggregated_data(client, mock_threat_service):
    """Test that GET /api/threats returns aggregated threat data"""
    expected_data = {
        "ninja": {"data": [{"id": "n1", "severity": "high"}]},
        "malwarebytes": {"results": [{"id": "m1", "severity": "critical"}]}
    }
    
    mock_threat_service.get_threats.return_value = expected_data
    
    # Override dependency
    app.dependency_overrides[get_threat_service] = lambda: mock_threat_service
    
    try:
        response = client.get("/api/threats")
        assert response.status_code == 200
        data = response.json()
        assert "ninja" in data
        assert "malwarebytes" in data
    finally:
        # Clean up override
        app.dependency_overrides.clear()


def test_get_threats_respects_force_refresh_param(client, mock_threat_service):
    """Test that force_refresh query parameter is respected"""
    mock_threat_service.get_threats.return_value = {"data": "fresh"}
    
    app.dependency_overrides[get_threat_service] = lambda: mock_threat_service
    
    try:
        response = client.get("/api/threats?force_refresh=true")
        assert response.status_code == 200
        # Verify service was called with force_refresh=True
        mock_threat_service.get_threats.assert_called_once()
        call_args = mock_threat_service.get_threats.call_args
        assert call_args.kwargs.get('force_refresh') is True
    finally:
        app.dependency_overrides.clear()


def test_get_threats_passes_params_to_service(client, mock_threat_service):
    """Test that query parameters are passed to ThreatService"""
    mock_threat_service.get_threats.return_value = {"data": "test"}
    
    app.dependency_overrides[get_threat_service] = lambda: mock_threat_service
    
    try:
        response = client.get("/api/threats?severity=high&status=active")
        assert response.status_code == 200
        call_args = mock_threat_service.get_threats.call_args
        params = call_args.kwargs.get('params', {})
        assert params.get('severity') == 'high'
        assert params.get('status') == 'active'
    finally:
        app.dependency_overrides.clear()


def test_get_threats_handles_service_errors(client, mock_threat_service):
    """Test that service errors are handled gracefully"""
    from app.core.exceptions import ProviderException
    
    mock_threat_service.get_threats.side_effect = ProviderException("Service error")
    
    app.dependency_overrides[get_threat_service] = lambda: mock_threat_service
    
    try:
        response = client.get("/api/threats")
        # Should return error response
        assert response.status_code >= 400
        data = response.json()
        assert "detail" in data
    finally:
        app.dependency_overrides.clear()


def test_get_threats_returns_json(client):
    """Test that response is valid JSON"""
    response = client.get("/api/threats")
    # Even if error, should be JSON
    assert response.headers.get("content-type") == "application/json"

