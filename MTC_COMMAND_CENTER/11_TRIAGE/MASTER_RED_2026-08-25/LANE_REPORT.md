# Lane N report — master-red repair and diagnosis

Date: 2026-08-25

Branch: `fix/master-red-tests-20260825`

Baseline: `4691a9dd843f05948b271a88972c94a3bdce13a7`

## T1 repair round 1 — onboarding guards and help-map self-reference

The single required T1 finding is repaired within the Lead-authorized scope extension:

- `test_dashboard_static.py` again guards `AI_RULES.md` explicitly as a coding-agent
  onboarding file.
- The test now inspects the live `GLOBAL_HANDOFF.md` explicitly and pins its existing
  historical `help_map.json` record rather than pretending that no `_AI_MEMORY` file
  mentions the map.
- Exactly one `help_map.json` string changed. It now states that `help_map.json` is the
  canonical AI-readable Help knowledge source, historical handoff records reference it,
  and coding-agent onboarding files do not currently direct agents to it.
- The test pins all three parts of that corrected claim.

The tight pre-fix RED run changed the test first and left the old JSON claim in place:

```powershell
python -m pytest -q tests/test_dashboard_static.py::test_help_knowledge_pins_ai_source_and_onboarding_guards -p no:randomly
```

Result:

```text
1 failed, 1 warning in 0.79s
AssertionError: the old JSON lacked
"canonical ai-readable knowledge source for the help surface is help_map.json"
```

After the one-string JSON correction, the same focused command passed:

```text
1 passed, 1 warning in 0.60s
```

Whole-file GREEN:

```text
python -m pytest -q tests/test_dashboard_static.py -p no:randomly
47 passed, 1 warning in 0.72s
```

Full-suite baseline confirmation:

```text
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
2 failed, 1379 passed, 1 warning in 131.08s
```

The failures are exactly the two already diagnosed below: the KVM2 ledger artifact hash
mismatch and WAL invariant `schema_version` `"4" != "2"`.

### D026 falsification against `d71bc073`

The current repaired test function was invoked with `help_map.json` loaded directly from
`git show d71bc073:IBKR_PAPER_BRIDGE/bridge/static/help_map.json`; no tracked file was
overwritten and no stash was used. Command harness:

```powershell
@'
import json
import runpy
import subprocess

module = runpy.run_path("tests/test_dashboard_static.py")
old_help = json.loads(
    subprocess.check_output(
        ["git", "show", "d71bc073:IBKR_PAPER_BRIDGE/bridge/static/help_map.json"],
        cwd=module["REPO_ROOT"],
        text=True,
    )
)
module["test_help_knowledge_pins_ai_source_and_onboarding_guards"](old_help)
'@ | python -
```

Real result: exit 1 at `test_dashboard_static.py:343`; the old claim failed the new
`canonical ai-readable knowledge source for the help surface is help_map.json` needle.
This establishes RED against the exact historical bytes and GREEN against the repair.

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

Repair round 1 stages exactly:

```text
IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py
IBKR_PAPER_BRIDGE/bridge/static/help_map.json
MTC_COMMAND_CENTER/11_TRIAGE/MASTER_RED_2026-08-25/LANE_REPORT.md
```
