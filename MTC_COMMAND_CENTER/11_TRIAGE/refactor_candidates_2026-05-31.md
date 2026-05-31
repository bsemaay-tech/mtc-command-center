# Refactor Candidates - 2026-05-31

These are the two modules to split next, but only when a new feature or bug fix touches them.

## 1. `pipeline_reader.build_candidate_pipeline`

Why it is a candidate:
- It now mixes canonical registry rows, promoted-spec rows, early candidates, and broader discovery ledgers in one large function.
- The current function is still readable, but it is carrying too many joins and row-shaping responsibilities.

Suggested extraction seams:
- promoted strategy row builder
- promoted producer-spec row builder
- early candidate row builder
- discovery-ledger row builder
- directional research / parity / paper-trade enrichment helpers

## 2. `audit_reader.py`

Why it is a candidate:
- It is still heavily procedural and now carries source loading, merge logic, split analysis, eligibility logic, and explanation builders in one module.
- The recent source-record merge made the module even more important to reason about carefully.

Suggested extraction seams:
- source index loader
- merge policy helper
- eligibility / blocked-reason engine
- source-quality engine
- explanation formatter bundle

## Guardrail

Do not refactor either module just for style. Split them only when the next change needs one of these seams.
