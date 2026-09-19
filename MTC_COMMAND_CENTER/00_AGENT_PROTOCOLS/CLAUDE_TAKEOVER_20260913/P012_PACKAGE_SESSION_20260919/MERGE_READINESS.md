# MERGE_READINESS — P0-12 capture tool (T3/T5) — 2026-09-19

**Candidate: `9f1aa532d49a9856caf766d2480f3b7744ce86dd`**
Branch `feature/p012-path1-capture-20260914`, worktree `C:/tmp/P1CAP_20260914`. History:
`af921d75` (Lead-authored correction, merge-track base) → `1029d6e9` (PACKAGE session: 7 NITs
closed) → `9f1aa532` (PACKAGE session: repair round 1, closing R-1/R-2 REQUIRED findings from
exact-Sol; also closed the NIT-A ruff-format regression).

## Roster (all on the final bytes `9f1aa532`)
| Reviewer | Verdict | REQUIRED | Record |
|---|---|---|---|
| Gemini 3.8 (delta) | PASS | 0 | `C:/tmp/P012_S16_REVIEWS_20260913/P1CAP_R1_GEMINI/LEAD_ADJUDICATION.md` |
| Exact-Opus (claude-opus-5 xhigh, MAX profile) | PASS-WITH-NITS | 0 | `C:/tmp/OPUS_QUEUE_20260916/P1CAP/LEAD_ADJUDICATION_P1CAP_R1_T0.md` (counted per Lead ruling on a post-report 429 — see that file's process-anomaly section and `ATTEMPT4_PASS_WITH_NITS_9f1aa532/README.md`) |
| Exact-Sol (gpt-5.6-sol xhigh, Codex Pro `free`) | PASS-WITH-NITS | 0 | `C:/CT13/.../CLAUDE_TAKEOVER_20260913/P1CAP_SOL_20260919/LEAD_ADJUDICATION_P1CAP_R1_SOL_T0.md` |
| PACKAGE session reproduction | — | — | Citations grep-verified against the committed blob for both flagship reports; the `assetPositions` real-capture claim and the `parse_utc` raw-`ValueError` finding independently reproduced; `git status --porcelain` clean, `HEAD` unchanged, both concurrent lanes left no trace |

**0 REQUIRED across the entire roster. Merge-ready** per the owner's conditional pre-authorization
`OD-20260919-P012-MERGE-CAPTURE-GO-1`.

## What was found and fixed along the way (for the record, not blocking)
- `1029d6e9` closed the 7 NITs from the exact-Opus read of `af921d75` (base correction).
- Exact-Sol's read of `1029d6e9` found two REQUIRED gaps the first two reviewers (Gemini, exact-Opus)
  missed: R-1 (pagination row-floor checked a constant instead of the advancing cursor) and R-2
  (a 2xx non-JSON SDK response was accepted as valid account state). Both independently reproduced
  by the PACKAGE session, then fixed test-first in `9f1aa532`.
- Carried, non-blocking NITs on `9f1aa532` (all disclosed, none REQUIRED): `verify_sidecars`
  doesn't require the manifest/derived sidecars to exist (Opus NIT-2/Sol NIT-1); a structurally
  malformed manifest escapes as a raw exception instead of a named refusal (Opus NIT-3); a dead
  `else` limb in `fill_derived` (Opus NIT-4); `--coin` is an unbound label, not a filter (Sol NIT-2);
  a malformed `--start`/`--end` timestamp escapes `parse_utc` as a raw `ValueError` (Sol NIT-3);
  R-2 is fixed at the consumer, not the source that manufactures the sentinel (Opus NIT-1,
  forward-looking).
- Carried owner item (not a NIT against the candidate): the signed ownership text binds
  `address+run_id` only, not `start`/`end`/`network` — both flagships agree this is the owner's
  call, not something a slice should change unilaterally (would invalidate the owner's existing
  r1/r2 signatures).

## Note on `master`
The Lead reports `master` moved (intake PR #196 merged) since this branch's base; the Lead will
run `gh pr update-branch` before merging PR #197. Nothing needed from the PACKAGE session.

## What's NOT done (T5, needs the owner and/or the Lead)
- **T5 — open + merge the PR.** PACKAGE session does not open or merge PRs. The Lead opens/merges
  per the owner's pre-authorization once this roster is confirmed (PR #197 already open per the
  Lead's last message).
- Records pushed to CT13 (`feature/claude-takeover-20260913`): pending final commit of this
  session's repair-round records (Sol + Opus copies, both adjudications) — committing now.
