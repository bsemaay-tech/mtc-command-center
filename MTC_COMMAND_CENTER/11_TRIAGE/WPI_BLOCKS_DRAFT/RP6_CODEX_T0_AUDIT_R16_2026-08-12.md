# VERDICT: PASS-WITH-NITS

TIER: **T0**. APPLIED AUDITOR CONTRACT: fresh Codex `gpt-5.6-sol`, xhigh,
Codex flagship slot. This was the kickoff's read-only, policy-soundness audit of
commit `753894bada19d90db007b6e54f1b45475c92077a`. There are **zero required
repairs**. The exact-byte-span census is a fail-closed fixpoint for every
construct already in the published detection vocabulary, and the Codex flagship
slot closes.

I ran only the five published, marker-delimited harnesses. I did not author,
echo, or execute a new shell mutant. The findings below are construct-class
decisions from the published source policy and the published D026 harnesses.

## Published harness execution

All five bodies were extracted from the commit-identical `SELF_QA_RP6.md` and
executed verbatim from `WPI_BLOCKS_DRAFT`. Output and stderr were captured to
separate files under an isolated local temporary directory. Return codes were
`0, 0, 0, 0, 1`; the final `1` is the published success condition for
`R11_R9RED`. Every stderr file was empty.

```text
R16_GRAMMAR_SUMMARY cases=50 pass=50 fail=0 result=PASS
R16_F1_RED_SUMMARY cases=52 pass=52 fail=0 result=PASS
R11_GUARDS_SUMMARY fences=25 pass=25 fail=0 result=PASS
R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS
R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL
```

The last summary is the intentional RED result preserved by `R11_R9RED`; its
recipe returned rc 1 rather than masking that status.

The round-16 GREEN run established the source-span premises and the two named
round-15 closures:

```text
ASSERT_MET funcdef_census_reconciled identities=26 raw=26 funcdef=26 paren_form=26 keyword_form=0 unmodeled_names=0
ASSERT_MET wrapper_definition_bytes_bound declared=2 occurrences=1/1 producers_per_declaration=1 spans_excluded=2
ASSERT_MET producer_spans_reconciled spans=163 raw=163 tokenizer=163 excluded_wrapper_spans=2
ASSERT_MET inventory_variable_targets variable_targets=113 inventory_targets=0 dynamic_targets=0
ASSERT_MET mutant=wrapline killed_by=census_covers_every_emitter(164!=165),grammar_closed,tokenizer_no_unmodeled_syntax(1),wrapper_definition_lines_closed(wrapper_definition_line_not_closed(p0_stop)),wrapper_definition_bytes_bound(wrapper_definition_bytes_occurrences(0))
ASSERT_MET mutant=inbody killed_by=census_covers_every_emitter(164!=165),grammar_closed,tokenizer_no_unmodeled_syntax(1),wrapper_definition_bytes_bound(wrapper_definition_bytes_occurrences(0))
ASSERT_MET mutant=spandecoy bash_n=0 killed_by=funcdef_census_reconciled(raw=27,tok=27)
```

`R16_F1_RED` mechanically extracted both published fences, applied the mutants
published by `R16_GRAMMAR`, and showed RED against round 15 and GREEN against
round 16 for `inbody` and `spandecoy`. It also executed the unresolved-span
boundary and confirmed that round 16 refuses it. The 52/52 summary is therefore
the D026 record for the two named defects, not a prose claim about test coverage.

## Policy-soundness decision

### 1. Every wrapper exclusion is bound to exact declared bytes

`SELF_QA_RP6.md:16604-16642` declares the two complete wrapper-definition lines
and makes the three text mechanisms discard a record only when its line text is
byte-identical to one declaration. `p0_r16_wrapper_bytes_bad` at
`:17117-17159` independently requires:

- exactly two declared wrapper lines;
- exactly one byte-identical occurrence of each line in the block;
- exactly one result producer in each declared line;
- no other definition of either wrapper; and
- exactly two resolved and exactly two excluded tokenizer spans.

Any byte added anywhere inside or after a wrapper body makes the line cease to
match the declaration. Its producer is then visible to the derivation, the raw
producer census, and the tokenizer. If the declaration premise itself cannot be
proved, `wrapper_definition_bytes_bound` makes the whole verdict nonzero. There
is therefore no wrapper region whose bytes are accepted but not bound.

### 2. Function definitions reconcile by source occurrence, not by line key

The raw census at `SELF_QA_RP6.md:16948-16996` and the tokenizer at
`:16314-16330` both record the column of the definition-name token. The common
identity function at `:16999-17004` orders `(line, column, form, name)` records
and adds an ordinal only to preserve multiplicity. Neither side uses `uniq`, and
the two complete streams are compared with `cmp` at `:17227-17232` and
`:17455-17470`.

A real definition the raw scanner misses therefore leaves an unmatched
tokenizer disposition. A false raw candidate remains unmatched. A false
candidate and a real definition at different positions on one line have
different columns and cannot cancel even when line, form, and name agree. Two
records can share the same identity only if they name the same source token;
that token cannot simultaneously be non-executed decoy text and a real shell
definition under the same parse.

### 3. Every detected producer has a terminal span disposition

The raw producer census at `SELF_QA_RP6.md:17018-17056` emits one record per
occurrence and the tokenizer emits one `EMIT` record per detected command-word
occurrence. `p0_r16_span_ident` retains multiplicity and the streams are compared
one-for-one with `cmp` at `:17241-17247` and `:17540-17552`. The sole exclusion
is the one declared producer span in each exact wrapper line.

The tokenizer's fragment mapping is explicit. Main-source and command-
substitution fragments are literal source substrings with resolvable line and
column positions. A normalized fragment such as a trap action is marked inexact.
`funcdef` and `emitspan` at `SELF_QA_RP6.md:16314-16346` emit an `UNMODELED`
record whenever the fragment or column cannot be resolved; an aborted scan emits
`SCAN_ERROR`. Assertion 9 counts either class and fails the whole verdict. An
unresolvable source occurrence is therefore refused, never silently excluded.

### 4. No remaining span-identity cancellation class

Within the published detection vocabulary, the independent raw mechanisms may
over-detect and the tokenizer may refuse a modeled position, but neither outcome
can disappear:

- an extra raw occurrence has no tokenizer identity and fails reconciliation;
- an extra tokenizer occurrence has no raw identity and fails reconciliation;
- different source positions cannot compare equal;
- duplicate records at one position receive different ordinals; and
- an unresolvable position produces `UNMODELED`/`SCAN_ERROR` and a nonzero
  verdict.

The remaining disclosed boundary -- a shell shape neither mechanism models --
is not claimed closed. That is outside the kickoff's question about constructs
already in the detection vocabulary and is stated as a residual rather than
silently admitted.

## Property-claim review

The current claim at `STATUS_RP6_P0.md:108-154` is narrowed to source syntax,
static binding, and conservation. It explicitly denies equivalence to bash's
parser and denies any runtime claim about handle values or function behavior.
It distinguishes span-exact tokenizer exclusion from byte-exact text exclusion,
states that dynamic mutation targets are refused rather than resolved, and says
that any unresolvable span makes the fence fail. The detailed residuals in the
status and `SELF_QA_RP6.md` also name the line+column representation, inexact
fragment boundary, static-only scope, and shapes neither mechanism models.

Those are the true span-level fail-closed properties. I found no broader
structural claim that would reopen the round-15 wrapper or correlated-decoy
classes.

## Optional nit - LOW - Patterns 9/10: recovered-session placeholders remain

The kickoff truthfully discloses the round-16 process exit and designates the
Lead's verbatim run as evidence of record. This audit independently reran all
five required harnesses and records their real summaries above, so the missing
embedded transcripts do not weaken acceptance or leave a required repair.

For documentary consistency only, a future authorized cleanup may remove the
still-unresolved placeholders at `RP6_R16_REPORT_2026-08-11.md:277`,
`STATUS_RP6_P0.md:199`, and `SELF_QA_RP6.md:17887,18170,18291,18336`, and narrow
the report's contrary statement at `RP6_R16_REPORT_2026-08-11.md:188-189` that
those placeholders were resolved. This is optional because the kickoff
supersedes the interrupted embedding step and the independent execution record
now exists in this verdict.

## Thirteen-pattern review

| Pattern | Decision |
|---|---|
| 1 - STOP is not a result | No new result-class mapping is introduced by this static QA-layer change. Unmodelled source state makes the fence nonzero rather than producing a host-state claim. |
| 2 - Whose kernel answered? | No host, namespace, service, or privilege-domain observation was made. |
| 3 - The leaf is not the path | No path-admission logic or block byte changed. |
| 4 - Privileged child environment | No privileged child or host-side interpreter ran. The published local harnesses used fresh non-profile bash processes. |
| 5 - grep is not a parser | No separate required finding. Grep/awk text mechanisms are cross-checked against the tokenizer and fail on disagreement; the broader coverage question is owned by Pattern 12. |
| 6 - Read status before stdout | Return codes and stderr were captured separately. No harness was accepted before its status was adjudicated. |
| 7 - Nonzero read is not EOF | No reader-completion change is in scope. Scan failures are explicit `SCAN_ERROR` and non-accepting. |
| 8 - The name is not the identity | Closed for this source-occurrence question: identity is line+column+form+name+ordinal, not the rendered name alone. |
| 9 - The sentence outruns the probe | The structural property is narrowed correctly. Optional documentary nit above for interrupted transcript-embedding claims. |
| 10 - Evidence that cannot fail | The two defect classes were RED against round 15 and GREEN against round 16 through the published 52/52 D026 harness. Optional placeholder nit above. |
| 11 - Declared instrument is not executed instrument | No new missing instrument path found in this QA-layer audit; the actual published fences, not paraphrased extracts, were executed. |
| 12 - Unmodeled must not disappear | PASS. Unknown syntax, unresolved spans, scan errors, unmatched raw records, and unmatched tokenizer records all make the verdict nonzero. |
| 13 - Every admitted member needs a terminal disposition | PASS. Definitions and producers reconcile one-for-one by source span with multiplicity preserved and no `uniq`. |

## Scope and identity

- `RP6-P0.sh` remained unchanged at
  `sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`,
  110817 bytes.
- The current branch head was `affd19c35c7e4db2ea30ab83f47ad020d8615e09`;
  the audited RP6 bytes were unchanged from `753894ba`, and the only later
  `WPI_BLOCKS_DRAFT` change was the audit kickoff itself.
- No host or network action occurred. No Git mutation occurred. No existing
  repository file was edited. Pre-existing unrelated untracked scratch and log
  files were preserved. This verdict file is the sole repository write.
- This accepting audit closes only the Codex flagship slot for the round-16
  census hardening cycle. It grants no freeze, dispatch, host, deployment,
  credential, broker, exchange, ARM, order, or trading authority.

