# DESIGN NOTES - B3-GAP-ENV Option 1 design repair, round 4 (BOUNDED CLOSURE)

Sections 1 to 9 are the round-3 design record and are unchanged except where a
round-3 statement about the mount reader was inaccurate; those corrections are
marked `ROUND 4` in place. **Section 10 is the round-4 record: the two closures
this round delivers, and nothing else.**

Round 3 received BLOCK at the third and last contracted audit
(`audit3/AUDIT3_REPORT.md`). Six of the eight final-list items were verified
CLOSED. Round 4 is an owner-authorized bounded round whose entire scope is the
TWO surviving REQUIRED findings: the mount-reader read-error arm (finding 1) and
the D026 QA record (finding 2). Nothing else in either block is touched, and
nothing audit 3 verified CLOSED is weakened.

| File | Role |
|---|---|
| `round4/RP1-B3.sh` | repaired unprivileged block, full file (662 lines) |
| `round4/RPD-VERIFY.sh` | root-side deploy-time verify block, full file (775 lines) |
| `round4/DESIGN_NOTES.md` | this file |
| `round4/SELF_QA.md` | syntax evidence, three exact counts, D026 RED/GREEN closure evidence, no-content audit |

sha256 as delivered (round 4):

```
6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc  RP1-B3.sh
3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c  RPD-VERIFY.sh
```

Superseded round-3 hashes, recorded so the delta is checkable:
`e561e8b4...97dd` (RP1-B3.sh) and `f4c5d61d...63a2` (RPD-VERIFY.sh).

Nothing outside `round4/` was created, modified or deleted. No remote host was
contacted. `01_RUNKIT/RP0-LIB.sh` is unmodified and was read only. The directory
contains exactly the four files above and no hidden file, cache or directory.

## 1. How each audit-2 finding was addressed

### A2-F1 - HIGH - the root-side Python child is environment-hijackable

**Addressed. The launch is replaced, not patched.**

What was wrong: `rpd_assert_manifest_binding` tested `command -v python3` and then
ran `python3 -c '...'` with the caller's PATH, the caller's environment and the
caller's working directory. `PYTHONPATH=<dir with json.py>` therefore replaced
`json.loads` inside a process running as root; the audit's own fixture returned
`bound=both`, rc 0, for a file whose entire content was
`THIS IS NOT JSON AND BINDS NOTHING`. Import-time code in that module ran with
root authority, which also refuted the block's `mutation=none` claim - a claim
about the block is a claim about its children.

What round 3 does, in four independent layers:

1. **Pinned absolute tools.** `PYTHON_BIN="/usr/bin/python3"` and
   `ENV_BIN="/usr/bin/env"` are literals. `command -v` is gone. `env` is pinned
   for the same reason as the interpreter: it is the program that builds the
   isolated environment, so taking it from an operator PATH would be the identical
   hole one level up.
2. **The pin is verified.** `rpd_require_pinned_tool` requires each pinned path to
   exist (STOP `manifest_tool_absent` otherwise), to classify as a regular file or
   a live symlink, to be executable, to be owned numerically `0:0`, and to be
   neither group- nor other-writable. A pinned path anyone can rewrite is not a
   pin. Every failure is rc 3, because none of these is a statement about the
   admitted host state - they are statements about whether the block can evaluate
   anything at all.
3. **`env -i` with an explicit minimal child environment.** The child receives
   exactly `PATH`, `LC_ALL` and the eight `RPD_*` values it reads, and nothing
   else. This is what removes `PYTHONPATH`, `PYTHONHOME`, `PYTHONSTARTUP`,
   `PYTHONUSERBASE`, `PYTHONNOUSERSITE`, `LD_PRELOAD`, `LD_LIBRARY_PATH`,
   `LD_AUDIT` and everything else unnamed. An allow-list was chosen over a
   deny-list deliberately: a deny-list has to be complete to work.
4. **Isolated mode and a safe cwd.** `-I` ignores `PYTHON*` variables, drops the
   user site directory and removes the current directory from `sys.path`; `-S`
   additionally skips `site`, so no `.pth` file executes at interpreter startup;
   `-E` is implied by `-I` and is spelled out so the intent survives an edit that
   touches one flag. Independently, the child is launched after
   `cd -- "$CHILD_CWD"` (`/`), so the cwd-shadow variant of the same attack has
   nothing to shadow with even if a future edit loses `-I`. `unset CDPATH` at
   block scope stops `cd` from printing a resolved path into the captured stdout.

The `cd` runs inside the command-substitution subshell only, so the block's own
working directory is unchanged; if it ever failed, the subshell yields no token
and the existing `manifest_parser_unadjudicable` STOP fires.

Driven RED/GREEN, both attack shapes, in SELF_QA section 5.1: the round-2
function returns `bound=both` rc 0 under `PYTHONPATH` and under a poisoned cwd;
the round-3 function returns `install_manifest_unparsable` rc 3 in both cases,
which is the truth about that file.

Residual, stated rather than hidden: `stat`, `readlink`, `id` and `find` are
still resolved through PATH in both blocks. That is inherited from the accepted
block and was not raised by either audit, but it is real, and the deploy channel
is required to supply a trusted PATH. The interpreter is pinned because it is the
one producer that executes arbitrary code from a file rather than returning a
string. See section 9 residual 2.

### A2-F2 - HIGH - the namespace check does not bind the host mount namespace or root

**Addressed. The inference is replaced by attestation.**

What was wrong: round 2 required `/proc/self/uid_map` to be the identity map and
`/proc/self/ns/{user,mnt}` to equal `/proc/1/ns/{user,mnt}`, then printed
`bound=initial`. Inside a rootful container with its own pid namespace, pid 1 is
that container's init and the uid map really is `0 0 4294967295`, so both
predicates hold while `/etc/mtc-bridge` is the container's filesystem. A chroot in
the same two namespaces changes what the literal `/etc` resolves to without
changing either link. No predicate evaluated from inside can close that gap:
every local witness is namespace-local. That is why the fix is not a better local
predicate.

What round 3 does: three comparisons against values minted OUTSIDE the boundary,
by the deploy channel, before this block runs:

1. `/proc/self/ns/user` must equal `RPD_EXPECT_NS_USER`, byte for byte;
2. `/proc/self/ns/mnt` must equal `RPD_EXPECT_NS_MNT`, byte for byte;
3. `stat -c '%d:%i' /` must equal `RPD_EXPECT_ROOTFS_ID`. The namespace tokens
   alone do not identify what `/` resolves to, and a chroot or a bind mount over
   `/` is exactly the case they miss.

Each mismatch is its own reasoned STOP (`namespace_not_attested ns=user|mnt`,
`rootfs_not_attested`). The round-2 uid_map identity predicate is KEPT: it is no
longer load-bearing, but it is a cheap independent refutation of the rootless case
and deleting it would be a weakening. The `/proc/1/ns/*` comparison is REMOVED,
because it contributed nothing that attestation does not contain and its only
observable effect was to license the `bound=initial` string. The evidence line now
reads `bound=attested source=deploy_channel_preregistration`. The token
`bound=initial` does not appear anywhere in either block.

The provenance contract for these three inputs is section 2.

### A2-F3 - MEDIUM - two ownership admissions remain name-mapped

**Addressed. There is no name branch left anywhere.**

What was wrong: `STATE_DIR` and `LOG_DIR` were compared against the rendered name
`mtc-bridge:mtc-bridge`, with only uid 0 or gid 0 refused numerically. An NSS
database that renders the wrong nonzero pair as that name therefore passed - the
audit demonstrated `owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge`, rc 0.

What round 3 does: `B3_SVC_UID` and `B3_SVC_GID` are new REQUIRED preregistered
inputs, guarded exactly like `B3_SWEEP_BUDGET_S` (missing, non-decimal and zero
are three distinct rc-3 STOPs), and `b3_assert_mode_owner` compares
`stat -c '%u:%g'` against `"$B3_SVC_UID:$B3_SVC_GID"` for both directories.
The name/numeric dispatch in `b3_assert_mode_owner` is deleted: every call site
now passes a numeric pair, and the function STOPs with
`owner_expectation_malformed` if it is ever handed anything but `<digits>:<digits>`.
`%U:%G` is still read and printed - a divergence between the numeric and the
rendered form is exactly the evidence an adjudicator wants - and it is also
appended to the ownership FAIL reason, which the round-2 numeric arm did not do.

Nothing is weakened by deleting the round-2 `0:*|*:0` guard: uid 0 or gid 0 now
fails the numeric comparison against a preregistered nonzero pair, and zero is
additionally refused as an INPUT, so the accepted state can no longer name a
root-owned STATE_DIR at all. Driven both ways in SELF_QA section 5.3.

Why the ids are not derived here: `id -u mtc-bridge` asks the same name-service
database the attack controls. An identity that the attacker can answer for is not
an identity. They are minted at provisioning time - section 2.

### A2-F4 - MEDIUM - the structural parser accepts non-JSON constants

**Addressed.** `json.loads` is called with
`parse_constant=constant`, where `constant()` raises `BadConst`. Python accepts
`NaN`, `Infinity` and `-Infinity` by default even though none of the three is a
JSON value, so round 2 adjudicated a manifest containing one as valid structural
JSON. `BadConst` is caught ahead of the generic handler and maps to the new
closed-set token `non_json_constant`, which the shell renders as
`install_manifest_non_json_constant`, rc 3. All three literals are driven RED and
GREEN in SELF_QA section 5.4.

The token stays inside the existing closed lowercase set and the existing
`[a-z0-9_]` guard, so no new channel out of the reader is created.

### A2-F5 - MEDIUM - the mount-table reader skips a partial final record

**Addressed in both blocks, with the same code.**

What was wrong: `while IFS=' ' read -r src tgt rest` never runs its body for a
final record that has no terminating newline, because `read` populates its
variables and THEN returns nonzero at EOF. A table whose last line was exactly
the mount the predicate exists to find was reported as "no mount boundary", rc 0.
Truncated proc reads and short reads produce that shape.

What round 3 does:

- reads one record at a time and PROCESSES a populated record even when the read
  returned nonzero;
- requires exactly the six fields of a mount record - short, empty and over-long
  records are `mount_record_malformed`, rc 3, instead of silently unmatched
  lines;
- treats an unterminated final record as evidence that the source was truncated
  or read short, which is COULD NOT EVALUATE for the whole table:
  `mount_table_unterminated_final_record`, rc 3, reported together with the hit
  count and first matching target it did observe, so an operator sees both facts
  in one line;
- keeps the record count in the success line (`records=<n>`), so "no mount
  boundary" can no longer be printed for a table nobody actually read.

**ROUND 4 CORRECTION.** The round-3 text at this point read: "A genuine read(2)
error mid-file surfaces to a shell caller as a nonzero read with a
possibly-populated buffer, which is the same arm. Driven RED and GREEN, for both
blocks, in SELF_QA section 5.5." That was wrong twice, and audit-3 finding 1 was
right to say so. The EMPTY nonzero read - the shape a read error at the FIRST
read produces - was NOT the same arm: round 3 classified it as ordinary EOF and
returned a false `no_mount_boundary` at rc 0. And it was not driven RED/GREEN at
all - round-3 `SELF_QA.md` claimed no such arm in its section 5.5 tables, so the
two documents disagreed and this one was the inaccurate one. Round 4 closes the
arm
(`mount_table_read_error`, rc 3) and drives it RED and GREEN for both blocks;
see section 10 and SELF_QA section 5.5.1. The genuinely undistinguishable case -
a read error raised MID-table, after a good record - is now stated as a limit
rather than claimed as covered.

### A2-F6 - LOW - ambiguous multi-line diagnostics select the PASS arm

**Addressed. The order of operations is the fix.**

What was wrong: `b3_sanitize` folded CR and LF into spaces and the classifier then
matched `*"Permission denied"*` on the result. Two diagnostic lines - one EACCES,
one ENOENT - collapsed into one string, and the first substring match won, so an
AMBIGUOUS observation returned 0 from a function whose stated contract is
fail-closed.

What round 3 does, in this order, on the RAW capture:

1. reject any diagnostic containing CR or LF -> `boundary_diagnostic_multiline`,
   rc 3. One probe of one path yields one line;
2. count errno phrases with a builtin-only literal counter and reject more than
   one -> `boundary_diagnostic_ambiguous`, rc 3. This catches the single-line
   two-class shape that step 1 cannot see;
3. compare the WHOLE remaining string against the exact C-locale GNU coreutils
   diagnostic shapes for THIS path. Not a substring: the message must name the
   path that was probed. Both the `stat` and `statx` spellings are accepted
   because coreutils switched producers; nothing else is.

Anything unrecognised keeps round 2's reason string
`boundary_probe_unclassified` at rc 3, so an existing expectation-table row still
matches. ENOENT remains a FAIL (audit 1 F5/O1) and the EACCES arm remains a PASS,
both unchanged in class; the PASS line's mechanism field is now
`message_lc_all_c_exact_shape`.

`b3_sanitize` is unchanged in behaviour but changed in ROLE: it is an output
filter that bounds what a diagnostic can push into the evidence leaf, and it is no
longer a classifier input. That is stated in its header so a future edit does not
reintroduce the ordering.

The audit's two-line EACCES+ENOENT fixture lands in step 1 and returns rc 3;
driven, with the round-2 rc 0 beside it, in SELF_QA section 5.6.

### A2-F7 - MEDIUM - N1 accounting is still not exact and closure tests lack D026 evidence

**Addressed.** `SELF_QA.md` section 3 states the three counts for round 3, counted
by the audit's own rule (category B is any arm with a stubbed command OR a
repointed path literal), with per-file subtotals and an explicit list of the arms
that were not driven at all. Both mount sections use a fixture in place of
`/proc/self/mounts` and are labelled B, which is the specific misclassification
the audit named.

`SELF_QA.md` section 5 is new: for every audit-2 item 1-6 it records the exact
command, the real RED output from the ROUND-2 code, and the real GREEN output from
the ROUND-3 code, both produced on this host in this round. Section 4 records the
extraction recipe and the preludes, so any reader can rebuild an arm from the
delivered bytes.

### A2-F8 - LOW - round2 contains a fifth, unrequested deliverable

**Addressed.** `round3/` contains exactly `DESIGN_NOTES.md`, `RP1-B3.sh`,
`RPD-VERIFY.sh` and `SELF_QA.md`. No hidden file, cache or directory was created
by this work, and the directory was verified empty of them after the last write
(SELF_QA section 2).

## 2. The two new preregistered-input families and their provenance contract

Round 3 adds five required inputs across two families. Both exist for the same
reason: a value the host can produce about itself cannot be used to admit the
host.

### Family A - host attestation (RPD-VERIFY)

| Input | Format | Minted by |
|---|---|---|
| `RPD_EXPECT_NS_USER` | the exact `readlink /proc/<pid>/ns/user` token, `user:[<decimal inode>]` | deploy channel, at provisioning time |
| `RPD_EXPECT_NS_MNT` | the exact `readlink /proc/<pid>/ns/mnt` token, `mnt:[<decimal inode>]` | deploy channel, at provisioning time |
| `RPD_EXPECT_ROOTFS_ID` | the exact `stat -c '%d:%i' /` identity, `<decimal dev>:<decimal inode>` | deploy channel, at provisioning time |

**Provenance contract.** The deploy channel mints these three values ON THE HOST,
OUTSIDE any container or chroot, at provisioning time, in the same step that
establishes the host as a deploy target - and carries them into preregistration
like every other value this block is not allowed to derive. Three properties are
required of that step and are the Lead's to enforce, because no code in this block
can check them:

1. it runs in the host's initial user and mount namespaces, on the real root
   filesystem;
2. its output is recorded in preregistration before `RPD-VERIFY` is ever invoked,
   never passed through the same channel that could be compromised at deploy time
   without leaving a preregistration record;
3. the values are re-minted whenever the host is rebooted or re-provisioned.
   Namespace inode numbers and the root-filesystem dev:inode are stable for the
   lifetime of a boot, not across boots. A stale attestation therefore fails
   CLOSED - `namespace_not_attested`, rc 3 - which is the correct behaviour for
   "the host is no longer the host we preregistered", and is why the STOP is
   reasoned rather than silent.

`RPD-VERIFY` never derives, defaults or falls back to any of the three. A missing
value is `input_missing`, rc 3; a malformed value is `input_shape` or
`input_charset`, rc 3, and the rejected value is never printed.

### Family B - service account identity (RP1-B3)

| Input | Format | Minted by |
|---|---|---|
| `B3_SVC_UID` | decimal, nonzero | the provisioning step that CREATES the `mtc-bridge` account |
| `B3_SVC_GID` | decimal, nonzero | the same step |

**Provenance contract.** These are the numeric ids assigned when the service
account is created, recorded at that moment and carried in preregistration. They
are not read back from the host, because `id -u mtc-bridge` consults the same
name-service database that A2-F3's attack controls. Zero is refused as an input,
not merely as an observation: the accepted state has no root-owned `STATE_DIR` or
`LOG_DIR`, so a preregistration that says otherwise is a plumbing error and is
rc 3, not a host FAIL.

Both families follow the rule already stated for `RPD_RELEASE_MANIFEST_SHA256` in
PREREGISTRATION.md sec. 2: an object cannot attest to its own acceptance.

## 3. Where every check of the original block landed

Line numbers are the accepted block `01_RUNKIT/RP1-B3.sh` (117 lines). Unchanged
from round 2 except rows 5, 6 and 14 and the new row 15.

| # | Original check (line) | Landed | One-sentence why |
|---|---|---|---|
| 1 | release tree `0555 root:root` (98) | unprivileged | `/opt` and `/opt/mtc-bridge/releases` are searchable by the route user, so mode and owner are fully evaluable without privilege. |
| 2 | release tree `/222` sweep (99) | unprivileged | The tree is `0555` and world-readable/searchable, so `find` walks it as the route user. |
| 3 | venv tree `0555 root:root` (102) | unprivileged | Same reachability as #1. |
| 4 | venv tree `/222` sweep (103) | unprivileged | Same reachability as #2. |
| 5 | `STATE_DIR` `0750 mtc-bridge:mtc-bridge` (106) | unprivileged, now NUMERIC | `stat` on the directory itself needs only search on `/var/lib`; the comparison is against the preregistered `B3_SVC_UID:B3_SVC_GID`, not against a rendered name (A2-F3). |
| 6 | `LOG_DIR` `0750 mtc-bridge:mtc-bridge` (107) | unprivileged, now NUMERIC | Same as #5, via `/var/log`. |
| 7 | `CONF_DIR` `0750 root:root` (108) | unprivileged | `stat /etc/mtc-bridge` needs only search on `/etc`; that is exactly the asymmetry the accepted block failed to distinguish from entering the directory. |
| 8 | `ENV_FILE` `0600 root:root` (109) | root-side (`RPD-VERIFY`) | Reading the metadata of any name under `/etc/mtc-bridge` requires search on that `0750 root:root` directory, which the unprivileged route user structurally cannot have. |
| 9 | `INSTALL_MANIFEST` `0640 root:root` (110) | root-side (`RPD-VERIFY`) | Same denial as #8; the name cannot even be resolved unprivileged. |
| 10 | `UNIT_FILE` `0644 root:root` (111) | unprivileged | `/usr/local/lib/systemd/system` is world-searchable and the unit fragment is `0644`. |
| 11 | manifest binds `release_sha` + `release_manifest_sha256` (113-114) | root-side (`RPD-VERIFY`) | The predicate must READ a `0640 root:root` file inside the opaque directory; no unprivileged formulation of it exists on this host. |
| 12 | (new, round 1) `CONF_DIR` opaque to the caller | unprivileged only | A demonstrated denial is the strongest honest statement an unprivileged operator can make about that directory, and the claim is meaningless when made as root. |
| 13 | (new, round 2) `CONF_DIR` identity: literal canonical path, no mount boundary | both blocks | Every claim about a directory is a claim about an OBJECT; without these the same predicates can be true of a decoy reached through a symlink or presented by a mount. |
| 14 | (round 2) initial-namespace binding -> (round 3) ATTESTED host binding | root-side only | uid 0, `0:0` and every namespace witness are namespace-local, so the binding cannot be inferred from inside; it is compared against deploy-channel attestation (A2-F2). |
| 15 | (new, round 3) pinned, isolated, env-scrubbed interpreter | root-side only | The binding check runs an interpreter as root; without a pin and a clean environment the check itself is an arbitrary-code surface (A2-F1). |

Checks #1-#7 and #10 keep the accepted predicate strength; #5 and #6 are strictly
stronger than round 2; #8, #9 and #11 keep theirs and are strictly stronger than
round 1. Nothing is relaxed.

## 4. Exact-diff summary, round 2 to round 3

### 4.1 `RP1-B3.sh`

Removed:

```
b3_assert_mode_owner: the `case "$want_own" in *[!0-9:]*)` NAME branch,
                      including the `0:*|*:0` service-account guard        # r2:214-222
b3_assert_no_mount_at_or_under: `while IFS=' ' read -r src tgt rest <&9`   # r2:350
b3_assert_conf_dir_opaque: `b3_sanitize "$out"` BEFORE classification,
                      and the two `case "$safe" in *"..."*` substring arms  # r2:435,439-445
```

Added:

- `B3_COUNT`, `B3_SHAPE`, `B3_EACCES_TEXT`, `B3_ENOENT_TEXT`, `ROOT_OWNER`,
  `SVC_OWNER`;
- `b3_count_substr` (builtin-only literal occurrence counter);
- `b3_classify_boundary_shape` (exact C-locale shape match, `stat` and `statx`);
- the rc-3 input pre-checks and `:?` backstops for `B3_SVC_UID` and `B3_SVC_GID`;
- an `owner_expectation_malformed` STOP in `b3_assert_mode_owner`;
- `owner_name=` on the ownership FAIL reason;
- the six-field record validation, the populated-final-record processing and the
  `records=` field in `b3_assert_no_mount_at_or_under`;
- `boundary_diagnostic_multiline` and `boundary_diagnostic_ambiguous` STOP arms;
- a `B3_SECTION preregistered_inputs` block that echoes the three operator inputs.

Reclassified: nothing. Every reason string that survives keeps its class.

Changed but not weakened: `b3_record_namespaces` now says
`note=host_binding_is_attested_only_in_RPD-VERIFY` instead of
`note=initial_ns_comparison_needs_root`, because the root-side binding is no
longer a pid-1 comparison. The two identities it records are unchanged.

### 4.2 `RPD-VERIFY.sh`

Removed:

```
command -v python3 >/dev/null 2>&1 || rpd_stop "manifest_parser_absent ..."  # r2:387-388
the bare `python3 -c` invocation with inherited env and cwd                  # r2:396
rpd_assert_initial_namespaces: the /proc/1/ns/{user,mnt} readlinks and both
                      `namespace_not_initial` comparisons, and the
                      `bound=initial` evidence token                        # r2:181-190
rpd_assert_no_mount_at_or_under: `while IFS=' ' read -r src tgt rest <&9`    # r2:309
```

Added:

- `ROOTFS`, `PYTHON_BIN`, `ENV_BIN`, `CHILD_PATH`, `CHILD_CWD`, `unset CDPATH`;
- three `input_missing` pre-checks and three `:?` backstops for the attestation
  inputs;
- `rpd_require_ns_token`, `rpd_require_devino`;
- `rpd_assert_attested_namespaces` (uid_map identity kept; three attested
  comparisons added; `bound=attested`);
- `rpd_require_pinned_tool` and its six STOP arms;
- the `env -i` launch with an explicit child environment, `-I -S -E`, and
  `cd -- "$CHILD_CWD"`;
- `parse_constant=constant` plus the `BadConst` class and the
  `non_json_constant` token and its `install_manifest_non_json_constant` STOP;
- the six-field record validation, the populated-final-record processing and the
  `records=` field in `rpd_assert_no_mount_at_or_under`;
- `isolation=pinned_env_i` on the manifest-binding evidence line and
  `host_binding=attested` on the terminal claim line.

Kept unchanged: the rc contract, the `RPD_` prefixes and section cadence, the
root precondition and its numeric identity rationale, `rpd_require_hex` and the
two rc-3 input pre-checks in front of the retained `:?` guards, `rpd_probe_kind`,
`rpd_assert_conf_dir`, `rpd_assert_regular_mode_owner`, the leaf kind taxonomy,
the fstat/O_NOFOLLOW/O_NONBLOCK swap binding, the 4 MiB bound, the duplicate-key
and top-level-object rules, the closed token set and its `[a-z0-9_]` guard, the
two round-1 FAIL strings for an unbound manifest, and the terminal `RPD PASS`.

### 4.3 One defect found by this round's own QA, and fixed

`rpd_require_ns_token` was first written as

```
local name="$1" val="$2" kind="$3" pfx="$kind:[" inner
```

Bash expands every word of a `local` command before it assigns any of them, so
`$kind` was read while still unset and the function aborted under `set -u` with
`kind: unbound variable`, rc 1 - a raw exit with no reason string, which is
exactly the class of failure this block's rc contract bans. It was caught by arm
`I2-G1` (SELF_QA section 5.2), fixed by hoisting `pfx` to its own line, and the
file carries a comment saying why the two lines are not folded together. Every
other `local` declaration in both blocks was audited for the same pattern; there
are none.

## 5. Additions beyond the audit's explicit list

Each is a strengthening, each is reversible, each is called out so an auditor does
not have to discover it.

1. **`ENV_BIN` is pinned and verified, not only `PYTHON_BIN`.** The audit names
   the interpreter. `env` builds the isolated environment, so an `env` resolved
   through an operator PATH would defeat the pin one level up.
2. **The pinned tools' owner and mode are checked** (`0:0`, not group- or
   other-writable). A pinned path anyone can rewrite is not pinned. A live symlink
   is accepted at the pinned path because stock distributions ship
   `/usr/bin/python3` that way; the SYMLINK TARGET is what is stat'ed.
3. **`-S` in addition to `-I -E`.** `-I` blocks `PYTHONPATH`, user site and cwd;
   `-S` additionally prevents `.pth` files in site-packages from executing code at
   startup in a root process. Disclosed first-run risk: a host whose stdlib is
   only reachable through `site` would STOP rather than run - fail-closed, and not
   a shape Debian-family python3 has.
4. **`unset CDPATH`.** With `CDPATH` set, `cd` prints the resolved directory, and
   that would land in the reader's captured stdout and be adjudicated as a token.
5. **Six-field validation of every mount record**, not only of the final one. The
   audit requires the field count to be validated; applying it to every record is
   the same code and turns a silently unmatched malformed line into a STOP.
6. **`records=<n>` on both mount success lines.** A "no mount boundary" claim now
   carries how many records were actually examined.
7. **`owner_expectation_malformed`** in `b3_assert_mode_owner`. With the name
   branch gone, a caller that passes anything but `<digits>:<digits>` is a coding
   error in the block; it STOPs rather than comparing against something
   unintended.
8. **`owner_name=` appended to the ownership FAIL reason.** The NSS divergence is
   the diagnostic an adjudicator wants, and round 2 printed it only on the
   preceding `B3_stat` line.
9. **A `preregistered_inputs` evidence section in RP1-B3.** Three `B3_input`
   lines, so a reader of the evidence leaf can see which numeric identity the
   ownership admissions were made against. All three values are format-proven
   before they are printed.

## 6. Admission claims after round 3

**`RP1-B3.sh` claims, and claims only:**

> As the unprivileged route identity `uid=<n>` with numeric groups `<list>`,
> inside user namespace `<id>` and mount namespace `<id>`, and for candidate
> `2ce41e34...321b`: the release tree and the venv tree are `0555` owned `0:0`
> with no write bit anywhere in either tree, both sweeps inside the preregistered
> budget; `/var/lib/mtc-bridge` and `/var/log/mtc-bridge` are `0750` owned
> numerically `<B3_SVC_UID>:<B3_SVC_GID>` as preregistered; `/etc/mtc-bridge` is
> `0750` owned `0:0`, is the literal canonical path, and the mount table read in
> full and well-formed shows no mount target at or under it; the unit fragment is
> `0644` owned `0:0`; this caller is not in `/etc/mtc-bridge`'s group, the kernel
> denies it search and read on that directory, and two distinct names under it
> were refused with a single unambiguous C-locale EACCES diagnostic each.

It explicitly does NOT claim: that `/etc/mtc-bridge/mtc-bridge.env` exists, that
it is spelled that way, that its mode is `0600`, that the install manifest exists,
or that any binding holds. Those three are named in the evidence as
`B3_deferred ... to=RPD-VERIFY`. It does not claim that the directory is opaque to
anyone other than this caller, and it does not claim to be in any particular
namespace - it records the two it observed.

**`RPD-VERIFY.sh` claims, and claims only:**

> As `uid=0` at deploy time, in the user and mount namespaces and on the root
> filesystem that the deploy channel attested for this host, with an identity
> `uid_map`, and with the candidate SHA and the accepted `RELEASE_SHA256SUMS`
> sha256 supplied from preregistration and never derived on the host:
> `/etc/mtc-bridge` is the literal canonical non-symlink directory, `0750`, owned
> `0:0`, with no mount target at or under it in a mount table read in full and
> well-formed; `/etc/mtc-bridge/mtc-bridge.env` is a regular file, `0600`, owned
> `0:0`; `/etc/mtc-bridge/install_manifest.json` is a regular file, `0640`, owned
> `0:0`; and that manifest - read through a pinned, root-owned, isolated
> interpreter launched with a scrubbed environment and a fixed cwd, parsed in full
> as a single JSON object with no duplicate key and no non-JSON constant - binds
> at TOP LEVEL exactly `release_sha` = `<candidate>` and
> `release_manifest_sha256` = `<preregistered>`, verified against the same inode
> that was admitted.

It explicitly does NOT claim anything about the trees, the sweeps, the ancillary
directories, the unit fragment, service state, or the env file's CONTENT - the env
file is never opened.

Together the two blocks reconstitute the accepted block's full admission set.
Neither alone does, and neither pretends to.

## 7. RPD-VERIFY is design-only in this unit

`RPD-VERIFY.sh` is **not executed tonight and has no execution path in this
unit.** There is no runner, no argv entry, no preregistration row and no evidence
leaf for it. It enters the runkit as a frozen, non-executed block exactly like
RP3/RP5: hashed and preregistered as an artifact, never invoked. Its
`[EXECUTABLE PROPOSAL BLOCK]` tag marks the block class, not an authorization to
run. Executing it requires root at install/deploy time through the deploy channel,
which is a separate authority from tonight's staging run.

O7 stands and is reinforced by round 3: the block now depends on
`/proc/self/uid_map`, `/proc/self/ns/*`, `/proc/self/mounts`, `stat -c '%d:%i' /`,
`/usr/bin/env` and `/usr/bin/python3`, and on three attestation inputs that do not
exist yet. Its root PASS path has still never been executed anywhere. An isolated
real-Linux root PASS and failure-path run is mandatory before operational freeze or
deploy use, and the first such run must also confirm that the deploy channel can
mint the attestation triple.

Consequence for the current unit, unchanged: the B3 admission set stays incomplete
until a deploy-time run happens. That is the honest cost of Option 1 and it is not
hidden by anything in these deliverables.

## 8. Preregistration impact (for the re-freeze cycle)

Not applied here - `02_PREREG/PREREGISTRATION.md` is immutable and outside
`round3/`. Recorded so the next preregistration can carry it.

- Section 2: `B3_RELEASE_MANIFEST_SHA256` is no longer consumed by `RP1-B3`. The
  same value (`edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26`)
  becomes `RPD_RELEASE_MANIFEST_SHA256`, consumed by `RPD-VERIFY` at deploy time.
  `RPD_CANDIDATE_SHA` (`2ce41e34bceb599d80af24c5c33d835820ec321b`) is a new named
  input of the same kind. `B3_SWEEP_BUDGET_S` = 120 is unchanged, but its accepted
  rc on absence is 3.
- Section 2, NEW (round 3, A2-F3): `B3_SVC_UID` and `B3_SVC_GID`, decimal and
  nonzero, minted by the step that creates the `mtc-bridge` account. Required
  inputs of `RP1-B3`; absence, non-decimal and zero are three distinct rc-3 STOPs.
- Section 2, NEW (round 3, A2-F2): `RPD_EXPECT_NS_USER`, `RPD_EXPECT_NS_MNT` and
  `RPD_EXPECT_ROOTFS_ID`, minted by the deploy channel at provisioning time under
  the provenance contract in section 2 of this file. They must be re-minted on
  every reboot or re-provisioning; a stale value fails closed at rc 3.
- Section 2, CHANGED: the deploy-time precondition for `RPD-VERIFY` is no longer
  "`python3` is present" but "`/usr/bin/python3` and `/usr/bin/env` exist, are
  executable, are owned `0:0` and are not group- or other-writable". The reason
  string moved from `manifest_parser_absent` to the `manifest_tool_*` family.
- Section 3: both blocks are new artifacts needing new expected hashes; the
  accepted `RP1-B3` hash `f40411b0...` is superseded by
  `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc` if this round
  is accepted, and `RPD-VERIFY` by
  `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c`.
  (ROUND 4: these replace the round-3 values `e561e8b4...97dd` and
  `f4c5d61d...63a2`, which were never preregistered.)
- Section 8: rows #4 and #5 move from B3's expectation table to RPD-VERIFY's.
  B3 gains rows for: "`/etc/mtc-bridge` denies entry to the route user", "the
  kernel denies this caller search on `/etc/mtc-bridge`", "`/etc/mtc-bridge` is
  the literal canonical path with no mount boundary", and "`STATE_DIR`/`LOG_DIR`
  are owned by the preregistered numeric service account".
- Section 8, RECLASSIFICATION (round 2, unchanged):
  `conf_dir_search_permitted_name_absent` is in the FAIL column, not STOP.
- Section 8, NEW (ROUND 4): the STOP reason `mount_table_read_error`, raised by
  both `*_assert_no_mount_at_or_under` when a nonzero `read` populated no field
  and no record had been consumed - a mount source that could not be read at all.
  It is a new expectation-table row in the STOP column for BOTH blocks.
- Section 8, NEW: the STOP reasons `mount_table_unterminated_final_record`,
  `mount_record_malformed`, `boundary_diagnostic_multiline`,
  `boundary_diagnostic_ambiguous`, `namespace_not_attested`,
  `rootfs_not_attested`, `install_manifest_non_json_constant` and the
  `manifest_tool_*` family are new expectation-table rows.
- Section 8, NEW: if the mount topology of `/etc/mtc-bridge` is preregistered,
  both `*_assert_no_mount_at_or_under` predicates should become a comparison
  against it rather than a blanket rejection. That is a preregistration change and
  a code change together, not a relaxation of what is delivered here.
- Section 8 #4's **named risk is not resolved by this repair.** The `bridge.env`
  vs `mtc-bridge.env` naming question is invisible to an EACCES denial, by
  construction. It is answerable only by the root-side block. Any reading of a
  future `B3 PASS` as settling that name is wrong.

## 9. Residuals for the Lead

Stated so the re-audit does not have to find them.

1. **The whole host binding now rests on the deploy channel.** That is the point
   of A2-F2's fix - no in-process predicate can establish it - but it moves the
   trust to a step no code in these blocks can inspect. If the attestation is
   minted from inside the container it is meant to exclude, the check passes and
   proves nothing. The provenance contract in section 2 is the control, and it is
   the Lead's to enforce.
2. **Only the interpreter toolchain is pinned.** `stat`, `readlink`, `id` and
   `find` are still PATH-resolved in both blocks. The deploy channel must supply a
   trusted PATH. Pinning them too would be a larger change than the audit's list
   and would add new STOP arms on hosts where those tools live elsewhere; it is
   named here rather than done silently.
3. **`/usr/bin` and the pinned symlink target are trusted.** The pin checks that
   the target is root-owned and not group/other-writable. It cannot check that
   `/usr/bin` itself is, and a host where `/usr/bin` is writable has already lost.
4. **The per-name EACCES classification is still message-based.** It is now an
   exact whole-string match against two C-locale shapes naming the probed path,
   with CR/LF and multi-class text refused first, so it is far narrower than round
   2 - but a coreutils release that changes the diagnostic wording again will land
   in `boundary_probe_unclassified`, rc 3. Fail-closed, and a real first-run risk.
5. **The boundary claim is caller-specific and point-in-time** (ruling O4,
   accepted). Two names are not a proof over every name under a name-sensitive MAC
   policy, and access(2) answers for this process's real ids only.
6. **`RPD-VERIFY` has never run as root anywhere** (O7), and round 3 added two
   more Linux-only dependencies and three inputs that do not exist yet. Treat the
   first deploy-time run as a first run.
7. **Neither block says anything about processes, services or listeners** (O6),
   and the B3 subcheck never did.
8. **A negative elapsed time** would pass the sweep budget comparison. Inherited
   from the accepted block, unchanged, and only reachable if the monotonic clock
   moves backwards.
9. **Namespace inode numbers are not globally unique across boots.** They identify
   a namespace within a running kernel, which is what the comparison needs, but a
   value carried across a reboot can in principle collide. `RPD_EXPECT_ROOTFS_ID`
   is the independent second factor, and the re-minting requirement in section 2
   is the control. A cryptographic host attestation would remove the residual
   entirely and is out of scope for this repair.

## 10. Round 4 - bounded closure of audit-3 findings 1 and 2

Round 4 is not a repair round. It is the bounded closure of the two REQUIRED
findings that survived audit 3, and it changes nothing else. Audit 3 verified
items 1, 2, 3, 4, 6 and 8 of the final list CLOSED; those closures are carried
forward byte-identical, and the diff below is the whole of what round 4 does.

### 10.1 Closure of audit-3 finding 1 - the mount-reader read-error arm

**What was wrong.** Round 3 fixed the populated unterminated-final-record case
but left the EMPTY nonzero read classified as ordinary end of input. On Linux,
opening a directory for input SUCCEEDS and the first `read` then reports
`read error: Is a directory`, returns nonzero and populates nothing. Both
round-3 loops took the `break`, printed a no-mount admission with `records=0`,
and returned rc 0. That is a false PASS on the exact input final-list item 5
requires to STOP, and audit 3 reproduced it against the delivered round-3
function bodies in both blocks.

**What round 4 does.** One arm is added, identically in
`b3_assert_no_mount_at_or_under` and `rpd_assert_no_mount_at_or_under`. The
discriminator is three conjuncts, all of which the loop already has in hand:

1. the `read` returned NONZERO, and
2. it populated NO field, and
3. NO record had been consumed before it (`records` is 0).

A mount table always has at least one record. A nonzero read at record zero
therefore did not reach the end of a table - it means the source was never read
at all - and that is COULD NOT EVALUATE, not "no mounts found". It STOPs with a
dedicated reason:

```
mount_table_read_error path=<source> records=0 read_rc=<rc> detail=nonzero_read_populated_no_field_and_consumed_no_record
```

rc 3, in both blocks, with the same reason string, because it is the same defect.

**What round 4 deliberately does NOT do.** An empty nonzero read AFTER at least
one record is left exactly as round 3 had it - that is what a well-terminated
table produces and it is the normal exit from the loop. The populated
unterminated-final-record arm, the six-field validation, the malformed-record
STOP, the hit accounting, the `records=` success field and the
`mounts_unreadable` open guard are all untouched. The executable delta is one
`if` nested inside an existing `if`, plus the `exec 9<&-` that every other STOP
path in the function already performs.

**Scope note, stated because it is a behaviour change beyond the literal
finding.** A zero-byte mount source now also STOPs, for the same reason and by
the same conjuncts - `records=0` means the source was never read. Round 3
admitted it at rc 0. This is not a separate fix: it is the same predicate, and
refusing to admit a boundary claim built on a table nobody read is the
fail-closed direction. It is driven as its own arm in SELF_QA section 5.5.1.

**Honest limit, stated rather than implied away.** Bash `read` returns 1 for BOTH
end of input and a read(2) failure, and the `read error:` text goes to the
process's stderr, not to a status a shell can test. A read error raised
MID-table, after at least one well-formed record has been consumed, is therefore
indistinguishable here from a clean EOF and is reported as EOF with the record
count it reached. Closing that case as well would require a non-shell reader in
`RP1-B3.sh`, which would make an interpreter-less host a new B3 STOP - a bigger
trade than this bounded round is authorized to make, and one for the Lead. It is
carried as SELF_QA gap 10 and as residual 10 below.

**Evidence.** Driven RED and GREEN, both blocks, both fixtures, with exact
executable commands and real output: SELF_QA section 5.5.1. RED is ROUND-3 code
returning the false `records=0` rc 0; GREEN is round-4 code returning
`mount_table_read_error` rc 3. The five no-weakening arms (`clean`, `sibling`,
`at`, `under`, `absent`) and the three round-3 closures (`nonl`, `short`, `wide`)
were re-driven against round-4 bytes and are unchanged: SELF_QA 5.5.2 and 5.5.3.

### 10.2 Closure of audit-3 finding 2 - the D026 QA record

**What was wrong.** Round-3 `SELF_QA.md` carried real RED/GREEN output but did
not record an exact executable command for every item 1-6 closure test: item 1's
GREEN commands were prose, item 4 referred to "the section 5.1 manifest arm with
the fixture swapped", item 5 gave the RPD command and described the B3 form as
"differs only", item 6 described its GREEN construction in prose - and the
required read-error arm was not tested at all. Separately, section 6.13 was
headed `(9)` while its own text enumerates 11 arms.

**What round 4 does**, all inside `round4/SELF_QA.md`:

1. Every item 1-6 closure test now records the EXACT command that was executed,
   for RED and for GREEN, with the real output of both. Where a command is
   parameterised, the parameter is named and every value it took is listed; no
   command is described relative to another. The harness definitions (`exfn`,
   `ex1`, `exc`, the six preludes, the pinned-tool stub, the fixture recipes and
   all three producer stubs) are recorded verbatim, so an auditor can rebuild any
   arm from the delivered bytes.
2. The read-error arm of fix 1 is added as section 5.5.1, RED and GREEN, both
   blocks, both fixtures.
3. Section 6.13 is labelled `(11)`, which is what the RPD B subtotal was always
   computed with. Every displayed subcount is reconciled to the totals in
   section 3 in one visible arithmetic block.
4. The counts move from 43 A / 115 B / 3 C to **43 A / 119 B / 3 C**. The delta is
   exactly the four new read-error arms (two fixtures x two blocks); no other arm
   count changed, because no other predicate changed.
5. A new table states, per section, how many arms were re-driven against ROUND-4
   bytes in this round (71) and how many are carried forward from round 3 and are
   NOT claimed as re-run (91) - with section 2.1 of that file showing the whole
   executable delta, which is what makes carrying them forward checkable rather
   than asserted.

### 10.3 What round 4 does not change

- Every predicate other than the two mount readers is byte-identical to round 3.
- The rc contract, the reason-string classes, the evidence line formats, the
  preregistered-input families and their provenance contract, the admission
  claims in section 6, and the residuals in section 9 are unchanged. Section 6's
  wording ("the mount table read in full and well-formed shows no mount target at
  or under it") is unchanged because it was already the claim round 4 now
  actually enforces - round 3 could print it for a table it had not read.
- No new command, producer, redirection, input or output field is introduced. The
  only new value that reaches an evidence line is the `read` builtin's own status
  in the new STOP reason.
- Preregistration impact is one added expectation-table row per block
  (`mount_table_read_error`, STOP) plus the two new artifact hashes. Both are
  recorded in section 8.

### 10.4 Residual added by this round

10. **A mid-table read(2) failure is not detectable from a shell.** Stated in
    full in 10.1. It is the one part of final-list item 5 that no shell
    formulation closes, it is named rather than covered by implication, and it is
    the Lead's decision whether a non-shell mount reader is worth an
    interpreter-less-host STOP in the unprivileged block.
