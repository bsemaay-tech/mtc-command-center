# Hours and cost — 2026-08-29 day session (Lead: Claude Fable 5, orchestrator-only)

Raw lane-by-lane times: `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt` (session section from
"R-SESSION start"). Times are lane start/end stamps recorded at dispatch/read moments; treat as
±5 min. Session ~09:45–17:20.

## Wall clock per package (lane time, overlapping — lanes ran in parallel)

| Package | Lane rounds | Approx wall clock |
|---|---|---:|
| WP-P0-11 (repairs 4–7 + audits + park/unpark) | 4 repair rounds, 9 audit lanes | ~5 h spread across the day |
| v3 / stage-4 design (revision + check + re-pin) | W44, G15, W44b | ~1 h 40 m |
| Registry guard (build→confirm→PR #140) | W1, N37 | ~1 h 20 m |
| Scorecard honesty (build→reject→repair→re-confirm→PR #141) | W34, N38, W34b, G13(died), N41 | ~2 h 30 m |
| Range Filter docs (build→confirm→PR #138) | W2, P12 | ~1 h |
| Survey mainnet-lock fix (build→die→complete→confirm→PR #139) | W9, W9b, P12 | ~1 h 10 m |
| Bridge fail-closed design (design→dual audit→repair→dual delta→fix) | W10, N36, P13, W10b, N43, P15, W10c | ~3 h |
| Migration/flatten runbook (3 repair rounds + 3 checks + final confirm) | W1112, G12, W1112b, G12b, W1112c, P17 | ~2 h 30 m |
| P0-20 papers + P0-12 design (+ audits) | W20P, W45, G16, N45 | ~1 h 30 m |
| Owner docs/decisions/feed/handoff | N30, N31, N32, G10, G14, P10, Lead | ~2 h |

## Session outcomes

- **5 PRs merged to master:** #138, #139, #140, #141 (+ continuous feed pushes on
  `docs/session-20260829-status`). Master ended at `d5be879e`.
- **~45 lanes dispatched** across 6 subscription routes; peak 8 concurrent.
- Owner decisions processed: 12 morning asks + 3 hash-memo YES + P0-12 kernel approval +
  repair-7 approval + mandatory-parallel directive.
- WP-P0-11: repairs 4–7; parked once by its own pre-written stopping rule, un-parked by owner;
  residual `run_*` label question open for next session.

## Waste, recorded as Lead errors

- **~90 min partial idle 13:20–15:05** — two Codex quota deaths (third, fourth) with a
  too-long waiter timeout. Structural fix deployed: death-detecting waiters (log-quiet
  heuristic per lane type). Smaller sibling of the night's 4-hour incident.
- 3 Grok silent deaths (W9, G13 + one probe-recovered); each recovered by completion lanes
  that treat orphaned edits as claims.
- Codex quota deaths total: 4 (N33/third 11:26, N42/third 13:23, W1112c/fourth 13:20,
  N46/secondary 16:14) — all requeued.

## Cost

**USD is NOT MEASURED by the Lead.** CodeBurn read **$118.85 today / $4,988.31 month at
session start (~09:45)**; no closing figure captured by the Lead — read CodeBurn for the delta.
Codex token counts appear in each lane's RUN.log footer; not aggregated here.
