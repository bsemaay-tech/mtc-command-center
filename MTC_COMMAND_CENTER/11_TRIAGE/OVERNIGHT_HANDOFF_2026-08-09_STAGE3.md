# OVERNIGHT HANDOFF — WP-L P2 Stage 3 onward (2026-08-09 evening → morning)

New Lead session (Claude Fable 5) picks up here. This file is self-contained; read it plus
`AGENTS.md`.

## STANDING RULES (v2 addendum, 2026-08-09 night — owner-stated, binding every session)

1. **NEVER STOP UNTIL MORNING.** This is a continuous autonomous session. Do not end your turn with a
   report and go idle. When the main path is owner-gated, pull the next item from the FALLBACK
   BACKLOG below and keep working. Maintain a self-paced `/loop` the whole night; the loop only ends
   at the morning summary (~06:30) or if literally every backlog item is exhausted AND every
   remaining path needs owner input — and even then keep the heartbeat armed, do not terminate.
2. **PRESERVE FABLE CREDITS — DELEGATE.** You (Fable, the Lead) orchestrate, verify, commit, and
   decide. You do NOT do heavy generation/implementation/audit yourself. Dispatch all substantial
   work to cheaper/other agents: Codex `gpt-5.6-sol` xhigh (audits, host-side execution units),
   Claude Max `claude-opus-5` xhigh (counterpart implementation), GLM-5.2 (second-opinion audits),
   DeepSeek (mechanical). Fable stays lightweight: read results, spot-verify, commit, route. Invocation
   syntax is in the "Operating rules" section below.
3. **ENGLISH ONLY.** All your output and every document/commit/record you write is in English, even
   when the owner writes in Turkish. No exceptions.
4. **ALWAYS END WITH NEXT STEPS.** Every time a task completes, write the next actions to take. If
   anything is needed from the owner, call it out explicitly and separately — and phrase what you
   need from the owner in plain, non-technical language (the rest can be technical). Choose a default
   path so work continues without waiting.

## Current status (verified, HEAD `d5b97594` on `feature/donchian-crypto-ladder`)

Overnight Stage 3 already ran: transport op 01–04 PASS (kit uploaded, remote 9/9 block hashes
verified); **B3 STOP (rc 3)** on a real design gap `B3-GAP-ENV` (see below); **Stage 3B R4-5 PASS**
(the last Windows-unclosable fixture is now closed — RP4-C3 symlink guard proven load-bearing).
Commits `7e9d1c4a`, `ee49a945`, `d5b97594`. Zero service mutation, zero ARM, single-writer held.
Ledger ~28.3 h remaining. Power fix verified (sleep/hibernate=0).

### B3-GAP-ENV — RESOLVED to Option 1 (autonomous, no owner gate needed)

`OVERNIGHT_RESULT_2026-08-09_STAGE3.md` raised three options. **Option 1 (repair the design) is the
authorized path and needs NO new owner gate** — it is design/doc/audit work identical in tier to
today's accepted 3×3 cycle, touches no host, mutates nothing. Options 2 and 3 require host mutation
and are NOT authorized (do not pursue them). So: **proceed autonomously with Option 1** — move the
env-file/manifest-binding admission out of unprivileged RP1-B3 into a root-side deploy-time verify
(T0 design), keep B3's checks 1–3 + ancillary modes unprivileged, then run the full repair→re-audit
cycle (Claude Max implements ↔ Codex re-audits, ≤3 rounds), and re-freeze Stage 1 run-kit (block
hash changes → new frozen kit; a frozen accepted block may never be edited silently). This is the
night's primary fuel. Delegate it per rule 2.

## FALLBACK BACKLOG (non-blocked work — pull in order whenever the main path waits)

1. **B3-GAP-ENV Option 1 repair cycle** (primary — see above): design repair → re-audit → runkit
   re-freeze. Many hours of legitimate delegated work; do this first.
2. **WP-I staging-verification prereg**: draft the WP-I preregistration for its non-BLOCKED checks,
   same rigor as Stage 2 (delegate to Claude Max; Lead verifies + commits).
3. **Audit 2 evidence checklist**: expand/verify the existing draft
   (`AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md`) against the accepted designs and banked evidence.
4. **Proposal status update**: R4-5 is now closed on Linux — update the proposal doc's open-item
   list to reflect it (T3 self-verify, single commit).
5. **Evidence index**: build a per-stage evidence index (RUNID → files → hashes) for the staging unit
   so Audit 2 can consume it fast.
Only after all five are exhausted may the loop idle to pure heartbeat — and even then, keep prepping.

Owner (Barış) wants a continuous all-night autonomous session; keep the pipeline moving until morning.

## Where we are (verified, HEAD `210b0168` on `feature/donchian-crypto-ladder`)

Roadmap: WP-0/WP-S/WP-L P1 merged → **Gate A A-0..A-9 PASS** (`5af8178b`, candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b`, staging DISARMED/loopback) → **WP-L Phase 2 IN
PROGRESS**. Order after: WP-I staging verification → Audit 2 (two-flagship) → WP-A → Gate B → WP-V
(all later, owner-gated).

WP-L P2 command designs went through a full adversarial cycle and are **ACCEPTED** (`4c0d5fc5`,
`WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md`). Staging unit dir:
`11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/`.

- **Stage 1** run-kit frozen + verified: `01_RUNKIT/` (`runkit.tar`, SHA
  `618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53`, 9 block identities = §8.1).
- **Stage 2** preregistration COMPLETE + Lead-verified (`210b0168`): `02_PREREG/` has
  `CANDIDATE_RELEASE_SHA256SUMS` (7058 entries derived read-only from frozen `2ce41e34`, one blob
  spot-verified bit-identical), `PREREGISTRATION.md` (RUNID, evidence paths, remote argv, stdin +
  script hashes), `PREREG_SHA256SUMS.txt`, `TRANSPORT_PLAN.tsv`, `transport_runner.ps1` (ASCII),
  `remote_close_tree.sh`, `run_b3.sh`, `run_r45.sh`, `STAGE2_PREREG_SELF_QA.md`. All scripts
  `bash -n`/`py_compile` clean.

## DO NOW — Stage 3 (owner-authorized this evening)

First real host contact, but **zero service mutation, zero ARM** — reversible, evidence-only:
1. Transfer the frozen run-kit to `GATEA-STAGING` per `TRANSPORT_PLAN.tsv` + `transport_runner.ps1`
   (operator-side transport evidence capture). Verify remote hashes before anything runs.
2. **B3** — read-only permission/ownership admission (0555, `/222` any-write-bit, manifest binding).
3. **R4-5** — Linux local-temp dangling-symlink restore fixture RED/GREEN (the one item that could
   not close on Windows; closes trivially here with real symlinks).
4. Checkpoint evidence + record after each step; commit exactly the files created, push. First-FAIL:
   stop, preserve, record, handoff note.

Then, if clean, proceed only with the **non-BLOCKED** designs. **BLOCKED — do NOT execute:** C1
(service stop — `C1-GAP-A`/`C1-GAP-B` open), both C2 reboot scenarios (baseline dep), C4 rollback,
C5 egress. Do not improvise closures for these; they escalate to owner.

## Hard boundaries (binding all night)

Bridge stays DISARMED, credential-free, loopback-only (`127.0.0.1:8790`). FORBIDDEN without a fresh
explicit Barış authorization: credential load, ARM, orders, broker/exchange contact,
TESTNET/mainnet, master merge, WP-V/KVM2, deleting the old payload archive, host reprovisioning.
First-FAIL; no-clobber evidence.

## Operating rules learned today (do not relearn the hard way)

- **Single writer.** Only THIS session drives staging/prereg. A second Fable session exists — do
  NOT let two implementers touch the same dir; today a double-dispatch nearly corrupted `02_PREREG/`.
  Before dispatching, confirm no other live codex/claude writer (`Get-Process`, CPU-delta probe).
- **Codex CLI content filter.** OpenAI kills Codex sessions that read the secret-scan category docs
  (`_AI_MEMORY` handoffs, `GATE_A_A*` files). Use narrow-scope self-contained kickoff files that
  exclude those; frame as authorized private-repo test-infra work.
- **Helper invocation.** Codex: `Invoke-CodexForClaude.ps1 -Account secondary -CodexArgs @('exec','-m','gpt-5.6-sol','-c','model_reasoning_effort=xhigh','--dangerously-bypass-approvals-and-sandbox',$prompt)`. Claude Max: `Invoke-ClaudeMax.ps1 --print $prompt --model claude-opus-5 --effort xhigh --dangerously-skip-permissions` (NOT `-p` — collides with `-PipelineVariable`). Both ASCII-only; ran fine today.
- **Bounded-call timeout.** A Codex-internal counterpart call timed out at 904s. For long
  implementer work dispatch Claude Max directly as a background task (no such limit).
- **Audit tiers** (`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md`): T0 (economic/deploy/systemd/verify.sh)
  = 2 flagships xhigh ≤3 rounds; T1 = 1 flagship high; T2 (docs) = single reviewer single round; T3
  (checkpoints/prompts/checklists) = self-verify, NO model audit. xhigh is T0-only. Audits at WP
  boundaries, not per-step. Meta-artifacts are never separately audited.
- **Ledger** RATIFIED: 20.5 h used / 29.5 h remaining at WP-L P2 start; book prospectively per unit
  (Stage-1+2 unit booked 0.8 h → ~28.7 h remaining). No retroactive reconstruction.

## Overnight autonomy setup

- Set up a self-paced monitor/loop watching `origin/feature/donchian-crypto-ladder` for new
  pushes + dispatched-task completions; drive the pipeline stage by stage.
- **Power:** machine slept 00:18–07:03 last night and killed the loop. Verify AC+DC idle sleep=0,
  hibernate off via `powercfg` before relying on overnight continuity (the other session was asked
  to fix this — confirm it actually took).
- Morning: summary + (if Remote Control connected) a push notification.

## Open non-critical items

Two mangled junk dirs (`C:\Users\BARSEM~2`, `BARSEM~3`) need an elevated-admin delete (backed up at
`C:\tmp\mangled_dirs_backup_2026-08-09`); WSL + Docker were installed by the other session today
(commit `241c9cd1`) — owner was unsure, not reverted.
