# AGENTS.md

> **REPO IDENTITY — read before anything.** This repository is **`C:\LAB\Tradingview_LAB_CLEAN`** (the live MTC Command Center). The sibling directory **`C:\LAB\tradingview-lab` is the FROZEN legacy repo — do NOT read its onboarding, run, or edit anything there.** If your entrypoint resolved under `C:\LAB\tradingview-lab\...`, stop and switch to `C:\LAB\Tradingview_LAB_CLEAN`. The canonical onboarding chain exists only in this repo under `MTC_COMMAND_CENTER\_AI_MEMORY\`.

Read this file first, then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Use token-efficient search before broad scans.
Do not change trading logic, Pine logic, MTC strategy behavior, or TradingView parity without explicit approval.

## TWO-TIER OPERATING MODEL (MANDATORY — read before dispatching any task)

The flagship model that receives Barış's task is the **LEAD ORCHESTRATOR** and independent acceptance authority.
- **Codex is lead:** delegates implementation to Claude Code CLI.
- **Claude is lead:** delegates implementation to Codex CLI.

The **IMPLEMENTER** (the counterpart flagship) may — only when useful and within scope/safety rails — sub-delegate bounded mechanical work (single/few-file edits, schema/JSON edits, script writing, audit runs) to DeepSeek or Grok via **Cline CLI** (first choice) or **`_deepseek_driver`** (fallback). See TOKEN DISCIPLINE below.

**Lead responsibilities (non-delegable):**
1. Independently inspect the actual diff/files, check scope and protected surfaces, and run or reproduce proportionate validation — never accept the implementer's self-report alone.
2. On any failure: send a focused repair prompt to the same counterpart implementer and repeat until an accepting verdict or a concrete blocker. Maximum 3 repair/re-audit rounds; after the third non-accepting verdict, stop and report to Barış.
3. Repo hygiene may begin only after an accepting audit verdict (PASS or PASS-WITH-NITS) — only where task/user authorization permits — commit/push and proceed to the next approved task.
4. Gate 5 is the lead's independent cross-model audit of the implementer's work, not mere report review.

**Implementer responsibilities:** implementation + self-QA (Gates 3–4). Scope, acceptance, repair loop, and authorized Git sequencing belong to the lead.

**If the required counterpart CLI/auth is unavailable:** the lead reports that concrete blocker and does not silently replace the counterpart with itself.

Hard safety gates remain unchanged: no Pine/parity/MTC/trading changes without explicit approval, no destructive Git, no secrets, no deployment/live action without explicit authorization.

## CANONICAL AUDIT ROSTER — Gate 5 and Gate 6 (MANDATORY)

Define once here; prompts may cross-reference but must include enough detail to be safely copy-pasted standalone.

### Claude auditor (G5 and G6)

- **Model:** `claude-opus-5` | **Effort:** `xhigh` — always, no exceptions.
- No Sonnet, no implicit/latest alias, no silent fallback.
- **If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives it.**
- Fresh independent session every audit round — never `--resume` or `--continue` from the implementer session.
- Example CLI: `claude -p --model claude-opus-5 --effort xhigh --no-session-persistence`

### Codex auditor (G5 and G6)

- **Model:** `gpt-5.6-sol` — always, no implicit alias.
- **Effort `high`** for ordinary Gate 5 audits.
- **Effort `xhigh`** whenever ANY of these apply: Gate 6 security review; Pine/parity/MTC/trading/protected surface; architecture or cross-cutting change; re-audit after REQUEST_CHANGES or BLOCK.
- **If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives it.**
- Fresh independent session every audit round.
- Example CLI (ordinary G5): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c "model_reasoning_effort=high" <audit_prompt_file>`
- Example CLI (G6/protected/re-audit): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c "model_reasoning_effort=xhigh" <audit_prompt_file>`

### DeepSeek V4 Flash auditor (G5 and G6) — canonical auditor 3

- **Model:** `cline-pass/deepseek-v4-flash` via Cline CLI. **Owner-authorised 2026-08-01 (D025).**
- Example CLI: `cline -P cline-pass -m cline-pass/deepseek-v4-flash --auto-approve false --cwd <audit worktree> "<audit prompt>"`
- Fresh independent session every audit round. Read-only intent; audit in a dedicated worktree at the frozen SHA, then verify `git status --porcelain` is empty to prove it edited nothing.

### GLM-5.2 auditor (G5 and G6) — canonical auditor 4

- **Model:** `GLM-5.2` via the Z.AI Coding Plan route. **Owner-authorised 2026-08-01 (D025).**
- Fresh independent session every audit round; same worktree-isolation and cleanliness proof as above.

### Four-auditor acceptance rule (D025 — governs all four entries above)

1. **A canonical auditor that cannot execute the mandated test suite must return BLOCK.** Non-execution is never acceptance. Codex already applies this to itself; it now binds every auditor. If a model can read the diff but not reproduce the evidence, its opinion is supplemental for that round regardless of the label it prints.
2. **A required finding from ANY canonical auditor is binding — after the Lead reproduces it on real source.** This is not a weakening: `AGENTS.md` already requires independent Lead inspection, and it stops a weaker model burning a capped repair round on a finding that does not reproduce. A finding the Lead cannot reproduce is recorded as unreproduced with the evidence, not silently dropped.
3. **Acceptance requires accepting verdicts from both flagship auditors** (`claude-opus-5` xhigh and `gpt-5.6-sol` xhigh) **plus no unresolved reproduced required finding from any auditor.** The flagships remain the acceptance floor because they are the two that have historically executed the suite and found real defects; auditors 3 and 4 add detection, not a veto based on an unexecuted read.
4. **Known failure mode, do not forget it:** GLM-5.2 once returned PASS-WITH-NITS on a commit carrying two severe defects while being unable to run the suite at all. Rule 1 exists because of that exact event.
5. This roster expansion supersedes the older restriction (including the 50-hour plan §23c/§39-10 wording, and D024's advisory-only limit) **for audit authority only**. It grants **no** implementation authority: protected Bridge/core-runtime implementation remains with the flagship implementer, and secondary models still may not implement protected work.

### Audit session contract

Provide only: scope contract, plan (if any), actual diff/files, test evidence, required repo rules.
Never feed implementer session context or continue it. The lead still owns acceptance and must inspect actual repo state independently.

### Verdict standards (all audit gates)

| Verdict | Meaning |
|---------|---------|
| **PASS** | Clean — no required changes. |
| **PASS-WITH-NITS** | Accepting — optional nits only; zero required repairs. Cannot contain a required repair — use REQUEST_CHANGES instead. |
| **REQUEST_CHANGES** | Non-accepting — contains at least one required repair. |
| **BLOCK** | Workflow cannot safely continue. |

### Repair loop bound

**Maximum 3 repair/re-audit rounds per task.** After the third non-accepting verdict (REQUEST_CHANGES or BLOCK), stop and report the blocker to Barış. Do not silently enter a fourth round.

### D026 — FALSIFIED-TEST RULE: a regression test is not evidence until it has been shown to fail (MANDATORY)

**Owner-ratified 2026-08-03.** A regression test claimed as evidence that a specific defect is closed **does not count as closure evidence** until it has been demonstrated:

1. **RED** against the exact pre-fix/reverted behaviour — or against an equivalent deliberate mutation/falsification — and
2. **GREEN** with the fix in place,

with the **commands and their real output recorded** in the evidence package. Asserting that a test covers a defect is not the same as showing it fails without the fix.

- If safe reversion is impractical, an **independent mutation/falsification** is required instead. If neither is done, the test is classified **supplemental — not closure evidence**, and the defect is not closed.
- **Binds implementers and auditors alike.** Implementers must produce the demonstration; auditors must check it rather than accept the claim, and must state for each new test whether they verified it.
- Applies with particular force to **protected Bridge, build, deployment, persistence, concurrency and safety defects**.
- **Does not** require mutating every unrelated legacy test. It governs tests offered as proof that a named defect is fixed.

**Why this exists — three real instances in a single session (2026-08-03), all on protected surfaces:**

| Defect | The test | How it failed |
|---|---|---|
| 3b `wal_state_bundle` | drift regression test | Discriminated on the string literal `"SELECT 1"`. Swapping the fix for `SELECT 2` — which touches no table and leaves the defect fully intact — left it **green**. |
| Build determinism | writable-path test | Asserted `returncode == 0`, which the *old* predicate also returned. Its only real guard sat in an `except OSError` branch that never executes on Linux, the deployment platform. |
| Build determinism | metacharacter-path test | Built an **LF-only** fixture and asserted success. The defective code succeeded too, while silently skipping inspection. |

In every case the test looked correct on review and was only exposed when someone deliberately broke the code underneath it. Two were caught by cross-model Gate 5 audit, not by the implementer or the Lead.

## TOKEN DISCIPLINE — implementer-tier sub-delegation to cheap models (MANDATORY)
Within the two-tier model above, the **IMPLEMENTER** (Claude Code CLI or Codex CLI) may sub-delegate bounded mechanical work to a cheap sub-agent. **Cline CLI is the first-choice path** (uses monthly subscription credits before paid API spend); fall back to `_deepseek_driver` when Cline is unavailable, unauthenticated, out of credits, unsuitable, blocked, or when explicit provider routing / DeepSeek API is desired.

### Cline CLI (first choice)
```
cline --cwd C:\LAB\Tradingview_LAB_CLEAN --auto-approve false "<bounded task prompt>"
```
For ClinePass subscription credits, prefer:
```
cline -P cline-pass -m cline-pass/deepseek-v4-flash --cwd C:\LAB\Tradingview_LAB_CLEAN --auto-approve false "<bounded task prompt>"
```
Use `cline-pass/deepseek-v4-pro` when the task needs stronger reasoning. Add `--json` when machine-readable logs are useful. Cline handles file reads/writes with its own safety rails; the orchestrator must still **audit results on real data** (never trust the sub-agent report). Do NOT route trading logic, Pine, parity, MTC strategy behavior, protected scopes, or schemas through Cline without explicit approval.

### _deepseek_driver (fallback/secondary)
- Harness: `_deepseek_driver\ds_agent.py`; how-to: `_deepseek_driver\README.md` (READ before dispatching).
- Flow: write task JSON (prompt + `allow` files + rails) → `python _deepseek_driver\ds_agent.py --task <file>` → **audit the result yourself on real data** (never trust the sub-agent report).
- Providers (env keys): `deepseek` (primary), `grok`/`xai` (`grok-4`), `openrouter` (`:free` = cheap/fallback). Route bulk/cheap work to the cheapest capable model.
- Safety (enforced in harness, not promptable away): HARD denylist `*.pine`/`parity`/`MTC_V2`/`.git` never writable; `06_SCHEMAS` only via `schema_allow`; writes limited to `allow`; `run_python` read-only; no git/commit; `read_file` capped 60KB (pre-extract small samples for huge files).
- Hand-edit yourself only for a trivial 1-liner cheaper than a dispatch round-trip. Serialize same-file tasks; parallelize disjoint ones.
Update relevant handoff files before stopping after approved write sessions.

## GLM SUPPLEMENTAL ROUTING — QUOTA-EFFICIENT (CANONICAL)

Single authoritative source for Z.AI Coding Plan model selection when sub-delegating via GLM models. Other memory files cross-reference here; do not copy the routing table elsewhere. GLM never replaces the mandatory audit roster (§CANONICAL AUDIT ROSTER) or the counterpart flagship implementer.

### Official facts (Lead-verified 2026-07-27 — time-sensitive; re-verify before acting after quota/model changes)

- Sources: https://docs.z.ai/devpack/faq · https://docs.z.ai/devpack/latest-model · https://docs.z.ai/guides/overview/pricing · https://docs.z.ai/guides/llm/glm-4.7
- **Coding Plan entitlement:** GLM-5.2, GLM-5-Turbo, GLM-4.7. Quota: 5.2/Turbo 3× peak, 2× off-peak; **temporary 1× off-peak cap through Sep 2026** (verify after Sep).
- **Z.AI recommendation:** 4.7 for routine/general; 5.2 for high-difficulty.
- **API tier** lists 5.2, 5.1, 4.7, 4.5-Air — API listing alone does **not** prove Coding Plan entitlement.
- **GLM-5.1** is NOT confirmed in the Coding Plan FAQ; do not assume entitlement. If absent on the active route, tighten scope with 4.7 or escalate directly to 5.2 if the task genuinely requires flagship.
- **GLM-4.7:** confirmed Coding Plan, agentic coding, 200K context.
- **Default Z.AI mapping example** (Haiku → 4.5-Air, Sonnet/Opus → 5.2) is the provider default for generic use. **Repo intentionally overrides this** — use the routing table below, not the provider default.
- **External helper status:** the current helper hard-maps all three tiers to 5.2 and is **out of scope**. Routine work must not use the fixed helper merely because it exists. Reconfiguring the helper requires separate Barış authorization; no external config was changed in this policy update.

### Canonical routing tiers

| Tier | Model | Use when |
|------|-------|----------|
| 1 — cheapest | 4.5-Air (only if active route explicitly supports it; else 4.7) | Discovery · targeted rg · format · small docs · simple JSON/YAML · log summary · bounded mechanics with no protected-surface impact |
| 2 — standard | GLM-4.7 | Ordinary coding · narrow bug · focused test · routine review/inspection · bounded unprotected multi-file |
| 3 — intermediate | GLM-5.1 **only if active route/entitlement explicitly confirms it** | Moderate debug · cross-file · concurrency/persistence repair · bounded architecture. If absent: use Tier 2 with tighter scope, or jump to Tier 4 if classification genuinely requires flagship. |
| 4 — flagship | GLM-5.2 | Difficult architecture · protected (Bridge/trading/risk/identity/persistence/concurrency/migration/broker) code · adversarial safety · complex post-audit repair · exact-model user request. **Never merely because available.** |

**Mapping shorthand:** Haiku → cheapest verified (4.5-Air if route supports, else 4.7) · Sonnet → 4.7 · Opus → 5.2 only when classification requires.

### Cheapest-capable decision tree

```
Is the task discovery / format / rg / small-doc / bounded-mechanics?
  YES → Tier 1 (4.5-Air if route supports; else Tier 2)
  NO ↓
Is the task ordinary coding / narrow bug / focused test / routine inspection / bounded unprotected multi-file?
  YES → Tier 2 (GLM-4.7)
  NO ↓
Is GLM-5.1 explicitly confirmed on the active route AND the task is moderate debug / cross-file / concurrency / bounded architecture?
  YES → Tier 3 (GLM-5.1)
  NO or UNSURE → skip to ↓
Does the task touch: difficult architecture; protected surface (Bridge/trading/risk/identity/persistence/concurrency/migration/broker); adversarial safety; complex post-audit repair; or is an exact-model user request?
  YES → Tier 4 (GLM-5.2)
  NO → can Tier 2 handle with tighter scope? Tighten and use 4.7. If not, escalate with written evidence.
```

### Six routing examples

| # | Task | Protected? | Tier / Model |
|---|------|------------|--------------|
| 1 | Update cross-reference in a memory doc (simple docs) | No | Tier 1 — 4.5-Air |
| 2 | Rename constant in a test file (mechanical test update) | No | Tier 1 — 4.5-Air (or Tier 2 if route lacks 4.5-Air) |
| 3 | Fix typo in Bridge order-formatter — Gate 1 has explicitly classified this exact path as unprotected; no broker, order-behavior, risk, persistence, concurrency, or evidence impact (ordinary Bridge bug, Gate 1-proven unprotected) | No (Gate 1 explicit) | Tier 2 — 4.7 |
| 4 | Repair idempotency logic in Bridge order executor touching risk/persistence (protected) | Yes | Tier 4 — 5.2 |
| 5 | Gate-5 adversarial audit of a cross-file refactor (Gate-5 audit) | Yes (audit surface) | **Canonical roster only** — `claude-opus-5` xhigh or `gpt-5.6-sol` high/xhigh; GLM is not a Gate-5 auditor |
| 6 | Barış requests exact GLM-5.2 for a specific bounded task (exact-model request) | N/A | Tier 4 — 5.2 (honor; no silent fallback or downgrade) |

> **Bridge default:** Any Bridge task not explicitly proven unprotected by Gate 1 classification defaults to protected — route to Tier 4 / GLM-5.2.

### Mandatory context rules for GLM tasks

- **Targeted rg first** — never recursively search `C:\` or drive/repo root. Use exact path allowlist per task.
- Line/symbol reads before full-file reads for large sources. Default max full-file: **400–500 lines** unless the task contract requires the complete file.
- Batch independent read-only checks in one call. Avoid many tiny turns.
- Fresh session when context is excessive. No `--resume`/`--continue` unless Barış explicitly authorizes.
- `--no-session-persistence` does **not** reduce active context or save quota.
- Lead provides compact evidence package for Tier 4 (5.2) tasks — do not feed whole-session context to the GLM call.
- Exact permissions in task JSON to avoid denial loops.
- Stop broad exploration once evidence is found. Record measured token/context consumption after unexpectedly large runs.

### Required routing record — every delegated/sub-delegated GLM task

```
Classification      : <tier + task type>
Protected           : <yes / no + reason>
Model + provider    : <GLM-X.Y via Z.AI Coding Plan>
Cheaper-model rationale : <why not one tier lower>
Exact paths         : <allow list>
Context/tool budget : <estimate>
Fallback            : <if entitlement unavailable>
External API credits: <yes / no>
```

## PARALLEL AGENT SAFETY — COMMIT AFTER EVERY AGENT (MANDATORY)
When multiple agents work on shared files (app.js, styles.css, etc.) in sequence or parallel:
- **Commit immediately after each agent completes** — before the next agent starts.
- Never leave an agent's work as uncommitted changes while launching a new agent on the same file.
- Reason: any agent that sees code not in git HEAD will treat it as corruption and may run `git checkout HEAD -- <file>`, silently destroying all prior agents' uncommitted work.
- When writing agent prompts, always state: "These files contain uncommitted changes from prior agents. Do NOT run git checkout, git reset, or git stash on any tracked file."
- If you cannot commit (e.g. Barış must approve), explicitly pause the pipeline — do not hand the file to the next agent raw.
Follow the workflow gates in `MTC_COMMAND_CENTER\_AI_MEMORY\AI_RULES.md`.
Use the prompt library at `MTC_COMMAND_CENTER\04_SHARED\prompts\05_ai_workflow\` (start at `00_index.md`).
For ANY backtest / optimization (in-day single-strategy, sprint, or overnight), TWO files are mandatory pre-read (Gate 0):
  1. Canonical rules: `MTC_COMMAND_CENTER\03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md` (4 gates, classification, promotion, antigravity checklist, morning report standard)
  2. Operational runbook: `MTC_COMMAND_CENTER\11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md`
Follow `04_SHARED\prompts\05_ai_workflow\08_backtest_launch.md`. Same gates apply whether the run is 5 minutes or 12 hours — single-strategy results without buy&hold + DSR + BH-FDR + multi-window are not promotable.

## DATA & LAUNCH — which data + exact run command (canonical)
Before running ANY backtest you must know which data the engine uses. Do not guess, and do not assume crypto-only.
- **Authoritative data inventory:** `MTC_COMMAND_CENTER\03_QUANTLENS\data\README.md` — every native bundle (symbols, timeframes, asset classes, bar counts) plus where crypto data lives. US equities, ETFs (commodity/index/bond/sector proxies), multi-asset, and 10m DO exist. The engine's hardcoded default manifest points to a legacy crypto archive and is NOT the current data.
- **How the engine selects data:** set env `MEGA_BUNDLE_MANIFEST` to a bundle's `manifests\dataset_manifest.json`; filter further with `--symbol` / `--tf`.
- **Canonical single-run command (QuantLens research engine):**
  ```
  $env:MEGA_BUNDLE_MANIFEST = "<repo>\MTC_COMMAND_CENTER\03_QUANTLENS\data\<bundle>\manifests\dataset_manifest.json"
  python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --strategy <id> --symbol <SYM> --tf <tf>
  ```
  `mega_walk_forward.py` is the canonical engine for strategy×symbol×timeframe research runs; `walk_forward_processor.py` is a lower-level/custom single-shot path, not the default. Primary multi-asset bundle: `native_multiasset_alpaca_2026-06-28`.

For STRATEGY RESEARCH (combining existing strategies/indicators into new candidates), read `MTC_COMMAND_CENTER\_AI_MEMORY\STRATEGY_RESEARCH_WORKFLOW.md` first. Strategy/indicator/component/tag inventory lives in `MTC_COMMAND_CENTER\05_REGISTRY\*.json` (generated by `03_QUANTLENS\tools\build_strategy_research_registry.py`) and is tracked in the dashboard's **Strategy Research Lab** tab. Log every variant in `VARIANT_LOG_REGISTRY.json`; save runs under `03_QUANTLENS\research\<run_id>\`. User transcripts/screenshots go in `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\`.

When writing to GLOBAL_HANDOFF.md, prefix each new section header with model name and date:
  Format: ## [MODEL_NAME] YYYY-MM-DD — Topic
  Example: ## Claude Sonnet 4.6 2026-06-01 — Transcript fix
Do NOT create per-model log files at repo root. GLOBAL_HANDOFF.md is the single source of truth for all models.

When adding tasks to NEXT_STEPS.md, tag each task with which AI can execute it:
  Format: [AI: Claude|DeepSeek|Any|Barış]
  Claude       — complex architectural work, cross-file refactors, git ops, verification, TradingView MCP
  DeepSeek     — narrow script fixes, audit runs, analysis (via opencode)
  Any          — read-only tasks, simple single-file analysis
  Barış        — requires human judgment, manual review, or explicit approval

## AI TOOL AUTO-USE (apply without being asked)
Local helper tools are installed. Use them automatically at the triggers below — do NOT wait for Barış to name the tool. Full rationale + per-tool detail: `MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md`.

- **Binary doc to read/ingest** (`.pdf`/`.docx`/`.pptx`/`.xlsx` in `00_INBOX\USER_INTAKE` or anywhere you must read one) → FIRST convert to Markdown, then read the `.md`, never feed the raw binary to a model:
  `python MTC_COMMAND_CENTER\03_QUANTLENS\tools\markitdown_ingest.py <file-or-dir> --apply --out <dir>`
- **Impact / blast-radius question** ("what breaks if I change X", cross-file refactor, "what depends on Y") → build a scoped code graph and query it instead of guessing:
  `python MTC_COMMAND_CENTER\03_QUANTLENS\tools\graphify_impact.py build <scoped-path>` then `… affected "<file.py>"` / `… explain "<symbol>"` / `… query "<question>"`. (Wrapper keeps graphs in temp; never commit `graphify-out/`.)
- **Cost / token check** (session start or end, after a big run, or when deciding model routing) → `codeburn status` (and `codeburn models` for the breakdown). If premium spend (Opus/Codex) dwarfs delegated work, route more mechanical work through **Cline CLI first**, then `_deepseek_driver` fallback, per TOKEN DISCIPLINE above.
- **Long backtest / overnight run** (you want done/failed/stalled visibility without staying open) → launch it under the run-progress supervisor so the stable contract is written, then let the one-shot watchdog notify: `03_QUANTLENS/tools/run_emitter_supervisor.py` + `run_watchdog.py` (canonical `progress/<run_id>/` heartbeat·events·status; git-ignored). Engine is not edited (supervisor observes the runner's existing `run_status.json`). Ops + n8n/Task-Scheduler wiring: `09_DOCS/AI_TOOLING/PHASE5_WATCHDOG_OPS.md`.

Rules: these tools are read-only/local; they never touch `*.pine`/`MTC_V2`/`parity`/schemas. Do not run `graphify install` (no per-vendor skill registration — the CLI/wrapper is the single shared path). Install once if missing: `uv tool install graphifyy --python 3.13`; MarkItDown venv self-bootstraps via its wrapper.

## AI BOARDROOM — multi-model review (APPROVAL-GATED, do NOT auto-run)
Read-only multi-model review board: one task → independent worker models (DeepSeek/xAI/OpenRouter) review with no cross-talk → a judge model synthesizes consensus / contradictions / coverage gaps / unique insights / risks / next action. Tool: `_deepseek_driver\board_runner.py` (shared provider layer in `_deepseek_driver\provider.py`). Config example: `_deepseek_driver\board_example.json`.

- **When to PROPOSE it** (Claude and Codex both): high-stakes or ambiguous decisions where a wrong call costs more than tokens/latency — architecture decisions, backtest *methodology* review (repaint/lookahead/data-leakage, CPCV/DSR design), strategy-transcript rule-extraction cross-check, promotion-gate escalation, risky cross-file refactor review. NOT for routine edits, formatting, or small known changes (those go through TOKEN DISCIPLINE dispatch).
- **Approval gate (MANDATORY):** a real run spends tokens and sends redacted task/diff/test slices to external APIs. Claude/Codex must **ask Barış and get explicit approval BEFORE any real (non-dry-run) run.** The `--dry-run` mock path (no network, no cost) needs no approval and is the way to demo/validate first.
- **Run:** `python _deepseek_driver\board_runner.py --config <board.json> [--dry-run]`.
- **Output:** `MTC_COMMAND_CENTER\11_TRIAGE\FUSION\runs\<timestamp>\` (git-ignored) — `final_report.md`, `worker_outputs\*.md`, `metadata.json`.
- **Safety (enforced):** read-only — never edits source files; refuses protected run paths (`*.pine`/`parity`/`MTC_V2`/`.git`); redacts secret-looking tokens before persisting. Never send `.env`, API keys, broker/exchange/wallet secrets, or whole-repo dumps. Board **consensus is NOT trading approval or promotion evidence** — humans decide; the board only informs.
- Provider failure is non-fatal: workers support `prov` / `prov:model` fallback, a failed call is captured and the run continues. Full decision record: `MTC_COMMAND_CENTER\11_TRIAGE\FUSION\FINAL_FUSION_CONSOLIDATED_RECOMMENDATION.md`.
