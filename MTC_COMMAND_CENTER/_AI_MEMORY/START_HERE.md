# START_HERE

> **▶▶ CURRENT ENTRY POINT — 2026-08-17:
> `..\11_TRIAGE\NEW_CHAT_HANDOFF_2026-08-17.md`.** Its §1 is the copy-paste
> prompt. **THE BRIDGE IS DEPLOYED AND RUNNING DISARMED on Hostinger KVM2**
> (release `be007fd8…`, since 2026-08-17T00:25:02Z, loopback-only,
> credential-free) — evidence `..\11_TRIAGE\KVM2_DEPLOYMENT_EXECUTED_2026-08-17.md`.
> Owner dashboard: `..\11_TRIAGE\KVM2_RUNKIT\Start-BridgeDashboard.cmd`.
> Never state a deployment status without naming the host. TESTNET wallet/ARM,
> Dashboard V2, and the network-audit redo are each separately owner-gated.
> Chain lane owner-paused; Pathscope closed. Every banner below is historical.
>
> Three facts that must not be re-learned the hard way: **GATEA-STAGING is a
> local Hyper-V VM on Barış's PC** and the bridge is already installed there and
> already ran disarmed for 2.5 days — while **KVM2 has nothing**, so never state
> a deployment status without naming the host. **Pathscope is closed**; a sixth
> cycle is forbidden. **Prerequisite gate 2 is UNKNOWN**, not satisfied.

> **Pathscope disclosure (owner decision 2026-08-16, section 6):** Pathscope is a supplemental aid only: its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream, and no Pathscope PASS may close any gate.
> Governing record: MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_SUPPLEMENTAL_DISCLOSURE_V2_2026-08-16.md. Identity split: the prover in this repository is the older 137520-byte R5 code; the audited 185272-byte Option C prover is UNMERGED on codex/pathscope-accounting-redesign-20260815. Prerequisite gate 2 is UNKNOWN until the Lead re-derives it at freeze-prerequisite review.


> **▶ CURRENT WP-I ENTRYPOINT — 2026-08-16 morning.** Start with
> `..\11_TRIAGE\NEW_CHAT_HANDOFF_2026-08-16_MORNING.md` **plus its correction
> banner**, then `..\11_TRIAGE\OWNER_DECISIONS_2026-08-16_MORNING.md` — **all six
> owner decisions are ANSWERED there** (staging-channel admin review approved ·
> Option A two-commit chain · cumulative plan reading · 6 h audit cap metered ·
> archive approved · Pathscope supplemental-with-disclosure, off critical path,
> no further cycle). The 2026-08-15 banner below is historical: its "Pathscope
> remains the active owner boundary" sentence is superseded by decision §6.
> Stage-1 now waits only on the admin review's eight channel facts and the
> reviewed two-commit chain design.

> **▶ historical (2026-08-15) —** Start with
> `..\11_TRIAGE\NEW_CHAT_HANDOFF_2026-08-15_AFTER_RP7_ACCEPTANCE.md` and
> `..\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md`.
> RP7 rows 1-9 is now **T0 ACCEPTED** on candidate `80cbed46` after Codex PASS
> and Claude PASS-WITH-NITS, zero required repairs. Pathscope remains the active
> owner boundary after its final authorized audit transport-BLOCK; do not rerun
> it without a new explicit owner decision. The older 2026-08-12/13 live-run
> banner immediately below is historical and is superseded by this paragraph.

> **▶▶ LIVE WP-I RUN — 2026-08-12/13. START WITH
> `..\11_TRIAGE\FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md`.** It is self-contained, its §0 is a
> **binding operating contract** (never idle · 4–6 parallel lanes · Codex primary · Claude Max is
> RESERVE with very little credit left · GLM is the second auditor while the Claude Pro window is
> shut · GLM/Max can NEVER fill a second-flagship slot), and §6 lists what is in flight. The
> next hard milestone is **23:00 Europe/Chisinau**, when the Claude Pro weekly window reopens and
> four second-flagship audits run back to back. Their kickoffs are written, preflighted and
> corrected — dispatch is immediate.

> **▶ CURRENT STATE: read `_AI_MEMORY/GLOBAL_HANDOFF.md` (newest section first) + `NEXT_STEPS.md` for live work.** The older `_AI_MEMORY/CODEX_PICKUP_2026-06-08.md` is historical (most items DONE) — read only for back-context. Everything below is standing reference.

Read order: `AGENTS.md`, this file, `AI_RULES.md`, `PROJECT_MEMORY.md`, `GLOBAL_HANDOFF.md` if needed, `NEXT_STEPS.md`, then project handoff files.

> **MANDATORY TWO-TIER MODEL (see `AGENTS.md` § Two-Tier):** Task recipient = **Lead** (Claude CLI *or* Codex CLI — whichever opened the session). Lead orchestrates and owns acceptance. Lead delegates *implementation* to the counterpart flagship CLI (Codex ↔ Claude). Cheap models (DeepSeek, Cline) are implementer sub-delegation tools only — never the lead. If the counterpart CLI is unavailable, the lead must surface the blocker and must not self-implement work assigned to the counterpart. Gates G1 (Scope) and G7 (Handoff) are **Lead-owned**. Gates G2–G4 (Plan/Impl/QA) are **Implementer-owned**. Gate G5 (Review) is **Lead-independent-inspection**. See `AI_RULES.md` and `SPRINT_WORKFLOW.md` for gate-level actor assignments.

> **MANDATORY AUDIT-TIER CLASSIFICATION (see `AGENTS.md` § AUDIT TIER POLICY — PERMANENT DEFAULT):** Every Gate-1 scope must classify its audit tier as **T0 / T1 / T2 / T3** and record it **before** audit dispatch. The tier decides auditor count, effort, cadence, and round cap. Rationale/history: `..\11_TRIAGE\OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` (owner-ratified 2026-08-10 as repo-wide permanent default).

> **Naming:** "QuantLens" = the research backtest engine/lab under `03_QUANTLENS/` AND the AI **expert-verdict** layer (labels-only opinions; the Scorecard owns all numbers). The old "QuantLens" Gemini pre-screen was renamed "Gemini Pre-Screen" — ignore that usage in pre-2026-06-08 handoff entries.

Workflow gates and prompt templates: see `AI_RULES.md` and `..\04_SHARED\prompts\05_ai_workflow\00_index.md`.

Per-job procedures (so every agent does a job the same way): backtest data+launch → `AGENTS.md` "DATA & LAUNCH"; results → dashboard → `..\11_TRIAGE\RESULTS_TO_DASHBOARD_MAP_2026-06-29.md`; AI/QuantLens verdict authoring → `..\03_QUANTLENS\_user_guide\13_AI_VERDICT_AUTHORING_PROCEDURE.md`.

AI tool auto-use (MarkItDown for binary docs, Graphify for impact questions, CodeBurn for cost/routing): see the `AI TOOL AUTO-USE` section in `AGENTS.md` and `..\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md`. Use them automatically at their triggers; don't wait to be told.

GLM supplemental routing (Z.AI Coding Plan model selection for sub-delegation): see `AGENTS.md` §GLM SUPPLEMENTAL ROUTING (canonical; cheapest-capable tier first; routing record required per task; GLM never replaces a flagship slot required by the audit tier, but may fill its T1 conditional or T2 reviewer slot).

Account homes, wrappers, and credential *source* names (Codex `CODEX_HOME` routes + mandatory Claude→Codex launcher, GLM, Cline, DeepSeek, Grok, NVIDIA NIM): `AI_ACCOUNT_AND_MODEL_ROUTING.md` — operational index only, no secrets; usage figures there are a dated snapshot and must be re-checked. `AGENTS.md` stays canonical for roster/tiers/policy.

HER backtest / optimizasyon için (in-day tek strateji, sprint, overnight — fark etmez) **zorunlu pre-read iki dosya:**
1. Canonical kurallar: `..\03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md` (4 gate, buy&hold + alpha, DSR, BH-FDR, classification, promotion levels, antigravity checklist)
2. Operasyonel runbook: `..\11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md`

Akış: `..\04_SHARED\prompts\05_ai_workflow\08_backtest_launch.md`. Single-strategy 5dk run dahi 4-gate (rolling WF + bootstrap+BH-FDR + DSR + multi-window) + buy&hold karşılaştırması olmadan promotable değil.

**Veri + çalıştırma (kanonik):** Hangi datayı kullanacağını bilmeden backtest çalıştırma. Otorite envanter: `..\03_QUANTLENS\data\README.md` (tüm native bundle'lar — sembol/timeframe/asset-class/bar sayısı + crypto data konumları). US equities / ETF / multi-asset / 10m **var**; engine'in hardcoded default manifest'i eski crypto arşivi, güncel data DEĞİL. Engine data seçimi: `MEGA_BUNDLE_MANIFEST` env → bir bundle'ın `manifests\dataset_manifest.json`'u + `--symbol`/`--tf`. Kanonik tek-koşu: `python ..\03_QUANTLENS\tools\mega_walk_forward.py --strategy <id> --symbol <SYM> --tf <tf>` (research engine; `walk_forward_processor.py` alt-seviye/custom). Birincil bundle: `native_multiasset_alpaca_2026-06-28`.

Do not change trading logic, Pine logic, MTC behavior, or parity checks without explicit approval.

**Before designing or auditing any executable check/block/preregistration, read
`..\11_TRIAGE\DESIGN_DEFECT_PATTERNS_2026-08-10.md`.** Ten recurring defect patterns
distilled from 24 required findings across seven adversarial audits, each with the
falsification that exposes it and a rule to apply before writing code. The first one —
an inability to evaluate must STOP, never FAIL — accounts for the single most expensive
gap of that cycle and recurred independently in a second artefact the same night.

## Strategy research (combining existing strategies/indicators)

Before any strategy-research session, read in this order:
1. `STRATEGY_COMPONENT_LIBRARY.md` — what exists, what combines.
2. `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` + `INDICATOR_REGISTRY.json` +
   `COMPONENT_REGISTRY.json` + `TAG_DICTIONARY.json`.
3. `STRATEGY_RESEARCH_WORKFLOW.md` (16-step process) and
   `STRATEGY_CODE_REVIEW_CHECKLIST.md`.

During research: log every variant (`VARIANT_LOG_REGISTRY.json` +
`03_QUANTLENS/_templates/VARIANT_LOG_TEMPLATE.md`), save runs under
`03_QUANTLENS/research/<run_id>/`, register in `RESEARCH_RUN_REGISTRY.json`, and
confirm visibility in the **Strategy Research Lab** dashboard tab. Do not reinvent
these workflows or hand-edit generated registries (regenerate via
`03_QUANTLENS/tools/build_strategy_research_registry.py`).

User-supplied transcripts/screenshots go in `00_INBOX/USER_INTAKE/`; route them
with `03_QUANTLENS/tools/route_user_intake.py` into each strategy's `source_intake/`.
