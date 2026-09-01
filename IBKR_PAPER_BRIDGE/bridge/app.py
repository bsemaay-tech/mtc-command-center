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
from bridge.broker.hyperliquid import HyperliquidBroker
from bridge.broker.mock import MockBroker
from bridge.config_contract import (
    ConfigIssue,
    RefusalKind,
    StartupConfigRefusal,
    construct_bridge_engine,
    prepare_runtime_settings,
)
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.store.db import Store

logger = logging.getLogger(__name__)

#: Infrastructure-only override for the runtime SQLite location. Used by the
#: Linux deployment (`/var/lib/mtc-bridge/bridge.db`) so the writable state
#: directory can live outside the read-only release tree. Unset everywhere
#: else, which keeps the in-repo default untouched.
STATE_DB_ENV_VAR = "MTC_BRIDGE_STATE_DB"


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
    config_path: str | Path | None = None,
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
    resolved_config_path = (
        Path(config_path)
        if config_path is not None
        else root / "config" / "bridge.yaml"
    )
    store = None
    validated_runtime_settings = None
    if store_path is not None or start_runtime:
        try:
            store = Store(store_path or root / "data" / "bridge.db")
            store.initialize()
        except StartupConfigRefusal:
            if store is not None:
                store.close()
            raise
        except Exception as exc:
            if store is not None:
                store.close()
            raise StartupConfigRefusal(
                [
                    ConfigIssue(
                        RefusalKind.STOP,
                        subject="schema_capabilities",
                        reason="store_initialize_failed",
                        action="repair_store_evaluation_and_retry",
                    )
                ]
            ) from exc
        if start_runtime:
            try:
                validated_runtime_settings = prepare_runtime_settings(
                    resolved_config_path, store, dry_run=dry_run
                )
            except StartupConfigRefusal:
                store.close()
                raise
        if store.get_meta("app_state") != "KILLED":
            store.set_meta("app_state", "DISARMED")
    init_runtime_state(app, store=store, validated=validated_runtime_settings)
    app.state.bridge_engine = None
    if start_runtime:
        if validated_runtime_settings is None or store is None:
            raise StartupConfigRefusal(
                [
                    ConfigIssue(
                        RefusalKind.STOP,
                        subject="config_binding",
                        reason="validated_settings_missing",
                        action="repair_startup_order_and_retry",
                    )
                ]
            )
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

        from bridge.engine.notify import build_notifier

        engine = construct_bridge_engine(
            validated_runtime_settings,
            run_id=run_id,
            broker=runtime_broker,
            store=store,
            strategy=KeltnerTrailEma8(),
            notifier=build_notifier(),
            state=store.get_meta("app_state") or "DISARMED",
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
    )
    uvicorn.run(runtime_app, host="127.0.0.1", port=8790, reload=False)
