# DESIGN NOTES - B3-GAP-ENV Option 1 design repair, round 2

Round 1 received REQUEST_CHANGES. This round applies the binding findings of
`audit1/AUDIT1_REPORT.md` (F1-F6, N1) and the rulings O1, O2, O3 and O5, keeps
O4, O6 and O7 as accepted, and weakens nothing that passed round 1.

| File | Role |
|---|---|
| `round2/RP1-B3.sh` | repaired unprivileged block, full file (489 lines) |
| `round2/RPD-VERIFY.sh` | root-side deploy-time verify block, full file (518 lines) |
| `round2/DESIGN_NOTES.md` | this file |
| `round2/SELF_QA.md` | syntax evidence, arm walk with three separate counts, no-content audit |

sha256 as delivered (round 2):

```
88ff0f23851b544e956a013c095b34180c0db04def85f04612b704348a1c2248  RP1-B3.sh
8e6edeeb232f4ed8a728810cfb4b3c5c7a9a21c0549d1d1f5a157e0d678650a9  RPD-VERIFY.sh
```

Nothing outside `round2/` was created, modified or deleted. No remote host was
contacted. `01_RUNKIT/RP0-LIB.sh` is unmodified and was read only.

## 1. How each finding was addressed

### F1 - HIGH - grep can admit the wrong manifest bindings

**Addressed. Mechanism replaced, not patched.** Both `LC_ALL=C grep -qsF`
predicates are gone. `rpd_assert_manifest_binding` now runs a silent structural
verification through `python3 -c` that:

- opens the manifest with `O_NOFOLLOW|O_NONBLOCK`, `fstat`s the OPEN descriptor
  and requires the same kind, mode and numeric ownership this block just
  admitted, then reads the WHOLE file under a 4 MiB bound;
- parses it with `json.loads(..., object_pairs_hook=...)` where the hook raises
  on a duplicate key at any depth, so an ambiguous manifest can never be
  adjudicated as bound;
- requires the top level to be a single JSON object;
- compares each expected value exactly, as a string, against the TOP-LEVEL key
  of that name, so a value that appears only in a nested object is unreachable.

rc mapping: rc 1 for a semantic mismatch (value differs, value is not a string,
or the key is absent at top level); rc 3 for read, parse, structural-ambiguity,
swap-detected or tool failure, INCLUDING `python3` being absent. There is no
grep fallback: a fallback is exactly what the audit refuted, so an interpreter
that is missing is a STOP, never a weaker check.

No manifest content can reach the evidence log. The reader writes one token from
a closed lowercase set, its stderr is discarded so that not even a parser
diagnostic (which can carry a line and column) is logged, and the shell refuses
to print any token outside `[a-z0-9_]` before it appears in a STOP reason.

Verified against the audit's own fixture: the decoy manifest that returned
`GREP_RELEASE_RC=0 GREP_MANIFEST_RC=0` in round 1 now returns
`RPD_FAIL reason=install manifest binds a different release_sha`, rc 1
(SELF_QA.md section 6, arm `BD_mf_decoy`), and the duplicate-key manifest
returns `RPD_STOP reason=install_manifest_ambiguous_duplicate_key`, rc 3.

### F2 - HIGH - RPD-VERIFY follows a symlinked configuration parent

**Addressed.** `rpd_assert_conf_dir` runs BEFORE either leaf is touched and
requires all of:

1. the final component classifies as `dir`, not `link_live` / `link_dangling`
   (local classifier, `stat` without `-L`);
2. `readlink -f` returns the LITERAL canonical path `/etc/mtc-bridge`, which
   proves that no component of the path - not only the last - is a symlink;
3. its own mode is exactly `750` and its ownership is numerically `0:0`.

`rpd_assert_no_mount_at_or_under` adds the mount-boundary predicate the audit
asked for: `/proc/self/mounts` is read and any mount target equal to or under
`/etc/mtc-bridge` is a STOP. Fail-closed in both directions - an unreadable
`/proc/self/mounts` is also a STOP, never "no mounts found". A mount is rc 3 and
not rc 1 because the accepted state records no mount topology, so what would be
admitted is not identified; that is could-not-evaluate, not proven deviance.
If the Lead preregisters the topology, the same predicate becomes a comparison
(see section 7).

The same three parent predicates were added to the unprivileged block as well
(`b3_assert_literal_canonical_dir`, `b3_assert_no_mount_at_or_under`), because
the audit's own point is that a cross-block admission is neither self-contained
nor atomic: each block now establishes the identity of the directory it makes a
claim about, in its own process, at its own time.

### F3 - HIGH - root and root ownership are not securely established

**Addressed in three parts.**

1. *Numeric ownership.* Every root-owned expectation is now spelled `0:0` and
   compared against `stat -c '%u:%g'`. `%U:%G` is still READ and PRINTED, because
   a divergence between the numeric and the rendered form is exactly the evidence
   an adjudicator wants for the NSS scenario, but nothing is decided on it.
2. *Namespace binding (RPD-VERIFY).* `rpd_assert_initial_namespaces` requires
   `/proc/self/uid_map` to be the initial-namespace identity map (exactly one
   line, `0 0 4294967295`) AND `/proc/self/ns/user` plus `/proc/self/ns/mnt` to
   be identical to pid 1's. Unreadable is STOP; each mismatch has its own reason.
   The uid_map predicate is what defeats the rootless case directly: mapping the
   whole uid space onto itself is what the initial user namespace IS, and a
   rootless namespace cannot produce it.
3. *Namespace disclosure (RP1-B3).* The unprivileged block cannot compare against
   pid 1 - reading `/proc/1/ns/*` needs PTRACE_MODE_READ, which an unprivileged
   caller does not have, so a comparison there would STOP on every healthy host.
   It RECORDS its own two namespace identities instead (`B3_namespace ...
   scope=self_only`), so the B3 claim is explicitly a claim made inside named
   namespaces and a later reader can compare it with the deploy-time
   `RPD_namespace` line. Unreadable is STOP, not a silent omission.

Disclosed residual, stated in the file: predicate 2's pid-1 comparison is
against pid 1 AS VISIBLE THERE, so inside a container with its own pid namespace
it can be satisfied without being on the host. The uid_map predicate is what
carries the weight, and a complete binding still belongs in the deploy channel's
attestation, exactly as the audit's minimal fix says.

Also part of F3's family and disclosed rather than hidden: `STATE_DIR` and
`LOG_DIR` are owned by the service account `mtc-bridge`, whose numeric ids are
host-assigned and are NOT preregistered, so those two comparisons remain
name-based. They are hardened by additionally refusing a service account that
resolves to uid 0 or gid 0 - the exact substitution the numeric form would catch
- and both forms are printed so the Lead can preregister the numeric ids in the
next freeze cycle (section 7).

### F4 - MEDIUM - the root-side verifier violates its no-mutation contract

**Addressed. The mutation surface of both blocks is now genuinely none, and both
headers say so with the evidence for it.** Every `mktemp` is gone:

| Round 1 temp-file site | Round 2 |
|---|---|
| `rp0_probe_path` (RP0-LIB:31), reached from `RPD-VERIFY:108,130` | replaced by `rpd_probe_kind`, no temp file |
| `rp0_probe_path`, reached from `RP1-B3:62` (`b3_assert_mode_owner`) | replaced by `b3_probe_kind`, no temp file |
| `RP1-B3:85` (`b3_assert_no_writable_paths`) | stderr captured into a shell variable |
| `RP1-B3:173` (`b3_assert_conf_dir_opaque`) | stderr captured into a shell variable |

The round 2 kickoff authorises this: where a library helper is unsound for these
blocks, a local replacement goes in the block with a comment naming the library
line that is deliberately not used and why. Both files carry that comment,
naming RP0-LIB:29-55 (helper), RP0-LIB:31 (temp file) and RP0-LIB:39 / RP0-LIB:49
(unadjudicated `tr`). The only RP0-LIB helper still called anywhere is
`rp0_monotonic_ms` (RP0-LIB:18-22), which reads `/proc/uptime`, allocates
nothing and runs no `tr`. RPD-VERIFY calls no library helper at all and is now
self-contained.

The local classifiers emit the same six tokens as the library helper
(`absent regular dir link_live link_dangling other`) and keep its rule that a
probe error is never `absent` and a dangling link is never `absent`. They SET a
variable instead of PRINTING their result, because a classifier that prints must
be called in `$( )`, and a STOP raised inside that subshell would be captured
into the caller's variable instead of reaching the evidence leaf.

### F5 - MEDIUM - ENOENT is a known deviation but is classified STOP

**Addressed (with O1).** In `b3_assert_conf_dir_opaque`, an ENOENT-shaped
diagnostic now routes to `b3_fail` with the same dedicated reason string as
round 1, `conf_dir_search_permitted_name_absent`, so an existing expectation-table
row still matches; only its class moved from STOP to FAIL. The audit is right
that ENOENT positively proves the directory search succeeded, which is the same
host-state contradiction a successful `stat` is.

STOP is now reserved for outcomes that do not establish whether entry was
permitted: an unrecognised diagnostic, a non-zero rc with empty stderr, and a
diagnostic that had to be suppressed as non-printable. The four-outcome
discipline is stated in the function header.

### F6 - MEDIUM - a documented raw exit violates the 0/1/3 contract

**Addressed (with O5), twice over.**

1. *The `tr` is gone.* Diagnostic sanitization is now `b3_sanitize` /
   `rpd_sanitize`: parameter expansion only, no external tool, no subshell, and
   therefore no tool status that can escape while a reason string is being
   composed. It normalises CR and LF to spaces, suppresses a diagnostic
   containing any non-printable byte to a fixed marker, and caps the result at
   400 bytes. Classification happens on the SANITIZED text, so a suppressed
   diagnostic lands in a STOP arm rather than being pattern-matched - fail-closed
   (driven: arm `O6`).
2. *Every capture is adjudicated at its call site,* and an `ERR` trap is
   installed in both blocks as a backstop: anything still unadjudicated prints
   `..._STOP reason=unadjudicated_command_status rc=<n> line=<n> cmd=[...]` and
   exits 3. No raw tool status can be this block's exit code any more, so rc 1
   can no longer be produced by a missing or failing tool and misread as a
   host-state FAIL. Driven for real (arms `T1`).

### N1 - NIT - SELF_QA overstates how many arms it drove

**Addressed.** `SELF_QA.md` section 3 reports three separate exact counts -
delivered-code arms run with no stubbed command, delivered-code arms run with at
least one stub, and inherited arms NOT re-run - and the third category is
explicitly not called driven. Every arm row carries its category, and the two
QA-environment substitutions (a fixture path in place of a kernel path literal;
QA-host file metadata in place of `0640 0:0`) are named where they were used.

### Open items O1-O7

| Item | Ruling | Round 2 |
|---|---|---|
| O1 | must change | ENOENT is now `b3_fail`, reason string unchanged. |
| O2 | must change | Both blocks emit a reasoned rc-3 STOP for a missing preregistered input. `RP1-B3` gained the pre-check for `B3_SWEEP_BUDGET_S` (plus digits-only and positive-integer guards); the accepted `:?` form is retained behind it as a fail-closed backstop. |
| O3 | must change | No temp file anywhere in either block; both headers state the mutation surface as none and name what was removed. |
| O4 | accept as-is | Kept. The blocks classify the observed access result and never diagnose whether ACL, MAC or capability caused it; the scope limitation is restated in `b3_assert_conf_dir_search_denied` and `b3_assert_conf_dir_opaque`. |
| O5 | must change | Every sanitization step is builtin-only and adjudicated; the ERR trap backstops the rest. |
| O6 | accept as-is | Kept. Neither block says anything about processes, services or listeners. |
| O7 | accept as-is | Kept and re-stated in section 6: an isolated real-Linux root PASS and failure-path run is mandatory before operational freeze or deploy use. `RPD-VERIFY` has still never run as root anywhere. |

### Errno discipline (audit section 2, kickoff item 9)

The PASS decision of the boundary section no longer rests on prose. `[ -x ]` and
`[ -r ]` are shell builtins over access(2): the kernel answers the permission
question itself, for this caller, including POSIX ACLs, capabilities and LSM
policy, and no diagnostic string is involved. Either being true is a FAIL, since
the directory is demonstrably more open to this caller than the accepted state
says.

The two per-name `stat` probes that corroborate it are still classified from the
diagnostic text, because GNU coreutils returns rc 1 for every `stat` error and
exposes no errno to a shell caller. The header says so explicitly and says why
it is acceptable here: `LC_ALL=C` is exported for the whole block AND pinned on
every producer; an unrecognised message is a STOP, never a PASS; and the PASS arm
additionally requires the access(2) predicate to have DENIED search, so a
manufactured "Permission denied" string on its own cannot manufacture a pass.

A block that classified the errno itself would need a non-shell reader.
RPD-VERIFY takes that dependency because its binding check needs a parser
anyway; RP1-B3 does not, and adding one there would convert an interpreter-less
host into a brand-new B3 STOP on a path the accepted block completed. That
trade-off is a deliberate choice, not an oversight.

## 2. Where every check of the original block landed

Line numbers are the accepted block `01_RUNKIT/RP1-B3.sh` (117 lines).

| # | Original check (line) | Landed | One-sentence why |
|---|---|---|---|
| 1 | release tree `0555 root:root` (98) | unprivileged | `/opt` and `/opt/mtc-bridge/releases` are searchable by the route user, so mode and owner are fully evaluable without privilege. |
| 2 | release tree `/222` sweep (99) | unprivileged | The tree is `0555` and world-readable/searchable, so `find` walks it as the route user; the STOP that occurred was never in this section. |
| 3 | venv tree `0555 root:root` (102) | unprivileged | Same reachability as #1. |
| 4 | venv tree `/222` sweep (103) | unprivileged | Same reachability as #2. |
| 5 | `STATE_DIR` `0750 mtc-bridge:mtc-bridge` (106) | unprivileged | `stat` on the directory itself needs only search on `/var/lib`, which the route user has; the block never enters it. |
| 6 | `LOG_DIR` `0750 mtc-bridge:mtc-bridge` (107) | unprivileged | Same as #5, via `/var/log`. |
| 7 | `CONF_DIR` `0750 root:root` (108) | unprivileged | `stat /etc/mtc-bridge` needs only search on `/etc`; that is exactly the asymmetry the accepted block failed to distinguish from entering the directory. |
| 8 | `ENV_FILE` `0600 root:root` (109) | root-side (`RPD-VERIFY`) | Reading the metadata of any name under `/etc/mtc-bridge` requires search on that `0750 root:root` directory, which the unprivileged route user structurally cannot have. |
| 9 | `INSTALL_MANIFEST` `0640 root:root` (110) | root-side (`RPD-VERIFY`) | Same denial as #8; the name cannot even be resolved unprivileged. |
| 10 | `UNIT_FILE` `0644 root:root` (111) | unprivileged | `/usr/local/lib/systemd/system` is world-searchable and the unit fragment is `0644`, so mode and owner are evaluable unprivileged. |
| 11 | manifest binds `release_sha` + `release_manifest_sha256` (113-114) | root-side (`RPD-VERIFY`) | The predicate must READ a `0640 root:root` file inside the opaque directory; no unprivileged formulation of it exists on this host. |
| 12 | (new) `CONF_DIR` opaque to the caller | unprivileged only | A demonstrated denial is the strongest honest statement an unprivileged operator can make about that directory, and the claim is meaningless when made as root. |
| 13 | (new, round 2) `CONF_DIR` identity: literal canonical path, no mount boundary | both blocks | Every claim about a directory is a claim about an OBJECT; without these the same predicates can be true of a decoy reached through a symlink or presented by a mount (F2). |
| 14 | (new, round 2) initial-namespace binding | root-side only | uid 0 and `0:0` are namespace-local; only the root-side block can read `/proc/1/ns/*`, so only it can bind them (F3). |

Checks #1-#7 and #10 keep the accepted predicate strength; #8, #9 and #11 keep
theirs and are strictly stronger in round 2 (numeric ownership, parent identity,
structural binding). Nothing is relaxed.

## 3. Exact-diff summary

### 3.1 `RP1-B3.sh`: round 1 to round 2

Removed:

```
errf="$(mktemp)" || b3_stop "sweep_tempfile_failed root=$root"          # r1:85
detail=$(tr -d '\r\n' <"$errf")   inside writable_inventory_failed      # r1:90
rm -f "$errf"                                                          # r1:92
errf="$(mktemp)" || b3_stop "boundary_tempfile_failed path=$p"         # r1:173
detail="$(tr -d '\r\n' <"$errf")" ; rm -f "$errf"                      # r1:175-176
kind="$(rp0_probe_path "$p")" || exit 3                                # r1:62
command -v rp0_probe_path ... || b3_stop "rp0_lib_not_sourced ..."     # r1:54
```

Reclassified: the ENOENT arm of `b3_assert_conf_dir_opaque` moved from
`b3_stop` to `b3_fail` (F5/O1); the reason string is byte-identical.

Added: `b3_on_err` + `trap ... ERR`; `b3_sanitize`; `b3_probe_kind`;
`b3_record_namespaces`; `b3_assert_literal_canonical_dir`;
`b3_assert_no_mount_at_or_under`; `b3_assert_conf_dir_search_denied`; the rc-3
input pre-checks for `B3_SWEEP_BUDGET_S`; `export LC_ALL=C`; the `MOUNTS`
constant; numeric owner expectations (`0:0`) at four call sites; the
non-root-service-account guard on the two name-based call sites; the
`writable_inventory_unparsable` arm; the monotonic-clock numeric guard.

Two predicates that round 1 kept byte-identical to the accepted block are no
longer byte-identical, deliberately:

- `b3_assert_mode_owner` - the `rp0_probe_path` call became `b3_probe_kind`
  (F4/O3) and the owner comparison became numeric (F3). The kind taxonomy, the
  accepted-kind set, the exact-mode comparison and every FAIL string are
  unchanged.
- `b3_assert_no_writable_paths` - the `mktemp`/`tr` pair became a variable
  capture (F4/O3, F6/O5). The predicate line
  `find "$root" ! -type l -perm /222 -print -quit` is untouched, as are the
  budget STOP and the offender FAIL.

Two honest consequences of that second change, stated rather than hidden:
on the STOP path stdout and stderr are merged into one `detail` field where
round 1 had `detail=` and `partial=[]` separately (diagnostic text only, no
predicate reads it); and because `-print -quit` emits at most one path, an rc-0
capture that is neither empty nor a path under `root` is now a STOP instead of
being read as an offender. Round 1 discarded rc-0 stderr unread, so the change
can only add an observation, never remove one.

### 3.2 `RPD-VERIFY.sh`: round 1 to round 2

Removed:

```
command -v rp0_probe_path ... || rpd_stop "rp0_lib_not_sourced ..."    # r1:58
kind="$(rp0_probe_path "$p")" || exit 3                                # r1:108,130
LC_ALL=C grep -qsF -- "\"release_sha\": \"$release_sha\"" "$manifest"  # r1:132
LC_ALL=C grep -qsF -- "\"release_manifest_sha256\": ..." "$manifest"   # r1:139
own="$(LC_ALL=C stat -c '%U:%G' ...)" used as the owner PREDICATE      # r1:117,120
```

Added: `rpd_on_err` + `trap ... ERR`; `rpd_sanitize`; `rpd_probe_kind`;
`rpd_assert_initial_namespaces`; `rpd_assert_conf_dir`;
`rpd_assert_no_mount_at_or_under`; the structural `python3` reader inside
`rpd_assert_manifest_binding` with its closed token set and its 13-way
adjudication; `export LC_ALL=C`; the `CONF_DIR`, mode, `ROOT_OWNER`, `MOUNTS`
and `MANIFEST_MAX_BYTES` constants.

Kept unchanged: the rc contract, the `RPD_` prefixes and section cadence, the
root precondition and its numeric identity rationale, `rpd_require_hex` and its
two rc-3 input pre-checks in front of the retained `:?` guards, the leaf kind
taxonomy (`dir` is not an accepted kind for a file), the terminal `RPD PASS`,
and the two round-1 FAIL strings for an unbound manifest.

`grep` no longer appears anywhere in either block, in code or in comments,
except in this file and in SELF_QA.md.

## 4. Additions beyond the audit's explicit list

Each is a strengthening, each is reversible, each is called out so an auditor
does not have to discover it.

1. **`export LC_ALL=C` at block scope** (both). The accepted per-command pins are
   kept as well. It makes the `[[:print:]]` class in the sanitizers ASCII and
   removes any locale dependence from a producer that might be added later.
2. **ERR trap backstop** (both). See F6. Reversible: delete two definitions and
   the blocks behave as round 1 did, minus the guarantee.
3. **Parent-identity predicates in the UNPRIVILEGED block** (canonical path,
   mount boundary). F2 was raised against the root-side block only; the audit's
   own reasoning about self-containment applies to both.
4. **access(2) predicate** `b3_assert_conf_dir_search_denied`. See the errno
   discipline note. It converts the strongest single statement in the block from
   a message match into a kernel permission decision.
5. **fstat binding inside the manifest reader.** The reader re-checks kind, mode
   and numeric owner on the OPEN descriptor and opens with `O_NOFOLLOW` and
   `O_NONBLOCK`. Without it the window between the shell `stat` and the read is a
   swap window, and a fifo swapped onto the path could hang a deploy-time
   verifier. Distinct STOP reasons name the swap
   (`..._changed_between_stat_and_read`).
6. **4 MiB read bound** on the manifest. A root-side reader that pulls an
   arbitrary number of bytes into memory because a file was renamed onto that
   path is an availability defect, not a verification. Over the bound is STOP.
7. **`writable_inventory_unparsable` arm** and the **monotonic-clock numeric
   guard** in the sweep. Both are consequences of removing the temp file; both
   are fail-closed and neither can turn a FAIL into a PASS.
8. **Non-root-service-account guard** on the two name-based owner comparisons.
   See F3.
9. **Digits-only and positive-integer guards** on `B3_SWEEP_BUDGET_S`. A budget
   that is not a number would otherwise fail inside an arithmetic comparison with
   no reason string.

## 5. Admission claims after round 2

**`RP1-B3.sh` claims, and claims only:**

> As the unprivileged route identity `uid=<n>` with numeric groups `<list>`,
> inside user namespace `<id>` and mount namespace `<id>`, and for candidate
> `2ce41e34...321b`: the release tree and the venv tree are `0555` owned `0:0`
> with no write bit anywhere in either tree, both sweeps inside the preregistered
> budget; `/var/lib/mtc-bridge` and `/var/log/mtc-bridge` are `0750`
> `mtc-bridge:mtc-bridge` with a non-root numeric owner; `/etc/mtc-bridge` is
> `0750` owned `0:0`, is the literal canonical path with no mount target at or
> under it, and the unit fragment is `0644` owned `0:0`; this caller is not in
> `/etc/mtc-bridge`'s group, the kernel denies it search and read on that
> directory, and two distinct names under it were refused with EACCES.

It explicitly does NOT claim: that `/etc/mtc-bridge/mtc-bridge.env` exists, that
it is spelled that way, that its mode is `0600`, that the install manifest
exists, or that any binding holds. Those three are named in the evidence as
`B3_deferred ... to=RPD-VERIFY`. It also does not claim that the directory is
opaque to anyone other than this caller.

**`RPD-VERIFY.sh` claims, and claims only:**

> As `uid=0` at deploy time, in the initial user namespace (identity uid_map) and
> in pid 1's user and mount namespaces, with the candidate SHA and the accepted
> `RELEASE_SHA256SUMS` sha256 supplied from preregistration and never derived on
> the host: `/etc/mtc-bridge` is the literal canonical non-symlink directory,
> `0750`, owned `0:0`, with no mount target at or under it;
> `/etc/mtc-bridge/mtc-bridge.env` is a regular file, `0600`, owned `0:0`;
> `/etc/mtc-bridge/install_manifest.json` is a regular file, `0640`, owned `0:0`;
> and that manifest, parsed in full as a single JSON object with no duplicate
> key, binds at TOP LEVEL exactly `release_sha` = `<candidate>` and
> `release_manifest_sha256` = `<preregistered>`, verified against the same inode
> that was admitted.

It explicitly does NOT claim anything about the trees, the sweeps, the ancillary
directories, the unit fragment, service state, or the env file's CONTENT - the
env file is never opened.

Together the two blocks reconstitute the accepted block's full admission set.
Neither alone does, and neither pretends to.

## 6. RPD-VERIFY is design-only in this unit

`RPD-VERIFY.sh` is **not executed tonight and has no execution path in this
unit.** There is no runner, no argv entry, no preregistration row and no evidence
leaf for it. It enters the runkit as a frozen, non-executed block exactly like
RP3/RP5: hashed and preregistered as an artifact, never invoked. Its
`[EXECUTABLE PROPOSAL BLOCK]` tag marks the block class, not an authorization to
run. Executing it requires root at install/deploy time through the deploy
channel, which is a separate authority from tonight's staging run. Its header
states this in the file itself so the file cannot be separated from the caveat.

O7 stands unchanged and is reinforced by round 2: the block now depends on
`/proc/self/uid_map`, `/proc/1/ns/*`, `/proc/self/mounts` and `python3`, none of
which exist on the QA host, so its root PASS path has still never been executed
anywhere. An isolated real-Linux root PASS and failure-path run is mandatory
before operational freeze or deploy use.

Consequence for the current unit, unchanged: the B3 admission set stays
incomplete until a deploy-time run happens. That is the honest cost of Option 1
and it is not hidden by anything in these deliverables.

## 7. Preregistration impact (for the re-freeze cycle)

Not applied here - `02_PREREG/PREREGISTRATION.md` is immutable and outside
`round2/`. Recorded so the next preregistration can carry it:

- Section 2: `B3_RELEASE_MANIFEST_SHA256` is no longer consumed by `RP1-B3`. The
  same value (`edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26`)
  becomes `RPD_RELEASE_MANIFEST_SHA256`, consumed by `RPD-VERIFY` at deploy time.
  `RPD_CANDIDATE_SHA` (`2ce41e34bceb599d80af24c5c33d835820ec321b`) is a new named
  input of the same kind. `B3_SWEEP_BUDGET_S` = 120 is unchanged, but its
  accepted rc on absence changes from 1 to 3 (O2).
- Section 2, NEW: the numeric uid and gid of the `mtc-bridge` service account
  should be preregistered, so the last two name-based owner comparisons can
  become numeric like the rest (F3).
- Section 2, NEW: `python3` becomes a named deploy-time precondition of
  `RPD-VERIFY`. Its absence is a STOP, not a degraded check.
- Section 3: both blocks are new artifacts needing new expected hashes; the
  accepted `RP1-B3` hash `f40411b0...` is superseded by
  `88ff0f23851b544e956a013c095b34180c0db04def85f04612b704348a1c2248` if this
  round is accepted.
- Section 8: rows #4 and #5 move from B3's expectation table to RPD-VERIFY's.
  B3 gains rows for: "`/etc/mtc-bridge` denies entry to the route user" (first
  divergence `B3_FAIL reason=conf_dir_entry_permitted ...`), "the kernel denies
  this caller search on `/etc/mtc-bridge`" (first divergence
  `B3_FAIL reason=conf_dir_search_permitted ...`), and "`/etc/mtc-bridge` is the
  literal canonical path with no mount boundary".
- Section 8, RECLASSIFICATION: `conf_dir_search_permitted_name_absent` moves from
  the STOP column to the FAIL column (F5/O1). The string is unchanged.
- Section 8, NEW: if the mount topology of `/etc/mtc-bridge` is preregistered,
  `rpd_assert_no_mount_at_or_under` should become a comparison against it rather
  than a blanket rejection. That is a preregistration change and a code change
  together, not a relaxation of what is delivered here.
- Section 8 #4's **named risk is not resolved by this repair.** The `bridge.env`
  vs `mtc-bridge.env` naming question is invisible to an EACCES denial, by
  construction. It is answerable only by the root-side block. Any reading of a
  future `B3 PASS` as settling that name is wrong.

## 8. Residuals for the Lead

Round 1's open items are resolved or accepted per section 1. These are what
remains, stated so the re-audit does not have to find them.

1. **The boundary claim is caller-specific and point-in-time.** Two names are not
   a proof over every name under a name-sensitive MAC policy, and access(2)
   answers for this process's real ids only (O4, accepted). The evidence line
   names the mechanism (`mechanism=access_builtin`, `mechanism=message_lc_all_c`)
   so a later reader cannot promote it to a global statement.
2. **The per-name EACCES classification is still message-based.** Mitigated as
   described under errno discipline, not eliminated. Eliminating it in the
   unprivileged block would require an interpreter dependency that would create a
   new STOP arm on a path the accepted block completed.
3. **The pid-1 namespace comparison can be satisfied inside a container** with
   its own pid namespace. The identity-uid_map predicate is what carries the
   rootless case. A complete binding belongs in the deploy channel's attestation.
4. **Two owner comparisons remain name-based** (`STATE_DIR`, `LOG_DIR`), pending
   preregistration of the service account's numeric ids.
5. **`RPD-VERIFY` has never run as root anywhere** (O7), and round 2 added four
   Linux-only dependencies to it. Treat the first deploy-time run as a first run.
6. **Neither block says anything about processes, services or listeners** (O6),
   and the B3 subcheck never did.
7. **A negative elapsed time** would pass the sweep budget comparison. Inherited
   from the accepted block, unchanged, and only reachable if the monotonic clock
   moves backwards.
