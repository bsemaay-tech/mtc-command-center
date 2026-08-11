# WP-I transport round 4 — repair report (2026-08-11)

Implementer: Claude Opus 5 xhigh, Max account, under `KICKOFF_TRANSPORT_REPAIR_R4.md`
and the Lead's `KICKOFF_TRANSPORT_R4_MAX_ADDENDUM.md`. Codex remains the auditor of
record for F1–F4; this session implemented and did not audit its own work.

This file also serves as the kickoff's `TRANSPORT_REPAIR_R4_REPORT.md` deliverable; the
addendum renamed it, and only one report exists.

## 0. Scope, method, and what was not done

- Working directory `C:\LAB\Tradingview_LAB_CLEAN`. **No commit** — the Lead commits.
- **No host contact and no network connection.** The Linux fixtures ran against a local
  WSL2 Ubuntu kernel (`6.18.33.2-microsoft-standard-WSL2`); every path they touched is
  under `/root/wpi_r4*` on that local filesystem. The operator-side fixtures started no
  process at all. Unlike round 3, this round did not need to execute `ssh.exe`/`scp.exe`
  even for configuration evaluation: nothing in F1–F4 or T5–T8 turns on the local
  client's configuration, which round 3 already closed and round 4 did not touch.
- Per addendum item 1, the concurrent session's edit at `cf049b6b` is **superseded**.
  All nine files were re-derived starting from the round-3 bytes at `78173bfd`; §3 below
  states, piece by piece, what was kept and what was dropped, and every kept piece is
  shown reachable from a plan-passed invocation.
- Per addendum item 2, the ordered resumption list in
  `TRANSPORT_STATE_ASSESSMENT_2026-08-11.md` was followed: contract first, then the close
  script, then the plan and launch domain, then the runner, then the wrappers, then the
  preregistration, and the evidence layer last.
- All shell files are LF-only (`tr -cd '\r' | wc -c` = 0, counted as bytes, per file).
  `transport_runner.ps1` parses under Windows PowerShell 5.1.26100.8875 with
  `PARSE_ERRORS=0`.
- Evidence lives in `SELF_QA_TRANSPORT.md` §R4 and is produced by three committed
  harnesses (`_r4_runner_probe.ps1`, `_r4_wsl_fixtures.sh`, `_r4_t5_compose.sh`). There
  is **no `PENDING-LEAD-EXECUTION` item in this round**: every fix has a RED and a GREEN
  this session executed.

### Why the evidence is stronger than a hand-written harness

The operator-side RED/GREEN does not re-implement the runner. `_r4_runner_probe.ps1`
**extracts named regions of a `transport_runner.ps1` file verbatim** — the outcome
grammar, the marker-family map, the prerequisite map, the provenance test, the
prerequisite resolver, the classifier, the per-op classification/counter block and the
run rollup — and `Invoke-Expression`s those exact bytes against injected per-operation
`(rc, capture)` pairs. It prints the line range and SHA-256 of every region it lifts and
brace-balance-checks each slice before executing it. RED is produced by pointing the
same harness at the **round-3 blob from commit `78173bfd`**, so the vulnerable behaviour
is demonstrated by the accepted bytes rather than described.

## 1. Finding → disposition → evidence

### F1 (CRITICAL) — remote interpreter outside the pinned domain; unrelated marker family accepted → **REPAIRED, with one residual disclosed**

Two independent defects were reported under F1 and both are addressed.

**(a) The launch domain.** Rounds 1–3 sent all six stdin scripts to bare `bash -s --`.
Reproduced here against the delivered bytes: with a fake `bash` first on `PATH` the
plant ran, ignored the delivered script and printed a forged
`CLOSE PASS … wrote_into_evidence_tree=0` at rc 0 (`PATH_RC=0 PATH_HIT=yes`); under an
absolute interpreter an inherited `BASH_ENV` did the same (`BASH_ENV_RC=0`,
`BASH_ENV_HIT=yes`).

Repair, stated on **both** sides so neither alone is load-bearing:

- `TRANSPORT_PLAN.tsv` — all six `ssh_stdin` rows carry, verbatim after the route and
  before the script's own arguments:
  `/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea /usr/bin/bash
  --noprofile --norc -s --`.
- `transport_runner.ps1` — that argv is the frozen `$REMOTE_LAUNCH_DOMAIN`, and
  `$SSH_TARGET` is frozen beside it. Plan parsing requires both element-for-element at
  their exact positions; a row that reverts to bare `bash` STOPs the run before
  execution. The record carries `TR_REMOTE_LAUNCH_DOMAIN`.
- All five delivered shell scripts — a class 5 preamble that runs **before the first
  external program**, using shell builtins and one `/proc/self/environ` read: the
  interpreter must be the pinned `/usr/bin/bash`; no startup files may have been read
  (`shopt -q login_shell`); no shell function may have been inherited; and the exec
  environment must be **exactly** the three constructed entries, each matched as a whole
  `name=value` string and seen exactly once. `BASH_ENV`, `ENV`, `LD_PRELOAD`, a
  `BASH_FUNC_x%%` entry and an inherited `TMPDIR` are therefore each refused **by name**.
  Every arm is rc 3. `/usr/bin/env` and `/usr/bin/bash` also joined each script's pinned
  tool set, so the interpreter is inside the program domain rather than beside it.

GREEN: with the PATH plant still first on the outer `PATH` and `BASH_ENV` still set, the
frozen argv produced the real record at rc 0 and neither plant ran
(`PATH_HIT=no STARTUP_HIT=no`). An exported shell function forced into the launch
environment gives `CLOSE_STOP reason=launch_domain_inherited_shell_function` rc 3.

Why the sweep reads `/proc/self/environ` rather than `compgen -e`: the kernel's copy is
what `execve` received, so the names bash adds for its own children (`PWD`, `SHLVL`,
`_`) cannot mask an entry the launch domain actually delivered, and the expected set is
an exact three rather than an allowlist with unavoidable exceptions.

**Residual, measured and disclosed rather than papered over.** `bash` reads `$BASH_ENV`
before the first byte of a stdin-delivered script, and `--norc`/`--noprofile` do not
disable that channel. A startup plant that **exits** therefore forges the record before
any in-script attestation can run — executed and recorded in self-QA as `F1 RESIDUAL`.
No in-script check can close this. It is closed by the operator side: the runner refuses
any plan row that does not carry the `env -i` domain verbatim, and that domain supplies
an explicit, complete variable list, so no plan row can introduce `BASH_ENV` at all. The
case is unreachable from the frozen plan; it is recorded because the claim must be
scoped honestly, and it is precisely why the domain is enforced on both sides. The
stealthier plant — one that lets the script run, and so is the only kind that could
forge a *real-looking* record — is refused by the sweep at rc 3, also executed.

**(b) The marker family.** Round 3 tested one global union of all five programs'
prefixes, so a close operation accepted `SETUP PASS` from an unrelated program as its
own provenance. `$MARKER_FAMILY_BY_STDIN` now binds each family to the stdin artifact
the row sends, `Test-RemoteProvenanceMarkerForOp` takes the operation, and an
`ssh_stdin` row whose stdin leaf has no registered family is a plan STOP.

RED (round-3 bytes, probe fixture D): op 07 `class=match reason=preregistered_rc`, run
`TR_RUN PASS`. GREEN (round-4 bytes, same fixture):
`class=not_evaluable reason=no_remote_program_marker_in_capture
expected_family=remote_close_tree_wpi.sh`, run `TR_RUN STOP` rc 3.

### F2 (HIGH) — inherited `TMPDIR` writes inside evidence while claiming read-only → **REPAIRED**

RED reproduces Codex's finding exactly. With `TMPDIR=$EV_DIR`, the round-3 close script
returned rc 0 and emitted, among its digests,
`CLOSE_DIGEST 8674b413…  tmp.SBgcK4chKj/raw.0` followed by
`CLOSE PASS … files=3 wrote_into_evidence_tree=0`: it created and hashed its own file
inside the tree it was measuring while reporting that it had not.

Repair (derivation class 6): `mktemp` is gone. `remote_setup_wpi.sh` allocates a fifth
directory, `<REMOTE_BASE>/work`, under the same create-once, bind-immediately discipline
as the other four and proves it disjoint from the evidence parent at allocation time.
The plan passes it to ops 07/08 as a third argument. The close script binds it as a
launch input (non-symlink, canonical, numeric owner, mode 700 — every refusal rc 3),
proves canonical two-way non-overlap with `EV_DIR` **before** `mkdir`, creates
`close_work_<RUNID>` with `mkdir -m 0700` and no `-p`, proves non-overlap again on the
object `mkdir` actually produced, points `TMPDIR` at it, and removes it on every exit
path with the removal's **own status adjudicated** — a work directory that could not be
removed is now `CLOSE_STOP reason=work_dir_removal_failed`, where the superseded edit
had `|| :`. The close script deliberately does **not** allocate its own scratch root: a
program that allocates the root it is about to trust proves nothing about where that
root is.

GREEN: the same `TMPDIR` injection now gives
`CLOSE_STOP reason=launch_domain_unexpected_environment_entry name=[TMPDIR]` rc 3. The
clean run under the frozen argv returns rc 0 and leaves the evidence tree containing
exactly its two original files and the work root empty. A `WORK_ROOT` pointed inside the
evidence tree is refused **before `mkdir`** with `work_dir_inside_evidence_tree
phase=before_create`, and a `find` over the tree afterwards shows nothing was created.

Claude's observation 1 (the worst case ends FAIL, not a false attestation) is consistent
with this repair and is now moot: the channel no longer exists.

### F3 (HIGH) — a mixed close probe error classified as absence → **REPAIRED**

RED: a `stat` wrapper answering the evidence-directory probe with
`No such file or directory; Permission denied` drove the round-3 script to
`CLOSE_FAIL reason=evidence_dir_absent` at rc 1 — a completed observation of missing
evidence manufactured out of an inability to evaluate.

Repair (derivation class 3, the same shape `remote_setup_wpi.sh` already used): the
absence sentence this run's own pinned `stat` emits is calibrated once, under the
already-bound work root, and turned into a template with the path replaced by `@PATH@`.
A probe is `absent` only when three independent statements agree — `stat` failed, the
kernel reports neither object nor link, and the diagnostic equals the rendered template
as a **whole string**. Multiline, mixed, wrapped or unrecognised diagnostics STOP.

GREEN: the same fixture returns rc 3,
`CLOSE_STOP reason=path_probe_error path=… rc=1 detail=…: No such file or directory;
Permission denied`. The arm reached is the kernel-corroboration arm rather than the
template arm, because in that fixture the directory does exist — which is the stronger
of the two refusals and is what the transcript records.

### F4 (HIGH) — the broad `always` rule hides an independent cleanup deviation → **REPAIRED per the Lead's adjudication (Codex prevails)**

The global `$sequenceOk` snapshot is removed. `$ALWAYS_PREREQUISITES` freezes the
dependency graph — 07←04, 08←05, 09←07, 10←08, 11←07+09, 12←08+10 — and the runner binds
it to the plan **before execution**: every `always` row must have an entry, every entry
must name a real, earlier op, and no entry may exist for an unknown or non-`always` op,
or the run STOPs. `Resolve-AlwaysPrerequisite` answers two separate questions from
`$classById`, the recorded class of each named operation: was every edge a match, and if
not, did any edge observe deviant state.

Codex's decisive fixture goes GREEN. Ops 01–06 all match; op 07 returns a genuine marked
`CLOSE_STOP` rc 3; the independent op 08 returns a genuine marked `CLOSE_FAIL` rc 1:

| | round-3 bytes (RED) | round-4 bytes (GREEN) |
|---|---|---|
| op 08 class | `not_evaluable reason=cleanup_after_unestablished_prerequisite` | `deviant reason=operation_ran_and_observed_deviant_state` |
| run class | `deviant=0 not_evaluable=4` | `deviant=1 not_evaluable=3` |
| verdict | `TR_RUN STOP` rc 3 — the RO deviation erased | `TR_RUN FAIL` rc 1 — the RO deviation counted |

Claude's scenario still holds (fixture B): with the P0 stage STOPping, op 07's rc 1 stays
`not_evaluable`, and the run is `TR_RUN STOP` in both round 3 and round 4.

Claude's nit N-h is subsumed (fixture C): where the RO **stage** ran and observed deviant
state, op 08's own failure now reports
`cleanup_after_earlier_deviation prerequisites=[05=deviant]` instead of the round-3
`cleanup_after_unestablished_prerequisite`, and the untouched P0 branch still passes at
op 07. Every executed `always` op also emits `TR_OP_PREREQ_STATE` naming the resolved
class of each edge, so the classification is auditable from the record rather than from
the code.

### T5 (CRITICAL) — `run_p0.sh` wires none of the `P0_ATTESTED_*` inputs → **REPAIRED, composition executed**

`run_p0.sh` now defines five freeze pins — `P0_ATTESTED_USER_NS`, `_MNT_NS`, `_PID_NS`,
`_NET_NS`, `_ROOT_MOUNT_ID` — and exports them with the other RP6 inputs, plus a
`P0W_attested_inputs` record line naming their deploy-channel origin.

Proved by executing the launch path with the connection stubbed, in two halves:

- **A.** The real wrapper was launched under the frozen launch domain with `EXTRACT_DIR`
  pointed at probe stubs, and the `P0_*` environment was captured **from the block
  position itself**. Round-3 wrapper: `P0_ATTESTED_names_exported=0`. Round-4 wrapper:
  `P0_ATTESTED_names_exported=5`, with the values visible in the transcript.
- **B.** The **real `RP6-P0.sh` row-8 gate bytes** (lines 683–744 plus the five frozen
  `P0_FIXED_ATTESTED_*` literals, extracted verbatim; block SHA-256 and extract SHA-256
  both printed) were then driven with exactly those environments:

| environment | block literals | result |
|---|---|---|
| round-3 wrapper | unfilled | `P0_STOP … detail=preregistered_value_missing` rc 3 |
| round-4 wrapper | unfilled | `P0_STOP … detail=freeze_pin_unfilled` rc 3 |
| round-4 wrapper | filled to match | `P0_GATE_PASSED all_five_attested_inputs_accepted` rc 0 |
| round-3 wrapper | filled | `P0_STOP … detail=preregistered_value_missing` rc 3 |
| round-4 wrapper, one value changed | filled | `P0_STOP … detail=prelude_value_differs_from_frozen_pin` rc 3 |

The middle row is the honest draft-stage state: with the wrapper wired, the composition
now reaches the **freeze-pin** arm instead of the **missing-input** arm, and the block
side is a Stage-1 fill rather than a wrapper defect. Filling both sides passes the gate;
filling one side does not. `RP6-P0.sh` was not modified — the filled-literals case runs
against a copy of the extracted gate.

### T6 — the close contract, the bytes and the plan disagreed → **REPAIRED (implemented, not withdrawn)**

Of the two branches the kickoff offered, this round took the first: classes 5 and 6 are
implemented and the plan passes the run-owned work root. All three surfaces now state
the same three-argument contract
(`remote_close_tree_wpi.sh <EV_DIR> <RUNID> <WORK_ROOT>`): the script's header and code,
`TRANSPORT_PLAN.tsv` rows 07/08 (`argc=45`, tail
`/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/work`), and draft §4/§5/§7.

The composition is executed end to end: op 01 allocates five directories including
`<BASE>/work`, and the close script then closes a tree under that base using exactly the
plan's argv shape at rc 0, reporting
`work_root_ok … allocator=op_01_remote_setup_wpi.sh`.

Also repaired here, and load-bearing for the runner's semantics: **argv errors are no
longer host findings**. The round-3 and superseded scripts called `fail()` for a wrong
argument count, so an operator-side composition error would have arrived at the runner as
a deviant *host* observation at rc 1 — exactly the manufactured-FAIL class this round
exists to remove. Executed: superseded bytes with two arguments →
`CLOSE_FAIL reason=usage … argc=2` rc 1; round-4 bytes with two arguments →
`CLOSE_STOP reason=argv_count=2 expected=3 …` rc 3. The RUNID grammar and the
`EV_DIR`/`RUNID` basename agreement moved to STOP for the same reason. The state of the
evidence tree itself — absent, symlink, wrong numeric owner or mode, non-regular
entries, empty, not quiescent — remains a completed observation at rc 1.

### T7 — the inert `WPI_INTERPRETER_TARGET` pin → **REMOVED**

`run_ro.sh` no longer defines or exports it; what remains at `run_ro.sh:124` is a comment
recording the removal and the condition for reintroducing it. Executed checks: 0
assignments, 0 exports, `RP7-WPI-RO.sh` references it 0 times, and the accepted
predicate that does exist is `wpi_assert_interpreter()` at `RP7-WPI-RO.sh:979`, which
derives `<WPI_VENV_ROOT>/bin/python` itself and refuses a symlinked object. **RP7 was not
touched** — another session owns it. Draft §2 now records the pin as deliberately absent;
the successor draft R3 §2.3 already carried the no-inert-pins clause.

### T8 — the preregistered transport summary was stale → **REPAIRED (documentation)**

Stated once, in draft §6, and aligned everywhere it is mirrored. It now says:
first-*mismatch* sequencing (not first-FAIL); after the first mismatching or
not-evaluable `sequence_ok` operation later `sequence_ok` operations are skipped while
all `always` operations still run; classification is by operation kind and provenance,
never by rc alone; `ssh` rc 255, any nonzero `scp` rc, an rc outside a kind's grammar and
an `ssh` rc without a marker **from that operation's own family** are all not-evaluable;
and an `always` failure caused by an earlier break **on its own branch** is
not-evaluable rather than a new host FAIL, naming which of the two cases it is. The
successor draft R3's §6 sentence (and its mirrored quote) were extended to match.

This item has **no executable predicate**, and none is claimed. Its evidence is the diff.

## 2. Draft edits

`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`:

| § | edit |
|---|---|
| §2 | added the five `P0_ATTESTED_*` rows with their grammars and deploy-channel origin; added the paragraph stating that `run_p0.sh` wires them, that the block requires both sides to agree, and that `WPI_INTERPRETER_TARGET` is deliberately absent (T5, T7) |
| §4 class 2 | withdrew the round-3 sentence that let the close script keep `mktemp` with the inherited-`TMPDIR` residual "disclosed"; replaced with the executed finding and a pointer to class 6 (F2) |
| §4 | added derivation **class 5** (launch-domain attestation, with its measured scope limit) and **class 6** (run-owned scratch), so the "exactly six classes" sentence now re-derives from six enumerated items (F1, F2) |
| §5 | added the frozen **remote launch domain** block with the two falsifications that motivate it; rewrote the op table's argv column for rows 01/03/04/05/07/08; recorded op 01 as allocating five directories and ops 07/08 as taking the work root (F1, F2, T6) |
| §5 | rewrote the `ssh_stdin` row of the observed-outcome grammar table for per-operation marker families (F1) |
| §5 | replaced the global cross-kind cleanup rule with the per-branch prerequisite table, the decisive-case statement, and the two distinct reason tokens (F4) |
| §6 | added the single, correct transport-semantics paragraph and the new record lines (T8) |
| §7 | close script now stated as classes 2/3/5/6, three arguments, op-01-allocated work root, and the argv-error-is-rc-3 rule (T6) |

`WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`: the §6 transport
summary sentence and its mirrored quote (2 occurrences) extended with per-branch
prerequisites, the two reason tokens, and per-operation marker families.

No other file in either draft directory was edited.

## 3. The superseded `cf049b6b` edit, piece by piece

The addendum superseded it; round 4 started from `78173bfd`. Every piece below was
re-derived from scratch against the round-3 bytes, and each kept piece is now reachable
from a plan-passed invocation.

| Piece of the superseded edit | Disposition | Why |
|---|---|---|
| Class 5 launch-domain attestation (concept) | **KEPT, re-derived** | Correct answer to F1. Now reachable: see the two defects below. |
| `LD_FUNCS="$(declare -F)"` placed **after** `ld_stop` is defined | **DROPPED** | Its own function is in the list, so a clean launch self-STOPs. Executed: `CLOSE_STOP reason=launch_domain_inherited_shell_function` rc 3 under the exact launch its header prescribes. The sweep now runs **before** this script defines any function. |
| `LD_FUNCS="$(declare -F)"` with no status guard | **DROPPED** — second, independent defect found while re-deriving | `declare -F` exits **1** when no function exists, so under `set -Eeuo pipefail` the assignment would have terminated the script at rc 1 **with no marker at all** the moment the first defect was fixed. The round-4 line is `LD_FUNCS="$(declare -F 2>/dev/null \|\| :)"` and tests emptiness afterwards. This one was never observable while the first defect masked it. |
| `compgen -e` environment sweep | **DROPPED, replaced** | It lists what the shell exports, so `PWD`/`SHLVL`/`_` must be allowlisted and a launch-domain entry could hide behind that allowance; and `for X in $(compgen -e)` word-splits. Replaced by an exact whole-string sweep of `/proc/self/environ`, which is what `execve` received: expected size 3, each entry matched once. |
| `[ "${BASH_ENV+set}" != 'set' ]` etc. as separate arms | **KEPT in effect, folded in** | The environ sweep refuses them by name and names the offender, so the separate arms are redundant. |
| Pinning `/usr/bin/env` and `/usr/bin/bash` into the tool set | **KEPT** | Puts the interpreter inside the pinned program domain rather than beside it. Extended to all five delivered scripts, not only the close script. |
| Class 3 exact ENOENT template + kernel corroboration | **KEPT, re-derived** | Correct answer to F3; now reachable, and independently falsified with the mixed diagnostic. |
| Numeric `EXPECT_UID`/`EXPECT_GID` with the rendered pair kept diagnostic | **KEPT** | Closes Claude nit N-d on the close script. Adds two freeze pins. |
| `WORK_ROOT` third argument, canonical two-way non-overlap, create-once 0700, `TMPDIR` export | **KEPT, re-derived** | Correct answer to F2. Now composed: op 01 allocates the root and the plan passes it, which the superseded edit did not do. |
| `[ "$#" -eq 3 ] \|\| fail "usage …"` | **DROPPED** | An operator-side composition error returned rc 1, which the runner would have counted as a deviant host observation. Now `stop` at rc 3, with the RUNID-grammar and basename-agreement arms moved for the same reason. |
| `trap '… "$TOOL_RM" -rf -- "$WORK" \|\| :' EXIT` | **DROPPED, replaced** | `\|\| :` discards the only evidence that the removal failed. The round-4 trap adjudicates rc, diagnostics and the object's continued existence, and STOPs at rc 3 if the work directory survived. It prints nothing on success, because §7's record grammar admits `CLOSE_NOTE` only before `CLOSE_BINDING`. |
| Header prose describing classes 5 and 6 | **KEPT, rewritten** | Rewritten to match the bytes that now exist, plus the measured `BASH_ENV` scope limit. |

No other file was modified by that commit, and no other piece of it exists.

## 4. Delivered identities

| Target | Bytes | SHA-256 | `<ALLOCATE-AT-DISPATCH>` | `<PIN-AT-FREEZE>` | CR bytes |
|---|---:|---|---:|---:|---:|
| `run_p0.sh` | 12,063 | `6646770f6884dc3e918e87c65f4c097af25b71e2612f67165662825d58709202` | 6 | 8 | 0 |
| `run_ro.sh` | 11,925 | `9ab8fa715f553f743bd23c2d177842d5c32c0c2bf074c9564861f0506f55cf12` | 6 | 4 | 0 |
| `transport_runner.ps1` | 69,932 | `45123de489ec48dfe7d4318dad7db547bcc03114fe886be16c7f4c616fc45fed` | 3 | 7 | 0 |
| `TRANSPORT_PLAN.tsv` | 7,970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` | 22 | 7 | 0 |
| `remote_setup_wpi.sh` | 24,938 | `2176448e710511ca0a7fa0b01c0c630012f0281691b36bf2b8c7bfe49531d8f4` | 0 | 3 | 0 |
| `remote_extract_verify_wpi.sh` | 22,047 | `fa57065b85b45fb652d7ef31f4fbc6a13970b7fed763d309daedb8df18323e41` | 0 | 7 | 0 |
| `remote_close_tree_wpi.sh` | 28,756 | `29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef` | 0 | 2 | 0 |
| `SELF_QA_TRANSPORT.md` | 148,396 | `492c0b60fb254e728705c9712f9111da03a0062b6e58438480397ca864c3e703` | — | — | 0 |
| `STATUS_TRANSPORT.md` | 12,470 | `7a6053e45e5fd6689cab91fcf64cb04dbbc395672faec97aa1c70124aa1b4a39` | — | — | 0 |

Census over the seven executable/plan targets: **37** allocation markers and **38** pin
markers, against 36 / 33 in round 3. The delta re-derives exactly:

| change | allocation | pin |
|---|---:|---:|
| work root in plan rows 07/08 | +2 | 0 |
| `P0_ATTESTED_*` in `run_p0.sh` | 0 | +5 |
| numeric `EXPECT_UID`/`EXPECT_GID` in the close script | 0 | +2 |
| `WPI_INTERPRETER_TARGET` removed from `run_ro.sh` | 0 | −1 |
| runner's `$UNFILLED_MARKERS` guard composed rather than literal (nit N-g) | −1 | −1 |
| **total** | **+1 → 37** | **+5 → 38** |

Three harnesses ship beside the targets and are not part of the frozen set:
`_r4_runner_probe.ps1`, `_r4_wsl_fixtures.sh`, `_r4_t5_compose.sh`. The two files
`_r4_logic.py` and `_r4_selfqa_harness.ps1`, left by the interrupted 2026-08-10 round-4
attempt, are **not** used by this round's evidence and no claim rests on them.

## 5. Nits from the round-3 audits

| Nit | Disposition |
|---|---|
| Codex 1 — §4 script-count ambiguity | Already corrected before this round; §4 reads "five delivered derived shell files … derived from four accepted bases" and the close script is the "third `_wpi` derived script". Verified, not re-edited. |
| Codex 2 / Claude N-g — compose `$UNFILLED_MARKERS` | **APPLIED.** The guard is now composed (`('<ALLOCATE-' + 'AT-DISPATCH>')`, `('<PIN-' + 'AT-FREEZE>')`), the same discipline `remote_setup_wpi.sh` already used. This removes the trap where a file-wide Stage-1 replacement would rewrite the guard into the real values and STOP a correctly frozen runner, and it keeps the placeholder census honest: the literals left in the runner are all consumers. |
| Claude N-a — §4 "Four scripts are reused" | Already corrected; the string no longer occurs. Verified. |
| Claude N-b — "four derived scripts" count | Already corrected in the draft; the stale copy at `STATUS_TRANSPORT.md:22` is gone in this round's rewrite. |
| Claude N-c — self-QA §9 cross-reference off by two | **APPLIED.** Now points at `TRANSPORT_REPAIR_R3_REPORT.md` §4 (`Delivered identities`). |
| Claude N-d — close script compared the rendered owner name | **APPLIED** as part of class 3: numeric `%u:%g` against `EXPECT_UID`/`EXPECT_GID`, rendered `%U:%G` kept diagnostic only, on the evidence directory, the work root and the work directory. |
| Claude N-e — `TR_ENV_POLICY` asserted, not derived | **APPLIED.** `ambient_ssh_config` is derived from `$SSH_PINNED_OPTIONS[0..1]` and the line records `derived_from=SSH_PINNED_OPTIONS[0..1]`. |
| Claude N-f — the `ACCEPTED` stdin root is registered but unused | **APPLIED** as documentation: the runner's `$STDIN_ROOTS` comment now states that `ACCEPTED` is not live, why it is retained, and that a row naming it would still have to satisfy the stdin digest pin. |
| Claude N-h — distinguish the two `always`-cleanup reasons | **APPLIED**, subsumed by F4; executed in probe fixture C. |

## 6. Freeze-gate inputs

Unchanged from round 3 except where noted. Each is fail-closed at rc 3 until supplied.

| input | consumer | note |
|---|---|---|
| `EXPECT_PARENT_MOUNT` | `remote_setup_wpi.sh` | owner grant #6, ordered **before op 01** |
| `EXPECT_UID` / `EXPECT_GID` | `remote_setup_wpi.sh`, `remote_close_tree_wpi.sh` | **the close script's pair is new this round** (nit N-d) |
| `P0_ATTESTED_USER_NS` / `_MNT_NS` / `_PID_NS` / `_NET_NS` / `_ROOT_MOUNT_ID` | `run_p0.sh` → `RP6-P0.sh` row 8 | **new this round** (T5). `RP6-P0.sh`'s `P0_FIXED_ATTESTED_*` literals must be filled to the same five values or the gate STOPs — proved in self-QA |
| `wpi_known_hosts`, `wpi_known_hosts_global`, `gatea_ed25519` + SHA-256 | `transport_runner.ps1` | unchanged |
| SHA-256 + bytes of all five delivered shell files, `runkit.tar`, `TRANSPORT_PLAN.tsv` | plan/runner pins | all five identities changed this round |
| `WPI_INTERPRETER_TARGET` | — | **withdrawn** (T7) |

## 7. Disclosed, not repaired

1. **`BASH_ENV` startup plant that exits** — measured, executed, and closed on the
   operator side only; see F1 above. Unreachable from the frozen plan.
2. **The remote login shell** `sshd` uses to run the command string is outside every
   attestation here. `env -i` clears what it exports and both launch programs are
   absolute, so it cannot select or influence what runs, but its own integrity is a
   deploy-channel property.
3. **Remote tool bytes are still not bound.** The pins bind a locator and that object's
   metadata; runtime digests are emitted as evidence and explicitly not compared. This
   now covers `/usr/bin/env` and `/usr/bin/bash` too, and each script says so in its own
   `tool_digest_limit` line.
4. **The mount binding remains a point-in-time statement about the allocation parent**
   (Claude observation 2). The five created directories are not themselves mount-bound.
5. **Deviation D-3 grew.** The pin set now includes `/usr/bin/env` and `/usr/bin/bash`,
   so `GATEA-STAGING` must carry those as regular, root-owned, not-group/other-writable
   files as well, or ops 01, 03, 04, 05, 07 and 08 STOP at dispatch. On the QA kernel
   most `/usr/bin` coreutils names are symlinks and the scripts refuse them — the safe
   direction, but not the target host's state.
6. **The wrappers now run under `env -i`.** Neither block has been executed end to end
   under that domain, which cannot be done without the host. If a block needs an
   environment name the domain does not deliver, it will STOP at rc 3 — fail-closed —
   and the fix is the domain or the wrapper's export set, not the classifier.

## 8. What I did not verify

- Any real connection behaviour against `GATEA-STAGING`. No socket was opened.
- The remote scripts' behaviour on the real host, including whether `/proc/self/environ`
  and the `/usr/bin` pin set have the shapes this round assumes there. The fixtures
  establish the logic on a Linux kernel, not on that host.
- `RP6-P0.sh` and `RP7-WPI-RO.sh` as wholes. Only `RP6-P0.sh`'s row-8 gate region was
  executed, and only as an extract; neither block was modified.
- The six-member happy path against the real WP-I `runkit.tar`, which does not exist yet.

## 9. Required next action

Codex re-audit under T0 policy, against the identities in §4. The three questions this
round most needs adversarial attention on are: (a) whether the class 5 sweep is complete
— is there a launch-domain channel it does not name; (b) whether the per-branch
prerequisite graph is the right graph, including whether op 11/12's dependency on both
its close and its fetch is correct; and (c) whether moving the close script's argv arms
from rc 1 to rc 3 removed a genuine host observation anywhere.

Two items need the Lead rather than the auditor: ratifying derivation classes 5 and 6 as
permitted deltas, and accepting the F1 residual's scoping — that a `BASH_ENV` startup
plant is closed by the plan/runner side and cannot be closed inside a delivered script.

This report grants no host, freeze, allocation, execution, dispatch, or Git authority.
