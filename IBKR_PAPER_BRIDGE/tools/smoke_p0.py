"""Approval-gated Hyperliquid P0 smoke.

Do not run this script unless Baris explicitly approves in-session. It connects
to Hyperliquid testnet and is intended to place and cancel a tiny bracket.
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime

from bridge.broker.hyperliquid import HyperliquidBroker


async def main() -> None:
    broker = HyperliquidBroker(network="testnet")
    await broker.connect()
    account = await broker.account()
    result = {
        "ts": datetime.now(UTC).isoformat(),
        "network": "testnet",
        "account_seen": bool(account),
        "note": "Order placement step intentionally requires human approval before this script is run.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
