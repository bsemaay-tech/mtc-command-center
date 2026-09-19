# P0-12 INTAKE session — final note — 2026-09-19

**Task:** T4, the WP-P0-12 intake-adapter NIT slice (NITs 1-9 + NIT-A from the lane-8 exact-Opus reads of `a871e429`, plus owner ruling D6-START B, `OD-20260918-P012-D6START-B-1`).

**Result:** merged to `master` as `5214f169` via PR #196, CI 9/9 green, 2026-09-19 ~12:36 UTC+3.

## What was built

New worktree `C:/tmp/P012_INTAKE_NIT_20260919`, branch `feature/p012-funding-intake-nit-20260919`, base `a871e429`, commit `8cbf4f1a`. Four files touched (`IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py`, `tools/funding_intake_adapter.py`, `tests/test_mtc_funding_export_real_capture.py`, `tests/test_funding_intake_adapter.py`), +342/-36. Test-first: RED on `a871e429` bytes (8 failed/71 passed), GREEN after (240 passed/1 skipped), full Bridge suite 1707 passed/1 skipped, 9 scratch mutants each killed by its named test, ruff parity 7/7 pre-existing (0 new), guard PASS.

## Roster (all four legs, 0 REQUIRED anywhere)
- Gemini (gemini-3.8-flash-high, detection): PASS, all 10 items CLOSED.
- Exact-Opus (claude-opus-5 xhigh, MAX profile — the Pro 5h window was capped mid-session): PASS-WITH-NITS.
- Exact-Sol (gpt-5.6-sol xhigh, Codex PRO `free`, independent family): PASS-WITH-NITS.
- Lead reproduction: independently confirmed the two standout findings below.

## Records
- Builder evidence: `C:/tmp/CLAUDE_P0_RUN_20260913/P012_FUNDING_INTAKE_20260915/NIT_SLICE_20260919/LEAD_VERIFICATION_P012_INTAKE_NIT.md` (+ RED/mutant/ruff/full-suite `.txt` files alongside it).
- Gemini: `C:/tmp/P012_S16_REVIEWS_20260913/P012_INTAKE_NIT_GEMINI/` (cid `566ab938`; `LEAD_ADJUDICATION.md`).
- Exact-Opus: `C:/tmp/OPUS_QUEUE_20260916/P012INTAKE/ATTEMPT6_PASS_WITH_NITS_8cbf4f1a/OPUS_REPORT.md`; `LEAD_ADJUDICATION_P012INTAKE_NIT_T0.md` in the same lane dir.
- Exact-Sol: `C:/tmp/SOL_QUEUE_20260919/P012INTAKE/sol/SOL_T0_REPORT.md`; CT13 `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P012INTAKE_SOL_20260919/` (commit `965eceec`, pushed).
- Roster summary: `C:/tmp/CLAUDE_P0_RUN_20260913/P012_PACKAGE_SESSION/MERGE_READINESS_INTAKE.md`.

## Carried, not built here (next slice, after the owner's word)
- **D6-GRID A|B** (exact-Opus NIT-B, Lead-reproduced): the D-6 completeness grid was not shifted along with the new D6-START B admission band, so a real single-window capture whose position is open at its own start hour is structurally unbuildable today. Refusal-only, does not affect the r1 capture, does not block this merge. Needs an owner one-liner before O-1 / the next real multi-window capture.
- Sol's NIT-3 (Lead-reproduced): the NIT-A regression test only pins the resulting refusal code, not that the exporter is actually invoked — a hardcoded-correct mutant still passes. Test-hardening item, not a behavior defect.
- Carried cosmetic/wording items: exact-Opus NIT-C through NIT-J, exact-Sol NIT-1/NIT-2 (mostly overlapping: stale `production_mode` label on a real candidate, admission-band wording not fully propagated to a couple of docstrings/adapter prose, a couple of small label-shape observations). None REQUIRED, none safety- or admission-affecting.

## Infra note for the route-lessons file
Launching the exact-Opus lane via PowerShell `Start-Job` kills the child `claude.exe` within ~10-15s once the parent PowerShell process exits (job cleanup ties to the creating process) — looks like a cap/crash (`exit=-1`, `rate_limit_info` in the transcript) but isn't. Fix: launch the lane's `run.ps1`/`run_max.ps1` as a directly-tracked foreground process (e.g. `powershell -File ... > log 2>&1` under a backgrounded, harness-tracked Bash/PowerShell call) so the parent stays alive for the whole run.

Session done. Idle, no further lanes, no further git, unless the Lead sends another task.
