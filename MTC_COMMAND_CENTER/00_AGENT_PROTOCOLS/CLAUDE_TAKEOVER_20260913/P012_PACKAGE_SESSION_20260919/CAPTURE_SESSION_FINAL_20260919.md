# P0-12 PACKAGE session — final report (capture tool, T3) — 2026-09-19

**Outcome: WP-P0-12 Layer A (capture tool) MERGED to master `9edf846b` at 13:53 UTC+3, PR #197.**
Branch `feature/p012-path1-capture-20260914` closed out; base was `af921d75`.

## What this session did, in order
1. **T3 NIT slice.** Applied the drafted patch closing 7 NITs from the exact-Opus read of
   `af921d75` (verify_sidecars coverage, descending-page refusal, account_state bytes-before-check,
   real r2 fixture + replay test, tid-less fill refusal, named signature refusals, manifest
   signed-text/signature). Hit and resolved a wrong-pinned-interpreter blocker early (the prompt
   named the P020 venv, which has no crypto packages; corrected to
   `C:/tmp/P012_FUNDING_PY312_20260911`). Commit `1029d6e9`. Gemini delta PASS; exact-Opus
   re-read PASS-WITH-NITS (0 REQUIRED).
2. **Exact-Sol read of `1029d6e9` → REQUEST_CHANGES**, two REQUIRED findings both prior reviewers
   missed: R-1 (pagination row-floor checked a constant `start_ms` instead of the advancing
   `cursor`, letting a later short page silently admit a stale/duplicate row) and R-2 (a 2xx
   non-JSON SDK response fell back to `{"error": ...}`, which the account-state shape check
   accepted as valid). Both independently reproduced with fresh scripts before touching any code.
3. **Repair round 1.** Test-first fixes for R-1 (`t < cursor`) and R-2 (require `assetPositions`);
   also closed the NIT-A ruff-format regression while already in both files. Commit `9f1aa532`.
   Gemini delta PASS (0 findings); exact-Opus re-read (MAX profile, Pro window capped) and
   exact-Sol re-read (account `free`) run in parallel, both PASS-WITH-NITS, 0 REQUIRED.
4. **Opus MAX-lane process anomaly**, resolved by Lead ruling: `launch.exit` showed `exit=1` from
   a 429 that landed ~0.9s *after* the report's final successful write (evidence: `stream.jsonl`
   line 481 write at `09:43:25.590Z`, error at `09:43:26.525Z`) — counted as valid per the Lead.
5. Roster complete on `9f1aa532` (Gemini + exact-Opus + exact-Sol, all 0 REQUIRED, + Lead
   reproduction). `MERGE_READINESS.md` written; Lead opened and merged PR #197.

## Record paths
| What | Path |
|---|---|
| NIT-slice evidence (RED/GREEN, mutants, ruff parity, verification doc) | `C:/tmp/CLAUDE_P0_RUN_20260913/P1CAP_NIT_SLICE_20260919/` |
| NIT-slice Gemini delta | `C:/tmp/P012_S16_REVIEWS_20260913/P1CAP_NIT_GEMINI/` |
| NIT-slice exact-Opus re-read | `C:/tmp/OPUS_QUEUE_20260916/P1CAP/ATTEMPT3_PASS_WITH_NITS_1029d6e9/`, adjudication `LEAD_ADJUDICATION_P1CAP_NIT_T0.md` |
| Exact-Sol REQUEST_CHANGES on `1029d6e9` + PACKAGE session's independent repro (R-1/R-2) | `C:/CT13/.../CLAUDE_TAKEOVER_20260913/P1CAP_SOL_20260919/` (`SOL_T0_REPORT.md`, `LEAD_REPRO_R1.py`, `LEAD_REPRO_R2.py`, `LEAD_ADJUDICATION_P1CAP_SOL_T0.md`) |
| Repair round 1 evidence | `C:/tmp/CLAUDE_P0_RUN_20260913/P1CAP_NIT_SLICE_20260919/LEAD_VERIFICATION_P1CAP_R1_REPAIR.md` + `LEAD_RED_R1_R2_prefix.txt`, `LEAD_RED_R-1.txt`, `LEAD_RED_R-2.txt`, `LEAD_GREEN_r1_*.txt`, `RUFF_PARITY_R1_20260919.txt` |
| Repair round 1 Gemini delta | `C:/tmp/P012_S16_REVIEWS_20260913/P1CAP_R1_GEMINI/` |
| Repair round 1 exact-Opus re-read (MAX) | `C:/tmp/OPUS_QUEUE_20260916/P1CAP/ATTEMPT4_PASS_WITH_NITS_9f1aa532/` (incl. `README.md` on the 429 anomaly), adjudication `LEAD_ADJUDICATION_P1CAP_R1_T0.md` |
| Repair round 1 exact-Sol re-read | `C:/CT13/.../CLAUDE_TAKEOVER_20260913/P1CAP_SOL_20260919/SOL_T0_REPORT_R1_9f1aa532.md`, `LEAD_ADJUDICATION_P1CAP_R1_SOL_T0.md`, `P1CAP_R1_OPUS_MAX/` (copy) |
| Merge readiness | `C:/tmp/CLAUDE_P0_RUN_20260913/P012_PACKAGE_SESSION/MERGE_READINESS.md` |
| Blocker record (interpreter mix-up) | `C:/tmp/CLAUDE_P0_RUN_20260913/P012_PACKAGE_SESSION/QUESTIONS_FOR_LEAD.md` |

## Carried, non-blocking NITs on the merged `9f1aa532` (none REQUIRED; nobody has claimed them closed)
From the `af921d75` exact-Opus read, closed at `1029d6e9`/`9f1aa532`: NIT-A (ruff format — closed
in repair round 1), NIT-B (record-accuracy on NIT-4's "no mutant" claim — corrected in the record).
Still open:
- **NIT-C** — `verify_sidecars` doesn't notice a payload file with neither a manifest entry nor a
  sidecar. Bounded: the five recorded responses, manifest, and derived view are all bound; an
  unlisted extra file is inert evidence.
- **NIT-D** — a structurally malformed `CAPTURE_MANIFEST.json` (non-dict `responses` entries, or
  one missing `response_sha256`) escapes `verify_sidecars` as a raw exception (exit 1), one layer
  deeper than what NIT-6 guaranteed. Log hygiene, not a safety gap — never prints
  `CAPTURE_VERIFY_OK` on that path.
- **NIT-E** — `fill_derived` still carries a dead `hash`/`oid` `else` limb; unreachable since
  `fill_identity` refuses any fill without an integer `tid`.

From the `9f1aa532` re-reads (new this round):
- **Opus NIT-1** — R-2 is fixed at the consumer (`account_state_query`'s `assetPositions` check),
  not the source that manufactures the sentinel (`CapturingInfo.post`'s `{"error": ...}` fallback).
  Forward-looking: a sixth Info call site returning a dict would silently re-open the same class of
  hole. Sol's first suggested fix (raise inside `post` on parse failure) would make it structural.
- **Sol NIT-1** — `--verify-existing` doesn't positively require `CAPTURE_MANIFEST.json.sha256` or
  the derived-view sidecar to exist; deleting just the manifest sidecar still prints
  `CAPTURE_VERIFY_OK`. Same family as the carried NIT-C above, from the second flagship's own
  arm.
- **Sol NIT-2** — `--coin` is an unbound label: the CLI accepts and records it, but native
  fills/funding of a different coin are neither filtered nor refused. Native rows stay truthful;
  downstream intake must compare, so not a false-capture risk, but the manifest field should be
  renamed as a request or bound to the native inventory.
- **Sol NIT-3** — a malformed `--start`/`--end` timestamp escapes `parse_utc` as a raw `ValueError`
  (exit 1) instead of the tool's named-refusal vocabulary (`CaptureRefused`, exit 2). Happens before
  any output or network call, so it cannot produce false evidence — inconsistency only.

**Owner item F (carried, not a NIT against the candidate):** the signed ownership text binds
`address+run_id` only — `start`/`end`/`network` are not signed, and the manifest's
`binds: "address+run_id"` field says so honestly. Both exact-Opus and exact-Sol independently
agree with the handling: extending what gets signed would invalidate the owner's existing r1/r2
signatures, and that is the owner's call, not something either NIT slice or repair round should
change unilaterally.

## Session end
Per the Lead's instruction: no further work, no lanes, no git. `C:/tmp/P1CAP_20260914` and the
intake worktrees are left as-is. Idle.
