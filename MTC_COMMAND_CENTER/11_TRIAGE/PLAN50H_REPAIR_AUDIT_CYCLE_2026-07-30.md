# 50-HOUR PLAN — DOCUMENTATION REPAIR + AUDIT CYCLE (2026-07-30)

**Status: ACCEPTED.** Both canonical audits returned accepting verdicts with zero required repairs.

Owner-authorised, documentation-only. No implementation, Git, VPS, staging-host, deployment, TESTNET, or ARM action was taken or is authorised by this cycle.

## Target

`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md`

| | SHA-256 | Lines |
|---|---|---|
| Baseline (owner-supplied, verified match) | `87a25792d622549c9f66717e059067e07fa627023f4d78b67e8208cb37254e82` | 1794 |
| After Codex edit 1 (four repair classes) | `d67c39858466ac6b7767fe759b4865d55197fc54ba330e38baf8563e904f6c2d` | 1854 |
| After Codex edit 2 (Lead pre-audit: Audit-1 double-funding) | `1f3abb995c5b2bfc4ba55910a42e88aeb378b7cdbfd6efa85299aa3fff9c3ded` | 1862 |
| After Codex edit 3 (audit round 1 repairs + 5 nits) | `06e2a4c559d023273f7a904a10c0cdfc6411d1abdae34c021eb8b17e32478ec3` | 1879 |
| **FINAL — accepted** | **`a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee`** | **1879** |

## Roles

- **Lead Orchestrator / acceptance authority:** Claude `claude-opus-5` (task received directly from owner).
- **Document implementer (sole editor):** Codex CLI `gpt-5.6-sol`.
- **Canonical auditors:** Claude `claude-opus-5` effort `xhigh` (fresh, `--no-session-persistence`); Codex `gpt-5.6-sol` effort `xhigh` (`--ephemeral --sandbox read-only`).
- **Supplemental (non-acceptance):** DeepSeek CLI, read-only `--approval-mode plan`.

## Audit rounds (max 3 non-accepting; cycle ended inside the limit)

| Round | Artifact | Claude `claude-opus-5` xhigh | Codex `gpt-5.6-sol` xhigh | Net |
|---|---|---|---|---|
| 1 | `1f3abb99` | REQUEST_CHANGES — 3 required | REQUEST_CHANGES — 2 required | non-accepting |
| 2 | `06e2a4c5` | PASS-WITH-NITS — 0 required | REQUEST_CHANGES — 1 required | non-accepting |
| 3 | `a07c90cc` | **PASS-WITH-NITS — 0 required** | **PASS-WITH-NITS — 0 required** | **ACCEPTED** |

Two non-accepting rounds used of the three permitted.

## The four commissioned repairs

**1. Gate-A and staging lifecycle.** Baseline discarded the staging host in five places (§18 scope, §23a step 2, Gate B item 1, §23b step 9, §34 diagram) while §23a step 3 and §34 simultaneously ran WP-A *on* that host. Now: local/static port work permitted pre-Gate-A; no Ubuntu execution of any kind before Gate A; the single Gate-A-authorised host retained through WP-L Phase 2 — Ubuntu revalidation → WP-I staging verification → WP-A; discard only after WP-A completes and all required staging evidence is captured. A canonical four-rule `## Staging Host Lifecycle` block was added to §18; §17, §19, §23a, §23b, Gate B, §34 and §36a were aligned to it.

**2. Contingency and audit sequencing.** Baseline §34 drew the whole WP-R block (Audits 1+2+3) *after* the final SHA freeze, contradicting §20/§23a/§25 which place Audit 1 after WP-S and Audit 2 after WP-L+WP-I. No repair→refreeze→re-audit loop existed anywhere. Now: audits sit at their real checkpoints in both §23a and §34; WP-R and contingency are drawn as non-sequential side-car funding; the loop *repair (contingency) → freeze new exact SHA/artifact → re-audit that exact artifact (WP-R)* is explicit in six places (§20, §22, §23a, §23b, §25, §34), with acceptance never carrying forward and a three-round cap per checkpoint. WP-R remains strictly audit-only; unfunded routes (WP-R exhaustion, contingency exhaustion, WP-0/WP-A overrun) are openly BLOCK-routed rather than absorbed.

**3. Model-role wording.** The prior GLM-5.2 plan edit is now marked, verbatim in §23c and §39 item 10, a **"docs-only and non-precedential exception"** scoped to documentation editing of this file only. Both passages explicitly deny GLM, DeepSeek, Grok, NVIDIA, Cline and any other secondary model authority over protected Bridge/core-runtime implementation and over canonical Gate-5/Gate-6 audits, and restate the `AGENTS.md` roster. Auditors confirmed those model names appear nowhere else in the document.

**4. Phase terminology.** Every ambiguous bare "Phase 2" eliminated (10 baseline occurrences). Three binding terms defined in a new §6.1: `WP-L Phase 2 — Ubuntu revalidation`, `Deferred Delivery Stage 2`, `canonical Master Roadmap Phase 2`.

## Two additional defects found and fixed during the cycle

- **Audit-1 double-funding** (Lead pre-audit inspection, later confirmed by both auditors): §16 budgeted 2 h + 2 h of Gate-5/6 audit inside WP-S's 12 h while §20/§34 assigned the same Audit 1 to WP-R's 6 h. Resolved without changing any number — WP-S's allocation funds the Audit-1 *first pass* only (and `Gate-5/6` → `Gate-5`, since Gate-6 is WP-R-funded); WP-R funds Audit 2, Audit 3, Gate-6 and every re-audit at all three checkpoints; contingency never funds audit work.
- **Post-discard repair loop was unexecutable, unfunded and unrouted** (Claude audit round 1): §20/§22 mandate a refreeze + re-audit after *any* repair, but a repair arising at Audit 3 or Gate-6 would invalidate WP-A's Ubuntu evidence after the only authorised host was already discarded — Gate A spent, Gate B authorises no staging, WP-V's VPS not yet existing, no hours funded. Resolved conservatively: Audit 3 and Gate-6 are declared artifact- and evidence-level reviews over the frozen SHA plus the captured staging evidence package, requiring no Ubuntu execution and no live host ("independently reproduces" = re-derives the map from frozen inputs). Post-discard repairs then split — **Case 1** (provably cannot invalidate executed-Ubuntu evidence; implementer states which invariants, Lead confirms) runs the normal hostless loop; **Case 2** (would invalidate that evidence) is **BLOCK** with owner report, since a new Gate-A-class staging authorisation and its hours are outside this budget.

## Budget — unchanged and independently recomputed by both auditors

| Work Package | Budget |
|---|---:|
| WP-0 Scope / Baseline Review | 2 h |
| WP-S TS-P1-009B S2 Closure + Minimum S3 | 12 h |
| WP-L Essential Linux Semantic Port | 8 h |
| WP-I Deps / systemd / State / Rollback / Staging | 6 h |
| WP-A DISARMED VPS Invariant Evidence Overlay | 3 h |
| WP-R Independent Audit Reserve (audit-only) | 6 h |
| WP-V VPS DISARMED Deployment + Verification | 8 h |
| Contingency | 5 h |
| **TOTAL** | **50 h** |

Internal splits also verified: WP-S 4+2+4+2 = 12; WP-L (2+3+1)+2 = 8.

## Safety boundary — verified intact by both auditors

Endpoint is one Ubuntu KVM2 VPS deployed and verified **DISARMED**, private/loopback-only. Hyperliquid **TESTNET / paper-simulated funds only**; mainnet and real capital forbidden. **ARM, the first TESTNET paper order, and long soak observation are outside the 50 hours** and each require separate owner authorisation. No trading thresholds, risk values, credentials, wallet details or infrastructure secrets appear anywhere (Claude ran a regex sweep for keys, wallets, IPs and limits — zero hits). The document authorises no implementation, deployment, VPS, TESTNET, ARM or runtime action.

## Optional nits (carried forward — none blocking)

From the final Claude audit:
1. §18 `Evidence Required` lacks the pre/post-Gate-A phase labels §17 carries (no contradiction; Gate A checklist and §34 disambiguate).
2. Audit-1 *first-pass* overrun has no explicitly named funding route; only the generic §23 "overrun → BLOCK" catches it. §22 already names WP-0/WP-A overruns explicitly — adding Audit-1 first pass would close the last implicit case.
3. §19's reconnect/stale-data invariant block has no disposition sentence (the restart block has one); falls back to the general three-class model, correct by default.
4. §23c/§39 list `claude-opus-5` xhigh on the canonical roster while this plan assigns Claude CLI the implementer role — accurate against AGENTS.md, but a half-sentence noting Claude is ineligible *in this plan* would remove the apparent option.
5. Only "Phase 2" was disambiguated; "Phase 3/4/5/6/7" remain bare (unambiguous today).
6. §19's 3 h breakdown item "existing Ubuntu-test execution" and the separate `## Verification Pass` heading read as one activity described twice — could invite double-counting against the 3 h.
7. §23a heading "Three Sequential Gates" undersells an 11-step sequence covering three audits, Gate-6, two SHA freezes and the discard step.

From the final Codex audit:
8. Executive Summary says "within approximately 50 active AI engineering hours"; "at most" would match the stated hard ceiling.

## Assumptions recorded (unattended decisions)

- **Audit-1 funding.** Chose the resolution that changes no published number: WP-S's internal 2 h + 2 h funds the Audit-1 first pass; all re-audits and Audit 2/3/Gate-6 come from WP-R. The alternative (moving all audit hours to WP-R) would have required inventing a new WP-S split.
- **Post-discard Case 2.** Routed to BLOCK rather than inventing a second staging authorisation or extra hours. Codex's stated default is also conservative: if it cannot be *proven* that a change leaves every applicable executed-Ubuntu invariant valid, it is Case 2.
- **Three-term model.** Round 2 added a fourth binding term (`P2-lite`) to §6.1 while closing an audit nit; the owner's brief mandates exactly three. Reverted in round 3 — §19's scope line now uses `canonical Master Roadmap Phase 2 (P2)`, matching §19 Explicit Non-Goals and §34.
- **Nit deferral.** With one repair round remaining after round 2, only the single required repair was applied. Remaining nits were deliberately not folded in, since each extra edit risked a new finding in the final audit.

## Tooling notes

- **Cline CLI is broken on this machine:** `Error: Cannot find module 'C:\Users\<user>\AppData\Roaming\npm\node_modules\cline\bin\cline'`. Fell back to the DeepSeek CLI for the supplemental read-only check. This is a tooling defect, not a plan defect, and affects the AGENTS.md TOKEN DISCIPLINE first-choice path.
- **Codex refused one dispatch** on a two-tier-role reading, attempting to delegate to Claude CLI (`API Error: ConnectionRefused`). It made no edits and left the file untouched. Resolved by prefixing the task with the owner's explicit role assignment for this cycle and distinguishing the plan's own §23c programme roles from this documentation cycle's edit roles.
- **The target file is untracked** (`?? MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/`), so no committed baseline exists and neither auditor could diff against a prior revision — collateral checks were internal-consistency only. Lead diffs were taken against scratchpad snapshots of each intermediate SHA. Both auditors recommended committing so future cycles have a baseline; committing is outside this cycle's authorisation.

## Repo state

`git status --porcelain` = 89 entries (18 modified, 71 untracked) — identical to cycle start plus this record. No Git command was run at any point. No other repo file was created, modified, or deleted by the repair cycle.

## Next actions requiring owner decision

1. Accept the plan (it now carries the accepting verdict its own §15 WP-0 requires before implementation may start).
2. Decide whether to commit `09_DOCS/ROADMAPS/TRADING_SYSTEM/` so the plan has version history.
3. Decide whether to apply any of the 8 optional nits.
4. Separately authorise WP-0 when ready — no implementation, Git, VPS, staging, TESTNET, deployment or ARM action has begun.
