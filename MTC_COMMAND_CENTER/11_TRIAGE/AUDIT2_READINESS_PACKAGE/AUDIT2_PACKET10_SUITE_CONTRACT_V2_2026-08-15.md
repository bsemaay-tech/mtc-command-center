# Packet 10 mandated-suite contract v2

Status: SUITE CONTRACT V2 - SUPERSEDES V1 - NOT ACCEPTED

| Review finding | Where v2 closes it | Constructible failure |
|---|---|---|
| 1. The process environment was ambient. | Sections 3 and 6 replace inheritance with a fresh-capsule contract and an `env -i` whitelist covering locale, timezone, paths, identity/home/XDG, temp, randomness, output, CPU/thread/resource controls, clock, filesystem, and network. | Add one unlisted variable to the pytest process, change one whitelisted value, start with a non-empty mutable directory, or expose an unmanifested executable; preflight must BLOCK before collection. The review identifies the ambient-variable defect at `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:9-24`. |
| 2. “Linux CPython 3.12” admitted materially different runtimes. | Section 2 requires a predeclared immutable image digest, machine/kernel/architecture/libc profile, exact CPython distribution, and complete interpreter/stdlib/shared-library payload manifest. Runtime measurements are compared with that independently sealed expectation. | Change the image digest, CPU/guest-kernel profile, interpreter executable, stdlib member, libc/loader, or mapped shared library; identity verification must BLOCK. The review requires pre-run payload identity rather than a post-run description at `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:26-32`. |
| 3. Installation was integrity-checked, not artifact-reproducible. | Section 4 makes the explicit policy choice: **artifact-reproducible**. A selected offline wheelhouse, installer payload, build report, and installed-file payload are all frozen by path/bytes/SHA-256; installation uses `--no-index --find-links`. | Remove, add, rename, or mutate a wheel; let pip select an unmanifested artifact; reuse a venv; alter pip; or change an installed file. The build or run preflight must BLOCK. The distinction is established at `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:292-306` and reviewed at `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:34-44`. |
| 4. No missing plugin was demonstrated, but list sufficiency was `UNKNOWN`. | Section 5 keeps `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and explicit `anyio.pytest_plugin`, labels sufficiency `UNKNOWN`, and defines the frozen-source inventory, loaded-plugin capture, strict collection, full execution, and negative-control procedure that alone may settle it. | Introduce an unresolved fixture, marker, hook, `pytest_plugins` declaration, or CLI option into a synthetic challenge corpus, omit its provider, or load an unexpected plugin; the inventory/collection/loaded-set gate must not pass. The unresolved state and settlement procedure come from `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:46-58`. |
| Review follow-up: raw provenance had no stable comparison semantics. | Sections 7 and 8 retain byte-exact evidence while adding a versioned result schema, a canonical semantic fingerprint, a fail-closed extractor contract, and two independent clean runs whose fingerprints must be identical. | Mutate one count, node ID, identity digest, warning/anomaly signature, plugin member, or normalized command/environment field; the fingerprint must change and equality must fail. The required repair is stated at `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:74-88`. |

## 0. Authority, status, and blocking unknowns

This is a T2 documentation-only suite definition. It is not an execution record, acceptance verdict, release decision, authorization, or permission for any host, network, deployment, service, credential, broker, trading, merge, or push action. Packet 10 still requires a frozen-SHA execution record and an observed/adjudicated anomaly register; the scope calls those separate unresolved producers. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-65`

The following exact values are **UNKNOWN (BLOCKING)** because no permitted source establishes them:

- full frozen repository SHA and canonical frozen worktree identity;
- immutable execution-image digest and exact machine/runtime profile digest;
- CPython patch/build and interpreter-payload manifest digest;
- base installer/pip payload identity;
- selected offline wheelhouse manifest digest and installed-payload manifest digest;
- exact allowlisted subprocess executable set;
- plugin-sufficiency inventory/tool/challenge-corpus identities and final approved explicit plugin list;
- result extractor/schema artifact identity;
- all observed baseline counts, collection manifest, semantic fingerprint, baseline source, and accepted anomaly register.

None may be copied from the provisional Windows run: it used Python 3.14.2 and pytest 9.0.2, while the lock pins pytest 9.1.1, and its own record says it is not the frozen-suite environment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:47-62`

Before either baseline run, the Lead/owner freeze authority must seal a read-only `P10_FREEZE_AUTHORITY_V2.json` and bind its exact path, bytes, SHA-256, schema version, and every referenced artifact identity into the authoritative dispatch manifest. Its literal future path is `UNKNOWN`. The freeze authority—not either operator and not the runtime verifier—supplies expected identities. Operators may only measure actual state and compare it with the sealed file. A missing/unreadable expected field is `BLOCK`, never a guessed value and never a suite `FAIL`.

The authority file must distinguish:

1. **normative choices** made by this contract;
2. **predeclared artifact facts** independently recomputed from sealed bytes before the runs;
3. **runtime observations** produced by each operator; and
4. **post-run adjudications**, which cannot retroactively change the contract used by that run.

A field produced by the same runtime process it is meant to check is corroboration only. It cannot be its own expectation.

## 1. Frozen suite and repository identity

The suite universe is exactly every item collected from `IBKR_PAPER_BRIDGE/tests` from repository-root CWD at the full frozen SHA, under this v2 environment and plugin contract. The README establishes repository-root CWD, `PYTHONUTF8=1`, and that explicit test path; `tests/conftest.py` inserts the Bridge root into `sys.path`. `IBKR_PAPER_BRIDGE/README.md:40-46`; `IBKR_PAPER_BRIDGE/tests/conftest.py:8-10`

The canonical in-capsule paths are normative choices, not derived current facts:

```text
P10_WORKTREE=/worktree
P10_BASE_PYTHON=/opt/p10/cpython/bin/python3.12
P10_PYTHON=/opt/p10/venv/bin/python
P10_WHEELHOUSE=/opt/p10/wheelhouse
P10_ALLOWBIN=/opt/p10/allowbin
P10_EVIDENCE=/evidence
```

The run is nonconforming unless `/worktree` is a fresh isolated worktree at the full frozen SHA, the exact-HEAD comparison succeeds, and pre/post `git status --porcelain` outputs are empty. Those are required Packet-10 isolation facts, not permission to use a different checkout. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63-65`

Before collection, re-scan the frozen repository root and `IBKR_PAPER_BRIDGE/` for `pyproject.toml`, `pytest.ini`, `tox.ini`, `setup.cfg`, `TSP1009B.pytest_tmp_s1r1`, and any other `pytest_tmp` member. The current-byte preflight found none but expressly requires the freeze-time rescan. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:24-27`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_CURRENT_BYTES_PREFLIGHT_2026-08-14.md:49-58`

**Failure rule:** an unexpected config/artifact is not ignored and no operator may add an ad hoc flag. It is a contract mismatch and therefore `BLOCK` pending a versioned contract amendment. A Git query that cannot be evaluated is also `BLOCK`; a completed query that observes the wrong SHA or dirt is a nonconforming-state result. Neither is acceptance.

## 2. Closed runtime and interpreter identity

### 2.1 Normative runtime choice

V2 chooses a content-addressed Linux/glibc `linux/amd64` execution image. `linux/amd64` and glibc are normative choices; they are not claimed to be derived from the lock. The lock itself specifies only Python 3.12 and `linux`, which is too broad and accepts multiple hashes for platform-bearing packages. `IBKR_PAPER_BRIDGE/requirements.lock:1-2`; `IBKR_PAPER_BRIDGE/requirements.lock:23-35`

An OCI digest alone does not pin the guest/host kernel or CPU surface visible to a container. Therefore a conforming capsule is the conjunction of:

- immutable image reference **by manifest digest**, never a mutable tag;
- exact image platform `linux/amd64`, rootfs/layer digests, and image-config digest;
- exact container/runtime executable identity and configuration digest;
- guest-visible kernel release, kernel build/config identity, architecture, libc/loader identity, CPU model/flag mask, cgroup mode, and filesystem/mount profile;
- the resource, identity, clock, and network profile in section 3.

Every literal digest/version above is currently `UNKNOWN (BLOCKING)`. The freeze authority must select and seal them before either operator runs. Two operators conform only if all actual values equal those same predeclared values.

### 2.2 CPython identity is a payload, not a version string

The image must contain the base interpreter at exactly `/opt/p10/cpython/bin/python3.12` and the prebuilt venv interpreter at `/opt/p10/venv/bin/python`. The following predeclared identities together define CPython:

- exact CPython distribution/provenance identifier, patch version, build string, compiler, build flags, ABI/SOABI, `sys.implementation` name/cache tag, and executable format/build ID;
- SHA-256 of the resolved base and venv interpreter executable bytes;
- a canonical full-tree manifest of `/opt/p10/cpython`, including each relative path, member type, mode, symlink target, byte count, and file SHA-256, with **no exclusions**;
- a canonical full-tree manifest of the immutable portions of `/opt/p10/venv`, including bootstrap tools, site-packages, scripts, metadata, and shared objects;
- exact dynamic loader, libc, libpython (if present), and every file-backed shared library mapped after importing pytest and the suite `conftest`, each by resolved path/bytes/SHA-256;
- `sys.version`, `sys.version_info`, `sys.executable`, `sys.prefix`, `sys.base_prefix`, `sys.platform`, `platform.machine()`, `platform.libc_ver()`, `platform.platform()`, `sysconfig.get_platform()`, `SOABI`, `MULTIARCH`, OpenSSL version, SQLite version, and default filesystem/locale encodings.

The expected tree manifests are made by an independent freeze-time verifier reading the sealed image/rootfs, then placed in the authority bundle. The runtime verifier walks the live mounted trees using the same canonical member grammar but writes only `actual`. It must compare expected and actual one-to-one and enforce the conservation equation:

```text
expected members = matching members + mismatching members + missing members
actual members   = matching members + mismatching members + unexpected members
```

`mismatching`, `missing`, or `unexpected` non-empty means `BLOCK`. An unreadable member or unrecognized member type is also `BLOCK`, not silently skipped. This prevents a verifier from passing over a reduced universe.

The outer runtime must also retain an inspection record binding the actual container instance to the predeclared image manifest digest. The inside-image manifest and post-run `sys.version` record remain corroboration; neither can substitute for the outer digest binding. This repairs v1’s post-hoc-only identity, identified at `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:21-27` and `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_2026-08-15.md:56-58`.

### 2.3 Runtime identity falsification

Before use, the identity verifier must be challenged against a scratch copy of the sealed payload by: changing one executable byte; deleting one stdlib file; adding one file; changing one symlink target; substituting one shared library; and changing the expected image digest. Every arm must produce the named mismatch or `BLOCK`. The unmodified payload must pass. Commands, stdout, stderr, and rc for RED and GREEN are retained. If a mutation is not detected, the identity proof is decorative and the suite may not collect.

## 3. Fresh capsule and closed process environment

### 3.1 Capsule controls

Each collection or execution starts from a newly instantiated immutable image with no reused writable layer or mutable volume except the fresh worktree and fresh evidence/tmp filesystems. The following are normative v2 choices:

| Surface | Frozen v2 treatment | Runtime proof and enforcement |
|---|---|---|
| CPU/concurrency | Exactly 1 visible vCPU; exact virtual CPU model and feature mask are blocking fields in the machine manifest. | Compare `os.cpu_count()`, affinity, cgroup cpuset/quota, and normalized CPU inventory to the authority file. Any difference BLOCKS. |
| Memory/swap/processes | Exactly 8 GiB memory, no swap, cgroup v2 `pids.max=256`. | Capture cgroup limits and in-process rlimits before collection; mismatch BLOCKS. Values are normative, not sourced measurements. |
| Rlimits | `NOFILE=1024:1024`, `NPROC=256:256`, `STACK=8388608:8388608`, `CORE=0:0`; all other limits must equal the exact predeclared machine-manifest values. | Capture all soft/hard rlimits. Missing/unparsed entries BLOCK; no “best effort.” |
| Umask | `077`. | Create a scratch sentinel without an explicit mode and require its effective permission to match the authority expectation; then remove it. A mode mismatch BLOCKS. |
| Process identity | UID/GID `1000:1000`, supplementary groups empty, `USER=LOGNAME=p10`, hostname `p10`. | Record numeric identities, group list, hostname, and `/proc/self/status`; mismatch BLOCKS. |
| Clock/timezone | Guest wall clock starts at `2026-08-15T00:00:00Z`, no time synchronization, `TZ=UTC`, and the selected UTC tzdata file hash is in the image manifest. | Compare RTC/start setting, `TZ`, resolved offset/name, and tzdata bytes. Runtime timestamps/durations are still raw evidence but excluded from the semantic fingerprint. |
| Filesystem | Worktree path `/worktree`; venv and interpreter trees read-only; canonical filesystem type/mount flags and case behavior recorded in the machine manifest. | Capture mount table and probe case sensitivity, symlink, mode, and newline byte behavior. Any mismatch or inability BLOCKS. |
| Home/XDG | `/run/p10/home` and each `/run/p10/xdg/*` are existing empty read-only directories. | Force-inclusive pre/post tree manifests must both have zero members. A member or unreadable directory BLOCKS. |
| Temp | Fresh writable tmpfs at `/run/p10/tmp`; `pytest --basetemp=/run/p10/tmp/pytest`. | Prove force-inclusive emptiness before run; retain post-run tree manifest; delete the run tree; prove force-inclusive emptiness after cleanup. Cleanup failure BLOCKS evidence finalization. |
| Network | No non-loopback network interface or route; loopback is the sole interface and is fixed up; no inherited sockets. | Record interface/route/socket inventory before and after. Any non-allowlisted interface, route, socket, or inability to inspect BLOCKS. |
| File descriptors/stdin | Only stdin/stdout/stderr plus explicitly manifested evidence descriptors; stdin is `/dev/null`. | Enumerate `/proc/self/fd`; unexplained descriptors BLOCK. Stdout/stderr are separate byte-preserving captures. |
| Wall-clock, RNG, machine-id consumers | Frozen-source inventory must enumerate reads of time, `random`, `secrets`, UUID, `/dev/*random`, hostname, machine-id, CPU count, environment, home, and temp. | Each member needs a terminal disposition: fixed input; mocked by existing suite code; proven not to reach compared fields; or `BLOCK`. Empty analyzer output is not proof of absence. |

The machine-profile expected values come from the sealed authority manifest. The current environment is not evidence for them.

### 3.2 Exact environment whitelist

The actual pytest process must be created with `env -i`. The only allowed environment entries are exactly the following key/value pairs; no operator-specific variable may pass through:

```text
HOME=/run/p10/home
USER=p10
LOGNAME=p10
XDG_CONFIG_HOME=/run/p10/xdg/config
XDG_CACHE_HOME=/run/p10/xdg/cache
XDG_DATA_HOME=/run/p10/xdg/data
XDG_STATE_HOME=/run/p10/xdg/state
TMPDIR=/run/p10/tmp
TMP=/run/p10/tmp
TEMP=/run/p10/tmp
PATH=/opt/p10/venv/bin:/opt/p10/allowbin
LANG=C.UTF-8
LC_ALL=C.UTF-8
TZ=UTC
TZDIR=/usr/share/zoneinfo
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONWARNINGS=default
COLUMNS=80
LINES=24
TERM=dumb
NO_COLOR=1
FORCE_COLOR=0
PY_COLORS=0
CLICOLOR=0
CLICOLOR_FORCE=0
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
VECLIB_MAXIMUM_THREADS=1
NUMEXPR_NUM_THREADS=1
BLIS_NUM_THREADS=1
MALLOC_ARENA_MAX=1
SOURCE_DATE_EPOCH=0
```

Because the process begins with `env -i`, `PYTHONHOME`, `PYTHONPATH`, `PYTEST_ADDOPTS`, `PYTEST_PLUGINS`, proxy variables, credential variables, shell startup variables, coverage variables, and every unnamed variable are absent by construction. The allowed environment is an exact set, not a minimum set.

`/opt/p10/allowbin` must itself be an immutable exact tree in the authority manifest. A frozen-source inventory must identify every external executable the suite can reach; each must map one-to-one to an allowbin member with path/bytes/SHA-256. An unresolved dynamic command, shell construction, or program lookup is `BLOCK`. No “not observed in one run” inference is allowed.

Before collection, an outer supervisor records `/proc/<pytest-pid>/environ` from the actual pytest process and compares its exact NUL-delimited set with the whitelist. The expected set comes from this contract/authority bundle, not from dumping the process. An added, missing, duplicate, undecodable, or changed entry BLOCKS. A negative control must add `P10_UNEXPECTED=1`; the comparer must reject it.

### 3.3 RNG and nondeterministic-input settlement

`PYTHONHASHSEED=0` and one visible vCPU are mandatory but do not prove that application/test RNGs are controlled. The frozen-source inventory must cover all collected test modules, imported `conftest` files, and repository modules they import under this exact run. For every time/RNG/system-identity input, the inventory must record source location, reachable consumer, provider, control, and whether it can change collection, node IDs, outcome, warning/anomaly signature, or compared payload.

- If an existing supported seed/control exists, its exact value joins the whitelist.
- If the value is intentionally variable but cannot reach any semantic-fingerprint field, its dataflow proof and excluded raw field are recorded.
- If reachability is unresolved, or a variable value can change a compared field without a frozen control, plugin sufficiency/result reproducibility is `UNKNOWN` and execution is `BLOCK`.

The inventory tool must fail closed on unparsed syntax/imports and be falsified with a synthetic module using each modeled RNG/time API plus one deliberately unsupported wrapper. The unsupported wrapper must produce an unresolved record and nonzero gate status, never an empty PASS.

## 4. Artifact-reproducible dependency installation

### 4.1 Policy choice

V2 explicitly chooses **artifact-reproducible installation with a pinned offline wheelhouse**. Integrity-checking against any hash accepted by the multi-platform lock is not accepted for Packet 10. There is no residual permission for online artifact selection.

This is stronger than v1’s command. The repository installer only adds `--no-index --find-links` when `WHEELHOUSE` is supplied. `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:292-306` The lock accepts multiple hashes for packages such as `bitarray`, and the repository verifier compares distribution names/versions while excluding pip and setuptools. `IBKR_PAPER_BRIDGE/requirements.lock:23-35`; `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:66-97`; `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:18-21`

### 4.2 Predeclared artifacts

Before image build, the freeze authority must seal:

1. the exact `requirements.lock` path/bytes/SHA-256;
2. an installer manifest covering base `venv`/`ensurepip`, pip, setuptools, build frontend, and every build-time executable by version/path/bytes/SHA-256;
3. one selected compatible wheel for every canonical lock distribution, with canonical name, version, exact filename, wheel tags, relative path, byte count, and SHA-256;
4. a force-inclusive wheelhouse directory manifest proving there are no extra, missing, symlinked, or non-regular members;
5. the expected pip install report identity;
6. an expected installed-payload manifest independently derived from the selected wheel archives and fixed installation rules, not generated by reading back the installed venv;
7. the final immutable venv tree manifest and final execution-image digest.

The literal selected artifacts/digests are `UNKNOWN (BLOCKING)`. The lock pins `pytest==9.1.1` and `anyio==4.14.2`, but those version facts do not choose a wheel artifact. `IBKR_PAPER_BRIDGE/requirements.lock:15-22`; `IBKR_PAPER_BRIDGE/requirements.lock:986-989`

The selected-wheel conservation rule is exact:

```text
lock distributions = selected compatible wheels
selected wheel filenames = wheelhouse regular-file members
```

Both equalities are one-to-one after canonical-name normalization. Duplicate canonical names, multiple selected wheels for one distribution, an unconsumed lock member, an extra wheel, an incompatible tag, or an unrecognized member type BLOCKS the build.

### 4.3 Fresh build and exact install form

The venv path must be absent, not merely “apparently empty,” before creation. A force-inclusive parent listing plus `lstat` must prove `/opt/p10/venv` does not exist. The image build then uses the absolute pre-identified interpreter and exact command:

```bash
/opt/p10/cpython/bin/python3.12 -m venv /opt/p10/venv
/opt/p10/venv/bin/python -m pip install \
  --require-hashes --no-deps --only-binary=:all: \
  --no-index --find-links=/opt/p10/wheelhouse \
  --no-input --no-cache-dir --disable-pip-version-check \
  --no-compile --report=/opt/p10/build/pip-install-report.json \
  -r /worktree/IBKR_PAPER_BRIDGE/requirements.lock
```

The base image digest and installer manifest pin the pip invoked by that command. No pip upgrade, index, cache, alternate link, or dependency re-resolution is allowed. The build has no network interface.

After install:

- verify every pip-report download/archive hash and filename against the selected-wheel manifest;
- run `verify_lock.py --check-installed` as a supplemental exact name/version check; the verifier’s real scope is documented at `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:75-98`;
- verify every installed distribution file against the independently wheel-derived payload manifest;
- verify bootstrap pip/setuptools and generated scripts against the installer manifest;
- enforce full-tree conservation: every actual venv member is expected or explicitly classified as a deterministic installer-generated member with an independently specified byte rule; no unexplained extra is allowed;
- seal the venv read-only, compute the final venv manifest, and seal the final image digest.

At run time, recompute the immutable venv tree and compare it to the predeclared final manifest. Installed name/version equality alone is insufficient.

### 4.4 Artifact falsification

The wheel/install verifier must demonstrate RED for each of: one changed wheel byte; one renamed wheel; one extra wheel; one missing wheel; two wheels for one canonical distribution; changed pip bytes; a pre-existing venv; one changed installed `.py`; one added site-packages member; and a pip report naming a nonmanifested artifact. It must demonstrate GREEN only on the sealed artifact set. The expected values come from the authority manifest; the verifier may not regenerate them after mutation.

## 5. Explicit pytest plugin set and sufficiency proof

### 5.1 Current contract state

Keep the real v1 improvement:

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
-p anyio.pytest_plugin
-p no:cacheprovider
```

The lock establishes that `anyio==4.14.2` is present and pytest is 9.1.1. `IBKR_PAPER_BRIDGE/requirements.lock:15-22`; `IBKR_PAPER_BRIDGE/requirements.lock:986-989` The inspected root `conftest.py` uses pytest’s built-in `monkeypatch` fixture and declares no third-party plugin itself. `IBKR_PAPER_BRIDGE/tests/conftest.py:6-21` Those facts do **not** establish whole-suite plugin sufficiency. The frozen explicit list is therefore:

```text
candidate explicit third-party list = [anyio.pytest_plugin]
sufficiency status = UNKNOWN (BLOCKING)
```

No operator may silently add a plugin to make collection pass. If the procedure below finds another required provider, the authority must amend and reseal the explicit list before either baseline run.

### 5.2 Universe and proof procedure

Plugin sufficiency quantifies over exactly: all frozen-SHA files in `IBKR_PAPER_BRIDGE/tests`; every discovered `conftest.py`; every active frozen pytest configuration file; every item collected under sections 1–3; and setup/call/teardown for every item executed under the exact v2 command. It does **not** claim sufficiency for another SHA, OS, Python build, environment, option set, or test path.

Sufficiency is established only when all steps below pass:

1. **Declare the source universe once.** Create a force-inclusive path/bytes/SHA-256 manifest of every test, conftest, and pytest configuration member. Every admitted member must receive one terminal inventory disposition.
2. **Static inventory, fail closed.** A pinned inventory tool scans the complete universe for fixture parameters, `usefixtures`, `pytest_plugins`, `pytest.mark.*`, hook implementations/specifications, plugin-manager calls, plugin-provided CLI/config options, dynamic imports, and generated test/marker names. Each usage maps to pytest core, a frozen conftest/local definition, or an exact explicit third-party provider. Unparsed syntax, unresolved imports, dynamic names, or unknown provider mappings produce `UNKNOWN/BLOCK`; zero findings is never proof by itself.
3. **Installed-entry-point inventory.** Enumerate every installed `pytest11` entry point as name, module value, distribution name/version, and distribution payload digest. This describes what could load; it does not prove what did load.
4. **Actual loaded-plugin capture.** Under the exact `env -i` whitelist and explicit `-p` flags, run pytest’s trace-config/collection probe and capture a machine-readable plugin-manager manifest after configuration and after collection. Record every loaded plugin module/object, provider distribution or built-in provenance, version, path, and payload digest. The loaded third-party set must equal the authority-approved explicit set; built-ins must equal the predeclared pytest-9.1.1 built-in manifest. An unexpected or missing member BLOCKS.
5. **Strict collection.** Execute the exact collection command with `--strict-config --strict-markers`, retain the ordered node IDs, and run the fixture-resolution view for every collected item. Every fixture/marker/provider must resolve to the static inventory. Collection errors, warnings about unknown markers/config, unresolved fixtures, a changed item universe, or inability to attribute a provider BLOCKS.
6. **Exact full execution.** Execute the mandated suite with autoload disabled. A completed green execution corroborates that the list supports this exact collected/executed universe; it does not replace steps 1–5.
7. **Independent pair.** Repeat steps 4–6 in the second clean capsule. Loaded-plugin manifests, canonical collection manifests, and semantic fingerprints must match exactly.

### 5.3 Proof-instrument falsification

The inventory/capture tools themselves require a sealed synthetic challenge corpus outside the frozen worktree. It must contain at least one fixture parameter, `usefixtures`, marker, `pytest_plugins` declaration, hook, plugin CLI/config option, dynamic provider name, duplicate provider identity, and unsupported construct. For each modeled construct, omit or replace its provider and require a named unresolved/mismatch result. The unsupported construct must produce `UNKNOWN/BLOCK`, not empty output. Add one unexpected loaded plugin and require the loaded-set comparator to reject it. Then run the unmutated corpus GREEN.

The challenge corpus, tools, expected outputs, commands, stdout/stderr, and rc identities are blocking freeze-authority fields. Their current values are `UNKNOWN`. Until RED and GREEN are recorded, the tool evidence is supplemental and plugin sufficiency remains `UNKNOWN`.

## 6. Exact collection and execution commands

The capsule setup, rlimits, umask, clock, mounts, and emptiness checks in section 3 happen before these commands. `/bin/bash`, `/usr/bin/env`, and every setup/supervisor tool are absolute, immutable image members in the machine manifest.

### 6.1 Collection command

```bash
/bin/bash --noprofile --norc -c '
  set -eu
  umask 077
  cd /worktree
  exec /usr/bin/env -i \
    HOME=/run/p10/home USER=p10 LOGNAME=p10 \
    XDG_CONFIG_HOME=/run/p10/xdg/config \
    XDG_CACHE_HOME=/run/p10/xdg/cache \
    XDG_DATA_HOME=/run/p10/xdg/data \
    XDG_STATE_HOME=/run/p10/xdg/state \
    TMPDIR=/run/p10/tmp TMP=/run/p10/tmp TEMP=/run/p10/tmp \
    PATH=/opt/p10/venv/bin:/opt/p10/allowbin \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC TZDIR=/usr/share/zoneinfo \
    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONWARNINGS=default \
    COLUMNS=80 LINES=24 TERM=dumb NO_COLOR=1 FORCE_COLOR=0 PY_COLORS=0 \
    CLICOLOR=0 CLICOLOR_FORCE=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    BLIS_NUM_THREADS=1 MALLOC_ARENA_MAX=1 SOURCE_DATE_EPOCH=0 \
    /opt/p10/venv/bin/python -m pytest IBKR_PAPER_BRIDGE/tests \
      --collect-only -q --strict-config --strict-markers --color=no \
      --basetemp=/run/p10/tmp/pytest \
      -p anyio.pytest_plugin -p no:cacheprovider
'
```

Run the separate loaded-plugin trace and fixture-resolution probes with the identical shell, CWD, environment, test path, strict flags, basetemp policy, and `-p` list; only the named diagnostic option may differ. The exact diagnostic argv and pinned parser identity must be predeclared in the authority file. An operator cannot improvise them.

### 6.2 Mandated execution command

```bash
/bin/bash --noprofile --norc -c '
  set -eu
  umask 077
  cd /worktree
  exec /usr/bin/env -i \
    HOME=/run/p10/home USER=p10 LOGNAME=p10 \
    XDG_CONFIG_HOME=/run/p10/xdg/config \
    XDG_CACHE_HOME=/run/p10/xdg/cache \
    XDG_DATA_HOME=/run/p10/xdg/data \
    XDG_STATE_HOME=/run/p10/xdg/state \
    TMPDIR=/run/p10/tmp TMP=/run/p10/tmp TEMP=/run/p10/tmp \
    PATH=/opt/p10/venv/bin:/opt/p10/allowbin \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC TZDIR=/usr/share/zoneinfo \
    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONWARNINGS=default \
    COLUMNS=80 LINES=24 TERM=dumb NO_COLOR=1 FORCE_COLOR=0 PY_COLORS=0 \
    CLICOLOR=0 CLICOLOR_FORCE=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    BLIS_NUM_THREADS=1 MALLOC_ARENA_MAX=1 SOURCE_DATE_EPOCH=0 \
    /opt/p10/venv/bin/python -m pytest IBKR_PAPER_BRIDGE/tests \
      -q -ra --strict-config --strict-markers --color=no \
      --basetemp=/run/p10/tmp/pytest \
      -p anyio.pytest_plugin -p no:cacheprovider
'
```

`P10_WORKTREE`, interpreter path, PATH, and all formerly ambient fields are literals. `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and the explicit plugin list are retained. No auditor may choose a substitute command; inability to execute the mandated suite is `BLOCK`, not acceptance. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:102-104`

## 7. Raw evidence and versioned machine-readable result

### 7.1 Byte-exact provenance retained

For collection, every plugin probe, every preflight verifier, and each suite run, retain separately:

- exact argv as a JSON string array, exact CWD, exact environment mapping, actual process rlimits/affinity/identity, and the supervisor’s process-environment capture;
- UTC outer start/end timestamps, guest timestamps, monotonic elapsed time, and pytest-reported duration;
- byte-preserved stdout and stderr, each exact path/byte count/SHA-256, and process rc;
- frozen SHA, worktree path, exact-HEAD proof, pre/post cleanliness bytes;
- image/machine/interpreter/venv/lock/installer/wheelhouse/installed-payload identities and all verifier transcripts;
- installed entry points, actual loaded plugins, plugin-source inventory, challenge-corpus RED/GREEN evidence;
- ordered collection node IDs and every outcome/warning/anomaly fact;
- a force-inclusive evidence manifest giving each retained member a unique role, relative path, byte count, and SHA-256.

This preserves what happened. Raw output hashes are provenance identities, not cross-run equality fields, because durations and timestamps legitimately vary; the provisional record demonstrates that duration is not stable. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:72-82`

### 7.2 Result schema

Each run must also produce one UTF-8 JSON document conforming to `p10-suite-result-v2`. The schema artifact’s future path/bytes/SHA-256 and the extractor’s future path/bytes/SHA-256 are `UNKNOWN (BLOCKING)` until sealed in the authority manifest. The document must contain at least:

```text
schema_version
contract_document_sha256
freeze_authority_sha256
full_frozen_sha
image_digest
machine_profile_digest
interpreter_payload_manifest_sha256
venv_payload_manifest_sha256
requirements_lock_sha256
installer_manifest_sha256
wheelhouse_manifest_sha256
installed_payload_manifest_sha256
normalized_argv
exact_environment_whitelist
resource_profile
explicit_plugin_manifest
actual_loaded_plugin_manifest_sha256
plugin_sufficiency_inventory_sha256
collection_manifest_sha256
counts: collected, executed, passed, failed, skipped, xfailed, xpassed,
        errors, warnings, deselected
ordered_collection_node_ids
ordered_nonpass_records: node_id, terminal outcome, phase
ordered_warning_signatures
ordered_anomaly_signatures
extractor_path, extractor_bytes, extractor_sha256
```

Every collected item must have exactly one selected/deselected disposition. Every selected item must have one record containing explicit setup, call, and teardown phase states; `not_run` is an explicit state, not an omitted member. The schema retains both pytest’s reported summary counts and a canonical mutually exclusive final node outcome. The canonical precedence is: collection/setup/teardown error → `error`; otherwise unexpected call failure → `failed`; expected-failure result → `xfailed`; unexpected pass under an expected-failure marker → `xpassed`; ordinary skip → `skipped`; ordinary successful call → `passed`. A selected item with no classifiable terminal state is unresolved, not silently dropped. The extractor enforces:

```text
collected = selected + deselected
selected  = passed + failed + skipped + xfailed + xpassed + errors + unresolved
executed  = selected items whose call phase has a report, including call-phase skip/xfail
```

The phase records preserve coexisting facts such as a passed call followed by teardown error even though the exclusive canonical outcome is `error`. `unresolved` must be zero for a complete baseline; otherwise the result is `BLOCK`. Pytest-reported and canonical counts are both fingerprinted, so an extractor cannot hide a disagreement by choosing the more convenient accounting.

### 7.3 Canonical semantic fingerprint

Canonicalize the result document as UTF-8 JSON with sorted object keys, no insignificant whitespace, LF line ending, and arrays in the explicit order stated by the schema. SHA-256 those canonical bytes after excluding only these run-instance fields:

- outer/guest timestamps;
- monotonic/pytest durations;
- raw stdout/stderr/evidence paths, byte counts, and hashes, plus the outer operator worktree bind-source path;
- container/process IDs and other explicitly named ephemeral instance identifiers.

Nothing else may be regex-redacted. Worktree, interpreter, home, temp, and evidence mount paths are already canonical literals. Warning signatures are `(category, exact message, repository-or-distribution-relative file, line)`. Anomaly signatures are `(node_id, phase, exception/assertion type, exact normalized message, repository-relative top file, line)`. Text is decoded strictly as UTF-8 and line endings are normalized to LF only for these semantic strings; undecodable or unparsable output is `BLOCK`. Raw bytes remain untouched in provenance.

The fingerprint binds the frozen SHA; all image/interpreter/lock/wheel/install/plugin identities; normalized argv/environment/resources; collection manifest; all exact counts including warnings and deselection; every non-pass node; and normalized warning/anomaly signatures. This supplies the comparison rule missing from v1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:78-86`

### 7.4 Extractor falsification

The extractor requires an independently authored sealed fixture corpus covering every outcome, collection error, setup/call/teardown error, skip, xfail, xpass, warning, deselection, duplicate node ID, undecodable stream, truncated stream, and inconsistent summary. For each field, mutate the raw fixture while holding the expected result fixed; the extractor must either change the corresponding result/fingerprint or BLOCK. It must reject every conservation violation and every admitted member lacking a terminal disposition. Then the unmutated corpus must reproduce the predeclared result bytes exactly.

The corpus expectation is sealed by the freeze authority before the extractor run. The extractor may not generate both fixture and expectation. Until real RED/GREEN commands and outputs exist, extractor-derived results are supplemental and cannot establish the baseline.

## 8. Two-run reproducibility gate and baseline fields

### 8.1 Independent-run rule

After every blocking `UNKNOWN` in sections 0–7 is filled and sealed, two different operators independently instantiate clean capsules from the same immutable image and authority bundle. They may not share a writable layer, venv, home/XDG/temp tree, worktree, evidence directory, or prior-run output. Each performs the full preflight, plugin proof, collection, and mandated execution.

The gate requires exact equality of:

- authority, image, machine, interpreter, dependency, environment, resource, and plugin identities;
- canonical ordered collection manifests;
- complete `p10-suite-result-v2` semantic documents after only the named run-instance exclusions;
- canonical semantic fingerprint.

One run cannot create an expectation and then “verify” itself. Run 1 proposes an observation; Run 2 independently challenges it. Only after equality and separate Lead/owner adjudication may the pair become `BASELINE_SOURCE`. A difference is a reproducibility deviation and remains non-accepting. An inability to compare is `BLOCK`. No field may be cherry-picked from one run.

### 8.2 Definition-time baseline

| Field | V2 value before the independent pair |
|---|---|
| `MANDATED_COMMAND` | Exact section 6.2 command. |
| `CONTRACT_TARGET_EXIT_CODE` | `0`; a green exact-frozen-SHA locked-environment run remains required. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72` |
| `CONTRACT_TARGET_FAIL_COUNT` | `0`; this is a target, not an observed accepted anomaly set. |
| `EXPECTED_EXIT_CODE` | `UNKNOWN` as a frozen observation until the independent pair and adjudication. |
| `EXPECTED_COLLECTED_COUNT` | `UNKNOWN`. |
| `EXPECTED_EXECUTED_COUNT` | `UNKNOWN`. |
| `EXPECTED_PASS_COUNT` | `UNKNOWN`. |
| `EXPECTED_FAIL_COUNT` | `UNKNOWN`. |
| `EXPECTED_SKIP_COUNT` | `UNKNOWN`. |
| `EXPECTED_XFAIL_COUNT` | `UNKNOWN`. |
| `EXPECTED_XPASS_COUNT` | `UNKNOWN`. |
| `EXPECTED_ERROR_COUNT` | `UNKNOWN`. |
| `EXPECTED_WARNING_COUNT` | `UNKNOWN`. |
| `EXPECTED_DESELECTED_COUNT` | `UNKNOWN`. |
| `EXPECTED_COLLECTION_MANIFEST_SHA256` | `UNKNOWN`. |
| `EXPECTED_LOADED_PLUGIN_MANIFEST_SHA256` | `UNKNOWN`. |
| `EXPECTED_SEMANTIC_FINGERPRINT` | `UNKNOWN`. |
| `EXPECTED_FAILURES` | `UNKNOWN`; an empty set must be observed and adjudicated, not prefilled. Packet P10-12 requires that rule. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:64` |
| `ACCEPTED_ANOMALY_REGISTER` | `UNKNOWN`; this contract accepts none. |
| `BASELINE_SOURCE` | `UNKNOWN`; future exact path/bytes/SHA-256 of the adjudicated two-run package. |

The auditor input requires exact command, exit/pass/fail/skip/xfail fields and baseline source from one authoritative frozen source; no auditor may infer them. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:84-104`

## 9. Known anomalies and fail-closed adjudication

The historical anomalies remain conditional expectations only:

- **A1:** ledger-schema working-tree CRLF hash mismatch; the accepted repair pins the path to LF. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:19-24`
- **A2:** stale hardcoded schema-version assertion; the accepted repair derives the version from the fixture database. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:26-29`

If the frozen SHA contains both accepted repairs and the checkout is fresh, A1 and A2 are expected absent. That is not a frozen observation: the repair record says the work was accepted at T1 but not merged and that an exact-frozen-SHA locked-environment green run remained outstanding. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:3-17`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72`

Adjudication is fail-closed:

1. Record every observed anomaly using the exact structured and raw evidence fields. Never silently convert A1/A2 or any new result into an expected failure.
2. First verify frozen SHA, repair bytes/semantics, capsule/interpreter/dependency/plugin/environment identity, collection universe, and evidence completeness.
3. Root-cause and reproduce against exact frozen bytes. Only separately recorded Lead/owner authority may accept an anomaly; this document supplies none.
4. Record a zero-anomaly result as an observed empty set, then adjudicate it. Do not derive emptiness from the target.
5. A suite that completes with a deviation is evidence of a deviation. A probe that cannot evaluate is `BLOCK`. Do not confuse the two.

## 10. Check semantics and falsifiability ledger

| Gate/check | Quantified universe | Independent expectation source | What makes it fail | Inability treatment |
|---|---|---|---|---|
| Frozen worktree identity | Exact `/worktree` Git state and frozen file universe. | Sealed full SHA/file manifest in freeze authority. | Wrong SHA, dirty status, missing/extra/mutated member. | `BLOCK`; never assume clean/current. |
| Capsule identity | Image plus machine/kernel/CPU/libc/runtime profile. | Independently recomputed sealed image/machine manifest. | Any digest/profile mismatch. | `BLOCK`. |
| Interpreter payload | Every member of base Python/venv immutable trees and mapped libraries. | Pre-run payload manifests from sealed rootfs. | Mutated/missing/extra/unreadable member or value mismatch. | `BLOCK`. |
| Wheel/install payload | Every lock distribution, selected wheel, installer member, and venv member. | Lock + preselected wheel/installer/payload manifests. | Non-bijection, altered artifact, reused venv, wrong installed byte. | `BLOCK`. |
| Environment closure | Exact process environment and all machine/resource controls in sections 3 and 6. | Literal v2 whitelist plus sealed machine profile. | Added/missing/changed env entry or control. | `BLOCK`. |
| Plugin sufficiency | Exact collected/executed frozen-suite universe under v2. | Frozen-source usage inventory mapped to approved providers. | Unresolved usage/provider, loaded-set mismatch, strict collection/execution failure. | Remains `UNKNOWN`; execution `BLOCK`. |
| Collection conservation | Every source-universe member and collected item. | Frozen source manifest plus pytest collection. | Unexplained source/item disappearance, duplicate identity, order/hash mismatch across runs. | `BLOCK`. |
| Result extraction | Every admitted event/outcome/warning/anomaly and raw evidence member. | Independently sealed extractor fixture expectations. | Mutation not reflected, conservation violation, missing disposition, schema mismatch. | `BLOCK`. |
| Reproducibility | Two independent clean conforming runs. | Neither run alone; equality against the shared authority and each other. | Any semantic-document/fingerprint mismatch. | `BLOCK`; no baseline. |

These checks make no claim outside their named universe. In particular, v2 does not prove behavior on Windows, another architecture, another SHA, another plugin/options set, a mutable/online dependency source, or an unmanifested executable. Those are outside the contract, not silently passing cases.

## 11. Runtime estimate

**NO SOURCED ESTIMATE.** The only measured runs were 85.53–100.01 seconds in the invalid Windows Python-3.14.2/pytest-9.0.2 environment, and that record says duration is not stable. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:72-82`

What settles an estimate is a measured isolated execution under the fully populated v2 authority bundle. That measurement is run-specific evidence, not part of the semantic fingerprint and not acceptance.
