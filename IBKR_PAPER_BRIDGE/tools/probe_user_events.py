"""B3: read-only user-event payload probe (16_GO_LIVE_PLAN).

Connects to Hyperliquid TESTNET, subscribes to userEvents + orderUpdates,
listens for a bounded window, and writes every received message's redacted
raw shape to docs/user_events_probe.json. Places NO orders. Also runs during
the B6 fill smoke so real fill payloads land here.
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bridge.broker.hyperliquid import HyperliquidBroker
from bridge.settings import resolve_hyperliquid_credentials

LOG_PATH = ROOT / "docs" / "user_events_probe.json"
LISTEN_SECONDS = 90


async def main() -> None:
    account, key, source = resolve_hyperliquid_credentials()
    broker = HyperliquidBroker(network="testnet", account_address=account, api_wallet_key=key)
    await broker.connect()

    captured: list[dict] = []

    def raw_capture(message: object) -> None:
        captured.append(
            {
                "received_ts": datetime.now(UTC).isoformat(),
                "raw_redacted": HyperliquidBroker._raw_response_safe(message),
            }
        )

    # Subscribe with the raw capture callback via the SDK directly so we see
    # the exact wire shapes, not our parsed types.
    broker.info.subscribe({"type": "userEvents", "user": broker.account_address}, raw_capture)
    broker.info.subscribe({"type": "orderUpdates", "user": broker.account_address}, raw_capture)

    deadline = time.monotonic() + LISTEN_SECONDS
    while time.monotonic() < deadline:
        await asyncio.sleep(1)

    result = {
        "probe": "user_events",
        "network": "testnet",
        "credential_source": source,
        "listened_seconds": LISTEN_SECONDS,
        "message_count": len(captured),
        "finished_ts": datetime.now(UTC).isoformat(),
        "messages": captured,
    }
    LOG_PATH.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    await broker.disconnect()
    print(json.dumps({"messages": len(captured), "log": str(LOG_PATH)}))


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
