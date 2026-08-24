# Lane H Report — WP-P0-25 Broker Boundary

**Status:** IMPLEMENTER WORK COMPLETE; T0 Lead audit/acceptance and Git commit remain Lead-owned.

**Date:** 2026-08-25

**Branch:** `feature/wp-p0-25-broker-boundary-20260825`

**Starting / current HEAD:** `4691a9dd843f05948b271a88972c94a3bdce13a7`

**Audit tier:** T0, gate G3, decision-only

**Decision:** reuse the existing `Broker` / `PartialRecoveryBroker` / `FullReconciliationBroker` structural family as-is.

## Deliverables

1. `BROKER_BOUNDARY_DECISION.md` — decision, complete method inventory, option pricing, V2A/V5 mapping, accepted-contract consequences, and nonexistent-protocol sweep.
2. `POINTER_REVERIFICATION.md` — stale pointer to planning-candidate pointer to fresh-HEAD pointer, plus method-set and semantic-anchor evidence.
3. `LANE_REPORT.md` — this status and self-QA record.

Only these three new files were written, all under the lane's authorized directory. No source, protocol, adapter, test, schema, governance, shared-memory, or handoff file was edited.

## Self-QA against every acceptance-gate bullet

| Acceptance requirement | Result | Evidence |
|---|---|---|
| Existing protocols named by fresh file and line | PASS | Decision sections 1-2; pointer report section 1 |
| Complete method inventory, including `funding_evidence` | PASS | Decision section 2 lists 15 + 6 + 5 methods; `funding_evidence` is mapped to `base.py:374-378`, `hyperliquid.py:1894`, `mock.py:1147` |
| Existing structural `Protocol` seam is the starting point | PASS | Decision section 1 states it explicitly and cites all three declarations |
| Reuse, extend, and replace/rename each priced against minimum-code and OSS-first O-17 | PASS | Decision section 3 provides a comparative table and cites O-17 |
| Chosen option states consequences for accepted TS-P1-004/005 contracts, tests, and reason codes | PASS | Decision section 6 preserves both contracts, every named test surface, and both default reason codes unchanged |
| Exact V2A account-snapshot and protection surface mapped | PASS | Decision section 4 maps `portfolio_evidence`, typed component evidence, intent submission primitives, and partial-recovery protection primitives to WP-V2A-04/05/06 ownership |
| Exact V5 surface mapped | PASS | Decision section 5 maps future IBKR work to the same base and opt-in protocols and preserves fail-closed unsupported capabilities |
| No document continues to assert a nonexistent `BrokerAdapter` protocol | PASS | Exact-token sweep found eight historical/corrective/acceptance-rule mentions in three planning files; none declares or promises such a protocol. Decision section 7 records every hit. This package creates none |
| Decision only; no implementation or rename | PASS | `git diff --name-only` is restricted to the three new Markdown files after staging; no broker or test file changed |

## Read-only verification performed

- Confirmed repository root, expected feature branch, clean starting checkout, and fresh HEAD.
- Proved planning baseline `01e0725890e456d079bca8967625ccb09c66b889` is an ancestor of HEAD.
- Confirmed no scoped diff from that baseline to HEAD for the three broker sources and contracts 25/26.
- Parsed the broker sources with Python AST and confirmed both concrete brokers implement every method in all three protocol sets; missing-method lists were empty.
- Swept the repository for exact `BrokerAdapter` and case/spacing variants of “broker adapter.”
- Read the WP-P0-25 package contract, F-9/F-9a, brief sections 4.1/5.4/17.5, V2A package surfaces, V5 rows, O-17, contracts 25/26, and the relevant fail-closed tests.
- Did not run the Bridge suite because this package changes documentation only and makes no executable claim. No simulated test result is offered as evidence.

## Boundary compliance

- No code, protocol file, rename, adapter, IBKR work, or Hyperliquid change.
- No network, Docker, WSL, host, broker, exchange, credential, deployment, paper, testnet, or live action.
- No Pine, parity, MTC, strategy, trading, risk, schema, or runtime change.
- No other AI CLI was invoked, as the lane contract requires.
- `SESSION_LOCK.md`, `GLOBAL_HANDOFF.md`, and `NEXT_STEPS.md` were not edited because the lane's hard whitelist permits only new files in this output directory. The separate Lead owns the T0 audit, acceptance, Gate-7 handoff, and Git sequencing.

## Staging and commit state

Exact staged paths expected at handoff:

- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/BROKER_BOUNDARY_DECISION.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/POINTER_REVERIFICATION.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/LANE_REPORT.md`

**Commit SHA(s):** none in the implementer lane. Current HEAD remains `4691a9dd843f05948b271a88972c94a3bdce13a7`. After the required accepting T0 audit, the Lead should commit the exact staged paths with:

`docs(wp-p0-25): broker-boundary decision record (T0/G3 decision-only, lane H 2026-08-25)`

No push is authorized.

## Open issues / Lead handoff

1. Mandatory T0 independent acceptance is still required: exact `claude-opus-5` xhigh plus `gpt-5.6-sol` xhigh, under the Lead's capped repair loop. The implementer lane did not run or substitute for those audits.
2. The work-package plan treats TS-P1-004 as an accepted input (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:566`), while the older contract document still says `PROPOSED` (`IBKR_PAPER_BRIDGE/docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md:17-18`). That out-of-scope status inconsistency is reported, not edited, and does not alter this package's owner-provided contract.
3. All source verification is repository-level only. Deployed runtime identity remains `UNVERIFIED` pending G9.

## Recommended next action

Lead runs the two required fresh T0 audits over only these three files plus the cited source excerpts. If both flagship verdicts accept and no reproduced required finding remains, the Lead updates required handoff records within its own authority, commits the exact paths with the prescribed message, and does not push.

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

The **individual** `flatten_reduce_only` method range `base.py:271-274` is deliberately unchanged at `BROKER_BOUNDARY_DECISION.md:54`, and the method anchor `flatten_reduce_only:271` is unchanged at `POINTER_REVERIFICATION.md:37`. Only the complete-declaration range moved to 275. `POINTER_REVERIFICATION.md:21` now records both facts so the two ranges are not confused again.

### Bounded self-QA for this repair round

Read-only `git status`, `git diff`, and `rg` only. No staging, commit, push, checkout, reset, or stash. No network, Docker, WSL, host, broker, or exchange access. No code, test, schema, shared-memory, session-lock, or handoff file touched.

| Check | Result |
|---|---|
| Exactly the three whitelisted files modified, and nothing else | PASS — `git status --porcelain` and `git diff --name-only` list only `BROKER_BOUNDARY_DECISION.md`, `POINTER_REVERIFICATION.md`, `LANE_REPORT.md` under `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_25_BROKER_BOUNDARY_2026-08-25/`; nothing staged |
| No remaining complete-declaration citation ending at 274 | PASS — sweep of the lane directory returns no complete-declaration range ending at 274. The one residual literal occurrence of the old token is Finding 2's "was cited as" sentence in this repair note, which records what was corrected rather than asserting a range |
| Individual method `:271-274` still present | PASS — `BROKER_BOUNDARY_DECISION.md:54` retains `base.py:271-274` for `flatten_reduce_only` |
| Repaired snapshot row names all four chain steps | PASS — `FullReconciler`, accepted checkpoint, `Store.load_authoritative_risk_snapshot`, Account Snapshot Service |
| Produce/hash assigned to the Account Snapshot Service; consume/bind assigned to the Decision Orchestrator | PASS — stated in the ownership column of `:97` |
| Cites `brief:1215` and `docs/27:36-72` in the repaired row | PASS — both cited |
| Rejects point-read fallback | PASS — stated in the fail-closed column of `:97` and again at `:98` |
| Sweep finds no other direct broker-method-to-snapshot assertion | PASS — `:98` repaired; `:93` and `:100` reviewed and correct |
| Source anchors re-read at HEAD `1a88728c`, not copied forward | PASS — `base.py:234-275`, `base.py:347-378`, `docs/27:36-72`, and `brief:1215` were each read directly this round |

### Repair-round boundary statement

This round changed documentation wording and two line-range citations only. It changes no decision, no runtime, no trading behavior, no protocol, no test, and no reason code. The chosen option remains **reuse the existing structural `Protocol` family as-is**. Lead T0 audit and commit authority are unchanged and still Lead-owned.
