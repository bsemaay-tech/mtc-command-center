# WP-S — MINIMUM S3: HARD STOP AFTER THE FINAL PERMITTED ROUND (2026-08-01)

**Status: STOPPED. The S3 repair loop is exhausted and `732b37c3` is NOT accepted.**
No fourth round has been started and none will be without a fresh explicit owner decision.

**Lead:** Claude `claude-opus-5`. **Implementer:** Codex CLI `gpt-5.6-sol` xhigh.
**Authorisation:** `11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md`.
Prior records: `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md`,
`WPS_TSP1009B_S2_CLOSURE_RECORD_2026-07-31.md`, `WPS_S3_AUDIT_ROUND2_BLOCKER_2026-07-31.md`.

## 1. Why this is a stop, not another round

On 2026-07-31 the owner was asked how the round bound applies, given that plan §25 defines Audit 1
as one checkpoint covering both S2 and minimum S3. **The owner chose the looser reading: S2's loop
had terminated successfully, so S3 is its own loop with one round remaining.** That round is
`732b37c3`. It is non-accepting. The loop is now spent under the owner's own chosen interpretation.

Additionally, under the roster expansion the owner authorised the same day (D025), acceptance
requires accepting verdicts from **both** flagship auditors. One has returned REQUEST_CHANGES.

## 2. Artifact chain

| Commit | Meaning | Suite |
|---|---|---|
| `678e8b94` | original blocked S2 artifact (entry floor) | 2F / 1113P |
| `d3a45529` | S2 round 1 — non-accepting | 2F / 1117P |
| **`0c65a731`** | **S2 round 2 — ACCEPTED, both flagships PASS-WITH-NITS, 0 required** | 2F / 1118P |
| `c26b00a4` | S3 round 1 — non-accepting, 6 required | 2F / 1125P |
| `e78eff59` | S3 round 2 — non-accepting, 1 required | 2F / 1131P |
| **`732b37c3`** | **S3 round 3 (final) — NON-ACCEPTING, 2 required** | 2F / 1140P |

Branch `feature/ts-p1-009b-s2-closure`, worktree `C:/WPS`, all pushed. Every suite figure
independently reproduced by the Lead; `732b37c3` also re-run by the auditor (`2 failed, 1140 passed`).

## 3. The two required findings — reproduced by the auditor, then verified by the Lead

Both are **executable reproductions on the frozen commit**, reached through a real
`BridgeEngine.start()` using only `UPDATE` statements the schema permits. No monkeypatching, no
injected failures. Per D025 rule 2 the Lead reproduced each on real source before treating it as
binding.

### R-1 — `bridge/store/db.py:7338-7339`: unguarded conversions in `insert_fill`, ahead of every round-3 guard

```python
existing = (
    str(row["fill_id"]), str(row["cloid"]), str(row["decision_uid"]), str(row["fill_ts"]),
    float(row["qty"]),          # unguarded
    float(row["px"]),           # unguarded
    float(row["fee"] or 0.0),   # guarded
    float(row["funding"] or 0.0),
)
```

`fills.qty REAL` / `px REAL` (`db.py:826-827`) are SQLite **affinity only** — no CHECK, no NOT NULL
— exactly the argument that made `orders.group_id` / `orders.trade_id` reachable in round 2. Both
non-numeric TEXT and NULL are schema-admitted.

| Durable state | Escape | queue depth | durable evidence |
|---|---|---|---|
| `fills.qty='abc'` | `ValueError` | 1 | **0** |
| `fills.qty=NULL` | `TypeError` | 1 | **0** |
| `fills.px=NULL` | `TypeError` | 1 | **0** |

```
start → order_manager.reconcile → sync_broker_state → drain_queued_events (orders.py:2902)
      → _ingest_queued_event (2829) → _ingest_event (3207) → _ingest_fill (3262)
      → store.insert_fill → db.py:7338  ValueError
```

The round-2 signature exactly: **startup failure with zero durable evidence.** A control probe with
the fill not queued is contained at depth 0, so this is reachable specifically through the queued
`FillEvent` drain — the path the whole round was scoped to close.

**Lead verification:** confirmed by direct source read. Round 3 guarded `order_fill_totals`,
`trade_fill_totals`, `orders.qty`, `trades.qty`, `trades.entry_px`, `trade_costs` and
`_canonical_trade_close_values` — but `insert_fill` executes *ahead of all of them* and re-reads the
durable row itself. The `or 0.0` present on `fee`/`funding` and absent on `qty`/`px` shows the NULL
case was considered for two columns and missed on the two that matter.

### R-2 — `bridge/engine/orders.py:2670`: the mandated `trade_id` repair was applied at two call sites, not at the entry point

```python
def _event_symbol(self, event: BrokerEvent) -> str | None:
    ...
    if isinstance(event, OrderUpdateEvent):
        ...
        trade = self.store.get_trade(int(order["trade_id"]))   # unguarded
```

`_parse_store_trade_id` was introduced this round (`orders.py:2687`) and applied at `2727` and
`3229` — **but not here**, and `_event_symbol` is called by *both* drains for *every* queued event,
before any guard runs.

Scenario: the same `orders.trade_id='not-an-integer'` row from round 3's own mandated repro; the
broker redelivers both the fill and an `OrderUpdateEvent` for that order — the ordinary case on
reconnect. The fill is contained correctly (`identity_evidence=1`), and then the sibling event
unwinds `start()` with `ValueError` at depth 2. **Containment of the fill is defeated by the event
queued beside it.**

Same class at `orders.py:2857-2859`: `float(order.get("filled_qty") or 0.0)` sits **outside** its
own `try`, so `orders.filled_qty='abc'` plus an `OrderUpdateEvent` escapes `start()` the same way.

**Lead verification:** confirmed by direct source read — `_parse_store_trade_id` exists and is used
at exactly two sites, neither of them `_event_symbol`.

### The auditor's escape-set enumeration

Asked the decisive question — *is the set of exceptions escaping the drain empty?* — the answer was
**no**. Of 14 schema-admitted corruptions probed across `orders`/`fills`/`trades`, **11 were
contained** with durable evidence at depth 0/1 and **3 escaped**, all R-1. `RuntimeError`,
`KeyError`, `LookupError` are genuinely closed. `KillConflictError` outside the allowlist still
propagates *by the Lead's declared decision* (§4 below).

## 4. The Lead decision that stands

`KILL_STALE_EVIDENCE_RECORD_FAILED` deliberately still propagates. It means the durable evidence
store itself cannot be written; no durable evidence can be recorded when the evidence store is the
failing component, so halting with `app_state` durably `KILLED` is the honest fail-closed outcome.
The canonical Codex auditor judged a contained operations state not required for *minimum* S3. This
was stated openly in the round-3 prompt so auditors would judge it rather than discover it. It is
**not** one of the two required findings.

## 5. Why three rounds failed — the structural diagnosis

This is the important part of this record.

Every S3 round closed the specific defect it was given and left the same *class* open somewhere
else:

| Round | Scoped to close | What it left open |
|---|---|---|
| 1 | the R1 startup-failure class | re-opened a reachable variant (F4), dropped an event (F3), relocated unbounded growth (F5) |
| 2 | identity shape validation | the store additionally required durable *binding*; `int()` ran before validation |
| 3 | identity parsing + durable binding + schema capability | `insert_fill` runs ahead of every guard; `_event_symbol` never got the parser |

The defect class has been identical every time: **schema-admitted data reaching an unguarded
conversion on the drain path, escaping through an unguarded `BridgeEngine.start()` with no durable
evidence.**

Each repair has been applied **point-by-point at the call sites the previous audit named**. That is
why each round closes the probed path and opens its neighbour — the repair strategy itself is the
problem, not the implementer's diligence.

**The auditor's own words: "Guard the entry point, not one line."** A structural fix would normalise
and validate every durable row once at the boundary — a typed accessor layer over `orders`, `fills`
and `trades` that either returns validated values or a containable fault — instead of guarding each
`float()`/`int()` as an auditor finds it. That is a larger change than "minimum S3", which is
precisely why it needs an owner decision rather than a fourth round of the same strategy.

## 6. What is accepted and safe right now

- **S2 closure is ACCEPTED at `0c65a731`** by both flagship auditors, zero required repairs. Both
  original blockers are genuinely closed: sub-1e-12 evidence tampering can no longer reach
  ACK/DISARM, and a superseded recovery can no longer commit a revoked lifecycle close.
- Everything on the branch is **DISARMED-only, test-only**. No runtime, broker, network, TESTNET or
  capital action has occurred at any point.
- The suite floor has held at every checkpoint: `2 failed, 1140 passed` at `732b37c3`, the two
  failures pre-existing and outside every allowlist.
- **The unfixed defects require a corrupted durable database to trigger.** They are startup-liveness
  faults on schema-admitted bad data — they do not create exposure, do not permit an unowned kill
  close, and do not weaken any accepted S2 evidence guarantee. The system fails *closed and stopped*,
  which is safe but not *available*.

## 7. Consequence for the programme

WP-L Phase 1 is gated on Audit 1 accepting (plan §23b step 7). **With S3 unaccepted, the entire
downstream chain — WP-L, WP-I, WP-A, Gate A, WP-V — is blocked.** There is no independent authorised
stream to continue in the meantime.

## 8. Options for the owner

1. **Authorise a new bounded cycle with a structural fix** — replace point-by-point guarding with a
   validated accessor boundary over durable rows. Larger than "minimum S3" and would need its own
   Gate-1 scope, but it is the only option that addresses why three rounds failed. *Lead
   recommendation.*
2. **Authorise one more narrow round** on exactly R-1 and R-2. Cheapest, but the last three rounds
   are direct evidence that point fixes on this surface reopen the class elsewhere.
3. **Descope minimum S3** — accept S2 at `0c65a731`, record S3 as deferred with these defects
   documented, and unblock WP-L. Weakens the liveness proof the plan asked S3 to establish; would
   need recording as a deliberate scope reduction against plan §16.
4. **Stop the programme here** and re-plan.

Under all options the accepted S2 artifact stays valid; nothing already accepted is invalidated by
this stop.

## 9. Hours, funding and spend — stated, not absorbed

| Activity | Budgeted | Actual |
|---|---|---:|
| WP-0 | 2 h | 2.0 h |
| WP-S S2 repair + Audit-1 first pass | 6 h | 6.0 h |
| WP-S S3 implementation + Gate-5 first pass | 6 h | 6.0 h |
| **WP-S subtotal** | **12 h** | **12.0 h — allocation fully consumed** |
| S3 round-2 and round-3 repairs | — | **3.0 h from CONTINGENCY** |
| All re-audits at checkpoint 1 | — | **3.5 h from WP-R** |

Funding follows §20/§22: repairs from contingency, re-audits from WP-R, never the reverse.
**Contingency 3.0 / 5 h. WP-R 3.5 / 6 h.** Both are hard ceilings; if either exhausts while a safety
requirement is unfunded, that is a BLOCK and an owner report.

Programme AI spend to date: **~$120**. Two Lead tooling defects account for roughly $35 of it, both
recorded rather than buried: a missing `-o` flag that made the dispatch wrapper re-run five complete
audits, and a 15-minute timeout that killed a DeepSeek audit mid-run.

## 10. Tooling notes worth keeping

- **A provider content filter can kill a canonical audit.** Codex's round-3 audit was terminated
  mid-run by `This content was flagged for possible cybersecurity risk` — triggered by the
  crash-simulation probe script *Codex itself wrote*, not by the prompt. Fixed by reframing the
  prompt as routine internal review and instructing the auditor to verify through the existing
  `pytest` suite rather than throwaway failure-simulation scripts. **The dispatch wrapper cannot
  distinguish a deterministic refusal from a transient loss** — it retried, and was stopped manually
  after one wasted attempt.
- **DeepSeek V4 Flash is genuinely reachable** as canonical auditor 3 (D025) — a direct probe
  returned `PROBE_OK`. Its first audit attempt failed only on a Lead-set 15-minute timeout; a full
  audit of this surface needs ~40+ minutes.
- **GLM-5.2's route is unconfirmed on this machine.** Under D025 rule 1 its absence is recorded as a
  gap, never treated as acceptance.

## 11. Safety statement

No implementation outside the frozen allowlist. No risk threshold invented or changed. No
credential, wallet secret, API key, host, IP, or private path written or sent to any model. Default
schema target remains v4; no migration added or executed. No Pine, parity, MTC strategy, or
protected-scope file touched. No bridge start against a real broker, no network, staging, Ubuntu
execution, VPS, deployment, TESTNET, ARM, or live-capital action occurred. Every audit worktree was
verified clean with unchanged HEAD afterwards, so no auditor edited the artifact it judged.
