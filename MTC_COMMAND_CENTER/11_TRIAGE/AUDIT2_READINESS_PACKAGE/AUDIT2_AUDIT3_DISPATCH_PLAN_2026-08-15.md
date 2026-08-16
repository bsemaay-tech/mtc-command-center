# Audit 2 and Audit 3/Gate 6 dispatch plan and shared-reserve recommendation

> **Correction, 2026-08-16 morning:** the reserve question this plan poses is
> answered — owner decision §4 (`OWNER_DECISIONS_2026-08-16_MORNING.md`) keeps
> the 6 h pool as a hard cap, accepts BLOCK on exhaustion, and makes metering
> both Audit 2 sessions mandatory, with measured actuals presented before
> Audit 3/Gate 6. Metering mechanism:
> `AUDIT2_METERING_AMENDMENT_2026-08-16.md` (same directory).

Status: **PLANNING MATERIAL ONLY — NO DISPATCH, NO GATE VERDICT, NO ACCEPTANCE, NO AUTHORIZATION.** The Audit 2 package itself is a readiness assembly that neither dispatches nor accepts an audit, contacts a host, executes an artifact, creates a freeze, or creates authority (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:3-6`).

## 1. Controlling roster and the apparent plan conflict

The active 50-hour plan assigns one aggregate **6 h** audit-only reserve to Audit 2, Audit 3, Gate 6, and every re-audit; it funds no implementation or repair, and exhaustion while an audit remains means BLOCK (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:841-853`). Rows R21 and R24 consequently remain `NO SOURCED ESTIMATE`; neither row has a disjoint allocation from that pool (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60`, `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:63`).

The active plan still contains Codex-only roster wording for Audit 2, Audit 3, and Gate 6 (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1020-1025`). The later permanent audit-tier policy makes `AGENTS.md` the canonical operational copy (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISION_AUDIT_TIERS_2026-08-09.md:7-11`), and `AGENTS.md` says the tier policy controls headcount and supersedes blanket roster language unless a later explicit owner contract overrides it (`AGENTS.md:31-46`). Therefore the dispatch roster below uses the current T0 default, not the plan's Codex-only sentence.

Exact default roster for **each checkpoint**:

1. Fresh independent Claude `claude-opus-5`, effort `xhigh` (`AGENTS.md:54-61`).
2. Fresh independent Codex `gpt-5.6-sol`, effort `xhigh` (`AGENTS.md:63-70`).

T0 requires those two independent xhigh flagships and permits at most three rounds (`AGENTS.md:33-35`). DeepSeek and GLM are not added by default: a four-auditor Gate 5/Gate 6 review exists only under a later explicit owner/task contract, and the permanent tier policy still decides headcount (`AGENTS.md:83-89`). Audit 2's own dispatcher record independently closes this question as exactly the two flagships and no silently added GLM (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:9-13`).

If either exact flagship model or required effort is unavailable, that session returns BLOCK unless Barış explicitly waives the exact requirement (`AGENTS.md:56-60`, `AGENTS.md:65-70`).

## 2. Audit 2 dispatch plan (R21)

### 2.1 Dispatch point and subject

Dispatch only after R16 has frozen the complete pre-WP-A checkpoint and R20 has finalized one authoritative Packet 10 manifest/bundle for both auditors (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55-60`). Audit 2 occurs immediately after WP-L Phase 2 plus WP-I staging verification and before WP-A (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:970-977`).

The Audit 2 subject is the Linux-port and staging-acceptance evidence for one already frozen pre-WP-A artifact at one exact SHA; the audit does not create that freeze (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:24-42`). Its required coverage is:

- frozen source, candidate, artifact, manifest, and evidence identities;
- WP-L Phase 2 closure and preserved open/BLOCKED items;
- WP-I staging closure, rows 1-24, and the final successor;
- chain of custody, preregistration order, RUNIDs, and hashes;
- the mandated suite and exact accepted anomaly set;
- D026 RED/GREEN evidence for tests offered as defect-closure proof;
- authority, budget, ordering, Stage-1, and freeze compliance; and
- the accepted section 10.1 access grammar and composite section 10.2 proof (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:26-37`).

### 2.2 Independence mechanics

Create two different audit-only worktrees at the same full frozen SHA. Give each a fresh standalone prompt, seal both initial reports before either report is shared, and never show one auditor the other's reasoning, findings, or verdict (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:26-32`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:9-22`).

For each worktree, the dispatcher records its resolved path, exact `git rev-parse HEAD`, and empty `git status --porcelain` before and after the audit. A SHA mismatch or non-empty cleanliness proof requires BLOCK (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`). Neither session uses `--resume` or `--continue`, an implementer worktree, the other auditor's worktree, or implementer-session context (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:16-18`, `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:67-76`).

### 2.3 Identical inputs to each flagship

Give each auditor only the same frozen scope contract, adopted plan if any, actual diff/files at the frozen SHA, test/evidence package, readiness package, and required repository rules (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:44-49`; `AGENTS.md:93-96`). The frozen packet must bind at least:

- full frozen SHA, base SHA, exact base-to-freeze diff, and frozen file list;
- candidate, artifact, manifest, and evidence identities;
- WP-L Phase 2 closure record and evidence index;
- final WP-I closure record and evidence index;
- current/final acceptance matrix and D026 register;
- owner-ratified freeze-time ledger and consolidated authority record; and
- one authoritative mandated-suite command, environment/baseline source, exit code, pass/fail/skip/xfail counts, exact anomaly IDs, and signatures (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:51-64`, `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:82-104`).

Copied digest strings alone are insufficient when recomputation is required; each auditor needs an immutable read-only evidence snapshot with exact root identity and recomputation instructions, or separately authorized read-only access to the create-once roots (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:65-70`). This plan creates no such access authority.

### 2.4 Required execution and output

Each flagship executes the same mandated suite; choosing a substitute command or inferring the anomaly set is forbidden, and inability to execute returns BLOCK (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:82-104`). For each new regression test claimed as closure evidence, each auditor reproduces RED against the exact pre-fix behavior or an equivalent mutation, restores the accepted implementation, reproduces GREEN, and labels evidence supplemental if neither arm can be demonstrated (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:106-116`).

Recommended output names:

- `AUDIT2_CLAUDE_T0_<date>.md`
- `AUDIT2_CODEX_T0_<date>.md`

Each auditor writes exactly one independent report with one overall verdict. The report includes the frozen SHA, worktree path, pre/post cleanliness evidence, exact suite command and real output, identity recomputations, D026 result per claimed closure, limitations, and every finding. A required finding names the exact file, observed behavior, expected behavior, and a reproducible command or comparison (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:118-124`).

## 3. Audit 3 with Gate 6 dispatch plan (R24)

### 3.1 Dispatch point and subject

Dispatch only after WP-A evidence has been captured and R23 has frozen the final exact SHA/artifact; this freeze is distinct from Audit 2's pre-WP-A checkpoint (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:61-63`). Audit 3 and Gate 6 review that exact final artifact plus the captured WP-A staging evidence package, after the staging host has been discarded and before Gate B (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:973-978`).

Recommended packaging is **two flagship sessions total**, with each session independently covering both the Audit 3/Gate-5 and Gate-6 subscopes. This applies the T0 headcount of two rather than silently multiplying it per gate (`AGENTS.md:33-35`, `AGENTS.md:48-50`). Each report still returns one overall verdict; it contains separate Gate-5 and Gate-6 determinations so a required defect in either subscope makes the overall result non-accepting.

Audit 3 re-derives the DISARMED VPS invariant map from the frozen artifact and captured WP-A evidence, confirming the required COVERED/SMALL-GAP invariants have passing Ubuntu evidence; Gate 6 performs the security review on those same frozen inputs (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:860-864`, `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1023-1025`). Both are artifact- and evidence-level reviews: they do not rerun Ubuntu tests and require no live staging host (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:977`, `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1201-1205`).

### 3.2 Independence mechanics

Use the same independence pattern as Audit 2: two separate audit-only worktrees at the same full final SHA, fresh standalone prompts, no implementer-session context, no resume/continue, no cross-sharing until both initial reports are sealed, and recorded clean pre/post state (`AGENTS.md:54-70`, `AGENTS.md:93-96`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:26-32`).

### 3.3 Identical inputs to each flagship

Give both sessions the same frozen packet containing:

- the Audit 3/Gate 6 scope contract and controlling plan/rules;
- the full final SHA, base, exact diff, frozen file list, ancestry, path manifest, artifact/manifest hashes, and unchanged-bits conclusion;
- the accepted Audit 2 close record and the final WP-S/WP-L/WP-I/WP-A composition record;
- the captured WP-A staging evidence package and final invariant map, including every COVERED/SMALL-GAP row and its immutable Ubuntu evidence binding;
- the frozen security-review evidence/checklist; and
- any mandated local/frozen suite command and exact baseline applicable to this checkpoint.

The final SHA/artifact, ancestry, path manifest, hash, and captured evidence are required final-freeze inputs (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1021-1025`). The generic audit-session contract limits inputs to scope, plan, actual diff/files, test evidence, and repository rules, without implementer context (`AGENTS.md:93-96`).

**UNKNOWN:** the documents read do not supply a freeze-time Audit 3/Gate 6 manifest schema, an exact security checklist, or a mandated local-suite command/baseline. The final dispatcher must settle those fields in one authoritative R23-bound packet before launch; the existing plan establishes the artifact/evidence scope but not those dispatch details (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1023-1025`).

### 3.4 Required output

Recommended output names:

- `AUDIT3_GATE6_CLAUDE_T0_<date>.md`
- `AUDIT3_GATE6_CODEX_T0_<date>.md`

Each session writes one independently sealed report with one overall verdict and two explicit determinations:

1. **Audit 3/Gate-5:** invariant-map re-derivation from exact frozen inputs.
2. **Gate 6:** security-review result on the exact same final identity and captured evidence.

Each report records exact identity and cleanliness proofs, every command/comparison and real output, the invariant/evidence crosswalk, security findings, limitations, and reproducible required findings. This is a proposed output layout applying the canonical one-session/one-verdict and finding rules (`AGENTS.md:93-105`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:118-124`).

## 4. Verdict, Lead reproduction, and repair rules

For every session, the only verdicts are:

- `PASS`: no required changes;
- `PASS-WITH-NITS`: accepting, optional nits only and zero required repairs;
- `REQUEST_CHANGES`: at least one required repair; or
- `BLOCK`: workflow cannot safely continue (`AGENTS.md:98-105`).

Checkpoint acceptance requires accepting verdicts from both flagships and no unresolved required finding that the Lead reproduced on real source. The Lead independently reproduces each required finding; a finding that does not reproduce is recorded with evidence rather than silently discarded (`AGENTS.md:87-89`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:120-124`). This dispatch plan makes no acceptance decision.

For a required repair, the prior artifact's acceptance never carries forward: repair, freeze a new exact SHA/artifact, and rerun the affected audit on the new identity. T0 permits at most three non-accepting rounds; after the third, stop and report to the owner without a fourth round (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:982-984`; `AGENTS.md:107-109`).

After the staging host is discarded, an Audit 3/Gate 6 repair is hostless only when the implementer states and the Lead confirms that it cannot invalidate the specified WP-A runtime invariants/evidence. If it would invalidate executed-Ubuntu evidence, the result is BLOCK pending new owner Gate-A-class staging authority outside the existing budget (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:855-858`, `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1683-1689`).

The 6 h WP-R pool pays only for audits and re-audits. Required repairs route to the counterpart implementer and are separately contingency-funded after Lead sign-off; this plan does not spend, move, or authorize either pool (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:847-853`).

## 5. Empirical comparators from tonight

These comparators establish workload shape and output volume. They do **not** establish end-to-end auditor hours.

### Comparator A — Codex Pathscope execution audit

The Pathscope retry was one fresh `gpt-5.6-sol` T1/high session over one frozen subject and four named artifacts; it returned `REQUEST_CHANGES` with three required findings (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:1-13`, `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:51-56`).

Its actual execution included a 472-line, 27,699-byte published harness; the harness produced transcript files of 768, 1,557, 150, and 324 lines and reproduced seven determinism pairs (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:62-108`). It additionally executed five C-3 shapes with literal R4/R5 RED/GREEN, six C-4 shape/site cases, adjacent complete-grammar fixtures, seven mutation copies, and carried-fence checks (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:114-160`, `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:183-270`). The resulting audit report is 361 lines and ends with the non-accepting disposition (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:314-361`).

### Comparator B — Claude Bridge-suite anomaly audit

The independent Claude T1 audit reviewed three changed files containing two repairs and one implementer report; its report verified the declared delta and found no undeclared product-code change (`7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:39-57`). The auditor was fresh `claude-opus-5`, independent from the Codex implementer, and returned `PASS-WITH-NITS` with four optional nits and no required repair (`7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:3-17`). The Lead's current-tree adjudication binds that audit to commit `7d4e9a96` (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:7-17`).

The Claude auditor performed an independent real-test mutation RED/GREEN rather than trusting the implementer's inline proof (`7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:162-201`). It ran the 1,021-test suite four times; two recorded runs took 75.35 s and 97.15 s, and it also ran the two repaired tests in isolation (`7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:228-255`). The independent report is 373 lines and ends with a provisional `PASS-WITH-NITS` (`7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:344-373`).

### What the comparators do and do not support

The Pathscope report supplies a date, model, effort, and session ID but no start/end timestamps (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:3-24`). The Claude report likewise identifies the date/model and records test durations, but it does not record an end-to-end session start/end pair (`7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:1-17`, `7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:228-245`). Therefore neither comparator can be converted honestly into a sourced hands-on-hour rate.

**Explicit extrapolation, not a source:** a full-freeze T0 session should be treated as at least as demanding as these narrow T1/high sessions because Audit 2 adds frozen identity, two work-package closure systems, staging evidence, chain of custody, full-suite baseline, D026, authority/budget, and two proof grammars, while Audit 3/Gate 6 adds a final-artifact invariant-map re-derivation and security review (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:26-37`; `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:860-864`). T0 also raises effort from `high` to `xhigh` and requires two independent flagships per checkpoint (`AGENTS.md:33-36`). This comparison supports caution about the reserve; it does **not** support inventing a replacement hour range.

## 6. Reserve conclusion and owner message

### Conclusion

**R21: NO SOURCED ESTIMATE. R24: NO SOURCED ESTIMATE.** The record explicitly says the roster/state do not supply separate prices and instructs the team to obtain timed executions rather than allocate the shared reserve twice (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60`, `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:63`).

The 6 h reserve is **not plausibly sufficient as a reliable closure reserve**. Under the current roster it must cover four first-pass xhigh flagship sessions: two for Audit 2 and two for combined Audit 3/Gate 6 (`AGENTS.md:33-35`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:9-18`). Six aggregate hours divided across those four sessions is **1.5 h per first-pass session**, with zero allowance for Lead finding reproduction or any re-audit. That is arithmetic from the sourced pool and roster, not a guessed duration. The two real narrow T1 comparators each produced more than 360 lines after substantive execution, so assuming every broader xhigh session will close inside 1.5 h is unsupported extrapolation, not evidence (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:314-361`; `7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:344-373`).

Parallel execution could reduce elapsed wall-clock time, but it does not create more aggregate auditor-session hours. **UNKNOWN:** the plan does not state whether its 6 h is additive auditor labor or elapsed wall-clock accounting. A written owner/ledger interpretation would settle that; the reserve sentence only defines one aggregate audit-only pool and an exhaustion BLOCK (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:841-853`).

### Exact message to Barış before spending the reserve

> The existing six hours are one hard audit-only pool for Audit 2, Audit 3, Gate 6, and every re-audit; they are not six hours per checkpoint (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:841-853`). Current permanent rules require four independent xhigh flagship first-pass sessions in total: Claude and Codex for Audit 2, then Claude and Codex for combined Audit 3/Gate 6 (`AGENTS.md:33-35`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:9-18`). That leaves an arithmetic average of 1.5 pool-hours per session before any re-audit. Tonight's real audits show substantial execution and 361/373-line outputs, but their end-to-end times were not recorded (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:314-361`; `7d4e9a96:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:344-373`). Therefore there is no honest replacement hour estimate, and R21/R24 must remain `NO SOURCED ESTIMATE` pending timed executions (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60`, `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:63`). Before Audit 2, choose explicitly whether (a) the six-hour pool remains a hard cap, accepting BLOCK if it is exhausted, or (b) a larger audit-only reserve is separately authorized and ratified. Do not borrow repair contingency; the plan separates repair and audit funding (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:847-853`). Meter both Audit 2 sessions, then use those actuals to price Audit 3/Gate 6 before dispatch.

That message preserves the active plan's exhaustion rule and separation between audit and repair funding (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:847-853`). It requests an owner decision; it does not spend, reallocate, or authorize funds.

## 7. Measurement record needed to replace `NO SOURCED ESTIMATE`

For each future flagship session, record in the immutable audit report:

- monotonic start and finish timestamps;
- model, effort, checkpoint, frozen SHA, and worktree identity;
- active review time, mandated-suite runtime, evidence-reproduction runtime, and report-writing time;
- commands executed, output bytes/lines, suite counts, D026 pairs, and finding count;
- verdict and whether a re-audit was required; and
- separate Lead reproduction time.

After both Audit 2 reports are sealed, total the two actual flagship-session hours and Lead reproduction time, subtract only that measured amount from the single pool, and present the observed data to the owner before Audit 3/Gate 6. The catalogue itself calls for timed auditor executions and forbids inventing or double-allocating a split (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60`, `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:63`).
