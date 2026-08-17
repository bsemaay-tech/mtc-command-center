# S3-STRUCT — HARD STOP AT THE ROUND BOUND (2026-08-01)

**The cycle did not reach acceptance. Three non-accepting rounds are spent. No fourth round was
started.** Per `AGENTS.md` §Repair loop bound and the cycle handoff §6, the Lead stops here and
reports to the owner.

**Nothing is merged. Nothing is deployed. No broker, network, ARM, TESTNET or runtime action was
taken at any point in this cycle.** Branch `feature/ts-p1-009b-s2-closure` sits at `dffbaf41`,
pushed. `origin/master` is untouched at `2ebb0475`.

---

## 1. The one-line summary

A single registry-driven accessor boundary was built and both flagship auditors judged it sound —
**it is not a fourth point fix, and no unrouted durable read of a registered column survives on the
queued-event reachable set.** The cycle failed on *containment semantics at the boundary's edges*,
three times, and the final round's own repair introduced the first defect in the whole programme
that fails **open** rather than closed.

## 2. Round-by-round

| Round | SHA | Suite (Lead-verified) | Verdict | Finding |
|---|---|---|---:|---|
| 1 | `34d35286` | 2F / 1262P | REQUEST_CHANGES (`gpt-5.6-sol`) | S3T-B's own raise escaped through an empty `missing_identity` |
| 2 | `216682ba` | 2F / 1266P | REQUEST_CHANGES (**both** flagships) | R-1 nullable-by-design NULL treated as corruption · R-2 fault type escaped an existing conversion contract · R-3 `DEFERRED` reachable and escaping |
| 3 | `dffbaf41` | 2F / 1297P | REQUEST_CHANGES (**both** flagships, same defect, independent reproductions) | the `ValueError` subclass hands the fault to pre-existing quantity-integrity handlers → `DISARMED`, not `KILLED` |

Every round: suite clean at the floor, no third failure, no weakened test, allowlist exact,
`engine.py` untouched, every audit worktree verified clean with `HEAD` unchanged. Every finding was
reproduced by the Lead on real source before it bound; two of the Lead's own round-1 candidates did
**not** reproduce and were dropped rather than spent.

## 3. The blocking defect — round 3 R-1

**Both flagships found it independently, by different reproductions, and named the same root cause.**

Round 3 changed `DurableRowFault` from a `RuntimeError` to a **`ValueError` subclass** so that the
store-side conversion-fault contracts would catch it (that was round 2's R-2, correctly fixed). The
same change hands the fault to the **pre-existing engine-side quantity-integrity handlers**, which
were written for ordinary conversion errors:

- `orders.py:3375` — `except (InvalidOperation, TypeError, ValueError, OverflowError)` around
  `order_fill_totals`
- `orders.py:3444`, `:3495`, `:3569`, `:3674` — the same tuple plus `LotQuantizationError` around
  `trade_fill_totals`, `trade_costs`, and the entry-basis selection

All of them call `_quantity_integrity_fault` (`orders.py:3684-3695`), which sets
**`app_state = "DISARMED"`** — not `KILLED`, no `kill_latched`, no `record_durable_event_fault`.

At `216682ba` the fault was a `RuntimeError`, was not caught there, and reached the drain's
`except DurableRowFault` → `kill_latched = True`, `app_state = "KILLED"`, ARM refuses. **At
`dffbaf41`, `engine.arm()` succeeds after schema-admitted corruption.**

Reproductions (either is sufficient):

- *`claude-opus-5`* — ordinary ARMED operation, no kill latched. A durable ENTRY `fills` row of trade
  T has corrupt `qty`. A non-KILL exit fill for T is queued and drained. `order_fill_totals` covers
  only the exit order's fills and passes; `trade_fill_totals` covers every fill of the trade, hits
  the corrupt row, raises — and lands in the `DISARMED` handler.
- *`gpt-5.6-sol`* — persist an older fill for cloid E with `qty='not-a-number'`, queue a different new
  `FillEvent` for E. `insert_fill` commits the new fill; `order_fill_totals` reads the older row and
  raises; the handler substitutes generic `ORDER_FILL_TOTAL_INVALID`, writes `DISARMED`, consumes the
  delivery, and returns without establishing the KILL latch.

**Aggravating:** `orders.py:3375` hardcodes `reason=ORDER_FILL_TOTAL_INVALID` with no
`getattr(exc, "reason_code", …)`, so the stable `DURABLE_<TABLE>_<COLUMN>_<CASE>` code that S3T-A
requires is **destroyed, not relocated**.

This violates S3T-D(3) — `app_state` durably `KILLED`, ARM refuses — and contradicts
`docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md` line 218.

### Why the matrix passed anyway — the most important lesson of the cycle

`_s3_stranded_kill_restart` builds the engine with `state="KILLED"` and a live `kill_request_active`
pointer, so `BridgeEngine._app_state()` unconditionally re-derives and re-persists `KILLED` on the
next read. The matrix's `assert store.get_meta("app_state") == "KILLED"` therefore **passes no matter
which handler ran** — it is non-discriminating for exactly the columns this defect affects. Its
evidence assertion also passes, because `_quantity_integrity_fault` embeds a reason code in the event
*detail*.

**That is the second time in this cycle that a green matrix proved nothing.** The first was round 2's
`UPDATE trades SET entry_px=100.0`, which masked a state every trade starts in. A generated matrix
that asserts a property the fixture already guarantees is not evidence, and this cycle produced two
of them.

### Root cause of the miss

Round 3's prompt required the affected callers be *"enumerated and proven complete, not sampled."*
The implementer enumerated the **`Store`** call graph (`_public_store_apis_reaching`) and did not
cross into the **`OrderManager`** ingest path. The requirement was right; its boundary was never
pinned, and the Lead did not pin it. **That is a Lead error, recorded as such.**

## 4. What the cycle did achieve — do not rebuild this

Both flagships state this independently at `dffbaf41`:

- **One boundary.** `DurableRowAccessor` / `ValidatedDurableRow` / `DURABLE_EVENT_ROWS` over the
  declared `DURABLE_EVENT_COLUMN_TYPES` registry, routed by store methods returning lazy validated
  row views, so a *new* consumer of an existing typed row is validated by default. Both legacy
  helpers (`_parse_store_trade_id`, `_store_float`) deleted — no competing path survives.
- **No unrouted durable read of a registered column survives on the queued-event reachable set.**
  Both auditors walked it explicitly from both drains and found none. This is the thing three prior
  rounds could never achieve.
- **`DurableColumnContract(value_type, nullable)`** extends the registry along the right axis, and
  `gpt-5.6-sol` verified **all ten** nullability declarations against their actual writers — the
  Lead's designated highest-value check, because a wrongly-nullable column would fail open.
- **Boundary totality** confirmed against bytes, `memoryview`, `bool`, `Decimal('NaN')`, non-finite
  floats, subnormals, `-2**63` accepted / `+2**63` rejected.
- **Class C intact and correct.** Epoch assertion plus both `kill_requests` and role/`group_id`/
  `trade_id` `orders` predicates inside one `BEGIN IMMEDIATE`; binding failure rolls back, records
  evidence, leaves the trade open.
- **`DEFERRED` contained**, both direct callers translate to `UNKNOWN`, evidence-store failures still
  propagate.
- Suite grew 1140 → 1297 passing with the same two pre-existing failures throughout.

**R-1 is a routing regression inside a sound boundary, not a design objection.** Both auditors said
so in those terms.

## 5. Safety position right now

- `dffbaf41` **must not merge.** It is the only artifact in the cycle that is *less* safe than its
  predecessor on a reachable path: schema-admitted corruption lands `DISARMED` with ARM reachable,
  where `216682ba` landed `KILLED` with ARM refused.
- `216682ba` must not merge either — it carries round 2's three findings.
- **S2 remains ACCEPTED at `0c65a731` and is entirely unaffected.** All three S3 rounds are unmerged
  work on a feature branch.
- The unfixed defects still require a corrupted durable database to trigger. They are startup and
  ingest-path faults. Nothing here creates exposure, an unowned kill close, or a weakened S2
  guarantee.

## 6. Auditor roster — coverage actually obtained

| Auditor | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| `gpt-5.6-sol` xhigh | REQUEST_CHANGES, suite run | REQUEST_CHANGES, suite run | REQUEST_CHANGES, suite run |
| `claude-opus-5` xhigh | **session limit, no verdict** | REQUEST_CHANGES, suite run | REQUEST_CHANGES, suite run |
| `cline-pass/deepseek-v4-flash` | not dispatched (round already settled) | **2 failed dispatches, no verdict** | not dispatched |
| GLM-5.2 via `Invoke-GlmAudit.ps1` | not dispatched | **BLOCK — 401 token expired or incorrect** | not dispatched |

**Auditor 4 needs owner action:** refresh `ZAI_GLM_CODING_PLAN_KEY` in Windows Credential Manager.
The route itself is correct and is **not** a Cline route — `Invoke-GlmAudit.ps1` → `glm.ps1` → Z.AI.
The invocation ran and failed authentication after passing a live test earlier the same day. No
credential was read, set, or duplicated by the Lead.

**Auditor 3 has now failed four dispatches across two cycles without ever producing a verdict** —
two timeouts last cycle, a non-TTY approval gate and a malformed provider stream this cycle.
Budget it as opportunistic, never as round-gating detection.

Acceptance was never in doubt on roster grounds: it requires **both flagships accepting**, and both
returned `REQUEST_CHANGES` in the final round.

## 7. Recommendation to the owner — the decision is yours

**Recommended: authorise one bounded round scoped to round-3 R-1 alone.**

Rationale: R-1 is a **routing fix, not design work**. The boundary, the registry, the nullability
contract, the class-C join and the `DEFERRED` containment are all accepted by both flagships. The
repair is: route `DurableRowFault` to `_contain_durable_row_fault` ahead of the pre-existing
`ValueError` tuples at the five named ingest sites, preserve `exc.reason_code` at `orders.py:3375`,
and — non-negotiably — **make the matrix discriminating**, because the current one cannot fail on
this defect. That means asserting the containment *event code* is `DURABLE_*` rather than
`FILL_QUANTITY_INTEGRITY`, and adding at least one corruption case whose fixture has **no** kill
latch and is not already `KILLED`.

Two alternatives, stated honestly:

- **Stop and bank nothing.** Leaves WP-S blocked and every downstream package blocked with it, since
  plan §23b step 7 gates WP-L Phase 1 on Audit 1 accepting. Costs everything spent so far.
- **Reconsider the `ValueError` inheritance instead.** Reverting to a distinct exception type fixes
  the engine-side downgrade but re-opens round 2's R-2 at the store-side callers. That is a real
  trade, not a free one — the two constraints genuinely conflict, and the correct resolution is
  probably an explicit `except DurableRowFault: raise` guard at each site rather than leaning on the
  type hierarchy to be correct everywhere at once.

**Hours** are recorded against the owner-authorised extension beyond the plan's contingency line, per
cycle handoff §6 — not absorbed into the 5 h contingency, which stands at 2.0 h remaining. The cycle
handoff said to flag it if implementation looked like exceeding ~6 h: **it has.** Three full
implement-plus-audit rounds with four flagship audits is materially past that estimate, and a fourth
round should be authorised with that known, not assumed.
