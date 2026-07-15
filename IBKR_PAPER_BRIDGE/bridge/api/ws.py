"""Persistent WebSocket hub with snapshot-on-connect resynchronization."""

from __future__ import annotations

import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from bridge.api.routes import make_snapshot


class WebSocketHub:
    def __init__(self) -> None:
        self.connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self.connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self.connections.discard(websocket)

    async def broadcast(self, topic: str, data: object) -> None:
        message = {"topic": topic, "data": data}
        stale: list[WebSocket] = []
        for websocket in list(self.connections):
            try:
                await websocket.send_json(message)
            except Exception:
                stale.append(websocket)
        for websocket in stale:
            await self.disconnect(websocket)


def install_ws(app: FastAPI) -> WebSocketHub:
    hub = WebSocketHub()
    app.state.ws_hub = hub

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        await hub.connect(websocket)
        await websocket.send_json({"topic": "snapshot", "data": await make_snapshot(websocket.app)})
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await hub.disconnect(websocket)

    return hub
