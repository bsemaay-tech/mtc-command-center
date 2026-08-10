# WP-I transport set status

**REPAIRED-PENDING-REAUDIT** (round 3 of the T0 cap 3 — the last round of the cap)

No host contact, RUNID allocation, archive build, freeze, execution, or Git commit was
performed. `C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry.

The real pinned `ssh.exe` and `scp.exe` were executed locally without connecting —
`ssh -G` evaluates configuration and exits, and `scp` copied one local file to another
— because round-2 Codex F2 required exactly that and it cannot be established any
other way. No socket was opened to any host; the only hostname passed to `ssh` was the
non-resolving literal `qa-target`, and `-G` returns before name resolution.

`<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` remain literal, and that is enforced
rather than incidental: a preflight marker gate STOPs the runner on the first unfilled
constant. Run exactly as it ships, the delivered file emits
`TR_STOP reason=unfilled_marker field=BASE_RUN` at exit 3 before it evaluates a path
(`SELF_QA_TRANSPORT.md` §5, arm L1).

Op → implementation: 01 `remote_setup_wpi.sh`; 02 pinned `runkit.tar` SCP up from
`01_RUNKIT`; 03 `remote_extract_verify_wpi.sh`; 04 `run_p0.sh`; 05 `run_ro.sh`;
06 bounded operator-side `tcp_probe`; **07/08 `remote_close_tree_wpi.sh`** — new this
round, the fourth derived script, resolved through the plan's `PREREG` root token;
09/10 SCP down; 11/12 local-only remote/local digest-set binding in
`transport_runner.ps1`.

## What changed in round 3

Both round-2 T0 re-audits returned REQUEST_CHANGES. Four required findings and one nit
are addressed, each with an executed RED/GREEN pair.

- **FAIL is now reserved for an operation that ran.** The round-2 classifier branched
  on the integer alone, so `ssh` exit 255 — its own code for a host that is down, a
  rejected key, a DNS failure or a dropped route, in which nothing was observed — was
  recorded as a completed observation of deviant host state. Classification is now by
  operation **kind** and by **provenance**: ssh rc 255, any rc outside `{0,1,3}`, any
  failed `scp` transfer, and a capture carrying no preregistered remote-program marker
  are all not-evaluable → `TR_RUN STOP`, exit 3. A cleanup row whose prerequisite
  sequence never completed can no longer manufacture a FAIL out of an honest STOP:
  driven over the whole 12-row plan, an early STOP that round 2 reported as
  `TR_RUN FAIL` (deviant=4) now reports `TR_RUN STOP` (deviant=0, not_evaluable=7).
- **The plan can now reach a remote block at all.** Under the round-2 child
  environment the real pinned OpenSSH exited **255 with zero bytes on both streams**
  before evaluating anything, because OpenSSH for Windows resolves `__PROGRAMDATA__`
  and has no fallback when `PROGRAMDATA` is unset. Measurement showed that is the only
  load-bearing variable in the constructed set. Ambient configuration is now disabled
  outright rather than inherited: `-F none` on every op refuses both the per-user and
  the system-wide `ssh_config`, `PROGRAMDATA` points at a run-owned empty directory
  under the record root, `UserKnownHostsFile`/`GlobalKnownHostsFile` are pinned files,
  `ProxyCommand`/`ControlMaster`/`ControlPath`/forwarding/local-command are all
  refused, and **nothing** is carried from the operator environment. The frozen option
  block lives inside the runner and every `ssh`/`scp` plan row must carry it verbatim.
- **The close operation is no longer PATH-selected.** The accepted
  `remote_close_tree.sh` invoked `mktemp`, `stat`, `tr`, `readlink`, `find`, `sort`,
  `sha256sum`, `cmp` and `rm` from the inherited `PATH`. Executed, a planted
  `sha256sum` appended to a closed evidence leaf and then delegated to the real tool;
  both digest passes observed the mutation, agreed, and the script printed
  `CLOSE PASS … wrote_into_evidence_tree=0` at rc 0. The accepted bytes are **not
  edited** — `remote_close_tree_wpi.sh` is a derivation whose only semantic delta is
  program identity, and under it the plant is never consulted.
- **The allocation parent's mount object is bound before the first `mkdir`.** A bind
  mount at the same literal canonical path with the same owner and mode satisfied
  `readlink -f` and every component predicate, and took all four allocations. The
  setup script now projects the covering mount from `/proc/self/mountinfo` and compares
  it with a preregistered constant; a mismatch STOPs before any mutation.

## Corrections to the round-2 status text

The round-2 entry led with "**A not-evaluable operation is no longer a FAIL**" and only
then narrowed to rc 3. That sentence outran the code and both flagships said so. It is
replaced above by a statement of what the classifier actually decides, per kind.

The round-2 self-QA placeholder census ("36 / 40") is corrected: the rejected baseline
carries 36 / 27 over the six executable/plan files and 41 / 33 over all eight
(`SELF_QA_TRANSPORT.md` §9).

## Freeze-gate inputs this round adds

Each must be supplied before the set can be frozen; until then the runner or the
script STOPs at rc 3, which is the intended fail-closed direction.

| input | consumer | source |
|---|---|---|
| `EXPECT_PARENT_MOUNT` | `remote_setup_wpi.sh` | the read-only attestation command set authorised as **owner grant #6**, run in the grant-#3 root session |
| `wpi_known_hosts` + its SHA-256 | `transport_runner.ps1`, every ssh/scp op | preregistered host-key material for `172.24.55.233` |
| `wpi_known_hosts_global` + its SHA-256 | same | the system half of the same decision |
| SHA-256 of `gatea_ed25519` | same | the pinned credential; compared, never printed |
| SHA-256 + bytes of `remote_close_tree_wpi.sh` | `TRANSPORT_PLAN.tsv` ops 07/08 | Stage 1, like every other derived script |

### Successor-ordering requirement (F4)

`EXPECT_PARENT_MOUNT` is the covering-mount identity of `/home/gatea` **as attested
from outside the login session being tested**. The successor preregistration must
therefore order the grant-#6 attestation **before op 01**, not merely before the RO
stage: op 01 is the operation that mutates, and an attestation taken afterwards cannot
make an earlier mutation retroactively target the accepted mount. The attested value is
embedded as a frozen constant and is never learned or re-pinned from the run.

## Open, and deliberately visible to the Lead

Section 4 of the preregistration draft was amended again this round: a **fourth**
derived script (`remote_close_tree_wpi.sh`), a mount-object clause added to derivation
class 3, and an operator-side configuration-identity rule added under class 2. Round 2
amended §4 to permit a four-class derivation of two scripts; round 3 extends that
permission to the close script and records that **no accepted Stage-2 script travels
unchanged any more**. The accepted originals are untouched and remain derivation bases.
This is the Lead's call to ratify, not a settled fact.

Deviation D-3 stands and is a hard Stage-1 precondition: `GATEA-STAGING` must carry
each `/usr/bin/<tool>` in the pin set as a regular, root-owned, not-group/other-writable
file, or ops 01, 03, 07 and 08 will STOP at dispatch. The QA kernel ships them as
symlinks and the scripts refuse them, which is the safe direction but is not the target
host's state.

The set remains authority- and budget-blocked by the preregistration's own dispatch
gates (§0 F6 amendment, §12). Nothing here is dispatch authority.
