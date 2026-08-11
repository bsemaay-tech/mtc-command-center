# RP7 status

Status: **REPAIRED-R8-PENDING-INDEPENDENT-REAUDIT**

Scope: `RP7-WPI-RO.sh` implements remote RO-stage rows 10-23 and records row 24
as operator-side only. Repair round 8 was authorized under owner grant #7, which
lifts the T0 round cap for this block set until both flagships accept. It answers
the Codex T0 part-B re-audit of the round-7 bytes
(`RP7_CODEX_T0_AUDIT_R7_PART_B_2026-08-11.md`, BLOCK on four findings, two of
them HIGH). Codex is the auditor of record and re-audits these bytes, so
implementer/auditor separation holds. Round 7's code repairs were confirmed by
that audit - the three NUL record STOPs, both queue-field STOPs, the
descriptor-bound listener inventory and the intended kill-after path all retain
their clean/wildcard/record-disposition controls - and were built on, not
re-litigated.

**One finding this round is not about the block.** Round 7 repaired four real
defects and, in the same edit, relaxed a carried regression assertion from `rc=0`
to the basic regex `rc=[0-9]*`, then justified the relaxation with a statement
about the old assertion that was false. That is Pattern 10 - evidence that cannot
fail - arriving from behind: the arm could fail yesterday and could not today.
The correction, and the rule that follows from it, are the first item below.

Material repair state added this round:

- **the weakened carried assertion is restored, and the false justification is
  corrected.** The round-6 fence's F5 leaf-race arm asserted
  `LEAF_RACE rc=0 outside_text=ORIGINAL ...`; round 7 moved the call into a
  subshell so the arm could survive an MSYS2 STOP - which was necessary - and in
  the same edit changed `rc=0` to `rc=[0-9]*`, which was not. Codex inserted an
  unrelated `return 7` at the top of `wpi_capture` and showed the relaxed
  assertion passing where the predecessor failed. The assertion now accepts
  exactly two outcomes and nothing else: **rc 0 with an empty capture result**
  (the `/dev/fd` re-open succeeded although the leaf name was gone - Linux), or
  **rc 3 with exactly `RP7_STOP reason=capture_stream_not_bindable
  label=leaf_race leaf=<...>`** (MSYS2 cannot re-open the descriptor of an
  unlinked leaf). The subshell is kept; both properties were always achievable
  together. `RP7_REPAIR_R7_REPORT.md` carries a correction notice and the false
  sentence is struck through in place. The `return 7` mutant is now an arm of
  both the round-6 and the round-8 fence, and the fence prints which assertion
  accepts which output (`ASSERTION_POWER round7_on_mutant=accept
  round8_on_mutant=reject`), so the claim is measured rather than asserted;
- **every capture read a row in this band attributes to its child is bound to the
  descriptor the capture created.** Round 7 bound one reader - the listener
  inventory - and left the rest of the class opening the leaf name. An executed
  fixture then replaced that name at the reader boundary and turned a
  child-observed HTTP 500 into an accepting `B5_status http=200`, and two unequal
  child-observed namespaces into `binding=equal`, both at rc 0. `wpi_capture` now
  binds **both** of its streams, and the row-20 status code, the row-21 parser
  result, both row-22 namespace identities and the emptiness of the diagnostic
  stream each of those is conditioned on are read through those descriptors.
  There is no fallback to a name: a capture that allocated no descriptor is
  `detail=capture_stream_unbound`, which is why several fixture stubs in the
  carried fences had to allocate what production allocates;
- **a production capture-bind inability now reaches the STOP the draft
  preregisters.** Round 7 made every bind failure a generic
  `RP7_STOP reason=capture_stream_not_bindable`, which no row declares; row 22's
  `B6_STOP ... detail=capture_stream_unbound` was reachable only from a stub. A
  caller with its own inability token now declares it immediately before its
  capture (`wpi_capture_bind_stop`), the declaration is consumed by exactly that
  capture and cleared, and a caller that declares nothing keeps the fail-closed
  generic STOP. Rows 20, 21 and 22 declare theirs; the executed arm shows the
  round-7 bytes emitting the generic token and these bytes emitting the exact
  preregistered one, with an undeclared caller still getting the generic;
- **the published evidence command attributes an rc of 137 instead of assuming
  it, and states only the bound it enforces.** Round 7 printed
  `kind=killed_after_grace` for every 137; `timeout ... bash -c 'exit 137'`
  finishes in a second and was labelled the same way. Each of the five wrappers
  now runs with `--verbose`, each fence's stderr is captured and echoed back
  unchanged, and a 137 is called this command's own kill-after event **only** when
  that wrapper recorded `sending signal KILL to command`. A 137 with no such
  record is `kind=sigkill_not_from_this_wrapper`, is not a timeout, and exits 1.
  The claim that `3720` was "an upper bound no execution of this command can
  exceed" is withdrawn rather than reworded: a FIFO in place of this document
  blocks the command in its own `sed` prelude, outside every wrapper. The result
  line now reads `fence_timeout_budget_s=4650 whole_command_bound=none
  prelude_bounded=no`. The reader arm's `adjudicated_name_sha256` field, which
  hashed the one thing the arm expressly does not adjudicate, is
  `name_at_read_time_sha256`.

**Two rules are in force from this round on.** A carried fence changes only with
a stated reason and a per-change discriminating-power argument - for every arm
touched, what input used to fail there and whether it still does. And no change
is justified by a claim about the old code without verifying it: the old
assertion is run against the new mutant and the new assertion against the old
mutant, inside the fence. Every carried-fence change below is listed under those
rules in `SELF_QA_RP7.md`.

Residuals are disclosed rather than claimed away, in `SELF_QA_RP7.md` under
*What this QA does not establish* and in the file header. The status-body leaf is
written by curl, which is handed a path and not a descriptor. Outside rows 20-24
- the rows 10-19 metadata, digest, enumeration, interpreter and verifier readers
- leaves are still opened by name, and **no preregistered row claims byte
identity for those**: what the block establishes about their content is exactly
what their record grammar establishes, which is why each STOPs on a record it
cannot represent byte for byte, NUL included, rather than adjudicating it. Those
rows were out of scope for this audit band; the mechanism to bind them now exists
and applying it is a matter of scope, not design, so it is named as the next
candidate rather than argued away. The read-diagnostic leaves are also
name-opened. One MSYS2 limitation is disclosed twice over: `/dev/fd/<n>`
*sometimes* still resolves for a leaf whose name has just been unlinked, so the
carried leaf-race arm accepts either documented outcome, and the round-8
bind-inability arm closes the creating descriptor instead of unlinking, because
an arm that reproduces its own precondition only sometimes is not a fence arm.

Local validation: literal Git Bash (MSYS2 bash 5.2.37, GNU coreutils 8.32,
CPython 3.14.2, git 2.52.0) - **five** fences, all extracted from
`SELF_QA_RP7.md` by the published anchored command and all `QA_PASS
all_assertions=yes` at rc 0 with empty stderr, in about 250 s:

- the round-8 fence (`dada2eaa...07f98`, 28633 B) drives every arm against the
  frozen round-7 blob `git cat-file blob c708511f:...` re-derived to 92853 B /
  `e695a67b...07f32` and against these bytes, with a real RED and a real GREEN for
  all four findings and a no-weakening control inside each finding's own group.
  Finding 1's RED is a `return 7` mutant of the block and its subject is the
  assertion, not the block; finding 4's arm runs the real `wpi_capture` and the
  real row adjudicator;
- the round-7 fence (`2a2eb893...327ff`, 22522 B) is carried and re-run as a
  regression gate, with four named changes: the two GREEN identity constants, the
  `adjudicated_name_sha256` -> `name_at_read_time_sha256` rename, both capture
  stubs allocating the stderr descriptor production now allocates, and its
  published-command GREEN pinned to the `c708511f` blob instead of the live
  document so the group stops re-adjudicating a moving subject;
- the round-6 fence (`0dc62137...d2fb1`, 32069 B) is carried with three round-8
  changes: the wrapper count 4 -> 5 with `--verbose` and a new assertion that the
  wrapper count equals the number of fence bodies the command extracts, the
  repaired F5 assertion plus its mutant RED, and the stderr descriptor in the
  stubs that feed a B5 or B6 assertion;
- the round-5 fence (`a3fb4b34...3fc56`, 20050 B) is carried unchanged except for
  its two GREEN identity constants, and its extracted body is byte-for-byte the
  same length because the substituted constants are the same length;
- the round-4 fence (`4ddfa8b5...c4cd1`, 77408 B) is carried unchanged except for
  its two anchor comments and the capture stubs that feed a B5 or B6 assertion,
  each of which gained the descriptor allocations production performs. No fixture
  byte, arm or assertion changed, and every round-3 and round-4 arm still passes
  on these bytes.

`bash -n` PASS. Zero CR bytes.

**DRAFT EDITS (three, all narrow, all forced by a repair).** Section 8.2 row 20
now names the read through the capture descriptor for the status code and its
diagnostic stream, and the `capture_stream_unbound` STOP; row 21 names the same
for the parser result record; row 22 names the same for both namespace identities
and adds `detail=<d>` to the `service_netns_unreadable` STOP so
`capture_stream_unbound` is declared there too. Row 22's listener half needed no
edit: it already declared `detail=capture_stream_unbound`, and finding 4 was
repaired by making the **block** reach the token the draft already preregisters,
not by moving the draft to the token the block happened to emit.

**FREEZE-GATE ITEMS (three, all carried deliberately, unchanged since round 5).**

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` is still `<PIN-AT-FREEZE>`, so
   there is no executed arm in which `wpi_validate_inputs` *accepts* a correct
   input set, and there cannot be one before freeze. The
   `normalised_path_projection_v2` digest the deploy channel must supply covers
   **21** point paths.
2. `WPI_FIXED_TRUSTED_PYTHON` is `<PIN-AT-FREEZE>`. `/usr/bin/python3` is a
   symlink on the target family and `wpi_bind_tool` admits no symlinked object,
   so the deploy channel must pin the resolved `/usr/bin/python3.<minor>`.
3. `WPI_FIXED_EVIDENCE_ROOT` is `<PIN-AT-FREEZE>`. Its value is
   `<REMOTE_BASE>/evidence`, and `REMOTE_BASE` is allocated at dispatch, so this
   pin carries an **ordering constraint Stage 1 must close**: the base must be
   allocated before the RO block is frozen and hashed. If Stage 1 cannot reorder
   that, the honest outcome is to record that the RO block does not claim
   evidence-root provenance for this run - not to fill the pin with anything the
   run learns about itself.

The first action after the deploy channel supplies all three values, and before
dispatch, is to execute the accepting-input arm and record it. The block cannot
be frozen on the strength of this QA alone.

Final executable identity:

```text
bytes=99903
sha256=11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the round-8 authorized deliverables occurred.
