# Lane H Report — WP-P0-25 Broker Boundary

**Status:** REPAIR ROUND 2 IMPLEMENTATION COMPLETE; T0 Lead re-audit/acceptance remains Lead-owned. This repair dispatch explicitly authorizes the implementer commit; no push is authorized.

**Date:** 2026-08-25

**Branch:** `feature/wp-p0-25-broker-boundary-20260825`

**Initial lane HEAD:** `4691a9dd843f05948b271a88972c94a3bdce13a7`

**Repair-round-2 audited HEAD:** `2601f0e27ffedc092e31a9563bee0467fb70c974`

**Audit tier:** T0, gate G3, decision-only

**Decision:** reuse the existing `Broker` / `PartialRecoveryBroker` / `KillRecoveryBroker` / `FullReconciliationBroker` structural family as-is.

## Deliverables

1. `BROKER_BOUNDARY_DECISION.md` — decision, complete method inventory, option pricing, V2A/V5 mapping, accepted-contract consequences, and nonexistent-protocol sweep.
2. `POINTER_REVERIFICATION.md` — stale pointer to planning-candidate pointer to fresh-HEAD pointer, plus method-set and semantic-anchor evidence.
3. `LANE_REPORT.md` — this status and self-QA record.

Only these three new files were written, all under the lane's authorized directory. No source, protocol, adapter, test, schema, governance, shared-memory, or handoff file was edited.

## Self-QA against every acceptance-gate bullet

| Acceptance requirement | Result | Evidence |
|---|---|---|
| Existing protocols named by fresh file and line | PASS | Decision sections 1-2; pointer report section 1 |
| Complete method inventory, including `KillRecoveryBroker` and `funding_evidence` | PASS | Decision section 2 lists 15 + 6 + 6 + 5 methods; the six kill-recovery methods and both concrete implementations are AST-verified, and `funding_evidence` maps to `base.py:374-378`, `hyperliquid.py:1894`, `mock.py:1147` |
| Existing structural `Protocol` seam is the starting point | PASS | Decision section 1 states it explicitly and cites all four declarations |
| Reuse, extend, and replace/rename each priced against minimum-code and OSS-first O-17 | PASS | Decision section 3 provides a comparative table and cites O-17 |
| Chosen option states consequences for accepted TS-P1-004/005 and TS-P1-009 contracts, tests, and reason codes | PASS | Decision section 6 preserves all three capability surfaces, their named test/evidence surfaces, and existing fail-closed reason codes unchanged |
| Exact V2A account-snapshot and protection surface mapped | PASS | Decision section 4 maps `portfolio_evidence`, typed component evidence, intent submission primitives, and partial-recovery protection primitives to WP-V2A-04/05/06 ownership |
| Exact V5 surface mapped | PASS | Decision section 5 requires future IBKR work to implement `Broker` and either completely implement or explicitly declare unavailable each opt-in surface, including all six `KillRecoveryBroker` methods; incomplete kill recovery fails closed |
| No document continues to assert a nonexistent `BrokerAdapter` protocol | PASS | Exact-token sweep found eight historical/corrective/acceptance-rule mentions in three planning files; none declares or promises such a protocol. Decision section 7 records every hit. This package creates none |
| Decision only; no implementation or rename | PASS | `git diff --name-only` is restricted to the three new Markdown files after staging; no broker or test file changed |

## Read-only verification performed

- Confirmed repository root, expected feature branch, clean starting checkout, and fresh HEAD.
- Proved planning baseline `01e0725890e456d079bca8967625ccb09c66b889` is an ancestor of HEAD.
- Confirmed no scoped diff from that baseline to HEAD for the three broker sources and contracts 25/26.
- Parsed the broker sources with Python AST and confirmed both concrete brokers implement every method in all four protocol sets (32 declarations total); missing-method lists were empty.
- Swept the repository for exact `BrokerAdapter` and case/spacing variants of “broker adapter.”
- Read the WP-P0-25 package contract, F-9/F-9a, brief sections 4.1/5.4/17.5, V2A package surfaces, V5 rows, O-17, contracts 25/26, and the relevant fail-closed tests.
- Did not run the Bridge suite because this package changes documentation only and makes no executable claim. No simulated test result is offered as evidence.

## Boundary compliance

- No code, protocol file, rename, adapter, IBKR work, or Hyperliquid change.
- No network, Docker, WSL, host, broker, exchange, credential, deployment, paper, testnet, or live action.
- No Pine, parity, MTC, strategy, trading, risk, schema, or runtime change.
- No other AI CLI was invoked, as the lane contract requires.
- `SESSION_LOCK.md`, `GLOBAL_HANDOFF.md`, and `NEXT_STEPS.md` were not edited because the lane's hard whitelist permits only the three files in this output directory. The separate Lead owns the T0 re-audit, acceptance, and Gate-7 handoff; this repair dispatch explicitly authorizes only the requested exact-path commit.

## Staging and commit state

Exact staged paths expected at handoff:

- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/BROKER_BOUNDARY_DECISION.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/POINTER_REVERIFICATION.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/LANE_REPORT.md`

**Pre-repair commit SHA(s):** `1a88728c` (initial record) and `2601f0e2` (repair round 1). Repair round 2 is explicitly authorized for an implementer commit with:

`fix(wp-p0-25): repair round 2 - fourth protocol KillRecoveryBroker inventoried`

No push is authorized.

## Open issues / Lead handoff

1. Mandatory T0 independent acceptance is still required: exact `claude-opus-5` xhigh plus `gpt-5.6-sol` xhigh, under the Lead's capped repair loop. The implementer lane did not run or substitute for those audits.
2. The work-package plan treats TS-P1-004 as an accepted input (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:566`), while the older contract document still says `PROPOSED` (`IBKR_PAPER_BRIDGE/docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md:17-18`). That out-of-scope status inconsistency is reported, not edited, and does not alter this package's owner-provided contract.
3. All source verification is repository-level only. Deployed runtime identity remains `UNVERIFIED` pending G9.

## Recommended next action

Lead runs the required fresh T0 re-audit over the repair commit and cited source excerpts. If the flagship contract accepts and no reproduced required finding remains, the Lead updates required handoff records within its own authority. No push is authorized.

---

## Repair note — 2026-08-25, repair round 1 of max 3

**Round:** 1 of 3. **Audit tier:** T0, gate G3, decision-only (classification unchanged by this repair).

**HEAD at repair start and end:** `1a88728c9908bf81c42ae9181a6019ffd8f6bc81` (unchanged; nothing staged, committed, or pushed by the implementer lane). The earlier `4691a9dd…` references above record the round-0 state and are left as the historical record.

**Branch:** `feature/wp-p0-25-broker-boundary-20260825`.

### Finding 1 — snapshot-chain correction (required)

`BROKER_BOUNDARY_DECISION.md:97` previously read as though `FullReconciliationBroker.portfolio_evidence()` were a direct input from which the V2A "Account Snapshot Service/Decision Orchestrator" constructed and content-hashed the immutable snapshot. That wording implied direct point-read construction and conflated two distinct owners.

Repaired so that `portfolio_evidence()` and the other `FullReconciliationBroker` evidence methods (`open_orders_evidence`, `fills_evidence`, `funding_evidence`) are stated as **upstream inputs only**, consumed through the full four-step chain:

`FullReconciler` → **accepted checkpoint** → `Store.load_authoritative_risk_snapshot` → **Account Snapshot Service**.

The repaired row now assigns **produce and content-hash** to the Account Snapshot Service, built on the Bridge's existing authoritative risk snapshot rather than a second source of account truth (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1215`), and assigns **consume and bind only** to the Decision Orchestrator. It records that `Store.load_authoritative_risk_snapshot` validates the sole pointer's complete accepted checkpoint and all seven components under one pinned committed epoch before any immutable `AuthoritativeRiskSnapshot` exists, and that there is **no point-read fallback**, retry, automatic re-arm, or submission (`IBKR_PAPER_BRIDGE/docs/27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md:36-72`).

REUSE is preserved and restated explicitly in the repaired row: the broker surface is reused as-is, and no broker method is added, renamed, or read directly to build a snapshot. The chosen option, the option pricing in section 3, and every other section are unchanged.

**Consistency sweep.** The whole decision was swept for any other direct broker-method-to-snapshot implication. One further site was found and repaired: `BROKER_BOUNDARY_DECISION.md:98` (legacy account read) previously said "the snapshot service uses evidence-carrying input above," which still implied a direct feed. It now states that the Account Snapshot Service is fed only through the reconciled chain above, never by a direct account point-read, with the same `docs/27:36-72` citation. `:93` (snapshot identity owned outside the broker) and `:100` (venue-level `symbol_snapshot` in the WP-V2A-06 protection row) were reviewed and are correct as written — `:100` concerns per-symbol venue evidence, not the account snapshot. No other site asserts direct construction.

### Finding 2 — `PartialRecoveryBroker` declaration range correction (required)

The complete declaration range was cited as `:234-274`. The protocol body's last statement is the `flatten_reduce_only` body ellipsis at `base.py:275`, so the complete declaration range is `:234-275`. Corrected at:

- `BROKER_BOUNDARY_DECISION.md:13`
- `POINTER_REVERIFICATION.md:21` (fresh-evidence column)

At round 1, the **individual** `flatten_reduce_only` method range was deliberately left at `base.py:271-274`, while only the complete-declaration range moved to 275. Repair round 2 supersedes that convention: both current inventory tables now use the AST-exact inclusive individual range `base.py:271-275`.

### Bounded self-QA for this repair round

Read-only `git status`, `git diff`, and `rg` only. No staging, commit, push, checkout, reset, or stash. No network, Docker, WSL, host, broker, or exchange access. No code, test, schema, shared-memory, session-lock, or handoff file touched.

| Check | Result |
|---|---|
| Exactly the three whitelisted files modified, and nothing else | PASS — `git status --porcelain` and `git diff --name-only` list only `BROKER_BOUNDARY_DECISION.md`, `POINTER_REVERIFICATION.md`, `LANE_REPORT.md` under `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/`; nothing staged |
| No remaining complete-declaration citation ending at 274 | PASS — sweep of the lane directory returns no complete-declaration range ending at 274. The one residual literal occurrence of the old token is Finding 2's "was cited as" sentence in this repair note, which records what was corrected rather than asserting a range |
| Round-1 individual method-range handling | SUPERSEDED — repair round 2 applies the inclusive AST `end_lineno` convention in every current inventory table |
| Repaired snapshot row names all four chain steps | PASS — `FullReconciler`, accepted checkpoint, `Store.load_authoritative_risk_snapshot`, Account Snapshot Service |
| Produce/hash assigned to the Account Snapshot Service; consume/bind assigned to the Decision Orchestrator | PASS — stated in the ownership column of `:97` |
| Cites `brief:1215` and `docs/27:36-72` in the repaired row | PASS — both cited |
| Rejects point-read fallback | PASS — stated in the fail-closed column of `:97` and again at `:98` |
| Sweep finds no other direct broker-method-to-snapshot assertion | PASS — `:98` repaired; `:93` and `:100` reviewed and correct |
| Source anchors re-read at HEAD `1a88728c`, not copied forward | PASS — `base.py:234-275`, `base.py:347-378`, `docs/27:36-72`, and `brief:1215` were each read directly this round |

### Repair-round boundary statement

This round changed documentation wording and two line-range citations only. It changes no decision, no runtime, no trading behavior, no protocol, no test, and no reason code. The chosen option remains **reuse the existing structural `Protocol` family as-is**. Lead T0 audit and commit authority are unchanged and still Lead-owned.

---

## Repair note — 2026-08-25, repair round 2 of max 3

**Round:** 2 of 3. **Audit tier:** T0, gate G3, decision-only (classification unchanged).

**Audited HEAD before repair:** `2601f0e27ffedc092e31a9563bee0467fb70c974`. All cited source files are byte-identical from source baseline `4691a9dd` through that audited HEAD; only the three Lane H Markdown files differ.

### Required finding — fourth protocol inventoried

`KillRecoveryBroker` is now included everywhere the record enumerates the structural family. Section 2 records its AST-exact declaration (`base.py:280-325`) and complete six-method surface: `lot_unit:281-282`, `symbol_snapshot:284-285`, `capture_kill_evidence:287-296`, `query_order:298-299`, `kill_cancel_order_by_cloid:301-311`, and `kill_flatten_reduce_only:313-325`. Both concrete implementations are complete at Hyperliquid anchors `975,1040,1840,1171,1357,1479` and Mock anchors `377,394,948,457,536,639`.

The V5 mapping now requires WP-V5-01 to implement `Broker` and, for each of the three opt-in capabilities, either implement the whole protocol or explicitly declare it unavailable. A partial or silently absent `KillRecoveryBroker` surface is forbidden; the existing six-callable feature detection rejects it as `KILL_BROKER_API_UNAVAILABLE` with no kill action.

`POINTER_REVERIFICATION.md` and this report now carry AST proof for all four protocols and 32 methods. They also record the 2026-08-25 audited-HEAD marker at `2601f0e2` and source byte-identity since `4691a9dd`.

### Nits closed

- All individual protocol-method declaration ranges in the decision and pointer tables now use Python AST `end_lineno` inclusively.
- `POINTER_REVERIFICATION.md` now distinguishes the `4691a9dd` source baseline from the dated audited HEAD `2601f0e2`.

### REUSE pricing re-check

The minimum-code and OSS-first pricing still holds with four protocols. `KillRecoveryBroker` is already implemented by both concrete brokers and already feature-detected fail-closed, so reuse adds no boundary code. Extension or replacement still carries the same implementation, conformance, compatibility, migration, and OSS-translation costs.

### Repair-round-2 bounded self-QA

| Check | Result |
|---|---|
| Four protocol declarations found by AST | PASS — `Broker:156-212`, `PartialRecoveryBroker:234-275`, `KillRecoveryBroker:280-325`, `FullReconciliationBroker:347-378` |
| Complete 32-method declaration inventory | PASS — `15 + 6 + 6 + 5`; every table range equals inclusive AST `lineno-end_lineno` |
| Both concrete implementations complete | PASS — zero missing methods for Hyperliquid and Mock across all four protocol sets |
| Kill runtime feature detection and fail-closed result | PASS — `orders.py:88-95`, `:316-317`, `:1742-1745`; capture fallback at `reconcile.py:209-238` |
| Scope | PASS — only the three authorized Lane H Markdown files changed; no runtime, trading logic, protocol, test, schema, or reason code changed |

### Repair-round boundary statement

This repair corrects the architecture record and future V5 acceptance mapping only. It changes no decision to reuse, no runtime, no trading behavior, no protocol, no broker implementation, no test, and no reason code. Lead T0 re-audit and acceptance remain required; no push is authorized.
