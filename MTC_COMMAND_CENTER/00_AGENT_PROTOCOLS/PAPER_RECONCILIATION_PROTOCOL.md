# PAPER / RECONCILIATION PROTOCOL

> Status: DRAFT.
> Track: SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.
> Binding status: active only under a signed
> `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/VERTICAL_SLICE_SCOPE.md`.

This protocol tests plumbing, not strategy quality.

No real exchange API keys, mainnet, real capital, broker actions, paper-broker
actions, TradingView actions, WunderTrading actions, or testnet actions are
authorized by this draft protocol.

## Three Ledgers

1. EXPECTED:
   signals the Python reference path says should exist. Source of truth for the
   core slice.
2. RECEIVED:
   signals accepted or rejected by the local receiver after validation and
   deduplication. Disposition values: `accepted`, `duplicate_dropped`, or
   `rejected(reason)`.
3. FILLED:
   simulated fill results in the core slice, or demo/testnet fills only in
   separately approved extension legs.

## Daily Reconciliation Report

One report artifact per day.

Required fields:

- date
- benchmark id
- environment
- active leg
- git commit
- expected count
- received count
- filled count
- duplicates dropped
- rejected count
- EXPECTED-not-RECEIVED rows
- RECEIVED-not-EXPECTED rows
- RECEIVED-not-FILLED rows
- explanation for every orphan or status `UNEXPLAINED`

Rules:

- Any `UNEXPLAINED` orphan halts the slice until explained.
- Reports must carry SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.
- Reports must not feed promotable buckets, scorecards, or strategy-quality
  KPIs.
- The dashboard may read reports only in a read-only status surface after
  separate approval.

## Induced-Failure Drills

Each active leg must run the relevant drills at least once and log the result.

| Drill | Injection | Pass criteria |
|---|---|---|
| D1 duplicate signal | Send identical payload twice | Second payload dropped by `idempotency_key`; one intent only |
| D2 dropped signal | Suppress one expected emission | Daily report flags EXPECTED-not-RECEIVED same day |
| D3 exit-with-no-position | Send EXIT while flat | Rejected with reason; no intent created |
| D4 wrong environment | Send `environment: "live"` payload | Rejected; loud log entry |
| D5 malformed payload | Break schema or checksum | Rejected; raw payload preserved in log |
| D6 receiver down | Stop receiver during extension-leg delivery | Observed behavior documented; no workaround building |
| D7 restart mid-state | Kill executor with open testnet position | Leg 3 only; restart reconciles state from testnet without duplicate order |

## Weekly Review Row

Append one row per week to a cumulative report:

- date
- new signals
- drills run
- orphan count
- unexplained count
- active leg status
- budget check against 75/25 cap
- one-line assessment

Unexplained count must be zero to continue.

## Roles

- Baris:
  signs gates, picks benchmark, halts/resumes on unexplained breaks, decides
  day-30 continue/pause/kill.
- Fable:
  decisions, contracts, and adversarial review only.
- Codex:
  bounded implementation planning and audit after approval.
- Cline / DeepSeek:
  mechanical work after approval, with exact allowlists and no protected-scope
  drift.

## Appendix A - Draft `mtc.signal/v1` Schema Content

This appendix is draft schema content only. It is intentionally not written to
`MTC_COMMAND_CENTER/06_SCHEMAS/`. That protected write requires a separate
Gate V1 `schema_allow` approval.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "mtc.signal/v1",
  "title": "MTC Signal Payload v1 - SYSTEM_TEST_ONLY track",
  "description": "Canonical signal contract emitted by the Python reference path and validated by any receiver. NO REAL MONEY: 'live' is a reserved environment value that no current component is authorized to emit or accept.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema",
    "strategy_id",
    "strategy_version",
    "environment",
    "symbol",
    "exchange",
    "timeframe",
    "signal_id",
    "idempotency_key",
    "timestamp_utc",
    "bar_time_utc",
    "side",
    "action",
    "qty_model",
    "risk_ref",
    "current_position_intent",
    "auth_token",
    "checksum"
  ],
  "properties": {
    "schema": { "const": "mtc.signal/v1" },
    "strategy_id": { "type": "string", "minLength": 1 },
    "strategy_version": {
      "type": "string",
      "description": "Parameter freeze tag plus git commit, for example 2026-07-02+commit8eae5790"
    },
    "environment": {
      "enum": ["paper", "testnet", "live"],
      "description": "Receivers must reject any environment they are not explicitly configured for. 'live' is currently forbidden everywhere."
    },
    "symbol": { "type": "string", "minLength": 1 },
    "exchange": { "type": "string", "minLength": 1 },
    "timeframe": { "type": "string", "pattern": "^[0-9]+(m|h|d)$" },
    "signal_id": {
      "type": "string",
      "description": "strategy_id|symbol|timeframe|bar_time_utc|action. Deterministic so retries carry the same id."
    },
    "idempotency_key": {
      "type": "string",
      "description": "sha256(signal_id + strategy_version). Receiver dedup key."
    },
    "timestamp_utc": { "type": "string", "format": "date-time" },
    "bar_time_utc": {
      "type": "string",
      "format": "date-time",
      "description": "UTC open time of the confirmed signal bar."
    },
    "side": { "enum": ["LONG", "SHORT", "FLAT"] },
    "action": { "enum": ["ENTRY", "EXIT", "CANCEL"] },
    "qty_model": { "enum": ["risk_pct", "fixed_qty", "none"] },
    "risk_ref": {
      "type": "string",
      "description": "Reference into the risk model, for example 0.5pct_equity. Receivers never invent size."
    },
    "stop_loss": { "type": ["number", "null"] },
    "take_profit": { "type": ["number", "null"] },
    "current_position_intent": {
      "enum": ["FLAT_TO_LONG", "FLAT_TO_SHORT", "LONG_TO_FLAT", "SHORT_TO_FLAT"]
    },
    "auth_token": {
      "type": "string",
      "description": "Per-strategy shared secret. Never committed to the repo."
    },
    "checksum": {
      "type": "string",
      "description": "sha256 of canonical concatenation of all fields except auth_token and checksum. Integrity only, not authenticity."
    }
  }
}
```

## Appendix B - Draft Validation Responsibilities

| Field | Producer | Receiver | Reconciler |
|---|---|---|---|
| `signal_id` | Derives deterministically from bar data | Logs raw value | Joins all ledgers |
| `idempotency_key` | Derives from `signal_id` and version | Dedup key | Confirms one fill per signal |
| `environment` | Sets per run config | Hard rejects mismatch | Flags leaks |
| `auth_token` | Embeds runtime secret | Authenticates before processing | Not stored in reports |
| `checksum` | Computes | Verifies truncation/integrity | Not applicable |
| `current_position_intent` | States expected transition | Verifies against tracked state | Flags state drift |
| `stop_loss` / `take_profit` / `risk_ref` | Computes | Sanity-checks, never invents | Compares intended versus applied risk |

