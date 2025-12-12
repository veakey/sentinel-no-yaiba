"""
WebSocket connection manager
"""
from typing import List, Dict, Any
from fastapi import WebSocket


# Global WebSocket manager instance
_websocket_manager: 'WebSocketManager' = None


def get_websocket_manager() -> 'WebSocketManager':
    """
    Get the global WebSocket manager instance (singleton pattern).
    
    Returns:
        WebSocketManager instance
    """
    global _websocket_manager
    if _websocket_manager is None:
        _websocket_manager = WebSocketManager()
    return _websocket_manager


class WebSocketManager:
    """
    Manages WebSocket connections and broadcasts messages to all connected clients.
    """
    
    def __init__(self):
        """Initialize WebSocketManager with empty connections list."""
        self.connections: List[WebSocket] = []
    
    def connect(self, websocket: WebSocket):
        """
        Add a WebSocket connection to the manager.
        
        Args:
            websocket: WebSocket connection to add
        """
        if websocket not in self.connections:
            self.connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection from the manager.
        
        Args:
            websocket: WebSocket connection to remove
        """
        if websocket in self.connections:
            self.connections.remove(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: Dictionary to send as JSON to all clients
        """
        disconnected = []
        
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Connection closed or error, mark for removal
                disconnected.append(connection)
        
        # Remove failed connections
        for connection in disconnected:
            self.disconnect(connection)
    
    def count(self) -> int:
        """
        Get the number of active connections.
        
        Returns:
            Number of connected clients
        """
        return len(self.connections)

