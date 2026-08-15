# PathScope Option C implementation report — 2026-08-15

Status: `IMPLEMENTED-PENDING-FRESH-FLAGSHIP-AUDIT`

Audit tier: **T1** — local-only, non-economic product code and tests. This implementation
does not accept itself. Under owner decision D1, one fresh flagship execution audit is the
only acceptance authority; a required finding returns the lane to the owner boundary and
does not authorize another implementation round.

## 1. Scope and starting state

The implementation used
`PATHSCOPE_OPTION_C_DESIGN_V2_2026-08-15.md` as the requirements authority, with the review
and F1/F2/F3 audit as context. The task's resolved worktree note superseded its stale
`b38fabe6` sentence: work began on branch
`codex/pathscope-accounting-redesign-20260815` at
`5aa06511fc15a49c6c195ad1f904b8bedf082dbf`, with an empty worktree.

Writes stayed under `WPI_PREREG_DRAFT_ROUND1/`. The only product sources changed are the
named prover and composite parser. `pathscope_option_c_qa.py` is a new local falsification
runner used by the published harness. No parser redesign, host probe, shell-fixture
execution, network, deployment, service, credential, broker/exchange, trading, Pine,
parity, MTC, push, merge, rebase, amend, or external AI/sub-agent action occurred.

## 2. Pre-change evidence

Before source changes, the then-published harness was executed literally from `C:\PSC`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r5_harness.ps1"
```

Measured result: outer rc `0`; stderr `0` bytes. Exact stdout:

```text
R1_BASELINE bytes=49820 sha256=3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
R3_PREREPAIR bytes=124251 sha256=0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7
R4_PREREPAIR bytes=131599 sha256=553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB
R5_REPAIRED bytes=137520 sha256=28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C
BLOCK RP6-P0.sh bytes=107252 sha256=A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617 git_blob=3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c
BLOCK RP7-WPI-RO.sh bytes=99903 sha256=11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4 git_blob=5c9a2f597cceaef80d1cbd0fc100732f4b216cf5
WROTE RED_R1.txt lines=768 sha256=667BF364D0008B3A5869C3ECC2CA16FDAC0C1D60086B3F8FB50CC3E93E70E89D
WROTE GREEN_R5.txt lines=1557 sha256=A534BDCFBBD7B21D874602EB5E90336CBF0796881BE650C3EEC973AF4DBE328C
WROTE RED_R3.txt lines=150 sha256=599B4482C91FCC22F5CA9BCE09261F193F25A4321BF53F650EAA31EEE8C4CBCC
WROTE RED_R4.txt lines=324 sha256=BC142778035AE9B759A47869CCEA86D8C23D9406735BBDB189009188C36CC01B
DETERMINISM find_exec rc1=1 rc2=1 equal=True sha1=f0f0bf2d14d9b504daa6528f230bc1bd4186dc8e9bcc5fd65d8d59b4016f11bd sha2=f0f0bf2d14d9b504daa6528f230bc1bd4186dc8e9bcc5fd65d8d59b4016f11bd
DETERMINISM assign_prefix rc1=1 rc2=1 equal=True sha1=dc1ab295175cb8cf28c9a0bfae247c2311957244714d1108a9e4b13297449ae1 sha2=dc1ab295175cb8cf28c9a0bfae247c2311957244714d1108a9e4b13297449ae1
DETERMINISM c2_list_prefix rc1=1 rc2=1 equal=True sha1=eed53413c5b972bae048263a7304aaeb5b6039f4abc5033d13b54b94596e53bd sha2=eed53413c5b972bae048263a7304aaeb5b6039f4abc5033d13b54b94596e53bd
DETERMINISM c3_ws_relative rc1=3 rc2=3 equal=True sha1=7c905b083423f11b616c6979c5d87b93aaa76b71f16325ea082a495971f38d6c sha2=7c905b083423f11b616c6979c5d87b93aaa76b71f16325ea082a495971f38d6c
DETERMINISM c4_export_quoted rc1=1 rc2=1 equal=True sha1=fa1ff7ce5b208da50c1dc11be72119ec0b906aec22afe15f7e2b124d32230581 sha2=fa1ff7ce5b208da50c1dc11be72119ec0b906aec22afe15f7e2b124d32230581
DETERMINISM RP6-P0 rc1=3 rc2=3 equal=True sha1=01bffdd3692a39ad2bdd025952b2dcba9d793162c2e83e8d83f92ed697ddfdc0 sha2=01bffdd3692a39ad2bdd025952b2dcba9d793162c2e83e8d83f92ed697ddfdc0
DETERMINISM RP7-WPI-RO rc1=3 rc2=3 equal=True sha1=2d87cffcc9f7fee241b5944fa8db62d5d6f652ea4b6af00760540f8e93c7c10a sha2=2d87cffcc9f7fee241b5944fa8db62d5d6f652ea4b6af00760540f8e93c7c10a
```

The pre-change attack run used the same R5 source and real prover command for every fixture:

```powershell
Push-Location "$env:TEMP\pathscope-option-c-baseline"
python -B C:\PSC\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py <fixture>.sh constants.env allowlist.txt
Pop-Location
```

R5 returned `PASS rc=0` for all five `${X:=v}`/`${X=v}` carriers, both F1 inputs, the F2
input, repeated empties, endpoint collision, interleaved empties, and newline words. It
collapsed the duplicate F3 pathname to one projection occurrence and repeated empties to
one PWD projection occurrence. Same-line duplicate assignments were likewise collapsed.
The first scratch generation attempt retained literal PowerShell backtick-`n` characters;
it was rejected as invalid evidence, regenerated with line arrays, and never touched the
repository. Only the corrected run above is used as the RED baseline.

## 3. Design sections 2–6 — accounting model and classification

Implemented as specified:

- `ExpansionSegment`/`ExpansionTrace` preserve ordered literal, escape, quote-elision,
  parameter-expansion, fallback-expansion, and semantic-PWD segments while reconstructing
  the exact rendered value.
- `AdmittedValue`, `MemberOccurrence`, `TerminalDisposition`, and `AccountingFault` are
  frozen records. `AccountingRunContext` assigns stable analyzer/value/member occurrence
  IDs (`A####.V####.<reading>.M####`) across nested analyzers.
- The splitter always emits one whole occurrence; emits `n+1` ordered colon occurrences
  outside protected URI authority spans; emits every word when whitespace has at least two
  non-empty matches; emits word-colon children; and retains duplicates and every zero-width
  empty slice. R5's `pool` ownership and one-empty Boolean are gone.
- Provenance is computed from each member's exact intersecting trace slice. It is never the
  value-wide source union. Semantic empty-colon PWD substitution is represented explicitly.
- The closed `DispositionKind` enum and ordered classifier implement the V2 reason/reading
  rules. Member dispositions never enter generic issue dedupe.
- Per-value validation runs immediately after splitting/classification. Run-level validation
  runs before serialization, and serialized-record reconciliation runs immediately before
  reporting. The checks cover trace reconstruction/ranges, independent reading cardinality,
  raw slices, value/member/global identity, `Counter(M)==Counter(D)`, enum closure,
  provenance equality, reason/reading/shape legality, rules, candidates, and printed rows.
- Any accounting exception or invariant fault emits the four standard headers, a minimal
  `accounting_summary=FAIL`, deterministic `ACCOUNTING_FAULT` rows, and
  `REJECT rc=3 reason=accounting_invariant_failed`; it cannot emit PASS.
- Quote-aware `parameter_assignment_effect` guards the exact registered path-free argv
  exemption. Assignment-effect or ambiguous parameter expansions become coverage
  unresolved; supported fallback and single-quoted controls remain unchanged.

## 4. Design sections 7–8 — output and composite integration

The additive prover grammar uses strict whitespace-free base64url fields and canonical JSON
for raw slices. Assignment-free output emits no accounting prefix or summary. The existing
grouped PATH/ENDPOINT projection remains mandatory; argv-only rows use the unchanged
formatting path, while member-derived evidence adds each contributing `member_id` in stable
order. MEMBER rows, not projection `sources=`, are provenance authority.

`SubprocessPathProver` now:

- accepts only the exact four standard headers and exact named accounting prefixes;
- rejects unknown prefixes, malformed base64/JSON, bad identifiers/enums/counts, duplicate
  headers/values/members, cross-ledger mismatches, invalid reasons/readings, and projection
  omissions;
- enforces conditional summary cardinality and terminal precedence;
- implements the accounting-fault arm and the zero-generic-issue member-unresolved arm; and
- forwards every accounting record in deterministic order.

Live interpretation checks returned PASS for an assignment-free control, STOP with
`prover_member_resolution_incomplete` for F1/F2, PASS for the conserved repeated-empty case,
and FAIL for forbidden duplicates. The exact parser mutations are recorded in §6 below.

## 5. Frozen-R5 RED and Option-C GREEN attacks

The edited harness runs the exact 18-case `$OPTION_C_CASES` list first under frozen blob
`695ca9c951e31f53da9580d41326583d71086bb3`, then under the candidate:

```powershell
Invoke-Suite 'pathscope_prover_R5.py' 'RED_R5_OPTION_C.txt' $OPTION_C_CASES $false
Invoke-Suite $TOOL 'GREEN_OPTION_C_ATTACKS.txt' $OPTION_C_CASES $false
```

Full transcript identities:

```text
WROTE RED_R5_OPTION_C.txt lines=155 sha256=78DD1C3B5EA3C192B681898FA344E2D18A854D7DAC07B8825E30B8DE6BD0F74A
WROTE GREEN_OPTION_C_ATTACKS.txt lines=222 sha256=4905124746EDF459A39FF3DA6B337B53679DC0AA757F98130E0F0746AB5E9E6D
```

The committed QA runner independently invokes both provers and checks the exact rows, IDs,
sources, dispositions, and cardinalities. Literal command and real concise output:

```powershell
python -B MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_option_c_qa.py `
  MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py `
  "$env:TEMP\pathscope-option-c\pathscope_prover_R5.py" `
  MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py `
  "$env:TEMP\pathscope-option-c"
```

```text
ATTACK guard_colon r5_rc=0 candidate_rc=3 closure=assignment_effect_guard
ATTACK guard_true r5_rc=0 candidate_rc=3 closure=assignment_effect_guard
ATTACK guard_echo r5_rc=0 candidate_rc=3 closure=assignment_effect_guard
ATTACK guard_printf r5_rc=0 candidate_rc=3 closure=assignment_effect_guard
ATTACK guard_equal r5_rc=0 candidate_rc=3 closure=assignment_effect_guard
ATTACK control_single_quote r5_rc=0 candidate_rc=0 closure=byte_identical_control
ATTACK control_fallback r5_rc=0 candidate_rc=0 closure=byte_identical_control
ATTACK f1_command_words r5_rc=0 candidate_rc=3 closure=two_unresolved_words
ATTACK f1_uri_bare r5_rc=0 candidate_rc=3 closure=bare_colon_unresolved
ATTACK f2_provenance r5_rc=0 candidate_rc=3 closure=literal_member_sources_none
ATTACK f3_duplicate r5_rc=1 candidate_rc=1 closure=two_distinct_duplicate_members
ATTACK f3_empty r5_rc=0 candidate_rc=0 closure=three_distinct_empty_members
ATTACK adjacent_endpoint r5_rc=0 candidate_rc=3 closure=endpoint_occurrences_and_local_provenance
ATTACK adjacent_interleaved_empty r5_rc=0 candidate_rc=0 closure=five_colon_members_four_empty
ATTACK adjacent_newline r5_rc=0 candidate_rc=3 closure=quoted_newline_two_words
ATTACK adjacent_duplicate_values r5_rc=1 candidate_rc=1 closure=same_line_value_ids_distinct
ATTACK adjacent_mixed_whole r5_rc=3 candidate_rc=3 closure=path_shaped_whole_and_colon_children
ATTACK adjacent_cross_analyzer r5_rc=3 candidate_rc=3 closure=global_analyzer_ordinals_distinct
```

For the three original findings, the candidate's literal report records:

- F1 words: `accounting_summary=OK admitted_value_count=1 member_count=3
  disposition_count=3`; two distinct `words` members are
  `UNRESOLVED_FAIL_CLOSED reason=consumer_word_semantics_unmodeled`; terminal rc 3.
- F1 URI/bare: the URL colon member carries `sources=URL`; the distinct literal bare member
  carries `sources=- disposition=UNRESOLVED_FAIL_CLOSED
  reason=member_consumer_search_unmodeled`; terminal rc 3.
- F2: `$ROOT/lib` carries `sources=ROOT`; `/safe/literal` carries `sources=-`, the exact
  raw slice `{raw_start:26, raw_end:39, raw_text:"/safe/literal", origin:"literal"}`, and
  `reason=member_exact_provenance_missing`; terminal rc 3. The R5 RED projection had
  incorrectly printed `sources=ROOT` for `/safe/literal` and passed rc 0.
- F3 duplicates: two colon members have different IDs and the same forbidden candidate;
  terminal remains rc 1. F3 empties: `::` emits one whole plus three separate empty colon
  members, each with `sources=PWD`; terminal remains rc 0.

## 6. D026 mutation evidence

The runner deliberately falsifies every V2 §10.5 arm. All 15 in-prover mutations returned
rc 3, `summary=FAIL`, at least one accounting fault, no PASS, and terminal
`accounting_invariant_failed`. The two specifically required conservation falsifications
were measured as:

```text
MUTATION M01_delete_disposition rc=3 summary=FAIL faults=4 pass_present=false terminal=accounting_invariant_failed
MUTATION M03_unknown_member rc=3 summary=FAIL faults=7 pass_present=false terminal=accounting_invariant_failed
```

The remaining in-prover arms cover duplicate dispositions, enum closure, member dedupe,
provenance laundering, printed-row suppression, reason/reading violations, cross-value and
cross-analyzer identity collisions, incomplete containers, and summary suppression. Exact
composite/compatibility output:

```text
COMPOSITE_MUTATION M16_removed_member_arm verdict=STOP reason=prover_pass_terminal_mismatch
COMPOSITE_MUTATION M17_fault_wrong_terminal verdict=STOP reason=prover_accounting_terminal_mismatch
COMPOSITE_MUTATION M18a_omitted_header verdict=STOP reason=prover_output_grammar_incomplete
COMPOSITE_MUTATION M18b_duplicate_header verdict=STOP reason=prover_output_grammar_incomplete
COMPOSITE_MUTATION M19a_duplicate_member_id verdict=STOP reason=prover_member_identity_mismatch
COMPOSITE_MUTATION M19b_value_count verdict=STOP reason=prover_value_account_count_mismatch
COMPOSITE_MUTATION M20_projection_omission verdict=STOP reason=prover_member_projection_mismatch
COMPOSITE_MUTATION M21_unknown_prefix verdict=STOP reason=prover_output_unknown_record
COMPAT_MUTATION M22_summary_on_assignment_free byte_equal=false composite=STOP reason=prover_accounting_count_mismatch
COMPAT_MUTATION M23_argv_projection_format byte_equal=false
OPTION_C_MUTATIONS PASS arms=23 checks=25
```

The complete 44-line mutation/attack transcript is emitted literally by the published
harness as `OPTION_C_MUTATIONS.txt`, SHA-256
`4AC0B546532E76F58DB83DE44DD875BE4A53D0E116547251A4E40687A1C9ADD0`.

## 7. Regression and determinism

The edited harness was mechanically extracted from the second `powershell` fence in
`SELF_QA_PATHSCOPE.md` and run verbatim:

```text
OUTER_RC=0 STDOUT_BYTES=7661 STDERR_BYTES=0
HARNESS_BYTES=37382
HARNESS_SHA=61FB09D27F53BF3F97902849215FF4AC9BEE9B3DC19846BBA3AE2F4B8AA27FC7
HISTORICAL_FENCES PASS red=3 retired_green_r5=true
FULL_SUITE_DETERMINISM equal=True sha256=B70F54B11703220DA272B526C5C2564A3D08CA67C8B073F2B81857B804D4EE64
REGRESSION_RC PASS cases=109 deltas=c2_benign_words:0->3,c3_colon_whole:1->3
REGRESSION_BYTES PASS identical_blocks=60
```

Transcript identities:

```text
RED_R1.txt lines=768 sha256=667BF364D0008B3A5869C3ECC2CA16FDAC0C1D60086B3F8FB50CC3E93E70E89D
RED_R3.txt lines=150 sha256=599B4482C91FCC22F5CA9BCE09261F193F25A4321BF53F650EAA31EEE8C4CBCC
RED_R4.txt lines=324 sha256=BC142778035AE9B759A47869CCEA86D8C23D9406735BBDB189009188C36CC01B
R5_BASELINE.txt lines=1557 sha256=A534BDCFBBD7B21D874602EB5E90336CBF0796881BE650C3EEC973AF4DBE328C
GREEN_OPTION_C.txt lines=3442 sha256=B70F54B11703220DA272B526C5C2564A3D08CA67C8B073F2B81857B804D4EE64
GREEN_OPTION_C_REPEAT.txt lines=3442 sha256=B70F54B11703220DA272B526C5C2564A3D08CA67C8B073F2B81857B804D4EE64
```

The 60 byte-identical blocks include every V2 §9.1 assignment-free/argv-only requirement,
`c4_export_opaque`, and both placeholder real-block runs. All assignment-admitting blocks
use their new accounting fence. RP6-P0 and RP7-WPI-RO remain rc 3 under placeholder and real
constants. The seven retired per-case digests are explicitly re-fenced in the published
harness stdout.

Projection review found 11 R5-to-Option-C row deltas after removing the new `member_id`
suffix. Ten are exact-provenance corrections (`ROOT`/`URL` to `NONE`) required by V2. The
eleventh is RP7-WPI-RO line 681: R5 trimmed the quoted rendered value `" / "` to the false
candidate `/`; Option C preserves the exact whole occurrence and fails it closed as
`member_normalization_failed`. The run remains rc 3 and the failure fact becomes stricter;
this row-level reason is declared rather than absorbed into a fence.

## 8. Runtime and identity evidence

Commands and literal results:

```text
python --version
Python 3.14.2

python -B -c "... ast.parse(..., feature_version=(3,12)) ..."
AST_PARSE_3_12 PASS pathscope_prover.py
AST_PARSE_3_12 PASS composite_pathproof.py
AST_PARSE_3_12 PASS pathscope_option_c_qa.py
AST_RC=0

py -3.12 -V
No suitable Python runtime found
PY312_RC=103
```

Installed-runtime direct execution:

```text
PROVER_DIRECT_RC=1 STDOUT_BYTES=483 STDERR_BYTES=0
COMPOSITE_DIRECT_RC=0 STDOUT_BYTES=701 STDERR_BYTES=0
```

The prover direct case was the existing forbidden `literal.sh`, so rc 1 is its expected
semantic result and proves execution reached normal reporting. Composite `--help` returned
rc 0. An actual Python 3.12 interpreter could not be run because it is not installed; this
is the only runtime check that could not be performed.

Required dual identity for `pathscope_prover.py`:

| form | bytes | SHA-256 | Git OID |
|---|---:|---|---|
| working tree | 185272 | `3DA28F8EC3F4762836350293D8B51A797E2B2A3EAA1D06EEE36C768F706C969F` | not applicable |
| staged Git blob | 185272 | `3DA28F8EC3F4762836350293D8B51A797E2B2A3EAA1D06EEE36C768F706C969F` | `db220dc6edf117cd1e1627bbed36fda3cb0b6057` |

Both forms happen to be byte-identical here; they were measured independently and are not
assumed equivalent.

## 9. Deviations, residuals, and audit handoff

No implementation deviation from accepted V2 is known. The parser/traversal and lexical
allowlist semantics outside the named seam were not redesigned.

The V2 §11 residuals remain. In particular: assignment-bearing parameter expansion is
guarded and stopped, not semantically executed; one-member bare scalars retain the disclosed
consumer-semantics hole; union-of-readings can over-reject; attached option paths are not
extracted; absolute byte columns are unavailable; generic non-member issues may still
dedupe; no host identity is proven; downstream admission absence is not independently
re-parsed; and the pre-existing composite endpoint `ALLOW-LEXICAL` versus `ALLOW` mismatch
can over-STOP an allowed endpoint. That endpoint mismatch was observed and left unchanged
under V2 residual 11.10; it cannot create a false PASS.

The fresh auditor should receive only the frozen diff, accepted V2, this report, the literal
published harness stdout, and the RED/GREEN and mutation transcripts—not this implementer
session context. If it finds a required change, stop at the owner boundary.
