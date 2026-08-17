# RP7-WPI-RO repair round 6 - implementer report

Implementer: Claude Opus 5, effort xhigh. Auditor of record for findings 1-4:
Codex `gpt-5.6-sol` (`RP7_CODEX_T0_AUDIT_R5_PART_B_2026-08-10.md`, BLOCK: 4).
Round 6 is authorised under owner grant #7. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no SSH/SCP, no
RUNID, no credential, no service, no deployment, no commit occurred. All fixture
writes were confined to `mktemp` directories under `/tmp` whose prefix was
checked before recursive removal. UNIX LF only.

## Identity

Input bytes, re-derived before any edit:

```text
SHA256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee
BYTES=77179
CR_BYTES=0
```

Output bytes, re-derived after the last edit with
`sha256sum`, `wc -c` and `tr -cd '\r' < file | wc -c`:

```text
SHA256=6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709
BYTES=88460
CR_BYTES=0
BASH_N_RC=0
```

The round-5 blob was materialised with
`git cat-file blob 1143a9ff:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
and re-derived to the kickoff identity exactly. No block file was ever
`git checkout`-ed.

## Every RED reproduced first, on the round-5 bytes

Before any repair, all four findings and the recovered test were reproduced by
running the audit's own fixture bodies against the round-5 worktree file. Each
reproduced exactly as recorded:

| Finding | Reproduced RED | Observed |
|---|---|---|
| 1 | NUL-bearing listener record | `B6_listener_inventory ... table=complete parse=complete_before_semantics` then `B6_listener_set port=8790 count=1 ...`, rc **0** |
| 1 (companions) | `nonsense:8790`, `127.0.0.1:99999` | `B6_FAIL reason=listener_set_unexpected ...`, rc **1**, both after a claimed complete parse |
| 2 | `TYPE state str` at child rc 5 | `B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=`, rc **1** |
| 3 | `000`, `099`, `600` | `B5_FAIL reason=status_endpoint_unexpected_http code=<c>`, rc **1** for all three |
| 4 | `bash; printf; bash; printf` | `R5_FENCE_RC=7`, `R4_FENCE_RC=9`, outer rc **0**; static scan `EXACT_BLOCK_OUTER_TIMEOUT_WRAPPERS=0`, `DOCUMENTED_AGGREGATE_BOUND_MENTIONS=0` |
| salvage | leaf replaced between allocation and write | `LEAF_REPLACEMENT_FALSIFICATION rc=0 outside_text=CAPTURED ... same_object=yes`, rc **0** |

Every one of those REDs is carried in the round-6 fence as an executed arm, not
as a quotation.

## Finding -> disposition -> evidence

### F1 (HIGH) - a malformed listener record is silently normalised - REPAIRED

**Disposition: closed.** The defect was that `IFS= read -r line` discards NUL, so
the reader repaired `LIS<NUL>TEN` into `LISTEN` and then adjudicated it. The
repair does not add a NUL check to the old reader; it removes the reader's
ability to lose a byte at all. `wpi_assert_listener_set` now opens the capture
once, reads it with `IFS= read -r -d ''` - which returns success **only** when it
actually finds a NUL, the one byte class a record reader cannot represent - and
splits records out of that single in-memory string. A NUL is a STOP
(`detail=nul_byte_in_inventory`); a whole-string charset check rejects any
control byte other than TAB and LF; an unterminated final record is a STOP; and
the loop closes with the conservation equation `consumed == ${#whole}`
(`detail=record_bytes_unaccounted` otherwise). The accepting inventory line
publishes the count as `bytes=<n>`.

The endpoint grammar is the second half of the same finding. `wpi_require_endpoint`
splits each token at its last colon and validates both halves: a complete dotted
quad (four octets, no leading zeros, each `<= 255`), a bracketed or bare IPv6
literal (at most one `::`, at most eight groups, optional zone, optional trailing
IPv4), or `*`; and a port of 1-5 decimal digits without leading zeros in 0-65535,
with `*` admissible only as a peer port. Every deviation is a STOP.

Field splitting also changed: `read -r ... <<< "$line"` became `set -- $line` with
an exact `[ "$#" -eq 5 ]`, which is a real token count rather than an "extra field
is empty" proxy, and needs no here-string.

**Evidence** (round-6 fence, `LISTENER_BYTES` and `LISTENER_CONSERVATION`):

```text
RED   LISTENER_BYTES case=nul rc=0 accepting=1 parsed_complete=1 stop=[] fail=[]
GREEN LISTENER_BYTES case=nul rc=3 accepting=0 parsed_complete=0 stop=[listener_inventory_unreadable_or_unparseable rc=0 detail=nul_byte_in_inventory]
RED   LISTENER_BYTES case=address rc=1 ... fail=[listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790]
GREEN LISTENER_BYTES case=address rc=3 ... stop=[... detail=local_address_grammar]
RED   LISTENER_BYTES case=port_range rc=1 ... fail=[listener_set_unexpected observed_count=0 expected=1x127.0.0.1:8790]
GREEN LISTENER_BYTES case=port_range rc=3 ... stop=[... detail=local_port_range port=99999]
GREEN LISTENER_BYTES case=octet rc=3 ... stop=[... detail=local_address_grammar]
GREEN LISTENER_BYTES case=leading0 rc=3 ... stop=[... detail=local_port_grammar]
LISTENER_CONSERVATION case=clean independent_wc_c=58 block_bytes_field=58
LISTENER_CONSERVATION case=wildcard independent_wc_c=36 block_bytes_field=36
```

**No-weakening controls, in the same arm group:** column-padded `ss` output still
parses to `rc=0 accepting=1` in both RED and GREEN, and a real wildcard listener
is still `rc=1 fail=[nonloopback_listener addr=0.0.0.0]` in both. The repair
added no new STOP over well-formed input. The `bytes` field is cross-checked
against an independent `wc -c` rather than asserted against a constant.

### F2 (HIGH) - malformed producer results become semantic FAILs - REPAIRED

**Disposition: closed.** Each of the three deviation records is now reconstructed
from its own tokens and compared byte-for-byte with what the child emitted
(`[ "TYPE $2 $3 $4" = "$record" ]` and its two siblings), with an exact token
count, membership of a preregistered field name, the field's own expected type,
a plausible observed type name, a rejection of a record claiming a type deviation
between identical types, and a 64-lowercase-hex digest. Everything else STOPs
under `status_body_unreadable_or_unparseable` with a `detail=*_record_*` token
naming the rule that failed.

The schema is declared **once**, as `WPI_STATUS_SCHEMA`, and passed to the child
as `argv[2]`. The child compares it with its own `expected` table and exits
`PARSE schema_declaration_mismatch` rc 3 if they differ. This is deliberate
pattern-11 hygiene: the parent must know the contract to check it, and a second
declaration would be free to drift from the one actually executing.

**Evidence** (`STATUS_RECORD` pairs and `STATUS_SCHEMA`):

```text
RED   rec=[TYPE state str]          rc=1 result=[B5_FAIL reason=flag_mismatch field=state observed_type=str expected_type=]
GREEN rec=[TYPE state str]          rc=3 result=[B5_STOP ... detail=type_record_grammar tokens=3]
RED   rec=[TYPE state str int]      rc=1 result=[B5_FAIL ... expected_type=int]
GREEN rec=[TYPE state str int]      rc=3 result=[B5_STOP ... detail=type_record_expected_type field=state]
GREEN rec=[TYPE state str str]      rc=3 result=[B5_STOP ... detail=type_record_not_a_deviation field=state]
GREEN rec=[TYPE rogue str str]      rc=3 result=[B5_STOP ... detail=type_record_field]
RED   rec=[MISMATCH state abc]      rc=1 result=[B5_FAIL ... observed_sha256=abc ...]
GREEN rec=[MISMATCH state abc]      rc=3 result=[B5_STOP ... detail=mismatch_record_digest]
GREEN rec=[MISMATCH rogue <64hex>]  rc=3 result=[B5_STOP ... detail=mismatch_record_field]
GREEN rec=[MISSING rogue]           rc=3 result=[B5_STOP ... detail=missing_record_field]
STATUS_SCHEMA mutated=yes rc=3 ... child=[PARSE schema_declaration_mismatch]
```

**No-weakening controls:** the four records the child really emits keep their
round-5 dispositions byte-identically - `TYPE state_version str int` -> rc 1 FAIL,
`MISMATCH state <64hex>` -> rc 1 FAIL, `MISSING state_version` -> rc 3
`schema_unexpected field=state_version`, `OK fields=8` -> rc 0 accepting line -
and the schema arm's clean half drives real CPython over the real production body
to `rc=0 ... child=[OK fields=8]`.

### F3 (MEDIUM) - invalid HTTP status tokens - REPAIRED

**Disposition: closed.** The `[0-9][0-9][0-9]` FAIL arm became `[1-5][0-9][0-9]`,
with `000` given its own reason (`detail=http_code_no_response`) because it is
curl's no-response sentinel rather than a malformed string, and everything else
falling to `detail=http_code_grammar`.

**Evidence** (`HTTP_CODE` pairs): `000`, `099` and `600` move from
`rc=1 B5_FAIL reason=status_endpoint_unexpected_http` to `rc=3 B5_STOP`. **Controls:**
`500` stays `rc=1 B5_FAIL ... code=500` and `401` stays `rc=3 B5_STOP
reason=status_endpoint_access_denied code=401`, both identical in RED and GREEN.

### F4 (MEDIUM) - the published command masks failure and is unbounded - REPAIRED

**Disposition: closed, both halves.** The command now captures each fence rc into
a variable, prints all three, and adjudicates them in a loop: `0` continues, `124`
prints `PUBLISHED_COMMAND_RESULT=timeout per_fence_bound_s=900` and exits 124, and
anything else prints `PUBLISHED_COMMAND_RESULT=fence_failed` and exits 1. Each
fence runs under `timeout --signal=TERM --kill-after=30s 900s`. The aggregate
bound - 2700 s - is stated in the document, and the command prints it on success.

The proof that it can fail is executed, not argued. The fence extracts the
published command from the document and runs it over a scratch document whose
three fence bodies are `exit 7`, `exit 9` and `exit 0`, with exactly two
substitutions: the `cd` target, and the `/tmp` prefix of the fence-body paths so
a nested run cannot overwrite the body of the run executing it. Both substitutions
are asserted before the copy runs.

```text
PUBLISHED_RC_MASK round5_sequence_rc=0 inner_rcs=[R5_FENCE_RC=7,R4_FENCE_RC=9,]
GREEN R6_FENCE_RC=7
GREEN R5_FENCE_RC=9
GREEN R4_FENCE_RC=0
GREEN PUBLISHED_COMMAND_RESULT=fence_failed
PUBLISHED_RC_PROPAGATION round6_command_rc=1 substitutions=2
PUBLISHED_BOUND timeout_wrappers=3 documented_aggregate_bound_mentions=2
PUBLISHED_BOUND_ENFORCED scaled_bound_s=3 rc=124 wall_s=3
```

The bound arm is a scaled reproduction: only the number differs from the published
900 s, because a QA fence cannot wait fifteen minutes to prove a fifteen-minute
bound. The wrapper form executed is the published one, and it turns a hanging body
into rc 124 - a result distinct from both PASS and assertion failure.

The command itself was then executed verbatim twice against the real document:
rc 0 in 214 s and rc 0 in 186 s, 38464 stdout bytes and 0 stderr bytes both times,
three `QA_PASS all_assertions=yes`, and identical fence-body digests. The diff
between the two runs is three lines: two measured wall clocks and one fixture path
that embeds its own scratch directory name.

### Recovered test (salvage) - the capture leaf can be replaced after allocation - REPAIRED for the write path, residuals disclosed

**Disposition: the demonstrated route is closed; two undemonstrated residuals are
stated narrowly rather than claimed closed.**

The recovered fixture was treated exactly as the kickoff framed it: it injects the
replacement through a hooked `wpi_clock_ms`, so it is not a route the block reaches
alone, and the defensible statement is about what the block *establishes*.
`noclobber` establishes that a name did not exist at allocation. It establishes
nothing about the object that the later write reaches, and the block's confinement
sentence rested on exactly that.

The repair is `wpi_open_leaf`: the same `noclobber` create-once test, but performed
as an `exec {fd}>` so the descriptor returned **is** the object the open created,
and the write goes through that descriptor. `wpi_capture` (both streams),
`wpi_write_text_leaf`, `wpi_capture_mountinfo_snapshot`, `wpi_build_mount_projection`
and every read-diagnostic stream now write through retained descriptors. The
create-once STOP reasons are unchanged, and `wpi_alloc_leaf` is retained unchanged
for the one leaf a descriptor cannot serve.

```text
RED   LEAF_RACE rc=0 outside_text=CAPTURED outside_bytes=9 payload_left_the_tree=yes
GREEN LEAF_RACE rc=0 outside_text=ORIGINAL outside_bytes=9 payload_left_the_tree=no
LEAF_WRITE_STATIC red_name_appends=12 green_name_appends=0 red_open_leaf=0 green_open_leaf=1
```

**Residual 1 - the status body.** `curl --output <path>` is handed a name, not a
descriptor, so `ro.status.body` is create-once allocated and then re-opened by
curl. That is the same route, unclosed, for one leaf. Closing it needs curl to
write to an inherited descriptor, which is a design change to the row-20 probe,
not a repair.

**Residual 2 - readers.** The write side is bound to the created object; readers
(`wpi_single_record`, the listener reader, `wpi_require_empty_file`, `wpi_sha_file`)
open the leaf path again after the child has run. What the block establishes about
that content is what its record grammar establishes - which is why every reader
STOPs on a record it cannot parse.

**Two repairs considered and rejected, with reasons:**

1. *A per-capture `/proc/self/fd` identity re-check.* The block already uses that
   technique for `EV_LOG`. Applying it to every capture makes each capture spawn a
   second capture to `stat` the first, which is recursive, and doubles both the
   child count and the leaf count. Rejected as disproportionate to a route no
   fixture reaches without an injected function.
2. *An `EV_DIR` ownership/mode precondition*, which would bound *who* could race.
   Rejected because the evidence directory's mode is not a preregistered input:
   RP0-BOOTSTRAP allocates it, and a block that STOPs on a group-writable evidence
   directory would fail a real run for a condition no accepted document requires.
   That is a false STOP invented by the implementer, which is a defect in its own
   right.

Both rejections, and both residuals, are recorded in `SELF_QA_RP7.md` under *What
this QA does not establish* and in the block header - which was narrowed so that it
no longer asserts confinement it does not establish.

## Draft edits (four, all narrow, all forced by a repair)

In `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`, `+14/-3`:

1. **Row 20** - names the 100-599 status grammar explicitly, with `000` and `600`
   as the two named cases, and states that an unparseable status token is an
   inability to evaluate rather than an observed deviation.
2. **Row 21** - adds the malformed-parser-result STOP to the `detail=<d>` list
   (exact token count, preregistered field, that field's expected type, 64 lowercase
   hex) and records that the schema is declared once and the parser refuses a
   declaration that differs from its own table.
3. **Row 22** - records the single NUL-delimited read and why a line-by-line reader
   cannot be used, the byte-conservation requirement, the endpoint-grammar STOPs,
   and the new `bytes=<n>` field on the accepting `B6_listener_inventory` line.
   **This edit is mandatory:** without it the block emits a field the
   preregistration does not declare, which is the defect class the catalogue calls
   pattern 9.
4. **Section 10.1** - one paragraph recording that permitted writes now bind to the
   created object rather than to the name, with the curl `--output` exception and
   the reader residual stated in the same place as the round-5 `/dev/null` note.

No other document was edited. Section 8.2 rows 1-9, rows 10-19, and the round-5
repairs were out of scope and were not touched.

## Catalogue check (thirteen patterns)

- **Pattern 13** (every admitted member needs a terminal disposition) is the primary
  home of F1 and F2, as the kickoff said. The listener repair adds an explicit
  conservation equation across the capture/parse boundary; the status repair gives
  every admitted producer record exactly one terminal disposition - conformant, or a
  STOP naming the grammar rule that failed.
- **Pattern 1** (STOP is not a result) is the shape of F3 and half of F1/F2: an
  inability to evaluate was emitted as a host-state verdict.
- **Pattern 5/12** (grammar completeness): the endpoint grammar and the result-record
  grammar are the modelled-input half; nothing in either is now admitted without a
  rule that can reject it.
- **Pattern 10** (evidence that cannot fail) is F4, and the rule the kickoff stated -
  make the fence's own rc the command's rc, and prove it by making a fence fail on
  purpose - is exactly what the F4 arm does.
- **Pattern 11** (declared vs executed instrument) drove the single schema
  declaration: rather than writing the field/type table twice, the parent hands its
  table to the child and the child refuses to answer unless they are equal.
- **Pattern 9** (the sentence outruns the probe) drove the header narrowing and the
  two residual disclosures.

## Freeze-gate inputs (unchanged from round 5; three)

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` - `<PIN-AT-FREEZE>`,
   `normalised_path_projection_v2` over 21 point paths. No accepting
   `wpi_validate_inputs` arm exists or can exist before it is filled.
2. `WPI_FIXED_TRUSTED_PYTHON` - `<PIN-AT-FREEZE>`, the resolved
   `/usr/bin/python3.<minor>`; a symlinked pin is refused, and that refusal is
   reachable from the production path as of round 5.
3. `WPI_FIXED_EVIDENCE_ROOT` - `<PIN-AT-FREEZE>`, `<REMOTE_BASE>/evidence`,
   carrying the Stage-1 ordering constraint that the base must be allocated before
   these bytes are frozen.

The first action after the deploy channel supplies all three, and before dispatch,
is to execute the accepting-input arm and record it.

## What this round did not do

No commit, no branch action, no `git checkout` of a block file. The Lead verifies
the hash and commits. Rows 1-9 are implemented by no block. Rows 10-19 and the five
round-5 repairs were out of scope and were not re-adjudicated; they are covered
only by the two carried fences, which still pass unchanged.
