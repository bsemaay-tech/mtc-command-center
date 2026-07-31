# Architecture Decision Records

This directory is the canonical ADR system for MTC Command Center. ADRs are append-only governance records: do not renumber or silently rewrite a decision after implementation begins. Use `Superseded` and link the replacement.

## Convention

- Filename: `ADR-NNNN-lowercase-title.md`.
- Numbering: four digits, sequential; the next available number after this package is ADR-0030.
- Allowed status: `Accepted`, `Proposed`, `Deferred`, `Rejected`, `Superseded`.
- `Accepted` records a supported architecture decision, not proof that code implements it.
- `Proposed` records a direction that still requires evidence or approval and blocks implementation of that decision area.
- Every expanded ADR must include context, alternatives, negative consequences, implications, validation, reversal conditions, open questions, and evidence.

See [ADR_INDEX.md](./ADR_INDEX.md) for the complete registry, dependencies, and roadmap prerequisites.

The 2026-07-17 trading-platform package extends the compact legacy ADRs without changing their status or meaning. No ADR authorizes runtime, testnet, paper, or live action by itself.
