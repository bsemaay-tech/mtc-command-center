# WP-I transport round 5 — repair report (2026-08-11)

Implementer: Claude Opus 5 xhigh, Max account, under `KICKOFF_TRANSPORT_REPAIR_R5.md`.
Codex remains the auditor of record; this session implemented and did not audit its own
work. Inputs: `TRANSPORT_CODEX_R4_AUDIT_BAND_A_2026-08-11.md` (BA-1, BA-2, BA-3) and
`TRANSPORT_CODEX_R4_AUDIT_BAND_B_2026-08-11.md` (F1), both **REQUEST_CHANGES**, read in
full; their text binds.

## 0. Scope, method, and what was not done

- Working directory `C:\LAB\Tradingview_LAB_CLEAN`. **No commit** — the Lead commits.
- **No host contact and no network connection.** No socket of any kind was created and
  no `ssh.exe`, `scp.exe` or `sshd` process was started. The Linux fixtures ran against
  the same local WSL2 Ubuntu kernel round 4 used (`6.18.33.2-microsoft-standard-WSL2`,
  GNU Bash 5.3.9); every path they touch is under `/root/wpi_r5`.
- No `git checkout`, `reset`, `stash`, `restore` or `clean` was run on any tracked file.
  The only Git command used was `git cat-file blob HEAD:…` to read the pre-repair close
  script for the D026 RED arm, and `git status`.
- **Input bytes confirmed.** The kickoff names commit `12d7bb6e` and frozen close-script
  SHA-256 `29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef`. Before any
  edit, all nine working-tree files hashed **identical** to the round-4 report §4 table,
  and the close script hashed to that exact frozen value. The blob extracted for the RED
  arm hashes to the same value, printed in the transcript. `HEAD` advanced during this
  session because other sessions committed their own work; the close-script **blob** is
  the same object at both points — `git rev-parse HEAD:…/remote_close_tree_wpi.sh` and
  `git rev-parse 12d7bb6e:…/remote_close_tree_wpi.sh` both return
  `61696132a5f2fce97aad4054d41a780297ff21a1` — so the RED arm ran on the kickoff's
  declared input bytes.
- All shell files remain LF-only (0 CR bytes, counted as bytes, per file).
  `transport_runner.ps1` parses under Windows PowerShell 5.1.26100.8875 with
  `PARSE_ERRORS=0` and remains 5.1-compatible (no new language constructs — the only
  runner change is comment text).
- Evidence is in `SELF_QA_TRANSPORT.md` §R5, produced by one committed harness,
  `_r5_wsl_fixtures.sh`, which ships beside the targets.
- **One deliverable is not applied and is reported as such**, not quietly dropped: three
  BA-3 draft sentences and the F1 draft mirror live under `WPI_PREREG_DRAFT_ROUND1/`,
  which this session was instructed at dispatch not to touch because a parallel Max
  session owns it. Exact old → new text for all four edits, with anchors verified
  byte-exact and unique against the current draft bytes, is in
  `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`. See §BA-3 and §5.

## 1. Finding → disposition → evidence

### F1 (Band B, CRITICAL) — "closed on the composition" is an overclaim → **OPEN, wording corrected everywhere; no code claim added**

**Disposition: F1 is OPEN — "inner child closed; outer SSH account-shell boundary
open".** Band B's finding is accepted in full. No client-side control was invented, and
no closure is claimed.

Round 4 argued the exiting-`BASH_ENV` case was *unreachable from the frozen plan*: the
runner enforces `$REMOTE_LAUNCH_DOMAIN` verbatim on every plan row, and that domain's
variable list is explicit and complete, so no plan row can introduce `BASH_ENV`. That
argument reasons about the wrong interpreter. The runner does not execute remote
`/usr/bin/env`; it starts local `ssh.exe` and supplies a remote **command string**.
`sshd` hands that string to the account's shell, and that shell processes its own startup
environment **before** the string's first token runs. **No plan row is involved**, so
enforcing the plan row cannot close it — and no command *inside* the same shell string,
on either side, can act before the shell that interprets the string.

**Executed** (`SELF_QA_TRANSPORT.md` §R5-2, block `F1 OPEN - the outer account-shell
boundary, reproduced locally`). The arm states its own scope before its result: it is
**not** closure evidence, it is **not** the real transport path, and no host, socket or
ssh/sshd process is involved. It is a local model of one composition step —
`BASH_ENV=<exiting plant> /usr/bin/bash -c "<the frozen command string>" < <the delivered script>` —
in which the command string is byte-identical to the frozen `$REMOTE_LAUNCH_DOMAIN` and
the delivered script is the **repaired round-5 file**:

```text
RC=0
OUTER_PLANT_RAN=yes
STDOUT:
  CLOSE PASS runid=WPIR5-FIXTURE-P0 dir=... files=2 wrote_into_evidence_tree=0
DELIVERED_SCRIPT_RECORD_LINES=0   (CLOSE_NOTE emitted by the real program)
```

The runner would accept that capture: `$MARKER_FAMILY_BY_STDIN` registers `CLOSE_` and
`CLOSE ` for the `remote_close_tree_wpi.sh` leaf, the forged line starts with one of
them, and rc 0 is in the grammar. Marker **shape** is bound to a plan row, not to the
producing process.

Two controls fix the boundary of the claim rather than leaving it rhetorical:

| control | result |
|---|---|
| **still closed** — a plant that lets the delivered script *run* (the only kind that could forge a *real-looking* record) | `CLOSE_STOP reason=launch_domain_unexpected_environment_entry name=[BASH_ENV]` rc 3, with `QUIET_PLANT_RAN=yes` proving the plant executed |
| **not closed** — the same exiting plant delivered *inside* the domain | forges at rc 0. Round 4 was right that the frozen plan cannot put `BASH_ENV` in the `env -i` list; it was wrong that the plan is the only way in |

**Every claim that the residual is unreachable or that F1 is closed on the composition
has been removed or struck, and the same wording now appears in all eight places:**

| file | what changed |
|---|---|
| `TRANSPORT_R4_REPORT_2026-08-11.md` | new "ROUND-5 CORRECTIONS — READ FIRST" block; §1 F1 heading and residual paragraph struck and corrected; §3 class-5 row narrowed to the inner-child half; §7 items 1 and 2 struck and corrected |
| `SELF_QA_TRANSPORT.md` | §R4-1 F1 verdict cell replaced with **OPEN**; §R4-4 "one residual" paragraph struck with the correction above it; new §R5-2 |
| `STATUS_TRANSPORT.md` | status header now leads with F1 OPEN; round-4 F1 bullet scope-corrected; open items 2 and 3 rewritten, including withdrawal of "cannot select or influence what runs" |
| `transport_runner.ps1` | the `$REMOTE_LAUNCH_DOMAIN` scope paragraph rewritten (comment only) |
| `run_p0.sh`, `run_ro.sh`, `remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh`, `remote_close_tree_wpi.sh` | the identical "MEASURED SCOPE LIMIT" comment block replaced in all five with the F1-OPEN wording; the close script's header scope-limit paragraph also corrected |

The draft mirror is the one place not swept — see §5.

**No enforcement point is claimed.** For a future round: closure requires something that
acts before account-shell startup processing — a deploy-channel-attested forced-command
or execution contract, or a transport path with no unbound shell — plus D026 RED/GREEN
through the real top-level path. A direct local `env -i` invocation is supplemental for
this residual, as Band B states. **A disclosure is not a control.**

### BA-1 (HIGH) — cleanup armed after a post-creation STOP → **REPAIRED, D026 RED/GREEN executed**

`remote_close_tree_wpi.sh:401` created the work directory; `:402` STOPped on any `mkdir`
diagnostic; the trap was not installed until `:424`. Codex reproduced
`SCRIPT_RC=3 … RESIDUE_PRESENT=yes`.

**Repair.** The create now captures rc **and** diagnostics without refusing; the cleanup
function is defined between the capture and the adjudication; on rc 0 the trap is armed
**before** the diagnostic is adjudicated and before every later check. Shape:

```text
MKDIR_RC=0
MKDIR_OUT="$(LC_ALL=C "$TOOL_MKDIR" -m 0700 -- "$WORK" </dev/null 2>&1)" || MKDIR_RC=$?
close_work_cleanup() { … }                    # unchanged body
if [ "$MKDIR_RC" -eq 0 ]; then
    trap 'close_work_cleanup $?' EXIT
else
    MKDIR_OBJ='absent'
    if [ -e "$WORK" ] || [ -L "$WORK" ]; then MKDIR_OBJ='present'; fi
    stop "work_dir_mkdir_failed path=$WORK rc=$MKDIR_RC object_after_failed_create=$MKDIR_OBJ cleanup=not_armed_for_a_nonzero_create detail=[$MKDIR_OUT]"
fi
[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics path=$WORK detail=$MKDIR_OUT"
```

**D026 RED/GREEN** (`SELF_QA_TRANSPORT.md` §R5-1). RED is the **pre-repair blob**
(`git cat-file blob HEAD:…`, SHA-256 `29b6412a466c…`, printed in the transcript), not a
reconstruction. Both arms are driven through the **same** declared instrument — a `mkdir`
that creates the directory, emits one diagnostic and returns 0 — the same launch domain
and the same argv, so the only variable is the delivered bytes:

| | pre-repair (RED) | repaired (GREEN) |
|---|---|---|
| `SCRIPT_RC` | 3 | 3 |
| refusal | `CLOSE_STOP reason=work_dir_mkdir_diagnostics … detail=injected_success_diagnostic` | **byte-identical** |
| `RESIDUE_PRESENT` | **yes** | **no** |

**No carried fence was weakened, and the transcript proves it rather than asserting it.**
The fence is `[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics …"`; predicate and
reason token are unchanged (line 402 → 483). The block `BA-1 FENCE DISCRIMINATING POWER`
quotes the old and the new assertion **and** the refusal each produced **against the same
injected diagnostic** — both refuse. The `work_dir_mkdir_failed` arm gained fields
(`rc=`, `object_after_failed_create=`, `cleanup=`, `detail=`) and lost none.

Five further arms bound the claim:

- clean run, pre-repair bytes: rc 0, `CLOSE PASS`, no residue;
- clean run, repaired bytes: rc 0, same `CLOSE PASS`, no residue — the happy path did
  not move;
- nonzero `mkdir` that created nothing: both arms STOP; the repaired arm additionally
  records `rc=1 object_after_failed_create=absent`;
- **the declared uncovered case** — nonzero `mkdir` that *did* create: the repaired bytes
  deliberately do **not** arm cleanup, residue remains, and the record now **names** it
  (`object_after_failed_create=present`);
- `rm_noop` on the newly covered path: `CLOSE_STOP reason=work_dir_removal_failed` — the
  removal adjudication is live where round 4 never exercised it;
- late refusal after a clean create (work-dir mode 750): both arms `RESIDUE_PRESENT=no`,
  a control that the repair did not move an exit path round 4 already covered.

**Why the nonzero case is not covered, stated rather than hidden.** A nonzero status is
this program's only reason to doubt that the object at `$WORK` is the one it created —
`mkdir` may have created nothing, or may have lost a race for the name. `rm -rf` on an
object the run cannot prove it created is precisely the wrong answer for a script whose
contract is read-only with respect to everything it did not make. Arming cleanup there
would trade a residue for a destructive action, so the claim is narrowed instead.

**Every every-exit-path claim narrowed**, at all four sites Band A named:

| site | now reads |
|---|---|
| `remote_close_tree_wpi.sh:58` (header, class 6) | "removes it on every exit path taken after the create returned 0" + the explicit nonzero carve-out |
| `remote_close_tree_wpi.sh:404-410` (create/cleanup comments) | rewritten; states the BA-1 defect, the fix, and the uncovered case |
| `remote_close_tree_wpi.sh:441` (`CLOSE_NOTE scratch`) | `removal=adjudicated_on_every_exit_path` → `removal=adjudicated_on_every_exit_path_after_a_zero_status_create` (both values visible side by side in the two clean-run transcripts) |
| `TRANSPORT_R4_REPORT_2026-08-11.md:126-130` | struck and corrected in place |
| `WPI_PREREGISTRATION_DRAFT.md:357-360` | **NOT APPLIED** — exact text in `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`, edit 4. See §5 |

### BA-2 (MEDIUM) — the claimed second `declare -F` defect is FALSE → **CLAIM WITHDRAWN; guard kept as no-op hardening**

Executed on GNU Bash 5.3.9 (`SELF_QA_TRANSPORT.md` §R5-3):

| arm | drives | result |
|---|---|---|
| A | bare `declare -F` in a function-free `--noprofile --norc` child | `DIRECT_RC=0` |
| **B** | **the unguarded assignment under `set -Eeuo pipefail` — the claimed RED** | `AFTER_ASSIGN len=0`, `STILL_RUNNING=yes`, `PROCESS_RC=0` |
| C | control: a **named** lookup of a missing function | `PROCESS_RC=1` |
| D | control: `LD_FUNCS="$(false)"` in the identical shell shape | `PROCESS_RC=1` |
| E | the delivered guarded form | `PROCESS_RC=0` |
| F | discriminating power of keeping the guard | `UNGUARDED=[declare -fx foo]` = `GUARDED=[declare -fx foo]` |
| G | the delivered script vs a real inherited exported function | `CLOSE_STOP reason=launch_domain_inherited_shell_function detail=[declare -fx a_plant]` rc 3 |

Arm D is what makes arm B a falsification rather than an inactive-option artefact: `set -e`
**is** armed in that exact shell shape and does kill the process for a genuinely failing
command. The claimed RED is not producible by the command the delivered code runs.

**Disposition: the guard is KEPT as explicit no-op hardening, and the claim is withdrawn.**
Arm F is the discriminating-power evidence for keeping it — guarded and unguarded list an
inherited exported function identically, so retaining it removes no detection — and arm G
shows the sweep it feeds is live. Removing the guard would have been equally defensible;
keeping it changes fewer bytes and covers the named/errored forms.

Corrected in all six places Band A listed:

| site | now reads |
|---|---|
| `TRANSPORT_R4_REPORT_2026-08-11.md:305` (superseded-edit table) | row struck; disposition changed to **NOT A DEFECT — ROUND-5 CORRECTION**, with the executed facts |
| `run_p0.sh:29-33`, `run_ro.sh:23-27`, `remote_setup_wpi.sh:62-66`, `remote_extract_verify_wpi.sh:53-57`, `remote_close_tree_wpi.sh:114-118` | the identical comment block replaced in all five: states the executed behaviour, labels the guard as hardening rather than a repair, and records that an overclaimed **defect** is still a false evidence claim |

`STATUS_TRANSPORT.md`'s "second latent defect" sentence is corrected too — Band A did not
list it, but it carried the same false claim.

### BA-3 (MEDIUM) — T8 overstates the two prerequisite reason tokens → **PROSE NARROWED; three of four sites NOT YET APPLIED**

**Branch taken: narrow the prose, not the classifier — per file, as required.**

The classifier is correct as written. `Get-OpOutcomeClass` returns
`scp_transfer_did_not_complete` (line 1103) for any nonzero `scp` and
`operation_reported_stop` (line 1108) for rc 3, both before the prerequisite branch
(lines 1116–1120) is reachable; only an **rc-1** `always` failure produces
`cleanup_after_unestablished_prerequisite` or `cleanup_after_earlier_deviation`. Codex's
round-4 Fixture B execution shows ops 09/10 and 11/12 doing exactly that with
prerequisites genuinely unestablished.

Widening the classifier so the broad claim became true would make the record **less**
precise — an operation whose own kind or status already explains the inability should
report that reason, not a prerequisite reason it never reached — and would require
re-proving F4's decisive fixture for no gain. The run verdict is fail-closed either way;
Band A itself classifies this as a claim-to-predicate mismatch, not a false PASS.

| site | disposition |
|---|---|
| `TRANSPORT_R4_REPORT_2026-08-11.md`, T8 | **APPLIED** — clause struck, correction states the reachability facts and the chosen branch |
| `WPI_PREREGISTRATION_DRAFT.md:688-691` | **NOT APPLIED** — `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`, edit 1 |
| `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:570` | **NOT APPLIED** — edit 2 |
| `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:678` | **NOT APPLIED** — edit 3, byte-identical to edit 2 as Band A requires |

The narrowed sentence keeps the two tokens for the rc-1 outcomes, names
`scp_transfer_did_not_complete` and `operation_reported_stop` as the earlier reasons, and
records that `TR_OP_PREREQ_STATE` still carries every edge's resolved class in all cases —
so the prerequisite state stays auditable from the record even where the reason token is
not a prerequisite token.

**BA-3 is therefore not fully closed by this session.** See §5.

## 2. What was NOT changed, and why

- **`TRANSPORT_PLAN.tsv`** — byte-unchanged. No finding touches it; its stdin digest
  columns are still `<PIN-AT-FREEZE>`.
- **The runner's classifier and prerequisite graph** — unchanged. BA-3 was answered by
  narrowing prose, per §BA-3.
- **`RP6-P0.sh`, `RP7-WPI-RO.sh`** — not touched; other sessions own them.
- **F2, F3, F4, T5, T6, T7** — no byte changes. Band A reproduced F4 and T5 on the frozen
  bytes and reconciled the census and the prerequisite/marker-family edits; nothing in
  round 5 disturbs them. The only F2-adjacent change is BA-1, which strengthens the
  read-only claim rather than weakening it.
- **No fence anywhere was weakened.** The only predicate changed in round 5 is the `mkdir`
  create block, and §BA-1 quotes the old and new assertions executed against the same
  deviant output.

## 3. Static gates on the repaired bytes

| gate | result |
|---|---|
| `bash -n` on all five delivered shell files | rc 0 for each |
| `bash -n _r5_wsl_fixtures.sh` | rc 0 |
| CR bytes per file (`tr -cd '\r' \| wc -c`) | 0 for all nine targets and the harness |
| Windows PowerShell 5.1.26100.8875 parse of `transport_runner.ps1` | `PARSE_ERRORS=0` |
| placeholder census over the seven executable/plan targets | `37` allocation / `38` pin — **unchanged from round 4** |
| `_r5_wsl_fixtures.sh` process rc | 0 |

The census is unchanged because every round-5 edit outside the close script's create
block is comment text, and the create block introduces no placeholder.

## 4. Delivered identities (round 5)

| Target | Bytes | SHA-256 | `<ALLOCATE-AT-DISPATCH>` | `<PIN-AT-FREEZE>` | CR | changed |
|---|---:|---|---:|---:|---:|:--:|
| `run_p0.sh` | 13,608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` | 6 | 8 | 0 | yes |
| `run_ro.sh` | 13,470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` | 6 | 4 | 0 | yes |
| `transport_runner.ps1` | 71,137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` | 3 | 7 | 0 | yes |
| `TRANSPORT_PLAN.tsv` | 7,970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` | 22 | 7 | 0 | **no** |
| `remote_setup_wpi.sh` | 26,483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` | 0 | 3 | 0 | yes |
| `remote_extract_verify_wpi.sh` | 23,592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` | 0 | 7 | 0 | yes |
| `remote_close_tree_wpi.sh` | 32,630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` | 0 | 2 | 0 | yes |
| `SELF_QA_TRANSPORT.md` | 176,070 | `59424c59f237f74c8a23c62fa3dcb7e07afc7f72d85dd6f00240ecab06dfd287` | — | — | 0 | yes |
| `STATUS_TRANSPORT.md` | 18,391 | `1bd4776a4ee2fdfd99c836d4829894d87d178ab1f932963f8ade975a2ef7186f` | — | — | 0 | yes |

Beside the frozen set, and not part of it:

| File | Bytes | SHA-256 |
|---|---:|---|
| `_r5_wsl_fixtures.sh` | 17,713 | `4d1a0b305d9c41341e5e37306a436f30b697e7e0af89b7de0801a50239667afe` |
| `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` | 7,173 | `a460e7f1524d0c21c833b0d83013017639214bbb23a647d155f17f07fdee2df6` |
| `TRANSPORT_R4_REPORT_2026-08-11.md` (corrected in place) | 38,356 | `33bdeced4f70d4e8e0d22b252b79afb1dabd0f13c5c4a8a05447e8f4f08b9b62` |

Only `remote_close_tree_wpi.sh` changed executable behaviour. The other five code changes
are comment text; `transport_runner.ps1`'s change is comment text only.

## 5. Not applied — stated plainly

`KICKOFF_TRANSPORT_REPAIR_R5.md` requires the F1 wording and the BA-3 narrowing to reach
the preregistration drafts. This session's dispatch instruction was:

> A parallel Max session owns `pathscope_prover.py` in `WPI_PREREG_DRAFT_ROUND1` — do not
> touch that directory.

That is the `AGENTS.md` **PARALLEL AGENT SAFETY** case, and the directory does carry
uncommitted work. The files were **read** and not written.

Four edits are therefore outstanding, specified as exact old → new text in
`TRANSPORT_R5_DRAFT_EDITS_PENDING.md`, with every anchor verified byte-exact and unique
against the current draft bytes (`grep -c -F` returns 1, 1, 1 and **2** respectively — the
successor draft's clause occurs exactly twice, as Band A requires):

1. `WPI_PREREGISTRATION_DRAFT.md:688-691` — BA-3.
2. `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:570` — BA-3.
3. `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:678` — BA-3, byte-identical to (2).
4. `WPI_PREREGISTRATION_DRAFT.md:357-360` — BA-1's every-exit-path sentence.

Plus one sweep that could not be performed without reading and possibly editing that
directory: any remaining draft text asserting F1 closure or the residual's
unreachability. The `grep` to run is given in the pending-edits file.

**This is not a `PENDING-LEAD-EXECUTION` item in the usual sense** — nothing about it
needs the Lead's host, credentials or authority. It is a session-boundary hold, and it is
the Lead's call whether to apply the four edits directly or hand them to whichever session
owns that directory next. Until they land:

- **BA-3 is NOT fully closed.**
- **F1's draft mirror is NOT yet aligned**, though every occurrence inside
  `WPI_BLOCKS_DRAFT/` is.

There is no other `PENDING-LEAD-EXECUTION` item in this round: BA-1's D026 RED/GREEN and
BA-2's falsification were both executed in this session.

## 6. What I did not verify

- Any real connection behaviour against `GATEA-STAGING`. No socket was opened.
- The **real** SSH account-shell boundary. §R5-2's reproduction is a local model of the
  composition step, executed and labelled as such; it demonstrates that the boundary is
  open, and it is explicitly **not** offered as closure evidence for anything.
- The remote scripts' behaviour on the real host, including whether `/proc/self/environ`
  and the `/usr/bin` pin set have the shapes this round assumes there.
- Whether the target host's `sshd`/account shell actually honours a startup file. F1 is
  marked OPEN because the transport **cannot establish** that it does not — not because a
  plant was observed on that host.
- Any part of `RP6-P0.sh` or `RP7-WPI-RO.sh`; neither was read or modified this round.
- The four unapplied draft edits, which by definition have not been executed against the
  draft bytes beyond anchor verification.

## 7. Required next action

Codex re-audit under T0 policy against the identities in §4. The three questions this
round most needs adversarial attention on:

1. **BA-1's narrowing.** Is "arm cleanup only on a zero-status create" the right cut, or
   does the uncovered nonzero-create arm need to become a refusal *before* the create —
   e.g. by proving exclusive creation some other way — rather than a recorded residue?
2. **F1's wording.** Does any surviving sentence anywhere in `WPI_BLOCKS_DRAFT/` still
   imply closure, unreachability, or that the account shell "cannot influence what runs"?
3. **BA-3's branch.** Is narrowing the prose the right call, or does the preregistration
   genuinely need every broken-branch `always` failure to name a prerequisite case — in
   which case the classifier, not the prose, is what must change?

Two items need the Lead rather than the auditor: applying (or reassigning) the four draft
edits in §5, and re-confirming the round-4 open items that F1's status change touches —
derivation classes 5 and 6 are still new permissions, and class 5 now buys an
inner-child guarantee rather than the end-to-end one round 4 implied.

This report grants no host, freeze, allocation, execution, dispatch, or Git authority.
