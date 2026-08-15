# Stage-1 Commit 1 — read-only attestation-only preregistration (L2 draft)

Date: 2026-08-15  
Status: **DRAFT MATERIAL ONLY — NOT COMMIT 1, NOT DISPATCHABLE, NO AUTHORIZATION, NO ACCEPTANCE**  
Audit tier: **T2 documentation/evidence**; this lane is self-verified only because its task contract forbids sub-delegation.

## 0. Purpose and hard boundary

This draft specifies the capture procedure that is intended to become Stage-1 Commit 1. Commit 1 must exist before the grant-#6 capture; the later Commit 2, not Commit 1, consumes the observed values and precedes WP-I op 01. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:488-533,550-579`

This artifact is **attestation-only**. It captures evidence and performs no WP-I transport operation 01–12, no allocation on the host, no service operation, and no WP-I predicate run. The source contract expressly forbids any WP-I transport op between Commit 1 and Commit 2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:502-505,528-533`

This artifact is **read-only on the target host** in the following precise sense: the producer source below calls only process-local operations, read-only file opens, `readlink`, `stat`, hashing, and stdout/stderr writes to the already-established channel. It contains no filesystem write/create/delete/rename/chmod/chown API, no subprocess call, no socket creation, and no service API. Python is launched with `-I -S -B` under a cleared environment; `-B` and `PYTHONDONTWRITEBYTECODE=1` prevent bytecode-cache writes. The need for a cleared environment, pinned interpreter/helper selection, fixed cwd, and no attacker-directed temporary location follows the privileged-child defect rule. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:243-299`

The existing owner grant is narrow: one separately preregistered and committed root-session command set may read `/proc/self/mountinfo`, namespace links, the canonical root-mount identity, and production-time hashes, with no mutation. This draft does not enlarge or spend that grant. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:32-36`

The later owner confirmation permits only the exact preregistered and committed capture on `GATEA-STAGING` using the pinned SSH identity and keeps all other credential and host actions excluded; it is not spendable until the exact preregistration is committed. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-58`

### 0.1 Unresolved prerequisite — do not guess

`ROOT_CHANNEL_TARGET_AND_LAUNCH = UNKNOWN`. The read sources establish that grant #6 runs in the grant-#3 root session, but they do not establish the exact SSH principal, forced-command mapping, or other mechanism that turns the pinned identity into that root session. The published transport rows instead name `gatea@172.24.55.233` for the later unprivileged WP-I operations. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:32-36`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:2-11`

What settles it: a committed source must state the exact root-channel target and the exact remote-command launch mapping for the already approved pinned identity. Until that source exists, the outer SSH argv in §4 cannot be finalized, Commit 1 cannot be claimed complete, and no socket may be opened. This is a missing input, not permission to infer `root@172.24.55.233`, `gatea`, `sudo`, or a forced command. The governing rule is that silence is not authority. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:66-68,85-85`

`SSH_INFRASTRUCTURE_SIDE_EFFECTS = UNKNOWN`. The producer payload cannot write target files, but the read sources do not establish whether sshd, PAM, auditd, or the root-channel wrapper writes connection/accounting logs. If “no mutation” includes infrastructure logging, an authoritative host-channel statement or a read-only execution environment proving those facilities cannot write is required before Commit 1. No weaker claim is made here. The catalogue requires the claim sentence to stay within what the predicate establishes. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:547-613`

## 1. Fixed subject and allocation dependencies

The attested staging subject is `GATEA-STAGING`; the later transport shape names address `172.24.55.233`, login `gatea`, and the pinned identity/known-hosts files. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:35-38,60-60`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:2-11`

The frozen WP-I candidate carried by the source contract is `2ce41e34bceb599d80af24c5c33d835820ec321b`; its release and venv roots are `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` and `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b`. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md:164-170`

The source-fixed allocation parent consumed by `EXPECT_PARENT_MOUNT` is `/home/gatea`; `remote_setup_wpi.sh` names that exact parent and requires the covering-mount record in a fixed field order. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh:142-151,203-217`

The following values are dependencies on the Stage-1 allocation record now being drafted by lane L1. The reconciliation says that record must supply the concrete base, P0/RO RUNIDs, stage IDs, `REMOTE_BASE`, confirmation token, operator root, collision/grammar results, and append-only dispositions. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:62-70`

| Draft token | Exact filler | Source of filler | Commit-1 rule |
|---|---|---|---|
| `{{ATTESTATION_RECORD_ID}}` | The one-use attestation record identifier allocated in the signed Stage-1 allocation record | Lane-L1 allocation record, exact field `ATTESTATION_RECORD_ID` | Must satisfy that record’s grammar/collision result; no independent typing |
| `{{BASE}}` | One allocated `BASE` | Lane-L1 allocation record, field `BASE` | Informational binding; producer does not allocate or consume it |
| `{{P0_RUNID}}` / `{{RO_RUNID}}` | The two derived RUNIDs | Lane-L1 allocation record | Informational binding only; no WP-I operation runs |
| `{{REMOTE_BASE}}` | Exact `/home/gatea/wpi_staging_<BASE>` | Lane-L1 allocation record, field `REMOTE_BASE` | Used only to prove the allocation-parent relationship; no host path is created or opened by this capture |
| `{{OPERATOR_ATTESTATION_ROOT}}` | Exact create-once local evidence root | Lane-L1 allocation record, field `operator_root`, plus its attestation-record child rule | Recorder may write only here, on the operator, never on the target |
| `{{CONFIRM_TOKEN}}` | Exact allocation confirmation token | Lane-L1 allocation record | Recorded but never interpreted as authority |

No allocation-dependent token may remain in the committed Commit-1 package. Allocation occurs locally before Commit 1 and performs no host contact. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-501`

## 2. Observation placeholders — deliberately non-consumable

Each value below is absent before the committed capture and therefore remains a literal non-consumable placeholder in Commit 1. The four namespace identities, canonical root-mount identity, effective allocation-parent mount identity, projection-v2 digest, record byte count, and record digest become computable only after the Commit-1-bound capture. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:535-548`

| Commit-1 field | Literal value in Commit 1 | Exact post-capture filler and source |
|---|---|---|
| `P0_ATTESTED_USER_NS` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | `user_ns` from the successful producer stdout, derived from exact `readlink('/proc/1/ns/user')` |
| `P0_ATTESTED_MNT_NS` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | `mnt_ns` from exact `readlink('/proc/1/ns/mnt')` |
| `P0_ATTESTED_PID_NS` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | `pid_ns` from exact `readlink('/proc/1/ns/pid')` |
| `P0_ATTESTED_NET_NS` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | `net_ns` from exact `readlink('/proc/1/ns/net')` |
| `P0_ATTESTED_ROOT_MOUNT_ID` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | `root_mount_id`, decimal `st_dev:st_ino` for `/`; RP6 consumes exactly one colon-separated numeric device/inode identity `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh:1394-1414` |
| `EXPECT_PARENT_MOUNT` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | decoded `expect_parent_mount_b64`, formatted `device=… root=… mount_point=… fstype=… source=… shared_mount_point_records=…` for `/home/gatea` `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh:288-337` |
| `WPI_FIXED_TRUSTED_PYTHON` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | `trusted_python_path`, the resolved non-symlink `/usr/bin/python3.<minor>` leaf actually executing the producer; the successor requires the same leaf in P0, RP7, and both tool-pin maps `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:41-45` |
| `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | `projection_sha256` over the exact decoded `projection_b64` bytes |
| `ATTESTATION_EVIDENCE_BYTES` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | byte count of the closed operator record, computed locally after stdout/stderr/rc capture |
| `ATTESTATION_EVIDENCE_SHA256` | `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` | SHA-256 of those same closed operator-record bytes |

Commit 2 is the only consumer: it derives the values once from the captured bytes, replaces every attestation placeholder, records evidence path/bytes/digest/producer/status, and must contain no unresolved dispatch token. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:550-570`

## 3. Exact producer contract

### 3.1 Producer identity

Final package path: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/capture_wpi_attestation.py`.

Encoding and bytes: ASCII, LF line endings, no BOM, final LF. The exact producer is the code-block body in §3.6 after extraction with no fence lines and no indentation change. Before Commit 1, `{{PRODUCER_BYTES}}`, `{{PRODUCER_SHA256}}`, and `{{PRODUCER_GIT_BLOB_OID}}` are filled from those final bytes by the local package builder; these are build outputs, not host observations. Commit 1 must contain no unfilled producer-identity field. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:511-525`

### 3.2 Exact inner argv, environment, cwd, and stdin

Once §0.1’s outer root-channel route is fixed, the remote command string after that route is exactly:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/root PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -S -B - --record-id {{ATTESTATION_RECORD_ID}} --candidate 2ce41e34bceb599d80af24c5c33d835820ec321b --allocation-parent /home/gatea --main-pid 189813 --producer-sha256 {{PRODUCER_SHA256}}
```

Stdin is exactly the producer bytes named in §3.1. The producer calls `chdir('/')` before any observation and requires `cwd=/`. The accepted RP7 bytes freeze `WPI_MAINPID=189813`, and projection v2 includes `/proc/<WPI_MAINPID>/ns/net`. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:1214-1227,1387-1392`

No other environment entry is allowed. No argument may be shell-expanded, independently typed, or learned from the target. `{{ATTESTATION_RECORD_ID}}` comes only from L1 and `{{PRODUCER_SHA256}}` only from the finalized local producer bytes.

### 3.3 Exact read set and why each access cannot write

| Producer operation | Exact target | Access | Why the producer cannot write the target |
|---|---|---|---|
| `chdir` | `/` | process cwd only | Changes only the producer process’s cwd; opens no filesystem object for write |
| `readlink` | `/proc/self/exe`, `/usr/bin/python3`, `/proc/{1,self}/ns/{user,mnt,pid,net}` | metadata read | Python `os.readlink` has no write mode and creates no descriptor with write access |
| `realpath`/`lstat`/`stat` | `/usr/bin/python3` chain, resolved interpreter leaf, `/`, `/home/gatea` | metadata read | These APIs inspect names/objects only; no mutation API exists in the producer |
| `open` + `read` | resolved interpreter leaf | `O_RDONLY|O_CLOEXEC|O_NOFOLLOW` | The only open flags exclude create, truncate, append, and read-write; used only for evidence SHA-256 |
| `open` + `read` | `/proc/self/mountinfo` | `O_RDONLY|O_CLOEXEC` | One complete byte-preserved read; no write-capable flag is present |
| stdout/stderr write | inherited fd 1/fd 2 | channel output | Writes only to the established capture channel, not a target-host pathname |

The source contract requires one complete byte-preserved `/proc/self/mountinfo` capture, the four `/proc/1/ns/*` link results, root identity, allocation-parent covering mount, and production-time binding. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:502-523`

### 3.4 Status-before-output and rc grammar

The producer buffers every observation, validates reader completeness, parses the entire mount table, builds the entire projection, and computes all hashes before its first stdout byte. This enforces status-before-output: partial or failed work is never interpreted as a completed observation. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:368-420`

Exactly two terminal classes exist:

- rc `0`: stdout matches §3.5 exactly, stderr is empty, and the final stdout line is `ATTESTATION_V1_PASS`.
- rc `3`: stdout is empty; stderr is exactly one LF-terminated line `ATTESTATION_V1_STOP reason=<fixed-token>`. No observed field is consumable.

Any other rc, any stdout on rc 3, any stderr on rc 0, a missing terminal line, duplicate key, unknown key, invalid field grammar, incomplete base64, byte-count/digest mismatch, or projection recount mismatch is recorder `STOP`. The design catalogue requires inability to evaluate to remain STOP and requires rc/stderr/completeness to be adjudicated before stdout. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107,368-420`

### 3.5 Exact successful stdout grammar and order

Every record is ASCII and LF-terminated. Keys occur exactly once and in this exact order; values may not contain CR, LF, NUL, TAB, or `=` unless the row explicitly uses base64.

```text
ATTESTATION_V1_BEGIN
protocol=normalised_path_projection_v2
record_id=<safe-component>
candidate=2ce41e34bceb599d80af24c5c33d835820ec321b
staging_host=GATEA-STAGING
execution_euid=0
cwd=/
producer_sha256=<64-lowercase-hex>
trusted_python_path=/usr/bin/python3.<one-or-two-decimal-digits>
trusted_python_sha256=<64-lowercase-hex>
user_ns=user:[<digits>]
mnt_ns=mnt:[<digits>]
pid_ns=pid:[<digits>]
net_ns=net:[<digits>]
root_mount_id=<digits>:<digits>
allocation_parent=/home/gatea
expect_parent_mount_b64=<RFC4648-base64-with-padding>
mountinfo_bytes=<positive-decimal>
mountinfo_sha256=<64-lowercase-hex>
mountinfo_b64=<RFC4648-base64-with-padding>
projection_points=21
projection_roots=6
projection_mount_records=<positive-decimal>
projection_bytes=<positive-decimal>
projection_sha256=<64-lowercase-hex>
projection_b64=<RFC4648-base64-with-padding>
ATTESTATION_V1_PASS
```

The recorder decodes both base64 fields strictly, verifies the declared byte counts and SHA-256 values, requires `mountinfo_b64` to end in exactly the captured LF-terminated record sequence, and independently re-runs the Commit-1 projection algorithm before any value is eligible for Commit 2. A zero-fact PASS is forbidden by the repository’s coverage rule. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:899-929`

### 3.6 Normative producer source

```python
import base64
import hashlib
import os
import re
import stat
import sys

STOP_PREFIX = "ATTESTATION_V1_STOP reason="
FIXED_CANDIDATE = "2ce41e34bceb599d80af24c5c33d835820ec321b"
FIXED_PARENT = "/home/gatea"
FIXED_MAIN_PID = "189813"
SAFE_COMPONENT = re.compile(r"^(?!-)(?!\.$)(?!\.\.$)[A-Za-z0-9._-]+$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class AttestationStop(Exception):
    pass


def stop(reason):
    raise AttestationStop(reason)


def read_all(path, nofollow=False):
    flags = os.O_RDONLY | os.O_CLOEXEC
    if nofollow and hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError:
        stop("read_open_failed")
    chunks = []
    try:
        while True:
            try:
                chunk = os.read(fd, 1024 * 1024)
            except OSError:
                stop("read_failed")
            if not chunk:
                break
            chunks.append(chunk)
    finally:
        os.close(fd)
    return b"".join(chunks)


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def parse_mountinfo(raw):
    if not raw or not raw.endswith(b"\n") or b"\x00" in raw or b"\r" in raw:
        stop("mountinfo_incomplete_or_invalid_bytes")
    rows = []
    seen_ids = set()
    for number, line in enumerate(raw[:-1].split(b"\n"), 1):
        if not line:
            stop("mountinfo_blank_record")
        fields = line.split(b" ")
        if b"" in fields:
            stop("mountinfo_field_grammar")
        try:
            sep = fields.index(b"-", 6)
        except ValueError:
            stop("mountinfo_field_grammar")
        if sep < 6 or len(fields) < sep + 4:
            stop("mountinfo_field_count")
        mount_id, parent_id, device, root, mount_point = fields[:5]
        fstype, source = fields[sep + 1], fields[sep + 2]
        if not mount_id.isdigit() or not parent_id.isdigit() or mount_id in seen_ids:
            stop("mountinfo_id_grammar")
        seen_ids.add(mount_id)
        if not re.fullmatch(rb"[0-9]+:[0-9]+", device):
            stop("mountinfo_device_grammar")
        if not root.startswith(b"/") or not mount_point.startswith(b"/"):
            stop("mountinfo_path_grammar")
        if any(x == b"" or re.search(rb"[\x00-\x20]", x) for x in (fstype, source)):
            stop("mountinfo_post_field_grammar")
        rows.append((device, root, mount_point, fstype, source))
    if not rows:
        stop("mountinfo_no_records")
    return rows


def covers(mount_point, path):
    return mount_point == b"/" or path == mount_point or path.startswith(mount_point + b"/")


def effective_mount(rows, path):
    best_index = -1
    best_length = -1
    for index, row in enumerate(rows):
        mount_point = row[2]
        if covers(mount_point, path) and len(mount_point) >= best_length:
            best_index = index
            best_length = len(mount_point)
    if best_index < 0:
        stop("mount_projection_unbound")
    winner = rows[best_index]
    shared = sum(1 for row in rows if row[2] == winner[2])
    return winner, shared


def build_projection(rows, trusted_python):
    release = b"/opt/mtc-bridge/releases/" + FIXED_CANDIDATE.encode("ascii")
    venv = b"/opt/mtc-bridge/venvs/" + FIXED_CANDIDATE.encode("ascii")
    tools = [
        b"/usr/bin/stat", b"/usr/bin/readlink", b"/usr/bin/env", b"/usr/bin/find",
        b"/usr/bin/sha256sum", b"/usr/bin/systemctl", b"/usr/bin/ss",
        b"/usr/bin/curl", b"/usr/bin/timeout", trusted_python.encode("ascii"),
    ]
    points = tools + [
        release, venv,
        b"/usr/local/lib/systemd/system/mtc-bridge-first-start.service",
        b"/var/lib/mtc-bridge", b"/var/log/mtc-bridge", b"/etc/mtc-bridge",
        release + b"/IBKR_PAPER_BRIDGE/requirements.lock",
        release + b"/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py",
        b"/proc/self/mountinfo", b"/proc/self/ns/net",
        b"/proc/" + FIXED_MAIN_PID.encode("ascii") + b"/ns/net",
    ]
    root_candidates = [release, venv, b"/etc/mtc-bridge", b"/var/lib/mtc-bridge", b"/var/log/mtc-bridge"]
    root_candidates.extend(path.rsplit(b"/", 1)[0] or b"/" for path in tools)
    roots = []
    for root in root_candidates:
        if root not in roots:
            roots.append(root)
    if len(points) != 21 or len(roots) != 6:
        stop("projection_universe_recount")
    output = bytearray()
    for path in points:
        (device, root, mount_point, fstype, source), shared = effective_mount(rows, path)
        output.extend(
            b"kind=point\tpath=" + path + b"\tdevice=" + device + b"\troot=" + root
            + b"\tmount_point=" + mount_point + b"\tfstype=" + fstype
            + b"\tsource=" + source + b"\tshared_mount_point_records="
            + str(shared).encode("ascii") + b"\n"
        )
    for subtree_root in roots:
        count = 0
        for device, root, mount_point, fstype, source in rows:
            if mount_point == subtree_root or mount_point.startswith(subtree_root.rstrip(b"/") + b"/"):
                count += 1
                output.extend(
                    b"kind=subtree\tsubtree_root=" + subtree_root + b"\tseq="
                    + str(count).encode("ascii") + b"\tdevice=" + device + b"\troot=" + root
                    + b"\tmount_point=" + mount_point + b"\tfstype=" + fstype
                    + b"\tsource=" + source + b"\n"
                )
        output.extend(
            b"kind=subtree_count\tsubtree_root=" + subtree_root + b"\trecords="
            + str(count).encode("ascii") + b"\n"
        )
    return bytes(output), len(points), len(roots)


def ns_link(path, kind):
    try:
        value = os.readlink(path)
    except OSError:
        stop("namespace_read_failed")
    if not re.fullmatch(kind + r":\[[0-9]+\]", value):
        stop("namespace_grammar")
    return value


def write_all(fd, value):
    view = memoryview(value)
    while view:
        try:
            count = os.write(fd, view)
        except OSError:
            raise SystemExit(3)
        if count <= 0:
            raise SystemExit(3)
        view = view[count:]


def parse_exact_argv(argv):
    keys = [
        "--record-id", "--candidate", "--allocation-parent",
        "--main-pid", "--producer-sha256",
    ]
    if len(argv) != 10 or argv[0::2] != keys:
        stop("argument_grammar")
    return dict(zip(keys, argv[1::2]))


def main():
    args = parse_exact_argv(sys.argv[1:])
    record_id = args["--record-id"]
    candidate = args["--candidate"]
    allocation_parent = args["--allocation-parent"]
    main_pid = args["--main-pid"]
    producer_sha256 = args["--producer-sha256"]
    if not SAFE_COMPONENT.fullmatch(record_id):
        stop("record_id_grammar")
    if candidate != FIXED_CANDIDATE or allocation_parent != FIXED_PARENT or main_pid != FIXED_MAIN_PID:
        stop("fixed_argument_mismatch")
    if not HEX64.fullmatch(producer_sha256):
        stop("producer_identity_grammar")
    if os.geteuid() != 0:
        stop("execution_euid_not_root")
    os.chdir("/")
    if os.getcwd() != "/":
        stop("cwd_not_fixed")

    try:
        invoked = os.path.realpath("/usr/bin/python3")
        actual = os.readlink("/proc/self/exe")
    except OSError:
        stop("interpreter_resolution_failed")
    if invoked != actual or not re.fullmatch(r"/usr/bin/python3\.[0-9]{1,2}", actual):
        stop("interpreter_identity_mismatch")
    try:
        meta = os.lstat(actual)
    except OSError:
        stop("interpreter_stat_failed")
    if not stat.S_ISREG(meta.st_mode) or meta.st_uid != 0 or meta.st_gid != 0 or meta.st_mode & 0o022:
        stop("interpreter_metadata_mismatch")
    interpreter_bytes = read_all(actual, nofollow=True)

    namespaces = {}
    for kind in ("user", "mnt", "pid", "net"):
        value = ns_link(f"/proc/1/ns/{kind}", kind)
        if ns_link(f"/proc/self/ns/{kind}", kind) != value:
            stop("root_domain_namespace_mismatch")
        namespaces[kind] = value
    try:
        if os.path.realpath(FIXED_PARENT) != FIXED_PARENT:
            stop("allocation_parent_not_literal_canonical")
        root_stat = os.stat("/", follow_symlinks=True)
    except OSError:
        stop("fixed_path_stat_failed")
    root_mount_id = f"{root_stat.st_dev}:{root_stat.st_ino}"

    mountinfo = read_all("/proc/self/mountinfo")
    rows = parse_mountinfo(mountinfo)
    (device, root, mount_point, fstype, source), shared = effective_mount(rows, FIXED_PARENT.encode("ascii"))
    expect_parent = (
        b"device=" + device + b" root=" + root + b" mount_point=" + mount_point
        + b" fstype=" + fstype + b" source=" + source
        + b" shared_mount_point_records=" + str(shared).encode("ascii")
    )
    projection, point_count, root_count = build_projection(rows, actual)

    fields = [
        "ATTESTATION_V1_BEGIN",
        "protocol=normalised_path_projection_v2",
        f"record_id={record_id}",
        f"candidate={FIXED_CANDIDATE}",
        "staging_host=GATEA-STAGING",
        "execution_euid=0",
        "cwd=/",
        f"producer_sha256={producer_sha256}",
        f"trusted_python_path={actual}",
        f"trusted_python_sha256={sha256_bytes(interpreter_bytes)}",
        f"user_ns={namespaces['user']}",
        f"mnt_ns={namespaces['mnt']}",
        f"pid_ns={namespaces['pid']}",
        f"net_ns={namespaces['net']}",
        f"root_mount_id={root_mount_id}",
        f"allocation_parent={FIXED_PARENT}",
        "expect_parent_mount_b64=" + base64.b64encode(expect_parent).decode("ascii"),
        f"mountinfo_bytes={len(mountinfo)}",
        f"mountinfo_sha256={sha256_bytes(mountinfo)}",
        "mountinfo_b64=" + base64.b64encode(mountinfo).decode("ascii"),
        f"projection_points={point_count}",
        f"projection_roots={root_count}",
        f"projection_mount_records={len(rows)}",
        f"projection_bytes={len(projection)}",
        f"projection_sha256={sha256_bytes(projection)}",
        "projection_b64=" + base64.b64encode(projection).decode("ascii"),
        "ATTESTATION_V1_PASS",
    ]
    payload = ("\n".join(fields) + "\n").encode("ascii")
    write_all(1, payload)


try:
    main()
except AttestationStop as exc:
    token = str(exc)
    if not re.fullmatch(r"[a-z0-9_]+", token):
        token = "internal_stop"
    write_all(2, (STOP_PREFIX + token + "\n").encode("ascii"))
    raise SystemExit(3)
except SystemExit:
    raise
except BaseException:
    write_all(2, (STOP_PREFIX + "internal_stop\n").encode("ascii"))
    raise SystemExit(3)
```

## 4. Operator-side route and recorder contract

### 4.1 Exact transport shape already fixed

The later WP-I plan uses one row per operation with fields `op_id`, `kind`, `run_when`, `expect_rc`, `cwd`, `stdin_file`, `stdin_sha256`, `argv`, and `purpose`; its SSH rows pin `-F none`, identity, strict known-host files, batch mode, identity-only mode, timeout, no proxy/control/local-command/forwarding, the address, and a cleared remote environment. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:1-11`

Commit 1 shall use one separate attestation row with that same table shape:

| op_id | kind | run_when | expect_rc | cwd | stdin_file | stdin_sha256 | argv | purpose |
|---|---|---|---:|---|---|---|---|---|
| `ATT-01` | `ssh_stdin_read_only_attestation` | `clean_head_and_manifest_ok` | `0` | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_STAGE1_COMMIT1` | `capture_wpi_attestation.py` | `{{PRODUCER_SHA256}}` | `UNKNOWN OUTER ROOT-CHANNEL PREFIX` + the exact inner argv in §3.2 | capture Commit-1-bound read-only attestation only |

The fixed SSH option prefix, once the root target is authoritatively supplied, is:

```text
ssh -F none -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20 -o UserKnownHostsFile=C:\HyperV\GATEA-STAGING\ssh\wpi_known_hosts -o GlobalKnownHostsFile=C:\HyperV\GATEA-STAGING\ssh\wpi_known_hosts_global -o ProxyCommand=none -o ControlMaster=no -o ControlPath=none -o PermitLocalCommand=no -o ForwardAgent=no -o ForwardX11=no -o ClearAllForwardings=yes {{ROOT_CHANNEL_TARGET}} <§3.2 exact inner argv>
```

`{{ROOT_CHANNEL_TARGET}}` is not an allocation value and must not be filled by L1 unless L1 cites the missing authoritative root-channel source. It remains the blocker in §0.1.

### 4.2 Command-by-command target-write proof

| Command | Runs where | Target-host write capability |
|---|---|---|
| `git diff --quiet --` | operator | None: reads worktree/index; no target contact |
| `git diff --cached --quiet --` | operator | None: reads index/HEAD; no target contact |
| `git ls-files --others --exclude-standard` | operator | None: enumerates untracked paths; no target contact |
| `git rev-parse --verify HEAD^{commit}` and `git rev-parse HEAD:<path>` | operator | None: reads object identities; no target contact |
| `git hash-object --no-filters <path>` | operator | None: computes an object ID without `-w`; no object or target write |
| local SHA-256/byte-count and local record creation | operator | None on target: writes only below `{{OPERATOR_ATTESTATION_ROOT}}` |
| `ssh … ATT-01` | operator plus target channel | The SSH client opens the one approved connection; the remote payload is exactly §3.6 and has only the read/output operations listed in §3.3. Infrastructure logging remains the explicit `UNKNOWN` in §0.1 |

### 4.3 Clean-current-HEAD rule before any socket

Before starting `ssh`, the recorder must, in this order:

1. require empty output/diff from the three cleanliness commands in §4.2;
2. derive `COMMIT_1` using `git rev-parse --verify HEAD^{commit}`;
3. require every manifest member to exist at `COMMIT_1:<path>`;
4. require `git hash-object --no-filters <worktree-path>` to equal `git rev-parse COMMIT_1:<path>`, proving the exact sent/worktree bytes equal the committed blob rather than merely a filtered checkout;
5. verify each declared byte count and SHA-256 against the exact worktree bytes;
6. create the local record at the L1-supplied create-once operator root and make its first line `attestation_prereg_commit=<COMMIT_1>`; and
7. only then open the socket and send the exact producer bytes.

The source contract requires a clean checkout, current-HEAD derivation, proof that HEAD contains the exact procedure and package manifest, and emission of `attestation_prereg_commit=<COMMIT_1>` before socket or root command. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:519-533`

The closed operator record grammar is exact:

```text
attestation_prereg_commit=<40-or-64-lowercase-hex Git object id>
package_manifest_blob=<Git blob oid>
producer_blob=<Git blob oid>
producer_bytes=<positive-decimal>
producer_sha256=<64-lowercase-hex>
record_id=<safe-component>
confirm_token=<L1 exact token>
stdout_bytes=<nonnegative-decimal>
stdout_sha256=<64-lowercase-hex>
stdout_b64=<strict base64>
stderr_bytes=<nonnegative-decimal>
stderr_sha256=<64-lowercase-hex>
stderr_b64=<strict base64>
ssh_rc=<decimal>
record_status=PASS|STOP
```

On rc 0, `record_status=PASS` is permitted only after strict §3.5 validation. Every other outcome is `STOP`; no placeholder is consumable. The final file is then closed, and its byte count and SHA-256 are computed over exactly those bytes for Commit 2. The source requires stdout/stderr/rc to be captured without editing and the complete production record to be hashed. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:528-533`

## 5. Projection-v2 universe and exact algorithm

The projection is an ordered TSV with LF records and three record kinds in fixed order: all `kind=point` rows, all per-root `kind=subtree` rows, then each root’s `kind=subtree_count` row as emitted during that root’s pass. Effective covering mounts use the longest matching mount point and, on equal length, the later mountinfo record; `shared_mount_point_records` counts every record with the winning mount point. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md:450-477`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:1199-1281`

The exact 21 point paths, in order, are:

1. `/usr/bin/stat`
2. `/usr/bin/readlink`
3. `/usr/bin/env`
4. `/usr/bin/find`
5. `/usr/bin/sha256sum`
6. `/usr/bin/systemctl`
7. `/usr/bin/ss`
8. `/usr/bin/curl`
9. `/usr/bin/timeout`
10. the captured exact `WPI_FIXED_TRUSTED_PYTHON` leaf
11. `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b`
12. `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b`
13. `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`
14. `/var/lib/mtc-bridge`
15. `/var/log/mtc-bridge`
16. `/etc/mtc-bridge`
17. `<release>/IBKR_PAPER_BRIDGE/requirements.lock`
18. `<release>/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py`
19. `/proc/self/mountinfo`
20. `/proc/self/ns/net`
21. `/proc/189813/ns/net`

This is the accepted RP7 point array and count. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:1214-1222,1280-1281`

The exact six subtree roots, de-duplicated on first appearance, are release root, venv root, `/etc/mtc-bridge`, `/var/lib/mtc-bridge`, `/var/log/mtc-bridge`, and `/usr/bin`. Every mountinfo record at or below each root is emitted in original mountinfo order, followed by that root’s count row. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:1223-1235,1262-1275`

The raw reader must accept only a nonempty, fully LF-terminated stream, reject NUL/CR, reject blank/malformed/duplicate-ID records, and STOP on any open/read/parse/completeness error before emitting output. The repository’s reader-completion rule distinguishes clean EOF, an unterminated populated record, and a hard read error. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:424-486`

## 6. Commit-1 package manifest

Commit 1 has exactly three package members; hidden or extra members are STOP because package-member conservation must not silently drop or add a member. The repository records hidden extra deliverables as a prior defect and requires force-inclusive enumeration. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:691-702`

| Ordinal | Exact repo-relative path | Role | Identity fill |
|---:|---|---|---|
| 1 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/COMMIT1_ATTESTATION_PREREGISTRATION.md` | finalized version of this preregistration | bytes/SHA-256/Git blob computed from final LF bytes before commit |
| 2 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/capture_wpi_attestation.py` | exact §3.6 producer | `{{PRODUCER_BYTES}}`, `{{PRODUCER_SHA256}}`, `{{PRODUCER_GIT_BLOB_OID}}` from final producer bytes |
| 3 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/COMMIT1_PACKAGE_MANIFEST.tsv` | ordered manifest of members 1–2 plus declared three-member set/count | its Git blob is derived after Commit 1 and recorded by the clean-HEAD recorder; it does not self-embed its own digest |

Manifest TSV columns are exactly `ordinal`, `path`, `bytes`, `sha256`, `git_blob_oid`, `role`, with one header and two payload rows in ordinal order. A separate footer line is exactly `package_members_including_manifest=3`. Duplicate path, duplicate ordinal, missing member, extra member, hash/byte/blob mismatch, wrong order, or count other than three is pre-socket STOP.

The manifest does not embed its own digest, avoiding a self-reference. After Commit 1, the recorder derives and emits the manifest blob OID from clean current HEAD. Neither commit may embed its own commit ID; the recorder binds it after the commit exists. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:575-579`

## 7. Post-capture non-consumption and Commit-2 handoff

After ATT-01 returns, the recorder closes and hashes the operator record. No WP-I operation runs. A separate local derivation must strictly decode and verify the record, independently rebuild projection v2 from the captured mountinfo bytes, and compare every derived field before Commit 2 is prepared. A read, parse, projection, status, completeness, or digest error is STOP and no Commit 2 is produced. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:550-573`

Commit 1 is never amended. If the producer, projection algorithm, universe, output grammar, root route, or package manifest changes, the capture is discarded for acceptance, a new Commit 1 is created, and capture repeats under that new commit. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:571-573`

The later order proof must establish strict Commit-1 ancestry of Commit 2, evidence byte/digest equality, absence of derived values in Commit 1, presence of all derived values in Commit 2, byte identity of the capture procedure/algorithm/universe/producer across both commits, and clean Commit-2 HEAD before op 01. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:581-607`

## 8. Placeholder and dependency conservation

| Class | Count | Terminal disposition |
|---|---:|---|
| L1 allocation dependencies | 6 token families | Every token has one named L1 field source in §1; none may remain in Commit 1 |
| Host observations | 10 fields | Every field remains exactly `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` in Commit 1 and has one successful-output source in §2 |
| Local build identities | 3 producer byte-hash-blob fields plus preregistration byte-hash-blob fields in the manifest | Filled from finalized local bytes before Commit 1; never from host output |
| Root-channel route | 1 | `UNKNOWN`; blocks final outer argv and Commit 1 until an authoritative source settles it |
| SSH infrastructure side effects | 1 | `UNKNOWN`; blocks an absolute whole-host “no mutation whatsoever” claim until settled |

The permanent conservation rule is that every admitted member must reach exactly one terminal disposition, with no overwrite, implicit filter, or unexplained count change. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`

## 9. Self-verification record

- Exactly one lane output is intended: this file outside the repository. No repository write, Git index operation, host/network contact, SSH, service action, credential use, deployment, broker/exchange contact, ARM/order action, TESTNET/mainnet action, Pine/parity/MTC/trading change, merge, push, or economic action is performed by this draft.
- The producer has one stdout success grammar and one stderr STOP grammar; all observations precede the first stdout byte.
- Projection conservation is fixed at 21 points and 6 roots, with later-record-wins ties and per-root count records.
- Every target-side operation in the producer has a no-write explanation in §3.3.
- This draft does **not** claim Commit-1 readiness: the exact root-channel target/launch, infrastructure-side-effect boundary, L1 values, and final package identities remain explicitly unresolved.
- `NO SOURCED ESTIMATE`: this lane makes no new hour estimate.

This self-verification is not an acceptance decision, gate verdict, authorization, or evidence that any command executed.
