# AGENTS.md

> **REPO IDENTITY — read before anything.** This repository is **`C:\LAB\Tradingview_LAB_CLEAN`** (the live MTC Command Center). The sibling directory **`C:\LAB\tradingview-lab` is the FROZEN legacy repo — do NOT read its onboarding, run, or edit anything there.** If your entrypoint resolved under `C:\LAB\tradingview-lab\...`, stop and switch to `C:\LAB\Tradingview_LAB_CLEAN`. The canonical onboarding chain exists only in this repo under `MTC_COMMAND_CENTER\_AI_MEMORY\`.

Read this file first, then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Then read `MTC_COMMAND_CENTER\_AI_MEMORY\COMPONENT_ROUTER.md` and route to the appropriate component before loading any volatile memory (GLOBAL_HANDOFF, NEXT_STEPS, ACTIVE_FILES). `SESSION_LOG.md` is retired historical-only — never a cold-start file. Component-scoped tasks load the component's `_AI_MEMORY/` chain instead of root histories.
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
3. Repo hygiene/commit/push may begin only after the sequence: accepting G5 verdict, G6 if applicable, G7 handoff — only where task/user authorization permits — then proceed to the next approved task.
4. Gate 5 is the lead's independent cross-model audit of the implementer's work, not mere report review.

**Implementer responsibilities:** implementation + self-QA (Gates 3–4). Scope, acceptance, repair loop, and authorized Git sequencing belong to the lead. Implementer is explicitly forbidden from commit, push, merge, rebase, and destructive Git operations (`reset --hard`, `restore`, `clean -fdx`, `stash drop`, branch deletion, `push --force`).

**Cheap models (DeepSeek, Cline, Grok) are implementer-tier sub-delegation tools only.** They are never the lead. Fable and Gemini are advisory/non-gate reviewers — they may supplement but never replace a canonical Claude/Codex gate audit. Historical audits remain historical evidence under the policy then in force.

**If the required counterpart CLI/auth is unavailable:** the lead reports that concrete blocker and does not silently replace the counterpart with itself.

Hard safety gates remain unchanged: no Pine/parity/MTC/trading changes without explicit approval, no destructive Git, no secrets, no deployment/live action without explicit authorization.

## CANONICAL AUDIT ROSTER — Gate 5 and Gate 6 (MANDATORY)

Define once here; prompts may cross-reference but must include enough detail to be safely copy-pasted standalone.

### Claude auditor (G5 and G6)

- **Model:** `claude-opus-4-8` | **Effort:** `xhigh` — always, no exceptions.
- No Sonnet, no implicit/latest alias, no silent fallback.
- **If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives it.**
- Fresh independent session every audit round — never `--resume` or `--continue` from the implementer session.
- `--fallback-model` forbidden.
- Example CLI: `claude -p --model claude-opus-4-8 --effort xhigh --no-session-persistence`

### Codex auditor (G5 and G6)

- **Model:** `gpt-5.6-sol` — always, no implicit alias.
- **Effort `high`** for ordinary Gate 5 audits.
- **Effort `xhigh`** whenever ANY of these apply: Gate 6 security review; Pine/parity/MTC/trading/protected surface; architecture or cross-cutting change; re-audit after REQUEST_CHANGES or BLOCK.
- **If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives it.**
- Fresh independent session every audit round.
- Example CLI (ordinary G5): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c 'model_reasoning_effort="high"' "<audit prompt>"`
- Example CLI (G6/protected/re-audit): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c 'model_reasoning_effort="xhigh"' "<audit prompt>"`

### Audit session contract

Provide only: scope contract, plan (if any), actual diff/files, test evidence, required repo rules.
Never feed implementer session context or continue it. The lead still owns acceptance and must inspect actual repo state independently.
Audits are diff-first: unified diff by default; full files only for necessary context with stated reason. If payload too large, split scope; no summary substitutes actual diff.

### Zero-token preflight (before every audit)

```powershell
claude --help 2>&1 | Select-String -Pattern 'claude-opus-4-8|xhigh'
codex --version
```
Checks syntax/slug exposure, not entitlement. Launch failure on either = BLOCK.

### Verdict standards (all audit gates)

| Verdict | Meaning |
|---------|---------|
| **PASS** | Clean — no required changes. |
| **PASS-WITH-NITS** | Accepting — optional nits only; zero required repairs. Cannot contain a required repair — use REQUEST_CHANGES instead. |
| **REQUEST_CHANGES** | Non-accepting — contains at least one required repair. |
| **BLOCK** | Workflow cannot safely continue. |

### Repair loop bound

**Maximum 3 repair/re-audit rounds per task.** After the third non-accepting verdict (REQUEST_CHANGES or BLOCK), stop and report the blocker to Barış. Do not silently enter a fourth round.

### G1 prerequisite for G2

Gate 1 must be complete before Gate 2: objective, exact whitelist, acceptance criteria, safety/authorization, validation plan, contract path.

### Sequence after implementation

Accepting G5 verdict (PASS or PASS-WITH-NITS) → G6 if applicable → G7 handoff → then and only then authorized hygiene/commit/push. G7 must not require a future commit hash.



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

## Gate 7 write-back — scoped per COMPONENT_ROUTER.md

Component-scoped tasks: update the component's `_AI_MEMORY/CURRENT.md` + `NEXT_STEPS.md` (and optionally `DECISIONS.md`, `ACTIVE_FILES.md`). Do not touch root `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, or `ACTIVE_FILES.md`. `SESSION_LOG.md` is retired historical-only — do not read or write.

Cross-component tasks: update every affected component per the above, then add one concise coordination entry to root `GLOBAL_HANDOFF.md`.

Global/policy tasks (no single component owner): use root memory files as usual.

When writing a root GLOBAL_HANDOFF.md entry, prefix each section header with model name and date:
  Format: ## [MODEL_NAME] YYYY-MM-DD — Topic
  Example: ## Claude Sonnet 4.6 2026-06-01 — Transcript fix
Do NOT create per-model log files at repo root.

When adding tasks to any NEXT_STEPS.md (component or root), tag each task with which AI can execute it:
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
