# Lane N report — master-red repair and diagnosis

Date: 2026-08-25

Branch: `fix/master-red-tests-20260825`

Baseline: `4691a9dd843f05948b271a88972c94a3bdce13a7`

## Result

Lane N completed both halves without crossing their boundary:

- FIX: committed only
  `IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py` as `12b58b29`.
- DIAGNOSE ONLY: wrote the ledger/WAL evidence chain and recommendations; no
  ledger, KVM2 evidence, fixture, WAL tool, Store, schema, or runtime file was
  edited.
- No Pine, parity, MTC_V2, schema, Bridge runtime, host, deployment, broker,
  network, or evidence-tree action occurred.
- No push was performed and no other AI CLI was used.

## Help-truth fix evidence

Baseline whole-file run:

```text
3 failed, 44 passed, 1 warning
```

The three failures were:

1. `dashboard_controls` still required the false
   `even with flatten=false the engine calls cancel_all()` wording.
2. `state_machine` still required the false `calls cancel_all() regardless`
   wording and its unprotected-position consequence.
3. The onboarding-link test treated a historical handoff mention as an active
   coding-agent onboarding pointer.

The needles now pin the source-correct facts already present in
`help_map.json`: one `/api/kill?flatten=false` interface path, no
`Engine.kill()` broad `cancel_all()`, old-schema latch-only behavior, and
schema-v9 selective risk-increasing cancellation with protection retention.
The onboarding check now examines the actual onboarding entry points rather
than every historical handoff record.

GREEN evidence:

```text
focused truth/onboarding checks: 23 passed, 1 warning
whole test_dashboard_static.py:   47 passed, 1 warning
```

D026 RED evidence used a disposable detached worktree at Commit 1 and restored
`help_map.json` from exact pre-correction commit `d71bc073`. Result:

```text
2 failed, 20 passed, 1 warning
dashboard_controls lost 'the engine never calls cancel_all()'
state_machine lost 'engine.kill() never calls cancel_all()'
```

The disposable worktree was removed after the run.

## Full-suite delta

Command:

```powershell
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```

Result:

```text
2 failed, 1379 passed, 1 warning in 110.49s
```

Exactly the three help failures are resolved. The only remaining failures are:

- `tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate`
- `tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history`

Their exact hashes, history, environment classification, first-red commits,
and unexecuted repair recommendations are in
`../MASTER_RED_TESTS_DIAGNOSIS_2026-08-25.md`.

## Commit contract

Commit 1 contains exactly:

```text
IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py
```

Commit 2 contains exactly:

```text
MTC_COMMAND_CENTER/11_TRIAGE/MASTER_RED_TESTS_DIAGNOSIS_2026-08-25.md
MTC_COMMAND_CENTER/11_TRIAGE/MASTER_RED_2026-08-25/LANE_REPORT.md
```
