# Audit 2 Packet 10 — current-bytes preflight

Type: **T2 documentation-only preflight**. This is not a frozen-SHA fill and
not an executed baseline.

## Repository-state boundary

- Recorded HEAD: `8bfc59ca`.
- `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` carries an unrelated uncommitted partial
  repair. Therefore the current checkout is **not** a freeze candidate.
- This report records current-byte facts only. It does not choose or bless the
  final suite command, worktree, interpreter, counts, rc, duration, anomalies,
  or frozen SHA.

## Current facts

`IBKR_PAPER_BRIDGE/README.md:43-46` uses repository-root CWD,
`PYTHONUTF8=1`, and:

```powershell
python -m pytest IBKR_PAPER_BRIDGE\tests -q
```

`IBKR_PAPER_BRIDGE/tests/conftest.py` inserts the Bridge project root into
`sys.path`. Neither the repository root nor `IBKR_PAPER_BRIDGE` currently has
`pyproject.toml`, `pytest.ini`, `tox.ini`, or `setup.cfg`. Neither root contains
`TSP1009B.pytest_tmp_s1r1` or another matching `pytest_tmp` entry.

The inspected desktop process is Python 3.14.2 with pytest 9.0.2. Its installed
`pytest11` entry points are `anyio` 4.12.1 and `pytest-cov` 7.0.0 only;
`pytest-randomly` is absent. `IBKR_PAPER_BRIDGE/requirements.lock` instead pins
`pytest==9.1.1`, so this desktop interpreter is not the future frozen-suite
interpreter.

## Conservative implications

- Keep `-p no:cacheprovider` as an explicit deterministic control.
- `-p no:randomly` is currently a no-op against an absent plugin, but retain it
  as a candidate control and recheck it in the frozen environment.
- `--ignore=TSP1009B.pytest_tmp_s1r1` is currently a no-op from Bridge CWD
  because that path is absent; recheck its need at the frozen SHA.
- The root-CWD explicit-tests form is the current README contract.
- `AUDIT2_PACKET10_SUITE_FILL_2026-08-13.md` intentionally remains unresolved
  until frozen-SHA reconciliation.

No test, pytest collection, product-code import, host/network/service/credential
action, or Git command was performed as part of this preflight.

## Freeze-time recheck checklist

1. Confirm the frozen SHA and a clean isolated worktree.
2. Re-read frozen README lines 43-46 and `tests/conftest.py`.
3. Re-scan both roots for pytest configuration files and `pytest_tmp` artifacts.
4. Reconcile root-CWD explicit-tests versus Bridge-CWD collection semantics.
5. Record the absolute interpreter path and verify the locked pytest version.
6. Re-enumerate all installed `pytest11` entry points.
7. Re-evaluate `no:cacheprovider`, `no:randomly`, and the ignore path.
8. Freeze the exact command and environment before execution.
9. Only then execute and record rc, counts, duration, anomaly identities, and
   baseline source under the separately authorized freeze-time gate.
