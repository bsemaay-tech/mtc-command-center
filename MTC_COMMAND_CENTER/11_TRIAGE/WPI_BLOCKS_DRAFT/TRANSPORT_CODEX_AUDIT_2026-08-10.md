# VERDICT: REQUEST_CHANGES — 10 required findings

**Tier:** T0. **Applied auditor contract:** fresh independent Codex `gpt-5.6-sol`,
`xhigh`, round 1 of at most 3. Owner amendment A2/A2a was observed: the audit was
performed directly with no sub-delegation. This was a local-only audit; no SSH, SCP,
staging-host, credential, service, broker, exchange, or trading operation was run.
Network use was limited to loopback TCP probe fixtures. The only repository file
written by this audit is this report.

The transport set is not safe to freeze or dispatch. In particular, a STOP returned by
an operation becomes runner rc 1/`TR_RUN FAIL`; the local digest binder cannot accept an
equal remote/local file; PATH-selected fake `ssh` and `sha256sum` programs are accepted;
and `remote_setup_wpi.sh` can allocate through an unbound parent or after an ambiguous
path diagnostic.

## V1–V8 disposition

| Check | Result | Independent evidence |
|---|---|---|
| V1 wrapper contract | **FAIL** | Both wrappers refuse live symlinks before `-f`, and all three sourced children use `</dev/null`; the published RED/GREEN wrapper fixture was re-run and reproduced rc 0 RED / rc 3 GREEN for symlinks and rc 1 RED / rc 0 GREEN for stdin theft. Child rc 3 reaches the runner's per-op `.rc`, but the runner then converts it to overall rc 1 and `TR_RUN FAIL` (F1). Wrapper hashing also trusts inherited PATH (F3). |
| V2 runner and plan | **FAIL** | The 12 operation kinds/order/run conditions otherwise match section 5; first-mismatch skipping and retention of every `always` op reproduced, and every op received `.argv/.stdout/.stderr/.rc/.elapsed_ms`. Ops 11/12 cannot bind equal evidence (F2), STOP is misclassified (F1), program identity is unbound (F3), op 02 has the wrong cwd (F8), and ops 07/08 name a missing stdin file (F9). Windows PowerShell 5.1 parse completed with 0 errors; no `&&`, `||`, or ternary syntax is used. |
| V3 TSV reader | **PASS** | Fresh local fixtures reproduced: clean LF EOF -> `completion=clean_eof`, rc 0; populated unterminated final record -> `plan_unterminated_final_record`, rc 3; directory-as-source hard read error -> distinct `plan_read_error`, rc 3. No partial record reached the parser. |
| V4 row-24 probe | **PARTIAL / not accepting** | Fresh loopback fixtures drove `timeout` -> op rc 0, `connected` -> op rc 1, and malformed/not-evaluable -> op rc 3. The exception-unwrapping code compares the inner `SocketException.SocketErrorCode` with `ConnectionRefused`, as required. Closed loopback ports on this audit host were filtered into `timeout`, so `connection_refused` did not reproduce in this session; SELF_QA's historical output is not independently rerunnable because its exact command is omitted (F10). No false-FAIL route was found in the code-reviewed branch. |
| V5 derivation | **FAIL** | Accepted originals byte-verified at 4976 B / `faee3725...21b5` and 8270 B / `ba0bef0e...3db3`. The setup diff is exactly the permitted prefix constant. The extractor changes executable count predicates outside the permitted archive-constants block (F7). Its member list itself is the six-file WP-I kit and excludes `RP1-B3.sh`. All freeze constants remain inert placeholders. |
| V6 placeholders | **PASS** | All `<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` markers remain literal; no concrete WP-I RUNID was minted. Concrete `WPLP2-...` text in SELF_QA is accepted-source provenance, not a new WP-I allocation. |
| V7 self-QA and falsification | **FAIL** | Wrapper and runner sequencing fixtures reproduced, but most claimed SELF_QA commands are absent, crucial binding functions had no author-executed arm, and fresh adversarial fixtures exposed F1–F6. Coverage details appear under F10. |
| V8 identity and syntax | **PASS** | All eight current files were re-hashed byte-for-byte; the six identities claimed in SELF_QA match. `bash -n` passed on all four in-scope shell files. Windows PowerShell 5.1.26100.8875 parsed the runner with 0 errors. |

## Required findings, most severe first

### F1 — CRITICAL — operation STOP is converted into transport FAIL

`transport_runner.ps1:504-531` treats every rc mismatch alike, emits
`TR_RUN FAIL`, and exits 1. This contradicts its own line 10 contract (rc 3 means an
operation could not be evaluated), Pattern 1, and V1's STOP-first requirement.

Fresh falsification used a one-op local plan whose TCP probe returned a reasoned rc 3
while `expect_rc=0`:

```text
TR_OP_END id=01 rc=3 expect_rc=0 ...
TR_FIRST_FAIL id=01 rc=3 expected=0 later_sequence_ops=skip always_ops=run
TR_RUN FAIL base_run=QA ...
B6_STOP reason=external_probe_not_evaluable outcome=port_invalid rc=3 detail=port_range
RUNNER_RC=1
```

Required repair: retain first-mismatch skipping and all `always` cleanup, but track STOP
separately and return/label rc 3 when an operation or evidence binding was not evaluable.
Define and test precedence when an earlier FAIL and a later cleanup STOP coexist. Supply
an exact D026 RED/GREEN transcript through the whole runner, not only a direct wrapper
invocation.

### F2 — CRITICAL — equal remote/local digest sets cannot bind

`transport_runner.ps1:376-381` captures the remote digest in automatic `$matches`, then
executes more `-notmatch`/`-match` expressions and finally reads `$matches[1]` after it
has been overwritten. The size parser repeats the defect at lines 391-395. Ops 11/12
therefore compare local hashes against a corrupted/null parsed value before reaching
digest-set reconstruction.

Fresh local integration used one LF-terminated close record and one seven-byte local
`file.txt`; both carried SHA-256
`f16d05ec6b29248d2c61adb1e9263f78e4f7bace1b955014a2d17872cfe4064d`:

```text
TR_BIND_COUNTS remote=1 local=1
TR_BIND_DIFF digest_differs=file.txt
TR_OP_END id=03 rc=1 expect_rc=0 ...
```

Required repair: copy every capture (`digest`, `relative path`, `size`) to ordinary local
variables immediately after its grammar match, before running any further regex. Add
literal paste-and-run RED/GREEN fixtures for equal sets, digest mismatch, name-set
mismatch, malformed/incomplete records, unsafe paths, and reconstructed set mismatch.

### F3 — CRITICAL — inherited PATH/environment selects the trusted transport chain

The binding execution-environment rule says inherited PATH, cwd, PYTHONPATH, or TMPDIR
must never select evidence-producing code. The delivered set does the opposite:

- `transport_runner.ps1:229-236,266-279` resolves bare `ssh`/`scp`, merely logs the
  resolution, and starts the bare name without path/hash/metadata binding or a cleared
  environment;
- `run_p0.sh:47` and `run_ro.sh:54` invoke bare `sha256sum` before sourcing the purportedly
  verified blocks;
- `remote_setup_wpi.sh:49-60,73,83-86` and
  `remote_extract_verify_wpi.sh:45-56,70-86,125-164` inherit PATH/TMPDIR and execute bare
  helpers.

Two fresh falsifications against current logic returned false admission:

```text
TR_PROGRAM name=ssh resolved=<QA>\ssh.cmd
FAKE_SSH_EXECUTED
TR_RUN PASS base_run=QA ...
RUNNER_RC=0
```

```text
ACTUAL_BLOCK_SHA=59407cce...57cf3 EXPECTED=aaaaaaaa...aaaaaaaa
P0W_block path=<QA>/RP6-P0.sh sha256=aaaaaaaa...aaaaaaaa
P0_HIJACKED_BLOCK_EXECUTED
WRAPPER_RC=0
```

Required repair: pin and verify the absolute Windows OpenSSH programs and every remote
helper by non-following kind, numeric ownership, non-writable mode, and frozen identity as
the binding requires; execute from fixed trusted cwd under a deliberately constructed
environment and run-owned TMPDIR. Re-run both attacks as D026 RED/GREEN.

### F4 — HIGH — ambiguous path failure is classified as absence and authorizes mutation

`remote_setup_wpi.sh:47-64` and the duplicate extractor helper flatten diagnostics with
`tr` and accept any text containing `No such file or directory` as positive absence.
They do not reject multiline/mixed diagnostics or observe an errno class. This violates
Patterns 1, 5, and 6 plus the structured-input rule.

Fresh falsification made the path probe return rc 1 with both ENOENT and EACCES text. The
current setup classified it absent, created all four directories, and returned PASS:

```text
SETUP_NOTE base_absent path=<QA>/wpi_staging_SAFE
SETUP PASS base=<QA>/wpi_staging_SAFE ...
SETUP_RC=0 BASE_CREATED=yes
```

Required repair: use a pinned interface that exposes the actual error class; ambiguous,
multiline, unreadable, or unclassified failure must STOP before `mkdir`. Apply the repair
to both copies and provide exact mixed-diagnostic RED/GREEN evidence.

### F5 — HIGH — setup binds the path after mutation and compares resolver names

`remote_setup_wpi.sh:78-110` creates the entire tree before canonicalizing it, checks only
the final component during the pre-allocation probe, and compares `%U:%G` with the names
`gatea:gatea`. Section 1 requires the P0-resolved numeric euid:egid, with names diagnostic
only; Pattern 3 requires binding the component chain before mutation; Pattern 8 forbids
resolver names as identity.

Fresh parent-symlink falsification produced:

```text
SETUP_NOTE allocated path=<QA>/link/wpi_staging_SAFE/kit
SETUP_FAIL reason=path_not_canonical ... canonical=<QA>/real/wpi_staging_SAFE
SETUP_RC=1 MUTATED_REAL_DIR=yes
```

The refusal arrived only after four directories had been created through the symlink.
Required repair: bind the full parent chain and accepted mount object before allocation,
then compare numeric owner/group with the frozen/P0-resolved values. Add a load-bearing
parent-symlink RED/GREEN fixture and numeric-NSS-alias fixture. Also replace inherited
`mktemp` use so the claim about the mutation set is truthful.

### F6 — HIGH — extractor interprets listing stdout before complete diagnostics/read completion

`remote_extract_verify_wpi.sh:81-120` captures only stdout from both tar listings. Stderr
is neither captured nor required empty, and command substitution removes original trailing
newlines before here-doc loops manufacture new ones. The implementation therefore cannot
prove diagnostic-free completion or the line-reader completion state required by Patterns
6 and 7.

Fresh six-member archive falsification used a listing helper that emitted a warning to
stderr while returning the correct list and rc 0. Current bytes returned:

```text
FAKE_TAR_WARNING: listing incomplete is possible
FAKE_TAR_WARNING: listing incomplete is possible
EXTRACT PASS ... members=6 verified=6 executed=0
EXTRACT_RC=0
```

Required repair: capture raw listing stdout, stderr, rc, elapsed time, and final-record
state independently; STOP on any diagnostic, incomplete record, timeout, invocation, or
read error before parsing member content. Provide warning-bearing, unterminated, and hard
read-error RED/GREEN cases.

### F7 — HIGH — extractor is not the section-4 minimal derivation

The accepted source identities are correct, and `remote_setup_wpi.sh` changes only its
prefix constant. The extractor does not satisfy
`WPI_PREREGISTRATION_DRAFT.md:223`, which permits only the archive-constants block
(bytes, member list, per-member digests). In addition to that block, current bytes change
executable count predicates at `remote_extract_verify_wpi.sh:100,114,141` and the emitted
PASS/count result at lines 120 and 170. SELF_QA lines 59-60 silently broaden the contract
to include count literals and result text; it cannot override the binding preregistration.

Required repair: either restore an exactly permitted derivation or explicitly amend and
re-audit the binding derivation contract before changing source. The final diff must make
the permitted semantic boundary mechanically unambiguous. Keep the exact six-member WP-I
set and exclusion of `RP1-B3.sh`.

### F8 — HIGH — op 02 violates the binding working directory

Binding section 5 line 304 requires SCP-up of bare `runkit.tar` with cwd `01_RUNKIT`.
`TRANSPORT_PLAN.tsv:3` instead uses `WPI_BLOCKS_DRAFT`, and
`transport_runner.ps1:25-27,33-35` also locates the pinned archive in that draft directory.
This is not a placeholder and will survive freeze.

Required repair: make plan cwd and archive pin source match the frozen `01_RUNKIT`
location (or amend the binding before implementation), then test that a decoy same-name
archive in the draft directory cannot be selected.

### F9 — HIGH — ops 07/08 name an absent executed artifact

`TRANSPORT_PLAN.tsv:8-9` supplies `remote_close_tree.sh` on stdin, and runner lines
201-215 resolve every stdin file only under `$PREREG_DIR`. That file is absent from
`WPI_BLOCKS_DRAFT`; after pins are filled the runner must STOP
`stdin_file_missing op=07` before execution. The accepted original does exist and was
independently verified at 7470 B / `87157f0e...f3f0e`, but SELF_QA hashes it only at the
old Stage-2 path. STATUS lines 11-12 inaccurately present it as part of the current op set.

Required repair: assemble a byte-identical copy at the exact path the frozen runner uses,
or change and pin the plan/runner to its real immutable location. Add it to package
enumeration and preflight QA; prove both identity and absence refusal.

### F10 — HIGH — SELF_QA is not literal D026 evidence and omitted the broken safety path

`SELF_QA_TRANSPORT.md:12-13` says the commands are complete paste-and-run commands, but
sections 4-8 provide prose plus claimed output without the executable commands. The only
recorded runner RED mutation is first-FAIL sequencing; there is no remote/local binding
fixture at all. This is exactly Pattern 10 and is material: the first independent local
binding execution exposed F2.

Functions with no author-recorded executed arm are:

- `transport_runner.ps1`: `Get-Sha256OfText`, `Test-Ascii`,
  `Invoke-ExternalProcess`, `Read-RemoteCloseRecord`, and `Invoke-LocalBind`;
- `remote_setup_wpi.sh`: `stop`;
- `remote_extract_verify_wpi.sh`: `stop`.

`Test-Ascii` has no caller in the runner. The author explicitly left the TCP timeout arm
undriven. This auditor drove `Invoke-ExternalProcess`, `Read-RemoteCloseRecord`,
`Invoke-LocalBind`, and the timeout arm; F2 prevented `Get-Sha256OfText` from being reached.
`Test-Ascii` remains dead, the two support-script STOP functions have no recorded fixture,
and `connection_refused` did not freshly reproduce on this host. STATUS lines 15-19 must
not claim blanket PASS while these gaps and F1/F2 remain.

Required repair: provide exact standalone commands and real output for every claimed
fixture, including each new regression's actual RED mutation/pre-fix behavior and GREEN
fixed behavior. Add function/arm coverage accounting and classify anything not executed
as supplemental, never PASS evidence.

## Re-derived identities

| File | Bytes | SHA-256 | Claim check |
|---|---:|---|---|
| `run_p0.sh` | 3693 | `8b2c520aa342f3f49fc9f0ad543b6c8a918c995b66e1cae8a1dd1c543b9dbfe9` | matches SELF_QA |
| `run_ro.sh` | 4407 | `88f9f736e68c4978cc15d29621082d0395dc49de97a4c8efc79893fc536ad3e0` | matches SELF_QA |
| `transport_runner.ps1` | 28946 | `84942683a6c25973f1785e48dc8ed76aea99be27c9ee50bf1ed5f7726b518cdc` | matches SELF_QA |
| `TRANSPORT_PLAN.tsv` | 4575 | `bcc10a6a71456580a93eb0da6c1f9bc03da154ae59cf14a0821e6b8bd6edd3b5` | matches SELF_QA |
| `remote_setup_wpi.sh` | 4973 | `5b2598184b228eef5d93c7f4ef7a5aa8a627ffbdea8c71e6cc093b416ebb0a34` | matches SELF_QA |
| `remote_extract_verify_wpi.sh` | 7689 | `17ed8f3f8d80a79fc1b132ff1ef55cf0677da13c551da30e0db7531935c1f6f2` | matches SELF_QA |
| `SELF_QA_TRANSPORT.md` | 18602 | `13b8204a835922824b1af817752f879be5b7b54c14d5095073a64877c7ba6cb4` | no prior claim |
| `STATUS_TRANSPORT.md` | 1103 | `89d4b99fb382b22777e94700cc63f794cbd10b711a8286b86e71d3096aede7c9` | no prior claim |

Accepted derivation sources:

| File | Bytes | SHA-256 |
|---|---:|---|
| `02_PREREG/remote_setup.sh` | 4976 | `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5` |
| `02_PREREG/remote_extract_verify.sh` | 8270 | `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3` |

## Required next action

Do not freeze, allocate identifiers, contact the host, or dispatch this set. Return all
10 findings to the same implementer for one bounded T0 repair round. The repair must
include literal D026 RED/GREEN evidence, after which both mandatory fresh T0 flagship
slots must audit the same final bytes at xhigh. This report is non-accepting and supplies
no host, freeze, execution, or Git authority.
