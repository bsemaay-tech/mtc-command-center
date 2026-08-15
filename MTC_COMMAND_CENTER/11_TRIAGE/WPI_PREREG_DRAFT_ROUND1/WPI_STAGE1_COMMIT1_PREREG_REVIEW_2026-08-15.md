NEEDS-REWORK

# Commit-1 preregistration adversarial review

The draft cannot become Commit 1 while the authority-bearing outer launch, end-to-end target no-trace property, operator-side recorder, several filler sources, and capture-time MainPID binding remain unresolved. The controlling reconciliation requires Commit 1 to fix the producer, argv, environment, cwd, output grammar, projection-v2 universe, placeholders, package manifest, and clean-HEAD rule; the draft itself still records blocking `UNKNOWN` values. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:62-70`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:19-27,582-591`

This is a T2 documentation/evidence review only. It is not acceptance, authorization, dispatch, or evidence that any command ran. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:3-5,604-604`

## Command-by-command target-write review

| Command or operation | Result | Finding |
|---|---|---|
| `git diff --quiet --` | Operator-side only; no target contact. The preregistration nevertheless must specify that rc `0`, not merely empty output, is required. `--quiet` is listed while the ordered rule says only “empty output/diff.” | **MUST-FIX-BEFORE-COMMIT** — make the rc/stdout/stderr acceptance tuple exact in the recorder. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:480-480,491-500` |
| `git diff --cached --quiet --` | Operator-side only; no target contact. It has the same unstated rc requirement. | **MUST-FIX-BEFORE-COMMIT** — make the rc/stdout/stderr acceptance tuple exact in the recorder. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:481-481,491-500` |
| `git ls-files --others --exclude-standard` | Operator-side only; no target contact. The required empty result is stated, but no exact recorder implements the check. | **MUST-FIX-BEFORE-COMMIT** — implement and package the check. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:482-482,491-500,560-570` |
| `git rev-parse --verify HEAD^{commit}` / object lookup | Operator-side only; no target contact. The command table names `HEAD:<path>`, while the ordered rule names `COMMIT_1:<path>`; those are not one byte-exact argv specification. | **MUST-FIX-BEFORE-COMMIT** — select one literal command sequence and implement it. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:483-483,493-497` |
| `git hash-object --no-filters <path>` | Operator-side only; without `-w` the declared operation does not write a Git object or contact the target. | **NOTE** — source-level target-read-only. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:484-484` |
| `git ls-tree -r --name-only ...` | Operator-side only; no target contact. The table uses `HEAD`, while the ordered rule uses `COMMIT_1`. | **MUST-FIX-BEFORE-COMMIT** — make the argv singular and literal. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:485-485,493-500` |
| Local SHA-256, byte count, and record creation | The draft confines the intended write to the operator root, not the target, but gives no recorder executable or exact output pathname beneath that root. | **MUST-FIX-BEFORE-COMMIT** — package the recorder and fix create-once path, argv, environment, cwd, serialization, close/fsync policy, and collision behavior. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:486-486,489-524,560-570` |
| `ssh … ATT-01` | **UNKNOWN** whether it leaves target traces: the draft expressly leaves sshd/PAM/auditd/root-wrapper logging unresolved, and the root-channel launch is also unknown. The review rule makes any possible target trace a must-fix. | **MUST-FIX-BEFORE-COMMIT** — settle or technically deny the infrastructure side effects before Commit 1. `C:\tmp\lane_kick\W2.md:35-39`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:21-27,466-474,487-487` |
| `/usr/bin/env -i … /usr/bin/python3 -I -S -B - …` | The Python child environment is enumerated, but **UNKNOWN** root-channel mapping means the pre-`env` process chain, initial target cwd, forced-command/wrapper behavior, and full outer argv are not fixed. Python calls `chdir('/')` only after interpreter startup and imports. | **MUST-FIX-BEFORE-COMMIT** — pin the entire launch chain and initial cwd, not only the post-start Python state. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:21-27,81-102,155-180,345-381,466-474` |
| `chdir('/')` | The embedded source changes only process cwd and opens no target path for writing. | **NOTE** — source-level target-read-only, but it does not cure the unfixed launch cwd before Python starts. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:97-97,362-381` |
| `readlink`, `realpath`, `lstat`, and `stat` | The source contains no explicit mutation API, but the end-to-end no-trace property remains **UNKNOWN** under the draft’s own runtime/infrastructure reservations. | **MUST-FIX-BEFORE-COMMIT** under the task’s zero-trace standard. `C:\tmp\lane_kick\W2.md:35-37`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:25-27,98-102,368-405` |
| `open`/`read` of the resolved interpreter leaf | The source uses `O_RDONLY|O_CLOEXEC|O_NOFOLLOW`; it has no create/truncate/append/read-write flag. **UNKNOWN**, however, whether ordinary reads or runtime/library loads change target metadata such as access-time state, because no filesystem-side-effect boundary is fixed. | **MUST-FIX-BEFORE-COMMIT** — prove a no-side-effect filesystem policy or enforce one; a source-code write-API inventory alone does not settle the stated rule. `C:\tmp\lane_kick\W2.md:35-37`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:25-27,100-102,181-201,368-381` |
| `open`/`read` of `/proc/self/mountinfo` | The source uses `O_RDONLY|O_CLOEXEC` and performs no explicit target write. End-to-end trace behavior is still **UNKNOWN** for the same infrastructure/runtime/filesystem reason. | **MUST-FIX-BEFORE-COMMIT** under the task’s zero-trace standard. `C:\tmp\lane_kick\W2.md:35-37`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:25-27,101-102,181-201,397-405` |
| In-process parsing, projection construction, base64, and SHA-256 | These operations use captured bytes and process memory; the visible source invokes no subprocess, socket, service, filesystem-write, or WP-I operation. | **NOTE** — source-level attestation-only. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:11-13,204-310,397-438` |
| `os.write` to inherited stdout/stderr | The visible source writes only to inherited fd 1/2, not a target pathname. The enclosing SSH/accounting trace remains **UNKNOWN**. | **MUST-FIX-BEFORE-COMMIT** for the end-to-end command until the enclosing channel is settled. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:25-27,103-103,323-332,437-453` |

## Required findings

### MUST-FIX-BEFORE-COMMIT — F1: full authority-bearing argv, launch environment, and cwd are not fixed

`ROOT_CHANNEL_TARGET_AND_LAUNCH` is explicitly `UNKNOWN`; the ATT-01 row contains `UNKNOWN OUTER ROOT-CHANNEL PREFIX`; and the displayed SSH command still contains `{{ROOT_CHANNEL_TARGET}}` plus a prose `<§3.2 exact inner argv>` marker. Therefore the document does not yet preregister one executable outer argv. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:19-23,462-474`

The statement that no argument may be shell-expanded is not established while the root-channel target, forced-command mapping, and wrapper/process chain are unknown. The inner `env -i` fixes the Python child environment only after the unknown outer launch has begun, and `chdir('/')` occurs inside Python after startup/imports. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:81-102,155-180,345-381,466-474`

What settles it: one committed authoritative source must pin the root principal/target, forced-command or wrapper mapping, complete literal SSH and remote argv, exact process chain, environment before and after `env -i`, initial remote cwd, stdin mapping, and allowed inherited descriptors; the final Commit-1 bytes must contain none of the three outer-launch markers above. The draft itself already says the missing source is required before Commit 1 and before any socket. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:21-23,466-474`

### MUST-FIX-BEFORE-COMMIT — F2: the mandated target no-mutation/no-trace claim is unresolved

The draft explicitly leaves both SSH infrastructure side effects and producer-runtime undocumented writes `UNKNOWN`, then repeats both as blockers to an absolute no-mutation claim. That is honest disclosure, but it is not closure under the task rule that any command capable of leaving a trace is a must-fix. `C:\tmp\lane_kick\W2.md:35-37`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:25-27,589-591`

The source-level inventory also does not settle target metadata effects of its ordinary reads or of interpreter/loader/import reads. The visible producer opens and reads the interpreter and mountinfo, while the draft offers only a future runtime trace or write-denial boundary as settlement. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:27-27,95-103,181-201,368-405`

What settles it: an authoritative channel statement plus an enforced boundary or exact-runtime evidence covering target files, metadata effects, sshd/PAM/audit/accounting/wrapper effects, and failure paths. If unavoidable infrastructure logging means the literal no-trace standard cannot be met, the current preregistration cannot be committed under that standard; a narrower definition would require an explicit owner decision, not inference. `C:\tmp\lane_kick\W2.md:29-37`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:23-27`

### MUST-FIX-BEFORE-COMMIT — F3: the operator-side capture producer does not exist in the package contract

The draft attributes clean-HEAD checks, stream capture, strict stdout validation, record serialization, PASS/STOP adjudication, and hashing to “the recorder,” but supplies no exact recorder source, executable, argv, environment, or stdin/stdout/stderr handling. The three-member package contains only the preregistration, target Python producer, and manifest. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:153-153,456-524,560-570`

This omission is authority-relevant: prose does not fix how an operator preserves raw stdout/stderr/rc, prevents overwrite, interprets `--quiet` return codes, or emits the exact record. Two implementations can produce different bytes or failure behavior from the same preregistration. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:489-524`

What settles it: add one normative operator-side recorder implementation and pin its executable/interpreter, full argv, cleared environment, cwd, exact input paths, create-once output pathname, atomic/collision behavior, byte serialization, rc/stdout/stderr capture, validation, close/hash behavior, and failure grammar. Include it in the package manifest and update the declared member count and clean-HEAD fence. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:66-70`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:560-570`

### MUST-FIX-BEFORE-COMMIT — F4: operator record grammar is not byte-canonical

The target stdout grammar is ordered and concrete, but the operator record uses underdefined metavariables including `<Git blob oid>`, `<positive-decimal>`, `<nonnegative-decimal>`, `<strict base64>`, `<decimal>`, and `PASS|STOP` without a packaged serializer. The draft also names only the operator root, not the exact record child pathname. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:49-49,118-153,499-524`

What settles it: the recorder required by F3 must define canonical decimal spelling, Git object format/length/case, RFC 4648 alphabet/padding/no-wrap rules, literal status values, LF/final-LF rules, exact child path, and duplicate/existing-path failure. This also settles whether two operators serialize the same capture identically. `C:\tmp\lane_kick\W2.md:40-45`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:504-524`

### MUST-FIX-BEFORE-COMMIT — F5: multiple fillers still lack one exact source path and field

`WPI_CANDIDATE_SHA` is sourced generically to an integration/fresh-staging identity record, while `WPI_MAINPID` is sourced to a “relevant” fresh-staging checkpoint; neither row pins one exact committed artifact path, object identity, stage/checkpoint, and field. The draft separately says both current values are `UNKNOWN`. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:33-50`

The allocation-derived fillers likewise cite “Lane-L1 allocation record” without an exact committed repo-relative path and identity, and the operator-root row refers to an unstated “attestation-record child rule.” `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:39-52`

What settles it: for every pre-Commit-1 filler, pin one committed source path, Git object/blob identity, exact key/field, grammar, and verbatim-copy rule. For MainPID, pin the exact checkpoint and freshness rule. For the operator root, pin the exact child-path derivation and create-once collision result. No allocation token may remain at Commit 1. `C:\tmp\lane_kick\W2.md:40-45`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:41-52`

### MUST-FIX-BEFORE-COMMIT — F6: the capture does not prove that `WPI_MAINPID` exists or is current

The projection builder treats `/proc/{{WPI_MAINPID}}/ns/net` only as a path string for lexical covering-mount selection. The producer reads namespace links for PID 1 and itself, but never opens, stats, or readlinks `/proc/<WPI_MAINPID>/ns/net`; it then repeats the fixed MainPID in stdout. An absent, stale, or reused MainPID is therefore not rejected by the shown checks. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:261-310,383-405,407-435,530-554`

What settles it: define and implement a read-only capture-time MainPID identity/liveness binding, its exact output fields and grammar, and the required relationship to the pinned candidate/staging evidence; STOP if the process is absent, changed, or cannot be bound. The exact source/checkpoint rule from F5 must say which identity is compared. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:33-35,44-45,89-89`

### MUST-FIX-BEFORE-COMMIT — F7: the clean-current-HEAD rule is not one executable, exact rule

The rule is presently prose, has no recorder implementation, describes `git diff --quiet` via empty output rather than explicit rc, and alternates between `HEAD:<path>`/`COMMIT_1:<path>` and `HEAD`/`COMMIT_1` spellings. It therefore does not yet fix one argv/rc/output contract that gates the socket. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:476-500`

What settles it: implement the ordered gate in the packaged recorder with literal executable paths/argv, expected rc/stdout/stderr for each command, one derived commit variable used consistently, force-inclusive package enumeration, exact raw-worktree-to-blob comparisons, and fail-closed behavior before local record creation and before the socket. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:489-502`

## Requirement coverage

| Required element | Status | Basis |
|---|---|---|
| Target producer | **PARTIAL** | The normative Python body and its source-level operation set are present, but runtime effects are `UNKNOWN`, and the operator recorder is absent. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:13-27,155-454,456-524` |
| argv | **FAIL** | Inner argv is shown, but outer root launch remains `UNKNOWN` and contains unresolved markers. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:81-91,462-474` |
| environment | **PARTIAL** | The Python child environment is enumerated; the pre-child root-channel/wrapper environment is not established. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:21-27,81-91` |
| cwd | **FAIL** | `/` is enforced only after Python starts; the initial remote launch cwd is not fixed by the displayed argv. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:81-102,345-381` |
| Target stdout/stderr/rc grammar | **PASS on paper** | Ordered success output and fail-closed rc/stderr classes are stated. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:107-153` |
| Operator record grammar | **FAIL** | Metavariables are not byte-canonical and no serializer is packaged. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:504-524,560-570` |
| Projection-v2 universe | **PARTIAL** | The 21 points, 6 roots, ordering, tie rule, and algorithm are fixed, but the MainPID point is only lexically projected and not capture-time bound. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:261-310,526-558` |
| Placeholders | **FAIL** | Several fillers lack one exact committed source path/field, and the root route is explicitly `UNKNOWN`. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:19-23,33-52,582-591` |
| Package manifest | **FAIL** | Its three-member grammar is stated, but it omits the recorder needed to execute the capture contract. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:456-524,560-572` |
| Clean-current-HEAD rule | **FAIL** | The intended sequence exists only as non-singular prose and has no packaged implementation. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:476-502` |

## Attestation-only and transport cross-check

### NOTE — attestation-only boundary is sound as currently drawn

The visible target payload performs observations, hashing, projection construction, and channel output; it contains no subprocess, socket, service API, host allocation, or WP-I predicate execution. The draft gives it a separate `ATT-01` row and states that WP-I ops 01–12 do not run between Commit 1 and Commit 2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:9-13,93-105,155-454,462-466,574-580`

### NOTE — transport table shape matches, but transport operations must remain excluded

The ATT-01 row uses the transport plan’s nine columns and copies its hardened SSH-option envelope. The later transport plan, however, separately creates the remote base, uploads an archive, verifies/extracts it, runs P0 and RO, probes TCP, closes/hashes evidence trees, retrieves evidence, and binds digests. Those are WP-I transport/operation rows, not attestation capture, and none may be imported into Commit 1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:458-474`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:1-13`

The owner record also distinguishes the unwritten attestation-only Commit 1 from later WP-I operations and makes the grant conditional on exact committed bytes; all other host/credential actions remain excluded. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-58`

## Final disposition

Do not commit or dispatch this draft. Repair F1–F7, fill every pre-Commit-1 dependency from one pinned source, regenerate the package/manifest with the recorder included, and repeat this adversarial review on the exact final bytes. The current document itself says Commit 1 cannot be complete while its root route and no-mutation boundaries remain unresolved. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_2026-08-15.md:19-27,582-604`

`NO SOURCED ESTIMATE`: no source provides a disjoint repair estimate for these findings. The work catalogue prices creation of Commit 1 as a whole but does not disaggregate these repairs. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:33-36,48-54`
