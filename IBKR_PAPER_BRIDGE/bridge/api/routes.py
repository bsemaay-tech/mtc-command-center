"""REST endpoint definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, Header, HTTPException, Request

from bridge.store.db import Store


def load_config() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[2] / "config" / "bridge.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def init_runtime_state(app: FastAPI, store: Store | None = None) -> None:
    if store is not None and store.get_meta("app_state") is None:
        store.set_meta("app_state", "DISARMED")
    app.state.bridge_status = {
        "state": store.get_meta("app_state") if store is not None else "DISARMED",
        "mode": "paper",
        "network": "testnet",
        "exchange_conn": "mock",
        "regime": "BOTH",
        "state_version": 1,
    }
    app.state.bridge_store = store
    app.state.bridge_config = load_config()
    app.state.bridge_bars = {"bars": []}
    app.state.bridge_data = {
        "positions": [],
        "orders": [],
        "trades": [],
        "events": [],
        "latest_gates": {"gate_results": []},
    }


def install_routes(app: FastAPI) -> None:
    @app.get("/api/status")
    async def status(request: Request) -> dict[str, Any]:
        return dict(request.app.state.bridge_status)

    @app.get("/api/config")
    async def get_config(request: Request) -> dict[str, Any]:
        return dict(request.app.state.bridge_config)

    @app.put("/api/config")
    async def put_config(request: Request, x_confirm: int | None = Header(default=None)) -> dict[str, Any]:
        _require_confirm(request, x_confirm)
        payload = await request.json()
        request.app.state.bridge_config.update(payload)
        _bump(request)
        return dict(request.app.state.bridge_config)

    @app.post("/api/arm")
    async def arm(request: Request, x_confirm: int | None = Header(default=None)) -> dict[str, Any]:
        _require_confirm(request, x_confirm)
        _set_state(request, "ARMED")
        _bump(request)
        return dict(request.app.state.bridge_status)

    @app.post("/api/disarm")
    async def disarm(request: Request) -> dict[str, Any]:
        _set_state(request, "DISARMED")
        _bump(request)
        return dict(request.app.state.bridge_status)

    @app.post("/api/kill")
    async def kill(request: Request, flatten: bool = False) -> dict[str, Any]:
        _set_state(request, "KILLED")
        request.app.state.bridge_status["flatten_requested"] = flatten
        _bump(request)
        return dict(request.app.state.bridge_status)

    @app.post("/api/kill/ack")
    async def kill_ack(request: Request) -> dict[str, Any]:
        _set_state(request, "DISARMED")
        _bump(request)
        return dict(request.app.state.bridge_status)

    @app.get("/api/bars")
    async def bars(request: Request, n: int = 300) -> dict[str, Any]:
        return {"bars": request.app.state.bridge_bars["bars"][-n:]}

    @app.get("/api/snapshot")
    async def snapshot(request: Request) -> dict[str, Any]:
        return make_snapshot(request.app)

    @app.get("/api/gates/latest")
    async def gates_latest() -> dict[str, Any]:
        return {"gate_results": []}

    @app.get("/api/positions")
    async def positions() -> list[Any]:
        return []

    @app.get("/api/orders")
    async def orders() -> list[Any]:
        return []

    @app.get("/api/trades")
    async def trades(limit: int = 50) -> list[Any]:
        return []

    @app.get("/api/decisions")
    async def decisions(trade_id: int | None = None) -> list[Any]:
        return []

    @app.get("/api/equity")
    async def equity() -> list[Any]:
        return []

    @app.get("/api/events")
    async def events(severity: str | None = None) -> list[Any]:
        return []

    @app.get("/api/runs/{run_id}")
    async def run(run_id: str) -> dict[str, Any]:
        return {"run_id": run_id}


def make_snapshot(app: FastAPI) -> dict[str, Any]:
    return {
        "status": dict(app.state.bridge_status),
        "config": dict(app.state.bridge_config),
        "positions": list(app.state.bridge_data["positions"]),
        "orders": list(app.state.bridge_data["orders"]),
        "trades": list(app.state.bridge_data["trades"]),
        "events": list(app.state.bridge_data["events"]),
        "latest_gates": dict(app.state.bridge_data["latest_gates"]),
        "bars": {"bars": list(app.state.bridge_bars["bars"])},
    }


def _require_confirm(request: Request, x_confirm: int | None) -> None:
    expected = int(request.app.state.bridge_status["state_version"])
    if x_confirm != expected:
        raise HTTPException(status_code=409, detail="stale state_version")


def _bump(request: Request) -> None:
    request.app.state.bridge_status["state_version"] += 1


def _set_state(request: Request, state: str) -> None:
    request.app.state.bridge_status["state"] = state
    store = getattr(request.app.state, "bridge_store", None)
    if store is not None:
        store.set_meta("app_state", state)
