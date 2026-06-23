# Fusion / 9Router / MTC Boardroom Review

## 1. Model identity
- Model name: DeepSeek V4 Pro
- Model version/number: `deepseek-v4-pro`
- Runtime/tool: opencode CLI, Windows 11, repo `C:\LAB\Tradingview_LAB_CLEAN`
- Date: 2026-06-22
- Confidence level: High on repo-fit (I am the primary worker model in the existing delegation harness — I know firsthand what `ds_agent.py` gives and what it lacks). Medium on external tool claims (taken from research brief + Claude's review; not re-verified live).

## 2. Files inspected
Targeted — no broad scan.
- `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md` — confirms TOKEN DISCIPLINE, dispatch harness usage, protected scopes.
- `_deepseek_driver\` listing — `ds_agent.py` + `README.md` (harness source not re-read this session; Claude's review confirmed its structure and I operate inside it regularly).
- `MTC_COMMAND_CENTER\11_TRIAGE\FUSION\` — existing reports from Claude Opus 4.8 + Codex GPT-5.
- `MTC_COMMAND_CENTER\11_TRIAGE\FUSION\CLAUDE_OPUS_4_8_FUSION_REVIEW.md` — full read, cross-referenced.
- `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md` — confirms all Phases 1-5 complete, provider routing already in harness.
- Repo explore agent report — confirmed no other AI delegation Python exists; no `12_AI_BOARDROOM/`; `04_SHARED\prompts\05_ai_workflow\` missing; `openai` package gap.

The two source docs (`fusion_review_generic_model_prompt.md`, `openrouter_fusion_9router_research_brief.md`) were read as part of this session.

## 3. Context understood
Decide whether MTC should integrate **OpenRouter Fusion**, **9Router**, or build a **custom MTC-native master-judge/workers system**. The core Fusion pattern: fan one normalized task → multiple independent worker models → judge synthesizes consensus/contradictions/gaps/unique insights → one verdict. Goal is Phase 0 research only — no implementation, no source edits, no new deps.

## 4. Existing repo capability assessment

The repo already operates a working worker-jarness system — I am its primary worker.

- **AI providers in `ds_agent.py`:** Already wired: `deepseek` (primary), `xai`/`grok`, `openrouter`, `openai`, `ollama`. All behind one OpenAI-compatible tool-calling loop. Key resolution via env vars. **No second harness exists — this is the single delegation path.**
- **DeepSeek / xAI:** Operational today. AGENTS.md TOKEN DISCIPLINE routes mechanical edits/audits through me (DeepSeek) as primary; xAI/Grok as alternative. I have firsthand knowledge: the harness works, but it is strictly sequential (one model per task, no fan-out, no judge synthesis).
- **OpenRouter:** Single-model access already wired (`OPENROUTER_API_KEY` env). OpenRouter Fusion (`openrouter/fusion` slug) is reachable as a model string change — zero new infrastructure at the provider layer.
- **Claude/Codex delegation:** Orchestrates, dispatches, audits results. Already the judge/orchestrator in practice — just not formalized as a Fusion-style panel.
- **Report folders:** `11_TRIAGE/` established. `11_TRIAGE/FUSION/` is target folder. Harness writes `report_out` to `C:\tmp\ds_<slug>_report.md` — not yet versioned under `FUSION/runs/`.
- **Safety rails:** HARD denylist (`*.pine`/`parity`/`MTC_V2`/`.git`), SOFT denylist (`06_SCHEMAS` opt-in), write allowlist, `run_python` AST-guard, no git/commit — enforced at harness level. Exactly the guardrails a Boardroom needs.

**Gap checklist (confirming Claude's analysis from the worker perspective):**
1. **Parallel fan-out** — absent. Harness runs one provider per task. A true Fusion fan-out would require launching multiple independent tool-calling loops and collecting outputs before synthesis.
2. **Judge/synthesis step** — absent. Claude/Codex manually reads worker reports today, but there is no automated "read all outputs → consensus/contradictions/gaps → verdict" pipeline.
3. **Read-only review mode** — absent. Harness is an editor (allow-based writes). A review board defaults to zero writes.
4. **Board definitions** — absent. No declarative YAML/JSON defining which workers sit on which review panel.
5. **Structured schemas** — absent. Worker/judge output is free-text markdown, not validated JSON.
6. **Run persistence under FUSION** — absent. Reports default to `C:\tmp`, not versioned `runs/<ts>/`.

**Additional gaps I observe (not in Claude's review):**
7. **`04_SHARED\prompts\05_ai_workflow\`** — referenced everywhere as existing (AGENTS.md, START_HERE.md, AI_RULES.md) but directory is missing. This is a blocker for any workflow integration. Must be created before Phase 1.
8. **`openai` package dependency** — GLOBAL_HANDOFF.md logs repeated dispatch failures because `openai` not installed in available Python runtimes. Resolving this is a prereq for any real provider call.
9. **Error handling** — harness has no retry/fallback logic (if DeepSeek is 402 Insufficient Balance, task fails instead of auto-routing to xAI). A Boardroom should add provider fallback.

## 5. OpenRouter Fusion assessment
- **Usefulness:** Real. Pattern has substance: multi-model deliberation catches blind spots a single model misses. OpenRouter's `openrouter/fusion` slug packages this as one API call — lower maint burden than building it ourselves.
- **Best MTC use cases:** architecture decisions, backtest methodology audit (repaint/lookahead/CPCV), strategy-transcript rule extraction cross-check, final escalation before promotion gate. **Not** for small diffs, formatting, routine edits.
- **Cost/latency/privacy risks:** Higher token burn (multiple completions per task). Slower (fan-out wait + synthesis). External cloud — responses may be logged/cached upstream. Fusion server tools marked as beta by OpenRouter docs. Sharpest risk: leaking secrets or whole-repo context. Send only redacted task+diff+test slices.
- **Integration level recommendation:** **Optional provider adapter, manual trigger only.** Add as model string on existing openrouter endpoint. Never default, never required.

## 6. 9Router assessment
- **Usefulness:** Legitimate as local gateway (`localhost:20128/v1`) for provider pooling, fallback, subscription reuse across tools. Token-saving (RTK/Caveman) aligns with repo cost discipline.
- **Local gateway value:** Moderate — useful for daily coding workflow. Low for the audit/decision use case this brief targets.
- **Fusion combo value:** Very new feature (per changelog read in brief). Should be **piloted**, not depended on. Treat as experimental.
- **Subscription/fallback value:** Best argument — pool quotas across Claude/Codex/DeepSeek/xAI through one endpoint. But `ds_agent.py` already calls providers directly; marginal benefit is convenience, not new capability.
- **Maturity risks:** Local service must be up. Auth/session can break. Quota behavior opaque. Logging could capture secrets. Vendoring source into repo would violate cleanliness.
- **Integration level recommendation:** **Optional, external, pilot-only.** If adopted: adapter pointing at `localhost:20128/v1`. Never `npm install -g 9router` as repo setup. Never required for repo operation.

## 7. Custom MTC Boardroom feasibility
- **Can we build it?** Yes. ~70% done already in `ds_agent.py`. What's missing (parallel fan-out, judge step, read-only mode, run persistence) is ~200-300 lines of Python — a thin orchestrator above the existing provider layer.
- **Should we build it?** **Yes — Option C.** A generic router cannot own MTC-specific domain judgments: protected Pine/MTC_V2, no-repaint/no-lookahead, YouTube-strategy-vs-MTC-light fairness, buy-and-hold benchmarks, registry consistency, audit trail. MTC owns these; external tools stay replaceable providers.
- **Reuse existing delegation?** Yes — extract `PROVIDERS` map + `resolve_provider()` + `chat()` from `ds_agent.py` into shared `provider.py`. Do not fork a second harness. One provider layer, two consumers (editor harness + read-only board runner).
- **Add OpenRouter API?** Already present. Fusion is a model string change.
- **Master judge/workers structure:** Fan-out: same normalized prompt → N independent worker calls (no cross-talk) → collect structured outputs → judge (Claude/Codex or OpenRouter Fusion) receives all → emits consensus/contradictions/gaps/unique-insights/risks/next-action → persist run.
- **Minimum MVP:** **Read-only review board.** Input = task text + selected diff + test output + protected-file list + context files. Workers = DeepSeek (me) + xAI (+ optional OpenRouter single/Fusion). Judge = Claude/Codex. Output = one markdown verdict under `11_TRIAGE/FUSION/runs/<ts>/`. **Zero file edits.** Test with `mock_provider` first.

**Worker-perspective addition:** As the primary cheap worker in this repo, I confirm the sequential editor-harness works well for mechanical edits. A parallel review board would give me a new role — technical reviewer alongside xAI as adversarial reviewer, with a judge above producing the final word. This formalizes what Claude already does informally (reading my reports and cross-checking). The value-add is structure + repeatability + logged audit trail.

## 8. Recommended architecture
Extend, don't duplicate. Start minimal, not the full `12_AI_BOARDROOM/` tree from the brief:

```text
_deepseek_driver/
  ds_agent.py            # unchanged — editor harness
  provider.py            # NEW — extract PROVIDERS + resolve + chat()
                          # shared by ds_agent and board_runner
  board_runner.py        # NEW — read-only: fan-out + judge + persist
  mock_provider.py       # NEW — tests, no API calls

MTC_COMMAND_CENTER/
  11_TRIAGE/FUSION/
    DEEPSEEK_V4_PRO_FUSION_REVIEW.md   # (this file)
    CLAUDE_OPUS_4_8_FUSION_REVIEW.md
    CODEX_GPT_5_FUSION_REVIEW.md
    FINAL_FUSION_INTEGRATION_DECISION.md   # to be written by Claude
    runs/<timestamp>/
      input.md
      worker_outputs/   # deepseek.md, xai.md, ...
      judge.json
      final_report.md
      metadata.json

  04_SHARED/prompts/05_ai_workflow/    # MUST CREATE — referenced but missing
    00_index.md
    08_backtest_launch.md
    ... (as needed per AI_RULES.md gates)

  12_AI_BOARDROOM/       # ONLY after MVP proves out
    boards/*.yaml
    providers/*.py       # adapters: deepseek, xai, openrouter, nine_router, mock
    schemas/*.schema.json
```

Principles:
- One shared provider layer (no duplicate client code).
- Board runner defaults to **read-only** — reports only, zero file modifications.
- Secrets: env-only, never in task JSON/reports/logs, never sent to any provider.
- Only redacted diff/test/metadata slices leave the machine.
- Run log + metadata persisted; transcript optionally retained for audit.
- Provider-agnostic: DeepSeek/xAI/OpenRouter/Fusion/9Router are all behind same `chat()` interface.

## 9. Repo cleanliness and safety risks
**Do not touch:** `01_PINE`, `MTC_V2`, `02_MTC_BACKTEST`, `07_ADAPTERS` (protected — Barış approval), `06_SCHEMAS` (opt-in), `.git`, broker/live/paper code, `.env`, credentials. Reuse existing denylist from `ds_agent.py:44-46`.

- **Dependency risk:** Boardroom needs `openai` Python package only (already expected by harness). **Fix the missing `openai` package issue** (GLOBAL_HANDOFF.md has 3+ logged failures).
- **Duplication risk:** HIGHEST risk. Second AI-delegation system parallel to `ds_agent.py` violates AGENTS.md. Must share provider layer. Must reuse `11_TRIAGE/FUSION/` for reports.
- **Security/API-key risk:** Keys via env only (existing pattern). Must not appear in task JSON, worker transcripts, judge reports, or metadata logs. Stricter redaction needed for board mode (multiple workers = more chances to leak).
- **Logging risk:** Worker transcripts can balloon (8 models × long responses). Cap payload size. Never dump full repo context. Sanitize paths/keys before logging.
- **External call risk:** OpenRouter Fusion/9Router calls leave machine. Send minimal redacted slices only. Assume upstream may cache/log.
- **Protected scope risk:** Board must inherit harness denylist exactly. Worker models must never be given write access to `*.pine`/`MTC_V2`/parity files — even read-only board mode needs this enforced.
- **Missing workflow folder:** `04_SHARED\prompts\05_ai_workflow\` referenced by 4+ files as existing — this gap causes confusion. Create with minimal content before Phase 1.

## 10. Phased implementation plan
- **Phase 0 — research only (NOW):** this report + sibling model reports under `11_TRIAGE/FUSION`. No code. ✅ (this file)
- **Phase 0.5 — fix prereqs:** Create `04_SHARED\prompts\05_ai_workflow\` with minimal index. Resolve `openai` package availability in repo Python runtimes. Add provider fallback to harness (402 → try next provider).
- **Phase 1 — read-only abstraction + mock:** Extract `provider.py` from `ds_agent.py`. Add `board_runner.py` with `mock_provider`. Add run logging under `FUSION/runs/`. Write tests.
- **Phase 2 — direct adapters:** Wire DeepSeek + xAI + OpenRouter single-model as workers. Claude/Codex as judge. Still read-only, report-only.
- **Phase 3 — OpenRouter Fusion optional adapter:** Add `openrouter/fusion` as judge/escalation. Manual trigger. Cost guard (max tokens/budget per run).
- **Phase 4 — 9Router local optional adapter:** Point adapter at `localhost:20128/v1`. Optional, never required. Pilot only.
- **Phase 5 — UI (if useful):** AI Boardroom dashboard tab. Only after CLI/report flow stable.

Adjustment vs original brief: The worker layer already exists — Phase 0.5 addresses real blockers found during inspection (missing workflow folder, `openai` package gap, no fallback). Phase 1 is refactor + orchestrate, not greenfield.

## 11. What not to do
- Do **not** make OpenRouter Fusion or 9Router a core/default/required dependency.
- Do **not** `npm install -g 9router` or vendor 9Router source into repo.
- Do **not** create a second delegation harness — extend/share `_deepseek_driver/`.
- Do **not** give worker models write access in board mode; MVP is read-only. Only one chosen implementation agent edits files, and only after a judge decision.
- Do **not** send `.env`, keys, broker/exchange/wallet secrets, or whole-repo dumps to any external API.
- Do **not** touch protected scopes (`01_PINE`, `MTC_V2`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `06_SCHEMAS`) without Barış approval.
- Do **not** implement before `FINAL_FUSION_INTEGRATION_DECISION.md` is accepted.
- Do **not** skip fixing the `04_SHARED\prompts\05_ai_workflow\` gap — it blocks workflow integration.
- Do **not** skip resolving `openai` package dependency — it blocks any real provider call.

## 12. Final verdict
**C. Build custom MTC Boardroom with optional OpenRouter Fusion and optional 9Router.**

Rationale:
1. **The hard part exists.** `ds_agent.py` already has multi-provider key resolution, denylist guardrails, tool-calling infrastructure, and report output. As the primary worker model running inside this harness, I can confirm it works.
2. **What's missing is thin.** Parallel fan-out, judge synthesis, read-only mode, and run persistence are ~200-300 lines of Python — an orchestrator on top of the existing provider layer.
3. **MTC-specific domain cannot be outsourced.** Protected Pine/MTC_V2, no-repaint/no-lookahead, YouTube-vs-MTC fairness, buy-and-hold benchmarks, registry consistency — these are MTC judgments, not generic router judgments. A generic Fusion will not know these constraints. MTC must own the board logic.
4. **OpenRouter Fusion has genuine value as optional cloud judge** for rare high-stakes audits where external multi-model perspective adds value. But it should never be the default or required path.
5. **9Router is a local convenience, not a capability unlock.** Harness already reaches providers directly. 9Router adds pooling/fallback/UX value but creates a new operational dependency. Pilot only.
6. **Prereqs must be fixed first.** Missing workflow folder and `openai` package gap are real blockers logged in GLOBAL_HANDOFF.md. Phase 0.5 before Phase 1.

## 13. Actionable next step
Before coding: fix `04_SHARED\prompts\05_ai_workflow\` (create minimal index), resolve `openai` package in applicable Python runtime, collect remaining model reports into `11_TRIAGE/FUSION/`. Then Claude synthesizes `FINAL_FUSION_INTEGRATION_DECISION.md`. First build step after acceptance: extract `provider.py` from `ds_agent.py` + `mock_provider` + tests.
