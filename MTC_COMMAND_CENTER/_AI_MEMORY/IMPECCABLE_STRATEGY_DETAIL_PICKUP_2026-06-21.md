# PICKUP — Impeccable critique pass on Strategy Detail (2026-06-21)

**For the next Claude Code session (after restart).** The Impeccable agent skill was installed
this session but its slash-commands only load on a fresh start. Restart done → execute this.

## Context (don't re-derive)
- Branch: **`feature/ui-impeccable-pilot`** (already checked out). Stay on it. Do NOT touch master.
- master still holds ~2700 lines of uncommitted prior dashboard work — NOT yours to commit; leave it.
- Tools live: Impeccable skill (`.claude/skills/impeccable`, git-ignored) + a PostToolUse hook that
  auto-runs the UI anti-pattern check after every Edit/Write. CodeBurn SessionStart hook also live.
- Full pilot context: `09_DOCS/AI_TOOLING/pilots/impeccable_pilot.md` and `AI_TOOL_INTEGRATION_PLAN.md`.

## Goal
Taste/UX refinement of the **Strategy Detail** view (Barış's open want — see memory
`mcc-ui-review-state`). Hierarchy, clarity, spacing, typography. **UI only.**

## Where Strategy Detail lives
- View id `"intelligence"` → **`renderIntelligence(c)`** at `08_DASHBOARD_APP/apps/web/app.js:903`.
- Sub-sections: `gate1Section(m)` `app.js:1093`, `advancedSection(m)` `app.js:1339`,
  `strategyModel(id)` `app.js:401`. Styles in `apps/web/styles.css`.

## Steps
1. `/impeccable init` — let it write design context (commit that context file on the branch if it lands in-repo and isn't git-ignored).
2. `/impeccable critique` focused on the Strategy Detail / Strategy Intelligence view.
3. Apply only safe, high-value UI fixes (`/impeccable polish` / `typeset` / `layout`) — incremental, reviewable commits.
4. After each change: `npx impeccable detect 08_DASHBOARD_APP/apps/web` → expect 0; `node --check apps/web/app.js`; run the API tests if any JS-affecting change (`cd 08_DASHBOARD_APP/apps/api && PYTHONPATH=. python -m unittest discover tests`).

## Hard constraints
- UI/CSS/markup only. **No** change to data contracts, `read_model`/API shape, registry, scorecard
  semantics, backtest, Pine/MTC_V2/parity/broker/execution.
- `renderIntelligence` reads `strategyModel` fields — do not alter what data is read, only how it looks.
- Keep safety badges/wording (RESEARCH ONLY / UNIVERSE MISMATCH / execution-disabled) intact.
- Visual QA before claiming done (serve the dashboard / Preview), since the detector is narrow.
