# Packet 10 mandated-suite contract — definition freeze

Status: **definition material for the Lead and owner; not an execution record, gate verdict, acceptance decision, or authorization.** Packet 10 requires separate frozen-SHA execution and anomaly records, and the earlier provisional run does not satisfy Packet 10. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-64`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:146-149`

## 1. Frozen suite definition

The suite is the repository-root invocation of `IBKR_PAPER_BRIDGE/tests`; the Bridge README establishes repository-root CWD, `PYTHONUTF8=1`, and `python -m pytest IBKR_PAPER_BRIDGE\tests -q`, while `tests/conftest.py` inserts the Bridge project root into `sys.path`. `IBKR_PAPER_BRIDGE/README.md:40-46`; `IBKR_PAPER_BRIDGE/tests/conftest.py:8-10`

The exact mandated command is the following Linux `bash` command. `P10_WORKTREE` and `P10_PYTHON` are frozen environment fields, not discretionary substitutions:

```bash
cd -- "$P10_WORKTREE" && \
env -u PYTHONHOME -u PYTHONPATH -u PYTEST_ADDOPTS -u PYTEST_PLUGINS \
  PYTHONUTF8=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  "$P10_PYTHON" -m pytest IBKR_PAPER_BRIDGE/tests -q \
  -p anyio.pytest_plugin -p no:cacheprovider
```

`P10_WORKTREE` must be the absolute path of a clean isolated worktree at the full frozen SHA. The worktree path, exact-HEAD equality, and empty pre/post `git status --porcelain` outputs are required execution evidence. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:65`

`P10_PYTHON` must be the absolute, symlink-resolved path of the isolated locked interpreter described below. **Its literal path is currently `UNKNOWN`** because neither the future frozen worktree nor its execution environment exists in the read sources. It is frozen before execution by writing the resolved value into the environment-identity record; the preflight checklist expressly requires the absolute interpreter path and locked pytest verification. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:51-58`

No auditor may replace this command or infer an anomaly set; inability to execute the mandated suite is a BLOCK for that auditor, not acceptance. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:102-104`

## 2. Interpreter and installation contract

The valid environment is **Linux CPython 3.12**, because the lock was generated for `--python-version 3.12 --python-platform linux`; the canonical Linux runtime also names `python3.12`. `IBKR_PAPER_BRIDGE/requirements.lock:1-2`; `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:31`

Create a fresh virtual environment with Python 3.12 and install the **entire** `IBKR_PAPER_BRIDGE/requirements.lock` with hashes, no dependency re-resolution, binary wheels only, no input, and no cache. Installing only pytest 9.1.1 is insufficient: the repository installer installs the complete lock and then verifies exact installed-set equality. `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:281-309`

The installation form is:

```bash
python3.12 -m venv "$P10_VENV"
"$P10_VENV/bin/python" -m pip install \
  --require-hashes --no-deps --only-binary=:all: \
  --no-input --no-cache-dir --disable-pip-version-check \
  -r "$P10_WORKTREE/IBKR_PAPER_BRIDGE/requirements.lock"
```

For the frozen run, `P10_PYTHON` is the real path of `$P10_VENV/bin/python`. Tonight's `C:\Python314\python.exe`, Python 3.14.2, pytest 9.0.2 environment is invalid for this contract: the provisional record says it is not the frozen-suite environment and requires a rerun with the locked pytest on the intended interpreter. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:47-62`

The lock pins `pytest==9.1.1` and `anyio==4.14.2`. `IBKR_PAPER_BRIDGE/requirements.lock:986-989`; `IBKR_PAPER_BRIDGE/requirements.lock:15-22`

Before collection or execution, run the frozen interpreter's offline equality check:

```bash
"$P10_PYTHON" \
  "$P10_WORKTREE/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" \
  --lock "$P10_WORKTREE/IBKR_PAPER_BRIDGE/requirements.lock" \
  --check-installed
```

This verifier compares installed names and versions with the lock, rejects missing/wrong or unexpected distributions apart from venv bootstrap tools, and performs no network access. `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:2-7`; `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:75-98`

### Identity proof that must be recorded

Record, before the run, all of the following from `P10_PYTHON`: `realpath(sys.executable)`, the interpreter executable's SHA-256, `sys.version`, `sys.implementation.name`, `sys.implementation.cache_tag`, `sys.platform`, `platform.platform()`, `pytest.__version__`, the `verify_lock.py --check-installed` stdout/stderr/rc, the requirements-lock path/bytes/SHA-256, and every installed `pytest11` entry point as `(entry-point name, module value, distribution name, distribution version)`. The preflight requires absolute interpreter identity, locked pytest verification, and complete `pytest11` enumeration. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:55-58`

Also record the full frozen SHA from the worktree and the empty pre/post cleanliness outputs; the suite execution record must prove that the run used that SHA. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:65`

## 3. Plugin set and deterministic controls

The required third-party pytest plugin set is exactly **`anyio=anyio.pytest_plugin` from locked `anyio==4.14.2`**. Third-party plugin autoload is disabled and that plugin is loaded explicitly by the mandated command. The provisional environment enumerated `anyio` and `pytest_cov`, but the complete locked environment—not that provisional desktop environment—is the required distribution set. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:37-44`; `IBKR_PAPER_BRIDGE/requirements.lock:15-22`; `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:83-92`

| Control | Frozen classification | Contract treatment | Source |
|---|---|---|---|
| Clean isolated worktree at the full SHA | **Real control** | Required; prove exact HEAD and empty pre/post status. | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:65` |
| Root CWD plus explicit `IBKR_PAPER_BRIDGE/tests` | **Real control** | Required in the exact command; it is the README collection contract. | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:17-27`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:42` |
| Exact Linux/Python-3.12 hash-locked venv | **Real control** | Required; exact installed-set verification must pass before collection. | `IBKR_PAPER_BRIDGE/requirements.lock:1-2`; `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:281-309` |
| `PYTHONUTF8=1` | **Real control** | Required in the exact command. | `IBKR_PAPER_BRIDGE/README.md:43-46` |
| Unset `PYTHONHOME`, `PYTHONPATH`, `PYTEST_ADDOPTS`, `PYTEST_PLUGINS` | **Real control** | Required in the exact command so those ambient variables cannot alter interpreter or pytest behavior. | Contract definition; the environment must be frozen before execution per `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:55-58`. |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` plus explicit `-p anyio.pytest_plugin` | **Real control** | Required in the exact command; loaded third-party plugins cannot vary with ambient installations. | Contract definition; plugin enumeration/re-evaluation is required by `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:55-58`. |
| `-p no:cacheprovider` | **Real control** | Required in the exact command; the provisional run used it as its deterministic control. | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:42-45`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:64-70` |
| `-p no:randomly` | **No-op in this frozen contract** | Omitted. Plugin autoload is disabled, the exact installed distribution set is lock-verified, and only `anyio` is explicitly loaded. The provisional desktop also found `pytest-randomly` absent. | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:29-33`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:39-44` |
| `--ignore=TSP1009B.pytest_tmp_s1r1` | **No-op if the required freeze-time rescan confirms the path absent; otherwise `UNKNOWN` and the command must not run** | Omitted. The current and provisional trees found no matching artifact, but the freeze checklist requires a fresh rescan rather than inference. | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:24-27`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:51-58`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:31-34` |

The command must not run until the frozen roots have also been rechecked for `pyproject.toml`, `pytest.ini`, `tox.ini`, and `setup.cfg`; the provisional absence is not permission to assume future absence. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:51-58`

## 4. Baseline fields

| Field | Definition-time value |
|---|---|
| `MANDATED_COMMAND` | Exact command in section 1. |
| `EXPECTED_EXIT_CODE` | `0` — the frozen contract is a green full-suite expectation, not an accepted-failure baseline. The accepted repair record says the exact frozen-SHA locked-environment green run remains required. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72` |
| `EXPECTED_FAIL_COUNT` | `0`; neither known anomaly is an accepted expected failure. The anomaly set still has to be observed and adjudicated at the frozen SHA. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:64` |
| `EXPECTED_PASS_COUNT` | `UNKNOWN`. It is settled only by collection/execution at the real frozen SHA in the valid locked environment; the provisional document forbids carrying its claims into the freeze without that rerun. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:58-62` |
| `EXPECTED_SKIP_XFAIL_COUNTS` | `UNKNOWN`. The required values must be filled from one authoritative frozen source. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:89-100` |
| `EXPECTED_FAILURES` | None expected; the accepted anomaly register is nevertheless `UNKNOWN` until the frozen observation/adjudication. An empty set must be observed/adjudicated, not hardcoded. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:64` |
| `BASELINE_SOURCE` | `UNKNOWN`. It is settled by the exact path/bytes/SHA-256 of the future frozen-SHA execution and anomaly records. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-64` |

The provisional observations—two runs at rc 1 with `2 failed, 1019 passed, 1 warning`—remain diagnostic history only, not the frozen baseline. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:72-82`

## 5. Execution evidence to record

Before the suite body, run the same interpreter, environment controls, plugin flags, CWD, and test path with `--collect-only -q`; retain the ordered collected node IDs and their count as a collection manifest. This is a contract mechanism for satisfying the required exact test identities; it does not substitute for executing the mandated suite, because every auditor must execute it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:89-104`

For the actual suite execution retain:

- full frozen SHA, absolute worktree path, pre/post cleanliness output, absolute real interpreter path and interpreter/environment identity from section 2; these bind the record to the frozen SHA and locked environment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63-65`
- the exact argv/command and CWD; the explicit environment values and the names confirmed unset; UTC start/end timestamps; monotonic elapsed milliseconds; and pytest's reported duration. The earlier two-run record demonstrates that duration is measured but is not a stable identity. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:74-80`
- byte-preserved stdout and stderr separately, each path/byte count/SHA-256, plus the process rc. Packet 10 requires stdout/stderr, rc, and output bytes/SHA. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`
- exact collected/executed/pass/fail/skip/xfail/xpass/error/warning counts; the ordered collection node IDs; and every failing, skipped, xfailed, xpassed, or errored node ID. The mandated baseline fields require exact pass/fail and skip/xfail values, and P10-11 requires exact counts and test IDs. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:89-100`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`
- for every anomaly: exact node ID, phase, exception/assertion type, stable assertion/error text, top repository `file:line`, and SHA-256 of the complete failure block. P10-10/P10-12 require exact IDs and accepted output signatures, not a remembered cardinality. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-64`
- the requirements-lock identity, `verify_lock` transcript/rc, plugin-entry-point inventory, collection-manifest identity, and a final manifest binding every retained evidence file by path/bytes/SHA-256. The frozen execution record and baseline source must be exact and authoritative. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-64`

## 6. Known-anomaly expectation and adjudication rule

**A1** was the ledger-schema working-tree CRLF hash mismatch; the accepted repair pins that one path to LF. **A2** was the stale hardcoded schema-version assertion; the accepted repair derives the version from the fixture source database. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:19-29`

The repairs were accepted at T1, with the implementer reporting `1021 passed` twice and the independent auditor returning `PASS-WITH-NITS` with zero required repairs; the auditor independently exercised A2's discriminating power and confirmed A1 in a fresh clone. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:31-44`

Therefore, **if the full frozen SHA contains both accepted repairs and the run uses a fresh isolated checkout, A1 and A2 are expected to be absent**. This is an expectation, not the frozen observation or an acceptance decision. The repairs were not merged at the adjudication record's time, and the exact-SHA locked-environment green run was still outstanding. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:3-17`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72`

A1 has one additional precondition on Windows: an existing checkout may retain stale CRLF bytes after a fetch, whereas a fresh clone has the repaired LF bytes. This contract requires a fresh isolated worktree; if a Windows execution is separately contemplated, the ledger-schema byte count/hash must be re-proved before execution rather than assuming the attribute retroactively changed existing bytes. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:51-64`

Adjudication is fail-closed:

1. Any observed anomaly, including recurrence of A1 or A2, is recorded with the exact evidence fields in section 5; it is not silently converted into an expected failure. P10-12 requires an exact anomaly register and adjudication/authority for every accepted member. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:64`
2. First verify the frozen SHA, both repair identities/semantics, worktree bytes, locked interpreter/distributions, plugin inventory, command, and environment. The provisional facts are valid only at their recorded SHA/environment and cannot be carried forward without the locked rerun. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:135-149`
3. Root-cause and reproduce each anomaly against the exact frozen bytes. Only a separately recorded Lead/owner-authorized adjudication may place it in the accepted anomaly register; this document supplies neither acceptance nor authority. P10-12 expressly requires adjudication/authority rather than inference. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:64`
4. A zero-anomaly result is recorded explicitly as the observed empty set and adjudicated as such; it is never prefilled from the expectation above. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:64`

## 7. Estimate for one isolated frozen execution

**NO SOURCED ESTIMATE.** The only measured comparison is 85.53–100.01 seconds for two provisional runs, but that document says duration is not stable and, more importantly, those runs used Python 3.14.2/pytest 9.0.2 rather than the required locked environment; it expressly forbids carrying claims into the freeze without rerunning under locked pytest on the intended interpreter. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:74-80`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:58-62`

What would settle the estimate: one measured isolated execution at the real full frozen SHA using the exact interpreter/install/plugin/command contract above, with its monotonic duration recorded. That run is also the missing P10-11 execution source. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`
