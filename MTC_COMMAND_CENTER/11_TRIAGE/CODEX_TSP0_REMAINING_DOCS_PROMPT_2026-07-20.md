# CODEX PROMPT — TS-P0 remaining documentation closeout after PR #25

Use this in a fresh Codex session in `C:\LAB\Tradingview_LAB_CLEAN`.

## Goal

Close only the remaining TS-P0 documentation nits and record the owner approvals
that arrived after audited commit `44338d61`. Produce a reviewable local diff and
a report. Do not commit or publish the follow-up without a new explicit gate.

## Fixed facts to verify before editing

- `C:\TSP0` branch: `feature/ts-p0-baseline`.
- Expected clean HEAD and remote PR head:
  `44338d61275499f2019011cd06e6f27007f6cbcf`.
- Draft PR: <https://github.com/bsemaay-tech/mtc-command-center/pull/25>, base
  `master`. The audited repair verdict is PASS in
  `MTC_COMMAND_CENTER/11_TRIAGE/FABLE_TSP0_BLOCK_REPAIR_AUDIT_2026-07-20.md`.
- Barış's 2026-07-20 decisions: TS-P0 hash scope approved;
  `RELEASE_EVIDENCE_CONTRACT.md` approved; sticky reset policy confirmed with
  300-second tolerance.
- Live paper runtime is Day 1 v2 on `C:\P2RT` at `008e065e`, run
  `paper-20260720090332`. It is out of scope and must remain untouched.
- The main worktree is intentionally dirty with unrelated user work. Never
  reset, clean, stash, restore, stage broadly, or overwrite unrelated changes.

If the TSP0 HEAD, branch, cleanliness, or remote PR head differs, stop and
report. Treat builder reports and handoffs as claims; verify every edited line.

## Hard boundaries

- Documentation-only. No Python/code/test/schema/config/strategy/threshold edits.
- No task start/stop, ARM/DISARM/KILL, deploy, checkout in P2RT, exchange call,
  or runtime status call.
- No commit, push, PR mutation, merge, or deploy in this session.
- Never use `git restore`, `git checkout -- <file>`, `git reset`, or `git stash`.
- Edit only the files named below plus the closeout report and the three canonical
  handoff files if needed.

## Required edits

1. In `C:\TSP0\IBKR_PAPER_BRIDGE\docs\RUNTIME_BASELINE_CONTRACT.md`, close N5
   with one precise limitation: a file symlink inside hash scope hashes the
   target content, creating a digest oracle but not exposing file content;
   Windows symlink creation normally requires privilege/developer mode.
2. In `C:\TSP0\IBKR_PAPER_BRIDGE\docs\RELEASE_EVIDENCE_CONTRACT.md`, record
   Barış's 2026-07-20 approval without changing the validated contract content.
3. In `C:\TSP0\IBKR_PAPER_BRIDGE\docs\21_WINDOW_STATE_CONTRACT.md`, record the
   2026-07-20 confirmation of the sticky reset policy and exact 300-second
   tolerance. Do not change behavior.
4. Close N3 by appending a dated correction to
   `MTC_COMMAND_CENTER/11_TRIAGE/FABLE_TSP0_AUDIT_HANDOFF_2026-07-19.md`:
   final HEAD correctly returns exit 2 with three reasons including
   `source_tree_hash_mismatch`; the two-reason expectation applied only at
   `fa449ce2`. Preserve the original text.
5. Close N4 by changing only the stale present-tense “Proposed status” rationale
   sentences in ADR-0020 line ~62, ADR-0025 line ~51, and ADR-0029 line ~49 to
   past-tense ratification wording tied to D016 (2026-07-18). Do not change the
   decisions or their qualifications. Grep the ADR directory for other stale
   present-tense proposal wording and report, but do not widen scope.

## Verification

- Prove the TSP0 diff is documentation-only with `git diff --name-only` and
  `git diff --check`.
- Prove no tracked code/config/test file changed in TSP0.
- Show exact before/after lines for N3/N4/N5 and approval markers.
- Prove `C:\P2RT` was not accessed or mutated by this session.
- Leave TSP0 changes uncommitted. State explicitly that PR #25 remains at
  `44338d61` until Barış separately authorizes a reviewed docs-only commit/push.

## Output

Write
`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP0_DOC_CLOSEOUT_REPORT_2026-07-20.md`
with scope, exact files, verification, remaining dirty state, and the next
approval sentence needed. Update `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and
`ACTIVE_FILES.md` conservatively. Do not claim the docs are on GitHub.

