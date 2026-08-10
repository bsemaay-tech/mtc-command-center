# DESIGN DEFECT PATTERNS - 2026-08-10

A reusable catalogue distilled from one night of adversarial audit over two artefacts:
the B3 staging-admission repair (six audit rounds `[AUDIT1]`-`[AUDIT6]`, opened by the
design gap recorded at `[B3-ADJ Design gap B3-GAP-ENV]`) and the WP-I staging-verification
preregistration draft (one audit `[WPI-AUDIT]`). It exists so a designer can check work
against it before writing code, and an auditor can attack work with it.

This document does not re-adjudicate anything. Verdicts, closure statuses and counts are
reproduced as the reports recorded them.

## Sources

1. `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/06_B3_REPAIR/audit1..audit6/AUDITN_REPORT.md`
2. WP-I preregistration draft audit report, dated 2026-08-09.
3. `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/03_TRANSPORT/B3_STOP_ADJUDICATION.md`

## Citation labels

| Label | Source |
|---|---|
| `[AUDIT1 F5]`, `[AUDIT1 N1]`, `[AUDIT1 sec. 2]` | audit1 report, finding id or numbered section |
| `[AUDIT2 A2-F3]`, `[AUDIT2 sec. 1]` | audit2 report |
| `[AUDIT3 finding 1]`, `[AUDIT3 rerun 3]` | audit3 report, findings and the audit-2 fixture reruns |
| `[AUDIT4 finding 1 case 2]`, `[AUDIT4 closure]` | audit4 report |
| `[AUDIT5 finding 1]`, `[AUDIT5 code freeze]` | audit5 report |
| `[AUDIT6 sec. 2]` | audit6 report |
| `[WPI-AUDIT F1]`, `[WPI-AUDIT answer 2]` | WP-I draft audit, required findings and the four answers |
| `[B3-ADJ Classification]` | B3 STOP adjudication |

Verdicts of record: `[AUDIT1] REQUEST_CHANGES`, `[AUDIT2] REQUEST_CHANGES`,
`[AUDIT3] BLOCK`, `[AUDIT4] BLOCK`, `[AUDIT5] BLOCK`, `[AUDIT6] PASS`,
`[WPI-AUDIT] REQUEST_CHANGES`.

**Path normalization (stated once):** where a report recorded a scratch directory under
`/tmp` `[AUDIT2 A2-F1]`, `[AUDIT3 rerun 1]`, that scratch root is rendered here as `<QA>`.
Nothing else in any quoted line is altered - result text, reason tokens, rc values and
diagnostics are verbatim. Reports that already normalized to `<QA>`, `$QA`, `$QAW` or
`$QA_PY` are quoted as they stand `[AUDIT4 closure]`, `[AUDIT5 finding 1]`,
`[AUDIT6 sec. 2]`.

Patterns are ordered by damage caused, most severe first. Each concrete instance has one
primary home; where an instance also illustrates another pattern it is marked as a
cross-reference and is not counted twice.

---

## Pattern 1 - "STOP is not a result"

**The mistake.** A condition under which the check could not be evaluated is emitted as a
host-state verdict (FAIL) `[WPI-AUDIT F1]`, or an evaluable observation of deviant state is
emitted as an inability to evaluate (STOP) `[AUDIT1 F5]`.

**Why it survives casual review.** The three-outcome contract 0/1/3 is written down and
the code does return one of the three, so the shape looks compliant: the ENOENT branch
emitted a legal rc 3 where rc 1 was the truthful value `[AUDIT1 F5]`, and the contract
itself is binding enough that a raw tool exit is a finding against it `[AUDIT1 F6]`.
Reviewers check that every branch produces a legal rc, not that every branch produces the
*truthful* rc - the WP-I repair instruction is "do not classify solely by numeric rc"
`[WPI-AUDIT F3 minimal fix]`. The error paths are also the least-exercised paths, so the
mapping is rarely seen running; in this cycle the mid-read error arm "was not driven at
all" `[AUDIT3 finding 1]`.

**Concrete instances.**

1. ENOENT at the boundary probe classified STOP, when it positively proves directory
   search succeeded and observes a missing preregistered path. "That result positively
   proves that directory search succeeded and also observes a missing preregistered path;
   it is not an inability to evaluate. The delivered code emits rc 3 instead of a
   deviant-state rc 1." `[AUDIT1 F5]`, restated as a must-change at `[AUDIT1 O1]`.
2. Unreadable distribution metadata becomes a package-parity FAIL: a generic nonzero
   verifier rc maps to `B1_FAIL reason=lock_installed_parity`, so "the draft therefore can
   report package drift when the unprivileged process merely could not evaluate the
   package set" `[WPI-AUDIT F1]`.
3. System-manager access failure becomes host drift: a denied system bus, absent
   `systemctl`, or an isolated PID/mount namespace makes the query fail before returning
   unit state, and only `B2_FAIL`/`B4_FAIL` divergences are provided `[WPI-AUDIT F3]`.
4. An unadjudicated tool status escapes as a raw exit: "Rc 1 can then be misread as a
   host-state FAIL even though the probe result was not classified" `[AUDIT1 F6]`.

The correct handling is on record too: an operator-side rc 3 was adjudicated as
could-not-evaluate rather than FAIL, on the ground that no probe which ran found deviant
host state and that checks #1 through #3 - release tree, venv tree, write-bit sweeps - all
held `[B3-ADJ Classification]`; the named naming risk was recorded as unresolved rather
than triggered `[B3-ADJ Classification]`.

**The falsification.** A host where the preregistered leaf is absent but its parent is
searchable. Round 1 produced `[AUDIT1 sec. 4]`:

```
B3_STOP reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES
```

at rc 3. After repair the same fixture produced `[AUDIT2 sec. 1, F5 CLOSED]`:

```
B3_FAIL reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES
```

at rc 1.

**The rule.** Before writing a branch, write the sentence it emits and ask which of three
things the branch witnessed: deviant state observed (FAIL), expected state observed
(PASS), or the observation itself did not happen (STOP). Enumerate every error class the
probe can raise and assign it a class in the design, not in the code. A blanket "any other
error is STOP" is a design defect: `[AUDIT1 F5]` records that "The kickoff's blanket 'any
other error class is STOP' must be narrowed accordingly."

---

## Pattern 2 - "Whose kernel answered?"

**The mistake.** The probe runs in a user, mount, PID or network namespace - or at a
privilege level - different from the domain the admission claim is about, and the answer
is read as if it came from the claimed domain `[AUDIT1 F3 scenario 2]`, `[AUDIT2 A2-F2]`,
`[WPI-AUDIT F2]`.

**Why it survives casual review.** The probe genuinely succeeds and prints a plausible,
correct-looking value. `id -u` really does print 0 and the files really can appear as
namespace `root:root` `[AUDIT1 F3 scenario 2]`; `ss` really does list listeners, succeeding
"without a permission error" while seeing only the login namespace `[WPI-AUDIT F2]`.
Nothing errors, so nothing draws attention - inside the container "All delivered checks
pass" `[AUDIT2 A2-F2]`. The claim sentence names a host; the observation names a namespace,
and no line of code marks the difference.

**Concrete instances.**

1. Rootless user namespace: "a rootless user namespace maps host UID 1000 to namespace UID
   0 and exposes operator-controlled files through its mount namespace. `id -u` prints 0,
   those files can appear as namespace `root:root`, and the block can PASS without
   host-root authority" `[AUDIT1 F3 scenario 2]`. The audit adds: "`id -u = 0` alone
   proves only namespace-local identity."
2. Container/chroot defeating the namespace binding: with an identity uid map and its own
   PID namespace, "All delivered checks pass even though `/etc/mtc-bridge` is the
   container's filesystem, not the host object the admission claim names," and a chroot in
   the same user and mount namespaces "similarly changes what literal `/etc` resolves to
   without changing either namespace link" `[AUDIT2 A2-F2]`.
3. Probe outside the service network namespace: "PAM, an ssh ForceCommand, or a service
   wrapper places the `gatea` login in a private network namespace while PID 1 and the
   bridge remain in the host namespace," which can produce a false FAIL, and "Conversely, a
   matching listener in the login namespace could conceal a bad listener set in the service
   namespace and create a false PASS" `[WPI-AUDIT F2]`.
4. Privilege domain: the accepted block "assumes the operator can `stat` root-protected
   paths under `/etc/mtc-bridge/`," while the accepted execution model is unprivileged with
   no sudo - the adjudication records the two checks as structurally impossible for an
   unprivileged operator on this host, not merely inconvenient `[B3-ADJ Design gap
   B3-GAP-ENV]`.

**The falsification.** Two host states. First, run the block as the unprivileged login user
against a `root:root` mode `750` directory; the recorded output was `[B3-ADJ Finding]`:

```
RP0_STOP reason=path_probe_error path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot statx '/etc/mtc-bridge/mtc-bridge.env': Permission denied
```

Second, run the namespace binding inside a rootful container with an identity uid map. The
delivered function reported `[AUDIT2 A2-F2]`:

```
RPD_namespace user=user:[4026531837] mnt=mnt:[4026532220] bound=initial uid_map=identity
RC=0
```

and the audit's judgement was that this "proves equality only with PID 1 visible in the
current PID namespace; it does not prove the printed mount namespace is the host's initial
namespace." The repair route was external attestation, closed in round 3: the verifier
"requires, validates, and compares all three deploy-channel attestation values. An actual
matching Linux run printed `bound=attested` and rc 0 ... No local `bound=initial` inference
remains" `[AUDIT3 item 2 CLOSED]`.

**The rule.** For every claim, name its domain (which host, which namespace set, which
privilege) in the same sentence as the predicate, then require that the domain be
established by something the probe cannot forge from inside itself - a deploy-channel
attestation, or execution through a channel already bound to that domain `[AUDIT2 A2-F2
minimal fix]`, `[WPI-AUDIT F2 minimal fix]`. If the execution model cannot reach the
domain, the design is wrong, not the run `[B3-ADJ Design gap B3-GAP-ENV]`.

---

## Pattern 3 - "The leaf is not the path"

**The mistake.** The final component is checked - kind, mode, owner - while the chain that
reaches it (intermediate symlinks, non-canonical components, mounts) is left unverified
`[AUDIT1 F2]`, `[AUDIT1 sec. 2]`.

**Why it survives casual review.** The leaf checks are visibly strict and often numerically
exact - "Exact mode comparison is sound for the observed leaf at that instant" - and an
`lstat` on the leaf is genuinely symlink-safe *for the leaf*, because the leaf-kind checks
"correctly reject final-component live and dangling symlinks, directories, and other object
kinds" `[AUDIT1 sec. 3]`. The reviewer sees "we reject symlinks" and stops. A second,
unprivileged block elsewhere may reject the parent, which makes the gap look covered even
though the two checks run at different times
`[AUDIT1 F2]`.

**Concrete instances.**

1. Symlinked configuration parent: "make `/etc/mtc-bridge` a symlink to a decoy directory
   containing regular files with the requested leaf modes, owner names, and grep strings.
   The leaf `lstat` sees regular files because the intermediate symlink is followed; both
   metadata checks and both binding checks can PASS." The separate unprivileged rejection
   "runs at a different time, so the root-side admission is neither self-contained nor
   atomic with that check" `[AUDIT1 F2]`.
2. Mount over the directory: "A mount over `/etc/mtc-bridge` can present mode 0750
   root:root and EACCES for both names, so B3 PASSes ... If it identifies the original
   backing filesystem object, this is a false pass because no mount check exists"
   `[AUDIT1 sec. 2]`; the same audit notes "path canonicalization alone does not detect a
   mount over the directory" `[AUDIT1 F2 minimal fix]`.
3. Inaccessible lower parent in the WP-I draft: hashing can fail because "a parent below
   the recorded `0555` release root, has a named ACL denying `gatea`" `[WPI-AUDIT F5]`, and
   traversal can be defeated by "an inaccessible nested mount ... even when the root
   reports `0555`" `[WPI-AUDIT answer 1, B3 INCLUDE half]`.

**The falsification.** Build the parent as a live symlink to a decoy directory holding
correctly-moded, correctly-owned leaves. Round 1, against real root-owned leaves reached
through the symlink `[AUDIT2 sec. 1, rerun 2]`:

```
RPD_stat path=<QA>/r1-link/mtc-bridge.env owner=root:root mode=600
RPD_stat path=<QA>/r1-link/install_manifest.json owner=root:root mode=640
RPD_manifest_binding path=<QA>/r1-link/install_manifest.json bound=both
RC=0
```

Round 2, same fixture:

```
RPD_FAIL reason=conf_dir_is_symlink kind=link_live path=<QA>/etc-mtc-bridge
RC=1
```

The fixture still failed correctly in round 3: "The symlinked configuration-parent fixture
still returned `conf_dir_is_symlink`, rc 1" `[AUDIT3 sec. 2]`.

**The rule.** Verify the container before the contents: require the parent itself to be a
non-symlink directory at the literal canonical path, with its own expected numeric mode and
ownership, before touching any leaf, and add an explicit mount-boundary predicate if the
accepted state includes the backing object `[AUDIT1 F2 minimal fix]`. Keep parent and leaf
checks in the same block so they are atomic, not split across blocks that run at different
times `[AUDIT1 F2]`.

---

## Pattern 4 - "The privileged child brought its own environment"

**The mistake.** A verifier running with root authority launches an interpreter or helper
that inherits operator- or attacker-influenced environment, PATH, working directory or
TMPDIR `[AUDIT2 A2-F1]`, `[AUDIT1 F4]`.

**Why it survives casual review.** The launch line looks like ordinary tooling - `python3
-c ...` `[AUDIT2 A2-F1]`, a temp file `[AUDIT1 F4]`, a helper binary. The security reasoning
is spent on the *predicate* the child computes, and the channel that decides which code the
child actually runs is invisible in the diff: the round-2 self-QA "missed all of A2-F1
through A2-F6" `[AUDIT2 sec. 4]`.

**Concrete instances.**

1. Module hijack of the root-side JSON parser: "invoke the verifier with PYTHONPATH naming
   an attacker-controlled directory that contains `json.py`. The delivered `python3 -c`
   command does not use isolated mode, does not remove Python environment variables, and
   does not pin a trusted interpreter ... Import-time code also runs with the verifier's
   root authority, contradicting `mutation=none`" `[AUDIT2 A2-F1]`. A current-directory
   shadow reaches the same child `[AUDIT3 item 1]`.
2. Attacker-controlled TMPDIR inside the protected directory: "every call to
   `rp0_probe_path` creates and removes a temporary file. With `TMPDIR=/etc/mtc-bridge`, a
   root execution creates that file inside the protected directory; interruption can leave
   it behind" `[AUDIT1 F4]`; the open item restates it as "New root-side and boundary code
   cannot claim no mutation while creating temp files, especially with attacker-controlled
   TMPDIR" `[AUDIT1 O3]`.
3. Interpreter resolution through operator-controlled PATH, named as part of the same
   defect: "Do not resolve `python3` from an operator-controlled PATH" `[AUDIT2 A2-F1
   minimal fix]`.

**The falsification.** A `PYTHONPATH` directory containing a `json.py` shadow, over a
manifest whose entire content is `THIS IS NOT JSON AND BINDS NOTHING`. The delivered
function returned `[AUDIT2 A2-F1]`:

```
RPD_manifest_binding path=<QA>/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

After pinning and isolation the same fixture returned `[AUDIT3 rerun 1]`:

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=/usr/bin/python3 mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_unparsable path=<QA>/wrong.json
RC=3
```

and "The cwd-shadow variant independently produced the same STOP and rc 3" `[AUDIT3 rerun
1]`.

**The rule.** Treat every child process of a privileged verifier as part of the trusted
computing base: pin the absolute interpreter and helper paths, verify their kind, mode and
numeric ownership, launch with a cleared environment and isolated mode from a fixed working
directory, and require the deploy channel to supply that clean environment `[AUDIT2 A2-F1
minimal fix]`, `[AUDIT3 item 1 CLOSED]`. Write the module-hijack regression at design time,
not after the audit.

---

## Pattern 5 - "grep is not a parser"

**The mistake.** A structured or grammatical input (JSON, an errno diagnostic, a table) is
adjudicated with substring or fixed-string matching `[AUDIT1 F1]`, `[AUDIT1 sec. 2]`,
`[AUDIT2 A2-F6]`.

**Why it survives casual review.** The match is real and the happy path is convincing: the
expected string is present and the search returns 0 - both `grep -qsF` predicates returned
0 on the decoy `[AUDIT1 F1]` - and hardened input filters (charset, length) make the code
look defensive. The filters block injection into the matcher; they do not give the matcher
a grammar - they "do not repair grep's lack of JSON structure" `[AUDIT1 sec. 3]`.

**Concrete instances.**

1. Fixed-string manifest binding: "Both delivered `grep -qsF` predicates return 0 ...
   Duplicated top-level keys produce the same false pass when an accepted value appears
   before the effective later value. The fixed-string search also accepts the strings in any
   object and does not establish that the file is valid JSON" `[AUDIT1 F1]`. The audit adds
   that the hex and length guards "correctly block newline, CR, quote, and multi-pattern
   injection into grep. They do not repair grep's lack of JSON structure" `[AUDIT1 sec. 3]`.
2. Substring matching an errno: "Matching the substring `Permission denied` is still not an
   errno check: a wrapper or mixed diagnostic containing that text can manufacture a pass. A
   reliable implementation should classify the actual EACCES errno, not prose" `[AUDIT1
   sec. 2]`.
3. First-substring-wins on a multi-line diagnostic: two lines, one EACCES and one ENOENT,
   at rc 1 - "`b3_sanitize` replaces the newline with a space and the case statement selects
   the first substring, so an ambiguous diagnostic is called EACCES and returns 0 rather
   than STOP" `[AUDIT2 A2-F6]`.

**The falsification.** Valid JSON whose preregistered values sit only in a nested decoy
while both top-level values are wrong. Reproduced output `[AUDIT1 F1]`:

```
GREP_RELEASE_RC=0
GREP_MANIFEST_RC=0
TOP_RELEASE=0000000000000000000000000000000000000000
TOP_MANIFEST=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Round 2 turned that fixture red-to-green: `RPD_FAIL reason=install manifest binds a
different release_sha`, `RC=1` `[AUDIT2 sec. 1, rerun 1]`. For the diagnostic variant, the
ambiguous two-line fixture returned `[AUDIT2 A2-F6]`:

```
B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1 mechanism=message_lc_all_c
RC=0
```

and after repair `[AUDIT3 rerun 4]`:

```
B3_STOP reason=boundary_diagnostic_multiline path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': Permission denied stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': No such file or directory
RC=3
```

**The rule.** Match the adjudicator to the grammar of the data before writing the check: if
the input has structure, parse it whole, reject duplicate keys, require the expected
top-level shape, and compare exact values `[AUDIT1 F1 minimal fix]`; if the input is an
errno, classify the errno; if a matcher cannot prove the stated binding, the *brief* must
change, not just the code - "This requires changing the binding brief; grep cannot prove
the stated JSON binding" `[AUDIT1 F1]`. Reject CR, LF and multi-class text before matching,
and keep ambiguous text at rc 3 `[AUDIT2 A2-F6 minimal fix]`.

---

## Pattern 6 - "Read the status before the stdout"

**The mistake.** A tool's output is interpreted before its exit status, stderr and
completeness have been adjudicated, so partial or failed work is read as a finished
observation `[WPI-AUDIT F4]`, `[AUDIT1 F6]`.

**Why it survives casual review.** stdout looks like a result: `find` "emits the writable
pathname, then emits EACCES and exits nonzero" `[WPI-AUDIT F4]`. Under `set -e` or a
pipeline the failure appears to be handled by the shell, and the tool prints something
plausible even when it stopped early, while an unadjudicated helper status escapes as a raw
exit that carries no reason `[AUDIT1 F6]`. The ordering defect is
invisible in a table of expected divergences because both rows exist - only their
precedence is wrong `[WPI-AUDIT answer 2]`.

**Concrete instances.**

1. Partial `find` output consumed before the walk error: a writable path is emitted early,
   an ACL-denied directory later makes `find` emit EACCES and exit nonzero, "A wrapper can
   therefore emit `B3_FAIL` for the writable path even though the sweep was incomplete and
   the correct first outcome is `B3_STOP`" `[WPI-AUDIT F4]`; the expectation table is
   affected because "Row 12 can consume partial output before row 14 reports the walk
   error, making the stated FAIL reachable only by violating STOP-first ordering"
   `[WPI-AUDIT answer 2]`.
2. Digest comparison before hash rc and stderr: rows "name only digest-mismatch FAILs as
   the exact predicted first divergence ... it neither gives the exact row-specific
   divergence nor states that rc/stderr is adjudicated before comparing possibly empty
   output" `[WPI-AUDIT F5]`.
3. Unadjudicated sanitizer status: "`tr` is unavailable or fails while reading the boundary
   diagnostic. Under `set -e`, the script exits with the raw tool status, potentially 1,
   126, or 127, and emits no B3 reason" `[AUDIT1 F6]`; the same inherited pattern was
   recorded in two library helper lines.
4. Quiet matching that stops reading: fixed-string search "can also stop reading after a
   quiet match, so a later read problem need not be observed" `[AUDIT1 sec. 3]`.

**The falsification.** Make the tool that produces the diagnostic fail. Round 1's `tr`
falsification "exited silently with rc 7"; the round-2 fixture printed `[AUDIT2 sec. 1, F6
CLOSED]`:

```
B3_STOP reason=unadjudicated_command_status rc=1 line=33 cmd=[false]
```

and returned rc 3. For the walk case the fixture is a tree containing both a
world-writable file early in traversal order and, later, a directory denying the caller
`[WPI-AUDIT F4]`.

**The rule.** Make each probe atomic for adjudication: "capture stdout, stderr, rc, and
elapsed time; first STOP on timeout or any probe/traversal error; only after a complete
rc-0 walk may stdout be inspected" `[WPI-AUDIT F4 minimal fix]`, and state that ordering in
the expectation table and acceptance criteria. Require a successful rc plus a syntactically
valid result before any mismatch may be called FAIL `[WPI-AUDIT F5 minimal fix]`. Every
helper that can fail must have its own status adjudicated into a reasoned STOP `[AUDIT1 F6
minimal fix]`.

---

## Pattern 7 - "Nonzero read is not end of file"

**The mistake.** A loop treats any nonzero read status as clean end-of-data, so truncated
input, an unterminated final record, or a hard read error is admitted as a complete,
clean scan `[AUDIT2 A2-F5]`, `[AUDIT3 finding 1]`.

**Why it survives casual review.** `while read ... ; do ... done < src` is the idiom
everyone writes and it is correct for well-formed input. The loop terminates, the
predicate prints its admission line, rc is 0 `[AUDIT2 A2-F5]`, and the diagnostic that
would betray the error goes to stderr where nobody adjudicates it:
`bash: read: read error: Is a directory` accompanied a clean rc-0 admission
`[AUDIT3 finding 1]`.

**Concrete instances.**

1. Populated final record without a trailing newline: "Bash `read` populates the fields but
   returns nonzero at EOF, so the while body never examines that record. The predicate
   prints no-mount and returns 0" `[AUDIT2 A2-F5]`, in both copies of the reader.
2. Empty nonzero read from a directory source: "opening a directory for input succeeds and
   the first Bash `read` reports `Is a directory`, returns nonzero, and populates no fields.
   Both delivered loops take the `break` ... print a no-mount admission with `records=0`,
   and return 0" `[AUDIT3 finding 1]`. The audit notes this is not new: it is "the
   surviving read-error arm explicitly named by item 5 of the final list."

**The falsification.** Two mount-table fixtures. First, one matching record with no final
newline `[AUDIT2 A2-F5]`:

```
RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=<QA>/mounts-no-final-newline
RC=0
```

closed in round 3 `[AUDIT3 rerun 3]`:

```
RPD_STOP reason=mount_table_unterminated_final_record path=<QA>/nonl records=1 hits=1 first_target=/etc/mtc-bridge
RC=3
```

Second, a directory as the mount source. Round 3 RED and round 4 GREEN, both recorded with
the report's own `<QA>` normalization `[AUDIT3 finding 1]`, `[AUDIT4 closure]`:

```
RPD round 3 RED:
<QA>/arm.sh: line 30: read: 0: read error: Is a directory
RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=<QA>/fix2/mounts/adir records=0
RC=0

RPD round 4 GREEN:
<QA>/arm.sh: line 30: read: 0: read error: Is a directory
RPD_STOP reason=mount_table_read_error path=<QA>/fix2/mounts/adir records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record
RC=3
```

The audit-4 closure confirms the delta "adds the same zero-record, empty-field, nonzero-read
STOP and changes no other executable arm" `[AUDIT4 closure]`.

**The rule.** Design the reader around three exit conditions, not one: clean EOF, EOF with a
populated unconsumed record, and read failure. Process a populated final record even when
`read` returns nonzero, validate that every record has the required fields, and STOP on
malformed, truncated or read-error input `[AUDIT2 A2-F5 minimal fix]`. Apply the repair to
every copy of the reader and test the source that cannot be read, not only the source with
bad content `[AUDIT3 finding 1]`, `[AUDIT4 closure]`.

---

## Pattern 8 - "The name is not the identity"

**The mistake.** An admission compares a rendered, resolver-supplied or inferred label -
user name, group name, a visible PID - instead of the numeric or kernel identity the claim
is about `[AUDIT1 F3 scenario 1]`, `[AUDIT2 A2-F3]`.

**Why it survives casual review.** `root:root` `[AUDIT1 F3 scenario 1]` and
`mtc-bridge:mtc-bridge` `[AUDIT2 A2-F3]` read as identity to a human. The comparison is
exact-string and looks strict, yet it is name-based rather than numeric `[AUDIT1 sec. 3]`,
and the rendering usually is faithful, so every ordinary test passes.

**Concrete instances.**

1. NSS-rendered root: "an NSS database maps a nonzero file UID and GID to the names `root`
   and `root`. GNU `stat -c '%U:%G'` then prints `root:root`, so files not owned by numeric
   0:0 pass" `[AUDIT1 F3 scenario 1]`; the section review restates that owner comparison
   "is name-based rather than numeric and can accept nonzero ownership under unusual NSS
   data" `[AUDIT1 sec. 3]`.
2. Name-mapped service account after the root case was fixed: "the accepted service account
   has preregistered numeric ownership different from 999:999, but NSS renders uid/gid
   999:999 as `mtc-bridge:mtc-bridge`. The round-2 branch compares the rendered name and
   rejects only numeric zero, so the wrong nonzero owner passes" `[AUDIT2 A2-F3]`.

Cross-reference (counted under pattern 2): comparing namespace links against those of the
visible PID 1 is the same substitution applied to kernel namespace identity - it "proves
equality only with PID 1 visible in the current PID namespace" `[AUDIT2 A2-F2]`.

**The falsification.** An object whose numeric ownership differs from its rendered names.
Root case, round 1 then round 2 `[AUDIT2 sec. 1, rerun 3]`:

```
RPD_stat path=/fixture/env owner=root:root mode=600
RC=0

RPD_stat path=/fixture/env owner_numeric=1000:1000 owner_name=root:root mode=600
RPD_FAIL reason=path=/fixture/env owner_numeric=1000:1000 expected=0:0
RC=1
```

Service-account case, round 2 then round 3 `[AUDIT2 A2-F3]`, `[AUDIT3 rerun 5]`:

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
RC=0

B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=999:999 expected=1500:1500 owner_name=mtc-bridge:mtc-bridge
RC=1
```

**The rule.** Preregister numeric identities and compare only those: `stat -c '%u:%g'`
against the preregistered pair, with printed names kept "diagnostic only" `[AUDIT2 A2-F3
minimal fix]`, `[AUDIT3 item 3 CLOSED]`. If a check compares any string a resolver produced,
say in the design which database supplies it and why that database is trusted.

---

## Pattern 9 - "The sentence outruns the probe"

**The mistake.** The claim recorded in the header, the log line or the design note is
broader than what the executed predicate can establish `[AUDIT1 F4]`, `[AUDIT1 sec. 2]`,
`[AUDIT2 A2-F4]`.

**Why it survives casual review.** The code is often correct for the narrow claim - "no
false pass exists under stable, ordinary Unix DAC with trusted GNU tools and the narrow
caller-specific claim" `[AUDIT1 sec. 2]` - and the overclaim lives in prose or in a single
token such as `bound=initial` `[AUDIT2 A2-F2 minimal fix]` or
`parser=python3_json_structural` `[AUDIT2 A2-F4]`. Reviewers read the sentence and the code
separately, and each looks fine on its own.

**Concrete instances.**

1. "No mutation of any kind" while the probe helper writes: "every call to
   `rp0_probe_path` creates and removes a temporary file ... Even with default TMPDIR, the
   statement ... that there is 'no mutation of any kind' is false" `[AUDIT1 F4]`. The audit
   notes the honest alternative is a contract change, not a compliance claim `[AUDIT1 F4
   minimal fix]`.
2. A two-name EACCES observation read as global opacity: "The probe supports only a narrow
   statement: at the two probe instants, this caller received a diagnostic classified as
   EACCES for two names. It does not prove that the directory is globally opaque or that its
   backing object is the accepted one," and under name-sensitive MAC policy "Both probes get
   EACCES while the directory is not actually opaque to the caller" `[AUDIT1 sec. 2]`. The
   conclusion is explicit: no false pass under the narrow claim, "False passes do exist once
   the claim is read globally."
3. `parser=python3_json_structural` over a parser that accepts non-JSON constants:
   "Python's `json.loads` accepts NaN, Infinity and -Infinity by default even though they
   are not JSON values. A manifest with both correct top-level bindings and an additional
   value NaN therefore passes the claim that the whole file is valid structural JSON"
   `[AUDIT2 A2-F4]`.
4. A residual limitation stated more broadly than it is: "The wording says a read error
   raised mid-table is generally indistinguishable. That should be narrowed to a read error
   that populates no field after one or more complete records. A nonzero read that leaves a
   partially populated record is already distinguished by the existing `truncated=1` arm and
   STOPs. This wording overstates the residual; it does not create a false admission or
   weaken the fix" `[AUDIT4 finding 2, OPTIONAL NIT - LOW]`. Closed: "The limitation is
   narrowed to a mid-table read failure that populates no field after at least one complete
   record" `[AUDIT5 nit 2]`, confirmed text-identical at `[AUDIT6 sec. 4]`. An honest
   disclosure can still be inaccurate: a sentence that outruns the probe in the direction of
   understating the fix is the same defect as one that overstates it.

Cross-reference (counted under pattern 2): "Do not label a visible-PID-1 comparison as
`bound=initial`" `[AUDIT2 A2-F2 minimal fix]`.

**The falsification.** A manifest carrying both correct top-level bindings plus a bare
`NaN`. Round 2 `[AUDIT2 A2-F4]`:

```
RPD_manifest_binding path=<QA>/nan.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

Round 3, with a raising `parse_constant` callback `[AUDIT3 rerun 2]`:

```
RPD_STOP reason=install_manifest_non_json_constant path=<QA>/nan.json detail=NaN_Infinity_-Infinity_are_not_JSON_values
RC=3
```

**The rule.** Write the claim sentence first, then delete every word the probe cannot
establish; the surviving sentence is the log line. Scope limitations that remain must be
stated explicitly in the evidence, which is what `[AUDIT1 O4]` accepted: "the block should
classify the observed access result, not diagnose whether ACL, MAC, or capability caused it;
the scope limitation must remain explicit." Naming a mechanism in a token (`parser=`,
`bound=`, `mechanism=`) is a claim and must be earned by the code that emits it.

---

## Pattern 10 - "Evidence that cannot fail"

**The mistake.** Self-produced evidence - arm counts, category labels, prose recipes,
templated command records - is offered as closure although nothing about it could have come
out wrong `[AUDIT1 N1]`, `[AUDIT2 A2-F7]`, `[AUDIT4 finding 1]`.

**Why it survives casual review.** It looks like the most rigorous part of the package:
large tables, exact-looking totals, headings that reconcile - the round-3 three-way totals
did reconcile while one subcount was internally wrong `[AUDIT3 finding 2]`. Reviewers audit
the arithmetic of the claim rather than its falsifiability: most arm tables "state a
scenario and claimed output but do not record the exact executable command and RED output"
`[AUDIT2 A2-F7]`. A count is not a fixture - it has no red state.

**Concrete instances.**

1. Overstated drive count: "line 56 says '43 arms driven,' while lines 58-59 and 287-294 say
   the `[accepted]` arms and the real library predicate were not driven. No commands or
   output are supplied for those inherited arms" `[AUDIT1 N1]`.
2. Miscategorised arms plus missing red evidence: "Both four-arm mount sections use a
   fixture in place of `/proc/self/mounts`, yet both sections are labelled A. At least eight
   runs are therefore counted in the wrong category. With no other corrections, the stated
   43 A / 82 B should be 35 A / 90 B ... Under the repository's D026 rule those tests are
   supplemental, not closure evidence" `[AUDIT2 A2-F7]`.
3. Prose standing in for commands, plus a wrong subcount: item 1's GREEN command "is only
   described as 'identical, with R3 in place of R2'", item 4 says only "the section 5.1
   manifest arm with the fixture swapped", and section 6.13 is "headed `Manifest binding ...
   (9)`; its own text enumerates 3 item-4 arms, 2 item-1 arms, and 6 table arms, which is 11
   ... it defeats the claim that every displayed count is exact" `[AUDIT3 finding 2]`.
4. Templates and shell state presented as exact commands: the recorded cwd RED command
   "runs GREEN and cannot produce the stated round-2 rc-0 output" because the file was
   overwritten by the GREEN construction `[AUDIT4 finding 1 case 1]`; commands containing
   the literal quoted component `<FIX>` "look for a file named `<FIX>` and cannot produce the
   listed NaN, Infinity, or -Infinity outputs" `[AUDIT4 finding 1 case 2]`; `STUB_CASE=<CASE>`
   "Executed literally ... is shell syntax, not the `twoline`, `oneline2`, `wrapper`, or
   `wrongpath` commands that produced the closure outputs" `[AUDIT4 finding 1 case 3]`. The
   document's own statement "that every command is the exact command executed is therefore
   false" `[AUDIT4 finding 1]`.
5. A prerequisite block that is not valid shell: line 354 records `QA=<the scratch directory
   rendered as $QA above>`, and "Every section 5 command depends on `R2`, `R3`, `R4`, `QA`,
   and related values from that block" `[AUDIT5 finding 1]`.

**The falsification.** Stop reading the evidence and execute it verbatim. Running the
declaration block exactly as written produced `[AUDIT5 finding 1]`:

```
bash: line 3: syntax error near unexpected token `newline'
bash: line 3: `QA=<the scratch directory rendered as $QA above>'
RC=2
```

The closing test was a literal paste-and-run: fenced bodies "extracted from
`round6/SELF_QA.md` without changing any character", sent by `printf '%s'` to the standard
input of "a fresh `bash --noprofile --norc` process", which "returned rc 0 and its stderr
was empty" `[AUDIT6 sec. 2]`. One recorded transcript:

```
RPD_manifest_binding path=$QAW/fix1/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
BLOCK_RC=0
```

and the item-6 block reproduced the rc vector `3,3,3,3,0,0,1,3,3,3,1`, "exactly matching the
section 5.6 table. No tested fence required an edit" `[AUDIT6 sec. 2]`.

**The rule.** Decide before writing QA what observation would have proved the claim false,
and record that observation: the exact executable command, its real red output against the
prior artefact, and its real green output against the current one `[AUDIT2 A2-F7 minimal
fix]`. A command that needs an edit, a substitution or undeclared shell state before it runs
is not closure evidence `[AUDIT5 finding 1]`. Counts and category labels are bookkeeping,
never closure; state separate exact counts for arms actually run, stubbed arms and inherited
arms not re-run, and do not call the last category driven `[AUDIT1 N1 minimal fix]`.

---

## One-offs

Genuine singletons in this evidence set - real defects with one supporting instance each.

1. **The hidden fifth deliverable.** "packaging or hashing round2 recursively includes a
   hidden cache file even though ROUND2_KICKOFF.md requires the same four deliverables. The
   directory therefore does not satisfy the binding deliverable set" `[AUDIT2 A2-F8]`,
   located at `round2/.impeccable/hook.cache.json:1`. Closed in round 3: "A force-inclusive
   recursive listing of `round3/` contains exactly `DESIGN_NOTES.md`, `RP1-B3.sh`,
   `RPD-VERIFY.sh`, and `SELF_QA.md`; there are no hidden files, caches, or directories"
   `[AUDIT3 item 8 CLOSED]`. Lesson: enumerate deliverable sets with a force-inclusive
   listing, because tooling writes files the author never sees.
2. **Authority omitted from an apparently exhaustive dispatch gate.** "An operator can read
   those statements as an exhaustive dispatch gate even though lines 583-585 separately say
   the run is authority-blocked and budget-blocked" `[WPI-AUDIT F6]`. The fix: "say the
   three listed items are necessary but not sufficient. Add explicit written
   host-contact/transport authority and the required budget lift to the dispatch gates, and
   state that `-Execute` and `-Confirm` are technical interlocks, not authority"
   `[WPI-AUDIT F6 minimal fix]`. The audit calls it "a real authority-discipline defect
   because its short dispatch checklist omits the authority and budget lifts that the same
   document says are still absent" `[WPI-AUDIT answer 4]`.

The B3 privilege-domain gap `B3-GAP-ENV` is deliberately not listed here; it is primary
evidence for pattern 2 `[B3-ADJ Design gap B3-GAP-ENV]`.

---

## What the cycle cost, and what it bought.

**Cost.** Seven audit reports are in scope for this catalogue. They belong to two separate
ledgers, kept separate here because they cover different artefacts.

*B3 repair ledger.* Six audits over the B3 staging-admission repair, `[AUDIT1]`-`[AUDIT6]`.
Verdicts in order: REQUEST_CHANGES `[AUDIT1]`, REQUEST_CHANGES `[AUDIT2]`, BLOCK
`[AUDIT3]`, BLOCK `[AUDIT4]`, BLOCK `[AUDIT5]`, PASS `[AUDIT6]`. They carry 18 required
findings - 6 `[AUDIT1 F1-F6]`, 8 `[AUDIT2 A2-F1..A2-F8]`, 2 `[AUDIT3 findings 1-2]`, 1
`[AUDIT4 finding 1]`, 1 `[AUDIT5 finding 1]`, 0 `[AUDIT6]` - plus one nit `[AUDIT1 N1]` and
one optional nit `[AUDIT4 finding 2]`.

*WP-I draft ledger.* One audit over the WP-I preregistration draft, `[WPI-AUDIT]`. Verdict:
REQUEST_CHANGES `[WPI-AUDIT]`. It carries 6 required findings `[WPI-AUDIT F1-F6]`.

Audit 4 recorded that "Per the kickoff, this escalates to the owner and there is no round
5" `[AUDIT4 final verdict]`;
reports exist for rounds 5 and 6, both with the code frozen - the three non-QA files were
byte-identical to round 4 `[AUDIT5 code freeze]` and equal to the kickoff hashes at round 6
`[AUDIT6 sec. 1]`. Six B3 audit rounds occurred: the first five ended non-accepting and
round 6 passed. Rounds 5 and 6 audited the evidence contract with the code frozen - no
non-QA file changed after round 4 `[AUDIT5 code freeze]`, `[AUDIT6 sec. 1]`, round 5's single
required finding was the non-executable QA prerequisite block `[AUDIT5 finding 1]`, and round
6's test was a literal paste-and-run of the recorded fences `[AUDIT6 sec. 2]`.

**Findings that existed only because of an earlier fix.** Several later findings arose on
repair paths introduced for earlier findings:

- Replacing `grep` with a Python parser closed `[AUDIT1 F1]` to PARTIALLY CLOSED and created
  an unisolated root-side interpreter `[AUDIT2 A2-F1]` and a parser that accepts non-JSON
  constants `[AUDIT2 A2-F4]`. The no-weakening table records that "The unisolated interpreter
  is an unjustified new root code-execution surface, so the overall no-weakening gate fails"
  `[AUDIT2 sec. 3]`.
- Adding the mount-boundary predicate for `[AUDIT1 F2]` created the mount-table reader
  defect `[AUDIT2 A2-F5]`, whose repair in round 3 still left the empty nonzero read
  `[AUDIT3 finding 1]`, repaired only in round 4 `[AUDIT4 closure]`.
- The namespace comparison added to close `[AUDIT1 F3]` was itself an overclaim:
  "Finding-closure attempt for F3, but its `bound=initial` claim is unjustified"
  `[AUDIT2 sec. 3]`, i.e. `[AUDIT2 A2-F2]`.
- The round-4 evidence repair introduced its own defect: the recorded RED command "runs
  GREEN and cannot produce the stated round-2 rc-0 output" because the round-4 GREEN
  construction had overwritten the file `[AUDIT4 finding 1 case 1]`.

**Findings exposed by executed fixtures.** Each finding listed here has executed
falsification output recorded against it, produced by an auditor who built a host state and
ran the delivered function: the nested-decoy JSON `[AUDIT1 F1]`; the `PYTHONPATH`/cwd module
shadow `[AUDIT2 A2-F1]`, `[AUDIT3 rerun 1]`; the NaN manifest `[AUDIT2 A2-F4]`; the
unterminated final mount record `[AUDIT2 A2-F5]`; the directory-as-mount-source read error,
which announced itself only as `bash: read: read error: Is a directory` on stderr while the
predicate still printed a clean admission at rc 0 `[AUDIT3 finding 1]`; the ambiguous
two-line diagnostic `[AUDIT2 A2-F6]`; the name-mapped ownership fixtures `[AUDIT2 sec. 1,
rerun 3]`, `[AUDIT3 rerun 5]`; and the non-executable QA prerequisite, found by running it
`[AUDIT5 finding 1]`. Audit 6 was final validation, not a finding; its literal paste-and-run
reproduced the recorded fences without edits `[AUDIT6 sec. 2]`. Audit 1
reproduced nine sampled arms independently `[AUDIT1 sec. 4]`, audit 2's independent sample
"exceeds the required five-arm sample and includes more than two new-code paths" `[AUDIT2
sec. 4]`.

**What it bought.** Round 6 records no required finding and no optional nit, with code frozen
and every tested fence reproducing its recorded transcript without an edit `[AUDIT6]`. The
route from round 1 to that state ran through defects that each looked correct on the page:
`grep` predicates that returned 0 on a decoy `[AUDIT1 F1]`, a root-side child that returned
`bound=both` for a file containing no JSON `[AUDIT2 A2-F1]`, and a mount reader that reported
a clean scan of a directory it could not read `[AUDIT3 finding 1]`. Against the WP-I draft,
the same method found five ordering and domain defects before any host was contacted
`[WPI-AUDIT F1-F5]` and one authority-discipline defect `[WPI-AUDIT F6]`. Executed fixtures
exposed the false outcomes listed above, while the final literal paste-and-run established
that the recorded evidence reproduced without edits `[AUDIT1 F1]`, `[AUDIT2 A2-F1]`,
`[AUDIT3 finding 1]`, `[AUDIT6 sec. 2]`.

---

## Lead note (2026-08-10) — the authority for rounds 5 and 6

The cost section correctly observes that `[AUDIT4]` stated "there is no round 5" and that
rounds 5 and 6 nonetheless happened. The distilling agent was not given the governing
authority documents, so that tension reads as unexplained. It is not a process violation,
and the record should say why.

The three-round limit came from the audit-tier policy as a *quality cadence*. Partway
through the night the owner granted a standing authority
(`STANDING_AUTONOMY_AUTHORITY_2026-08-09.md` §1) making that limit explicitly not a stop
sign: when a cycle reaches its round limit with only NARROW survivors — mechanical code
fixes or documentation gaps, as opposed to architectural defects or anything needing a
hard gate — the Lead opens a bounded fix round automatically and re-audits, repeating until
PASS. The owner separately and explicitly authorized the bounded round 4 in-session before
it ran.

Each continuation was recorded with its scope locked before dispatch, in
`06_B3_REPAIR/B3_REPAIR_CYCLE_RECORD.md`:

- **Round 4** — owner-authorized in-session; scope limited to the two `[AUDIT3]` survivors.
- **Round 5** — doc-only, opened under the standing authority because the sole survivor
  `[AUDIT4 finding 1]` was a documentation defect; the code was frozen by hash and the
  freeze was verified independently `[AUDIT5 code freeze]`.
- **Round 6** — doc-only for the same reason, with a convergence stop recorded in advance:
  another same-class BLOCK would escalate to the owner rather than trigger a round 7.

The substantive point for this catalogue is unaffected and worth stating plainly: **the
code stopped changing after round 4.** Rounds 5 and 6 moved no executable byte. What they
fixed was the evidence contract — whether the recorded commands were literally the commands
that ran. Two full audit rounds were spent on that alone, which is the strongest available
argument for Pattern 10: evidence that cannot be re-executed is not evidence, and proving
it takes as much work as the code did.

---

# AMENDMENT — 2026-08-10 night (Lead), after a full re-review against the day's evidence

Source: `DEFECT_PATTERNS_REVIEW_CODEX_2026-08-10.md`, verdict `AMEND: 7 changes`, produced
by a fresh flagship session against the day's ten review rounds across RP6-P0, RP7, the
transport set and the §10.2 path-scope prover.

## Lead adjudication on the proposed changes

The re-review recommended deleting standalone Pattern 7 and folding it into Pattern 6.
**Rejected in that form, accepted in substance.** Dozens of committed audit reports cite
these patterns by number; renumbering or deleting one silently invalidates every citation
and makes older evidence unreadable. Numbering is therefore **frozen permanently**.

Instead:

- **Pattern 7 stays where it is** and is reclassified as the reader-completion subtype of
  Pattern 6. Cite them together (`6/7`) when the defect is "semantics decided before the
  read completed". Pattern 7 had no new primary hit today; that is a reason to subordinate
  it, not to erase its falsifications.
- **Pattern 5 narrows** to grammar completeness *inside a modeled input or argv contract*.
  Coverage of unmodeled grammar is now Pattern 12's job.
- **Pattern 9 narrows** to claim-to-predicate mismatch and is an **overlay**, not the
  primary home of every false outcome. Almost any defect can be described as a sentence
  outrunning its probe; when a more specific pattern fits, cite that one and use 9 only for
  the wording defect itself.
- **Pattern 10 narrows** to falsifiability and literal reproducibility of evidence.
- **Patterns 2, 3 and 8 are kept** despite sparse hits today: 2 and 3 both caught the
  prover's overclaim, and 8 exposed a name-based identity residual still carried in the
  transport set.

Three new patterns are added as **11, 12 and 13**. All three earned their place by
appearing independently in more than one artifact on the same day.

---

## Pattern 11 — "The declared instrument is not the executed instrument"

**The mistake.** A tool, interpreter, helper or prerequisite is pinned, validated,
projected and documented, but the real accepting caller never passes that object through
the binding gate. The claim is produced by an executable or function whose identity was
never established.

**Why it survives casual review.** Every component exists on the page: a pin parser, a
binding function, a required-count check, an isolation flag, a QA loop. Reviewers verify
each component independently. The missing fact is *reachability from the production
caller*. A helper-level test can even prove the binder works while the real caller omits
one member.

**Concrete instances.**

1. RP7 accepted, projected and required `python3`, but `wpi_main` bound only nine tools;
   the unbound program forged `OK fields=8`, wrote a marker and reached `RP7 PASS`
   (`RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` F1; the Lead reproduced it independently in
   `RP7_LEAD_VERIFICATION_R4_2026-08-10.md`).
2. RP6 printed `pinned_timeout` although its accepted one-entry pin set required only
   Python, so the object producing the bound was never required to be pinned
   (`RP6_CODEX_AUDIT_R6_2026-08-10.md` A10).
3. The transport plan pinned the local SSH client but invoked bare remote `bash`; a PATH
   plant or `BASH_ENV` startup file outside the pinned program domain forged the remote
   program marker (`TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md` F1).

**The falsification.** Replace exactly the declared instrument with a deviant executable
that writes a marker and emits the accepted terminal grammar. **Drive the real top-level
caller, not the helper.** If the marker appears, or the accepting line is reached before
the binder rejects the object, the declaration is ornamental.

**The rule.** For every accepting claim, trace the dynamic call path backward to a binding
event for every executable, helper and function that can produce it. Derive the production
instrument inventory *from the caller* once; never redeclare it in QA. Require an exact
one-to-one comparison between declared, bound and executed instruments, and mutation-test
the real caller by removing or replacing each member.

---

## Pattern 12 — "What the analyzer does not model must not disappear"

**The mistake.** A static analyzer, policy engine or dispatcher meets a command, option,
redirection or nested program form outside its model and emits neither a resolved fact nor
an unresolved marker. Empty output is then read as proof that no sink or risk exists.

**Why it survives casual review.** Modeled happy paths produce detailed, deterministic
rows, so the tool looks comprehensive. The registry of known commands is mistaken for proof
that the language is covered. Shortcuts such as "no-path command" or "ignore options" keep
common fixtures quiet, and determinism merely reproduces the same omission every run.

**Concrete instances.** All from `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` F1–F4 and F7:

1. `pushd "$ROOT"` and a `trap` firing a reader at EXIT produced zero resolved paths, zero
   unresolved issues, and `PATHSCOPE verdict=PASS rc=0`.
2. `ssh "$HOST"` and `getent hosts "$HOST"` silently lost their endpoints.
3. A `find … -exec <reader> ;` form reported only the allowed root; curl upload, tar output
   and cp target paths supplied as `--name=value` likewise disappeared.
4. The unsupported `<>` token produced an invented target rather than a coverage refusal.

**The falsification.** For every registered command and shell construction, add one
unmodeled-but-valid path or endpoint form and one nested sink. Delete an adapter, or insert
an unknown option. The tool must emit a specific unresolved coverage record and rc 3.
**Zero facts plus PASS is always red.**

**The rule.** Coverage is a fail-closed property. Keep an explicit grammar matrix for
commands, options, redirections, nesting and implicit endpoints. A recognised primitive
with any unconsumed token or unsupported semantic form must STOP with a coverage reason.
An unknown command capable of executing or opening anything is an opaque sink, not a no-op.
Report modeled coverage separately from resolved-path counts, and never infer absence of
risk from absence of analyzer output.

---

## Pattern 13 — "Every admitted member needs a terminal disposition"

**The mistake.** A stage declares or enumerates a universe, and a later stage silently
drops, overwrites, reinterprets or fails to bind one member. The reduced universe passes,
so absence from the result is mistaken for absence from the subject.

**Why it survives casual review.** Each stage is locally plausible: enumeration prints the
right count, preflight proves the bytes readable, a library returns a convenient
dictionary, and the comparison succeeds over whatever remains. Nobody checks conservation
across stage boundaries. Dictionary overwrite and library skip behaviour are especially
quiet because they return valid data structures at rc 0.

**Concrete instances.**

1. RP7 preflight admitted two readable `*.dist-info` directories; the verifier silently
   skipped the one whose METADATA lacked `Name`, compared one package, and emitted parity
   PASS (`RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` F2).
2. The same verifier overwrote duplicate canonical package names in a dictionary, so two
   admitted objects could collapse into one compared identity.
3. RP6 validated pathname-expanded `id -G` items but reconciled the raw string against the
   forbidden-GID ledger, so a raw `0*` could be rendered `form=numeric_only` from the
   expanded item while the forbidden numeric identity vanished from the later whole-word
   intersection (`RP6_CLAUDE_REAUDIT_R5_2026-08-10.md` F2).

**The falsification.** Add one malformed-but-readable member, two members that canonicalise
to the same key, and one member whose representation changes between validation and
comparison. The terminal accounting must show **one disposition per input member** and must
STOP on missing identity, duplicate identity, representation drift or an unexplained count
change. A final PASS over fewer members is red.

**The rule.** Declare the universe once, assign every member a stable identity, and carry
that identity unchanged through preflight, parse, normalisation and comparison. Enforce a
conservation equation at every boundary: input members = accepted + rejected + explicitly
unresolved, with no overwrite and no implicit filter. PASS requires every admitted member
to reach exactly one terminal disposition.

---

## Standing note on numbering

Pattern numbers are permanent. A pattern that stops earning its keep is **narrowed,
subordinated or marked dormant in place** — never renumbered and never deleted. The cost of
breaking every citation in the committed audit trail is far higher than the cost of
carrying a quiet pattern.

## Effective time

This amendment landed at ~22:00 on 2026-08-10, while two RP7 round-5 reviews were already
in flight against the pre-amendment text. Those two reviews are judged against the ten
original patterns; every round dispatched after this commit is judged against thirteen.
