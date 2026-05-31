# Claude Audit Prompt

You are auditing one proposed feature for `MTC V2`.

## Goal
Assess whether this feature is architecturally worth implementing or if it mostly adds code bloat / semantic risk.

## Feature
`L18c Pending Gate Release`

Meaning:
- Raw signal arrives on bar `N`
- Entry is blocked by one or more gates
- Instead of discarding the signal immediately, system keeps one pending same-side candidate for a short timeout
- If selected gates pass on a later bar and no cancel condition happened, entry is released on that later bar

## Important Constraints
- Do **not** redesign architecture
- Must preserve `03_DOCS/MTC_V2_ARCHITECTURE.md`
- Producer contract stays pulse/event-style
- Gate contract stays stateless per-bar evaluation
- New behavior, if accepted, must live as an optional transform after gates and before entry decision
- Pine and Python must keep identical state semantics
- Default must stay `OFF`

## Proposed Minimal Spec
- New optional transform: `L18c Pending Gate Release`
- Suggested config:
  - `use_pending_gate_release`
  - `pending_gate_release_timeout_bars`
  - `pending_gate_release_cancel_on_opposite_raw`
  - `pending_gate_release_scope`
- First-scope recommendation:
  - allow only `activity_only` gates:
    - volume
    - adx
    - chop
    - momentum
    - session
- Exclude in first version:
  - MA filter
  - HTF trend
  - MACD cross
  - candle pattern
  - level proximity

## Read Only These Files
1. `03_DOCS/MTC_V2_ARCHITECTURE.md`
   - sections 4, 5, 6, 8, 19, 20
2. `01_PINE/MTC_V2.pine`
   - raw signal / gate / confirm / deferred flip flow
3. `00_PYTHON/mtc_v2/signals/supertrend.py`
4. `00_PYTHON/mtc_v2/core/gates.py`
5. `00_PYTHON/mtc_v2/core/runner.py`
6. `03_DOCS/HANDOFF.md`

## Output Format
Reply in **max 220 tokens**.

Use exactly these sections:
1. `Verdict`
2. `Critical Risks`
3. `Recommendation`

## What I Need
- Is this feature genuinely useful for the current system?
- Or does it mostly create semantic drift and code bloat?
- If useful, what is the **smallest safe version**?
- Mention only critical points. No long walkthrough.
