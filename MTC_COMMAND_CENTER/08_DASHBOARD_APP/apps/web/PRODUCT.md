# PRODUCT.md — MTC Strategy Intelligence Command Center (web)

> Design north-star for the read-only research dashboard at `apps/web`.
> Register: **product** (design serves the task). The tool disappears into the work.

## What this is

A read-only command center for reviewing trading-strategy research candidates as they
move through a gated evaluation pipeline (Gate 1 intake → Gate 1B MTC feasibility →
Gate 2 backtest evidence → Gate 3 production readiness → paper trading). The flagship
surface is **Strategy Detail** (`renderIntelligence`): one strategy, every gate, all
evidence and provenance, on a single scrollable page with a sticky decision rail.

It renders a snapshot read model. It **never** writes, triggers runs, or executes trades.
Safety wording (RESEARCH ONLY / READ-ONLY / UNIVERSE MISMATCH / execution-disabled) is
load-bearing and must stay visible and unambiguous.

## Who uses it

A small number of expert operators (the strategy researcher and AI agents) who already
know the domain. They scan for state, trust, and the next decision — not for onboarding.
No first-timers, no mobile-primary, no marketing. Density is welcome; hand-holding is not.

## Personality

**Precise · calm · expert.** A reading instrument, not a billboard.

- High data density, low visual variance, minimal motion.
- Restraint over flourish. Color is state, never decoration.
- Every element earns its pixel; nothing competes for attention without a reason.

## Anti-reference

A **cluttered legacy terminal**: every field shouting at equal weight, accent color
sprayed for flavor, decorative stripes and chrome, no hierarchy, no breathing room.
If a change makes the page louder without adding meaning, it is wrong.

## Identity (committed — preserve)

Dark command-center theme. Teal/slate palette, JetBrains Mono for data/identifiers,
system sans for prose. See `DESIGN.md` for the concrete token system. This identity is
shipped and committed; refinement preserves it rather than re-theming.

## Success test

Would an expert operator trust this page at a glance and find the next decision without
hunting? Failure mode here is not "looks AI-made" — it is *strangeness without purpose*
and *uniform visual weight that buries the signal*.
