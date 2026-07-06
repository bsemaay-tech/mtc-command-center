"""WebSocket hub."""

from __future__ import annotations

from fastapi import FastAPI, WebSocket

from bridge.api.routes import make_snapshot


def install_ws(app: FastAPI) -> None:
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        await websocket.accept()
        await websocket.send_json({"topic": "snapshot", "data": make_snapshot(websocket.app)})
        await websocket.close()
