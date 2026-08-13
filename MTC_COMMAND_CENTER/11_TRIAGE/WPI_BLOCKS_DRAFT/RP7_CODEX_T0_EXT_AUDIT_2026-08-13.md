# RP7 rows 1-9 extension - Codex T0 flagship audit

**Verdict: REQUEST_CHANGES** (3 REQUIRED, 1 NIT)

Auditor: Codex, fresh independent non-implementer session. Session-header model:
`gpt-5.6-sol`. Tier T0, xhigh per kickoff. Date: 2026-08-13.

The round-3 `[Install]` repair is correct, and the labelled row-1 preregistration
amendment is an adequate documentary amendment. The published rebuild fence also
executes cleanly and its invariant transcript matches the document. Acceptance is
withheld because the block does not implement all inability arms of the row-1
amendment, the row-6 parser mis-models a documented systemd continuation form, and
the row-9 tokenizer silently drops an unmodeled token and still passes.

## Identities and mandatory execution

- `RP7-WPI-RO.sh`: **127038 bytes**, SHA-256
  `ac73485ff75ab6e731bf1bc137ae77f7074cab04700603ab71cba1c591141fe3`.
  This matches the kickoff and commit `30f638f1bf461768b6258352bb79a0ea38484b42`.
- `SELF_QA_RP7.md` audited identity: **416814 bytes**, SHA-256
  `576404972772a0717f1868929083e44765dd3775a1fa15b1b8c427b20172613a`.
- Both artifacts contain **0 CR bytes**. WSL `bash --noprofile --norc -n
  RP7-WPI-RO.sh` returned **rc 0** with no diagnostic.
- History identities independently verified from Git objects:
  - r9 `437593c5...`: 108301 bytes / `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`.
  - round 2 `f184139b...`: 127046 bytes / `a2ec1d0c47db53a756b7abe0803e7c6e62d42dd4c6b69934332c2eb501c714ad`.
  - round 3 `30f638f1...`: 127038 bytes / `ac73485ff75ab6e731bf1bc137ae77f7074cab04700603ab71cba1c591141fe3`.

I ran the kickoff's WSL rebuild command verbatim, in the foreground from
`WPI_BLOCKS_DRAFT`. Result: **rc 0**, empty stderr, 60 transcript lines:

```text
D026_ROWS=52 RED=24 GREEN=24 CONTROL=4 D026_CONTROL=2 FAIL_MARKERS=0
D026_SUMMARY rows=1-9 red_green_pairs=24 controls=4 result=PASS instrument=RP7-WPI-RO.sh extracted_block_functions=yes block_logic_reimplemented=no
```

The actual transcript and `SELF_QA_RP7.md:296-355` are identical after normalizing
only the disclosed host-derived `HARNESS_ATTESTED_MOUNTINFO sha256=` value. All 59
other lines match exactly. My WSL instance produced `be94739e...82dbb2`; the pasted
run records `78388f0d...b1e15`. The block identity, clean-fragment identity, every
case disposition, counts, and summary all match.

## REQUIRED-1 - Row 1 does not implement the amended STOP domain

The labelled amendment is clear and adequate as prose. It requires the
`ActiveState` record to be present and declares
`B2_STOP reason=system_manager_unreachable operation=show rc=<n> detail=<d>` for
invocation, incomplete-output, or grammar failure before comparison
(`WPI_PREREGISTRATION_DRAFT.md:1115-1127`). The binding system-manager rule repeats
that an unevaluable manager/query/parse result uses `operation=show`
(`:1239-1242`).

The delivered code implements only part of that contract:

- Whole-table parse failures use `unit_definition_unreadable`, not the amended
  row-1 reason (`RP7-WPI-RO.sh:766`; the published truncated-table arm reproduces
  this at `SELF_QA_RP7.md:328`).
- An absent `ActiveState` record uses `system_manager_unreachable prop=ActiveState`,
  not `operation=show` (`RP7-WPI-RO.sh:768`, through `wpi_show_get:566-570`).
- `wpi_require_show_value_grammar` rejects only non-printable bytes and admits the
  empty string (`:572-575`); the next line classifies that unparseable empty state
  as a host-state FAIL (`:769-770`).

I drove both untested arms through the extracted production function:

```text
B2_STOP reason=system_manager_unreachable prop=ActiveState rc=0 detail=property_record_absent query=ActiveState
PROBE active_absent rc=3
B2_FAIL reason=unit_not_active state= expected=active
PROBE active_empty rc=1
```

The first is an undeclared result grammar; the second is a Pattern-1 false FAIL.
This is also a Pattern-9 code-versus-preregistration divergence. Repair every
query/table-parse/missing-record/value-grammar inability before the first
`ActiveState` comparison to the amended `operation=show` STOP grammar, and define
the accepted `ActiveState` token grammar so an empty or unknown token cannot become
a state observation. Add executed D026 falsifications for table parse failure,
missing `ActiveState`, and empty/invalid `ActiveState`, with RED on these bytes and
GREEN on the repair.

## REQUIRED-2 - Row 6 ends a continuation at an intervening comment

The row-6 parser resets `continued` from the physical comment line
(`RP7-WPI-RO.sh:658-663`). That is not systemd's line grammar. The installed
`systemd.syntax` manual states that when comment lines follow a line ending in a
backslash, the comment block is ignored and the continued line is concatenated
with whatever follows the comment block. Section D.5 requires an `[Install]` token
after a continuation not to trigger `install_section_present`
(`ROWS_1_9_OPTIONS_CODEX_2026-08-10.md:341`).

I supplied one continued directive, an intervening comment, then `[Install]` to
the real extracted row-6 function. The block returned:

```text
B2_FAIL reason=install_section_present path=/tmp/rp7_rows_1_9_rebuild_evidence/unit/mtc-bridge-first-start.service
PROBE r6_comment_bridge rc=1
```

The same bytes passed `systemd-analyze verify` with rc 0 and reported
`Unknown key 'WantedBy' in section [Unit], ignoring.` That diagnostic proves
systemd concatenated `[Install]` into the preceding `Description` value; it did not
open an Install section. The block therefore emits a false host-state FAIL. This is
a Pattern-5 grammar defect and Pattern-1 classification defect.

Carry continuation state across intervening blank/comment lines exactly as
systemd does, and add a D026 control for this form. Demonstrate current RED (the
false FAIL above) and repaired GREEN with the production parser.

## REQUIRED-3 - Row 9 silently drops an unmodeled token and passes

Row 9 requires the *complete* effective `Environment` value to be parsed under
systemd's tokenized environment grammar, with a grammar error producing STOP
(`ROWS_1_9_OPTIONS_CODEX_2026-08-10.md:114`; preregistration `:1097`). The parser
instead silently continues past every token without `=` (`RP7-WPI-RO.sh:732-736`),
then accepts if the target assignment alone is correct (`:739-740`).

Executed through the extracted production function:

```text
B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed parser=systemd_environment_tokenizer occurrences=1
PROBE env_unmodeled rc=0
```

The input was `UNMODELED_TOKEN MTC_BRIDGE_START_MODE=credential_free_disarmed`.
The first token is not a valid environment assignment; it must make the complete
record unevaluable, not disappear. This is Pattern 12 directly and violates
Pattern 13's terminal-disposition rule.

Require every token to receive a valid assignment disposition, including a valid
environment-variable name, and STOP on any unconsumed or malformed token before
target semantics. Add a D026 falsification showing these bytes pass the malformed
record and the repaired bytes STOP it; retain the existing quoted, duplicate, and
substring controls.

## Round-3 repair adjudication

1. **Claude REQUIRED-1 (`[install]`) - CLOSED.** The delivered parser uses exact
   `m.group(1)=="Install"` at `RP7-WPI-RO.sh:667`. An independent read-only
   `systemd-analyze verify` probe produced one `Unknown section 'install'. Ignoring.`
   diagnostic for lowercase `[install]`, zero for canonical `[Install]`, and rc 0
   for both. The restored case-variant CONTROL is correct.
2. **Claude REQUIRED-2 (row-1 amendment record) - DOCUMENTARILY CLOSED.** The
   labelled block at `WPI_PREREGISTRATION_DRAFT.md:1115-1127` preserves the
   original sentence, declares the `ActiveState` predicate and `operation=show`
   STOP grammar, cites section D.4 authority, and the later system-manager rule
   explicitly says it supersedes the original route (`:1239-1242`). The amendment
   is adequate; REQUIRED-1 above is a block-conformance defect, not a request to
   rewrite the amendment.
3. **Round-3 report section - materially accurate.** Its repair descriptions,
   identities, and 24-pair/4-control terminal summary reproduce. See the NIT below
   for one stale earlier paragraph.
4. **Row-8 pin disclosure - adequate.** The fence honestly labels the values as
   asserted renderings, says host fidelity is not established, and keeps
   derivation as a freeze-time act. `CapabilityBoundingSet=''` is specifically
   named as highest risk. This audit does not treat absent host derivation as a
   repair finding, per kickoff.
5. **Carried C1 / descriptor discipline - no new implementation class.**
   `wpi_alloc_leaf` has zero matches. `wpi_capture` is byte-identical to r9
   (3884 bytes, SHA-256 `927ecca34598d62f0ed3590d646f3ee8caa998cdf8568da771876c62d4cdaf1e`),
   as is `wpi_assert_regular_digest` (1001 bytes, SHA-256
   `3a6dd84879357821a1d59195b2d797dbf9ed187e71a4c0f820cbbd3d0849296f`).
   Row 6 reads the fragment through the already-open descriptor. Rows 6-7 do
   exercise the existing mount-guard helper, so the separately disclosed C1
   projection-digest name re-resolution remains present; this round neither
   repairs it nor introduces a second allocator/reader form.

## Thirteen-pattern adjudication

| Pattern | Adjudication |
|---|---|
| 1 STOP is not a result | **Finding:** empty `ActiveState` and row-6 comment-bridged continuation become false FAILs. |
| 2 Whose kernel answered? | Clean for this extension: the terminal claim remains limited to the attested execution domain that answered. |
| 3 Leaf is not path | Component/mount binding is retained; carried C1 remains disclosed as above. |
| 4 Child environment | Clean: pinned absolute tools, cleared environment, and trusted Python under `-I -S`. |
| 5 Parser completeness | **Finding:** row-6 continuation grammar is incomplete. |
| 6 Status before stdout | Clean ordering: rc/diagnostics/completeness precede semantics in both bounded captures. |
| 7 Nonzero read is not EOF | Clean in the show-table reader; truncated and hard-read forms STOP. |
| 8 Name is not identity | No new rendered-name identity comparison. |
| 9 Sentence outruns probe | **Finding:** row-1 emitted grammar does not match its amendment; report-count NIT below. |
| 10 Evidence can fail | Fence is literal, reproducible, and arithmetic is honest for the cases it contains; the findings expose missing discriminators. |
| 11 Declared instrument not executed | Clean: the fence extracts the delivered functions, and production binds all invoked tools. |
| 12 Unmodeled input disappears | **Finding:** row 9 ignores a non-assignment token and passes. |
| 13 Terminal disposition | **Finding:** the ignored row-9 token has no disposition; property-table members are otherwise conserved and duplicate-checked. |

## NIT-1 - stale count in the build report

`RP7_ROWS_1_9_REPORT_2026-08-13.md:97` still says the current rebuild produced 23
RED/GREEN pairs and 3 controls. The current summaries at `:119`, `:220`, and
`:303`, the round-3 section, and my run all establish 24 pairs and 4 controls.
Label the 23/3 sentence as the round-2 historical count or update it. This does not
affect the executable verdict.

## Delta gate and standing

The governing verdict path was absent at session start and immediately before
this write. This session wrote exactly:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_EXT_AUDIT_2026-08-13.md
```

No Git mutation was performed: no stage, commit, checkout, reset, stash, branch,
or push. The shared-worktree HEAD advanced concurrently from the audited round-3
commit line to `5abd997ee344ab107b62316d4b74651cf1fce816` during this audit; the subject
and SELF_QA identities remained unchanged and all audited tracked files were clean
against that HEAD immediately before this write. Pre-write whole status contained
135 pre-existing paths and is advisory only. All audit scratch was under guarded
`/tmp` directories and was removed by traps.

This verdict does **not** fill the Codex T0 acceptance slot. Repair and re-audit are
required under the T0 round cap.
