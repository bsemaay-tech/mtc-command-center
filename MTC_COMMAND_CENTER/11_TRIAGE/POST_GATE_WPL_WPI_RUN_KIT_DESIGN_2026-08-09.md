# Post-Gate WP-L Phase 2 / WP-I Run-Kit Design (2026-08-09)

```
################################################################################
##                                                                            ##
##        D E S I G N   O N L Y  —  N O T   E X E C U T E D                    ##
##        N O T   A U T H O R I Z E D   F O R   H O S T   U S E                ##
##                                                                            ##
##  Nothing in this file has been run. No command block here has touched       ##
##  GATEA-STAGING, any service, any database, any credential, any broker,      ##
##  any exchange, or any network. This document is an implementation           ##
##  CONTRACT for a run kit that does not yet exist and is not yet              ##
##  authorised to exist as an executable.                                      ##
##                                                                            ##
##  Reading this file grants no authority. Copying a block out of this file    ##
##  and running it is a violation of the stop conditions in §12.               ##
##                                                                            ##
################################################################################
```

- **Date:** 2026-08-09.
- **Model / route:** `claude-opus-5`, effort `xhigh` (counterpart flagship implementer, `AGENTS.md`
  §Two-Tier). Documentation-only unit in an isolated local worktree.
- **Starting documentation HEAD:** `851d2aa5`.
- **Frozen product candidate:** `2ce41e34bceb599d80af24c5c33d835820ec321b` (unchanged; no product
  file was read for modification and none was modified).
- **Unit class:** `local-static`. Targeted reads and `rg` only. **No** SSH, sudo, `systemctl`,
  reboot, service, package/install, pytest, broker/network/exchange, credential, ARM/order, Git,
  staging-host, or mutation command was run. No credential value was read or printed. No executable
  script was created.

---

## 0. What this document is, and what it deliberately is not

The governing scope record
`GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` closes with five explicit
**COMMAND GAP** markers and one stale evidence-map node, and names the next autonomous safe unit as
*local run-kit design/validation only*. This file is that unit's deliverable.

**It is:** an implementation-ready contract — exact inputs, exact outputs, exact ordering, exact
predicates, exact stop conditions, redaction rules, and no-clobber rules — for a future run kit,
expressed as pseudocode and shell blocks that are all marked `NOT EXECUTED`.

**It is not:** a script, a runbook authorisation, a claim that any evidence exists, or a claim that
any host action may now be taken. Where an input cannot be established from source in this unit it is
marked **UNRESOLVED-INPUT** and must be resolved *locally* before the corresponding stage is
authored as an executable. Nothing is invented to fill a gap.

**Standing blockers, unchanged by this document** (gap matrix §7):

1. **Budget (binding).** The exact 50-hour used/remaining balance is NOT REPRODUCIBLE
   (`GATE_A_50H_LEDGER_RECONSTRUCTION_2026-08-09.md`, state 5). No server-executed post-Gate work may
   be committed against an unknown hard ceiling. A human re-plan or an explicit ceiling extension is
   required before **any** stage below is executed.
2. **Authority.** WP-V, KVM2, master merge, credentials, broker/exchange, ARM, orders,
   TESTNET/mainnet, economic action, and old-payload deletion each require a new explicit named lift.
   Gate-A A-0..A-9 PASS is *staging acceptance only* and grants none of them.

---

## 1. Preserved host invariant this design must not break

Recorded read-only facts (`GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md`), treated here as
the **current invariant** every stage is measured against:

| Fact | Recorded value |
|---|---|
| Unit | `mtc-bridge-first-start.service`, **active/running**, **unmasked** |
| MainPID | `189813` |
| Restart policy | `Restart=no`, `NRestarts=0` |
| Listener | exactly one — `127.0.0.1:8790` |
| Runtime state | credential-free **DISARMED**, `state_version=1`, all credential/network/exchange/ARM flags off |
| Installed releases | exactly one — `/opt/mtc-bridge/releases/2ce41e34…321b` (old `ebada020…` install + venv already absent) |
| Unit fragment | `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`, SHA-256 `538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd`, 3736 B, root `0644` |
| Symlinks | no `current` / `previous` under `/opt/mtc-bridge`; no steady or legacy unit |

**Stage B preserves this invariant exactly.** Stages C1–C4 each *change* it and each therefore need
their own named authority plus an owner-acknowledged plan for returning to (or deliberately leaving)
the changed state. That distinction is the spine of §2.

---

## 2. Stage model — independently authorised, no monolith, no chaining across a mutating boundary

The run kit is **five separate artifacts**, not one script with flags. Each is authored, reviewed,
hash-recorded and authorised on its own. Stage labels deliberately reuse the gap-matrix labels so
there is exactly one taxonomy in the programme.

| Stage | Gap-matrix origin | Mutation class | Ends with the host in |
|---|---|---|---|
| **B** — post-start read-only evidence | Group B + G2 | `read-only-host` | the §1 invariant, unchanged |
| **C1** — post-SIGTERM clean shutdown / no dangling state | C1 · E8 · WP0 I-R4 | `mutating-host` | **stopped**, unmasked |
| **C2** — post-reboot read-only subcheck | C2 · G1 | `mutating-host` (reboot) | rebooted; unit inactive |
| **C3** — WAL bundle capture → verify → restore-into-temp | C3 | `read-only-host` (C3-a) / quiesced-window (C3-b) | unchanged by the capture itself |
| **C4** — rollback stop+mask-only | C4 · G3 | `mutating-host` | stopped **and masked** |

### 2.1 The four hard structural rules

**R1 — One authority, one artifact.** A stage script may not contain another stage's actions. In
particular Stage B must contain no `stop`, `start`, `mask`, `unmask`, `reboot`, `install`, `rm`,
`chmod`, `chown`, or write to any path outside its own evidence directory.

**R2 — No automatic chaining across a mutating boundary.** A stage script terminates at its own
boundary and returns an exit code. It never invokes the next stage, never "continues on success",
and never offers a `--and-then` flag. The operator re-reads the evidence, obtains the next named
authority, and starts the next artifact by hand. Concretely: C1 must not start the service again, C1
must not call C3, C3 must not call C4, and C4 must not perform a recovery start (that is the
`KVM2-P4-08A` authorisation and a separate single `KVM2-P4-08B` attempt — `rollback.sh:185`).

**R3 — Read-only stages run to completion; mutating stages stop at first mismatch.** Stage B mirrors
`verify.sh`'s accumulate-then-fail-closed shape (`lib/common.sh:38` increments `MTC_FAILURES`;
`verify.sh:247-252` exits on the total) because a complete picture of a read-only state is more
valuable than an early exit. Stages C1–C4 do the opposite: the first failed predicate aborts before
the next mutation, because a mutation performed on top of an unexplained mismatch destroys the
evidence that would explain it.

**R4 — The quiesced window is declared in advance, never discovered.** C1's stop opens a window in
which the writer is down. C3-b's capture is the only read that is trustworthy in that window. If the
owner wants both, the *single* authorisation sentence must name both C1 and C3-b. If it names only
C1, the window closes when C1 exits and re-opening it costs another authorised stop. The run kit
must never "notice the service is already stopped and helpfully also capture a bundle."

### 2.2 Prerequisite graph (read top-down; each arrow is a separate authorisation)

```
Stage B  ──(no prerequisite beyond host access + budget lift)
   │
   ├─► C2   plain reboot from the current unmasked state (Scenario A)
   │
   └─► C1   authorised single `systemctl stop`  ── opens the quiesced window
              │
              ├─► C3-b  quiesced capture + verify + restore-into-temp
              │           │
              │           └─► C4   rollback stop+mask (needs C3-b's manifest + its SHA-256)
              │
              └─► (recovery start — KVM2-P4-08A authority, NOT designed here)

C3-a  live-source capture — WARNING CLASS ONLY, never a cutover or continuity proof
```

---

## 3. Common contract — shared by every stage (normative)

### 3.1 Preregistered constants

These are the exact values a stage script must carry as literals and assert against. Every one is
either re-derived in this unit or cited to an immutable evidence record.

```bash
# ---- NOT EXECUTED — constants block, identical in every stage artifact ----
CANDIDATE_SHA='2ce41e34bceb599d80af24c5c33d835820ec321b'
RELEASE_DIR="/opt/mtc-bridge/releases/${CANDIDATE_SHA}"
VENV_DIR="/opt/mtc-bridge/venvs/${CANDIDATE_SHA}"
VENV_PY="${VENV_DIR}/bin/python"
UNIT_NAME='mtc-bridge-first-start.service'
UNIT_FILE="/usr/local/lib/systemd/system/${UNIT_NAME}"
MASK_LINK="/etc/systemd/system/${UNIT_NAME}"          # must be ABSENT while unmasked
STEADY_UNIT='mtc-bridge-steady.service'               # must be absent from both dirs
STATE_DIR='/var/lib/mtc-bridge'
STATE_DB="${STATE_DIR}/bridge.db"
LOG_DIR='/var/log/mtc-bridge'
CONF_DIR='/etc/mtc-bridge'
ENV_FILE="${CONF_DIR}/mtc-bridge.env"                 # NEVER read; mode/owner only
INSTALL_MANIFEST="${CONF_DIR}/install_manifest.json"
BIND='127.0.0.1'; PORT='8790'

EXPECT_UNIT_SHA256='538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd'
EXPECT_UNIT_BYTES='3736'
EXPECT_LOCK_SHA256='40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3'
EXPECT_LOCK_PACKAGES='56'
EXPECT_PYVER='3.12'
EXPECT_MAINPID='189813'          # Stage B only; C2 legitimately changes it
EXPECT_TIMEOUT_STOP_SEC='45'
```

**Provenance of `EXPECT_LOCK_SHA256`.** Independently re-derived in *this* unit at the candidate
checkout: `sha256sum IBKR_PAPER_BRIDGE/requirements.lock` →
`40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`; the same tree carries **56**
`==`-pinned entries and **1345** `--hash=sha256:` lines. This reproduces the Lead's value in the gap
matrix §0.5/A3 exactly. Do **not** cite the `1adf9ae5`-era blob hash from `SECURITY_BASELINE.md` §1
as the current candidate's — that hash belongs to frozen source `637307e8` (gap matrix A3
⚠ Lock-identity precision).

**UNRESOLVED-INPUT — `EXPECT_HOSTNAME`.** `GATEA-STAGING` is recorded as the *VM name* in
`GATE_A_STAGING_HOST_PROVENANCE_2026-08-02.md:107` (`C:\HyperV\GATEA-STAGING\`). This unit did **not**
establish that the guest OS `hostnamectl --static` value is the same string. A stage script must
therefore take `EXPECT_HOSTNAME` as an operator-supplied preregistered literal read from the
cloud-init seed record, and must not hard-code `GATEA-STAGING` on the assumption that VM name equals
OS hostname. Resolve locally from the seed evidence before authoring Stage B.

### 3.2 Evidence directory, no-clobber, and sealing

**Naming.** Follow the established Gate-A convention (`/home/gatea/gatea-A8-20260808D.log`,
`C:\WPI_ARTIFACTS\…`). `RUN_ID` is operator-supplied, `YYYYMMDD<letter>`, never derived from `date`
inside the script (a derived id makes two runs collide silently across a midnight boundary and makes
resume ambiguous).

```
remote : /home/gatea/postgate-<stage>-<RUN_ID>/          # one directory per stage per run
         ├── 00_manifest.txt        # every artifact + its sha256 + byte count
         ├── NN_<check>.out         # one file per check, stdout
         ├── NN_<check>.err         # one file per check, stderr
         └── VERDICT                # single line: <STAGE> PASS | FAIL(n) | STOP(<reason>)
local  : C:\WPI_ARTIFACTS\postgate-<stage>-<RUN_ID>\     # mirror, fetched read-only after the run
```

**No-clobber rules (normative).**

```bash
# ---- NOT EXECUTED ----
set -Eeuo pipefail
set -C                                   # noclobber: `>` refuses to truncate an existing file
IFS=$'\n\t'

RUN_ID="${1:?RUN_ID is a required, operator-supplied argument}"
[[ "${RUN_ID}" =~ ^[0-9]{8}[A-Z]$ ]] || { echo 'REFUSE: RUN_ID must be YYYYMMDD<A-Z>' >&2; exit 3; }
RUN_DIR="/home/gatea/postgate-B-${RUN_ID}"

# N1. Never reuse a directory. No --force, no --overwrite, no -p rescue.
[ -e "${RUN_DIR}" ] && { echo "REFUSE: evidence path already exists: ${RUN_DIR}" >&2; exit 3; }
mkdir "${RUN_DIR}"                       # plain mkdir: a missing parent is a stop, not a repair
chmod 0700 "${RUN_DIR}"

# N2. Every write goes through `>` under `set -C`. Never `>>` into a pre-existing evidence file,
#     never `tee -a`, never `sed -i`, never `mv` over an existing artifact.
# N3. Nothing outside ${RUN_DIR} is ever written. Not /tmp, not the release tree, not the state dir.
#     A temp file lives at "${RUN_DIR}/.tmp.<name>" and is renamed into place with `mv -n`.
# N4. Immediately after each artifact is closed, seal it:
seal() {                                  # seal <path>
  local p="$1"
  printf '%s  %s  %s\n' "$(sha256sum "$p" | awk '{print $1}')" \
                        "$(stat -c '%s' "$p")" "$(basename "$p")" >> "${RUN_DIR}/00_manifest.txt"
}
# N5. 00_manifest.txt is the ONLY append-target in the run directory, and it is appended only by
#     seal(). At the end the manifest itself is hashed and that hash is printed to the terminal so
#     the operator records it out-of-band before the directory is copied anywhere.
```

**Rationale for N1.** Every previous Gate-A evidence log is cited elsewhere by SHA-256
(`GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md`, "Canonical Gate-A evidence index"). An
artifact that can be silently rewritten in place breaks every one of those citations. Refusing to
start is cheaper than discovering a broken hash chain later.

### 3.3 Redaction rules (normative)

| # | Rule |
|---|---|
| **D-1** | The env file is **never read**. `stat -c '%a %U:%G'` only. No `cat`, `grep`, `head`, `wc -c`, `md5sum`, or `sha256sum` of `${ENV_FILE}`. Its *content hash* is itself a credential-derived value and must not be recorded. |
| **D-2** | `grep` over a unit file for credential **names** is permitted (`verify.sh:143-147` does exactly this) because the unit legitimately contains no values. `grep` over the env file is not, in either direction. |
| **D-3** | `/api/status` output is **never written raw**. It is projected through a key allowlist (§4.6) before it touches disk. Any key not on the allowlist is emitted as `{"__redacted__": "<json-type>"}` — the key name survives so schema drift is detectable; the value never does. |
| **D-4** | Journal output is filtered to the single unit, bounded by `--since`, and passed through the A-9 secret-signature scan **on the host, before the file is sealed**. A journal slice that produces a non-zero signature count is not sealed and not copied off the host — it is a STOP. |
| **D-5** | No host IP, SSH user, key path, or account address is written into an evidence artifact or into any run-kit script. The scripts address the host as `127.0.0.1` (they run *on* it) and the operator reaches it through an SSH alias defined outside the kit. |
| **D-6** | `wal_state_bundle.py` output is already sanitised at source (`tools/wal_state_bundle.py:28-34`, `_assert_sanitized`, which rejects path separators, drive letters, IPv4 and hostname literals before emitting). Do not add a second redaction layer around it — capture its JSON verbatim. Adding a wrapper filter would mask a genuine `SanitizationError` exit 3. |
| **D-7** | No stage prints a value it has not asserted. `echo "got: ${X}"` on an unexpected value is how an unredacted field escapes. Print the *predicate result*; print the *observed value* only for the fixed, non-secret fields enumerated in that stage's output table. |

### 3.4 Exit codes (identical across stages)

| Code | Meaning | Operator action |
|---|---|---|
| `0` | every predicate passed | seal, record, stop; the next stage needs its own authority |
| `1` | at least one predicate failed | do **not** run any further stage; report with the evidence |
| `2` | **STOP condition** — drift from the §1 invariant, or a safety assertion tripped | preserve evidence, take no corrective action, escalate to the owner |
| `3` | refuse — bad usage, no-clobber violation, missing preregistered input, missing tool | fix the invocation; a missing tool is *not* silently skipped |

**Missing-tool policy.** `lib/common.sh:154-156, 196-199, 209-212` fails closed when `ufw`/`ss` is
absent rather than skipping the assertion. Every stage inherits that: an assertion that *cannot be
made* is a failure, never a pass. `require_cmd` runs first, and the list is exact per stage.

---

## 4. Stage B — post-start read-only evidence

**Purpose.** Replace the wholesale `verify.sh` run, which is a *pre-start, masked-mode* verifier and
**intentionally fails after Gate A started the service** (gap matrix G2). The three specific
predicates that invert post-start are:

| `verify.sh` | Pre-start expectation | Post-start truth |
|---|---|---|
| `:201-206` | mask symlink → `/dev/null` present | mask symlink **absent** (Gate A unmasked it) |
| `:207-211` | unit **not** active | unit **active** |
| `:237-244` | **zero** `bridge.app` writers, control port **closed** | **exactly one** writer (= MainPID), port **open on loopback only** |

Everything else in `verify.sh` remains correct post-start and is reused verbatim in intent below.

**Authority:** host access + budget lift. **Both currently blocked (§0).**
**Mutation class:** `read-only-host`. **End state:** §1 invariant, unchanged.
**Required tools:** `systemctl sha256sum stat find getent id pgrep ss sed cmp awk grep curl`.

### 4.0 B0 — guard (runs first; aborts the stage, mutates nothing)

```bash
# ---- NOT EXECUTED ----
[ "$(id -u)" -eq 0 ] || { echo 'REFUSE: must run as root' >&2; exit 3; }
[ -d "${RELEASE_DIR}" ] || { echo 'STOP: candidate release directory absent' >&2; exit 2; }
# Exactly one installed release — a second release is the G3 drift signal.
installed_count="$(find /opt/mtc-bridge/releases -mindepth 1 -maxdepth 1 -type d | wc -l)"
[ "${installed_count}" -eq 1 ] || { echo "STOP: expected 1 installed release, found ${installed_count}" >&2; exit 2; }
# No mutable indirection may have appeared.
for p in /opt/mtc-bridge/current /opt/mtc-bridge/previous; do
  [ -e "$p" ] || [ -L "$p" ] && { echo "STOP: mutable symlink present: $p" >&2; exit 2; }
done
# Steady profile must be absent from BOTH the unit dir and the mask dir (verify.sh:217-225).
for d in /usr/local/lib/systemd/system /etc/systemd/system; do
  [ -e "$d/${STEADY_UNIT}" ] || [ -L "$d/${STEADY_UNIT}" ] \
    && { echo "STOP: steady unit present at $d" >&2; exit 2; }
done
```

### 4.1 B1 — host / candidate identity and expected unit name

| Input | Command (NOT EXECUTED) | PASS predicate |
|---|---|---|
| `EXPECT_HOSTNAME` (**UNRESOLVED-INPUT**, §3.1) | `hostnamectl --static` | output `= ${EXPECT_HOSTNAME}` |
| — | `cat "${RELEASE_DIR}/RELEASE_SHA"` (whitespace-stripped) | `= ${CANDIDATE_SHA}` |
| — | `systemctl list-units --type=service --all --no-legend 'mtc-bridge*'` | exactly one line, and its unit is `${UNIT_NAME}` |
| — | `readlink -f "${RELEASE_DIR}"` | equals `${RELEASE_DIR}` (not a symlink; `assert_not_symlink` intent) |
| `EXPECT_MAINPID` | `systemctl show -p MainPID --value "${UNIT_NAME}"` | `= 189813` |

**Why MainPID is an identity check, not a liveness check.** `189813` was recorded at A-8/A-9 and the
unit is `Restart=no` with `NRestarts=0`. If MainPID differs, the process was replaced — which under
`Restart=no` means someone stopped and started it, or the host rebooted. Either is drift from §1 and
is **exit 2**, not a retry. This check is Stage-B-only; C2 changes MainPID by design.

### 4.2 B2 — Python 3.12 and exact installed lock parity

```bash
# ---- NOT EXECUTED ----
# 2a. Interpreter version, from the per-SHA venv (verify.sh:104-112).
pyver="$("${VENV_PY}" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
[ "${pyver}" = "${EXPECT_PYVER}" ]                      # expect: 3.12

# 2b. The lock blob on the host is byte-identical to the accepted candidate lock.
lock="${RELEASE_DIR}/IBKR_PAPER_BRIDGE/requirements.lock"
[ "$(sha256sum "${lock}" | awk '{print $1}')" = "${EXPECT_LOCK_SHA256}" ]

# 2c. Installed distribution set exactly equals the lock. Offline; contacts no index.
"${VENV_PY}" "${RELEASE_DIR}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" \
    --lock "${lock}" --check-installed > "${RUN_DIR}/02_verify_lock.out" 2> "${RUN_DIR}/02_verify_lock.err"
# expect rc 0 and stdout EXACTLY:
#   verify_lock: PASS: lock+installed; packages=56
```

**Exact expected stdout** is `verify_lock: PASS: lock+installed; packages=56` — the format string is
`verify_lock.py:96-97` and `len(expected)` is the entry count. Assert the **whole line**, not a
`grep -q packages=56`: a substring match would also accept `packages=560`.

**Failure disposition.** `verify_lock.py:84-92` distinguishes `missing-or-wrong=` from `unexpected=`.
Either is install/product drift → **exit 2**, never a "reinstall and retry". Note `pip`/`setuptools`
are the only tolerated extras (`BOOTSTRAP_DISTRIBUTIONS`, `:21`).

### 4.3 B3 — systemd runtime identity (the strict block)

```bash
# ---- NOT EXECUTED ----
# 3a. Active.
[ "$(systemctl is-active "${UNIT_NAME}")" = 'active' ]

# 3b. UNMASKED, and structurally un-enableable. Assert the printed STRING is exactly `static`.
enabled="$(systemctl is-enabled "${UNIT_NAME}" 2>&1 || true)"
[ "${enabled}" = 'static' ]            # NOT `!= enabled`, NOT the verify.sh masked|disabled|static set
[ ! -e "${MASK_LINK}" ] && [ ! -L "${MASK_LINK}" ]      # direct proof the mask symlink is gone

# 3c. Restart policy.
[ "$(systemctl show -p Restart   --value "${UNIT_NAME}")" = 'no' ]
[ "$(systemctl show -p NRestarts --value "${UNIT_NAME}")" = '0'  ]
[ "$(systemctl show -p TimeoutStopUSec --value "${UNIT_NAME}")" = '45s' ]   # TimeoutStopSec=45

# 3d. ExecStart is bound to the exact SHA — assert the unit-file literal, exactly.
grep -Fxq "ExecStart=${VENV_PY} -m bridge.app" "${UNIT_FILE}"
grep -Fq  "WorkingDirectory=${RELEASE_DIR}/IBKR_PAPER_BRIDGE" "${UNIT_FILE}"
# and no OTHER release/venv SHA may appear anywhere in the unit:
! grep -Eq "(releases|venvs)/(?!${CANDIDATE_SHA})[0-9a-f]{40}" "${UNIT_FILE}" \
  || true   # see note below — implemented with grep -oE + a comparison loop, not PCRE

# 3e. No [Install] section (verify.sh:192-196).
! grep -q '^\[Install\]' "${UNIT_FILE}"

# 3f. Unit fragment hash and size match the recorded values.
[ "$(sha256sum "${UNIT_FILE}" | awk '{print $1}')" = "${EXPECT_UNIT_SHA256}" ]
[ "$(stat -c '%s' "${UNIT_FILE}")" = "${EXPECT_UNIT_BYTES}" ]
[ "$(stat -c '%a %U:%G' "${UNIT_FILE}")" = '644 root:root' ]

# 3g. Rendered-unit / template parity (verify.sh:182-190 intent, no-clobber temp inside RUN_DIR).
sed "s/@RELEASE_SHA@/${CANDIDATE_SHA}/g" \
    "${RELEASE_DIR}/IBKR_PAPER_BRIDGE/deploy/linux/systemd/${UNIT_NAME}.template" \
    > "${RUN_DIR}/.tmp.expected_unit"
mv -n "${RUN_DIR}/.tmp.expected_unit" "${RUN_DIR}/03_expected_unit.rendered"
cmp -s "${RUN_DIR}/03_expected_unit.rendered" "${UNIT_FILE}"

# 3h. The systemd-EFFECTIVE view corroborates the file (catches a drop-in override the file cannot show).
systemctl show -p FragmentPath -p DropInPaths -p ExecStart --value "${UNIT_NAME}" \
    > "${RUN_DIR}/03_effective.out"
# expect FragmentPath = ${UNIT_FILE}; DropInPaths EMPTY; ExecStart naming only ${VENV_PY}.
```

**Design notes.**

- **`is-enabled` must be asserted as the exact string `static`, not merely "not enabled."**
  `verify.sh:212-215` accepts `masked|disabled|static` because pre-start it only cares that the unit
  is not enabled. Post-start that set is too loose in the dangerous direction: it would silently
  accept `masked`, and a masked unit is a *different* host state from the accepted one. `static`
  simultaneously proves (i) the unit is unmasked and (ii) it has no `[Install]` section and therefore
  cannot be enabled at boot. That single token is the strongest available one-line statement of the
  §1 invariant, and B3b pairs it with the direct `MASK_LINK` absence check so the assertion does not
  rest on systemd's vocabulary alone.
- **Do not rely on `is-enabled`'s exit code.** Its exit status semantics vary by state and version;
  the printed token does not. `2>&1 || true` captures the token in every case, exactly as
  `verify.sh:212` already does.
- **B3d's negative match**: `grep -E` has no lookahead. Implement as
  `grep -oE '(releases|venvs)/[0-9a-f]{40}' "${UNIT_FILE}" | awk -F/ '{print $2}' | sort -u` and
  assert the result is the single line `${CANDIDATE_SHA}`. Recorded here so the implementer does not
  reach for PCRE and quietly get an always-true assertion.
- **`DropInPaths` must be empty.** A `.d/` drop-in can override `Restart=`, `ExecStart=` or
  `TimeoutStopSec=` without changing `${UNIT_FILE}`, so 3f/3g would still pass while the running
  service differs. This closes a real hole in the file-hash-only approach.

### 4.4 B4 — paths, ownership, permissions (closes gap matrix B3's COMMAND GAP)

The bounded post-start permissions subcheck. It reproduces `verify.sh` §2/§4 assertions and
**omits nothing except** the mask/active/port-closed preconditions of §6/§8.

| Path | Expected mode / owner | Source |
|---|---|---|
| `${RELEASE_DIR}` | `555 root:root` | `verify.sh:79` |
| `${VENV_DIR}` | `555 root:root` | `verify.sh:105` |
| `${STATE_DIR}` | `750 mtc-bridge:mtc-bridge` | `verify.sh:124` |
| `${LOG_DIR}` | `750 mtc-bridge:mtc-bridge` | `verify.sh:125` |
| `${CONF_DIR}` | `750 root:root` | `verify.sh:126` |
| `${ENV_FILE}` | `600 root:root` — **mode/owner only, never content (D-1)** | `verify.sh:127` |
| `${INSTALL_MANIFEST}` | `640 root:root` | `verify.sh:128` |
| `/etc/logrotate.d/mtc-bridge` | present | `verify.sh:228-232` |

```bash
# ---- NOT EXECUTED ----
# 4a. Immutability of the release + venv trees: no write bit for anyone (common.sh:95-103).
find "${RELEASE_DIR}" -perm /222 -print -quit    # expect EMPTY
find "${VENV_DIR}"    -perm /222 -print -quit    # expect EMPTY

# 4b. Payload inventory still matches its manifest, and every file hash still verifies.
#     Safe post-start: pure read, and the tree is 0555 so nothing can have legitimately changed.
[ "$(sha256sum "${RELEASE_DIR}/RELEASE_SHA256SUMS" | awk '{print $1}')" = "${MANIFEST_SHA256}" ]
( cd "${RELEASE_DIR}" && sha256sum --strict --quiet -c RELEASE_SHA256SUMS )

# 4c. Canonical paths are not symlinks (common.sh:72-77 intent, applied to the live host).
for p in /opt/mtc-bridge /opt/mtc-bridge/releases /opt/mtc-bridge/venvs \
         "${RELEASE_DIR}" "${VENV_DIR}" "${STATE_DIR}" "${LOG_DIR}" \
         "${CONF_DIR}" "${ENV_FILE}" "${INSTALL_MANIFEST}" "${UNIT_FILE}"; do
  [ ! -L "$p" ]
done

# 4d. Service user is non-login, unprivileged, correct primary group (verify.sh:55-75).
#     Verbatim reuse; nothing about this inverts post-start.

# 4e. Secret hygiene, names only, values never read (verify.sh:138-148 — D-1/D-2).
! grep -qE '^[[:space:]]*Environment=.*HL_(API_WALLET_KEY|ACCOUNT_ADDRESS|LIVE_ACK)' "${UNIT_FILE}"
grep -c '^[[:space:]]*\(export[[:space:]]\+\)\?HL_LIVE_ACK=' "${ENV_FILE}"   # expect: 0
```

**UNRESOLVED-INPUT — `MANIFEST_SHA256` (4b).** The accepted `RELEASE_SHA256SUMS` SHA-256 **for
candidate `2ce41e34…321b`** was not located in the records read by this unit; the value recorded in
`WPI_READINESS_RECORD_2026-08-01.md:9` (`bfefea2f…ced02`) belongs to the earlier candidate
`1adf9ae5…`. Resolve it locally from `/etc/mtc-bridge/install_manifest.json`'s
`release_manifest_sha256` field, or from the A-2 install log
(`0376c576…f49bc1`), **before** Stage B is authored. Do not compute it on the host and then
"verify" against itself — that is a tautology, not a check.

**Two deliberate deviations from `verify.sh`, both documented rather than silent:**

1. **File-name discrepancy, recorded not resolved.** `lib/common.sh:18` and both unit templates
   name the env file `/etc/mtc-bridge/mtc-bridge.env`, and `:59` names the error log
   `bridge.err.log`. The transition inventory writes these as `bridge.env` and `bridge.err`. The
   canonical sources are the template and `common.sh`; the inventory strings read as shorthand.
   Stage B must assert the **canonical** names and, if a canonical path is missing, exit 2 rather
   than fall back to the shorthand name. This is flagged as a documentation-shorthand discrepancy —
   **not** as an observed host fault, because no host read occurred in this unit.
2. **`logrotate -f` is NOT part of Stage B.** `COMMANDS.md:221` runs a forced rotation as part of
   P4-07 evidence. Forced rotation *writes* — it renames and recreates log files. That is a
   mutation and belongs to no read-only stage.

### 4.5 B5 — effective sandboxing directives

```bash
# ---- NOT EXECUTED ----
systemctl show "${UNIT_NAME}" \
  -p NoNewPrivileges -p PrivateTmp -p PrivateDevices -p ProtectSystem -p ProtectHome \
  -p ProtectProc -p ProcSubset -p ProtectClock -p ProtectHostname -p ProtectKernelTunables \
  -p ProtectKernelModules -p ProtectKernelLogs -p ProtectControlGroups -p RestrictNamespaces \
  -p RestrictRealtime -p RestrictSUIDSGID -p LockPersonality -p RemoveIPC -p UMask \
  -p CapabilityBoundingSet -p AmbientCapabilities -p RestrictAddressFamilies \
  -p SystemCallArchitectures -p ReadWritePaths -p User -p Group \
  > "${RUN_DIR}/05_sandbox.out"
```

PASS = every property's **effective** value equals the template declaration
(`mtc-bridge-first-start.service.template:62-91`): `NoNewPrivileges=yes`, `PrivateTmp=yes`,
`ProtectSystem=strict`, `CapabilityBoundingSet=` (empty), `AmbientCapabilities=` (empty),
`RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX`, `UMask=0077`, `User=mtc-bridge`,
`ReadWritePaths=/var/lib/mtc-bridge /var/log/mtc-bridge`.

This is the **effective** check that B3g's byte-comparison cannot give: `show` reports what the
kernel/systemd actually applied, including any drop-in or unsupported-directive downgrade. Assert
both; they answer different questions.

### 4.6 B6 — credential-free DISARMED runtime (allowlist projection, no raw capture)

```bash
# ---- NOT EXECUTED ----
curl -fsS --max-time 5 --noproxy '*' "http://${BIND}:${PORT}/api/status" \
  | "${VENV_PY}" -c '
import json, sys
ALLOW = {"state_version", "state", "app_state", "mode", "network",
         "exchange_conn", "credential_lookup", "exchange_enabled", "arm_enabled"}
def project(node):
    if isinstance(node, dict):
        return {k: (project(v) if k in ALLOW or isinstance(v, (dict, list))
                    else {"__redacted__": type(v).__name__})
                for k, v in node.items()}
    if isinstance(node, list):
        return [project(v) for v in node]
    return node
json.dump(project(json.load(sys.stdin)), sys.stdout, indent=2, sort_keys=True)
' > "${RUN_DIR}/06_status_projected.json"
```

**PASS predicates** (from A-5/A-7/A-8/A-9 recorded fields and the transition inventory):
`state_version = 1`; state `DISARMED`; mode `credential_free_disarmed`; and `network`,
`exchange_conn`, `credential_lookup`, `exchange_enabled`, `arm_enabled` **all off**.

**Design notes.**

- The allowlist is derived from *recorded evidence fields*, not from a full read of the API schema,
  which this unit did not perform. That is why the projector is an allowlist with a name-preserving
  redaction fallback rather than a denylist: an unknown key is redacted by default and its *name*
  still appears, so schema drift is visible without any value ever reaching disk (**D-3**).
- The raw body exists only in a pipe. It is never assigned to a shell variable (which would put it in
  the process environment of every child), never written, never echoed.
- `--noproxy '*'` prevents an inherited `http_proxy` from turning a loopback read into an egress
  event.
- **`curl` failure is not a pass.** `-f` makes a non-2xx an error; a connection refusal means the
  service is not serving, which contradicts B3a and is exit 2.

### 4.7 B7 — writer count, listener, firewall (the inverted block)

```bash
# ---- NOT EXECUTED ----
# 7a. EXACTLY ONE bridge.app writer, and it is MainPID. (verify.sh:237-241 expects ZERO pre-start.)
mapfile -t writers < <(pgrep -f '[b]ridge\.app' || true)
[ "${#writers[@]}" -eq 1 ]
[ "${writers[0]}" = "$(systemctl show -p MainPID --value "${UNIT_NAME}")" ]

# 7b. That writer is inside the unit's cgroup — not a stray process that merely matches the pattern.
[ "$(systemctl show -p ControlGroup --value "${UNIT_NAME}")" \
  = "/$(tr -d '\0' < /proc/${writers[0]}/cgroup | sed 's/^0:://')" ]   # normalise before comparing

# 7c. Exactly one listener on the control port, loopback only.
ss -H -ltnp "sport = :${PORT}" > "${RUN_DIR}/07_listeners.out"
#   expect exactly 1 line; Local Address:Port = 127.0.0.1:8790; owning pid = MainPID.
#   MUST NOT use verify.sh's assert_control_port_closed (common.sh:208-218) here — post-start it is
#   inverted and would fail correctly-running state.

# 7d. No non-loopback listener anywhere on that port (common.sh:195-206 — still valid post-start).
ss -H -ltn | awk -v p=":${PORT}" '$4 ~ p && $4 !~ /^127\.0\.0\.1:/ && $4 !~ /^\[::1\]:/'  # expect EMPTY

# 7e. UFW read-only, active, default-deny in, SSH-only, no mention of 8790 (common.sh:153-179).
ufw status verbose > "${RUN_DIR}/07_ufw.out"
```

Optional host-side reprobe (the A-8 method, run from the Windows operator host, not from the staging
host): assert port 22 reachable and port 8790 **not** reachable. It is optional because it needs the
operator host and adds no staging-host state; when run it is a separate artifact with its own
`RUN_ID`, exactly as A-8 was split into `gatea_A8.sh` + `gatea_A8_host.ps1`.

### 4.8 B8 — seal and verdict

Write `00_manifest.txt` (already accumulated by `seal()`), hash the manifest itself, print that hash
to the terminal, write `VERDICT`, exit. **Stage B ends here.** It does not fetch the directory to
Windows, does not commit anything, and does not suggest a next stage.

### 4.9 Stage B stop conditions

- More than one installed release, or any `current`/`previous` symlink → exit 2.
- Steady unit present in either directory → exit 2.
- `is-enabled` ≠ `static`, or the mask symlink exists → exit 2 (host state differs from §1).
- MainPID ≠ `189813`, or `NRestarts` ≠ 0 → exit 2 (the process was replaced under `Restart=no`).
- Unit fragment hash ≠ `538c1c60…279bd`, or non-empty `DropInPaths` → exit 2.
- `verify_lock` non-zero, or `packages` ≠ 56, or lock blob hash ≠ `40873556…8ec3` → exit 2.
- Writer count ≠ 1, any non-loopback listener, or any UFW rule beyond SSH → exit 2.
- Any assertion that cannot be made because a tool is missing → exit 3.

---

## 5. Stage C1 — post-SIGTERM clean shutdown / no dangling state

**Closes:** WP0 I-R4, the single **OPEN** minimum restart invariant
(`WP0_SCOPE_BASELINE_RECORD_2026-07-31.md:366`, and the Lead assessment at `:368-384`), and gap
matrix C1 / E8.

**The gap this closes.** WP0 states plainly: *"No test asserts SIGTERM/lifespan shutdown leaves no
dangling state."* And there is no verifier for it either. `verify.sh` cannot be that verifier — it
asserts a *pre-start* world. So "no dangling state" has never been given an operational definition.
**§5.2 is that definition.** Everything else in this stage is instrumentation around it.

**Authority:** an explicit named lift for **one** `systemctl stop`, plus the budget lift. **Blocked.**
**Mutation class:** `mutating-host`. **End state:** service **stopped**, still unmasked. This is a
departure from the §1 invariant and must be acknowledged in the authorising sentence, together with
the owner's decision about whether a recovery start (separate authority) will follow.

### 5.1 Preconditions (all must hold before the stop; any miss = exit 2, no stop)

1. A Stage B run with `VERDICT = B PASS` exists for the **same host, same day**, and its
   `00_manifest.txt` hash is supplied to C1 as a preregistered argument. C1 re-reads that file and
   checks the hash. C1 does **not** re-run Stage B (R1: one authority, one artifact).
2. `NRestarts = 0` and MainPID matches the Stage B value.
3. `TimeoutStopUSec = 45s`, `KillSignal = SIGTERM`, `FinalKillSignal = SIGKILL`, `KillMode = mixed`
   — read from `systemctl show`, so the *effective* contract is confirmed, not just the template.
4. The operator has recorded, out of band, that the service will be left **stopped**.

### 5.2 "No dangling state" — the operational definition (normative)

A SIGTERM shutdown is clean **iff all seven hold**:

| # | Predicate | Instrument |
|---|---|---|
| **N1** | The unit reaches `inactive` with `Result=success`, `ExecMainCode=1` (`CLD_EXITED`) and `ExecMainStatus=0` | `systemctl show -p ActiveState -p Result -p ExecMainCode -p ExecMainStatus` |
| **N2** | `FinalKillSignal=SIGKILL` was **not** used | journal for the unit contains **no** `State 'stop-sigterm' timed out` and **no** `Killing process` line in the stop window |
| **N3** | Stop latency `< 45 s` | `InactiveEnterTimestampMonotonic − ActiveExitTimestampMonotonic`, corroborated by wall-clock around the `systemctl stop` call |
| **N4** | `NRestarts` still `0`; the unit did not re-activate | `systemctl show -p NRestarts -p NActiveTasks`; `is-active` = `inactive` |
| **N5** | Zero `bridge.app` writers; **control port fully closed** | `pgrep -f '[b]ridge\.app'` empty; `assert_control_port_closed` semantics (`common.sh:208-218`) — **valid again**, because the pre-start world has returned |
| **N6** | **SQLite left clean:** `bridge.db-shm` **absent**, and `bridge.db-wal` absent or exactly `0` bytes; no process holds an open descriptor on `bridge.db*` | `stat` / `find`; `lsof -t -- ${STATE_DB}` empty (missing `lsof` ⇒ exit 3, never a skip) |
| **N7** | No residual unit runtime: `ControlGroup` empty and `/sys/fs/cgroup/system.slice/${UNIT_NAME}` absent; `PrivateTmp` namespace torn down | `systemctl show -p ControlGroup`; `test -d` |

N6 is the concrete reading of WP0's *"the SQLite WAL is left clean"* (`:375`). SQLite removes the
`-shm` file when the last connection to a WAL database closes and checkpoints the WAL; a surviving
`-shm`, or a non-empty `-wal`, is exactly the "dangling state" the invariant names.

### 5.3 The ordering rule that makes N6 measurable (critical)

> **N6 must be captured BEFORE any read of the database — including a read-only one.**

`wal_state_bundle.py` documents this against itself twice: `:602-604` ("SQLite may materialise empty
WAL/SHM files while opening a read-only connection") and `:491-500` (a zero-byte WAL can appear
purely from opening a read-only WAL-mode database). A verifier that opens the DB first and *then*
looks for sidecars will observe sidecars it created and report a false failure — or, worse, be
"fixed" later by relaxing N6 into meaninglessness.

**Therefore the C1 sequence is fixed and may not be reordered:**

```text
 1. preconditions (§5.1)                 read-only, no DB access
 2. record ActiveExitTimestampMonotonic baseline + wall clock
 3. systemctl stop <unit>                THE MUTATION — exactly once, never retried
 4. wait for is-active != active, bounded by 60s poll; timeout => exit 2
 5. N1, N2, N3, N4, N5, N7               no DB access yet
 6. N6 sidecar + fd snapshot             ** still no DB access **   <-- the boundary
 7. DB consistency read (§5.4)           first and only DB access; its sidecar side effects are
                                         expected, and are recorded as post-N6 artifacts
 8. seal, verdict, EXIT                  no start, no mask, no next stage (R2)
```

If step 4 times out, or step 3 returns non-zero, C1 stops with exit 2 and **does not retry the
stop**. A second stop attempt after an unexplained first is precisely the "retry blindly" that
`rollback.sh:89` refuses to do.

### 5.4 DB consistency read (step 7)

```bash
# ---- NOT EXECUTED ----
# Writer is down, so this is a quiescent read. Read-only URI; never a write, never a repair.
"${VENV_PY}" -c '
import sqlite3, sys
con = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True)
print("quick_check=%s"      % con.execute("PRAGMA quick_check").fetchone()[0])
print("integrity_check=%s"  % con.execute("PRAGMA integrity_check").fetchone()[0])
print("foreign_key_check=%d"% len(con.execute("PRAGMA foreign_key_check").fetchall()))
print("app_state=%s"        % (con.execute(
      "SELECT value FROM meta WHERE key=?", ("app_state",)).fetchone() or ("<absent>",))[0])
con.close()
' "${STATE_DB}" > "${RUN_DIR}/07_db_postcheck.out"
```

PASS: `quick_check=ok`, `integrity_check=ok`, `foreign_key_check=0`, and `app_state` ∈
{`DISARMED`, `KILLED`} — **never** `ARMED`. The `meta(key, value)` shape and the `app_state` key are
source-confirmed (`bridge/store/db.py:654-657`, `:4313-4315`; `bridge/app.py:109-110`).

**Never `PRAGMA integrity_check` with a write-capable handle, never `VACUUM`, never `.recover`,
never a repair of any kind.** Plan §19 Safety Rule: *"Never intentionally corrupt the active runtime
database."* A repair attempt on evidence is worse than corruption — it destroys the record of what
happened.

### 5.5 What C1 explicitly does NOT prove

- **Invariant continuity across the stop.** A pre-stop baseline would have to be captured from a
  *live* writer, and `wal_state_bundle.py` correctly fails such a capture closed on drift
  (`:685-686`). A `--allow-live-source` baseline is a warning-class artifact, not a continuity proof
  (gap matrix C3 ⚠). Continuity is therefore deferred to **C3-b**, in the quiesced window C1 opens.
  C1 must state this in its own `VERDICT` file rather than let a reader infer it.
- **Recovery.** Whether the service comes back is `KVM2-P4-08A`/`08B` and is not designed here.
- **Reboot.** A stop is not a reboot; see C2.

### 5.6 Failure disposition

Timeout-to-SIGKILL (N2 or N3 fails), a surviving writer (N5), a dangling `-shm`/non-empty `-wal`
(N6), or DB drift (§5.4) is a **STOP**, and under plan §19 SMALL-GAP treatment is **not available**
for I-R4: the outcome routes to FULL-TASK → Deferred Delivery Stage 2 or BLOCK, reported to the
owner (`WP0_SCOPE_BASELINE_RECORD_2026-07-31.md:379-384`). It is a candidate-repair signal — which
changes the frozen SHA and reopens the audit picture — not a documentation outcome, and **no code
change to the shutdown path is authorised on the strength of an observation alone.**

### 5.7 D026 — if a regression test is offered as the closure

Any new test proposed as proof that I-R4 is closed is **not closure evidence** until it has been
shown **RED** against the exact pre-fix/reverted behaviour (or an equivalent deliberate
falsification) **and GREEN** with the fix, with the commands and real output recorded
(`AGENTS.md` §D026). For a SIGTERM/lifespan-shutdown test the falsification must be one that leaves
the defect intact if the test is weak — e.g. neutering `engine.stop()`'s task cancellation, or
forcing the lifespan `finally` to be skipped — and the test must go red. A test that merely asserts
`returncode == 0` around `systemctl stop` will pass against the broken code too; that is failure
mode #2 in the D026 table, verbatim. Absent the demonstration, the test is **supplemental — not
closure**, and I-R4 stays OPEN.

---

## 6. Stage C2 — post-reboot read-only subcheck

**Closes:** gap matrix C2, and gives G1's *"reboot DISARMED"* a precise, falsifiable meaning.

**Why a definition is needed first.** The first-start unit has `Restart=no` **and no `[Install]`
section**, so it is structurally incapable of starting at boot; the steady profile is a gated
artifact that is not installed and itself has no `[Install]`. A reboot therefore cannot produce a
running-but-disarmed service. It also does not *create* a mask: mask state is a symlink in
`/etc/systemd/system`, which survives a reboot unchanged. So "reboot DISARMED" here means
**DISARMED-by-absence**: no process, no listener, no order, and persisted DB state not ARMED.

### 6.1 Scenario declaration — before the reboot, in writing

Exactly one scenario is preregistered in the authorising sentence. Choosing after the fact is
evidence laundering and is a stop condition in its own right.

| | Scenario **A** — plain reboot | Scenario **B** — authorised stop+mask, then reboot |
|---|---|---|
| Pre-reboot state | active, unmasked (the §1 invariant) | stopped and masked (requires C1 and/or C4 first) |
| Extra authority | reboot only | reboot **plus** the stop/mask authority |
| `is-active` after | `inactive` | `inactive` |
| `is-enabled` after | **`static`** | **`masked`** |
| `MASK_LINK` after | absent | symlink → `/dev/null` |

Both scenarios share predicates P1–P5 below. Only the mask-state row differs.

### 6.2 Post-reboot predicates (all read-only; run after the host returns)

| # | Predicate | Note |
|---|---|---|
| **P1** | `systemctl is-active ${UNIT_NAME}` = `inactive`; `ActiveEnterTimestamp` is empty (never activated this boot) | proves no auto-start |
| **P2** | `is-enabled` = the scenario's declared token, **exactly**; `MASK_LINK` presence matches | the §4.3 strict-token rule applies here too |
| **P3** | zero `bridge.app` writers; control port `8790` closed (`common.sh:208-218` — valid again) | DISARMED-by-absence, half 1 |
| **P4** | persisted `app_state` ∈ {`DISARMED`, `KILLED`}, never `ARMED` — read with the §5.4 read-only snippet | DISARMED-by-absence, half 2 |
| **P5** | `uptime -s` / `systemd-analyze` confirm the boot actually happened, and `journalctl --list-boots` shows exactly one new boot | proves the reboot occurred and only once |
| **P6** | the §4.4 permissions/ownership table still holds, and the unit fragment hash is still `538c1c60…279bd` | a reboot must not change installed state |

**P4 ordering caveat.** The §5.3 rule applies with equal force: capture the sidecar state *before*
the P4 read, because the P4 read can materialise a zero-byte `-wal`/`-shm`. If C2 follows scenario A
without a preceding C1, the sidecar state at boot is whatever systemd's shutdown SIGTERM left — which
is itself interesting evidence and must be captured before it is disturbed.

### 6.3 A real observation, recorded but not credited

A plain reboot *does* send SIGTERM to the running unit as part of system shutdown, so scenario A
incidentally exercises the shutdown path. **It is not a substitute for C1.** During shutdown the
unit's `TimeoutStopSec=45` interacts with systemd's own `DefaultTimeoutStopSec` and the final
`systemd-shutdown` kill sweep, the journal may not be fully persisted for the last moments, and stop
latency cannot be bounded from outside. C1's instrumented, isolated stop is the measurable one. C2
may *record* what the shutdown transcript shows; it may not *claim* I-R4 from it.

### 6.4 Stop conditions

Any writer, any listener, `app_state = ARMED`, a mask state that does not match the declared
scenario, more than one new boot, or any change to the installed state → **exit 2**. Do not
"correct" the mask state to match the scenario after the fact.

---

## 7. Stage C3 — WAL bundle capture → verify → restore-into-temp → invariant re-derivation

**Closes:** gap matrix C3's *"restore-into-temp wrapper is not yet authored"* COMMAND GAP, and the
WPI §6 obligation *"Prove SQLite backup/restore and risk/history continuity."*

### 7.1 The design fact that shapes this stage

`wal_state_bundle.py` has exactly **two** subcommands — `create` and `verify` (`:1062-1080`). **There
is no `restore` subcommand.** So "restore into a temp DB and re-verify" cannot be a flag; it has to
be composed. The composition that works, using only existing tooling:

> Copy the bundle's `bridge.db` to a second temporary path, then run **`create` against that copy**
> and assert that the resulting `invariants_sha256` equals the original bundle's.

This works because `create` already does everything a restore-validator needs: it opens the source
read-only (`:618`), runs `integrity_check` and `foreign_key_check` on it (`:630-635`), calls
`collect_invariants` (`:639`), and emits `invariants_sha256` in its JSON report (`:698`, `:752`).
Feeding it the restored copy re-derives the invariants from the restored bytes independently.

**Assert on `invariants_sha256`, never on `bundle_db_sha256`.** The re-`create` performs a fresh
online backup, so the produced file is a new physical database and its hash legitimately differs.
The *invariants* — counts, open trades, live orders, per-environment realized PnL, consecutive
closed losses, the `risk_days` ledger (`:19-23`) — are exactly the risk/history continuity the
predicate is about, and they must match to the hash. An implementer who asserts `bundle_db_sha256`
here will get a spurious failure and may then "fix" it by dropping the assertion entirely.

### 7.2 C3-a — live-source capture (WARNING CLASS ONLY)

Capturing from the running bridge **without** `--allow-live-source` will correctly fail closed on
drift (`:685-686`). Capturing **with** it produces an artifact whose manifest records
`changed_during_capture` and is, by construction, **not** a cutover or continuity proof
(`COMMANDS.md:190-191`: *"Do not pass `--allow-live-source`: for a cutover the writer must already be
quiesced, so any source drift during capture is a stop condition, not a warning."*).

C3-a therefore exists only as an optional smoke observation. Its output must be filed as
`WARNING-CLASS — NOT A CONTINUITY PROOF` in its own `VERDICT`, and it may never be passed to C4 as
the state manifest.

### 7.3 C3-b — quiesced capture, verify, restore-into-temp (the real proof)

Runs **only** inside the quiesced window C1 opens, and **only** if the authorising sentence named
both (R4).

```bash
# ---- NOT EXECUTED — Stage C3-b ----
WSB="${RELEASE_DIR}/IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py"   # stdlib-only; venv python is fine
BUNDLE_DIR="${RUN_DIR}/bundle"                     # created by the tool; must not pre-exist
TEMP_RESTORE="${RUN_DIR}/restore/bridge.db"        # the "second temp DB"
REDERIVE_DIR="${RUN_DIR}/rederive"
HASH_RECORD="${RUN_DIR}/expected.sha256"           # separately held; see COMMANDS.md Stage E

# --- 1. capture from the QUIESCED source. No --allow-live-source. No --force. -------------------
"${VENV_PY}" "${WSB}" create --source "${STATE_DB}" --out-dir "${BUNDLE_DIR}" \
    > "${RUN_DIR}/10_capture_report.json"
# expect rc 0 and report.verdict == "CAPTURED"

# --- 2. preregister the expected hashes BEFORE verifying (COMMANDS.md:134-159 pattern) ----------
EXPECTED_BUNDLE_SHA256="$("${VENV_PY}" -c 'import json,sys;print(json.load(open(sys.argv[1]))["bundle_db_sha256"])' "${RUN_DIR}/10_capture_report.json")"
EXPECTED_INVARIANTS_SHA256="$("${VENV_PY}" -c 'import json,sys;print(json.load(open(sys.argv[1]))["invariants_sha256"])' "${RUN_DIR}/10_capture_report.json")"
EXPECTED_MANIFEST_FILE_SHA256="$(sha256sum "${BUNDLE_DIR}/bundle_manifest.json" | awk '{print $1}')"
for h in "${EXPECTED_BUNDLE_SHA256}" "${EXPECTED_INVARIANTS_SHA256}" "${EXPECTED_MANIFEST_FILE_SHA256}"; do
  [[ "${h}" =~ ^[0-9a-f]{64}$ ]] || exit 2
done
umask 077
printf 'EXPECTED_BUNDLE_SHA256=%s\nEXPECTED_INVARIANTS_SHA256=%s\nEXPECTED_MANIFEST_FILE_SHA256=%s\n' \
  "${EXPECTED_BUNDLE_SHA256}" "${EXPECTED_INVARIANTS_SHA256}" "${EXPECTED_MANIFEST_FILE_SHA256}" \
  > "${HASH_RECORD}"        # `set -C` refuses if it already exists

# --- 3. verify the bundle against those hashes -------------------------------------------------
"${VENV_PY}" "${WSB}" verify --bundle-dir "${BUNDLE_DIR}" \
    --expect-bundle-sha256 "${EXPECTED_BUNDLE_SHA256}" \
    --expect-invariants-sha256 "${EXPECTED_INVARIANTS_SHA256}" \
    > "${RUN_DIR}/11_verify_report.json"
# expect rc 0 and report.verdict == "VALID"

# --- 4. RESTORE INTO A TEMP DB — never over ${STATE_DB} ----------------------------------------
mkdir "${RUN_DIR}/restore"
cp -- "${BUNDLE_DIR}/bridge.db" "${TEMP_RESTORE}"          # plain cp; no -f, no clobber possible
[ "$(sha256sum "${TEMP_RESTORE}" | awk '{print $1}')" = "${EXPECTED_BUNDLE_SHA256}" ] || exit 2

# --- 5. RE-DERIVE invariants from the restored copy (the composed "restore verification") -------
"${VENV_PY}" "${WSB}" create --source "${TEMP_RESTORE}" --out-dir "${REDERIVE_DIR}" \
    > "${RUN_DIR}/12_rederive_report.json"
REDERIVED="$("${VENV_PY}" -c 'import json,sys;print(json.load(open(sys.argv[1]))["invariants_sha256"])' "${RUN_DIR}/12_rederive_report.json")"

# --- 6. THE CONTINUITY PREDICATE ---------------------------------------------------------------
[ "${REDERIVED}" = "${EXPECTED_INVARIANTS_SHA256}" ] || exit 2
```

### 7.4 Why each guard is there

| Guard | Reason |
|---|---|
| no `--allow-live-source` in C3-b | the writer is already down; drift is then a stop, not a warning (`COMMANDS.md:190-191`) |
| no `--force` | `--force` replaces an existing bundle (`:1074`); combined with a reused `RUN_DIR` it silently destroys prior evidence. §3.2 N1 already refuses a reused directory; `--force` would defeat it |
| `${TEMP_RESTORE}` under `${RUN_DIR}` | the restore target must be provably not `${STATE_DB}`. `_resolve_capture_paths` (`:522-559`) rejects source/output aliasing for *its* paths, but the `cp` in step 4 is ours, and ours must be obviously safe by construction |
| assert on `invariants_sha256` | §7.1 — `bundle_db_sha256` legitimately differs on re-capture |
| `HASH_RECORD` written before verify | preregistration; verifying against a hash derived after the fact proves only self-consistency |
| production DB never written | plan §19 Safety Rule; `rollback.sh:104` — *"risk history is evidence, never cleanup"* |

### 7.5 Failure disposition and D026

Exit `2` from either `create` or `verify` means corruption, drift, invariant mismatch, or a
forbidden sidecar (`:598-600`, `:995-1032`) → **STOP**, preserve everything, escalate. Exit `3` is
invalid input or a sanitisation refusal — fix the invocation, do not loosen the tool.

`test_bundle_never_contains_a_wal_shm_trio` (`tests/test_wal_state_bundle.py:289`) and
`test_invariants_preserve_risk_and_history` (`:315`) are **existing** coverage that C3-b exercises on
Ubuntu. Under D026 they are not new closure evidence for any newly named defect, and this stage must
not be written up as if they were.

---

## 8. Stage C4 — rollback stop+mask-only

**Closes:** gap matrix C4's *"the stop+mask-only run-kit step is not yet authored"* COMMAND GAP.

**Scope, exactly.** `rollback.sh` with `--state-manifest-file` and `--state-manifest-sha256` and
**no `--to-*` flags**. It stops (SIGTERM, 45 s) if active, masks, asserts the control port closed and
no `bridge.app` writer, preserves `/var/lib/mtc-bridge`, and writes
`/etc/mtc-bridge/rollback_manifest.json` (`rollback.sh:79-181`).

**Release-rebind is NOT designed here, and must not be attempted.** `--to-release-sha` requires an
already-installed previous immutable release plus its venv (`rollback.sh:117-134`), and only
candidate `2ce41e34…321b` is installed — the old `ebada020…` install and venv are already absent.
That prerequisite is **unmet** (gap matrix G3). Do not invent a target SHA. Do not reinstall an old
release to manufacture one.

### 8.1 Inputs

| Input | Source | Note |
|---|---|---|
| `--state-manifest-file` | `${C3B_RUN_DIR}/bundle/bundle_manifest.json` | must come from **C3-b**, never C3-a |
| `--state-manifest-sha256` | `EXPECTED_MANIFEST_FILE_SHA256` from C3-b's `HASH_RECORD` | `rollback.sh:61-62` hashes the file and dies on mismatch |

C3-b is therefore a **hard prerequisite** of C4. This is a genuine dependency, not paperwork:
`rollback.sh` refuses to run without a state-manifest hash it can verify.

### 8.2 Sequence — one stop, maximum evidence

Because `rollback.sh:80-85` stops the unit only *if it is active*, running C1 → C3-b → C4 in that
order means the service is stopped **once**, under C1's instrumentation, and C4 then finds it
already inactive and only masks. Running C4 first would consume the stop un-instrumented and forfeit
the I-R4 evidence permanently for that window.

```text
C1 (instrumented stop)  →  C3-b (quiesced capture/verify/restore)  →  C4 (mask + manifest)
```

Each arrow is a separate authorisation and a separate invocation (R2). C4 must not detect "the
service is already stopped, so C1 probably ran" and skip anything on that basis; it re-asserts its
own preconditions from scratch.

### 8.3 Mandatory dry-run preflight

`rollback.sh` honours `--dry-run` through `run()` (`lib/common.sh:41-48`): every mutating call prints
instead of executing, and §4's manifest write is skipped entirely (`:158`). This is a real,
source-backed safe preflight and it is **mandatory**:

```bash
# ---- NOT EXECUTED — C4 preflight, prints the plan, mutates nothing ----
sudo bash "${RELEASE_DIR}/IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh" \
    --state-manifest-file   "${C3B_MANIFEST}" \
    --state-manifest-sha256 "${C3B_MANIFEST_SHA256}" \
    --dry-run > "${RUN_DIR}/20_rollback_dryrun.out"
```

Read the printed plan in full. It must show exactly: a stop (or "already inactive"), a mask, and
nothing else — **no `install`, no `daemon-reload`, no unit rewrite**, all of which appear only on the
`--to-*` path (`:136-154`). If any of those appear, a `--to-*` flag leaked in: **exit 2, do not
proceed.**

### 8.4 The real run and its postcheck

```bash
# ---- NOT EXECUTED — C4 real run, requires KVM2-P4-08 authority ----
sudo bash "${RELEASE_DIR}/IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh" \
    --state-manifest-file   "${C3B_MANIFEST}" \
    --state-manifest-sha256 "${C3B_MANIFEST_SHA256}" \
    > "${RUN_DIR}/21_rollback.out"
```

Independent postcheck (the run kit re-asserts rather than trusting the script's own log):

| # | Predicate |
|---|---|
| 1 | `is-active` = `inactive`; `is-enabled` = **`masked`**; `MASK_LINK` is a symlink resolving to `/dev/null` |
| 2 | zero `bridge.app` writers; control port `8790` closed |
| 3 | `${STATE_DIR}` present with `bridge.db` intact — mode/owner unchanged, **byte size unchanged** from the C3-b observation |
| 4 | `/etc/mtc-bridge/rollback_manifest.json` exists, `0640 root:root`, and records `"rollback_release_sha": ""`, `"first_start_unit_state": "masked"`, `"service_started_by_this_script": false`, `"state_dir_preserved": true` |
| 5 | `${UNIT_FILE}` SHA-256 is **still** `538c1c60…279bd` — the no-target path must not rewrite the unit |

Predicate 5 is the sharpest one available for proving no rebind occurred, and it is free.

### 8.5 End state and its consequences

C4 leaves the host **stopped and masked**. That is a deliberate, recorded departure from the §1
invariant and it means:

- Stage B, as written, will now fail 3b (`is-enabled` = `masked`, `MASK_LINK` present) and 3a. That
  is **correct behaviour**, not a Stage B bug. Do not relax Stage B to accommodate a post-C4 host.
- A full `verify.sh` run becomes appropriate again for the mask/active/port predicates — but its §3
  lock check and §2 payload checks were already covered by B2/B4, and its `--manifest-sha256`
  argument still needs the UNRESOLVED-INPUT of §4.4.
- Returning to the accepted running state requires `systemctl unmask` + `start`, which is
  `KVM2-P4-08A` authorisation and a single `KVM2-P4-08B` attempt (`rollback.sh:185`). **Not designed
  here, and not implied by C4's authority.**

Because of that last point, the C4 authorising sentence must also state what happens next: leave it
masked, or obtain 08A/08B. Executing C4 without that decision strands the staging host in a state no
one has agreed to, and WP-A still needs the host.

---

## 9. Deliberately not designed here

| Item | Why |
|---|---|
| **C5 — runtime egress / TESTNET-only / no-mainnet capture** | needs credentials **plus** broker/TESTNET network authority, both explicitly unavailable (gap matrix §1, C5). It does **not** require ARM — the TESTNET broker is constructed before any human ARM transition — but ARM remains forbidden regardless, and any future capture must stay DISARMED and no-order. Designing the capture commands now would produce a run kit whose only missing piece is the credential, which is the wrong artifact to leave lying around. |
| **Release-rebind rollback** | unmet prerequisite (§8, G3). |
| **Recovery start after C1 or C4** | `KVM2-P4-08A`/`08B`, separate authority. |
| **Wholesale `verify.sh` post-start** | intentionally fails (G2); Stage B replaces it. |
| **`logrotate -f`** | a write; see §4.4 note 2. |
| **Any executable artifact** | this unit is documentation-only. The stage scripts do not exist and must not be created until the §0 blockers clear. |

---

## 10. Discrepancies and unresolved inputs found in this unit

| # | Finding | Disposition |
|---|---|---|
| 1 | `EXPECT_HOSTNAME` — `GATEA-STAGING` is the **VM name** (`GATE_A_STAGING_HOST_PROVENANCE_2026-08-02.md:107`); the guest OS hostname was not established here | **UNRESOLVED-INPUT.** Resolve locally from the cloud-init seed record before authoring Stage B. Do not assume VM name = OS hostname. |
| 2 | `MANIFEST_SHA256` for candidate `2ce41e34…321b` not located in the records read here; `WPI_READINESS_RECORD_2026-08-01.md:9`'s `bfefea2f…ced02` belongs to candidate `1adf9ae5…` | **UNRESOLVED-INPUT.** Resolve from `install_manifest.json` `release_manifest_sha256` or the A-2 install log before Stage B's 4b. |
| 3 | Env-file name: canonical `mtc-bridge.env` (`common.sh:18`, both templates `:43`/`:42`) vs the inventory's shorthand `bridge.env`. Error log: canonical `bridge.err.log` (templates `:59`/`:57`) vs the inventory's `bridge.err` | Assert canonical names; a missing canonical path is exit 2. Recorded as a **documentation-shorthand discrepancy**, **not** an observed host fault — no host read occurred in this unit. |
| 4 | `wal_state_bundle.py` has **no `restore` subcommand** (`:1062-1080`) | Resolved by design: restore-into-temp is composed from `cp` + a second `create`, asserting `invariants_sha256` (§7.1). |
| 5 | `verify.sh:212-215` accepts `masked\|disabled\|static`; post-start only `static` is correct | Resolved by design: Stage B asserts the exact token (§4.3). `verify.sh` itself is **not** modified — it is correct for its own pre-start mode. |
| 6 | Stale WP0 evidence-map symbol (G4) | Refreshed under this unit's narrow authorisation — see §11. |

---

## 11. Stale evidence-map node (G4) — what was changed and what was not

**Independently re-verified in this unit** (`rg` over `IBKR_PAPER_BRIDGE/tests/`):

| Symbol | Result |
|---|---|
| `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` | **ABSENT** — no definition, no reference, and no partial match for `kill_restart_after_request_commit` or `resumes_once` anywhere under `tests/` |
| `test_kill_persists_across_restart` | EXISTS — `tests/test_api.py:61` |
| `test_killed_alive_is_interrupted` | EXISTS — `tests/test_window_state.py:82` |
| `test_gates_persist_across_restart` | EXISTS — `tests/test_interim_risk_wiring.py:333` |

`WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` I-R2 was edited under this unit's narrow authorisation to
remove the absent symbol, with a dated correction note recording what was removed and why. The
historical text is otherwise preserved; nothing was rewritten silently.

**Deliberately left unchanged:** the same absent symbol also appears in that file's §9.1 row
*"killed/disarmed state survives restart"* (`:308`). This unit's write authorisation names the
**I-R2 evidence-map symbol** only, so `:308` was not touched. It is recorded here and in the
correction note so the residue is visible rather than lost — refreshing it needs its own narrow
authorisation.

**This is an evidence-map defect, not a product defect.** I-R2 retains two source-verified symbols
and its COVERED (code+test) / COVERED-STATIC-on-Ubuntu classification is unaffected. No replacement
symbol was invented. Under D026, the surviving symbols are *existing coverage* and are not closure
evidence for any newly named defect.

---

## 12. Stop conditions for the next session

- Executing **any** command block in this file. Every one is `NOT EXECUTED` and none is authorised.
- Creating any of the five stage scripts as an executable before the §0 budget blocker and the
  relevant named authority lift are both resolved.
- Running `verify.sh` wholesale against the started service (G2).
- Any stop, start, mask, unmask, reboot, install, or firewall change without its own named lift.
- Inventing `EXPECT_HOSTNAME`, `MANIFEST_SHA256`, a rollback target SHA, a replacement test symbol,
  or any hash for an artifact that does not yet exist.
- Destructively testing, repairing, `VACUUM`-ing, or overwriting `/var/lib/mtc-bridge/bridge.db`.
- Reading or printing any credential value, or hashing the env file.
- Discarding `GATEA-STAGING` — it is needed through WP-A.
- Any observed drift from §1 (second release, extra listener, non-loopback bind, ARM enabled,
  credentials present, MainPID change under `Restart=no`): investigate read-only, report, take no
  corrective action.
- Any post-Gate evidence that would require a **product repair** — that changes the frozen SHA and
  reopens the audit picture, and is not a documentation unit.

---

## 13. Acceptance criteria for whoever implements these stages

A stage artifact is acceptable only if all of the following hold:

1. It carries the §3.1 constants as literals and asserts every one of them.
2. It implements `set -Eeuo pipefail`, `set -C`, `IFS=$'\n\t'`, and refuses a pre-existing `RUN_DIR`.
3. It contains **no** action belonging to another stage, and **no** invocation of another stage (R1, R2).
4. Read-only stages accumulate failures and exit once (R3); mutating stages abort at first mismatch (R3).
5. Every assertion that cannot be made returns exit 3 — no assertion is ever skipped.
6. No path outside `${RUN_DIR}` is written.
7. Redaction rules D-1..D-7 are observed; the env file is never read; `/api/status` is never written raw.
8. Every artifact is sealed with `sha256` + byte count into `00_manifest.txt` at creation time.
9. For C1: the §5.3 ordering is present and commented, so a later editor cannot reorder the DB read
   ahead of the N6 sidecar snapshot without deleting an explicit warning.
10. For C3-b: the continuity assertion is on `invariants_sha256`, and `--allow-live-source` and
    `--force` are absent.
11. For C4: `--to-release-sha` / `--to-manifest-sha256` are absent, and the `--dry-run` preflight is
    unconditional.
12. Its own SHA-256 is recorded before execution and re-verified on the host (the run-kit D/E
    pattern: packaged script hash + `SHA256SUMS` members verified, LF-only, syntax-checked).

---

## Routing record

```
Classification      : Tier 4 — protected Bridge deployment/evidence surface; run-kit design contract.
Protected           : yes — deployment/runtime/persistence/restart/rollback evidence surface; documentation only.
Model + provider    : claude-opus-5, effort xhigh (counterpart flagship implementer, AGENTS.md §Two-Tier).
Cheaper-model rationale : protected-surface safety design with adversarial ordering/failure analysis;
                      no cheaper tier is permitted to author protected Bridge deployment procedure.
Exact paths         : writes — MTC_COMMAND_CENTER/11_TRIAGE/POST_GATE_WPL_WPI_RUN_KIT_DESIGN_2026-08-09.md (new),
                      MTC_COMMAND_CENTER/11_TRIAGE/WP0_SCOPE_BASELINE_RECORD_2026-07-31.md (narrow I-R2 refresh + dated note),
                      MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md (prepend),
                      MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md (prepend),
                      MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md (prepend).
                    reads — AGENTS.md; _AI_MEMORY/START_HERE.md; 50-hour plan §17-20 + §23a;
                      GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX / _TRANSITION_INVENTORY (2026-08-09);
                      WP0_SCOPE_BASELINE_RECORD; WPI_READINESS_RECORD; GATE_A_STAGING_HOST_PROVENANCE;
                      GATE_A_A8_PREFLIGHT (style reference); deploy/linux/{README,COMMANDS,verify.sh,
                      verify_lock.py,rollback.sh,package.sh,lib/common.sh,systemd/*.template};
                      tools/wal_state_bundle.py; bridge/app.py + bridge/store/db.py (targeted rg);
                      IBKR_PAPER_BRIDGE/tests (targeted rg for symbol existence only).
Context/tool budget : targeted reads and rg only; no broad repo scan; five-file write ceiling.
Fallback            : none; if the exact model/effort is unavailable, stop as BLOCK without edits.
External API credits: no.
```

## Exclusions

No SSH, sudo, `systemctl`, reboot, service, package/install, pytest, broker/network/exchange,
credential, ARM/order, Git, staging-host, or mutation command was run in this unit. No credential
value was read or printed. No executable script was created. No product code, test, script, schema,
Pine/parity/MTC/trading logic, or existing Gate-A run-kit file was changed. No file outside the
five-file allowlist was modified. Two local read-only derivations were performed on the working
tree — `sha256sum IBKR_PAPER_BRIDGE/requirements.lock` and `rg`/`grep` over
`IBKR_PAPER_BRIDGE/tests` and `bridge/` for symbol and schema existence — and both are recorded
above with their results.
