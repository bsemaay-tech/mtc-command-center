# Snapshot Payload Slim — Low-Risk Patch Report — 2026-06-16

Implements L1+L2+L3 from `11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md`.
Read-only serialization patch. No frontend, schema, data, or execution changes.

## 1. Executive summary
HTTP `/api/snapshot` slimmed from **115.56 MB → 44.64 MB** (−70.9 MB, **−61%**), beating the
~75 MB target. Achieved by stripping three UI-unused / count-only fields from the HTTP payload
only, after the rich internal model is built and consumed:
- dropped `scorecards.by_strategy` (duplicate of `cards`; never read by frontend);
- omitted top-level `candidate_audit` (CLI/tests still build it; never read by frontend);
- collapsed `candidate_pipeline.rows[].scorecard_v2_cases` arrays to integer counts (frontend
  already reads this as a count).
Underlying readers, CLI `audit` command, source artifacts, and `scorecards.cards` untouched.
69 API tests pass; `node --check` passes; `/healthz` 200 read_only; `POST` 405.

## 2. Preflight worktree scope
`git status --short` / `git diff --stat` run read-only. Pre-existing dirty tree from prior
accepted work (read_model.py, test_readonly_core.py modified; launcher .ps1, schemas, tools,
tests, 11_TRIAGE reports untracked). Nothing cleaned/reset/staged/committed/moved. Intended
touch scope: `read_model.py` (snapshot builder), `test_readonly_core.py` (contract test),
report + handoff.

## 3. Files changed
- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` — added `_slim_http_snapshot()` (+
  `_slim_rows_cases()`, `_count_or_passthrough()` helpers); `build_dashboard_snapshot` now
  assembles the dict as `snapshot` and returns `_slim_http_snapshot(snapshot)`. `candidate_audit`
  is still built and fed to `build_mtc_v2_readiness`; it is just no longer emitted in the dict.
- `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py` — flipped the `candidate_audit`
  presence assertion to absence; added slim assertions (cards present, by_strategy absent,
  scorecard_v2_cases int/None not list).
- `11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md` — this report.
- `_AI_MEMORY/SESSION_LOG.md`, `NEXT_STEPS.md`, `ACTIVE_FILES.md` — updated.

## 4. Snapshot builder changes
`_slim_http_snapshot(snapshot)` returns a shallow-copied dict with:
- `slimmed.pop("candidate_audit", None)`;
- `scorecards` shallow-copied with `by_strategy` popped (only if present); `cards` kept;
- `candidate_pipeline` shallow-copied; `rows` and `candidates` lists rebuilt with each row's
  `scorecard_v2_cases` passed through `_count_or_passthrough` (list→`len`, int/None preserved).
Slimming runs only at the HTTP-builder return, *after* internal consumers (e.g.
`mtc_v2_readiness`, AI-name/expert/scorecard row enrichment) have used the full data. Source
readers are unchanged; no on-disk data touched.

## 5. Tests added/updated
- `test_http_contract_is_read_only` (test_readonly_core.py): now asserts
  - `candidate_audit` **absent** from HTTP snapshot;
  - `scorecards.cards` **present**, `scorecards.by_strategy` **absent**;
  - every `candidate_pipeline.rows[].scorecard_v2_cases` is int or None, never a list.
- Reader/CLI tests unchanged and still green: `test_audit_reader.py` (build_candidate_audit),
  `test_ai_names_reader.py` / `test_expert_quantlens_reader.py` (scorecards.by_strategy from
  the *reader*, not the HTTP snapshot), `test_mtc_v2_reader.py`.
- Full suite: **Ran 69 tests … OK**.

## 6. Before/after payload size and latency
Measured via read-only stdlib HTTP GET (`/api/snapshot?refresh=1`); server restarted with
cleared bytecode between measurements.
| | Before (old code) | After (this patch) |
|---|--:|--:|
| Bytes | 121,172,209 | 46,808,919 |
| MB | 115.56 | **44.64** |
| Warm fetch | 5.93 s | 5.37 s |
| Top-level keys | 29 | 28 |
| `candidate_audit` present | True | **False** |
| `scorecards.by_strategy` present | True | **False** |
| `scorecards.cards` present | True | True |
| `scorecard_v2_cases` type | list | **int** (e.g. 11) |

Reduction: **−70.9 MB (−61%)**, below the ~75 MB target. (Actual exceeded the ~47 MB audit
estimate because the embedded scorecard payload was even heavier in live data.) Warm fetch
slightly faster; cold-build/transfer benefit scales with the smaller payload.

## 7. Removed / summarized fields
| Field | Action | Approx saved |
|---|---|--:|
| `scorecards.by_strategy` | removed from HTTP snapshot | ~31.6 MB |
| `candidate_audit` (top-level) | omitted from HTTP snapshot | ~8.4 MB |
| `candidate_pipeline.rows[].scorecard_v2_cases` | array → integer count | ~7.1 MB + audit's embedded copy |
All remain available via the underlying readers / CLI / source files.

## 8. UI compatibility check
- `node --check app.js` → **JS_OK**. No frontend edits.
- `app.js` reads `scorecard_v2_cases` as length-or-number ([app.js:400](08_DASHBOARD_APP/apps/web/app.js#L400)) → count is accepted.
- Home metrics read `scorecards.cards` + `candidate_pipeline.rows` (unchanged) and `gate2.score`/`gate_summary.statuses` (still inline) → intact.
- Strategy Intelligence reads `candidate_pipeline.rows[].scorecard_v2` + `cardsForStrategy()` (`scorecards.cards`) → intact (gate `sub_scores` still inline; lazy-load deferred).
- Result Explorer / Leaderboard read `night_artifacts.profile_results` + `scorecards.cards`; research-only badges read `provenance`/`profile_mapping`/`promotion_status`/`robustness` → untouched. Legacy quarantine unaffected.
- `scorecards.by_strategy` and `candidate_audit` confirmed never referenced in `apps/web`.

## 9. API / read-only validation
- `/healthz` → 200, `mode=read_only`.
- `/api/snapshot?refresh=1` → 200, 44.64 MB.
- `POST /api/snapshot` → **405**.
- Single server process after restart + `-KillStaleMccOnly` cleanup (`server_count=1`).

## 10. Safety confirmation
No data deleted/mutated; no scorecards or score semantics changed; safety/research-only/
universe-mismatch flags untouched (live on `scorecards.cards` + `night_artifacts`). No
backtest/optimization/artifact generation. No Pine / MTC_V2 / backtest engine / broker / live
/ paper execution touched. No write API added (POST→405). Gate `sub_scores` lazy-load NOT
implemented (deferred per scope). Temp measurement scripts (C:\tmp) removed; never git-tracked.

## 11. Remaining limitations
- Per-card gate `sub_scores` (~26 MB) still ship inline for all cards; the remaining bulk.
  Deferred medium-risk M1 (per-strategy lazy endpoint) is the next lever.
- `expert_quantlens` still appears both top-level and embedded per card (<1 MB); not pursued.
- gzip (audit L4) not enabled here; would further cut on-wire bytes (transport-only).

## 12. Recommended next phase
- Implement M1: move `gate1/1B/2/3.sub_scores` (and verbose `notes`) out of the default
  snapshot, keep `score` + `gate_summary.statuses` inline, serve full detail via a read-only
  per-strategy GET endpoint with fetch-on-open in Strategy Intelligence (~26 MB more).
- Optionally enable gzip on the response for transport latency.
