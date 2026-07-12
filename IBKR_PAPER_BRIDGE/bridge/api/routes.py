"""REST endpoints wired to the running engine, broker, and Store."""

from __future__ import annotations

from datetime import UTC, datetime
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
        "reconcile_ready": False,
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
        engine = _engine(request)
        if engine is not None:
            request.app.state.bridge_status.update(engine.status())
        return dict(request.app.state.bridge_status)

    @app.get("/api/config")
    async def get_config(request: Request) -> dict[str, Any]:
        return dict(request.app.state.bridge_config)

    @app.put("/api/config")
    async def put_config(request: Request, x_confirm: int | None = Header(default=None)) -> dict[str, Any]:
        _require_confirm(request, x_confirm)
        payload = await request.json()
        if "broker" in payload and "network" in payload["broker"]:
            raise HTTPException(status_code=422, detail="broker.network is restart-only")
        before = dict(request.app.state.bridge_config)
        request.app.state.bridge_config.update(payload)
        store = _store(request)
        if store is not None:
            store.insert_event("runtime", datetime.now(UTC), "INFO", "CONFIG_CHANGED", f"before={before}; after={payload}")
        await _bump_and_broadcast(request, "status", dict(request.app.state.bridge_status))
        return dict(request.app.state.bridge_config)

    @app.post("/api/arm")
    async def arm(request: Request, x_confirm: int | None = Header(default=None)) -> dict[str, Any]:
        _require_confirm(request, x_confirm)
        engine = _engine(request)
        if engine is not None:
            try:
                await engine.arm()
            except RuntimeError as exc:
                raise HTTPException(status_code=409, detail=str(exc)) from exc
            request.app.state.bridge_status.update(engine.status())
        else:
            _set_state(request, "ARMED")
        await _bump_and_broadcast(request, "status", dict(request.app.state.bridge_status))
        return dict(request.app.state.bridge_status)

    @app.post("/api/disarm")
    async def disarm(request: Request) -> dict[str, Any]:
        engine = _engine(request)
        if engine is not None:
            await engine.disarm_runtime()
            request.app.state.bridge_status.update(engine.status())
        else:
            _set_state(request, "DISARMED")
        await _bump_and_broadcast(request, "status", dict(request.app.state.bridge_status))
        return dict(request.app.state.bridge_status)

    @app.post("/api/kill")
    async def kill(request: Request, flatten: bool = False) -> dict[str, Any]:
        engine = _engine(request)
        if engine is not None:
            await engine.kill(flatten=flatten)
            request.app.state.bridge_status.update(engine.status())
        else:
            _set_state(request, "KILLED")
        request.app.state.bridge_status["flatten_requested"] = flatten
        await _bump_and_broadcast(request, "status", dict(request.app.state.bridge_status))
        return dict(request.app.state.bridge_status)

    @app.post("/api/kill/ack")
    async def kill_ack(request: Request) -> dict[str, Any]:
        engine = _engine(request)
        if engine is not None:
            await engine.acknowledge_kill()
            request.app.state.bridge_status.update(engine.status())
        else:
            _set_state(request, "DISARMED")
        await _bump_and_broadcast(request, "status", dict(request.app.state.bridge_status))
        return dict(request.app.state.bridge_status)

    @app.get("/api/bars")
    async def bars(request: Request, n: int = 300) -> dict[str, Any]:
        store = _store(request)
        rows = store.get_bars(n) if store is not None else []
        return {"bars": [_chart_bar(row) for row in rows]}

    @app.get("/api/snapshot")
    async def snapshot(request: Request) -> dict[str, Any]:
        return await make_snapshot(request.app)

    @app.get("/api/gates/latest")
    async def gates_latest(request: Request) -> dict[str, Any]:
        store = _store(request)
        return store.get_latest_gates() if store is not None else {"gate_results": []}

    @app.get("/api/positions")
    async def positions(request: Request) -> list[Any]:
        engine = _engine(request)
        return [row.model_dump(mode="json") for row in await engine.broker.positions()] if engine is not None else []

    @app.get("/api/orders")
    async def orders(request: Request) -> list[Any]:
        engine = _engine(request)
        return [row.model_dump(mode="json") for row in await engine.broker.open_orders()] if engine is not None else []

    @app.get("/api/trades")
    async def trades(request: Request, limit: int = 50) -> list[Any]:
        store = _store(request)
        return store.get_trades(limit) if store is not None else []

    @app.get("/api/decisions")
    async def decisions(request: Request, trade_id: int | None = None) -> list[Any]:
        store = _store(request)
        return store.get_decisions(trade_id) if store is not None else []

    @app.get("/api/equity")
    async def equity(request: Request) -> list[Any]:
        store = _store(request)
        return store.get_equity() if store is not None else []

    @app.get("/api/events")
    async def events(request: Request, severity: str | None = None) -> list[Any]:
        store = _store(request)
        return store.get_events(severity) if store is not None else []

    @app.get("/api/runs/{run_id}")
    async def run(request: Request, run_id: str) -> dict[str, Any]:
        store = _store(request)
        row = store.get_run(run_id) if store is not None else None
        if row is None:
            raise HTTPException(status_code=404, detail="run not found")
        return row


async def make_snapshot(app: FastAPI) -> dict[str, Any]:
    engine = getattr(app.state, "bridge_engine", None)
    store = getattr(app.state, "bridge_store", None)
    positions = [row.model_dump(mode="json") for row in await engine.broker.positions()] if engine is not None else []
    orders = [row.model_dump(mode="json") for row in await engine.broker.open_orders()] if engine is not None else []
    bars = [_chart_bar(row) for row in store.get_bars(300)] if store is not None else []
    return {
        "status": dict(app.state.bridge_status),
        "config": dict(app.state.bridge_config),
        "positions": positions,
        "orders": orders,
        "trades": store.get_trades(50) if store is not None else [],
        "events": store.get_events(limit=100) if store is not None else [],
        "latest_gates": store.get_latest_gates() if store is not None else {"gate_results": []},
        "equity": store.get_equity() if store is not None else [],
        "bars": {"bars": bars},
    }


def _engine(request: Request):
    return getattr(request.app.state, "bridge_engine", None)


def _store(request: Request) -> Store | None:
    return getattr(request.app.state, "bridge_store", None)


def _require_confirm(request: Request, x_confirm: int | None) -> None:
    expected = int(request.app.state.bridge_status["state_version"])
    if x_confirm != expected:
        raise HTTPException(status_code=409, detail="stale state_version")


async def _bump_and_broadcast(request: Request, topic: str, data: object) -> None:
    request.app.state.bridge_status["state_version"] += 1
    if topic == "status":
        data = dict(request.app.state.bridge_status)
    hub = getattr(request.app.state, "ws_hub", None)
    if hub is not None:
        await hub.broadcast(topic, data)


def _set_state(request: Request, state: str) -> None:
    request.app.state.bridge_status["state"] = state
    store = _store(request)
    if store is not None:
        store.set_meta("app_state", state)


def _chart_bar(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "time": int(datetime.fromisoformat(row["bar_end_ts"]).timestamp()),
        "open": row["open"],
        "high": row["high"],
        "low": row["low"],
        "close": row["close"],
        "volume": row["volume"],
    }
