# Gate A Queue C repair — owner-waiver acceptance

Date: 2026-08-03

## Disposition

**ACCEPTED** for source-candidate purposes at
`17402a58b7152be7367d10421a55d3e8cd35c7c5`, repairing frozen candidate
`5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002` through three linear repair commits.

This is not Queue D authorization, integration approval, artifact rebuild approval, a Gate A
execution pass, deployment approval, or permission for runtime, broker, or economic action.

## Owner waiver and exact scope

Barış explicitly waived the unavailable-Claude dependency on 2026-08-03 and directed continued
Codex/alternative-model implementation and audit. The repair cycle after `5a9bb922` changes exactly:

- `IBKR_PAPER_BRIDGE/bridge/app.py`
- `IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py`

The original cycle from common base `637307e83951ffe23e768ed8e50ddaf8712b0660` also contains the
pre-existing `IBKR_PAPER_BRIDGE/bridge/api/routes.py` change. No other product file is in scope.

## Repaired findings

1. Public `create_app()` now defaults `start_mode` to `None` and resolves an explicit argument before
   the real environment. Environment-selected credential-free DISARMED therefore reaches the safe
   factory path; empty or invalid values fail closed before broker selection.
2. The vacuous `not hasattr(app.state, "bridge_broker")` assertion was removed. Tests instead assert
   the selected-mode flag, absent engine, zero broker/credential calls, DISARMED status, and durable
   ARM rejection.
3. The first Codex audit found that module-level `app = create_app()` ran before `__main__` parsed a
   valid explicit CLI mode. An invalid environment value could therefore defeat explicit CLI
   precedence. Commit `17402a58` skips module-level ASGI construction only while executing as
   `__main__`, preserving environment-aware import behavior and production CLI precedence.

All credentialed probes patched `_build_broker`; no real credential resolver or broker path ran.

## D026 falsification evidence

Two independently meaningful RED/GREEN demonstrations were retained:

| Named defect | Exact pre-fix behavior with candidate tests | Repaired behavior |
|---|---:|---:|
| Public factory ignored environment / invalid env failed open | `2 failed, 4 passed` with `app.py` from `5a9bb922` | `6 passed` at `21f82133` |
| Invalid env defeated valid explicit CLI mode | `1 failed, 6 passed` with `app.py` from `21f82133` | `7 passed` at `17402a58` |

The final RED failed at the unconditional module-level `create_app()` before CLI parsing. The GREEN
reached fake uvicorn exactly once in credential-free DISARMED mode, used an isolated temporary DB,
and invoked no broker or credential path. Candidate app/test blobs were restored exactly afterward.

## Platform evidence

| Platform | Focused | Complete `IBKR_PAPER_BRIDGE/tests` |
|---|---:|---:|
| Windows final candidate | `7 passed` | `2 failed, 1311 passed` |
| Locked Linux final candidate | `7 passed` | `25 failed, 1288 passed` |
| Locked Linux frozen parent `5a9bb922` | `5 passed` | `25 failed, 1286 passed` |

Windows failures remain the KVM2 ledger artifact-hash mismatch and stale WAL schema expectation.
Linux retains exactly the same 25 failure node IDs: two Python-3.12 order-state GC assertions and
23 pre-existing WAL-bundle failures. The final candidate adds two passing tests over the frozen
parent and no new full-suite failure.

Lead commands included:

```text
python -m pytest -q IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py
python -m pytest -q IBKR_PAPER_BRIDGE/tests
PYTHONPATH=<scratch>/IBKR_PAPER_BRIDGE <locked-python> -m pytest -q ...
```

Linux validation used only `/home/gatea/queue-c-repair-17402a58-20260803` on the locked staging host.
No service or deployed runtime was touched.

## Independent audit chronology

- Round 1 at `21f82133`: GLM-5.2 returned PASS, but fresh `gpt-5.6-sol` xhigh returned
  **REQUEST_CHANGES** for the production CLI-precedence regression. The Lead reproduced it and the
  finding was binding.
- Round 2 at `17402a58`: the read-only GLM wrapper returned **BLOCK** because it could execute none
  of pytest, SSH, or D026. Per D025 it has no acceptance weight; its static review found no defect.
- Round 2 execution-enabled fresh GLM-5.2: **PASS**, with Windows, Linux, D026 RED/GREEN, behavior,
  and final-clean proof executed.
- Round 2 fresh `gpt-5.6-sol` xhigh: **PASS**, independently executing the same required evidence.
- Lead independently reproduced scope, the round-1 finding, both D026 demonstrations, safe factory
  and CLI behavior, platform counts, failure-name equality, ancestry, blobs, and cleanliness.

This used one non-accepting repair round of the three-round bound.

## Safety and next boundary

The repaired branch may be published for source-candidate evidence. It must not be merged or used
for artifact rebuild under this record. Read-only integration readiness may proceed; Queue D and all
deployment/runtime/economic surfaces remain stopped.
