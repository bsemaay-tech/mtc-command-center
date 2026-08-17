# Audit 2 — Evidence checklist (DRAFT v2, 2026-08-09 night) — T3 + one T2 review applied

**Status: DRAFT v2 — T3 checkpoint/index artifact under the owner tier policy
(`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §2). v2 applies the findings of a T2
single-round read-only review by auditor 4 (GLM-5.2, 2026-08-09 night, report at
`C:\tmp\GLM_REPORT_AUDIT2_CHECKLIST_2026-08-09.md`, repo copy
`AUDIT2_CHECKLIST_GLM_REVIEW_2026-08-09.md`): F1 staleness fixed, F2–F5 missing
evidence classes added as §2b, F6/F7 verifiability anchors noted inline.** Compiled read-only from the gap matrix Group D
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
- ☐ Honest BLOCKED registry, restated at freeze time. Corrections applied tonight (GLM F1/S2):
  **R4-5 is CLOSED on Linux** — `05_TRANSPORT_R45B/STAGE3B_TRANSPORT_RECORD.md`, RUNID
  `…-R45B` CONSUMED, both arms held, guard proven load-bearing; the `ce0bc93e` Windows
  attempt (WinError 1314) is a historical superseded record, hand it as history only.
  **B3 is BLOCKED-UPSTREAM on `B3-GAP-ENV`** — `03_TRANSPORT/B3_STOP_ADJUDICATION.md`
  (STOP rc 3, checks 1–3 held; design repair cycle in `06_B3_REPAIR/`). Auditors must see
  BLOCKED items as BLOCKED and closed items as closed.
- ☐ Repair-round ledger for WP-L P2 (≤3 bound, who audited which round under which tier).
  Verifiability anchor (GLM F6): for every closed non-R4-5 RED/GREEN row, this ledger must
  name the exact re-audit file holding the RED demonstration — a row without a named file
  is handed as UNVERIFIED, not as closed.

## 2b. Transport-evidence package (added v2 — GLM F2–F5; largest banked body of evidence)

All in `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/`; per-file hashes in
`EVIDENCE_INDEX.md` (recomputed, with RUNID ledger).

- ☐ Operator-side transport records, both runs: `03_TRANSPORT/operator_record/` (ops
  01–06, 08–12) and `05_TRANSPORT_R45B/operator_record/` (ops 01–04) — per-op argv,
  stdout, stderr, rc, plus `TRANSPORT_RECORD.txt` + `TRANSPORT_SHA256SUMS.txt`.
- ☐ Remote-vs-local digest-set bindings — the ONLY on-repo proof of the git-excluded
  evidence logs: B3 `b3.log` = `079d6ac9…` (1784 B), set `b25612df…` (op 11 bind);
  R45B `r45b.log` = `00078e7e…` (4521 B), set `1f74d69a…` (op 04 bind). Auditors must
  recompute the digest set from the create-once record roots
  (`C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08{,-R45B}`) and match
  both the per-file digests and the `CLOSE_DIGEST_SET_SHA256` rendering.
- ☐ Burned-RUNID accounting (`EVIDENCE_INDEX.md` §RUNID ledger): `-B3` BURNED (STOP),
  `-R45` BURNED (never allocated), `-R45B` CONSUMED (PASS) — proves no replay and that
  the retry followed the fresh-preregistration rule (§11).
- ☐ Preregistration-before-invocation ordering proof: git commit order
  `04_PREREG_R45B/` (prereg) strictly precedes `05_TRANSPORT_R45B/` (execution record);
  same for Stage 2 `02_PREREG/` (`210b0168`) vs Stage 3 (`7e9d1c4a`).
- ☐ First-FAIL cascade evidence: rc pattern 05=3, 06=0, 07=skipped (no `07.*` files
  exist), 08=1, 10=1, 12=3 in `03_TRANSPORT` — proves R4-5's original skip was
  collateral sequencing, not a defect.

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
  by WP-L P2/WP-I, so the auditors can verify the budget envelope claim. Verifiability
  anchor (GLM F7): the freeze-time figure must name its source file; the banked slice so
  far is Stage-1+2 = 0.8 h and Stage 3+3B = 0.4 h (`STAGE3B_TRANSPORT_RECORD.md`),
  ~28.3 h remaining.
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
