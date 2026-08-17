# WP-I transport set status

**CODEX-FLAGSHIP-ACCEPTED — PENDING SECOND FLAGSHIP** (round 6b, under owner grant #7 —
the T0 cap is lifted for this block set until both flagships accept)

*Header corrected 2026-08-12 ~18:20. It read `REPAIRED-PENDING-REAUDIT` and the body never
recorded the round-6 audit cycle at all, even though this file was edited earlier the same day
for the owner's F1 ratification. The omission was found by a systematic STATUS-versus-bytes
sweep (`WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md`), not by an auditor. The state was
understated, not overstated.*

**The round-6 Codex cycle, now recorded:**

1. `TRANSPORT_CODEX_R6_AUDIT` returned **REQUEST_CHANGES** on a real defect: `SELF_QA_TRANSPORT.md`
   claimed the **nine-file** set was byte-unchanged, when two of those nine — this status file and
   the self-QA itself — had in fact changed, carrying the R5-F2/R5-F3 corrections. A byte-identity
   claim that covers files which actually moved is exactly the defect class this project keeps
   finding.
2. **That claim is already repaired in the bytes.** `SELF_QA_TRANSPORT.md:2667-2668` now scopes
   the unchanged claim to the **seven targets**, and the placeholder census and CR-byte checks at
   `:2631-2633` are stated over those seven.
3. `TRANSPORT_CODEX_R6B_CONFIRM` then returned **PASS** (commit `7e4b5e9f`), **closing the Codex
   flagship slot** for this set.

**What is therefore still pending is only the second flagship** — the Claude `claude-opus-5`
audit, scheduled for the 23:00 window via
`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md`. A GLM advance read-audit
(`TRANSPORT_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`) returned PASS-WITH-NITS with zero required
repairs, but is ADVANCE-SUPPLEMENTAL and closes no slot.

**F1 is OPEN: inner child closed; outer SSH account-shell boundary open.** Round 4
recorded F1 as closed on the composition with one disclosed residual. Codex's round-4
Band B audit rejected that, and round 5 accepts the finding: see "What changed in
round 5" below. No other finding is open on these bytes.

**OWNER RATIFICATION 2026-08-12 (in chat, recorded at handoff commit `6fcafe39`):
F1 is ACCEPTED-WITH-DISCLOSURE.** F1 stays honestly OPEN as an inherent limit of the
SSH trust model; it is carried as an accepted, explicitly disclosed residual and is
**not a freeze blocker** — the block set is freezable with F1 disclosed. Closure (an
enforcement point ahead of account-shell startup processing) remains a successor item;
no text may present the cleared inner-child domain as an end-to-end F1 closure.

**The three findings of Codex's round-5 re-audit are closed** — see "What changed in
round 6". They were an evidence-provenance defect in the fixture (R5-F2), a stale
pending status for draft edits that had already landed (R5-F3), and a draft-side F1
wording gap the Lead applied directly (R5-F1). **No transport target byte changed in
round 6**; the only executable change is the harness beside them.

No host contact, RUNID allocation, archive build, freeze, execution, or Git commit was
performed. No external listing is claimed here; the delivered runner cannot create a
`C:\WPI_ARTIFACTS\WPI_TRANSPORT_*` record root while shipped with markers because the
marker gate fires before record-root creation and `Flush-Log` writes nothing until
`RecordReady` is true. The QA arms used fixture scratch for `RECORD_ROOT`.

Rounds 4, 5 and 6 ran their shell fixtures against a **local WSL2 Ubuntu kernel**;
every path they touch is under `/root/wpi_r4*` or `/root/wpi_r5` on that local
filesystem. The operator-side fixtures start no process at all. No socket was opened to
any host in any round, and no `ssh.exe`, `scp.exe` or `sshd` process was started.

Round-3 Fixture D has a bounded reproducibility disclosure: its cleanup failed
access-denied on `C:\Users\Public\wpi_r3\qb\pd_evil\ssh\ssh_config`, and the published
fixture body does not check the `icacls` restore exit code or assert the cleanup
post-condition. The residue is inert for the delivered set and later WSL2 rounds, but a
re-auditor on the same host may need to clear it or repair the fixture before re-running
that historical body.

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
  **Scope corrected in round 5:** that result is about the *inner child*. It does not
  close F1 — see "What changed in round 5" and open item 2.
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
  every exit path taken after the create returned 0 — **narrowed in round 5**, see
  BA-1 below. The read-only claim is now earned.
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

## What changed in round 5

Codex's two round-4 T0 audits both returned REQUEST_CHANGES: Band B on F1, Band A on
BA-1/BA-2/BA-3. All four are addressed. Every byte change has an executed RED/GREEN or
an executed falsification in `SELF_QA_TRANSPORT.md` §R5; the placeholder census and all
static gates are unchanged.

- **F1 is OPEN — the verdict, not the code, was wrong (Band B).** Round 4 said the
  exiting-`BASH_ENV` residual was *unreachable from the frozen plan* because the runner
  enforces the `env -i` domain verbatim on every plan row. That reasons about the wrong
  interpreter: the runner starts local `ssh.exe` and supplies a remote command *string*,
  and `sshd` gives that string to the account's shell, which processes its own startup
  environment **before** the string's first token — no plan row required. Reproduced
  locally against the **repaired** bytes: rc 0, a forged `CLOSE PASS`, and zero record
  lines from the real program, which the runner's provenance test would accept because
  it binds marker *shape* to a plan row rather than to the producing process. What the
  domain still does close is the inner child, and the stealthier plant that lets the
  script run is still refused by name at rc 3. No client-side control was invented; a
  command inside the same shell string cannot act before the shell that runs it. The
  claim is now stated identically in the report, this file, the self-QA, the runner and
  all five wrappers: **inner child closed; outer SSH account-shell boundary open**.
- **The close script no longer leaves residue on a post-creation STOP (BA-1, HIGH).**
  `mkdir` created the work directory, the next line STOPped on any diagnostic, and the
  cleanup trap was not installed until twenty lines later, so that branch exited at rc 3
  with the directory still there — Codex reproduced `SCRIPT_RC=3 … RESIDUE_PRESENT=yes`.
  The create now captures rc and diagnostics without refusing; on rc 0 the cleanup is
  armed **before** the diagnostic is adjudicated and before every later check. Same
  instrument, same launch, same argv, only the bytes differ: pre-repair
  `RESIDUE_PRESENT=yes`, repaired `RESIDUE_PRESENT=no`, with the reasoned STOP retained
  byte-for-byte. *(Round-5's harness did not in fact use one common argv, which Codex's
  round-5 re-audit caught as R5-F2; the harness is repaired and re-run in round 6, and
  the sentence above is now carried by `SELF_QA_TRANSPORT.md` §R6-1/§R6-2 —
  `DISTINCT_SUBJECT_ARGV_LINES=1` over ten arms and `REFUSAL_BYTE_IDENTICAL=yes`.)* A
  **nonzero** `mkdir` is deliberately *not* covered — a nonzero status
  is no evidence the object at that path is the one this run created — so that arm STOPs
  while recording `object_after_failed_create=present|absent`, and the header, the create
  block and the `CLOSE_NOTE scratch` field all state the narrowed scope instead of the
  old every-exit-path sentence.
- **The claimed second `declare -F` defect was FALSE and is withdrawn (BA-2).** Bare
  no-argument `declare -F` returns 0 in a function-free shell; the unguarded assignment
  under `set -Eeuo pipefail` runs straight through. Only a *named* lookup of a missing
  function returns 1. A control in the identical shell shape confirms `set -e` is armed,
  so this is a falsification and not an inactive-option artefact. The `2>/dev/null || :`
  guard is **kept as explicit no-op hardening** — the guarded and unguarded forms list an
  inherited exported function identically, so keeping it removes no detection — and the
  false explanation is corrected in the round-4 report and in all five delivered scripts.
  An overclaimed *defect* is still a false evidence claim.
- **T8's two prerequisite reason tokens are overstated (BA-3).** The classifier returns
  `scp_transfer_did_not_complete` and `operation_reported_stop` before the
  prerequisite-based rc-1 branch is reachable, so only rc-1 cleanups actually yield
  `cleanup_after_unestablished_prerequisite` / `cleanup_after_earlier_deviation`. Round 5
  narrows the prose rather than widening the classifier: an operation whose own kind or
  status already explains why it is not evaluable should report *that*. The round-4
  report's T8 disposition is corrected here; the three mirrored draft sentences live
  under `WPI_PREREG_DRAFT_ROUND1/`, which a parallel session owned during round 5, and
  their exact replacement text was specified in `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`
  for the Lead to apply. **The Lead applied all three, plus the BA-1 draft mirror,
  before freezing: they are present in commit `37a87046`, and BA-3 is FULLY CLOSED.**
  Verified read-only on the committed bytes in round 6 — `SELF_QA_TRANSPORT.md` §R6-3
  carries the per-edit check and the bound draft blob identities.

## What changed in round 6

Codex's round-5 re-audit (`TRANSPORT_CODEX_R5_AUDIT_2026-08-11.md`, REQUEST_CHANGES,
frozen commit `37a87046`) confirmed the BA-1 **code** repair works — it reran both
blobs through one common subject and one common argv itself, and RED retained the
residue while GREEN removed it — and raised three findings about the evidence rather
than the bytes. **No transport target byte changed in round 6.** All seven
executable/plan targets hash exactly as the round-5 report §4 recorded them.

- **The published BA-1 fixture did not use the argv it claimed (R5-F2, HIGH) —
  REPAIRED and re-run.** Round 5's `_r5_wsl_fixtures.sh` gave each arm its own subject
  pathname and its own tree, so the RED and GREEN refusals differed in their `path=`
  field and the "same instrument, launch and argv" and "byte-identical refusal" claims
  were false of the delivered harness. Every BA-1 arm now resets **one** tree, installs
  its bytes at **one** subject pathname and launches with **one** argument vector; the
  arm prints the pathname, the argv and the installed SHA-256, and the harness asserts
  the result — `BA1_ARMS_RECORDED=10`, `DISTINCT_SUBJECT_ARGV_LINES=1`,
  `REFUSAL_BYTE_IDENTICAL=yes`. Every arm's disposition is unchanged: RED
  `RESIDUE_PRESENT=yes`, GREEN `RESIDUE_PRESENT=no`, the carried fence still refusing in
  both. The round-5 transcript is **withdrawn** rather than kept beside the new one, so
  a re-auditor has exactly one reproducibility target: `SELF_QA_TRANSPORT.md` §R6-1 and
  §R6-2.
- **The four cross-directory draft edits had already landed (R5-F3, MEDIUM) —
  status corrected.** The round-5 chain recorded them as outstanding; that was true of
  the implementer session's boundary and false as the final status of the frozen
  commit. The Lead applied the three BA-3 edits and the BA-1 draft mirror in
  `37a87046`. `STATUS_TRANSPORT.md` (above), the round-5 report and the self-QA now say
  APPLIED and cite the commit; `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` is marked
  **SUPERSEDED** and kept as the historical specification rather than deleted. **BA-3 is
  fully closed** and **F1's draft mirror is aligned.**
- **The prereg drafts' F1 wording (R5-F1, HIGH) — applied by the Lead, commit
  `008d2dde`.** Round 6 did not touch `WPI_PREREG_DRAFT_ROUND1/`; it verified the
  result read-only. Both drafts now state *inner child closed; outer SSH account-shell
  boundary OPEN* at every site the finding named, and the scoped sweep for closure,
  unreachability or "cannot select or influence" claims returns no F1-related hit.
  Detail and bound blob identities: `SELF_QA_TRANSPORT.md` §R6-4.

**F1 remains OPEN.** Nothing in round 6 narrows it.

## The superseded concurrent edit

Commit `cf049b6b` preserved an unverified close-script edit from another session. Per
the Lead's addendum it is **superseded**, and round 4 restarted from the round-3 bytes
at `78173bfd`. Driven exactly as its own header prescribed, that edit refuses its own
clean execution: it sweeps `declare -F` *after* defining `ld_stop`, so a clean launch
emits `CLOSE_STOP reason=launch_domain_inherited_shell_function` at rc 3. Round 4 also
claimed a *second, independent* latent defect in the same two lines — that bare
`declare -F` exits 1 with no functions defined and would end the run under `set -e`.
**That claim was FALSE and is withdrawn in round 5** (Codex Band A, BA-2); the executed
falsification is in `SELF_QA_TRANSPORT.md` §R5-3. Its substantive ideas — a launch-domain
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
2. **F1 IS OPEN — inner child closed, outer SSH account-shell boundary open.**
   *Owner ratification 2026-08-12: accepted-with-disclosure, not a freeze blocker (see
   header). The finding stays OPEN and honestly described; only its freeze-gating status
   changed.* This is
   the one unrepaired finding on these bytes, and it is a finding rather than a
   disclosure. `sshd` does not execute the remote command string itself: it hands the
   string to the account's shell, and that shell processes its own startup environment
   (`BASH_ENV`/`ENV`, or whatever startup controls that shell honours) **before** the
   string's first token, `/usr/bin/env`, runs. An exiting startup file can therefore
   emit a line carrying the row's registered marker prefix, return rc 0, and never let
   the delivered script run — and the runner's provenance test cannot separate that from
   the intended program, because it binds marker *shape* to a plan row rather than to the
   producing process. **No command inside the same shell string, on either side, can act
   before that shell.** What the frozen `env -i` domain and the class 5 sweep do
   establish is the inner child: its exec environment is exactly the three constructed
   entries, so the stealthier plant that lets the script run is refused by name at rc 3.
   Closure requires an enforcement point ahead of account-shell startup processing — a
   deploy-channel-attested forced command / execution contract, or a transport path with
   no unbound shell — plus D026 evidence driven through the real top-level path. That is
   a successor item and is **not** claimed here. A disclosure is not a control.
3. **The remote account shell is outside the attestation, and acts first.** Round 4 said
   `env -i` clears what that shell exports and both launch programs are absolute, so the
   shell "cannot select or influence what runs". **That sentence is withdrawn** — it does
   not compose with item 2. `env -i` constrains that shell's *child*, not the shell, and
   the shell runs first. Its integrity, and whether it processes a startup file at all,
   are deploy-channel properties this set does not establish.
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
