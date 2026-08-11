# RP7 status

Status: **REPAIRED-R7-PENDING-INDEPENDENT-REAUDIT**

Scope: `RP7-WPI-RO.sh` implements remote RO-stage rows 10-23 and records row 24
as operator-side only. Repair round 7 was authorized under owner grant #7, which
lifts the T0 round cap for this block set until both flagships accept. It answers
the Codex T0 part-B re-audit of the round-6 bytes
(`RP7_CODEX_T0_AUDIT_R6_PART_B_2026-08-11.md`, BLOCK on four findings, three of
them HIGH). Codex is the auditor of record and re-audits these bytes, so
implementer/auditor separation holds. Round 6's repairs were confirmed by that
audit - the padded-listener, wildcard, `500` and `401` controls hold, the four
status-result dispositions hold, and `wpi_open_leaf` genuinely binds the
shell-side write to the object its create-once open created - and were built on,
not re-litigated.

Three of the four findings are one defect wearing three faces: **a value is
admitted, transformed, or re-read, and the claim made about it is stronger than
what survived the transformation.** rc 0 means a completed probe established
conformant host state. It must not be reachable from bytes the block silently
changed, from a field it never checked, or from an object it never read.

Material repair state added this round:

- **every single-record read is byte-preserving.** `wpi_single_record` used
  `IFS= read -r`, which silently discards NUL, so `2<NUL>00` became the completed
  HTTP status `200`, `O<NUL>K fields=8` became the parser's accepting result, and
  `ne<NUL>t:[100]` became a valid namespace identity - three malformed records
  normalised into accepting observations at rc 0. The record is now taken in ONE
  NUL-delimited read, which returns success only when it actually finds the one
  byte class the reader cannot represent, and `${#first} + 1 == ${#whole}` is a
  conservation equation over every captured byte. This is the same discipline the
  listener reader already used, now applied to the reader all of rows 20, 21 and
  22 share. The four dispositions the reader already had
  (`empty_or_read_error`, `unterminated_final_record`, `multiple_records`,
  `unterminated_extra_record`) keep their exact reason tokens;
- **each listener queue field is validated separately.** The parser checked the
  CONCATENATION `"$recvq:$sendq"` against a class that permits the separator, so
  `recvq=:` and `sendq=12:34` were admitted as structurally complete and reached
  the accepting listener line at rc 0. Each of `Recv-Q` and `Send-Q` is now
  required to be a nonempty decimal-digit field before any inventory-complete
  line. Column padding still parses and a real wildcard is still a host-state
  FAIL;
- **the listener inventory is read through the descriptor the capture created.**
  Row 22 claimed the byte string adjudicated *is* the byte string captured while
  the reader re-opened `$WPI_CAP_OUT` by name after the child had exited. An
  executed fixture replaced that name between the two and the block adjudicated
  a record the child never wrote, PASSing on a wildcard capture. `wpi_capture`
  now re-derives a read descriptor from its own creating write descriptor
  through `/dev/fd/<n>` - after the child exits, before the write descriptor is
  closed - so no name is resolved after capture and the child never inherits the
  read side. The accepting inventory line publishes `read_binding=capture_descriptor`,
  and an unbound stream is `detail=capture_stream_unbound`, never a read by name;
- **the published evidence command classifies both of its timeout outcomes and
  documents a bound arithmetic supports.** `timeout --kill-after=30s` has two
  terminal outcomes: 124 when the body dies on TERM, and 137 when it ignores TERM
  and is killed after the grace. Round 6 recognised only 124, so a killed fence
  was reported as `fence_failed` - an assertion failure that never happened. Both
  are now `timeout`, distinguished by `kind=`, and the command exits with the
  fence's own 124 or 137. The documented aggregate was `2700` against three 900 s
  bounds whose graces make 2790, and no wrapper enforced it; it is now **3720**,
  which is `4 * (900 + 30)` over four sequential bounded fences, is re-derived
  from the published text inside the fence rather than asserted in prose, and
  carries `aggregate_enforced_by=sequential_per_fence_bounds` on the result line.
  Round 6's rc propagation is carried unchanged and re-executed.

Residuals are disclosed rather than claimed away, in `SELF_QA_RP7.md` under
*What this QA does not establish* and in the file header. The status-body leaf is
written by curl, which is handed a path and not a descriptor. Readers other than
the listener inventory - `wpi_single_record`, `wpi_require_empty_file`,
`wpi_sha_file` - still open leaves by name, and **no preregistered row claims
byte identity for those**: what the block establishes about their content is
exactly what their record grammar establishes, which is why each STOPs on a
record it cannot represent byte for byte, NUL included, rather than adjudicating
it. Binding them the same way is a signature change to every reader and to every
carried regression arm, for claims no row makes; it was weighed and deliberately
not taken this round. One MSYS2 limitation is disclosed: `/dev/fd/<n>` cannot
re-open the descriptor of a leaf whose name has just been unlinked, so the
carried leaf-replacement arm additionally STOPs on this workstation where Linux
would return rc 0. The payload still never leaves the evidence tree, which is
what that arm asserts.

Local validation: literal Git Bash (MSYS2 bash 5.2.37, GNU coreutils 8.32,
CPython 3.14.2, git 2.52.0) - **four** fences, all extracted from
`SELF_QA_RP7.md` by the published anchored command and all `QA_PASS
all_assertions=yes` at rc 0 with empty stderr, in 206 s:

- the round-7 fence (`d4c730e5...00dbe`, 21450 B) drives every arm twice, once
  against the frozen round-6 blob `git cat-file blob 3e2a976a:...` re-derived to
  88460 B / `6586698c...40709` and once against these bytes, with a real RED and
  a real GREEN for all four findings and a no-weakening control inside each
  finding's own group. The F3 arms run the REAL `wpi_capture` against a real
  child and hook only the reader-allocation boundary, exactly where the auditor
  injected the substitution; the F4 arms run the two published command TEXTS
  themselves, RED extracted from the round-6 document at the same commit;
- the round-6 fence (`b080dad4...70a06`, 27355 B) is carried and re-run as a
  regression gate, with four named changes and nothing else: the two GREEN
  identity constants, `expect_rc f4_bound_wrappers` from 3 to 4, one capture stub
  that must now allocate the read descriptor production allocates, and the
  leaf-race arm moved into a subshell so it survives the disclosed MSYS2 STOP;
- the round-5 fence (`6a5a80fe...507a6`, 20050 B) is carried unchanged except for
  its two GREEN identity constants, and its extracted body is byte-for-byte the
  same length because the substituted constants are the same length;
- the round-4 fence (`ceb45f11...28159`, 76873 B) is carried unchanged except for
  its two anchor comments and the four capture stubs that drive the listener
  reader, each of which gained exactly one `exec {WPI_CAP_OUT_FD}<...` statement.
  No fixture byte, arm or assertion changed, and every round-3 and round-4 arm
  still passes on the round-7 bytes.

`bash -n` PASS. Zero CR bytes.

**DRAFT EDITS (four, all narrow, all forced by a repair).** Section 8.2 row 20
now names the byte-preserving status record and its `nul_byte_in_record` /
`record_bytes_unaccounted` STOPs; row 21 names the same for the parser result
record; row 22 names the byte-preserving namespace records, the read through the
capture descriptor, the separate `Recv-Q`/`Send-Q` grammar, the
`capture_stream_unbound` STOP, and the new `read_binding=capture_descriptor`
field on the accepting inventory line; section 10.1 records that the one reader a
row makes an identity claim about is now descriptor-bound and that the others are
not, replacing the sentence that said readers open by name. Without the row-22
edit the block would emit a field the preregistration does not declare.

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
bytes=92853
sha256=e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the round-7 authorized deliverables occurred.
