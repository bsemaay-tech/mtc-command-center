# ACTIVE_FILES

## 2026-06-21 Claude Opus 4.8 Graphify piloted (KEEP on-demand)
- `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\pilots\graphify_pilot.md` (PASS; local/keyless code graph; impact analysis accurate)
- installed: `graphifyy` v0.8.44 via `uv tool install` (global uv tool, no repo footprint); NOT `graphify install` (skill reg deferred)
- `.gitignore` += `graphify-out/` + `**/graphify-out/` (graphs never committed)
- usage pattern: scoped copy → `graphify update <path> --no-cluster` → `affected/explain/query`

## 2026-06-21 Claude Opus 4.8 MarkItDown promoted to permanent (item 1)
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\markitdown_ingest.py` (COMMITTED wrapper: self-bootstrap venv + convert intake docs → .md; dry-run default, --apply/--out/--bootstrap)
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\.venvs\markitdown\` (git-IGNORED venv, Py3.13, markitdown 0.1.6) — rebuilt on fresh clone via --bootstrap
- `.gitignore` += `MTC_COMMAND_CENTER/03_QUANTLENS/tools/.venvs/`
- composes with (does NOT modify) `03_QUANTLENS\tools\route_user_intake.py`

## 2026-06-21 Claude Opus 4.8 Phase 3 pilots: MarkItDown + CodeBurn (both KEEP)
- `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\pilots\codeburn_pilot.md` (PASS; read-only cost observability; DeepSeek underuse finding)
- `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\pilots\markitdown_pilot.md` (PASS for XLSX/Office; PDF deferred — no PDFs in repo)
- installed: CodeBurn v0.9.12 global npm (no repo footprint); MarkItDown 0.1.6 now permanent (see block above; old `C:\tmp` venv removed)

## 2026-06-20 Claude Opus 4.8 AI tool integration backlog filed + prepped
- `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md` (source backlog; moved from root `docs\`, banner added)
- `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md` (real-path map, phase gates, per-tool acceptance, §6 checklist, next command)
- `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\CLAUDE_REVIEW_OF_CODEX_BACKLOG.md` (Claude critique of Codex plan)
- updated: `_AI_MEMORY\NEXT_STEPS.md`, `_AI_MEMORY\GLOBAL_HANDOFF.md`, `_AI_MEMORY\SESSION_LOG.md`, root `docs\ACTIVE_FILES.md`
- key prep facts: model routing already exists (`_deepseek_driver\ds_agent.py`); review prompts already exist (`04_SHARED\prompts\05_ai_workflow\`); NOTHING installed — approval-gated per tool

## 2026-06-16 Claude Opus 4.8 snapshot gate-detail lazy-load (M1) active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\read_model.py` (_slim_gate/_slim_card/_slim_scorecard_cases; _FULL_SCORECARDS_CACHE; build_scorecard_detail)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\server.py` (GET /api/scorecard-detail, param-validated, POST→405)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js` (state.detailCards, loadStrategyDetail/detailBestCard, fetch-on-open, subscoreList loading states, advancedSection detail)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_readonly_core.py` (slim + detail endpoint asserts)
- `MTC_COMMAND_CENTER\11_TRIAGE\SNAPSHOT_GATE_DETAIL_LAZY_LOAD_PATCH_REPORT_2026-06-16.md`
- result: 44.64MB→4.45MB (orig 115.56→−96%); endpoint `GET /api/scorecard-detail?strategy_id=`

## 2026-06-16 Claude Opus 4.8 snapshot payload slim (low-risk L1+L2+L3) active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\read_model.py` (_slim_http_snapshot: drop by_strategy, omit candidate_audit, scorecard_v2_cases→count)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_readonly_core.py` (slim contract asserts)
- `MTC_COMMAND_CENTER\11_TRIAGE\SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md`
- `MTC_COMMAND_CENTER\11_TRIAGE\SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md` (audit basis)
- result: 115.56MB→44.64MB; OPEN M1 = gate sub_scores per-strategy lazy endpoint (~26MB)

## 2026-06-16 Claude Opus 4.8 launcher single-instance follow-up active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\run_dashboard_server.ps1` (-StatusOnly non-mutating: moved before Limit-LogSize, Write-Output not Write-Launcher)
- Startup VBS (verified, NOT modified): `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MTC_Command_Center_Dashboard.vbs` → guarded launcher; sole auto-start, no duplicates
- `MTC_COMMAND_CENTER\11_TRIAGE\DASHBOARD_LAUNCHER_SINGLE_INSTANCE_FOLLOWUP_REPORT_2026-06-15.md`
- OPEN perf task (NEXT_STEPS 13): `/api/snapshot` ~121 MB / ~60 s

## 2026-06-16 Claude Opus 4.8 dashboard launcher single-instance guard active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\run_dashboard_server.ps1` (single-instance guard + flags + bounded logs)
- `MTC_COMMAND_CENTER\11_TRIAGE\DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md`

## 2026-06-16 Claude Opus 4.8 profile-result research-only UI hardening active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js` (profileRowFlags/Badges/researchOnlyBanner; Result Explorer/SI/Leaderboard/Advanced Artifacts)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html` (cache v9)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\night_artifacts_reader.py` (provenance + profile_mapping passthrough)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_build_profile_result_artifact.py` (+badge-data passthrough test)
- `MTC_COMMAND_CENTER\11_TRIAGE\PROFILE_RESULT_RESEARCH_ONLY_UI_HARDENING_REPORT_2026-06-15.md`

## 2026-06-16 Claude Opus 4.8 first profile-separated result artifact pilot active set
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_profile_result_artifact.py` (read-only converter, real soak → backtest_profile_result.json)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\pilot_profile_result_QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-16\backtest_profile_result.json`
- source: `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\MEGA_results_iter_1_20260601_054633_results.json`
- `MTC_COMMAND_CENTER\11_TRIAGE\FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md`

## 2026-06-15 Claude Opus 4.8 Home canonical universe + invariant hardening active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js` (canonicalStrategyIds/orphanScorecardIds/strategyMetrics; Needs Review rename; metric() title)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html` (cache v8)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css` (.metric-group/.metric-note)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_home_metric_invariants.py`
- `MTC_COMMAND_CENTER\11_TRIAGE\HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md`
- `MTC_COMMAND_CENTER\11_TRIAGE\HOME_METRIC_AGGREGATION_PATCH_REPORT_2026-06-15.md`
- `MTC_COMMAND_CENTER\11_TRIAGE\NEXT_CODEX_AUDIT_PROMPT_HOME_CANONICAL_UNIVERSE_2026-06-15.md`

## 2026-06-15 Claude Opus 4.8 first run_plan.json artifact flow active set
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_run_plan.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_build_run_plan.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15\` (run_plan.json, artifact_index.json, run_plan.md)

## 2026-06-15 Claude Opus 4.8 night-artifact contract + reader integration active set
- `MTC_COMMAND_CENTER\06_SCHEMAS\run_plan.schema.json`
- `MTC_COMMAND_CENTER\06_SCHEMAS\run_status.schema.json`
- `MTC_COMMAND_CENTER\06_SCHEMAS\backtest_profile_result.schema.json`
- `MTC_COMMAND_CENTER\06_SCHEMAS\artifact_index.schema.json`
- `MTC_COMMAND_CENTER\06_SCHEMAS\top_results.schema.json`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\night_artifacts_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\read_model.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_night_artifacts_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\11_TRIAGE\BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15.md`

## 2026-06-06 Codex GPT-5 S6 D3b worker monitor active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S6_D3B_WORKER_MONITOR_REPORT.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-14 Codex GPT-5 Google Strategy Intelligence final cleanup active set

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\11_TRIAGE\ui_references\google_strategy_intelligence_v2_final\`
- `C:\Users\BarışSemaay\.codex\attachments\c62ab0bb-e553-4b3f-9848-57528d4a2af4\pasted-text.txt`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-06 Codex GPT-5 S5 A8 dashboard active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S5_CODEX_A8_REPORT.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-06 Codex GPT-5 S2 dashboard UI active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S2_CODEX_UI_REPORT.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-06 Codex GPT-5 MEV producer parity active set
- `MTC_COMMAND_CENTER\01_MTC_PROJECT\parity_oracles\feature_adapters\pinets\producer_ql_fam_momentum_continuation_v1.pine`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\tools\parity\run_quantlens_producer_parity.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\results\producer_parity\ql_fam_momentum_continuation_trx_4h_2026-06-06_bridge\`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\results\mtc_engine_validation_runs\ql_fam_momentum_continuation_trx_4h_parity_csv_2026-06-06\`
- `MTC_COMMAND_CENTER\03_STATUS\producer_parity_2026-06-06\`
- `MTC_COMMAND_CENTER\03_STATUS\producer_parity_2026-06-06\reverse_reentry_cooldown_mapping.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-06 Codex GPT-5 MEV QuantLens producer active set
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\src\modules\signals\producers\quantlens_momentum_continuation_producer.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\src\modules\signals\producers\__init__.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\tests\test_producer_adapter.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\configs\producer_params\ql_fam_momentum_continuation_trx_4h.json`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\data\mev_validation\TRXUSDT_4h_20240101_RESEARCH.csv`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\results\mtc_engine_validation_runs\ql_fam_momentum_continuation_trx_4h_2026-06-06\`
- `MTC_COMMAND_CENTER\03_STATUS\mtc_engine_validation_2026-06-06\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-06 Codex GPT-5 C3 dry-run + A3 closure active set
- `MTC_COMMAND_CENTER\07_ADAPTERS\liveops\dry_run_adapter.py`
- `MTC_COMMAND_CENTER\07_ADAPTERS\liveops\tests\test_dry_run_adapter.py`
- `MTC_COMMAND_CENTER\07_ADAPTERS\liveops\README.md`
- `MTC_COMMAND_CENTER\03_STATUS\LIVEOPS_STATUS.json`
- `MTC_COMMAND_CENTER\03_STATUS\dry_run_evidence_2026-06-06\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\A3_GAP_MATRIX.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\DEEPSEEK_DISPATCH.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-05 Codex GPT-5 SP-005 Wave C scorecard_v2 active set
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\scorecard_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\read_model.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\enriched_metrics_2026-06-05\scorecard_v2\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-05 Codex GPT-5 Hermes memory import package active set
- `_HERMES_MEMORY_IMPORT/01_PROPOSED_HERMES_MEMORY/USER.md`
- `_HERMES_MEMORY_IMPORT/01_PROPOSED_HERMES_MEMORY/MEMORY.md`
- `_HERMES_MEMORY_IMPORT/02_PROJECT_CONTEXT/MTC_COMMAND_CENTER_CONTEXT.md`
- `_HERMES_MEMORY_IMPORT/README.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md`

## 2026-06-04 Codex GPT-5 confirmation run active set

- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\confirmation_runner_2026-06-04.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\run_confirmation_2026-06-04.sh`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\start_confirmation_2026-06-04_keepawake.ps1`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\run_confirmation_validation_tail_2026-06-04.ps1`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\confirm_morning_watchdog_2026-06-04.ps1`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\write_overnight_morning_report.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\night_runs\confirm_2026-06-04\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\overnight_runs\_heartbeat_confirm_morning_watchdog.json`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\confirm_2026-06-04\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-04 Codex GPT-5 YT transcript collector active set

- `YT_TRANSCRIPT_COLLECTOR\collect_transcripts.py`
- `YT_TRANSCRIPT_COLLECTOR\requirements.txt`
- `YT_TRANSCRIPT_COLLECTOR\urls.txt`
- `YT_TRANSCRIPT_COLLECTOR\README.md`
- `YT_TRANSCRIPT_COLLECTOR\tests\test_collector.py`
- `YT_TRANSCRIPT_COLLECTOR\transcripts\`
- `YT_TRANSCRIPT_COLLECTOR\transcripts\hermes\`
- `YT_TRANSCRIPT_COLLECTOR\reports\`
- `%USERPROFILE%\.hermes\profiles\mtc-steward\`
- `%USERPROFILE%\.hermes\profiles\quantlens-research\`
- `%USERPROFILE%\.hermes\profiles\dashboard-qa\`
- `%USERPROFILE%\.hermes\profiles\backtest-monitor\`
- `%USERPROFILE%\.hermes\profiles\repo-hygiene\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\PROJECT_MEMORY.md`

- `MTC_COMMAND_CENTER\03_QUANTLENS\_user_guide\12_STRATEGY_EVALUATION_RUBRIC.md`  (SP-004 P0A canonical rubric — awaiting Barış D1-D6)
- `MTC_COMMAND_CENTER\06_SCHEMAS\status_envelope.schema.json`  (SP-004 P0A)
- `MTC_COMMAND_CENTER\06_SCHEMAS\evaluation_artifact_v1.schema.json`  (SP-004 P0A, Gate2 inputs)
- `MTC_COMMAND_CENTER\06_SCHEMAS\production_readiness_artifact_v1.schema.json`  (SP-004 P0A, Gate3 inputs)
- `MTC_COMMAND_CENTER\03_QUANTLENS\_templates\strategy_evaluation_record_template.yaml`  (SP-004 P0A)
- `MTC_COMMAND_CENTER\03_QUANTLENS\_user_guide\10_STRATEGY_SCORECARD_REDESIGN_PLAN.md`  (SP-004 plan)
- `MTC_COMMAND_CENTER\11_TRIAGE\_eval_pipeline_source_TEMP\`  (SP-004 source rubric — DELETE in Phase 5)

- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\src\config\profiles\light_risk.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\src\modules\signals\producers\`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\src\cli\mtc_engine_validate.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\tests\test_light_risk_profile.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\tests\test_mtc_engine_validate_cli.py`
- `MTC_COMMAND_CENTER\01_MTC_PROJECT\parity_oracles\feature_adapters\pinets\producer_supertrend_v1.pine`
- `MTC_COMMAND_CENTER\03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md`
- `MTC_COMMAND_CENTER\11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md`

- `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\hardcoded_path_rewrite_TODO.md`
- `MTC_COMMAND_CENTER\11_TRIAGE\ingest.py`
- `MTC_COMMAND_CENTER\11_TRIAGE\generate_worklist.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\paths.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\registry_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\pipeline_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\audit_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\mtc_v2_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_audit_reader.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\12_LLM_WIKI\manual_backfill\2026-05-31\quantlens_source_map.csv`
- `MTC_COMMAND_CENTER\03_QUANTLENS\00_INBOX_REPORTS\Transcrips\`
- `MTC_COMMAND_CENTER\11_TRIAGE\duplicate_url_strategy_audit_2026-05-31.md`
- `MTC_COMMAND_CENTER\11_TRIAGE\duplicate_url_strategy_audit_2026-05-31.csv`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`

## 2026-06-04 Codex GPT-5 active set

- `MTC_COMMAND_CENTER\11_TRIAGE\retriage_progress.json`
- `MTC_COMMAND_CENTER\11_TRIAGE\retriage_dispositions_2026-06-04.md`
- `MTC_COMMAND_CENTER\05_REGISTRY\STRATEGY_RESEARCH_REGISTRY.json`
- `MTC_COMMAND_CENTER\05_REGISTRY\INDICATOR_REGISTRY.json`
- `MTC_COMMAND_CENTER\05_REGISTRY\COMPONENT_REGISTRY.json`
- `MTC_COMMAND_CENTER\05_REGISTRY\TAG_DICTIONARY.json`
- `MTC_COMMAND_CENTER\05_REGISTRY\TRIAGE_CANDIDATE_REGISTRY.json`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG061_ryan_pierpont_breakout_discipline\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG062_stan_weinstein_stage_analysis\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG063_tito_options_aware_rs_breakout\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG032_10_ty_microcap_short\source_intake\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG022_ql_vcp_richard_1d\source_intake\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG056_oliver_kell_price_cycle\source_intake\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`

## 2026-06-04 Codex GPT-5 SP-005 Wave A active set

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\pipeline_reader.py`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-04 DeepSeek SP-004 P1A active set

- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\cpcv_validator.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\probabilistic_pbo.py`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-05 Codex GPT-5 Hermes Desktop install active set

- `%LOCALAPPDATA%\hermes\hermes-agent\`
- `%LOCALAPPDATA%\hermes\hermes-agent\apps\desktop\release\win-unpacked\Hermes.exe`
- `%USERPROFILE%\Desktop\Hermes.lnk`
- `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Hermes.lnk`
- `C:\tmp\hermes_desktop_final.png`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-05 Codex GPT-5 SP-004 all-gate evidence active set

- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_all_gate_evidence.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\cpcv_validator.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\score_gate1.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\score_gate1b.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\score_gate2.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\score_gate3.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\score_all_gates.py`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\final_gate2_2026-06-05_39b51db\all_gate_artifacts\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\final_gate2_2026-06-05_39b51db\scorecard_v2\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\final_gate2_2026-06-05_39b51db\scorecard_v2_all_gate\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\final_gate2_2026-06-05_39b51db\gate1_scorecards\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\final_gate2_2026-06-05_39b51db\gate1b_scorecards\`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\final_gate2_2026-06-05_39b51db\gate3_scorecards\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\PROJECT_MEMORY.md`

## 2026-06-14 Codex GPT-5 Strategy Intelligence dark visual fidelity active set

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_readonly_core.py`
- `MTC_COMMAND_CENTER\11_TRIAGE\ui_references\google_strategy_intelligence_v2_final\`
- `C:\Users\BarışSemaay\.codex\attachments\5689d283-53a2-4a6e-89d5-60b70969990b\pasted-text.txt`
- `C:\tmp\mcc_dark_ui_visual_audit_task.json`
- `C:\tmp\ds_mcc_dark_ui_visual_audit_report.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\PROJECT_MEMORY.md`

## 2026-06-04 SP-004 Batch C + DeepSeek harness active set

- `_deepseek_driver\ds_agent.py`  (NEW — DeepSeek sandboxed subagent harness; untracked)
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\paths.py`  (AUDIT-007)
- `MTC_COMMAND_CENTER\11_TRIAGE\ingest.py`  (AUDIT-010)
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\rigorous_walk_forward.py`  (Batch B, AUDIT-003)
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\rigorous_walk_forward_parallel.py`  (Batch B, AUDIT-003)
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\overnight_v2_runner.py`  (Batch A, AUDIT-001)
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py`  (Batch A, AUDIT-004/006)

## 2026-06-06 Codex GPT-5 MTC lifecycle active set

- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\src\engine\mtc_runner.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\data_tools\validate.py`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\results\producer_parity\ql_fam_momentum_continuation_trx_4h_2026-06-06_after_lifecycle_exit_fix\`
- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\results\mtc_engine_validation_runs\ql_fam_momentum_continuation_20260606_120640Z\`
- `MTC_COMMAND_CENTER\03_STATUS\lifecycle_fixed_2026-06-06\readiness_artifacts\QL_FAM_MOMENTUM_CONTINUATION__TRXUSDT__4h.readiness.json`
- `MTC_COMMAND_CENTER\03_STATUS\lifecycle_fixed_2026-06-06\gate3_scorecards\`
- `MTC_COMMAND_CENTER\03_STATUS\lifecycle_fixed_2026-06-06\scorecard_v2\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\A3_GAP_MATRIX.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-07 Codex GPT-5 UI-36 canonical row active set

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\scorecard_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\read_model.py`
- `MTC_COMMAND_CENTER\_AI_MEMORY\UI Reviev\RESULT_UI36_codex.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-07 Codex GPT-5 night 1M quiet run active set

- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\night_1m_2026-06-07.sh`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\start_night_1m_2026-06-07_keepawake.ps1`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\overnight_runs\_heartbeat_night_1m_2026-06-07.json`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\overnight_runs\_heartbeat.json`
- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\overnight_runs\night_1m_2026-06-07.log`
- `MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\night_1m_2026-06-07\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-14 Codex GPT-5 Strategy Intelligence UI pilot active set

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\11_TRIAGE\ui_references\strategy_intelligence_lovable\CODEX_MTC_STRATEGY_INTELLIGENCE_UI_PILOT_PROMPT.md`
- `MTC_COMMAND_CENTER\11_TRIAGE\ui_references\strategy_intelligence_lovable\`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`

## 2026-06-14 Codex GPT-5 Strategy Intelligence UI rescue active set

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `C:\Users\BarışSemaay\.codex\attachments\2ae7c77a-4fa4-4894-b31f-9e2e654eb12c\pasted-text.txt`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`
## 2026-06-14 Codex GPT-5 dashboard shell replacement correction active set

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_readonly_core.py`
- `MTC_COMMAND_CENTER\11_TRIAGE\ui_references\strategy_intelligence_lovable\`
- `C:\Users\BarışSemaay\.codex\attachments\c3cd19e8-60a2-4685-939a-ce36f028e068\pasted-text.txt`
- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\ACTIVE_FILES.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\PROJECT_MEMORY.md`
