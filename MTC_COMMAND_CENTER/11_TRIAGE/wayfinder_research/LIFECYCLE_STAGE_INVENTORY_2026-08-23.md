# Lifecycle / Promotion / State Inventory — Today vs Planned (2026-08-23)

> **Scope note.** This is a macro-level architecture inventory for GitHub issue #55
> ("Research: lifecycle stages and states as they exist today"), not a line-by-line
> code audit. Each concept below was read far enough to characterize its shape,
> writer, and consumer — not traced call-by-call. Read-only research; no repository
> state was modified.

**Sources read**

1. `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`
2. `MTC_COMMAND_CENTER/05_REGISTRY/*.json` (20 files, listed in full below)
3. `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md`
4. `IBKR_PAPER_BRIDGE/bridge/engine/{types.py,window.py,engine.py,orders.py}`,
   `IBKR_PAPER_BRIDGE/bridge/api/routes.py`, `IBKR_PAPER_BRIDGE/bridge/store/db.py`
5. Frozen planning doc, read via
   `git show 764da27f:MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`
   — `§6.3` (21-step lifecycle), `§6.4` (four forward environments), `§6.5`
   (eligibility states), `§6.7` (identity/hash model), `§6.8` (fast-screen vs
   slow-battery split).

---

## 1. The planned lifecycle, for reference (§6.3 / §6.5)

**21 steps (§6.3):** 1 Discovery → 2 Source-rule extraction+provenance → 3
`SOURCE_LITERAL` definition + Missing-Rule Ledger → (branch) 3a `SIGNAL_EDGE`
evaluation → 4 Data quality + leakage checks → 5 `SOURCE_COMPLETED_BASELINE` → 6
`MTC_ENRICHED` (optional modules) → 7 FREEZE `package_hash` → 7b MINT
`deployment_identity_hash` → 8 `FORWARD_SHADOW` → 9 Optimization (trial identities
only) → 10 Walk-forward + lockbox → 11 Buy-and-hold + excess alpha → 12 DSR≥0.95 +
BH-FDR → 13 CPCV/PBO/parameter stability → 14 A/B (signal vs baseline vs enriched)
→ 14b FREEZE selected optimized package → 14b-ii MINT its
`deployment_identity_hash` → 14c `FORWARD_SHADOW` on new composite → 15
`TESTNET_PAPER_ELIGIBLE?` → 16 `EXCHANGE_TESTNET` execution fleet → 17
Multi-strategy portfolio test → 18 `LIVE_CANDIDATE` → 19 Signed live gate (owner,
14 preconditions) → 20 `LIMITED_LIVE` (≤1% capital) → 21 Scale up / suspend /
retire.

**Eligibility states (§6.5):** `SHADOW_ELIGIBLE` → `TESTNET_PAPER_ELIGIBLE` →
`LIVE_CANDIDATE` → `LIMITED_LIVE_APPROVED`, each gated by named falsifiable
checks (deterministic replay, lookahead, repaint, data quality, basic-failure
floor, unsimulated controls) with `PASS/FAIL/BLOCKED` verdicts bound to a
`deployment_identity_hash`.

**§6.4 four forward environments:** `FORWARD_SHADOW` (zero orders) →
`INTERNAL_PAPER` (`MockBroker`, carried by `WP-V2B-07`, **not yet run or
authorized**) → `EXCHANGE_TESTNET` (real order lifecycle, no real money, also
`WP-V2B-07`, **not yet run or authorized**) → `LIMITED_LIVE` (real fills, tiny
capital).

**§6.8:** the plan explicitly compresses discovery into a "fast screen (hours)"
(`SOURCE_LITERAL`/`SIGNAL_EDGE` → data/leakage → buy-and-hold →
`SHADOW_ELIGIBLE`) followed by a "slow battery (days, batched overnight)"
(optimization → WF/lockbox → DSR/BH-FDR → CPCV/PBO → A/B → `LIVE_CANDIDATE`),
freezing the baseline package **before** the slow battery runs so its forward
clock starts early. This section is the plan's own acknowledgment that today's
process is being deliberately restructured, not merely renamed.

---

## 2. Concept-by-concept inventory

### 2.1 QuantLens candidate classification labels (§6 of the backtest rules doc)

- **Name:** `TRUE_ALPHA_CANDIDATE`, `BENCHMARK_BEATER`, `BETA_DISGUISED_AS_ALPHA`,
  `REGIME_SPECIFIC_EDGE`, `OVERFIT_SUSPECT`, `STATISTICALLY_UNCONFIRMED`,
  `INSUFFICIENT_TRADES`, `NO_DATA`, `REJECTED` (9 labels).
- **Where recorded:** defined in
  `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`
  §6; applied inside ad-hoc overnight Markdown reports
  (`05_BACKTEST_RESULTS/MORNING_REPORT.md`, `CLAUDE_AUDIT_FINDINGS.md`,
  `alpha_summary.json` — see doc Appendix C) and per-strategy
  `PROMOTION_PACKET.md` files under `03_QUANTLENS/strategies/<id>/`. No single
  registry column holds these 9 exact label strings.
- **Who writes it:** an AI agent (Claude/Codex) running the standard workflow,
  per doc §2 step 11 ("Classify each candidate"). Manual/LLM judgment applied
  against the doc's quantitative gates — not a script that mechanically emits
  the label.
- **Planned §6.3/§6.5 slot:** **No equivalent.** The plan's checks
  (deterministic replay, lookahead, repaint, data quality, basic-failure floor)
  are binary PASS/FAIL/BLOCKED verdicts on a candidate's *evaluation
  mechanics*; none of them classify *why* a candidate is interesting the way
  `BETA_DISGUISED_AS_ALPHA` or `REGIME_SPECIFIC_EDGE` do. `REJECTED` is the one
  label with a rough analog — the plan's DEC1 branch ("Signal carries
  information? no → REJECTED - research note").

### 2.2 QuantLens promotion levels (§9 of the backtest rules doc)

- **Name:** `REJECTED` → `KEEP_AS_RESEARCH_NOTE` → `PROMOTE_TO_SANDBOX` →
  `PROMOTE_TO_FORWARD_PAPER_TRADE` → `MTC_ENGINE_VALIDATED` →
  `PROMOTE_TO_PARITY_CANDIDATE` → `APPROVED_FOR_MTC_V2_INTEGRATION` (7 stages,
  linear).
- **Where recorded:** doc §9 defines them. Actually **populated** at
  `MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json`, field
  `strategies[].current_status` (e.g. `STG001` carries
  `"PROMOTE_TO_FORWARD_PAPER_TRADE|PROMOTE_TO_PARITY_CANDIDATE"`), and echoed in
  per-strategy `03_QUANTLENS/strategies/<id>/PROMOTION_PACKET.md` and
  `03_QUANTLENS/06_PROMOTED_TO_PARITY/PROMOTION_INDEX.md`.
- **Who writes it:** `STRATEGY_RESEARCH_REGISTRY.json` is machine-generated by
  `03_QUANTLENS/tools/build_strategy_research_registry.py` from source
  `producer_spec.json` / `01_candidate_metadata.yaml` files (per
  `STRATEGY_RESEARCH_WORKFLOW.md` "Hard rules" — edit the source, regenerate,
  never hand-edit). The underlying classification decision is still a human/AI
  judgment call baked into the source metadata; the registry step is
  mechanical.
- **Planned §6.3/§6.5 slot:** **Partial / contradiction.** `PROMOTE_TO_SANDBOX`
  and `PROMOTE_TO_FORWARD_PAPER_TRADE` roughly span what the plan splits into
  `SHADOW_ELIGIBLE` (step 8, zero orders) and the not-yet-authorized
  `INTERNAL_PAPER` lane (§6.4). `MTC_ENGINE_VALIDATED` has no named planned
  counterpart at all. `APPROVED_FOR_MTC_V2_INTEGRATION` is the rough analog of
  reaching step 19/20 (`LIMITED_LIVE_APPROVED`), but the plan requires a signed
  14-precondition gate bound to an exact `deployment_identity_hash` (§6.7);
  today's promotion string carries no hash binding at all. See Contradictions
  §3.1.

### 2.3 `PROMOTION_REGISTRY.json` — the unused promotion registry (audit F-6)

- **Name/path:** `MTC_COMMAND_CENTER/05_REGISTRY/PROMOTION_REGISTRY.json`.
- **Schema:** `{"schema_version": "1.0", "promotions": []}` — 50 bytes, empty
  array, no populated records, no field-level schema beyond the empty list
  (i.e. no `status`/`stage`/`promoted_at`/`tier` fields ever got instantiated
  because no row was ever written).
- **Evidence it has never been used:**
  - `git log --oneline -- MTC_COMMAND_CENTER/05_REGISTRY/PROMOTION_REGISTRY.json`
    returns exactly **one** commit (`77a10e65`, "init: migrated from
    tradingview-lab archive 2026-05-31") — the file has never been touched
    since the repo's initial migration.
  - `grep -r "PROMOTION_REGISTRY"` across the repo returns zero hits in any
    `.py`, `.md`, or dashboard-reader file that treats it as a path to read or
    write — the only matches are unrelated SHA-manifest CSVs and a couple of
    inventory docs that merely *list* the filename as existing.
  - The actual promotion state (§2.2 above) is written to a **different**
    file, `STRATEGY_RESEARCH_REGISTRY.json`, via a **different** generator
    script and a **different** field name (`current_status`, not
    `promotions`).
- **Who writes it:** nobody, currently. No script references its path.
- **Planned §6.3/§6.5 slot:** **No direct slot**, but the plan's "promotion
  decision artifact" (§6.7, stamped with `package_hash`, `evaluation_run_hash`,
  `deployment_identity_hash`) is conceptually the successor this file's name
  implies it should have become — the plan reinvents a promotion-record concept
  from scratch rather than building on this file.

### 2.3b `STRATEGY_REGISTRY.json` — a second empty/orphaned registry (secondary finding, not F-6)

- **Path:** `MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_REGISTRY.json`.
- **Schema:** `{"schema_version": "1.0", "generated_at": ..., "candidates": []}`
  — 97 bytes, empty array.
- **Evidence:** also exactly one commit (`77a10e65`, the same init migration).
  Distinct from `STRATEGY_RESEARCH_REGISTRY.json` (which is populated and
  actively regenerated — 2 commits, 133 KB, real records). The near-identical
  name to the actively-used registry is itself a source of confusion worth
  flagging alongside F-6.

### 2.4 `05_REGISTRY/` full directory listing (20 files)

| File | Size | Commits | Populated? |
|---|---|---|---|
| `AI_QUANTLENS_VERDICT_REGISTRY.json` | 222 KB | 1 | Yes — "expert commentary," own decision vocabulary (`NEEDS_CLARIFICATION`, `RESEARCH_ONLY`, ...), explicitly labeled "Opinion/labels only; no numeric score. **The Scorecard remains the only scoring authority**" (a 4th, external classification authority referenced but not located in this pass) |
| `AI_STRATEGY_NAME_REGISTRY.json` | — | — | not read in depth (naming only, not lifecycle) |
| `AI_TASKS.json` | — | — | not read in depth (task queue, not lifecycle) |
| `AI_WORKER_REGISTRY.json` | — | — | not read in depth |
| `CASE_REGISTRY.json` | — | — | not read in depth |
| `COMPONENT_REGISTRY.json` | — | — | referenced by `STRATEGY_RESEARCH_WORKFLOW.md` step 3, component taxonomy |
| `DATA_SOURCE_REGISTRY.json` | — | — | not read in depth |
| `INDICATOR_REGISTRY.json` | — | — | referenced by workflow step 3 |
| `MTC_V2_INDICATOR_INVENTORY.md` | — | — | Markdown, not JSON |
| `PROMOTION_REGISTRY.json` | 50 B | **1** | **No — see §2.3, audit F-6** |
| `RESEARCH_BACKTEST_REGISTRY.json` | — | — | referenced by workflow step 14 |
| `RESEARCH_RUN_REGISTRY.json` | 4.7 KB | 6 | Yes — actively regenerated, run-level index |
| `STRATEGY_PARAM_SPECS.json` | — | — | not read in depth |
| `STRATEGY_PARAM_SPEC_ANNOTATIONS.json` | — | — | not read in depth |
| `STRATEGY_REGISTRY.json` | 97 B | **1** | **No — see §2.3b** |
| `STRATEGY_RESEARCH_REGISTRY.json` | 133 KB | 2 | Yes — carries `current_status` promotion string, read by dashboard `research_reader.py` |
| `TAG_DICTIONARY.json` | — | — | referenced by workflow step 3 |
| `TRIAGE_CANDIDATE_REGISTRY.json` | 129 KB | 2 | Yes — populated |
| `TW_EXPORT_REGISTRY.json` | — | — | not read in depth |
| `VARIANT_LOG_REGISTRY.json` | 11 KB | 7 | Yes — actively appended per workflow step 8 |

### 2.5 `STRATEGY_RESEARCH_WORKFLOW.md` — the ~16-step research process

- **Steps (paraphrased):** 1 read AI-memory + registries → 2 select components
  by tags → 3 define hypothesis → 4 choose architecture family (4 named
  families) → 5 design backtest → 6 run baseline tests → 7 create variants → 8
  log every variant to `VARIANT_LOG_REGISTRY.json` → 9 reject weak variants
  (recorded reason) → 10 anti-overfitting checks → 11 code-safety review → 12
  write final report → 13 save run under
  `03_QUANTLENS/research/<research_run_id>/` → 14 register run in
  `RESEARCH_RUN_REGISTRY.json` + `RESEARCH_BACKTEST_REGISTRY.json` → 15 confirm
  visible in dashboard "Strategy Research Lab" tab → 16 update
  `_AI_MEMORY/GLOBAL_HANDOFF.md` / `NEXT_STEPS.md`.
- **Where recorded:**
  `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md`.
- **Who performs each step:** almost entirely an AI agent acting autonomously
  end-to-end (steps 1–14, 16); step 15 is a human-facing checkpoint (confirm
  the dashboard shows the run) but nothing in the doc requires a human
  sign-off to proceed past it.
- **Planned §6.3/§6.5 slot:** **Partial, structurally different.** Steps 1–12
  loosely span the plan's steps 1–14 (Discovery through A/B), but this
  workflow has **no freeze/mint discipline at all** — no `package_hash`, no
  `deployment_identity_hash`, no `SOURCE_LITERAL`/`SIGNAL_EDGE` vocabulary, and
  no environment separation (`FORWARD_SHADOW` vs `INTERNAL_PAPER` vs
  `EXCHANGE_TESTNET`). The workflow terminates at "final report + registry
  entry + dashboard visibility" — it has no forward-testing or live-promotion
  steps whatsoever (plan steps 15–21 have no equivalent here).

### 2.6 Bridge `app_state` — ARMED / DISARMED / KILLED

- **States:** `ARMED`, `DISARMED`, `KILLED` (3 states, `DISARMED` is the
  hard-coded startup default and a sticky fail-safe target).
- **Where defined/written:** no single `Enum` — string literals used directly
  across `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` (the owning state machine,
  e.g. `_set_state`, `_app_state`, lines ~63, 115–125, 359–410, 1080–1125),
  `IBKR_PAPER_BRIDGE/bridge/api/routes.py` (HTTP arm/disarm/kill endpoints,
  lines ~22–132, 237), `IBKR_PAPER_BRIDGE/bridge/engine/window.py` (reads it to
  compute soak-window state), `IBKR_PAPER_BRIDGE/bridge/engine/orders.py`
  (reads it as an order-submission gate, lines ~226–227, 317–319). Persisted in
  `IBKR_PAPER_BRIDGE/bridge/store/db.py` `meta` table, key `app_state`.
- **Who writes it:** the bridge engine itself (`Engine._set_state`), triggered
  by owner HTTP calls to `/arm`, `/disarm`, `/kill` (routes.py), and by the
  engine's own fail-safe paths (any error/uncertainty collapses to
  `DISARMED`).
  Read by: order submission gates (`orders.py`), the monitoring-window
  calculator (`window.py`), and the dashboard status endpoint (`routes.py`
  `/status`).
- **Planned §6.3/§6.5 slot:** **No named equivalent.** This is an
  operational safety interlock for whichever environment is currently running
  (today: paper/mock execution against Hyperliquid), not a lifecycle/promotion
  state. It sits *inside* the §6.4 environments (`INTERNAL_PAPER`/
  `EXCHANGE_TESTNET`/`LIMITED_LIVE`) without being named by the plan at all.

### 2.7 Bridge `WindowState` — RUNNING / DOWN / INTERRUPTED / RESET

- **States:** `RUNNING`, `DOWN`, `INTERRUPTED`, `RESET` (4 states), computed
  deterministically (`compute_window_state`) from persisted evidence
  (`window_started_ts`, `window_last_alive_ts`, `window_interrupted_ts`,
  `window_reset_ts` meta keys) plus a liveness-staleness rule — never from an
  in-memory claim.
- **Where recorded:** `IBKR_PAPER_BRIDGE/bridge/engine/window.py` (full
  docstring + `compute_window_state`/`window_status`), backed by
  `store/db.py` meta keys.
- **Who writes it:** the bridge engine writes the underlying meta timestamps
  (`window_started_ts` etc.) as it runs/restarts/gets interrupted; the state
  itself is a pure read-time derivation, not a stored field.
- **Planned §6.3/§6.5 slot:** **Partial — anticipates an unbuilt planned
  concept, with different vocabulary.** This is functionally a monitoring-soak
  tracker for exactly the evidence the plan's `INTERNAL_PAPER` lane requires
  (§6.4: "no restarted window unless a newly approved plan exists," "zero
  unexplained reconciliation breaks"). But §6.4 states in the frozen doc that
  `INTERNAL_PAPER`/`EXCHANGE_TESTNET` are **"not run or authorized by this
  document"** — i.e. the plan treats the soak-window lane as not yet started,
  while a working soak-window state machine already exists in code today under
  different state names (`RUNNING`/`DOWN`/`INTERRUPTED`/`RESET` vs. the plan's
  `evidence_window_start`/composite-clock model, §6.7). See Contradictions §3.3.

### 2.8 Bridge `OrderState` — order lifecycle (11 states)

- **States:** `PENDING_NEW`, `SUBMITTING`, `SUBMITTED`, `OPEN`,
  `PARTIALLY_FILLED`, `PENDING_CANCEL`, `FILLED`, `CANCELED`, `REJECTED`,
  `EXPIRED`, `UNKNOWN_SUBMISSION`, with an explicit transition table
  (`ORDER_STATE_TRANSITIONS`) and terminal-state set.
- **Where recorded:** `IBKR_PAPER_BRIDGE/bridge/engine/types.py` lines
  119–420 (`OrderState` enum, `ORDER_STATE_TRANSITIONS`,
  `can_transition`/`validate_order_transition`,
  `normalize_raw_order_status`), documented fully in
  `IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md` (ADR-0023, TS-P1-001/004).
  Persisted `orders.status` column in `store/db.py`.
- **Who writes it:** `bridge/engine/orders.py` (`OrderManager`), driven by
  broker fill/order-update events and internal submission logic; read by the
  reconciliation layer and the dashboard.
- **Planned §6.3/§6.5 slot:** **No named slot in §6.3/§6.5** — this is
  execution-layer evidence, not a candidate-lifecycle stage. It is exactly the
  kind of evidence the plan's `EXCHANGE_TESTNET` row promises ("order
  acceptance, rejects, partial fills, protective-order behaviour," §6.4), but
  the plan never names or references this state machine, its 11 states, or its
  transition table.

### 2.9 Bridge `PartialProtectionState` — partial-fill recovery (10 states)

- **States:** `PARTIAL_DETECTED`, `PROTECTION_PENDING`, `PROTECTION_VERIFIED`,
  `PROTECTED_PARTIAL`, `CANCEL_PENDING`, `CANCEL_UNKNOWN`, `FLATTEN_PENDING`,
  `FLATTEN_UNKNOWN`, `SAFE_FLAT`, `UNPROTECTED_ABORT` — "deliberately separate
  from `OrderState`" per its own docstring.
- **Where recorded:** `IBKR_PAPER_BRIDGE/bridge/engine/types.py` lines
  545–689, documented in
  `IBKR_PAPER_BRIDGE/docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md` (TS-P1-004).
  The consuming state machine lives in `bridge/engine/orders.py`.
- **Who writes it:** the order manager's partial-fill protect-or-flatten
  logic, on a bounded 10s/5s deadline budget.
- **Planned §6.3/§6.5 slot:** **No equivalent — purely an execution-safety
  recovery mechanism**, unrelated to candidate promotion. Not referenced
  anywhere in the frozen planning doc.

### 2.10 Bridge `ReconcileAttemptState` — reconciliation attempt lifecycle

- **States:** `COLLECTING`, `COMPLETE`, `INCOMPLETE`, `CONFLICTING`, `STALE`.
- **Where recorded:** `IBKR_PAPER_BRIDGE/bridge/engine/types.py` lines
  852–868, documented in
  `IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md` (TS-P1-005).
- **Who writes it:** `bridge/engine/reconcile.py`'s `FullReconciler`.
- **Planned §6.3/§6.5 slot:** **No named slot**, though the plan's
  `EXCHANGE_TESTNET` row references "reconciliation" and
  "backtest-vs-execution divergence" as evidence that environment must produce
  (§6.4) — functionally adjacent, not a named match.

---

## 3. Contradictions

### 3.1 Seven-stage promotion ladder vs 21-step / 4-eligibility-state plan

Today's `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §9 promotion ladder (7 stages,
written into `STRATEGY_RESEARCH_REGISTRY.json.current_status`) has **no
1:1 correspondence** to the planned 21-step lifecycle (§6.3) or 4-state
eligibility ladder (§6.5):

- Different stage counts: 7 vs 21 (or 4, depending which planned axis you
  compare against).
- `MTC_ENGINE_VALIDATED` (today) names a specific validation harness
  (`MTCRunner`, light-risk profile) that has no analog anywhere in §6.3/§6.5 —
  the plan's validation is expressed as falsifiable checks bound to a
  `deployment_identity_hash`, not a named harness-pass milestone.
- `APPROVED_FOR_MTC_V2_INTEGRATION` (today, `07_BACKTEST_AND_OPTIMIZATION_RULES.md`
  §9) vs `LIMITED_LIVE_APPROVED` (plan, §6.5): both are terminal "cleared to go
  live" states, but today's version requires no `deployment_identity_hash`
  binding, no 14-precondition signed gate, and no separate loss-at-stop cap
  (D-07, plan §6.3 step 20) — today's promotion string alone would satisfy
  none of the plan's admission requirements.
- Ownership: today's promotion decision is a narrative judgment call embedded
  in a Markdown report/registry field (`STRATEGY_RESEARCH_WORKFLOW.md` step
  12, `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §2 step 11); the plan's
  `LIMITED_LIVE_APPROVED` requires a machine-readable "promotion decision
  artifact" (§6.7) stamped with three separate hashes and reviewed against an
  append-only observation ledger (§6.6 rules 6–8). Today: informal/manual.
  Planned: structured/automated-evidence-gated.

### 3.2 Three-plus overlapping classification vocabularies exist today; the plan has one

Today's repo simultaneously runs at least three classification/verdict
vocabularies for the same underlying concept ("is this strategy any good and
what should happen to it next"):

1. `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §6 candidate classification (9
   labels: `TRUE_ALPHA_CANDIDATE`, `BETA_DISGUISED_AS_ALPHA`, ...).
2. `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §9 promotion levels (7 stages,
   written to `STRATEGY_RESEARCH_REGISTRY.json`).
3. `AI_QUANTLENS_VERDICT_REGISTRY.json`'s own "expert commentary" decision
   vocabulary (`NEEDS_CLARIFICATION`, `RESEARCH_ONLY`, ...), which its own
   header explicitly disclaims as "Opinion/labels only... **the Scorecard
   remains the only scoring authority**" — implying a fourth authority
   ("the Scorecard") that this research pass did not locate.

The plan (§6.5) replaces all of this with a single falsifiable
PASS/FAIL/BLOCKED verdict table bound to `deployment_identity_hash`. None of
today's three-plus vocabularies map cleanly onto that table, and the plan
never mentions reconciling or migrating them.

### 3.3 A working soak-window state machine exists today for a lane the plan says hasn't started

`IBKR_PAPER_BRIDGE/bridge/engine/window.py`'s `RUNNING`/`DOWN`/`INTERRUPTED`/
`RESET` state machine is a functioning, tested (see
`IBKR_PAPER_BRIDGE/tests/test_window_state.py`) soak/monitoring-window tracker
that already implements much of what the plan's `INTERNAL_PAPER` canonical
paper-soak lane needs (persisted evidence, staleness rules, sticky
interruption across re-arm). Yet the frozen planning doc's §6.4 states
`INTERNAL_PAPER`/`EXCHANGE_TESTNET` are **"not run or authorized by this
document"** and assigns their carrier to a not-yet-executed work package
(`WP-V2B-07`) — the plan is written as if this lane is greenfield, while
load-bearing plumbing for it already exists in the bridge under a different
name and a different state vocabulary (no `evidence_window_start`, no
`deployment_identity_hash` binding, no `package_hash`/`family_id` concept at
all in `window.py`).

### 3.4 `app_state` (ARMED/DISARMED/KILLED) has no named home in the plan

The bridge's own execution-safety interlock — `ARMED`/`DISARMED`/`KILLED`,
gating every order submission (`orders.py` lines 226–227, 317–319) — is not
named anywhere in §6.3, §6.4, or §6.5 of the plan. It is real, load-bearing,
tested state that any `EXCHANGE_TESTNET`/`LIMITED_LIVE` implementation will
need, but the plan's environment table (§6.4) describes *what* each
environment proves without naming *how* a running instance is armed/disarmed
at all. This is a gap rather than a strict contradiction, but it means the
plan's environment descriptions cannot be implemented as-is without silently
reusing (or redesigning) this existing state machine.

### 3.5 Research workflow has no freeze/mint step; the plan makes freeze/mint the load-bearing rule

`STRATEGY_RESEARCH_WORKFLOW.md` runs discovery through final-report-and-registry
(steps 1–16) with no `package_hash`, no `deployment_identity_hash`, and no
concept of "freezing" a candidate before forward-testing it. The plan's §6.3
"freeze rule" and §6.6 "shadow leakage rules" are explicit that a candidate
**must** be frozen and have a composite identity minted *before* any forward
observation is legitimate evidence (§6.6 rule 1: "No exceptions"). Under
today's workflow, a candidate can be iterated, backtested, and written into
`RESEARCH_RUN_REGISTRY.json`/`VARIANT_LOG_REGISTRY.json` with no freeze point
at all — every existing research run is, by the plan's own rule, evidentially
compromised for future forward-testing claims unless retrofitted with hashes
after the fact.

---

## 4. Orphaned stages

1. **`PROMOTION_REGISTRY.json` (§2.3).** A file whose name and schema
   (`promotions: []`) imply it is the canonical promotion-state store. One git
   commit ever (the initial migration), zero code references to its path
   anywhere in the repo, empty array. Nothing writes to it; nothing reads from
   it. The actual promotion state lives in a completely different file
   (`STRATEGY_RESEARCH_REGISTRY.json.current_status`). This is audit fact F-6.

2. **`STRATEGY_REGISTRY.json` (§2.3b).** Same pattern — one commit, empty
   `candidates: []` array, no code reference found — sitting alongside the
   similarly-named but actively-used `STRATEGY_RESEARCH_REGISTRY.json`. Not
   named by the F-6 audit fact but structurally identical to it.

3. **The §6 candidate-classification labels themselves (`TRUE_ALPHA_CANDIDATE`
   etc.).** These 9 labels are defined as a formal table in
   `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §6, but this research pass found no
   single registry field that stores them verbatim — they surface only inside
   free-text Markdown reports and JSON blobs (`alpha_summary.json`,
   `CLAUDE_AUDIT_FINDINGS.md`). A reasonable-effort grep across
   `MTC_COMMAND_CENTER/08_DASHBOARD_APP` for these exact label strings as a
   *read/consumed* field (vs. prose mention) found no dashboard code branching
   on them — they appear to be assigned by narrative convention and read by
   humans in reports, not consumed by any downstream promotion logic.

4. **`AI_QUANTLENS_VERDICT_REGISTRY.json`'s "Scorecard" reference.** The
   registry's own header states it is not the scoring authority and that "the
   Scorecard" is — but this research pass, scoped to the sources listed in the
   task, did not locate a file or component named "Scorecard" that the 222 KB
   of verdict entries here actually defer to. If real, it is a fourth
   classification store this inventory could not verify; if aspirational, the
   222 KB of entries here point at a non-existent authority.

---

## 5. Summary table

| Concept | Source | Planned §6.3/§6.5 slot? | Status |
|---|---|---|---|
| §6 candidate classification labels (9) | `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §6 | No (only `REJECTED` partially maps to DEC1) | Orphan / no plan equivalent |
| §9 promotion levels (7 stages) | `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §9; written to `STRATEGY_RESEARCH_REGISTRY.json.current_status` | Partial — different stage count, no hash binding | Contradiction |
| `PROMOTION_REGISTRY.json` | `05_REGISTRY/PROMOTION_REGISTRY.json` | No (plan's "promotion decision artifact," §6.7, is the conceptual successor) | Orphan (F-6) |
| `STRATEGY_REGISTRY.json` | `05_REGISTRY/STRATEGY_REGISTRY.json` | No | Orphan (secondary, not F-6) |
| `AI_QUANTLENS_VERDICT_REGISTRY.json` decision vocabulary | `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json` | No | Orphan / unverifiable "Scorecard" dependency |
| `STRATEGY_RESEARCH_WORKFLOW.md` 16-step process | `_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md` | Partial — spans plan steps 1–14 only, no freeze/mint, no environments | Contradiction |
| `app_state` (ARMED/DISARMED/KILLED) | `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` + `api/routes.py` | No named slot (operates inside §6.4 environments, unnamed) | No plan equivalent |
| `WindowState` (RUNNING/DOWN/INTERRUPTED/RESET) | `IBKR_PAPER_BRIDGE/bridge/engine/window.py` | Partial — anticipates `INTERNAL_PAPER` lane the plan calls not-yet-authorized | Contradiction |
| `OrderState` (11 states) | `IBKR_PAPER_BRIDGE/bridge/engine/types.py` + `docs/22_ORDER_STATE_CONTRACT.md` | No named slot (feeds `EXCHANGE_TESTNET` evidence, unreferenced by plan) | No plan equivalent |
| `PartialProtectionState` (10 states) | `IBKR_PAPER_BRIDGE/bridge/engine/types.py` + `docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md` | No | No plan equivalent |
| `ReconcileAttemptState` (5 states) | `IBKR_PAPER_BRIDGE/bridge/engine/types.py` + `docs/26_FULL_RECONCILIATION_CONTRACT.md` | No named slot (feeds §6.4 "reconciliation" evidence generically) | No plan equivalent |
| Planned 21-step lifecycle (§6.3) | Frozen brief, `git show 764da27f:...MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` | — (this is the plan itself) | Matches plan by definition |
| Planned eligibility states (§6.5) | Same | — | Matches plan by definition |
