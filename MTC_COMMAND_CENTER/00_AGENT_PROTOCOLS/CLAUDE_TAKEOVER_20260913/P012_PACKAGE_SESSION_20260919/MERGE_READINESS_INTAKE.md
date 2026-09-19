# MERGE_READINESS — WP-P0-12 funding intake NIT slice `8cbf4f1a` — 2026-09-19

**Branch:** `feature/p012-funding-intake-nit-20260919`, worktree `C:/tmp/P012_INTAKE_NIT_20260919`, base `a871e429` (which merges separately, as-is, per `OD-20260919-P012-INTAKE-ASIS-1`).
**Scope:** closes NITs 1-9 + NIT-A from the lane-8 exact-Opus read of `a871e429`, plus owner ruling `D6-START B` (`OD-20260918-P012-D6START-B-1`).

## Roster (all four legs complete)

| Leg | Verdict | Evidence |
|---|---|---|
| Builder self-QA | RED 8/71, GREEN 240/1, full suite 1707/1, ruff 7/7 (0 new), 9 mutants each killed by its named test, guard PASS | `C:/tmp/CLAUDE_P0_RUN_20260913/P012_FUNDING_INTAKE_20260915/NIT_SLICE_20260919/LEAD_VERIFICATION_P012_INTAKE_NIT.md` |
| Gemini (gemini-3.8-flash-high, detection/delta) | **PASS**, COUNTED (exit 0, sentinel, native-read audit 37/0 outside/0 failures), all 10 items CLOSED, `scope_clean: true`, 0 findings | `C:/tmp/P012_S16_REVIEWS_20260913/P012_INTAKE_NIT_GEMINI/` (cid `566ab938-71ce-4c58-9232-f7131f20cd37`; `LEAD_ADJUDICATION.md`) |
| Exact-Opus (claude-opus-5, xhigh, MAX profile — Pro capped) | **PASS-WITH-NITS**, 0 REQUIRED, all 10 items independently VERIFIED (own mutants, own failing inputs, own real-r1 dry run, own 4-way dict-reorder determinism check); standout NIT-B escalated to owner (non-blocking) | `C:/tmp/OPUS_QUEUE_20260916/P012INTAKE/ATTEMPT6_PASS_WITH_NITS_8cbf4f1a/OPUS_REPORT.md`; `LEAD_ADJUDICATION_P012INTAKE_NIT_T0.md` |
| Exact-Sol (gpt-5.6-sol, xhigh, Codex PRO `free`, second flagship family) | **PASS-WITH-NITS**, 0 REQUIRED, all 10 items independently VERIFIED (own failing inputs per D-1..D-6, own start-limit mutant, own boundary sweep, own real-r1 dry run, own RED reproduction) | `C:/tmp/SOL_QUEUE_20260919/P012INTAKE/sol/SOL_T0_REPORT.md`; CT13 `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P012INTAKE_SOL_20260919/LEAD_ADJUDICATION_P012INTAKE_SOL_T0.md` |

**Lead (this session) reproduction:** grep-verified key citations from both flagship reports against the `8cbf4f1a` bytes; independently reproduced Opus's NIT-B (natural r1-style stamp in the payments-position branch → `CANDIDATE_BINDING_OUT_OF_INTERVAL` under the fixed code — CONFIRMED) and Sol's NIT-3 (a hardcoded-correct `_export_tool_outcome_today` mutant still passes the current adapter test — CONFIRMED); worktree `git status --porcelain` empty after both reviewer lanes.

## Open items (none blocking; roster is complete as of both flagships returning PASS-WITH-NITS)

- **Owner one-liner needed before O-1 / the next real multi-window capture** (not before this merge): `D6-GRID A` (shift the D-6 completeness grid to `[start+1h, end]` to match the new admission band) or `D6-GRID B` (leave the grid, document the resulting dead zone). Raised by exact-Opus (NIT-B), independently reproduced by the Lead. Relayed to the owner by the P0 Lead session alongside the roster's other pending one-liners.
- Carried cosmetic/wording NITs (Opus C,D,E,F,G,H,I,J; Sol 1,2,3) — none REQUIRED, none safety- or admission-affecting; candidates for a follow-up slice, not this merge.

## Owner one-liner for this merge

`P012-MERGE intake go` (`OD-20260919-P012-MERGE-INTAKE-GO-1`, already recorded as conditional on roster completion) — roster is now complete on `8cbf4f1a`.

Recorded by the P0-12 INTAKE session (Claude Sonnet 5). No PR opened or merge performed by this session; the P0 Lead session opens/merges per standing delegation.
