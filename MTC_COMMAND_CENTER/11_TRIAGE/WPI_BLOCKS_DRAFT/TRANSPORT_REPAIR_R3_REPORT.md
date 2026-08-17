# WP-I transport set — repair round 3

**Implementer:** `claude-opus-5`, xhigh, fresh session, 2026-08-10.
**Contract:** `KICKOFF_TRANSPORT_REPAIR_R3.md`, closing the round-2 re-audit lists —
Codex `gpt-5.6-sol` xhigh `REQUEST_CHANGES 4` + N1
(`TRANSPORT_CODEX_REAUDIT_R2_2026-08-10.md`) and Claude `claude-opus-5` xhigh
`REQUEST_CHANGES 1` (`TRANSPORT_CLAUDE_REAUDIT_R2_2026-08-10.md`).
**Rejected baseline:** commit `9ef4437d`, whose eight blobs re-derive to exactly the
identities both re-audit reports recorded.
**Round 3 of the T0 cap 3 — the last round of the cap.**

**Safety state.** No host contact, no SSH/SCP connection, no host key offered, no
credential read, no RUNID allocated, no archive built, nothing frozen, no Git commit.
`C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry. **2026-08-12 transport prose
repair marker:** this historical sentence did not paste a directory listing and must
not be treated as external-listing evidence; the repaired proof is construction-based:
the shipped runner's marker gate fires before record-root creation and `Flush-Log`
writes nothing before `RecordReady`. The real pinned `ssh.exe` and `scp.exe` were
executed locally without connecting — `ssh -G` evaluates configuration and exits; `scp`
copied one local file to another — which round-2 F2 required and which cannot be
established any other way. The only sockets attempted were loopback with port 9
closed. `RP6-P0.sh`, `SELF_QA_RP6.md` and `STATUS_RP6_P0.md` were neither read nor
written: they are under concurrent repair.

---

## 1. Finding → disposition → evidence

### F1 — CRITICAL, both flagships — CLOSED

*An observed rc outside the preregistered `{0,1,3}` grammar, and any native transport
or cleanup failure, must be not-evaluable → `TR_RUN STOP`, runner exit 3.*

**Disposition.** `transport_runner.ps1` no longer classifies by integer. A new
`Get-OpOutcomeClass` decides by operation **kind** and by **provenance**:

| kind | result | everything else → not-evaluable |
|---|---|---|
| `ssh_stdin` | rc ∈ `{0,1,3}` **and** the capture carries a preregistered remote result-line prefix | rc 255 (`ssh_transport_failure_rc255`); any other rc (`rc_outside_outcome_grammar`); no marker (`no_remote_program_marker_in_capture`) |
| `scp_up`/`scp_down` | rc 0 only | every non-zero rc (`scp_transfer_did_not_complete`) — scp's failure rc is 1, which collides with FAIL and cannot be separated by rc alone |
| `tcp_probe`, `local_bind` | rc ∈ `{0,1,3}`; rc 1 is a genuine observation | rc outside the grammar |

Cutting across all kinds: an `always` cleanup op whose prerequisite sequence never
completed is classified `cleanup_after_unestablished_prerequisite`, never deviant. FAIL
remains reachable only for an operation that ran and returned the deviant value its own
contract defines. `TR_FIRST_FAIL` is renamed `TR_FIRST_MISMATCH` and `first_fail=` to
`first_mismatch=`, because the old token labelled a STOP as a FAIL in the record.

**Evidence** (`SELF_QA_TRANSPORT.md` §4; 2026-08-12 transport prose repair marker:
this report's original shorthand under-counted the J-family runner executions and did
not state the supported OpenSSH count. Corrected coverage is eleven J-family runner
executions because J5 is GREEN-only, plus K1-K2; real pinned OpenSSH starts are 17 by
M7-row reading or 10 by M7-arm reading, with L1-L3 starting none):

| arm | RED — round-2 bytes `2f076ed9…` | GREEN — round-3 bytes |
|---|---|---|
| J1 whole 12-row plan, early STOP, every `always` row runs | `deviant=4 not_evaluable=3`, **`TR_RUN FAIL` rc 1** | `deviant=0 not_evaluable=7`, **`TR_RUN STOP` rc 3** |
| J2 ssh native rc 255 | `TR_OP_DEVIANT id=01 rc=255` → FAIL rc 1 | `reason=ssh_transport_failure_rc255` → STOP rc 3 |
| J3 rc 2, outside the grammar | FAIL rc 1 | `reason=rc_outside_outcome_grammar` → STOP rc 3 |
| J4 ssh rc 0 with no output at all | **treated as a match**; ops 02–05 all ran | `reason=no_remote_program_marker_in_capture` → STOP rc 3 at op 01 |
| J5 a block that ran and returned 1 | — | `class=deviant` → **`TR_RUN FAIL` rc 1** (FAIL survives) |
| J6 failed scp transfer | FAIL rc 1 | `reason=scp_transfer_did_not_complete` → STOP rc 3 |
| K1/K2 the real pinned `ssh.exe` | rc 255, empty-file digest on both streams, `TR_OP_DEVIANT` → FAIL rc 1 | rc 0 with real output, `not_evaluable` → STOP rc 3 |

J1 is the case Codex named: one honest STOP at op 01 was outvoted by four consequences
of itself — a close that found no tree (rc 1) twice and two failed retrievals.
J4 exposed a defect neither re-audit had named: under round 2, an `ssh` that returned 0
having produced nothing was a **match**, so the plan ran on and spent both one-use
stage RUNIDs. That is now a STOP at op 01.

### F2 — CRITICAL — CLOSED

*The constructed child environment cannot run the real pinned OpenSSH.*

**Disposition.** Codex's second branch, taken: ambient configuration is disabled and
every configuration input is supplied as a pinned argument or a pinned file.

- `PROGRAMDATA` is set to a run-owned, freshly created, empty directory under the
  record root. Measurement (`M7`) shows it is the **only** load-bearing variable:
  dropping any other constructed variable leaves `ssh -G` at rc 0; dropping
  `PROGRAMDATA` gives rc 255 with zero bytes.
- `-F none` is now the first element of every `ssh`/`scp` op, refusing **both** the
  per-user and the system-wide `ssh_config`.
- `UserKnownHostsFile`, `GlobalKnownHostsFile`, `ProxyCommand=none`,
  `ControlMaster=no`, `ControlPath=none`, `PermitLocalCommand=no`, `ForwardAgent=no`,
  `ForwardX11=no`, `ClearAllForwardings=yes` added.
- **Nothing is carried** from the operator environment. `USERPROFILE`, `HOMEDRIVE` and
  `HOMEPATH` are gone: measurement showed OpenSSH for Windows resolves the home
  directory from the OS token, so carrying them never closed that channel — only
  `-F none` plus the pinned files does. The child now receives eight variables, each
  printed with the reason it exists (`TR_ENV … why=`).
- The option block is frozen **inside the runner**; every `ssh`/`scp` plan row must
  carry it verbatim after the program name. The identity file and both `known_hosts`
  files are bound by kind, reparse state and frozen digest before the first process
  starts; the identity file's digest is compared but never printed.

**Evidence** (`SELF_QA_TRANSPORT.md` §5 and §4):

| arm | result |
|---|---|
| M1 RED, round-2 environment, real `ssh.exe` | `rc=255 stdout_bytes=0 stderr_bytes=0` |
| M2 | `+PROGRAMDATA` alone → `rc=0 stdout_bytes=3915` |
| M7 one-variable-out bisect | only `without_PROGRAMDATA` fails |
| M3 RED | ambient system `ssh_config` → `proxycommand … SYSTEM_CONFIG_HIJACK` |
| M4 GREEN | same hostile file + `-F none` → no `proxycommand` line |
| M5 RED / M6 GREEN | per-user config honoured via `-F`; `-F none` selects nothing; whole pinned set observed in effect |
| K1 RED / K2 GREEN | the same, driven through the runner's own `Invoke-ExternalProcess` |
| K3 | the real pinned `scp.exe` through the runner, local-to-local, `TR_RUN PASS` rc 0, bytes moved, no socket |
| L2 | a plan row dropping `-F none` → `plan_row_pinned_option_differs`, rc 3 |
| L3 | an unfilled configuration pin → rc 3 |

`cmd.exe` remains a substitute in the J family only, for driving native statuses
deterministically; it is supplemental, and the K family carries the F2 closure.

**Scope, stated rather than implied.** `ssh -G` and a local `scp` copy establish that
the real programs initialise under the constructed environment, parse the pinned
option block and apply it. They do not establish that the host accepts the pinned host
key, that the credential authenticates, or that a remote `bash -s` runs.

### F3 — CRITICAL — CLOSED by derivation, per the Lead adjudication

*Derive, do not edit.* The accepted `remote_close_tree.sh` is byte-frozen and is **not
edited**: its digest re-verifies as `87157f0e…` / 7470 B and `git status` shows no
change under `02_PREREG/`.

**Disposition.** New fourth derived script `remote_close_tree_wpi.sh` (12039 B). Its
only semantic delta against the accepted original is derivation class 2: every tool it
invokes — `mktemp`, `stat`, `tr`, `readlink`, `find`, `sort`, `sha256sum`, `cmp` **and
`rm`** — resolved from the frozen absolute `/usr/bin/<tool>` pin set under the same
non-following-kind / numeric `0:0` / not-group-or-world-writable admission the other
derived scripts use, with no inherited-`PATH` lookup anywhere. `rm` was not in the
kickoff's enumeration; the accepted bytes invoke it three times, so it is pinned too.

The derivation diff's **deletion** side is seventeen non-comment lines. Sixteen are a
bare tool invocation replaced by the same invocation through its pin; the seventeenth
is the `usage` diagnostic string, which names the script. No predicate, rc, ordering,
output record or comparison changed. The rendered `%U:%G` owner comparison is retained
deliberately — making it numeric would be a class 3 change and is outside the permitted
delta.

Runtime tool digests are emitted as evidence and explicitly **not** compared to pins,
with that limit stated in the script's own `CLOSE_NOTE tool_digest_limit …` line and
its header, because no remote tool digest can be known before host contact.

**Evidence** (`SELF_QA_TRANSPORT.md` §2 — Codex's PATH-first `sha256sum` attack):

| arm | result |
|---|---|
| RED, accepted bytes | `PATH_PLANT_CONSULTED=yes calls=5`, `MUTATED=yes`, rc 0, `CLOSE PASS … wrote_into_evidence_tree=0`, and `CLOSE_DIGEST a8201c99…  a.txt` — the post-mutation digest |
| G0, derived as shipped | `CLOSE_STOP reason=tool_is_symlink path=/usr/bin/stat`, rc 3, nothing mutated (deviation D-3) |
| GREEN, derived with pins retargeted | `PATH_PLANT_CONSULTED=no`, `MUTATED=no`, rc 0, `CLOSE_DIGEST b6a98d9c…  a.txt` — the true value |
| CTL | GREEN reproduced with no plant on `PATH` |

`TRANSPORT_PLAN.tsv` ops 07/08 now name `PREREG:remote_close_tree_wpi.sh` with a
`<PIN-AT-FREEZE>` stdin digest. The `ACCEPTED` stdin root token stays registered in the
runner: §4 still records the accepted original as the derivation basis, and both
resolution directions of the token remain covered by the round-2 arms.

### F4 — HIGH — CLOSED by binding, per the Lead adjudication

*Bind, do not waive.*

**Disposition.** `remote_setup_wpi.sh` projects the covering mount of `EXPECT_PARENT`
from `/proc/self/mountinfo` — longest matching mount point, later record wins a tie,
shared mount points counted — and compares it against a new `EXPECT_PARENT_MOUNT`
`<PIN-AT-FREEZE>` constant, **before the first `mkdir`**. An unfilled or malformed pin
is a missing input at rc 3; a mismatch is STOP before any mutation. The reader handles
three exit conditions, not one. No new tool pin was needed: the projection is parsed
with shell builtins.

**Evidence** (`SELF_QA_TRANSPORT.md` §3):

| arm | result |
|---|---|
| RED, round-2 bytes `e91bae08…`, decoy bind-mounted over the parent | `SETUP PASS` rc 0, **`DIRS_CREATED_IN_DECOY=4`, `DIRS_CREATED_IN_ACCEPTED_OBJECT=0`** — with `owner=0:0 mode=755` and `readlink -f` answering the expected path |
| GREEN, round-3 bytes, same decoy | `SETUP_STOP reason=parent_mount_differs`, rc 3, **zero directories anywhere**; observed `root=/wpi_r3_f4/decoy` vs attested `root=/` |
| CTL, nothing substituted | `parent_mount_bound … attestation=deploy_channel_before_op_01`, rc 0, four directories |
| PIN, exactly as shipped | `SETUP_STOP reason=mount_pin_unfilled field=EXPECT_PARENT_MOUNT`, rc 3 |
| N1–N5, the reader | no records → `mountinfo_no_records`; short record → `mountinfo_record_short fields=5`; no separator → `mountinfo_record_no_separator`; **populated final record with no trailing newline → rc 0, four directories (consumed, not dropped)**; nothing covers the parent → `mountinfo_no_covering_mount` |

### N1 — nit — CLOSED

Re-derived from the rejected baseline: **36 / 27** over the six executable/plan files
and **41 / 33** over all eight — exactly the correction both re-audits asked for. The
round-2 claim of "36 / 40" is corrected in `SELF_QA_TRANSPORT.md` §9, which also states
the round-3 delivered figures over the set it closes (seven executable/plan files, now
that `remote_close_tree_wpi.sh` joins the set).

---

## 2. Draft edits (`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`)

Narrow, and each traceable to a finding:

| § | edit | why |
|---|---|---|
| 4 table | new row `remote_close_tree_wpi.sh` as the fourth derived script | F3 |
| 4 table | `remote_close_tree.sh` row rewritten as **derivation basis only; it no longer travels**, with the reason recorded | F3 |
| 4 disposition ¶ | replaces the round-1.5 wording: no accepted Stage-2 script travels unchanged any more; the accepted originals stay byte-frozen and unedited | F3 |
| 4 class 2 | extended to all derived scripts; records the `mktemp` residual in the close script and the runtime-digest-as-evidence-only limit | F3 |
| 4 class 3 | **mount-object binding added**, with the projection rule, the rc-3 missing-input pre-check, and the freeze-gate/successor-ordering requirement | F4 |
| 4 (new ¶) | operator-side configuration identity: the measured `PROGRAMDATA` failure, `-F none`, pinned `known_hosts`, nothing carried, the frozen option block, and the scope limit | F2 |
| 5 option block | replaced with the round-3 block, each option's purpose stated; freeze-gate inputs named | F2 |
| 5 op table | ops 07/08 now name `remote_close_tree_wpi.sh` | F3 |
| 5 (new ¶ + table) | **observed-outcome grammar per kind**, plus the `always`-cleanup rule; "first-FAIL" renamed "first-mismatch" | F1 |
| 7 | ops 07/08 run the derived script; the `wrote_into_evidence_tree=0` claim explained as something the derivation earns, with the falsification recorded | F3 |

Nothing else in the draft was touched. §8's expectation tables, §10's path-scope
material and §12's safety state are unchanged.

---

## 3. Freeze-gate inputs

Round 3 adds five. Until each is supplied the runner or the script STOPs at rc 3.

| input | consumer | source |
|---|---|---|
| `EXPECT_PARENT_MOUNT` | `remote_setup_wpi.sh` | the read-only attestation set authorised as **owner grant #6**, in the grant-#3 root session, **ordered before op 01** |
| `wpi_known_hosts` + SHA-256 | runner, every ssh/scp op | preregistered host-key material for `172.24.55.233` |
| `wpi_known_hosts_global` + SHA-256 | same | system half of the same decision |
| SHA-256 of `gatea_ed25519` | same | the pinned credential; compared, never printed |
| bytes + SHA-256 of `remote_close_tree_wpi.sh` | plan ops 07/08, §4 | Stage 1 |

Carried forward unchanged from earlier rounds: `BASE_RUN` / `CONFIRM_TOKEN` /
`RECORD_ROOT` allocation, `PLAN_SHA256`, the `runkit.tar` digest, the five stdin
digests, `EXPECT_UID` / `EXPECT_GID`, `EXPECT_ARCHIVE_BYTES` and the six member
digests, `RP6_P0_SHA` / `RP7_WPI_RO_SHA` and the RP6/RP7 tool-pin inputs, and the two
`ssh`/`scp` program digests.

---

## 4. Delivered identities

Per-file SHA-256, bytes and placeholder counts, re-derived after every fixture had run
and its scratch had been removed. This report is not self-hashed.

| file | bytes | SHA-256 | `<ALLOCATE-AT-DISPATCH>` | `<PIN-AT-FREEZE>` |
|---|---:|---|---:|---:|
| `run_p0.sh` | 5215 | `e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80` | 6 | 3 |
| `run_ro.sh` | 5933 | `cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8` | 6 | 5 |
| `transport_runner.ps1` | 57826 | `13a57438c12effa108aacc39bbe91345acf7551b76f0991a669059040c5590e4` | 4 | 8 |
| `TRANSPORT_PLAN.tsv` | 7219 | `2a1cd2a65d447526dee8748b17a762dfe85e88de686a8f7d337dff8830161650` | 20 | 7 |
| `remote_setup_wpi.sh` | 17775 | `c0b7caa7f856db6b6d8aad4d407d42d450064a9e55a9cbbacf464f28e97b8d74` | 0 | 3 |
| `remote_extract_verify_wpi.sh` | 16614 | `8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412` | 0 | 7 |
| `remote_close_tree_wpi.sh` | 12039 | `fc183751c634c7fd6d1d9bd75143b7229357e52b7eec5f25a8eec0192bd1f75f` | 0 | 0 |
| **seven executable/plan files** | | | **36** | **33** |
| `SELF_QA_TRANSPORT.md` | 100406 | `84730522fd77b4a754d35556b740f6438a0bd0bc68e3d90340cb348b715c27da` | 6 | 10 |
| `STATUS_TRANSPORT.md` | 7445 | `dfdf7fb931905e3f6404c14bb32dd3c93f0323c812dc5ae10c1fb3c9c2be23a7` | 1 | 1 |

`remote_extract_verify_wpi.sh`, `run_p0.sh` and `run_ro.sh` are **byte-identical to the
rejected baseline**: no round-2 finding touched them and none of the round-3 findings
does either.

Accepted sources, re-verified unchanged and unedited:

| file | bytes | SHA-256 |
|---|---:|---|
| `02_PREREG/remote_setup.sh` | 4976 | `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5` |
| `02_PREREG/remote_extract_verify.sh` | 8270 | `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3` |
| `02_PREREG/remote_close_tree.sh` | 7470 | `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e` |

**Syntax.** `bash -n` passes on all five in-scope shell files and on the accepted
`remote_close_tree.sh`. `[Parser]::ParseFile` on `transport_runner.ps1` → **0 errors**
under Windows PowerShell 5.1.26100.8875; no `&&`, `||` or ternary. Zero CR bytes in all
seven executable/plan files; the runner and plan are pure ASCII; the three remote shell
scripts carry 6, 9 and 5 high bytes, all em-dashes on comment lines, matching the
accepted originals' style.

---

## 5. Disclosed, not repaired

Each is stated so the re-audit adjudicates it rather than discovering it.

1. **Remote tool bytes are not bound.** The pins bind a locator and metadata, not
   bytes. Runtime digests are recorded as evidence only. Binding them needs a
   deploy-channel attestation and is a successor item.
2. **`mktemp` in the close script still honours the login `TMPDIR`.** The work
   directory's location is inherited; it is outside `EV_DIR` by construction. Removing
   it would be a class 3 change.
3. **The close script's owner comparison is still name-rendered** (`%U:%G` against
   `gatea:gatea`), inherited from the accepted original. Making it numeric is class 3.
4. **A placeholder guard must not contain the placeholder.** A guard comparing against
   the literal `<PIN-AT-FREEZE>` is destroyed by a Stage-1 fill that replaces that text
   globally — it would then hold the real value and STOP on a correctly frozen file.
   The new setup guard therefore composes its marker. The runner's pre-existing
   `$UNFILLED_MARKERS` array has the same shape, was accepted in round 2, and is left
   unchanged; the Stage-1 fill procedure must fill constants individually.
5. **Claude round-2 nits N-c, N-d, N-e are not repaired.** N-b is repaired as part of
   F2 (`-F none` plus the pinned `UserKnownHostsFile` closes the `ProxyCommand`
   channel it named). N-a is repaired as N1. N-c (`run_capture` labelling two
   conditions alike), N-d (`bind_component` STOPping where line 23's contract says
   FAIL) and N-e (`tar`/`find` without `</dev/null`) are optional and were left, so
   this round's diff stays inside the four findings.
6. **The `always`-cleanup rule is deliberately broad.** Any `always` op that mismatches
   while the sequence is already broken is not-evaluable, even if in principle it could
   have observed real deviant state. That is the safe direction — a cleanup's failure
   after an earlier break is not independent evidence about the host — but it is a
   design choice, not a derivation, and the Lead should ratify it.

---

## 6. Round-2 findings: no regression

All 16 round-1 findings and the 12 round-2 closures stand. The three files that carry
most of them — `remote_extract_verify_wpi.sh`, `run_p0.sh`, `run_ro.sh` — are
byte-identical to the rejected baseline. In `transport_runner.ps1` the `$Matches`
latching, the program-identity block, the stdin-root grammar, the plan grammar, the
marker gate and the top-level trap are untouched; arm **L1** re-drives the marker gate
on the delivered file (`TR_STOP reason=unfilled_marker field=BASE_RUN`, rc 3) and every
J/K arm exercises the plan reader, the program pins and the record root end to end. In
`remote_setup_wpi.sh` the parent-chain binding, numeric identity, absence calibration
and allocate/assert interleave are unchanged and are exercised by the F4 CTL arm, which
allocates all four directories normally.

---

## 7. Required next action

Return the delivered bytes to two fresh T0 flagship slots. This report grants no host,
freeze, allocation, execution, or Git authority, and nothing was committed.
