# WP-I transport set status

**REPAIRED-PENDING-REAUDIT** (round 4, under owner grant #7 — the T0 cap is lifted
for this block set until both flagships accept)

No host contact, RUNID allocation, archive build, freeze, execution, or Git commit was
performed. `C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry.

Round 4 ran its shell fixtures against a **local WSL2 Ubuntu kernel**; every path they
touch is under `/root/wpi_r4*` on that local filesystem. The operator-side fixtures
start no process at all. No socket was opened to any host in this round.

`<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` remain literal, and that is enforced
rather than incidental: a preflight marker gate STOPs the runner on the first unfilled
constant. Run exactly as it ships, the delivered file emits
`TR_STOP reason=unfilled_marker field=BASE_RUN` at exit 3 before it evaluates a path
(`SELF_QA_TRANSPORT.md` §5, arm L1).

Op → implementation: 01 `remote_setup_wpi.sh`; 02 pinned `runkit.tar` SCP up from
`01_RUNKIT`; 03 `remote_extract_verify_wpi.sh`; 04 `run_p0.sh`; 05 `run_ro.sh`;
06 bounded operator-side `tcp_probe`; 07/08 `remote_close_tree_wpi.sh`;
09/10 SCP down; 11/12 local-only remote/local digest-set binding in
`transport_runner.ps1`.

## What changed in round 4

Both round-3 T0 audits are addressed: Codex returned REQUEST_CHANGES with four
required findings (F1–F4), Claude returned an accepting verdict with nits, and the Lead
adjudicated F4 in Codex's favour. Four further items (T5–T8) came from the
successor-skeleton review. Every item below has an executed RED/GREEN pair in
`SELF_QA_TRANSPORT.md` §R4; nothing is credited on the strength of a comment.

- **The remote interpreter is inside the pinned program domain (F1).** Rounds 1–3 sent
  every stdin script to bare `bash -s --`. Re-executed here with the delivered bytes: a
  fake `bash` first on `PATH` returned rc 0, ignored the delivered script and printed a
  forged `CLOSE PASS`; under an absolute interpreter an inherited `BASH_ENV` did the
  same. All six `ssh_stdin` rows now carry one frozen launch domain —
  `/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea /usr/bin/bash
  --noprofile --norc -s --` — which `transport_runner.ps1` holds as a constant and
  requires verbatim, and **each delivered script re-attests that same domain from the
  inside** before its first external program (derivation class 5). With both plants
  still in place the frozen argv produced the real record and neither plant ran.
- **Provenance is bound per operation, not to a global marker union (F1).** Round 3
  accepted any of the five programs' prefixes for any ssh row, so a close operation
  accepted `SETUP PASS` from an unrelated program as its own provenance and the run
  reported PASS. Each row's expected family is now bound to the stdin artifact it
  sends; the same fixture is now `not_evaluable … expected_family=remote_close_tree_wpi.sh`
  and the run STOPs. An `ssh_stdin` row whose stdin leaf has no registered family is a
  plan STOP before execution.
- **The close script no longer inherits a scratch location (F2).** Round 3 kept
  `mktemp` and *disclosed* the inherited-`TMPDIR` residual in its header. Executed, that
  disclosure cost evidence: with `TMPDIR` set to the tree being measured the script
  created and hashed its own file inside evidence and printed
  `wrote_into_evidence_tree=0` at rc 0. A disclosure is not a control. `mktemp` is gone;
  op 01 now allocates a fifth directory, `<REMOTE_BASE>/work`, and the plan passes it to
  ops 07/08 as a third argument. The close script proves canonical two-way non-overlap
  with the evidence tree before creating `close_work_<RUNID>` at mode 0700, proves it
  again on the object `mkdir` produced, and adjudicates the removal's own status on
  every exit path instead of ignoring it. The read-only claim is now earned.
- **An ambiguous close probe STOPs (F3).** With a mixed `No such file or directory;
  Permission denied` diagnostic the round-3 script returned `CLOSE_FAIL
  reason=evidence_dir_absent` rc 1 — a completed observation of missing evidence
  manufactured out of an inability to evaluate. The absence sentence is now calibrated
  once, in-run, from the pinned `stat` itself and matched as a whole string with the
  kernel corroborating; the same fixture now returns `CLOSE_STOP` rc 3.
- **Cleanup prerequisites are per branch and per operation (F4, Lead adjudication).**
  The single global `$sequenceOk` snapshot is gone. The runner freezes the dependency
  graph (07←04, 08←05, 09←07, 10←08, 11←07+09, 12←08+10), binds it to the plan before
  execution, and resolves each edge against the class that operation actually received.
  Codex's decisive fixture now goes GREEN: ops 01–06 match, op 07 `CLOSE_STOP` rc 3, op
  08 a genuine marked `CLOSE_FAIL` rc 1 → `deviant=1`, `TR_RUN FAIL` rc 1, where round 3
  reported `deviant=0`, `TR_RUN STOP`. Claude's scenario still holds: a cleanup after a
  genuinely unestablished prerequisite stays not-evaluable. The two cases now carry
  distinct reasons — `cleanup_after_unestablished_prerequisite` and
  `cleanup_after_earlier_deviation` — with the resolved prerequisite classes in the
  record.
- **`run_p0.sh` wires the five `P0_ATTESTED_*` values (T5).** Round 3 defined and
  exported none of them, so the composition STOPped at
  `execution_domain_unattested … detail=preregistered_value_missing` before any host
  observation. Proved by execution, not assertion: the real wrapper was launched under
  the frozen launch domain with the connection stubbed and its exported environment
  captured at the block position (0 names before, 5 after), and the **real
  `RP6-P0.sh` row-8 gate bytes** were then driven with exactly that environment —
  `preregistered_value_missing` before, `P0_GATE_PASSED` after with both sides filled,
  and `prelude_value_differs_from_frozen_pin` when one value is changed.
- **The close contract, its bytes and the plan now agree (T6).** The draft claimed
  classes 5 and 6, a cleared launch domain and a run-owned `WORK_ROOT`; the bytes took
  two arguments and inherited `TMPDIR`; the plan passed two arguments. All three now
  state the same three-argument contract, and an argv-count, RUNID-grammar or
  `EV_DIR`/`RUNID` disagreement is rc 3 rather than the rc 1 that would have reached the
  runner as a deviant *host* observation.
- **The inert `WPI_INTERPRETER_TARGET` pin is removed (T7).** `RP7-WPI-RO.sh` never read
  it; it derives `<venv>/bin/python` itself and refuses a symlink. A filled but unread
  value costs a deploy-channel answer and establishes no preregistered check. It is gone
  from the wrapper and absent from the draft's input table. RP7 was not touched.
- **The transport summary is stated once, correctly (T8).** §6 of the preregistration
  draft now carries first-*mismatch* sequencing, per-kind and per-provenance
  classification, the not-evaluable set, and the per-branch cleanup rule with its two
  distinct reasons; the successor draft R3's §6 sentence was extended to match.

## The superseded concurrent edit

Commit `cf049b6b` preserved an unverified close-script edit from another session. Per
the Lead's addendum it is **superseded**, and round 4 restarted from the round-3 bytes
at `78173bfd`. Driven exactly as its own header prescribed, that edit refuses its own
clean execution: it sweeps `declare -F` *after* defining `ld_stop`, so a clean launch
emits `CLOSE_STOP reason=launch_domain_inherited_shell_function` at rc 3. A second
latent defect in the same two lines was found while re-deriving them and is recorded in
`TRANSPORT_R4_REPORT_2026-08-11.md`. Its substantive ideas — a launch-domain
attestation, an exact absence template, numeric identity, and a run-owned `WORK_ROOT` —
were re-derived and kept; each is now reachable from a plan-passed invocation and each
carries executed evidence. Its argv-count arm, which returned rc 1, was dropped.

## Corrections to the round-3 status text

The round-3 entry said program identity was the close script's only semantic delta. That
is superseded: the permitted deltas are classes 2, 3, 5 and 6, and the round-3 sentence
is withdrawn rather than quietly widened. The round-3 header's `mktemp` disclosure
paragraph is withdrawn with it.

## Freeze-gate inputs

Each must be supplied before the set can be frozen; until then the runner or the script
STOPs at rc 3, which is the intended fail-closed direction.

| input | consumer | source |
|---|---|---|
| `EXPECT_PARENT_MOUNT` | `remote_setup_wpi.sh` | the read-only attestation command set authorised as **owner grant #6**, run in the grant-#3 root session, ordered **before op 01** |
| `EXPECT_UID` / `EXPECT_GID` | `remote_setup_wpi.sh`, `remote_close_tree_wpi.sh` | the recorded numeric identity of `gatea` |
| `P0_ATTESTED_USER_NS` / `MNT_NS` / `PID_NS` / `NET_NS` / `ROOT_MOUNT_ID` | `run_p0.sh` → `RP6-P0.sh` row 8 | **new this round** (T5): deploy channel, owner grant #6, never learned from the login under test. `RP6-P0.sh`'s own `P0_FIXED_ATTESTED_*` literals must be filled to the same values, or the gate STOPs |
| `wpi_known_hosts` + its SHA-256 | `transport_runner.ps1`, every ssh/scp op | preregistered host-key material for `172.24.55.233` |
| `wpi_known_hosts_global` + its SHA-256 | same | the system half of the same decision |
| SHA-256 of `gatea_ed25519` | same | the pinned credential; compared, never printed |
| SHA-256 + bytes of all five delivered shell files | `TRANSPORT_PLAN.tsv` stdin pins | Stage 1 |

Placeholder census over the seven executable/plan targets: **37** `<ALLOCATE-AT-DISPATCH>`
and **38** `<PIN-AT-FREEZE>`, against 36 / 33 in round 3. The delta is exactly
+2 allocation (the work root in plan rows 07/08), +5 pin (`P0_ATTESTED_*`), +2 pin
(the close script's numeric `EXPECT_UID`/`EXPECT_GID`), −1 pin
(`WPI_INTERPRETER_TARGET`, removed) and −1/−1 (the runner's `$UNFILLED_MARKERS`
guard is now composed rather than a literal, so the only markers left in that file
are consumers).

## Open, and deliberately visible to the Lead

1. **Derivation classes 5 and 6 are new permissions.** §4 of the draft now enumerates
   six classes rather than four. Round 4 wrote them into the contract because F1 and F2
   cannot be satisfied inside the existing four. This is the Lead's call to ratify.
2. **One measured residual on F1, disclosed rather than papered over.** `bash` reads
   `$BASH_ENV` before the first byte of a stdin-delivered script, and
   `--norc`/`--noprofile` do not disable that channel, so a startup plant that *exits*
   forges the record before any in-script attestation can run. Nothing inside a
   delivered script can close it. It is closed by the operator side — the runner refuses
   any plan row that does not carry the `env -i` domain verbatim, and that domain
   supplies an explicit complete variable list — so the case is unreachable from the
   frozen plan. A plant that lets the script run is refused by the class 5 sweep at
   rc 3. Both cases are executed in self-QA.
3. **The remote login shell is outside the attestation.** `sshd` runs the command string
   with the account's login shell. `env -i` clears what that shell exports and both
   launch programs are absolute, so the shell cannot select or influence what runs — but
   its own integrity is a deploy-channel property, not something this set establishes.
4. **Deviation D-3 stands** and is a hard Stage-1 precondition: `GATEA-STAGING` must
   carry each `/usr/bin/<tool>` in the pin set — now including `/usr/bin/env` and
   `/usr/bin/bash` — as a regular, root-owned, not-group/other-writable file, or ops 01,
   03, 04, 05, 07 and 08 will STOP at dispatch. The QA kernel ships them as symlinks and
   the scripts refuse them, which is the safe direction but is not the target host's
   state.
5. **`run_p0.sh` and `run_ro.sh` now run under `env -i`.** The wrappers export what the
   blocks need, but neither block has been executed end to end under this domain — that
   cannot be done without the host. If a block turns out to require an environment name
   the launch domain does not deliver, it will STOP at rc 3, which is the fail-closed
   direction, and the domain or the wrapper's export set is what changes.

The set remains authority- and budget-blocked by the preregistration's own dispatch
gates (§0 F6 amendment, §12). Nothing here is dispatch authority.
