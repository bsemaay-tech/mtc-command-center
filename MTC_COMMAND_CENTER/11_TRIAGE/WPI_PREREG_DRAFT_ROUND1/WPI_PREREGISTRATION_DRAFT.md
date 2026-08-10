# WP-I staging verification - preregistration DRAFT (round 1.4)

Status: **DRAFT - NOT A PREREGISTRATION, NOT DISPATCHABLE, NO HOST CONTACT HAS OCCURRED**

Unit: `<ALLOCATE-AT-DISPATCH>` - branch `feature/donchian-crypto-ladder`
Frozen candidate: `2ce41e34bceb599d80af24c5c33d835820ec321b`
Check universe: `GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md`
Groups A3, B (B1, B1a, B2, B3, B4, B5, B6), C (C1-C5).
Rigor template: `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/PREREGISTRATION.md`.
Governing lesson: `.../03_TRANSPORT/B3_STOP_ADJUDICATION.md` (design gap `B3-GAP-ENV`).
Banked-evidence check: `.../EVIDENCE_INDEX.md`.

This document is the *shape* of the WP-I preregistration, not the preregistration
itself. A preregistration mints one-use identifiers; a draft must not, so every
identifier here is a marked placeholder. Writing this document authorizes nothing:
not transport, not host contact, not a socket, not a RUNID. Section 12 states
exactly what has and has not happened.

**Round 1.3 (Codex audit F3 and F4 applied).** Round 1.2 closed F1, F2, F5 and F6.
This round closes the two findings it left open: F3 (B2/B4 system-manager access)
and F4 (B3 partial-walk output). They share the existing `B3-GAP-ENV` rule: an
inability-to-evaluate must STOP (rc 3), never FAIL (rc 1). A manager query is not a
unit-state observation until invocation, bus, namespace, authorization and parsing
have succeeded. A filesystem sweep is not a finding until its timeout, exit status
and complete diagnostics prove the walk finished successfully. F3 and F4 are now
closed; `SELF_QA.md` records the exact changes and supersedes the round-1.2 open list.

**Round 1.4 (retroactive ten-pattern catalogue pass).** The whole draft - every
preflight, expectation row, evidence block and deferred root-side rule - has been
checked against `DESIGN_DEFECT_PATTERNS_2026-08-10.md`. This pass strengthens domain
binding, numeric identity, path-object binding, structured parsing, result
classification, status-before-output ordering, line-reader completeness and
falsifiable acceptance evidence. It authorizes no host contact or new operation and
does not fill or alter any existing PIN-BEFORE-DISPATCH placeholder.

**Round 1.5 (transport-set contract repair — Lead adjudication of a Codex authoring
STOP, 2026-08-10).** Authoring the transport set falsified the round-1.1 N1 claim that
all three reused remote scripts fit the WP-I contract unchanged. Two do not:
`remote_setup.sh` (4976 B, `faee3725…`) hardcodes the base prefix
`/home/gatea/wpl_p2_staging_` and therefore cannot allocate the section-1
`wpi_staging_` base (op 01 would always fail); `remote_extract_verify.sh` (8270 B,
`ba0bef0e…`) pins the old nine-member 102400-byte archive **including `RP1-B3.sh`**,
which section 3 excludes from the WP-I kit (op 03 would reject every valid WP-I
archive). The implementer stopped without writing rather than author deliverables
that could never run — the correct STOP. Section 4 is amended accordingly:
WP-I-specific `remote_setup_wpi.sh` and `remote_extract_verify_wpi.sh` replace the
two misfit rows as minimal derivations of the accepted bytes, and only
`remote_close_tree.sh` (verified free of unit-specific constants) remains byte-reuse.

Three things must happen before any successor of this document is dispatchable, and
each is named at the point where it bites: Stage 1 must freeze and hash the blocks
(sections 3 and 4), the values marked `<PIN-BEFORE-DISPATCH: ...>` must be filled
from the cited record (sections 2 and 8), and the identifiers must be allocated and
tested against `rp0_require_safe_component` (section 1).

**These three are necessary but not sufficient (Codex audit F6, applied round 1.2).**
Two further gates are required and are currently unmet (section 12, and matrix
section 1): (a) **explicit written host-contact/transport authority** - a named
authorisation for SSH/SCP contact with `GATEA-STAGING` and for the operator-side
external probe (op 06); and (b) **the required budget lift** - the matrix records the
exact 50-hour balance as NOT REPRODUCIBLE, so no host execution may be authorised or
performed until a budget lift is granted. The `-Execute` and `-Confirm` switches in
section 6 are technical interlocks on the runner, not authority: flipping both
executes the plan the runner holds, it does not grant the authority or the budget the
plan still lacks. No successor is dispatchable while either (a) or (b) is absent.

---

## 0. Design gate: unprivileged feasibility

Tonight's B3 stage stopped with rc 3 at
`RP0_STOP reason=path_probe_error path=/etc/mtc-bridge/mtc-bridge.env rc=1
detail=stat: cannot statx ...: Permission denied`, because an adversarially
accepted block assumed the operator could `stat` a name inside a `0750 root:root`
directory as the unprivileged login user. The design and the execution model
contradicted each other, and the contradiction was only discovered on the host,
after a one-use RUNID had been spent.

This draft therefore treats unprivileged feasibility as an admission gate on the
*design*, ahead of expectations, argv, or evidence contract. Three rules follow,
and they govern every later section:

1. **Every check admitted to the run plan carries a written reason why it works as
   `gatea` without sudo.** The reason must be a permission-semantics argument over a
   recorded mode and owner, not an assumption of convenience. The full ledger with
   one row per Group A3/B/C check is `WPI_CHECK_FEASIBILITY.tsv`; the reasoning and
   its residual gaps are in `SELF_QA.md`.
2. **Anything that needs privilege goes to DEFER-ROOT-SIDE under the RPD-VERIFY
   pattern (section 10), never into the run plan** - not as a "best effort" probe,
   not as an optional corroboration, not behind a conditional. A block that contains
   an unreachable path will reach it.
3. **`sudo` is not used, and is not probed.** No `sudo -n`, no capability test, no
   fallback. On a host under a zero-mutation authority, testing for privilege is
   itself outside the envelope, and a block that can escalate on some future host is
   a block whose scope is not what this document describes.

The mechanical form of rule 2 is the **path-scope proof** (section 10.2): Stage 1
must emit the sorted closed set of absolute host paths reachable after expansion in
each frozen block, reject unresolved dynamic construction, and show every result
inside the section 10.1 allowlist. The distinction
that proof enforces is exactly the one B3 missed - `/etc/mtc-bridge` as a terminal
`stat` target is feasible; `/etc/mtc-bridge/` as a path prefix is not.

---

## 1. Run identifiers and evidence tree

Two stages run, each with its own **one-use** RUNID. A RUNID is never reused: if
allocation fails for any reason it is **burned**, and a retry requires a new
preregistration, not a second attempt with the same identifier. RUNID
`WPLP2-20260809T125940Z-8dc78f08-B3` is already burned this way.

| Field | P0 preflight stage | RO check stage |
|---|---|---|
| `RUNID` | `<ALLOCATE-AT-DISPATCH>-P0` | `<ALLOCATE-AT-DISPATCH>-RO` |
| `EV_STAGE_ID` | `p0` | `ro` |
| `EV_DIR` | `<EV_RUNKIT>/<ALLOCATE-AT-DISPATCH>-P0` | `<EV_RUNKIT>/<ALLOCATE-AT-DISPATCH>-RO` |
| `EV_LOG` | `<EV_DIR>/p0.log` | `<EV_DIR>/ro.log` |

Shared, to be preregistered at dispatch:

| Field | Value | Expected owner | Expected mode |
|---|---|---|---|
| `REMOTE_BASE` | `/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>` | P0-resolved numeric euid:egid for the named `gatea` login (`gatea:gatea` diagnostic only) | `0700` |
| `EV_PARENT` | `<REMOTE_BASE>/evidence` | same numeric euid:egid | `0700` |
| `EV_RUNKIT` | `<REMOTE_BASE>/evidence/runkit` | same numeric euid:egid | `0700` |
| `REMOTE_KIT` | `<REMOTE_BASE>/kit` | same numeric euid:egid | `0700` |
| remote archive | `<REMOTE_BASE>/kit/runkit.tar` | - | - |
| `EXTRACT_DIR` | `<REMOTE_BASE>/kit/extracted` | - | `0700`, files `0444` |

Allocation rules, binding on the successor document:

- No identifier in this table may be made concrete here. A draft that mints a RUNID
  has spent it, and a spent identifier cannot be preregistered.
- Every allocated component must be tested against the **accepted** predicate
  `rp0_require_safe_component` from `RP0-LIB.sh` and must be accepted (rc 0), with
  the same refusal set demonstrated (`../escaped`, `a/b`, `.`, `..`, `-lead`, empty,
  `bad name` -> rc 1). Assertion is not demonstration; the transcript goes in the
  successor's self-QA.
- `REMOTE_BASE` and the operator record root are **create-once**. Before allocation,
  both must be shown not to collide with any existing tree - on the host under
  `/home/gatea/`, and operator-side against the two recorded roots
  `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08` and the same
  path suffixed `-R45B` (`EVIDENCE_INDEX.md`, RUNID ledger).

Two stages rather than one is deliberate. P0 establishes the executing identity and
tool inventory that every feasibility claim in section 0 rests on; the RO stage is
admissible only if P0 confirmed those premises. Folding them together would let the
run assert a result whose precondition it never checked - the B3 failure mode with a
different path in it.

## 2. Preregistered inputs consumed by the accepted blocks

| Variable | Value | Origin |
|---|---|---|
| `WPI_CANDIDATE_SHA` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | frozen candidate; immutable (matrix A1) |
| `WPI_RELEASE_ROOT` | `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` | matrix B1, B1a; transition inventory |
| `WPI_VENV_ROOT` | `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b` | matrix B1 |
| `WPI_UNIT_FRAGMENT` | `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` | matrix B2 |
| `WPI_UNIT_FRAGMENT_BYTES` | `3736` | transition inventory, via matrix B2 and template section 8 |
| `WPI_UNIT_FRAGMENT_SHA256` | `<PIN-BEFORE-DISPATCH: GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md; matrix B2 records it elided as 538c1c60...279bd>` | see section 8 risk R1 |
| `WPI_EXPECTED_LOCK_SHA256` | `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` | matrix A3 / B1a, round-2 and round-3 blocks; LF blob content, 117762 B |
| `WPI_EXPECTED_LOCK_BYTES` | `117762` | same |
| `WPI_EXPECTED_PACKAGES` | `56` | matrix A3 / A6, re-derived at the candidate twice |
| `WPI_STATE_DIR` | `/var/lib/mtc-bridge` | matrix C3 (`/var/lib/mtc-bridge/bridge.db`), C4 |
| `WPI_STATE_UID` | `999` | recorded host `getent passwd mtc-bridge` preflight; numeric identity of the dynamically allocated `mtc-bridge` account for this frozen host state |
| `WPI_STATE_GID` | `988` | primary gid from the same recorded `getent` preflight; uid and gid are deliberately not assumed equal |
| `WPI_LOG_DIR` | `/var/log/mtc-bridge` | `LEAD_PIN_RESOLUTION_2026-08-10.md`, unit-template `ReadWritePaths` at the candidate SHA |
| `WPI_CONF_DIR` | `/etc/mtc-bridge` | matrix B3; adjudication (numeric `0:0`, `0750`; `root:root` diagnostic only) |
| `WPI_CONTROL_ENDPOINT` | `http://127.0.0.1:8790/api/status` | matrix B5, B6 |
| `WPI_SWEEP_BUDGET_S` | `120` | per-tree budget for the `find ... -perm /222` sweep, carried over unchanged from the accepted Stage 2 rationale: `-quit` only shortens a *failing* sweep, so a clean walk is a full walk, and exceeding the budget is STOP, never a pass |

`WPI_EXPECTED_LOCK_SHA256` is the **expected** value, source-derived
(`git cat-file blob 47f53fa2... | sha256sum`). It has never been observed on the
host (matrix round-3 block; B1a "Existing evidence: NONE"). It is therefore a
predicate to be tested, not a fact to be restated, and its failure disposition in
section 8 is *investigate read-only*, not an automatic drift STOP. The Windows
CRLF worktree value `40873556...` (119274 B) is withdrawn and must never be cited.

`WPI_UNIT_FRAGMENT_SHA256` is **never** derived at run time and never re-pinned from
what the host reports. A digest a run reads from the object it is attesting is not
an attestation. Until it is filled from the transition inventory, this draft has no
successor that can be dispatched.

## 3. Expected SHA-256 of every proposed block the stages carry

Blocks marked `<PIN-AT-STAGE-1>` do not yet exist. The WP-I run kit has not been
built; naming a hash for an unwritten file would be the same error class as minting
a RUNID in a draft. The three reused blocks are already frozen and accepted, and
their digests are pinned here from `EVIDENCE_INDEX.md` (01_RUNKIT):

| Block | File | Bytes | SHA-256 | Carried by |
|---|---|---:|---|---|
| RP0-LIB | `RP0-LIB.sh` | 18968 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | P0, RO |
| RP0-BOOTSTRAP | `RP0-BOOTSTRAP.sh` | 1937 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` | P0, RO |
| RP6-P0 (new) | `RP6-P0.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | P0 |
| RP7-WPI-RO (new) | `RP7-WPI-RO.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | RO |

Archive: `runkit.tar`, `<PIN-AT-STAGE-1>` bytes, `<PIN-AT-STAGE-1>`.

Reuse is byte reuse: Stage 1 must verify `RP0-LIB.sh` and `RP0-BOOTSTRAP.sh` against
the two digests above before admitting them, and the remote extract step re-verifies
every member again from constants before anything is sourced.

**`RP1-B3.sh` (`f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af`) does
not travel in the WP-I kit.** Its accepted bytes contain the `/etc/mtc-bridge/`
probes that produced `B3-GAP-ENV`. Shipping it "but not executing it" is how a
frozen block gets executed: the Stage 2 archive carried five never-executed blocks
precisely because the archive was already frozen, and that concession must not be
extended to a block now known to be infeasible under this execution model. The
scoped replacement is `RP7-WPI-RO.sh`, and it is a new block requiring its own
adversarial acceptance, not an edit of an accepted one.

## 4. Support-script hashes (every executed artifact)

Everything the operator sends is pinned. Four scripts are reused from the accepted
Stage 2 set at their recorded digests (`EVIDENCE_INDEX.md`, 02_PREREG); the rest are
authored for WP-I and pinned at Stage 1.

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `remote_setup_wpi.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | op 01 stdin - create-once remote allocation. Derivation of the accepted `remote_setup.sh` (4976 B, `faee3725…`) whose permitted semantic changes are EXACTLY, and only, the four classes enumerated in the round-2 derivation contract below; the derivation diff is recorded in self-QA and must show nothing outside those four classes |
| `remote_extract_verify_wpi.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | op 03 stdin - archive/member/hash verification + extraction. Derivation of the accepted `remote_extract_verify.sh` (8270 B, `ba0bef0e…`) whose permitted semantic changes are EXACTLY, and only, the four classes enumerated in the round-2 derivation contract below. No member-count literal may exist: every count is derived from the `MEMBERS` constant, so the archive-constants block remains the single source of the member set |
| `remote_close_tree.sh` | 7470 | `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e` | ops 07 and 08 stdin - closed-tree hashing. Byte-identical reuse; verified free of unit-specific constants (round 1.5). It is NOT copied into the WP-I draft directory: the plan names it with the `ACCEPTED` root token and the runner resolves that token to the frozen Stage-2 `02_PREREG` directory, so the bytes that travel are the accepted bytes at the digest above and nowhere else |
| `transport_runner.ps1` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | operator-side recorder (Stage 2 variants exist at 18095/`c5bdb47c...` and 17849/`a48ddc93...`; the WP-I op list differs, so the runner is re-pinned, not assumed) |
| `run_p0.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | op 04 stdin - P0 wrapper |
| `run_ro.sh` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | op 05 stdin - RO wrapper |
| `TRANSPORT_PLAN.tsv` | `<PIN-AT-STAGE-1>` | `<PIN-AT-STAGE-1>` | the ordered op list; pinned inside the runner |

Reused-script disposition (round 1.5, superseding the round-1.1 N1 claim): only
`remote_close_tree.sh` is kept byte-identical to the Stage-2-accepted artifact at the
digest above. The N1 "contract fit, unchanged contract, no edit" claim was falsified
for the other two at transport-set authoring (Codex STOP, 2026-08-10): both carry
unit-specific constants incompatible with WP-I (see the round-1.5 note, section 0).
`remote_setup_wpi.sh` and `remote_extract_verify_wpi.sh` are their bounded
derivations; each derivation must be proven bounded by a recorded diff against the
accepted bytes in self-QA, and each is a new artifact requiring Stage 1 adversarial
acceptance and its own pinned digest. Any byte change to `remote_close_tree.sh`
still voids this section and re-opens review.

**Round-2 derivation contract (amended 2026-08-10; Codex transport audit F3/F4/F6/F7,
Claude transport audit F5).** Round 1 permitted only a constants change. Two required
findings from the round-1 T0 audits cannot be satisfied inside a constants block —
`remote_setup_wpi.sh` classified an ambiguous path diagnostic as absence and mutated
through an unbound parent, and `remote_extract_verify_wpi.sh` consumed listing stdout
before adjudicating status, diagnostics and record completion — and a third, the
execution-environment rule below, is by construction executable. The permitted
semantic changes for both derived scripts are therefore EXACTLY these four classes,
and any delta outside them is still a finding:

1. **Pinned archive/allocation constants** — the round-1 permission, unchanged: the
   base-prefix constant for the setup script; the archive-constants block (bytes,
   member list, per-member digests) for the extractor, plus the preregistered numeric
   `EXPECT_UID`/`EXPECT_GID` the setup script compares against.
2. **Program identity** — every executable either script invokes is resolved by a
   frozen absolute path under the preregistered `/usr/bin/<tool>` set and admitted
   only after a non-following kind check, numeric `0:0` ownership, and a
   not-group/other-writable mode. The inherited `PATH` selects nothing, and no
   `mktemp`/`TMPDIR` object is created at all.
3. **STOP-before-mutation path classification** — the full parent chain is bound
   (non-symlink, canonical, searchable, numerically owned, not group/other writable)
   before the first `mkdir`; identity is compared numerically with the rendered
   `%U:%G` name kept diagnostic only; and a path probe is classified `absent` only
   when the probe failed, the kernel reports neither object nor link, and the
   diagnostic equals — as a whole string — the template calibrated in the same run
   from the pinned tool itself. Multiline, mixed or unrecognised diagnostics STOP.
4. **Status-before-stdout adjudication** — every listing and tree walk has its exit
   status, its complete diagnostic stream and its final-record termination adjudicated
   before one byte of its stdout is parsed, and the archive is re-hashed after the
   listings so a listing cannot describe different bytes from the ones hashed.

Class 2 is not optional for either script: it is the same execution-environment rule
the operator side obeys. `transport_runner.ps1` starts `ssh` and `scp` only from
frozen absolute paths whose SHA-256, reparse state and full-chain write ACL (compared
by numeric SID, never a rendered account name) are adjudicated first; it never
consults `Get-Command` or the inherited `PATH`; and every child receives a
deliberately constructed environment with a run-owned `TEMP` rather than the
operator's. Both wrappers resolve `sha256sum` the same way.

The frozen `runkit.tar` and the plan/runner live in **distinct** pinned directories —
the kit in `01_RUNKIT` per section 5's op-02 working directory, the plan and runner in
the preregistration directory — so an archive of the same name placed beside the
runner cannot be selected.

Both wrappers inherit the two repairs the Stage 2 wrappers needed: block paths are
refused if they are symlinks (`-f` dereferences, so `-f` alone is not a refusal),
and any child process reads from `/dev/null`, because the wrapper itself arrives on
ssh stdin and a child that read stdin would consume the rest of the script.

Stage 1 adversarial acceptance of `RP6-P0.sh`, `RP7-WPI-RO.sh` and both wrappers must
also demonstrate the round-1.3 STOP-first contract before any bytes are frozen:

- missing `systemctl`, denied D-Bus/polkit access, or an unavailable manager namespace
  produces P0/B2/B4 STOP and cannot reach a unit-state or property comparison; and
- a `find ... -perm /222` fixture that emits a writable pathname and then encounters
  an LSM, ACL, mount or traversal error produces `B3_STOP`, never `B3_FAIL`.

The accepted implementation must capture stdout, stderr, rc and elapsed time for
each probe, adjudicate timeout/rc/the complete diagnostic stream first, and expose
stdout to result comparison only after that gate holds. An assertion of this order
without the adversarial transcript is not block acceptance. Each regression transcript
offered as closure evidence must record the exact executable command and real output
for both RED against the pre-fix behaviour (or an equivalent deliberate mutation) and
GREEN with the accepted bytes. A prose recipe, substituted template, count, or command
that needs undeclared shell state is supplemental only and cannot freeze a block.

Before `RP6-P0.sh` is frozen, a root-authorised deploy channel outside the ssh login
domain must attest the staging guest's user, mount, PID and network namespace identities
and the canonical root-mount identity plus accepted mount topology for every
preregistered host path. The mount-topology attestation is the SHA-256 of
`normalised_path_projection_v2`, an ordered TSV (TAB-separated fields, LF records)
carrying three record kinds in this fixed order:

1. `kind=point / path=<p> / device=<major:minor> / root=<r> / mount_point=<m> /
   fstype=<f> / source=<s> / shared_mount_point_records=<n>` - one per preregistered
   point path, in the order: the nine tool pins, `WPI_RELEASE_ROOT`, `WPI_VENV_ROOT`,
   `WPI_UNIT_FRAGMENT`, `WPI_STATE_DIR`, `WPI_LOG_DIR`, `WPI_CONF_DIR`,
   `<release>/IBKR_PAPER_BRIDGE/requirements.lock`,
   `<release>/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py`, `/proc/self/mountinfo`,
   `/proc/self/ns/net`, `/proc/<MainPID>/ns/net` - twenty records. The projected mount
   is the **effective** one: the longest matching mount point, and among equally long
   matches the **last** record in `mountinfo` order, because a later record at the same
   mount point shadows the earlier one. `shared_mount_point_records` is the number of
   records sharing the winning mount point, so a stacked mount is visible in the
   projection rather than silently collapsed.
2. `kind=subtree / subtree_root=<R> / seq=<i> / device=… / root=… / mount_point=… /
   fstype=… / source=…` - every `mountinfo` record whose mount point is at or below a
   preregistered root, in `mountinfo` order, for each root in the fixed order
   `WPI_RELEASE_ROOT`, `WPI_VENV_ROOT`, `WPI_CONF_DIR`, `WPI_STATE_DIR`, `WPI_LOG_DIR`,
   then each tool's directory, de-duplicated on first appearance (six roots under the
   pinned `/usr/bin/<tool>` set).
3. `kind=subtree_count / subtree_root=<R> / records=<n>` - one per root, in the same
   root order.

The subtree closure is load-bearing, not decoration: the objects the RO stage digests,
executes and enumerates - `requirements.lock`, `verify_lock.py`, `<venv>/bin/python`,
`<venv>/lib/python3.12/site-packages` and every `*.dist-info` member - lie *below* the
preregistered roots, where a point-only projection cannot observe a bind or overlay
mount because the roots' own covering mounts are unchanged. The superseded
`normalised_path_projection_v1` projected eighteen point paths only, resolved ties to
the *first* matching record, and was therefore blind to both a decoy mount inside a
trusted subtree and a mount stacked on an existing mount point - the exact
substitutions this binding exists to prevent. The deploy channel must attest the
complete v2 record set; a per-path covering-mount list is not sufficient.

The run captures `/proc/self/mountinfo` once into a create-once evidence leaf,
parses and hashes that same leaf, derives exactly this projection, and compares
its digest with the literal embedded at freeze. The exact attested values and their producing
record are embedded in the frozen P0 block; they are never learned or re-pinned from
the login session being tested. If that external attestation is unavailable, P0 STOPs
and no RO row runs. Equality with a PID visible from inside the login session, including
visible PID 1, is not a substitute for deploy-channel attestation.

The complete set, including the successor of this document, is checksummed in
`WPI_PREREG_SHA256SUMS.txt` at dispatch.

## 5. Exact remote argv

Route (recorded): `gatea@172.24.55.233`, identity
`C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`. Options are pinned fail-closed on every
op, unchanged from the accepted Stage 2 set:

```
-i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519
-o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20
```

`BatchMode=yes` refuses to prompt rather than hang. `StrictHostKeyChecking=yes`
refuses an unknown or changed host key rather than trusting it: a changed key means
the host identity is not the one this document describes, and silently accepting it
would defeat the preregistration. `IdentitiesOnly=yes` stops any agent key being
substituted for the named identity.

Every argv element must be free of spaces and shell metacharacters, so the remote
login shell's re-parse of the command is a no-op. Scripts are delivered **on ssh
stdin** to `bash -s --`; no script is written to the host before it runs.

| op | run_when | kind | remote/local argv after the pinned options |
|---|---|---|---|
| 01 | sequence_ok | ssh stdin `remote_setup_wpi.sh` | `gatea@172.24.55.233 bash -s -- <REMOTE_BASE>` |
| 02 | sequence_ok | scp up | `runkit.tar gatea@172.24.55.233:<REMOTE_BASE>/kit/runkit.tar` (cwd `01_RUNKIT`, a pinned directory distinct from the preregistration directory) |
| 03 | sequence_ok | ssh stdin `remote_extract_verify_wpi.sh` | `gatea@172.24.55.233 bash -s -- <REMOTE_BASE>/kit/runkit.tar <REMOTE_BASE>/kit/extracted <PIN-AT-STAGE-1 archive sha256>` |
| 04 | sequence_ok | ssh stdin `run_p0.sh` | `gatea@172.24.55.233 bash -s --` |
| 05 | sequence_ok | ssh stdin `run_ro.sh` | `gatea@172.24.55.233 bash -s --` |
| 06 | sequence_ok | operator-side probe, **host contact** | single TCP connect attempt to `172.24.55.233:8790`, no payload sent, no ssh (B6 external half) |
| 07 | **always** | ssh stdin `remote_close_tree.sh` | `gatea@172.24.55.233 bash -s -- <EV_DIR P0> <RUNID P0>` |
| 08 | **always** | ssh stdin `remote_close_tree.sh` | `gatea@172.24.55.233 bash -s -- <EV_DIR RO> <RUNID RO>` |
| 09 | **always** | scp down | `-r gatea@172.24.55.233:<EV_DIR P0> .` (cwd `<record>\evidence`) |
| 10 | **always** | scp down | `-r gatea@172.24.55.233:<EV_DIR RO> .` (cwd `<record>\evidence`) |
| 11 | **always** | local only | `local_bind 07 09 evidence\<RUNID P0>` - no host contact |
| 12 | **always** | local only | `local_bind 08 10 evidence\<RUNID RO>` - no host contact |

Every op preregisters `expect_rc = 0`. On the first rc that differs, **first-FAIL
stopping engages**: remaining `sequence_ok` ops are skipped, and only the `always`
ops still run - because a failed stage is exactly when its evidence must be closed,
bound and retrieved. The successor must demonstrate this behaviour with exact
paste-and-run commands and real output: RED against a deliberate mutation that wrongly
runs a later `sequence_ok` op, then GREEN with the accepted runner while all `always`
ops still execute. A narrated plan or reconciled op count cannot satisfy this gate.

Op 06 is the one op that touches the host without ssh. It is called out here and in
section 12 rather than buried, because "no host contact" is a claim the record has
to be able to make precisely: op 06 opens one TCP connection attempt toward a port
that is expected to be closed, sends nothing, and is recorded operator-side. Its
evidence is bound by the operator-side digest set, not by `CLOSE_DIGEST_SET_SHA256`,
because nothing about it is written on the host.

The scp local paths are bare filenames with the working directory set, so no
argument ever contains a drive-letter colon that `scp` could parse as a host.

## 6. Operator-side transport evidence

`transport_runner.ps1` records, per op, from the first byte and independently of
anything the remote side writes:

- `ops/<id>.argv` - the exact argv sent, one element per line;
- `ops/<id>.stdout`, `ops/<id>.stderr` - complete, separately captured;
- the exit status, compared against the preregistered `expect_rc`;
- `TRANSPORT_RECORD.txt` - the full narration including every digest;
- `TRANSPORT_SHA256SUMS.txt` - sha256 of every captured file.

Record root, **create-once**:
`C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>`. If it already exists the
runner stops before any process starts; a rerun therefore needs a new
preregistration rather than a silent overwrite. The path must be shown at allocation
not to collide with the two recorded Stage 2/3B roots (section 1).

This matters because `RP0-BOOTSTRAP` calls `exec > "$EV_LOG" 2>&1`: after the
evidence leaf opens, remote output stops reaching ssh stdout. **Every failure before
that point is visible only in the operator-side record** - and those are precisely
the failures that decide whether a RUNID is burned. Tonight's B3 STOP is the worked
example: the STOP line reached the log because the leaf was already open, but the
`stat` rc that caused it is only interpretable against the operator-side record of
what was sent.

Default mode is a dry run. Execution requires **both** `-Execute` and
`-Confirm <ALLOCATE-AT-DISPATCH>-EXECUTE`; anything else prints the plan and opens
nothing. Both switches are **technical interlocks on the runner, not authority**
(Codex audit F6, applied round 1.2): they gate *whether the recorded plan executes*,
not *whether it is authorised*. They are not a substitute for the written
host-contact/transport authority and budget lift named in the dispatch gates above; a
runner with both switches set still opens nothing the plan is not authorised and
budgeted to do.

## 7. Closing and binding the evidence tree

A process never hashes its own still-open evidence. Ops 07 and 08 run
`remote_close_tree.sh` as **separate ssh invocations after the stage connection has
already returned** - that is the structural guarantee the stage shell has exited.
Because a structural guarantee is not a measurement, the script also computes the
digest set **twice** and refuses if the two passes differ, so a tree that is still
being written is never bound as closed. Each pass is independently complete only
after its enumeration and hashing commands have exited 0 with empty diagnostics and
every emitted record has parsed; partial records or a pathname emitted before a later
read/hash error are discarded and STOP the close. Equality of two partial stdout
streams is not closure evidence.

It writes nothing into the evidence tree (writing a digest file into the directory
being hashed would change the bytes being attested) and emits, on stdout only:

- `CLOSE_DIGEST <sha256>  <path relative to EV_DIR>` per file, `LC_ALL=C` order;
- `CLOSE_SIZE <relpath> <bytes>` per file;
- `CLOSE_DIGEST_SET_SHA256 <runid> <sha256 of the digest set itself>`.

Ops 11 and 12 then perform the **local half of the binding**: local per-file digests
over the retrieved tree must equal the remote set name-for-name and
digest-for-digest, and the reconstructed digest-set rendering must reproduce
`CLOSE_DIGEST_SET_SHA256`. The local enumerator/hash/parser statuses and complete
diagnostics are adjudicated before comparison under the same rule. A remote-only or
local-only hash is not a binding.

## 8. Preregistered expectations and predicted first divergence

Preregistering the expected outcome is what stops a result being re-narrated
afterwards. The **recorded** host state (transition inventory, read-only, as carried
into the matrix section 0.3 and B1/B2/B3/B6) is: only release `2ce41e34...321b`
installed at mode `555`; venv counterpart `555`; `/etc/mtc-bridge` metadata only,
`install_manifest.json` 1007 B mode `640`; unit fragment 3736 B mode `644`;
first-start unit active with `Restart=no`, `NRestarts=0`, MainPID 189813; exactly one
bridge listener on `127.0.0.1:8790` (sshd:22 is necessarily also listening - see named
risk R5, wording per GLM review N2); credential-free DISARMED `state_version=1` with
all credential/network/exchange/ARM flags off.

Outcome grammar, unchanged from the accepted Stage 2 contract: **rc 0 = PASS**,
**rc 1 = FAIL** (a probe that ran observed deviant host state), **rc 3 = STOP** (a
probe could not be evaluated). A STOP is never re-read as a PASS, and a STOP never
becomes a FAIL by inference - tonight's adjudication turned on exactly that
distinction, because permission denial precedes the existence question and the
env-file naming risk remains *unresolved*, not *triggered*.

### 8.1 P0 preflight - the premises every later row depends on

| # | check | predicted outcome if it holds | exact predicted first divergence if it does not |
|---|---|---|---|
| 1 | `getent` present | `command -v getent` resolves and the resolved executable can run | `P0_STOP reason=missing_tool tool=getent` for absence, or `P0_STOP reason=tool_not_evaluable tool=getent path=<p> rc=<n|na> detail=<d> mechanism=<m>` when the resolved object cannot be evaluated as executable. **`rc=na` is mandatory for the `mechanism=access_builtin_x` arm and `rc=<n>` is reserved for an arm that actually invoked something** (amended round 3, RP6-P0 re-audit R2 finding 1): P0 decides resolution and executability with shell builtins only — `command -v` and the access(2) predicate `[ -x ]` — and deliberately never invokes an inventory tool, so no P0 arm can carry an honest invocation status, and a numeric `rc` here would assert a probe that never ran. `path=<p>` is required because the `P0_tool name=… path=…` inventory lines are printed only after every tool has resolved, so this STOP is the sole place the rejected object is named |
| 2 | executing identity | a complete, uniquely parsed `getent passwd gatea` entry defines the named login contract; numeric `id -u` and `id -g` equal that entry's uid and primary gid, while `id -un=gatea` and rendered names are diagnostic only | `P0_STOP reason=identity_unresolvable account=gatea rc=<n> detail=<d>` for resolver/invocation/parse ambiguity; after successful resolution, `P0_STOP reason=identity_unexpected observed_numeric=<u:g> expected_numeric=<u:g> account=gatea` for a mismatch |
| 3 | service-account identity and login groups | because `install.sh` allocates the named account dynamically, a complete unique `getent passwd mtc-bridge` result must map that name to the preregistered numeric `WPI_STATE_UID:WPI_STATE_GID=999:988`; then complete numeric `id -G` output for `gatea` contains neither gid `0` nor gid `988`; rendered names are diagnostic only | `P0_STOP reason=identity_unresolvable account=mtc-bridge rc=<n> detail=<d>` for resolver/invocation/parse ambiguity; `P0_STOP reason=identity_unexpected observed_numeric=<u:g> expected_numeric=999:988 account=mtc-bridge` if the named allocation moved; `P0_STOP reason=group_query_not_evaluable rc=<n> detail=<d>` before group interpretation; after a complete parse, `P0_STOP reason=capability_wider_than_ledger gid=<g>` if 0 or 988 is present |
| 4 | `ss` present | `command -v ss` resolves | `P0_STOP reason=missing_tool tool=ss` |
| 5 | `curl` present | `command -v curl` resolves | `P0_STOP reason=missing_tool tool=curl` |
| 6 | `sha256sum` present | `command -v sha256sum` resolves | `P0_STOP reason=missing_tool tool=sha256sum` |
| 7 | `systemctl` present | `command -v systemctl` resolves | `P0_STOP reason=missing_tool tool=systemctl` |
| 8 | execution-domain binding | the login's user, mount, PID and network namespace identities plus canonical root-mount identity exactly equal the values supplied by the external deploy-channel attestation frozen into `RP6-P0.sh` | `P0_STOP reason=execution_domain_unattested field=<f>` if the attestation is missing/unreadable/unparseable; `P0_STOP reason=execution_domain_mismatch field=<f> observed=<v> attested=<v>` on mismatch; comparison with visible PID 1 is not admissible |
| 9 | system-manager query readiness | only after row 8, `systemctl` can execute, reach the intended system manager over its system bus, pass D-Bus/polkit authorization, and return a complete parseable manager response | `P0_STOP reason=system_manager_unreachable rc=<n> detail=<d>` for invocation, bus, namespace, authorization, timeout, incomplete-output or parse failure |

Row 3 is an inversion worth stating plainly: **more privilege than the ledger assumed
is a STOP, not a bonus.** If `gatea` turns out to be in the state/log group, the
feasibility ledger's premises are wrong, several DEFER-ROOT-SIDE calls were wrong,
and the correct response is re-adjudication of the scope - not a run that quietly
reaches further than the document it was preregistered under. Rows 1 and 4-7 fail closed
to STOP with **no substitution**: a missing tool is not an invitation to improvise a
replacement at run time, which is the whole reason the tool list is preregistered.
Row 8 binds every local result to the externally attested guest domain; an apparently
successful query from a container, chroot, private namespace or visible-PID-1 lookalike
is STOP, not host evidence. Row 9 is not inferred from tool presence. It must exercise a harmless manager query
and distinguish a valid manager response from an invocation, D-Bus, polkit, PID/mount
namespace or parse error. If row 9 cannot hold as `gatea`, manager-backed B2/B4 checks
move to RPD-VERIFY; they do not accuse the host from an empty or error result.

### 8.2 RO stage - one row per admitted check

| # | check | predicted outcome if it holds | exact predicted first divergence if it does not |
|---|---|---|---|
| 1 | B2 active | `systemctl is-active` returns a parseable unit state and that state is `active` | `B2_STOP reason=system_manager_unreachable operation=is-active rc=<n> detail=<d>` for invocation, bus, namespace, authorization or parse failure; after manager reachability is proven, a valid state such as `inactive` is evaluable and becomes `B2_FAIL reason=unit_not_active state=<s> expected=active` even when `is-active` uses a nonzero result rc |
| 2 | B2 restart count | `NRestarts` is `0` | `B2_STOP reason=unit_property_unreadable prop=NRestarts rc=<n> detail=<d>` before comparison on any manager/query/parse error; only a successfully read value may become `B2_FAIL reason=nrestarts_nonzero value=<n> expected=0` |
| 3 | B2 restart policy | `Restart` is `no` | `B2_STOP reason=unit_property_unreadable prop=Restart rc=<n> detail=<d>` before comparison on any manager/query/parse error; only a successfully read value may become `B2_FAIL reason=restart_policy value=<v> expected=no` |
| 4 | B2 process identity | `MainPID` is `189813` | `B2_STOP reason=unit_property_unreadable prop=MainPID rc=<n> detail=<d>` before comparison on any manager/query/parse error; only a successfully read value may become `B2_FAIL reason=mainpid_changed value=<p> expected=189813` - **named risk R3**: with `Restart=no` a live unit cannot have self-restarted, so a changed MainPID means a manual restart between the transition inventory and dispatch. That is a FAIL requiring Lead adjudication, never a silent re-pin |
| 5 | B2 candidate binding | after P0 domain binding, complete manager properties are structurally parsed: the effective `ExecStart` argv (not comments, inactive directives, environment text or arbitrary substrings) binds its executable and release argument to the exact venv and release roots for `2ce41e34...321b`, and the effective fragment/drop-in set contains no unpreregistered override | a valid complete manager result `LoadState=not-found` is observed deviant state and becomes `B2_FAIL reason=unit_not_loaded`; `B2_STOP reason=unit_definition_unreadable operation=show rc=<n> detail=<d>` applies only to invocation, bus, namespace, authorization, timeout, incomplete-output or grammar error; any other complete structural mismatch becomes `B2_FAIL reason=unit_not_bound_to_candidate field=<field> observed=<v>` |
| 6 | B2 no `[Install]` | after path-object binding, a complete byte read of the fragment is parsed under the systemd unit-file line grammar and contains no section header whose exact parsed name is `Install`; comments, continuations and arbitrary substrings do not count | `B2_FAIL reason=unit_fragment_absent path=<p>` on positively established ENOENT; `B2_STOP reason=fragment_unreadable_or_unparseable rc=<n> path=<p> detail=<d>` on invocation/access/read/encoding/NUL/grammar or ambiguous-ENOENT error; only a complete successful parse may become `B2_FAIL reason=install_section_present path=<p>` - grep or substring matching is not admissible |
| 7 | B2 fragment identity | after the section-wide path-object binding holds, `sha256sum` equals `WPI_UNIT_FRAGMENT_SHA256`, size 3736 | `B2_FAIL reason=unit_fragment_absent path=<p>` when a searchable, bound parent chain positively establishes ENOENT; `B2_FAIL reason=unit_fragment_digest_mismatch observed=<h> expected=<h>` only after `sha256sum` exited 0 and emitted a syntactically valid 64-hex digest plus the 3736-byte count; `B2_STOP reason=fragment_unreadable rc=<n> path=<p>` for invocation, permission, LSM, ambiguous-ENOENT or parent-traversal error |
| 8 | B4 sandboxing | each named property is successfully read and equals the template-declared value (`PrivateTmp`, `ProtectSystem`, `NoNewPrivileges`, `RestrictAddressFamilies`, `CapabilityBoundingSet`, `ReadWritePaths`, `KillSignal`, `KillMode`, `TimeoutStopSec`, `FinalKillSignal`) | `B4_STOP reason=unit_property_unreadable prop=<P> rc=<n> detail=<d>` before comparison on any invocation, bus, namespace, authorization, incomplete-output or parse error; only a successfully read property may become `B4_FAIL reason=property_mismatch prop=<P> observed=<v> expected=<v>` |
| 9 | B4 start mode | the complete effective `Environment` value is parsed as systemd's tokenized environment grammar and contains exactly one effective `MTC_BRIDGE_START_MODE` assignment whose value is `credential_free_disarmed`; a duplicate, shadowed or substring-only occurrence does not satisfy the row | `B4_STOP reason=unit_property_unreadable prop=Environment rc=<n> detail=<d>` before interpretation on any manager/query/grammar error; only a complete successful parse may become `B4_FAIL reason=start_mode_missing_or_altered observed=<v>` |
| 10 | B3s release root | after component-wise path and mount binding, the literal release root is a non-symlink directory with numeric mode/owner `0555 0:0` (rendered `root:root` diagnostic only) | `B3_FAIL reason=path_absent path=<p>` on positively established ENOENT; `B3_FAIL reason=path_metadata_mismatch path=<p> kind=<k> mode=<m> owner_numeric=<u:g> expected=directory,555,0:0` after a successful `lstat`; `B3_STOP reason=path_not_evaluable path=<p> rc=<n> detail=<d>` on invocation/access/traversal/ambiguous error |
| 11 | B3s venv root | after component-wise path and mount binding, the literal venv root is a non-symlink directory with numeric mode/owner `0555 0:0` | same classification grammar as row 10 |
| 12 | B3s sweep budget | each sweep's stdout, stderr, rc and elapsed time are captured atomically and the sweep finishes inside 120 s; pinned `/usr/bin/timeout` is the ninth bound tool and enforces the bound on every child, with the post-hoc clock retained as a second gate | `B3_STOP reason=sweep_budget_exceeded root=<r> elapsed_s=<n> elapsed_ms=<n> budget_s=120`; timeout is adjudicated before rc, diagnostics or stdout |
| 13 | B3s walk completeness | after row 12 holds, each complete diagnostic stream is empty and `find` exits 0; no LSM, ACL, mount or traversal error occurred | `B3_STOP reason=walk_incomplete root=<r> rc=<n> detail=<d>` on any nonzero rc or mount/traversal/diagnostic error. `walk_permission_error` is deleted: Pattern 5 forbids deriving an errno class from `find` prose. This STOP disqualifies rows 14 and 19 |
| 14 | B3s write bits | only after rows 12-13 prove a complete rc-0 sweep may the captured stdout be interpreted; it contains no writable pathname in either tree | `B3_FAIL reason=writable_path_inside_immutable_tree path=<p> count=<n>` is admissible only from stdout of a sweep already proven complete; an unsafe-to-render but valid absolute pathname uses `path=[unrenderable] path_sha256=<h> count=<n>`. Partial stdout is discarded as result evidence and can produce only the row-12/13 STOP |
| 15 | B3s metadata dirs | component-wise `lstat` of `/etc/mtc-bridge` proves a non-symlink directory at numeric `0750 0:0`; `WPI_STATE_DIR` and `WPI_LOG_DIR` prove non-symlink directories at numeric `0750 999:988`, the preregistered numeric allocation of the named `mtc-bridge` account (names diagnostic only) | `B3_FAIL reason=path_absent path=<p>` on positively established ENOENT; `B3_FAIL reason=path_metadata_mismatch path=<p> kind=<k> mode=<m> owner_numeric=<u:g> expected=<kind,mode,u:g>` after a successful `lstat`; `B3_STOP reason=path_not_evaluable path=<p> rc=<n> detail=<d>` on invocation/access/traversal/ambiguous error |
| 16 | B3s scope | the block contains no path with prefix `/etc/mtc-bridge/`, `<WPI_STATE_DIR>/` or `<WPI_LOG_DIR>/` | not a run-time predicate: a Stage-1 path-scope proof failure (section 10.2) blocks the freeze, so this can never divergence at run time |
| 17 | B1a lock bytes | after path-object binding, `sha256sum` of the installed non-symlink regular `requirements.lock` equals `a1881296...bf66e`, size 117762 | `B1a_FAIL reason=installed_lock_absent path=<p>` on positively established ENOENT; `B1a_FAIL reason=installed_lock_object_unexpected kind=<k>` for a symlink/non-regular leaf; `B1a_FAIL reason=installed_lock_digest_mismatch observed_bytes=<n> expected_bytes=117762` when the successfully `lstat`-ed size diverges, which is adjudicated before the digest; `B1a_FAIL reason=installed_lock_digest_mismatch observed=<h> expected=a1881296...bf66e` only after `sha256sum` exited 0 and emitted a syntactically valid 64-hex digest plus the 117762-byte count - disposition **investigate read-only**: weigh a wrong expected value *and* genuine drift, re-check blob -> LF-pinned export -> manifest-verified install before escalating a STOP or dismissing one; `B1a_STOP reason=installed_lock_unreadable rc=<n> path=<p>` for invocation, permission, LSM, ambiguous-ENOENT or parent-traversal error |
| 18 | B1 interpreter | after path-object binding, `<venv>/bin/python` is a non-symlink regular file; its execute is a separately bounded post-binding observation, `-V` demonstrably runs, and reports a `3.12.` version | `B1_FAIL reason=interpreter_absent path=<venv>/bin/python` on positively established ENOENT; `B1_STOP reason=interpreter_not_executable path=<venv>/bin/python` on access/exec/EACCES/126 denial (never a version FAIL); every observed symlink or other object is `B1_STOP reason=interpreter_object_unbound kind=<k> target=<sanitised-t>` routed to Lead adjudication; `B1_FAIL reason=interpreter_version observed=unpreregistered_version expected=3.12.*` is the accepted content-suppressed rendering after the regular file demonstrably ran |
| 19 | B1 lock parity | `verify_lock.py --check-installed` exits 0 and emits its structurally parsed PASS result with `packages=56`; **preflight (Codex F1): after path-object binding and a complete metadata enumeration, every `*.dist-info` directory and its required `METADATA` and `RECORD` under `<WPI_VENV_ROOT>/lib/python3.12/site-packages` is proven present and open+readable by `gatea` before parity runs** | `B1_FAIL reason=distribution_metadata_absent path=<p>` when complete enumeration of a readable bound parent positively establishes a required member is missing; unsafe-to-render valid paths use `path=[unrenderable] path_sha256=<h>`; the component walk of `site-packages` and of each `*.dist-info` directory carries the default walk outcome, so a positively absent component is `B1_FAIL reason=path_absent path=<p>` and a deviant one is `B1_FAIL reason=path_metadata_mismatch path=<p> kind=<k> mode=<m> owner_numeric=<u:g> expected=<kind,mode,u:g>`; enumeration budget/traversal failures use the row-12/13 tokens under prefix `B1`; `B1_FAIL reason=lock_installed_parity observed=<detail>` ONLY when the verifier ran clean and structurally distinguished a genuine named missing/extra distribution, never on a generic nonzero rc or substring; `B1_STOP reason=metadata_unreadable path=<p>` for open/parse/EACCES/LSM/traversal error; `B1_STOP reason=verifier_not_evaluable rc=<n> detail=<d>` for any other nonzero verifier rc that did not positively distinguish a mismatch. Row 18's STOP and this row's completeness/readability precondition each disqualify parity entirely |
| 19a | B1 verifier identity | before row 19 parity executes, the non-symlink regular `verify_lock.py` is component/mount-bound, size 3735, and SHA-256 `d951e0ee...a451e5`; execution is separately bounded after that pre-exec window closes | `B1_FAIL reason=verifier_absent path=<p>` on positive ENOENT; `B1_FAIL reason=verifier_object_unexpected path=<p> kind=<k>`; `B1_FAIL reason=verifier_digest_mismatch observed=<h> expected=<h>` or the corresponding `observed_bytes=<n> expected_bytes=3735`; `B1_STOP reason=verifier_unreadable path=<p> rc=<n> detail=<d>` when identity cannot be evaluated |
| 20 | B5 endpoint | only after the row-22 service-netns binding precondition, `GET /api/status` completes and returns HTTP 200 | `B5_STOP reason=status_endpoint_not_evaluable rc=<n> detail=<d>` for invocation, transport, timeout, incomplete/malformed response or unbound namespace; a complete valid 401/403 is `B5_STOP reason=status_endpoint_access_denied code=<c>`; any other complete valid non-200 response is an observed deviant state and becomes `B5_FAIL reason=status_endpoint_unexpected_http code=<c>` |
| 21 | B5 flags | only after row 20, the complete response body is strict JSON (duplicate keys and NaN/Infinity/-Infinity rejected), has the required top-level shape and exact typed fields, and reports `state` DISARMED, `state_version` 1, `mode` `credential_free_disarmed`, `network` disabled, `exchange_conn` disabled, `exchange_enabled` false, `credential_lookup` disabled, `arm_enabled` false | `B5_STOP reason=status_body_unreadable_or_unparseable detail=<d>` for incomplete/read/strict-JSON/duplicate-key/top-level-shape failure; absent preregistered key -> `B5_STOP reason=schema_unexpected field=<f>`; present key with wrong type -> `B5_FAIL reason=flag_mismatch field=<f> observed_type=<t> expected_type=<t>`; wrong typed value -> `B5_FAIL reason=flag_mismatch field=<f> observed_sha256=<h> expected=preregistered_typed_value`, the accepted content-suppressed rendering - **named risk R4**: these key names come from matrix prose, not from an observed response body |
| 22 | B5/B6 service network-namespace binding and B6 listener set | before either `curl` (rows 20-21) or `ss` (rows 22-23) output is interpreted, `readlink /proc/self/ns/net` equals `readlink /proc/<MainPID>/ns/net` (MainPID from row 4); then the unfiltered complete `ss -H -ltn` output is captured whole as a create-once evidence leaf, every socket row is structurally parsed, and only then the block scopes to port 8790 and requires exactly one listener at `127.0.0.1` | `B6_STOP reason=netns_mismatch caller=<i> service=<i>` if identities differ; `B6_STOP reason=service_netns_unreadable path=/proc/<pid>/ns/net rc=<n>` if the identity cannot be read, routing both B5 and the listener-set half to RPD-VERIFY; `B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=<n> detail=<d>` on invocation/read/timeout/incomplete/table-grammar error; `B6_FAIL reason=listener_set_unexpected observed_count=<n> expected=1x127.0.0.1:8790` is the accepted content-suppressed rendering only after binding and a complete structural parse; a structurally parsed port-8790 row whose local address is neither `127.0.0.1` nor one of row 23's wildcard/VM addresses is `B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790` - the address itself is suppressed, so this is the accepted rendering rather than an `addr=<a>` echo |
| 23 | B6 no wildcard | no structurally parsed port-8790 row has local address `0.0.0.0`, `::` or the VM IP, subject to row 22 | `B6_FAIL reason=nonloopback_listener addr=<a>` admissible only after row 22's namespace binding and complete table parse held; substring matching of `ss` text is not admissible |
| 24 | B6 external closed | a bounded operator-side TCP probe completes with the classified result `connection_refused` or `timeout` for `172.24.55.233:8790` | `B6_FAIL reason=host_reachable_8790 outcome=connected` only after a completed connection; `B6_STOP reason=external_probe_not_evaluable outcome=<o> rc=<n> detail=<d>` for invocation, local socket, routing, cancellation, clock or unclassified errors |

**Path-object binding rule (catalogue Pattern 3).** Rows 6-7, 10-11, 15 and 17-19
bind paths, not only leaves. In the same frozen block and before content or metadata
comparison, the wrapper walks every literal component with non-following metadata,
proves the expected directory/regular-file kind, rejects `.`/`..`, alternate spellings
and every unpreregistered live or dangling symlink, and compares numeric ownership.
No venv-interpreter symlink is accepted: an observed symlink STOPs for Lead adjudication.
For each mount observation, `/proc/self/mountinfo` is copied once into a create-once
evidence leaf; that same leaf is structurally parsed and hashed. The ordered
`normalised_path_projection_v2` record set defined in section 4 - effective covering
mount per point path, subtree closure below every preregistered root, and per-root
counts - is hashed and compared with the literal deploy-channel-attested digest, so an
overlay or bind mount cannot substitute a decoy object anywhere inside a trusted
subtree. A missing leaf under a successfully searched, bound parent is evaluable FAIL;
inability to inspect a component or mount record is STOP. Parent, mount and leaf checks
are one atomic observation, not evidence gathered in different stages.

**Preregistered `binding=` vocabulary.** The binding tokens are evidence, so their set
is fixed here and no other spelling is admissible: `binding=component_and_mount` (leaf
and every component bound inside an open mount window - metadata directories and
regular-file digests), `binding=component_and_mount_window_closed` (the same, with the
window proven closed before the result line - immutable-tree rows),
`binding=window_open_pending_close` (a per-member result emitted while the enclosing
window is still open, closed later by the section's own guard - metadata members),
`binding=equal` (the two namespace identities compared equal),
`preexec_binding=component_and_mount_window_closed` and
`verifier_preexec_binding=component_mount_digest_window_closed` (the pre-exec object
binding of an object that is then executed, the second including its digest), and
`exec_binding=separate_bounded_exec` (the execution itself, a separately bounded
observation after that window closed).

**Instrument-attestation disclosure (round-3, auditor finding 3).** Each `RP7_tool`
binding line carries `resolution=pinned_absolute attestation=<a>`. `attestation=self`
is emitted for `stat`, `env`, `sha256sum` and `timeout`: the mount projection and the
tool binding itself are *built with* those four, so they are exercised before any tool
binding line exists and they attest their own integrity. `attestation=bound_instrument`
is emitted for `readlink`, `find`, `systemctl`, `ss` and `curl`, which are bound by
already-attested instruments. This is a disclosed property of the design, not a defect
to be discovered at adjudication: a digest comparison needs a digest tool, and the
pinned absolute path plus the non-group/world-writable mode check are what stand behind
the first four.

**Binding ordering rule.** Row 19 is admissible **only** after row 13 has held for
the venv tree, row 18's interpreter has demonstrably run, and the row-19
metadata-readability precondition has passed. The row-13 `find` guard proves
traversal and stat-ability of the tree, **not** regular-file readability: a
`*.dist-info/METADATA` at mode `000`, under a named ACL denying `gatea`, or denied by
an LSM rule is stat-able by `find` yet unreadable to the verifying process.
`verify_lock.py --check-installed` enumerates installed distributions from metadata
objects; an unreadable one is indistinguishable from a distribution that is not
installed, so it would surface as a *missing distribution* - a false FAIL against a
correct host, which is the same shape of error as tonight's, arriving through a
different door. If row 12 or 13 STOPs, row 14 is not evaluated, row 19 must STOP too,
and neither a writable-path FAIL nor a parity FAIL may be reported from partial output.

**Atomic-walk adjudication rule (Codex audit F4, applied round 1.3).** For every
filesystem walk, including the immutable-tree write-bit sweeps and any metadata
enumeration feeding row 19, the wrapper captures stdout, stderr, rc and elapsed time
without streaming stdout into a result parser. It adjudicates in this binding order:
(1) timeout/budget, (2) exit status plus the complete diagnostic stream, and only then
(3) stdout. A timeout, nonzero rc, or any LSM, ACL, mount, permission or traversal
diagnostic is `B3_STOP`/`B1_STOP` as applicable. A pathname emitted before the later
error is partial output and cannot become `B3_FAIL`. Only a proven complete rc-0,
diagnostic-free walk exposes stdout for writable-path or metadata interpretation.

**Metadata-readability adjudication rule (Codex audit F1, applied round 1.2).** Row
19 is evaluated under a fixed precedence. The wrapper first proves every metadata
object the verifier consumes - every `*.dist-info` directory and its `METADATA` and
`RECORD` under `<WPI_VENV_ROOT>/lib/python3.12/site-packages` - is open+readable by
`gatea`. Then the verifier's own exit status is adjudicated in this order: a
required metadata member positively absent under a completely enumerated, readable,
bound parent is an evaluable `B1_FAIL reason=distribution_metadata_absent`; otherwise a
**positively-distinguished installed-set mismatch** (the verifier named a missing or
extra distribution, having read every object) is the **only** input that may become
`B1_FAIL reason=lock_installed_parity`; every open, parse, permission, LSM or
traversal error from the preflight or from the verifier, and every other nonzero
verifier rc that did not positively distinguish a mismatch, is `B1_STOP`. A generic
nonzero verifier rc must never become `B1_FAIL reason=lock_installed_parity`. This
makes the row-13 traversal guard non-sufficient by construction, exactly as the audit
requires, and is the same defect class as `B3-GAP-ENV` - an inability-to-evaluate
misread as a host finding.

**System-manager adjudication rule (Codex audit F3, applied round 1.3).** P0 first
requires `systemctl`, then separately proves query readiness against the intended
system manager. Every B2/B4 manager probe captures stdout, stderr, rc and elapsed
time. Invocation, missing-tool, D-Bus, polkit, PID/mount-namespace, authorization,
timeout, incomplete-output and parse errors are adjudicated as P0/B2/B4 STOP before
any stdout is compared. `systemctl is-active` is not classified by numeric rc alone:
if the manager returned a valid state such as `inactive`, the probe ran and the state
is an evaluable B2 FAIL; if no valid state was obtained, it is STOP. `show` and `cat`
must likewise return complete, parseable results before a missing value or mismatch
may FAIL. If readiness cannot be established as `gatea`, the affected manager-backed
checks move to RPD-VERIFY.

**General probe-output precedence (binding on every interpreted stdout).** Every
external command and local transport primitive - including `command -v`, `getent`,
`id`, `lstat`/`stat`, `find`, the unit parser, `ss`, `curl`, `sha256sum`, `readlink`,
`systemctl`, `mktemp`, the TCP probe, close/bind hashing and every verifier - captures
stdout, stderr, rc and elapsed time. Timeout,
invocation/access/traversal errors, complete diagnostics and parse validity are
adjudicated before stdout is treated as an observation. Defined result statuses such
as a parser's defined no-match and a valid inactive unit state remain evaluable only when the tool
actually ran and returned a complete parseable result. Partial or error-path stdout
is evidence of the attempted probe, never evidence of host drift.

**Probe execution-environment rule (catalogue Pattern 4).** Evidence-producing
children run from a fixed trusted working directory with a cleared environment, fixed
`LC_ALL=C`, a minimal pinned PATH or absolute helper paths, and a run-owned TMPDIR that
cannot name a protected host directory. The bounding wrapper is **inside** the cleared
environment, not outside it: the cleared-environment exec comes first and the pinned
`timeout` is its argument, so the process that decides whether a probe was bounded runs
under the same cleared environment as the probe it bounds. Each helper is bound by
non-following kind, numeric ownership and non-group/world-writable mode before
execution; any accepted symlink has an explicitly preregistered target chain. Python runs isolated with Python
environment variables removed. This rule binds the unprivileged blocks for evidence
integrity and binds RPD-VERIFY additionally because its children execute with root
authority. An inherited PATH, PYTHONPATH, cwd or TMPDIR can never select code or a
write location for a check.

**Structured-input adjudication rule (catalogue Pattern 5).** JSON, systemd unit
files and manager properties, `ss` tables, transport TSV, digest sets, mount tables
and line-oriented diagnostics are parsed under their full declared grammar. Fixed
strings, regular-expression presence, first-substring-wins and prose errno matching
cannot prove a structural claim. Parsers consume the complete input, reject duplicate
or extra structural ambiguity where it changes meaning, and distinguish valid
no-match from invocation/read/parse failure. Error classification uses a directly
observed error class where the interface exposes one; ambiguous prose remains STOP.

**Line-reader completion rule (catalogue Pattern 7).** Every reader of
`TRANSPORT_PLAN.tsv`, digest records, path lists, mount tables or captured multi-line
probe output distinguishes clean EOF, an unterminated populated final record, and a
hard read error. It processes a valid populated final record only under the input's
explicit newline contract, rejects malformed/truncated records, and STOPs on any read
failure. A shell loop ending because `read` returned nonzero is not evidence of a
complete scan. Stage 1 must falsify both the no-final-newline and unreadable-source
cases for every shared reader implementation.

**Interpreter-exec extension (GLM review F1, applied round 1.1).** The recorded host
state proves the venv tree is `0555` (traverse+read for other) but records no per-file
execute bit for `<venv>/bin/python`. Executing it is not a privileged action, so B1
stays INCLUDE - but an exec denial must surface as row 18's dedicated
`interpreter_not_executable` STOP, never as a version or parity FAIL. A false FAIL
against a correct host is exactly the B3-GAP-ENV failure shape arriving through a
different door, and this table exists to make that shape impossible.

**Namespace-binding adjudication rule (Codex audit F2, extended by catalogue pass).**
Both `curl 127.0.0.1` and `ss -ltn` operate in the *caller's* network namespace, not
necessarily the service's. If
PAM, an ssh ForceCommand, or a service wrapper lands the `gatea` login in a private
netns while PID 1 and the bridge listen in the host namespace, `ss` succeeds without
a permission error yet observes the wrong namespace - yielding a false `B6_FAIL` (no
port 8790 listener seen) or, in the mirror case, a false PASS (a matching listener in
the login namespace concealing a bad set in the service namespace). Tool presence and
unprivileged socket visibility do not establish namespace identity. The shared row-22
preflight is therefore evaluated before rows 20-21 despite its display number, and
rows 20-23 are admissible **only** after the namespace binding is proven:
`readlink /proc/self/ns/net` (always readable by `gatea`) must equal
`readlink /proc/<MainPID>/ns/net` (the service's netns identity, MainPID from row 4).
A mismatch is `B6_STOP reason=netns_mismatch`; an unreadable service netns identity
(EACCES on `/proc/<pid>/ns/net` for a root-owned service process under ptrace/yama
gating) is `B6_STOP reason=service_netns_unreadable` and routes the listener-set half
to RPD-VERIFY (section 10), where a root-authorised channel establishes the binding.
The B5 status and B6 listener claims are admissible only when the observations are
proven to be in the same namespace as the service. This service-relative binding is
in addition to P0's deploy-channel binding of the login domain to the named staging
guest; neither replaces the other. The operator-side external TCP probe (row 24) is independent
corroboration and is unaffected - it probes reachability from outside, which holds or
fails regardless of which namespace `ss` observed.

**Named risks carried into dispatch.**

- **R1** - `WPI_UNIT_FRAGMENT_SHA256` is elided in the matrix (`538c1c60...279bd`).
  Row 7 cannot be preregistered until the full value is read from the transition
  inventory. No successor is dispatchable with this unfilled.
- **R2** - `WPI_LOG_DIR` has a recorded mode but no recorded literal path in the
  inputs. Row 15 cannot be preregistered until it is pinned from the unit fragment's
  `ReadWritePaths`/`LogsDirectory`. Deriving it at run time from the same
  `systemctl show` output the run is asserting against would make row 15 circular.
- **R3** - MainPID equality (row 4) is a strong predicate precisely because
  `Restart=no` forbids self-restart; it is also the row most likely to move for a
  benign reason. It is preregistered as FAIL-with-adjudication so that a benign cause
  is *established* rather than *assumed*.
- **R4** - the B5 field names are unobserved (see above).
- **R5** - "exactly one listener" in the source records is read here as *exactly one
  bridge listener on 8790*. `sshd` is necessarily also listening, since the run
  arrives over ssh. Rows 22-23 are therefore scoped to port 8790, and the full
  listener inventory is captured as evidence rather than asserted against a count.
  If the source records meant a literal global count of one, that reading is
  falsified by the transport itself and must be corrected in the successor.

Any `FAIL` is a **STOP requiring Lead adjudication** - a candidate-repair question,
not a documentation outcome. Any `STOP` from a `stat`, `find`, `grep`, `ss`, `curl`,
`sha256sum`, `readlink`, `systemctl`, system-bus query, `mktemp` or clock error, or any
internal open/parse/permission error raised by `verify_lock.py`, stops the stage and
is never re-read as a PASS. Probe error adjudication always precedes stdout comparison.

**Scope of the WP-I claim, preregistered.** A clean RO stage admits exactly this:
the running unit is the accepted first-start unit bound to the frozen candidate,
the complete release and venv walks found no DAC write bits, the installed lock bytes
match the preregistered lock digest and the completely readable installed-distribution
set matches that lock, its sandboxing and start-mode pins are effective, its status
endpoint in the service network namespace reports credential-free DISARMED, and the
same service namespace has only the preregistered loopback control listener while the
operator-side probe cannot connect. The write-bit sweep is not a proof against ACL,
capability, writable-mount or future-mutation mechanisms, and lock/package parity is
not byte identity of either whole tree. It is **not**
a full `verify.sh` run (that verifier is pre-start and post-Gate-A fails by design -
G2), **not** a permissions proof of the root-owned metadata surface (deferred,
section 10), **not** a SIGTERM/reboot/rollback/backup proof (Group C, section 9),
and **not** WP-L, WP-A or Audit-2 completion.

## 9. What is deliberately NOT preregistered

Nothing in this section has an executable form anywhere in the run kit. Each item is
listed with the dependency that blocks it, exactly as the Stage 2 template does for
C1-C5.

**Group C - mutating checks. No block, no command, no argv, no conditional branch.**

- **C1 (graceful SIGTERM clean shutdown, WP0 I-R4).** Blocked twice over: it needs an
  explicitly named authority lift for `systemctl stop` plus the recovery start, and a
  budget lift; and it has an open **COMMAND GAP** - no verifier asserts "no dangling
  state after SIGTERM". A bounded post-stop evidence procedure must be designed
  locally first. Do not improvise one.
- **C2 (reboot DISARMED).** Blocked on reboot authority + budget, and on a definition
  that does not yet exist: scenario A (plain reboot from the current unmasked state,
  expecting inactive+unmasked) and scenario B (separately authorised stop+mask, then
  reboot, expecting inactive+masked) are different predicates and one must be chosen
  and preregistered before anything runs. `verify.sh` is a pre-start masked-mode
  verifier and is not the post-reboot instrument. **COMMAND GAP.**
- **C3 (WAL-consistent backup/verify/restore on a temporary copy).** Blocked on
  authority + budget, and on a **COMMAND GAP confirmed at the candidate**:
  `wal_state_bundle.py` exposes exactly two subcommands, `create` and `verify`. There
  is **no `restore` subcommand**, so the restore-into-temp wrapper does not exist and
  must be authored locally. Note also that the live DB lives under a directory
  `gatea` cannot read at all.
- **C4 (rollback stop+mask, and release-rebind).** Blocked on KVM2-P4-08
  authorisation + budget. The stop+mask path additionally requires the accepted
  state-manifest hash from C3, which `rollback.sh` makes mandatory (`:57-58`). The
  release-rebind path has an **unmet prerequisite** (G3): only candidate
  `2ce41e34...321b` is installed, and the previous release is already absent. Do not
  invent a target release.
- **C5 (runtime egress / TESTNET-only / no-mainnet / Telegram disposition).** Blocked
  on credential and broker/TESTNET network authority that does not exist, and
  **structurally unobtainable from the current runtime**: at
  `2ce41e34...321b:IBKR_PAPER_BRIDGE/bridge/app.py:149` the credential-free DISARMED
  branch never reaches broker construction, so no broker egress exists to capture. A
  future capture would require a different, separately authorised start mode. ARM
  remains forbidden, and any future capture must remain DISARMED.

**DEFER-ROOT-SIDE - privileged checks routed to RPD-VERIFY (section 10), not to the
run plan.**

- Existence, name, mode and ownership of the env file under `/etc/mtc-bridge`. The
  `bridge.env` vs `mtc-bridge.env` naming question from the Stage 2 expectations
  table remains **unresolved, not triggered**, and this run plan does not adjudicate
  it - permission denial precedes the existence question, and it will precede it
  again for any unprivileged successor.
- `/etc/mtc-bridge/install_manifest.json`: the release-SHA binding, the
  release-manifest binding, and the `requirements_lock_sha256` corroboration of B1a.
- Any per-file mode or ownership assertion *inside* the state and log directories.
- `ufw status` (B6's firewall half).
- B5 rows 20-21 and B6 rows 22-23 if the unprivileged login cannot bind its network
  namespace to the service MainPID namespace; a loopback `curl` result from an
  unbound namespace is no more admissible than an unbound `ss` inventory.
- B2 rows 1-5 and B4 rows 8-9 if `gatea` cannot establish P0 system-manager query
  readiness because `systemctl`, the system bus, the intended PID/mount namespace or
  D-Bus/polkit authorization is unavailable. Direct fragment reads in B2 rows 6-7
  remain unprivileged; manager-backed state/property claims require RPD-VERIFY.

**Everything the Stage 2 template excludes, excluded here on the same terms.**

- No mutating step of any kind: no service stop, start, enable, disable, mask or
  unmask; no reboot; no rollback rehearsal; no unit write; no chmod/chown of any host
  object outside the run's own create-once tree.
- No credential read, no `POST /api/arm`, no broker/exchange/order/TESTNET/mainnet
  action, no master merge, no KVM2/WP-V action, no deletion of the old payload
  archive, no host reprovisioning.
- No `sudo`, and no probe for `sudo` (section 0, rule 3).
- No `git add`, `git commit`, `git push`, branch or worktree action: Git sequencing
  belongs to the Lead.

## 10. RPD-VERIFY: the root-side channel for deferred checks

### 10.1 Unprivileged path allowlist

The RO stage may reference only these host paths. The list is exhaustive; anything
else is a Stage-1 freeze failure.

| Path pattern | Recorded mode/owner | Why `gatea` can reach it |
|---|---|---|
| `/opt/mtc-bridge/releases/2ce41e34...321b/**` | numeric `0555 0:0` at the root (`root:root` diagnostic only) | root is `r-x` for other; complete traversal/readability and absence of DAC write bits are separate rows 12-14 predicates |
| `/opt/mtc-bridge/venvs/2ce41e34...321b/**` | `0555` | same |
| `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` | `0644`, 3736 B | world-readable regular file |
| `/etc/mtc-bridge` **(terminal only)** | numeric `0750 0:0` | `lstat` of the directory needs search on `/` and `/etc` (both world-searchable), not on the target itself |
| `<WPI_STATE_DIR>` **(terminal only)** | numeric `0750 999:988` | same argument via `/var/lib`; `mtc-bridge` name diagnostic only |
| `<WPI_LOG_DIR>` **(terminal only)** | numeric `0750 999:988` | same argument via the log parent; `mtc-bridge` name diagnostic only |
| `<REMOTE_BASE>/**` | `0700`, P0-resolved numeric euid:egid | the run's own create-once tree; `gatea:gatea` diagnostic only |
| `127.0.0.1:8790` | loopback listener | loopback is not privilege-gated for a local user |

"Terminal only" is the whole B3-GAP-ENV repair in two words: the path may appear as a
complete `stat` argument and may never appear as a prefix.

### 10.2 Path-scope proof (Stage 1 gate)

Stage 1 must emit, per frozen block, the sorted set of every host path that can reach a
filesystem or network primitive after constant and variable expansion, and must show
every entry inside section 10.1. A literal-string scan is supplemental only: it misses
concatenated variables, command substitutions, arrays, sourced values and dynamically
constructed prefixes. The accepted proof therefore parses the complete shell input,
rejects unresolved/dynamic path construction, proves every path-bearing argument is
derived only from preregistered constants, expands those constants, and checks the
resulting closed set against section 10.1. It also falsifies a forbidden path assembled
from separately harmless tokens and must reject it. The proof is recorded in the Stage
1 record with the exact command and real RED/GREEN output, and the archive is not frozen
until it passes. This is a static check over frozen bytes, so it cannot be satisfied by
a run-time guard and cannot be skipped by a run-time branch.

The check `RP1-B3.sh` failed tonight would have failed this proof before transport.

### 10.3 RPD-VERIFY pattern

A deferred check is discharged root-side at deploy time, not by widening this run:

1. A root-authorised channel (deploy-time hook, or a separately authorised root
   session) executes the check and writes its output plus the exact command that
   produced it. Every child process is part of the privileged trusted computing base:
   the channel pins and verifies absolute helper/interpreter paths, non-symlink kind,
   numeric `0:0` ownership and non-group/world-writable mode; clears inherited
   environment variables (including PATH, Python variables and TMPDIR); uses an
   isolated interpreter mode and fixed trusted working directory where applicable;
   and creates no temporary file under a protected host path. If any of those
   preconditions cannot be proved, RPD-VERIFY STOPs without executing the child.
2. The record is hashed at the point of production, by the producing channel.
3. The record reaches the unprivileged verifier by one of two routes, and **which
   route is used is itself a preregistered decision**:
   - **(a) operator-side transport** - the root channel returns the record out of
     band, and it is bound in the operator record. No host mutation.
   - **(b) deposit at a world-readable path** - e.g. numeric `0444 0:0` under a
     preregistered directory outside the protected metadata dirs, which the
     unprivileged run then reads and binds. This **creates a file on the host** and
     is therefore a mutation requiring its own authority; it is not available under
     the current envelope.
4. The unprivileged run **reads and binds** the record; it never re-derives the
   predicate, because it cannot, and a check that appears to re-derive what it is
   actually reading back is worse than no check.

Both routes are named here so that the successor picks one deliberately. Neither is
authorised now, and route (b)'s deposit path is not preregistered in this draft.

## 11. Immutability rules

The successor of this document is void, and a **new** one with fresh RUNIDs is
required, if any of the following changes: any hash in section 3 or 4; the route,
user, identity path or ssh options in section 5; any path in section 1 or section
10.1; either RUNID or stage id; any pinned value in section 2; or the op list in
section 5. In particular, **if the staging VM's IP address is no longer
`172.24.55.233`, the preregistration does not describe the run** - the argv is
pinned, and editing it invalidates `TRANSPORT_PLAN.tsv`, whose digest the runner
pins, which is the intended failure mode rather than a silent edit.

Two rules are added for WP-I, both from tonight:

- **The P0 result is part of the immutability surface.** If P0 reports an executing
  identity or capability set different from the ledger's premise - including a
  *wider* one - the RO stage does not run under this preregistration. The feasibility
  ledger is an argument from a specific identity against specific recorded modes; a
  different identity is a different argument.
- **A filled `<PIN-BEFORE-DISPATCH: ...>` value is frozen at the moment it is filled,
  and is filled from the cited record only.** Filling one from host output would make
  the run attest to a value it read from the object under test.

A failed allocation burns its RUNID. There is no retry pool and no second RUNID
preregistered for either stage.

## 12. Safety state at the moment of this draft

- SSH/SCP/remote invocation count: **0**
- Staging host contact: **none**; no socket opened, no process spawned toward it, no
  TCP connect attempted, and no deploy-channel domain attestation requested or
  produced (op 06 and the attestation prerequisite are described, not performed)
- RUNIDs minted: **0**. Unit ids minted: **0**. Record roots created: **0**. Remote
  trees created: **0**
- Blocks authored, built or frozen: **0**; `runkit.tar` for WP-I: does not exist
- Service stop/start/enable/mask, reboot, rollback: **none**
- Credential read, ARM, order, broker/exchange, TESTNET/mainnet: **none**
- A3 re-derivation, B1, B1a, B2, B3, B4, B5, B6 execution: **none**
- C1, C2, C3, C4, C5 execution: **none**, and no executable form of any of them exists
  in this draft
- `sudo` invoked or probed: **none**
- Repository writes: confined to the `WPI_PREREG_DRAFT_ROUND1` directory - the
  round-1 files plus this amended draft and `WPI_CATALOGUE_PASS_CODEX_2026-08-10.md`.
  No file outside it was created,
  modified or deleted; no `git add`, `commit`, `push`, checkout, branch or worktree
  action was performed
- Files read for the round-1.4 catalogue task: its kickoff, the ten-pattern catalogue
  and this draft; repository-mandated onboarding was read before task execution. No
  handoff or `GATE_A_A*` file was read for this pass

This draft grants no authority. It grants only a *shape* for a preregistration that
does not yet exist, over a run kit that has not been built, for a run that is
budget-blocked and authority-blocked at section 1 of the matrix.

Verification of every feasibility call and every expectation row is in `SELF_QA.md`;
the per-check ledger is `WPI_CHECK_FEASIBILITY.tsv`.
