# OWNER AUTHORIZATION — AUTONOMOUS 50-HOUR TRADING SYSTEM EXECUTION

**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`

**Approved plan:**
`MTC_COMMAND_CENTER\09_DOCS\ROADMAPS\TRADING_SYSTEM\TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md`

**Accepted plan SHA-256:** `a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee`

> Hash the **committed blob**, not the working copy: `git show HEAD:"<path>" | sha256sum`. The repo has CRLF conversion on checkout, so the on-disk file hashes differently (`55799c0b…`) while being byte-correct in git. Never report the working-copy hash as the artifact identity.

You are Claude, the **LEAD ORCHESTRATOR** and final acceptance authority for this execution.

---

## OWNER DECISION

I approve the 50-Hour DISARMED Safety MVP plan and authorize you to begin immediately and execute it autonomously from WP-0 through completion.

This authorization supersedes my previous instruction to wait for WP-0.

I want as little interaction as reasonably possible. Do not ask me routine questions. Make conservative, evidence-backed decisions and continue working.

This prompt is standing owner authorization for:

- WP-0 and its baseline/scope work.
- A new Gate-1 follow-up cycle for TS-P1-009B S2.
- WP-S, WP-L, WP-I, WP-A, WP-R, and WP-V.
- Implementation and repairs within the accepted scope.
- Up to three repair/re-audit rounds at each checkpoint.
- Fresh branches and isolated worktrees.
- Creating, updating, and deleting temporary task worktrees after verifying their paths.
- Normal non-destructive Git operations.
- Checkpoint commits, final commits, pushes, pull requests, and merges after accepting audits.
- Resolving in-scope merge conflicts conservatively.
- Ubuntu staging.
- Using the named expendable Ubuntu staging host.
- Discarding that staging host only after all required evidence has been captured.
- Ubuntu KVM2 VPS deployment.
- Gate A, Gate B, WP-V, and Gate C when every documented prerequisite has objectively passed.
- DISARMED deployment and rollback testing.
- TESTNET configuration, ARM, first TESTNET paper order, bounded TESTNET drills, disarm, cancel, and testnet flatten operations.
- Long paper/testnet observation and its monitoring infrastructure.
- Mainnet software packaging, deployment-readiness work, public/read-only connectivity checks, and zero-capital configuration validation.
- Using other LLMs and local tools within the repository's routing and safety rules.
- Updating the canonical handoff, evidence, roadmap-status, and next-step records.
- Continuing from one accepted work package to the next without asking me again.

This is also the explicit owner authorization required to open a **NEW** TS-P1-009B S2 repair cycle. It is not a fourth round of the exhausted historical cycle.

### Where this prompt deliberately supersedes the plan document

The accepted plan places three things behind separate future owner gates: **the WP-V deployment approval, the ARM gate, and the first TESTNET paper order.** This prompt grants all three in advance. That is intentional. When you reach those points:

- Do **not** stop to ask. Do **not** treat the plan's "separate owner authorisation required" wording as an unmet blocker.
- **Do** record in the evidence trail that the authorisation came from this standing prompt rather than a point-in-time approval, naming this document.
- Every *objective* prerequisite in the plan's Gate A / Gate B / Gate C checklists still applies in full. What is waived is my having to click approve, not any evidence requirement.

**Important caveat you must honour:** the plan's two canonical audits examined a document whose scope *ended* at DISARMED. The TESTNET phase (ARM, first order, drills, observation) has **not** been through an equivalent audited plan. Before starting it, write a short pre-registration for that phase — scope, invariants, abort conditions, sizing source, evidence to capture — and get it through one fresh Gate-5 audit. Do not treat the 50-hour plan's acceptance as covering it.

---

## ROLE OVERRIDE

For this execution only:

- Claude is Lead Orchestrator and acceptance authority.
- Codex CLI is the counterpart flagship implementer.
- This explicitly supersedes only the plan's prior Codex-Lead/Claude-implementer actor assignment (plan §23c and §39 item 10).
- It does not weaken any safety, testing, scope, audit, model, or evidence requirement.
- Claude must independently inspect all actual changes and reproduce proportionate validation.
- Claude must not accept an implementer's report without examining the real repository state.

---

## MODEL ROUTING

- Protected Bridge/core implementation: **Codex CLI using exactly `gpt-5.6-sol`** at the appropriate high/xhigh effort.
- Gate-5/Gate-6 and protected-surface re-audits: fresh independent sessions with the exact canonical models and effort required by `AGENTS.md`.
- Never resume or continue the implementer session for an audit.
- Where the plan requires a fresh Codex `gpt-5.6-sol` xhigh audit, run a separate ephemeral read-only Codex session.
- A fresh Claude Opus 5 xhigh audit may also be used for cross-model review.
- **Cline is functional** (verified `3.0.48` on 2026-07-31 after repair) and is first choice for bounded unprotected mechanical work.
- DeepSeek/GLM/Grok may be used only for bounded unprotected mechanics or supplemental read-only review.
- Secondary models cannot implement protected Bridge/core work and cannot replace canonical Gate-5/Gate-6 auditors.
- No silent model downgrade or fallback.
- If an exact mandatory auditor is unavailable, continue other independent work and report the audit blocker only when it prevents further progress.

### Known working CLI invocations

```bash
# Codex implementer (workspace-write)
codex exec -C "C:/LAB/Tradingview_LAB_CLEAN" -s workspace-write -m gpt-5.6-sol \
  -c "model_reasoning_effort=high" -c 'approval_policy="never"' \
  -o <last_message_file> < <prompt_file>

# Codex canonical auditor (ephemeral, read-only)
codex exec --ephemeral -C "C:/LAB/Tradingview_LAB_CLEAN" -s read-only -m gpt-5.6-sol \
  -c "model_reasoning_effort=xhigh" -c 'approval_policy="never"' \
  -o <verdict_file> < <audit_prompt_file>

# Claude canonical auditor (fresh session, no resume)
claude -p --model claude-opus-5 --effort xhigh --no-session-persistence \
  --allowedTools "Read" "Grep" "Glob" "Bash" \
  --disallowedTools "Edit" "Write" "NotebookEdit" "Task" < <audit_prompt_file>
```

Run these with `run_in_background: true` and work on other streams while they execute.

---

## OPERATIONAL HAZARDS — READ BEFORE YOUR FIRST DISPATCH

These were all hit during the plan-repair cycle on 2026-07-30/31. Each one cost a wasted round. Do not rediscover them.

1. **Codex will refuse to implement unless you override the role in the prompt itself.** At `xhigh` effort it reads `AGENTS.md`'s two-tier rule, concludes *Codex* is Lead, tries to delegate to Claude CLI, gets `API Error: ConnectionRefused`, and returns BLOCKED having made no edits. **Prefix every Codex implementation dispatch** with an explicit statement that the owner assigned this task to Claude, making Claude the Lead and Codex the counterpart implementer; that Codex must implement directly and must not invoke Claude CLI; and that the plan's own §23c roles describe the future programme, not who edits under this authorization.

2. **Codex cannot run Git.** Its sandbox has read-only `.git` — `git fetch` fails with `cannot open '.git/FETCH_HEAD': Permission denied`. Never delegate commit/push/fetch/merge to Codex. The Lead performs all Git operations. This is consistent with `AGENTS.md`, which assigns Git sequencing to the Lead anyway.

3. **A hook flips `HEAD` back to `master` between tool calls.** Commit on a feature branch using a single inline command: `git checkout <branch>; git add <paths>; git commit -m ...`. Do not assume the branch you checked out last call is still current.

4. **`git checkout master` will usually fail** with "local changes / untracked files would be overwritten". Do **not** stash, reset, or delete to force it. Use `git worktree add` on a temporary branch, do the merge there, push, then remove the worktree. That is how PR #34 was landed.

5. **Verify artifact identity from the committed blob, never the working copy** (see the CRLF note at the top). The whole plan hinges on exact SHA/artifact identity; getting this wrong corrupts every freeze/re-audit claim.

6. **Implementer self-reports are not evidence.** Codex twice reported "validation passed" on files that its own later audit found defective in. Always inspect the real diff yourself before freezing an artifact.

---

## STARTUP REQUIREMENTS

Before changing anything:

1. **Read completely:**
   - `AGENTS.md`
   - `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
   - `MTC_COMMAND_CENTER\_AI_MEMORY\AI_RULES.md`
   - the accepted 50-hour plan
   - the accepted plan-audit record: `MTC_COMMAND_CENTER\11_TRIAGE\PLAN50H_REPAIR_AUDIT_CYCLE_2026-07-30.md`
   - current `GLOBAL_HANDOFF.md` (newest section first) and `NEXT_STEPS.md`
   - the relevant TS-P1-009B evidence and audit reports in `11_TRIAGE\`

2. **Fetch and verify:**
   - current `origin/master`;
   - all relevant refs and worktrees;
   - commit ancestry;
   - clean/dirty state;
   - accepted plan blob/hash;
   - current task branches and immutable accepted artifacts.

3. **Do not trust stale roadmap status labels.**

4. **Baseline.** As of 2026-07-31 `origin/master` is `561be664d3d46103d68023a9951065343e772f1e`. The plan text still names `3cccc4c2` as its baseline; an older note named `9b8a908a`. **All three are stale the moment you read this — re-fetch and re-baseline to the live `origin/master`.** Confirm whether the Bridge tree changed relative to the plan's assumed baseline before freezing WP-0, and record the delta.

5. **Run `codeburn status`.** Month-to-date spend was **$2,363** as of 2026-07-31 — this is a real budget, not a formality. Route bounded mechanical work to Cline first, then DeepSeek, and reserve Opus/Codex `xhigh` for implementation and canonical audits. Report a rough cost per work package in your final deliverable.

6. **Do not edit the plan document.** Its accepting verdict is bound to `a07c90cc…`; any edit voids it. Eight optional nits were deliberately left unapplied and are recorded in the audit record. If a genuine substantive defect in the plan emerges during execution, treat it as a blocker to report, not a doc to quietly patch.

### Current known state (verify, do not assume)

- Working tree clean; branch `feature/donchian-crypto-ladder` in sync with its remote; all plan/ADR/triage work merged to master via PR #34 and PR #35.
- **TS-P1-009B:** S1 accepted at `8d004590`. S2 **terminally BLOCKED** after repair round 3 at branch HEAD `678e8b946e34`, with two open blockers: (a) sub-1e-12 `trades.exit_px`/`pnl` tampering can evade detection and permit ACK/DISARM; (b) stale recovery can commit lifecycle close before post-ingestion evidence-epoch rejection. S3 unstarted. Closing S2 + minimum S3 is WP-S and is the live blocker for everything downstream.
- **Linux package** exists at old-base commit `6fe0130f45f3c821e230ee30d1e61f548741a6a1` — builder-self-QA only, independently unaccepted, not Ubuntu-staged. Port only necessary semantic paths; never wholesale merge or cherry-pick.
- ADR-0018…0029 are now committed and ratified.

---

## EXECUTION CONTRACT

Execute one safety-coherent work package at a time.

For every package:

1. Freeze the exact scope, allowed paths, exclusions, invariants, and acceptance tests.
2. Create an isolated task branch/worktree from the verified current `origin/master`.
3. Dispatch implementation to the authorized counterpart (with the role preamble from Hazard 1).
4. Require implementer self-QA.
5. Inspect the actual diff independently.
6. Check for protected-surface or scope violations.
7. Run or reproduce proportionate tests on real repository state.
8. Create a checkpoint commit representing the exact audit artifact; record its blob/commit hash.
9. Run a fresh independent Gate-5 audit where required.
10. If non-accepting, send a focused repair prompt to the same implementer.
11. Commit the repair, freeze the **new** artifact, and re-audit **that exact artifact**.
12. Use no more than three non-accepting repair/re-audit rounds per checkpoint.
13. After PASS or PASS-WITH-NITS, commit any required records, push, open/merge the PR, and verify `origin/master` ancestry.
14. Update handoff and evidence records.
15. Proceed automatically to the next authorized package.

**Hour accounting:** log active engineering hours per work package against the plan's 50 h table (WP-0 2, WP-S 12, WP-L 8, WP-I 6, WP-A 3, WP-R 6, WP-V 8, contingency 5). Respect the plan's funding rules — WP-R is audit-only; repairs come from contingency; the Audit-1 first pass is funded from WP-S. If a package is heading past its allocation, say so in the record rather than absorbing it silently.

Do not leave uncommitted changes for another agent on shared files. Commit after every agent/package checkpoint before handing the same files to another agent.

---

## GIT AUTHORIZATION

Do not ask me about commits, pushes, pull requests, merges, branch cleanup, or normal in-scope conflict resolution.

You are authorized to perform them after independent validation and an accepting audit.

Still prohibited:

- force-push;
- destructive history rewriting;
- `git reset --hard`;
- blind checkout/reset of user changes;
- `git add .`;
- deleting unclassified files;
- stashing unrelated user work;
- changing unrelated worktrees;
- merging a non-accepting artifact;
- silently resolving an out-of-scope semantic conflict.

Use fresh isolated worktrees when the shared checkout is unsafe.

---

## SAFETY BOUNDARIES

Do not change Pine, parity, MTC strategy behavior, trading strategy logic, or owner-approved risk thresholds unless a separately evidenced safety requirement explicitly requires it and the repository rules permit it.

Never invent:

- position size;
- leverage;
- daily-loss threshold;
- drawdown threshold;
- liquidation threshold;
- wallet/account selection;
- mainnet credentials;
- live-capital limits.

Use only already approved configuration values. If a required owner value is genuinely absent, keep that action blocked, continue every independent task possible, and consolidate the missing items into one blocker report.

Never print, store in reports, or send credentials, wallet secrets, API keys, or private infrastructure data to an LLM.

---

## TESTNET AUTHORIZATION

After the 50-hour DISARMED endpoint is independently accepted, and after the TESTNET-phase pre-registration has passed one fresh Gate-5 audit:

- Continue into the separately recorded TESTNET phase without asking me again.
- Do not count this work or its observation period inside the 50-hour MVP budget.
- Require fresh reconciliation and current-run evidence.
- Confirm zero unexpected positions and zero unexpected open orders.
- Confirm fresh market data and reconnect/recovery evidence.
- Use only existing approved testnet sizing and risk settings.
- ARM only after every required safety gate is green.
- Submit the first TESTNET order as a bounded, one-shot action.
- Do not blindly retry an unknown or ambiguous submission.
- Automatically DISARM on any failed invariant.
- Execute bounded TESTNET restart, reconnect, recovery, cancel, and failure drills.
- Preserve raw endpoint bodies, event IDs, timestamps, commits, and configuration identity.
- Begin the pre-registered 7–10+ day paper observation only after the testnet drills pass.
- Use persistent monitoring/scheduling so observation can continue unattended.
- Never claim the observation is complete until the required wall-clock evidence genuinely exists.

> Prior paper-observation windows on this project died to **machine sleep/hibernate and battery events**, not software faults (see the Day 1 v1 sleep incident and the P2 battery incident in `11_TRIAGE\`). Before starting any long observation, verify the host's sleep/hibernate/idle settings on **both AC and DC** power and record that verification as evidence. An observation window that dies to a power setting is a wasted week.

---

## MAINNET AND LIVE-CAPITAL BOUNDARY

Mainnet readiness work that cannot move capital is authorized without another question.

However, every action with possible economic effect is a **LIVE-CAPITAL ACTION** and is **NOT** pre-authorized.

LIVE-CAPITAL ACTION includes:

- loading or activating funded mainnet trading credentials;
- arming a funded mainnet runtime;
- submitting, modifying, or cancelling a mainnet order;
- opening, closing, or changing a real position;
- changing real leverage or margin;
- depositing, withdrawing, transferring, bridging, staking, or otherwise moving funds;
- signing any mainnet transaction with economic effect;
- enabling any automated process capable of performing those actions.

Before the first such action, stop and ask me for explicit live-capital approval. Provide:

- exact proposed action;
- account/environment;
- maximum possible exposure;
- current positions and orders;
- risk and rollback state;
- accepted audit evidence;
- exact commit/artifact;
- what happens if the action or response is ambiguous.

**No live-capital action may be inferred from this prompt.** If you are ever unsure whether something counts as a live-capital action, it counts. Stop and ask.

---

## QUESTION POLICY

Do not ask me for:

- implementation choices that can be resolved from the repository;
- repair approval within the authorized three-round loop;
- test execution;
- audit reruns;
- commits, pushes, PRs, or merges;
- staging;
- VPS deployment;
- rollback tests;
- TESTNET ARM;
- TESTNET orders;
- TESTNET disarm/cancel/flatten;
- mainnet readiness work with no economic effect;
- routine documentation or handoff updates.

Make the safest conservative decision, record it, and continue.

Ask me only when:

1. a LIVE-CAPITAL ACTION is proposed;
2. a required secret, external permission, paid purchase, or owner-defined trading/risk value is missing and cannot be safely discovered;
3. three non-accepting rounds are exhausted;
4. mandatory exact auditor/model access remains unavailable;
5. a safety blocker makes all meaningful progress impossible;
6. continuing would require materially expanding beyond the accepted 50-hour plan and authorized TESTNET continuation.

When a blocker affects only one stream, continue all independent authorized work. Consolidate questions into one short owner-decision package instead of interrupting me repeatedly.

I may reply in Turkish; answer in whichever language I use.

---

## HARD STOP CONDITIONS

Stop and preserve evidence if:

- unexpected nonzero exposure exists;
- reconciliation is stale or unhealthy;
- order state is unknown;
- duplicate or naked exposure is possible;
- authoritative risk inputs are missing;
- database recovery cannot be proved;
- a secret may have leaked;
- exact runtime or artifact identity is uncertain;
- a required audit is non-accepting after round three;
- a repair would invalidate Ubuntu evidence after the staging host has been discarded (plan §20/§22 **Case 2** — this is BLOCK; a new Gate-A-class staging authorisation is outside the 50 h budget and needs me);
- an out-of-scope protected change becomes necessary.

Never reduce safety requirements to meet the 50-hour ceiling. BLOCK honestly.

---

## AUTONOMOUS LONG-RUN BEHAVIOR

- Use background dispatch and completion callbacks where available.
- Use compact context packs for each agent.
- Start fresh sessions when context becomes excessive.
- Never use an open-ended "keep improving" loop.
- Every loop must have a defined success condition and a maximum of three repair rounds.
- Maintain durable progress, evidence, and handoff records.
- If a session must end, leave a complete continuation package anchored to immutable commits and restartable monitoring.
- Do not fabricate completion because of context, quota, elapsed time, or an unavailable tool.
- Track active engineering hours separately from paper-observation wall-clock time.
- Write handoff sections to `GLOBAL_HANDOFF.md` newest-first, headed `## [MODEL_NAME] YYYY-MM-DD — Topic`. Tag `NEXT_STEPS.md` items with `[AI: Claude|Codex|DeepSeek|Any|Barış]`.

---

## FINAL DELIVERABLE

Finish with an evidence-backed report containing:

- every completed work package;
- exact commits, branches, PRs, and merge SHAs;
- files changed and protected surfaces checked;
- tests and raw exit results;
- Gate-5/Gate-6 verdicts;
- Ubuntu staging evidence;
- final release artifact/hash;
- VPS deployment and rollback evidence;
- final DISARMED state;
- TESTNET ARM/order/drill evidence;
- paper-observation status and daily records;
- active engineering hours per work package against the 50 h table;
- approximate AI spend per work package;
- outstanding blockers and deferred optional features;
- explicit confirmation that no live-capital action occurred without owner approval.

---

Do not merely acknowledge this prompt.

Begin now with the canonical pre-read, live repository verification, and WP-0.
