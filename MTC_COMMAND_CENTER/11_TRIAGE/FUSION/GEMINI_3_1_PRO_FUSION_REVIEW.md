# Fusion / 9Router / MTC Boardroom Review

## 1. Model identity
- Model name: Gemini Pro
- Model version/number: 3.1 Pro (High)
- Runtime/tool: Antigravity Agent
- Date: 2026-06-22
- Confidence level: High

## 2. Files inspected
- `C:\Users\BarışSemaay\Downloads\fusion_review_generic_model_prompt.md` (Prompt)
- `C:\Users\BarışSemaay\Downloads\openrouter_fusion_9router_research_brief.md` (Research Brief)
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\FUSION\CLAUDE_OPUS_4_8_FUSION_REVIEW.md` (Repo context)

## 3. Context understood
The goal is to determine whether to integrate OpenRouter Fusion, 9Router, or a custom MTC-native master-judge/workers system into the MTC Command Center repository. The focus is on leveraging a Fusion-style multi-model review panel without polluting the existing repository with redundant architectures, hardcoded dependencies, or compromising security.

## 4. Existing repo capability assessment
- **AI providers**: A multi-provider delegation harness already exists in `_deepseek_driver/ds_agent.py`. It supports `deepseek`, `xai`, `grok`, `openrouter`, `openai`, and `ollama` as OpenAI-compatible REST endpoints.
- **DeepSeek & xAI**: These are already callable via the existing harness.
- **OpenRouter**: Single-model OpenRouter access is already supported in the harness.
- **Claude/Codex delegation**: Claude and Codex act as orchestrators dispatching tasks to the worker layer (`ds_agent.py`).
- **Report/triage folders**: `11_TRIAGE` is established for audits and reports, including the `11_TRIAGE/FUSION` folder.
- **Workflow files**: `ds_agent.py` contains safety rails (denylists for `.pine`, `MTC_V2`, etc.). What is missing is the parallel fan-out and judge synthesis step for a full Boardroom system.

## 5. OpenRouter Fusion assessment
- **Usefulness**: High value for complex decisions (multi-perspective synthesis), but unnecessary for simple coding tasks.
- **Best MTC use cases**: Architecture review, backtest methodology review, strategy transcript review, final audit escalation.
- **Cost/latency/privacy risks**: Slower and more expensive than single calls. Privacy is a major risk; sensitive data (keys, full repo dumps) must never be sent to the external OpenRouter API.
- **Integration level recommendation**: Optional provider.
- **Should it be optional/default/manual?**: Optional and manual (for high-stakes reviews only).

## 6. 9Router assessment
- **Usefulness**: Functions as a local gateway for fallback and subscription pooling.
- **Local gateway value**: Useful for coding ergonomics.
- **Fusion combo value**: Very new and experimental. Not mature enough for core repo dependency.
- **Subscription/fallback value**: Good for maximizing provider quotas.
- **Maturity risks**: Requires a local service to be running constantly; auth may break; not built for strict MTC logging or governance out of the box.
- **Integration level recommendation**: Optional local pilot.
- **Should it be optional/default/manual?**: Optional and manual.

## 7. Custom MTC Boardroom feasibility
- **Can we build it?**: Yes. The `ds_agent.py` harness already implements the worker connection layer.
- **Should we build it?**: Yes. A generic external router cannot handle MTC-specific logic (e.g., Pine protections, lookahead/repaint checks).
- **Can existing DeepSeek/xAI delegation be reused?**: Yes. The provider logic in `ds_agent.py` can be abstracted and shared.
- **Can OpenRouter API be added?**: Yes. It is already supported.
- **How should master judge/workers be structured?**: Fan-out to DeepSeek, xAI, and other workers -> collect structured outputs -> Claude/Codex (or OpenRouter Fusion) judges and synthesizes -> generate final verdict.
- **What minimum MVP should do?**: A read-only review board. No code modification. Emits a single markdown verdict after analyzing task + diff + test output.

## 8. Recommended architecture
- Extract the provider logic from `_deepseek_driver/ds_agent.py` into a shared module (e.g., `provider.py`) to prevent duplicating the client.
- Introduce `12_AI_BOARDROOM/board_runner.py` (read-only orchestrator).
- Retain all reports in `11_TRIAGE/FUSION/runs/`.
- Treat DeepSeek, xAI, and OpenRouter as interchangeable provider adapters behind the `provider.py` abstraction.

## 9. Repo cleanliness and safety risks
- **Files/folders to avoid touching**: `01_PINE`, `MTC_V2`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `06_SCHEMAS`, `.git`, `.env`, credential files.
- **Dependency risks**: Boardroom should only use existing dependencies (like `openai`). Do not globally install 9Router or vendor it.
- **Duplication risks**: High risk of creating a duplicate AI harness if `ds_agent.py` is ignored.
- **Security risks**: Sending whole repo dumps, `.env` files, or exchange keys to external APIs.
- **API key risks**: Must remain in environment variables only.
- **Logging risks**: Secrets could leak into `run/` logs if not properly filtered.

## 10. Phased implementation plan
- **Phase 0**: Research only (this phase, generating model reports).
- **Phase 1**: Refactor `ds_agent.py` to extract a shared `provider.py`. Build a read-only board runner with a mock provider.
- **Phase 2**: Wire direct DeepSeek, xAI, and OpenRouter single-model workers into the read-only board.
- **Phase 3**: Add OpenRouter Fusion as an optional judge adapter.
- **Phase 4**: Add 9Router as an optional local gateway adapter.
- **Phase 5**: UI integration (only if CLI/report flow is proven).

## 11. What not to do
- Do NOT install 9Router globally or make it a mandatory dependency.
- Do NOT rely exclusively on OpenRouter Fusion.
- Do NOT create a parallel worker harness; extend the existing `ds_agent.py`.
- Do NOT allow the MVP board to write or edit files.
- Do NOT implement any code before the `FINAL_FUSION_INTEGRATION_DECISION.md` is approved.

## 12. Final verdict
**C. Build custom MTC Boardroom with optional OpenRouter Fusion and optional 9Router**

**Why**: MTC Command Center has unique, domain-specific requirements (Pine guardrails, backtest integrity, repaint checks) that generic cloud routers (OpenRouter Fusion) or local gateways (9Router) cannot enforce. By building a custom, thin orchestration layer on top of the already existing `ds_agent.py` worker harness, MTC retains full control over the execution context, safety rails, and audit trails, while still leveraging the benefits of OpenRouter Fusion and 9Router as optional plugins.

## 13. Actionable next step
Wait for Claude to review all generated model reports in `11_TRIAGE\FUSION` and synthesize them into `FINAL_FUSION_INTEGRATION_DECISION.md`. Do not start Phase 1 until that decision is finalized.