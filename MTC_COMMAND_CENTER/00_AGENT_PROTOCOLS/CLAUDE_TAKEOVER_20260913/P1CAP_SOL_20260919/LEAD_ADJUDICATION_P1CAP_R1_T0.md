# LEAD_ADJUDICATION — lane 2 (P1CAP): exact `claude-opus-5` xhigh re-read of repair round 1 `9f1aa532`

**Lane:** `OPUS_QUEUE_20260916/P1CAP/opus/run_max.ps1` (MAX profile, `~/.claude-max`, owner ruling
`OD-20260919-MAX-LANES-TODAY-1`), attempt 4 (attempts 1-3 archived: `ATTEMPT1_CAPPED_1247Z/`,
`ATTEMPT2_PASS_WITH_NITS_af921d75/`, `ATTEMPT3_PASS_WITH_NITS_1029d6e9/`). Launched via
`Start-Process` (not `Start-Job`, per instruction) 09:27:22Z, 68 turns, $6.36. Report 492 lines,
11 sections, ends with a proper `VERDICT:` line. Archived as
`ATTEMPT4_PASS_WITH_NITS_9f1aa532_MAX/`.

## Process anomaly — read before trusting the verdict as COUNTED
`launch.exit` reads `exit=1`, not `exit=0` — the campaign's standing rule (same wording as the
Gemini rule) is that a non-zero launcher exit means NOT COUNTED. `stream.jsonl`'s final turn shows
`"api_error_status":429`, `"terminal_reason":"api_error"`, message *"You've hit your session limit
- resets 1:40pm (Europe/Chisinau)"*. This is the MAX profile's own 5-hour-window cap, hit on the
**last** turn (turn 68) — after the full report was already written to disk (verified: `OPUS_T0_REPORT.md`
has all 11 expected sections, a correctly-terminated `VERDICT: PASS-WITH-NITS` line, and internal
content that is self-consistent — e.g. §8 directly answers "why did my `1029d6e9` read miss R-1
and R-2", which only makes sense as the final, deliberate content, not a truncated fragment).
Distinguishing feature from a genuine CAPPED run (e.g. `ATTEMPT1_CAPPED_1247Z/`): those have an
incomplete or missing report; this one does not.

**Decision: COUNTED**, per the Lead's ruling (message to the PACKAGE session, 2026-09-19): count
iff the report's final write preceded the 429. Evidence (`stream.jsonl`, archived
`ATTEMPT4_PASS_WITH_NITS_9f1aa532/README.md`): line 481 (`ts=2026-09-19T09:43:25.590Z`) is the
successful write of `OPUS_T0_REPORT.md`; line 483/484 (`ts=2026-09-19T09:43:26.525Z`,
`api_error_status:429`) is the rate-limit termination — **~0.9s after** the report's last write,
on the wrap-up turn that followed it. Additionally:
1. Every citation I checked against the committed `9f1aa532` blob is exact (below).
2. One factual claim (both real captures' `account_state.json` top-level keys include
   `assetPositions`) was independently reproduced by re-parsing the actual fixture files —
   matched exactly.
3. The report's own findings cross-corroborate Sol's independent read (both flag the
   `verify_sidecars` manifest-sidecar gap; neither found a REQUIRED issue).

**Verdict as returned:** `VERDICT: PASS-WITH-NITS` — **0 REQUIRED**. One new NIT (NIT-1, R-2 fixed
at the consumer not the source — forward-looking, not blocking), three carried NITs (was NIT-C/D/E,
unchanged, not claimed closed), one record-only NIT (NIT-5, two citation ranges in
`LEAD_VERIFICATION_P1CAP_R1_REPAIR.md` were off by a few lines post-format — corrected below), one
carried owner item (NIT-F, unchanged).

## Lead (PACKAGE session) reproduction
| Check | Result |
|---|---|
| R-1 citation `capture_own_account_evidence.py:370-373` (`if t < cursor:`) | **EXACT** at committed `9f1aa532` |
| R-2 citation `capture_own_account_evidence.py:478-482` (`if "assetPositions" not in parsed:`) | **EXACT** at committed `9f1aa532` |
| Claim: both real captures' `account_state.json` carry `assetPositions` among `['assetPositions','crossMaintenanceMarginUsed','crossMarginSummary','marginSummary','time','withdrawable']` | **CONFIRMED** — re-parsed both `r1/account_state.json` and `r2/account_state.json` directly, identical key sets |
| Sol's `parse_utc` finding (tool `:116-120`, unhandled `ValueError` on a malformed timestamp) | **CONFIRMED** independently — `cae.parse_utc("not-a-time")` raises `ValueError: Invalid isoformat string: 'not-a-time'`, not `CaptureRefused` |
| Worktree integrity | `git status --porcelain` in `C:/tmp/P1CAP_20260914`: only the 4 pre-existing untracked scratch files; `HEAD` unchanged at `9f1aa532` (both the Opus MAX lane and the Sol lane ran concurrently against this worktree with `--add-dir` write access; neither left a trace) |

## NIT-5 record correction (this session, same day)
`LEAD_VERIFICATION_P1CAP_R1_REPAIR.md` cited the R-1 fix at `:362-370` and R-2 at `:464-473`
("post-format"); the actual post-format locations are `:370-373` and `:478-482` (confirmed above).
Corrected in the record; `9f1aa532` itself is untouched.

## Standing
Lane 2 read COUNTED (with the process anomaly disclosed above): exact-Opus PASS-WITH-NITS on
`9f1aa532`, 0 REQUIRED. Combined with Gemini delta COUNTED PASS (0 findings,
`P012_S16_REVIEWS_20260913/P1CAP_R1_GEMINI/LEAD_ADJUDICATION.md`) and exact-Sol PASS-WITH-NITS
(0 REQUIRED, adjudicated separately), the roster for `9f1aa532` is complete: two flagships of
different families + Gemini + Lead reproduction, all 0 REQUIRED. Merge-ready.

Recorded by the P0-12 PACKAGE session (Claude Sonnet 5), 2026-09-19.
