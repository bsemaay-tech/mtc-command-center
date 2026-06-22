# Fusion / 9Router / MTC Boardroom Review

## 1. Model identity
- Model name: Claude (Anthropic), running as Claude Code agent
- Model version/number: Opus 4.8 (`claude-opus-4-8`)
- Runtime/tool: Claude Code CLI (Agent SDK), Windows 11, repo `C:\LAB\Tradingview_LAB_CLEAN`
- Date: 2026-06-22
- Confidence level: High on repo-fit findings (inspected the actual delegation harness); Medium on external-tool feature claims (OpenRouter Fusion / 9Router facts taken from the research brief, not re-verified live in this session).

## 2. Files inspected
Targeted inspection only — no broad repo scan.
- `_deepseek_driver/ds_agent.py` — existing multi-provider delegation harness (full read).
- `_deepseek_driver/` listing (`ds_agent.py`, `README.md`, `__pycache__`).
- `AGENTS.md` — TOKEN DISCIPLINE / delegation section (lines 7–11, 38–51).
- `MTC_COMMAND_CENTER/11_TRIAGE/` listing + `11_TRIAGE/FUSION/` (target folder; existed, empty).
- `grep` for `deepseek|xai|grok|openrouter|provider|delegate|router` across `*.py` (18 hits; most are backtest *data* providers, not AI providers — only `_deepseek_driver/ds_agent.py` is an AI-delegation system).
- Ran `repo_guard.ps1` (dry-run, read-only) → RESULT: PASS, branch `feature/chatgpt-mentor-bundle-plan`.

The two source docs (`fusion_review_generic_model_prompt.md`, `openrouter_fusion_9router_research_brief.md`) live in the user's Downloads, **not** in the repo; the brief's claim that they already sit in `11_TRIAGE/FUSION` is not true as of this session.

## 3. Context understood
Decide whether MTC Command Center should adopt **OpenRouter Fusion**, **9Router**, or build a **custom MTC-native master-judge/workers ("Boardroom") system**. The pattern in question: fan one normalized task out to several independent worker models, then have a judge model synthesize consensus / contradictions / gaps / unique insights into one verdict. The deliverable is this single research report — **no implementation**, no source edits, no new packages, no secrets, repo stays clean.

## 4. Existing repo capability assessment
The repo already has **most of the worker layer**, in one file: `_deepseek_driver/ds_agent.py`.

- **AI providers:** A `PROVIDERS` map already wires `deepseek`, `xai`, `grok`, `openrouter`, `openai`, `ollama` — all as OpenAI-compatible REST endpoints behind one tool-calling loop (`ds_agent.py:50-57`). `resolve_provider()` picks per-task via `task["provider"]` and reads the key from env (`DEEPSEEK_API_KEY`, `XAI_API_KEY`, `OPENROUTER_API_KEY`, …).
- **DeepSeek / xAI:** Already callable today. AGENTS.md TOKEN DISCIPLINE (mandatory) routes bounded mechanical work through this harness; DeepSeek is primary, `grok`/`xai` and `openrouter :free` are listed fallbacks.
- **OpenRouter:** Single-model access is **already supported** (`"openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY")`). OpenRouter **Fusion** (the `openrouter/fusion` slug) is not specifically wired, but would be reachable as just another `model` string on the existing openrouter base URL — near-zero new code.
- **Claude/Codex delegation:** Claude/Codex orchestrate and dispatch tasks to the harness; they are the implementation/judge layer, workers are the cheap models. This is exactly the "orchestrator + workers" half of Fusion.
- **Report/triage folders:** `11_TRIAGE/` is the established home for audits/reports (dozens of dated `*.md`). `11_TRIAGE/FUSION/` is the designated output folder. `ds_agent.py` already writes structured run reports + full transcript to a `report_out` path (default `C:\tmp\ds_<slug>_report.md`).
- **Safety rails already present:** HARD denylist (`.pine`, `parity`, `MTC_V2`, `.git`) never writable; SOFT denylist (`06_SCHEMAS`) opt-in; write allowlist; read-only `run_python` with banned imports/attrs; "no git/commit/push" in system prompt. These are exactly the guardrails the brief asks a Boardroom to own.

**Gap analysis — what's missing to be "Fusion-like":**
1. **Parallel fan-out** — `ds_agent.py` runs **one** provider per task. No multi-worker, same-prompt fan-out.
2. **Judge/synthesis step** — no model reads all worker outputs to extract consensus/contradictions/gaps.
3. **Read-only review mode** — the harness is an *editor* (allowlist writes). A review board should default to **no writes at all**, emitting reports only.
4. **Board definitions / panel selection** — no declarative "architecture_review uses workers X,Y judge Z".
5. **Structured schemas** — worker/judge outputs are free-text markdown, not validated JSON.
6. **Run persistence under FUSION** — reports default to `C:\tmp`, not a versioned `runs/` tree.

## 5. OpenRouter Fusion assessment
- **Usefulness:** Genuinely useful for **high-stakes, low-frequency** decisions where a wrong call costs more than tokens/latency. The `openrouter/fusion` slug gives multi-model deliberation + judge synthesis behind a single API call — no orchestration code to maintain.
- **Best MTC use cases:** architecture decisions, backtest **methodology** review (repaint/lookahead/data-leakage, CPCV/DSR design), strategy-transcript rule extraction sanity-check, "final escalation" audit before a promotion gate. **Not** for routine diffs or formatting.
- **Cost/latency/privacy risks:** Costs more than a single call (multiple underlying completions); slower (fan-out + synthesis); it is an **external cloud dependency**; Fusion server tools are **beta** (API may change). Privacy is the sharp risk for MTC — never send `.env`, keys, broker/exchange/wallet secrets, or whole-repo dumps; send only redacted diff/test/metadata slices.
- **Integration level recommendation:** **Optional provider adapter, manual/escalation trigger only.** Reachable today as a `model` string on the existing openrouter base — do not hardwire it into core workflow, do not make it a default.

## 6. 9Router assessment
- **Usefulness:** Real value as a **local OpenAI-compatible gateway** (`http://localhost:20128/v1`) for provider pooling, fallback routing, and subscription reuse across coding tools. Token-saving features (RTK/Caveman) are a plus for this repo's cost discipline.
- **Local gateway value:** Moderate-high for daily coding ergonomics; low for the *audit/decision* use case this brief targets.
- **Fusion combo value:** Its Combo-Fusion strategy is **very new / actively changing** (per the brief's changelog read). Treat as **pilot**, not dependency.
- **Subscription/fallback value:** Best argument for it — could route the harness's worker calls through one local endpoint and pool quotas. But `ds_agent.py` already reaches providers directly, so the marginal benefit is convenience, not capability.
- **Maturity risks:** local service must be running; provider/session auth can break; quota behavior opaque; logging could capture secrets if misconfigured; vendoring its source into the repo would violate cleanliness rules.
- **Integration level recommendation:** **Optional, external, pilot-only.** Add later as one more adapter pointing at `localhost:20128/v1`. **Do not** `npm install -g 9router` as part of repo setup; **do not** make repo operation depend on it.

## 7. Custom MTC Boardroom feasibility
- **Can we build it?** Yes, cheaply. ~70% of the worker layer already exists in `ds_agent.py` (multi-provider client, key resolution, denylists, report dump). The new code is a thin orchestrator on top.
- **Should we build it?** Yes — Option **C**. A generic router cannot own MTC-specific judgments (protected Pine/MTC_V2 logic, no-repaint/no-lookahead, YouTube-strategy-vs-MTC-light fairness, buy-and-hold benchmark, registry consistency, audit trail). MTC must own board logic; external tools stay replaceable providers.
- **Reuse existing DeepSeek/xAI delegation?** Yes — refactor the provider/client part of `ds_agent.py` into a shared `provider` call (or import it) rather than forking a parallel system. **Avoid a second duplicate harness.**
- **Add OpenRouter API?** Already present; add Fusion as a model string + optional adapter.
- **Master judge/workers structure:** normalize task → fan out same prompt to N workers in parallel (no cross-talk round 1) → collect structured outputs → judge model receives all → emits consensus/contradictions/gaps/unique-insights/risks/next-action → persist run.
- **Minimum MVP:** **read-only review board.** Input = task text + selected git diff + selected test output + protected-file list + context file(s). Workers = DeepSeek + xAI (+ optional OpenRouter single/Fusion). Judge = Claude/Codex (or OpenRouter Fusion). Output = one saved markdown verdict under `11_TRIAGE/FUSION/runs/`. **Zero file edits in the MVP.**

## 8. Recommended architecture
Do not build the full `12_AI_BOARDROOM/` tree from the brief blindly. Start minimal, reuse the harness:

```text
_deepseek_driver/
  ds_agent.py            # existing editor harness — UNCHANGED
  provider.py            # (new, small) extract PROVIDERS + resolve + one-shot chat() call
                         #   so both ds_agent and the board share one provider layer

MTC_COMMAND_CENTER/
  11_TRIAGE/FUSION/      # reports + runs live here until final decision
    CLAUDE_OPUS_4_8_FUSION_REVIEW.md   # (this file)
    <other model reports>
    FINAL_FUSION_INTEGRATION_DECISION.md   # written later by Claude after all reports
    runs/<timestamp>/
      input.md  worker_outputs/  judge.json  final_report.md  metadata.json
  12_AI_BOARDROOM/       # ONLY if MVP proves out — boards/ schemas/ providers/
    boards/architecture_review.yaml ...
    board_runner.py      # read-only: fan-out + judge + persist, NO writes
    mock_provider.py     # tests with no API calls
```

Principles: one shared provider layer (no duplicate client); board runner is **read-only** by construction; secrets never leave the machine; only redacted diff/test/metadata slices are sent; every run logged. Keep it provider-agnostic — DeepSeek/xAI/OpenRouter/Fusion/9Router are all just adapters behind the same `chat()` call.

## 9. Repo cleanliness and safety risks
**Do not touch:** `01_PINE`, `MTC_V2`, `02_MTC_BACKTEST`, `07_ADAPTERS` (protected — need Barış approval), `06_SCHEMAS` (opt-in only), `.git`, broker/live/paper code, `.env` and any credential files. The existing denylist in `ds_agent.py:44-46` already encodes most of this — reuse it, don't reinvent.
- **Dependency risk:** Boardroom needs nothing new beyond `openai` (already a dependency). Reject 9Router global install / vendoring.
- **Duplication risk:** Highest risk. A second AI-delegation harness parallel to `ds_agent.py` would violate AGENTS.md "no duplicate parallel systems." Share the provider layer.
- **Security/API-key risk:** keys via env only (already the pattern); never in task JSON, reports, logs, or sent to any provider.
- **Logging risk:** run logs/transcripts can leak secrets or oversized context. Redact and cap payloads; never dump whole repo.
- **Privacy risk:** external Fusion/OpenRouter calls leave the machine and may be cached/indexed upstream — send minimal redacted slices only.

## 10. Phased implementation plan
- **Phase 0 — research only (NOW):** this report + sibling model reports under `11_TRIAGE/FUSION`. No code. ✅ (this file)
- **Phase 1 — read-only abstraction + mock:** extract `provider.py` from `ds_agent.py`; add a read-only board runner with a `mock_provider` (no real API calls); add run logging under `FUSION/runs/`; write tests.
- **Phase 2 — direct adapters:** wire DeepSeek + xAI + OpenRouter single-model workers (all already reachable) + a Claude/Codex judge. Still read-only, report-only.
- **Phase 3 — OpenRouter Fusion optional adapter:** add `openrouter/fusion` as judge/escalation option; manual trigger; cost guard.
- **Phase 4 — 9Router local optional adapter:** point one adapter at `localhost:20128/v1`; optional, never required.
- **Phase 5 — UI:** an "AI Boardroom" dashboard tab **only after** the CLI/report flow is stable and useful.

Adjustment vs the brief: collapse its 6-phase plan because the worker/provider layer already exists — Phase 1 is mostly *refactor + orchestrate*, not greenfield.

## 11. What not to do
- Do **not** make OpenRouter Fusion or 9Router a core/default/required dependency.
- Do **not** `npm install -g 9router` or vendor its source into the repo.
- Do **not** create a second delegation harness parallel to `_deepseek_driver/ds_agent.py` — extend/share it.
- Do **not** give worker models write access; MVP is read-only. Only one chosen implementation agent ever edits files, and only after a decision.
- Do **not** send `.env`, keys, broker/exchange/wallet secrets, or whole-repo dumps to any external API.
- Do **not** touch protected scopes (`01_PINE`, `MTC_V2`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `06_SCHEMAS`) without Barış approval.
- Do **not** implement anything before `FINAL_FUSION_INTEGRATION_DECISION.md` is accepted.

## 12. Final verdict
**C. Build custom MTC Boardroom with optional OpenRouter Fusion and optional 9Router.**

Why: the repo already owns the hard part — a multi-provider, sandboxed, denylisted worker harness (`ds_agent.py`) that reaches DeepSeek/xAI/OpenRouter today. What's missing (parallel fan-out, a judge step, a read-only review mode, run persistence) is a thin orchestration layer MTC should own, because the decisions involved (protected logic, repaint/lookahead, benchmark fairness, audit trail) are MTC-specific and cannot be delegated to a generic external router. OpenRouter Fusion earns a place as an **optional cloud judge** for rare high-stakes audits; 9Router earns at most an **optional local-gateway pilot**. Neither should be load-bearing.

## 13. Actionable next step
Collect the sibling model reports (Codex/DeepSeek/xAI) into `11_TRIAGE/FUSION`, then have Claude write `FINAL_FUSION_INTEGRATION_DECISION.md` synthesizing them. **No code until that decision is accepted.** (If a single concrete first build step is wanted afterward: Phase 1 = extract `provider.py` from `ds_agent.py` + a read-only `mock_provider` board runner with tests.)
