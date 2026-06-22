# Pilot — Taste-Skill (`leonxlnx/taste-skill`)

**Date:** 2026-06-22 · **By:** Claude Opus 4.8 · **Branch:** `feature/ui-taste-skill` ·
**Verdict:** ⏸️ DEFER / DO-NOT-INSTALL for the MTC dashboard. The tool **self-excludes our
domain**, and **Impeccable already covers it**. Mine its ideas as reference only.

## What
`Leonxlnx/taste-skill` — "The Anti-Slop Frontend Framework for AI Agents." Portable agent skill
set (Claude Code / Codex / Cursor), install via `npx skills add <repo>`. MIT, very active
(48.7k★, 131 commits, v2 rewrite in progress). Skills: `taste-skill`, `minimalist-skill`,
`brutalist-skill`, `soft-skill`, `redesign-skill`, `image-to-code`, `brandkit`, etc.
Core concept: 3 dials — `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY` — plus an
"anti-default discipline" (no AI-purple gradients, no centered-hero-on-mesh, no Inter+slate-900).

## Evaluation method
Shallow-cloned to `C:\tmp\taste-skill` (read-only, non-repo) and read
`skills/taste-skill/SKILL.md` (1206 lines). **Did not install** into `.claude/skills` — no point
running third-party skill content for a domain it disclaims (see below).

## Decisive finding — scope mismatch
The skill's own header states its scope:
> "Landing pages, portfolios, and redesigns. **Not dashboards, not data tables, not multi-step
> product UI.**"
Its `name`/`description` are literally `design-taste-frontend ... for landing pages, portfolios,
and redesigns`. MTC's flagship surfaces (Strategy Detail, Research Lab, scorecards, gate tables)
are **data-dense dashboards / multi-step product UI** — exactly the cases taste-skill excludes.

## Overlap with Impeccable (the backlog's actual question)
Backlog asked: *"Impeccable yeterli mi önce görülmeli."* Answer: **yes.**
- **Impeccable** (already KEEP, in use for Strategy Detail) explicitly covers *dashboards,
  product UI, app shells, forms, settings, data tables, information architecture, cognitive
  load* — MTC's domain.
- **Taste-skill** targets the inverse (marketing/landing/portfolio aesthetics) and disclaims
  dashboards.
So for MTC they don't compete — Impeccable is the correct tool, taste-skill is out of scope.

## §6 checklist
- [x] repo maintained — yes (48.7k★, active, v2 WIP)
- [x] license — MIT
- [x] Windows / install — `npx skills add` (Node); would write into `.claude/skills` (git-ignored)
- [x] local-only — yes (skill text; no API key)
- [x] read-only to repo — evaluated via clone in `C:\tmp`; nothing written to MTC tree
- [!] **overlaps existing** — Impeccable already owns the dashboard/product-UI domain
- [!] **scope mismatch** — tool explicitly NOT for dashboards/data tables (our core surfaces)
- [x] denylist — no pine/parity/MTC_V2/schema touch

## Acceptance — NOT MET (out of scope)
Phase-4 gate is a "visible improvement on one screen." Taste-skill disclaims our screen type and
duplicates Impeccable's covered domain → not promoted (per §6 "overlaps existing / scope
mismatch" without override).

## Decision
- **DEFER / do-not-install.** Keep **Impeccable** as the single UI-craft skill for MTC.
- **Reusable idea (not the tool):** borrow its *anti-default discipline* list and the
  variance/motion/density dial framing as a mental checklist when running Impeccable on MTC —
  but do not add the skill.
- **Re-open only if** MTC ever ships a public marketing/landing page (then taste-skill's domain
  applies and it can be A/B'd against Impeccable on that page).
- Clone at `C:\tmp\taste-skill` is ephemeral/deletable.
