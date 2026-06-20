# Snapshot Gate-Detail Lazy-Load Patch Audit - 2026-06-16

## 1. Executive verdict

Verdict: **ACCEPT WITH SMALL FOLLOW-UP**

The M1 lazy-load patch meets the core goal: the default `/api/snapshot` is materially smaller, verbose gate `sub_scores` and notes arrays are removed from default scorecard payloads, gate summary semantics remain inline, and full scorecard detail is available through a read-only GET endpoint only when Strategy Intelligence opens a strategy.

Small follow-up: the prompt/report example `GEN_ATR_PULLBACK` is not a live strategy id in the current server response and returns 404. The verified live id is `GEN_ATR_PULLBACK_TREND`, which returns 200 with 11 full cards. Also, the loading text uses a unicode ellipsis instead of the prompt's three-dot literal, and the frontend empty-state string exists but unknown-strategy 404s currently route through the generic error/fallback state, not the empty state.

## 2. Files inspected

- `AGENTS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/CODEX_PICKUP_2026-06-08.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md`
- `_deepseek_driver/README.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/SNAPSHOT_GATE_DETAIL_LAZY_LOAD_PATCH_REPORT_2026-06-16.md`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/server.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js`

Preflight:
- `git status --short`: dirty worktree as expected from previous accepted phases.
- `git diff --cached --stat`: empty index.
- `git log --oneline -5`: latest commit `7ce20ff Slim dashboard snapshot payload`.
- Cheap harness attempted with empty write allow-list; it hit max iterations and wrote no repo files, so this verdict relies on direct verification.

## 3. Default snapshot verification

Live `/api/snapshot?refresh=1`:
- HTTP 200.
- Elapsed: 10.981 seconds.
- Raw content length: 4,666,007 bytes.
- `candidate_audit`: absent.
- `scorecards.by_strategy`: absent.
- `scorecards.cards`: 837 cards.
- Cards with `gate1.sub_scores`: 0.
- Cards with `gate1B.sub_scores`: 0.
- Cards with `gate2.sub_scores`: 0.
- Cards with `gate3.sub_scores`: 0.
- Cards with notes arrays: 0.
- Cards with `notes_count`: 837.
- First card has `gate_summary`: true.
- First card has `gate_summary.statuses`: true.
- First card has `gate_summary.promotable`: true.
- First card gate keys retain summary semantics:
  - `gate1`: `score,max,status,pass`
  - `gate1B`: `score,max,status,pass,verdict`
  - `gate2`: `score,max,status,pass,overfit_suspect`
  - `gate3`: `score,max,status,pass`

Pipeline `scorecard_v2` gate sub-score counts are also 0 for `gate1`, `gate1B`, `gate2`, and `gate3`.

Code inspection:
- `_slim_gate()` removes only `sub_scores`.
- `_slim_card()` preserves small fields and collapses list notes to `notes_count` / `notes_preview`.
- `_slim_scorecard_cases()` removes `scorecard_v2` gate `sub_scores` from pipeline rows/candidates.
- Full scorecards are cached before HTTP slimming.

## 4. Scorecard detail endpoint verification

Endpoint: `GET /api/scorecard-detail?strategy_id=...`

Live success path:
- `GEN_ATR_PULLBACK`: 404.
- `GEN_ATR_PULLBACK_TREND`: 200, 578,798 bytes, `count=11`.
- Returned detail includes `gate1.sub_scores`, `gate2.sub_scores`, `gate3.sub_scores`, and full `notes`.

Guard verification:
- Missing `strategy_id`: 400.
- `../../etc/passwd`: 400.
- `..\..\windows`: 400.
- `abc/def`: 400.
- Control character `%01`: 400.
- Unknown strategy: 404.
- POST/PUT/PATCH/DELETE to `/api/scorecard-detail`: 405.
- POST to `/api/snapshot`: 405.

Code inspection:
- `server.py` exposes only the GET route for scorecard detail.
- All write methods return 405 through shared read-only handlers.
- `_send_scorecard_detail()` rejects missing ids, ids longer than 200 chars, slash/backslash path-like values, and control characters.
- `build_scorecard_detail()` matches only in-memory `base_strategy_id` / `strategy_id` from loaded scorecards; it does not accept filesystem paths or read arbitrary files.

## 5. Frontend fetch-on-open verification

Startup fetch behavior:
- `loadDashboard()` fetches only `/healthz` and `/api/snapshot` / `/api/snapshot?refresh=1`.
- No full scorecard detail fetch is triggered on startup.

Strategy Intelligence behavior:
- `renderIntelligence()` calls `loadStrategyDetail(id)` when a strategy is opened.
- `loadStrategyDetail()` fetches `/api/scorecard-detail?strategy_id=...`.
- Detail fetches are cached per strategy id in `state.detailCards`; repeat opens do not refetch while status is `loading` or `ok`.
- `strategyModel()` uses `detailBestCard()` for full gate `sub_scores` and falls back to summary data when full detail is absent.
- `advancedSection()` switches between full detail and summary-only labels.

State strings verified in `app.js`:
- `Loading full scorecard detail...` prompt expectation is implemented as `Loading full scorecard detail...` with a unicode ellipsis character in source rather than three ASCII dots.
- `Full gate detail unavailable; showing summary only.`
- `No full scorecard detail found for this strategy.`

Note: because unknown ids return HTTP 404 and `fetchJson()` throws on non-OK responses, the empty-state string is present but not reached for unknown strategy responses today. The UI shows the summary-only fallback instead.

Non-detail pages:
- Home, Leaderboard, and Result Explorer do not call `/api/scorecard-detail`.
- Research-only / universe-mismatch / non-robust / provenance badge logic remains present in profile-result rendering.

## 6. API/read-only verification

`GET /healthz`:
- HTTP 200.
- `mode=read_only`.
- `overall_ok=true`.

No source scorecard file mutation was observed or required. The endpoint uses the same read-only scorecard reader path and an in-memory cache. No backtest, optimization, broker, live, paper, Pine, MTC_V2, or execution logic was run or modified.

## 7. Test results

- `node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`: passed with no output.
- `python -m unittest discover tests` from `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api` with `PYTHONPATH=.`: ran 69 tests in 26.355 seconds, OK.

The unittest output included expected dry-run and warning text from existing run-plan/profile-result tests; no test failure occurred.

## 8. Protected scope check

Commands:
- `git diff --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2`
- `git diff --cached --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2`

Result: no output from either command. No protected execution diffs and no staged protected diffs.

## 9. Issues found

1. **Small follow-up - stale or imprecise verified id in prompt/report**
   - The audit prompt and patch report cite `GEN_ATR_PULLBACK` as the known detail endpoint example.
   - Live result: `GEN_ATR_PULLBACK` returns 404.
   - Live verified id: `GEN_ATR_PULLBACK_TREND` returns 200 with 11 full cards.
   - Impact: endpoint behavior is correct for actual ids, but the report/example should be corrected to avoid a false verification claim.

2. **Small follow-up - empty state is present but likely unreachable for unknown ids**
   - `No full scorecard detail found for this strategy.` exists in `app.js`.
   - Current endpoint returns 404 for unknown strategy ids, and `fetchJson()` maps non-OK responses to the error state.
   - Impact: not a blocker because fallback is safe and summary-only, but the explicit empty state is not the current unknown-id path unless the endpoint returns 200 with `count=0` or the frontend treats 404 as empty.

3. **Small follow-up - loading text is not the exact prompt literal**
   - Prompt expected: `Loading full scorecard detail...`
   - Source uses the same text with a unicode ellipsis character.
   - Impact: behavioral state exists; only exact-string audit assertions would fail.

## 10. Recommended next action

Accept the patch. Then apply a small documentation/UI follow-up:
- Update the verified example id from `GEN_ATR_PULLBACK` to `GEN_ATR_PULLBACK_TREND`, or document that callers must use exact `base_strategy_id`.
- Either keep unknown strategy as 404 and remove the unreachable empty-state expectation, or make the frontend treat 404 detail responses as `ok` with empty cards so the explicit empty state is shown.
- Normalize the loading text to the exact three-dot prompt literal if downstream checks assert exact copy.
