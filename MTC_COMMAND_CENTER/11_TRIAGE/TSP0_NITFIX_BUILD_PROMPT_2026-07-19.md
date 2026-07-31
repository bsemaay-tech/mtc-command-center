# TS-P0 NIT-FIX BUILD PROMPT — 2026-07-19

> **PARTIALLY SUPERSEDED 2026-07-19:** N1/N2 and the later Codex BLOCK findings
> were repaired by `CODEX_TSP0_BLOCK_REPAIR_REPORT_2026-07-19.md`. Do not rerun
> Tasks 1–2 from this prompt. First execute
> `TSP0_BLOCK_REPAIR_REAUDIT_PROMPT_2026-07-19.md`; after a non-BLOCK verdict,
> only the remaining N3/N4/N5 docs closeout and owner gates below remain.

For the builder AI (Codex or Fable) that closes the TS-P0 audit nits.
Written by the independent Fable auditor; nit definitions and reproduction
evidence live in `11_TRIAGE/FABLE_TSP0_INDEPENDENT_AUDIT_2026-07-19.md` (N1–N5).

## PRECONDITIONS (hard gate — verify before any edit)

1. The Codex cross-audit (`CODEX_TSP0_AUDIT_2026-07-19.md` or equivalent) has
   landed AND has been reconciled with the Fable audit. **No unresolved BLOCK
   finding from either audit.** If Codex found additional findings, they are
   either folded into this task list by Barış/Fable or explicitly deferred —
   do not silently expand scope yourself.
2. Worktree `C:\TSP0` exists, branch `feature/ts-p0-baseline`, HEAD
   `7777273f`, porcelain clean, stash empty. If HEAD differs, STOP and report.
3. Runtime `C:\P2RT` is a LIVE Day 1 window: **READ-ONLY. Never write /
   checkout / restart / ARM / DISARM / touch scheduler or DB.** This task does
   not need to touch P2RT at all.
4. Repo guard dry-run PASS in the main worktree
   (`powershell -ExecutionPolicy Bypass -File MTC_COMMAND_CENTER/tools/repo_guard.ps1`).

## BOUNDARIES (same as the TS-P0 build session)

No push, no PR, no merge, no deploy, no network calls, no dependency additions,
no protected-scope edits (`02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `MTC_V2`),
no execution beyond pytest. Code edits ONLY in `C:\TSP0`. Main-worktree edits
ONLY the named docs/memory files, left uncommitted per convention. Never clean/
reset/stash the main worktree. TDD: capture RED before implementing N1/N2.

## TASK 1 — N1: release_evidence exit-code contract on malformed-but-signed manifest

Defect (reproduced by the audit): in
`IBKR_PAPER_BRIDGE/tools/release_evidence.py`, `_validate_manifest` guards the
`REQUIRED_HASH_KEYS` check with `isinstance(manifest["hashes"], dict)` and
records NO failure when `hashes` is present but not a dict. A manifest with
`"hashes": "<string>"` and a re-computed `integrity_sha256` therefore passes
the structural phase and crashes in the live-state comparison
(`manifest["hashes"]["source_tree_hash"]` → `TypeError`) → traceback,
**process exit 1**; the documented contract allows only 0/2/3.

Required behavior: `hashes` present but not a dict → structural failure
`invalid_field_type:hashes` (or `missing_field:hashes` — pick one, document it)
→ verdict INVALID, **exit 2**. No traceback. While there, sweep
`_validate_manifest` for any other uncaught-exception path on adversarial
manifest content (wrong types for `release_commit`, `rollback_commit`,
individual hash values): every such input must land on exit 2 (structural/
validation failure) or exit 3 (corrupt input), never a traceback.

TDD: new test(s) in `IBKR_PAPER_BRIDGE/tests/test_release_evidence.py` —
build the manifest, re-sign with `_integrity_hash`, run validate at the
SUBPROCESS level, assert exit 2 and the failure token in stdout JSON. Capture
RED (current code exits 1) before the fix.

Also update `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md` (still
DRAFT): add the failure token and one sentence stating `integrity_sha256` is a
checksum against corruption, not a signature — forged/re-signed manifests are
caught by live-state comparison only (audit item 8 evidence).

## TASK 2 — N2: secret denylist `.env`-suffix gap  [CONDITIONAL — needs Barış]

`_is_secret_name` in `IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py`
misses `prod.env` / `config.env` (pattern `^\.env(\..*)?$` is prefix-anchored).

Two acceptable resolutions — **ask Barış which, do not decide yourself**
(this is part of his pending hash-scope confirmation):
- **(a) recommended:** add pattern `.*\.env$` to `SECRET_FILE_PATTERNS`.
  Consequence: any `*.env` file inside scope is excluded-by-name from hashing;
  manifest `secret_denylist` echo changes; add a fixture test proving
  `config/prod.env` is excluded, never opened (extend the spy-hash test).
- **(b):** leave the pattern, document in `RUNTIME_BASELINE_CONTRACT.md` that
  `*.env` outside the `.env*` basename convention is deliberately in hash
  scope (digest-only exposure accepted).

If Barış has not answered by build time, implement NOTHING for N2 and record
it as still-open in the report.

## TASK 3 — N4: residual stale "Proposed status" ADR wording (docs-only, main worktree)

Same class as the three sentences TS-P0-004 already fixed. Rewrite to past
tense + D016 (2026-07-18) ratification reference, changing status wording only
— never decision content:
- `MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0020-hybrid-backtesting-validation-stack.md:62`
  ("Proposed status is required until the gap audit …")
- `MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0025-build-core-risk-reconciliation-internally.md:51`
  ("Proposed status follows ADR-0018 and the unresolved gap audit.")
- `MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0029-paper-to-live-promotion-gates.md:49`
  ("Proposed status reflects the unsigned current gate and open thresholds.")
Then grep the whole ADR dir for remaining present-tense `Proposed status` /
`remains Proposed` outside D016 quotes; report anything you deliberately leave.
Do NOT edit `_AI_MEMORY/DECISIONS.md` (owner record; the stale D016 sentence
stays flagged for Barış).

## TASK 4 — N5 + N3 doc corrections (small, docs-only)

- N5: one line in `RUNTIME_BASELINE_CONTRACT.md` attack-surface/limitations:
  file symlinks inside scope hash their target's content (digest oracle only;
  no content leak; Windows symlink creation is privileged).
- N3: append a dated correction note to
  `11_TRIAGE/FABLE_TSP0_AUDIT_HANDOFF_2026-07-19.md` §Integration re-run: at
  final HEAD `7777273f` the CORRECT result is exit 2 with THREE reasons
  including `source_tree_hash_mismatch` (Task C files legitimately differ from
  P2RT@`008e065e`); the two-reason expectation was valid only at `fa449ce2`.
  Do not rewrite the original text — append a clearly marked correction.

## VERIFICATION & COMMIT

1. Full suite from BOTH CWDs (`C:\TSP0` and `C:\TSP0\IBKR_PAPER_BRIDGE`,
   PYTHONUTF8=1): expected 210 + new N1/N2 tests, zero failures, existing
   tests untouched.
2. Re-run the audit's N1 subprocess probe shape → now exit 2.
3. Repo guard dry-run PASS before commit.
4. ONE commit in `C:\TSP0` for Tasks 1(+2 if approved): explicit paths only,
   never `git add .`; verify `git diff --cached --name-only` = intended set.
   Suggested message: `fix(bridge): TS-P0 audit nits N1/N2 — release_evidence
   exit-code contract + env denylist`. Docs in main worktree stay uncommitted.
5. Update `_AI_MEMORY/NEXT_STEPS.md` (mark nits fixed) + `GLOBAL_HANDOFF.md`
   head entry + write build note under `11_TRIAGE/`.

## STAGE 2 — PUSH/PR CLOSURE  [SEPARATELY GATED — do NOT run in the same breath]

Only after Barış explicitly approves ALL of: (1) hash scope [incl. N2 choice],
(2) release-evidence contract (DRAFT→approved), (3) window reset policy, and
states the push/PR sentence for `feature/ts-p0-baseline`. Then: push branch,
open PR to master (body per repo convention, no merge without approval),
repo guard PASS before and after. If any approval is missing → STOP after the
commit and report.

## REPORT FORMAT

End with the standard block: branch / files changed / checks run / guard /
commit / pushed / remaining dirty / next action. Report honestly anything
skipped or still open (N2 pending Barış, Codex-audit deltas, etc.).
