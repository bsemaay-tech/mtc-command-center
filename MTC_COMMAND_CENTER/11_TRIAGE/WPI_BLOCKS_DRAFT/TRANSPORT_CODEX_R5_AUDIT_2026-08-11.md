# Transport round-5 Codex audit

Date: 2026-08-11  
Frozen commit: `37a870464860d4eeade0e5ad13d34ec935d12c79`  
Tier: **T0**  
Auditor contract: fresh Codex `gpt-5.6-sol`, xhigh, read-only except for this verdict
file. No host contact, network connection, transport process, or Git mutation.

## Verdict

**REQUEST_CHANGES**

F1 being honestly OPEN is not an acceptance blocker. The round is non-accepting because
the audited bytes do not consistently carry that disposition, the published BA-1 D026
fixture does not satisfy its claimed same-argv control, and the final status/evidence
documents still describe draft edits that are already present in the frozen commit as
unapplied.

## Required findings

### R5-F1 — HIGH — the main preregistration draft still closes the open outer boundary

`WPI_PREREGISTRATION_DRAFT.md:333-352` still says that the exiting `STARTUP_PLANT`
case is “closed by the operator side.” That is the exact round-4 overclaim F1 required
round 5 to withdraw. The same draft's launch-domain narrative at `:556-577` continues to
present the cleared inner-child domain as the F1 answer without recording the required
status: **inner child closed; outer SSH account-shell boundary open**.

This also falsifies `TRANSPORT_R5_REPORT_2026-08-11.md:88-99`, which says every closure
or unreachability claim was removed or struck and identifies the draft as the only
unswept location, even though the final commit includes that draft. Pattern 9 applies:
the sentence still outruns the control. Pattern 11 is the underlying boundary error:
the attested inner instrument is not the earlier outer instrument that can produce the
accepted record.

Minimum repair: align both preregistration drafts with the exact OPEN disposition already
used by the runner and five scripts. In the main draft, correct both the derivation-class
description and the remote-launch-domain section; in the successor draft, make the
current open boundary explicit wherever it inherits the “cleared launch domain.” Then
repeat a scoped sweep for active closure, unreachability, or “cannot influence” claims.
Do not add a client-side closure mechanism inside the same shell string.

### R5-F2 — HIGH — the published BA-1 D026 arms do not use the claimed same argv

`SELF_QA_TRANSPORT.md:2446-2447` and
`TRANSPORT_R5_REPORT_2026-08-11.md:131-146` say the pre-repair and repaired arms use the
same instrument, launch, and argv, leaving delivered bytes as the only variable. The
delivered harness contradicts that claim:

- `_r5_wsl_fixtures.sh:145-148` runs the RED bytes through `RED_SUBJECT` with
  `RED_BASE` arguments.
- `_r5_wsl_fixtures.sh:155-158` runs the GREEN bytes through `GREEN_SUBJECT` with
  `GREEN_BASE` arguments.
- The recorded refusals at `SELF_QA_TRANSPORT.md:2667-2668` consequently differ in
  their path field, so the report's “byte-identical” refusal claim is also false.

The instrument and launch-domain shape are the same, and the code repair itself works.
I independently reran the two blobs through one common subject pathname and one common
argument vector, resetting the common tree between arms; RED retained the residue and
GREEN removed it. That supplemental audit result does not make the delivered harness's
opposite provenance claim true. D026 makes the implementer's recorded RED/GREEN and its
literal reproducibility part of closure evidence; Pattern 10 therefore applies.

Minimum repair: make `_r5_wsl_fixtures.sh` use one common subject pathname and one common
EV/RUNID/work argv for both arms, restoring the common tree between runs and replacing
only the subject bytes. Re-run it and replace the BA-1 transcript and the same-argv /
byte-identical-refusal claims in self-QA and the report. Keep the carried assertion
unchanged; it did retain discriminating power.

### R5-F3 — MEDIUM — final status and evidence still say committed draft edits are pending

The frozen commit contains BA-1's narrowed cleanup prose in the main draft, BA-3's
narrowed prose in the main draft, and both byte-identical successor occurrences. The
current evidence package nevertheless records the opposite:

- `STATUS_TRANSPORT.md:154-162` says the three BA-3 edits still need to land and BA-3
  is not fully closed.
- `TRANSPORT_R5_REPORT_2026-08-11.md:35-40,180,216-247,303-338` labels the four draft
  edits unapplied/outstanding.
- `SELF_QA_TRANSPORT.md:2411,2583-2590` and
  `TRANSPORT_R5_DRAFT_EDITS_PENDING.md:1-18` retain the same pending-state record with
  no final Lead addendum binding the later application.

Those statements may accurately describe the implementer session boundary, but they are
false as the final status of commit `37a87046`. Pattern 13 applies: the four admitted
edits reached a terminal disposition in Git, while the evidence/status chain still drops
that disposition.

Minimum repair: preserve the historical implementer-session account, but add a final
Lead application note to self-QA and the round-5 report; update `STATUS_TRANSPORT.md` and
the pending-edits record to APPLIED; bind the two final draft blob identities and the
commit. Do not mark F1 fully aligned until R5-F1 is repaired.

No optional nits are recorded.

## Evidence

### BA-1 execution — F1 exploit block deliberately excluded

I extracted the exact raw Git blobs for commit `37a87046` and the declared pre-repair
blob, then executed the BA-1 and BA-2 portions of `_r5_wsl_fixtures.sh` on local WSL. The
F1 `STARTUP_PLANT` block was not constructed or run, as the kickoff makes F1 a wording
and consistency check only. Fixture-process rc was 0; its own stderr line count was 0.

Published-harness BA-1 diagnostic arms, in transcript order:

```text
SCRIPT_RC=3
RESIDUE_PRESENT=yes
SCRIPT_RC=3
RESIDUE_PRESENT=no
```

Independent common-argv control:

```text
SCRIPT_RC=3
RESIDUE_PRESENT=yes
SCRIPT_RC=3
RESIDUE_PRESENT=no
```

The pre-repair and repaired SHA-256 identities matched the two identities required by
the kickoff. The delivered harness emitted 10 `SCRIPT_RC=` lines, 10
`RESIDUE_PRESENT=` lines, and 10 `CLOSE_STOP ...` lines across its BA-1 arms. The
carried old/new assertion compared equal after removing only its source line number
(1/1). The two recorded refusal lines were not byte-identical (0/1); after replacing
their distinct arm-base tokens with one symbolic base, they compared equal (1/1).

The deliberately uncovered nonzero-create arm remained fail-closed and recorded an
object-present disposition; the clean nonzero-create arm recorded object absent. The
removal no-op arm reached the removal-failure STOP. These checks support the executable
repair while leaving R5-F2 as an evidence-contract defect.

### BA-2

All 7/7 BA-2 arms matched the withdrawn-claim disposition: the bare enumeration and its
unguarded assignment continued, the two controls that genuinely return nonzero stopped,
the guarded form continued, guarded and unguarded forms preserved inherited-function
detection, and the delivered script refused the inherited function. No false RED remains
as an active claim; surviving mentions are explicitly historical and withdrawn.

### BA-3

The classifier order at `transport_runner.ps1:1090-1122` matches the narrowed prose:
nonzero transfer is classified first, rc 3 is classified second, and only the later rc-1
`always` branch reaches prerequisite adjudication. The main draft contains one narrowed
“first applicable reason” block. The successor phrase count is exactly 2, and the two
successor paragraphs compare byte-identical after removing the second occurrence's
Markdown quote prefix.

### Static and identity gates

| Check | Result |
|---|---:|
| `bash -n` on the five delivered shell files | 5/5 clean |
| `bash -n` on `_r5_wsl_fixtures.sh` | rc 0 |
| Windows PowerShell parser | major 5, `PARSE_ERRORS=0` |
| CR-byte scan over all 15 audited commit files | 15 checked, 0 nonzero |
| Placeholder census over seven executable/plan targets | allocation 37 / pin 38 |
| Round-5 report identity rows checked | 12/12 match, 0 mismatches |
| Successor narrowed-prose occurrences | 2; byte-identical 1/1 |

### Thirteen-pattern sweep

Patterns 9, 10, 11, and 13 produced R5-F1 through R5-F3. The only executable round-5
change is the close-script create/cleanup block; its synchronous STOP ordering, cleanup
adjudication, deliberately uncovered nonzero-create disposition, and carried fence held
in the executed arms. No additional required defect was found under patterns 1-8 or 12.

This audit grants no host, freeze, allocation, execution, dispatch, or Git authority.
