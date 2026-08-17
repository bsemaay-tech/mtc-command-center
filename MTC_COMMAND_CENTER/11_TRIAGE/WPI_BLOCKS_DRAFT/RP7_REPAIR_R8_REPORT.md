# RP7-WPI-RO repair round 8 - report

Implementer: Claude Opus 5, effort xhigh, authorised under owner grant #7.
Auditor of record: Codex, who re-audits these bytes; separation holds.
No host contact, network connection, SSH/SCP, RUNID minting, service, credential,
deployment, trading or commit action occurred. The Lead verifies and commits.

## Disposition of every finding

| Finding | Severity | Disposition |
|---|---|---|
| 1. The changed carried-fence leaf-race assertion accepts an unrelated capture regression | HIGH | **REPAIRED, and the false justification corrected.** Exact two-outcome status pin restored, subshell kept, `return 7` mutant added as a RED arm in two fences, and both assertions executed against the same three outputs |
| 2. Status and namespace child observations can still be replaced by name | HIGH | **REPAIRED.** Both capture streams are descriptor-bound; the row-20 status code, row-21 parser result, both row-22 namespace records and the diagnostic-stream emptiness each is conditioned on are read through them, with no fallback to a name |
| 3. The evidence command overclaims rc-137 provenance and a whole-command aggregate; one reader-arm field is mislabeled | MEDIUM | **REPAIRED, all three parts.** Wrappers instrumented with `--verbose` so a 137 is attributed from the wrapper's own diagnostic; the enforcement claim withdrawn and replaced with what is enforced; the field renamed |
| 4. The production listener bind-inability branch cannot emit its declared STOP | MEDIUM | **REPAIRED by making the branch reachable**, not by editing the draft to match the block. The draft edits this round are for rows 20-21-22's namespace half, which are consequences of finding 2 |

Nothing was dismissed, deferred or renegotiated. Two scope decisions are recorded
as such below and both are also in the delivered document: readers outside rows
20-24 are not descriptor-bound, and no outer wrapper was added to the published
command.

## Subject identity

| Subject | Bytes | SHA-256 | CR | `bash -n` |
|---|---|---|---|---|
| Predecessor (round 7, commit `c708511f`) | 92853 | `e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32` | 0 | rc 0 |
| **Round 8 (delivered)** | **99903** | **`11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4`** | **0** | **rc 0** |

Both identities are re-derived inside the round-8 fence before any arm runs, and
the predecessor is materialised only with `git cat-file blob`, never checked out.

Other delivered files:

| File | Bytes | SHA-256 |
|---|---|---|
| `SELF_QA_RP7.md` | 295829 | `d46d7c9c73a1fb62b55fdf57fc1f31e7bfd50c76f7df219b0e380ff457a70d35` |
| `WPI_PREREGISTRATION_DRAFT.md` (3 rows edited) | 117270 | `808f4ca9cc8d4caf034044a5520695b05414d3d33f09fa8b0216eb671ca6aa32` |
| `RP7_REPAIR_R7_REPORT.md` (correction appended) | 19024 | `e4dac0c508dbad931bab75a6b11274e46ece3409eb9ba8ded0d70b07afdbaca0` |

`SELF_QA_RP7.md` is quoted as it stood when this report was written; pasting the
final published-command transcript is the last edit to it and does not touch any
fence marker range, so the five fence-body digests below are unaffected.

## Finding 1 - the assertion that stopped discriminating

**What round 7 did.** The round-6 fence's F5 leaf-race arm hooks `wpi_clock_ms` to
unlink the freshly allocated capture leaf and hard-link a file from outside the
evidence tree in its place. Its GREEN assertion was

```text
LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no
```

Round 7 moved the capture into a subshell, because the round-7 read binding makes
the repaired block additionally STOP on MSYS2 and an arm that dies on its own STOP
cannot report the outside file. That part was necessary. In the same edit the
assertion became

```text
LEAF_RACE rc=[0-9]* outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no
```

which accepts any decimal status, and an empty one.

**Why that matters more than the regex.** `RP7_REPAIR_R7_REPORT.md:209` justified
the change by saying the rc was "no longer pinned in an assertion that never
measured it." **That statement is false.** The arm prints `LEAF_RACE rc=%s ...`
and the predecessor `grep` matched the literal `rc=0`, which pins the field to
zero. The report described a control it was removing as a control that had never
existed. A repair justified by an inaccurate claim about the thing it replaces is
the most dangerous change in this process, because it removes protection while
reading as diligence: a reviewer who trusts the justification has no reason to
look at the arm, and the arm is where the loss is.

Two further things are worth stating plainly, because they are what makes this a
process failure rather than a typo. First, the two properties were never in
tension - a subshell and an exact status pin are independent, and keeping both
required no more work than dropping one. Second, the same actor repaired the code
and maintained the tests, so nothing in the round stood between "this assertion
is inconvenient right now" and "this assertion is weaker forever."

**The repair.** The assertion accepts exactly two outcomes and nothing else:

- `rc=0` **and an empty capture result** - the `/dev/fd/<n>` re-open through the
  still-open creating descriptor succeeded although the leaf name was unlinked,
  which is what Linux does; or
- `rc=3` **and exactly** `RP7_STOP reason=capture_stream_not_bindable
  label=leaf_race leaf=<scratch>/ev/ro.0001.leaf_race.stdout` - MSYS2 cannot
  re-open the descriptor of an unlinked leaf, so the capture STOPs before it
  returns.

Anything else, including an empty status or either status carrying unexpected
output, classifies as `unclassified` and fails the fence. The subshell stays.

**The verification the original claim never had.** The `return 7` mutation is now
an arm of the round-6 fence and of the round-8 fence, and both fences run the
round-7 assertion and the round-8 assertion over the same three outputs:

```text
escaping_round5  LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes capture_result=[]
green            LEAF_RACE rc=3 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[RP7_STOP reason=capture_stream_not_bindable label=leaf_race leaf=<scratch>/ev/ro.0001.leaf_race.stdout]
mutant_return7   LEAF_RACE rc=7 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no capture_result=[]
ASSERTION_POWER mutant_bash_n=0 round7_on_green=accept round7_on_mutant=accept round7_on_escaping=reject round8_on_green=accept round8_on_mutant=reject round8_on_escaping=reject green_kind=unlinked_leaf_not_rebindable_rc3
```

`round7_on_mutant=accept round8_on_mutant=reject` is the finding, executed.
`round7_on_escaping=reject round8_on_escaping=reject` is the control that the
repair did not trade one blind spot for another: the round-5 block, whose payload
really does leave the evidence tree, still fails both assertions. Look at the
mutant's line: `outside_text=ORIGINAL`, `payload_left_the_tree=no` - everything
the arm watches is unchanged, and only the status gives the regression away. That
is precisely why an assertion that does not pin the status cannot see it.

`RP7_REPAIR_R7_REPORT.md` now carries a correction notice at the top and the false
sentence is struck through in place with the correction beside it.

## Finding 2 - binding one reader of a class does not close the class

Round 7 bound the row-22 listener inventory to the descriptor `wpi_capture`
re-derives from its own creating write descriptor, and left the shared
single-record reader executing `exec {fd}<"$file"` - a second name resolution
after the child has exited. The auditor drove the real `wpi_single_record` and the
real row adjudicators, hooked only the `wpi_alloc_read_diag` boundary, and showed
a child-observed `500` adjudicated as an accepting `200` and two unequal
child-observed namespaces adjudicated as `binding=equal`, both at rc 0.

**The repair, in the block:**

- `wpi_capture` binds **both** streams. Round 7 bound stdout only; the five
  in-band results are each conditioned on "the child emitted no diagnostics", and
  that is as much a child observation as the record itself - establishing it by
  re-opening the stderr leaf name establishes only that whatever the name resolved
  to at read time was empty.
- The record grammar moved into `wpi_read_record_from`, which takes an already-open
  descriptor. `wpi_single_record` resolves a name and passes what it got;
  `wpi_captured_record` passes the capture's own descriptor. One grammar, two
  bindings, so the two cannot drift apart.
- `wpi_require_empty_captured` establishes stream emptiness over the descriptor.
  `read -d ''` returns 0 only when it found a NUL, so a stream holding a single
  NUL byte is nonempty even though the string it produces is empty; both cases
  STOP.
- A capture descriptor is **consumed**: it is closed and cleared after one read,
  so a second read of the same stream is `detail=capture_stream_unbound` rather
  than a silent EOF a caller could mistake for an empty record.
- `wpi_assert_status` (rows 20-21) and `wpi_assert_netns_binding` (row 22) use the
  captured variants for all four record reads and all four emptiness checks. The
  listener reader already consumed `WPI_CAP_OUT_FD` and is unchanged apart from
  its stderr check.

**Executed RED/GREEN**, with the auditor's own fixture and hook point:

```text
NAME_REOPEN mode=status swap=yes subject=red   rc=0 result=[B5_status http=200 json=strict required_fields=8 flags=expected ...]
NAME_REOPEN mode=status swap=yes subject=green rc=1 result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
NAME_REOPEN mode=netns  swap=yes subject=red   rc=0 result=[B6_netns caller=net:[100] service=net:[100] mainpid=123 binding=equal]
NAME_REOPEN mode=netns  swap=yes subject=green rc=3 result=[B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]]
READER_SUBSTITUTION red_child_ne_name=yes green_child_ne_name=yes
```

`swap=no` on both subjects and both modes is the control; `CLEAN_CONTROL` shows a
clean `200` + `OK fields=8` and a clean equal namespace pair still accepting at
rc 0 on both subjects; and `NO_NAME_FALLBACK` feeds a stub that allocates no
descriptor at all, which GREEN refuses with the row's own token
(`B5_STOP ... detail=capture_stream_unbound`) rather than falling back to a name.

**Scope decision, stated rather than implied.** Readers outside rows 20-24 -
`wpi_lstat`, `wpi_sha_file`, `wpi_assert_manager_ready`,
`wpi_assert_evidence_leaf_bound`, the two `find`-stdout walkers, the interpreter
`-V` record, the verifier streams - still open by name, as do the read-diagnostic
leaves. Rows 10-19 were out of scope for this audit band and no row among them
states captured identity for its bytes; what the block establishes about their
content is exactly what their record grammar establishes. The mechanism to bind
them now exists and applying it is a matter of scope, not design, so it is named
in `SELF_QA_RP7.md` as the next candidate rather than argued away.

## Finding 3 - attribute the status, state the bound that exists

**Rc 137.** The classifier saw a number. `timeout ... bash -c 'exit 137'` returns
137 in about a second and was printed as `kind=killed_after_grace`. Each of the
five wrappers now runs with `--verbose`, which makes GNU `timeout` announce the
signals it sends; each fence's stderr is captured to a file and echoed back
unchanged, so nothing is swallowed. A 137 is called this command's own kill-after
event only when that fence's wrapper recorded `sending signal KILL to command`;
otherwise it is `kind=sigkill_not_from_this_wrapper`, is **not** a timeout, and
exits 1.

```text
RC137_PROVENANCE body=direct_137  subject=red   rc=137 result=[timeout kind=killed_after_grace per_fence_bound_s=900 kill_grace_s=30]
RC137_PROVENANCE body=direct_137  subject=green rc=1   result=[fence_failed fence=r8 rc=137 kind=sigkill_not_from_this_wrapper wrapper_sent_kill=no]
RC137_PROVENANCE body=ignore_term subject=green rc=137 result=[timeout fence=r8 kind=killed_after_grace wrapper_sent_term=yes wrapper_sent_kill=yes per_fence_bound_s=900 kill_grace_s=30]
```

The third line is the no-weakening control: the real event the audit asked round 7
to classify is still classified, now on the wrapper's own evidence. The residual
is stated: a body killed by something else *while* the wrapper was also killing it
is still reported as a kill-after event.

**The aggregate.** `aggregate_enforced_by=sequential_per_fence_bounds` described a
property no code enforced, and the prose called 3720 "an upper bound no execution
of this command can exceed". The four `sed` extractions, the `sha256sum`, the
`wc -c` and the shell's overhead are outside every wrapper; a FIFO in place of the
document blocks the command before the first wrapper starts. **The claim is
withdrawn, not reworded.** The result line states what is enforced:

```text
PUBLISHED_COMMAND_RESULT=pass fences=5 per_fence_bound_s=900 kill_grace_s=30 fence_timeout_budget_s=4650 whole_command_bound=none prelude_bounded=no
```

and the fence executes the FIFO on both command texts, showing identical behaviour
and opposite claims:

```text
UNBOUNDED_PRELUDE subject=red   outer_test_rc=124 ... claims_whole_command_bound=1 states_prelude_unbounded=0
UNBOUNDED_PRELUDE subject=green outer_test_rc=124 ... claims_whole_command_bound=0 states_prelude_unbounded=1
```

No outer wrapper was added. An outer `timeout` would bound the same quantity a
second time while discarding the per-fence rcs the classification depends on, and
the kickoff permits stating only what is enforced. That is a scope decision, and
it is recorded as one.

**The field label.** `adjudicated_name_sha256` hashed the bytes at the leaf name -
the one thing GREEN expressly does not adjudicate. It is now
`name_at_read_time_sha256`, which is what the surrounding prose always said it
was. The fence asserts zero emissions of the old field name and assembles the
token from two pieces so the checking lines cannot count themselves.

## Finding 4 - make the declared STOP reachable

The draft declares `B6_STOP reason=listener_inventory_unreadable_or_unparseable
rc=0 detail=capture_stream_unbound` for a descriptor-binding inability. Production
exited first, inside `wpi_capture`, as a generic
`RP7_STOP reason=capture_stream_not_bindable`.

**Which side moved, and why: the block.** The draft's token is the correct one -
row 22 is the row that cannot be evaluated, and a row-specific inability is more
informative than a generic one - so the repair makes the production path reach it
rather than editing the preregistration down to whatever the block happened to
emit. A caller with its own token declares it immediately before its capture:

```bash
wpi_capture_bind_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound"
wpi_capture listeners "$WPI_SS" -H -ltn
```

The declaration is consumed by exactly that capture and cleared at its entry, so a
capture nested inside a caller cannot inherit another row's token, and **a caller
that declares nothing keeps the fail-closed generic STOP** - the repair adds a
route, it does not broaden one. Rows 20, 21 and 22 declare theirs.

```text
ROW22_BIND_INABILITY subject=red   caller=listeners  rc=3 draft_declared_b6_token=0 generic_rp7_token=1 adjudicated_line=[RP7_STOP reason=capture_stream_not_bindable label=listeners ...]
ROW22_BIND_INABILITY subject=green caller=listeners  rc=3 draft_declared_b6_token=1 generic_rp7_token=0 adjudicated_line=[B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound]
ROW22_BIND_INABILITY subject=green caller=undeclared rc=3 draft_declared_b6_token=0 generic_rp7_token=1 adjudicated_line=[RP7_STOP reason=capture_stream_not_bindable label=undeclared_probe ...]
```

The arm is production, not stub-only: the real `wpi_capture`, the real bounding
wrapper, a real child and the real row adjudicator. The injection is the close of
the creating write descriptor, reached through Bash's dynamic scoping from a hooked
`wpi_clock_ms`. It is **not** the unlink the carried leaf-race arm uses, and the
reason is recorded in the fence: on this workstation `/dev/fd/<n>` sometimes still
resolves for a leaf whose name has just been removed, so the unlink route
reproduces its own precondition only sometimes. An arm that is flaky about the
condition it is testing is not a fence arm - which is also why the carried
leaf-race assertion accepts either documented outcome and nothing else.

## Carried fences - every change, with its discriminating-power argument

| Fence | Body SHA-256 | Bytes | Changes this round |
|---|---|---|---|
| Round 8 (new) | `dada2eaa8ce970c75ffec583ebff5fcb1d41d928fcce511dbc5b990322007f98` | 28633 | n/a |
| Round 7 | `2a2eb8932352ea865022daf8c4be566b50bde61977339cfac91a71020ff327ff` | 22522 | four, named below |
| Round 6 | `0dc6213799d422f0921b0742a28840334c7453697087b205ced56d48ecfd2fb1` | 32069 | three, named below |
| Round 5 | `a3fb4b346d1fbb8785b20eefd7b6c96be1ae79adcf74ac4804e3323906d3fc56` | 20050 | one: the two GREEN identity constants |
| Round 4 | `4ddfa8b51bf31c99db560b07aac8572579020c231682201add643ea1f07c4cd1` | 77408 | one class: descriptor allocation in the stubs that feed a B5 or B6 assertion |

**Round-7 fence.**

1. *The two GREEN identity constants.* They name the subject by hash and byte
   count. A different subject file still fails, exactly, before any arm runs.
2. *`adjudicated_name_sha256` -> `name_at_read_time_sha256` in the `READER_BINDING`
   printf.* Nothing was ever asserted on the field's name - the four `expect_has`
   patterns match `.*` there and are unchanged - and the arm's discrimination is
   `bytes_field` against `independent_wc_c` plus the result token, all untouched.
   A wildcard capture read through a substituted loopback name still fails.
3. *Both capture stubs allocate `WPI_CAP_ERR_FD` as well as `WPI_CAP_OUT_FD`.*
   Interface adaptation to a production reader that now requires it. The stubs feed
   the same fixture bytes to the same readers; every malformed record in the group
   still STOPs with the same token, which the transcript shows line for line.
4. *The F4 group's GREEN command text is the `c708511f` blob, not `$DOC`.* With the
   live document as GREEN, a carried regression fence re-adjudicates a moving
   subject and has to be re-edited whenever the command changes - which is how
   assertions drift, and is the shape of finding 1. The round-6 misclassification
   still fails exactly as before. What this group no longer covers, the current
   command text, is covered by the round-8 F3 group under a strictly stronger
   assertion.

**Round-6 fence.**

5. *`expect_rc f4_bound_wrappers` 4 -> 5, the pattern gains `--verbose`, `DOCBOUND`
   looks for "fence-timeout budget", and a new `expect_rc f4_every_body_wrapped`
   asserts wrappers == extracted fence bodies.* A fence run without a `timeout`
   wrapper still fails, and now fails harder: the count is tied to the number of
   bodies the command extracts instead of being a bare constant, so adding an
   unwrapped fence fails even if the constant is updated with it.
6. *The F5 GREEN assertion becomes an exact two-outcome classifier, and a `return 7`
   mutant is added as a RED arm.* Finding 1. The round-5 escape still fails under
   both the old and the new assertion; what newly fails is the mutant, and the
   fence asserts both `f5_old_accepts_mutant` and `f5_new_rejects_mutant` so the
   weakening is on the record rather than in prose.
7. *Descriptor allocation in the stubs that feed a B5 or B6 assertion.* As (3).

**Round-5 fence.** Only the two GREEN identity constants, same length as the ones
they replace, so the extracted body is still exactly 20050 B. Its one stub,
`forge_capture`, drives the `lock_parity` child, whose readers are outside this
round's binding change.

**Round-4 fence.** Only the descriptor allocations in the stubs that feed a B5 or
B6 assertion. No fixture byte, arm or assertion changed, and the transcript is the
check: the same bytes reach the same readers and the same result lines come back.

## Verification

Five fences, extracted by the published anchored command from `SELF_QA_RP7.md`,
all `QA_PASS all_assertions=yes`, command rc 0 with empty stderr:

```text
R8_FENCE_RC=0
R7_FENCE_RC=0
R6_FENCE_RC=0
R5_FENCE_RC=0
R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=5 per_fence_bound_s=900 kill_grace_s=30 fence_timeout_budget_s=4650 whole_command_bound=none prelude_bounded=no
```

Delivered block:

```text
bytes=99903
sha256=11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4
cr_bytes=0
bash_n=0
```

`cr_bytes` was derived with `LC_ALL=C tr -cd '\r' < RP7-WPI-RO.sh | wc -c`, and
the same command returns 0 for `SELF_QA_RP7.md`, `STATUS_RP7.md`, this report, the
corrected `RP7_REPAIR_R7_REPORT.md` and the edited
`WPI_PREREGISTRATION_DRAFT.md`.

## Draft edits (three, all narrow, all forced by a repair)

1. **Row 20** - the status code, and the emptiness of the diagnostic stream it is
   conditioned on, are read through the descriptor the capture created;
   `detail=capture_stream_unbound` is added to the STOP set; the executed
   substitution that turned a child-observed 500 into an accepting 200 is named.
2. **Row 21** - the same for the parser result record.
3. **Row 22** - the same for both namespace identities, and `detail=<d>` is added
   to `B6_STOP reason=service_netns_unreadable ...` so `capture_stream_unbound` is
   declared there too.

Row 22's listener half was not edited: it already declared
`detail=capture_stream_unbound`, and finding 4 was repaired by making the block
reach the token the draft preregisters.

## Nothing was left unrepaired

All four findings are repaired. Two scope decisions are recorded above and in the
delivered document rather than as silent omissions: readers outside rows 20-24 are
not descriptor-bound, and no outer wrapper was added to the published command. One
statement in a previous report was false and is corrected in place with a notice at
the top of that file.
