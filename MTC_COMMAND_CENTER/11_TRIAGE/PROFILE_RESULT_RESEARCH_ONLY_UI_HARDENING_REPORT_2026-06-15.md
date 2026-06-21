# Profile-Result Research-Only UI Hardening — Report — 2026-06-15

## 1. Executive summary
The first profile-separated pilot artifact is real but non-native-universe (strategy id
implies US-equities/10m; soak evidence is crypto at 1h/4h/1D) and non-robust
(`robust_final=false`, `promotion_status=RESEARCH_ONLY`). This patch makes those facts
**unmissable in the UI** so the pilot can't be read as native-universe validation. Added
read-only badge/flag helpers and surfaced them in Result Explorer (bucket rows + active
comparison + banner), Strategy Intelligence §5 preview (banner + badges), Leaderboard
(research-only relabel + per-card badges), and Advanced Artifacts (quality-flag counts). A
minimal read-only reader passthrough was added so `provenance.universe_mismatch` and
`profile_mapping.is_interpretation` reach the snapshot. No KPIs faked, no artifacts created,
API still read-only.

## 2. Files changed
- `08_DASHBOARD_APP/apps/web/app.js` — `profileRowFlags()`, `profileRowBadges()`, `profileRowHasFlags()`, `researchOnlyBanner()`; wired into `bucketBlock`, `renderResultExplorer`, `explorerPreviewSection`, `leaderboardValidatedPanel`, `renderArtifacts`.
- `08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py` — `_extract_profile_rows` now forwards `provenance` (per row) + `profile_mapping` (row or doc-level). Read-only; no other behavior changed.
- `08_DASHBOARD_APP/apps/web/index.html` — cache bump `app.js?v=8 → v=9`.
- `08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py` — +1 test (`test_reader_passes_through_badge_data`).
- `11_TRIAGE/PROFILE_RESULT_RESEARCH_ONLY_UI_HARDENING_REPORT_2026-06-15.md` — this report; `_AI_MEMORY/*` updated.

## 3. Result Explorer changes
- **Official bucket rows** (`bucketBlock`): new **Flags** column showing `RESEARCH ONLY` / `UNIVERSE MISMATCH` / `NON-ROBUST` / `PROFILE MAPPING INTERPRETED`; robustness cell shows `non-robust` (warn) when `robust_final=false`; an amber caption appears above the table when any row is flagged.
- **Active Comparison State**: prominent `researchOnlyBanner(pr0)` above the panel (strategy id, source universe/TF, mismatch text, promotion status, robust_final, source path); badge row added; Artifact Status reads "present — research-only" when flagged.
- Official buckets still populate from real `profile_results`; legacy scorecard rows remain quarantined under "Legacy Scorecard Reference".

## 4. Strategy Intelligence changes
§5 Backtest Result Explorer preview: `researchOnlyBanner(pr)` shown above the best
profile-separated result, and badges appended to the bucket head. Copy: "Research-only
profile result. Real metrics are present, but this result comes from a non-native
universe/timeframe and is not a production or paper-trading validation."

## 5. Leaderboard / Home safety check
- **Leaderboard**: `leaderboardValidatedPanel` now detects flagged rows; when any are flagged the heading/banner change to "Top profile-separated results (research-only — not validated category winners)", the rank glyph becomes ⚠, and per-card badges render. Not shown as production/paper-ready.
- **Home**: leaderboard/benchmark previews consume **scorecard cards**, not `profile_results`, so the pilot is not displayed as a validated/paper-ready winner there. No change required (verified in `renderHome`). Future profile-result use on Home should reuse `profileRowBadges`.

## 6. Advanced Artifacts / Diagnostics check
Advanced Artifacts still lists `backtest_profile_result.json` as **usable** (correct). Added
a "Profile Result Rows — Quality Flags" panel (only when rows exist) showing: Profile Rows,
Universe Mismatch Rows, Research-only Rows, Non-robust Rows (for the pilot: 4 / 4 / 4 / 4),
with an amber note. Built from existing snapshot data only; no overbuild. Diagnostics
unchanged.

## 7. Tests and validation
- `node --check app.js` → **JS_OK**.
- API suite → **Ran 69 tests … OK** (+1 reader-passthrough test; existing converter/invariant/night-artifact tests green).
- New test asserts the snapshot row carries the four badge signals (promotion RESEARCH_ONLY, robustness.robust_final false, provenance.universe_mismatch truthy, profile_mapping.is_interpretation true).
- Live `/api/snapshot?refresh=1` (after reader reload): `profile_result_rows=4`; row shows promotion RESEARCH_ONLY, robust_final false, universe_mismatch true, is_interpretation true.
- `POST /api/snapshot` → **405**; `/healthz` → **200**.
- Note: the running server had cached the old reader (multiple stale `pythonw` instances); it was restarted with cleared bytecode so the passthrough fields appear live (see §9).

## 8. Safety confirmation
No backtest, no optimization, no `top_results.json`, no fabricated KPIs (badge logic reads
existing fields only). No Pine / MTC_V2 / backtest engine / broker / live / paper execution
touched. No POST/PUT/PATCH/DELETE behavior added. Reader change is read-only passthrough.
Official bucket still sourced from the real artifact; legacy quarantine intact.

## 9. Remaining limitations
- **Runaway server processes (ops, pre-existing):** ~150 stale `pythonw -m mcc_readonly serve` instances were found (persistence-loop relaunching without a single-instance guard). They were stopped and one fresh instance started to verify this patch, but the launcher should be fixed to prevent re-accumulation. Flagged as a separate ops task — not modified here.
- `universe_mismatch` is a descriptive string (truthy) rather than a strict boolean; badge logic treats any truthy value as mismatch. Fine for current data; a boolean field could be added later.
- Badge logic is JS; validated indirectly via the Python reader-passthrough test + live snapshot. No jsdom harness yet.

## 10. Recommended next phase
- Fix the dashboard-server launcher to enforce a single instance (kill-or-skip if port bound) and stop the process pile-up.
- When a native US-equities-10m soak exists, regenerate the pilot from that source for a clean-universe row (badges then auto-clear).
- Consider promoting `universe_mismatch` to an explicit boolean + structured detail in the converter for stricter UI logic.
