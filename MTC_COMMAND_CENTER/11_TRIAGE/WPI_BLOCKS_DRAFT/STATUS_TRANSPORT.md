# WP-I transport set status

**REPAIRED-PENDING-REAUDIT** (round 2 of the T0 cap 3)

No host contact, RUNID allocation, archive build, freeze, execution, or Git
commit was performed. `C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry.

`<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` remain literal, and that is now
enforced rather than incidental: a preflight marker gate STOPs the runner on the
first unfilled constant. Run exactly as it ships, the delivered file emits
`TR_STOP reason=unfilled_marker field=BASE_RUN` at exit 3 before it evaluates a
path — the round-1 claim that the placeholders make the draft STOP is, for the
first time, demonstrated rather than asserted (`SELF_QA_TRANSPORT.md` §4, arm I).

Op → implementation: 01 `remote_setup_wpi.sh`; 02 pinned `runkit.tar` SCP up
from `01_RUNKIT`; 03 `remote_extract_verify_wpi.sh`; 04 `run_p0.sh`;
05 `run_ro.sh`; 06 bounded operator-side `tcp_probe`; 07/08 the accepted
byte-identical `remote_close_tree.sh`, resolved through the plan's `ACCEPTED`
root token to the frozen Stage-2 directory at `87157f0e…`; 09/10 SCP down;
11/12 local-only remote/local digest-set binding in `transport_runner.ps1`.

## What changed in round 2

Both round-1 T0 audits returned REQUEST_CHANGES; all 16 required findings are
addressed, each with an executed RED/GREEN pair. The four that changed behaviour
most:

- **Ops 11/12 can now bind.** A `$Matches` clobber made every remote digest parse
  as null, so a byte-perfect run reported `digest_differs` for every file and
  FAILed after both one-use RUNIDs were spent. A byte-equal pair now returns
  `TR_BIND_PASS` and exit 0; a differing pair FAILs for its own specific reason.
- **A not-evaluable operation is no longer a FAIL.** Op rc 3 now produces
  `TR_RUN STOP` and the runner's documented exit 3. When a genuine deviant
  observation and a later STOP coexist, the deviant observation wins and both are
  counted in `TR_RUN_CLASS`.
- **Nothing on the inherited PATH selects evidence-producing code.** `ssh`/`scp`
  run only from frozen absolute paths, digest- and ACL-bound by numeric SID, with
  a constructed environment and a run-owned TEMP; the wrappers and both remote
  scripts pin their tools the same way and no longer create a `mktemp` object.
- **STOP happens before mutation.** `remote_setup_wpi.sh` binds the whole parent
  chain, compares numeric identity, and refuses an ambiguous path diagnostic
  before the first `mkdir`; `remote_extract_verify_wpi.sh` adjudicates status,
  diagnostics and record completion before it parses a listing.

## Evidence standard

Every closure carries the exact executable command and its real output, RED and
GREEN, in `SELF_QA_TRANSPORT.md`. The shell RED arms execute the audited round-1
bytes read from commit `1c1c9ed1`; the runner RED arms execute the current file
with the repair reverted at an asserted anchor. Arms that were not driven are
listed by name as supplemental, with the direction each fails in.

## Open, and deliberately visible to the Lead

Preregistration §4 was amended this round to permit a materially larger
derivation of the two reused remote scripts than round 1 allowed, because two
required findings cannot be satisfied inside a constants block. The amendment is
enumerated as four closed classes in §4 and raised as a deviation request in
`TRANSPORT_REPAIR_R2_REPORT.md`; it is the Lead's call, not a settled fact.

The set remains authority- and budget-blocked by the preregistration's own
dispatch gates (§0 F6 amendment, §12). Nothing here is dispatch authority.
