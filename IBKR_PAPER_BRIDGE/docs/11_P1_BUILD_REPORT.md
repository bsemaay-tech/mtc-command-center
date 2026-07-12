# P1 Build Report - 2026-07-12

## Executive result

**P1 local gate: PASS. P0: BLOCKED before connection. Real golden: BLOCKED. P2: not started.**

The bridge is now a continuous, broker-typed, Store-backed MockBroker runtime with live REST/WS
dashboard updates and all eight P1 failure drills. The approved P0 run reached SDK key validation
only; the configured API-wallet value decodes to 20 bytes instead of 32, so no Hyperliquid network
connection or order action occurred. The golden remains provisional because the canonical
QuantLens engine has no exact `keltner_trail_ema8` strategy ID.

## 1. Per-task status

| Task | Status | Evidence |
|---|---|---|
| T1 | DONE (local proof) | `bridge/broker/hyperliquid.py`; `tests/test_hyperliquid_broker.py` |
| T2 | DONE | Typed parity assertions in `test_broker_normalization_type_parity` |
| T3 | DONE | `test_async_sdk_calls_are_offloaded_from_event_loop_thread` |
| T4 | PARTIAL | `bridge/engine/bars.py`; timer/dedupe/stale/reconnect tests pass; automatic real SDK drop detection not wired |
| T5 | PARTIAL | Typed event ingestion/reconcile implemented; order_ref/attribute fallback matching remains |
| T6 | DONE for P1 | `BridgeEngine.start/arm/disarm_runtime/kill/on_bar` plus continuous mock test |
| T7 | DONE for P1 | Runtime endpoints, persistent WS, snapshot resync, decision stream |
| T8 | DONE | `tests/test_p1_failure_drills.py` plus owned/foreign reconcile tests |
| T9 | DONE | Identical 54-test pass from both required CWDs |
| T10 | DONE | Local SVG renderer; `docs/screenshots/overview.png`, `trading.png` |
| T11 | BLOCKED | `docs/p0_smoke_log.json`; invalid key length before connection; no orders |
| T12 | BLOCKED | `docs/12_GOLDEN_REGEN_ATTEMPT.md`; exact strategy is absent from engine registry |
| T13 | DONE | This report, `03_STATUS.md`, and canonical handoff |

## 2. Commands and full pytest summaries

Repo-root command:

```powershell
$env:PYTHONUTF8='1'; python -m pytest IBKR_PAPER_BRIDGE\tests -q
```

Full summary:

```text
......................................................                   [100%]
============================== warnings summary ===============================
..\..\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1
  C:\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
54 passed, 1 warning in 3.25s
```

Bridge-directory command:

```powershell
$env:PYTHONUTF8='1'; python -m pytest tests -q
```

Full summary:

```text
......................................................                   [100%]
============================== warnings summary ===============================
..\..\..\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1
  C:\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
54 passed, 1 warning in 3.33s
```

Other verification:

```powershell
node --check IBKR_PAPER_BRIDGE\bridge\static\app.js
python -m py_compile IBKR_PAPER_BRIDGE\tools\smoke_p0.py
```

Both exited 0. Live browser evidence showed `DRY_RUN`, `ARMED`, equity `$100000.00`, 80 SVG candle
bodies, 10 decision rows, and zero CDN scripts.

## 3. P0 smoke log and order identities

No oid or cloid exists because SDK private-key validation failed before client construction and
before any network connection.

```json
{
  "approved_scope": "one tiny resting entry plus native SL, modify, cancel, flatten only if needed",
  "finished_ts": "2026-07-12T17:47:41.471821+00:00",
  "network": "testnet",
  "orders": [],
  "result": "FAIL",
  "run_id": "p0-20260712T174741Z",
  "started_ts": "2026-07-12T17:47:41.190117+00:00",
  "steps": [
    {
      "data": {
        "error": "The private key must be exactly 32 bytes long, instead of 20 bytes.",
        "error_type": "ValueError"
      },
      "name": "failure",
      "status": "FAIL",
      "ts": "2026-07-12T17:47:41.471803+00:00"
    },
    {
      "data": {"errors": ["flatten:HyperliquidNotConfigured"]},
      "name": "best_effort_cleanup",
      "status": "WARN",
      "ts": "2026-07-12T17:47:41.471819+00:00"
    }
  ]
}
```

## 4. SDK contract proof

Installed package: `hyperliquid-python-sdk 0.24.0`.

```text
Exchange.bulk_orders(self, order_requests: List[OrderRequest], builder: BuilderInfo | None = None, grouping: 'na' | 'normalTpsl' | 'positionTpsl' | PriorityGrouping = 'na') -> Any
Exchange.modify_order(self, oid: int | Cloid, name: str, is_buy: bool, sz: float, limit_px: float, order_type: OrderType, reduce_only: bool = False, cloid: Cloid | None = None) -> Any
Exchange.cancel_by_cloid(self, name: str, cloid: Cloid) -> Any
```

Call sites in `bridge/broker/hyperliquid.py`:

- Atomic bracket: line 226, `bulk_orders(requests, grouping="positionTpsl")`.
- Full stop modify: lines 263-272, typed cloid + coin + side + size + price + trigger + reduce-only.
- Modify fallback cancel/re-place: lines 276-280.
- Normal cancel: line 288, `cancel_by_cloid(coin, Cloid)`.
- Re-protection group: line 346, `bulk_orders(..., grouping="positionTpsl")`.

The fake exchange is created with `unittest.mock.create_autospec(Exchange, instance=True)`, so an
incorrect method signature fails locally.

## 5. Golden regeneration

Data physically validated:

- Bundle: `native_multiasset_alpaca_2026-06-28`
- Manifest dataset: `BTCUSD`, `1h`, validation `PASS`
- 48,077 bars, `2021-01-01 06:00:00+00:00` through `2026-06-28 00:00:00+00:00`

Exact command (output redirected outside MCC):

```powershell
$env:MEGA_EXIT_MODES='trail_ema8'
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --strategy keltner_trail_ema8 --symbol BTCUSD --tf 1h
```

Result:

```text
Unknown strategy id(s): ['keltner_trail_ema8']
```

Signal count and `golden_run_id` therefore remain the provisional values: 1 synthetic-reference
signal and `PROVISIONAL_SYNTHETIC_REFERENCE_2026-07-06`. `GEN_KELTNER_BREAKOUT` was not substituted
because its rules are not parity-equivalent. Full evidence: `docs/12_GOLDEN_REGEN_ATTEMPT.md`.

## 6. Honest remaining gaps

1. Correct the Windows user `HL_API_WALLET_KEY` to the 32-byte agent-wallet private key, restart
   Codex, and obtain a separate P0 retry approval.
2. Real testnet behavior for atomic grouping, trigger modification, open-order normalization, and
   user-event payload parsing remains unverified because P0 did not connect.
3. Automatic detection of an SDK WebSocket drop is not wired to `BarFeed.reconnect`; the tested
   reconnect/resubscribe path currently needs an explicit disconnect signal.
4. Reconciler matching uses cloid. The specified `order_ref` then conservative-attribute fallbacks
   are not implemented.
5. Real golden parity remains blocked until the exact bridge strategy is registered/exportable in
   QuantLens.
6. P2 is neither approved nor started. This report is not promotion evidence and not live-trading
   approval.

## 7. Build commits

```text
cd306691 fix(bridge): align hyperliquid sdk contract
b2291e49 fix(bridge): normalize broker snapshots
b5c849d9 fix(bridge): offload synchronous sdk calls
0de985b9 feat(bridge): implement candle feed supervision
b5c1ed1f feat(bridge): ingest broker user events
05eda571 feat(bridge): run continuous safe engine
dd2d05d4 feat(bridge): wire runtime api and websocket
01692467 test(bridge): prove p1 failure recovery
be729574 test(bridge): make suite cwd independent
c1af202b fix(bridge): use local live candle chart
0084564c feat(bridge): complete bounded p0 smoke
2cf44b65 docs(bridge): record golden run blocker
ca5efda0 fix(bridge): scope bar dedupe to runtime
4f6a3bad fix(bridge): render live decision stream
95e732d6 docs(bridge): report p1 acceptance evidence
```

Commit `95e732d6` is the T13 status/report/handoff commit. A later metadata-only commit may contain
this self-reference line.
