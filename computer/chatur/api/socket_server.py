from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List, Dict, Any
import json
import asyncio
from chatur.utils.logger import setup_logger
from chatur.api.routes import settings, history

# Setup logger
logger = setup_logger('chatur.api')

app = FastAPI()

# Include routes
app.include_router(settings.router, prefix="/api")
app.include_router(history.router, prefix="/api")

from fastapi.staticfiles import StaticFiles
import sys
from pathlib import Path

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine path to UI assets (handle Dev vs PyInstaller)
if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    base_path = Path(sys._MEIPASS)
else:
    # Running in dev mode
    base_path = Path(__file__).parent.parent.parent

ui_dist_path = base_path / "ui" / "dist"

if ui_dist_path.exists():
    app.mount("/", StaticFiles(directory=str(ui_dist_path), html=True), name="static")
    logger.info(f"Serving UI from {ui_dist_path}")
else:
    logger.warning(f"UI dist directory not found at {ui_dist_path}")

class ConnectionManager:
    """Manages WebSocket connections and broadcasting"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a JSON message to all connected clients"""
        if not self.active_connections:
            return
            
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Cleanup broken connections
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

@app.get("/status")
async def get_status():
    return {"status": "online", "service": "Chatur Voice Assistant"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We just keep the connection open and listen for any client messages (optional)
            # Most communication is Server -> Client
            data = await websocket.receive_text()
            # process client messages if needed
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Global reference to the event loop
server_loop = None

@app.on_event("startup")
async def startup_event():
    global server_loop
    server_loop = asyncio.get_running_loop()
    logger.info(f"Captured server loop: {server_loop}")

def broadcast_message_sync(status: str, data: Dict = None):
    """Thread-safe method to broadcast from non-async code"""
    if server_loop and server_loop.is_running():
        msg = {"status": status}
        if data:
            msg.update(data)
            
        asyncio.run_coroutine_threadsafe(manager.broadcast(msg), server_loop)
    else:
        logger.warning("Cannot broadcast: Server loop not running")

# Helper function to run the server content
def run_api_server(host="0.0.0.0", port=8000):
    import uvicorn
    # Clean up any existing loop policy issues on Windows
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host=host, port=port, log_level="warning")
