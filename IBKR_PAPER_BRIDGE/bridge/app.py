"""FastAPI application factory for Crypto Paper Bridge."""

from __future__ import annotations

import argparse
import logging
import os
from collections.abc import Mapping
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from bridge.api.routes import init_runtime_state, install_routes
from bridge.api.ws import install_ws
from bridge.store.db import Store

logger = logging.getLogger(__name__)

#: Infrastructure-only override for the runtime SQLite location. Used by the
#: Linux deployment (`/var/lib/mtc-bridge/bridge.db`) so the writable state
#: directory can live outside the read-only release tree. Unset everywhere
#: else, which keeps the in-repo default untouched.
STATE_DB_ENV_VAR = "MTC_BRIDGE_STATE_DB"
START_MODE_ENV_VAR = "MTC_BRIDGE_START_MODE"
CREDENTIALED_START_MODE = "credentialed"
CREDENTIAL_FREE_DISARMED_START_MODE = "credential_free_disarmed"


def resolve_start_mode(
    cli_value: str | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    """Resolve an explicit runtime mode without weakening the normal default."""
    environ = os.environ if env is None else env
    raw = cli_value if cli_value is not None else environ.get(START_MODE_ENV_VAR)
    if raw is None:
        return CREDENTIALED_START_MODE
    mode = raw.strip()
    if mode not in {
        CREDENTIALED_START_MODE,
        CREDENTIAL_FREE_DISARMED_START_MODE,
    }:
        raise ValueError(
            f"--start-mode/{START_MODE_ENV_VAR} has an invalid start mode"
        )
    return mode


def resolve_state_db_path(
    cli_value: str | None = None,
    env: Mapping[str, str] | None = None,
) -> Path | None:
    """Resolve the runtime database path from the CLI first, then the env var.

    Returns ``None`` when neither source is set, so ``create_app`` keeps its
    existing ``<repo>/data/bridge.db`` default. Purely infrastructural: no
    trading, risk, or strategy behaviour depends on this value.

    Fails closed (``ValueError``) on an empty or relative path rather than
    silently writing runtime state to an unexpected location.
    """
    environ = os.environ if env is None else env
    raw = cli_value if cli_value is not None else environ.get(STATE_DB_ENV_VAR)
    if raw is None:
        return None
    candidate = raw.strip()
    if not candidate:
        raise ValueError(f"--state-db/{STATE_DB_ENV_VAR} is set but empty")
    path = Path(candidate)
    posix_path = PurePosixPath(candidate)
    # The deployment contract is POSIX, but the repository suite also runs on
    # Windows. Accept a native absolute path or an absolute POSIX path so the
    # exact Linux value can be validated without weakening the runtime check.
    if not (path.is_absolute() or posix_path.is_absolute()):
        raise ValueError(
            f"--state-db/{STATE_DB_ENV_VAR} must be an absolute path, got a relative one"
        )
    if ".." in path.parts or ".." in posix_path.parts:
        raise ValueError(f"--state-db/{STATE_DB_ENV_VAR} must not contain parent traversal")
    return path


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
    start_mode: str | None = None,
) -> FastAPI:
    """Build an import-safe FastAPI app, resolving start mode from arg then env."""
    start_mode = resolve_start_mode(cli_value=start_mode)
    credential_free_disarmed = start_mode == CREDENTIAL_FREE_DISARMED_START_MODE
    if credential_free_disarmed and dry_run:
        raise ValueError("credential-free DISARMED start mode cannot use --dry-run")
    if credential_free_disarmed and broker is not None:
        raise ValueError("credential-free DISARMED start mode cannot accept a broker")
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
    app.state.credential_free_disarmed = credential_free_disarmed
    if credential_free_disarmed:
        app.state.bridge_status.update(
            {
                "mode": CREDENTIAL_FREE_DISARMED_START_MODE,
                "network": "disabled",
                "exchange_conn": "disabled",
                "exchange_enabled": False,
                "credential_lookup": "disabled",
                "arm_enabled": False,
            }
        )
    if start_runtime and not credential_free_disarmed:
        runtime_broker = broker or _build_broker(root, dry_run)
        run_id = f"{'dryrun' if dry_run else 'paper'}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"

        from bridge.engine.engine import BridgeEngine
        from bridge.engine.risk import RiskConfig, RiskEngine
        from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8

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
            policy_id=str(risk_cfg_raw.get("policy_id", "ts-p1-007-v1")),
            risk_pct_per_trade=float(risk_cfg_raw.get("risk_pct_per_trade", 0.005)),
            max_daily_loss_pct=float(risk_cfg_raw.get("max_daily_loss_pct", 0.02)),
            max_intraday_drawdown_pct=float(
                risk_cfg_raw.get("max_intraday_drawdown_pct", 0.05)
            ),
            equity_floor_usdc=float(
                risk_cfg_raw.get("equity_floor_usdc", 500.0)
            ),
            max_position_notional_pct=0.5 if dry_run else float(risk_cfg_raw.get("max_position_notional_pct", 0.20)),
            min_stop_distance_pct=float(risk_cfg_raw.get("min_stop_distance_pct", 0.001)),
            min_order_usd=float(risk_cfg_raw.get("min_order_usd", 10)),
            max_leverage=int(risk_cfg_raw.get("max_leverage", 1)),
            max_consecutive_losses=int(risk_cfg_raw.get("max_consecutive_losses", 3)),
            exposure_policy_id=str(risk_cfg_raw.get("exposure_policy_id", "ts-p1-008-v1")),
            max_symbol_gross_pct=float(risk_cfg_raw.get("max_symbol_gross_pct", 0.20)),
            max_portfolio_gross_pct=float(risk_cfg_raw.get("max_portfolio_gross_pct", 0.40)),
            max_wallet_margin_util_pct=float(risk_cfg_raw.get("max_wallet_margin_util_pct", 0.25)),
            max_effective_leverage=float(risk_cfg_raw.get("max_effective_leverage", 1.0)),
            min_liquidation_distance_pct=float(risk_cfg_raw.get("min_liquidation_distance_pct", 0.15)),
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
            bar_data_restore_timeout_s=float(broker_cfg_raw.get("data_restore_timeout_s", 300.0)),
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
        from bridge.broker.mock import MockBroker

        broker = MockBroker.from_csv(root / "tests" / "fixtures" / "BTC_1h.csv", starting_equity=100000)
        broker.streaming = True
        return broker
    # E1: resolve credentials process-env-first, then HKCU registry — the
    # BaseSettings defaults are empty when the parent process predates the
    # user-env variables.
    from bridge.broker.hyperliquid import HyperliquidBroker
    from bridge.settings import resolve_hyperliquid_credentials

    account_address, api_wallet_key, _source = resolve_hyperliquid_credentials()
    return HyperliquidBroker(
        network="testnet",
        account_address=account_address,
        api_wallet_key=api_wallet_key,
        coin="BTC",
        leverage=1,
    )


if __name__ != "__main__":
    app = create_app()


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--start-mode",
        default=None,
        metavar="MODE",
        help=(
            f"runtime start mode; use {CREDENTIAL_FREE_DISARMED_START_MODE!r} "
            f"for credential-free DISARMED operation, or set {START_MODE_ENV_VAR}"
        ),
    )
    parser.add_argument(
        "--state-db",
        default=None,
        metavar="PATH",
        help=(
            "absolute path to the runtime SQLite database; overrides "
            f"{STATE_DB_ENV_VAR}. Omit both to keep the in-repo default."
        ),
    )
    args = parser.parse_args()
    runtime_app = create_app(
        dry_run=args.dry_run,
        store_path=resolve_state_db_path(args.state_db),
        start_runtime=True,
        start_mode=resolve_start_mode(args.start_mode),
    )
    uvicorn.run(runtime_app, host="127.0.0.1", port=8790, reload=False)
