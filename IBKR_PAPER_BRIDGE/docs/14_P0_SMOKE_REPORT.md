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

## Authorized rounded-price attempt - 2026-07-12

Barış approved exactly one additional bounded P0 attempt after a Hyperliquid price-precision fix.
Commit `42018032` added `round_hl_price()` and applied it at the smoke plan plus adapter entry,
SL/TP, modify-stop, and reprotection submission boundaries. Required fixtures pass:
`57542.4 -> 57540.0`, sub-unit precision respects `6 - szDecimals`, and valid prices remain
unchanged. Both full suites passed before network access: `72 passed, 1 warning` from each CWD.

The single attempt `p0-20260712T185408Z` **FAILED** after atomic submission because the real
`positionTpsl` response contained fewer status objects than the adapter's one-status-per-request
assumption. Earlier stages passed: `unifiedAccount`, equity/available/withdrawable `999.0`, three
live BTC candles, and rounded prices `entry=57600`, `SL=56448`, `modified SL=56736` for
`0.0002 BTC` (~`$11.52`). Clean websocket disconnect passed.

No oid was returned to the script. Deterministic cloids for the run were:

- entry: `0x8f2bdc2a2d4dd7e14f2a1df9d7b6c7ee`
- SL: `0x5bf0e44907d2e1fd1f7843d05be2347d`
- TP (not submitted by this plan): `0x23f6088a36b8838cd90b984c0a477e04`

A separate read-only post-failure query found `open_orders=0`, no owned cloid, and zero positions;
therefore no cancellation or flatten action was required. No second attempt was run.

Complete overwritten `p0_smoke_log.json` for this attempt:

```json
{
  "approved_scope": "one tiny resting entry plus native SL, modify, cancel, flatten only if needed",
  "finished_ts": "2026-07-12T18:54:23.898448+00:00",
  "network": "testnet",
  "orders": [],
  "result": "FAIL",
  "run_id": "p0-20260712T185408Z",
  "started_ts": "2026-07-12T18:54:08.310060+00:00",
  "steps": [
    {
      "data": {
        "account_format": "valid_20_bytes",
        "key_format": "valid_32_bytes"
      },
      "name": "key_precheck",
      "status": "PASS",
      "ts": "2026-07-12T18:54:08.310084+00:00"
    },
    {
      "data": {
        "account_address": "0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49",
        "account_mode": "unifiedAccount",
        "network": "testnet"
      },
      "name": "connect",
      "status": "PASS",
      "ts": "2026-07-12T18:54:19.447185+00:00"
    },
    {
      "data": {
        "available_margin": 999.0,
        "equity": 999.0,
        "withdrawable": 999.0
      },
      "name": "account",
      "status": "PASS",
      "ts": "2026-07-12T18:54:20.139904+00:00"
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
            "close": 64000.0,
            "high": 64029.0,
            "low": 63888.0,
            "open": 63932.0,
            "ts": "2026-07-12T18:00:00Z",
            "volume": 3.5548
          }
        ],
        "count": 3
      },
      "name": "candles",
      "status": "PASS",
      "ts": "2026-07-12T18:54:20.829684+00:00"
    },
    {
      "data": {
        "coin": "BTC",
        "entry_limit": 57600.0,
        "market_reference": 64000.0,
        "modified_stop_trigger": 56736.0,
        "notional_usd": 11.520000000000001,
        "qty": 0.0002,
        "size_decimals": 5,
        "stop_trigger": 56448.0
      },
      "name": "meta_and_plan",
      "status": "PASS",
      "ts": "2026-07-12T18:54:21.628216+00:00"
    },
    {
      "data": {
        "error": "bulk order response did not contain every status",
        "error_type": "HyperliquidOrderError"
      },
      "name": "failure",
      "status": "FAIL",
      "ts": "2026-07-12T18:54:22.632403+00:00"
    },
    {
      "data": {
        "flattened_symbols": []
      },
      "name": "partial_fill_guard",
      "status": "PASS",
      "ts": "2026-07-12T18:54:23.165621+00:00"
    },
    {
      "data": {
        "errors": []
      },
      "name": "best_effort_cleanup",
      "status": "PASS",
      "ts": "2026-07-12T18:54:23.165631+00:00"
    },
    {
      "data": {},
      "name": "disconnect",
      "status": "PASS",
      "ts": "2026-07-12T18:54:23.898439+00:00"
    }
  ]
}
```

Current blocker: capture and normalize the real `positionTpsl` status cardinality/representation
without assuming one status dict per submitted request, while retaining deterministic owned-cloid
cleanup even when placement result parsing fails. This requires local fixtures/tests first and a
new explicit approval before any further testnet order attempt. P2 remains unapproved.

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

## Approved P0 attempt 4 — 2026-07-12

Commit `09a7a92f` completed the approved local C1-C3 hardening before the one authorized smoke invocation.

- **C1 — cardinality:** `bridge/broker/hyperliquid.py:288` no longer requires one status per submitted request. It maps the returned statuses as hints, then uses `open_orders()` as the authority; each submitted cloid must be visible or be specifically explained as filled. `reprotect_position()` uses the same verifier. Tests cover 1, 2, and 3 statuses for a three-order group, error statuses, filled explanation, and missing trigger failure (`tests/test_hyperliquid_broker.py:487`).
- **C2 — diagnostics:** `bridge/broker/hyperliquid.py:565` attaches the complete JSON-safe, 64+-hex-redacted raw response to parse/verification errors, capped at 4000 characters; `tools/smoke_p0.py:244` carries that diagnostic into the smoke log; `bridge/engine/orders.py:43` persists submission failure context to an events row. Tests cover redaction, parser shapes, and smoke-log failure data.
- **C3 — cleanup:** `tools/smoke_p0.py:204` deterministically derives only the submitted entry/SL cloids, queries open orders, cancels owned resting orders, verifies they are absent, and flattens only an unexpected changed position. The cleanup test is `tests/test_smoke_p0.py:58`.

Full local pytest summaries, run before the network attempt:

Repository root:

```text
........................................................................ [ 80%]
.................                                                        [100%]
89 passed, 1 warning in 3.69s
```

`IBKR_PAPER_BRIDGE/`:

```text
........................................................................ [ 80%]
.................                                                        [100%]
89 passed, 1 warning in 3.55s
```

The one authorized command was run once from the repository root with `HL_LIVE_ACK` cleared for that process:

```powershell
$env:PYTHONUTF8='1'; Remove-Item Env:HL_LIVE_ACK -ErrorAction SilentlyContinue; python IBKR_PAPER_BRIDGE\tools\smoke_p0.py
```

It failed at the local key-format precheck before SDK construction. Therefore **no testnet connection, account query, candle query, exchange response, order, cancellation, or flatten action occurred**. No retry was run. There is no real `positionTpsl` response shape to amend in `01_ARCHITECTURE.md`; the C1 correction remains the local response-shape hardening pending a newly approved future attempt.

Complete overwritten `p0_smoke_log.json` for this attempt:

```json
{
  "approved_scope": "one tiny resting entry plus native SL, modify, cancel, flatten only if needed",
  "finished_ts": "2026-07-12T19:28:48.427179+00:00",
  "network": "testnet",
  "orders": [],
  "result": "FAIL",
  "run_id": "p0-20260712T192848Z",
  "started_ts": "2026-07-12T19:28:48.427061+00:00",
  "steps": [
    {
      "data": {
        "error": "HL_API_WALLET_KEY must be a 32-byte hexadecimal private key",
        "error_type": "RuntimeError"
      },
      "name": "failure",
      "status": "FAIL",
      "ts": "2026-07-12T19:28:48.427175+00:00"
    }
  ]
}
```

Placed/cancelled oids and cloids: none. Secret scan command and result:

```powershell
$targets = @('IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py','IBKR_PAPER_BRIDGE/bridge/engine/orders.py','IBKR_PAPER_BRIDGE/tools/smoke_p0.py','IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py','IBKR_PAPER_BRIDGE/tests/test_smoke_p0.py','IBKR_PAPER_BRIDGE/docs/p0_smoke_log.json','IBKR_PAPER_BRIDGE/docs/14_P0_SMOKE_REPORT.md','IBKR_PAPER_BRIDGE/docs/03_STATUS.md'); @(rg -l -i '[0-9a-f]{64,}' @targets 2>$null).Count
```

Result: `0`.

Remaining gap: the Windows environment inherited by this run did not contain a valid 32-byte API-wallet key. Correct the local credential, then obtain a **new explicit P0 approval** before any future smoke invocation. P0 exit criteria are not met; P2 remains unapproved.

## Re-approved P0 attempt 5 — E1 user-registry fallback — 2026-07-12

Commit `25cee696` implements approved local fix E1. `bridge/settings.py` resolves a valid complete
credential pair from the process environment first, otherwise from `HKCU\Environment`, with the
same format checks and no credential disclosure. `tools/smoke_p0.py` records only
`credential_source` and passes the resolved pair directly to `HyperliquidBroker`. New monkeypatched
registry tests cover absent process values, invalid process values with valid registry values, and
invalid values in both sources. Both full suites passed before the attempt:

```text
Repo root: 92 passed, 1 warning in 4.69s
IBKR_PAPER_BRIDGE/: 92 passed, 1 warning in 4.91s
```

The resolver selected `user_registry` (source label only; no credential value was output). The one
re-approved testnet run was executed once with `HL_LIVE_ACK` removed from that process. It connected
to testnet, read the Unified account and live BTC candles, then failed at the atomic group call.
The real response captured by C2 is:

```json
{"status":"ok","response":{"type":"order","data":{"statuses":[{"error":"Trigger order has unexpected type."}]}}}
```

No exchange order was accepted, so there were no placed or cancelled oids. The deterministic entry
cloid reported in the failure was `0x95f589787908b598642cba45f8562333`; C3 queried owned orders,
found none, observed no changed position, and completed cleanup with `errors: []`. No retry was run.

Complete overwritten `p0_smoke_log.json` for attempt 5:

```json
{
  "approved_scope": "one tiny resting entry plus native SL, modify, cancel, flatten only if needed",
  "finished_ts": "2026-07-12T19:46:42.075264+00:00",
  "network": "testnet",
  "orders": [],
  "result": "FAIL",
  "run_id": "p0-20260712T194622Z",
  "started_ts": "2026-07-12T19:46:22.827525+00:00",
  "steps": [
    {"data":{"credential_source":"user_registry"},"name":"credential_source","status":"PASS","ts":"2026-07-12T19:46:22.827612+00:00"},
    {"data":{"account_address":"0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49","account_mode":"unifiedAccount","network":"testnet"},"name":"connect","status":"PASS","ts":"2026-07-12T19:46:35.256210+00:00"},
    {"data":{"available_margin":999.0,"equity":999.0,"withdrawable":999.0},"name":"account","status":"PASS","ts":"2026-07-12T19:46:35.970227+00:00"},
    {"data":{"bars":[{"close":63919.0,"high":64120.0,"low":63863.0,"open":63994.0,"ts":"2026-07-12T17:00:00Z","volume":6.64689},{"close":64012.0,"high":64029.0,"low":63888.0,"open":63932.0,"ts":"2026-07-12T18:00:00Z","volume":3.5634},{"close":64016.0,"high":64120.0,"low":64009.0,"open":64012.0,"ts":"2026-07-12T19:00:00Z","volume":0.32303}],"count":3},"name":"candles","status":"PASS","ts":"2026-07-12T19:46:37.008545+00:00"},
    {"data":{"coin":"BTC","entry_limit":57610.0,"market_reference":64016.0,"modified_stop_trigger":56740.0,"notional_usd":11.522,"qty":0.0002,"size_decimals":5,"stop_trigger":56450.0},"name":"meta_and_plan","status":"PASS","ts":"2026-07-12T19:46:37.777163+00:00"},
    {"data":{"flattened_symbols":[]},"name":"partial_fill_guard","status":"PASS","ts":"2026-07-12T19:46:41.107691+00:00"},
    {"data":{"errors":[]},"name":"deterministic_cleanup","status":"PASS","ts":"2026-07-12T19:46:41.107701+00:00"},
    {"data":{"error":"cloid 0x95f589787908b598642cba45f8562333 (ENTRY) missing from open_orders and not explained; raw_response={\"status\": \"ok\", \"response\": {\"type\": \"order\", \"data\": {\"statuses\": [{\"error\": \"Trigger order has unexpected type.\"}]}}}","error_type":"HyperliquidOrderError","raw_response":"{\"status\": \"ok\", \"response\": {\"type\": \"order\", \"data\": {\"statuses\": [{\"error\": \"Trigger order has unexpected type.\"}]}}}"},"name":"failure","status":"FAIL","ts":"2026-07-12T19:46:41.107730+00:00"},
    {"data":{},"name":"disconnect","status":"PASS","ts":"2026-07-12T19:46:42.075252+00:00"}
  ]
}
```

Remaining blocker: the native trigger request type is rejected by the real exchange. The response
shape is captured and the architecture amendment records it. P0 exit criteria are not met; any
payload correction and any subsequent testnet attempt require new explicit approval. P2 remains
unapproved.

## Re-approved P0 attempt 6 — G1/G2 normalTpsl grouping — 2026-07-12

Commit `a4de4a6e` changed entry brackets to `grouping="normalTpsl"`, retained
`positionTpsl` for re-protection, and added one bounded in-run `na` fallback for concrete
type/grouping rejections. Adapter requests are tested through the installed SDK's
`order_type_to_wire` and `order_request_to_order_wire` helpers. Both local suites passed before
the run:

```text
Repo root: 98 passed, 1 warning in 4.81s
IBKR_PAPER_BRIDGE/: 98 passed, 1 warning in 4.68s
```

The single testnet process ran once with `HL_LIVE_ACK` cleared. `normalTpsl` reached the exchange
and returned a resting entry plus the pending child status `waitingForFill`; this demonstrates that
the grouping/wire format was accepted for the unfilled entry. The C1 parser rejected the non-dict
pending status before it could construct verified order results. This was not a type/grouping
rejection, so the G2 `na` fallback was correctly **not** invoked. Total placement calls: **one**.

The captured raw response was:

```json
{"status":"ok","response":{"type":"order","data":{"statuses":[{"resting":{"oid":56380800181,"cloid":"0x473f5818479690c75b757a38900ad51b"}},"waitingForFill"]}}}
```

No `orders` result was persisted because parsing stopped; the resting entry identified above was
removed by C3. The log shows no changed position and two idempotent cleanup passes, both with
`errors: []` (the inner failed-placement cleanup plus the outer failure guard). No second smoke
process and no fallback placement occurred.

Complete overwritten `p0_smoke_log.json` for attempt 6:

```json
{
  "approved_scope":"one tiny resting entry plus native SL, modify, cancel, flatten only if needed",
  "finished_ts":"2026-07-12T20:03:00.579701+00:00",
  "network":"testnet",
  "orders":[],
  "result":"FAIL",
  "run_id":"p0-20260712T200243Z",
  "started_ts":"2026-07-12T20:02:43.147580+00:00",
  "steps":[
    {"data":{"credential_source":"user_registry"},"name":"credential_source","status":"PASS","ts":"2026-07-12T20:02:43.147640+00:00"},
    {"data":{"account_address":"0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49","account_mode":"unifiedAccount","network":"testnet"},"name":"connect","status":"PASS","ts":"2026-07-12T20:02:52.306032+00:00"},
    {"data":{"available_margin":999.0,"equity":999.0,"withdrawable":999.0},"name":"account","status":"PASS","ts":"2026-07-12T20:02:52.601957+00:00"},
    {"data":{"bars":[{"close":64012.0,"high":64029.0,"low":63888.0,"open":63932.0,"ts":"2026-07-12T18:00:00Z","volume":3.5634},{"close":64069.0,"high":64120.0,"low":64009.0,"open":64012.0,"ts":"2026-07-12T19:00:00Z","volume":0.37676},{"close":64139.0,"high":64161.0,"low":64081.0,"open":64081.0,"ts":"2026-07-12T20:00:00Z","volume":0.09881}],"count":3},"name":"candles","status":"PASS","ts":"2026-07-12T20:02:53.641938+00:00"},
    {"data":{"coin":"BTC","entry_limit":57720.0,"market_reference":64139.0,"modified_stop_trigger":56850.0,"notional_usd":11.544,"qty":0.0002,"size_decimals":5,"stop_trigger":56560.0},"name":"meta_and_plan","status":"PASS","ts":"2026-07-12T20:02:54.579669+00:00"},
    {"data":{"diagnostic":"waitingForFill; raw_response={\"status\": \"ok\", \"response\": {\"type\": \"order\", \"data\": {\"statuses\": [{\"resting\": {\"oid\": 56380800181, \"cloid\": \"0x473f5818479690c75b757a38900ad51b\"}}, \"waitingForFill\"]}}}","error_type":"HyperliquidOrderError","grouping":"normalTpsl"},"name":"placement_normalTpsl_failed","status":"WARN","ts":"2026-07-12T20:02:55.966715+00"},
    {"data":{"flattened_symbols":[]},"name":"partial_fill_guard","status":"PASS","ts":"2026-07-12T20:02:59.138038+00"},
    {"data":{"errors":[]},"name":"deterministic_cleanup","status":"PASS","ts":"2026-07-12T20:02:59.138047+00"},
    {"data":{"error":"waitingForFill; raw_response={\"status\": \"ok\", \"response\": {\"type\": \"order\", \"data\": {\"statuses\": [{\"resting\": {\"oid\": 56380800181, \"cloid\": \"0x473f5818479690c75b757a38900ad51b\"}}, \"waitingForFill\"]}}}","error_type":"HyperliquidOrderError","raw_response":"{\"status\": \"ok\", \"response\": {\"type\": \"order\", \"data\": {\"statuses\": [{\"resting\": {\"oid\": 56380800181, \"cloid\": \"0x473f5818479690c75b757a38900ad51b\"}}, \"waitingForFill\"]}}}"},"name":"failure","status":"FAIL","ts":"2026-07-12T20:02:59.138076+00"},
    {"data":{"flattened_symbols":[]},"name":"partial_fill_guard","status":"PASS","ts":"2026-07-12T20:03:00.277802+00"},
    {"data":{"errors":[]},"name":"deterministic_cleanup","status":"PASS","ts":"2026-07-12T20:03:00.277812+00"},
    {"data":{},"name":"disconnect","status":"PASS","ts":"2026-07-12T20:03:00.579690+00"}
  ]
}
```

Remaining blocker: teach the C1 verification parser to classify `waitingForFill` as an expected
normalTpsl pending child state and verify the accepted resting entry before cancellation. This is a
local parsing change, but a new P0 approval is required before another testnet run. P0 exit criteria
are not met; P2 remains unapproved.

## P0 attempt 7 — PASS — 2026-07-12 (builder+auditor: Claude Opus 4.8)

W1 (`93713647`) normalized `waitingForFill`/`waitingForTrigger` string statuses into a
`pending_child` marker, verified such roles as `WAITING_CHILD`, exempted them from the smoke
visibility check, and made modify tolerant on pending children. Both suites: **100 passed** from
both CWDs. Secret grep on changed files + log: zero matches.

Run `p0-20260712T201750Z`, result **PASS**, 12 steps all green:
`credential_source(user_registry)` → `connect(testnet, unifiedAccount)` → `account(999 USDC)` →
`candles(3 bars)` → `meta_and_plan(entry 57680, SL 56560→56810, qty 0.0002, ~$11.54)` →
`place_atomic_normalTpsl` (ENTRY oid **56381230513**, SL oid **56381230514** — this run the SL
also rested with its own oid; both shapes now supported) → `verify_open_orders` (both cloids
visible, `pending_children: []`) → `modify_stop` (**real on-exchange trigger modify worked**) →
`cancel_owned_orders` → `verify_cleanup` (zero remaining) → `partial_fill_guard` (no fills) →
`disconnect`.

**PREREG §4 P0 exit criteria: connect ✓ account ✓ live candle ✓ entry + SL trigger group placed ✓
(and modified ✓) cancelled ✓ all steps JSON-logged ✓ — P0 exit criteria MET.**
Gate formally closed under Barış's 2026-07-12 blanket approval (16_GO_LIVE_PLAN §0); evidence
self-audited on the raw log by the same model that ran it — next model may re-verify from
`docs/p0_smoke_log.json`.
