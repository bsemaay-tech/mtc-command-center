# RP7 status

Status: **REPAIRED-R9-PENDING-INDEPENDENT-REAUDIT**

Scope: `RP7-WPI-RO.sh` implements remote RO-stage rows 10-23 and records row 24
as operator-side only. Repair round 9 was authorized under owner grant #7, which
lifts the T0 round cap for this block set until both flagships accept. It answers
the Codex T0 part-B re-audit of the round-8 bytes
(`RP7_CODEX_T0_AUDIT_R8_PART_B_2026-08-11.md`, BLOCK on five findings, one of
them BLOCK/HIGH). Codex is the auditor of record and re-audits these bytes, so
implementer/auditor separation holds. Round 8's code repairs were confirmed by
that audit - the descriptor binding for the status-code, parser-result, namespace
and listener capture streams, the restored two-outcome assertion that rejects the
`return 7` mutant, and a published command that really extracts and runs the
files it names - and were built on, not re-litigated.

**The headline finding is a residual that came due, and the sentence it teaches
is the one this round is built around: an accurate disclosure is not a safety
control.** Round 6 found that `ro.status.body` was create-once allocated and then
handed to curl, to the digest and to the parser by NAME; it called closing that
"a design change to the row-20 probe, not a repair" and wrote the residual down.
Round 8 restated the note. Codex then executed both halves of what the note
admitted: a hard link at that name made curl overwrite an object **outside the
evidence tree** at capture rc 0, and a replacement of that name between the digest
and the parser turned a child-produced ARMED body into an accepting DISARMED
result whose line carried the ARMED body's digest. The note was true and the
block's own unqualified sentences - `No host object outside that tree is changed`,
`rows_10_23_read_only_predicates` - were false beside it, inside rows 20-21 where
the rows 10-19 scope boundary does not reach. Round 9 makes the design change.

Material repair state added this round:

- **the status body is no longer addressed by name, on either side.** The leaf is
  opened by `wpi_open_leaf`, which keeps the descriptor its `O_CREAT|O_EXCL` open
  returned. That descriptor is duplicated into the capture child at fd 3 and curl
  is given `--output /dev/fd/3`, a path that resolves through this process's
  descriptor table rather than through the evidence directory - so the object curl
  truncates and fills is the object the create-once open created, whatever the
  leaf name resolves to by then, and curl is handed no evidence-tree name at all.
  The matching read descriptor is derived from that same open **at creation time**,
  before the child exists, so there is no window on the read side either. The
  parser is given no path: its stdin is that descriptor. It digests exactly the
  bytes it parses and reports that digest, which the parent grammar-checks and
  renders as `body_sha256`, so the field cannot disagree with the verdict beside
  it; `wpi_sha_file` over the body - a second read, of a name - is gone. There is
  now exactly one reader and one writer of that object and they are the same
  object. `wpi_alloc_leaf`, the name-only allocator whose last caller this was, is
  **deleted** rather than left available: there is no longer any way in this block
  to create a leaf and then address it by name;
- **a descriptor-bind STOP reports the status the child returned, not a caller's
  literal.** Round 8 let every caller write `rc=0` into its own declared reason and
  `wpi_capture` emitted that literal whatever the child had returned; an executed
  fixture ran a child that exited 7 and the block still printed `rc=0`. The rc
  field is no longer part of the declared reason: the caller declares the reason
  and whether its row's grammar carries an rc field at all - rows 20 and 22 declare
  `rc=<n>`, row 21 declares none - and `wpi_capture` fills it from the measured
  status, adjudicated before any caller-specific token is emitted;
- **both nonzero namespace-read branches emit the `detail` field row 22 declares.**
  Draft row 22 declares `B6_STOP reason=service_netns_unreadable
  path=/proc/<pid>/ns/net rc=<n> detail=<d>`; the capture-bind, record, grammar and
  read-diagnostic branches carried one and the two immediate nonzero `readlink`
  branches did not. The **block** was the wrong side - a child that could not read
  the link is an inability with a name, and the diagnostic leaf that names it is
  already captured - so both branches now emit
  `detail=identity_read_child_failed diagnostic_file=<leaf>`;
- **the published command attributes rc 137 on a stream the bounded body cannot
  write.** Round 8's `timeout --verbose` and the body it bounds wrote to the same
  stderr file, so a body that printed `timeout: sending signal KILL to command` and
  exited 137 was called this wrapper's kill-after event. Each wrapper's own stderr
  now goes into an **unnamed pipe** read straight into a shell variable, while an
  `sh -c` shim redirects the body's stderr to its own named file before it execs
  the body. The body has no descriptor and no name for the wrapper's stream.
  `killed_after_grace` requires that variable to hold the KILL record; both streams
  are still echoed back, so separating them hides nothing;
- **the carried wrapper/body assertion checks the mapping instead of two counts.**
  Round 8 asserted `count(wrappers) == count(extractions)` and called it strictly
  stronger. It is not: a command with six wrappers and six extractions can run one
  body twice and another never. The replacement requires, per fence, exactly one
  extraction of that fence's own body path, exactly one wrapper whose `sh -c`
  operand is that path and whose body-stderr operand and rc variable are that
  fence's own, exactly one occurrence of that path across all wrapper lines, and
  exactly one classifier call binding that fence's rc to its own wrapper stream.
  The auditor's exact omit-R8/duplicate-R7 mutant is now a RED arm.

**The two rules from round 8 stay in force, and this round adds a third.** A
carried fence changes only with a stated reason and a per-change
discriminating-power argument. No change is justified by a claim about the old
code without verifying it. And: **a disclosure is not a control** - writing down
that something is unbound does not bind it, and a truthful note beside an
unqualified claim leaves the unqualified claim false. All eleven carried-arm
changes this round are tabled in `SELF_QA_RP7.md` under those rules.

Residuals are disclosed rather than claimed away, in `SELF_QA_RP7.md` under
*What this QA does not establish* and in the file header. Outside rows 20-24 - the
rows 10-19 metadata, digest, enumeration, interpreter and verifier readers - leaves
are still opened by name, and **no preregistered row claims byte identity for
those**: what the block establishes about their content is exactly what their
record grammar establishes, which is why each STOPs on a record it cannot
represent byte for byte, NUL included, rather than adjudicating it. Those rows were
out of scope for this audit band; the mechanism to bind them now exists and
applying it is a matter of scope, not design, so it is named as the next candidate
rather than argued away. The read-diagnostic leaves are also name-opened. Two MSYS2
limitations are disclosed: `/dev/fd/<n>` *sometimes* still resolves for a leaf whose
name has just been unlinked, so the carried leaf-race arm accepts either documented
outcome; and MSYS2 resolves `/dev/fd/<n>` through the path where Linux resolves it
through the descriptor table, so the F1 outside-write arm's GREEN disposition here
is a fail-closed `rc=23 detail=transport_error` rather than the Linux `rc=0`
completion. Both establish what the row needs - no object outside the tree is
written and no accepting line is produced over substituted bytes - and the arm
asserts the one this workstation reproduces.

Local validation: literal Git Bash (MSYS2 bash 5.2.37, GNU coreutils 8.32,
CPython 3.14.2, git 2.52.0) - **six** fences, all extracted from `SELF_QA_RP7.md`
by the published anchored command and all `QA_PASS all_assertions=yes`:

- the round-9 fence drives every arm against the frozen round-8 blob
  `git cat-file blob bb8546e6:...` re-derived to 99903 B /
  `11621044...141a4` and against these bytes, with a real RED and a real GREEN for
  each of the five findings and a no-weakening control inside each finding's own
  group. Findings 1, 2 and 5 run the real production callers with a real child;
  finding 3's subjects are the published command TEXT at `bb8546e6` and here;
  finding 4's replacement assertion and its executed mutant live in the round-6
  fence that carries the assertion, and this fence asserts the replacement is
  present and the round-8 form is gone;
- the round-8 fence is carried with two changes: the subject-specific accepting
  parser record, and a rebuilt F4 injection - the round-8 injection closed the
  creating descriptor **before** the child's redirection, so the child it claimed
  to test never ran (this round's finding 2). The rebuilt arm diverts the stdout
  leaf's descriptor to a pipe, which fails the post-child bind deterministically,
  and asserts `child_ran=yes` and `escaped_stderr_bytes=0`;
- the round-7 fence is carried with the same subject-specific accepting record and
  its GREEN identity constants;
- the round-6 fence is carried with the replaced mapping assertion and its mutant,
  the split accepting-record arm plus two added arms that make the split honest
  (GREEN must reject the round-8 record and a malformed digest), and the child
  descriptor binding in its forge stub;
- the round-5 fence is carried with `wpi_alloc_leaf` retargeted to `wpi_open_leaf`
  - the same create-once test, the same two reason tokens, the same zero-byte
  diagnostic streams - and the child descriptor binding in its forge stub;
- the round-4 fence is carried with the child descriptor binding in its forge stub
  and one assertion pattern anchored at end of line, because the row-21
  parser-failure STOP no longer carries a `body_sha256` field. No fixture byte,
  arm or expected disposition changed.

`bash -n` PASS. Zero CR bytes.

**DRAFT EDITS: NONE REQUIRED, AND NONE MADE.** The concurrent preregistration lane
owns `WPI_PREREGISTRATION_DRAFT.md` and this round's scope fence excludes it. No
draft edit is forced by any of the five findings: rows 20 and 22 declare `rc=<n>`,
so the measured rc conforms; row 21 declares no rc field, so the row-21 bind STOP
conforms; `detail=<d>` is free-form, so `identity_read_child_failed` conforms; and
the row-21 accepting line is emitted with the exact field list the draft declares -
no field was added to it. The three round-8 draft edits recorded in the previous
status remain in place and are unaffected.

**One design option is recorded for the prereg lane rather than taken.** Writing
the response body to the capture's own stdout descriptor (`curl --output -`) would
need no `/dev/fd` path at all and is the stronger binding. It requires moving the
HTTP status code onto stderr via `--write-out '%{stderr}%{http_code}'`, and draft
row 20 declares that the status code is conditioned on **the emptiness of the
diagnostic stream** - so it needs a draft edit this lane may not make. It is noted
in `RP7_REPAIR_R9_REPORT.md` for whoever owns that decision.

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
bytes=108301
sha256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the round-9 authorized deliverables occurred.
