# RP7-WPI-RO repair round 7 - report

Implementer: Claude Opus 5, effort xhigh, authorised under owner grant #7.
Auditor of record: Codex, who re-audits these bytes; separation holds.
No host contact, network connection, SSH/SCP, RUNID minting, service, credential,
deployment, trading or commit action occurred. The Lead verifies and commits.

## Subject identity

| Subject | Bytes | SHA-256 | CR | `bash -n` |
|---|---|---|---|---|
| Predecessor (round 6, commit `3e2a976a`, blob `2bc44445142e0259c14116111df69719b5e0b8ad`) | 88460 | `6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709` | 0 | rc 0 |
| **Round 7 (delivered)** | **92853** | **`e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32`** | **0** | **rc 0** |

Both identities are re-derived inside the round-7 fence before any arm runs, and
the predecessor is materialised only with `git cat-file blob`, never checked out.

Other delivered files:

| File | Bytes | SHA-256 |
|---|---|---|
| `SELF_QA_RP7.md` | 230272 | `d8acd072be93979ed972f04dda27775b0e485692c44ed5924659985dd463ade5` |
| `STATUS_RP7.md` | (see worktree) | rewritten for round 7 |
| `WPI_PREREGISTRATION_DRAFT.md` | 116062 | `65b71cfdffff77906dccbd0c953497503c15076cd37a6fbf3a11ee8eba4375f3` |

Diffstat for the round: `RP7-WPI-RO.sh` +90/-23, `SELF_QA_RP7.md` (round-7 fence,
transcripts, carried-fence updates, prose), `STATUS_RP7.md` rewritten,
`WPI_PREREGISTRATION_DRAFT.md` 20 lines touched across four narrow edits.

## Finding dispositions

Every finding in `RP7_CODEX_T0_AUDIT_R6_PART_B_2026-08-11.md` was reproduced as a
RED on the round-6 bytes before it was repaired, and every repair is measured as a
GREEN on the delivered bytes by the same arm.

### F1 (HIGH) - the common single-record reader normalises NUL-bearing records - **REPAIRED**

**Change.** `wpi_single_record` (`RP7-WPI-RO.sh:294-352`) no longer reads the
record with `IFS= read -r`, which silently discards NUL. The whole stream is taken
in ONE NUL-delimited read: that read returns 0 only when it actually found a NUL -
the one byte class this reader cannot represent - and otherwise returns EOF with
every captured byte in the variable. The record is split out of that single
in-memory string, and `${#first} + 1 == ${#whole}` accounts for every captured byte
against the one record and its terminator (`LC_ALL=C` is pinned at the top of the
block, so `${#...}` is a byte count). NUL is `detail=nul_byte_in_record`; an
unaccounted byte is `detail=record_bytes_unaccounted`. Both STOP before status,
parser-result or namespace semantics are applied, which closes all three affected
records at once because all three share this reader.

**Deliberately not done.** No additional charset gate was added here, unlike the
listener inventory reader. With `-r`, an empty `IFS` and a NUL delimiter, NUL is
the only class `read` can drop, and every caller already adjudicates the record
against an exact grammar of its own. A gate that STOPped on, say, CR would silently
change the accepted row-18 symlink-target disposition, which no finding asks for.
The reasoning is recorded in the function's own comment.

**Evidence** (round-7 fence, `RECORD_BYTES` group; transcript in `SELF_QA_RP7.md`):

| Record | RED (round-6 bytes) | GREEN (round-7 bytes) |
|---|---|---|
| `2<NUL>00` | rc 0, `B5_status http=200 ... flags=expected` | rc 3, `B5_STOP reason=status_endpoint_not_evaluable rc=0 detail=nul_byte_in_record` |
| `O<NUL>K fields=8` | rc 0, `B5_status http=200 ...` | rc 3, `B5_STOP reason=status_body_unreadable_or_unparseable detail=nul_byte_in_record` |
| `ne<NUL>t:[100]` | rc 0, `B6_netns ... binding=equal` | rc 3, `B6_STOP reason=service_netns_unreadable ... detail=nul_byte_in_record` |

**No-weakening controls, all in the same arm group:** clean `200`, clean
`OK fields=8` and clean `net:[100]` are accepting at rc 0 on both subjects; and the
four dispositions the reader already had - `empty_or_read_error`,
`unterminated_final_record`, `multiple_records`, `unterminated_extra_record` - are
produced with the identical reason token on both subjects. The rewrite changed
which records STOP, not which reason a record that already STOPped gets.

### F2 (HIGH) - nonnumeric listener queue fields reach a complete accepting set - **REPAIRED**

**Change.** `wpi_assert_listener_set` validated `"$recvq:$sendq"` against a class
that permits the separator itself. Each field is now validated separately as a
nonempty decimal-digit field, before any inventory-complete line, under the same
`detail=queue_grammar` token the preregistration already declares.

**Evidence** (round-7 fence, `QUEUE_FIELDS` group):

| Record | RED | GREEN |
|---|---|---|
| `LISTEN : 128 127.0.0.1:8790 0.0.0.0:*` | rc 0, `accepting=1 bytes=38`, `table=complete` | rc 3, `detail=queue_grammar`, no inventory line |
| `LISTEN 0 12:34 127.0.0.1:8790 0.0.0.0:*` | rc 0, `accepting=1 bytes=40` | rc 3, `detail=queue_grammar` |

**No-weakening controls:** the published column-padded record still parses to an
accepting set with `bytes=58` on both subjects, and a real wildcard is still
`B6_FAIL reason=nonloopback_listener addr=0.0.0.0` at rc 1 with `bytes=36` on both.

### F3 (HIGH) - row 22 claims byte identity the disclosed reader residual does not establish - **REPAIRED (option A: the capture descriptor is kept and read)**

**Option chosen and why.** The audit offered two honest options: bind the read to
the created object, or narrow row 22 and the `bytes=` description to the re-opened
object. **Option A was taken.** Row 22's sentence is the correct claim to make
about an inventory the block adjudicates as a complete observation of host state,
and it is cheap to make true for exactly that reader; narrowing it would have left
the block adjudicating a name while a row's whole purpose is to adjudicate what the
instrument produced. Option A also yields a real RED/GREEN arm, where a narrowing
would have produced only a documentation diff.

**Change.** `wpi_capture` re-derives a READ descriptor from its own creating write
descriptor - `exec {WPI_CAP_OUT_FD}</dev/fd/"$ofd"` - after the child exits and
before the write descriptor is closed. `/dev/fd/<n>` resolves through the existing
descriptor rather than through the evidence directory, so no name lookup happens
after the child ran, and a later replacement of the leaf name cannot change the
bytes read. The descriptor is opened after the child exits, so the child never
inherits it, and it is closed at the next capture, so exactly one capture's stream
is bound at a time. `wpi_assert_listener_set` reads that descriptor; an unbound
stream is `detail=capture_stream_unbound`, never a fallback read by name. The
accepting inventory line now publishes `read_binding=capture_descriptor`, so the
binding is checkable from the transcript rather than from prose.

**Scope of the repair, stated rather than implied.** Only the listener inventory
reader is bound this way. It is the only reader whose bytes a preregistered row
makes an identity claim about. `wpi_single_record`, `wpi_require_empty_file` and
`wpi_sha_file` still open by name, no row claims byte identity for them, and after
F1 each STOPs on a record it cannot represent byte for byte rather than
adjudicating it. Binding every reader is a signature change to every reader in the
block and to every carried regression arm that stands in for a capture, for claims
no row makes; it was weighed and deliberately not taken this round. Both the file
header and `SELF_QA_RP7.md` state this in those terms.

**Evidence** (round-7 fence, `READER_BINDING` group; the REAL `wpi_capture` runs a
real child under the real cleared environment and the real bounding wrapper, and
only `wpi_alloc_read_diag` is hooked, at the same boundary the auditor used):

| Subject | child captured | name at read time | Result |
|---|---|---|---|
| RED | wildcard `0.0.0.0:8790` (`97783a08...`) | loopback (`db4755ec...`) | rc 0, accepting `B6_listener_set`, `bytes=38` |
| GREEN | wildcard `0.0.0.0:8790` (`97783a08...`) | loopback (`db4755ec...`) | rc 1, `B6_FAIL reason=nonloopback_listener addr=0.0.0.0`, `bytes=36` = independent `wc -c` |

`READER_SUBSTITUTION red_child_ne_name=yes green_child_ne_name=yes` proves the
substitution really happened on both subjects; only the subject that reads the
descriptor is unaffected by it. **Control:** with no substitution both subjects
reach the same verdict and `bytes=` equals an independent `wc -c` of the child's
capture.

**Disclosed limitation.** On Linux, `/dev/fd/<n>` re-opens the inode even when the
leaf name has been unlinked. MSYS2 cannot, so the carried round-6 leaf-replacement
arm - which unlinks the leaf and hard-links an outside file in its place -
additionally reaches `RP7_STOP reason=capture_stream_not_bindable` on this
workstation where Linux would return rc 0. The payload still never leaves the
evidence tree, which is what that arm asserts, and the arm now runs the capture in
a subshell so it survives the STOP and can still report it.

### F4 (MEDIUM) - kill-after timeout misclassified, claimed aggregate unenforced - **REPAIRED**

**Change (classification).** `timeout --signal=TERM --kill-after=30s` has two
terminal outcomes. A body that dies on TERM exits 124; a body that ignores TERM and
is killed after the grace exits 137. The published command recognised only 124, so
a killed fence landed in the generic failure branch and was reported as
`fence_failed`. Both are now `PUBLISHED_COMMAND_RESULT=timeout`, distinguished by
`kind=terminated_at_bound` and `kind=killed_after_grace`, and the command exits
with the fence's own 124 or 137 rather than 1.

**Change (aggregate).** The documented `2700` was neither the sum of the three
bounds' graces (2790) nor enforced by any wrapper. The command now runs four
fences and documents **3720**, which is `4 * (900 + 30)`: four sequential bounded
steps cannot exceed the sum of their bounds, so the per-fence wrappers *are* the
enforcement, and the result line says so with
`aggregate_enforced_by=sequential_per_fence_bounds`. No outer wrapper was added: an
outer `timeout` would bound the same quantity a second time while discarding the
per-fence rcs the classification depends on. That reasoning is in the document, not
only here.

**Disclosed residual.** 137 is `SIGKILL`. A fence body killed by something other
than this command's own kill-after grace is indistinguishable from inside the
command and is reported the same way. Stated in `SELF_QA_RP7.md` rather than
claimed away.

**Evidence** (round-7 fence, `TIMEOUT_CLASS` and `BOUND_ARITHMETIC` groups; both
subjects are the published command TEXTS themselves, RED extracted from the
round-6 document at `3e2a976a`, each retargeted into a scratch tree with its bound
scaled from `900s`/`30s` to `1s`/`2s` and nothing else altered):

| Arm | RED | GREEN |
|---|---|---|
| TERM-ignoring fence body | fence rc 137, `PUBLISHED_COMMAND_RESULT=fence_failed`, command rc 1 | fence rc 137, `timeout kind=killed_after_grace`, command rc 137 |
| TERM-honouring fence body (control) | fence rc 124, `timeout`, command rc 124 | fence rc 124, `timeout kind=terminated_at_bound`, command rc 124 |
| Aggregate | `wrappers=3 computed_max_s=2790 claimed_s=2700 claim_true=no outer_wrapper=absent` | `wrappers=4 computed_max_s=3720 claimed_s=3720 claim_true=yes outer_wrapper=absent` |

The TERM-ignoring fence the audit asked for is now part of the published failure
evidence, so the kill-after path is proven rather than asserted. Round 6's rc
propagation repair is carried unchanged in the round-6 fence and re-executed here
(`PUBLISHED_RC_PROPAGATION round6_command_rc=1`).

## Nothing was left unrepaired

All four findings are repaired. No finding was dismissed, deferred or renegotiated.
Two things this round deliberately did **not** do are recorded above as scope
decisions rather than as unrepaired findings, and both are also in the delivered
document: no charset gate was added to `wpi_single_record` (F1), and readers other
than the listener inventory were not descriptor-bound (F3).

## Carried fences

| Fence | Body SHA-256 | Bytes | Carried |
|---|---|---|---|
| Round 7 (new) | `d4c730e5efb253a24ee0019a7eae9074f689233778f13a6248e42bf5cd100dbe` | 21450 | n/a |
| Round 6 | `b080dad4315281d0447baff10dae26797ba04998bc7c9e32fb2bbbd15a570a06` | 27355 | **not byte-identical**; four named changes |
| Round 5 | `6a5a80fef963c6506af93891cec362ce8e74fd6bde64f01d81bcb54cbe6507a6` | 20050 | **not byte-identical**; two GREEN identity constants only, same length, so the body is the same 20050 B |
| Round 4 | `ceb45f11f071bd61055a894deb72af229b253cb0eff3931c9ea46a0628028159` | 76873 | **not byte-identical**; two anchor comments (from round 5) plus one `exec {WPI_CAP_OUT_FD}<...` statement in each of four capture stubs |

The round-6 fence's four changes: the two GREEN identity constants (they name the
subject by hash and byte count); `expect_rc f4_bound_wrappers` from 3 to 4 (the
published command now runs four fences); its F1 listener stub, which must allocate
the read descriptor production allocates; and its F5 leaf-race arm, moved into a
subshell so it survives the disclosed MSYS2 STOP, with the rc no longer pinned in
an assertion that never measured it. No fixture byte and no other assertion moved.

A capture stub that sets `WPI_CAP_OUT` without allocating the read descriptor is
no longer standing in for `wpi_capture`; the block STOPs with
`detail=capture_stream_unbound` rather than falling back to a read by name. That is
why four stubs in the carried fences changed, and it is the intended consequence of
refusing a fallback.

## Draft edits (four, all narrow, all forced by a repair)

1. **Row 20** - the status record is byte-preserved: one NUL-delimited read before
   any status semantics, `detail=nul_byte_in_record` and
   `detail=record_bytes_unaccounted`, with the reason named (a line-by-line reader
   turned `2<NUL>00` into `200`).
2. **Row 21** - the same for the parser result record, naming
   `O<NUL>K fields=8` as the case it closes.
3. **Row 22** - the namespace identities are read under the same rule; the
   inventory is read **through the descriptor the capture created**, with both
   halves of the identity sentence tied to the defect each answers; each of
   `Recv-Q` and `Send-Q` must separately be nonempty decimal digits;
   `detail=queue_grammar` and `detail=capture_stream_unbound` are added to the STOP
   set; and the accepting inventory line gains
   `read_binding=capture_descriptor`, with `bytes` re-described as the accounting
   of every byte consumed **from the capture descriptor** and `evidence_file` as a
   location only. Without this edit the block would emit a field the
   preregistration does not declare.
4. **Section 10.1** - the sentence "Readers still open by name, so what the block
   establishes about captured content is what its record grammar establishes" is
   replaced by the true version: the one reader a row makes an identity claim about
   is descriptor-bound and why, and the others are not and claim nothing beyond
   their record grammar.

## Executed validation

Published command, run verbatim from `WPI_BLOCKS_DRAFT`:

```bash
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

Three verbatim runs: rc 0, empty stderr, 46348 stdout bytes each; 206 s, 207 s and
a third against the file as delivered. All four fences printed
`QA_PASS all_assertions=yes`; `R7_FENCE_RC=0 R6_FENCE_RC=0 R5_FENCE_RC=0
R4_FENCE_RC=0`; final line `PUBLISHED_COMMAND_RESULT=pass fences=4
per_fence_bound_s=900 kill_grace_s=30 aggregate_bound_s=3720
aggregate_enforced_by=sequential_per_fence_bounds`. The diff between runs is
confined to two measured wall clocks and one Windows scratch path, which the
document names as the only non-deterministic outputs in the suite.

Independent re-derivation of the delivered block:

```text
sha256=e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32
bytes=92853
cr_bytes=0        (LC_ALL=C tr -cd '\r' < file | wc -c)
bash -n           rc 0
```

## Freeze-gate inputs (unchanged from round 5; still owner/deploy-channel items)

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` - `<PIN-AT-FREEZE>`. No accepting
   `wpi_validate_inputs` arm exists or can exist before freeze. The
   `normalised_path_projection_v2` digest covers 21 point paths.
2. `WPI_FIXED_TRUSTED_PYTHON` - `<PIN-AT-FREEZE>`. Must be the resolved
   `/usr/bin/python3.<minor>`, because `wpi_bind_tool` admits no symlinked object.
3. `WPI_FIXED_EVIDENCE_ROOT` - `<PIN-AT-FREEZE>`, value `<REMOTE_BASE>/evidence`.
   Carries an ordering constraint Stage 1 must close: `REMOTE_BASE` is allocated at
   dispatch, so the base must be allocated before the RO block is frozen and
   hashed. If Stage 1 cannot reorder that, the honest outcome is to record that the
   RO block does not claim evidence-root provenance for this run.

The first action after all three are supplied, and before dispatch, is to execute
the accepting-input arm and record it. The block cannot be frozen on this QA alone.
Section 8.2 rows 1-9 remain implemented by no block and are a separate owner
decision.
