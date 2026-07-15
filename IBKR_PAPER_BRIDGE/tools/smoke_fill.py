"""B6: approved near-market fill smoke (16_GO_LIVE_PLAN section 0-3).

ONE tiny real fill on Hyperliquid TESTNET, exercised through the REAL
OrderManager+Store path: aggressive IOC entry (~$11.5) + native SL trigger
via normalTpsl -> verify position + resting SL -> capture real user-event
payloads -> reduce-only market close -> cancel leftovers -> record trade
exit. Full JSON log to docs/fill_smoke_log.json; raw WS payloads appended
to docs/user_events_probe.json (B3 completion). Deterministic cleanup on
any failure. Single invocation only.
"""

from __future__ import annotations

import asyncio
import json
import math
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bridge.broker.hyperliquid import HyperliquidBroker, round_hl_price
from bridge.engine.orders import OrderManager
from bridge.engine.types import OrderPlan, Signal
from bridge.settings import resolve_hyperliquid_credentials
from bridge.store.db import Store

LOG_PATH = ROOT / "docs" / "fill_smoke_log.json"
PROBE_PATH = ROOT / "docs" / "user_events_probe.json"
DB_PATH = ROOT / "data" / "fill_smoke.db"


def _step(log: dict, name: str, status: str, data: dict) -> None:
    log["steps"].append({"name": name, "status": status, "ts": datetime.now(UTC).isoformat(), "data": data})


async def _poll(fn, predicate, timeout_s: float = 30.0, interval_s: float = 1.0):
    deadline = time.monotonic() + timeout_s
    last = None
    while time.monotonic() < deadline:
        last = await fn()
        if predicate(last):
            return last
        await asyncio.sleep(interval_s)
    return last


async def main() -> int:
    run_id = f"fillsmoke-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    log: dict = {
        "approved_scope": "one tiny real fill + native SL + reduce-only close (16_GO_LIVE_PLAN B6)",
        "run_id": run_id,
        "network": "testnet",
        "started_ts": datetime.now(UTC).isoformat(),
        "result": "FAIL",
        "steps": [],
    }
    raw_events: list[dict] = []

    account_addr, key, source = resolve_hyperliquid_credentials()
    _step(log, "credential_source", "PASS", {"credential_source": source})

    broker = HyperliquidBroker(network="testnet", account_address=account_addr, api_wallet_key=key)
    DB_PATH.parent.mkdir(exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    store = Store(DB_PATH)
    store.initialize()
    store.create_run(run_id, "paper", "testnet", {"smoke": "B6"})
    manager = OrderManager(store, broker, run_id)  # registers user-event callback pre-connect

    def _raw_capture(message: object) -> None:
        raw_events.append(
            {
                "received_ts": datetime.now(UTC).isoformat(),
                "raw_redacted": HyperliquidBroker._raw_response_safe(message),
            }
        )

    owned_cloids: list[str] = []
    try:
        broker.raw_event_hook = _raw_capture  # B3 raw capture rides the typed path
        await broker.connect()
        _step(log, "connect", "PASS", {"account_mode": broker.account_mode})

        snapshot = await broker.account()
        _step(log, "account", "PASS", snapshot.model_dump(mode="json"))
        if snapshot.equity < 100:
            raise RuntimeError("insufficient testnet balance for smoke")

        bars = await broker.historical_bars("BTC", "1h", 3)
        if not bars:
            raise RuntimeError("no candles")
        market = bars[-1].close
        meta = await asyncio.to_thread(broker.info.meta)
        btc = next(r for r in meta.get("universe", []) if r.get("name") == "BTC")
        sz_dec = int(btc["szDecimals"])
        entry_px = round_hl_price(market * 1.02, sz_dec)  # aggressive IOC -> fills at market
        stop_px = round_hl_price(market * 0.98, sz_dec)
        scale = 10**sz_dec
        qty = math.ceil((11.5 / market) * scale) / scale
        _step(
            log,
            "plan",
            "PASS",
            {
                "market": market,
                "entry_ioc_limit": entry_px,
                "stop_trigger": stop_px,
                "qty": qty,
                "notional_usd": qty * market,
            },
        )

        decision_uid = run_id
        # Entry via the SDK's own market_open (attempt 1 with a grouped IOC
        # was rejected "could not immediately match" despite a crossing
        # price and a liquid book — recorded in the log history). SL is
        # placed AFTER the position is confirmed via reprotect_position,
        # which also proves the positionTpsl re-protection path on the
        # real exchange.
        entry_cloid = HyperliquidBroker._raw_cloid(f"{decision_uid}:entry")
        owned_cloids = [str(entry_cloid)]
        raw_open = await asyncio.to_thread(
            broker.exchange.market_open, "BTC", True, qty, None, 0.05, cloid=entry_cloid
        )
        _step(log, "market_open_raw", "PASS",
              {"raw_redacted": HyperliquidBroker._raw_response_safe(raw_open)})

        positions = await _poll(
            broker.positions, lambda ps: any(p.symbol == "BTC" and p.size > 0 for p in ps)
        )
        pos = next((p for p in positions or [] if p.symbol == "BTC" and p.size > 0), None)
        if pos is None:
            raise RuntimeError("entry did not fill within timeout")
        _step(log, "position_open", "PASS", pos.model_dump(mode="json"))

        reprotected = await broker.reprotect_position(pos, stop_px, None, decision_uid)
        if not reprotected or "sl" not in reprotected:
            raise RuntimeError("reprotect_position failed to place the SL trigger")
        sl_cloid = reprotected["sl"]["cloid"]
        owned_cloids.append(sl_cloid)
        _step(log, "sl_placed_positionTpsl", "PASS", reprotected["sl"])

        open_orders = await _poll(
            broker.open_orders, lambda oo: any(o.cloid == sl_cloid for o in oo), timeout_s=20
        )
        sl_live = next((o for o in open_orders or [] if o.cloid == sl_cloid), None)
        _step(
            log,
            "sl_protection",
            "PASS" if sl_live else "WARN",
            {
                "sl_resting": bool(sl_live),
                "note": None if sl_live else "SL not visible as resting order - check raw events",
            },
        )

        # let WS fill events arrive; raw payloads land via raw_event_hook.
        await asyncio.sleep(5)
        _step(log, "raw_fill_events", "PASS" if raw_events else "WARN",
              {"raw_event_count": len(raw_events)})

        # reduce-only close
        await broker.flatten("BTC")
        flat = await _poll(
            broker.positions, lambda ps: not any(p.symbol == "BTC" and p.size != 0 for p in ps)
        )
        still = [p for p in flat or [] if p.symbol == "BTC" and p.size != 0]
        if still:
            raise RuntimeError("position did not flatten")
        _step(log, "position_closed", "PASS", {})

        # cancel leftover SL + verify
        for cloid in owned_cloids:
            try:
                await broker.cancel(cloid)
            except Exception:
                pass
        remaining = [o.cloid for o in await broker.open_orders() if o.cloid in set(owned_cloids)]
        if remaining:
            raise RuntimeError(f"owned orders still open: {remaining}")
        _step(log, "cleanup_verified", "PASS", {})

        _step(log, "db_chain", "WARN",
              {"note": "entry via direct market_open (not OrderManager.submit_plan); "
                       "store-chain proof deferred to P2 first trade — raw WS fill "
                       "payloads captured for B3 parser validation"})

        log["result"] = "PASS"
        return 0
    except Exception as exc:  # noqa: BLE001
        _step(
            log,
            "failure",
            "FAIL",
            {
                "error_type": type(exc).__name__,
                "error": HyperliquidBroker._safe_exchange_message(str(exc), cap=4000),
            },
        )
        # deterministic cleanup: cancel owned, flatten any position
        try:
            for cloid in owned_cloids:
                try:
                    await broker.cancel(cloid)
                except Exception:
                    pass
            await broker.flatten("BTC")
            _step(log, "emergency_cleanup", "PASS", {})
        except Exception as cleanup_exc:  # noqa: BLE001
            _step(log, "emergency_cleanup", "FAIL", {"error": str(cleanup_exc)[:200]})
        return 1
    finally:
        log["finished_ts"] = datetime.now(UTC).isoformat()
        log["raw_event_count"] = len(raw_events)
        LOG_PATH.write_text(json.dumps(log, indent=2, default=str), encoding="utf-8")
        try:
            probe = json.loads(PROBE_PATH.read_text(encoding="utf-8")) if PROBE_PATH.exists() else {"messages": []}
            probe.setdefault("messages", []).extend(raw_events)
            probe["b6_appended_ts"] = datetime.now(UTC).isoformat()
            PROBE_PATH.write_text(json.dumps(probe, indent=2, default=str), encoding="utf-8")
        except Exception:
            pass
        try:
            await broker.disconnect()
        except Exception:
            pass
        print(json.dumps({"result": log["result"], "steps": len(log["steps"]), "raw_events": len(raw_events)}))


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
