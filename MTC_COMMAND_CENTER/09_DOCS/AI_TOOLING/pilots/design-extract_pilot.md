# Pilot — Design-Extract (`designlang`)

**Date:** 2026-06-22 · **By:** Claude Opus 4.8 · **Branch:** `feature/ui-design-extract` ·
**Verdict:** ✅ KEEP on-demand for **design inspiration only** (not auto, not copy). Do not apply
to the dashboard in this pilot — any dashboard change is a separate, scoped UI task.

## What / install
`Manavarya09/design-extract`, npm package **`designlang`** (v12.21.0). MIT, Node 20+ (ran Node
24). Playwright/Chromium headless; **`--system-chrome`** skips the 150 MB Playwright download.
No API key required (optional `--smart` LLM fallback supports OPENAI/ANTHROPIC/ATLASCLOUD keys).
- Run (ephemeral, **outputs kept out of repo**): `npx -y designlang -o C:\tmp\design_extract_out
  -n linear --dark https://linear.app --system-chrome`.
- Output: 35+ files — DTCG design tokens (JSON), Tailwind config, CSS vars, Figma variables,
  agent-native `DESIGN.md` (YAML front matter), `AGENT.md` system prompt, brand `voice.json`,
  motion presets (Framer/GSAP/WAAPI/CSS), dark-mode pairing, visual-DNA, intent/section roles.

## Real test — Linear (dark)
Extraction produced accurate, usable output: bg `#08090a`, brand `#5e6ad2`, `Inter Variable`,
shadow/radii/gradient/motion tokens, plus a clean agent `DESIGN.md`. Token JSON is DTCG-valid.

## Findings (honest)
- **Post-step crash:** all 35 artifacts wrote ✓, then a wrap-up step threw
  `The "string" argument must be ... Received undefined` → **exit 1**. Cosmetic (final
  report/summary writer); outputs are complete and usable. Re-check on a newer version.
- **Samples whatever the URL renders:** `linear.app` is a **marketing landing**, not the Linear
  *app* dashboard → output is landing-centric (intent "landing", confidence 0.31; messy
  `spacing.scale [1,39,47,...]`; reading-order = hero/testimonials/nav). For dashboard
  data-density inspiration, point it at an actual authenticated app screen (`--cookie-file`),
  not the homepage.
- **Git-noise:** 35+ files per run. Keep all output in `C:\tmp` (or a git-ignored scratch dir).
  Only curated insight notes belong in the repo.
- **Backlog rule holds:** *inspiration, not copy.* Never paste a marketing-site palette into the
  MTC data dashboard — mine it for ideas (color relationships, motion timing, type scale).

## §6 checklist
- [x] repo maintained — yes (v12.21.0, 273+ commits, active 2026)
- [x] license — MIT
- [x] Windows — yes (Node 20+); `--system-chrome` avoids the 150 MB browser download
- [x] Node req — 20+ (ran 24)
- [x] local-only key — none required (optional `--smart` LLM = pilot-gated if ever used)
- [~] outward action — headless-browses **external public** sites; fine for public design refs,
      use `--cookie-file` carefully for authed targets (never commit cookies)
- [!] git-noise — 35+ files/run → outputs must stay out of repo (`C:\tmp`)
- [x] read-only to repo — does not modify MTC files; writes only to `-o` dir
- [!] **overlaps existing** — Claude-in-Chrome / Claude_Preview MCPs + our own
      `08_DASHBOARD_APP/apps/web/DESIGN.md`. **Differentiator:** token/system *extraction*
      (DTCG/Tailwind/Figma/motion) the MCPs don't produce. Complement, not replacement.
- [x] denylist — no pine/parity/MTC_V2/schema touch (UI-inspiration only)

## Acceptance (Phase 4 gate) — tool PASS; dashboard improvement DEFERRED
Phase 4 gate = "visible improvement on one screen, no API/contract diff, no console errors."
This pilot **evaluated the tool only** (no dashboard edit) → tool works + adds value, but the
"visible improvement" half is intentionally deferred to a scoped follow-up UI task so we don't
copy a marketing-site look into a data dashboard.

## Decision
- **KEEP on-demand** (like Graphify): run `designlang ... --system-chrome` against a real
  product/app screen when seeking color/type/motion inspiration; outputs to `C:\tmp`.
- **Next (optional, approval-gated):** target an actual dashboard-style app screen
  (Grafana/Datadog/Linear-app) and distill 3–5 concrete, *adapted* ideas into one scoped
  `feature/ui-*` polish task with screenshot before/after.
- Pilot outputs at `C:\tmp\design_extract_out` are ephemeral/deletable.
