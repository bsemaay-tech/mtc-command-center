# WP-P0-12 — Layer-A close-out record (DRAFT, Sat 2026-09-19; fields marked PENDING fill in as the roster lands)

**Status line (target):** *P0-12 research/engineering scope complete; production admission pending.* (`OD-20260913-P012-SCOPE-1`)

## 1. Scope closed by this record
The Hyperliquid own-account evidence capture tool and the funding-intake adapter (D-1..D-6 accepting half), each reviewed by two flagships of different families plus Gemini and reproduced by the Lead, merged to `master` under the owner's explicit release acts. Production admission (Layer B: OPEN-01..OPEN-10, the qualified-human review, KVM2 gate order, real-capture admission) is NOT granted: the intake fence `ACCEPTED_EVIDENCE_KINDS == (SYNTHETIC_FIXTURE,)` stays, every real capture stays `REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD`.

## 2. Merge roster
| Candidate | Branch / sha | Exact-Opus | Sol | Gemini | Lead reproduction | Owner release act | PR / merge |
|---|---|---|---|---|---|---|---|
| Capture tool NIT slice | `feature/p012-path1-capture-20260914` @ `1029d6e9` (= `af921d75` + NITs 1-7) | base `af921d75` PASS-WITH-NITS (`P1CAP/LEAD_ADJUDICATION_P1CAP_T0.md`); slice re-read PASS-WITH-NITS, 0 REQUIRED, 5 NITs carried (`P1CAP/LEAD_ADJUDICATION_P1CAP_NIT_T0.md`, `ATTEMPT3_PASS_WITH_NITS_1029d6e9/`) | REQUEST_CHANGES on `1029d6e9` (R-1 stale later page accepted as terminal; R-2 2xx non-JSON state accepted) - both CONFIRMED by the package session (CT13 `P1CAP_SOL_20260919/`); repair round 1 = `9f1aa532` (12:2x; TDD, 34/34, Bridge 1632/0, 2 mutants, guard PASS) -> Gemini + Opus[MAX] + Sol on the new bytes | PASS COUNTED (`P012_S16_REVIEWS_20260913/P1CAP_NIT_GEMINI/LEAD_ADJUDICATION.md`, 0 REQUIRED, 7/7 CLOSED) | package session: 32/32 targeted, Bridge 1630/0, mutants RED (`P1CAP_NIT_SLICE_20260919/`); Lead: 32/32 targeted re-run on the pinned interpreter 11:2x | `OD-20260919-P012-MERGE-CAPTURE-GO-1` | PENDING |
| Intake accepting half + NIT slice (owner `INTAKE-MERGE slice`) | `feature/p012-funding-intake-nit-20260919` @ `8cbf4f1a` (= `a871e429` + NITs 1-9/NIT-A + D6-START B) | base x2 PASS-WITH-NITS; slice [MAX] PASS-WITH-NITS 0 REQUIRED (`P012INTAKE/LEAD_ADJUDICATION_P012INTAKE_NIT_T0.md`) | PASS-WITH-NITS, REQUIRED none, NITs 1-3 carried (12:07-12:31 on Codex Pro; `SOL_QUEUE_20260919/P012INTAKE/sol/`) | PASS COUNTED 10/10 (`P012_INTAKE_NIT_GEMINI`) | intake session: RED 8/71, GREEN 240, Bridge 1707/0, 9 mutants (`NIT_SLICE_20260919/`) | `OD-20260919-P012-MERGE-INTAKE-GO-1` + `OD-20260919-P012-INTAKE-MERGE-SLICE-1` | **PR #196 MERGED 12:36 UTC+3 -> master `5214f169`** (CI 9/9 green) |

## 3. Carried into the next pull requests (not blocking this closure)
- (moved into the merge roster above by `INTAKE-MERGE slice`) intake NIT slice `8cbf4f1a` (intake session, committed 11:2x: RED 8/71 on `a871e429` bytes, GREEN 240, Bridge 1707/0, 9 mutants, ruff parity, guard PASS; Gemini delta + exact-Opus [MAX] PASS-WITH-NITS 0 REQUIRED 11:5x, NIT-B -> owner `D6-GRID A|B`), own roster; PR C after PR B.
- Capture tool: any NITs of the slice re-read (PENDING).
- Oracle capture O-1 (`O-1 wait`), the O-2 tolerance 0.05 %, the r3 real capture with tool-filled D-4 - all owner-gated.

## 4. Evidence pointers
Records in the run root `C:/tmp/CLAUDE_P0_RUN_20260913/` mirrored to CT13 `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/`: `P012_CLOSEOUT_PLAN_20260919.md`, `P1CAP_NIT_SLICE_20260919/`, `P012_FUNDING_INTAKE_20260915/`, `P012_PATH1_REAL_CAPTURE_20260917/r2/` (first real D-1..D-6 candidate, non-accepting by design), the queue log `OPUS_QUEUE_20260916/QUEUE_LOG.txt`, CT13 `DECISIONS.md` rows `OD-20260919-P012-*`.

## 5. Register row (to add in CT13 next to the WP-P0-12 rows)
`WP-P0-12 | research/engineering scope COMPLETE 2026-09-19 (capture tool <sha>, intake a871e429 merged; rosters above) | production admission PENDING (Layer B, owner-gated)`

Recorded by the P0 Claude Lead (session 7). PENDING fields are filled only from verdict files, never from a chat message.
