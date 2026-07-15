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
                app.state.bridge_status["state_version"] += 1
                data = dict(app.state.bridge_status)
            hub = getattr(app.state, "ws_hub", None)
            if hub is not None:
                await hub.broadcast(topic, data)

        # C3/C4: engine risk limits come from config/bridge.yaml (frozen P2
        # profile), not hardcoded literals. Dry-run keeps the wider notional
        # so the fixture replay still trades.
        import yaml as _yaml

        bridge_cfg_raw = _yaml.safe_load((root / "config" / "bridge.yaml").read_text(encoding="utf-8"))
        risk_cfg_raw = bridge_cfg_raw.get("risk", {})
        broker_cfg_raw = bridge_cfg_raw.get("broker", {})
        risk_config = RiskConfig(
            risk_pct_per_trade=float(risk_cfg_raw.get("risk_pct_per_trade", 0.005)),
            max_daily_loss_pct=float(risk_cfg_raw.get("max_daily_loss_pct", 0.02)),
            max_position_notional_pct=0.5 if dry_run else float(risk_cfg_raw.get("max_position_notional_pct", 0.20)),
            min_stop_distance_pct=float(risk_cfg_raw.get("min_stop_distance_pct", 0.001)),
            min_order_usd=float(risk_cfg_raw.get("min_order_usd", 10)),
            max_leverage=int(risk_cfg_raw.get("max_leverage", 1)),
            max_consecutive_losses=int(risk_cfg_raw.get("max_consecutive_losses", 3)),
        )
        from bridge.engine.notify import build_notifier

        engine = BridgeEngine(
            run_id=run_id,
            broker=runtime_broker,
            store=store,
            strategy=KeltnerTrailEma8(),
            risk_engine=RiskEngine(risk_config),
            notifier=build_notifier(),
            state="DISARMED",
            mode="dry_run" if dry_run else "paper",
            on_update=publish,
            reconcile_max_consecutive_failures=int(
                risk_cfg_raw.get("reconcile_max_consecutive_failures", 3)
            ),
            bar_reconnect_attempts=int(broker_cfg_raw.get("reconnect_attempts", 9)),
            bar_reconnect_base_delay_s=float(broker_cfg_raw.get("reconnect_base_delay_s", 5.0)),
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
    # E1: resolve credentials process-env-first, then HKCU registry — the
    # BaseSettings defaults are empty when the parent process predates the
    # user-env variables.
    from bridge.settings import resolve_hyperliquid_credentials

    account_address, api_wallet_key, _source = resolve_hyperliquid_credentials()
    return HyperliquidBroker(
        network="testnet",
        account_address=account_address,
        api_wallet_key=api_wallet_key,
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
