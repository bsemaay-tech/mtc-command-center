# Audit 2 Packet 10 — provisional mandated-suite baseline — 2026-08-15

Status: **PROVISIONAL BASELINE — NOT THE FREEZE-TIME BASELINE.**

The pre-WP-A freeze SHA does not exist yet, so this cannot be the freeze-time
run. Its purpose is narrower and still useful: it pins the exact command, the
exact environment identity, the real counts and duration, and the identity and
root cause of every anomaly, so that the freeze-time run is a **re-run of a
known thing** rather than a discovery. Owner authorization for this local
execution was given on 2026-08-15.

## Subject and isolation

| item | value |
|---|---|
| Worktree | `C:\P10BASE`, detached, created for this run |
| Commit | `ddc8a9c802cc45f66f449b02f18a07448afc5f70` |
| `git status --porcelain` | empty before and after both runs |
| Branch of origin | `codex/rp7-r1-r4-repair-20260815` |

## Freeze-time recheck checklist — steps 1 to 8

Executed in order, from the checklist in
`AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md`.

1. **Frozen SHA and clean isolated worktree** — done, see table above.
2. **Frozen README lines 40-50 and `tests/conftest.py`** — the README contract is
   unchanged: repository-root CWD, `PYTHONUTF8=1`, and
   `python -m pytest IBKR_PAPER_BRIDGE\tests -q`. `conftest.py` still inserts the
   Bridge project root into `sys.path`.
3. **pytest configuration files** — none present. `pyproject.toml`, `pytest.ini`,
   `tox.ini`, and `setup.cfg` are absent from both the repository root and
   `IBKR_PAPER_BRIDGE/`. No `pytest_tmp` artifact exists in either root, so
   `--ignore=TSP1009B.pytest_tmp_s1r1` remains a no-op and was not used.
4. **Root-CWD explicit-tests vs Bridge-CWD collection** — the root-CWD explicit
   form was used, matching the README contract.
5. **Interpreter identity** — recorded below. **The locked version is not
   installed; this is the single most important limitation of this baseline.**
6. **`pytest11` entry points** — `anyio=anyio.pytest_plugin` and
   `pytest_cov=pytest_cov.plugin`. `pytest-randomly` is absent, so
   `-p no:randomly` remains a no-op and was not used.
7. **Deterministic controls** — `-p no:cacheprovider` was used. The other two
   candidate controls are no-ops here as recorded above; they must be
   re-evaluated in the frozen environment, not assumed.
8. **Command and environment frozen before execution** — yes, then executed.

## Environment identity

```text
INTERPRETER = C:\Python314\python.exe
PYTHON      = 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]
PLATFORM    = Windows-11-10.0.26200-SP0
PYTEST      = 9.0.2
PYTHONUTF8  = 1
pytest11    = anyio, pytest_cov
```

`IBKR_PAPER_BRIDGE/requirements.lock` pins `pytest==9.1.1`. The installed pytest
is **9.0.2**, and the only interpreters available on this machine are 3.14.2 and
3.13. **This is not the frozen-suite environment**, and no claim in this document
should be carried into the freeze without re-running under the locked pytest on
the intended interpreter.

## Exact command

```powershell
cd C:\P10BASE
$env:PYTHONUTF8 = "1"
python -m pytest IBKR_PAPER_BRIDGE\tests -q -p no:cacheprovider
```

## Results — two independent runs

| run | rc | counts | duration |
|---|---:|---|---|
| 1 | 1 | `2 failed, 1019 passed, 1 warning` | 100.01 s |
| 2 | 1 | `2 failed, 1019 passed, 1 warning` | 85.53 s |

Counts and failing test identities are identical across both runs. Duration is
not stable and must not be treated as an identity. The single warning is a
`StarletteDeprecationWarning` from `fastapi/testclient.py` about `httpx`, raised
by an installed dependency and not by product code.

## Anomaly A1 — `test_canonical_ledger_and_all_three_row_fixtures_validate`

`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:407`, failing with
`kvm2_ledger_validator.LedgerValidationError: publishable artifact hash mismatch`
raised at
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/validate_ledger.py:101`.

**Root cause: line-ending normalization, not a product defect.** The evidence
ledger has exactly one artifact row, and it records the Git-object hash:

| form | bytes | SHA-256 |
|---|---:|---|
| recorded in `EVIDENCE_LEDGER.jsonl` | — | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| Git object (LF) | 867 | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| Windows working tree (CRLF) | 903 | `b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a` |

The validator hashes the file on disk. The repository sets `* text=auto`, so a
Windows checkout renders CRLF and the hash cannot match. **This test fails on
every Windows checkout and passes on Linux** — including on the Ubuntu 24.04
deploy target. It is an environment-dependent test, not a deployment blocker,
but it means the Windows suite can never be green as written.

Reproduce:

```bash
git -C C:/P10BASE cat-file -p HEAD:MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json | sha256sum
sha256sum C:/P10BASE/MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
```

This is the **third** instance in two days of a recorded hash being ambiguous
between the Git-object and working-tree forms — see
`WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md`.
The standing rule proposed there applies here too.

## Anomaly A2 — `test_invariants_preserve_risk_and_history`

`IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py:321`, failing with
`AssertionError: assert '4' == '2'` on `inv["schema_version"]`.

**Root cause: a stale test expectation, not a product defect.**
`IBKR_PAPER_BRIDGE/bridge/store/db.py:263` sets `SCHEMA_VERSION_BASELINE = 4`, so
the `source_db` fixture creates a v4 database and the WAL bundle correctly
records `schema_version = "4"`. The assertion still expects the old baseline of
`"2"`. Default-v4 is the intended current behaviour; the test was not updated
when the baseline moved.

Unlike A1, **this one fails on Linux too**, so it does block a green suite on the
deploy target.

## Consequences for Packet 10 and for deploy

1. The two failures are now **identified, root-caused, and reproducible**, which
   is what the open question in `OPEN_QUESTIONS_FOR_DISPATCHER.md` section 2 said
   must not be inferred from the earlier vague "two-failure" description. That
   description is now replaced by measured fact — but only at this SHA and in
   this environment.
2. Neither failure is a product-behaviour defect. A1 is an artifact-hashing
   convention problem; A2 is an out-of-date assertion.
3. Deploy checklist item 9 requires the exact-SHA matrices to pass before the
   first VPS start. As things stand, A2 must be repaired for that to be
   achievable on Linux, and A1 must be either repaired or explicitly and
   permanently classified as Windows-only.
4. The freeze-time run must still happen, under the locked pytest, on the
   intended interpreter, at the real freeze SHA. **This document does not
   satisfy Packet 10.** It reduces Packet 10 to a re-run with a known expected
   result.

## What was not done

No repair was written. No product or test file was modified. No host, network,
deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet,
Pine, parity, MTC, trading, or economic action occurred. No freeze was implied or
performed.

Raw transcripts: `C:\tmp\p10_suite_run_2026-08-15.log` and
`C:\tmp\p10_suite_run2_2026-08-15.log`, copied to `11_TRIAGE/` alongside this
record.
