# P2 — MTC Integration Contract Pack (OrderIntent / ExitIntent / Sizing Ownership / Three-Layer State)

**Artifact:** Package 2 contract pack — Bridge V2, MTC integration contracts.
**Tier:** T2, documentation only.
**Date:** 2026-08-17 night.
**Gate-1 scope:** `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE2_MTC_INTEGRATION_CONTRACT_2026-08-17.md`.
**Accepted source:** `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §3 rows
"MTC sizing ownership and `OrderIntent`" and "MTC exit lifecycle, Multi-TP and basket/add support"; §4 Package 2.
**Status:** PROPOSED contract text — pending independent T2 review and owner acceptance. It **activates
nothing**. It is contract text that governs a **FUTURE, separately-gated T0 implementation**. No
implementation, wiring, configuration change, MTC/Pine/parity edit, order, TESTNET/MAINNET, ARM, or
economic action is authorized by this pack (see §7).
**Worktree HEAD read:** `b08aab35f7625e481c4a06f47ceffd1fd0740216` (observed via `git rev-parse HEAD` in
`C:\V2PACKS`, clean worktree of merged master; every `docs/30:<lines>` citation below was read at and
verified against this HEAD, so cited line numbers are committed lines, not the dirty-copy B8 numbering
warned about in the backlog's §1 evidence caveat).

---

## 0. Scope and method

This pack freezes: (a) the sizing-ownership contract direction and its open gates (§2); (b) frozen
`OrderIntent` / `ExitIntent` v1 schemas (§3, §4); (c) the desired / accepted / actual three-layer state
model (§5); (d) a register of every Pine/Python sizing and lifecycle parity gap named by the accepted
backlog's cited `docs/30` ranges, each RESOLVED (by contract text here) or OPEN (with what would close
it) (§6). Where `docs/30` leaves a decision genuinely open, this pack preserves it as OPEN with options
and consequences; it does not invent resolutions. UNKNOWN/OPEN stays UNKNOWN/OPEN.

Current-state truth was verified by direct read of the cited files (paths and line ranges in §1 and §8);
claims about design direction cite `docs/30:<lines>` at the HEAD above.

## 1. Current-state record (verified read-only at HEAD `b08aab35`)

**Bridge signal/plan shapes** — `Signal` carries `ts, symbol, direction ("LONG"|"SHORT"|"FLAT"), reason,
ref_price, stop_loss?, take_profit?` and **has no quantity field**
(`IBKR_PAPER_BRIDGE/bridge/engine/types.py:27-34`). A quantity first appears on `OrderPlan`
(`decision_uid?, signal, qty, entry_type ("MKT"|"LMT"), limit_price?, stop_loss, take_profit?, leverage=1,
risk_dollars, risk_pct`), which the Bridge itself creates (`types.py:37-47`).

**Bridge originates its own size** — `RiskConfig.risk_pct_per_trade` defaults to **0.005** (fraction
convention: 0.005 = 0.5%) (`bridge/engine/risk.py:37`; deployed value `config/bridge.yaml:14`),
`max_position_notional_pct` 0.20 (`risk.py:41`), `min_order_usd` 10.0 (`risk.py:43`), `max_leverage` 1
(`risk.py:44`; `bridge.yaml:21`), `min_stop_distance_pct` 0.001 (`risk.py:42`). `RiskEngine` computes
`risk_dollars = equity * risk_pct_per_trade`, `raw_qty = risk_dollars / stop_distance`,
`qty = round(raw_qty, size_decimals)` (`risk.py:379-381`), after stop-side and stop-distance gates
(`risk.py:370-377`), then minimum-order, notional-cap and margin gates (`risk.py:384-394`). One strategy
file is configured (`bridge.yaml:11`) and `tp_mode: none` (`bridge.yaml:34`).

**MTC Pine sizing** — `calc_l6_qty` uses `contract_multiplier = syminfo.pointvalue`, `min_qty =
syminfo.mincontract` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:339-341`); stop-risk branch
`raw_qty := risk_amount / (per_unit_risk * contract_multiplier)` (`MTC_V2.pine:351`); no-stop fallback
percent-of-equity notional (`MTC_V2.pine:353-354`); leverage cap divides by
`entry * contract_multiplier` (`MTC_V2.pine:356-357`); rounding is floor-to-`syminfo.mincontract`-step
(`MTC_V2.pine:251-253,359`) with a minimum-quantity gate only (`MTC_V2.pine:360-361`) — **no
minimum-notional gate**. Inputs: `risk_per_long_pct`/`risk_per_short_pct` default 1.0 (percent
convention: 1.0 = 1%), `fallback_size_pct` 10.0, `max_leverage_cap` 1.0 (`MTC_V2.pine:90-94`).

**MTC Python sizing** — `PositionSizer.calc_qty` stop-risk branch computes
`risk_amount = equity * (risk_pct / 100.0)`, `raw_qty = risk_amount / per_unit_risk` — **stop distance
only, no `contract_multiplier` in this branch** (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:43-47`)
— while the same function does use the multiplier in its leverage cap (`position_sizer.py:52-55`) and
applies `floor_qty`, `min_qty` (`position_sizer.py:60-64`) **and a `min_notional` gate**
(`position_sizer.py:66-68`). It returns 0.0 rather than an unsafe size.

**MTC basket/add and Multi-TP** — Pine declares `pyramiding=100` as a deliberately generous broker-level
ceiling (`MTC_V2.pine:5-7`); the actual add permission is `max_entries`, default **1** (`MTC_V2.pine:19`),
so with defaults MTC does not pyramid. Adds merge stops via `merge_pyramid_stop` (tightening max/min)
(`MTC_V2.pine:283-289`). `tp_mode` options include "Multi-TP" (`MTC_V2.pine:110`); TP1 closes
`tp1_close_pct` (default 50.0, max <100) of the position via `strategy.exit(..., qty_percent=tp1_close_pct)`
and TP2 closes the remainder (`MTC_V2.pine:115-117,1125-1139`, comment `MTC_V2.pine:941-942`); a completed
TP1 stays disarmed across same-direction adds (`MTC_V2.pine:942,959`).

**MTC live alert path** — the WunderTrading entry alert sends the fixed input `wt_amount` (default 100.0,
quote/base per `wt_amount_type`), not MTC's computed quantity (`MTC_V2.pine:183,2020`).

**Not connected** — MTC and the Bridge are not wired; within `bridge/` the only "MTC" occurrences are the
state-DB env var and deploy path (`docs/30:589-599`). This is a future integration conflict, not a present
double-order problem (`docs/30:598-599`).

**Divergent defaults (illustrative, `contract_multiplier = 1` assumed)** — $10,000 equity, entry $60,000,
stop $58,000: MTC default 1.0% → $100 risk → 0.05 BTC ($3,000 notional); Bridge default 0.5% → $50 risk →
0.025 BTC ($1,500) (`docs/30:551-560`). The Bridge's notional cap at 0.20 × 1x = $2,000 would reject the
$3,000 MTC request in any future validator that retained it (`docs/30:570-581`). Today no MTC number
arrives at all (`docs/30:576-579`).

## 2. Sizing ownership decision (contract text)

### 2.1 The ownership split — as docs/30 directs

Contract text (direction per `docs/30:608-633`, `docs/30:740-749` alternatives analysis):

1. **The strategy quantity is owned by the MTC strategy engine, not by the Bridge.** An `OrderIntent`
   carries an **exact requested quantity** together with the frozen policy and provenance inputs that
   produced it (risk percent, equity snapshot, instrument metadata, caps, rounding mode) — the full field
   set of §3. The Bridge `Signal`'s missing quantity (`types.py:27-34`) and the Bridge-originated
   `OrderPlan.qty` (`types.py:37-47`, `risk.py:379-381`) are the current-state gap this resolves: under
   this contract the quantity in an executed plan must be traceable to an accepted intent's
   `requested_qty`, never to an independently Bridge-originated number.
2. **The Bridge is an independent execution-safety envelope, not a second sizing brain.** On receiving a
   requested quantity it must: (a) **recompute and validate** the quantity from the supplied inputs;
   (b) check live account truth (margin, exposure, daily loss, leverage, liquidation distance, current
   positions); (c) **execute the exact quantity, or reject and log with a reason** (`docs/30:622-627`).
3. **The Bridge must not silently resize.** A silently resized order breaks the identity between what was
   backtested and what trades (`docs/30:628-630`). Reject-on-mismatch is the preferred mismatch policy;
   a `min(MTC, Bridge)` silent clamp is explicitly **not preferred** — it fails quietly, the worst failure
   mode (`docs/30:641-642`).
4. **The Portfolio Guardian may veto** an intent but must not silently mutate size; any policy permitting
   resize requires its own explicit parity contract and re-backtesting under that contract
   (`docs/30:631-633`, `docs/30:840-842`).

Options and consequences for the parts docs/30 leaves open (`docs/30:635-642`): *Bridge as sole sizing
owner* (viable, not preferred — discards MTC's tested sizing, backtests stop describing live behavior);
*shared canonical packaged sizing library* (viable strong long-term candidate — removes drift by
construction, couples releases, Pine remains a third implementation); *silent min-clamp* (not preferred);
*reject-on-mismatch* (**preferred** — divergence becomes a loud logged event; needs explicit tolerances so
rounding noise is not a mismatch — provided as `validation_tolerances`, §3.11).

### 2.2 Gated appointment — OPEN conditions

The preferred direction that **the MTC Python engine becomes the canonical strategy-sizing owner** takes
effect only once (`docs/30:611-621`): (a) the Pine↔Python parity gaps — the `contract_multiplier`
denominator (PSG-01) and the `min_notional` gate (PSG-02) — are **closed or explicitly bounded**; and
(b) a **frozen sizing contract is written and accepted** (this pack proposes that contract; acceptance is
still open). Until both hold, calling Python canonical would freeze a contract its own reference
implementation does not match. **Status of (a): OPEN** (§6). Which side of each gap is correct is itself
open and is not decided here (`docs/30:517`).

### 2.3 Envelope divergence — handling resolved now, values open

The numeric incompatibility between MTC's default sizing (1.0% risk → $3,000 on the illustration) and the
Bridge's currently configured envelope ($2,000 notional cap at 0.20 × 1x) is real and would surface the
moment the two are wired (`docs/30:570-587`). **Handling is fixed by this contract:** any such intent is
rejected loudly (`REJECTED:NOTIONAL_CAP`), never silently resized or clamped (§2.1.3). **Which values
change — MTC defaults, Bridge envelope thresholds, or both — is an owner decision at the future T0 gate
and is OPEN** (PSG-11b). The envelope behaving correctly is the shape of the conflict, not a defect
(`docs/30:583-587`).

### 2.4 Precedence

Per the accepted backlog and `docs/30:376-407`, this contract must exist **before any MTC-to-Bridge
integration, including a single-worker one** — the A10 sizing-ownership conflict exists as soon as the
first MTC-connected worker exists and cannot be deferred to the two-worker staging step
(`docs/30:392-397,405-407`).

## 3. Frozen `OrderIntent` schema v1 (`orderintent-v1`)

Field tables: **Name | Type | Unit | R | Semantics | Validation rule**. R = required (✓) / optional (o) /
conditional (c). All timestamps are timezone-aware UTC, ISO-8601, microsecond precision, `Z` suffix
(consistent with the TS-P1-002 canonical encoding, `docs/23:20-22,188-192`). All floats finite — NaN/±Inf
rejected before digesting (`docs/23:199-203`).

### 3.1 Envelope

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `schema_version` | literal string | — | ✓ | Exactly `"orderintent-v1"`. | Any other value rejects with `UNKNOWN_SCHEMA`; no best-effort parsing. |
| `intent_kind` | enum | — | ✓ | `"ENTRY"` for OrderIntent; `"EXIT"` is ExitIntent (§4). | Must be `"ENTRY"`. |

### 3.2 Identity and provenance (docs/30:651-659)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `intent_id` | string | — | ✓ | Unique idempotent identity of this decision, so a retry or duplicate delivery cannot become a second order. Format `intent-v1:<sha256-hex>` per TS-P1-002. | Length/prefix/hex checks per `docs/23:61`; digest verified against exact preimage, never trusted alone (`docs/23:49-53`); canonical fields (domain version, strategy id, uppercase symbol, uppercase direction, UTC signal ts) must reproduce it (`docs/23:15-23`). Exact duplicate intent+request → `BLOCKED`, no broker I/O (`docs/23:131-136`). |
| `decision_uid` | string | — | ✓ | Run-scoped decision identity carried through decision/trade/order lineage (`docs/23:165-167`). | Non-empty; the Bridge's `OrderPlan.decision_uid` lineage discipline applies unchanged. |
| `strategy_id` | string | — | ✓ | Stable strategy identifier of the emitting engine (current Bridge value `keltner_trail_ema8`, `docs/23:17`; the MTC integration's stable id is assigned at the future T0 wiring — OPEN, not invented here). | Non-empty; must equal the id inside the `intent_id` preimage. |
| `strategy_version` | string | — | ✓ | Immutable version of the strategy logic that produced the decision. | Non-empty. |
| `sizing_policy_version` | string | — | ✓ | Version id or immutable hash of the sizing config, so a validator can prove both sides used the *same* policy, not merely the same field names (`docs/30:656-658`). | Non-empty; validator must be able to recompute the hash from the §3.7 policy inputs. |
| `reason` | string | — | ✓ | Decision provenance / signal reason code. | Non-empty; stable reason-code vocabulary owned by the strategy. |

### 3.3 Time (docs/30:661-667)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `created_ts` | datetime | UTC | ✓ | When the intent was produced. | Tz-aware (naive rejected, `docs/23:188-192`); normalized UTC µs `Z`. |
| `signal_ts` | datetime | UTC | ✓ | The bar/event the decision was made from. **Not the same value as `created_ts` and must not be collapsed** (`docs/30:664-666`). | Tz-aware; `signal_ts <= created_ts`; must equal the `intent_id` preimage signal ts. |
| `expires_ts` | datetime | UTC | ✓ | Freshness bound: after it, the intent must be rejected rather than executed late (`docs/30:666-667`). | `expires_ts > created_ts`; a Bridge receive past `expires_ts` → `REJECTED:FRESHNESS`. |

### 3.4 Instrument, venue, account, direction, timeframe (docs/30:669-675)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `symbol` | string | — | ✓ | Instrument identifier, normalized uppercase (`docs/23:20`). | Non-empty, uppercase; matches `intent_id` preimage. |
| `venue` | string | — | ✓ | Exchange identifier. | Non-empty; must match the worker's configured venue. |
| `account` | string | — | ✓ | Account/subaccount the intent is bound to (ties to the A3/A6 isolation boundary, `docs/30:673`). | Non-empty; must match the receiving worker's account identity. **Value binding is conditioned on the Package 1 / Package 7 exchange-model decisions — OPEN.** |
| `direction` | enum | — | ✓ | `"LONG"` \| `"SHORT"` (open intent). `"FLAT"` is expressed only via ExitIntent CLOSE (consistent with `types.py:30`). | Matches `intent_id` preimage; consistent with stop/TP sides. |
| `timeframe` | string | — | ✓ | Strategy bar timeframe the decision was evaluated on (`docs/30:675`). | Non-empty; within the strategy_version's declared timeframe set. |

### 3.5 Entry execution

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `entry_type` | enum | — | ✓ | `"MKT"` \| `"LMT"` (mirrors `types.py:41`). | Enum member; part of the request identity (`docs/23:33`). |
| `limit_price` | price | quote/base | c | Limit price; **required iff `entry_type="LMT"`**, else null (`docs/23:34` requires explicit null symmetry). | Finite > 0 when present; correct side vs `entry_ref_price`. |
| `leverage` | int | × | ✓ | Requested leverage. Part of request identity (`docs/23:37`). | Integral (non-integral rejected, never truncated, `docs/23:117,201`); ≥ 1 and ≤ the authorized venue/worker cap (V1 baseline cap is 1). |

### 3.6 Quantity semantics (docs/30:677-684)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `requested_qty` | decimal | see `qty_unit` | ✓ | The exact strategy-owned quantity (`docs/30:679`). | Finite > 0; exact multiple of `qty_step` in integer lot units (no epsilon; consistent with `types.py:474-495`); ≥ `min_qty`; notional ≥ `min_notional`; Bridge recomputes from §3.7 inputs and rejects beyond `validation_tolerances` — never resizes. |
| `qty_unit` | enum | — | ✓ | `"BASE"` \| `"QUOTE"` \| `"CONTRACTS"` — a bare number is unusable without it (`docs/30:680-681`). | Enum member. Accepted-unit subset for execution is bound to the accepted sizing contract; `CONTRACTS` is affected by PSG-01 and stays outside the validated domain until that gap closes. |
| `qty_semantics` | enum | — | ✓ | `"DELTA"` (order size to send) or `"TARGET_TOTAL"` (resulting total position) — the two produce different orders from the same number; the single most dangerous ambiguity in the schema (`docs/30:682-684`). | Required, **no default**. For `entry_seq>1`, validator derives the implied order from `existing_position_context` and cross-checks against `target_position_context`; inconsistency → `REJECTED:QTY_SEMANTICS`. |

### 3.7 Sizing-policy inputs (docs/30:686-702)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `sizing_branch` | enum | — | ✓ | `"STOP_RISK"` \| `"FALLBACK"` — the branch actually taken (`docs/30:688`). | `STOP_RISK` requires `stop_loss`; `FALLBACK` requires `fallback_size_pct`. |
| `risk_pct` | percent | percent units | c | Risk percent used, **scale stated explicitly: `1.0` means one percent** (the MTC Pine/Python convention, `risk_pct / 100.0`, `MTC_V2.pine:350`, `position_sizer.py:46`). The Bridge's internal fraction convention (0.005 = 0.5%, `risk.py:37`) never appears in an intent; conversion is validator-internal (`docs/30:690-694` requires the contract to name one convention — this is it). | Required iff `sizing_branch="STOP_RISK"`; > 0; never compared raw across conventions. |
| `fallback_size_pct` | percent | percent units | c | Percent-of-equity notional used when no stop-based risk distance exists (`docs/30:689`; `MTC_V2.pine:353-354`, `position_sizer.py:49-50`). | Required iff `sizing_branch="FALLBACK"`; > 0. |
| `entry_ref_price` | price | quote/base | ✓ | Entry reference price (`docs/30:695`). | Finite > 0; part of request identity (`docs/23:31`). |
| `entry_ref_price_meaning` | enum | — | ✓ | Meaning of the reference, e.g. `"SIGNAL_BAR_CLOSE"`. | Enum member from the strategy_version's declared vocabulary. |
| `stop_loss` | price | quote/base | c | Initial stop-loss (`docs/30:696`). | Required iff `sizing_branch="STOP_RISK"`; finite > 0; correct side (LONG: < entry; SHORT: > entry — mirrors `risk.py:373-376`); Bridge min-stop-distance policy applies as a loud reject, not a silent move. |
| `take_profit` | price | quote/base | c | Single full-quantity target for TP modes ATR/Percent/R (`MTC_V2.pine:110`). | Present only iff `tp_mode ∈ {ATR, PERCENT, R}` and a target exists; correct side of entry; mutually exclusive with non-empty `tp_legs`. |
| `equity_snapshot` | object | — | ✓ | Frozen equity the size was computed against: value, id, timestamp, source (`docs/30:697`; per-bar freeze, `docs/30:518-521`). | Subfields all required: `value` (quote, finite > 0), `snapshot_id` (non-empty, idempotent), `ts` (tz-aware UTC, ≤ `created_ts`), `source` (named). |
| `contract_multiplier` | decimal | × | ✓ | Instrument contract multiplier (`docs/30:698`). | Finite > 0. **Until PSG-01 closes or is explicitly bounded, the validated domain is `contract_multiplier = 1` instruments only** (the bounding option `docs/30:513-517` permits); a multiplier ≠ 1 intent rejects with `OUT_OF_PARITY_DOMAIN`. |
| `qty_step` | decimal | base | ✓ | Instrument quantity step (`docs/30:699`). | > 0; `requested_qty` must quantize exactly (§3.6). |
| `min_qty` | decimal | base | ✓ | Instrument minimum quantity (`docs/30:700`). | > 0; `requested_qty ≥ min_qty` (both MTC implementations return 0.0 below minimum rather than an unsafe size — `position_sizer.py:63-64`, `MTC_V2.pine:360-361`; an intent below minimum is a validation failure). |
| `min_notional` | quote | quote | ✓ | Instrument minimum notional (`docs/30:700`). | `requested_qty × entry_ref_price × contract_multiplier ≥ min_notional` else `REJECTED:BELOW_MIN_NOTIONAL`. **Pine-side parity of this gate is OPEN (PSG-02)** — the intent carries the value; cross-implementation agreement is not yet claimed. |
| `leverage_cap` | decimal | × | ✓ | Strategy internal sizing cap, not broker margin (`MTC_V2.pine:94`; `docs/30` A10 evidence). | ≥ 1…≥ 0 per strategy policy; `qty × entry × multiplier ≤ equity_snapshot.value × leverage_cap` (`MTC_V2.pine:356-357`, `position_sizer.py:52-55`). |
| `rounding_mode` | enum | — | ✓ | Rounding applied to the raw size. MTC current: `"FLOOR_TO_STEP"` (`MTC_V2.pine:251-253,359`, `position_sizer.py:60`). | Enum member; `requested_qty` must equal the declared rounding of the recomputed raw value within `validation_tolerances` — a mismatch rejects, never rounds. |

### 3.8 Stop semantics (docs/30:808-820, 874-875)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `stop_semantics` | enum | — | ✓ | `"NATIVE_STRATEGY_STOP"` (the MTC stop is itself the continuously active native exchange stop) or `"SYNTHETIC_EXIT_PLUS_EMERGENCY"` (MTC uses a synthetic/bar-evaluated exit while the Bridge maintains a separately named emergency native safety stop). The two meanings **cannot share one field or be mixed silently** (`docs/30:816-817`). | Required, no default. **Which value the MTC integration uses is OPEN (PSG-05)** — the field forces the choice to be explicit per intent; parity evidence is required for whichever semantics is chosen (`docs/30:818-820`). |
| `emergency_stop` | object | — | c | When `stop_semantics="SYNTHETIC_EXIT_PLUS_EMERGENCY"`: the separate emergency stop's name and level policy (`docs/30:874-875`). | Required iff synthetic mode. Subfields: `name` (distinct from the strategy stop's identity), `level_policy` (how the level is set). **Definition is OPEN under PSG-05.** |

### 3.9 TP structure — Multi-TP (docs/30:799-806, 868-869)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `tp_mode` | enum | — | ✓ | `"NONE"` \| `"ATR"` \| `"PERCENT"` \| `"R"` \| `"MULTI_TP"` (mirrors `MTC_V2.pine:110`; current Bridge config is `none`, `bridge.yaml:34`). | Enum member; decides `take_profit` vs `tp_legs` exclusivity. |
| `tp_legs` | list<leg> | — | c | **Required iff `tp_mode="MULTI_TP"`**, else empty. Expresses MTC's fractional TP1 plus TP2 remainder — the capability the current single-optional-`take_profit` `OrderPlan` cannot carry (`docs/30:799-803`). | 1–2 legs initially (TP1 fractional, TP2 remainder; `MTC_V2.pine:115-117,1125-1139`); ordered by `order_ordinal`; all prices on the profit side of entry; distinct prices; `close_pct` of every non-final leg in (0, 100); **exactly one final leg flagged `is_remainder`** closing the remainder (`MTC_V2.pine:1128-1129`); fractional legs plus remainder = 100% of the position at decision time. Leg identity, activation and cancellation behavior per `docs/30:868-869`: legs activate at entry fill; a filled or cancelled leg's effect on later legs recomputes from **actual** fills (§5 layer 3); what happens when TP1 only partly fills is **OPEN (PSG-07)**. |

`tp_legs` leg subfields: `leg_id` (string, e.g. "TP1"/"TP2"), `trigger_price` (price, required),
`close_pct` (percent units, required), `close_basis` (enum `"FRACTION_OF_POSITION"` per
`MTC_V2.pine:1127` `qty_percent`), `order_ordinal` (int, required), `is_remainder` (bool, required).

### 3.10 Add / basket lifecycle (docs/30:704-713, 727-729; 870-871)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `lifecycle_id` | string | — | ✓ | Which position lifecycle this intent belongs to, so adds and a fresh entry are distinguishable (`docs/30:706-707`). | Non-empty; `entry_seq=1` opens a new lifecycle; `entry_seq>1` must reference an existing accepted lifecycle for the same `strategy_id`, `symbol`, `direction`. |
| `entry_seq` | int | ordinal | ✓ | Entry/add sequence number within the lifecycle (`docs/30:708`). | ≥ 1; ≤ the strategy's declared `max_entries` (the actual add permission — default 1, `MTC_V2.pine:19`; `pyramiding=100` is only a broker ceiling, `MTC_V2.pine:5-7`, `docs/30:527-536`); beyond it → `REJECTED:ADD_PERMISSION`. |
| `existing_position_context` | object | — | ✓ | Existing position at decision time (side, base size, avg entry) — null iff `entry_seq=1` (`docs/30:709`). | When present, must match the Bridge's **actual** layer (§5) within `validation_tolerances`; mismatch → `REJECTED:STALE_CONTEXT` — the Bridge never trades against a book it cannot confirm. |
| `target_position_context` | object | — | c | Target total position at decision time (`docs/30:709-710`). | Required iff `qty_semantics="TARGET_TOTAL"`; consistent with `existing_position_context` + `requested_qty`. |

**Open sub-decision preserved:** whether MTC emits one intent per add or an intent describing the target
basket is OPEN (PSG-04b, `docs/30:727-729`); the schema carries both unambiguously via `qty_semantics` +
`entry_seq` (`docs/30:710-713` demands the schema be unambiguous when `max_entries > 1` even though the
default is 1).

### 3.11 Validation (docs/30:715-720, 881-882)

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `validation_tolerances` | object | — | ✓ | What counts as a mismatch, so rounding noise is not treated as divergence (`docs/30:642,717`). | Subfields: `qty_lots_abs_tol` (integer lot units — quantities compare in exact integer lots, `types.py:474-495`; 0 means exact), `price_abs_tol` (quote). A recomputation outside tolerance → loud `REJECTED:QTY_MISMATCH` with the expected value logged. **Never silent mutation.** |
| `parity_binding` | object | — | o | References binding this intent's policy to its parity evidence: sizing-contract version, Pine export ref, Python run ref (`docs/30:718-720`). | Optional in transport; **required non-null before any activation gate** — Pine == Python == Bridge-validated plus exchange precision (step/minimum satisfied by the same number) must be on record before the first live intent is accepted (`docs/30:885-886`). |

## 4. Frozen `ExitIntent` schema v1 (`exitintent-v1`)

Direction per `docs/30:825-839`: after an accepted lifecycle contract exists, the MTC Python engine owns
desired economic intent — initial SL, every TP leg and quantity, break-even and trailing desired updates,
close reason, add/basket identity. The Bridge owns execution and truth: idempotent identity, submission,
reduce-only flags, acknowledgements, fill accounting, reconciliation, missing-stop re-protection,
cancel/replace, safe flattening (`docs/30:829-832`, current custodian duties `docs/30:762-777`). The
Bridge must execute the exact accepted intent or reject and log it; it must not silently change quantity,
SL, TP, or TP-leg allocation, widen a stop, independently rerun MTC exit logic, or treat an MTC simulated
close as proof of an exchange fill (`docs/30:833-836`).

| Name | Type | Unit | R | Semantics | Validation rule |
|---|---|---|---|---|---|
| `schema_version` | literal string | — | ✓ | Exactly `"exitintent-v1"`. | Else `UNKNOWN_SCHEMA`. |
| `intent_kind` | enum | — | ✓ | `"EXIT"`. | Must be `"EXIT"`. |
| `intent_id` | string | — | ✓ | Idempotent identity of this exit decision (TS-P1-002 semantics as §3.2). | Same rules as §3.2; duplicate delivery → `BLOCKED`, never a second order. |
| `decision_uid` | string | — | ✓ | Run-scoped decision identity. | Non-empty. |
| `strategy_id` | string | — | ✓ | As §3.2. | Non-empty; matches lifecycle. |
| `strategy_version` | string | — | ✓ | As §3.2. | Non-empty. |
| `reason` | string | — | ✓ | Decision provenance (which rule fired: trail, BE, TP, time stop…). | Non-empty. |
| `created_ts` | datetime | UTC | ✓ | When the exit intent was produced. | Tz-aware UTC; `signal_ts <= created_ts`. |
| `signal_ts` | datetime | UTC | ✓ | Bar/event the exit decision was made from. | Tz-aware UTC. |
| `expires_ts` | datetime | UTC | ✓ | Freshness bound — a late stop update must be rejected, not applied (`docs/30:872-873` freshness). | > `created_ts`; expiry → `REJECTED:FRESHNESS`. |
| `symbol` | string | — | ✓ | As §3.4. | Uppercase; matches lifecycle. |
| `venue` | string | — | ✓ | As §3.4. | Matches worker. |
| `account` | string | — | ✓ | As §3.4 (binding OPEN, same condition). | Matches worker. |
| `direction` | enum | — | ✓ | Side of the position being managed: `"LONG"` \| `"SHORT"`. | Matches the accepted lifecycle. |
| `timeframe` | string | — | ✓ | As §3.4. | Within strategy vocabulary. |
| `lifecycle_id` | string | — | ✓ | The position lifecycle this exit applies to (`docs/30:706-707`, `870-871`). | Must reference an accepted, non-terminal lifecycle. |
| `action` | enum | — | ✓ | `"STOP_UPDATE"` (covers break-even and trail — they are stop-level updates) \| `"TP_LEG_UPDATE"` \| `"CLOSE_FULL"` \| `"CLOSE_PARTIAL"`. | Enum member; gates the conditional fields below. |
| `update_seq` | int | ordinal | ✓ | Monotonic ordering of updates within the lifecycle, so stale reordering cannot apply (`docs/30:872-873` ordering). | Strictly greater than the last applied update for this lifecycle; equal/lower → `REJECTED:STALE_ORDERING` (unless exact duplicate → `BLOCKED`). |
| `new_stop_price` | price | quote/base | c | Required iff `STOP_UPDATE`: the requested stop. **Tighten-only:** for LONG `new_stop_price ≥` current accepted stop; for SHORT `≤` (`docs/30:837-839`; current Bridge applies stop updates only when they tighten protection, `docs/30:775-776`). | Widening → `REJECTED:STOP_WIDEN_FORBIDDEN`. Correct side of entry/position; fresh, authorized, correctly versioned before any native-order modification (`docs/30:837-839`). |
| `stop_semantics` | enum | — | c | Required iff `STOP_UPDATE`: same enum as §3.8; must equal the lifecycle's accepted `stop_semantics`. | Mismatch with the accepted lifecycle → `REJECTED:STOP_SEMANTICS_MISMATCH` (no silent mixing, `docs/30:816-817`). |
| `target_leg_id` | string | — | c | Required iff `TP_LEG_UPDATE`: which leg (`docs/30:868-869` TP-leg identity). | Must reference an active leg of the lifecycle. |
| `new_tp_leg` | object | — | c | Required iff `TP_LEG_UPDATE`: replacement leg (trigger price, close_pct; same subfield vocabulary as §3.9). | Validates as a leg per §3.9; reallocation may not silently change other legs — a change to allocation is its own explicit update (`docs/30:833-835`). |
| `close_qty` | decimal | see `close_qty_unit` | c | Required iff `CLOSE_PARTIAL`. | Finite > 0; lot-exact; ≤ actual remaining position. |
| `close_qty_unit` | enum | — | c | Required iff `CLOSE_PARTIAL`: `"BASE"` (QUOTE/CONTRACTS per PSG-01 domain note). | Enum member. |
| `close_qty_semantics` | enum | — | c | Required iff `CLOSE_PARTIAL`: `"DELTA"` (reduce amount) \| `"TARGET_REMAINING"` (leave this much). | No default — same anti-ambiguity rule as §3.6. |
| `close_reason` | enum/string | — | c | Required iff `CLOSE_FULL`/`CLOSE_PARTIAL`: the strategy's close reason (`docs/30:827`). | From the strategy's stable reason vocabulary (e.g. MTC exit reasons `MTC_V2.pine:217-218,329-337`). |
| `reduce_only` | literal bool | — | ✓ | Always `true` — exits are reduce-only by construction (native reduce-only trigger orders, `docs/30:779-782`). | Any other value → `REJECTED:REDUCE_ONLY_REQUIRED`. |

**Hard rule:** a `CLOSE_*` intent requests the Bridge's cancel/replace and safe-flatten path
(`docs/30:776-777`); the lifecycle closes only on actual exchange-fill truth (§5 layer 3) — an MTC
simulated close is never proof of a fill (`docs/30:835-836`, `788-790`).

## 5. Desired / accepted / actual — three-layer state model

Direction per `docs/30:843-846`: the dashboard must show three separate states — **desired by MTC**,
**accepted or rejected by Bridge**, **actually acknowledged/filled at the exchange**; combining them into
one "current order" value would hide exactly the divergence this contract exists to expose.

### 5.1 Layer definitions and ownership

| Layer | Owner ( sole write authority ) | Content | Never contains |
|---|---|---|---|
| **1. Desired** | MTC strategy engine | The stream of OrderIntent/ExitIntent objects and their per-intent states: `EMITTED → EXPIRED \| SUPERSEDED` (terminal). A later intent in the same lifecycle supersedes an unexecuted earlier one (e.g. a stop-update chain). | Any claim about the exchange: no fill, no acknowledgment, no position fact. MTC simulated exits stay here (`docs/30:788-790`). |
| **2. Accepted / Rejected** | Bridge | The Bridge's verdict per intent: `RECEIVED → VALIDATING → ACCEPTED (reserved durably) → SUBMITTED`, or terminal `REJECTED:<reason_code>`, `BLOCKED_DUPLICATE`, `IDENTITY_COLLISION`. Durable reservation follows TS-P1-002: `BEGIN IMMEDIATE`, insert `RESERVED` before any broker I/O; exact intent+request duplicate → `BLOCKED` with no I/O; same intent different request → `IdentityCollisionError` (`docs/23:127-136`); atomic finalization `RESERVED → SUBMITTED` (identity-table state, distinct from the Layer-3 `OrderState.SUBMITTED`; `docs/23:138-149`). Guardian veto is a `REJECTED:GUARDIAN_VETO`, never a mutation (`docs/30:840-842`). | Fabricated fills; silently mutated quantities, SL, TP, or TP-leg allocation (`docs/30:833-835`). |
| **3. Actual** | Exchange (recorded and reconciled by the Bridge only) | Exchange truth per order: the canonical `OrderState` vocabulary — `PENDING_NEW, SUBMITTING, SUBMITTED, OPEN, PARTIALLY_FILLED, PENDING_CANCEL, FILLED, CANCELED, REJECTED, EXPIRED, UNKNOWN_SUBMISSION` (`types.py:119-142`, `docs/22`) — with transitions only per `ORDER_STATE_TRANSITIONS` (`types.py:206-292`); position actuals from authoritative fills only (`docs/30:770-771`); partial-entry protection states per TS-P1-004 (`types.py:595-619`, `docs/22` amendment). | Anything copied from layers 1–2. `UNKNOWN_SUBMISSION` is frozen pending reconciliation — never terminal, never blindly retried (`docs/22:82,157-163`). |

### 5.2 Cross-layer transitions and invariants

1. **1→2:** acceptance requires: schema valid; fresh (`expires_ts`); identity reserved per `docs/23`;
   recomputed quantity within `validation_tolerances`; envelope checks (margin, exposure, daily loss,
   leverage, liquidation distance, current positions — `docs/30:625-626`) pass. Any failure → terminal
   `REJECTED:<reason>`; nothing is executed partially-valid.
2. **2→3:** only `ACCEPTED → SUBMITTED` crosses into the exchange layer; from there only exchange
   observations move layer 3, through the docs/22 transition table. Restart/reconciliation authority —
   which component may re-create, cancel, replace, or flatten each owned order — belongs to the Bridge
   (`docs/30:879-880`; current custodian duties `docs/30:762-777`).
3. **3→lifecycle closure:** a lifecycle (and its legs) closes **only** from actual fills; partial-entry,
   partial-TP, partial-close, late-fill, and overfill behavior follows TS-P1-004 where it applies, and the
   Multi-TP partial behaviors remain OPEN (PSG-07) until the lifecycle contract amendment defines them.
4. **No layer copies another as fact.** Layer 1 never writes into layer 3; layer 2 never fabricates fills;
   layer 3 evidence never overwrites a layer-1 desired state — divergence stays visible (required
   dashboard fields: desired, accepted/rejected, acknowledged, partially filled, actually closed — kept
   visibly separate, `docs/30:883-884`).
5. **Window/liveness consistency (docs/21):** intent freshness (`expires_ts`) is wall-clock and internal
   to layers 1–2. It is *not* monitoring-window state: window state remains DERIVED from persisted
   evidence + the liveness staleness rule (`docs/21:26-42`) and is never carried in, or asserted by, an
   intent. A dead bridge can therefore never present an intent stream as an active window, and an intent
   never presents the window as alive.

## 6. Pine/Python parity gap register

Each sizing/lifecycle parity gap named by the cited `docs/30` ranges. RESOLVED = closed by contract text
in this pack (citation given). OPEN = preserved open; the closure column names the evidence or decision
that would close it. **Runs, edits, and wiring are NOT authorized here** — closure work is future,
separately gated (T2 decision records or T0 implementation packages per the backlog's tiers).

| ID | Gap | Evidence (verified at HEAD `b08aab35`) | Status | Closure requirement |
|---|---|---|---|---|
| PSG-01 | **Multiplier denominator**: Pine stop-risk qty divides by `stop_distance × contract_multiplier`; Python divides by stop distance only — different stop-risk quantities for any `contract_multiplier != 1`. | `MTC_V2.pine:351` vs `position_sizer.py:47` (multiplier present in Python's caps `position_sizer.py:52-55,66`); recorded `docs/30:492-504`. | **OPEN** | An accepted parity decision: fix one side (T0 code edit, separately gated) **or** an explicit bound declaring the contract valid only for `contract_multiplier = 1` instruments (`docs/30:512-517`) — which is what §3.7 provisional validation does. Gates appointing Python canonical (`docs/30:616-621`). Which side is correct is not decided here (`docs/30:517`). |
| PSG-02 | **Minimum-notional gate**: Python rejects to 0.0 below `min_notional`; Pine gates only minimum quantity — one side sizes where the other returns zero. | `position_sizer.py:66-68` vs `MTC_V2.pine:341,360-361`; recorded `docs/30:505-510`. | **OPEN** | Same form as PSG-01: fix a side (T0) or state `min_notional` semantics for both sides in an accepted bound (`docs/30:513-517`). Also gates Python-canonical appointment. |
| PSG-03 | **Multi-TP expressibility**: Bridge `OrderPlan` has one optional full-quantity `take_profit` and its bracket expects the same quantity for ENTRY/SL/TP — it cannot express MTC fractional TP1 + TP2 remainder. | `types.py:37-47` (single optional `take_profit`); recorded `docs/30:799-806`. | **RESOLVED (schema)** — §3.9 `tp_mode` + `tp_legs` (fractional `close_pct` + `is_remainder`) expresses it. | The **execution-model** extension (bracket legs of different quantities) remains future, separately-gated T0 — `docs/30:804-806` requires both schema *and* execution model extended and accepted before Multi-TP runs through the Bridge. Not authorized here. |
| PSG-04a | **Basket/add representation**: no current field distinguishes an add from a fresh entry or states delta-vs-total quantity. | `types.py:27-47` (no lifecycle fields); requirement `docs/30:704-713,870-871`. | **RESOLVED (representation)** — §3.10 `lifecycle_id` + `entry_seq` + `qty_semantics` + existing/target position context; add permission is `max_entries` (default 1), `pyramiding=100` is only a ceiling (`MTC_V2.pine:5-7,19`; `docs/30:527-536`). | — |
| PSG-04b | **Add emission policy and Pine↔Python add/basket parity**: one intent per add, or an intent describing the target basket; accepted parity of add/basket behavior (incl. `merge_pyramid_stop` tightening, `MTC_V2.pine:283-289`) does not exist. | Open per `docs/30:727-729`; umbrella item `docs/30:864-865`; no-accepted-parity statement `docs/30:788-790`. | **OPEN** | The accepted Pine↔Python lifecycle parity contract must bind the emission policy; schema supports both modes unambiguously until then (§3.10 note). |
| PSG-05 | **Native vs synthetic stop semantics**: whether the strategy stop is itself the continuously active native exchange stop, or MTC uses a synthetic/bar-evaluated exit with a separate emergency native safety stop (different fills possible vs backtest). | Options and consequence analysis `docs/30:808-820`; required field `docs/30:874-875`. | **OPEN** (choice) — §3.8 resolves only the *explicitness*: `stop_semantics` is a required per-intent field, no silent sharing or mixing. | Owner decision on the semantics + parity evidence produced for the chosen semantics (`docs/30:818-820`); emergency stop name/level/authority defined under the same decision. |
| PSG-06 | **Same-bar stop/target collision**: bar-evaluated simulation vs continuously active real exchange orders can resolve a same-bar stop-and-target collision differently. | `docs/30:876-877`. | **OPEN** | Falsification/parity evidence runs comparing simulated vs exchange-order collision resolution under the accepted stop semantics (PSG-05). Runs not authorized here. |
| PSG-07 | **Partial TP1 fill**: what happens when TP1 only partly fills (allocation of the remainder, leg cancellation, re-protection). | `docs/30:869,878`; existing TS-P1-004 partial protection covers entry partials in the single-TP model (`types.py:545-557` `PartialProtectionState`, transitions `types.py:595-619`, `docs/22` amendment), not TP1-partial under Multi-TP. | **OPEN** | Lifecycle-contract amendment defining TP1-partial behavior + regression/restart evidence before Multi-TP activation (`docs/30:885-886`). |
| PSG-08 | **Overall Pine↔Python lifecycle parity acceptance**: entry/exit, break-even, trail, TP, add/basket semantics — no accepted parity claim exists today. | `docs/30:864-865`; explicit no-claim statement `docs/30:788-790`. | **OPEN** (umbrella over PSG-04b/-05/-06/-07) | An accepted Pine↔Python strategy-lifecycle contract with regression, falsification, integration, restart, and exchange-adapter evidence (`docs/30:885-886`). |
| PSG-09 | **`wt_amount` alert parity**: MTC's live alert path sends a fixed input amount (default 100.0), not MTC's computed quantity — its own open integration question, distinct from the ownership conflict. | `MTC_V2.pine:183,2020`; recorded `docs/30:601-606,730-731`. | **OPEN** | Decision whether the MTC alert path should carry the computed quantity, and what that changes downstream (`docs/30:730-731`). Independent of §2; solving one does not solve the other (`docs/30:604-606`). |
| PSG-10 | **Risk-percent convention divergence**: MTC uses percent units (1.0 = 1%); Bridge uses fractions (0.005 = 0.5%). | `MTC_V2.pine:350`, `position_sizer.py:46` vs `risk.py:37`; recorded `docs/30:690-694`. | **RESOLVED (convention naming)** — §3.7 fixes the intent's scale as percent units (1.0 = 1%); the Bridge converts internally; raw cross-convention comparison is forbidden. | — |
| PSG-11a | **Envelope divergence handling**: MTC default sizing exceeds the Bridge's currently configured notional cap ($3,000 vs $2,000 in the cited illustration); a future validator would reject. | `risk.py:37,41`, `bridge.yaml:14,21`; illustration `docs/30:551-587`. | **RESOLVED (handling)** — §2.3: loud `REJECTED:NOTIONAL_CAP` (reject-on-mismatch preferred, `docs/30:641-642`); never silent resize/clamp (`docs/30:628-633`). | — |
| PSG-11b | **Envelope divergence values**: which defaults change (MTC risk %, Bridge `risk_pct_per_trade` / `max_position_notional_pct`, or both). | Same evidence as PSG-11a. | **OPEN** | Owner configuration decision at the future T0 gate; explicitly not decided here — this pack fixes only the handling rule. |

**Register totals: RESOLVED 4 (PSG-03, PSG-04a, PSG-10, PSG-11a) · OPEN 9 (PSG-01, PSG-02, PSG-04b,
PSG-05, PSG-06, PSG-07, PSG-08, PSG-09, PSG-11b).**

## 7. Explicit non-authorization

- **No implementation, wiring, or activation.** Nothing in this pack authorizes code, runtime wiring,
  configuration change, or any connection between MTC_V2 and the Bridge (`docs/30:735-738,888-890`).
- **No MTC, Pine, TradingView-parity, or strategy-logic edits.** Parity-gap closure requiring source
  changes (PSG-01, PSG-02, PSG-04b, PSG-05 implementations) is future, separately owner-gated T0.
- **No orders, broker/exchange contact, TESTNET/MAINNET, ARM, credentials, host/VPS action, or any
  economic action.** Standing prohibitions (frozen-V1 mutation included) apply in full; V1 remains
  untouched (`docs/30:420-449`).
- **No runs.** No parity run, backtest, falsification run, or exchange-adapter evidence gathering is
  authorized by this pack; the register only names what such evidence would close.
- **Precedence rule preserved:** this contract must exist and be accepted before the first
  MTC-connected worker (`docs/30:376-407`, backlog §3) — it is a precondition, not an enabler.

## 8. Self-verification

1. **Current-state claims cite path:lines** — §1 and the register's Evidence column cite files read
   directly at HEAD `b08aab35`: `bridge/engine/types.py:27-47,119-142,206-292,474-495,595-619`;
   `bridge/engine/risk.py:37-59,370-394`; `config/bridge.yaml:11,14,21,34`;
   `MTC_V2.pine:5-7,19,90-94,110,115-117,183,217-218,251-253,283-289,329-337,339-361,941-942,959,1125-1139,2020`;
   `position_sizer.py:17-70`. Design-direction claims cite `docs/30:<lines>` verified at the same HEAD.
2. **Accepted contracts not contradicted; tensions flagged, not overridden:**
   - `docs/23` (order identity): `intent_id`/`request_id` semantics, canonical encoding, reservation and
     finalization protocols are adopted as-is (§3.2, §5.1). **Flagged tension:** the `request-v1`
     canonical field list carries a single `take profit or null` (`docs/23:27-38`); Multi-TP intents need
     the leg set in the request identity. Resolution must come as a **new identity domain version**
     (e.g. `request-v2`) at the future T0 — this pack does not mutate `docs/23` semantics.
   - `docs/22` (order state): the actual layer reuses the canonical `OrderState` vocabulary and
     transition table unchanged (§5.1); no new order states invented; `UNKNOWN_SUBMISSION` semantics
     preserved.
   - `docs/21` (window state): no intent field asserts window/liveness; window state stays derived
     (§5.2.5).
3. **UNKNOWN/OPEN preserved:** PSG-01, PSG-02, PSG-04b, PSG-05, PSG-06, PSG-07, PSG-08, PSG-09, PSG-11b
   remain OPEN; the Python-canonical appointment remains gated (§2.2); the `account` value binding, the
   `strategy_id` value for the MTC wiring, and the `stop_semantics` value choice remain OPEN. Nothing in
   this pack converts an OPEN item into an implied resolution.
4. **No prohibited surface touched:** repositories read only; the only command executed in them was
   `git rev-parse HEAD` (explicitly permitted). The only file written is this pack
   (`C:\tmp\night\P2_MTC_INTEGRATION_CONTRACT_PACK.md`). No MTC/Pine/parity/strategy/config file was
   modified; no order, broker, exchange, host, credential, TESTNET/MAINNET, or ARM surface was contacted.
