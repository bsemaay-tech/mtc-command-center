Status: DRAFT V2 — NOT COMMITTED, NOT SPENT

# Stage-1 Commit 1 — read-only attestation-only preregistration, version 2

Date: 2026-08-15  
Audit tier: T2 documentation/evidence  
Disposition: complete V2 draft; **not Commit 1 and not dispatchable** because the exact root-channel launch and the category-1 mutation-denial/crossover facts identified below remain `UNKNOWN`.

## 0. Review-finding disposition

| Review finding | V2 disposition | Where V2 closes or carries it |
|---|---|---|
| F1 — authority-bearing argv, environment, cwd, and process chain | **CARRIED AS A COMMIT BLOCKER, not guessed.** The sources grant a root session but do not establish its SSH principal, account shell, forced-command/wrapper mapping, pre-`env` environment, initial cwd, descriptor set, or mutation-denial wrapper. The later transport plan establishes only the unprivileged `gatea@172.24.55.233` route. | Sections 4.3, 5, and 8.1 define the one required binding record and the exact literal expansion rule. Until that record exists, `ATT-01_OUTER_ARGV`, `ATT-01_TARGET_PROCESS_CHAIN`, and `ATT-01_INITIAL_CWD` are `UNKNOWN`, the recorder exits before record creation, and this draft may not be committed as Commit 1. This accepts the review finding rather than silently filling it. `C:\tmp\lane_out\W2_PREREG_REVIEW.md:31-37`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:32-35`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:2` |
| F2 — no-mutation/no-trace | **REJECTED IN PART under the Lead adjudication; retained in part.** The review merged category 1 target mutation with category 2 inherent infrastructure records. Category 2 is disclosed and is not a blocker. Category 1 remains strict. | Sections 2 and 3 define the split, disclose expected sshd/PAM/auditd/wrapper/atime records, and keep log rotation, out-of-store audit actions, hooks, content/configuration writes, and runtime write capability as category-1 blockers. `C:\tmp\lane_kick\X3B.md:24-48`; `C:\tmp\lane_out\W2_PREREG_REVIEW.md:39-45` |
| F3 — no packaged operator recorder | **CLOSED IN DESIGN.** | Sections 8–10 package one recorder and one deterministic launcher, fix their paths, interpreter, argv, child environment, cwd, stream handling, create-once path, collision response, fsync/close policy, and failure grammar. The recorder is the normative source in section 9. `C:\tmp\lane_out\W2_PREREG_REVIEW.md:47-53` |
| F4 — non-canonical operator record | **CLOSED IN DESIGN.** | Section 8.5 fixes ASCII/LF/final-LF bytes, canonical decimals, 40-lowercase-hex SHA-1 object IDs, RFC 4648 base64 with padding and no wrapping, literal status tokens, the exact child path, and create-once collision behavior. The serializer is implemented in section 9. `C:\tmp\lane_out\W2_PREREG_REVIEW.md:55-59` |
| F5 — fillers lack exact source path/field | **SOURCE CONTRACT CLOSED; VALUES NOT YET AVAILABLE.** | Section 4 names exactly three future committed TSV sources, every exact field, grammar, Git-blob binding, and verbatim-copy rule. Their current blob OIDs and concrete values are `UNKNOWN`, because the allocation and fresh candidate-bound staging records do not exist. Therefore this V2 remains a draft. `C:\tmp\lane_out\W2_PREREG_REVIEW.md:61-67`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:43,66-70` |
| F6 — MainPID not capture-time bound | **CLOSED IN DESIGN.** | Sections 6.2–6.6 and the producer in section 7 open a pidfd, require it non-readable before and after observation, compare two complete `/proc/<pid>` snapshots, bind start-time ticks to the exact checkpoint, require candidate-specific cwd and command line, bind executable path/digest and network namespace, and STOP on absence, exit, exec/reuse, drift, or unreadability. `C:\tmp\lane_out\W2_PREREG_REVIEW.md:69-73`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:950-976` |
| F7 — clean-current-HEAD rule is not executable or singular | **CLOSED IN DESIGN.** | Section 8.3 gives one ordered command table with an exact `(rc, stdout, stderr)` acceptance tuple for every subprocess check. `COMMIT_1` is derived once and every later object lookup uses only `COMMIT_1`; no later command uses `HEAD`. Section 9 implements the table and fails before record creation and before the socket. `C:\tmp\lane_out\W2_PREREG_REVIEW.md:75-79` |

The review's NOTE that the visible target payload is attestation-only is accepted. No WP-I transport operation 01–12 is imported here. `C:\tmp\lane_out\W2_PREREG_REVIEW.md:96-106`

## 1. Purpose, authority, and hard boundary

Commit 1 exists only to bind one later grant-#6 observation to exact committed bytes. The two-commit order is mandatory: allocate locally; create Commit 1; perform the exact read-only capture; close and hash its operator record; then create Commit 2 from the captured values. No WP-I op 01–12 may run between Commit 1 and Commit 2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:488-533`

The owner authorized only the exact preregistered and committed read-only grant-#6 capture and later named WP-I operations on `GATEA-STAGING`, using the pinned identity solely for those actions. The grant is conditional on Commit 1 and the allocation record and excludes every other host, credential, write, deployment, broker/exchange, ARM, order, TESTNET/mainnet, and merge-to-master action. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-60`

This document preregisters only `ATT-01`. It does not authorize or specify a deployment, service operation, remote allocation, upload, extraction, WP-I predicate, broker/exchange contact, ARM action, order, TESTNET/mainnet action, Pine/parity/MTC/trading change, merge, push, or economic action.

## 2. The controlling category split

### 2.1 Category 1 — target mutation

For this preregistration, category 1 means any effect, other than the narrowly enumerated category-2 records below, that creates, deletes, renames, modifies, truncates, changes permissions/ownership/xattrs, rotates, moves, or reconfigures content or persistent configuration on `GATEA-STAGING`.

Category 1 must be impossible for each command and must be demonstrated before Commit 1. Source inspection alone proves only that the visible producer requests read-only operations; it does not prove the interpreter, loader, account shell, root wrapper, PAM hooks, audit rules, or failure paths cannot mutate. The defect catalogue requires the claim sentence to stay within the predicate and requires the executed instrument, not merely a declared instrument, to be bound. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:547-613,817-849`

Current category-1 status:

| Surface | Required demonstration | Current fact |
|---|---|---|
| Target producer source | No write/create/delete/rename/chmod/chown/xattr/mount/service/socket/subprocess API; file opens are read-only; only fd 1/2 are written. | Demonstrated by the normative source in section 7. |
| Python, loader, and standard-library runtime before and during the producer | Exact runtime identity plus an enforced control that denies content/configuration mutation on success and every failure path while allowing inherited stdout/stderr. | `UNKNOWN`. No source establishes the exact enforcement control. |
| Account shell, forced command, sudo/root wrapper, or equivalent pre-`env` chain | Exact chain and a demonstrated no-mutation contract for each process before `env -i`. | `UNKNOWN`. The grant names a root session but not its mechanism. |
| Native auth/audit record rollover | The bounded category-2 append must not trigger log rotation, journal vacuum/rotation, audit rule action outside its native store, or another content/configuration mutation. | `UNKNOWN`. This is a plausible category-2-to-category-1 crossover and therefore blocks Commit 1. |
| PAM/root-wrapper hooks | No hook may create a home object, refresh credentials, update an unrelated database, execute a profile, or invoke another side-effecting program. | `UNKNOWN`; blocks Commit 1. |

No operator may convert an `UNKNOWN` in this table into a claim of impossibility. A final Commit 1 must cite one exact committed root-channel binding/proof record that closes every row.

### 2.2 Category 2 — inherent infrastructure records

The following records are inherent to the owner's authorized use of the pinned SSH identity. They are disclosed, not claimed absent, and are not blockers by themselves:

| Subsystem | Expected record from an authorized read-only session | Exact host implementation |
|---|---|---|
| `sshd` / system journal or auth log | Connection attempt and success/failure, authenticated principal/key identity or fingerprint as configured, source endpoint, session open/close, and possibly the requested command. | Exact backend, fields, path, retention, and verbosity are `UNKNOWN`. |
| PAM | Authentication/account/session module records and session-open/session-close accounting when the configured stack emits them. | Exact module stack and stores are `UNKNOWN`. |
| `auditd` / kernel audit | Login/session/user-command/syscall records selected by installed audit rules. | Whether enabled, the exact rules, store, and record set are `UNKNOWN`. |
| Root wrapper / `sudo` / forced command | Invocation and policy decision records produced by the exact root-channel mechanism. | The mechanism itself is `UNKNOWN`. |
| Login accounting | `wtmp`, `btmp`, `lastlog`, journal equivalents, or other native login accounting when enabled. | Which stores are enabled is `UNKNOWN`. |
| Filesystem metadata | Access-time metadata that the active mount/filesystem policy may update because the interpreter, libraries, `/proc` objects, executable, and observation inputs are ordinarily read. | Mount atime policy and which reads update it are `UNKNOWN`. |

These bounded records are consistent with the permission because the permission expressly authorizes use of the pinned identity for the exact capture on `GATEA-STAGING`; they are evidence that the authorized login/read occurred, not producer-directed host content/configuration work. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:35-58`

The disclosure is not a waiver for crossovers. A native log append is category 2; a rollover/rotation/vacuum caused by it, an audit rule writing outside its native audit store, a PAM hook changing unrelated state, or a wrapper updating configuration is category 1 and must be denied or proven impossible before Commit 1. `C:\tmp\lane_kick\X3B.md:39-48`

## 3. Command-by-command target-mutation adjudication

| Command/operation | Location | Category-1 capability and required proof | Category-2 disclosure |
|---|---|---|---|
| All `git` commands in section 8.3 | Operator | No target contact. Commands are read-only; `git hash-object` is used without `-w`. | None on target. |
| Local manifest hashing and record creation | Operator | Writes only the exact create-once operator record outside the repository. No target contact. | None on target. |
| Windows `ssh.exe` client | Operator | Opens only the one authorized connection after all local gates. It must not enable forwarding, proxy, control persistence, agent forwarding, X11, or local commands. | The connection is expected to create native auth/session/accounting records described in section 2.2. |
| Target `sshd` → account shell/forced command/wrapper → `env` chain | Target | Exact chain and mutation-denial proof are `UNKNOWN`; Commit 1 is blocked. Native log rotation, audit out-actions, and side-effecting hooks remain category 1. | Bounded native sshd/PAM/audit/wrapper/login records are disclosed. |
| `/usr/bin/env -i` and Python startup | Target | Exact executable identities and a mutation-denial control must be bound before Commit 1. `-I -S -B`, an empty Python environment except the fixed entries, and no current-directory import are necessary but not a substitute for enforcement. | Ordinary executable/library-read atime may occur. |
| `chdir('/')` | Target | Process-local cwd only; it does not modify a target object. | None beyond any access metadata inherent to lookup. |
| `readlink`, `realpath`, `lstat`, `stat`, pidfd open/poll | Target | The producer exposes no mutation API. Runtime enforcement is still required. | Ordinary read/access metadata may occur. |
| `open`/`read` of the resolved interpreter, `/proc/self/mountinfo`, and `/proc/<MainPID>/{stat,cmdline}` | Target | All opens are `O_RDONLY|O_CLOEXEC`, and the interpreter adds `O_NOFOLLOW`. No create/truncate/append/read-write flag exists. Runtime enforcement is still required. | Ordinary read/access metadata may occur. |
| In-process parsing, SHA-256, base64, and projection construction | Target | Memory-only; no subprocess, socket, service, or filesystem mutation API. | None. |
| `os.write` to inherited fd 1/2 | Target channel | The source permits only inherited stdout/stderr. The binding record must prove the descriptor mapping and deny extra inherited writable descriptors. | Channel/accounting records are disclosed. |

## 4. Exact pre-Commit-1 input sources

The final Commit-1 builder may consume only the three exact committed TSV sources below. Each source must be ASCII, LF-only, final-LF, have exactly one header plus one data row, have no duplicate key/path, and be proved from clean current `HEAD` by `(rc=0, stdout=<40-lowercase-hex>+LF, stderr=empty)` for both its commit and blob. Each copied value is byte-for-byte; no trimming other than the single TSV field boundary, case folding, independent typing, or target discovery is allowed.

The paths are fixed now; their concrete values and blob OIDs are `UNKNOWN` because the records do not exist. The reconciliation expressly says the allocation, Commit 1, capture, and final identities do not exist. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:43,58-70`

### 4.1 Allocation source

Exact path: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_ALLOCATION/STAGE1_ALLOCATION_RECORD.tsv`  
Current Git blob OID: `UNKNOWN`

Required fields and grammar:

| Field | Grammar / exact relationship |
|---|---|
| `ATTESTATION_RECORD_ID` | `WPI-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}-ATT-01` |
| `BASE` | `WPI-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}` and exact prefix of `ATTESTATION_RECORD_ID` |
| `P0_RUNID` | `<BASE>-P0` |
| `RO_RUNID` | `<BASE>-RO` |
| `REMOTE_BASE` | `/home/gatea/wpi_staging_<BASE>` |
| `CONFIRM_TOKEN` | `<BASE>-EXECUTE` |
| `OPERATOR_RECORD_ROOT` | `C:\WPI_ARTIFACTS\WPI_TRANSPORT_<BASE>` |
| `OPERATOR_RECORD_PATH` | `<OPERATOR_RECORD_ROOT>\attestation\<ATTESTATION_RECORD_ID>.record` |
| `OPERATOR_RECORD_PARENT_STATE` | literal `EXISTS_EMPTY_CREATE_ONCE` |
| `COLLISION_RESULT` | literal `NO_COLLISION_ALL_CANONICAL_SOURCES` |
| `ALLOCATION_DISPOSITION` | literal `RESERVED` |

The operator path is derived once, not independently typed. A missing parent, nonempty attestation directory, existing output path, junction/symlink/reparse redirect, or collision is pre-record `STOP`; the recorder neither overwrites nor deletes anything.

### 4.2 Candidate/checkpoint source

Exact path: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_ALLOCATION/STAGE1_CANDIDATE_BINDING.tsv`  
Current Git blob OID: `UNKNOWN`

Required fields and grammar:

| Field | Grammar / exact relationship |
|---|---|
| `STAGING_HOST` | literal `GATEA-STAGING` |
| `CHECKPOINT_ID` | literal `STAGE1_EXACT_CANDIDATE_A0_A9_FINAL` |
| `WPI_CANDIDATE_SHA` | exactly 40 lowercase hex |
| `UNIT_NAME` | literal `mtc-bridge-first-start.service` |
| `UNIT_ACTIVE_STATE` | literal `active` |
| `UNIT_NRESTARTS` | literal `0` |
| `WPI_MAINPID` | canonical positive decimal, no leading zero |
| `WPI_MAINPID_STARTTIME_TICKS` | canonical positive decimal, no leading zero, field 22 from the complete LF-terminated `/proc/<pid>/stat` record at the named checkpoint |
| `WPI_MAINPID_CWD` | `/opt/mtc-bridge/releases/<WPI_CANDIDATE_SHA>/IBKR_PAPER_BRIDGE` |
| `WPI_MAINPID_CMDLINE_SHA256` | SHA-256 of exact bytes `/opt/mtc-bridge/venvs/<sha>/bin/python\0-m\0bridge.app\0`; 64 lowercase hex |
| `WPI_MAINPID_EXE_PATH` | exact absolute `/proc/<pid>/exe` link result at the checkpoint; ASCII, no whitespace, no ` (deleted)` suffix |
| `WPI_MAINPID_EXE_SHA256` | SHA-256 of that exact regular executable; 64 lowercase hex |
| `WPI_MAINPID_NET_NS` | `net:[<positive-decimal>]` |

Freshness is identity-based, not inferred from a timestamp: the capture must open a pidfd for the exact PID, observe the same start-time ticks, candidate-specific cwd and command line, executable path/digest, and network namespace twice, and keep the pidfd non-readable throughout. Any mismatch means the named checkpoint subject is absent, exited, exec-changed, reused, or otherwise not bound; outcome is STOP.

The accepted RP7 predicate already binds `MainPID`, `WorkingDirectory`, and candidate-specific `ExecStart`; this capture adds the missing live kernel-process binding. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:950-976`

### 4.3 Root-channel and mutation-boundary source

Exact path: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_ALLOCATION/STAGE1_ROOT_CHANNEL_BINDING.tsv`  
Current Git blob OID: `UNKNOWN`

Every field below must be concrete before Commit 1:

| Field | Required content |
|---|---|
| `POWERSHELL_EXE_PATH` / `POWERSHELL_EXE_SHA256` | exact operator launcher executable path and 64-lowercase-hex digest |
| `OPERATOR_PYTHON_PATH` / `OPERATOR_PYTHON_SHA256` | exact recorder interpreter path and 64-lowercase-hex digest |
| `GIT_EXE_PATH` / `GIT_EXE_SHA256` | exact clean-gate executable path and 64-lowercase-hex digest |
| `SSH_EXE_PATH` / `SSH_EXE_SHA256` | exact operator executable path and 64-lowercase-hex digest |
| `SSH_TARGET` | exact principal and address consumed by OpenSSH |
| `SERVER_AUTHORIZED_KEY_BINDING` | exact committed proof that the pinned identity maps to that principal and only the preregistered route |
| `ACCOUNT_UID_GID` | exact numeric `0:0` if direct root, or the exact pre-root identity plus separately bound escalation step |
| `ACCOUNT_SHELL_PATH` / `ACCOUNT_SHELL_SHA256` | exact shell used by sshd for the command, even when a wrapper is present |
| `FORCED_COMMAND_MODE` | exactly `NONE` or `EXACT`; `EXACT` requires the full byte-exact forced command/wrapper argv |
| `ROOT_WRAPPER_PATH` / `ROOT_WRAPPER_SHA256` | exact wrapper or literal `NONE` |
| `ATT01_TARGET_PROCESS_CHAIN` | one ordered `exec` chain from sshd's session child through shell/forced command/wrapper and `/usr/bin/env` to `/usr/bin/python3`; no prose ellipsis |
| `ATT01_INITIAL_CWD` | exact cwd of the first target command process before any `chdir`; absolute path |
| `ATT01_PRE_ENVIRONMENT_B64` | canonical base64 of sorted `name=value\0` bytes for the target process immediately before `/usr/bin/env -i` |
| `ATT01_POST_ENVIRONMENT_B64` | canonical base64 of exactly `HOME=/root\0LC_ALL=C\0PATH=/usr/bin:/bin\0PYTHONDONTWRITEBYTECODE=1\0` in byte-sorted key order |
| `ATT01_STDIN_MAPPING` | literal `producer_blob_to_python_stdin_no_prefix_or_suffix` |
| `ATT01_FD_MAPPING` | exact `0=ssh-stdin,1=ssh-stdout,2=ssh-stderr,all_other_fds=closed` |
| `ATT01_REMOTE_COMMAND` | the complete shell command bytes or forced-command input; no placeholder, shell metavariable, prose marker, or independent expansion |
| `ATT01_OUTER_ARGV_B64` | canonical base64 of the exact NUL-separated UTF-8 Windows argv, including final NUL |
| `ATT01_OUTER_ARGV_SHA256` | SHA-256 of those exact canonical argv bytes; 64 lowercase hex |
| `TARGET_MUTATION_DENIAL_CONTROL` | exact executable/control identity and proof that category-1 mutation is denied on success and failure paths while fd 1/2 remain usable |
| `INFRASTRUCTURE_CROSSOVER_RESULT` | literal `NO_ROTATION_NO_OUT_OF_STORE_ACTION_NO_SIDE_EFFECT_HOOK` with cited host-channel proof |

No examined source establishes those values. The grant states only that G6 runs in the G3 root session; the fixed later transport row is the different unprivileged `gatea` route. Therefore every field is currently `UNKNOWN`. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:32-35`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:2`

## 5. Exact launch contract

### 5.1 Operator launcher

Final package path: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/launch_record_wpi_attestation.ps1`.

The only launcher argv is:

```text
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_STAGE1_COMMIT1\launch_record_wpi_attestation.ps1
```

Initial operator cwd is exactly `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_STAGE1_COMMIT1`. The launcher in section 10 creates the Python recorder directly with no shell, clears its environment, sets the exact environment in section 8.1, and forwards the recorder's stdout/stderr/rc unchanged.

The final launcher also copies `POWERSHELL_EXE_SHA256` from section 4.3 and verifies the running executable's exact path and file digest before creating Python. Its current digest is `UNKNOWN`, so this draft launcher stops rather than starting the recorder.

### 5.2 `ATT-01` target launch

`ATT01_OUTER_ARGV = UNKNOWN`  
`ATT01_TARGET_PROCESS_CHAIN = UNKNOWN`  
`ATT01_INITIAL_CWD = UNKNOWN`  
`FORCED_COMMAND_MODE = UNKNOWN`  
`TARGET_MUTATION_DENIAL_CONTROL = UNKNOWN`

These are facts, not fillable editorial markers. There is no executable ATT-01 row until the exact source in section 4.3 is committed and its values are copied verbatim into all three places: this section, the recorder constants, and the package manifest build record. The recorder refuses any literal `UNKNOWN`, any mismatch with the binding-record digest, or any outer argv whose canonical NUL-separated bytes do not equal `ATT01_OUTER_ARGV_B64`.

The current non-executable row is recorded without suggesting otherwise:

| op_id | kind | run_when | expect tuple | operator cwd | stdin bytes | stdin SHA-256 | outer argv | purpose |
|---|---|---|---|---|---|---|---|---|
| `ATT-01` | `ssh_stdin_read_only_attestation` | `clean_commit1_package_and_all_bindings_ok` | `(0, exact section-6.6 stdout, empty stderr)` | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_STAGE1_COMMIT1` | exact committed `capture_wpi_attestation.py` blob | `UNKNOWN` until final filled producer bytes exist | `UNKNOWN` until section-4.3 binding exists | capture only the Commit-1-bound attestation |

Both `UNKNOWN` cells are commit blockers. In final Commit 1 the row is regenerated from the exact producer blob and root-channel binding, and the resulting literal digest/argv must equal the recorder constants byte-for-byte.

This prevents two operators from choosing different captures: at present both must STOP; after finalization both invoke the one byte-identical argv.

## 6. Target producer contract

### 6.1 Identity, environment, cwd, stdin, and terminal tuples

Final path: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/capture_wpi_attestation.py`. Encoding is ASCII, LF-only, no BOM, final LF. The exact bytes are the code-block body in section 7 with all section-4 inputs filled verbatim and no `UNKNOWN` remaining.

The post-`env` argv is exactly:

```text
/usr/bin/python3 -I -S -B - --record-id <ATTESTATION_RECORD_ID> --candidate <WPI_CANDIDATE_SHA> --allocation-parent /home/gatea --main-pid <WPI_MAINPID> --main-starttime <WPI_MAINPID_STARTTIME_TICKS> --producer-sha256 <PRODUCER_SHA256>
```

The post-`env` environment bytes are exactly the sorted entries in section 4.3; cwd before Python startup is supplied by the root-channel binding and cwd at the first observation is `/`. Stdin is exactly the committed producer blob, with no prefix/suffix or newline conversion. Allowed inherited descriptors are exactly 0/1/2 with the mapping in section 4.3.

Terminal acceptance tuples are exact:

| Class | `(rc, stdout, stderr)` |
|---|---|
| PASS | `(0, exact section-6.6 ASCII/LF grammar ending ATTESTATION_V2_PASS+LF, empty)` |
| STOP | `(3, empty, exactly ATTESTATION_V2_STOP reason=<fixed-token>+LF)` |

Any other tuple is recorder STOP. Status is adjudicated before stdout is parsed. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:368-420`

### 6.2 Exact MainPID binding

Before other observations, the producer:

1. opens `pidfd_open(WPI_MAINPID, 0)` and requires a zero-event nonblocking poll;
2. captures one complete snapshot of `/proc/<pid>/stat` field 22, `/proc/<pid>/cwd`, `/proc/<pid>/exe`, executable bytes, `/proc/<pid>/cmdline`, and `/proc/<pid>/ns/net`;
3. requires exact equality to the committed checkpoint fields and the candidate-derived cwd/command line;
4. performs every other observation;
5. captures the same snapshot again, requires byte equality to the first, and again requires the pidfd non-readable; and
6. closes the pidfd only after every field is buffered.

An absent/unreadable process, unsupported pidfd, exited pidfd, malformed stat/cmdline, start-time mismatch, PID reuse, cwd/cmdline candidate mismatch, executable mismatch, namespace mismatch, or before/after drift is STOP before stdout.

### 6.3 Exact read set

The producer reads only `/proc/self/exe`, `/usr/bin/python3` resolution metadata, the resolved interpreter bytes, `/proc/{1,self}/ns/{user,mnt,pid,net}`, `/`, `/home/gatea`, `/proc/self/mountinfo`, and the exact MainPID objects in section 6.2. It performs only process-local calculation after those reads and writes only inherited fd 1/2.

### 6.4 Projection-v2 universe

The 21 ordered points remain:

1. `/usr/bin/stat`
2. `/usr/bin/readlink`
3. `/usr/bin/env`
4. `/usr/bin/find`
5. `/usr/bin/sha256sum`
6. `/usr/bin/systemctl`
7. `/usr/bin/ss`
8. `/usr/bin/curl`
9. `/usr/bin/timeout`
10. the captured trusted Python leaf
11. `/opt/mtc-bridge/releases/<WPI_CANDIDATE_SHA>`
12. `/opt/mtc-bridge/venvs/<WPI_CANDIDATE_SHA>`
13. `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`
14. `/var/lib/mtc-bridge`
15. `/var/log/mtc-bridge`
16. `/etc/mtc-bridge`
17. `<release>/IBKR_PAPER_BRIDGE/requirements.lock`
18. `<release>/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py`
19. `/proc/self/mountinfo`
20. `/proc/self/ns/net`
21. `/proc/<WPI_MAINPID>/ns/net`

The six ordered, first-occurrence-deduplicated subtree roots are release, venv, `/etc/mtc-bridge`, `/var/lib/mtc-bridge`, `/var/log/mtc-bridge`, and `/usr/bin`. Effective mount selection is longest covering mount point; equal lengths select the later mountinfo record. `shared_mount_point_records` counts all records with the selected mount point. The accepted RP7 source fixes the same point/root counts and order. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:1214-1281`

### 6.5 Reader completeness

`/proc/self/mountinfo` must be nonempty, fully LF-terminated, NUL/CR-free, and entirely parseable. Blank/malformed records, duplicate mount IDs, invalid fields, open/read error, partial read, or zero records are STOP. The recorder independently parses the decoded bytes and rebuilds the projection; absence of facts never means PASS. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:424-486,899-929`

### 6.6 Exact PASS stdout order

Every line is ASCII and LF-terminated; every key appears once in this order:

```text
ATTESTATION_V2_BEGIN
protocol=normalised_path_projection_v2
record_id=<safe-component>
candidate=<40-lowercase-hex>
main_pid=<positive-canonical-decimal>
main_pid_starttime_ticks=<positive-canonical-decimal>
main_pid_cwd=/opt/mtc-bridge/releases/<candidate>/IBKR_PAPER_BRIDGE
main_pid_exe=<exact committed absolute path>
main_pid_exe_sha256=<64-lowercase-hex>
main_pid_cmdline_bytes=<positive-canonical-decimal>
main_pid_cmdline_sha256=<64-lowercase-hex>
main_pid_net_ns=net:[<positive-canonical-decimal>]
staging_host=GATEA-STAGING
execution_euid=0
cwd=/
producer_sha256=<64-lowercase-hex>
trusted_python_path=/usr/bin/python3.<one-or-two-decimal-digits>
trusted_python_sha256=<64-lowercase-hex>
user_ns=user:[<positive-canonical-decimal>]
mnt_ns=mnt:[<positive-canonical-decimal>]
pid_ns=pid:[<positive-canonical-decimal>]
net_ns=net:[<positive-canonical-decimal>]
root_mount_id=<nonnegative-canonical-decimal>:<positive-canonical-decimal>
allocation_parent=/home/gatea
expect_parent_mount_b64=<canonical-RFC4648-base64>
mountinfo_bytes=<positive-canonical-decimal>
mountinfo_sha256=<64-lowercase-hex>
mountinfo_b64=<canonical-RFC4648-base64>
projection_points=21
projection_roots=6
projection_mount_records=<positive-canonical-decimal>
projection_bytes=<positive-canonical-decimal>
projection_sha256=<64-lowercase-hex>
projection_b64=<canonical-RFC4648-base64>
ATTESTATION_V2_PASS
```

## 7. Normative target producer source

```python
import base64
import hashlib
import os
import re
import select
import stat
import sys

STOP_PREFIX = "ATTESTATION_V2_STOP reason="
FIXED_CANDIDATE = "UNKNOWN"
FIXED_PARENT = "/home/gatea"
FIXED_MAIN_PID = "UNKNOWN"
FIXED_MAIN_STARTTIME = "UNKNOWN"
FIXED_MAIN_EXE = "UNKNOWN"
FIXED_MAIN_EXE_SHA256 = "UNKNOWN"
FIXED_MAIN_NET_NS = "UNKNOWN"
SAFE_COMPONENT = re.compile(r"^(?!-)(?!\.$)(?!\.\.$)[A-Za-z0-9._-]+$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
POSDEC = re.compile(r"^[1-9][0-9]*$")


class AttestationStop(Exception):
    pass


def stop(reason):
    raise AttestationStop(reason)


def read_all(path, nofollow=False):
    flags = os.O_RDONLY | os.O_CLOEXEC
    if nofollow:
        if not hasattr(os, "O_NOFOLLOW"):
            stop("nofollow_unavailable")
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
    for line in raw[:-1].split(b"\n"):
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
    return winner, sum(1 for row in rows if row[2] == winner[2])


def build_projection(rows, trusted_python):
    release = b"/opt/mtc-bridge/releases/" + FIXED_CANDIDATE.encode("ascii")
    venv = b"/opt/mtc-bridge/venvs/" + FIXED_CANDIDATE.encode("ascii")
    tools = [
        b"/usr/bin/stat", b"/usr/bin/readlink", b"/usr/bin/env", b"/usr/bin/find",
        b"/usr/bin/sha256sum", b"/usr/bin/systemctl", b"/usr/bin/ss",
        b"/usr/bin/curl", b"/usr/bin/timeout", trusted_python.encode("ascii"),
    ]
    points = tools + [
        release, venv, b"/usr/local/lib/systemd/system/mtc-bridge-first-start.service",
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
    if not re.fullmatch(kind + r":\[[1-9][0-9]*\]", value):
        stop("namespace_grammar")
    return value


def proc_starttime(raw, pid):
    if not raw.endswith(b"\n") or b"\x00" in raw or b"\r" in raw:
        stop("mainpid_stat_grammar")
    body = raw[:-1]
    prefix = pid.encode("ascii") + b" ("
    end = body.rfind(b") ")
    if not body.startswith(prefix) or end < len(prefix):
        stop("mainpid_stat_grammar")
    tail = body[end + 2:].split(b" ")
    if len(tail) < 20 or b"" in tail or not tail[19].isdigit():
        stop("mainpid_stat_grammar")
    value = tail[19].decode("ascii")
    if not POSDEC.fullmatch(value):
        stop("mainpid_stat_grammar")
    return value


def pid_snapshot(pid):
    base = "/proc/" + pid
    starttime = proc_starttime(read_all(base + "/stat"), pid)
    try:
        cwd = os.readlink(base + "/cwd")
        exe = os.readlink(base + "/exe")
    except OSError:
        stop("mainpid_link_unreadable")
    cmdline = read_all(base + "/cmdline")
    net_ns = ns_link(base + "/ns/net", "net")
    if not cmdline or not cmdline.endswith(b"\x00"):
        stop("mainpid_cmdline_grammar")
    expected_cwd = "/opt/mtc-bridge/releases/" + FIXED_CANDIDATE + "/IBKR_PAPER_BRIDGE"
    expected_cmdline = (
        "/opt/mtc-bridge/venvs/" + FIXED_CANDIDATE + "/bin/python\x00-m\x00bridge.app\x00"
    ).encode("ascii")
    if starttime != FIXED_MAIN_STARTTIME:
        stop("mainpid_starttime_mismatch")
    if cwd != expected_cwd or cmdline != expected_cmdline:
        stop("mainpid_candidate_binding_mismatch")
    if exe != FIXED_MAIN_EXE or net_ns != FIXED_MAIN_NET_NS:
        stop("mainpid_identity_mismatch")
    exe_bytes = read_all(exe, nofollow=True)
    if sha256_bytes(exe_bytes) != FIXED_MAIN_EXE_SHA256:
        stop("mainpid_executable_mismatch")
    return (starttime, cwd, exe, sha256_bytes(exe_bytes), cmdline, net_ns)


def pidfd_require_alive(pidfd):
    poller = select.poll()
    poller.register(pidfd, select.POLLIN | select.POLLERR | select.POLLHUP)
    if poller.poll(0):
        stop("mainpid_not_live")


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
        "--record-id", "--candidate", "--allocation-parent", "--main-pid",
        "--main-starttime", "--producer-sha256",
    ]
    if len(argv) != 12 or argv[0::2] != keys:
        stop("argument_grammar")
    return dict(zip(keys, argv[1::2]))


def main():
    args = parse_exact_argv(sys.argv[1:])
    if "UNKNOWN" in (
        FIXED_CANDIDATE, FIXED_MAIN_PID, FIXED_MAIN_STARTTIME,
        FIXED_MAIN_EXE, FIXED_MAIN_EXE_SHA256, FIXED_MAIN_NET_NS,
    ):
        stop("unfilled_commit1_input")
    record_id = args["--record-id"]
    producer_sha256 = args["--producer-sha256"]
    if not SAFE_COMPONENT.fullmatch(record_id) or not HEX64.fullmatch(producer_sha256):
        stop("argument_grammar")
    if (
        args["--candidate"] != FIXED_CANDIDATE
        or args["--allocation-parent"] != FIXED_PARENT
        or args["--main-pid"] != FIXED_MAIN_PID
        or args["--main-starttime"] != FIXED_MAIN_STARTTIME
    ):
        stop("fixed_argument_mismatch")
    if not re.fullmatch(r"[0-9a-f]{40}", FIXED_CANDIDATE):
        stop("candidate_identity_grammar")
    if not POSDEC.fullmatch(FIXED_MAIN_PID) or not POSDEC.fullmatch(FIXED_MAIN_STARTTIME):
        stop("mainpid_identity_grammar")
    if not HEX64.fullmatch(FIXED_MAIN_EXE_SHA256):
        stop("mainpid_executable_grammar")
    if os.geteuid() != 0:
        stop("execution_euid_not_root")
    os.chdir("/")
    if os.getcwd() != "/":
        stop("cwd_not_fixed")

    if not hasattr(os, "pidfd_open"):
        stop("pidfd_unavailable")
    try:
        pidfd = os.pidfd_open(int(FIXED_MAIN_PID), 0)
    except OSError:
        stop("mainpid_absent")
    try:
        pidfd_require_alive(pidfd)
        before = pid_snapshot(FIXED_MAIN_PID)

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
        (device, root, mount_point, fstype, source), shared = effective_mount(
            rows, FIXED_PARENT.encode("ascii")
        )
        expect_parent = (
            b"device=" + device + b" root=" + root + b" mount_point=" + mount_point
            + b" fstype=" + fstype + b" source=" + source
            + b" shared_mount_point_records=" + str(shared).encode("ascii")
        )
        projection, point_count, root_count = build_projection(rows, actual)

        after = pid_snapshot(FIXED_MAIN_PID)
        pidfd_require_alive(pidfd)
        if after != before:
            stop("mainpid_changed_during_capture")
    finally:
        os.close(pidfd)

    starttime, main_cwd, main_exe, main_exe_sha, cmdline, main_net_ns = before
    fields = [
        "ATTESTATION_V2_BEGIN",
        "protocol=normalised_path_projection_v2",
        f"record_id={record_id}",
        f"candidate={FIXED_CANDIDATE}",
        f"main_pid={FIXED_MAIN_PID}",
        f"main_pid_starttime_ticks={starttime}",
        f"main_pid_cwd={main_cwd}",
        f"main_pid_exe={main_exe}",
        f"main_pid_exe_sha256={main_exe_sha}",
        f"main_pid_cmdline_bytes={len(cmdline)}",
        f"main_pid_cmdline_sha256={sha256_bytes(cmdline)}",
        f"main_pid_net_ns={main_net_ns}",
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
        "ATTESTATION_V2_PASS",
    ]
    write_all(1, ("\n".join(fields) + "\n").encode("ascii"))


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

## 8. Operator recorder contract

### 8.1 Identity, argv, environment, cwd

Final path: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/record_wpi_attestation.py`; ASCII, LF-only, final LF.

Python executable: `C:\Python314\python.exe`. Its final SHA-256 is copied from the root-channel/tool binding record and is currently `UNKNOWN`; the recorder verifies its own path and bytes before any Git command. The exact child argv is:

```text
C:\Python314\python.exe -I -S -B C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_STAGE1_COMMIT1\record_wpi_attestation.py
```

No recorder argument is permitted. Cwd is the package directory. The launcher clears the environment and supplies exactly these case-sensitive entries:

```text
ComSpec=C:\Windows\System32\cmd.exe
PATH=C:\Windows\System32
PYTHONDONTWRITEBYTECODE=1
SystemRoot=C:\Windows
WINDIR=C:\Windows
```

The recorder opens no socket until all section-8.3 checks have accepted, the create-once first record line is fsynced, and the same clean/HEAD checks accept again.

### 8.2 Exact package paths

`PACKAGE_DIR := MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1`

The final package has exactly five members:

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/COMMIT1_ATTESTATION_PREREGISTRATION.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/capture_wpi_attestation.py`
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/record_wpi_attestation.py`
4. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/launch_record_wpi_attestation.ps1`
5. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1/COMMIT1_PACKAGE_MANIFEST.tsv`

The manifest contains one header, four member rows for ordinals 1–4, and the final literal line `package_members_including_manifest=5`. It does not self-embed its digest. The clean gate binds the manifest itself from `COMMIT_1` after the commit exists.

### 8.3 Ordered clean-current-HEAD checks and exact tuples

All Git subprocesses use `C:\Program Files\Git\cmd\git.exe`, `cwd=C:\LAB\Tradingview_LAB_CLEAN`, stdin empty/closed, no shell, and the exact Git child environment fixed in the recorder. `EMPTY := b""`, `LF := b"\n"`, and `OID := exactly 40 lowercase hex ASCII bytes`. `COMMIT_1` is assigned once from check 5 after its tuple validates. Every later object expression uses the bytes of `COMMIT_1`; the token `HEAD` does not occur in any later argv.

| # | Exact argv after `git.exe` | Required `(rc, stdout, stderr)` |
|---:|---|---|
| 1 | `rev-parse --show-object-format` | `(0, b"sha1\n", EMPTY)` |
| 2 | `diff --quiet --` | `(0, EMPTY, EMPTY)` |
| 3 | `diff --cached --quiet --` | `(0, EMPTY, EMPTY)` |
| 4 | `ls-files --others --exclude-standard -z` | `(0, EMPTY, EMPTY)` |
| 5 | `rev-parse --verify HEAD^{commit}` | `(0, OID+LF, EMPTY)`; assign `COMMIT_1 := OID` |
| 6 | `ls-tree -r -z --name-only COMMIT_1 -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1` | `(0, exact NUL-terminated sorted five-path byte sequence, EMPTY)` |
| 7 | for each path `P`: `rev-parse --verify COMMIT_1:P` | `(0, OID+LF, EMPTY)` |
| 8 | for each path `P`: `hash-object --no-filters -- P` | `(0, exact OID from check 7 + LF, EMPTY)` |
| 9 | manifest parse, byte count, SHA-256, row OID, ordinal/order/role/count checks | in-process success with no ignored byte; otherwise STOP |
| 10 | repeat exact checks 2, 3, and 4 | their exact tuples above |
| 11 | `rev-parse --verify HEAD^{commit}` | `(0, exact COMMIT_1+LF, EMPTY)` |
| 12 | after first-line fsync, repeat exact checks 2, 3, 4, and 11 | their exact tuples above; only then may `ssh.exe` start |

Checks 7–8 are performed for all five members, including the manifest. The four manifest rows must also equal the exact raw worktree bytes by length, SHA-256, and Git blob OID. An absent/extra/hidden path, dirty index/worktree, untracked nonignored path, warning on stderr, SHA-256 mismatch, blob mismatch, manifest self-row, duplicate, invalid order, or HEAD change is pre-socket STOP.

### 8.4 Exact output path, collision, and close/fsync policy

The only output file is the allocation-derived `OPERATOR_RECORD_PATH` from section 4.1. The parent must already exist, be empty at allocation, and resolve to its literal non-reparse path. The recorder opens the final path with create-new/exclusive semantics. Existing path means `RECORDER_V1_STOP reason=record_collision record_created=0`; it is never opened, changed, removed, renamed, or truncated.

After all pre-record checks, the recorder writes exactly `attestation_prereg_commit=<COMMIT_1>\n`, flushes with `fsync`, repeats the pre-socket checks, then starts SSH. After SSH returns or fails to start, it appends the canonical tail, `fsync`s, closes once, reopens read-only, and computes byte count/SHA-256 over the complete closed bytes. It never uses a temp file or rename. If a write/fsync/close fails, it makes a best-effort close, preserves the partial create-once file without deletion/truncation, emits STOP, and the record is permanently non-consumable.

### 8.5 Canonical record serialization

Encoding is ASCII; separator and final terminator are LF; CR/NUL are forbidden. Canonical nonnegative decimal is `0|[1-9][0-9]*`; positive decimal is `[1-9][0-9]*`; signed decimal is `0|-?[1-9][0-9]*`; Git OID is exactly 40 lowercase hex; SHA-256 is exactly 64 lowercase hex. Base64 is RFC 4648 standard alphabet with required padding, no whitespace/wrapping, and re-encode equality; empty bytes serialize as an empty value after `=`.

After the already-written first line, the exact order is:

```text
package_manifest_blob=<40-lowercase-hex>
prereg_blob=<40-lowercase-hex>
producer_blob=<40-lowercase-hex>
recorder_blob=<40-lowercase-hex>
launcher_blob=<40-lowercase-hex>
producer_bytes=<positive-canonical-decimal>
producer_sha256=<64-lowercase-hex>
record_id=<safe-component>
confirm_token=<safe-component>
outer_argv_sha256=<64-lowercase-hex>
outer_argv_b64=<canonical-RFC4648-base64-of-NUL-separated-UTF8-argv-with-final-NUL>
stdout_bytes=<nonnegative-canonical-decimal>
stdout_sha256=<64-lowercase-hex>
stdout_b64=<canonical-RFC4648-base64>
stderr_bytes=<nonnegative-canonical-decimal>
stderr_sha256=<64-lowercase-hex>
stderr_b64=<canonical-RFC4648-base64>
ssh_started=0|1
ssh_rc=not-started|<signed-canonical-decimal>
record_status=PASS|STOP
stop_reason=none|<fixed-lowercase-token>
```

`PASS` is permitted only for exact SSH/producer tuple `(0, validated section-6.6 stdout, empty stderr)`. Every other result is `STOP`. Raw streams are never edited; base64 is the lossless embedding.

Recorder terminal tuples:

| Class | `(rc, stdout, stderr)` |
|---|---|
| PASS | `(0, exactly four LF lines: RECORDER_V1_PASS; record_path_b64=...; record_bytes=<positive>; record_sha256=<64hex>, empty)` |
| pre-record STOP | `(3, empty, exactly RECORDER_V1_STOP reason=<token> record_created=0+LF)` |
| post-record STOP | `(3, empty, exactly RECORDER_V1_STOP reason=<token> record_created=1 record_path_b64=<canonical> record_bytes=<positive> record_sha256=<64hex>+LF)` |

## 9. Normative operator recorder source

The following is the packaged implementation. Its `UNKNOWN` constants are deliberate draft blockers and must be replaced only from section 4 before Commit 1.

```python
import base64
import hashlib
import os
import re
import subprocess
import sys

REPO_ROOT = r"C:\LAB\Tradingview_LAB_CLEAN"
PACKAGE_DIR = "MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT1"
PREREG = PACKAGE_DIR + "/COMMIT1_ATTESTATION_PREREGISTRATION.md"
PRODUCER = PACKAGE_DIR + "/capture_wpi_attestation.py"
RECORDER = PACKAGE_DIR + "/record_wpi_attestation.py"
LAUNCHER = PACKAGE_DIR + "/launch_record_wpi_attestation.ps1"
MANIFEST = PACKAGE_DIR + "/COMMIT1_PACKAGE_MANIFEST.tsv"
MEMBERS = (PREREG, PRODUCER, RECORDER, LAUNCHER, MANIFEST)
ROLES = ("preregistration", "target_producer", "operator_recorder", "operator_launcher")
GIT = r"C:\Program Files\Git\cmd\git.exe"
GIT_SHA256 = "UNKNOWN"
SSH = r"C:\Windows\System32\OpenSSH\ssh.exe"
SSH_SHA256 = "UNKNOWN"
PYTHON = r"C:\Python314\python.exe"
PYTHON_SHA256 = "UNKNOWN"
RECORD_ID = "UNKNOWN"
CONFIRM_TOKEN = "UNKNOWN"
RECORD_ROOT = "UNKNOWN"
RECORD_PATH = "UNKNOWN"
FIXED_CANDIDATE = "UNKNOWN"
FIXED_MAIN_PID = "UNKNOWN"
FIXED_MAIN_STARTTIME = "UNKNOWN"
FIXED_MAIN_EXE = "UNKNOWN"
FIXED_MAIN_EXE_SHA256 = "UNKNOWN"
FIXED_MAIN_NET_NS = "UNKNOWN"
OUTER_SSH_ARGV = ("UNKNOWN",)
OUTER_SSH_ARGV_SHA256 = "UNKNOWN"
EXPECTED_ENV = {
    "ComSpec": r"C:\Windows\System32\cmd.exe",
    "PATH": r"C:\Windows\System32",
    "PYTHONDONTWRITEBYTECODE": "1",
    "SystemRoot": r"C:\Windows",
    "WINDIR": r"C:\Windows",
}
GIT_ENV = {
    "ComSpec": r"C:\Windows\System32\cmd.exe",
    "GIT_CONFIG_GLOBAL": "NUL",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
    "HOME": r"C:\Windows\Temp\wpi-no-home",
    "LC_ALL": "C",
    "PATH": r"C:\Windows\System32",
    "SystemRoot": r"C:\Windows",
    "WINDIR": r"C:\Windows",
}
SSH_ENV = {
    "ComSpec": r"C:\Windows\System32\cmd.exe",
    "LC_ALL": "C",
    "PATH": r"C:\Windows\System32",
    "SystemRoot": r"C:\Windows",
    "WINDIR": r"C:\Windows",
}
OID = re.compile(rb"[0-9a-f]{40}")
HEX64 = re.compile(r"[0-9a-f]{64}")
POSDEC = re.compile(r"[1-9][0-9]*")
SAFE = re.compile(r"(?!-)(?!\.$)(?!\.\.$)[A-Za-z0-9._-]+")


class RecorderStop(Exception):
    pass


def stop(reason):
    if not re.fullmatch(r"[a-z0-9_]+", reason):
        reason = "internal_stop"
    raise RecorderStop(reason)


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def b64(value):
    return base64.b64encode(value).decode("ascii")


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def local_path(repo_path):
    return os.path.join(REPO_ROOT, *repo_path.split("/"))


def run_git(args):
    result = subprocess.run(
        [GIT, *args], cwd=REPO_ROOT, env=GIT_ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return result.returncode, result.stdout, result.stderr


def require_tuple(args, expected_out):
    rc, out, err = run_git(args)
    if (rc, out, err) != (0, expected_out, b""):
        stop("git_tuple_mismatch")


def require_oid_tuple(args, expected=None):
    rc, out, err = run_git(args)
    if rc != 0 or err != b"" or not out.endswith(b"\n") or not OID.fullmatch(out[:-1]):
        stop("git_oid_tuple_mismatch")
    value = out[:-1].decode("ascii")
    if expected is not None and value != expected:
        stop("git_oid_changed")
    return value


def clean_tuple_gate(expected_commit=None):
    require_tuple(["diff", "--quiet", "--"], b"")
    require_tuple(["diff", "--cached", "--quiet", "--"], b"")
    require_tuple(["ls-files", "--others", "--exclude-standard", "-z"], b"")
    commit = require_oid_tuple(["rev-parse", "--verify", "HEAD^{commit}"], expected_commit)
    return commit


def parse_manifest(raw):
    if not raw.endswith(b"\n") or b"\r" in raw or b"\x00" in raw:
        stop("manifest_bytes")
    try:
        lines = raw[:-1].decode("ascii").split("\n")
    except UnicodeDecodeError:
        stop("manifest_bytes")
    if len(lines) != 6 or lines[0] != "ordinal\tpath\tbytes\tsha256\tgit_blob_oid\trole":
        stop("manifest_grammar")
    if lines[-1] != "package_members_including_manifest=5":
        stop("manifest_count")
    rows = []
    for index, line in enumerate(lines[1:5], 1):
        fields = line.split("\t")
        if len(fields) != 6:
            stop("manifest_grammar")
        ordinal, path, size, digest, oid, role = fields
        if ordinal != str(index) or path != MEMBERS[index - 1] or role != ROLES[index - 1]:
            stop("manifest_identity")
        if not POSDEC.fullmatch(size) or not HEX64.fullmatch(digest) or not re.fullmatch(r"[0-9a-f]{40}", oid):
            stop("manifest_value_grammar")
        rows.append((path, int(size), digest, oid))
    return rows


def package_gate():
    if sys.argv != [sys.argv[0]] or os.environ != EXPECTED_ENV:
        stop("recorder_launch_contract")
    if os.path.normcase(os.path.abspath(sys.executable)) != os.path.normcase(PYTHON):
        stop("operator_python_path")
    if sha256_bytes(read_bytes(PYTHON)) != PYTHON_SHA256:
        stop("operator_python_digest")
    required = (
        PYTHON_SHA256, GIT_SHA256, SSH_SHA256, RECORD_ID, CONFIRM_TOKEN, RECORD_ROOT, RECORD_PATH,
        FIXED_CANDIDATE, FIXED_MAIN_PID, FIXED_MAIN_STARTTIME, FIXED_MAIN_EXE,
        FIXED_MAIN_EXE_SHA256, FIXED_MAIN_NET_NS, OUTER_SSH_ARGV_SHA256, *OUTER_SSH_ARGV,
    )
    if "UNKNOWN" in required:
        stop("unfilled_commit1_input")
    if not SAFE.fullmatch(RECORD_ID) or not SAFE.fullmatch(CONFIRM_TOKEN):
        stop("allocation_grammar")
    if (
        not HEX64.fullmatch(PYTHON_SHA256)
        or not HEX64.fullmatch(GIT_SHA256)
        or not HEX64.fullmatch(SSH_SHA256)
        or not HEX64.fullmatch(FIXED_MAIN_EXE_SHA256)
        or not HEX64.fullmatch(OUTER_SSH_ARGV_SHA256)
    ):
        stop("identity_grammar")
    if sha256_bytes(read_bytes(GIT)) != GIT_SHA256:
        stop("git_identity_mismatch")
    if sha256_bytes(read_bytes(SSH)) != SSH_SHA256 or OUTER_SSH_ARGV[0] != SSH:
        stop("ssh_identity_mismatch")
    if any(not argument or "\x00" in argument for argument in OUTER_SSH_ARGV):
        stop("outer_argv_grammar")
    expected_record_path = os.path.join(RECORD_ROOT, "attestation", RECORD_ID + ".record")
    if os.path.normcase(os.path.normpath(RECORD_PATH)) != os.path.normcase(os.path.normpath(expected_record_path)):
        stop("record_path_derivation")
    outer_raw = b"".join(arg.encode("utf-8") + b"\x00" for arg in OUTER_SSH_ARGV)
    if sha256_bytes(outer_raw) != OUTER_SSH_ARGV_SHA256:
        stop("outer_argv_binding")
    require_tuple(["rev-parse", "--show-object-format"], b"sha1\n")
    commit = clean_tuple_gate()
    sorted_members = sorted(MEMBERS)
    expected_tree = b"".join(path.encode("ascii") + b"\x00" for path in sorted_members)
    require_tuple(["ls-tree", "-r", "-z", "--name-only", commit, "--", PACKAGE_DIR], expected_tree)
    object_ids = {}
    for path in MEMBERS:
        oid = require_oid_tuple(["rev-parse", "--verify", commit + ":" + path])
        require_oid_tuple(["hash-object", "--no-filters", "--", path], oid)
        object_ids[path] = oid
    manifest_raw = read_bytes(local_path(MANIFEST))
    rows = parse_manifest(manifest_raw)
    for path, size, digest, oid in rows:
        raw = read_bytes(local_path(path))
        if len(raw) != size or sha256_bytes(raw) != digest or object_ids[path] != oid:
            stop("manifest_member_mismatch")
    producer = read_bytes(local_path(PRODUCER))
    clean_tuple_gate(commit)
    return commit, object_ids, producer


def strict_b64(text):
    try:
        raw = base64.b64decode(text.encode("ascii"), validate=True)
    except (UnicodeEncodeError, ValueError):
        stop("target_base64")
    if b64(raw) != text:
        stop("target_base64")
    return raw


def parse_mountinfo_independent(raw):
    if not raw or not raw.endswith(b"\n") or b"\x00" in raw or b"\r" in raw:
        stop("target_mountinfo_bytes")
    rows = []
    seen_ids = set()
    for line in raw[:-1].split(b"\n"):
        if not line:
            stop("target_mountinfo_record")
        fields = line.split(b" ")
        if b"" in fields:
            stop("target_mountinfo_record")
        try:
            separator = fields.index(b"-", 6)
        except ValueError:
            stop("target_mountinfo_record")
        if separator < 6 or len(fields) < separator + 4:
            stop("target_mountinfo_record")
        mount_id, parent_id, device, root, mount_point = fields[:5]
        fstype, source = fields[separator + 1], fields[separator + 2]
        if not mount_id.isdigit() or not parent_id.isdigit() or mount_id in seen_ids:
            stop("target_mountinfo_record")
        seen_ids.add(mount_id)
        if not re.fullmatch(rb"[0-9]+:[0-9]+", device):
            stop("target_mountinfo_record")
        if not root.startswith(b"/") or not mount_point.startswith(b"/"):
            stop("target_mountinfo_record")
        if any(value == b"" or re.search(rb"[\x00-\x20]", value) for value in (fstype, source)):
            stop("target_mountinfo_record")
        rows.append((device, root, mount_point, fstype, source))
    if not rows:
        stop("target_mountinfo_record")
    return rows


def independently_covers(mount_point, path):
    return mount_point == b"/" or path == mount_point or path.startswith(mount_point + b"/")


def independently_effective_mount(rows, path):
    selected = None
    selected_length = -1
    for row in rows:
        mount_point = row[2]
        if independently_covers(mount_point, path) and len(mount_point) >= selected_length:
            selected = row
            selected_length = len(mount_point)
    if selected is None:
        stop("target_projection_unbound")
    return selected, sum(1 for row in rows if row[2] == selected[2])


def independently_build_projection(rows, trusted_python):
    release = b"/opt/mtc-bridge/releases/" + FIXED_CANDIDATE.encode("ascii")
    venv = b"/opt/mtc-bridge/venvs/" + FIXED_CANDIDATE.encode("ascii")
    tools = [
        b"/usr/bin/stat", b"/usr/bin/readlink", b"/usr/bin/env", b"/usr/bin/find",
        b"/usr/bin/sha256sum", b"/usr/bin/systemctl", b"/usr/bin/ss", b"/usr/bin/curl",
        b"/usr/bin/timeout", trusted_python.encode("ascii"),
    ]
    points = tools + [
        release, venv, b"/usr/local/lib/systemd/system/mtc-bridge-first-start.service",
        b"/var/lib/mtc-bridge", b"/var/log/mtc-bridge", b"/etc/mtc-bridge",
        release + b"/IBKR_PAPER_BRIDGE/requirements.lock",
        release + b"/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py",
        b"/proc/self/mountinfo", b"/proc/self/ns/net",
        b"/proc/" + FIXED_MAIN_PID.encode("ascii") + b"/ns/net",
    ]
    root_candidates = [
        release, venv, b"/etc/mtc-bridge", b"/var/lib/mtc-bridge", b"/var/log/mtc-bridge",
    ]
    root_candidates.extend(path.rsplit(b"/", 1)[0] or b"/" for path in tools)
    roots = []
    for root in root_candidates:
        if root not in roots:
            roots.append(root)
    if len(points) != 21 or len(roots) != 6:
        stop("target_projection_recount")
    output = bytearray()
    for path in points:
        (device, root, mount_point, fstype, source), shared = independently_effective_mount(rows, path)
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


def validate_target(stdout, producer_sha):
    if not stdout.endswith(b"\n") or b"\r" in stdout or b"\x00" in stdout:
        stop("target_stdout_bytes")
    try:
        lines = stdout[:-1].decode("ascii").split("\n")
    except UnicodeDecodeError:
        stop("target_stdout_bytes")
    keys = [
        "protocol", "record_id", "candidate", "main_pid", "main_pid_starttime_ticks",
        "main_pid_cwd", "main_pid_exe", "main_pid_exe_sha256", "main_pid_cmdline_bytes",
        "main_pid_cmdline_sha256", "main_pid_net_ns", "staging_host", "execution_euid", "cwd",
        "producer_sha256", "trusted_python_path", "trusted_python_sha256", "user_ns", "mnt_ns",
        "pid_ns", "net_ns", "root_mount_id", "allocation_parent", "expect_parent_mount_b64",
        "mountinfo_bytes", "mountinfo_sha256", "mountinfo_b64", "projection_points",
        "projection_roots", "projection_mount_records", "projection_bytes", "projection_sha256",
        "projection_b64",
    ]
    if len(lines) != len(keys) + 2 or lines[0] != "ATTESTATION_V2_BEGIN" or lines[-1] != "ATTESTATION_V2_PASS":
        stop("target_stdout_grammar")
    values = {}
    for expected, line in zip(keys, lines[1:-1]):
        if "=" not in line:
            stop("target_stdout_grammar")
        key, value = line.split("=", 1)
        if key != expected or key in values or any(ch in value for ch in "\t\r\n\x00"):
            stop("target_stdout_grammar")
        values[key] = value
    exact = {
        "protocol": "normalised_path_projection_v2", "record_id": RECORD_ID,
        "candidate": FIXED_CANDIDATE, "main_pid": FIXED_MAIN_PID,
        "main_pid_starttime_ticks": FIXED_MAIN_STARTTIME,
        "main_pid_cwd": "/opt/mtc-bridge/releases/" + FIXED_CANDIDATE + "/IBKR_PAPER_BRIDGE",
        "main_pid_exe": FIXED_MAIN_EXE, "main_pid_exe_sha256": FIXED_MAIN_EXE_SHA256,
        "main_pid_net_ns": FIXED_MAIN_NET_NS, "staging_host": "GATEA-STAGING",
        "execution_euid": "0", "cwd": "/", "producer_sha256": producer_sha,
        "allocation_parent": "/home/gatea", "projection_points": "21", "projection_roots": "6",
    }
    if any(values[key] != value for key, value in exact.items()):
        stop("target_fixed_value_mismatch")
    expected_cmd = (
        "/opt/mtc-bridge/venvs/" + FIXED_CANDIDATE + "/bin/python\x00-m\x00bridge.app\x00"
    ).encode("ascii")
    if values["main_pid_cmdline_bytes"] != str(len(expected_cmd)) or values["main_pid_cmdline_sha256"] != sha256_bytes(expected_cmd):
        stop("target_mainpid_binding")
    for key in ("trusted_python_sha256", "mountinfo_sha256", "projection_sha256"):
        if not HEX64.fullmatch(values[key]):
            stop("target_digest_grammar")
    for key in ("mountinfo_bytes", "projection_mount_records", "projection_bytes"):
        if not POSDEC.fullmatch(values[key]):
            stop("target_decimal_grammar")
    if not re.fullmatch(r"/usr/bin/python3\.[0-9]{1,2}", values["trusted_python_path"]):
        stop("target_python_grammar")
    for key, kind in (("user_ns", "user"), ("mnt_ns", "mnt"), ("pid_ns", "pid"), ("net_ns", "net")):
        if not re.fullmatch(kind + r":\[[1-9][0-9]*\]", values[key]):
            stop("target_namespace_grammar")
    if not re.fullmatch(r"[0-9]+:[1-9][0-9]*", values["root_mount_id"]):
        stop("target_root_identity_grammar")
    expect_parent = strict_b64(values["expect_parent_mount_b64"])
    mountinfo = strict_b64(values["mountinfo_b64"])
    projection = strict_b64(values["projection_b64"])
    if len(mountinfo) != int(values["mountinfo_bytes"]) or sha256_bytes(mountinfo) != values["mountinfo_sha256"]:
        stop("target_mountinfo_binding")
    if len(projection) != int(values["projection_bytes"]) or sha256_bytes(projection) != values["projection_sha256"]:
        stop("target_projection_binding")
    rows = parse_mountinfo_independent(mountinfo)
    if values["projection_mount_records"] != str(len(rows)):
        stop("target_projection_record_count")
    (device, root, mount_point, fstype, source), shared = independently_effective_mount(rows, b"/home/gatea")
    rebuilt_parent = (
        b"device=" + device + b" root=" + root + b" mount_point=" + mount_point
        + b" fstype=" + fstype + b" source=" + source
        + b" shared_mount_point_records=" + str(shared).encode("ascii")
    )
    if expect_parent != rebuilt_parent:
        stop("target_parent_mount_binding")
    rebuilt, point_count, root_count = independently_build_projection(rows, values["trusted_python_path"])
    if point_count != 21 or root_count != 6 or rebuilt != projection:
        stop("target_projection_rebuild")
    return values


def write_all(fd, raw):
    view = memoryview(raw)
    while view:
        count = os.write(fd, view)
        if count <= 0:
            raise OSError("short write")
        view = view[count:]


def sealed_identity(path):
    raw = read_bytes(path)
    return len(raw), sha256_bytes(raw)


def emit_pre_stop(reason):
    os.write(2, (f"RECORDER_V1_STOP reason={reason} record_created=0\n").encode("ascii"))
    return 3


def main():
    try:
        commit, object_ids, producer = package_gate()
    except RecorderStop as exc:
        return emit_pre_stop(str(exc))
    parent = os.path.dirname(RECORD_PATH)
    if os.path.normcase(os.path.realpath(parent)) != os.path.normcase(os.path.normpath(parent)) or not os.path.isdir(parent):
        return emit_pre_stop("record_parent_invalid")
    if os.path.lexists(RECORD_PATH):
        return emit_pre_stop("record_collision")
    try:
        if os.listdir(parent) != []:
            return emit_pre_stop("record_parent_not_empty")
    except OSError:
        return emit_pre_stop("record_parent_unreadable")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(RECORD_PATH, flags, 0o600)
    except FileExistsError:
        return emit_pre_stop("record_collision")
    except OSError:
        return emit_pre_stop("record_create_failed")
    reason = "none"
    status = "STOP"
    started = "0"
    ssh_rc = "not-started"
    stdout = b""
    stderr = b""
    try:
        write_all(fd, ("attestation_prereg_commit=" + commit + "\n").encode("ascii"))
        os.fsync(fd)
        clean_tuple_gate(commit)
        outer_raw = b"".join(arg.encode("utf-8") + b"\x00" for arg in OUTER_SSH_ARGV)
        try:
            proc = subprocess.Popen(
                list(OUTER_SSH_ARGV), cwd=local_path(PACKAGE_DIR), env=SSH_ENV,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=False, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            started = "1"
            try:
                stdout, stderr = proc.communicate(producer, timeout=120)
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate()
                reason = "ssh_timeout"
            ssh_rc = str(proc.returncode)
        except OSError:
            reason = "ssh_start_failed"
        producer_sha = sha256_bytes(producer)
        if reason == "none":
            if started != "1" or ssh_rc != "0" or stderr != b"":
                reason = "ssh_or_target_tuple"
            else:
                try:
                    validate_target(stdout, producer_sha)
                    status = "PASS"
                except RecorderStop as exc:
                    reason = str(exc)
        tail = [
            "package_manifest_blob=" + object_ids[MANIFEST],
            "prereg_blob=" + object_ids[PREREG],
            "producer_blob=" + object_ids[PRODUCER],
            "recorder_blob=" + object_ids[RECORDER],
            "launcher_blob=" + object_ids[LAUNCHER],
            "producer_bytes=" + str(len(producer)),
            "producer_sha256=" + producer_sha,
            "record_id=" + RECORD_ID,
            "confirm_token=" + CONFIRM_TOKEN,
            "outer_argv_sha256=" + sha256_bytes(outer_raw),
            "outer_argv_b64=" + b64(outer_raw),
            "stdout_bytes=" + str(len(stdout)),
            "stdout_sha256=" + sha256_bytes(stdout),
            "stdout_b64=" + b64(stdout),
            "stderr_bytes=" + str(len(stderr)),
            "stderr_sha256=" + sha256_bytes(stderr),
            "stderr_b64=" + b64(stderr),
            "ssh_started=" + started,
            "ssh_rc=" + ssh_rc,
            "record_status=" + status,
            "stop_reason=" + reason,
        ]
        write_all(fd, ("\n".join(tail) + "\n").encode("ascii"))
        os.fsync(fd)
    except RecorderStop as exc:
        reason = str(exc)
    except BaseException:
        reason = "record_write_failed"
    finally:
        try:
            os.close(fd)
        except OSError:
            reason = "record_close_failed"
    try:
        size, digest = sealed_identity(RECORD_PATH)
    except OSError:
        return emit_pre_stop("record_reopen_failed")
    path_b64 = b64(RECORD_PATH.encode("utf-8"))
    if status == "PASS" and reason == "none":
        output = (
            "RECORDER_V1_PASS\nrecord_path_b64=" + path_b64 + "\nrecord_bytes="
            + str(size) + "\nrecord_sha256=" + digest + "\n"
        )
        os.write(1, output.encode("ascii"))
        return 0
    output = (
        f"RECORDER_V1_STOP reason={reason} record_created=1 record_path_b64={path_b64} "
        f"record_bytes={size} record_sha256={digest}\n"
    )
    os.write(2, output.encode("ascii"))
    return 3


try:
    raise SystemExit(main())
except SystemExit:
    raise
except BaseException:
    os.write(2, b"RECORDER_V1_STOP reason=internal_stop record_created=0\n")
    raise SystemExit(3)
```

The recorder independently parses the complete decoded mountinfo stream, recomputes the allocation-parent record, rebuilds all 21 projection points and six roots, and requires byte equality with the captured projection before PASS. The remaining draft blockers are the concrete section-4 inputs and their required falsification evidence, not a missing recorder branch.

## 10. Normative launcher source

```powershell
$ErrorActionPreference = 'Stop'
if ($args.Count -ne 0) { throw 'RECORDER_LAUNCH_ARGUMENT_STOP' }
$powerShellPath = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
$powerShellSha256 = 'UNKNOWN'
if ($powerShellSha256 -eq 'UNKNOWN') { throw 'POWERSHELL_IDENTITY_UNFILLED_STOP' }
$runningPath = (Get-Process -Id $PID).Path
if (-not [String]::Equals($runningPath, $powerShellPath, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'POWERSHELL_PATH_STOP'
}
$hasher = [Security.Cryptography.SHA256]::Create()
$stream = [IO.File]::OpenRead($powerShellPath)
try {
    $actualPowerShellSha256 = ([BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-', '').ToLowerInvariant()
} finally {
    $stream.Dispose()
    $hasher.Dispose()
}
if (-not [String]::Equals($actualPowerShellSha256, $powerShellSha256, [StringComparison]::Ordinal)) {
    throw 'POWERSHELL_DIGEST_STOP'
}
$package = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_STAGE1_COMMIT1'
$python = 'C:\Python314\python.exe'
$recorder = "$package\record_wpi_attestation.py"
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.Arguments = "-I -S -B $recorder"
$psi.WorkingDirectory = $package
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.EnvironmentVariables.Clear()
$psi.EnvironmentVariables['ComSpec'] = 'C:\Windows\System32\cmd.exe'
$psi.EnvironmentVariables['PATH'] = 'C:\Windows\System32'
$psi.EnvironmentVariables['PYTHONDONTWRITEBYTECODE'] = '1'
$psi.EnvironmentVariables['SystemRoot'] = 'C:\Windows'
$psi.EnvironmentVariables['WINDIR'] = 'C:\Windows'
$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi
if (-not $process.Start()) { throw 'RECORDER_PROCESS_START_STOP' }
$stdout = $process.StandardOutput.ReadToEnd()
$stderr = $process.StandardError.ReadToEnd()
$process.WaitForExit()
[Console]::Out.Write($stdout)
[Console]::Error.Write($stderr)
exit $process.ExitCode
```

## 11. Manifest grammar

Exact columns:

```text
ordinal\tpath\tbytes\tsha256\tgit_blob_oid\trole
```

Rows 1–4 are the first four members in section 8.2 and roles are, respectively, `preregistration`, `target_producer`, `operator_recorder`, and `operator_launcher`. `bytes` is positive canonical decimal, `sha256` is 64 lowercase hex, and `git_blob_oid` is 40 lowercase hex. The exact final line is:

```text
package_members_including_manifest=5
```

No blank, comment, self row, duplicate, extra field, CR, BOM, or missing final LF is allowed.

## 12. Observation placeholders and Commit-2 handoff

Commit 1 contains the literal `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` for:

- four PID-1 namespace identities;
- root-mount identity;
- `EXPECT_PARENT_MOUNT`;
- trusted Python path/digest;
- mountinfo bytes/digest;
- projection bytes/digest;
- MainPID live snapshot output fields;
- operator record byte count/digest.

Only a closed `record_status=PASS` record whose first line binds exact Commit 1 may supply those values. Commit 2 independently decodes and verifies raw stdout/stderr/rc, rebuilds projection v2, verifies the live MainPID output against the pre-Commit-1 checkpoint source, records the evidence path/bytes/SHA-256, and replaces all observation placeholders. If the producer, recorder, launch chain, mutation boundary, projection algorithm/universe, grammar, or manifest changes, the capture is discarded, a new Commit 1 is created, and capture repeats. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:535-579`

## 13. Commit-1 readiness gate

This V2 must **not** become Commit 1 until every item is true:

- [ ] all three section-4 sources exist in a clean committed ancestor and have concrete blob OIDs;
- [ ] all producer/recorder/launch constants are copied verbatim and no `UNKNOWN`, prose executable requirement, angle-bracket metavariable, or allocation token remains;
- [ ] one literal full ATT-01 outer argv appears identically in section 5, the root-channel binding, and the recorder's canonical argv bytes;
- [ ] the root principal, shell, forced-command/wrapper mapping, pre/post environment, initial cwd, stdin, and descriptor mapping are exact;
- [ ] category-1 mutation is denied on success and failure paths, and log rotation/out-of-store audit/PAM-wrapper crossovers are proved absent;
- [ ] the independent recorder projection implementation and every other final executable byte have the required D026 falsification evidence;
- [ ] every Git check has been executed with the exact tuples in section 8.3;
- [ ] the producer and recorder have D026 RED/GREEN evidence for MainPID reuse/exit/drift, dirty tree, untracked member, manifest mismatch, output collision, malformed base64, bad rc/stderr, and projection mismatch;
- [ ] the five-member force-inclusive package set and manifest reconcile exactly;
- [ ] a fresh T2 review of the exact final bytes accepts with no required repair; and
- [ ] no socket or host command has run before the resulting Commit 1 exists.

The current blocking register is therefore exact:

| Item | Status |
|---|---|
| Stage-1 allocation source and concrete values | `UNKNOWN` |
| Exact candidate/checkpoint source, MainPID starttime/exe/ns identities | `UNKNOWN` |
| Root-channel principal, process chain, forced-command/wrapper behavior, initial cwd, complete outer argv | `UNKNOWN` |
| Category-1 runtime mutation-denial proof | `UNKNOWN` |
| Infrastructure crossover proof (no rotation/out-of-store action/side-effect hook) | `UNKNOWN` |
| Operator Python SHA-256 | `UNKNOWN` |
| Required D026 falsification evidence on the exact filled producer/recorder bytes | `UNKNOWN` |

This is why the status is `DRAFT V2 — NOT COMMITTED, NOT SPENT`. Treating category-2 logging/atime as a blocker would contradict the Lead adjudication; treating any category-1 row above as harmless would widen the owner's narrow permission. `C:\tmp\lane_kick\X3B.md:29-48`

## 14. Lane self-verification

This lane performed no host, network, SSH, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or economic action. It wrote only this document, outside the read-only repository, as required by the lane contract. `C:\tmp\lane_kick\X3B.md:3-8,74-83`
