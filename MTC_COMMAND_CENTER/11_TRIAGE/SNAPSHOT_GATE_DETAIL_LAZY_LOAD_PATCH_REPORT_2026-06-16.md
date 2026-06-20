# Snapshot Gate-Detail Lazy-Load (M1) — Patch Report — 2026-06-16

Implements M1 from `SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md`, after the accepted
low-risk slim (`SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md`).
Read-only serialization + new read-only GET endpoint + frontend fetch-on-open.

## 1. Executive summary
Verbose gate detail moved out of the default `/api/snapshot` and lazy-loaded per strategy.
Default snapshot dropped **44.64 MB → 4.45 MB** (−90%; vs the original 115.56 MB this is
**−96%**), far below the ~25–30 MB target. Per-card gate `sub_scores` and verbose `notes` are
stripped from all 837 scorecard cards (and from pipeline `scorecard_v2` gates); gate
**scores + statuses + gate_summary** stay inline so Home, Leaderboard, Result Explorer, and
the all-versions table keep working unchanged. A new read-only endpoint
`GET /api/scorecard-detail?strategy_id=…` serves the full cards (with `sub_scores`) for one
strategy from an in-memory full-scorecards cache. Strategy Intelligence fetches it on open and
degrades gracefully (loading / summary-only states) if it fails. 69 API tests pass;
`node --check` passes; `/healthz` 200 read_only; `POST` (both endpoints) 405.

## 2. Preflight worktree scope
`git status --short` / `git diff --stat` run read-only. Pre-existing dirty tree from prior
accepted work (read_model.py, test_readonly_core.py, app.js modified; launcher .ps1 + new
tools/schemas/reports untracked). Nothing cleaned/reset/staged/committed/moved. Intended
touch scope: `read_model.py`, `server.py`, `app.js`, `test_readonly_core.py`, report + handoff.

## 3. Files changed
- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` — gate/card slim helpers
  (`_slim_gate`, `_slim_card`, `_slim_scorecard_cases`); `_slim_http_snapshot` now strips
  per-card gate `sub_scores` + collapses `notes`→`notes_count`/`notes_preview`, and strips
  pipeline `scorecard_v2` gate `sub_scores`; full scorecards retained in
  `_FULL_SCORECARDS_CACHE` during build; new `build_scorecard_detail()` + `_full_scorecards_cached()`.
- `08_DASHBOARD_APP/apps/api/mcc_readonly/server.py` — new GET route `/api/scorecard-detail`
  with `_send_scorecard_detail()` (param validation, 400/404/200; write verbs stay 405).
- `08_DASHBOARD_APP/apps/web/app.js` — `state.detailCards` cache; `loadStrategyDetail()` +
  `detailBestCard()`; `strategyModel` sources gate `sub_scores` from the loaded detail card
  (falls back to inline then empty) and exposes `detailStatus`/`detailCard`; `renderIntelligence`
  triggers fetch-on-open; `subscoreList(g, m)` shows loading / summary-only states;
  `advancedSection` uses loaded full detail (gates + cards) when available.
- `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py` — slim + endpoint assertions.
- `11_TRIAGE/SNAPSHOT_GATE_DETAIL_LAZY_LOAD_PATCH_REPORT_2026-06-16.md` + `_AI_MEMORY/*`.

## 4. Default snapshot slimming behavior
Kept inline on each card: ids (`strategy_id`, `base_strategy_id`), run/row ids, display name,
symbol, timeframe, profile, `gate1/1B/2/3.score` + `.max` + `.status`, `gate_summary.statuses`,
`gate_summary.promotable`, `promotion_status`, `provenance`, `profile_mapping`, `robustness`,
`universe_mismatch`, and all other small fields. Removed: `gateN.sub_scores` (all four gates);
verbose `notes` arrays → `notes_count` + short `notes_preview`. Pipeline
`rows[].scorecard_v2.gateN.sub_scores` also stripped (scores/statuses kept). Not touched:
`promotion_status`, `provenance`, `profile_mapping`, `robustness`, `universe_mismatch`,
research-only badge fields, profile-result rows, night-artifact safety fields.

## 5. New read-only detail endpoint
`GET /api/scorecard-detail?strategy_id=<id>`:
- GET only; `do_POST/PUT/PATCH/DELETE` remain 405.
- Validates the param: non-empty, ≤200 chars, no `/` or `\`, no control chars → else 400.
  Accepts an **id only**, never a path; cannot read arbitrary files.
- Returns `{schema_version, mode:"read_only", strategy_id, source:"scorecards", generated_at,
  count, cards:[…full cards…]}` from the in-memory full-scorecards cache (rebuilt on miss via
  a normal snapshot build). Full cards include gate `sub_scores` + notes.
- `count=0` / empty `cards` with HTTP **404** when no card matches; 200 when found.
- Match is `strategy_id ∈ {card.base_strategy_id, card.strategy_id}`. No mutation, no backtest.

## 6. Frontend fetch-on-open behavior
On opening a strategy, `renderIntelligence` calls `loadStrategyDetail(id)` (once per id;
cached). Default page renders from slim snapshot summaries. On success the full cards are
cached and the view re-renders only if still viewing that strategy. Gate 1 / 1B sub-score
panels use full detail when present; show `Loading full scorecard detail...` (ASCII) while
pending, `Full gate detail unavailable; showing summary only.` on a real network/server error,
and `No full scorecard detail found for this strategy.` when detail is empty. `loadStrategyDetail`
reads the JSON body even on **HTTP 404**: a 404 with `count=0` (or a 200 with zero cards) maps to
the `empty` status → empty-state message, while only network failures / non-OK 5xx map to the
error message. Advanced Technical Details uses loaded full gates/cards when available, else a
summary-only label. A failed/absent detail fetch never blocks the dashboard; no fetch happens
at startup or for Home/Leaderboard/Result Explorer.

## 7. Before/after snapshot size and latency
| | Original | After low-risk slim | After M1 (this) |
|---|--:|--:|--:|
| Snapshot MB | 115.56 | 44.64 | **4.45** |
| Bytes | 121,172,209 | 46,808,919 | 4,666,007 |
| Warm fetch s | ~5.9 | ~5.4 | ~8.7* |
| cards with gate sub_scores | 837 | 837 | **0** |
| `candidate_audit` / `by_strategy` | present | absent | absent |

\* warm fetch measured right after a forced refresh/rebuild; steady-state is cache-served.
Net reduction vs original: **−96%**.

## 8. Endpoint response validation
- `GET /api/scorecard-detail?strategy_id=GEN_ATR_PULLBACK_TREND` → 200, `count=11`,
  ~565 KB, fetch ~0.06 s, gate `sub_scores` present in returned cards.
- Unknown id → **404**, `count=0`, `cards=[]`.
- `strategy_id=../../etc/passwd` (path-like) → **400**; missing param → **400**.
- `POST /api/scorecard-detail` → **405**.

## 9. UI compatibility check
- `node --check app.js` → **JS_OK**, no redesign.
- Home / Leaderboard / Result Explorer read `scorecards.cards` (scores + `gate_summary`) and
  `night_artifacts` — all still inline; unaffected.
- Strategy Intelligence: gate scores/statuses render from inline summary; sub_scores arrive via
  the endpoint with loading/error fallback.
- Research-only badges (`provenance`, `profile_mapping`, `promotion_status`, `robustness`,
  `universe_mismatch`) preserved inline; legacy quarantine unaffected.

## 10. Tests run
- `node --check 08_DASHBOARD_APP/apps/web/app.js` → JS_OK.
- `python -m unittest discover tests` → **Ran 69 tests … OK**. New assertions: cards drop all
  gate `sub_scores` + `notes`; cards keep `gate_summary.statuses`; pipeline `scorecard_v2`
  gates drop `sub_scores`; detail endpoint returns full sub_scores for a real id; unknown→404;
  traversal/missing param→400; POST→405.

## 11. API / read-only validation
`/healthz` 200 `read_only`; `/api/snapshot?refresh=1` 200 (4.45 MB);
`/api/scorecard-detail?strategy_id=…` 200; `POST /api/snapshot` 405; `POST /api/scorecard-detail`
405; single server process after restart.

## 12. Safety confirmation
No source data deleted/mutated; no scorecard files written; score semantics unchanged (only
`sub_scores`/`notes` relocated, scores/statuses intact). Safety flags (`RESEARCH_ONLY`,
`UNIVERSE MISMATCH`, `NON-ROBUST`, provenance/profile_mapping/robustness) preserved inline. No
backtest/optimization/artifact/`top_results.json` generation. No Pine / MTC_V2 / backtest
engine / broker / live / paper execution touched. No write API added (both endpoints GET-only,
POST→405). Temp measurement scripts (C:\tmp) removed; never git-tracked.

## 13. Remaining limitations
- Full-scorecards kept in process memory (`_FULL_SCORECARDS_CACHE`, 120 s TTL); a detail
  request after expiry rebuilds the model once (same cost as a snapshot refresh).
- Per-strategy detail payload scales with versions (e.g. 11 cards ≈ 565 KB); acceptable for
  on-open fetch.
- `expert_quantlens` still appears top-level and embedded per card (<1 MB); not pursued.
- gzip (audit L4) still not enabled; would further cut on-wire bytes (transport-only).

## 14. Recommended next phase
- Optional: enable gzip on JSON responses (transport-only) for the remaining payloads.
- Optional: add a small client cache-bust note; consider caching detail by id across views.
- Snapshot size goal achieved; further work is polish, not bloat reduction.
