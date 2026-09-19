# LEAD_ADJUDICATION — P020_DERIVED_G37 (gemini-3.7-flash-high corroboration of the WP-P0-20 derived measurement plan `d84b043a…` + derivation tool `0bfd1891…`) — 2026-09-15 05:40Z

**Verdict as returned: PASS-WITH-NITS — 0 REQUIRED, 2 NITs; q1 NIT, q2 SOUND, q3 SOUND (`evidence_class` SUPPLEMENTAL_UNEXECUTED).** Corroboration slot SATISFIED for the derived plan.

## Envelope and provenance
- Attempt 1 (05:28:12-05:31:18Z) VOIDED by the wrapper guard (`Changed: .git\worktrees\P1CAP_20260914\info\exclude`) — cause: the Claude Code harness writes `info/exclude` when a session's shell cwd enters a worktree (the Lead's cwd had drifted into `C:/tmp/P1CAP_20260914` while reading files); not a reviewer event; archived `FAILED_ATTEMPTS/attempt1`, not counted.
- Attempt 2 (05:32:27-05:35:41Z): conversation `2887e3c9-f556-4607-aa91-bac44c8e5278`, status SUCCESS, 152.7 s, 1 turn, usage input 235 094 / output 39 008 / thinking 23 973 / cache 2 660 079; `REVIEW.log` sha256 `c9bdec57…`; response 23 717 chars sha256 `0fbd6237…` (`REPORT_RESPONSE_UTF8.md`); sentinel `GEMINI_READ_ONLY_OK` present.
- Native reads (`NATIVE_READ_VERIFICATION.json`): 37 native `read_file` steps, 37/37 displayed content EQUAL to the packet bytes, 0 failures; every REQUIRED range covered with continuations (tool 1-262; tests 1-337; derived plan 1-533; frozen 1-457; base plan 1-383; driver 1-50/85-207/586-692; `preselect_profile.py` 412-448 and 1102-1154; all authority/derived/inputs files). One read outside the packet: idx 2 `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md` — the Gemini CLI's automatic context-file load at start (cwd = canonical checkout), before the first packet read; not a reviewer choice; no other outside read.

## Findings and Lead disposition
| # | Reviewer finding | Lead disposition |
|---|---|---|
| G37-01 (NIT) | `_validate_plan` (`run_bounded_benchmark.py:185-194`) reads only `derivation.family_order`; the four derivation input digests are not checked on the `--run` path | Same as Sol NIT-1. Accepted as NIT for the once-only Lead run: the launcher ASSERTS the installed plan equals `d84b043a…` before `--validate-plan`, immediately before `--run` and after the run (Sol's condition), and records pre/post digests of driver, manifest, compatibility, records + sidecars and implementation sources (Gemini's condition). Driver-level pinning = candidate for the next reviewed driver change (would re-open the driver identity `3d4453cd…`). |
| G37-02 (NIT) | documentation citation residuals (Opus N6-1/N6-7, Sol-6-3; `PRESELECTION_FROZEN.json:139`, prereg) | Carried; next re-freeze. |
| Q1 | NIT — documentary chain sufficient for one Lead run | Agrees with Sol (NIT with the assertion condition). |
| Q2 | SOUND — swap does not invalidate any identity check on the `--run` path; record pre/post digests | Agrees with Sol (temporary substitution; `SHA256SUMS_V16.txt` plan line updated for the interval and restored byte-exact). Launcher updated accordingly. |
| Q3 | SOUND — zero degrees of freedom affect what is measured | Agrees with Sol. |
| Trial table | 15/15 EQUAL | Matches the Lead's `LEAD_TRIAL_CHECK_S4.txt` and Sol's table. |
| Base-plan keys | 16 EQUAL, `trials` DIFFERENT (mandated), `derivation` added | Matches. |
| N6-8 / N6-6 | CLOSED with file:line; line-by-line comparison of the transcribed matching: only docstring + exception class differ | Matches the Lead's byte comparison (session 3) and Sol's scratch RED/GREEN/RED. |

## Roster for the derived plan (OD-20260914-P020-MEASURE-1 condition (c))
Lead ✔ (`LEAD_TRIAL_CHECK_S4.txt` ALL EQUAL; PLAN_VALID harness) · exact Sol ✔ PASS-WITH-NITS (0 REQUIRED; `P020_DERIVED_PLAN_REVIEW_20260915/sol/SOL_DERIVED_REPORT.md` sha256 `96273b29…`) · Gemini 3.7 ✔ PASS-WITH-NITS (this record) · **Grok pre-screen VACANT** (route `402 Grok Build usage balance exhausted`, probed 05:25Z) — the owner decision text names the Grok pre-screen; the Lead puts the vacancy to the owner as a one-line question before the single run · exact Opus: not required by the decision ("no further Opus unless separately authorized").

Recorded by Claude Opus 5 Lead (743291).
