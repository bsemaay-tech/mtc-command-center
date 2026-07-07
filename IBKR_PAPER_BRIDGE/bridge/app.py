"""FastAPI application factory for Crypto Paper Bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from bridge.api.routes import init_runtime_state, install_routes
from bridge.api.ws import install_ws
from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.store.db import Store

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Crypto Paper Bridge starting")
    yield
    logger.info("Crypto Paper Bridge shutting down")


def create_app(dry_run: bool = False, store_path: str | Path | None = None) -> FastAPI:
    """Build an import-safe FastAPI app without exchange or LLM calls."""
    app = FastAPI(
        title="Crypto Paper Bridge",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:8790", "http://localhost:8790"],
        allow_methods=["GET", "POST", "PUT"],
        allow_headers=["X-Confirm", "Content-Type"],
    )
    store = None
    if store_path is not None:
        store = Store(store_path)
        store.initialize()
    init_runtime_state(app, store=store)
    if dry_run:
        _preload_dry_run(app)
    install_routes(app)
    install_ws(app)

    static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return (static_dir / "index.html").read_text(encoding="utf-8")

    return app


def _preload_dry_run(app: FastAPI) -> None:
    root = Path(__file__).resolve().parents[1]
    store = Store(root / "data" / "bridge.db")
    store.initialize()
    broker = MockBroker.from_csv(root / "tests" / "fixtures" / "BTC_1h.csv", starting_equity=100000)
    engine = BridgeEngine(
        run_id=f"dryrun-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
    )
    asyncio.run(engine.run_replay(max_bars=80))
    snapshot = store.get_snapshot()
    app.state.bridge_status["mode"] = "dry_run"
    app.state.bridge_data["orders"] = snapshot["orders"][-25:]
    app.state.bridge_data["trades"] = snapshot["trades"][-25:]
    app.state.bridge_data["events"] = snapshot["events"][-25:]
    app.state.bridge_bars["bars"] = [
        {
            "time": int(datetime.fromisoformat(row["bar_end_ts"]).timestamp()),
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row["volume"],
        }
        for row in snapshot["bars"][-300:]
    ]


app = create_app()


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    runtime_app = create_app(dry_run=args.dry_run)
    uvicorn.run(runtime_app, host="127.0.0.1", port=8790, reload=False)
