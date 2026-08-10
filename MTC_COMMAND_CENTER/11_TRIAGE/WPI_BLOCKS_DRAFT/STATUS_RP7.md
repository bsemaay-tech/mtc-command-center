# RP7 status

Status: **REPAIRED-R6-PENDING-INDEPENDENT-REAUDIT**

Scope: `RP7-WPI-RO.sh` implements remote RO-stage rows 10-23 and records row 24
as operator-side only. Repair round 6 was authorized under owner grant #7, which
lifts the T0 round cap for this block set until both flagships accept. It
answers the Codex T0 part-B audit of the round-5 bytes
(`RP7_CODEX_T0_AUDIT_R5_PART_B_2026-08-10.md`, BLOCK on four findings, two of
them HIGH) together with the one executed test recovered from the review the
provider interrupted (`RP7_R5_SALVAGE_FROM_INTERRUPTED_AUDIT_2026-08-10.md`).
Codex is the auditor of record for findings 1-4 and re-audits these bytes, so
implementer/auditor separation holds. Round 5's own repairs were independently
verified clean (`+93/-7`, no unexplained hunks, no weakening) and were built on,
not re-litigated.

Every finding this round was one defect wearing four faces: **a record the block
could not parse was repaired into one it could, and then adjudicated as host
state.** rc 1 means a completed probe established deviant host state. It must
not be reachable from bytes that state nothing.

Material repair state added this round:

- **the listener inventory is read once, whole, and byte-accounted.** Bash
  `read` discards NUL, so the record `LIS<NUL>TEN 0 128 127.0.0.1:8790 ...` was
  consumed as `LISTEN ...`: the reader normalised a malformed record into a
  conformant one and the block printed both `parse=complete_before_semantics`
  and the accepting listener-set line at rc 0. The inventory is now taken in one
  NUL-delimited read - which returns success only when it actually finds the one
  byte class the record reader cannot represent - and records are split out of
  that single in-memory string, so there is no second open, no second pass, and
  a closing conservation equation `consumed == captured` that the accepting line
  publishes as `bytes=<n>`;
- **listener endpoints have a numeric grammar.** Round 5 required only that the
  address half contain a colon and the port half be decimal, so `nonsense:8790`
  became an observed non-preregistered listener and `127.0.0.1:99999` became an
  observed absence of the preregistered one - two host-state FAILs derived from
  records that state no address and no port. Both halves are now validated
  (complete dotted quad or IPv6 literal with at most one `::` and an optional
  zone; port 0-65535 with no leading zeros; `*` only as a peer port), and every
  deviation is a STOP;
- **the status parser's result records are parsed, not scanned.** The parent
  checked a character class and nothing else, so `TYPE state str` - three
  tokens, naming no expected type, a record the child cannot emit - became
  `B5_FAIL ... expected_type=` at rc 1, and `MISMATCH state abc` did the same
  with a three-character digest. Each record is now reconstructed from its own
  tokens and compared to the bytes the child emitted, with an exact token count,
  a preregistered field name, that field's own expected type, and 64 lowercase
  hex. The field/type schema is declared **once** and passed to the child as
  argv[2]; the child refuses to answer unless the declaration equals its own
  table (`PARSE schema_declaration_mismatch`), so the parent cannot drift into
  checking a contract the child is not executing;
- **invalid HTTP status tokens STOP.** Every three-digit string was read as a
  completed response, so curl's no-response sentinel `000` and the out-of-range
  `600` were reported as observed endpoint deviations. Only 100-599 is a status
  line the endpoint sent; `000` carries its own reason token;
- **the published evidence command can fail, and is bounded.** Each fence
  invocation was followed by a `printf`, so the command returned the `printf`
  status: Codex proved two fences exiting 7 and 9 with an outer rc of 0. The
  command now captures all three fence rcs, prints them, exits nonzero if any is
  nonzero, and reports a fence killed at its bound as a distinct `timeout`
  result. Each fence runs under an explicit 900 s `timeout`; the documented
  aggregate bound is 2700 s and the measured runs were 214 s and 186 s;
- **writes go to the object the block created, not to the name.** The recovered
  test replaced a freshly allocated capture leaf with a hard link to a file
  outside the evidence tree in the window between allocation and write; the
  capture wrote its payload outside the tree at rc 0 with no STOP. `noclobber`
  proves a name did not exist at allocation, which is not the same fact as "the
  object written is the object allocated". Every shell-side write now goes
  through the descriptor the creating `O_CREAT|O_EXCL` open returned, and no
  leaf is re-opened by name for writing (12 name-based appends before, 0 now).

Two residuals are disclosed rather than claimed away, in `SELF_QA_RP7.md` under
*What this QA does not establish* and in the file header: the status-body leaf is
written by curl, which is handed a path and not a descriptor; and readers still
open leaves by name, so what the block establishes about captured content is what
its record grammar establishes. A per-capture `/proc/self/fd` identity re-check
and an `EV_DIR` ownership/mode precondition were both considered and rejected,
with reasons recorded in the report.

Local validation: literal Git Bash (MSYS2 bash 5.2.37, GNU coreutils 8.32,
CPython 3.14.2, git 2.52.0) - **three** fences, all extracted from
`SELF_QA_RP7.md` by the published anchored command and all `QA_PASS
all_assertions=yes` at rc 0 with empty stderr:

- the round-6 fence (`022607b8...0130a`, 26681 B) drives every arm twice, once
  against the frozen round-5 blob `git cat-file blob 1143a9ff:...` re-derived to
  77179 B / `393a16ce...b0ee` and once against these bytes, with a real RED and a
  real GREEN for all four findings and the recovered test - and with a
  no-weakening control inside each finding's own group;
- the round-5 fence (`71907795...3c9e2`, 20050 B) is carried unchanged except for
  its two GREEN identity constants, which name the subject by hash and byte count;
- the round-4 fence (`94101ef7...56e0`, 76710 B) is carried byte-for-byte
  unchanged and re-run as the no-weakening gate: every round-3 and round-4 arm
  still passes on the round-6 bytes.

`bash -n` PASS. Zero CR bytes.

**DRAFT EDITS (four, all narrow, all forced by a repair).** Section 8.2 row 20
now names the 100-599 status grammar; row 21 names the malformed-parser-result
STOP and the single schema declaration; row 22 names the single NUL-delimited
read, the byte-conservation requirement, the endpoint grammar STOPs, and the new
`bytes=<n>` field on the accepting inventory line; section 10.1 records that
permitted writes now bind to the created object, with the curl exception. Without
the row-22 edit the block would emit a field the preregistration does not declare.

**FREEZE-GATE ITEMS (three, all carried deliberately, unchanged from round 5).**

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
bytes=88460
sha256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the round-6 authorized deliverables occurred.
