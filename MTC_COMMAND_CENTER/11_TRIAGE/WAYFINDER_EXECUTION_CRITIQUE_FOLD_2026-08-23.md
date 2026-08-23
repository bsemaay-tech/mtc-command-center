# WAYFINDER EXECUTION-CRITIQUE FOLD — 2026-08-23 (map #79)

**Status:** owner-decision record and plan-amendment pass. Planning only — **implementation authorized: NO.** Per D-12, nothing here authorizes trading code, Pine, Bridge behaviour, schema activation, host contact, credentials, deployment, testnet, live, ARM, KILL or any work package to start.

**What this is.** GitHub map issue [Bridge V2 & Execution Architecture critique map (#79)](https://github.com/bsemaay-tech/mtc-command-center/issues/79) ran as a critique of the already-settled architecture, not a redesign. Two research tickets compared the deployed Bridge with the V2A/V2B plan and mapped macro responsibilities. Four owner-grilled tickets then settled Guardian policy, reconciliation, worker/window failure semantics and the disposition of the confirmed gaps. **Detail lives in each ticket's resolution comment; this document indexes and applies.**

**Locked prior art.** Nothing in folds #37, #54 or #67 is reopened: KVM2 hosting, subaccounts/agent-wallet account binding, hybrid worker stores, custody, CI, venue data, kernel seams, lifecycle/ledger doctrine, admission/promotion separation, post-live tail, succession, economic-honesty rules and the cost-registry doctrine remain binding. A carrier assignment below makes a settled decision executable; it does not re-decide it.

**Change-control position.** Amends the planning set at master `a01de9c58031fb43e0ac45770db4d6c99ede6349`. **Owner outcome documents are untouched. Requirement count stays 60 = 44 + 16. Package count changes from 75 to 76** through one genuinely new package, WP-P0-31. Existing packages are amended in place and none is renumbered. **Materiality: MATERIAL** — the fold adds a T0 lifecycle authority, changes the schema-activation boundary from v8 to v9, and assigns load-bearing reconciliation/failure carriers. A fresh G1 acceptance round over the amended set is recommended before G1-IA for any affected package; that audit and every implementation authorization remain separate owner decisions.

---

## 1. Owner decisions

| Ticket | Ratified decision |
|---|---|
| [Decide: the Guardian policy macro (#89)](https://github.com/bsemaay-tech/mtc-command-center/issues/89) | Guardian judges the risk envelope, never alpha. Allowed inputs: bucket exposure/caps, correlation, snapshot freshness, venue state, daily-loss ledger and protection placeability. Seven fail-closed veto classes; policy crash rejects as `POLICY_ERROR`. Policy content is owner-gated/versioned/identity-bound. Guardian and tail consume one threshold source. Guardian never writes lifecycle state and never resizes. |
| [Decide: the reconciliation doctrine (#90)](https://github.com/bsemaay-tech/mtc-command-center/issues/90) | Worker owns scope-level venue truth; supervisor owns portfolio cross-check/divergence reporting. Target is three-way intended/authorized vs store vs venue, with two-way explicitly interim before Guardian. Inherited V1 reconciliation must be D026 re-proven before ARM trusts it. Standing unexplained breaks block ARM, promotion and affected evidence windows, but never auto-KILL. |
| [Decide: worker and window failure semantics (#91)](https://github.com/bsemaay-tech/mtc-command-center/issues/91) | Map-#54 evidence doctrine remains canonical. Worker death preserves identity, records the gap and requires reconciliation before re-attachment. Supervisor death blocks new risk while worker protection survives, pages the watchdog and requires portfolio reconciliation before authorization resumes. Feed/venue failures map to the existing freshness/venue vocabulary. The current global sticky 300-second value is not ratified; threshold stays `[OPEN]`. |
| [Decide: disposition of the found gaps (#92)](https://github.com/bsemaay-tech/mtc-command-center/issues/92) | Existing packages receive staged reconciliation, cost feedback, freshness/divergence and evidence-window duties; schema activation expands through v9; one genuinely new WP-P0-31 becomes the Lifecycle Ledger/Registrar carrier. No settled map is reopened, no other package is created, and all numbers remain `[OPEN]`. |

Research inputs, both closed 2026-08-23: [deployed Bridge vs V2A/V2B plan (#87)](https://github.com/bsemaay-tech/mtc-command-center/issues/87) and [responsibility-matrix scan (#88)](https://github.com/bsemaay-tech/mtc-command-center/issues/88). Their files remain on their research branches; this fold carries only the verified findings that reached owner decisions.

---

## 2. Responsibility assignments

| Responsibility | Building/owning carrier | Consumer/proof carrier |
|---|---|---|
| Lifecycle Ledger storage, append gate, derived current view, Registrar | **New WP-P0-31** | WP-V2A-10 admissions, WP-V3-03 promotions, WP-V2B-03 post-live tail append through the same gate |
| Worker-level reconciliation and evidence-window identity/gaps | **WP-V2A-02** | WP-V2A-08 shadow; WP-V2B-07 paper/testnet |
| Portfolio-wide reconciliation, divergence report and aggregate freshness | **WP-V2B-03** | WP-V2B-07 proof; dashboard consumers later |
| Research-side cost-model registry | **WP-P0-20** | WP-V2B-07 supplies paper/testnet fills; WP-V3-05 supplies live fills later |
| Backtest-versus-forward divergence | **WP-P0-21 computes** | WP-V3-03 blocks further promotion and notifies the owner |
| Common freshness vocabulary | **WP-P0-04 defines** | WP-P0-30 market, WP-V2A-04 account, WP-V2B-03 aggregate order/fill/reconciler domains |
| Existing v9 kill-evidence fields | **WP-V2B-04 activates v4→v9** | No new behaviour; testnet proof remains WP-V2B-07 |
| Guardian policy | **WP-V2B-01** | WP-V2B-02 simulates the same policy; downstream surfaces only render it |

The Decision Orchestrator remains inside WP-V2A-03/04/05. Protective-order placement remains with the execution seam and its WP-V2B-07 paper/testnet proof. No new carrier is created for either.

---

## 3. Owner-gated definition artifact registered by this fold

**Guardian policy content — v1.** Versioned; changing content requires the owner's word; applying the accepted version is automatic. Its v1 content is the allowed/forbidden input lists, seven-class veto taxonomy, fail-closed `POLICY_ERROR`, no-resizing rule, and one-threshold-source contract shared with the §6.9 tail. Any content change mints a new `deployment_identity_hash`. Numerical values are not part of v1 and remain `[OPEN]`.

Existing members of this definition class remain: eligibility check sets, slot-ranking rule and triage worthiness checklist (map #54); control-parity checklist, statistical-battery definition and search-space definition (map #67); Explorer display doctrine (map #78). This registration completes the “map #79, in flight” entry already anticipated by the Explorer fold.

---

## 4. Amendments applied

| # | File · location | Amendment |
|---|---|---|
| A1 | Technical brief · §6.9 and §11.5 | Names WP-P0-31 and the three downstream lifecycle writers without changing map-#54 semantics. |
| A2 | Technical brief · §9.7 | Names cost-registry and divergence computation/enforcement carriers. |
| A3 | Technical brief · new §10.4 | Normative Guardian, reconciliation, failure/window and gap-carrier summary with ticket links. |
| A4 | Technical brief · §12.3 | Assigns the common freshness vocabulary to contracts and domain producers. |
| A5 | Technical brief · §17.1/§17.2, risk R-6, acceptance A-8/A-13/A-14/A-14b | Adds the lifecycle package to Phase 0; corrects v4→v9; makes failure, Guardian and reconciliation acceptance failable. |
| A6 | Work-package plan · package count and dependency graph | Count 76; adds WP-P0-31; changes the schema node to v4-v9; adds ledger dependencies. |
| A7 | Work-package plan · WP-P0-04/P0-20/P0-21/P0-30 | Adds shared contract, cost registry, divergence computation and market-freshness duties. |
| A8 | Work-package plan · new WP-P0-31 | Full nine-field Lifecycle Ledger and Registrar package, provisionally T0 and gated under G3 plus G1-IA. |
| A9 | Work-package plan · WP-V2A-02/V2A-08/V2A-10 | Adds worker reconciliation/window ownership and makes admission a Lifecycle Ledger writer. |
| A10 | Work-package plan · WP-V2B-01/V2B-03/V2B-04/V2B-07 | Adds Guardian policy, supervisor reconciliation/failure/tail, v9 activation and paper/testnet proof/cost feeds. |
| A11 | Work-package plan · WP-V3-03/V3-05 | Promotion reads divergence and writes the Lifecycle Ledger; live fills feed the cost registry. |
| A12 | Requirements register · scheme/count note | Count 76 and explicit mapping extensions; requirement and safeguard texts unchanged. |

---

## 5. Brownfield facts preserved

- The deployed Bridge is the brownfield baseline, not evidence that V2 responsibilities already exist.
- Existing V1 reconciliation is real and durable but **two-way**, not the target three-way doctrine. It is not trusted for ARM until independently D026 re-proven.
- Schema migrations v4 through v9 already exist in code/tests; this fold corrects the activation plan to include v9. It creates no migration code and changes no deployed database.
- The existing window machine has a global sticky interruption after 300 seconds. This value is an observed implementation detail, not an owner-approved threshold. The conforming design scopes windows by worker and environment; the number remains `[OPEN]`.
- Ticket #91's provisional wording placed window conformance at “V2 activation” while leaving the exact carrier to gap disposition. Ticket #92 settled that carrier as WP-V2A-02; WP-V2B-04 remains schema-v9 activation only, with no “while we are in there” window edit.
- A supervisor does not exist today. Assigning its responsibilities is planning, not a claim that the capability is present.

---

## 6. What remains open

- Every numerical threshold: Guardian limits, flap counts/windows, evidence-gap duration, freshness bounds, divergence tolerances and all other values remain `[OPEN]`.
- G1 re-acceptance of this material amendment and G1-IA for every affected package.
- Any exact implementation design inside the package boundaries, including storage technology details beyond the already-ratified SQLite worker truth and append-only ledger doctrine.
- Safety mechanics owned by map #96: ARM/DISARM/KILL/FLATTEN internals, break-glass and incident response. This fold names interlocks only.
- Operator surfaces owned by map #95 and repository topology owned by map #97.

---

## 7. What this fold does not do

- No source, trading, Pine, Bridge-runtime, schema, migration, host, credential, deployment, testnet or live change.
- No database opened or modified; no process, service, server, worker, broker or venue contacted.
- No package started and no G1/G1-IA/G2–G9 gate satisfied.
- No settled map reopened; no owner outcome document changed.
- No invented numeric value and no silent promotion/demotion/KILL behaviour.

---

## 8. Verification

- Base: `origin/master` at `a01de9c58031fb43e0ac45770db4d6c99ede6349`.
- Branch: `feature/wayfinder-fold-map79-20260823` in isolated worktree `C:\WF93`.
- Editing discipline: exact anchored patches only; no broad replacement, no protected path and no owner outcome document.
- Post-pass checks: repo-wide marker searches, package/requirement counts, exact changed-path review, whitespace check and repo guard at pre-commit.
- Counts: requirements **60 = 44 + 16** unchanged; packages **76** (one new package, no renumbering).
