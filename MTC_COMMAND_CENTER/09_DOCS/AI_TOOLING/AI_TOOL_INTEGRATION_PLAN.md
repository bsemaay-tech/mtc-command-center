# AI Tool Integration Plan (MTC Command Center)

**Owner:** Barış · **Drafted:** 2026-06-20 by Claude Opus 4.8 · **Status (2026-06-22):** **ALL Phases 1–5 COMPLETE.** Remaining = operator config only (wire n8n notify channel) + standing DEFER re-open triggers (LiteParse/Claude-Video/Taste-Skill) + parked watchlist items (Zapier, Supermemory/GBrain/Obsidian — repo-external, none now). Per-tool status in §5.

This is the actionable companion to
[`MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md`](MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md)
(the source backlog, written by a prior Codex session). It exists so that a future Claude /
Codex / other LLM session can pick up tool integration **without re-reading the whole chat**
and without breaking the existing repo structure.

Read order for any AI tool work:
1. `AGENTS.md` (root) → `_AI_MEMORY/START_HERE.md` → `_AI_MEMORY/AI_RULES.md`.
2. This file.
3. `CLAUDE_REVIEW_OF_CODEX_BACKLOG.md` (sibling) — Claude's disagreements with the backlog.
4. The source backlog itself for per-tool detail.

---

## 0. Hard rules (inherited, non-negotiable)

- **No installs / no integrations without explicit Barış approval.** This whole track is
  documentation + memory until approved tool-by-tool.
- Do not touch `*.pine`, `MTC_V2`, `parity`, registry schemas, or backtest/broker/execution
  logic for any tool work. (Enforced by the DeepSeek harness denylist; applies to humans too.)
- No secrets / `.env` / API keys printed or committed. Tools that need keys are pilot-gated.
- Preserve existing structure. **Do not create the parallel folders the source backlog
  assumes.** Use the path map in §1.

---

## 1. Path map — backlog's assumed paths → this repo's real paths

The source backlog was written against a generic layout. This repo is different. Use the
right column.

| Backlog assumes | Use instead (real) | Notes |
|---|---|---|
| `00_DOCS/AI_WORKFLOW/` | `MTC_COMMAND_CENTER/09_DOCS/AI_TOOLING/` | This folder. `09_DOCS/AI_WORKFLOW.md` already exists as a file. |
| `00_KNOWLEDGE_BASE/` | `MTC_COMMAND_CENTER/09_DOCS/` + `_AI_MEMORY/` | No separate KB. Research/decisions → `09_DOCS`; operational memory → `_AI_MEMORY`. Do **not** scaffold a new KB tree unless Barış asks. |
| `00_PLANS/active/PLAN.md` + `PLAN-REVIEW-LOG.md` | `04_SHARED/prompts/05_ai_workflow/` + `09_DOCS/ADR/` | Plan/review prompts already exist (see §2). ADRs already have a home. |
| `09_TOOLS/<tool>/` | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/` (analysis tooling) or a new top-level `09_TOOLS/` **only if Barış approves** | Most existing helper scripts live in `03_QUANTLENS/tools/`. |
| `09_AUTOMATION/n8n/` | new `09_AUTOMATION/` **only on approval** | Side-service, repo-external preferred. |
| `.claude/skills/mtc-grill-plan/` | extend `04_SHARED/prompts/05_ai_workflow/` | Adversarial-review prompts already exist; extend them, don't fork a skill. |
| `MODEL_ROUTING_POLICY.md` (new) | **already implemented** — see §3 | Do not duplicate. |
| `CODEX.md` (root, new) | `AGENTS.md` (root) is the shared contract | Codex reads `AGENTS.md`. A separate `CODEX.md` is optional, not required. |

---

## 2. What already exists (do not rebuild)

Before integrating any "workflow/pattern" tool, know these are already in the repo:

- **Cheaper-model delegation harness** — `_deepseek_driver/ds_agent.py` (+ `README.md`),
  `_AI_MEMORY/DEEPSEEK_DISPATCH.md`, and the mandated "TOKEN DISCIPLINE" section in
  `AGENTS.md`. This **is** the model-routing implementation the backlog's Part 6 asks to
  "create." It just gets forgotten — fix is a read-first reminder, not a new policy doc.
- **Adversarial plan / code review (Grill-Me-style)** — `04_SHARED/prompts/05_ai_workflow/`:
  `01_office_hours_scope_review.md`, `02_engineering_plan_review.md`,
  `04_adversarial_code_review.md`, `06_security_review.md`, `07_handoff_update.md`.
- **Backtest/optimization gate workflow** — `03_QUANTLENS/_user_guide/07_*` +
  `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`.
- **ADR home** — `09_DOCS/ADR/`. (Backlog's "draft ADR only until implemented" rule still applies.)
- **Caveman output-compression** — already active as a Claude Code *client plugin* in this
  environment (not a repo artifact). No repo integration needed.
- **Document skills** — `pdf` / `docx` / `pptx` / `xlsx` Anthropic skills are available in the
  Claude Code client; evaluate them before adding MarkItDown/LiteParse as repo dependencies.
- **Browser automation** — `Claude-in-Chrome` and `Claude_Preview` MCPs are already available;
  evaluate before adding Webwright/Playwright.

---

## 3. Model routing — already real, just enforce it

The backlog's Part 6 / C4 is **already implemented**. Action is *enforcement*, not creation:

- **Use the harness for bounded mechanical work** (single/few-file edits, schema/JSON edits,
  audit runs, script writing): write task JSON → `python _deepseek_driver/ds_agent.py
  --task <file>` → audit on real data yourself. See `_deepseek_driver/README.md`.
- **When to route cheap:** large summarization, broad research, repeated audit passes, long
  log summarization, draft critique, non-final classification.
- **When NOT to route cheap:** final architecture decisions, registry/schema migration
  approval, security-sensitive review, live-trading/broker logic, final user-facing verdicts.
- **Providers:** `deepseek` (primary), `grok`/`xai`, `openrouter` (`:free` = fallback). Keys
  via env only; never assume a key exists, never print one.

> If Barış wants a single canonical "routing policy" page, it should *link to* the harness
> README, not restate it — one source of truth.

---

## 4. Phased plan (gated)

Each phase needs Barış approval to start. "Acceptance" = what proves a phase done.

### Phase 1 — Durable instructions + memory (zero-dependency, safe now) — DONE 2026-06-21
- DONE: read-first reminders point to this folder + the harness.
- DONE (Barış-approved): added an **`AI TOOL AUTO-USE`** section to `AGENTS.md` and a pointer
  in `_AI_MEMORY/START_HERE.md` so every agent auto-uses the tools at their triggers
  (MarkItDown for binary docs, Graphify for impact questions, CodeBurn for cost/routing) —
  vendor-neutral, no per-tool `graphify install` skill registration.
- Acceptance MET: a fresh LLM session, reading only the read-first files, finds this plan, the
  backlog, the routing harness, AND the auto-use triggers without the user repeating anything.
- DONE 2026-06-21 (optional L2, **local-only**): a Claude Code `SessionStart` hook surfaces
  CodeBurn spend into context at each session start — `.claude/settings.json` +
  `.claude/hooks/codeburn_sessionstart.sh`. NOTE: `.claude/` is git-ignored (repo convention),
  so this hook is **per-machine, not committed/portable** — Claude Code only. The AGENTS.md
  `AI TOOL AUTO-USE` convention remains the portable, all-agent backbone. To rebuild on another
  machine, recreate those two files (script fails silent if `codeburn` is absent).

### Phase 2 — Knowledge consolidation (light) — SATISFIED (standing policy) 2026-06-22
- Keep tool decisions in `09_DOCS/AI_TOOLING/` (this folder), research notes in `09_DOCS`,
  operational state in `_AI_MEMORY`. **Do not build a new KB tree.**
- Acceptance MET: every pilot/decision since landed in `09_DOCS/AI_TOOLING/`, ops state in
  `_AI_MEMORY/NEXT_STEPS.md`; no new KB tree built. This is a standing convention, not a build
  task — nothing further to "complete."

### Phase 3 — Local tools (each pilot-gated, run §6 checklist FIRST) — COMPLETE 2026-06-21
Order, lowest-risk first: MarkItDown ✅DONE (KEEP+promoted) → LiteParse ⏸️DEFER (overlaps MarkItDown, no PDFs) → CodeBurn ✅DONE (KEEP) → Graphify ✅DONE (KEEP on-demand). All 2026-06-21.
- Acceptance per tool: §6 checklist green + a real-MTC-data A/B test recorded in
  `09_DOCS/AI_TOOLING/pilots/<tool>_pilot.md`.

### Phase 4 — Research / UI pilots (branch-isolated) — COMPLETE 2026-06-22
Claude-Video, Impeccable, Design-Extract, Taste-Skill. UI tools on `feature/ui-*` branches
only; **no data-contract / registry / backtest change**.
- Acceptance: visible improvement on one screen, no API/contract diff, no console errors.
- DONE: **Impeccable** (Strategy Detail polish, merged to master).
- DONE 2026-06-22: **Design-Extract** (`designlang`) → KEEP on-demand for inspiration only
  (`pilots/design-extract_pilot.md`). Wrapper `03_QUANTLENS/tools/design_extract.ps1`.
- DONE 2026-06-22: **Taste-Skill** → DEFER/do-not-install — self-excludes dashboards/data
  tables; Impeccable already owns MTC's domain (`pilots/taste-skill_pilot.md`).
- DONE 2026-06-22: **Claude-Video** → DEFER/do-not-install — piloted on a real strategy video;
  frame value is content-gated (only an indicator-config screencast beats transcript), and the
  pipeline is reproducible with installed tools (`pilots/claude-video_pilot.md`).
- **→ Phase 4 COMPLETE.**

### Phase 5 — Side-service automation (repo-external preferred) — COMPLETE 2026-06-22
n8n watchdog for long backtests + Telegram/email notify. Required a stable progress/log file first.
- DONE 2026-06-22 (TDD): **stable emitter contract** shipped — `progress_emitter.py` +
  `run_emitter_supervisor.py` (engine-untouched; observes the runner's existing `run_status.json`)
  + strict `heartbeat_reader.py`. Design `RUN_PROGRESS_EMITTER_DESIGN_2026-06-22.md`.
- DONE 2026-06-22 (TDD): **watchdog** `run_watchdog.py` — one-shot poll, derives
  running/stalled/dead/done/failed, fires one notification per alert transition (de-duped), local
  log always + opt-in webhook. n8n workflow `03_QUANTLENS/tools/n8n/mtc_backtest_watchdog.workflow.json`;
  ops `PHASE5_WATCHDOG_OPS.md` (n8n or Windows Task Scheduler).
- Acceptance MET: a finished/failed/stalled run pushes a notification without an agent staying
  open. Tools tests 22 passed; API suite 86 passed. **→ Phase 5 COMPLETE.**
- Operator action (config, not code): wire the notify node to a real Telegram/Email/Slack channel
  and activate the schedule (no outward send happens until a webhook URL is configured).

---

## 5. Per-tool quick reference (decision · benefit · risk · next action · acceptance)

Decisions below are **Claude's adjusted** view; where they differ from the source backlog,
the reason is in `CLAUDE_REVIEW_OF_CODEX_BACKLOG.md`.

| Tool | Decision (adjusted) | Next action | Acceptance / gate |
|---|---|---|---|
| CLAUDE.md/AGENTS.md/CODEX.md rules | **DONE** — AGENTS.md has TOKEN DISCIPLINE (DeepSeek routing) + AI TOOL AUTO-USE (MarkItDown/Graphify/CodeBurn + long-backtest→watchdog); START_HERE points here. | None — extend only as new tools land. | MET — read-first files link here + harness. |
| MTC Grill Plan | Already present as prompt library. | Extend `05_ai_workflow/`. | No new parallel skill folder. |
| Codex read-only review | Already present (`04_adversarial_code_review.md`). | Use as-is. | Used on high-risk diffs. |
| Model routing / DeepSeek | **Already implemented** (`_deepseek_driver`). | Enforce, don't recreate. | Harness used for mechanical work. |
| MarkItDown | **DONE 2026-06-21** — promoted, KEEP for XLSX/Office batch ingestion (PDF value deferred, no PDFs in repo). | Committed wrapper `03_QUANTLENS/tools/markitdown_ingest.py` (py3.13 git-ignored venv). | PASS — see `pilots/markitdown_pilot.md`. |
| LiteParse | **DEFER 2026-06-21** — piloted; ties MarkItDown on text PDF, overlaps it; real edge (scanned-PDF OCR+spatial) untestable (0 PDFs in repo) + needs Tesseract/LibreOffice/ImageMagick. | Re-A/B when a real scanned strategy PDF lands. | NOT MET (blocked) — see `pilots/liteparse_pilot.md`. |
| CodeBurn | **DONE 2026-06-21** — KEEP (v0.9.12 global npm). Finding: DeepSeek harness underused (Opus $563 + Codex $377 vs DeepSeek $2.44). | Periodic `codeburn status` at session boundaries. | PASS — see `pilots/codeburn_pilot.md`. |
| Graphify | **DONE 2026-06-21** — KEEP on-demand (`graphifyy` 0.8.44 via uv tool; local/keyless; graphs git-ignored; not auto/whole-repo). | Use for impact (`affected`/`explain`/`query`); `graphify install` skill-reg deferred. | PASS — see `pilots/graphify_pilot.md`. |
| Understand-Anything | **SKIP 2026-06-22** — superseded. Graphify was piloted and KEPT (local/keyless, accurate); the "one winner, not both" rule resolves to Graphify. | None — re-open only if Graphify proves insufficient on a real impact query. | Closed (Graphify won). |
| Caveman Light | Client plugin, already active. | No repo work. | n/a |
| ~~Headroom~~ | **DROPPED 2026-06-20** — MITM proxy risk, ~5% real saving. | None. | n/a |
| Claude-Video | **DEFER 2026-06-22** — piloted on a real video; frames add ~nothing on animated/price-action content (no on-screen settings); value only on indicator-config screencasts; tool unnecessary (pipeline reproducible). | On-demand manual pipeline (yt-dlp+ffmpeg+captions) only when a video shows real platform UI. | DEFER — see `pilots/claude-video_pilot.md`. |
| ~~NotebookLM-py~~ | **DROPPED 2026-06-20** — unofficial API, fragile. | None. | n/a |
| Impeccable | **DONE** — UI critique/polish skill, in use (Strategy Detail). | `feature/ui-impeccable-pilot` (merged). | UI-only diff. |
| Design-Extract (`designlang`) | **DONE 2026-06-22** — KEEP on-demand for inspiration (not copy). | `pilots/design-extract_pilot.md`; wrapper `tools/design_extract.ps1`. | Tool PASS; dashboard apply deferred. |
| Taste-Skill | **DEFER 2026-06-22** — do-not-install; self-excludes dashboards, overlaps Impeccable. | `pilots/taste-skill_pilot.md`. | NOT MET (out of scope). |
| ~~Webwright / Playwright~~ | **DROPPED 2026-06-20** — redundant with existing browser MCPs. | Use Claude-in-Chrome / Preview. | n/a |
| n8n watchdog | **DONE 2026-06-22** — emitter contract + supervisor + `run_watchdog.py` + n8n workflow shipped (TDD). | Operator: wire notify node to a channel + activate schedule. | MET — `PHASE5_WATCHDOG_OPS.md`. |
| Zapier | Watchlist. | None now. | n/a |
| Supermemory / GBrain / Claude-Obsidian | Later / repo-external. | None. | n/a |
| MoneyPrinter / VoxCPM / Career-Ops / Odysseus / ECC / Higgsfield | **Do not integrate** (agreed). | None. | n/a |

### 5.1 DROPPED — do not integrate, do not pilot (decided 2026-06-20, Barış)

Removed from all phases. Rationale in `CLAUDE_REVIEW_OF_CODEX_BACKLOG.md` §2.

- **Headroom** — compression proxy sits between agent and LLM (sees all prompts/repo content); ~5% real saving. Not worth the security/accuracy risk.
- **NotebookLM-py** — wraps an unofficial, undocumented API; breaks whenever Google changes it.
- **Webwright** — duplicates the already-available `Claude-in-Chrome` / `Claude_Preview` MCPs.

Plus Codex's original do-not list stands: MoneyPrinterTurbo, VoxCPM, Career-Ops, Odysseus, ECC, Higgsfield.

---

## 6. Per-tool pre-integration checklist (run before any install)

```
[ ] repo maintained / not abandoned?
[ ] license compatible?
[ ] Windows compatible (this is a Windows 11 repo)?
[ ] Python/Node version requirement known?
[ ] local-only or external API? (external API => key handling => pilot-gate)
[ ] secrets/privacy risk? (anything that reads repo content or prompts => review)
[ ] output file size / git noise? (large artifacts => .gitignore decision up front)
[ ] does it modify files, or read-only?
[ ] overlaps an existing repo capability (§2)? if yes, justify the addition
[ ] conflicts with MTC denylist (pine/parity/MTC_V2/schemas)?
```

A tool that fails "Windows compatible", "secrets risk", or "overlaps existing" should not be
promoted to integration without an explicit Barış override.

---

## 7. Exact next command for the user

To start Phase 1 (safe, doc-only) in a fresh session, paste:

```
Read MTC_COMMAND_CENTER/09_DOCS/AI_TOOLING/AI_TOOL_INTEGRATION_PLAN.md and
CLAUDE_REVIEW_OF_CODEX_BACKLOG.md. Then propose the exact pointer lines to add to AGENTS.md
and _AI_MEMORY/START_HERE.md so future sessions auto-discover the AI-tool roadmap and the
DeepSeek routing harness. Do not install any tool. Show diffs for my approval first.
```
