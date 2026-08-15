# Packet 10 mandated-suite contract v3

Status: SUITE CONTRACT V3 - SUPERSEDES V2 - NOT ACCEPTED

Audit tier: **T2** (documentation/evidence). This document defines a future
offline suite procedure. It is not an execution record, acceptance verdict,
release decision, authorization, or permission for any host, network, SSH,
deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet,
Pine, parity, MTC, trading, merge, push, or economic action.

## 0. V3 decision and present state

The controlling requirement is one sentence:

> Two operators following this contract exactly must not be able to vary any
> input that can change a field recorded by the Packet-10 baseline.

V2 did not meet that requirement. It cleared the pytest child's environment
only after an outer Bash had started, so `BASH_ENV` or other ambient startup
state could act first. It also accepted a clean Git worktree without defining
the full raw member/byte identity of the files actually executed.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:31-39`

V3 makes four binding choices:

1. **No shell is in the launch path.** A sealed, statically linked launcher and
   a sealed in-capsule supervisor use direct `execve` calls with exact argv and
   environment arrays. Bash, `env`, operator profiles, and operator commands do
   not participate.
2. **No operator checkout is executed.** Both operators mount the same
   content-addressed, read-only worktree payload. Its complete filesystem
   member/byte manifest is independently bound to the full frozen Git tree.
3. **Dependency installation is artifact-reproducible, not merely
   integrity-checked.** One selected offline wheel per locked distribution is
   frozen, and two clean builds must produce identical full venv payloads.
   There is no online or alternate-wheel residual.
4. **The explicit pytest plugin set is a proved freeze artifact, not an
   operator guess.** `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` remains mandatory. The
   candidate third-party list remains exactly `[anyio.pytest_plugin]`, but no
   baseline run may occur until a fail-closed source/dynamic proof establishes
   that this list is sufficient for the exact frozen suite.

These are normative choices, not facts derived from the present workstation.
The v1 review required an empty-environment launcher, an exact runtime payload,
an explicit decision between integrity and artifact reproducibility, a proven
plugin set, and stable comparison semantics.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:9-58`;
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:74-88`

### 0.1 Blocking unknowns

The following literal identities remain **UNKNOWN (BLOCKING)** because no
permitted source establishes them:

- full frozen repository SHA and frozen Git-tree manifest identity;
- raw worktree payload, manifest, filesystem-image bytes, and SHA-256;
- immutable execution image digest and complete machine/capsule profile;
- outer launcher, low-level runtime, OCI configuration, in-capsule supervisor,
  verifier, and attestor identities;
- exact CPython patch/build/distribution and full interpreter payload manifest;
- installer/pip/build-capsule identities;
- selected offline wheelhouse and twice-reproduced venv payload identities;
- exact allowed executable set;
- final plugin-sufficiency inventory, proof-tool/challenge identities, and
  authority-approved explicit plugin manifest;
- result schema, event recorder, extractor, normalizer, and comparator identities;
- observed collection, loaded-plugin, outcome, warning/anomaly, normalized-stream,
  and semantic-fingerprint values;
- accepted anomaly register and final `BASELINE_SOURCE`.

The provisional Windows record cannot fill any of those values: it used Python
3.14.2 and pytest 9.0.2 while the lock pins pytest 9.1.1, and the record calls
itself non-frozen. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:62-77`

Therefore **no conforming baseline run exists yet**. `UNKNOWN` is never replaced
with a locally convenient value. Missing, unreadable, ambiguous, or
self-produced expected data is `BLOCK` before collection.

## 1. Independent authority and state machine

Before any run, the Lead/owner freeze authority must publish one read-only
`P10_FREEZE_AUTHORITY_V3.json` and bind its exact path, bytes, SHA-256, schema,
and every referenced artifact into the authoritative dispatch manifest. Its
future literal path and digest are `UNKNOWN`.

The authority must distinguish:

- `normative`: literal choices made by this contract;
- `expected`: identities independently recomputed from sealed artifacts before
  either operator runs;
- `actual`: operator-run observations, never usable as their own expectations;
- `adjudicated`: post-run owner/Lead decisions, which cannot rewrite the
  contract used by either run.

The expected-value channel is one-way:

```text
frozen Git objects + selected sealed artifacts
        -> independent freeze verifiers
        -> P10_FREEZE_AUTHORITY_V3.json
        -> two read-only operator runs measure actual state
        -> exact comparison
```

Neither operator, the runtime supervisor, nor the result extractor may generate
an expected identity from the actual object it is checking. That is the
self-confirming defect named at
`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:31-52`.

The only legal state progression is:

```text
DRAFT -> AUTHORITY_SEALED -> INSTRUMENTS_FALSIFIED -> PLUGINS_PROVEN
      -> RUN_1_COMPLETE -> RUN_2_COMPLETE -> REPRODUCIBLE_PAIR
      -> SEPARATELY_ADJUDICATED_BASELINE
```

Any failed preflight comparison, unavailable check, unresolved inventory member,
or proof-tool falsification failure transitions to `BLOCKED`. A completed suite
deviation is recorded as a suite observation and remains non-accepting; it is
not misreported as inability to evaluate.

## 2. Frozen repository and raw worktree identity

The suite universe is every item collected from `IBKR_PAPER_BRIDGE/tests` from
repository-root CWD. The repository README supplies that CWD/test-path form and
`PYTHONUTF8=1`; the root conftest inserts the Bridge root into `sys.path`.
`IBKR_PAPER_BRIDGE/README.md:40-46`; `IBKR_PAPER_BRIDGE/tests/conftest.py:8-10`

### 2.1 One payload, not two checkouts

The freeze producer must construct one canonical, read-only worktree filesystem
image directly from the full frozen Git tree. Operators may not run checkout,
clone, reset, clean, autocrlf conversion, smudge/clean filters, submodule update,
or LFS materialization. The normative materialization is:

- Git regular blobs become regular files with the exact blob bytes;
- Git executable blobs have mode `0755`; non-executable blobs have mode `0644`;
- Git symlink blobs become symlinks whose target bytes equal the blob bytes;
- tree directories use one authority-declared mode/owner/time policy;
- a submodule, unsupported Git mode, path collision, undecodable path, filter
  requirement, or special member is `BLOCK` unless a later versioned contract
  defines it;
- no untracked, ignored, generated, cache, `.pyc`, or tool-created member exists;
- Git administrative data is outside the test-visible `/worktree` namespace.

This removes the line-ending ambiguity exposed by `* text=auto`.
`.gitattributes:1-2` A clean Git status alone is supplemental; it is not raw-byte
identity. The v2 review specifically found that two clean worktrees could
materialize different bytes. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_AND_SUITE_V2_REVIEW_2026-08-16.md:35-35`

### 2.2 Canonical worktree manifest

The expected manifest declares the universe once. Each member record contains:

```text
relative_path_utf8_bytes, git_mode, git_object_id, member_type,
mode, uid, gid, byte_count, sha256, symlink_target_bytes,
hardlink_group, mtime_ns, xattrs, acl, capabilities
```

Fields inapplicable to a member are explicit `null`, never omitted. Paths are
relative, slash-separated, NUL-free, unique byte strings; `.` and `..` path
components are forbidden. Records sort by raw relative-path bytes. The manifest
also binds the full frozen commit SHA, root tree object ID, filesystem-image
bytes/SHA-256, manifest grammar/version, and builder/verifier identities.

An independent verifier walks both the frozen Git tree and the filesystem image
without following symlinks and enforces:

```text
Git tree members = image payload members
expected members = matching + mismatching + missing
actual members   = matching + mismatching + unexpected
```

Every admitted Git member receives exactly one image disposition. Duplicate,
missing, extra, unreadable, unrecognized, or overwritten identities `BLOCK`.
This is enforced exact-set conservation, not an assertion.

At run time `/worktree` is a read-only mount of those same sealed image bytes at
the literal path `/worktree`. The supervisor recomputes the complete live
manifest before and after pytest and compares it to the sealed expectation.
Mount identity, flags, filesystem type, case behavior, Unicode/path behavior,
symlink behavior, stat-visible metadata, and read-only enforcement are also
compared with the machine profile. Any write attempt or pre/post difference
invalidates the run.

The Packet-10 scope separately requires proof that execution used the frozen SHA
and records exact command/environment/output facts.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-65`

### 2.3 Worktree falsification

Before use, the real top-level verifier must be run against scratch copies with:

- one changed blob byte;
- one CRLF materialization replacing an LF blob;
- one missing, extra, renamed, mode-changed, and symlink-retargeted member;
- one duplicate/colliding path identity;
- one changed root-tree or frozen-commit identity;
- one unreadable directory and one unsupported member type.

Each mutation must produce the named mismatch or `BLOCK`; the unmodified payload
must pass. Expected values stay sealed during every mutation. Commands, stdout,
stderr, rc, and mutated member identity are retained.

## 3. Closed launch chain: ambient state cannot run first

### 3.1 No-shell launch architecture

V3 forbids `/bin/bash`, `/bin/sh`, `/usr/bin/env`, PowerShell, command strings,
and operator-authored wrappers from the accepting launch path. The only allowed
chain is:

```text
authority dispatch controller
  execve(sealed static P10 launcher, sealed argv, envp=[])
    execve(sealed static low-level runtime, sealed argv, envp=[])
      sealed OCI config starts static /opt/p10/supervisor as PID 1
        supervisor forks exactly once; PID 2 directly execve(
          /opt/p10/venv/bin/python, exact argv, exact envp)
```

The launcher, low-level runtime, and supervisor are statically linked and have
no ELF interpreter, constructors, plugin/config search, shell expansion, or
environment-dependent startup path. Their exact executable bytes, source/build
provenance, argv grammar, and configuration bytes are authority artifacts.
Dynamic linkage in any of the three is `BLOCK`.

The dispatch controller passes an empty environment directly to the launcher.
The launcher first validates: `envp` is empty; argv equals the sealed vector;
CWD, root, namespace, umask, signal mask/dispositions, session/process group,
stdin/stdout/stderr types, open-fd set, and executable identity equal the
authority profile. It closes every nonmanifested fd before starting the runtime.
It passes an empty environment to the low-level runtime. The OCI config, not an
operator CLI, supplies the in-capsule process argv, empty supervisor environment,
CWD, user, mounts, resources, capabilities, and security policy.

The outer attestor independently records the actual launcher/runtime executable
bytes, OCI config bytes, image manifest digest, instance-to-image binding, and
machine profile. The in-capsule supervisor cannot substitute its own statement
for that outer binding.

**What makes this fail:** use a shell, set `BASH_ENV`, add `LD_PRELOAD`, alter
argv, change an fd/redirection, invoke a different runtime/image/config, or start
the supervisor with any environment entry. The direct launcher or outer attestor
must reject before collection. A negative control launches with
`BASH_ENV=/tmp/marker` and a marker-writing file; no marker may be created and
the environment mismatch must `BLOCK`.

### 3.2 Capsule identity

V3 retains the v2 normative platform choice: content-addressed Linux/glibc
`linux/amd64`. The lock itself establishes only Python 3.12 on broad `linux`, so
it does not select the platform-bearing artifacts.
`IBKR_PAPER_BRIDGE/requirements.lock:1-2`;
`IBKR_PAPER_BRIDGE/requirements.lock:23-35`

A conforming capsule requires one predeclared value for every row below:

| Surface | Normative treatment | Runtime enforcement |
|---|---|---|
| Image/runtime | OCI manifest digest, config digest, rootfs/layer digests, runtime/launcher bytes. | Outer attestation exact comparison; inner report is corroboration only. |
| Kernel/architecture | Exact guest-visible kernel release/build/config, `linux/amd64`, libc/loader, cgroup mode. | Machine probe compared to authority; unreadable/mismatch `BLOCK`. |
| CPU | Exactly one visible vCPU; exact model, flags, microcode/virtualization profile, affinity and cpuset/quota. | Compare `/proc`, affinity, cgroup, `os.cpu_count()`, and Python platform values. |
| Memory/processes | Exactly 8 GiB, no swap, cgroup-v2 `pids.max=256`. | Exact cgroup and process-view comparison. |
| Rlimits | `NOFILE=1024:1024`, `NPROC=256:256`, `STACK=8388608:8388608`, `CORE=0:0`; every other limit authority-pinned. | Enumerate all soft/hard limits; missing/unparsed value `BLOCK`. |
| Identity | UID/GID `1000:1000`, no supplementary groups, hostname `p10`, fixed PID namespace/layout. | Numeric ID, groups, hostname/domain, PID/TID, session and `/proc/self/status` comparison. |
| Privilege | Empty capabilities, `no_new_privs=1`, exact seccomp/LSM/personality/ASLR policy, fixed nice/scheduler policy. | Exact process/security-state comparison. |
| Clock | `TZ=UTC`; fixed capsule RTC/start epoch; no time sync; exact UTC tzdata. | Compare clocks, offset/name and tzdata. Reachable time reads require section 5 disposition. |
| Locale | `LANG=LC_ALL=C.UTF-8`; no other `LC_*`; exact libc/locale payload. | Capture resolved locale categories/encodings and compare to authority. |
| Filesystems | Exact rootfs/mount table, read-only worktree/interpreter/venv/allowbin, fixed case/symlink/newline semantics. | Full mount capture and behavioral probes; inability/mismatch `BLOCK`. |
| Home/XDG | Existing empty read-only `/run/p10/home` and `/run/p10/xdg/{config,cache,data,state}`. | Force-inclusive pre/post manifests must both be empty. |
| Temp | Fresh tmpfs `/run/p10/tmp`; exact size/options; canonical basetemp. | Empty before; complete post manifest retained; cleanup to empty required. |
| Evidence | Fresh fixed-type `/evidence` mount, empty before launch, root-owned and inaccessible to pytest UID 1000 after the supervisor opens canonical write-only captures. | Child sees only the manifested stdout/stderr fds; pre/post evidence-member conservation and fd target/flag checks. |
| Network | Network namespace with only fixed loopback; no non-loopback interface/route, DNS path, inherited socket, or network capability. | Interface/route/socket inventories before/after; any other member or inability `BLOCK`. |
| NSS/system files | Exact `/etc/passwd`, group, nsswitch, hosts, resolv, certificates, locale and timezone bytes from sealed image. | Files are in the image manifest; resolved identity probes must match. |
| FDs/terminal | stdin `/dev/null`; stdout/stderr fixed non-TTY regular captures; exact flags/modes; no other child fd. | `/proc/<pid>/fd` exact-set comparison and `isatty`/terminal probe. |
| Signals/process | Exact signal mask/dispositions, umask `077`, CWD `/worktree`, process group/session and parent-death policy. | Supervisor sets and then measures every value before child import. |
| Executables | Exact absolute-path allowlist and payload identities; no ambient command search. | Source inventory plus actual `execve` event ledger exact-set comparison. Unexpected execution invalidates run. |

All non-normative literal digests/profile values are currently `UNKNOWN
(BLOCKING)`. The current machine is not their source.

### 3.3 Exact pytest environment

The supervisor passes exactly this **ordered environment vector** to pytest;
entries are ordered by raw key bytes and duplicate keys are forbidden. This is
an ordered sequence, not merely a key/value set, because environment iteration
order is observable:

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
PYTHONIOENCODING=utf-8:strict
PYTHONNOUSERSITE=1
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

No `PWD`, `_`, `SHLVL`, `PYTHONHOME`, `PYTHONPATH`, `PYTEST_ADDOPTS`,
`PYTEST_PLUGINS`, proxy, credential, shell-startup, coverage, CI, editor, Git,
cloud, or unnamed variable exists. Absence is enforced by direct `execve`, not
by an `unset` list.

The outer attestor reads the actual supervisor environment; the supervisor reads
`/proc/<pytest-pid>/environ` after `execve` and before pytest collection. Both
compare the exact NUL-delimited ordered sequence to the authority vector.
Added, missing, duplicate, undecodable, reordered, or changed entries `BLOCK`.
Negative controls add one unexpected variable, delete one required entry,
reorder two entries, and change one value; all must be rejected by the real
top-level launcher.

## 4. Interpreter identity: payload plus run-time proof

The literal paths are normative:

```text
P10_WORKTREE=/worktree
P10_BASE_PYTHON=/opt/p10/cpython/bin/python3.12
P10_PYTHON=/opt/p10/venv/bin/python
P10_WHEELHOUSE=/opt/p10/wheelhouse
P10_ALLOWBIN=/opt/p10/allowbin
P10_EVIDENCE=/evidence
```

“Python 3.12” is not an identity. The authority must predeclare:

- CPython provenance/distribution, patch version, build string, compiler,
  configure/build flags, ABI/SOABI/MULTIARCH, cache tag, executable format and
  build ID;
- SHA-256 of resolved base and venv interpreter executable bytes;
- complete no-exclusion manifests for `/opt/p10/cpython` and immutable
  `/opt/p10/venv`, including relative path, type, mode, owner, symlink target,
  bytes/SHA-256 and relevant metadata;
- dynamic loader, libc, libpython, OpenSSL, SQLite, timezone/locale payloads and
  every file-backed shared library mapped after importing pytest and the frozen
  conftest, each by resolved path and bytes/SHA-256;
- exact `sys.version`, `version_info`, executable/prefix/base_prefix, platform,
  implementation/cache tag, filesystem/default/locale encodings,
  `sysconfig.get_platform()`, `SOABI`, `MULTIARCH`, `sys.path`, `sys.flags`,
  `sys._xoptions`, site paths, and initially imported module origins.

Expected tree manifests are made by an independent freeze verifier over the
sealed image/rootfs. At run time the sealed supervisor measures the live mounts
and the actual interpreter process. Full member conservation is required:

```text
expected = matching + mismatching + missing
actual   = matching + mismatching + unexpected
```

Only `matching=expected=actual` conforms. An unreadable member, unknown mapped
library, changed executable, site path outside the manifest, or missing runtime
field is `BLOCK`. `sys.version` printed by the process is corroboration, not the
expected value. The v1 review required this pre-run payload identity rather than
a post-run description. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:26-32`

The actual container-to-image binding is independently supplied by the outer
attestor. Thus a process cannot claim that its own altered interpreter is the
expected interpreter.

Falsification must change one interpreter byte, remove/add a stdlib member,
retarget a symlink, substitute a mapped library, inject `sitecustomize`, change a
site path, and lie about the outer image digest. Every arm must reject; the
unmodified sealed image must pass.

## 5. All remaining nondeterministic inputs

The fixed environment and one vCPU do not prove that time, entropy, scheduling,
or machine identity cannot affect a baseline. Before plugin proof or collection,
one sealed fail-closed inventory must cover every collected test/conftest and
every repository module imported by that exact collection. It must also consume
the actual file-open, executable, network, entropy, and system-information event
ledger from a proof run.

The inventory universe includes at least:

- realtime/monotonic/performance clocks, sleeps, timeouts, timezone and locale;
- `random`, `secrets`, UUID, hash randomization, OpenSSL RNG and
  `/dev/{u,}random`/`getrandom`;
- PID/TID, process order, thread/task scheduling, signals, CPU count/affinity,
  multiprocessing and thread pools;
- hostname/domain, machine-id, boot-id, MAC/interface data, user/group/NSS;
- environment, argv, CWD, home/XDG, temp, current directory and executable PATH;
- filesystem enumeration order, inode/device/ctime/mtime, permissions, umask,
  case/Unicode behavior, free space and mount data;
- memory addresses/ASLR, object reprs, floating-point/CPU feature behavior;
- terminal/width/color/encoding, warnings filters, stdout/stderr buffering and fd
  properties;
- subprocess/shell execution, absolute executables, configuration/certificate
  discovery, sockets and any external endpoint.

Each admitted read has exactly one terminal disposition:

1. `FIXED`: actual value equals an independently sealed authority value;
2. `EXISTING_TEST_CONTROL`: exact frozen test code supplies a deterministic value;
3. `SEMANTICALLY_UNREACHABLE`: a reviewed dataflow proof establishes that it
   cannot change collection, node IDs, phase/outcome, warning/anomaly, normalized
   stdout/stderr, or any other baseline field;
4. `UNRESOLVED`: execution `BLOCKS`.

No new product/test mock is authorized by this document. If an uncontrolled
input is reachable, the contract must be amended or the suite cannot form a
baseline. Variable duration and outer timestamps may differ only because they
are raw provenance fields explicitly excluded from baseline semantics in section
9. A test-emitted time, PID, address, ordering, or random value is **not**
automatically normalized; it changes the normalized stream and blocks the pair.

The inventory tool must reject unparsed syntax, unresolved import/call target,
dynamic command/path/provider, unsupported syscall/event, incomplete trace, and
any member without a disposition. A challenge corpus covers every modeled class
plus an unsupported wrapper. The unsupported wrapper must produce
`UNRESOLVED/BLOCK`, never empty PASS.

## 6. Artifact-reproducible dependencies

### 6.1 Explicit policy choice

V3 chooses **artifact-reproducible offline installation**. Integrity-checking
against any hash accepted by the multi-platform lock is insufficient and is not
a fallback. If artifact reproduction cannot be demonstrated, Packet 10 remains
blocked until a versioned contract amendment explicitly discloses a different
policy and residual.

This choice is necessary because the lock accepts multiple hashes for
platform-bearing packages, while the repository verifier checks canonical
distribution names/versions and excludes pip/setuptools from exact-set equality.
`IBKR_PAPER_BRIDGE/requirements.lock:23-35`;
`IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:18-21`;
`IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:66-97` The repository installer
uses `--no-index --find-links` only when a wheelhouse is supplied.
`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:281-309`

### 6.2 Selected artifacts and exact build

The authority must seal:

1. exact `requirements.lock` bytes/SHA-256;
2. base interpreter, `venv`/`ensurepip`, pip, setuptools, build frontend and
   every build executable/library;
3. exactly one compatible wheel per canonical locked distribution, with name,
   version, filename, tags, relative path, bytes and SHA-256;
4. a force-inclusive wheelhouse manifest with no extra, missing, symlinked or
   non-regular member;
5. exact build capsule, supervisor, argv, environment, paths, resources and
   network-absent configuration;
6. canonical pip report schema/result;
7. independently wheel-derived expected installed members;
8. two independently built full venv manifests and their equality result;
9. final read-only venv payload/image identity.

The lock pins `anyio==4.14.2` and `pytest==9.1.1`, but those version facts do not
choose wheel artifacts. `IBKR_PAPER_BRIDGE/requirements.lock:15-22`;
`IBKR_PAPER_BRIDGE/requirements.lock:986-989`

The exact-set equations are:

```text
canonical lock distributions = selected compatible wheels
selected wheel filenames     = wheelhouse regular-file members
build-1 venv members          = build-2 venv members
build-1 member identities     = build-2 member identities
```

Each build begins with `/opt/p10/venv` proven absent by `lstat` and a
force-inclusive parent enumeration. The sealed build supervisor directly execs
these argv vectors; the displayed form is descriptive, not a shell command:

```json
["/opt/p10/cpython/bin/python3.12", "-m", "venv", "/opt/p10/venv"]
["/opt/p10/venv/bin/python", "-m", "pip", "install",
 "--require-hashes", "--no-deps", "--only-binary=:all:",
 "--no-index", "--find-links=/opt/p10/wheelhouse",
 "--no-input", "--no-cache-dir", "--disable-pip-version-check",
 "--no-compile", "--report=/opt/p10/build/pip-install-report.json",
 "-r", "/worktree/IBKR_PAPER_BRIDGE/requirements.lock"]
```

There is no shell, index, cache, alternate link, pip upgrade, build isolation
download, dependency re-resolution, or network interface. The canonical build
path, environment, umask, locale, timezone, clock policy and source epoch are
the same in both builds.

After each build, verify the pip report against the selected wheels and require
the two canonical reports to be identical; run
`verify_lock.py --check-installed` only as a supplemental name/version check;
compare every installed member against the wheel-derived expectation; account
for bootstrap/generated members with independently specified byte rules; and
manifest the full venv without exclusions. Two builds must have identical
member sets, bytes, modes, links and recorded semantic metadata. Only then may
one identical venv payload be placed in the execution image.

At baseline run time, no installation occurs. The entire immutable venv is
recomputed and compared with the twice-reproduced sealed manifest.

### 6.3 Dependency falsification

The real build gate must reject: changed/renamed/extra/missing wheel; duplicate
canonical distribution; incompatible tag; changed pip/installer byte;
pre-existing venv; altered installed file; extra site-packages member;
unmanifested pip-report artifact; network/index attempt; and two clean builds
whose output differs by one byte or metadata field. Expected values are not
regenerated after mutation. The unmodified pair must reproduce exactly.

## 7. Explicit pytest plugins and sufficiency gate

### 7.1 Fixed candidate set

The exact pytest control remains:

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
explicit third-party plugin argv = ["-p", "anyio.pytest_plugin"]
disabled built-in plugin argv     = ["-p", "no:cacheprovider"]
```

The lock proves the `anyio` and pytest versions are present, and the inspected
root conftest itself declares only an autouse fixture using pytest's built-in
`monkeypatch`. `IBKR_PAPER_BRIDGE/requirements.lock:15-22`;
`IBKR_PAPER_BRIDGE/requirements.lock:986-989`;
`IBKR_PAPER_BRIDGE/tests/conftest.py:6-21` These facts do not prove whole-suite
sufficiency. Installed `pytest11` entry points describe what could autoload, not
what this suite requires. The v1 review therefore correctly classified
sufficiency as unknown. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_SUITE_CONTRACT_REVIEW_2026-08-15.md:46-58`

Current status is **UNKNOWN (BLOCKING)**, not assumed sufficient. This question
is closed at contract level as a mandatory producer: the authority may mark
`PLUGINS_PROVEN` only after every step below succeeds for the exact frozen SHA;
otherwise no baseline execution is conforming. An operator may never add a
plugin to make collection pass. If the proof discovers another required
provider, this v3 contract fails: a versioned successor must change the explicit
list and section 8 argv before either run. The authority file cannot silently
amend the hardcoded instrument.

### 7.2 Proof universe and acceptance rule

The universe is exactly all members in the frozen raw manifest under
`IBKR_PAPER_BRIDGE/tests`, every discovered conftest, every active pytest config,
every collected item, and every setup/call/teardown fixture/hook/provider reached
under the exact v3 argv/environment.

The proof requires:

1. **Force-inclusive source manifest.** Every test/conftest/config member has one
   stable identity and one terminal inventory disposition.
2. **Fail-closed static inventory.** A sealed tool inventories fixture
   parameters, `usefixtures`, `pytest_plugins`, marks, hooks, plugin-manager
   calls, CLI/config options, dynamic imports/names and generated items. Every
   use maps to pytest core, a local conftest definition, or an exact explicit
   third-party provider. Unknown syntax/import/provider is `BLOCK`.
3. **Installed entry points.** Record every installed `pytest11` entry point and
   provider payload. This is descriptive only.
4. **Actual loaded set.** A sealed in-process recorder obtains the plugin manager
   set after configuration and after collection. Third-party loaded providers
   must equal exactly `[anyio.pytest_plugin]`; built-ins must equal the sealed
   pytest-9.1.1 built-in manifest minus `cacheprovider`. Every provider module,
   distribution, path and payload digest must match the venv manifest.
5. **Strict collection and resolution.** Exact collection with
   `--strict-config --strict-markers`; ordered node IDs; per-item fixture/marker/
   hook resolution. Every resolution must map to the static inventory. Unknown
   marker/config, unresolved fixture/provider, collection warning/error, or
   changed universe is `BLOCK`.
6. **Full execution.** The exact suite executes with autoload disabled. Completion
   corroborates the proof but cannot replace steps 1-5.
7. **Second capsule.** Steps 4-6 repeat independently. Loaded sets, collection
   manifests and semantic results must be identical.

Sufficiency means every required third-party provider is in the explicit set and
every loaded third-party provider is exactly in that set. Minimality is not
claimed: `anyio.pytest_plugin` may be explicit even if no frozen item requires
it, but no missing provider can be silently tolerated.

### 7.3 Proof-tool falsification

The independently sealed challenge corpus contains a fixture parameter,
`usefixtures`, mark, `pytest_plugins`, hook, plugin CLI/config option, dynamic
provider, duplicate provider identity, provider available only by autoload, and
unsupported construct. Omit or replace each provider in turn; the real top-level
proof must name the unresolved use and `BLOCK`. Add one unexpected loaded plugin;
the exact-set comparator must reject it. The unsupported construct must not
disappear. The unmodified challenge must pass.

Until those RED/GREEN transcripts and tool/corpus identities are sealed, plugin
sufficiency remains `UNKNOWN` and section 8 may not run.

## 8. Exact collection and execution instruments

Each probe, collection, and execution starts in a separate fresh capsule so no
writable layer, process, PID sequence, home, temp, cache or output carries over.
The PID-1 supervisor performs all preflight checks without spawning a helper,
opens fixed write-only captures, then forks exactly once. The PID-2 child
directly `execve`s the interpreter; PID 1 retains supervision and evidence
finalization. No shell command is authoritative.

### 8.1 Collection argv

```json
["/opt/p10/venv/bin/python", "-X", "utf8=1", "-B", "-m", "pytest",
 "IBKR_PAPER_BRIDGE/tests", "--collect-only", "-q",
 "--strict-config", "--strict-markers", "--color=no",
 "--basetemp=/run/p10/tmp/pytest",
 "-p", "anyio.pytest_plugin", "-p", "no:cacheprovider"]
```

### 8.2 Mandated execution argv

```json
["/opt/p10/venv/bin/python", "-X", "utf8=1", "-B", "-m", "pytest",
 "IBKR_PAPER_BRIDGE/tests", "-q", "-ra",
 "--strict-config", "--strict-markers", "--color=no",
 "--basetemp=/run/p10/tmp/pytest",
 "-p", "anyio.pytest_plugin", "-p", "no:cacheprovider"]
```

For both: CWD is exactly `/worktree`; environment is exactly section 3.3; umask,
resources, identity, mounts, fds and machine state are exactly section 3.2. The
authority stores argv as JSON arrays, never a command string. Diagnostic plugin
and fixture probes have separately sealed argv arrays; only their named
diagnostic option may differ.

`MANDATED_COMMAND` means the section 8.2 argv plus the sealed launcher,
supervisor, CWD, environment, fd, capsule and authority identities. An operator
cannot substitute `python`, add an option, alter order, or omit a preflight.
Inability to execute the mandated suite is `BLOCK`, not acceptance.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:102-104`

## 9. Evidence, semantic projection, and baseline record

### 9.1 Raw per-run provenance

For every preflight, probe, collection and suite execution, retain separately:

- exact launcher/supervisor/child argv arrays, CWD and environment map;
- actual identities, resources, mounts, security state, fds and process profile;
- outer and guest UTC timestamps, monotonic elapsed time and pytest duration;
- byte-preserved stdout/stderr, exact sizes/SHA-256 and process rc;
- frozen SHA, raw worktree/image manifests and pre/post comparisons;
- image/machine/interpreter/venv/lock/installer/wheel/plugin identities;
- plugin proof and nondeterministic-input inventory/falsification evidence;
- ordered collection IDs, phase reports, outcomes, warnings and anomalies;
- a force-inclusive evidence manifest with one role/disposition for every member.

After the supervisor closes the child and completes postflight, it fsyncs the
captures/result/manifest, makes the evidence tree read-only, and hands its root
identity to the outer attestor. The attestor recomputes the force-inclusive
member/byte manifest and binds it to the instance record. Any later missing,
extra or changed byte breaks that binding and invalidates the evidence package.

Raw evidence preserves what happened. It is not itself the cross-run baseline:
the provisional runs demonstrate that duration can differ while outcome counts
and identities agree. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:87-97`

### 9.2 `p10-suite-result-v3`

Each run produces one UTF-8 JSON result containing at least:

```text
schema/contract/authority/extractor/normalizer/comparator identities
full frozen SHA, Git-tree and raw-worktree manifest identities
launcher/runtime/OCI/image/machine identities
interpreter/base-tree/venv/lock/installer/wheelhouse/install identities
normalized argv, exact environment, resource/security/mount/fd profiles
explicit and actual-loaded plugin manifests; plugin-proof identity
nondeterministic-input inventory identity and terminal counts
ordered collection IDs and collection-manifest identity
reported and canonical counts: collected, selected, deselected, executed,
  passed, failed, skipped, xfailed, xpassed, errors, warnings, unresolved
per-item setup/call/teardown states and exclusive terminal outcome
ordered non-pass, warning and anomaly records
normalized complete stdout/stderr bytes and SHA-256
```

Every collected item has exactly one selected/deselected disposition. Every
selected item has explicit setup/call/teardown states; `not_run` is explicit.
Terminal precedence is: collection/setup/teardown error -> `error`; unexpected
call failure -> `failed`; expected failure -> `xfailed`; unexpected pass ->
`xpassed`; ordinary skip -> `skipped`; ordinary success -> `passed`. Anything
else is `unresolved`, and baseline formation requires `unresolved=0`.

```text
collected = selected + deselected
selected  = passed + failed + skipped + xfailed + xpassed + errors + unresolved
executed  = selected items with a call-phase report
```

Reported pytest counts and canonical counts are both retained and fingerprinted.
A teardown error after a passed call remains visible in phases and has terminal
outcome `error`.

### 9.3 Complete normalized streams

The semantic projection includes the **entire** stdout and stderr after one
grammar-aware normalization pass. Only these fields may be replaced:

- pytest's parsed terminal duration field;
- outer/guest evidence timestamps and monotonic durations emitted by the sealed
  supervisor, in their named structured records;
- container/process IDs explicitly classified as instance identifiers in the
  authority schema and proven unable to identify a test outcome.

No free-form regex deletion is allowed. Test-emitted timestamps, random values,
paths, addresses, ordering differences or messages remain unchanged. Unknown or
ambiguous grammar, undecodable bytes, a second possible parse, or an unconsumed
token `BLOCKS`. Raw streams remain untouched in provenance. Thus two runs cannot
hide a semantic difference merely because the extractor did not model a count.

Warning signatures are `(category, exact message, repository-or-distribution-
relative file, line)`. Anomaly signatures are `(node_id, phase,
exception/assertion type, exact normalized message, repository-relative top
file, line)`. Paths that should be canonical already are; no operator path is
regex-redacted.

### 9.4 Semantic fingerprint and baseline boundary

Canonical JSON uses sorted object keys, no insignificant whitespace, UTF-8, LF,
and schema-declared array ordering. SHA-256 covers every result field except:

- raw evidence paths, sizes and hashes;
- outer/guest timestamps and elapsed/duration fields;
- explicitly named ephemeral container/process instance IDs.

The exclusions are a closed schema list. Adding an exclusion is a contract
change. Everything else—including full normalized stdout/stderr—is fingerprinted.

`BASELINE_RECORD_V3.json` contains only the common semantic document and
fingerprint established by both runs. Per-run raw facts are supporting evidence,
not baseline expectation values. The baseline source package references both
raw evidence manifests by operator role, but it never promotes their unequal
timestamps/durations/raw hashes into expected run semantics.

Accordingly, “the baseline records” in the v3 closure test means the fields of
`BASELINE_RECORD_V3.json`. Raw run packages remain mandatory, sealed provenance
and may differ only in the closed ephemeral list above; any other raw-stream
difference changes the normalized stream and prevents baseline formation.

### 9.5 Extractor/normalizer falsification

An independently authored sealed corpus covers every phase/outcome, collection
error, warning, deselection, duplicate ID, undecodable/truncated stream,
inconsistent summary, normalized duration, test-emitted timestamp/address, and
unknown output grammar. Mutate each admitted semantic fact while holding the
expectation fixed: the result/fingerprint must change or the tool must `BLOCK`.
Mutating only an allowed structured duration must preserve the semantic
fingerprint while changing raw provenance. A test-emitted timestamp/address must
change it. The unmodified corpus must reproduce predeclared bytes exactly.

The corpus author supplies expectations before the extractor runs. The extractor
cannot produce both input and expected result.

## 10. Two-operator closure test

Only after every blocking unknown and every instrument/plugin/nondeterminism
proof is sealed do two different operators run. They receive the same authority
bundle and immutable artifacts. They share no writable layer, process, home,
XDG, temp, evidence directory, worktree mount instance, or prior output.

### 10.1 Constructed operators

**Operator A** begins from an interactive shell with one locale, timezone, HOME,
PATH, CPU count and `BASH_ENV`. **Operator B** begins from another shell with
different values, a different Git autocrlf setting, extra pytest plugins in a
personal Python installation, and more physical CPUs.

Neither ambient state is an input to a conforming run:

- the authority controller directly execs the same static launcher with
  `envp=[]`; no shell or startup file is executed;
- the same sealed OCI config and machine profile expose the same one-vCPU
  capsule, resources, kernel/libc surface, mounts and identity;
- both mount the same raw read-only worktree payload, not local checkouts;
- both use the same prebuilt twice-reproduced venv and wheel identities;
- the supervisor passes the same exact pytest env/argv/CWD/fds;
- plugin autoload is disabled and the same proven explicit list is loaded;
- home/XDG are empty read-only, temp is fresh at the same canonical path, and
  all remaining reachable nondeterministic inputs have terminal dispositions.

If either operator bypasses this chain or substitutes any value, that run is
nonconforming and cannot be compared as a baseline candidate.

### 10.2 Required equality

Both runs must have exact equality of:

- authority, raw worktree, launcher/runtime/image/machine/interpreter/dependency
  identities;
- argv, environment, resources, security, mount, fd and allowed-executable
  profiles;
- explicit/loaded plugin manifests and sufficiency proof;
- nondeterministic-input inventory/dispositions;
- ordered collection manifest;
- complete `p10-suite-result-v3` semantic document;
- complete normalized stdout/stderr and semantic fingerprint.

The comparator obtains neither expectation from one operator. It compares both
against the shared authority and then against each other. A difference prevents
`REPRODUCIBLE_PAIR`; inability to compare is `BLOCK`. No field is selected from
the more convenient run.

### 10.3 Adversarial search for a legal difference

| Attempted difference | Why it is not legal or cannot become a baseline difference |
|---|---|
| Shell profile, `BASH_ENV`, parent locale/PATH/HOME | No shell; launcher receives empty env and validates it before runtime. Negative control must reject. |
| Different checkout bytes/CRLF/untracked cache | Operators do not checkout. Same sealed raw image; pre/post exact manifest. |
| Different Python patch/stdlib/shared library | Exact image, interpreter trees, mapped libraries and runtime observations must match authority. |
| Different accepted lock wheel or pip | One selected wheel per distribution; exact wheelhouse; two byte-identical clean builds; run-time full venv match. |
| Extra/missing pytest plugin | Autoload disabled; loaded third-party exact-set equality; sufficiency must be proven first. |
| Locale, timezone, PATH, user/home/XDG/temp | Literal exact environment plus sealed payloads/directories and run-time comparisons. |
| CPU count, threads, memory, rlimits, umask | One pinned profile, explicit thread controls, actual comparison. |
| Clock, RNG, PID, scheduling, inode/order, ASLR | Fixed, existing-test-controlled, or proved unreachable; unresolved blocks. If a value reaches output, normalized-stream equality exposes it. |
| Different pytest duration/timestamps | Preserved as per-run raw evidence but deliberately not baseline semantics; grammar-aware normalization proves this is the only difference. |
| Extractor silently ignores changed text | Complete normalized streams are fingerprinted; unknown grammar blocks; mutation corpus must expose omissions. |
| Operator changes expected values to match actual | Authority is presealed by an independent producer; operator cannot write it. |

**Self-finding:** physical scheduling and elapsed time can still differ between
the two capsule instances. V3 does not claim otherwise. They are legal only as
raw provenance differences and cannot change any baseline field. If they change
test ordering, message text, outcome, warning, anomaly, or any normalized byte,
the semantic documents differ and no baseline forms. This is a disclosed
residual of the physical execution, not a route to two different accepted
baselines.

No other legal baseline-recorded difference was found. That conclusion is
conditional on the currently `UNKNOWN` instruments and plugin/nondeterminism
proofs being populated and passing. Until then, the correct result is `BLOCK`,
not a claim that the environment is already reproducible.

## 11. Definition-time baseline and anomalies

| Field | V3 value before the independent pair |
|---|---|
| `MANDATED_COMMAND` | Section 8.2 argv plus all sealed launch/capsule inputs; artifact identities `UNKNOWN`. |
| `CONTRACT_TARGET_EXIT_CODE` | `0`; exact frozen-SHA locked-environment green remains required. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72` |
| `CONTRACT_TARGET_FAIL_COUNT` | `0`; target, not observation. |
| `EXPECTED_EXIT_CODE` | `UNKNOWN`. |
| `EXPECTED_COLLECTED/SELECTED/EXECUTED/DESELECTED` | `UNKNOWN`. |
| `EXPECTED_PASS/FAIL/SKIP/XFAIL/XPASS/ERROR/WARNING` | `UNKNOWN`. |
| `EXPECTED_COLLECTION_MANIFEST_SHA256` | `UNKNOWN`. |
| `EXPECTED_LOADED_PLUGIN_MANIFEST_SHA256` | `UNKNOWN`. |
| `EXPECTED_NORMALIZED_STDOUT/STDERR_SHA256` | `UNKNOWN`. |
| `EXPECTED_SEMANTIC_FINGERPRINT` | `UNKNOWN`. |
| `EXPECTED_FAILURES` | `UNKNOWN`; an empty set must be observed/adjudicated. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-64` |
| `ACCEPTED_ANOMALY_REGISTER` | `UNKNOWN`; this contract accepts none. |
| `BASELINE_SOURCE` | `UNKNOWN`; future exact path/bytes/SHA-256 of adjudicated pair. |

Historical A1 (working-tree line endings) and A2 (stale schema-version assertion)
remain conditional expectations only. Their repairs were accepted at T1 but not
merged, and an exact-frozen-SHA locked-environment green run remained required.
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:3-17`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:19-29`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72`

Every observed anomaly is recorded before adjudication. First verify all
identity/environment/plugin/evidence gates, then reproduce root cause against
the frozen bytes. Only separate Lead/owner authority can accept an anomaly. A
zero-anomaly result is an observed empty set, never inferred from target zero.

## 12. Falsifiability and enforcement ledger

| Check | Declared universe | Independent expectation | Concrete RED | Enforcement, not assertion |
|---|---|---|---|---|
| Authority identity | Dispatch manifest and every referenced artifact. | Prepublished authority digest from independent freeze channel. | Substitute authority byte/path/digest. | Launcher/attestor refuse before capsule start. |
| Raw worktree | Every frozen Git-tree and image member. | Git-object/tree manifest independently compared to sealed image manifest. | CRLF, missing/extra/mutated/mode/link member. | Exact-set conservation; live pre/post full walk. |
| Launch closure | Launcher/runtime/supervisor chain, argv/env/CWD/fds/startup inputs. | Literal v3 chain plus sealed binaries/config. | `BASH_ENV` marker, extra env/fd, altered argv/runtime. | Static direct exec; outer/inner exact comparisons; no shell. |
| Capsule/machine | Image, kernel/libc, CPU/resources, identity/security/mount/network profile. | Independently sealed machine profile. | Change one profile field or make probe unreadable. | Preflight `BLOCK`; no collection. |
| Interpreter | Every CPython/venv member and mapped library plus runtime fields. | Rootfs-derived manifests and authority values. | Mutate interpreter/stdlib/library/site path. | Full conservation and outer image binding. |
| Nondeterministic inputs | Every source/event-ledger input that can reach a baseline field. | Sealed inventory grammar and authority controls. | Unsupported wrapper or unclassified time/RNG/system read. | One terminal disposition per member; unresolved `BLOCK`. |
| Dependency artifacts | Lock distributions, selected wheels, builders and every venv member. | Lock + selected wheel/installer manifests + independent two-build result. | Alternate wheel, reused venv, byte-different second build. | Exact bijections and full-tree equality; no fallback. |
| Plugin sufficiency | Entire frozen collected/executed suite and provider graph. | Source usage mapped to authority-approved providers. | Missing provider, autoload-only provider, unexpected loaded plugin. | Fail-closed inventory, strict collection, loaded exact set; status currently `UNKNOWN/BLOCK`. |
| Result extraction | Every raw event, phase, item, warning/anomaly and output byte. | Independent fixture corpus/expected result. | Mutate one semantic byte/count; add unknown grammar. | Fingerprint changes or tool `BLOCKS`; no silent drop. |
| Reproducibility | Both complete conforming semantic documents. | Shared authority plus symmetric comparison. | Any semantic field differs. | No `REPRODUCIBLE_PAIR`; no baseline. |

For every row, inability to evaluate is `BLOCK`, not PASS and not a suite FAIL.
For every row, the expected value predates and is outside the checked operator
run. Every check has a constructible RED and must show it before use.

## 13. Runtime estimate

**NO SOURCED ESTIMATE.** The only recorded measurements are 85.53-100.01 seconds
in the invalid Windows Python-3.14.2/pytest-9.0.2 environment, and duration was
not stable. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:87-97`

Only measurements from the fully populated v3 pair can supply an operational
estimate. Such durations remain raw run evidence, never baseline identity or
acceptance.
