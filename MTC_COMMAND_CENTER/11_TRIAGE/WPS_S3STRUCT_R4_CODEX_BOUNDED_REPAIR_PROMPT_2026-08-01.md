# S3-STRUCT ROUND 4 — BOUNDED REPAIR, OWNER-AUTHORISED (2026-08-01)

## 0. ROLE OVERRIDE — READ FIRST

**You are the IMPLEMENTER.** Claude `claude-opus-5` is Lead and acceptance authority; you are the
counterpart flagship implementer (`gpt-5.6-sol`, effort `xhigh`). Do **not** delegate to Claude Code
CLI or any other model — a delegation attempt returns `ConnectionRefused` and wastes the round.

**You cannot run Git.** `.git` is read-only for you. The Lead does every Git operation.

Workspace: `C:/WPS` — branch `feature/ts-p1-009b-s2-closure`, HEAD `dffbaf41`.

## 1. AUTHORISATION AND BOUNDS — READ BEFORE TOUCHING ANYTHING

The S3-STRUCT cycle hit its three-round bound and was stopped. **Barış has authorised exactly one
further round, scoped to round-3 R-1 and nothing else.**

This is **not** a general repair round. Both flagship auditors independently judged the boundary
design sound at `dffbaf41`, and neither could find an unrouted durable read of a registered column
on the queued-event reachable set. **Do not redesign, refactor, rename, or "improve" anything outside
§2 and §3.** Any change that is not required by §2 or §3 is a scope violation and will be rejected
even if it is an improvement.

Specifically **do not**: revert the `DurableRowFault(ValueError)` inheritance · alter
`DURABLE_EVENT_COLUMN_TYPES` or `DurableColumnContract` · touch the class-C join, the epoch fence,
`expected_identity`, or the `DEFERRED` containment · change the nullability declarations · address
any deferred nit (N-1/N-2/N-3, the `trades.sl_initial` / `tp_initial` registry gap, or the raw reads
in `record_kill_action_event`).

## 2. R-1 (THE ONLY DEFECT IN SCOPE) — `DISARMED` where the predecessor latched `KILLED`

Round 3 made `DurableRowFault` a `ValueError` subclass so the store-side conversion-fault contracts
would catch it. That was correct and stays. **The same change also handed the fault to the
pre-existing *engine-side* quantity-integrity handlers**, which were written for ordinary conversion
errors and downgrade containment.

Lead-verified on real source at `dffbaf41`:

- `orders.py:3375` — `except (InvalidOperation, TypeError, ValueError, OverflowError)` around
  `order_fill_totals`
- `orders.py:3444`, `:3495`, `:3569`, `:3674` — the same tuple plus `LotQuantizationError`, around
  `trade_fill_totals`, `trade_costs`, `_canonical_trade_close_values`, the entry-basis selection, and
  `_has_live_entry_remainder_exact`

Each calls `_quantity_integrity_fault` (`orders.py:3684-3695`), which sets
**`app_state = "DISARMED"`** — no `kill_latched`, no `record_durable_event_fault`.

At `216682ba` the fault was a `RuntimeError`, was **not** caught there, and reached the drain's
`except DurableRowFault` → `_contain_durable_row_fault` → `kill_latched = True`,
`app_state = "KILLED"`, ARM refuses. **At `dffbaf41`, `engine.arm()` succeeds after schema-admitted
corruption.** This is the first defect in the programme that fails **open**, which is why the round
was authorised.

Both flagships reproduced it independently — either reproduction is sufficient, and **both must
become tests**:

- *`claude-opus-5`* — ordinary ARMED operation, no kill latched, no active kill request. A durable
  ENTRY `fills` row of trade T has corrupt `qty` (TEXT `'not-a-number'`, or NULL). A **non-KILL** exit
  `FillEvent` (role `CLOSE`/`SL`/`TP`) for T is queued during broker I/O and drained.
  `order_fill_totals(fill.cloid)` covers only the exit order's own fills and passes;
  `trade_fill_totals(trade_id)` covers every fill of the trade, hits the corrupt row, raises — and
  lands in the `DISARMED` handler.
- *`gpt-5.6-sol`* — persist an older fill for cloid E with `qty='not-a-number'`, then queue a
  *different, new* `FillEvent` for E. `insert_fill` commits the new fill; `order_fill_totals` reads
  the older row and raises; the handler substitutes generic `ORDER_FILL_TOTAL_INVALID`, writes
  `DISARMED`, consumes the delivery, and returns without establishing the KILL latch.

**Aggravating, and also required:** `orders.py:3375` hardcodes `reason=ORDER_FILL_TOTAL_INVALID` with
no `getattr(exc, "reason_code", …)`. The stable `DURABLE_<TABLE>_<COLUMN>_<CASE>` code that S3T-A
requires is **destroyed, not relocated**. Preserve it wherever a durable-row fault is recorded.

### Required fix

A `DurableRowFault` reaching any of these handlers must be contained the way the drains contain it —
`kill_latched`, `app_state` durably `KILLED`, ARM refuses, ACK unreachable, `record_durable_event_fault`
with the fault's own stable reason code — **not** downgraded to `DISARMED` /
`FILL_QUANTITY_INTEGRITY`. An ordinary `ValueError` / `InvalidOperation` / `TypeError` /
`OverflowError` / `LotQuantizationError` from any other source must keep its **current** behaviour
exactly: those handlers still exist for real conversion errors and must not start killing on them.

**Pin the enumeration this time.** Round 3's completeness proof walked the `Store` call graph and
never crossed into `OrderManager` — that omission is why this defect shipped. Your enumeration
boundary for this round is explicit:

> **Every `except` clause in `bridge/engine/orders.py` that can catch a `ValueError` — whether by
> naming `ValueError`, a tuple containing it, `Exception`, or a bare `except` — and that sits on any
> path reachable from either queued-event drain or from a direct `_ingest_fill` caller.**

Enumerate that set exhaustively, state it in your report, and say for each entry whether it is
reachable from a boundary-routed read and how it now behaves. Include the broad
`except Exception: return str(raw_status)` fallback in `_canonical_status` in the enumeration —
decide whether it can swallow a durable-row fault and say so explicitly either way.

## 3. THE MATRIX MUST BE ABLE TO FAIL — non-negotiable

**The existing matrix cannot fail on this defect, and that is the deeper problem.**
`_s3_stranded_kill_restart` builds the engine with `state="KILLED"` and a live `kill_request_active`
pointer, so `BridgeEngine._app_state()` re-derives and re-persists `KILLED` on the next read. The
assertion `store.get_meta("app_state") == "KILLED"` therefore passes **regardless of which handler
ran**. Its evidence assertion also passes, because `_quantity_integrity_fault` embeds a reason code in
the event *detail*.

This is the second time in this cycle a generated matrix passed while proving nothing — round 2 hid a
defect behind `UPDATE trades SET entry_px=100.0`. **A test that cannot fail is not evidence.**

Required:

1. **Make the existing assertions discriminating.** Assert the containment **event code** is the
   fault's own `DURABLE_<TABLE>_<COLUMN>_<CASE>` — not merely that the code appears somewhere in a
   detail string, and not `FILL_QUANTITY_INTEGRITY`. Assert `kill_latched` directly rather than
   inferring it from a re-derived `app_state`.
2. **Add at least one generated corruption case whose fixture starts clean** — no kill latch, no
   active kill request, `app_state` not already `KILLED`, engine ARMED — so that
   `app_state == "KILLED"` is a real assertion rather than a restatement of the fixture. Assert
   `engine.arm()` **refuses** in that case; at `dffbaf41` it succeeds.
3. **Both auditor reproductions above become generated or parametrized cases**, not two hand-written
   one-offs.
4. **Prove the tests fail without the fix.** State in your report, for at least the two reproductions,
   what the assertion output is when the §2 change is reverted. If a new test passes at `dffbaf41`, it
   is not testing this defect.

## 4. UNCHANGED CONSTRAINTS

**Allowlist — exhaustive:**

```
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py
IBKR_PAPER_BRIDGE/tests/test_store.py
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
```

`bridge/engine/engine.py` is **not** allowed. Report a needed scope extension; never take one.

**Forbidden:** any `*.pine`, `MTC_V2`, `parity`, `01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS` path ·
`bridge/engine/strategies/**`, `config/strategies/**` · `bridge/api/routes.py` · `bridge/broker/**` ·
**any risk-threshold value** in `config/bridge.yaml` · any credential, wallet secret, API key, host,
IP or private path · **weakening, deleting, skipping or `xfail`-ing any existing test — grep your own
diff for `-` lines under `tests/` and list every one in your report** · any migration or schema
change · any broker, network, TESTNET, ARM or runtime action. DISARMED only.

`KILL_STALE_EVIDENCE_RECORD_FAILED` and genuine evidence-store write failures **still propagate**.

**Test contract** — from `C:/WPS/IBKR_PAPER_BRIDGE`:

```
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```

`--ignore` is mandatory. Never pass `--basetemp` inside `.pytest_cache`.

Floor at `dffbaf41`: **`2 failed, 1297 passed`** — the two pre-existing failures only (stale KVM2
ledger hash; `schema_version == "2"` against default v4). **Do not "fix" them.** A third failure is a
required finding. Run the full suite yourself before reporting.

## 5. REPORT FORMAT — end with exactly this

```
Handler enumeration : <every except-clause in orders.py catching ValueError on the reachable set;
                       for each: reachable from a boundary-routed read? how does it behave now?>
_canonical_status   : <can its broad `except Exception` swallow a durable-row fault? yes/no + why>
R-1 fix             : <how a DurableRowFault is now contained at those sites>
Ordinary faults     : <proof non-DurableRowFault conversion errors keep their exact prior behaviour>
Reason code kept    : <where exc.reason_code is now preserved, incl. orders.py:3375>
Matrix discriminating : <the new assertions; why they can now fail>
Clean-fixture case  : <the ARMED/no-latch case and its arm() refusal assertion>
Reproductions       : <both auditor scenarios, as generated/parametrized cases>
Fails without fix   : <literal assertion output for both when the §2 change is reverted>
files changed       : <exact list>
tests added         : <names>
existing tests touched : <every '-' line under tests/, with why>
suite output        : <the literal final pytest line>
scope extensions    : <none | what you needed and why you did NOT take it>
open risks          : <anything the Lead should probe first>
```

Begin. Implement in `C:/WPS`. No Git. No delegation. Nothing outside §2 and §3.
