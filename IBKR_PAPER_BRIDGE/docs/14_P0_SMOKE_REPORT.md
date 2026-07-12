# 14_P0_SMOKE_REPORT - F0/F1/F2 fixes and P0 retry

Date: 2026-07-12
Branch: `feature/ibkr-bridge-final`
Builder: Codex GPT-5

## Correction - 2026-07-12

The original post-run diagnosis below treated the `999.0` USDC returned by `spot_user_state` as
unavailable to Perps. That diagnosis was incorrect: a read-only
`query_user_abstraction_state` call returned `unifiedAccount`, where Hyperliquid intentionally
stores shared Spot/Perps balances and holds in `spot_user_state`. **No Spot-to-Perps transfer is
required, and Barış should not change account mode.**

Commit `944a5323` adds Unified-account detection and balance handling, safe string-response error
normalization, and explicit websocket shutdown. Both full suites now pass with
`70 passed, 1 warning` from each required CWD. The failed smoke was not rerun; its raw log remains
unchanged as historical evidence. The exact exchange rejection remains unknown because the old
parser masked it, so another order attempt still requires separate explicit approval.

## Original run verdict (collateral interpretation superseded)

**F0/F1/F2: PASS locally. P0: FAIL before any order was accepted.**

The testnet connection, account query, live candles, metadata, and bounded order plan completed.
The old adapter reported zero collateral from the legacy Perps summary, while a follow-up read-only
query found `999.0` mock USDC in the shared Unified balance. The atomic order call failed before
returning any oid or cloid. A separate read-only cleanup check found zero positions and zero open
orders. No retry was performed.

## F0/F1/F2 changes

- F0: `tools/smoke_p0.py:161` validates the API key as 32-byte hex and the account as a
  20-byte `0x` address before constructing SDK clients. It logs format labels only.
- F1: `bridge/broker/hyperliquid.py:330` uses installed SDK
  `Exchange.market_close(coin, sz=..., slippage=0.05, cloid=...)`. SDK-contract tests prove long
  positions generate crossing SELL reduce-only IOC orders, shorts generate crossing BUY orders,
  and zero positions submit nothing.
- F2: `bridge/broker/hyperliquid.py:306` rebuilds modify-stop fallback payloads through
  `_request(...)`; bookkeeping fields such as `role` cannot reach `bulk_orders`.
- Stored-spec sweep: reprotection stores bookkeeping metadata but sends its separately constructed
  clean request list. No other stored spec is passed directly to `order` or `bulk_orders`.

Commits:

- `a50cb4a9 fix(bridge): validate P0 credentials before connect`
- `7f4f7888 fix(bridge): use SDK market close for flatten`
- `92bc4f19 fix(bridge): sanitize stop replacement request`

New/updated tests: `tests/test_smoke_p0.py` and `tests/test_hyperliquid_broker.py`.

## Local test gates

From repository root:

```text
python -m pytest -q IBKR_PAPER_BRIDGE
67 passed, 1 warning in 4.15s
```

From `IBKR_PAPER_BRIDGE/`:

```text
python -m pytest -q
67 passed, 1 warning in 4.12s
```

The warning in both runs is the existing Starlette `httpx` deprecation warning.

## P0 smoke evidence

Command: `PYTHONUTF8=1 python IBKR_PAPER_BRIDGE/tools/smoke_p0.py`, with Windows user credentials
loaded into the child process without printing them and `HL_LIVE_ACK` explicitly unset.

Placed oids/cloids: **none**.
Cancelled oids/cloids: **none required**.
Post-failure read-only state: `positions=0`, `open_orders=0`, Perps account value `0.0`, Spot USDC
`999.0`.

Complete `p0_smoke_log.json`:

```json
{
  "approved_scope": "one tiny resting entry plus native SL, modify, cancel, flatten only if needed",
  "finished_ts": "2026-07-12T18:21:20.971248+00:00",
  "network": "testnet",
  "orders": [],
  "result": "FAIL",
  "run_id": "p0-20260712T182108Z",
  "started_ts": "2026-07-12T18:21:08.200569+00:00",
  "steps": [
    {
      "data": {
        "account_format": "valid_20_bytes",
        "key_format": "valid_32_bytes"
      },
      "name": "key_precheck",
      "status": "PASS",
      "ts": "2026-07-12T18:21:08.200596+00:00"
    },
    {
      "data": {
        "account_address": "0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49",
        "network": "testnet"
      },
      "name": "connect",
      "status": "PASS",
      "ts": "2026-07-12T18:21:17.642152+00:00"
    },
    {
      "data": {
        "available_margin": 0.0,
        "equity": 0.0,
        "withdrawable": 0.0
      },
      "name": "account",
      "status": "PASS",
      "ts": "2026-07-12T18:21:17.931519+00:00"
    },
    {
      "data": {
        "bars": [
          {
            "close": 64011.0,
            "high": 64093.0,
            "low": 63930.0,
            "open": 64023.0,
            "ts": "2026-07-12T16:00:00Z",
            "volume": 2.09213
          },
          {
            "close": 63919.0,
            "high": 64120.0,
            "low": 63863.0,
            "open": 63994.0,
            "ts": "2026-07-12T17:00:00Z",
            "volume": 6.64689
          },
          {
            "close": 63936.0,
            "high": 64021.0,
            "low": 63888.0,
            "open": 63932.0,
            "ts": "2026-07-12T18:00:00Z",
            "volume": 2.42695
          }
        ],
        "count": 3
      },
      "name": "candles",
      "status": "PASS",
      "ts": "2026-07-12T18:21:19.558316+00:00"
    },
    {
      "data": {
        "coin": "BTC",
        "entry_limit": 57542.4,
        "market_reference": 63936.0,
        "modified_stop_trigger": 56679.3,
        "notional_usd": 11.50848,
        "qty": 0.0002,
        "size_decimals": 5,
        "stop_trigger": 56391.6
      },
      "name": "meta_and_plan",
      "status": "PASS",
      "ts": "2026-07-12T18:21:20.340268+00:00"
    },
    {
      "data": {
        "error": "'str' object has no attribute 'get'",
        "error_type": "AttributeError"
      },
      "name": "failure",
      "status": "FAIL",
      "ts": "2026-07-12T18:21:20.660461+00:00"
    },
    {
      "data": {
        "flattened_symbols": []
      },
      "name": "partial_fill_guard",
      "status": "PASS",
      "ts": "2026-07-12T18:21:20.971235+00:00"
    },
    {
      "data": {
        "errors": []
      },
      "name": "best_effort_cleanup",
      "status": "PASS",
      "ts": "2026-07-12T18:21:20.971245+00:00"
    }
  ]
}
```

## Real-response surprises

1. The account uses `unifiedAccount`. In this mode, `user_state.marginSummary` is not the balance
   authority; shared USDC total/holds come from `spot_user_state`. The original Spot-only blocker
   diagnosis is superseded by the correction above.
2. The SDK/exchange failure response reached `_extract_statuses` with a string-shaped `response`,
   while the adapter assumes `response.data.statuses`. The adapter therefore surfaced
   `AttributeError` instead of the exchange rejection. The raw response was not persisted, so the
   exact rejection text is not claimed here.
3. The script wrote its final failure log after about 13 seconds, but SDK websocket worker state
   kept the Python process alive until the outer 120-second timeout. A clean disconnect lifecycle
   is still needed for a reliable standalone smoke command.

## Secret scan

No credential value was printed or persisted. The exact long-hex scan used before commit:

```powershell
rg -n -i "[0-9a-f]{64,}" IBKR_PAPER_BRIDGE/docs/p0_smoke_log.json IBKR_PAPER_BRIDGE/docs/14_P0_SMOKE_REPORT.md
```

Result: zero matches.

## Remaining gaps and next gate

- Unified-account balance handling is implemented and covered by tests; no user transfer or account
  mode change is required.
- `_extract_statuses` now preserves secret-redacted string exchange errors.
- The smoke now explicitly disconnects the SDK websocket before exit.
- Because this failure was not transient, a further P0 order attempt requires a new explicit
  approval. That attempt will reveal the previously masked exchange rejection if it recurs.
- P0 remains failed; P2 unattended ARM remains not approved.
