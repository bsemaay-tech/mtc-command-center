# Changelog

All notable contract changes are recorded here. This package follows Semantic
Versioning. A field removal, required-field addition, enum narrowing/expansion
that an older fail-closed consumer cannot accept, or identity-preimage change is
a breaking change and requires a major version increment after v1.

## 0.1.0 — 2026-08-25

- Add snapshot-independent `SizingRequest` and orchestrator-bound
  `BoundSizingIntent` with exactly four normalized sizing methods.
- Add `OrderIntent`, `ExitIntent`, `StrategyPackage`, `AccountSnapshot`, risk,
  allocation, Guardian, trial, admission, lineage, freshness, evidence-window,
  reconciliation, and lifecycle-ledger record shapes.
- Add canonical candidate/package/evaluation/deployment/trial/run/family identity
  formulae and explicit environment-lineage exclusion.
- Add read-only simulator and Bridge consumer compatibility tests.
- Establish artifact-only installation and the v0 compatibility fence.
