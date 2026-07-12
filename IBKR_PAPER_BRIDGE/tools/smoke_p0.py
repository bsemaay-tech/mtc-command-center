"""Approved P0 Hyperliquid testnet smoke with bounded order scope and cleanup."""

from __future__ import annotations

import asyncio
import json
import math
import os
import string
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bridge.broker.hyperliquid import HyperliquidBroker, round_hl_price
from bridge.engine.types import OrderPlan, Signal

LOG_PATH = ROOT / "docs" / "p0_smoke_log.json"


async def main() -> None:
    log: dict = {
        "run_id": f"p0-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}",
        "network": "testnet",
        "approved_scope": "one tiny resting entry plus native SL, modify, cancel, flatten only if needed",
        "started_ts": datetime.now(UTC).isoformat(),
        "steps": [],
        "orders": [],
        "result": "RUNNING",
    }
    broker: HyperliquidBroker | None = None
    owned_cloids: list[str] = []
    initial_sizes: dict[str, float] = {}
    try:
        _validate_credentials()
        _step(
            log,
            "key_precheck",
            "PASS",
            {"key_format": "valid_32_bytes", "account_format": "valid_20_bytes"},
        )
        broker = HyperliquidBroker(network="testnet", coin="BTC", leverage=1)
        await broker.connect()
        _step(
            log,
            "connect",
            "PASS",
            {
                "network": broker.network,
                "account_address": broker.account_address,
                "account_mode": broker.account_mode,
            },
        )

        account = await broker.account()
        _step(log, "account", "PASS", account.model_dump(mode="json"))
        initial_sizes = {position.symbol: position.size for position in await broker.positions()}

        bars = await broker.historical_bars("BTC", "1h", 3)
        if len(bars) != 3:
            raise RuntimeError(f"expected 3 candles, received {len(bars)}")
        _step(log, "candles", "PASS", {"count": len(bars), "bars": [bar.model_dump(mode="json") for bar in bars]})

        meta = await asyncio.to_thread(broker.info.meta)
        universe = meta.get("universe", []) if isinstance(meta, dict) else []
        btc_meta = next((row for row in universe if row.get("name") == "BTC"), None)
        if btc_meta is None:
            raise RuntimeError("BTC metadata not found")
        size_decimals = int(btc_meta["szDecimals"])
        market = bars[-1].close
        entry_px = round_hl_price(market * 0.90, size_decimals)
        stop_px = round_hl_price(entry_px * 0.98, size_decimals)
        modified_stop = round_hl_price(entry_px * 0.985, size_decimals)
        scale = 10**size_decimals
        qty = math.ceil((11.5 / entry_px) * scale) / scale
        notional = qty * entry_px
        _step(
            log,
            "meta_and_plan",
            "PASS",
            {
                "coin": "BTC",
                "size_decimals": size_decimals,
                "market_reference": market,
                "entry_limit": entry_px,
                "stop_trigger": stop_px,
                "modified_stop_trigger": modified_stop,
                "qty": qty,
                "notional_usd": notional,
            },
        )

        signal = Signal(
            ts=datetime.now(UTC),
            symbol="BTC",
            direction="LONG",
            reason="approved P0 resting-order smoke",
            ref_price=market,
            stop_loss=stop_px,
        )
        plan = OrderPlan(
            decision_uid=log["run_id"],
            signal=signal,
            qty=qty,
            entry_type="LMT",
            limit_price=entry_px,
            stop_loss=stop_px,
            leverage=1,
        )
        placed = await broker.place_bracket(plan)
        owned_cloids = [row["cloid"] for row in placed.values()]
        log["orders"] = [
            {"role": row["role"], "cloid": row["cloid"], "oid": row.get("oid"), "qty": row["qty"]}
            for row in placed.values()
        ]
        _step(log, "place_atomic_position_tpsl", "PASS", {"orders": log["orders"]})

        visible = await broker.open_orders()
        visible_cloids = {order.cloid for order in visible}
        missing = sorted(set(owned_cloids) - visible_cloids)
        if missing:
            raise RuntimeError(f"placed cloids not visible: {missing}")
        _step(log, "verify_open_orders", "PASS", {"owned_cloids_visible": sorted(owned_cloids)})

        await broker.modify_stop(placed["sl"]["cloid"], modified_stop)
        _step(log, "modify_stop", "PASS", {"cloid": placed["sl"]["cloid"], "new_trigger_px": modified_stop})

        for cloid in owned_cloids:
            await broker.cancel(cloid)
        _step(log, "cancel_owned_orders", "PASS", {"cancelled_cloids": sorted(owned_cloids)})

        remaining = {order.cloid for order in await broker.open_orders()}
        uncleared = sorted(set(owned_cloids) & remaining)
        if uncleared:
            raise RuntimeError(f"owned cloids still open after cancel: {uncleared}")
        _step(log, "verify_cleanup", "PASS", {"owned_open_orders_remaining": []})

        await _flatten_if_changed(broker, initial_sizes, log)
        log["result"] = "PASS"
    except Exception as exc:
        log["result"] = "FAIL"
        _step(log, "failure", "FAIL", {"error_type": type(exc).__name__, "error": str(exc)})
        if broker is not None:
            await _best_effort_cleanup(broker, owned_cloids, initial_sizes, log)
        raise
    finally:
        if broker is not None:
            try:
                await broker.disconnect()
                _step(log, "disconnect", "PASS", {})
            except Exception as exc:
                _step(log, "disconnect", "WARN", {"error_type": type(exc).__name__})
        log["finished_ts"] = datetime.now(UTC).isoformat()
        LOG_PATH.write_text(json.dumps(log, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps({"result": log["result"], "log": str(LOG_PATH), "steps": len(log["steps"])}))


def _validate_credentials() -> None:
    key = os.environ.get("HL_API_WALLET_KEY", "").strip()
    key_hex = key[2:] if key.startswith("0x") else key
    if len(key_hex) != 64 or any(char not in string.hexdigits for char in key_hex):
        raise RuntimeError("HL_API_WALLET_KEY must be a 32-byte hexadecimal private key")

    account = os.environ.get("HL_ACCOUNT_ADDRESS", "").strip()
    account_hex = account[2:] if account.startswith("0x") else ""
    if len(account_hex) != 40 or any(char not in string.hexdigits for char in account_hex):
        raise RuntimeError("HL_ACCOUNT_ADDRESS must be a 20-byte 0x-prefixed hexadecimal address")


async def _flatten_if_changed(broker: HyperliquidBroker, initial_sizes: dict[str, float], log: dict) -> None:
    positions = await broker.positions()
    changed = [position for position in positions if position.size != initial_sizes.get(position.symbol, 0.0)]
    for position in changed:
        await broker.flatten(position.symbol)
    _step(
        log,
        "partial_fill_guard",
        "PASS",
        {"flattened_symbols": [position.symbol for position in changed]},
    )


async def _best_effort_cleanup(
    broker: HyperliquidBroker,
    owned_cloids: list[str],
    initial_sizes: dict[str, float],
    log: dict,
) -> None:
    cleanup_errors: list[str] = []
    for cloid in owned_cloids:
        try:
            await broker.cancel(cloid)
        except Exception as exc:
            cleanup_errors.append(f"cancel:{type(exc).__name__}")
    try:
        await _flatten_if_changed(broker, initial_sizes, log)
    except Exception as exc:
        cleanup_errors.append(f"flatten:{type(exc).__name__}")
    _step(log, "best_effort_cleanup", "PASS" if not cleanup_errors else "WARN", {"errors": cleanup_errors})


def _step(log: dict, name: str, status: str, data: dict) -> None:
    log["steps"].append(
        {"name": name, "status": status, "ts": datetime.now(UTC).isoformat(), "data": data}
    )


if __name__ == "__main__":
    asyncio.run(main())
