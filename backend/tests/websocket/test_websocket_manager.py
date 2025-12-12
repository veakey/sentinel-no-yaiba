"""
Tests for WebSocketManager
"""
import pytest
from app.websocket.manager import WebSocketManager


@pytest.fixture
def ws_manager():
    """Fixture for WebSocketManager"""
    return WebSocketManager()


def test_websocket_manager_initialization(ws_manager):
    """Test that WebSocketManager initializes correctly"""
    assert ws_manager.connections == []


def test_websocket_manager_connect(ws_manager):
    """Test connecting a WebSocket client"""
    mock_websocket = object()
    
    ws_manager.connect(mock_websocket)
    
    assert len(ws_manager.connections) == 1
    assert mock_websocket in ws_manager.connections


def test_websocket_manager_disconnect(ws_manager):
    """Test disconnecting a WebSocket client"""
    mock_websocket1 = object()
    mock_websocket2 = object()
    
    ws_manager.connect(mock_websocket1)
    ws_manager.connect(mock_websocket2)
    assert len(ws_manager.connections) == 2
    
    ws_manager.disconnect(mock_websocket1)
    
    assert len(ws_manager.connections) == 1
    assert mock_websocket1 not in ws_manager.connections
    assert mock_websocket2 in ws_manager.connections


def test_websocket_manager_disconnect_nonexistent(ws_manager):
    """Test disconnecting a non-existent WebSocket client"""
    mock_websocket = object()
    
    # Should not raise error
    ws_manager.disconnect(mock_websocket)
    assert len(ws_manager.connections) == 0


@pytest.mark.asyncio
async def test_websocket_manager_broadcast(ws_manager):
    """Test broadcasting message to all connected clients"""
    messages_received = []
    
    # Mock WebSocket with send_json method
    class MockWebSocket:
        def __init__(self, msg_list):
            self.msg_list = msg_list
        
        async def send_json(self, data):
            self.msg_list.append(data)
    
    mock_ws1 = MockWebSocket(messages_received)
    mock_ws2 = MockWebSocket(messages_received)
    
    ws_manager.connect(mock_ws1)
    ws_manager.connect(mock_ws2)
    
    test_message = {"type": "threats_updated", "data": "test"}
    await ws_manager.broadcast(test_message)
    
    # Both clients should receive the message
    assert len(messages_received) == 2
    assert all(msg == test_message for msg in messages_received)


@pytest.mark.asyncio
async def test_websocket_manager_broadcast_handles_errors(ws_manager):
    """Test that broadcast handles errors gracefully"""
    class FailingWebSocket:
        async def send_json(self, data):
            raise Exception("Connection error")
    
    class WorkingWebSocket:
        messages = []
        
        async def send_json(self, data):
            self.messages.append(data)
    
    failing_ws = FailingWebSocket()
    working_ws = WorkingWebSocket()
    
    ws_manager.connect(failing_ws)
    ws_manager.connect(working_ws)
    
    test_message = {"type": "threats_updated", "data": "test"}
    # Should not raise exception
    await ws_manager.broadcast(test_message)
    
    # Working client should still receive message
    assert len(working_ws.messages) == 1
    # Failed connection should be removed
    assert failing_ws not in ws_manager.connections


def test_websocket_manager_count(ws_manager):
    """Test getting connection count"""
    assert ws_manager.count() == 0
    
    ws_manager.connect(object())
    ws_manager.connect(object())
    
    assert ws_manager.count() == 2

