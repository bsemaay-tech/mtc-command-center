# Fusion / 9Router / MTC Boardroom Review

## 1. Model identity
- Model name: Codex
- Model version/number: GPT-5 based Codex runtime; exact minor/runtime build not exposed
- Runtime/tool: Codex in local repo workspace, PowerShell shell
- Date: 2026-06-22
- Confidence level: High on repo-fit and local architecture recommendations; medium on current external OpenRouter Fusion and 9Router product details because I used the supplied research brief rather than re-browsing live docs in this run.

## 2. Files inspected
- `AGENTS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/CODEX_PICKUP_2026-06-08.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/DEEPSEEK_DISPATCH.md`
- `MTC_COMMAND_CENTER/09_DOCS/AI_TOOLING/AI_TOOL_INTEGRATION_PLAN.md`
- `_deepseek_driver/README.md`
- `_deepseek_driver/ds_agent.py`
- `MTC_COMMAND_CENTER/11_TRIAGE/FUSION/`
- Downloads: `fusion_review_generic_model_prompt.md`
- Downloads: `openrouter_fusion_9router_research_brief.md`
- `C:/tmp/ds_fusion_boardroom_readonly_repo_inspection_report.md` only to verify the failed cheap-agent attempt wrote no repo files

Targeted search terms used: `deepseek`, `xai`, `grok`, `openrouter`, `ds_agent`, `provider`, `router`, `boardroom`, `fusion`, `9router`.

## 3. Context understood
The decision is whether MTC Command Center should use OpenRouter Fusion, 9Router, or a custom MTC-native master-judge/workers system for multi-model review.

The repo already has a strong AI delegation pattern: Codex/Claude write the task, a cheap model performs bounded work through `_deepseek_driver/ds_agent.py`, and the orchestrator audits the result. The missing piece is not "can we call other models"; the missing piece is a read-only Boardroom layer that fans out the same review task to multiple workers, captures structured responses, and synthesizes a judge verdict while respecting MTC-specific safety rules.

## 4. Existing repo capability assessment
- AI providers: `_deepseek_driver/ds_agent.py` has an OpenAI-compatible provider table for `deepseek`, `xai`, `grok`, `openrouter`, `openai`, and `ollama`.
- DeepSeek: already the primary cheap-agent provider, keyed by `DEEPSEEK_API_KEY`.
- xAI/Grok: already supported by the same harness through `XAI_API_KEY`.
- OpenRouter: already supported as a provider through `OPENROUTER_API_KEY`, but only as a generic OpenAI-compatible endpoint. I found no repo-native OpenRouter Fusion adapter or board-runner abstraction.
- Claude/Codex delegation: already formalized in `AGENTS.md`, `_deepseek_driver/README.md`, `_AI_MEMORY/DEEPSEEK_DISPATCH.md`, and `AI_TOOL_INTEGRATION_PLAN.md`.
- Report/triage folders: `MTC_COMMAND_CENTER/11_TRIAGE/` is the active report area. `MTC_COMMAND_CENTER/11_TRIAGE/FUSION/` already exists and contains a Claude report. `_AI_MEMORY/` is the operating memory layer. `09_DOCS/AI_TOOLING/` is the tool-decision documentation home.
- Existing workflow files: `AI_RULES.md` defines the seven gates and explicit handoff requirements. `DO_NOT_TOUCH.md` protects Pine logic, MTC strategy behavior, and hardcoded path rewrites without approval.

Important repo reality: the existing delegation harness is an editor/audit harness, not a Fusion system. It supports providers and guarded file access, but it does not yet provide independent fan-out, worker schemas, judge synthesis, run metadata, or board-level persistence.

## 5. OpenRouter Fusion assessment
- Usefulness: useful as an optional high-quality external deliberation provider for hard reviews, especially when independent model disagreement matters.
- Best MTC use cases: architecture review, code diff audit, strategy transcript review, backtest methodology review, backtest result review, and final judge escalation.
- Cost risk: higher than single-model OpenRouter calls because Fusion can invoke multiple underlying models plus a judge.
- Latency risk: slower by design due to fan-out and synthesis.
- Privacy risk: high if agents send entire repo context, backtest dumps, logs, or secrets. It should receive only selected, redacted prompt slices, diffs, test output, and summaries.
- External dependency risk: acceptable as an optional provider, unacceptable as a default repo requirement.
- Integration recommendation: optional provider only, behind an MTC-owned abstraction. Do not wire it directly into daily workflows or make it the default.
- Manual/default decision: use manually for high-stakes or ambiguous decisions until cost, output quality, and privacy controls are proven.

OpenRouter Fusion should not become the core architecture. The useful part is the pattern: independent workers plus judge synthesis. MTC should own the task selection, context minimization, safety filters, schemas, and report persistence.

## 6. 9Router assessment
- Usefulness: useful mainly as a local OpenAI-compatible gateway, not as a repo-core dependency.
- Local gateway value: potentially good for local routing, provider pooling, subscription/API fallback, and connecting coding clients through one endpoint.
- Fusion combo value: interesting, but should be treated as a pilot feature based on the supplied brief. It is not mature enough to become load-bearing for MTC.
- Subscription/fallback value: useful outside the repo. It may simplify local provider routing for a human/operator setup, but `_deepseek_driver/ds_agent.py` already supports direct provider routing.
- Maturity risks: local service must be running, provider auth can break, quota behavior may be opaque, logs may capture sensitive prompt content, and new Fusion behavior may change.
- Integration recommendation: optional external local endpoint adapter only, later. Do not install it as part of repo setup. Do not vendor 9Router into the repo.
- Manual/default decision: manual pilot only. It can be tested as `nine_router_local` behind the same provider interface after a mock and direct-provider MVP exists.

9Router should stay outside the repo unless Baris explicitly approves a small optional adapter. Repo operation must not depend on it.

## 7. Custom MTC Boardroom feasibility
- Can we build it? Yes. The provider-call foundation already exists in `_deepseek_driver/ds_agent.py`.
- Should we build it? Yes, but only as a read-only Boardroom/review layer first.
- Can existing DeepSeek/xAI delegation be reused? Yes. The safest path is to reuse or extract the provider table and OpenAI-compatible call logic from `ds_agent.py`, not create a second unrelated model-routing stack.
- Can OpenRouter API be added? It is already present as a provider slug in `ds_agent.py`; what is missing is a clean adapter contract and an optional Fusion-specific call mode.
- How should master judge/workers be structured? Workers should be independent first-pass reviewers. They should not see each other's answers. The judge receives worker outputs, identifies consensus, contradictions, missing coverage, unique findings, and gives a final action recommendation.
- Minimum MVP: read-only, mock-first, no source edits, no package installs, no trading logic contact, no live API calls required for tests.

Minimum MVP should do:
- Accept a task description plus selected context files/diffs/test output.
- Redact or block secrets and protected files.
- Run a mock provider in tests.
- Optionally call existing DeepSeek/xAI/OpenRouter adapters only when explicitly enabled.
- Persist a run folder or report with inputs, worker outputs, judge synthesis, metadata, provider names, and cost/token fields where available.
- Produce Markdown for human review.

What is probably missing today:
- Board definitions.
- Worker response schema.
- Judge response schema.
- Independent fan-out controller.
- Report/run persistence contract.
- Context redaction and size limits for external providers.
- Tests that prove read-only behavior and no protected-file leakage.

## 8. Recommended architecture
Recommended path: keep the existing `_deepseek_driver` as the provider/delegation source of truth, then add a thin read-only Boardroom layer only after Phase 0 reports are reviewed.

Clean shape:

```text
_deepseek_driver/
  ds_agent.py              # existing guarded edit/audit harness
  provider_client.py       # future small extraction, shared by ds_agent and boardroom

MTC_COMMAND_CENTER/
  11_TRIAGE/
    FUSION/
      *_FUSION_REVIEW.md
      FINAL_FUSION_INTEGRATION_DECISION.md
      runs/                # optional after approval; read-only reports/artifacts

  12_AI_BOARDROOM/          # only after approval, if a separate module is preferred
    boards/
    schemas/
    providers/
    tests/
```

I would not create `12_AI_BOARDROOM/` during the research phase. If implemented later, start either under `11_TRIAGE/FUSION/` for reports-only experimentation or a small dedicated module after final approval.

Provider abstraction:
- `deepseek_direct`
- `xai_direct`
- `openrouter_single`
- `openrouter_fusion_optional`
- `nine_router_local_optional`
- `mock_provider`

Keep all providers behind the same contract: `run_review(input) -> structured worker response`. The board runner should never edit source files.

## 9. Repo cleanliness and safety risks
- Avoid touching: `*.pine`, anything containing `MTC_V2`, parity paths, `.git`, `.env`, credential files, broker/live execution paths, `06_SCHEMAS` unless explicitly approved, and trading/backtest behavior.
- Dependency risk: adding 9Router or OpenRouter Fusion directly as a repo dependency would create local setup and availability problems.
- Duplication risk: highest risk. A new model-routing harness parallel to `_deepseek_driver/ds_agent.py` would violate the repo's existing token-discipline design.
- Security risk: worker prompts may accidentally include secrets, API keys, OAuth tokens, broker keys, exchange keys, or private repo context.
- API key risk: keys must stay in environment variables only. They should not appear in task JSON, reports, logs, screenshots, or model prompts.
- Logging risk: Boardroom reports must avoid saving full unredacted prompts if they contain secrets, private transcripts, or oversized repo context.
- Cost risk: Fusion-like systems can multiply token usage. This repo already tracks spend with CodeBurn; Boardroom runs need explicit cost controls and should be reserved for high-value decisions.

The current repo is already dirty/untracked in this area: `MTC_COMMAND_CENTER/11_TRIAGE/FUSION/` and `CHATGPT_MENTOR_BUNDLE_PLAN_2026-06-22.md` are untracked. I did not remove or overwrite them.

## 10. Phased implementation plan
- Phase 0: research only. Keep collecting model reports in `MTC_COMMAND_CENTER/11_TRIAGE/FUSION/`. No implementation.
- Phase 1: read-only abstraction/mock provider. Create a tiny Boardroom runner with mock provider, schemas, and tests. No real API calls. No source edits by workers.
- Phase 2: direct DeepSeek/xAI/OpenRouter adapters. Reuse/extract the existing `_deepseek_driver/ds_agent.py` provider logic instead of forking a second router.
- Phase 3: OpenRouter Fusion optional adapter. Manual trigger only, cost-labeled, context-minimized, never default.
- Phase 4: 9Router local optional adapter. Treat `http://localhost:20128/v1` as a configurable optional endpoint. Do not require 9Router installation.
- Phase 5: UI only if needed. Add dashboard visibility after the CLI/report workflow is stable and useful. UI should be read-only.

Adjustment from the supplied brief: Phase 1 should emphasize reusing the existing harness/provider logic. This is not greenfield provider routing.

## 11. What not to do
- Do not implement anything before the final integration decision is accepted.
- Do not make OpenRouter Fusion the default provider.
- Do not make 9Router a required repo dependency.
- Do not install 9Router from inside this repo workflow.
- Do not vendor 9Router or any provider SDK into the repo.
- Do not create a second delegation harness parallel to `_deepseek_driver/ds_agent.py`.
- Do not let worker models edit files directly in the first Boardroom MVP.
- Do not send whole-repo dumps to external models.
- Do not send secrets, `.env`, credentials, exchange keys, broker keys, wallet keys, OAuth tokens, or private API keys to any model.
- Do not touch Pine, MTC strategy behavior, parity, live/broker code, or schemas without explicit approval.
- Do not treat model consensus as trading approval or promotion evidence.
- Do not add dashboard write-back controls.

## 12. Final verdict
C. Build custom MTC Boardroom with optional OpenRouter Fusion and optional 9Router.

Why: MTC already has direct provider/delegation capability for DeepSeek, xAI/Grok, OpenRouter, OpenAI, and Ollama through `_deepseek_driver/ds_agent.py`. Directly adopting OpenRouter Fusion or 9Router as the core would duplicate or bypass repo-specific safety rules. MTC's value comes from its own guardrails: protected Pine/MTC/parity boundaries, no-repaint/no-lookahead standards, backtest methodology rules, report persistence, and skeptical review workflow.

OpenRouter Fusion is worth keeping as an optional cloud judge/escalation provider. 9Router is worth considering as an optional local gateway/pilot endpoint. Neither should be mandatory, default, or load-bearing.

## 13. Actionable next step
Have Claude or the designated final reviewer read all reports in `MTC_COMMAND_CENTER/11_TRIAGE/FUSION/` and write `FINAL_FUSION_INTEGRATION_DECISION.md`. No code implementation should begin before that decision is accepted.
