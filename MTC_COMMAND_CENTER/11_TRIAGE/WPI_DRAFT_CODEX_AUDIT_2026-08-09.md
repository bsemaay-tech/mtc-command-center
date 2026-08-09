REQUEST_CHANGES

# AUDIT REPORT - CODEX

## Required findings

### F1 - B1 can turn unreadable distribution metadata into a parity FAIL

Severity: HIGH

File and line: `WPI_PREREGISTRATION_DRAFT.md:359-374`;
`WPI_CHECK_FEASIBILITY.tsv:13`; `SELF_QA.md:92-101,300-306`.

Concrete failure scenario: the venv root and every directory below it are searchable,
so `find` completes with zero permission diagnostics, but one regular file such as
`site-packages/pkg.dist-info/METADATA` is mode `000`, has a named ACL denying `gatea`,
or is denied to the Python process by an LSM rule. `find` can stat the file without
reading its contents, so row 14 holds. `verify_lock.py --check-installed` then cannot
read that distribution's metadata. A metadata library may omit the distribution or
the verifier may return a generic nonzero rc. Row 19 maps a generic nonzero rc to
`B1_FAIL reason=lock_installed_parity`; its STOP is conditional on an unreadable path
being positively identified. The draft therefore can report package drift when the
unprivileged process merely could not evaluate the package set. The claimed row-14
guard does not prove regular-file readability.

Minimal fix: before interpreting parity, prove that every metadata object consumed by
the verifier is readable by `gatea`, or change the wrapper/verifier contract so every
open, parse, permission, and traversal error is distinguishable from a genuine set
mismatch. Any such error must produce B1_STOP. Preregister and demonstrate that error
adjudication; do not let a generic verifier rc become B1_FAIL.

### F2 - B6 is not bound to the service network namespace

Severity: HIGH

File and line: `WPI_PREREGISTRATION_DRAFT.md:363-365,398-403`;
`WPI_CHECK_FEASIBILITY.tsv:19`; `SELF_QA.md:178-189`.

Concrete failure scenario: PAM, an ssh ForceCommand, or a service wrapper places the
`gatea` login in a private network namespace while PID 1 and the bridge remain in the
host namespace. `ss -ltn` succeeds without a permission error but sees only the login
namespace. It can return no port 8790 listener, causing row 22 to emit B6_FAIL even
though the bridge is correctly listening in the service namespace. Conversely, a
matching listener in the login namespace could conceal a bad listener set in the
service namespace and create a false PASS. Tool presence and unprivileged socket
visibility do not establish namespace identity.

Minimal fix: before interpreting `ss`, bind the probe namespace to the namespace of
the running unit, for example by comparing the probe network-namespace identity with
the unit MainPID network-namespace identity. If that comparison is inaccessible or
different, STOP. If unprivileged `gatea` cannot establish the binding, move this half
to an appropriately authorized channel.

### F3 - B2 and B4 can classify system-manager access failure as host drift

Severity: HIGH

File and line: `WPI_PREREGISTRATION_DRAFT.md:324-336,342-350,405-407`;
`WPI_CHECK_FEASIBILITY.tsv:15,17`; `SELF_QA.md:116-122,157-166`.

Concrete failure scenario: `gatea` is denied access to the system bus by a D-Bus or
polkit policy, `systemctl` is absent, or the login is placed in a PID/mount namespace
where the system manager is unavailable. `systemctl is-active`, `show`, or `cat` then
fails before returning unit state. Rows 1-5 and 8-9 provide only B2_FAIL/B4_FAIL result
divergences. The general STOP list at lines 405-407 does not include `systemctl`.
Thus an empty/error result can be rendered as `unit_not_active`, missing candidate
binding, or property mismatch rather than could-not-evaluate.

Minimal fix: add `systemctl` and system-manager query readiness to P0, and specify for
every systemctl probe that invocation, bus, namespace, authorization, and parse errors
STOP before output is compared. Preserve evaluable states such as a successful
`is-active` response of `inactive` as FAIL; do not classify solely by numeric rc.

### F4 - B3 can inspect partial `find` output before adjudicating walk failure

Severity: HIGH

File and line: `WPI_PREREGISTRATION_DRAFT.md:351-355,367-374,405-407`;
`WPI_CHECK_FEASIBILITY.tsv:16`; `SELF_QA.md:79-101,133-155`.

Concrete failure scenario: the venv contains a world-writable file encountered early
and, later in traversal order, a directory with a named ACL denying `gatea`. The
`find ... -perm /222` command emits the writable pathname, then emits EACCES and exits
nonzero. Row 12 precedes row 14 and the draft does not require the command rc and all
diagnostics to be adjudicated before its stdout is interpreted. A wrapper can
therefore emit B3_FAIL for the writable path even though the sweep was incomplete and
the correct first outcome is B3_STOP. The same issue exists for any partial walk
followed by an LSM, ACL, mount, or traversal error.

Minimal fix: make each sweep atomic for adjudication: capture stdout, stderr, rc, and
elapsed time; first STOP on timeout or any probe/traversal error; only after a complete
rc-0 walk may stdout be inspected for writable paths and produce FAIL. State this
ordering in the expectation table and frozen-block acceptance criteria.

### F5 - Hash rows omit their earlier could-not-read divergence

Severity: MEDIUM

File and line: `WPI_PREREGISTRATION_DRAFT.md:346-348,358,405-407`;
`WPI_CHECK_FEASIBILITY.tsv:14-15`.

Concrete failure scenario: the installed `requirements.lock`, or a parent below the
recorded `0555` release root, has a named ACL denying `gatea`; alternatively the unit
fragment remains mode `0644` but a parent directory or LSM policy denies direct read.
`sha256sum` fails before producing a digest. Rows 7 and 17 name only digest-mismatch
FAILs as the exact predicted first divergence. The later generic sentence says a
sha256sum error STOPs, but it neither gives the exact row-specific divergence nor
states that rc/stderr is adjudicated before comparing possibly empty output. The
table's claimed exact first divergence is therefore incomplete.

Minimal fix: add explicit B2_STOP and B1a_STOP forms for hash open/read/execute errors,
and require successful rc plus a syntactically valid digest and byte count before a
digest mismatch may be reported as FAIL.

### F6 - The draft gives a technically complete path to dispatch while authority remains absent

Severity: MEDIUM

File and line: `WPI_PREREGISTRATION_DRAFT.md:19-23,276-278,583-585`.

Concrete failure scenario: Stage 1 freezes the blocks, the two pins are filled, and
identifiers are allocated, but no authority or budget lift has been granted. Lines
19-23 say that three things must happen before a successor is dispatchable, and lines
276-278 describe the two execution switches. An operator can read those statements
as an exhaustive dispatch gate even though lines 583-585 separately say the run is
authority-blocked and budget-blocked.

Minimal fix: say the three listed items are necessary but not sufficient. Add explicit
written host-contact/transport authority and the required budget lift to the dispatch
gates, and state that `-Execute` and `-Confirm` are technical interlocks, not authority.

## Answers to the four audit questions

### 1. Unprivileged feasibility, attacked

- A3 is local-static and ALREADY-BANKED, so it has no unprivileged host probe.
- B1: a noexec mount, missing execute bit, or exec-denying LSM can prevent Python from
  starting. Row 18 now correctly calls an actual exec denial STOP. However unreadable
  distribution metadata can survive the `find` guard and become a parity FAIL. This is
  required finding F1.
- B1a INCLUDE half: an ACL, unreadable regular file, inaccessible lower parent, or LSM
  denial can prevent hashing. The generic rule says STOP, but row 17's exact divergence
  omits it. This is required finding F5. The manifest half is correctly DEFER-ROOT-SIDE.
- B2: missing `systemctl`, denied system-bus access, namespace isolation, inaccessible
  unit search paths, ACLs, or LSM denial can prevent evaluation. Several rows would
  become FAILs. This is required finding F3; direct hash/read error coverage is also
  incomplete under F5.
- B3 INCLUDE half: a named ACL or inaccessible nested mount can defeat traversal even
  when the root reports `0555`; missing search permission on the log parent can defeat
  terminal stat. The draft generally calls these STOP, but partial `find` output can
  be interpreted first. This is required finding F4. Children of the three protected
  metadata directories are correctly DEFER-ROOT-SIDE.
- B4: denied system-bus/polkit access or a different manager namespace prevents the
  property query and can be mislabeled property drift. This is required finding F3.
- B5: missing `curl` is caught by P0; auth failure, HTTP failure, schema mismatch, and
  curl probe errors are specified as STOP. An executable-denying ACL, noexec mount, or
  LSM denial after `command -v` must be treated by the generic curl-error STOP. No
  false-FAIL defect is established here, provided the frozen block enforces that rule.
- B6: missing/denied `ss` is covered by the generic STOP rule, and `ufw` is correctly
  DEFER-ROOT-SIDE. A successful probe in the wrong network namespace is not covered
  and can create false FAIL or false PASS. This is required finding F2.

### 2. Expectation table soundness

The table is not sound enough to claim exact first divergences. Conditional on the
host states above:

- Row 19's parity FAIL is preceded by an unreadable-metadata STOP that the current
  guard cannot reliably detect.
- Rows 1-5 and 8-9 have a system-manager invocation/access error before any unit-state
  or property comparison.
- Row 12 can consume partial output before row 14 reports the walk error, making the
  stated FAIL reachable only by violating STOP-first ordering.
- Rows 7 and 17 have an open/read/hash error before any digest mismatch exists.
- Row 22 may be evaluating the wrong namespace, so its stated listener divergence is
  not a divergence of the service host state at all.

These are not merely alternate observations; they are earlier inability-to-evaluate
conditions. The successor must define probe-error precedence before result comparison.

### 3. Template parity and immutability

The draft carries the template's one-use RUNID burn rule, create-once remote and local
roots, first-FAIL sequencing, separate close invocation, double-pass closed-tree hash,
remote-versus-local binding, pinned route/argv, and fresh-preregistration void rules.
It also keeps the reused support scripts byte-identical with an explicit disposition.

The practical three-outcome discipline is weaker than the stated contract because
F1-F5 leave paths by which probe inability can become FAIL or an observation from the
wrong namespace can be accepted. F6 also makes the dispatch prerequisite list looser
than the document's own final authority/budget blocker. These are required repairs;
the remaining named immutability elements are present.

### 4. Placeholder and authority discipline

No new concrete one-use RUNID, unit id, remote base, or record root is minted. The
concrete B3 RUNID and prior record roots are historical references used for burn and
collision rules. The candidate SHA and accepted artifact hashes are inputs, not new
one-use identifiers.

No Group C check has executable form in the block table, operation table, expectation
table, or conditional plan. Command names in the blocked prose describe forbidden
future work and do not constitute executable argv.

The document repeatedly says it grants no authority, but F6 is a real authority-
discipline defect because its short dispatch checklist omits the authority and budget
lifts that the same document says are still absent.
