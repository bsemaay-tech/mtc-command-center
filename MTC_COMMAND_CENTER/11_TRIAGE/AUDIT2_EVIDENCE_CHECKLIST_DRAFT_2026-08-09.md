# Audit 2 — Evidence checklist (DRAFT, 2026-08-09) — T3, no audit performed

**Status: DRAFT — T3 checkpoint/index artifact under the owner tier policy
(`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §2): implementer self-verification only, no model
audit run for this file.** Compiled read-only from the gap matrix Group D
(`GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` §Group D, commit `851d2aa5`),
the owner decision record (`66ca76a1`), and `AGENTS.md` (canonical roster, D025, D026). Nothing
here executes, authorizes, or replaces Audit 2; the dispatching Lead session owns the actual
round. Items marked ☐ are what the auditors must be HANDED; this file creates none of them.

## 0. Controlling contract (note one open reconciliation)

- Owner decision 2026-08-09 §3 (newer, binding): **Audit 2 stays two-flagship** —
  `claude-opus-5` xhigh + Codex `gpt-5.6-sol` xhigh, fresh independent sessions — because it
  freezes the pre-WP-A SHA (T0 surface; xhigh is T0-only and this is T0).
- Gap matrix D1 (earlier same day) words Audit 2 as the **four-auditor D025 contract**
  (flagships + `cline-pass/deepseek-v4-flash` + GLM-5.2). D025's acceptance floor is the two
  flagships either way; auditors 3–4 "add detection". Practical state: auditor 3 is BLOCKED
  (ClinePass subscription paused, unpaid — 2026-08-08).
- **⚑ RECONCILIATION FLAG for the dispatcher:** confirm at dispatch time whether GLM-5.2 runs as
  supplemental detection or is omitted under the owner two-flagship directive. This draft does not
  decide it.

## 1. Freeze identity (prerequisite — Audit 2 cannot start without these)

- ☐ Exact frozen checkpoint commit SHA after WP-L Phase 2 close **and** WP-I staging verification
  close (sequence per D2: Audit 2 runs after both, **before** any WP-A step).
- ☐ Frozen product candidate identity restated: `2ce41e34bceb599d80af24c5c33d835820ec321b` +
  artifact/manifest hashes (Group A1/A2 immutable set).
- ☐ Statement that candidate bits are unchanged since Gate-A acceptance (`5af8178b` record), or an
  exact diff if not.

## 2. WP-L Phase 2 closure evidence package

- ☐ Final accepted revision of `WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` + its block-digest
  table (§8.1 blob SHA-256s, `bash -n` / `py_compile` results).
- ☐ RED/GREEN records for every closed falsification row (D026: commands + real output; a test
  never shown RED is supplemental, not closure).
- ☐ Honest BLOCKED registry — including `WPL_P2_R45_CLOSURE_ATTEMPT_2026-08-09.md` (`ce0bc93e`):
  R4-5 remains BLOCKED (WinError 1314 reproduced 2026-08-09); shell-level equivalent closed by
  R0-2. Auditors must see BLOCKED items as BLOCKED, not as closed.
- ☐ Repair-round ledger for WP-L P2 (≤3 bound, who audited which round under which tier).

## 3. WP-I staging verification evidence package

- ☐ Static minimum-security / secret-scan / egress inventory (Group A3) at the frozen SHA.
- ☐ Executed read-only host-check logs (Group B items actually run), each with no-clobber log
  path, SHA-256, byte count — Gate-A evidence conventions.
- ☐ Current-state proofs: DISARMED, `state_version`, loopback-only listener, `Restart=no`,
  no credentials loaded (Group B5/B6 style).
- ☐ Any mutating check performed (Group C) with its preregistration reference; anything not
  preregistered = finding, not evidence.

## 4. Authority & budget chain

- ☐ `OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` (tier policy + cadence + ledger ratification).
- ☐ Ratified 50h ledger figure at freeze time (20.5h/29.5h baseline `66ca76a1`) + hours consumed
  by WP-L P2/WP-I, so the auditors can verify the budget envelope claim.
- ☐ WP-L P2 + WP-I authorization record and its hard exclusions (no ARM, no credentials, no
  TESTNET/mainnet, no master merge, no economic action).

## 5. Auditor session inputs (per `AGENTS.md` audit session contract)

- ☐ Scope contract (what Audit 2 accepts/rejects: Linux-port + staging acceptance of the frozen
  artifact — D2).
- ☐ Actual diff/files at the frozen SHA — never implementer session context, never `--resume`.
- ☐ Mandated test-suite command + expected baseline (current accepted anomaly set, e.g. the two
  permitted `test_order_state.py` gc-referent failures, stated explicitly) — D025 rule 1:
  an auditor that cannot execute the suite must return BLOCK.
- ☐ Isolated worktree instructions at the frozen SHA + required cleanliness proof
  (`git status --porcelain` empty) per auditor.
- ☐ D026 checklist: for each new test offered as closure, where its RED demonstration lives;
  auditors must state per test whether they verified it.

## 6. Verdict & loop bookkeeping (to be produced by the round itself)

- ☐ Two independent flagship verdicts (PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK) + Lead
  reproduction notes for every required finding (rule 2: binding only after Lead reproduces on
  real source; unreproduced findings recorded with evidence, not dropped).
- ☐ Acceptance decision against the D025 floor; repair loop ≤3 rounds, then STOP and report.
- ☐ Sequence proof in the closing record: accepting Audit 2 verdict exists **before** WP-A begins
  (starting WP-A earlier = sequence violation, STOP — D2).

## Exclusions

Read-only compilation. No audit dispatched, no model invoked, no host/staging contact, no
existing file modified, no authority created or spent. DRAFT until the dispatching Lead session
adopts or supersedes it.
