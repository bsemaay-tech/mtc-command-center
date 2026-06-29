# Results → MTC Command Center — artifact map (canonical)

**Why:** cold-onboarding audits (6 models, 2026-06-29) unanimously flagged W3 as PARTIAL —
the result-to-dashboard pipeline is real but scattered across writers/readers with no single map,
so two agents wire the same backtest output differently. This file is the **single authoritative
map**: each artifact → its writer → its dashboard reader → the view it populates → when to produce
it. Read this before publishing any result to the dashboard.

> Artifact **generation is approval-gated** (see `_AI_MEMORY/DO_NOT_TOUCH.md` "No execution").
> NEVER fabricate `backtest_profile_result.json` or `top_results.json`
> (`00_AGENT_PROTOCOLS/NO_PROMOTION_SAFETY_RULES.md`). Non-robust / insufficient results stay
> `RESEARCH_ONLY` and produce NO profile/leaderboard artifact.

## The map

| Artifact | Writer (who produces it) | Reader (dashboard) | Dashboard view | When |
|---|---|---|---|---|
| `MEGA_walk_forward_results.json` (+ exported `<run>_results.json`) | `mega_walk_forward.py` (the engine itself) | `backtest_reader.py` — globs `05_BACKTEST_RESULTS/*_results.json` and `*/MEGA_walk_forward_results.json` | **Backtest Runs** tab | **Every run, automatic.** No extra step. |
| `scorecard_v2/*.scorecard.json` | `mcc_night_tail.sh` (CPCV + PBO + scoring enrichment pipeline) | `scorecard_reader.py` | Strategy Intelligence — gates / scorecards | When you are **scoring** a strategy (Gate 1/1B/2/3). |
| `run_plan.json` + `artifact_index.json` | `build_run_plan.py` (review-only, `approved:false` until frozen) | `night_artifacts_reader.py` | Planner / Advanced Artifacts / SI §4 | When planning an **approved** run (universe frozen). |
| `backtest_profile_result.json` | `build_profile_result_artifact.py` (**never fabricates KPIs**) | `night_artifacts_reader.py` (schema-validated vs `06_SCHEMAS/backtest_profile_result.schema.json`) | Result Explorer / SI profile buckets + KPIs | **Only for a validated profile result.** Not for smokes / `INSUFFICIENT_TRADES` / non-robust. |
| `top_results.json` | **NO sanctioned writer** — must come from an approved same-bucket multi-row set | `night_artifacts_reader.py` (read-only) | Leaderboard | **Only** from an approved same-profile multi-row result set. Never hand-write. |
| `leaderboard_delta.json`, `benchmark_update_candidate.json` | approval-gated tooling | `night_artifacts_reader.py` | SI / benchmark panels | Rare, approval-gated. |

Night-artifact reader states (per artifact): `absent` → not found; `invalid` → unparseable;
`incomplete` → parsed but fails schema; `usable` → parsed + schema-valid. Schemas live in
`06_SCHEMAS/` (protected — read, don't edit without approval).

## Which subset applies to MY run?

**Single-strategy / sprint run (the common case):**
1. Run the engine (`mega_walk_forward.py …`). It writes `MEGA_walk_forward_results.json`.
2. **That is enough for the dashboard** — `backtest_reader.py` auto-surfaces it in **Backtest Runs**.
3. Do **NOT** run `mcc_night_tail.sh`, `build_profile_result_artifact.py`, `aggregate_overnight_iters.py`,
   or write `top_results.json` for an ad-hoc/smoke run. Those are for scoring/profile/leaderboard
   publishing of a **validated** result and are approval-gated.

**Overnight sweep:** follow the runbook §6.4 closing sequence in order
(aggregate → alpha_vs_buyhold → morning report → dashboard upgrade → lessons). Step 4 there is the
dashboard upgrade that feeds `backtest_reader.py`.

## Verify the dashboard saw it (read-only)
```
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api
python -c "from mcc_readonly.backtest_reader import build_backtest_status; from pathlib import Path; bs=build_backtest_status(Path('<MCC_ROOT>')); print(len(bs['runs']), bs['runs'][0]['run_id'])"
```
If your run isn't listed, the engine output didn't land in `05_BACKTEST_RESULTS` (check
`MEGA_OUTPUT_DIR`) — not a dashboard bug.

## One-line summary
Ad-hoc backtest → engine writes `*_results.json` → appears in **Backtest Runs** automatically.
Everything else (scorecards, profile result, leaderboard) is a separate, validated, approval-gated
publishing step — and `backtest_profile_result.json` / `top_results.json` are **never fabricated**.
