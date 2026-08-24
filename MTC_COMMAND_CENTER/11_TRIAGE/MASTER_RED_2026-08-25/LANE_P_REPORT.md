# Lane P — WAL stale-test repair

Date: 2026-08-25

Branch: `fix/wal-schema-test-20260825`

Starting SHA: `6654fa9f4fbf55e6d47a33890a86be99c28d52a3`

Audit tier: **T1** — local, non-economic Bridge test work plus its evidence report. Gate 5 acceptance remains Lead-owned.

## Scope and boundaries

This lane changes only the stale WAL bundle test and this report. It does not change the WAL bundle producer, Bridge runtime, a schema definition, Pine, parity, MTC_V2, `KVM2_PROGRAM`, or any evidence artifact. It performs no host, deployment, service, credential, broker, exchange, ARM, paper/live-trading, network, merge, or push action.

## Evidence chain: producer truth is schema version 4

1. Merge `f61ed91919110e8856b2bc309c2c807365bb5fea` combined first parent `ecc7a07e` with KVM2 feature parent `6fe0130f`. The feature parent introduced `test_wal_state_bundle.py` and `wal_state_bundle.py`; its `Store.initialize()` created fresh databases with `meta.schema_version = "2"`, matching the test's original literal.
2. Commit `65eaedb0f72ec6e7cfd6cb955ec1792052f295e2` is an ancestor of merge first parent `ecc7a07e` and is not an ancestor of `6fe0130f`. The first-parent Store line defines `SCHEMA_VERSION_BASELINE = 4`, makes it the default `initialize()` target, and writes `("schema_version", "4")` in `_initialize_v4_fresh()`.
3. Current `bridge/store/db.py` preserves that contract: `SCHEMA_VERSION_BASELINE = 4`; `initialize()` defaults to it; a new database calls `_initialize_v4_fresh()`; that initializer writes the string `"4"` to `meta`.
4. The current producer does not invent or upgrade this value. `tools/wal_state_bundle.py::collect_invariants()` reads `meta.schema_version` through `_meta()`. `create_bundle()` collects source invariants, performs SQLite online backup, collects bundle invariants, requires source/bundle invariants to match, and writes the bundle-derived invariants to the manifest.
5. `docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md` section 7 explicitly states that `meta.schema_version` is the database authority, `initialize(...)` defaults to **4**, and v5 is explicit opt-in. `KVM2_PROGRAM/recovery/STATE_CONTINUITY.md` defines the bundle contract as preserving and rechecking sanitized risk/history invariants.

Conclusion: schema version `4` is legitimate producer truth. The literal `"2"` was stale merge drift, not a producer defect and not Python 3.14 behavior.

## Repair

`test_invariants_preserve_risk_and_history` now queries the fixture database's real `meta.schema_version` before capture, asserts that the row exists, and requires the manifest invariant to equal that independently observed source value. This is stronger than replacing `"2"` with another constant: it directly proves preservation and remains valid for any explicitly supported fixture schema.

The test's real risk/history assertions are unchanged: DISARMED state, one open trade, one live order, three closed trades, paper/testnet identity, three consecutive losses, total/latest realized PnL of `-18.0`, the trading date, and risk-day loss/rearm values remain asserted.

## RED/GREEN evidence

### Original focused RED

```powershell
python -m pytest IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history -q
```

```text
AssertionError: assert '4' == '2'
1 failed in 0.99s
```

### D026 deliberate producer-truth mutation — RED

An isolated temporary copy of `tools/wal_state_bundle.py` changed only the collected invariant from `_meta(conn, "schema_version")` to the false literal `"999"`. `PYTHONPATH` selected that copy; the repository producer was not edited. The temporary copy and its generated `__pycache__` were deleted after the run.

```powershell
$env:PYTHONPATH = 'C:\tmp\LANE_P_D026_MUTANT_20260825;C:\WPPWAL_20260825\IBKR_PAPER_BRIDGE'
python -c "from tools import wal_state_bundle as wal; print(wal.__file__)"
python -m pytest IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history -q -p no:cacheprovider
```

```text
C:\tmp\LANE_P_D026_MUTANT_20260825\tools\wal_state_bundle.py
AssertionError: assert '999' == '4'
FAILED IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history
1 failed in 0.77s
```

This is discriminating: a bundle producer that reports a schema version different from the real source database is rejected.

### Real producer — GREEN

```powershell
$env:PYTHONUTF8 = '1'
python -m pytest IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history -q -p no:cacheprovider
```

```text
.                                                                        [100%]
1 passed in 0.54s
```

### Full Bridge suite

```powershell
$env:PYTHONUTF8 = '1'
python -m pytest IBKR_PAPER_BRIDGE/tests -q -p no:cacheprovider
```

```text
FAILED IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate
1 failed, 1350 passed, 1 warning in 131.31s (0:02:11)
```

The only remaining failure is the known Windows CRLF publishable-artifact hash mismatch. This lane did not touch it or anything under `KVM2_PROGRAM/evidence`.

## Final scope and staging record

`git diff --check` returned exit 0; Git emitted only its existing LF-to-CRLF working-copy warning for the test file. No Bridge-local Ruff configuration exists, so the focused and full pytest runs are the applicable QA checks. The change has no strategy, Pine, parity, MTC, runtime, or trading-behavior impact.

Exact staged paths:

```text
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
MTC_COMMAND_CENTER/11_TRIAGE/MASTER_RED_2026-08-25/LANE_P_REPORT.md
```

The final lane commit SHA is printed with the `LANE P DONE` handoff. A commit cannot embed its own SHA without changing that SHA; the starting, causal, and merge SHAs are recorded above.
