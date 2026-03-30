from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any
import asyncio
import sys
from pathlib import Path
from chatur.utils.logger import setup_logger
from chatur.api.routes import settings, history

# Setup logger
logger = setup_logger('chatur.api')

# Global reference to the running event loop (set during lifespan startup)
server_loop = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    global server_loop
    server_loop = asyncio.get_running_loop()
    logger.info(f"API server started, loop captured: {server_loop}")
    yield
    logger.info("API server shutting down")


app = FastAPI(lifespan=lifespan)

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes first so they take priority over the static file catch-all
app.include_router(settings.router, prefix="/api")
app.include_router(history.router, prefix="/api")


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
            # Keep connection open; most communication is Server → Client
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


def broadcast_message_sync(status: str, data: Dict = None):
    """Thread-safe broadcast from non-async (background) threads."""
    if server_loop and server_loop.is_running():
        msg = {"status": status}
        if data:
            msg.update(data)
        asyncio.run_coroutine_threadsafe(manager.broadcast(msg), server_loop)
    else:
        logger.warning("Cannot broadcast: server loop not running yet")


def run_api_server(host="0.0.0.0", port=8000):
    import uvicorn

    # On Windows with Python ≥3.10, ProactorEventLoop is the default which
    # conflicts with uvicorn's selector-based loop.  Switch to the selector
    # loop policy before starting the server.
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Mount static UI files last so explicit API/WS routes take priority.
    # (StaticFiles at "/" would otherwise swallow WebSocket upgrade requests.)
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent.parent

    ui_dist_path = base_path / "ui" / "dist"
    if ui_dist_path.exists():
        app.mount("/", StaticFiles(directory=str(ui_dist_path), html=True), name="static")
        logger.info(f"Serving UI from {ui_dist_path}")
    else:
        logger.warning(f"UI dist directory not found at {ui_dist_path}")

    uvicorn.run(app, host=host, port=port, log_level="warning")
