REQUEST_CHANGES

# Findings

## A2-F1 - HIGH - REQUIRED: the root-side Python child is environment-hijackable

Location: round2/RPD-VERIFY.sh:387-396 and round2/RPD-VERIFY.sh:466-488.

Failure scenario: invoke the verifier with PYTHONPATH naming an attacker-controlled
directory that contains json.py. The delivered python3 -c command does not use
isolated mode, does not remove Python environment variables, and does not pin a
trusted interpreter. The imported json module can return the two expected values
for a manifest that is not JSON, print bound, and exit 0. Import-time code also
runs with the verifier's root authority, contradicting mutation=none.

Actual local fixture output, using the delivered function and a manifest containing
only THIS IS NOT JSON AND BINDS NOTHING:

    RPD_manifest_binding path=/tmp/audit2-codex.Mq9H45/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
    RC=0

Minimal fix: invoke a preregistered absolute interpreter in isolated mode, for
example /usr/bin/python3 -I, from a deploy channel that supplies a clean trusted
environment and working directory. Remove PYTHONPATH, PYTHONHOME, user-site and
loader injection variables before this script starts. Do not resolve python3 from
an operator-controlled PATH. Add a RED/GREEN PYTHONPATH and current-directory
module-hijack regression.

## A2-F2 - HIGH - REQUIRED: the namespace check does not bind the host mount namespace or root

Location: round2/RPD-VERIFY.sh:158-190 and round2/RPD-VERIFY.sh:517.

Failure scenario: run inside a rootful container with the identity uid map and its
own PID namespace. /proc/self/uid_map is 0 0 4294967295, while /proc/self/ns/user
and /proc/self/ns/mnt equal the links for container-visible PID 1. All delivered
checks pass even though /etc/mtc-bridge is the container's filesystem, not the host
object the admission claim names. A chroot in the same user and mount namespaces
similarly changes what literal /etc resolves to without changing either namespace
link. DESIGN_NOTES.md:475-477 already discloses the container half of this defect.

The delivered function on the current Linux fixture reported:

    RPD_namespace user=user:[4026531837] mnt=mnt:[4026532220] bound=initial uid_map=identity
    RC=0

That output proves equality only with PID 1 visible in the current PID namespace;
it does not prove the printed mount namespace is the host's initial namespace.

Minimal fix: have the deploy channel preregister and attest the expected host user
and mount namespace identities plus the host root filesystem identity, and compare
against those values. Alternatively execute through a channel already bound to
those identities and include that attestation in the evidence. Do not label a
visible-PID-1 comparison as bound=initial.

## A2-F3 - MEDIUM - REQUIRED: two ownership admissions remain name-mapped

Location: round2/RP1-B3.sh:193-222 and round2/RP1-B3.sh:462-463.

Failure scenario: the accepted service account has preregistered numeric ownership
different from 999:999, but NSS renders uid/gid 999:999 as
mtc-bridge:mtc-bridge. The round-2 branch compares the rendered name and rejects
only numeric zero, so the wrong nonzero owner passes. The binding round-2 change
said all ownership comparisons must be numeric. DESIGN_NOTES.md:478-479 admits
that these two are not.

Actual delivered-function output with numeric 999:999 rendered as the expected
name:

    B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
    RC=0

Minimal fix: preregister the numeric uid and gid of the service account and compare
stat %u:%g exclusively against that pair for STATE_DIR and LOG_DIR. Printed names
may remain diagnostic only.

## A2-F4 - MEDIUM - REQUIRED: the structural parser accepts non-JSON constants

Location: round2/RPD-VERIFY.sh:451-465.

Failure scenario: Python's json.loads accepts NaN, Infinity and -Infinity by
default even though they are not JSON values. A manifest with both correct
top-level bindings and an additional value NaN therefore passes the claim that
the whole file is valid structural JSON.

Actual delivered-function output:

    RPD_manifest_binding path=/tmp/audit2-codex.Mq9H45/nan.json bound=both parser=python3_json_structural keys=top_level_exact
    RC=0

Minimal fix: pass a parse_constant callback that always raises, map the result to
parse_error rc 3, and add RED/GREEN fixtures for NaN, Infinity and -Infinity.

## A2-F5 - MEDIUM - REQUIRED: the mount-table reader skips a partial final record

Location: round2/RPD-VERIFY.sh:306-321 and round2/RP1-B3.sh:347-362.

Failure scenario: the mount source ends with a matching record but no final
newline, as can occur with a truncated or failed read or with an untrusted proc
view. Bash read populates the fields but returns nonzero at EOF, so the while body
never examines that record. The predicate prints no-mount and returns 0.

Actual delivered-function output for the single unterminated line
src /etc/mtc-bridge ext4 rw 0 0:

    RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=/tmp/audit2-codex.Mq9H45/mounts-no-final-newline
    RC=0

Minimal fix: process a populated final record even when read returns nonzero,
validate every record has the required fields, and STOP on malformed, truncated
or read-error input. Apply the same repair to both copies and add a falsified
unterminated-record test.

## A2-F6 - LOW - REQUIRED: ambiguous multi-line diagnostics select the PASS arm

Location: round2/RP1-B3.sh:432-445.

Failure scenario: stat emits two diagnostic lines, one containing Permission
denied and one containing No such file or directory, with rc 1. b3_sanitize
replaces the newline with a space and the case statement selects the first
substring, so an ambiguous diagnostic is called EACCES and returns 0 rather than
STOP.

Actual delivered-function output:

    B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1 mechanism=message_lc_all_c
    RC=0

The preceding access builtin reduces ordinary GNU-coreutils exposure, but the
classifier's stated fail-closed contract is still false under a wrapper, loader
diagnostic or mixed producer output.

Minimal fix: reject raw diagnostics containing CR, LF or more than one error
class before sanitizing; then require one exact C-locale diagnostic shape. Keep
unrecognized or ambiguous text at rc 3.

## A2-F7 - MEDIUM - REQUIRED: N1 accounting is still not exact and most closure tests lack D026 evidence

Location: round2/SELF_QA.md:62-70, round2/SELF_QA.md:199-210, and
round2/SELF_QA.md:302-317.

Failure scenario: category B is defined as any arm with a stubbed command or
repointed path literal. Both four-arm mount sections use a fixture in place of
/proc/self/mounts, yet both sections are labelled A. At least eight runs are
therefore counted in the wrong category. With no other corrections, the stated
43 A / 82 B should be 35 A / 90 B, with per-file counts RP1-B3 11 A / 52 B and
RPD-VERIFY 24 A / 38 B.

In addition, most arm tables state a scenario and claimed output but do not
record the exact executable command and RED output against round 1 or an
equivalent mutation. Under the repository's D026 rule those tests are
supplemental, not closure evidence. The independent RED/GREEN runs in this audit
close several named cases, but they do not make SELF_QA's accounting or evidence
claim honest.

Minimal fix: correct the three-way counts and labels, and record exact commands
and real RED/GREEN output for every new regression test offered as closure
evidence for F1-F6 and the must-change items.

## A2-F8 - LOW - REQUIRED: round2 contains a fifth, unrequested deliverable

Location: round2/.impeccable/hook.cache.json:1.

Failure scenario: packaging or hashing round2 recursively includes a hidden cache
file even though ROUND2_KICKOFF.md requires the same four deliverables. The
directory therefore does not satisfy the binding deliverable set.

Minimal fix: remove round2/.impeccable and leave exactly DESIGN_NOTES.md,
RP1-B3.sh, RPD-VERIFY.sh and SELF_QA.md.

# 1. Finding closure

| Item | Status | Round-2 evidence or remaining defeat |
|---|---|---|
| F1 | PARTIALLY CLOSED | RPD-VERIFY.sh:397-465 parses the whole file, rejects duplicate keys and compares exact top-level strings. The audit-1 decoy now fails. A2-F1 can replace json.loads through PYTHONPATH and return a false bound token; A2-F4 also admits non-JSON NaN. |
| F2 | PARTIALLY CLOSED | RPD-VERIFY.sh:270-287 rejects a symlinked/canonicalized parent, and lines 306-321 add the mount predicate. The symlink fixture now fails, but A2-F5 lets a matching partial final mount record pass. |
| F3 | PARTIALLY CLOSED | RPD-VERIFY.sh:281-286 and 343-349 use numeric 0:0 and reject the name-mapped root case. Lines 168-190 reject an ordinary rootless uid map. A2-F2 still admits container-local mount/root state, and A2-F3 leaves two ownership checks name-based. |
| F4 | CLOSED | RP1-B3.sh:159-182 and RPD-VERIFY.sh:228-251 replace rp0_probe_path; RP1-B3.sh:242-265 replaces the temp-backed sweep. The original mktemp mutation is gone. The RED probe had one live temp file; the round-2 probe had zero and rc 0. A2-F1 is a separate new arbitrary-code/mutation exposure. |
| F5 | CLOSED | RP1-B3.sh:443-444 routes ENOENT to b3_fail. Actual output was B3_FAIL reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES, rc 1. |
| F6 | CLOSED | RP1-B3.sh:73-100 and RPD-VERIFY.sh:76-99 remove tr and add reasoned rc-3 backstops. The round-1 tr falsification exited silently with rc 7; the round-2 ERR fixture printed B3_STOP reason=unadjudicated_command_status rc=1 line=33 cmd=[false] and returned rc 3. |
| N1 | NOT CLOSED | SELF_QA separates three categories, but at least eight fixture-backed mount arms are misclassified as A; see A2-F7. |
| O1 | CLOSED | Same evidence as F5: ENOENT is FAIL rc 1. |
| O2 | CLOSED | RP1-B3.sh:113-120 and RPD-VERIFY.sh:126-131 emit reasoned STOP. Actual missing-input runs returned rc 3 in both blocks. |
| O3 | CLOSED | The intended delivered code contains no mktemp, rm or write redirection and the live temp probe went from count 1 in round 1 to count 0 in round 2. |
| O5 | CLOSED | Builtin sanitization plus the ERR traps prevent the original raw tr status escape; actual RED/GREEN statuses were 7 and 3. |

Required audit-1 fixture reruns against round 2:

1. Decoy JSON manifest.

   Invocation: rpd_assert_manifest_binding "$mf_decoy" "$GOODREL" "$GOODMAN" 0640

       RPD_FAIL reason=install manifest binds a different release_sha
       RC=1

   The round-1 fixed-string predicates returned 0 for both bindings. This is a
   verified RED/GREEN closure for that exact fixture, subject to A2-F1 and A2-F4.

2. Symlinked configuration parent.

   Round 1, using real root-owned local leaves through the symlink:

       RPD_stat path=/tmp/audit2-codex-red.74vRAC/r1-link/mtc-bridge.env owner=root:root mode=600
       RPD_stat path=/tmp/audit2-codex-red.74vRAC/r1-link/install_manifest.json owner=root:root mode=640
       RPD_manifest_binding path=/tmp/audit2-codex-red.74vRAC/r1-link/install_manifest.json bound=both
       RC=0

   Round 2:

       RPD_FAIL reason=conf_dir_is_symlink kind=link_live path=/tmp/audit2-codex.Mq9H45/etc-mtc-bridge
       RC=1

3. Name-mapped root ownership.

   Round 1:

       RPD_stat path=/fixture/env owner=root:root mode=600
       RC=0

   Round 2:

       RPD_stat path=/fixture/env owner_numeric=1000:1000 owner_name=root:root mode=600
       RPD_FAIL reason=path=/fixture/env owner_numeric=1000:1000 expected=0:0
       RC=1

# 2. New-defect sweep

Python child:

- PYTHONPATH module injection produced false binding rc 0: A2-F1.
- A correct manifest plus NaN produced false structural-JSON rc 0: A2-F4.
- A 4,194,305-byte file produced
  RPD_STOP reason=install_manifest_oversize ... limit_bytes=4194304, rc 3.
- Invalid UTF-8 produced RPD_STOP reason=install_manifest_unparsable, rc 3.
- Duplicate keys, trailing data, absent keys, wrong types and wrong bindings are
  structurally fail-closed by inspection and by the decoy/duplicate evidence.

Mount and namespace code:

- The real Linux namespace arm returned rc 0, but A2-F2 shows why that is not host
  attestation.
- Exact at/under mount targets with normal newline-terminated fixture records
  STOP. An unterminated matching final record returns false rc 0: A2-F5.
- Symlinked and noncanonical configuration parents fail rc 1.

No-temp and stderr classifiers:

- A real clean local tree returned B3_no_write_bit and rc 0.
- Adding a mode-0644 file returned
  B3_FAIL reason=writable path inside immutable tree: <fixture>/file, rc 1.
- A live observation found one temp file during the round-1 probe and zero during
  the equivalent round-2 probe.
- ENOENT returns FAIL rc 1; EIO and unknown text return STOP rc 3.
- LC_ALL=C is exported at both file entries and pinned on each stat producer.
- An ambiguous two-line EACCES plus ENOENT diagnostic returns rc 0: A2-F6.

# 3. No-weakening check

The code-only round1-to-round2 diff was inspected independently. No accepted
round-1 host predicate was deleted: the same release, venv, state, log,
configuration and unit paths remain; the exact modes remain; both immutable-tree
sweeps retain find "$root" ! -type l -perm /222 -print -quit; the unprivileged
identity/group checks, three deferred evidence lines and terminal B3 PASS remain.

Delta classification:

| Delta | Classification |
|---|---|
| Input prechecks and rc-3 reasons in both blocks | Finding closure: O2. |
| LC_ALL=C, builtin sanitizer and ERR traps | Finding closure: F6/O5; justified fail-closed hardening. |
| Local no-temp path classifiers and sweep capture | Finding closure: F4/O3. The find predicate is unchanged; rc-0 unexpected output now STOPs, which is stronger. |
| Numeric 0:0 comparisons | Finding closure: F3. The two service-name branches are incomplete, not a weakening of round 1; see A2-F3. |
| ENOENT STOP to FAIL | Finding closure: F5/O1. |
| Parent canonicality and mount checks in both blocks | Finding closure plus justified symmetric hardening for F2. The parser implementation is incomplete; see A2-F5. |
| B3 namespace recording and access-builtin denial checks | Justified additions that narrow and identify the caller-specific claim. |
| RPD uid-map/PID-1 namespace comparison | Finding-closure attempt for F3, but its bound=initial claim is unjustified; see A2-F2. |
| grep replacement with Python JSON and descriptor fstat | Required F1 closure plus justified size, O_NOFOLLOW, kind, mode and owner hardening. The unisolated interpreter is an unjustified new root code-execution surface, so the overall no-weakening gate fails; see A2-F1. |
| Structural parser accepting NaN | Incomplete F1 closure, not weaker than round 1 but still below the required JSON contract; see A2-F4. |
| Updated claims, design notes and QA | Finding-closure documentation, except the incorrect QA counts and overclaimed initial namespace. |
| round2/.impeccable/hook.cache.json | Unjustified extra deliverable. |

# 4. QA honesty

Independent sample results:

| Arm | Code path | Actual result | Rc | Assessment |
|---|---|---|---:|---|
| Decoy manifest | New Python JSON verifier | different release_sha | 1 | Matches intended closure |
| Oversize manifest | New Python size guard | install_manifest_oversize | 3 | Matches |
| Invalid UTF-8 | New Python decoder | install_manifest_unparsable | 3 | Matches |
| Symlinked parent | New parent classifier | conf_dir_is_symlink | 1 | Matches intended closure |
| Name-mapped root | New numeric owner check | owner_numeric=1000:1000 expected=0:0 | 1 | Matches intended closure |
| Real namespace read | New namespace binding | RPD_namespace ... bound=initial | 0 | Code result reproduced; semantic claim refuted by A2-F2 |
| Clean immutable tree | New no-temp sweep | B3_no_write_bit | 0 | Matches |
| Writable offender | New no-temp sweep | writable path .../file | 1 | Matches |
| ENOENT boundary | Changed classifier | conf_dir_search_permitted_name_absent | 1 | Matches intended closure |
| Missing inputs | New O2 guards in both blocks | reasoned input_missing | 3 | Matches |

This exceeds the required five-arm sample and includes more than two new-code
paths. Syntax checks returned rc 0 for both scripts. The two documented SHA-256
values in SELF_QA match the delivered scripts, and all four intended deliverables
are ASCII.

QA is nevertheless non-accepting. The three-way counts are not exact, the
fixture-backed mount arms are mislabeled, the self-QA missed all of A2-F1 through
A2-F6, and most claimed closure tests do not carry the commands plus actual
RED/GREEN output required by D026.

# Final complete repair list for round 3

1. Isolate and pin the Python interpreter and sanitize its launch environment;
   add module-hijack RED/GREEN tests.
2. Replace visible-PID-1 inference with deploy-channel attestation of host
   namespace and root-filesystem identity.
3. Preregister and compare numeric service uid/gid for STATE_DIR and LOG_DIR.
4. Reject NaN, Infinity and -Infinity in the JSON parser.
5. Make both mount readers reject malformed, partial and read-error input.
6. Reject multi-line or ambiguous boundary diagnostics before EACCES matching.
7. Correct QA counts and add D026 commands plus real RED/GREEN output.
8. Remove the hidden .impeccable cache so round2/ contains only four deliverables.

Final verdict: REQUEST_CHANGES
