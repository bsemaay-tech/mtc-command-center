# S3-STRUCT — ACCEPTED AND MERGED (2026-08-01)

**Supersedes `WPS_S3STRUCT_HARD_STOP_2026-08-01.md`**, which stopped the cycle at its three-round
bound. Barış then authorised one bounded round scoped to round-3 R-1 alone. That round closed it.

| | |
|---|---|
| Accepted artifact | `16cbc717` |
| Merge commit | `637307e8` on `origin/master` |
| Ancestry verified | `16cbc717` and the accepted S2 `0c65a731` are both ancestors of `origin/master` |
| Merge scope | 21 files, **all** under `IBKR_PAPER_BRIDGE/`, zero conflicts, zero non-Bridge paths |
| Suite on merged tree | `2 failed, 1304 passed` — the two pre-existing failures only |

**WP-S is closed. Audit 1 is accepted.** No broker, network, ARM, TESTNET, VPS or runtime action was
taken at any point in this cycle. DISARMED throughout.

## Acceptance evidence

| Auditor | Verdict | Suite | Worktree |
|---|---|---|---|
| `gpt-5.6-sol` xhigh | **PASS** — 0 required, 0 nits | `2 failed, 1304 passed in 126.21s` | clean, HEAD `16cbc717` |
| `claude-opus-5` xhigh | **PASS-WITH-NITS** — 0 required, 5 nits | `2 failed, 1304 passed in 108.49s` | clean, HEAD `16cbc717` |
| Lead independent | — | `2 failed, 1304 passed in 122.94s` | — |
| Lead on merged tree | — | `2 failed, 1304 passed in 132.92s` | — |

D025 acceptance rule satisfied: **both flagships accepting, no unresolved reproduced required finding
from any auditor.** Auditors 3 and 4 produced no verdict this cycle and are recorded as gaps in §5 —
under D025 rule 1 non-execution is never acceptance, and neither was counted as one.

## What was delivered

One registry-driven boundary over durable `orders`/`fills`/`trades` reads:

- `DURABLE_EVENT_COLUMN_TYPES` maps `(table, column)` → `DurableColumnContract(value_type, nullable)`
  — ten columns, the single declared source of truth. Both acceptance matrices generate their column
  dimension from it.
- `DurableRowAccessor` / `ValidatedDurableRow` validate on `__getitem__`, so a registered column
  cannot be read without passing the boundary. Store methods return the validated views, which is what
  makes a *new* consumer validated by default rather than requiring a new guard.
- Reached through **exactly 7 store-side wrap sites** (`db.py:7525, 7792, 7821, 9579, 9704, 9760,
  9784`) — greppable in one line.
- Both legacy per-site helpers (`_parse_store_trade_id`, `_store_float`) deleted; no competing
  validation path survives.
- `close_trade_once_with_decision` re-derives inside its existing `BEGIN IMMEDIATE` that the trade is
  still bound to the active episode (`role='KILL_FLATTEN'` + `group_id` + `trade_id`), as a conjunct
  added alongside the epoch fence, which is intact and unweakened.
- Accessor totality confirmed by both auditors against `bytes`, `memoryview`, `bool`,
  `Decimal('NaN')`, non-finite floats, subnormals, `-2**63` accepted / `+2**63` rejected.

**Both flagships state independently that no durable read of a registered column bypasses the
boundary on the queued-event reachable set.** That is the property three earlier rounds could never
establish. Suite grew 1140 → 1304 passing with the same two pre-existing failures throughout.

## The four rounds

| Round | SHA | Suite | Outcome |
|---|---|---:|---|
| 1 | `34d35286` | 2F / 1262P | REQUEST_CHANGES — S3T-B's own raise escaped through an empty `missing_identity` |
| 2 | `216682ba` | 2F / 1266P | REQUEST_CHANGES ×2 — nullable-by-design NULL treated as corruption · fault type escaped an existing conversion contract · `DEFERRED` reachable and escaping |
| 3 | `dffbaf41` | 2F / 1297P | REQUEST_CHANGES ×2 — the `ValueError` subclass downgraded containment to `DISARMED`; **hard stop at the round bound** |
| 4 | `16cbc717` | 2F / 1304P | **PASS / PASS-WITH-NITS** — owner-authorised bounded round |

Every finding was reproduced by the Lead on real source before it bound. Two of the Lead's own
round-1 candidates did **not** reproduce and were dropped rather than spent — that is D025 rule 2
working as intended.

## Lessons worth carrying — these cost the cycle three rounds

**1. A generated matrix can pass while proving nothing. Twice.** Round 2 hid a defect behind
`UPDATE trades SET entry_px=100.0`, masking the state *every* trade starts in, since `create_trade`
never writes `entry_px`. Round 3's fixture starts already `KILLED` with a live `kill_request_active`
pointer, so `assert app_state == "KILLED"` re-derives and restates the fixture rather than testing
anything. **Ask what would make the assertion fail.** Round 4 was the first round to prove it: the two
new corruption cases were re-run by the Lead against `dffbaf41` in an isolated worktree and both
failed with `Failed: DID NOT RAISE <class 'RuntimeError'>`, while the five ordinary-fault cases passed
there — proving they pin unchanged behaviour rather than the fix.

**2. "Prove the enumeration complete" needs its boundary named.** Round 3 was asked to enumerate every
affected caller and prove completeness. It walked the `Store` call graph and never entered
`OrderManager` — which is exactly where the defect lived. Round 4 pinned the set explicitly (*every*
`except` in `orders.py` catching a `ValueError` on the reachable set) and it held. Recorded as a Lead
error, not an implementer one.

**3. Publishing the Lead's reasoning is what let it be falsified.** The round-2 rationale claimed the
deferral predicate was strictly stronger than the close predicate, so `DEFERRED` was unreachable. Both
flagships broke it by different mechanisms — one snapshot-level, one showing that no snapshot argument
can hold across two transactions, since the close rolls back and returns before the deferral opens its
own. Stating the argument in the brief is why it was tested instead of trusted.

**4. Fail-open is a different severity class.** Round 3's defect was the first in the programme where
the artifact was *less* safe than its predecessor — `DISARMED` with ARM reachable, where `216682ba`
latched `KILLED`. Round 4's brief therefore led with the opposite risk (over-correction: killing on a
benign broker quirk would be a bridge that will not start), and both auditors verified ordinary
conversion faults kept their exact prior behaviour.

## Deferred to TS-P1-010 — recorded, not dropped

- **N-1 (coverage)** — four of the six new `except DurableRowFault` clauses are never executed by the
  suite (measured). The anti-downgrade property is proven at **2 of 6 sites**; the other four are
  byte-identical to the proven pair. Cheapest close: extend the clean-ARMED parametrization with a
  corrupt fill on a *sibling* cloid of the same trade, and a corrupt `fills.fee`/`funding` on the exit
  path.
- **The one real unrouted read** — `_recover_applied_kill_flatten_lifecycles`
  (`orders.py:1649, 1653`, and the unguarded `int(order["trade_id"])` at `1701`) and
  `_kill_query_flatten` (`1307-1311`) convert raw rows outside the boundary. At `1654` a fault would be
  caught by a `ValueError` tuple and downgraded to `_KillEvidenceFault(AMBIGUOUS)` — **the same shape
  as round-3 R-1**. Reachable only via `engine.kill()` → `_run_kill_episode`, **not** from a queued
  broker event or `BridgeEngine.start()`, so outside S3T-C's stated scope and outside round 4's
  authorisation.
- **N-3** — the `BridgeEngine.start()` leg is proved only by the matrix whose fixture starts `KILLED`.
  Re-basing that matrix on the clean-ARMED fixture is larger than a bounded round should carry.
- **N-4** — `_canonical_status`'s broad `except Exception: return str(raw_status)` is never exercised.
  Safe today (both auditors verified the registered reads precede the `try`), but it is the one
  construct in the reachable set that could downgrade a future registered read with nothing failing.
- **N-5** — the containment handlers at `orders.py:2727-2728` and `3002-3007` are never executed.
  Round-3 vintage, same family as N-1.
- Earlier deferred nits stand: int64 range check applied to `FINITE_FLOAT` columns · two reason codes
  for one storage-class fault · asymmetric TEXT policy between `INT64` and `FINITE_FLOAT` ·
  `trades.sl_initial` / `tp_initial` registry gap (`orders.py:3069-3071`, `:3186`) · raw reads in
  `record_kill_action_event` (`db.py:6162-6168`, `6665-6676`).

## Auditor roster — coverage actually obtained, and what needs owner action

| Auditor | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| `gpt-5.6-sol` xhigh | REQUEST_CHANGES | REQUEST_CHANGES | REQUEST_CHANGES | **PASS** |
| `claude-opus-5` xhigh | session limit, no verdict | REQUEST_CHANGES | REQUEST_CHANGES | **PASS-WITH-NITS** |
| `cline-pass/deepseek-v4-flash` | — | 2 failed dispatches | — | — |
| GLM-5.2 via `Invoke-GlmAudit.ps1` | — | **BLOCK** — `401 token expired or incorrect` | — | — |

**Owner action outstanding:** refresh `ZAI_GLM_CODING_PLAN_KEY` in Windows Credential Manager.
Auditor 4's route is `Invoke-GlmAudit.ps1` → `glm.ps1` → Z.AI and is **not** a Cline route; the
invocation ran and failed authentication after passing a live test earlier the same day. No credential
was read, set or duplicated by the Lead.

**Auditor 3 has now failed four dispatches across two cycles without producing a verdict** — two
timeouts last cycle, a non-TTY approval gate and a malformed provider stream this cycle. Budget it as
opportunistic, never as round-gating detection.

## What unblocks now

Plan §23b step 7 gated WP-L Phase 1 on Audit 1 accepting. That gate is now satisfied.

**WP-L Phase 1 is verification only.** Finding F-0-1 stands: the Linux package at `6fe0130f` is
already an ancestor of master and byte-identical, so nothing is ported and no cross-branch Git
operation occurs. It has not been started and needs its own go-ahead.

## Hours

Recorded against the owner-authorised extension beyond the plan's contingency line, per cycle handoff
§6 — **not** absorbed into the 5 h contingency, which stands at 2.0 h remaining. Four
implement-plus-audit rounds with seven flagship audits is materially past the ~6 h implementation
estimate the handoff asked to be flagged, and it was flagged before round 4 was authorised.
