NEEDS-REWORK

# Packet 10 suite-contract adversarial review

The contract is strong about preserving a run after it happens, but it does not yet make two conforming runs reproducible. The mandated command inherits almost the whole operator environment, the installation does not freeze the platform or selected wheel artifacts, plugin sufficiency is not established from the permitted sources, and no stable semantic fingerprint is separated from deliberately unstable raw evidence. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:27-41`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:96-105`

## Required findings

### 1. The execution environment is not closed

The exact command unsets only `PYTHONHOME`, `PYTHONPATH`, `PYTEST_ADDOPTS`, and `PYTEST_PLUGINS`, and sets only `PYTHONUTF8` and `PYTEST_DISABLE_PLUGIN_AUTOLOAD`; every other process variable remains ambient. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16`

| Variable/control | Finding | Required settlement |
|---|---|---|
| Locale (`LC_ALL`, `LC_*`, `LANG`) | **UNKNOWN and unfixed.** The command contains no locale assignment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16` | Set one available locale in a frozen image and record its resolved locale output. |
| Timezone (`TZ` and host zone) | **UNKNOWN and unfixed.** The contract requests UTC evidence timestamps but does not set the process timezone. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:101-101`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16` | Set `TZ=UTC` in the launcher and freeze the timezone-data source. |
| `PATH` | **UNKNOWN and unfixed.** Suite subprocesses inherit ambient `PATH`, and environment creation invokes the non-absolute name `python3.12`. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:33-38` | Use an explicit minimal `PATH`; use an absolute, pre-identified interpreter to create the venv; record hashes/versions for any external executable the suite invokes. |
| `HOME`, `USER`, `LOGNAME`, and XDG directories | **UNKNOWN and unfixed.** The command neither clears nor assigns them, while the only global fixture shown isolates Telegram credential resolution rather than the full user environment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16`; `IBKR_PAPER_BRIDGE/tests/conftest.py:13-21` | Run with an empty, controlled home/config/cache tree and a documented identity, or prove by a source inventory that no test or imported code reads these inputs. |
| Temp root (`TMPDIR`, `TMP`, `TEMP`) | **UNKNOWN and unfixed.** No temp-root value appears in the exact command. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16` | Allocate a fresh controlled temp directory at a canonical path, record its identity, and prove it is empty before and after the run. |
| Randomness (`PYTHONHASHSEED` plus application/test RNG seeds) | **UNKNOWN and unfixed.** The command sets no seed, and disabling plugin autoload does not itself establish an application/test seed. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:73-75` | Fix `PYTHONHASHSEED`; inventory every RNG used by collection/tests and either seed it or classify the affected output as non-comparable. |
| CPU count, concurrency, thread limits, resource limits, and umask | **UNKNOWN and unfixed.** The contract records platform identity but specifies no CPU count/cpuset, thread-limit environment, limits, or umask. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:56-60`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16` | Freeze these in the execution image/launcher and include their resolved values in the identity record. |
| Warnings and output formatting (`PYTHONWARNINGS`, `COLUMNS`, `TERM`, color controls) | **UNKNOWN and unfixed.** The contract compares warning counts and preserves raw output bytes, but the command does not close these ambient inputs. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:101-104` | Fix or clear them and record the final whitelist. |

A reproducible launcher should start from an empty environment (for example, `env -i`) and add a reviewed whitelist. Recording only selected values after execution does not constrain what influenced execution. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:58-60`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:100-105`

### 2. “Linux CPython 3.12” permits materially different runtimes

The precondition fixes only Linux and the Python minor line; the literal interpreter path is explicitly `UNKNOWN` until the future environment is created, and version/platform/hash are recorded only afterward. Two operators can therefore use different CPython patch/builds, distributions, kernels, libc implementations, architectures, and executable/stdlib payloads while satisfying the written pre-run rule. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:21-27`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:56-58`

The lock header likewise targets Python 3.12 on “linux” without fixing an architecture or OS image. `IBKR_PAPER_BRIDGE/requirements.lock:1-2`

Required repair: freeze an immutable execution-image digest, architecture/libc identity, exact interpreter distribution and full payload identity before either operator runs. Keep the existing post-run identity record as corroboration, not as the control. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:56-60`

### 3. The dependency installation is integrity-checked, not artifact-reproducible

The contract installation uses hashes, binary-only mode, no cache, and no dependency resolution, but it does not use `--no-index` or a frozen `--find-links` source. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:33-39`

The repository installer adds `--no-index --find-links` only when `WHEELHOUSE` is non-empty, confirming that the ordinary form and the offline-wheelhouse form are distinct. `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:292-306`

The lock permits multiple hashes for platform-bearing packages—for example, the `bitarray` entry immediately lists multiple accepted hashes—while the verifier checks installed distribution names and versions, not the selected wheel filename/hash or installed-file hashes. `IBKR_PAPER_BRIDGE/requirements.lock:23-30`; `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:66-97`

The verifier also excludes `pip` and `setuptools` from exact-set equality, and the contract does not record the pip version used for installation. `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:18-21`; `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:83-97`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:56-58`

Required repair: freeze an offline wheelhouse manifest with every selected wheel path/bytes/SHA-256, use `--no-index --find-links`, freeze the installer/pip identity, require the venv path to be absent before creation, and verify installed payload hashes as well as distribution versions. `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:281-309`; `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:66-97`

### 4. The explicit plugin list has no demonstrated missing member, but sufficiency is `UNKNOWN`

The explicit `anyio.pytest_plugin` module is available because the lock pins `anyio==4.14.2`, and pytest itself is pinned to 9.1.1. `IBKR_PAPER_BRIDGE/requirements.lock:15-22`; `IBKR_PAPER_BRIDGE/requirements.lock:986-989`

The inspected `conftest.py` defines only an autouse fixture using pytest’s `monkeypatch` fixture; it declares no third-party fixture or hook requirement. `IBKR_PAPER_BRIDGE/tests/conftest.py:6-21`

However, the lock describes `anyio` as a transitive runtime dependency of `anthropic`, `httpx`, `starlette`, and `watchfiles`; that does not establish that `anyio` is the suite’s only required third-party pytest plugin. `IBKR_PAPER_BRIDGE/requirements.lock:15-22`

The Windows baseline autoloaded both `anyio` and `pytest_cov`, whereas the new contract disables autoload and loads only `anyio`; the baseline therefore cannot prove equivalence of the plugin graph. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:37-44`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:62-75`

**UNKNOWN:** the permitted sources do not inventory plugin-dependent markers, fixtures, or hooks used by every test module. What would settle it is a frozen-SHA source inventory plus successful collection and execution under the exact disabled-autoload command, with the actually loaded plugin set captured (not merely all installed `pytest11` entry points). The contract already calls for collect-only and installed-entry-point evidence, but not a loaded-plugin manifest. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:58-64`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:96-105`

If a required plugin is absent, the run must remain non-accepting; the upstream audit rule already says inability to execute the mandated suite is `BLOCK`. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:102-104`

## Windows-to-Linux carryover and the two anomalies

The contract correctly refuses to carry the provisional counts into the freeze: the Windows run used Python 3.14.2 and pytest 9.0.2, while the lock pins pytest 9.1.1, and the provisional record expressly calls itself an invalid frozen-suite environment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:47-62`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:41-43`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:87-92`

The two Windows runs had identical counts and failure identities but different durations, and the provisional record explicitly says duration is not an identity. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:72-82`

The prediction for **A1** is correctly conditional: the accepted repair pins the ledger-schema path to LF, while the adjudication warns that a pre-existing Windows checkout can retain stale CRLF bytes and says the fresh Linux target was not affected. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:19-24`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:51-64`

The prediction for **A2** is also correctly conditional: the accepted repair reads the fixture database’s schema version rather than hardcoding `2`, and the independent audit exercised the repaired test’s discriminating power. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:26-40`

**UNKNOWN:** whether the future frozen SHA contains both repairs and whether either anomaly is absent under the exact locked Linux environment. The repair record says the changes were not merged and the exact frozen-SHA locked-environment green run remained outstanding; only inspection of the final SHA followed by the mandated run settles this. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:3-17`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72`

Thus the contract’s statement that A1 and A2 are expected absent **if** both accepted repairs are present and the checkout is fresh is supported as an expectation, not as a frozen observation. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:107-122`

## Evidence contract: strong provenance, missing stable comparison semantics

The contract does require the key raw facts: collection node IDs/count, frozen SHA, worktree/interpreter identity, exact command/environment, timestamps and durations, separate byte-preserved stdout/stderr with sizes and hashes, detailed outcome counts and non-pass IDs, anomaly signatures, lock/plugin identities, and a final evidence manifest. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:94-105`

That is enough to preserve what happened, but not enough to define when a future run “matched”:

1. UTC timestamps, absolute worktree/interpreter paths, monotonic elapsed time, and pytest duration are intentionally run-specific. The contract itself says duration is not stable. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:100-102`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:74-80`
2. Raw stdout/stderr hashes bind each transcript, but the contract defines no canonical, duration/path-neutral output signature for cross-run equality. It separately asks for “stable” error text and a hash of the complete failure block without specifying normalization. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:101-105`
3. Ordered node IDs are retained, but **UNKNOWN** whether collection order and generated parameter IDs are stable under the unfixed environment. Two independent exact-environment collection manifests, plus an explicit canonical encoding and comparison rule, would settle it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:96-96`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:103-105`
4. The baseline table freezes expected exit/fail/pass/skip/xfail fields but has no expected collected, executed, error, xpass, warning, deselected, or collection-manifest hash fields, even though some of those are requested later as actual execution evidence. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:80-90`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:98-105`
5. The contract does not define a machine-readable schema or named extractor for counts/signatures, so two operators can preserve the same bytes yet transcribe or classify them differently. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:98-105`

Required repair: retain all raw evidence exactly as proposed, but add a versioned machine-readable result schema and a canonical semantic fingerprint that excludes timestamps, durations, absolute ephemeral paths, and other run-specific fields. It should bind the frozen SHA; image/interpreter/lock/wheel/plugin identities; normalized command and environment whitelist; canonical collection manifest; exact outcome counts including deselection; every non-pass node ID; normalized warning/anomaly signatures; and the extractor’s own path/bytes/SHA-256. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:94-105`

Finally, demonstrate reproducibility with two independent clean environments/operators and compare the canonical fingerprints before calling the freeze-time baseline reproducible. The earlier two-run record is not sufficient because it used the wrong interpreter/pytest/plugin environment and expressly forbids carryover. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:37-62`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:72-82`

## Minimum rework before execution

1. Replace the ambient launcher with a frozen-image, empty-environment whitelist that explicitly controls locale, timezone, path, home/XDG, temp, hash/RNG seeds, warning/output settings, CPU/thread/resource limits, and umask. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:12-16`
2. Predeclare the exact image, architecture/libc, interpreter payload, installer, and offline selected-wheel manifest; make venv creation provably fresh. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:21-41`; `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:281-309`
3. Prove the required loaded-plugin set from suite usage and an exact-command collection/execution, and retain the loaded set. `IBKR_PAPER_BRIDGE/tests/conftest.py:6-21`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:62-78`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:96-105`
4. Add the structured normalized fingerprint and comparison rule while retaining raw byte evidence as provenance. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:94-105`
5. Run the final contract independently twice and require semantic-fingerprint equality; do not use provisional Windows counts or durations as the expectation. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:58-82`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:87-92`

No runtime estimate is derived here: **NO SOURCED ESTIMATE**. The contract itself says the provisional durations cannot supply one for the locked frozen environment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:124-128`
