# WP-P0-20 Claude takeover handoff

Prepared: `2026-09-13T09:39:02Z`

## Exact state

- Worktree: `C:/P020_IMPL_20260912`
- Branch: `feature/p020-successor-20260912`
- Clean HEAD: `b9b72f858dc830a9389517f79da5ea3c1fa6122c`
- Implementation candidate before prose-only repair: `52422017e032b11d5cdc31aaeb94d8cfda1a42cf`
- Base used by final implementation reviews: `d60b7694332d1e3513e2c114e01698c3ed072279`
- Current remote master, read-only verified: `fcac0ac67cf2682693ad28138b1a56e15a0846f2`
- Current branch relation to remote master: 51 commits behind / 25 ahead; 40 changed paths.
- No remote feature branch, PR, push or merge. Read-only `merge-tree` showed no textual conflict signal.
- Current shared state: HELD for `P012-S16-G5-ITEMS14-WINDOW1`. After RELEASE remain parked for Claude ownership transfer; do not auto-resume.

## Owner-authorized scope and decisions

1. Benchmark Option 1: authoritative venue `min_qty` and `min_notional` may be zero; `tick_size`, `lot_size`/quantity step and `contract_multiplier` remain positive. Preserve exact record values and metadata identity; no normalization or invented venue fact.
2. Narrow typed time exit: a true holding-limit exit records existing immutable `FillDecision.exit_id = TIME_STOP`; generic `MARKET_EXIT` and a caller-truncated slice receive no `time_bars` credit.
3. Newly authorized on 2026-09-13: preregistered benchmark profile-selection procedure. Authorization was received while the P012 quiet window was active and immediately superseded by the owner-requested Claude takeover. It is APPROVED BUT NOT STARTED.
4. Existing bounded measurement authority resumes only after a frozen profile passes the preregistered eligibility contract and required review.
5. No live/production trading, host, credentials, ARM, orders, deploy, PAYG, profitability/strategy-quality claim, full grid, 100,000-trial execution, destructive Git, push, PR or merge authority.

## Completed work

- Option 1 and typed-time-exit implementation and repair are locally committed.
- Lead reproduced the exact repair boundary: unavailable economic peers produce typed refusal; only the true elapsed holding limit produces `TIME_STOP`; truncated slices are generic.
- Lead evidence on `52422017`: 304 full P020-plus-identity tests; 231 CI-selected tests with two expected Pydantic warnings; 73 owner-policy tests; all 11 workflow checkers; CP1254-safe acceptance output.
- Acceptance remains intentional exit 1: 8/16 criteria MET / `NOT ACCEPTABLE`.
- Enabled REQUIRED control coverage is 17/17 across five mutually exclusive fixtures; the canonical single run still reports nine gaps.
- Fresh exact Sol/xhigh Standards PASS and Spec PASS on `52422017`.
- Two complete Gemini 3.7 Flash High slices returned supplemental PASS and covered all 11 changed paths.
- Exact Opus 5/xhigh post-reset verdict was `REQUEST_CHANGES` for one stale P2 paragraph only; it reported no required protected-implementation defect.
- That paragraph alone was corrected and self-checked as T2 prose under current policy, commit `b9b72f85`. The reporter still returns 8/16 and exit 1; worktree is clean.
- Option 1 benchmark preflight preserved exact record facts `1/1/0/0/1`. Existing frozen 15-trial plan has only 4/15 trade-bearing trials, so no measured run/output root/resource result/extrapolation exists.

## Full-package acceptance blockers

The live reporter still blocks exactly:

1. `cost_admission`
2. `p012_full_acceptance`
3. `frozen_probe_compatibility` (two known failures)
4. `production_admission`
5. `real_before_after`
6. `dependent_disposition`
7. `real_benchmark`
8. `independent_reviews` (external evidence is not self-certifiable by the reporter)

WP-P0-20 is therefore not package-accepted or merge-ready. P012 remains an external dependency. Current branch also needs later current-master reconciliation, required Bridge CI on an up-to-date head, PR review and explicit push/PR/merge authority.

## Newly authorized benchmark profile-selection work

Purpose: construct a deterministic trade-bearing workload for successor-path throughput/restart measurement only. It is not profitability, optimization, strategy ranking, promotion or economic truth.

Read-only preparation identified the smallest defensible shape; it is a proposal to freeze and review, not executed evidence:

- Preserve exactly five BTCUSDT frozen datasets/timeframes: 15m, 1h, 2h, 4h, 1D.
- Preserve three measured sizes per selected family: 512, 1024, 2048 rows; exactly 15 trials; one process.
- Candidate universe: the nine existing OHLC-only `GEN_*` families and their 359 already-registered parameter records. No new parameters, risk values, strategy code or data.
- Freeze deterministic ordering before reading eligibility results: family order by `(registered grid size, strategy_id)` and parameters by canonical JSON bytes.
- Eligibility is binary only: an actual committed P020 2.1.0 successor trade event exists and ledger projection succeeds. Do not expose/compare returns, PnL, ranking or strategy metrics.
- Use a fixed calibration window distinct from the locked measurement suffixes; record exact offsets/prefix hashes before execution. The 1D dataset has only 2,409 derived rows, so window separation must be checked carefully rather than assumed.
- Preserve five distinct families. Select the lexicographically first complete family-to-timeframe matching from the frozen eligibility matrix; never choose the best economic result.
- Once frozen, execute one locked 15-trial eligibility check. If any trial is non-trade-bearing, return `BENCHMARK_PROFILE_BLOCKED`; no adaptive second selection or silent substitution without new owner direction.
- Only if all 15 pass may the already-authorized bounded interrupted/resumed versus uninterrupted measurement run start in a new non-existing external output root.
- The exact preregistration/fixture must receive the applicable independent T0 review before eligibility execution because it controls economic-path evidence.

Apply Ponytail/YAGNI: extend the existing external driver/plan/runbook; do not build a general optimizer or add dependencies.

## Important paths

### Durable/current state

- `C:/tmp/P020_LEAD_20260912/STATUS.md`
- `C:/P020_IMPL_20260912/check_p020_acceptance.py`
- `C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md`

### Benchmark preparation

- `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_ADAPTER_DECISION_20260912.md`
- `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_PLAN.json`
- `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_RUNBOOK.md`
- `C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py`
- `C:/tmp/P020_LEAD_20260912/benchmark/SYNTH-P020-BOUNDED-{INSTRUMENT,COST,FUNDING}-V1.json` plus `.sha256`
- `C:/tmp/P020_DERIVED_20260912/selected_manifest.json` (recorded SHA-256 `712ddc2745c7fec8b3ab52e0e07d42a26d8d2a216ba0ea638192e795aa0b0e9a`)
- `C:/tmp/P020_LEAD_20260912/dataset/STRATEGY_INPUT_COMPATIBILITY.json`

### Reviews/evidence

- `C:/tmp/P020_LEAD_20260912/reviews/p020_52422017/CANDIDATE_FULL_DIFF.patch`
- `C:/tmp/P020_LEAD_20260912/reviews/p020_52422017/SOURCE_IDENTITY.json`
- `C:/tmp/P020_LEAD_20260912/reviews/p020_52422017/OPUS_POSTRESET_STREAM.jsonl`
- `C:/tmp/P020_LEAD_20260912/reviews/p020_52422017/OPUS_POSTRESET_EXIT.txt`
- `C:/tmp/P020_LEAD_20260912/reviews/p020_52422017/gemini_slices/COVERAGE_MANIFEST.json`
- `C:/tmp/P020_LEAD_20260912/reviews/p020_52422017/gemini_slices/GEMINI_SLICE_{A,B}_RESULT.json`
- `C:/tmp/P020_LEAD_20260912/reviews/p020_52422017/opus_tmp/acceptance.txt`

## Mutable/uncommitted state and processes

- Repository worktree: clean; zero tracked or untracked changes.
- No profile-selection procedure file, result or output root has been created.
- External benchmark files listed above are existing preparation artifacts and are not repository commits.
- Process check at handoff: no active `run_bounded_benchmark.py`, `p020_benchmark_runner`, `ds_agent.py`, or P020 launch/resume helper other than the checking shell itself.
- Do not delete or overwrite existing benchmark/review artifacts. New outputs require fresh non-existing paths.

## Routing and required roles

- Owner requests Claude takeover because Codex usage is about 4%; priority order is P012, then P020, then P013, then other packages.
- No new provider call may be launched by this parked Lead.
- Use included subscriptions only; no PAYG, purchase, reset or silent model substitution.
- Current T0 contract: exact `claude-opus-5` xhigh plus exact `gpt-5.6-sol` xhigh, with required Gemini High corroboration, and independent Lead reproduction. Coordinate Gemini quiet windows through Mentor.
- Existing implementation reviews may be reused only for unchanged reviewed scope. The new profile-selection contract is new evidence logic and requires fresh applicable review before execution.

## Next action and stop condition

NEXT ACTION: after Mentor RELEASE and explicit Claude ownership claim, reverify clean `b9b72f85`, current refs, P012 dependency and source hashes. Freeze the minimal profile-selection preregistration in external scratch first, audit it before any eligibility run, then execute the one-shot selection/locked eligibility procedure within the approved boundaries.

STOP CONDITION: stop on identity/hash mismatch, missing data, overlapping or unfrozen selection/measurement windows, unavailable required reviewer, no distinct five-family matching, any locked trial without a committed successor event, source drift, a new shared HOLD, or any need for new economic facts/parameters/PAYG/live/production/push/PR/merge authority. Preserve evidence and ask the owner only for a materially new decision.

WAITING FOR OWNER: Nothing for the preregistered profile-selection procedure itself. Claude takeover and the current Mentor RELEASE are operational dependencies; P012/full-package admission and later PR/merge authority remain separate.
