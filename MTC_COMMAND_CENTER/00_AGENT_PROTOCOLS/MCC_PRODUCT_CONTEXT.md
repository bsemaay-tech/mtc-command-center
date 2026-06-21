# Product

## Register

product

## Users

A single expert operator (Barış) running an internal, read-only trading-strategy
research workspace — the MTC Strategy Intelligence Command Center (MCC dashboard).
Context: deep, focused desktop sessions reviewing backtest evidence, gate
evaluations, and strategy verdicts. The user is fluent in the domain (quant
backtesting: DSR, CPCV, BH-FDR, buy&hold/alpha, promotion gates) and reviews the
UI screenshot-by-screenshot, section-by-section. The job to be done: decide which
strategies are trustworthy and promotable, on the strength of sourced evidence —
without being misled by noise, stale data, or pretty-but-empty metrics.

## Product Purpose

Turn raw backtest + gate-evaluation output into a calm, legible verdict surface.
Each screen answers one question at a glance — "is this real, and is it
promotable?" — and lets the user drill from verdict → gates → evidence → run data
without losing the thread. Success = the user trusts the page enough to act on it,
because every number is sourced and every verdict is earned. Read-only by design;
runs and parameter freezes happen outside the UI.

## Brand Personality

**Precise · calm · expert.** Quiet authority over flash. Bloomberg-terminal
restraint, but with modern legibility and hierarchy. The interface conveys
confidence through accuracy and clarity, never decoration. Voice is exact and
unhedged: state what is known, label what is estimated, surface what is stale.
Skepticism is a feature — the page should make it easy to distrust a weak result.

## Anti-references

- **Cluttered legacy terminal** (primary). No wall of undifferentiated numbers,
  no MT4/old-Bloomberg density-without-hierarchy. Density is allowed only where it
  serves the scan; every dense block needs a clear visual spine.
- Generic SaaS dashboard: no hero-metric template, no gradient accents, no
  identical icon+heading+text card grids.
- Crypto/retail trading app: no neon glow, no gamified hype green/red, no casino
  energy.
- Consumer fintech (Robinhood-style): no playful rounding, confetti, or
  emotion-driven oversimplification of a research tool.

## Design Principles

1. **Earned trust over assertion.** Every verdict shows its source; every number
   carries provenance (real / estimated / stale). Never present a metric the page
   can't back.
2. **One question per screen.** Lead with the decision the user is here to make;
   let everything else recede into progressive drill-down (verdict → gates →
   evidence → runs).
3. **Hierarchy is the antidote to density.** This is a dense tool; legibility
   comes from a strong visual spine and rhythm, not from removing information.
4. **The tool disappears into the task.** Earned familiarity — standard
   affordances, consistent component vocabulary, no invented controls. Calm, not
   busy.
5. **Honest by default.** Stale, missing, and estimated states are first-class UI,
   not afterthoughts. Make it easy to see what NOT to trust.

## Accessibility & Inclusion

- Target WCAG 2.1 AA contrast on the dark theme: body text ≥4.5:1, large/bold
  text ≥3:1. Muted slate text must clear 4.5:1 against its panel, not just look
  elegant.
- State is never signaled by color alone (pass/fail/stale carry an icon, label, or
  shape as well) — colorblind-safe.
- Respect `prefers-reduced-motion`: all state transitions degrade to instant or
  crossfade.
- Single-operator internal tool, so locale/i18n is out of scope; correctness and
  legibility under long focused sessions are in scope.
