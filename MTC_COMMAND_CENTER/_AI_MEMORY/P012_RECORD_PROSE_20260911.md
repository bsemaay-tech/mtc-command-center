# P012 instrument-record prose correction

- Branch: `feature/p012-record-prose-20260911`
- Worktree: Lead-owned `C:/tmp/P012_RECORD_PROSE_20260911`
- Base: `e42fa192507d77e2d1765702a4a9f54e56ad793f`
- Source instrument SHA-256: `8620f499d7903f5ea801d99f6654f01546ad6638f7c85dad81d441209ff73fb8`
- Proposed instrument SHA-256: `5abb99abbdb9735e95ad1084c706a3c5326fb6bb134e48a79e9bb0992b68316a`

The defects were independently reproduced. `/status` points to the superseded addendum 15 row 36 pending-approval wording instead of the recorded OPEN01 selection at addendum 16 row 42. `/field_basis/price_tick` contradicts the already-approved v1.27 integer exception by claiming a mandatory 10-unit step above 100000. Only those two explanatory strings change.

Initial apply is exactly these four paths:

1. `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json`
2. `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json.sha256`
3. `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json`
4. `MTC_COMMAND_CENTER/_AI_MEMORY/P012_RECORD_PROSE_20260911.md`

Before applying anything beyond those four, separately enumerate and remeasure these dependent identities:

- Probe: `tests/corrected_vnext/probes/{PROBE-P012-01-A,PROBE-P012-01-B,PROBE-P012-02-A,PROBE-P012-04-A,PROBE-P012-05-A,PROBE-P012-05-B,PROBE-P012-06-A,PROBE-P012-07-A,PROBE-P012-08-A}/kernel/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json`, each sidecar, and each `modified_tree_manifest.json`.
- Catalog: `tests/corrected_vnext/contracts/scenario_catalog.json`.
- Anchor: `tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json`, `implementation_anchor.json`, and `implementation_anchor.json.sha256`.
- Receipt: `tests/corrected_vnext/contracts/semantic_coverage_review.json`.

There is no core Python, numeric, behavioral, or semantic change. Original baseline34 and R34 acceptance are preserved. The current unit remains NONACCEPTED. Lead owns all writes; no other workers write source.

NEXT ACTION: commit core-only candidate then regenerate dependent probe/evidence identities.

WAITING FOR OWNER: Nothing for existing corrective authority, later genuine Section16 ratification remains separate.
