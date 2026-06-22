# MTC Dashboard Data Availability Audit - 2026-06-15

Scope: read-only audit for the Strategy Intelligence Command Center dashboard. This report maps which dashboard fields can be populated from current repo data and which fields must remain explicit missing-artifact placeholders.

## 1. Executive Summary

Current dashboard data is strong for read-only operational status, pipeline/catalog rows, scorecard_v2 evidence, AI display names, Codex/Claude QuantLens expert verdicts, Gemini pre-screen/intake metadata, task/report manifests, health diagnostics, and legacy backtest run summaries.

Current snapshot evidence:

| Area | Available now |
|---|---:|
| candidate_pipeline rows | 176 |
| candidate_audit rows | 176 |
| scorecard_v2 cards | 837 |
| scorecard_v2 runs | 19 |
| distinct scorecard strategies | 46 |
| strategy_registry candidates | 14 |
| QuantLens candidates | 31 |
| AI strategy names | 212 |
| expert QuantLens verdicts | 212 |
| backtest_status runs exposed | 80 |
| report_manifest reports | 13 |
| strategy research strategies/components/indicators | 63 / 78 / 27 |

Main missing pieces:

| Missing capability | Current state |
|---|---|
| durable run plan | no `run_plan.json` found |
| progress/heartbeat contract artifact | no exact `progress.json` or `heartbeat.json`; `overnight_heartbeat` reader reports `overnight_runs dir not found` from its configured path |
| canonical artifact inventory | no `artifact_index.json` found |
| profile-separated result model | no `backtest_profile_result.json`; scorecards do not carry reliable `profile` |
| leaderboard delta/benchmark package | no `leaderboard_delta.json`, `top_results.json`, or `benchmark_update_candidate.json` found |
| chart-ready equity/drawdown/trade artifacts | not in the read model; only some promoted pipeline rows can have a small `equity_curve` preview |
| report content for backtest artifact reports | backtest reader exposes artifact paths, but `/api/report` reads only manifest entries under `04_REPORTS` |

Dashboard-safe conclusion: render current scorecards, pipeline, registry, status, diagnostics, AI verdicts, and report manifest as real data. Render Backtest Planner, profile buckets, leaderboard categories, charts, benchmark-vs-challenger, artifact index, and run-plan/progress details as explicit missing-artifact/read-only placeholders.

## 2. Existing Read Models / API Endpoints

| Endpoint / reader | Source files read | Output shape | Dashboard pages that can consume it | Limitations |
|---|---|---|---|---|
| `/healthz` via `build_health_report()` | `00_CONFIG/paths.*.json`, read model files, schemas, lock dirs | `{schema_version, service, mode, overall_ok, checks, path_checks, read_model_summary}` | Home, Diagnostics | Confirms health and read-only mode; not a data inventory for profile/result artifacts. Current direct health build returned `overall_ok=True`, `mode=read_only`. |
| `/api/read-model` via `build_read_model()` | `03_STATUS/*.json`, `02_TASKS/*.json`, `05_REGISTRY/STRATEGY_REGISTRY.json`, `00_CONFIG/*`, `06_SCHEMAS/*` | `{schema_version, mode, summary, files}` with per-file JSON/schema diagnostics | Diagnostics, Read Model / Data Model | File-level status only; does not enrich pipeline, scorecards, AI names, or QuantLens. |
| `/api/snapshot` via `build_dashboard_snapshot_cached()` | all read-model files plus mcc_readonly domain readers | enriched top-level payload: `candidate_pipeline`, `candidate_audit`, `scorecards`, `strategy_registry`, `strategy_research`, `quantlens`, `backtest_status`, `liveops_status`, `parity_status`, `mtc_v2_readiness`, `report_manifest`, diagnostics | All current dashboard pages | No `run_plans`, `artifact_index`, `profile_results`, `leaderboard_snapshot`, or chart/trade-list model. Cache is 30s unless `?refresh=1`. |
| `/api/snapshot?refresh=1` | same as `/api/snapshot` | same payload with cache status `REFRESH` | All pages during manual refresh | Rebuilds snapshot only; does not create missing artifacts. |
| `/api/report?path=...` | `03_STATUS/REPORT_MANIFEST.json`; files under `04_REPORTS` only | `{report, path, content_type, size_bytes, content}` | Reports | Cannot read backtest artifact reports under `03_QUANTLENS/05_BACKTEST_RESULTS` unless those reports are also in manifest and under `04_REPORTS`. |
| `build_candidate_pipeline()` | candidate audit/registry/status/promotion/provenance files, read-only status readers, scorecard attachments | `{stages, summary, rows}` | Home, Strategy Pipeline, Strategy Intelligence, Paper Trading, MTC readiness | Good workflow rows, but stage labels can look more mature than scorecard evidence; scorecard/canonical fields are the safer authority for backtest status. |
| `build_candidate_audit()` | triage/source audit records and pipeline/registry merge | `{summary, rows, source_record_count}` | Home, Pipeline, Strategy Intelligence, Diagnostics | Has 176 rows and 2139 source records; many rows are source-parent/split/blocked states, not direct runnable strategies. |
| `build_scorecards()` | `03_QUANTLENS/05_BACKTEST_RESULTS/**/scorecard_v2/*.scorecard.json`, selected `03_STATUS/*/scorecard_v2` | `{count, source, runs, cards, by_strategy, diagnostics}` | Home, Strategy Intelligence, Result Explorer, Leaderboard, Pipeline | Strongest Gate 1/1B/2/3 evidence source, but legacy cards have no profile separation, no chart artifacts, and no explicit leaderboard bucket. |
| `build_canonical_display_row()` | pipeline row plus linked display scorecard | `{defined_tf, tested_tf, tf_mismatch, backtest_status, gate2_score, gate2_status, gate2_band, promotable, blocking, evidence_level}` | Strategy Intelligence, Pipeline, MTC readiness | Good safety layer for display, but only fields listed here are canonical; do not infer profile/sizing/chart readiness from it. |
| `build_strategy_registry()` | `03_QUANTLENS/_registry/*`, candidate folders, `06_PROMOTED_TO_PARITY/*/producer_spec.json` | `{candidates, strategies}` | Strategy Registry, Strategy Intelligence | Current snapshot has 14 candidates and 0 promoted strategy entries from this reader; source URL recovery is partial. |
| `build_strategy_research()` | `05_REGISTRY/*.json`, research workflow docs, triage data | `{overview, strategies, indicators, components, tags, triage_candidates, missing_metadata, workflow_docs}` | AI Knowledge Base, Strategy Taxonomy candidates | Excellent taxonomy/component inventory; not wired as per-strategy detail sections in the current Strategy Intelligence renderer. |
| `build_quantlens()` | `03_QUANTLENS/03_SALVAGE_IDEAS`, `03_QUANTLENS/strategies` | `{candidates, count, source}` | Strategy Intelligence legacy Gemini pre-screen/source material | Current count 31; not the same as Codex/Claude expert QuantLens verdict registry. |
| `build_ai_strategy_names()` | `05_REGISTRY/AI_STRATEGY_NAME_REGISTRY.json` | `{count, by_strategy_id, diagnostics}` and attached row/card fields | Pipeline, Registry, Strategy Intelligence, Result Explorer | Display-only metadata; does not prove strategy readiness. |
| `build_expert_quantlens()` | `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json` | `{count, by_strategy_id, diagnostics}` and attached row/card fields | Strategy Intelligence, AI Knowledge Base | Opinion labels only; never a numeric score. Scorecard remains scoring authority. |
| `build_backtest_status()` | `03_QUANTLENS/05_BACKTEST_RESULTS/*_results.json`, `*/MEGA_walk_forward_results.json`, `**/detached/run_status.json`, configured optimization metrics | `{summary, runs}` with limited artifact path discovery | Home, Backtest Runs, Result Explorer | Capped at 80 runs; large JSON may be skipped with `large_result_json_not_loaded`; artifact discovery is filename-based and partial. |
| `build_overnight_heartbeat()` | `03_QUANTLENS/tools/overnight_runs/_heartbeat*.json` from the API module's configured root | `{available, reason}` or latest heartbeat envelope | Backtest Runs, Home | Current snapshot: `available=False`, reason `overnight_runs dir not found`; exact `heartbeat.json` contract is not present. |
| `build_liveops_status()` | `03_STATUS/LIVEOPS_STATUS.json` | dry-run/liveops status, safety gates, paper plans, events | Paper Trading, Diagnostics | Dry-run status only. Current `paper_trade_plans=0`; no approval packages. |
| `build_mtc_v2_readiness()` | pipeline + audit + MTC_V2 parity tracker paths | `{summary, rows, parity_tracker}` | Paper Trading, MTC readiness/detail rail | Current configured `MTC_V2` root paths are absent in this clean checkout; all 151 rows blocked/parked/low-score. |
| `build_parity_status()` | configured parity results | `{summary, cases}` | Advanced Artifacts, Diagnostics | Source points to legacy path; useful as read-only parity status, not current strategy detail proof. |
| `build_optimization_status()` | configured `reports/optimization` | `{summary, runs, top_candidates, risk_notes}` | Backtest Planner/Explorer, Diagnostics | Current snapshot has 0 runs/top candidates/risk notes from this reader. |

## 3. Dashboard Page Data Map

### Command Center Home

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Total Strategies | `snapshot.candidate_pipeline.rows` | yes | none | `No pipeline data available.` | 176 rows. |
| Gate 1 Intake | pipeline row stage text / stages | partial | canonical Gate 1 aggregate | `Gate intake count unavailable.` | Current count is heuristic in UI. |
| Benchmark Candidates | sorted `snapshot.scorecards.cards` by `gate2.score` | partial | profile-safe leaderboard | `No benchmark rows available.` | Use as preview only, not official leaderboard. |
| Gate 2 Failed | `scorecards.cards[].gate_summary.statuses.gate2` | yes | none | `No scorecard rows available.` | Strong source if scorecard_v2 exists. |
| Pending/attention queue | `candidate_pipeline.rows[].next_action`, notes, canonical | partial | curated action queue | `No action queue data available.` | Text search can over/under-count. |
| Artifact Health | `snapshot.file_diagnostics` | yes | none | `No diagnostics data available.` | 13 file checks, all OK in this audit. |
| Backtest Activity | `snapshot.backtest_status.summary` | yes | profile/run-plan metadata | `No backtest run data available.` | 80 runs exposed, not full profile explorer. |

### Strategy Pipeline

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Strategy cards | `candidate_pipeline.rows` | yes | none | `No pipeline data available.` | 176 rows. |
| Gate strip | linked `scorecard_v2` or row stages | partial | scorecards for every strategy | `Gate evidence not linked yet.` | Prefer `row.canonical` and linked scorecard over stage text. |
| Horizon/category | row `horizon`, `timeframe`, `current_stage_label` | partial | normalized taxonomy mapping | `Not available.` | Current rows often lack dedicated horizon/category. |
| Method | row `method`, `evidence_level`, stage key | partial | canonical method field | `Method not available.` | Risk of showing workflow status as method. |
| Best Result Profile | `scorecard_v2.timeframe/run_name`; no true profile | partial | profile-separated result artifact | `Profile artifact missing.` | Do not call timeframe/run_name a profile. |

### Strategy Registry

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Catalog cards | `strategy_registry.candidates` | yes | none | `No registry entries available.` | 14 entries. |
| Source/title | candidate row `source_url`, `title`, recovered URL | partial | complete source metadata | `Source material not available.` | Source URL recovery from folders is best-effort. |
| Source type/market/horizon | registry row fields | partial | normalized source taxonomy | `Not available.` | Many fields may be blank. |
| Gate status/best result | linked scorecard if base id matches | partial | full scorecard coverage | `No linked scorecard yet.` | Registry and pipeline are distinct; not every registry row has scorecard evidence. |
| Reusable components | `candidate_kind` or research registry | partial | per-strategy component join | `Reusable components not mapped yet.` | Strategy research registry has component inventory but not always joined to registry card. |

### Strategy Intelligence

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Hero summary | pipeline row, AI name registry, description fields | partial | enriched strategy detail model | `Strategy summary not available.` | Name is strong; thesis may be missing. |
| Workflow bar | current UI hardcoded stage labels + gate state | partial | workflow/status contract | `Workflow state not available.` | Good display guide, not a backend workflow object. |
| Gate status summary | linked `scorecard_v2.gate_summary`, `row.canonical` | yes when scorecard linked | scorecard_v2 for no-scorecard rows | `Gate evidence not linked yet.` | Use scorecard as authority. |
| Right-side decision rail | `row.next_action`, scorecard promotable, expert verdict | partial | decision package/readiness artifact | `Decision package not available.` | Do not imply approval. |
| Strategy Overview | row description/timeframe/symbol fields | partial | deterministic spec/detail reader | `Overview fields not available.` | Some data exists in research registry but not joined here. |
| Core Rules Breakdown | not a dedicated current UI/read-model section | no/partial | strategy detail enriched read model from specs/producer_spec | `Core rule breakdown not available yet.` | Can be sourced later from `strategy_research.strategies` and producer specs. |
| Strategy Taxonomy | `strategy_research` inventories, row candidate kind | partial | per-strategy taxonomy join | `Taxonomy mapping not available yet.` | Inventory exists; detail join is incomplete. |
| Source Material | row source URL/transcript fields | partial | complete transcript/source reader | `Source material not available.` | Candidate audit says 166 source-material rows. |
| Gate 1 / Gate 1B | scorecard gate fields if linked | yes/partial | scorecards for all strategies | `Pre-backtest assessment not linked yet.` | Current UI text includes generic explanation. |
| AI Verdict & Reuse Notes | `expert_quantlens_verdict`, legacy `quantlens_verdict`, candidate kind | partial | full reuse notes model | `AI verdict not available.` | Expert QuantLens count 212. |
| Backtest Plan & Evidence | linked scorecard and static expected-artifact text | partial | `run_plan.json`, artifact index, profile results | `Backtest plan artifact missing.` | Do not claim plan exists from scorecard alone. |
| Backtest Result Explorer Preview | scorecards filtered by strategy | partial | profile-separated explorer model | `No result rows available for this strategy.` | Scorecard rows can render; charts/buckets cannot. |
| Paper Trading Readiness | scorecard gate3/promotable, liveops dry-run status | partial | paper approval package / Gate3 readiness package | `No paper trading readiness package available.` | Current liveops has 0 paper plans. |
| Advanced Technical Details | raw `{row, card}` JSON | yes | none | `Raw strategy payload not available.` | Safe for debugging; not a polished field model. |

### Backtest Planner

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Selected strategy | dashboard selection/default pipeline row | partial | durable plan selection | `No strategy selected.` | UI-only state. |
| Run intent | static text | no | `run_plan.json` | `Run plan artifact missing.` | No backend plan reader. |
| Timeframes/universe/risk/sizing | mostly placeholders | no | `run_plan.json`, profile result schema | `Pending / artifact missing.` | Must not infer from scorecard rows. |
| Smoke test/approval package | static placeholders | no | approval/run package | `Approval package not available.` | Read-only only. |
| Expected artifact list | static `NIGHT_CONTRACT` | partial | artifact schemas/readers | `Pending / repo implementation required.` | Contract display exists; ingestion does not. |

### Backtest Runs

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Run table | `backtest_status.runs` | yes | profile and full artifact index | `No backtest runs available.` | 80 exposed, capped. |
| Status/symbol/timeframe | parsed run results/status files | partial | normalized run status schema | `Not available.` | Large JSON may skip details. |
| Report path | `run.artifacts.morning_report` or `report_path` | partial | content reader for backtest reports | `Report artifact not linked.` | Paths may exist but not readable through `/api/report`. |
| Heartbeat | `overnight_heartbeat` | no currently | heartbeat artifact path contract | `Heartbeat not available.` | Current reason: `overnight_runs dir not found`. |

### Backtest Result Explorer

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Result rows | `scorecards.cards` sorted by Gate 2 score | yes/partial | profile result artifact | `No result rows available.` | 837 scorecard rows available. |
| Profile buckets | static labels plus scorecard presence | no/partial | `backtest_profile_result.json` | `No profile-separated result available yet.` | Only SOURCE_NAKED can show legacy rows with warning. |
| Same-profile warning | static UI text | yes | none | n/a | Correct warning; keep visible. |
| Selected result detail | selected scorecard fields | partial | artifact index, benchmark package | `Artifact missing.` | Current code looks for `relative_path`, but scorecards expose `source_path`. |
| Benchmark/challenger | top scorecard row | partial | `leaderboard_delta.json` or benchmark package | `Benchmark comparison artifact missing.` | Do not show as official comparison. |
| Charts | none | no | equity/drawdown/trade artifacts | `Result chart preview unavailable until equity/trade artifacts are present in the read model.` | Current UI already uses this wording. |

### Strategy Leaderboard

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Top 20 table | scorecards sorted by `gate2.score` | partial | leaderboard snapshot with categories/profiles | `No leaderboard data available.` | Preview only. |
| Category cards | top scorecard rows by index | partial | bucketed leaderboard engine | `No leaderboard snapshot available yet.` | Current categories are not computed buckets. |
| Profile/net profit/drawdown | scorecard fields if present | mostly no | profile result artifact | `Not available.` | scorecard cards expose Gate data, not net profit/drawdown top-level. |

### Paper Trading

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Approval package count | scorecard `gate_summary.promotable` | partial | paper approval package | `No paper trading readiness packages available.` | Promotable flag is not live approval. |
| Gate3 checklist | scorecard gate3, liveops status | partial | production readiness package | `View Gate 3 Readiness Checklist unavailable.` | Current liveops dry-run has 0 paper plans. |
| Execution state | `liveops_status` | yes | none | `Execution remains disabled.` | Read-only dry-run mode. |

### AI Knowledge Base

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Reusable components | `strategy_research.strategies/components/indicators` | yes | none | `Knowledge records not available.` | 63 strategies, 78 components, 27 indicators. |
| Tags/taxonomy | `strategy_research.tags` | yes | none | `Tags not available.` | Useful for future per-strategy taxonomy join. |
| Research runs/variants | `strategy_research.research_runs`, `variants` | no currently | research run/variant logs | `No research variants logged yet.` | Current counts are 0. |

### Advanced Artifacts

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Night artifact contract | static `NIGHT_CONTRACT` list | partial | schemas/readers/writers for contract | `Pending / repo implementation required.` | Display-only contract view. |
| Artifact health | file diagnostics/status readers | partial | artifact index | `Artifact index not available.` | Use Diagnostics for current read-model health. |

### Diagnostics

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Data contract coverage | `snapshot.file_diagnostics` | yes | none | `No diagnostics data available.` | All required JSON/schema checks passed in this audit. |
| UI route coverage | static route list | yes | none | n/a | Route coverage is not data coverage. |
| Read-only API status | `/healthz` payload | yes | none | `API health unavailable.` | Direct build returned `overall_ok=True`. |

### Reports

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Report list | `report_manifest.reports` | yes | none | `No reports available.` | 13 reports. |
| Report content viewer | `/api/report?path=` | yes for manifest paths under `04_REPORTS` | backtest report manifest/content bridge | `Unable to load report.` | Does not read arbitrary QuantLens morning reports. |

### Read Model / Data Model

| UI field/section | Available data source | Available now? | Missing artifact if any | Recommended empty-state wording | Notes |
|---|---|---|---|---|---|
| Snapshot keys | `Object.keys(snapshot)` | yes | none | `No snapshot loaded.` | Current keys include `candidate_pipeline`, `scorecards`, `strategy_research`, `expert_quantlens`, etc. |
| Page feed table | static `PAGE_FEEDS` | partial | audited field-level feed map | `Feed map unavailable.` | This report can become the source for a backend field map later. |

## 4. Strategy Intelligence Field Availability

| Section | Field | Source artifact/read-model | Exact existing key if known | Fallback if missing | Safe to render now |
|---|---|---|---|---|---|
| Hero summary | display name | AI names registry attached to rows/cards | `row.strategy_display_name`, `card.strategy_display_name` | `row.name`, `row.title`, `humanizeStrategyId(id)` | yes |
| Hero summary | description/thesis | candidate pipeline/audit row | `row.strategy_description_en`, `row.description.what`, `row.description.summary`, `row.summary` | `Not available` | partial |
| Hero summary | technical id | route/default strategy id | selected `id` | `No strategy selected` | yes |
| Workflow bar | stages | current UI static labels plus gate state | derived in `renderStrategyIntelligence()` | `Review` / `Read-only` / `Locked` | partial |
| Gate status summary | Gate 1 | linked scorecard | `card.gate_summary.statuses.gate1`, `card.gate1.status` | `Not available` | yes if scorecard linked |
| Gate status summary | Gate 1B | linked scorecard | `card.gate_summary.statuses.gate1B`, `card.gate1B.status` | `Not available` | yes if scorecard linked |
| Gate status summary | Gate 2 | linked scorecard/canonical | `card.gate_summary.statuses.gate2`, `row.canonical.gate2_status` | `Not available` | yes if scorecard linked |
| Gate status summary | Gate 3 | linked scorecard | `card.gate_summary.statuses.gate3`, `card.gate3.status` | `Locked` | yes if clearly non-approval |
| Right-side decision rail | next action | candidate pipeline/audit | `row.next_action`, `row.next_action_hint` | `Freeze rules / review artifacts` | partial |
| Right-side decision rail | decision | scorecard | `card.gate_summary.promotable` | `Locked` | partial; render as review state, not approval |
| Right-side decision rail | missing fields | candidate audit | `row.blocked_reason` | `Risk/rule artifacts pending` | partial |
| Right-side decision rail | AI knowledge value | expert verdict | `row.expert_quantlens_verdict.decision` | `Review needed` | yes |
| Strategy Overview | thesis | row description | `row.description`, `row.summary` | `Not available` | partial |
| Strategy Overview | market condition | row/research registry | `row.market_condition`, `strategy_research.strategies[].expected_market_regime` | `Not available` | partial |
| Strategy Overview | entry/exit/avoid | row description | `row.description.entry`, `.exit`, `.avoid` | `Not available` | partial |
| Strategy Overview | defined/tested timeframe | row + canonical | `row.timeframe`, `row.canonical.tested_tf` | `Not available` | partial |
| Core Rules Breakdown | entry logic | strategy research registry | `strategy_research.strategies[].entry_logic_summary` | `Core rule breakdown not available yet.` | partial only after join |
| Core Rules Breakdown | exit/SL/TP logic | strategy research registry | `exit_logic_summary`, `stop_loss_logic`, `take_profit_logic` | `Core rule breakdown not available yet.` | partial only after join |
| Strategy Taxonomy | category/method/tags | strategy research registry | `strategy_category`, `method`, `tags`, `reusable_components` | `Taxonomy mapping not available yet.` | partial only after join |
| Source Material | URL | registry/audit/pipeline row | `row.source_url`, `row.source` | `Not available` | partial |
| Source Material | transcript | audit/research row | `row.transcript_path`, `has_transcript` | `Transcript not available` | partial |
| Gate 1 / Gate 1B | score/status | scorecard | `card.gate1.score`, `card.gate1.status`, `card.gate1B.score`, `card.gate1B.status` | `Pre-backtest assessment not linked yet.` | yes if linked |
| Gate 1 / Gate 1B | sub-score details | scorecard gates | `card.gate1.sub_scores[]`, `card.gate1B.sub_scores[]`, `deduction_reason` | `Sub-score detail not available.` | yes if linked |
| AI Verdict & Reuse Notes | expert verdict | AI QuantLens verdict registry | `row.expert_quantlens_verdict.decision` | `Not available` | yes |
| AI Verdict & Reuse Notes | Gemini pre-screen | QuantLens/intake data if attached | `row.quantlens_verdict.decision` | `Not available` | partial |
| AI Verdict & Reuse Notes | reuse factor | registry/research row | `row.candidate_kind`, `reusable_components` | `Review needed` | partial |
| Backtest Plan & Evidence | Gate 2 evidence | scorecard | `card.gate2.status`, `card.gate2.score`, `card.gate2.sub_scores[]` | `Artifact missing` | yes if linked |
| Backtest Plan & Evidence | score method | scorecard | `scorecard_v2` | `Scorecard not linked` | yes |
| Backtest Plan & Evidence | expected artifacts | static contract | `NIGHT_CONTRACT` | `Pending / repo implementation required` | partial |
| Backtest Plan & Evidence | case count/parameter space | none | no `run_plan.json` | `Repo implementation required` | no |
| Backtest Plan & Evidence | sizing/profile | none | no `backtest_profile_result.json` | `Pending / artifact missing` | no |
| Backtest Result Explorer Preview | scoped rows | scorecards by base strategy id | `scorecards.cards[]` | `No result rows available for this strategy.` | partial |
| Paper Trading Readiness | status | scorecard/liveops | `gate3`, `gate_summary.promotable`, `liveops_status` | `Locked until Gate 2 evidence passes` | partial |
| Advanced Technical Details | raw payload | current row/card | `{row, card}` JSON | `Raw strategy payload not available.` | yes |

## 5. Backtest Result Explorer Data Gap Analysis

| Requirement | Available now | Missing | Likely artifact needed | Safe placeholder wording |
|---|---|---|---|---|
| profile/timeframe buckets | timeframe from scorecards yes; profile no | explicit profile labels and bucket metadata | `backtest_profile_result.json`, scorecard profile fields | `No profile-separated result available yet.` |
| `SOURCE_NAKED` | partial legacy scorecards can be treated only as unprofiled legacy rows | explicit source-faithful profile declaration | profile result artifact + run plan | `Legacy rows visible / profile field missing.` |
| `RISK_NORMALIZED` | no | risk model, stop distance, quantity/leverage assumptions | `backtest_profile_result.json` with sizing metadata | `RISK_NORMALIZED artifact missing.` |
| `MTC_LIGHT` | no for Result Explorer | MTC-light profile outputs tied to strategy/result | MTC-light result artifact and artifact index | `MTC_LIGHT artifact missing.` |
| `FULL_MTC_CANDIDATE` | no for Result Explorer | production/paper readiness package and Gate3 evidence | production readiness + profile result artifact | `FULL_MTC_CANDIDATE artifact missing.` |
| top 5 per bucket | partial global top scorecards only | bucketed ranking by profile/timeframe/category | `top_results.json` or `leaderboard_snapshot.json` | `No bucketed top results available.` |
| benchmark vs challenger | partial top scorecard preview | same-profile benchmark package and deltas | `leaderboard_delta.json`, `benchmark_update_candidate.json` | `Benchmark comparison artifact missing.` |
| KPI deltas | no | paired baseline/challenger metrics | leaderboard delta artifact | `KPI delta artifact missing.` |
| equity curve chart | partial pipeline preview for promoted trade CSV only; not explorer-ready | chart-ready equity series per result | `backtest_profile_result.json` or chart artifact path in `artifact_index.json` | `Equity curve unavailable until chart artifacts are present.` |
| drawdown chart | no | drawdown series | chart artifact path / profile result | `Drawdown chart unavailable until chart artifacts are present.` |
| trade list | no | normalized trade rows or trade CSV path in read model | `artifact_index.json` + trade list reader | `Trade list artifact missing.` |
| artifact availability | partial filename discovery in `backtest_reader` | canonical per-run artifact inventory | `artifact_index.json` | `Artifact index not available.` |

## 6. Night Artifact Contract Gap

| Artifact | Found? | Found path(s) | Schema exists? | Currently read by API? | Recommended dashboard state |
|---|---|---|---|---|---|
| `run_plan.json` | no | none found under `MTC_COMMAND_CENTER` | no | no | Show `Run plan artifact missing`; keep planner read-only. |
| `run_status.json` | yes, legacy only | `03_QUANTLENS/05_BACKTEST_RESULTS/overnight_research_20260501/detached/run_status.json`; `03_QUANTLENS/05_BACKTEST_RESULTS/overnight_research_20260501/smoke/detached/run_status.json`; `01_MTC_PROJECT/reports/optimization/detached_resume_smoke/run/run_status.json` | no dedicated `run_status.schema.json` | partial: `backtest_reader` scans `**/detached/run_status.json`, but current top-80 snapshot reported `detached_status_runs=0` | Show only if surfaced by API; otherwise `No active run status artifact.` |
| `progress.json` | no | none found | no | no | Show `Progress artifact missing.` |
| `heartbeat.json` | no exact file | none found as exact `heartbeat.json`; heartbeat reader looks for `_heartbeat*.json` | no | partial reader exists for `_heartbeat*.json`; current unavailable | Show `Heartbeat not available.` |
| `artifact_index.json` | no | none found | no | no | Show `Artifact index not available.` |
| `summary.json` | yes, legacy MTC/backtest outputs | 29 files, mostly under `02_MTC_BACKTEST/results/.../summary.json` | no | no direct dashboard night-contract reader | Do not use for new night contract; show `Legacy summary exists; not wired to dashboard contract.` |
| `backtest_profile_result.json` | no | none found | no | no | Show `No profile-separated result available yet.` |
| `top_results.json` | no | none found | no | no | Show `No bucketed top results available.` |
| `leaderboard_delta.json` | no | none found | no | no | Show `Leaderboard delta artifact missing.` |
| `benchmark_update_candidate.json` | no | none found | no | no | Show `Benchmark update candidate artifact missing.` |
| `morning_report.md` | yes | `03_QUANTLENS/05_BACKTEST_RESULTS/MORNING_REPORT.md`; `03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/MORNING_REPORT.md`; `03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/MORNING_REPORT.md`; plus uppercase/prefixed `*MORNING_REPORT*.md` files discovered by run artifact scanning | no | partial: `backtest_reader` exposes paths, `/api/report` does not read these unless manifest/04_REPORTS | Show link/path as artifact only; content viewer unavailable until report content reader or manifest bridge exists. |

## 7. Data Quality / Mapping Risks

| Risk | Evidence / current behavior | Dashboard handling |
|---|---|---|
| Method incorrectly showing `classified` or `backtested` | Pipeline cards fall back from `row.method` to `row.evidence_level` or `row.current_stage_key`; candidate audit summary has stage counts `classified=165`, `backtested=11`. | Label fallback as workflow status, not method; prefer research registry `method` when joined. |
| Missing source metadata | Registry/audit rows have source URL/transcript fields but coverage is partial; candidate audit shows 166 source-material rows out of 176. | Use `Source material not available` rather than hiding the field. |
| Missing profile labels | Scorecards expose `run_name`, `symbol`, `timeframe`, but no reliable `profile`. | Never compare as official profile buckets; show `Profile missing`. |
| Legacy scorecard rows without profile separation | 837 scorecards are scorecard_v2 evidence, but they predate the profile-result contract. | Treat them as legacy scorecard rows; use same-profile warning. |
| Hardcoded or misleading fields | Current UI has static profile labels and planner artifact list; these are not backed by readers. | Keep explicit `Pending / repo implementation required` wording. |
| Ambiguous gate status mapping | Pipeline stage and scorecard gate status can disagree. | Prefer linked `scorecard_v2` and `row.canonical` for backtest/gate status. |
| Duplicated leaderboard rows | Scorecards include multiple runs per base strategy; `by_strategy.display_card` exists, but leaderboard currently sorts cards directly. | Official leaderboard should dedupe by strategy/profile/timeframe/run criteria. |
| Unknown timeframe/symbol values | Backtest reader compresses many symbols/timeframes as `17 values` / `5 values` for matrix runs; large JSON can be skipped. | Show aggregate labels as aggregate labels, not precise per-result fields. |
| Report path without content reader | Backtest artifacts expose report paths outside `04_REPORTS`; `/api/report` forbids non-manifest/non-04_REPORTS paths. | Display artifact path, not clickable content, until a backtest report reader is added. |
| Artifact availability mismatch | `renderBacktestResultExplorer()` checks `selected.relative_path`, while normalized scorecards expose `source_path`. | Future backend/read-model should expose a stable `artifact_availability` object; UI should avoid implying missing if `source_path` exists. |
| Current heartbeat path mismatch | Reader reports `overnight_runs dir not found`, while historical overnight logs may exist under tool folders. | Show unavailable until the heartbeat reader path and contract are standardized. |
| MTC_V2 readiness path drift | Current `mtc_v2_readiness` says configured clean-checkout `MTC_V2` pine/parity paths do not exist. | Treat MTC readiness as blocked/read-only, not production ready. |

## 8. Recommended Next Backend-Only Read-Model Patch

Do not implement in this task. Smallest future backend/read-model additions:

1. Add a read-only `run_plan_reader.py` that discovers approved `run_plan.json` artifacts and emits selected/excluded strategies, symbols, timeframes, profile, sizing/leverage assumptions, estimated cells/runtime, output dir, smoke command, and approval state.
2. Add an `artifact_index_reader.py` that reads `artifact_index.json` and normalizes presence/paths for morning report, scorecards, CPCV/PBO, alpha summary, equity curve, drawdown, trade list, and charts.
3. Add `backtest_profile_result_reader.py` for `SOURCE_NAKED`, `RISK_NORMALIZED`, `MTC_LIGHT`, and `FULL_MTC_CANDIDATE`; require same-profile grouping keys: strategy, symbol, timeframe, market universe, profile, score method.
4. Add a lightweight `leaderboard_reader.py` that builds deduped top-N buckets from profile results, not raw scorecards.
5. Add a backtest report content reader or extend `/api/report` safely for allowlisted QuantLens report artifacts outside `04_REPORTS`.
6. Add a `strategy_detail_enriched` read model that joins pipeline/candidate audit rows with strategy research registry fields: method, category, tags, entry/exit summaries, SL/TP logic, reusable components, known weaknesses, and source metadata.
7. Normalize scorecard cards with stable artifact fields: `source_path`, `artifact_availability`, `profile`, `result_key`, and `display_rank_key`.
8. Standardize heartbeat/progress discovery under the same run contract used by the planner and artifact index.

## 9. Validation Commands Run

| Command | Result |
|---|---|
| `python _deepseek_driver\ds_agent.py --task C:\tmp\dashboard_data_availability_audit_task.json` | First run failed before repo write: JSON BOM decode error. Second run used UTF-8 no BOM; cheap-agent explored but hit `max_iters` without `finish()`. No target report was created by the harness. |
| `git status --short` | Worktree already had unrelated modified dashboard UI/API test and `_AI_MEMORY` files before this report. Those were treated as off-limits. |
| `rg --files MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests MTC_COMMAND_CENTER\05_REGISTRY MTC_COMMAND_CENTER\06_SCHEMAS` | Listed current readers, tests, registries, and schemas used for this audit. |
| `rg -n "@app\.(get|route)|def .*snapshot|def .*read|class |def build_|healthz|/api/snapshot|/api/read-model" MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api -g "*.py"` | Confirmed endpoint and reader functions/classes. |
| `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover tests` from `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api` | PASS: 39 tests in 61.094s. |
| Python snapshot inspection importing `build_dashboard_snapshot`, `build_read_model`, `build_health_report` | PASS: snapshot/read-model built; health `overall_ok=True`, `mode=read_only`; counts recorded above. |
| Python artifact scan for exact target names under `MTC_COMMAND_CENTER` | PASS: found no `run_plan.json`, `progress.json`, `heartbeat.json`, `artifact_index.json`, `backtest_profile_result.json`, `top_results.json`, `leaderboard_delta.json`, or `benchmark_update_candidate.json`; found 3 legacy `run_status.json`, 29 `summary.json`, and 3 exact lowercase `morning_report.md`. |
| `rg -n "SOURCE_NAKED|RISK_NORMALIZED|MTC_LIGHT|FULL_MTC_CANDIDATE|artifact_index|run_plan|backtest_profile_result|morning_report" ...` | PASS: labels and gap worklist appear in UI/reference/audit docs; no implemented backend readers for run plan/profile result/artifact index. |

## 10. Strict No-Code-Change Confirmation

- No dashboard UI files were modified by this task.
- No API files were modified by this task.
- No `_AI_MEMORY` files were modified by this task.
- No Pine, MTC_V2, parity, backtest engine, broker, live execution, or paper execution files were modified by this task.
- The only intended repo write from this task is this new report file:
  `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_DATA_AVAILABILITY_AUDIT_2026-06-15.md`
