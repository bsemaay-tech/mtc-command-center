# Claude Handoff

- Version: `2026-04-23-v2`
- Scope: `MTC V2` only
- Source of truth:
  - `03_DOCS/MTC_V2_ARCHITECTURE.md`
  - `03_DOCS/HANDOFF.md`
  - `03_DOCS/RUNBOOK.md`

## Current State
- `case_110`, `case_111`, `case_134`, `case_153`, `case_154`: all PineTS/Python PASS as of 2026-05-29.
- Three Python runner bugs fixed: exit reason label map, L18 one-shot fire reset, deferred flip post-L21, L18 gate condition (gate_results not gated.short).
- `case_134` / `case_153`: need fresh TW re-export (stale 2026-04-14 exports).

## Active Backlog
- `case_134` / `case_153` fresh TW re-export (PineTS/Python already PASS)
- `case_124` / `case_125` re-export parity
- `L22 Candle Pattern Lookback` new export parity
- `case_160` / `case_161` missing exports

## Current Audit Request
- Topic: optional delayed entry after a gate-blocked signal
- Proposed owner: new signal transform, not producer/gate rewrite
- Prompt file: `04_AUDIT/CLAUDE_PENDING_GATE_RELEASE_AUDIT_v2.md`
