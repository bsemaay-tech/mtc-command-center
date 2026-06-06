# MCC Readiness Report

**Date:** 2026-06-06  
**Prepared by:** Claude Sonnet 4.6  
**Scope:** Summary of all parallel agent work completed in the 2026-06-06 sprint.

---

## Sprint Summary

All 7 parallel agent streams (S1–S7) are complete and audited. 35 API tests pass. Dashboard JS syntax clean.

---

## Completed Work — By Stream

### S1 — Strategy Metadata Extractor (DeepSeek A1)
- **extractor:** `03_QUANTLENS/tools/extract_strategy_metadata.py` (new)
- **registry patch:** `03_QUANTLENS/tools/build_strategy_research_registry.py` patched — `trailing_logic` and `filters_used` now read from YAML instead of hardcoded `review_needed`
- **Result:** 28/63 strategies have real metadata. 35 blocked (no `07_deterministic_spec.md`).
- **Post-audit fix by Claude:** 11 broken YAML files in STG048–STG060 repaired (9 pre-existing `New:` colon issues, 2 S1 extractor `""` escaping bugs). Registry regenerated.

### S2 — Dashboard UI Components (Codex A5/A6/A7/D4)
- **A5:** Gate 2 evidence card grid in strategy detail (`renderGate2EvidenceBlock`)
- **A6:** Promotability panel with blocking gate list (`renderPromotabilityPanel`)
- **A7:** Pipeline gate filter (`#pipelineGateFilter` — gate2_pass, promotable_only, gate3_incomplete, blocked_gate3)
- **D4:** Night-run detail panel in Backtest tab, clickable rows, artifact links (`renderNightRunDetail`)

### S3 — Backend Fixes (Antigravity C4/D2/5 tests)
- `scorecard_reader.py`: scans `03_STATUS/` in addition to `05_BACKTEST_RESULTS/` — promotable strategy now visible
- `backtest_reader.py`: `_find_run_artifacts()` — 79/80 runs surface artifact paths
- 5 failing tests fixed (stale paths, stale nav labels, missing TV CSV skip)

### S4 — Heartbeat Reader + Forward Paper Queue (B4/D3a)
- `heartbeat_reader.py` (new): reads `_heartbeat*.json` from `overnight_runs/`, returns alive/stale/offline state
- `read_model.py`: `overnight_heartbeat` key added to snapshot
- `build_forward_paper_queue.py` (new): scans scorecard_v2, criteria Gate2=PASS + CPCV≥0.70 + net>0 → 0 candidates currently

### S5 — Global Acceptance Panel (Codex A8)
- `#mccStatusPanel`: shows promotable count, total scored, per-strategy rows
- Reads from `snapshot.scorecards.cards`

### S6 — Worker Monitor (Codex D3b)
- `#overnightRunnerStatus`: embedded in Backtest tab, ONLINE/STALE/OFFLINE states
- Functions: `renderOvernightRunnerStatus`, `renderWorkerMonitorRow`, `formatHeartbeatTimestamp`

### S7 — Missing Metadata Tab (A4)
- Inside `renderResearchLab()` — reads from `strategy_research.strategies`
- Shows: coverage bars, per-strategy missing-field table, count badge
- Post-incident: S7 reverted app.js to HEAD (wiped S2/S5/S6 JS). Claude recovered all functions manually.

---

## Current System State

### Strategy Research Registry
| Field | Filled | N_A | review_needed |
|---|---|---|---|
| trailing_logic | 4 | 24 | 35 |
| filters_used | 20 | 8 | 35 |
| known_strengths | 28 | 0 | 35 |
| known_weaknesses | 19 | 11 | 33 |

35 strategies have no `07_deterministic_spec.md` — they cannot be auto-extracted until spec files are written.

### Scorecard v2
| Metric | Count |
|---|---|
| Total scorecards | 349 |
| Promotable | **1** — `QL_FAM_MOMENTUM_CONTINUATION\|TRXUSDT\|4h` |
| Gate3 status | INCOMPLETE (97.0/100, blockers remain) |

**Promotable ≠ live trading approval.** Scorecard status only.

### Dashboard API
- `node --check app.js` → **PASS**
- `pytest` → **35 passed, 1 subtests passed**
- Endpoints: `/api/snapshot`, `/healthz`, `/api/report`

---

## What Is Blocked / Not Done

| Item | Reason | Owner |
|---|---|---|
| B3 — Confirmation grid pre-registration | Requires Barış threshold/pattern definitions | Barış |
| E1/E2 — Pine Builder + parity plan | Scope approval required | Barış |
| MORNING-003 — 31 transcript review | Manual human review | Barış |
| Gate3 PASS for promotable strategy | 5 lifecycle tests failing (reverse/reentry/cooldown/EOD) | Claude (after Barış unblocks) |
| 35 strategies without spec files | No `07_deterministic_spec.md` exists yet | Barış (intake) or research sprint |
| Git commit | Barış commits; Claude does not push | **Barış** |

---

## Files Changed (This Sprint — Uncommitted)

### New files
- `03_QUANTLENS/tools/extract_strategy_metadata.py`
- `03_QUANTLENS/tools/build_forward_paper_queue.py`
- `08_DASHBOARD_APP/apps/api/mcc_readonly/heartbeat_reader.py`

### Modified files
- `08_DASHBOARD_APP/apps/web/app.js` — S2/S5/S6/S7 features
- `08_DASHBOARD_APP/apps/web/index.html` — mount points
- `08_DASHBOARD_APP/apps/web/styles.css` — CSS for all new components
- `08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py` — 03_STATUS scan
- `08_DASHBOARD_APP/apps/api/mcc_readonly/backtest_reader.py` — artifact discovery
- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` — overnight_heartbeat key
- `03_QUANTLENS/tools/build_strategy_research_registry.py` — trailing_logic/filters_used patch
- 11× `03_QUANTLENS/strategies/STGxxx/01_candidate_metadata.yaml` — YAML fixes
- 28× `03_QUANTLENS/strategies/STG035-045/01_candidate_metadata.yaml` — A1 extracted metadata
- `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` — regenerated (63 entries)
- `AGENTS.md` — parallel agent safety rule added
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/` — 5 test fixes

### Reverted by Claude (S1 violations)
- `03_QUANTLENS/tools/overnight_v2_runner.py` — ADX signal inversion reverted
- `03_QUANTLENS/tools/rigorous_walk_forward.py` — short-side code reverted
- `03_QUANTLENS/tools/rigorous_walk_forward_parallel.py` — 73-line change reverted

---

## Immediate Next Step for Barış

1. **Review + commit** the changes above (see files list). Suggested commit order:
   - Backend changes (scorecard_reader, backtest_reader, read_model, heartbeat_reader)
   - New tools (extract_strategy_metadata, build_forward_paper_queue)
   - Strategy YAML files + registry
   - Frontend (app.js, index.html, styles.css)
   - AGENTS.md
2. **Pre-register B3 thresholds** if continuing STG057/054/047 coding
3. **Choose next research sprint:** 35 strategies without spec files are the metadata ceiling
