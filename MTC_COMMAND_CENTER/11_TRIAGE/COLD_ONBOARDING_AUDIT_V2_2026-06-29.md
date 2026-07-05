# Cold Onboarding Audit v2 — DeepSeek v4 Pro (via opencode)

## Repo confirmed: `C:\LAB\Tradingview_LAB_CLEAN` (legacy-repo trap avoided: yes)

## Files I read (and what pointed me there)

| # | File | Pointer |
|---|------|---------|
| 1 | `AGENTS.md` | Self (entrypoint) |
| 2 | `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md` | AGENTS.md:5 |
| 3 | `MTC_COMMAND_CENTER\_AI_MEMORY\AI_RULES.md` | START_HERE.md:5 |
| 4 | `MTC_COMMAND_CENTER\03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md` | AGENTS.md:28 (Gate 0 mandatory) |
| 5 | `MTC_COMMAND_CENTER\11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md` | AGENTS.md:29 (Gate 0 mandatory) |
| 6 | `MTC_COMMAND_CENTER\04_SHARED\prompts\05_ai_workflow\00_index.md` | AGENTS.md:26 |
| 7 | `MTC_COMMAND_CENTER\04_SHARED\prompts\05_ai_workflow\08_backtest_launch.md` | 00_index.md:25 |
| 8 | `MTC_COMMAND_CENTER\04_SHARED\prompts\05_ai_workflow\07_handoff_update.md` | AI_RULES.md:86 (Gate 7 prompt) |
| 9 | `MTC_COMMAND_CENTER\03_QUANTLENS\data\README.md` | AGENTS.md:34 (data inventory) |
| 10 | `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md` | START_HERE.md:5 |
| 11 | `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md` | START_HERE.md:5 |
| 12 | `MTC_COMMAND_CENTER\_AI_MEMORY\DO_NOT_TOUCH.md` | AI_RULES.md:97 |
| 13 | `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md` | AGENTS.md:58 |
| 14 | `MTC_COMMAND_CENTER\_AI_MEMORY\CODEX_PICKUP_2026-06-08.md` | START_HERE.md:3 |
| 15 | `MTC_COMMAND_CENTER\03_QUANTLENS\_user_guide\12_STRATEGY_EVALUATION_RUBRIC.md` | Gap search (W2 scoring detail) |
| 16 | `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\backtest_reader.py` | Gap search (W3 dashboard consumption) |
| 17 | `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\scorecard_reader.py` | Gap search (W3 dashboard consumption) |
| 18 | `MTC_COMMAND_CENTER\05_REGISTRY\AI_QUANTLENS_VERDICT_REGISTRY.json` | Gap search (W4 verdict format) |
| 19 | `MTC_COMMAND_CENTER\_AI_MEMORY\SPRINT_WORKFLOW.md` | 00_index.md:13 |

## Workflow-uniformity matrix

| Job | PASS / PARTIAL / GAP | Authoritative source (file/§) | Where two agents would diverge |
|-----|----------------------|-------------------------------|-------------------------------|
| W1 backtest | **PASS** | AGENTS.md §DATA & LAUNCH (lines 32-41) + RUNBOOK.md §0.5.1 | No divergence. Exact `$env:MEGA_BUNDLE_MANIFEST=...` + `python mega_walk_forward.py --strategy <id> --symbol <SYM> --tf <tf>` is one unambiguous command. Data binding via env var is deterministic. In-day/sprint/overnight variants all documented in runbook §0.5 table. |
| W2 scoring/gates | **PASS** | Rules doc §§6,8,9 (classification, quality gates, promotion levels) + Rubric doc §12 (per-gate /100 criteria) + RUNBOOK.md §4.1 (DSR thresholds) | Low divergence risk. Classification labels, gate list, promotion ladder, and /100 criteria with min-75 thresholds are all explicit. DSR calibration (0.50 research / 0.85 production) is in runbook §4.1. Rubric D5 numeric bands are deferred (anchors provisional) — minor ambiguity on exact band boundaries but gates are binary PASS≥75. |
| W3 results → MCC dashboard | **PARTIAL** | RUNBOOK.md §6.4 (overnight-end sequence) + backtest_reader.py + scorecard_reader.py + build_profile_result_artifact.py + mcc_night_tail.sh | **Scattered pipeline.** Runbook §6.4 steps 1–4 describe the overnight-end sequence (aggregate→alpha→morning report→dashboard upgrade→lessons). But a cold agent doing a single-strategy run (not overnight) would not know which subset applies. `backtest_reader.py` globs `*_results.json` from `05_BACKTEST_RESULTS/`. `scorecard_reader.py` scans `scorecard_v2/*.scorecard.json`. `build_profile_result_artifact.py` writes `backtest_profile_result.json`. `mcc_night_tail.sh` enriches scorecards via CPCV+PBO+scoring pipeline. No single "artifact contract" document maps which writer→which artifact→which reader→which UI panel. **Two agents would wire the pieces differently**, especially for single-strategy vs overnight runs. The "no fabrication" rule is clear (spread across NEXT_STEPS.md + GLOBAL_HANDOFF.md + AGENTS.md). |
| W4 AI verdict | **GAP** | CODEX_PICKUP_2026-06-08.md item 3 + AI_QUANTLENS_VERDICT_REGISTRY.json + GLOBAL_HANDOFF.md line 1791 | **No production procedure exists.** The verdict registry (212 entries, Codex GPT-5 authored on 2026-06-08) is opinion-only metadata with a reader (`expert_quantlens_reader.py`) and UI section. But there is zero documentation of HOW a verdict is produced: what evidence is mandatory, what decision tree yields NEEDS_CLARIFICATION vs RESEARCH_ONLY vs SALVAGE vs PASS, who decides, what quality bar applies, whether a verdict is one-shot or revisable. CODEX_PICKUP says "manually review each strategy → produce a QuantLens verdict → write to a new data file" — no criteria. **Two agents would produce wildly different verdicts** for the same strategy. The scorecard is explicitly the only scoring authority; the verdict is "commentary/labels only" — but without a rubric for that commentary, it has no reproducibility. |
| W5 AI_MEMORY update | **PASS** | AI_RULES.md §Gate 7 (lines 78-86) + 07_handoff_update.md | No divergence. Exact file list (GLOBAL_HANDOFF.md, NEXT_STEPS.md, SESSION_LOG.md mandatory; DECISIONS.md/ACTIVE_FILES.md/PROJECT_MEMORY.md conditional). Format conventions from AGENTS.md lines 45-55: GLOBAL_HANDOFF.md header = `## [MODEL_NAME] YYYY-MM-DD — Topic`; NEXT_STEPS.md tags = `[AI: Claude\|DeepSeek\|Any\|Barış]`. 07_handoff_update.md step-by-step for each file. |
| W6 git workflow | **PASS** | DO_NOT_TOUCH.md + AGENTS.md §PARALLEL AGENT SAFETY (lines 18-24) + AI_RULES.md lines 94-97 | No divergence. Branch policy: never work on master, branch `feature/<scope>` first (DO_NOT_TOUCH.md:26). Staging: exact explicit paths only, no `git add .`/`-A` (DO_NOT_TOUCH.md:26-27). Commit-after-every-agent rule (AGENTS.md:20). No destructive ops (`reset --hard`, `push --force`, `--no-verify`, `stash`) without approval (AI_RULES.md:94-97). Protected scopes listed in next section. |
| W7 tool auto-use | **PASS** | AGENTS.md §AI TOOL AUTO-USE (lines 57-67) + AI_TOOL_INTEGRATION_PLAN.md | No divergence. Each tool has exact command + trigger: (a) PDF→`markitdown_ingest.py` (AGENTS.md:60-61); (b) impact→`graphify_impact.py` (AGENTS.md:62-63); (c) cost→`codeburn status` (AGENTS.md:64); (d) mechanical edit→`_deepseek_driver/ds_agent.py` (AGENTS.md:10-12, TOKEN DISCIPLINE). The overnight watchdog (AGENTS.md:65) is also listed. |

## Fidelity check (F1–F5 with confidence)

| # | Question | Answer | Confidence | Source |
|---|----------|--------|------------|--------|
| F1 | Single command + env var to run engine on one strategy/symbol/timeframe | `$env:MEGA_BUNDLE_MANIFEST = "<repo>\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"; python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --strategy <id> --symbol SPY --tf 10m` | HIGH | AGENTS.md:37-39, data/README.md:10-12 |
| F2 | Dataset for SPY 10m + how engine is told | Bundle `native_multiasset_alpaca_2026-06-28/` (51 symbols × 7 TFs, SPY 10m = PASS, 357/357 validated, ~11.86M bars). Engine told via `$env:MEGA_BUNDLE_MANIFEST` pointing to bundle's `manifests\dataset_manifest.json`. Filters: `--symbol SPY --tf 10m`. | HIGH | data/README.md:24 (bundle row), AGENTS.md:35, AGENTS.md:38-39 |
| F3 | Is a single-cell PASS promotable? Why/why not? | **No.** Rules doc §8 requires multi-symbol (cross-symbol consistency ≥5 cells), multi-window, buy&hold comparison, DSR, BH-FDR. Runbook §3.2: "Single-cell pass kabul etme" (dismiss single-cell pass). AGENTS.md:30: "single-strategy results without buy&hold + DSR + BH-FDR + multi-window are not promotable." A single cell fails cross-symbol consistency and statistical robustness requirements. | HIGH | Rules doc §8, RUNBOOK.md §3.2:185-187, AGENTS.md:30 |
| F4 | Installed AI tools by name + triggers | **(a) MarkItDown** (wrapper: `markitdown_ingest.py`) — trigger: any binary doc (.pdf/.docx/.pptx/.xlsx). **(b) Graphify** (wrapper: `graphify_impact.py`) — trigger: any impact/blast-radius question. **(c) CodeBurn** (global npm: `codeburn status`) — trigger: session start/end, big run, model routing decision. **(d) DeepSeek dispatch harness** (`ds_agent.py`) — trigger: bounded mechanical work. **(e) Run-progress supervisor + watchdog** (`run_emitter_supervisor.py` + `run_watchdog.py`) — trigger: long backtest/overnight run. | HIGH | AGENTS.md:60-65, AI_TOOL_INTEGRATION_PLAN.md §5 |
| F5 | Protected scopes never touch without approval | `*.pine`, `parity`, `MTC_V2`, `.git/`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `06_SCHEMAS`, Pine logic, MTC strategy behavior, TradingView parity, trading logic, promotion gates, scoring rules. Hard denylist in cheap-agent harness: `*.pine`/`parity`/`MTC_V2`/`.git` (cannot be prompted away). | HIGH | DO_NOT_TOUCH.md:6-19, AGENTS.md:14 (harness denylist) |

## GAPS (ranked by severity)

### 1. [CRITICAL] W4 — No AI verdict production procedure (GAP)

**Missing:** A documented step-by-step procedure for producing an AI QuantLens verdict. The registry exists (`AI_QUANTLENS_VERDICT_REGISTRY.json`, 212 entries, opinion-only), a reader exists (`expert_quantlens_reader.py`), and the dashboard displays it. But there is **zero** documentation of:
- What evidence is mandatory before a verdict can be rendered
- What decision criteria distinguish NEEDS_CLARIFICATION / RESEARCH_ONLY / SALVAGE / PASS
- Who decides (which model, under what constraints)
- Whether verdicts are one-shot or revisable

**Impact:** Two cold agents given the same strategy would produce completely different verdicts with no shared methodology. The verdict section in the dashboard would carry uncalibrated opinions.

### 2. [HIGH] W3 — Dashboard artifact pipeline is fragmented (PARTIAL)

**Where:** RUNBOOK.md §6.4 (6-step overnight-end sequence) + `backtest_reader.py` + `scorecard_reader.py` + `build_profile_result_artifact.py` + `mcc_night_tail.sh`.

**Missing:** No single "artifact contract" document that maps:
- Writer script → artifact produced → dashboard reader it feeds → UI panel it populates
- Which subset applies to single-strategy runs (not overnight)

The runbook §6.4 covers overnight only. A cold agent running a single-strategy backtest (W1 path) wouldn't know whether to also run `build_profile_result_artifact.py`, `mcc_night_tail.sh`, or `aggregate_overnight_iters.py` to populate the dashboard.

**Impact:** Two agents would produce different dashboard content for the same backtest output — one might call `mcc_night_tail.sh` on a single run, another might skip it, a third might run only `alpha_vs_buyhold.py`.

### 3. [MEDIUM] Data-bundle selection ambiguity for overlapping symbol/TF (PARTIAL)

**Where:** `data/README.md` lists `native_multiasset_alpaca_2026-06-28/` (PRIMARY, SPY 10m PASS) and `native_us_equities_10m_alpaca_2026-06-28/` (SPY 10m PASS, "superseded… kept for provenance").

**Issue:** The README says narrower bundle is "superseded" but also "kept for provenance" — without an explicit rule. A cold agent sees two valid manifests and must make a judgment call (pick PRIMARY). This is a subtle choice, not a documented rule. An explicit statement like "always prefer the PRIMARY bundle unless explicitly testing provenance" would close this.

### 4. [MEDIUM] START_HERE.md active pickup link is stale (GAP)

**Where:** START_HERE.md:3 says `read _AI_MEMORY/CODEX_PICKUP_2026-06-08.md FIRST`. That file is 3 weeks old (2026-06-08). Most items in it are marked DONE. The true active state is in GLOBAL_HANDOFF.md (last entry 2026-06-29, Claude Opus — dataset built).

**Impact:** A cold agent following START_HERE literally spends time processing stale pickup items before finding the real active state.

### 5. [MEDIUM] "QuantLens" name ambiguity across docs (PARTIAL)

**Where:** CODEX_PICKUP_2026-06-08.md item 3 explains the rename: old Gemini pre-screen was renamed FROM "QuantLens" TO "Gemini Pre-Screen"; "QuantLens" is now reserved for the AI expert verdict. But older docs (START_HERE.md, GLOBAL_HANDOFF.md entries pre-06-08) use "QuantLens" in multiple contexts.

**Impact:** A cold agent reading multiple chronological layers of handoff would need to carefully disambiguate "QuantLens the research engine" from "QuantLens the AI verdict" from "QuantLens the (old) Gemini pre-screen."

### 6. [LOW] Rubric DRAFT status vs canonical usage (PARTIAL)

**Where:** `12_STRATEGY_EVALUATION_RUBRIC.md` header says "DRAFT (Phase 0A deliverable)" but the backtest rules doc and scoring engines treat it as canonical. The D5 numeric bands remain "DEFERRED" (anchors provisional).

**Impact:** Low — the gates are binary PASS≥75 regardless of band precision. But a strict agent might question using a DRAFT document as a scoring standard.

## Verdict: for which job types is the workflow uniform across cold agents, and where would they still diverge?

**Uniform (PASS):** W1 (backtest launch), W2 (scoring/gates), W5 (AI_MEMORY update), W6 (git workflow), W7 (tool auto-use). All have one authoritative file with an exact procedure. Two cold agents would produce identical results.

**Partially uniform (PARTIAL):** W3 (dashboard artifacts) — the overnight pipeline is documented but fragmented; single-strategy artifact flow is undocumented. Two agents would produce different dashboard content from the same raw backtest output.

**Would diverge (GAP):** W4 (AI verdict) — no production procedure exists. Two agents would produce wildly different verdicts on the same strategy.

**Data-binding gap from prior audit:** **CLOSED** — AGENTS.md now has an explicit DATA & LAUNCH section with the exact env var mechanism (`MEGA_BUNDLE_MANIFEST`), the canonical run command, and a pointer to the authoritative data inventory README. The data README lists all bundles with symbol/TF/bar-count detail. A cold agent can now deterministically bind data to the engine. Residual ambiguity (gap #3 above) is minor — there are two bundles with overlapping SPY 10m, but labeling one "PRIMARY" and the other "superseded" gives clear guidance.
