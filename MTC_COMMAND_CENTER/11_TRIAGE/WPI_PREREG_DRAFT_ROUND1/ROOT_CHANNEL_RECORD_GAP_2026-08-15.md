# V1 — Root-channel record gap

## Result

The repository establishes two things and only two things about the relevant channels:

1. Barış authorized a narrowly scoped root execution on `GATEA-STAGING`, and grant #6 may use that same root session for one separately preregistered, committed, read-only capture.
2. The later WP-I transport has a concrete, different, unprivileged route: the pinned `gatea_ed25519` identity is invoked as `gatea@172.24.55.233`, followed by an inner `/usr/bin/env -i ... /usr/bin/bash --noprofile --norc` command.

The repository does **not** establish how the authorized root session is obtained. For the privileged channel, all eight requested facts remain `UNKNOWN`: SSH principal, account shell, forced command, wrapper mapping, pre-`env` environment, initial cwd, descriptor set, and mutation-denial wrapper.

This is not solely an observation chicken-and-egg problem. Five facts are facts of the eventual host channel and can only be proved by an authoritative record of that channel or an authorized read-only observation. Three facts first require a decision that the repository does not contain: the privileged route/principal, its direct-root-versus-wrapper mapping, and the mutation-denial control. Host observation cannot choose among multiple possible routes or invent a missing enforcement contract.

No host, network, SSH, credential, deployment, service, or other excluded action was performed.

### Source-state note

The detached worktree at `C:\RO` is at `25564449b8a8254eaa75535039acef4993f5f27e`. The Commit-1 draft v2 is absent there, and its self-confirming-check path is an empty file there. The nonempty versions used by v2 are tracked together in Git object `cd735760d32158d4ef97e3bc4b9524c95f35f77b`. I read them with read-only Git object access. Citations to those two paths below refer to that object. No checkout or repository write occurred.

## 1. Record sweep

### 1.1 Owner authority grants root scope, not a root route

The original authorization ledger says:

> “You may run `RPD-VERIFY.sh` as root on `GATEA-STAGING`.”

`MTC_COMMAND_CENTER/11_TRIAGE/NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md:23-25`

It then says grant #6 may use “Grant #3's root session” for one preregistered command set and that it is the “same session and limits as grant #3.” It supplies no principal, shell, forced command, wrapper, environment, cwd, or descriptor mapping.

`MTC_COMMAND_CENTER/11_TRIAGE/NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md:28-34`

The consolidated ledger preserves exactly that boundary:

> “Run `RPD-VERIFY.sh` as root on `GATEA-STAGING`, read-only. Root is granted only for that block.”

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:55`

> “In the G3 root session, run one separately preregistered and committed read-only command set...”

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:58`

The later owner decision authorizes use of “the pinned SSH identity,” but again does not name the privileged SSH principal or server-side mapping:

> “I authorize the exact preregistered and committed read-only grant-#6 attestation capture and WP-I operations on `GATEA-STAGING`, including use of the pinned SSH identity solely for those actions...”

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-38`

That grant is conditional on Commit 1 containing the exact “producer, argv, environment, cwd and output grammar”; the record says those bytes had not been written.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-52`

Conclusion: authority to run as root is established. The mechanism that turns the pinned identity into the authorized root process is not.

### 1.2 The transport plan establishes only the unprivileged route

The first SSH row literally invokes:

> `... gatea@172.24.55.233 /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea /usr/bin/bash --noprofile --norc -s -- ...`

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:2`

The P0 and RO rows use the same `gatea@172.24.55.233` target and inner launch string.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:5-6`

No transport-plan row invokes a root principal, `sudo`, `doas`, a forced command, or a root wrapper. These rows therefore cannot establish the separate grant-#3/#6 root channel.

### 1.3 `run_p0.sh` and `run_ro.sh` expressly leave the outer boundary open

Both wrappers repeat the transport plan's inner child:

> `/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea /usr/bin/bash --noprofile --norc -s --`

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh:8-12`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh:5-9`

Both then state that the outer SSH account-shell boundary is open. `run_p0.sh` explains:

> “`sshd` does not execute the command string itself: it hands the string to the account's shell, and that shell processes its own startup environment BEFORE the string's first token, `/usr/bin/env`, ever runs.”

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh:51-64`

It says closure would need “a deploy-channel-attested forced-command or execution contract, or a transport path with no unbound shell,” and ends: “A DISCLOSURE IS NOT A CONTROL.”

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh:65-72`

`run_ro.sh` makes the same statement and the same non-claim.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh:45-66`

The canonical transport status agrees: “inner child closed; outer SSH account-shell boundary open.” It explains that `sshd` gives the command string to the account shell, which processes its startup environment before the first token.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md:31-38`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md:165-178`

That residual was owner-accepted for the **unprivileged later transport**. Acceptance-with-disclosure is not evidence of the privileged channel and is not a mutation-denial control.

### 1.4 The RP7 harness neither obtains nor proves privileged authority

`RP7-WPI-RO.sh` labels itself an authoring-only proposal and says its bytes grant no host contact, transport, or credential authority. It also permits create-once writes inside `EV_DIR`, so it is not the no-target-mutation ATT-01 wrapper v2 needs.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:2-14`

Its final claim explicitly says it does not establish `host_authority`.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:2276-2278`

The harness does define cleared environments and descriptor handling for its own evidence-producing children, for example `cd "$EV_DIR"` followed by `env -i` and bounded child execution.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:302-306`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:331-376`

Those are inner-child mechanics after the harness is already running. They do not establish the SSH principal, account-shell startup, pre-`env` state, initial target cwd, inherited descriptor universe, or privileged wrapper that caused the harness process to exist.

### 1.5 The successor preregistration requires the missing facts but does not supply them

The successor draft says the attestation is produced through “the separately preregistered read-only root command set covered by grant #6.”

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:476-484`

It requires Commit 1 to carry the “pinned command/producer identity, argv, clean environment, working directory” and the operator-side route before a socket or root command starts.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-525`

It does not provide those values. Its separate transport discussion also keeps the outer SSH account-shell boundary open.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:452-462`

### 1.6 Commit-1 v2 records the same gap precisely

V2's disposition says it is not dispatchable because the exact root-channel launch and mutation-denial/crossover facts remain `UNKNOWN`.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:1-7`

Its review-disposition row says the sources grant a root session but do not establish “its SSH principal, account shell, forced-command/wrapper mapping, pre-`env` environment, initial cwd, descriptor set, or mutation-denial wrapper,” while the transport plan establishes only `gatea@172.24.55.233`.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:9-18`

V2 defines the missing binding record and its required fields, including `SSH_TARGET`, account UID/GID and shell, forced-command mode, root-wrapper identity, target process chain, initial cwd, pre-`env` environment, FD mapping, and mutation-denial control.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:139-168`

It then states:

> “No examined source establishes those values... Therefore every field is currently `UNKNOWN`.”

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:170`

The proposed ATT-01 row remains non-executable: outer argv, process chain, initial cwd, forced-command mode, and mutation-denial control are all `UNKNOWN`.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:188-206`

### 1.7 The original Gate-A staging runbook does not define a privileged login

The runbook requires only that the host be reachable and says, “Credentials stay owner-held. Provide reachability, not secrets.”

`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md:29-54`

It contains no SSH principal, account shell, forced-command, sudo/root-wrapper, initial-cwd, environment, descriptor, or mutation-denial mapping for grant #3 or grant #6.

### 1.8 Broader-record follow-up: limited Gate-A sudo is not the G3/G6 route

A repository-wide targeted search found later Gate-A records outside the requested runbook. Run-kit D and E say Gate-A ran as `gatea` with passwordless sudo for enumerated command families.

`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt:150-171`; `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/README.txt:434-461`

The A-7 preflight proves only command-specific NOPASSWD families. A generic `sudo -n -v` returned “a password is required”; the exact limited families then returned rc 0.

`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A7_PREFLIGHT_2026-08-09D.md:24-43`

No record maps grant #3/#6, `RPD-VERIFY.sh`, the ATT-01 Python producer, or `/usr/bin/env` to one of those command-specific sudo rules. Therefore this is useful context, not category-(a) closure and not evidence that the privileged channel is `gatea + sudo`.

## 2. Eight-fact table

`UNKNOWN` means no cited record establishes the exact fact. A specified desired value is not an observed or independently bound value.

| V2 fact | Repository status | Gap class | What would settle it |
|---|---|---|---|
| SSH principal | **NOT ESTABLISHED — `UNKNOWN`.** The host address, key path, and unprivileged `gatea` principal are fixed for ops 01–12; D2 permits a pinned identity; neither names the privileged target. | **(c), then (b) verification.** Someone must first select which server mapping is the G3/G6 route; observation can then prove that the selected mapping exists. | A Barış/host-administrator decision naming the exact privileged `user@address` and whether the pinned key is intended for that principal, followed by independent server-side key-to-principal binding evidence. Do not infer `root@172.24.55.233` or reuse `gatea@...`. |
| Account shell | **NOT ESTABLISHED — `UNKNOWN`.** The run wrappers prove that an account shell is security-relevant; they do not name its path or bytes. | **(b).** It is a property of the selected account/server configuration. | An authoritative provisioning/account record or a later authorized read-only observation binding the selected principal to the exact shell path and executable identity. |
| Forced command | **NOT ESTABLISHED — `UNKNOWN`.** The wrappers name a deploy-attested forced command as one possible closure, not as an existing fact. | **(b).** `NONE` is also a fact, but it must be proved from the selected key/sshd configuration. | An authoritative effective sshd/authorized-key mapping that yields byte-exact forced-command argv or explicit `NONE`. |
| Wrapper mapping | **NOT ESTABLISHED — `UNKNOWN`.** No record selects direct root, `gatea` plus escalation, or another wrapper. Limited Gate-A NOPASSWD families do not include ATT-01/RPD. | **(c), then (b) verification.** The intended privileged route is undecided in the record. | A Barış/host-administrator decision choosing direct root versus one exact wrapper/escalation chain, followed by independent configuration evidence for that exact chain. |
| Pre-`env` environment | **NOT ESTABLISHED — `UNKNOWN`.** The inner child environment is exact; the server/account-shell environment before `/usr/bin/env -i` is explicitly open. | **(b).** It is runtime/channel state after the route is selected. | A byte-preserved, independently sourced record of the first target process environment immediately before `env -i`, including absence/presence of `BASH_ENV`, `ENV`, loader variables, functions, and hooks. |
| Initial cwd | **NOT ESTABLISHED — `UNKNOWN`.** V2 fixes `/` only after its Python code calls `chdir`; that is not the cwd at account-shell/interpreter startup. | **(b).** It is runtime/channel state. | An independently bound record of cwd for the first target command process, before shell startup, Python import, or any `chdir`. |
| Descriptor set | **NOT ESTABLISHED — `UNKNOWN`.** V2 specifies the desired `0/1/2` mapping, but no record proves the inherited set or closes all others. | **(b).** It is runtime/channel state. | An independent record of every inherited FD, target, access mode, and close-on-exec state at the first target process, proving `0=ssh-stdin`, `1=ssh-stdout`, `2=ssh-stderr`, and no other inherited writable descriptor. |
| Mutation-denial wrapper/control | **NOT ESTABLISHED — `UNKNOWN`.** Source inspection constrains the visible producer but V2 expressly says it does not prove the interpreter, loader, account shell, PAM, audit rules, wrapper, or failure paths cannot mutate. | **(c), then (b) execution proof.** No repository decision selects the required enforcement control. | A Barış/host-administrator decision naming the exact enforcement mechanism and its owner, followed by identity binding and discriminating success/failure-path proof that category-1 mutation is denied while fd 1/2 remain usable. Producer source inspection alone is insufficient. |

No fact is category (a): the targeted repository-wide search found no separate authoritative record that closes any row. The later Gate-A sudo records are the only plausible lead found, and they prove only a limited, different command family.

### Adjacent blocker outside the requested eight

Even if all eight rows were settled, V2 separately requires `INFRASTRUCTURE_CROSSOVER_RESULT`: no native auth/audit append may cause rotation, out-of-store action, or side-effecting PAM/wrapper hooks. That result is also `UNKNOWN`.

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:41-49`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:167-170`

This report therefore does not imply that resolving the eight facts alone makes Commit 1 ready.

## 3. Self-confirming-check assessment

The governing note defines the defect as “A check that can pass without proving the thing it claims,” asks what would make the check fail, and says a property with no enforcement mechanism is only a comment.

`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:6-23`; `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`

Applied here:

| Check or proposed check | What makes it fail? | Where does the expectation come from? | Assessment |
|---|---|---|---|
| `run_p0.sh` / `run_ro.sh` inner environment sweep | Wrong inner Bash, login-shell mode, an unexpected `/proc/self/environ` entry, a missing expected entry, or an inherited function. | Constants in the wrapper are compared with the kernel's actual inner-child environment. | A real check for the **inner child**, not decorative. It cannot fail when an earlier account shell processes a startup plant and exits before the wrapper executes. It proves no outer-channel fact. |
| `execution_euid=0` or an `id -u == 0` check | It fails when the observed namespace-local EUID is nonzero. | The process itself. | Insufficient for the privileged channel. The catalogue records that namespace-local UID 0 can pass without host-root authority. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:111-176` |
| Desired `ATT01_FD_MAPPING` copied into a binding TSV and recorder constant | A typo or mismatch between two copied values. | If both values are produced by the Commit-1 builder, the same process supplies artifact and expectation. | Decorative unless the expected mapping comes from independent server/runtime evidence and the actual first-process FD set is observed. |
| Source scan showing no write API in the Python producer | A visible prohibited API or write-capable open appears in that source. | The producer source itself. | Useful source-scope evidence, but not mutation-denial evidence for sshd, PAM, shell, loader, wrapper, runtime, or failure paths. It cannot go red for an external hook's write. |
| Gate-A “passwordless sudo” label | One of the exact enumerated command-family invocations returns nonzero. | The run-kit command list, checked by the A-7 preflight. | Real for those limited families. It does not test an ATT-01/RPD/env/Python root wrapper and therefore cannot prove the G3/G6 route. |
| Future mutation-denial control | A deliberate target-write mutation succeeds, a failure path writes, an extra writable FD survives, or the control can be bypassed before it starts. | Must come from an independently bound enforcement policy, not from the producer that is being constrained. | No such check/control exists in the record. V2 correctly leaves it `UNKNOWN`; any final proof needs real RED/GREEN evidence on the exact executable chain. |

The key expected-value rule is therefore: `STAGE1_ROOT_CHANNEL_BINDING.tsv` cannot be accepted merely because the launcher and recorder agree with values copied from that same TSV. The server/account configuration or independently observed first-process state must supply the expectation; otherwise the check can fail only on a typo.

## 4. Narrow owner question

There are category-(c) facts, so the gap is not purely “use the channel to observe the channel.” The owner/admin must choose the privileged route and the mutation-denial design before the remaining category-(b) observations can have a single subject.

Exact fill-in sentence for Barış:

> **“For grants #3/#6, I select `<exact SSH principal and address>` using the already approved pinned identity as the sole privileged route, with `<direct root | exact account-shell → forced-command/root-wrapper chain>` as the complete pre-`env` mapping, and I select `<exact named enforcement control>` as the mandatory category-1 mutation-denial control; this decision grants no host contact, configuration change, execution, or broader credential authority.”**

The angle-bracket fields are decisions, not values this lane can derive. Barış should not sign the sentence with placeholders. If he does not know the host implementation, the exact narrower question is:

> **“Is the intended G3/G6 channel direct-root SSH, the existing `gatea` identity plus a dedicated exact root wrapper, or a forced-command key, and which exact control is intended to deny category-1 mutation before and during the capture?”**

Answering that question does not establish the five category-(b) runtime facts and does not authorize observing them. It only removes the currently missing design subject.

## Final disposition

- Root authority: **ESTABLISHED, narrow and unspent**.
- Unprivileged `gatea` transport: **ESTABLISHED for later ops 01–12 only**.
- Privileged root-channel mechanism: **UNKNOWN**.
- Eight v2 facts: **0 established, 0 fully category-(a), 5 category-(b), 3 category-(c) with later verification required**.
- Commit-1 readiness: **BLOCKED**; no acceptance or authorization is created by this report.
