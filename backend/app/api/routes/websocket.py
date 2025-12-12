"""
WebSocket routes for real-time updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import get_websocket_manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time threat intelligence updates.
    
    Clients connecting to this endpoint will receive broadcast messages
    when new threat data is available.
    """
    manager = get_websocket_manager()
    
    # Accept connection
    await websocket.accept()
    manager.connect(websocket)
    
    try:
        # Keep connection alive and handle client messages (ping/pong)
        while True:
            # Wait for messages from client (optional ping/pong)
            data = await websocket.receive_text()
            # Echo back for keepalive (optional)
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        # Client disconnected normally
        manager.disconnect(websocket)
    except Exception:
        # Any other error, disconnect
        manager.disconnect(websocket)
        raise

