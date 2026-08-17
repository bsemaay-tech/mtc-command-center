# RP7-WPI-RO repair round 9 — report

Implementer: Claude Opus 5 (Max), local Git Bash (MSYS2) session, 2026-08-11.
Auditor of record: Codex `gpt-5.6-sol`. Authority: owner grant #7.
Binding scope: `RP7_CODEX_T0_AUDIT_R8_PART_B_2026-08-11.md` — **BLOCK: 5**.

No host contact, no network connection, no SSH/SCP, no RUNID, no service, no credential,
no deployment, no trading action, no Git mutation, **no commit**. Fixture writes were
confined to `mktemp` directories under `/tmp` whose prefix was checked before recursive
removal. Files changed: `RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, and this report.

## Subject identity

| | SHA-256 | Bytes | CR bytes | `bash -n` |
|---|---|---|---|---|
| Round-8 input (`bb8546e6`) | `11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4` | 99903 | 0 | rc 0 |
| Round-9 output (worktree) | `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62` | `108301` | 0 | rc 0 |

Re-derivation commands and their real output are in `SELF_QA_RP7.md` (`BYTE_IDENTITY` line
of every fence) and in the round-9 transcript.

## Disposition of every finding

| # | Severity | Disposition |
|---|---|---|
| 1 | BLOCK/HIGH | **Repaired.** Design change, as the auditor required. |
| 2 | HIGH | **Repaired**, in the block and in the round-8 fence arm that mis-demonstrated it. |
| 3 | MEDIUM | **Repaired.** The wrapper stream is now unwritable by the bounded body. |
| 4 | MEDIUM | **Repaired.** Exact per-fence mapping; the auditor's exact mutant is the RED. |
| 5 | MEDIUM | **Repaired on the block side.** The block was wrong, not the draft. |

Nothing is left unrepaired. Two items are carried forward as **stated limitations, not
repairs**, and both are named below and in the QA.

---

### F1 (BLOCK/HIGH) — `ro.status.body` as an outside-tree write primitive and a false-PASS primitive

**What the auditor established.** `wpi_alloc_leaf` proved only that the name was absent when
an empty leaf was created. Curl then received the *name* through `--output "$body"`, and
`wpi_sha_file` and the parser received the name again. Nothing bound the object curl wrote,
the object the parser opened, and the created leaf to each other. Two executed arms: a hard
link at that name made curl overwrite a file outside the evidence tree at capture rc 0, and
a replacement of the name after the digest turned a child-produced ARMED body into an
accepting DISARMED result whose line carried the ARMED body's digest.

**The point absorbed.** An accurate disclosure is not a safety control. `SELF_QA_RP7.md`
said this truthfully and the block's own unqualified sentences — `No host object outside
that tree is changed` and `rows_10_23_read_only_predicates` — were false beside it, inside
rows 20–21, where the rows 10–19 scope boundary does not reach. Round 6 called closing it "a
design change to the row-20 probe, not a repair"; that description was right, and round 9
makes the design change.

**The repair.** `wpi_assert_status` now derives BOTH ends of the body from one create-once
open, before the child exists:

- the leaf is opened by `wpi_open_leaf`, which keeps the descriptor its `O_CREAT|O_EXCL`
  open returned;
- `wpi_capture_bind_child "$bodyfd" w3` duplicates that descriptor into the capture child at
  fd 3, and curl is given `--output /dev/fd/3`. That path resolves through this process's
  descriptor table rather than through the evidence directory, so the object curl truncates
  and fills is the object the create-once open created — whatever the leaf name resolves to
  by then. Curl is handed no evidence-tree name at all;
- the read descriptor is derived from that same creating descriptor **at creation time**
  (`exec {pfd}</dev/fd/"$bodyfd"`), before the child runs, so there is no window in which a
  name could be resolved on the read side either;
- the parser is given **no path**. Its stdin is `pfd`. It cannot be pointed at another
  object;
- the parser digests exactly the bytes it parses and reports that digest
  (`OK fields=8 sha256=<h>`), which the parent grammar-checks and renders as `body_sha256`.
  `wpi_sha_file` over the body — a second read, of a name — is gone. There is now exactly
  one reader and one writer of the body and they are the same object, so the digest cannot
  disagree with the verdict beside it;
- `wpi_alloc_leaf`, the name-only allocator whose last caller this was, is **deleted** rather
  than left available.

`B5_status ... body_sha256=<h> ...` keeps the exact field list draft row 21 declares — no
field was added or removed from that line. The row-21 parser-failure STOP loses its
`body_sha256=` field, and that is deliberate: the only digest this block now has is the one
the parser reports for bytes it accepted, so a result the parser did not accept has no
adjudicated bytes to digest. Round 8 printed a number there about an object it had
established nothing about.

**RED/GREEN** (round-9 fence, `BODY_BINDING` lines; RED = round-8 blob at `bb8546e6`):

| Arm | RED | GREEN |
|---|---|---|
| outside-tree write | `outside_bytes=197 outside_is_original=no`, rc 0, `B5_status ... flags=expected` | `outside_bytes=9 outside_is_original=yes`, rc 3, `B5_STOP reason=status_endpoint_not_evaluable rc=23 detail=transport_error` |
| ARMED→DISARMED | rc 0 `B5_status ... body_sha256=378c48e9…` while `child_body_sha256=d03ba34a…` | rc 1 `B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a96…` |
| no-weakening: clean DISARMED, no substitution | rc 0 accepting `body_sha256=378c48e9…` | identical |
| no-weakening: ARMED, no substitution | rc 1 `flag_mismatch field=state` | identical |

The child body digest `d03ba34a30627a3990cb326fe9187ae0ff02e838be06c572ab6c00470e95dbb3` and
the substituted digest `378c48e98a2adb8de54c192c70253a2175bff6c4b29d6f04a3a961ae7ae24821`
are the auditor's own values, reproduced.

**Stated limitation, not a repair.** On Linux `/dev/fd/<n>` resolves through the process's
descriptor table — that is the binding this repair rests on. MSYS2 resolves it through the
path, so once the name has been replaced the open fails and GREEN's outside arm STOPs at
`rc=23 detail=transport_error` rather than completing at rc 0 as it would on the target.
Both dispositions establish what the row needs — no object outside the evidence tree is
written, and no accepting line is produced over substituted bytes — and the arm asserts the
one this workstation reproduces. The read side has no such dependency: its descriptor is
derived at creation time and is a real descriptor on both platforms, which is why the reader
arm produces the truthful `B5_FAIL` here rather than a STOP.

**Why not `--output -`.** Writing the body to the capture's own stdout descriptor would need
no `/dev/fd` at all, and was considered. It requires moving the HTTP status code onto stderr
via `--write-out '%{stderr}%{http_code}'`, and draft row 20 declares that the status code is
conditioned on **the emptiness of the diagnostic stream**. That alternative therefore needs a
draft edit, and this lane is fenced out of the draft. It is recorded here as the stronger
option should the prereg lane want it.

---

### F2 (HIGH) — the row-22 bind-inability fence and the false `rc 0`

**Block side.** `wpi_capture_bind_stop` took the whole reason token as a caller literal, and
every caller wrote `rc=0` into it. `wpi_capture` emitted that literal whatever the child had
returned. The rc field is no longer part of the declared reason: the caller declares the
reason and whether its row's grammar carries an rc field (`with_rc` / `no_rc` — row 20 and
row 22 declare `rc=<n>`, row 21 declares no rc), and `wpi_capture` fills the field from the
status the child really returned, adjudicated before any caller-specific token is emitted.

**Fence side.** The round-8 arm's hook closed the creating write descriptor at
`wpi_clock_ms` call 1, which happens *before* the child subshell's stdout redirection. Bash
could not establish the redirection, the child never ran, its failure was discarded, and a
raw shell diagnostic escaped. That arm was not closure evidence and has been rebuilt on a
new injection in **both** the round-9 fence and the round-8 fence: the stdout capture leaf
is created by the real allocator and its descriptor is then replaced with the write end of a
pipe that drains into that same leaf. `/dev/fd/<n>` of a pipe cannot be re-opened on Linux
or MSYS2, so the post-child bind fails deterministically while the child runs to completion
through the descriptor it inherits.

**RED/GREEN** (`BIND_RC` lines):

| Arm | RED | GREEN |
|---|---|---|
| bind fails after a child that exited 7 | `rc=0 detail=capture_stream_unbound` — false | `rc=7 detail=capture_stream_unbound` — measured |
| no-weakening: bind fails after a child that exited 0 | `rc=0 …` | identical |
| no-weakening: caller with no declared token | generic `RP7_STOP … label=undeclared_probe` | identical |
| no-weakening: nothing diverted, clean inventory | `B6_listener_inventory … B6_listener_set port=8790 count=1` | identical |

Every arm asserts `child_ran=yes` (a marker the child writes) and
`escaped_stderr_bytes=0` (no unstructured line escapes), which is what the round-8 arm could
not claim.

**Draft conformance:** draft row 22 declares `rc=<n>`, so the measured rc conforms. No draft
edit is needed for this finding.

---

### F3 (MEDIUM) — a fence body could forge the wrapper-owned rc-137 diagnostic

Round 8's `timeout --verbose` wrote to the same stderr file as the body it bounded, so a
body printing `timeout: sending signal KILL to command` and exiting 137 was called this
wrapper's kill-after event. The two writers are now separated, and the wrapper's stream is
given **no name**:

```
<FENCE>_W=$(timeout --verbose … sh -c 'exec 2>"$1"; exec bash --noprofile --norc "$0"' <body> <body-err> 2>&1 1>&3)
```

The wrapper's stderr is an unnamed pipe read straight into a shell variable. The `sh -c`
shim redirects the body's stderr to its own named file *before* it execs the body, so the
body has fd 1 (the command's stdout, restored through fd 3), fd 2 (its own file), and
neither a descriptor nor a name for the wrapper's stream. `killed_after_grace` now requires
that variable to hold `sending signal KILL to command`. Both streams are still echoed to
stderr — the body's by `cat`, the wrapper's by `WRAPPER_STREAM` lines — so separating them
hides nothing.

**RED/GREEN** (`RC137_PROVENANCE` lines; RED = the round-8 published command text at
`bb8546e6`):

| Arm | RED | GREEN |
|---|---|---|
| **child_spoof** — body prints the wrapper's phrase, exits 137 | `timeout … kind=killed_after_grace`, command exits 137 | `fence_failed … kind=sigkill_not_from_this_wrapper wrapper_stream=body_cannot_write`, exits 1 |
| carried: bare `exit 137` | `sigkill_not_from_this_wrapper`, exit 1 | identical |
| carried: TERM-ignoring body | `killed_after_grace`, exit 137 | identical |

**Claim boundary, stated not narrowed away.** The claim is that the body cannot write *this*
stream, which holds because the stream has no name. A body that is killed by something else
*while* the wrapper is also killing it is still reported as a kill-after event; that residual
is unchanged from round 8 and is stated in the QA.

---

### F4 (MEDIUM) — a changed carried assertion accepted a command that never runs the round-8 body

`expect_rc f4_every_body_wrapped "$BOUNDS" "$BODIES"` proved only that two counts were equal.
It is replaced by `map_check`, which for each fence requires **exactly one** extraction line
writing that fence's own body path, **exactly one** wrapper line whose `sh -c` operand is
that same body path and whose body-stderr operand and rc variable are that fence's own,
**exactly one** occurrence of that body path across all wrapper lines, and **exactly one**
classifier call binding that fence's rc variable to its own wrapper stream. Totals are then
required equal to the table size, so the case the old count check existed for — a fence added
without a wrapper — still fails.

The auditor's exact mutant (R8 wrapper operand retargeted at the R7 body) is now a RED arm in
the round-6 fence that carries the assertion, and the fence prints the comparison rather than
asserting it:

```
MAPPING_ASSERTION_POWER round8_on_green=accept round8_on_mutant=accept round9_on_green=accept round9_on_mutant=reject
PUBLISHED_MAP text=mutant fence=r8 extractions=1 wrappers=0 wrapper_operand_occurrences=0 classifier_calls=1
PUBLISHED_MAP text=mutant fence=r7 extractions=1 wrappers=1 wrapper_operand_occurrences=2 classifier_calls=1
```

---

### F5 (MEDIUM) — draft row 22 requires `detail=<d>` on namespace-read failure

**The block was the wrong side, and the draft is right.** Draft row 22 declares
`B6_STOP reason=service_netns_unreadable path=/proc/<pid>/ns/net rc=<n> detail=<d>`; the
capture-bind, record, grammar and read-diagnostic branches all carried a detail and the two
immediate nonzero `readlink` branches did not. A child that could not read the link is an
inability with a name, and the diagnostic leaf that names it is already captured, so the
missing field was an omission rather than a case the draft over-declared. Both branches now
emit `detail=identity_read_child_failed diagnostic_file=<leaf>`.

**RED/GREEN** (`NETNS_DETAIL` lines): RED emits `… rc=7` with `detail_field_present=0` on
both the caller path and the service path; GREEN emits the same line with the detail and
`detail_field_present=1`. The no-weakening control — two equal namespaces — reaches the
identical `B6_netns … binding=equal` on both subjects.

**This lane did not touch the preregistration draft.** The concurrent prereg lane owns it and
the scope fence for this round excludes it. No draft edit is required by any of the five
findings: rows 20 and 22 declare `rc=<n>` (so the measured rc conforms), row 21 declares no
rc field (so the row-21 bind STOP conforms), `detail=<d>` is free-form, and the row-21
accepting line is emitted with its declared field list unchanged.

---

## Design-defect pattern check

`DESIGN_DEFECT_PATTERNS_2026-08-10.md`, thirteen patterns, checked against the repaired
bytes:

- **Pattern 11 — the declared instrument is not the executed instrument**, applied to an
  *object*: F1. The leaf that was created was not the leaf that was written and read. Closed
  by making one descriptor the source of the write handle and both read handles.
- **Pattern 10 — evidence that cannot fail**: F2's round-8 arm (the child never ran) and F4's
  count equality. Both replaced by arms/assertions that were shown to reject a mutant.
- **Pattern 6 — a claim printed beside a fact that does not support it**: F2's `rc=0` literal,
  F3's forged provenance, F5's missing declared field.
- The remaining ten patterns were checked and produced no new finding in the changed bytes.

## What was executed

- Round-9 fence: 5 arm groups, RED = round-8 blob at `bb8546e6`, GREEN = worktree. `QA_PASS`.
- Carried round-8, round-7, round-6, round-5 and round-4 fences: all re-run against the
  round-9 bytes after the eleven carried-arm changes tabled in `SELF_QA_RP7.md`. All
  `QA_PASS`.
- The published command, verbatim, end to end, **four times**. Run one produced the six
  transcripts in `SELF_QA_RP7.md`; runs two and three followed successive prose edits; run
  four was executed against the two executable deliverables exactly as delivered. The wall
  clock and byte counts of every run after the first are recorded HERE and not in
  `SELF_QA_RP7.md`, because a run pinned inside the file it reads is not a fixed point —
  pinning it would require editing the file after the run it describes. Editing this report
  changes nothing the command reads.

| Run | rc | wall s | stdout B | stderr B | `QA_PASS` | fence-body digests |
|---|---|---|---|---|---|---|
| one — produced the transcripts | 0 | 229 | 66458 | 210 | 6 | pinned in `SELF_QA_RP7.md` |
| two — after transcripts pasted | 0 | 234 | 66458 | 210 | 6 | identical to run one |
| three — after prose rewrite | 0 | 236 | 66458 | 210 | 6 | identical to run one |
| four — **the delivered files** | 0 | 239 | 66458 | 210 | 6 | identical to run one |

Every prose and transcript edit between those runs lies outside every `# RP7_*_FENCE_BEGIN` /
`_END` range, which is why all six fence-body digests and byte counts are identical across
all four runs. Run four's result line, verbatim:

```text
PUBLISHED_COMMAND_RESULT=pass fences=6 per_fence_bound_s=900 kill_grace_s=30 fence_timeout_budget_s=5580 whole_command_bound=none prelude_bounded=no wrapper_stream=unnamed_pipe_body_cannot_write
```

The 210 stderr bytes are the six `WRAPPER_STREAM fence=<f> bytes=0 []` lines the round-9
command prints, one per fence — the wrapper stream finding 3 moved onto a channel the bounded
body cannot write, echoed back so that separating it hides nothing. No unstructured
diagnostic escapes. One did before carried-arm change 11: with `wpi_alloc_leaf` deleted from
the block, the frozen round-3 RED bodies in the round-4 fence leaked seven
`wpi_alloc_leaf: command not found` lines and skipped the allocation they were supposed to
perform, while the fence still passed. That is exactly the class of defect this audit series
exists to catch, it was found by running the published command rather than by reading it,
and it is repaired rather than tolerated.

`bash -n` rc 0; zero CR bytes (`tr -cd '\r' < file | wc -c` = 0) for all four deliverables.

## Known freeze-gate items, unchanged and not findings

`WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`, `WPI_FIXED_TRUSTED_PYTHON` and
`WPI_FIXED_EVIDENCE_ROOT` remain `<PIN-AT-FREEZE>`, so no accepting `wpi_validate_inputs` arm
exists or can exist before freeze. Section 8.2 rows 1–9 remain implemented by no block and
remain a separate owner decision. Row 24 remains operator-side.

Do not commit on this report alone — the Lead verifies and commits.
