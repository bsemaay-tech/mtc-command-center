# DESIGN.md — Strategy Intelligence Command Center

Documents the **as-built** visual system in `styles.css` / `app.js`. Source of truth for
refinement: change how the UI *looks*, never what data `strategyModel` reads. Register:
**product**.

## Color tokens (`:root`)

Dark, slate-based. Single accent (teal) plus a fixed semantic state ramp.

| Role | Token | Value |
|------|-------|-------|
| App bg | `--bg` | `#07090E` |
| Surfaces | `--panel` `--panel-2` `--panel-3` | `#0E131C` / `#121924` / `#0A0D15` |
| Hover surface | `--panel-hover` | `#1A2333` |
| Borders | `--border` `--border-soft` `--border-strong` | `#1e2733` / `rgba(148,163,184,.12)` / `#2b3645` |
| Accent | `--teal` `--teal-dim` | `#2dd4bf` / `#14b8a6` |
| State | `--emerald` `--amber` `--red` `--blue` `--purple` | success / warn / fail / info / reuse |
| Ink ramp | `--text` `--text-strong` `--muted` `--faint` `--faintest` | `#e2e8f0` → `#475569` |

**Color = state, not decoration.** Teal = accent / selection / read-only mode. Emerald =
pass/OK. Amber = warn/review/locked-soft. Red = fail/blocking/danger. Purple = AI-reuse.
Gray ramp carries all neutral hierarchy.

### Known contrast risk
`--faint` (#64748b) on `--panel-3` (#0A0D15) is used for many labels/notes; near AA for
small text. `--faintest` (#475569) on dark is sub-AA — acceptable only for non-essential
decoration, never for content the operator must read.

## Type

- Families: `--sans` (system stack) for prose/labels/UI; `--mono` (JetBrains Mono) for
  data, scores, IDs, paths. One sans, one mono — correct for product register.
- **Fixed px scale, not fluid.** Body 14px. Steps in use: 8.5 / 9 / 9.5 / 10 / 10.5 / 11 /
  11.5 / 12 / 12.5 / 13 / 14 / 15 / 16 / 17 / 20 / 26px.
- ⚠️ The scale is **over-crowded at the small end** (8.5–10.5 has six near-identical
  steps). Refinement should consolidate, not add steps.
- Uppercase + letter-spacing (0.06–0.14em) marks labels/eyebrows/captions.

## Spacing & radius

- Radius: `--radius` 10px, `--radius-sm` 7px.
- Panels: `padding: 18px 20px; margin-bottom: 20px`.
- Section rhythm: `.si-main` stacks sections with `gap: 22px`.
- Inline `style="margin-top:18px"` repeats on `h4.section-title` throughout `app.js` —
  spacing is partly hard-coded inline rather than tokenized.

## Layout

- `.si-layout`: 2-col grid, `minmax(0,1fr) 320px`, gap 22px. Rail (`.si-rail`) sticky at
  `top:88px`. Collapses to 1 col < 1200px; sidebar hidden < 860px.
- Strategy Detail order: hero → constraint notice → gate summary → 7 numbered sections
  (Overview, Gate 1/1B, Verdict, Evidence, Explorer, Paper Readiness, Advanced) → rail.

## Components (as-built vocabulary)

`.panel` · `.banner` (info/warn/danger) · `.gate-card` · `.info-card` / `.info-grid` ·
`.rule-block` / `.rule-grid` · `.subscore` · `.grid-table` / `.matrix` · `.badge`
(ok/bad/warn/teal/purple/neutral) · `.chip` · `.rail-card` · `.workflow-card` ·
`details.acc` (collapsed raw JSON) · `.empty-state`.

State coverage is good for badges/chips/buttons (hover/active/disabled present). Motion is
minimal (.15s transitions, one pulse dot, one toast slide) — correct for the register.

## Conventions to preserve

1. Read-only identity + safety wording are load-bearing — keep visible.
2. Dark teal/slate identity is committed — refine, don't re-theme.
3. Empty/missing data is first-class: `missing()` / `emptyState()` / `value-muted` carry
   "not extracted / artifact missing" states everywhere. Keep them honest and quiet.

## Known design-debt (refinement backlog)

- **Side-stripe accent**: `.gate-card .bar` is a 3px full-height left stripe — the classic
  AI side-stripe tell. Replace with full border-tint or badge-led emphasis.
- **Eyebrow + number on every section**: `sectionHead()` prints `Section N` eyebrow above
  all 7 headings — uniform AI scaffolding. Numbering is real (a pipeline order) but the
  per-section tracked eyebrow is noise.
- Over-dense small type scale (see Type).
- Hard-coded inline spacing scattered through `app.js`.
