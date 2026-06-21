# Pilot — Impeccable (frontend design skill + anti-pattern detector)

**Date:** 2026-06-21 · **By:** Claude Opus 4.8 · **Branch:** `feature/ui-impeccable-pilot` · **Verdict:** ✅ KEEP — useful deterministic UI auditor; skill mode deferred.

## What / install
Multi-tool design system for AI agents. Two faces:
- **Standalone detector** — `npx impeccable detect <file|dir|url>`: 44 deterministic anti-pattern rules, local, **no API key, no LLM**. Read-only (reports; does not edit).
- **Agent skill** — `npx impeccable install` writes slash-commands (`/impeccable craft|audit|critique|polish|typeset|layout|…`) into the AI tool's config. Modifies files via the agent.
- Other commands: `ignores`, `help`, `link`, `update`, `check`. (No `--help` body; run bare `impeccable` for usage.)

## How piloted (safe, branch-isolated)
1. **Blocker found first:** the dashboard web files (`app.js`/`styles.css`/`index.html`) carried ~2700 lines of *uncommitted prior work* vs HEAD. Editing on top would violate AGENTS.md PARALLEL AGENT SAFETY. → Per Barış: created `feature/ui-impeccable-pilot` and committed the current web state as a **baseline snapshot** (commit `18b6a47`) before any edit. Master untouched.
2. Ran `npx impeccable detect` on `08_DASHBOARD_APP/apps/web` (read-only).

## Findings (only 2 — CSS is already clean)
Both = "thick colored border on one side of a card — the most recognizable tell of AI-generated UIs":
- `styles.css:402` `.constraint-notice` → `border-left: 4px solid var(--red)`
- `styles.css:848` `.toast` → `border-left: 3px solid var(--teal)`

## Fix applied (UI-only, semantics preserved)
- `.constraint-notice`: removed the 4px red left bar. It already has a full `1px` red border + red-tinted background + red icon, so identity is intact; the bar was redundant.
- `.toast`: replaced the 3px teal left bar with a uniform `1px solid var(--border)` (the codebase's standard panel border token). Teal identity stays via the existing teal `.tt` label + box-shadow.

## Acceptance — PASS
- `npx impeccable detect …` re-run → **0 anti-patterns** (was 2).
- Diff = exactly 2 lines, CSS-only. No `app.js`/`index.html` change, no data-contract/registry/backtest/API change. Token `var(--border)` matches existing panels (consistency).

## Caveats
- Detector is deterministic and narrow (44 rules) — it found little because the CSS is already disciplined. The richer value (`craft`/`critique`/`polish`) lives in the **agent skill**, which needs `npx impeccable install` + a Claude Code reload to expose the slash-commands. Deferred (skill registration is a separate decision, like Graphify's).
- Pilot scope was the detector loop only; no broad restyle (would be a huge, risky diff on a 2366-line stylesheet).

## Next (optional, approval-gated)
- Install the agent skill (`npx impeccable install`, local `.claude`) for `critique`/`polish` passes on Strategy Detail (matches the open UI taste/UX refinement want).
- Then evaluate Taste-Skill (`npx skills add …`) and Design-Extract (inspiration from TradingView/Linear) as the next two Phase-4 tools.
- Merge decision for `feature/ui-impeccable-pilot` is Barış's (depends on what happens with the larger uncommitted dashboard changeset on master).
