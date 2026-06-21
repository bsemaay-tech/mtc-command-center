# Claude's Review of the Codex AI-Tools Backlog

**Author:** Claude Opus 4.8 · **Date:** 2026-06-20 · **Reviews:**
[`MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md`](MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md)

The source backlog (a prior Codex/ChatGPT session) is a solid survey and its risk instincts
are mostly right. The problem is not the tool research — it's that the **embedded Claude Code
prompt was written against a generic repo layout and assumes things this repo already has or
does not have.** Acting on it verbatim would create a parallel architecture the prompt itself
forbids. Below is where I disagree, what I'd drop, and what I'd re-rank.

## TL;DR

- ✅ Agree with the whole **"Grup I — do not integrate"** list (MoneyPrinter, VoxCPM,
  Career-Ops, Odysseus, ECC, Higgsfield). Off-mission, correctly rejected.
- ⚠️ The backlog over-uses **"Hemen entegre et" (integrate now)** — 9 of its tools. Only the
  *documentation/workflow* items are truly safe-now. Every item with a `pip`/`npm` install is
  pilot-gated and was labelled too eagerly.
- ❌ Three things should be **rejected or downgraded** beyond Codex's call: **Headroom**,
  **NotebookLM-py**, **Webwright**.
- 🔁 Several "integrate now" items **already exist** in the repo; the correct action is *use /
  enforce*, not *build*.

---

## 1. Where the backlog contradicts repo reality (highest priority)

### 1.1 Model routing is already built — don't create a new policy doc
Backlog **Part 6 / C4** says "create `MODEL_ROUTING_POLICY.md`" and treats cheaper-model
delegation as missing. It is not. The repo ships `_deepseek_driver/ds_agent.py` (+ README),
`_AI_MEMORY/DEEPSEEK_DISPATCH.md`, and a mandatory "TOKEN DISCIPLINE" section in `AGENTS.md`
with a hard-rail sandbox. Creating a second policy file invites drift and a contradicting
source of truth. **Fix the real problem** (agents forget it) with a read-first pointer, not a
duplicate document.

### 1.2 The assumed folder tree does not exist
`00_DOCS`, `00_KNOWLEDGE_BASE`, `09_TOOLS`, `09_AUTOMATION`, `00_PLANS` — none exist. Real
homes are `09_DOCS/` (+ `ADR/`), `04_SHARED/prompts/05_ai_workflow/`, `_AI_MEMORY/`. Following
the prompt's "Önerilen aksiyon" paths literally would scatter new top-level folders across a
repo whose own instructions say *"Do not invent a parallel architecture."* Path map is in
`AI_TOOL_INTEGRATION_PLAN.md` §1.

### 1.3 "MTC Grill Plan" already exists as a prompt library
Backlog A2/C1 wants a new `.claude/skills/mtc-grill-plan/SKILL.md`. The repo already has
adversarial scope/plan/code/security review prompts in `04_SHARED/prompts/05_ai_workflow/`
(`01`, `02`, `04`, `06`). Extend those. A forked skill folder would compete with the existing
library and the AGENTS.md gate workflow.

### 1.4 Caveman / document-skills / browser-automation are already available client-side
Caveman is already an active Claude Code plugin (this very session). `pdf/docx/pptx/xlsx`
skills and `Claude-in-Chrome` / `Claude_Preview` MCPs are available in the client. The backlog
treats MarkItDown, Webwright, and Caveman as fresh integrations without checking what the agent
runtime already provides. Evaluate the built-ins **first**.

---

## 2. Tools to reject or downgrade (beyond Codex's list)

### 2.1 Headroom — reject for MTC (backlog says "controlled pilot")
Headroom inserts a **compression proxy between the agent and the LLM**, so it sees every prompt
and tool output — including repo source, paths, and anything adjacent to secrets. Codex's own
note records the real saving as **~4.8% median**, not the headline 60–95%. For a repo with
explicit broker/credential and parity-protection rules, a man-in-the-middle proxy is high
security/accuracy risk for a single-digit token saving. Not worth a pilot except a fully
isolated, log-only experiment. → moved toward **do-not** in the plan.

### 2.2 NotebookLM-py — skip (backlog says "controlled research pilot")
It wraps an **unofficial, undocumented** NotebookLM API. Codex flags the fragility but still
green-lights a pilot. Anything built on an unofficial API becomes a maintenance trap the moment
Google changes it. Skip until/unless an official API exists. → **skip**.

### 2.3 Webwright — defer (backlog says "controlled pilot")
Browser automation for dashboard E2E is reasonable, but it **duplicates** the already-available
`Claude-in-Chrome` and `Claude_Preview` MCPs and would add a second Playwright stack to
maintain. Use the existing MCP tooling for dashboard QA first; only add Webwright/Playwright if
those prove insufficient. → **defer**.

---

## 3. Re-ranking: "integrate now" is too generous

The backlog's Group A marks 9 tools "Hemen entegre et." Realistically only the **zero-
dependency, no-install** items are safe now:

- Safe now (docs/memory/workflow): repo rules (exist), adversarial review (exists), model
  routing (exists), this knowledge-consolidation step. → these are the only true "now."
- **Everything that installs software** (Graphify, MarkItDown, LiteParse, CodeBurn) must pass
  the §6 pre-integration checklist (Windows compat, license, secrets, git-noise) **before**
  being called "integrated." Labelling them "now" understates the gate.

**Graphify specifically**: downgrade from "immediate architecture layer" to **pilot**. The repo
already has strong structured memory (`_AI_MEMORY`, registries, `09_DOCS`, ADRs). A knowledge
graph is a nice-to-have, not an urgent gap, and the "huge token savings" claim is unproven on
Windows. Pilot it against one concrete impact-analysis question and decide on `graph.json`
git-noise before committing anything.

---

## 4. Where I agree with Codex

- The entire **do-not-integrate** group is correct and well-reasoned (off-mission, ethics/
  voice-cloning risk, context-pollution from giant skill packs like ECC).
- The **"draft ADR only; accepted ADR after implementation + audit + approval"** rule is exactly
  right and matches this repo's discipline.
- **Memory-service tools** (Supermemory, GBrain, Claude-Obsidian) correctly deferred — a second
  memory system would conflict with `_AI_MEMORY`.
- The **per-tool research checklist** is good and is carried into the plan (§6).
- The **side-service framing for n8n** (don't embed in core; needs a real log emitter) is right.

---

## 5. Net recommendation

Treat the source backlog as a **research catalog**, not an executable plan. Execute through
`AI_TOOL_INTEGRATION_PLAN.md` instead, which (a) uses real repo paths, (b) does not duplicate
the existing routing harness or review prompts, (c) pilot-gates every install, and (d) rejects
Headroom/NotebookLM-py/Webwright. Nothing here gets installed without explicit Barış approval,
tool by tool.
