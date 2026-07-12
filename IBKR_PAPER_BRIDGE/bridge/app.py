"""FastAPI application factory for Crypto Paper Bridge."""

from __future__ import annotations

import argparse
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
from bridge.broker.hyperliquid import HyperliquidBroker
from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.store.db import Store
from bridge.settings import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Crypto Paper Bridge starting")
    engine = getattr(app.state, "bridge_engine", None)
    if engine is not None:
        await engine.start()
    try:
        yield
    finally:
        if engine is not None:
            await engine.stop()
        logger.info("Crypto Paper Bridge shutting down")


def create_app(
    dry_run: bool = False,
    store_path: str | Path | None = None,
    start_runtime: bool = False,
    broker=None,
) -> FastAPI:
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
    root = Path(__file__).resolve().parents[1]
    store = None
    if store_path is not None or start_runtime:
        store = Store(store_path or root / "data" / "bridge.db")
        store.initialize()
        if store.get_meta("app_state") != "KILLED":
            store.set_meta("app_state", "DISARMED")
    init_runtime_state(app, store=store)
    app.state.bridge_engine = None
    if start_runtime:
        runtime_broker = broker or _build_broker(root, dry_run)
        run_id = f"{'dryrun' if dry_run else 'paper'}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"

        async def publish(topic: str, data: object) -> None:
            if topic == "status" and isinstance(data, dict):
                app.state.bridge_status.update(data)

        engine = BridgeEngine(
            run_id=run_id,
            broker=runtime_broker,
            store=store,
            strategy=KeltnerTrailEma8(),
            risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
            state="DISARMED",
            mode="dry_run" if dry_run else "paper",
            on_update=publish,
        )
        app.state.bridge_engine = engine
        app.state.bridge_status["mode"] = "dry_run" if dry_run else "paper"
        app.state.bridge_status["exchange_conn"] = "mock" if dry_run else "hyperliquid"
    install_routes(app)
    install_ws(app)

    static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return (static_dir / "index.html").read_text(encoding="utf-8")

    return app


def _build_broker(root: Path, dry_run: bool):
    if dry_run:
        broker = MockBroker.from_csv(root / "tests" / "fixtures" / "BTC_1h.csv", starting_equity=100000)
        broker.streaming = True
        return broker
    return HyperliquidBroker(
        network="testnet",
        account_address=settings.hl_account_address,
        api_wallet_key=settings.hl_api_wallet_key,
        coin="BTC",
        leverage=1,
    )


app = create_app()


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    runtime_app = create_app(dry_run=args.dry_run, start_runtime=True)
    uvicorn.run(runtime_app, host="127.0.0.1", port=8790, reload=False)
