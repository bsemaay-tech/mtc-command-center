# VERDICT: REQUEST_CHANGES

TIER: T0.

APPLIED AUDITOR CONTRACT: fresh Codex `gpt-5.6-sol` at xhigh, read-only except
this verdict file. This is the Codex flagship slot; overall T0 acceptance still
requires the separately invoked Claude `claude-opus-5` xhigh slot. Round cap: 3.

## Required finding

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:2665`:
**MEDIUM - false byte-freeze claim.** The round-6 self-QA says, "No byte of the
nine-file transport set changed in round 6." The repository's established
nine-file definition is the seven executable/plan targets plus
`SELF_QA_TRANSPORT.md` and `STATUS_TRANSPORT.md`. Commit `979552d9` modifies both
of those documents, so the sentence is false and contradicts the actual commit
diff. The following sentence correctly narrows the unchanged identity claim to
the seven executable/plan targets.

Required repair: replace the first sentence at line 2665 with the narrow fact
actually established: "No byte of the seven executable/plan transport targets
changed in round 6." Do not change a transport target, the BA-1 harness, or the
honest OPEN disposition of F1 for this repair.

## Reasoning

R5-F2 and R5-F3 are closed on the audited bytes, and the Lead-applied R5-F1 draft
correction is present and honest. The exact R6-2 fixture reproduces the intended
RED/GREEN discrimination with one subject pathname and one argument vector, and
the static gates pass. No further defect was found in the harness rewrite. The
single false nine-file freeze statement is nevertheless a required evidence
repair: an accepting verdict cannot retain a byte-identity claim disproved by the
same commit's diff. F1 remaining honestly OPEN is not an acceptance blocker for
this focused round, but the transport block remains non-freezable until F1 is
closed out of scope.

## Evidence

### Scope and identities

- Audited exact commit: `979552d98bf63583493a32e4eb6fb64a3f8c63a1`.
- Its six changed paths are the BA-1 harness plus five evidence/status documents;
  no executable/plan transport target is in the commit diff.
- All seven executable/plan targets are byte-identical to round 5 commit
  `37a87046`; their byte counts and SHA-256 values reproduce the round-6 report
  table, 7/7.
- The canonical nine-file set is independently defined in the transport state
  assessment as those seven targets plus the QA and status documents. Therefore
  the self-QA's line-2665 claim is not a harmless synonym for the correct
  seven-target claim.

### R5-F2 - exact R6-2 rerun

The pre-repair close-script object was extracted by exact Git blob identity into
the prescribed scratch location. The candidate harness and current close script
were extracted from commit `979552d9`. Fixture stdout and stderr were redirected
to scratch files. The harness exited cleanly, wrote no stderr, and recorded ten
arms. The required summary is:

```text
SCRIPT_RC=3
RESIDUE_PRESENT=yes
SCRIPT_RC=3
RESIDUE_PRESENT=no
REFUSAL_BYTE_IDENTICAL=yes
BA1_ARMS_RECORDED=10
DISTINCT_SUBJECT_ARGV_LINES=1
```

Independent transcript checks also established:

- ten subject-path records, one distinct subject pathname;
- ten argv records, one distinct EV/RUNID/WORK_ROOT vector;
- ten subject-byte hashes, all ten distinct;
- the expected ten-arm script-status and residue vectors;
- exactly one refusal record in each D026 arm, byte-identical across RED/GREEN;
- the carried source fence occurs once at pre-repair line 402 and once at repaired
  line 483, with identical predicate text, and it still refuses both arms;
- the clean-run program records become byte-identical after normalizing only the
  documented removal-scope field.

This closes R5-F2. The round-5 transcript is correctly marked withdrawn, leaving
R6-2 as the single reproducibility target.

### R5-F1 - Lead-applied draft correction

- Both preregistration draft blobs at `979552d9` are byte-identical to their blobs
  at Lead commit `008d2dde`.
- The main draft records the inner-child-only disposition in derivation class 5
  and again in the remote-launch-domain section.
- The successor draft carries the same inner-child-only/outer-boundary-OPEN
  statement at both inherited sites.
- A scoped case-insensitive sweep found no claim that F1 is closed on the
  composition, that the startup residual is unreachable, that the operator side
  closes it, or that the account shell cannot influence what runs.

R5-F1's draft wording is therefore corrected. The underlying F1 remains honestly
OPEN, as required by the kickoff.

### R5-F3 - stale status

- `STATUS_TRANSPORT.md`, `TRANSPORT_R5_REPORT_2026-08-11.md`, and
  `SELF_QA_TRANSPORT.md` now record the four draft edits as applied and cite the
  carrying commits.
- `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` is retained but has a prominent
  SUPERSEDED/HISTORICAL-ONLY box stating that it is not an outstanding work list;
  its old live status is struck and explicitly replaced.
- Remaining uses of "pending" describe the superseded historical defect or the
  current re-audit state, not unapplied draft work. No live "not yet landed" claim
  remains.

This closes R5-F3.

### Static and safety gates

- Placeholder census over the seven executable/plan targets: allocation 37,
  freeze pin 38; unchanged.
- `bash -n`: clean for all five delivered shell files; the R6 harness is also
  clean.
- Windows PowerShell 5.1 parse: clean for `transport_runner.ps1`.
- CR-byte count: zero across the seven targets, harness, edited evidence/status
  documents, and the two preregistration drafts inspected.
- Commit scope contains only the expected six files. No protected Pine, parity,
  MTC, trading, schema, broker, credential, deployment, or host surface was
  changed.
- No host or network was contacted and no Git mutation was performed.

## Minimum required repair

Make only the line-2665 documentation correction stated above, preserve every
passing identity and fixture result, and return the exact repaired bytes for the
next bounded T0 re-audit.
