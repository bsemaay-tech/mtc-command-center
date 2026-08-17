REQUEST_CHANGES

# Findings

## F1 - HIGH - REQUIRED: grep can admit the wrong manifest bindings

Location: `round1/RPD-VERIFY.sh:132`, `round1/RPD-VERIFY.sh:139`, and
`round1/RPD-VERIFY.sh:145`.

Failure scenario: this valid JSON has the preregistered values only in a nested
decoy object, while both top-level values are wrong:

```json
{"decoy": {"release_sha": "2ce41e34bceb599d80af24c5c33d835820ec321b", "release_manifest_sha256": "edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26"}, "release_sha": "0000000000000000000000000000000000000000", "release_manifest_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```

Both delivered `grep -qsF` predicates return 0. An independent JSON parse reports
the two wrong top-level values. The reproduced output was:

```text
GREP_RELEASE_RC=0
GREP_MANIFEST_RC=0
TOP_RELEASE=0000000000000000000000000000000000000000
TOP_MANIFEST=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Duplicated top-level keys produce the same false pass when an accepted value
appears before the effective later value. The fixed-string search also accepts
the strings in any object and does not establish that the file is valid JSON.

Minimal fix: replace the two greps with a silent, full-file JSON parse that (1)
rejects duplicate keys, (2) requires one top-level object, and (3) compares the
two top-level string values exactly. Preserve rc 1 for a semantic mismatch and
rc 3 for read, parse, or tool failure. This requires changing the binding brief;
grep cannot prove the stated JSON binding.

## F2 - HIGH - REQUIRED: RPD-VERIFY follows a symlinked configuration parent

Location: `round1/RPD-VERIFY.sh:106-120`,
`round1/RPD-VERIFY.sh:128-145`, and `round1/RPD-VERIFY.sh:161-165`.

Failure scenario: make `/etc/mtc-bridge` a symlink to a decoy directory containing
regular files with the requested leaf modes, owner names, and grep strings. The
leaf `lstat` sees regular files because the intermediate symlink is followed;
both metadata checks and both binding checks can PASS. The separate unprivileged
block would reject the parent symlink at `round1/RP1-B3.sh:208`, but it runs at a
different time, so the root-side admission is neither self-contained nor atomic
with that check.

Minimal fix: in RPD-VERIFY, independently require `CONF_DIR` itself to be a
non-symlink directory at the literal canonical path before touching either leaf,
and verify its expected numeric mode and ownership there. If mount identity is
part of the accepted state, add an explicit mount-boundary predicate too; path
canonicalization alone does not detect a mount over the directory.

## F3 - HIGH - REQUIRED: root and root ownership are not securely established

Location: `round1/RPD-VERIFY.sh:70-74` and
`round1/RPD-VERIFY.sh:106-120`.

Failure scenario 1: an NSS database maps a nonzero file UID and GID to the names
`root` and `root`. GNU `stat -c '%U:%G'` then prints `root:root`, so files not
owned by numeric 0:0 pass lines 119-120.

Failure scenario 2: a rootless user namespace maps host UID 1000 to namespace UID
0 and exposes operator-controlled files through its mount namespace. `id -u`
prints 0, those files can appear as namespace `root:root`, and the block can PASS
without host-root authority.

Minimal fix: compare file ownership with `stat -c '%u:%g'` against `0:0`, and bind
execution to the initial user and intended mount namespace through a deploy-channel
attestation or an explicit fail-closed namespace check. `id -u = 0` alone proves
only namespace-local identity.

## F4 - MEDIUM - REQUIRED: the root-side verifier violates its no-mutation contract

Location: `round1/RPD-VERIFY.sh:108`, `round1/RPD-VERIFY.sh:130`,
`../01_RUNKIT/RP0-LIB.sh:31`, and `../01_RUNKIT/RP0-LIB.sh:38-49`.

Failure scenario: every call to `rp0_probe_path` creates and removes a temporary
file. With `TMPDIR=/etc/mtc-bridge`, a root execution creates that file inside the
protected directory; interruption can leave it behind. Even with default TMPDIR,
the statement at `round1/RPD-VERIFY.sh:16` that there is "no mutation of any kind"
is false.

Minimal fix: use a no-temp, read-only path classifier in RPD-VERIFY and in the new
boundary probe. If temporary scratch writes are intentionally allowed, the brief
and header must say so and TMPDIR must be pinned outside verified paths, but that
would be a contract change rather than compliance with "no mutation of any kind."

## F5 - MEDIUM - REQUIRED: ENOENT is a known deviation but is classified STOP

Location: `round1/RP1-B3.sh:184-185` and
`round1/DESIGN_NOTES.md:241-249`.

Failure scenario: the caller can search `/etc/mtc-bridge`, but
`mtc-bridge.env` is absent. `stat` returns ENOENT. That result positively proves
that directory search succeeded and also observes a missing preregistered path;
it is not an inability to evaluate. The delivered code emits rc 3 instead of a
deviant-state rc 1.

Minimal fix: route ENOENT to `b3_fail` with the existing dedicated reason, and
retain STOP only for errors that do not establish whether entry was permitted.
The kickoff's blanket "any other error class is STOP" must be narrowed accordingly.

## F6 - MEDIUM - REQUIRED: a documented raw exit violates the 0/1/3 contract

Location: `round1/RP1-B3.sh:175` and
`round1/DESIGN_NOTES.md:265-268`.

Failure scenario: `tr` is unavailable or fails while reading the boundary
diagnostic. Under `set -e`, the script exits with the raw tool status, potentially
1, 126, or 127, and emits no B3 reason. Rc 1 can then be misread as a host-state
FAIL even though the probe result was not classified. The same inherited pattern
exists in `../01_RUNKIT/RP0-LIB.sh:39` and `../01_RUNKIT/RP0-LIB.sh:49`.

Minimal fix: capture and adjudicate the diagnostic-sanitization status explicitly;
any failure must emit a STOP reason and exit 3. Apply the same rule to every new
path that relies on the library helper, or narrow the claimed rc contract.

## N1 - NIT: SELF_QA overstates how many arms it drove

Location: `round1/SELF_QA.md:56-59` and
`round1/SELF_QA.md:287-294`.

Concrete evidence issue: line 56 says "43 arms driven," while lines 58-59 and
287-294 say the `[accepted]` arms and the real library predicate were not driven.
No commands or output are supplied for those inherited arms.

Minimal fix: report separate exact counts for delivered-code arms actually run,
stubbed arms, and inherited arms not re-run. Do not call the last category driven.

# 1. Spec compliance and complete behavioral delta classification

The surviving release-tree, venv-tree, write-bit sweep, state-directory,
log-directory, configuration-directory, and unit-file predicates and invocations
are unchanged in strength. The two shared predicate bodies are byte-identical
apart from an ASCII-only comment character. `set -Eeuo pipefail`, the B3/RP0 log
families, `/222`, the sweep budget guard, and terminal `B3 PASS` are preserved.

The behavioral deltas from the accepted block are:

1. Required by brief: remove the B3 manifest-SHA input guard because B3 no longer
   consumes it.
2. Required by brief: remove unprivileged mode/owner admission for `ENV_FILE` and
   `INSTALL_MANIFEST`, remove the manifest-binding function and call, and remove
   the old binding section.
3. Required by brief: retain the env path only as a denied-entry probe target and
   retain the manifest path only for a deferral log; no manifest stat, open, or
   grep remains in B3.
4. Required by brief: add an EACCES boundary pass arm, a visible-file FAIL arm,
   and an other-error STOP arm. The current ENOENT STOP follows the literal brief
   but is semantically wrong and must change per F5.
5. Justified addition: add `command -v` preconditions for the two required RP0
   predicates, converting an unsourced-library rc 127 into a reasoned rc 3.
6. Justified addition: add numeric UID/group probes and stop root or a caller in
   the directory group before making a caller-specific opacity claim. This also
   changes ordering: an invalid caller now STOPs before the old tree checks.
7. Justified addition: probe a second absent name. Under ordinary DAC it is
   redundant for an EACCES pass, but it helps expose permitted search as ENOENT.
8. Justified addition: add explicit deferral and reduced-claim evidence lines.
9. Unjustified implementation addition: the new boundary predicate uses a
   temporary file even though the brief says no host mutation; see F4.

No other runtime delta was found. Header expansion, provenance commentary, and
ASCII punctuation changes do not alter behavior.

# 2. Soundness of the boundary probe

The probe supports only a narrow statement: at the two probe instants, this
caller received a diagnostic classified as EACCES for two names. It does not
prove that the directory is globally opaque or that its backing object is the
accepted one.

- A POSIX ACL granting search only to a third user can coexist with mode 0750 and
  an EACCES result for `gatea`. B3 then PASSes. That is not a false pass against
  the narrowly worded `opaque_to_operator` claim, but it is a false pass if the
  evidence is later read as "no non-root outsider can enter."
- An ACL or CAP_DAC_READ_SEARCH grant to the actual caller normally does not
  produce a pass: the existing name becomes visible and FAILs, while the absent
  name yields ENOENT. The capability case is therefore detected, although ENOENT
  is misclassified as STOP.
- A name-specific MAC policy can create a false pass. For example, grant the
  caller directory search by ACL, deny metadata access to exactly the env and
  probe-name patterns by MAC policy, and permit another name. Both probes get
  EACCES while the directory is not actually opaque to the caller. Two names do
  not prove a universal property under name-sensitive policy.
- A final-component symlink at `/etc/mtc-bridge` is rejected by the earlier
  `rp0_probe_path` call. An intermediate symlink in the root-side verifier is not;
  that is F2.
- A mount over `/etc/mtc-bridge` can present mode 0750 root:root and EACCES for
  both names, so B3 PASSes. If the accepted state identifies only current path
  properties, that is within the narrow claim. If it identifies the original
  backing filesystem object, this is a false pass because no mount check exists.
- The pair of names is stronger than one observation only for ordinary permitted
  search. It is not a proof over every name, policy, or point in time.
- `LC_ALL=C` is correctly applied to `stat`, so GNU coreutils localization does
  not turn a normal EACCES into a translation-dependent PASS. A different message
  normally becomes STOP, which is fail-closed. Matching the substring
  `Permission denied` is still not an errno check: a wrapper or mixed diagnostic
  containing that text can manufacture a pass. A reliable implementation should
  classify the actual EACCES errno, not prose.

Conclusion: no false pass exists under stable, ordinary Unix DAC with trusted GNU
tools and the narrow caller-specific claim. False passes do exist once the claim
is read globally, backing-object identity matters, or name-sensitive policy/tool
output is admitted.

# 3. RPD-VERIFY soundness

The metadata checks are not sufficient to support the stated admission claim.

- The leaf-kind checks correctly reject final-component live and dangling
  symlinks, directories, and other object kinds.
- Exact mode comparison is sound for the observed leaf at that instant.
- Owner comparison is name-based rather than numeric and can accept nonzero
  ownership under unusual NSS data; see F3.
- The parent directory is not checked, so both leaves can be reached through a
  symlinked configuration parent; see F2.
- The lowercase-hex and exact-length guards correctly block newline, CR, quote,
  and multi-pattern injection into grep. They do not repair grep's lack of JSON
  structure.
- Fixed-string grep is unsound for nested keys, duplicate keys, malformed JSON,
  and strings in the wrong structural location. It can also stop reading after a
  quiet match, so a later read problem need not be observed. The nominal rc
  mapping is correct only for the status grep actually returns: 1 becomes FAIL
  and greater than 1 becomes STOP.
- `id -u = 0` is a numeric check, but it proves only namespace-local UID 0 unless
  the deploy channel binds the initial namespaces.
- Missing RPD inputs are correctly classified rc 3, and the format-rejection
  arms do not print rejected values.

Therefore RPD-VERIFY can PASS a manifest whose effective bindings are wrong and
can PASS files reached through the wrong parent or identity context. It does not
yet support the root-side admission claim.

# 4. Independent SELF_QA reproduction

I ran local `bash -n` on both delivered scripts. Both returned rc 0. I then
mechanically extracted the delivered functions with awk, supplied only the
minimum command/predicate stubs needed to reach each arm, and ran nine sampled
arms. The reproduced results were:

| Arm | Reproduced output | Rc | Match |
|---|---|---:|---|
| B1 root caller | `B3_STOP reason=must_run_unprivileged uid=0` | 3 | yes |
| B5 caller in directory group | `B3_STOP reason=caller_in_conf_dir_group path=/etc/mtc-bridge gid=0 caller_gids=[1000 0 27]` | 3 | yes |
| A1 visible boundary name | `B3_FAIL reason=conf_dir_entry_permitted path=/etc/mtc-bridge/mtc-bridge.env stat=[regular file\|600\|root:root] expected=EACCES` | 1 | yes |
| EACCES pass | `B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1` | 0 | yes |
| A4 ENOENT | `B3_STOP reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES` | 3 | yes |
| C3 bad hex charset | `RPD_STOP reason=input_charset name=RPD_CANDIDATE_SHA expected=lowercase_hex` | 3 | yes |
| C7 wrong hex length | `RPD_STOP reason=input_length name=RPD_CANDIDATE_SHA len=8 expected=40` | 3 | yes |
| E2 first binding absent | `RPD_FAIL reason=install manifest does not bind release_sha` | 1 | yes |
| E4 grep tool/read error | `RPD_STOP reason=install_manifest_unreadable path=/tmp/manifest grep_rc=2` | 3 | yes |

I also ran the delivered RPD script with both inputs absent; it reproduced the
documented candidate-input STOP and rc 3. No sampled arm had an output mismatch.

The honesty problem is N1: the evidence does not support the global claim that
all 43 arms were driven. The report itself says multiple accepted arms were not
re-driven. My nine-arm sample does not cure that unsupported count.

# 5. Open items O1-O7

- O1 - must change. ENOENT proves search succeeded and is deviant-state evidence,
  so FAIL is the truthful classification.
- O2 - must change. A missing preregistered input is operator plumbing failure,
  not host deviation; both blocks should emit a reasoned STOP with rc 3.
- O3 - must change. New root-side and boundary code cannot claim no mutation while
  creating temp files, especially with attacker-controlled TMPDIR.
- O4 - accept as-is. The block should classify the observed access result, not
  diagnose whether ACL, MAC, or capability caused it; the scope limitation must
  remain explicit.
- O5 - must change. An unadjudicated `tr` failure violates the binding 0/1/3 rc
  contract and can be misread as a host FAIL.
- O6 - accept as-is. Process, service, and listener state are outside this B3
  permissions/ownership repair and no new claim covers them.
- O7 - accept as-is for this design-only unit. The disclosure is honest and the
  kickoff permits local fixture testing, but an isolated real-Linux root PASS and
  failure-path run is mandatory before operational freeze or deploy use.

Final verdict: REQUEST_CHANGES
