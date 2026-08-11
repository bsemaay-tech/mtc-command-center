# VERDICT: REQUEST_CHANGES

TIER: **T0**. APPLIED AUDITOR CONTRACT: fresh Codex `gpt-5.6-sol`, xhigh,
Codex flagship slot. This was the kickoff's policy-read audit of commit
`957ab7983874652fee6b1886213ea5416ad1453c`. I ran only the five published,
marker-delimited harnesses. I did not author, echo, or execute a new shell
mutant; the findings below are construct-class decisions from the published
extractor policy.

## Required findings

### F1 - HIGH - Patterns 12/13, with Pattern 9 overlay: assertion 18 closes only the after-body append class, not the wrapper-line exclusion class

Four mechanisms still discard the complete physical line of each wrapper:
the derivation and line census at `SELF_QA_RP6.md:13385-13439`, the tokenizer's
line-keyed `WRAPDEF` exclusion at `SELF_QA_RP6.md:13817`, and the independent
site count. The new predicate at `SELF_QA_RP6.md:14223-14229` proves only that
each wrapper is one physical line, has no nested brace, and has nothing after
its closing brace. It does not prove that the text *inside* that body is exactly
the one declared result producer.

Therefore an additional emitter command or direct result producer inside the
one-line wrapper body is still removed by all four exclusions, while the
`wrapper_definition_lines_closed` predicate accepts the outer line shape. This
is already inside the fence's emitter vocabulary; it is not a shell form that
the analyzer is entitled to ignore. The statements that the exclusion can now
exclude only the wrapper itself (`SELF_QA_RP6.md:13204,14700` and
`RP6_R15_REPORT_2026-08-11.md:148`) outrun the predicate.

Required repair: remove the whole-line blind spot or bind the complete expected
wrapper body and disposition every result producer on that line. Publish D026
RED/GREEN evidence for the intra-body additional-emitter class. The published
`wrapline` case proves the after-closing-brace class only.

### F2 - HIGH - Patterns 12/13: the function identity is a same-line multiset key, not a source-occurrence identity

`p0_r15_census_funcdefs` (`SELF_QA_RP6.md:14291-14328`) is intentionally a raw,
line-oriented scanner: it does not track shell quoting or inline-comment state,
and it does not model every command-position transition. `p0_r15_ident`
(`:14335-14339`) then sorts records and assigns an ordinal only within identical
`(line, form, name)` triples. Neither side records a column or source span.

That permits correlated cancellation on one physical line: a false raw
candidate from non-executed text can have the same normalized name and form as
a real definition at a position the raw scanner misses. The tokenizer records
the real definition, the raw scanner records the decoy, and the two sorted
identity multisets compare equal even though the records refer to different
source occurrences. The new comparison correctly catches a simple name
mis-disposition and a simple multiplicity mismatch, but it still does not prove
one terminal disposition for each actual definition occurrence.

Required repair: make source occurrence part of the identity (a column/span or
an equivalently discriminating independent mapping), or add a fail-closed rule
that prevents raw false candidates from cancelling missed real definitions.
Publish D026 RED/GREEN evidence for the correlated same-line
false-candidate/missed-definition class. Do not reduce either side with `uniq`.

### F3 - HIGH - Patterns 12/13: inventory mutation is conserved only when the protected variable name appears literally

`p0_r15_name_misuse` (`SELF_QA_RP6.md:14130-14139`) is a lexical exact-name
search after deleting direct parameter references. It catches the published
append case and literal-name mutating forms. It cannot disposition a variable-
mutating builtin whose target is resolved dynamically and therefore contains no
literal protected inventory name in that command. Those builtins remain
admissible command words, and their operands are not classified by the
inventory policy.

Consequently the ordered composition check at `SELF_QA_RP6.md:14160-14208` is
multiset-conserving only for the declared literal assignment shape. It does not
yet establish the broader claim that every mutation capable of affecting the
three inventory variables receives a terminal disposition. This is the same
gap between a lexical mention inventory and the shell's executed target
identity.

Required repair: classify the target identity of every admitted variable-
mutating construct, or forbid dynamic targets and other unsupported target
forms fail-closed. Publish D026 RED/GREEN evidence for the dynamically resolved
mutation-target class while retaining the append and duplicate-composition
fences.

### F4 - MEDIUM - Patterns 9/10: the round-15 report and status claim embedded complete execution evidence while retaining unresolved transcript placeholders

`RP6_R15_REPORT_2026-08-11.md:180-185` and `STATUS_RP6_P0.md:162-168` still
contain unresolved transcript placeholders next to claims that the captured
output is present and that nothing is pending. The kickoff honestly explains
that the implementer session ended during transcript insertion, and this audit
independently reproduced all five required runs, so this did not block
execution. It does make the two delivered evidence claims literally false.

Required repair: replace the placeholders with the Lead/auditor's real permitted
summary evidence, or narrow the documents to cite the external execution record
without claiming the transcript is embedded.

## Policy-soundness decisions

| Question | Decision |
|---|---|
| Is the function census definition-conserving? | **No.** It preserves the multiset of `(line, form, name)` keys but not source-occurrence correspondence; same-line correlated cancellation remains (F2). |
| Does stable identity catch a tokenizer name mis-disposition while the raw line matches? | **Yes for an isolated mismatch; no as a general one-for-one proof.** A same-line false candidate with the same key can cancel a missed real occurrence (F2). |
| Is inventory reconciliation ordered and multiplicity-preserving? | **Yes inside the literal declared composition shape.** The published append and duplicate cases fail. It is not complete for dynamically resolved mutation targets (F3). |
| Does assertion 18 close the wrapper-definition-line append class? | **Partly.** It closes material after the closing brace; it does not close an additional emitter inside the accepted one-line body (F1). |
| Are the property claims narrowed to the true fail-closed property? | **No.** The definition-occurrence, inventory-target, wrapper-exclusion, and embedded-evidence sentences remain broader than their predicates (F1-F4). |

The extractors and still-silent construct classes are therefore:

1. `p0_r15_wrapper_lines_bad` plus the four line exclusions - an additional
   in-body result producer on an otherwise closed wrapper-definition line.
2. `p0_r15_census_funcdefs` / `p0_r15_ident` - same-line correlated raw-decoy
   cancellation of a missed real definition occurrence.
3. `p0_r15_name_misuse` / `p0_r15_inventory_bad` - a dynamically resolved
   target of an admitted variable-mutating construct.

The RP6 census hardening cycle has **not** reached a fail-closed fixpoint, and
the Codex flagship slot remains open.

## Published harness execution

All five marker-delimited bodies were extracted from the commit-identical
`SELF_QA_RP6.md` and executed verbatim from `WPI_BLOCKS_DRAFT`. Output and
stderr were captured to separate local temporary files. Return codes were
`0, 0, 0, 0, 1`; the final `1` is the published success condition for
`R11_R9RED`. All five stderr files were empty.

```text
ASSERT_MET funcdef_census_reconciled identities=26 raw=26 funcdef=26 paren_form=26 keyword_form=0 unmodeled_names=0
ASSERT_MET tool_inventory_conserved halves=2 consumed=P0_RO_TOOLS names=12 handles_bound=6 [P0_STAT=stat P0_READLINK=readlink P0_ID=id P0_GETENT=getent P0_ENV=env rl=readlink]
ASSERT_MET wrapper_definition_lines_closed p0_stop=1 p0_fail=1 nothing_after_closing_brace=1
ASSERT_MET mutant=cmdquote bash_n=0 killed_by=tokenizer_no_unmodeled_syntax(2)
ASSERT_MET mutant=expand bash_n=0 killed_by=tokenizer_no_unmodeled_syntax(1)
ASSERT_MET mutant=continuation bash_n=0 killed_by=tokenizer_no_unmodeled_syntax(2)
ASSERT_MET mutant=handle bash_n=0 killed_by=runtime_command_words_declared(1)
ASSERT_MET mutant=alias bash_n=0 killed_by=alias_indirection_impossible(alias_expand_aliases_enabled)
ASSERT_MET mutant=shadow bash_n=0 killed_by=no_wrapper_shadow(p0_stop=2,p0_fail=1,builtin_shadow=0,tool_shadow=0,prefix_shadow=0),wrapper_definition_lines_closed(wrapper_definition_line_count(p0_stop=2))
ASSERT_MET mutant=toolshadow bash_n=0 killed_by=no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=0,tool_shadow=1,prefix_shadow=0)
ASSERT_MET mutant=funckw bash_n=0 killed_by=no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=1,tool_shadow=0,prefix_shadow=0)
ASSERT_MET mutant=prefixkw bash_n=0 killed_by=no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=1,tool_shadow=0,prefix_shadow=1)
ASSERT_MET mutant=aliasopt bash_n=0 killed_by=tokenizer_no_unmodeled_syntax(1)
ASSERT_MET mutant=aliasdef bash_n=0 killed_by=alias_indirection_impossible(alias_builtin_executed(1))
ASSERT_MET mutant=invpartial bash_n=0 killed_by=tool_inventory_conserved(inventory_half_unextracted(P0_P0_ONLY_TOOLS))
ASSERT_MET mutant=invempty bash_n=0 killed_by=tool_inventory_conserved(inventory_half_unextracted(P0_RP7_RO_TOOLS)),no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=0,tool_shadow=UNDEFINED_EMPTY_INVENTORY,prefix_shadow=0)
ASSERT_MET mutant=defcont bash_n=0 killed_by=funcdef_census_reconciled(raw=29,tok=28)
ASSERT_MET mutant=defmulti bash_n=0 killed_by=funcdef_census_reconciled(raw=27,tok=28)
ASSERT_MET mutant=invappend bash_n=0 killed_by=tool_inventory_conserved(inventory_half_assignments(P0_P0_ONLY_TOOLS=2))
ASSERT_MET mutant=invdup killed_by=tool_inventory_conserved(inventory_composition_unmodeled(P0_RO_TOOLS=[$P0_RP7_RO_TOOLS $P0_RP7_RO_TOOLS $P0_P0_ONLY_TOOLS]))
ASSERT_MET mutant=wrapline killed_by=wrapper_definition_lines_closed(wrapper_definition_line_not_closed(p0_stop))
R15_GRAMMAR_SUMMARY cases=44 pass=44 fail=0 result=PASS
R15_F1_RED_SUMMARY cases=58 pass=58 fail=0 result=PASS
R11_GUARDS_SUMMARY fences=23 pass=23 fail=0 result=PASS
R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS
R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL
```

These results verify every published round-15 and carried case named by the
kickoff. They do not falsify the three construct classes in F1-F3; no new test
is closure evidence until its RED/GREEN behavior is published and executed.

## Thirteen-pattern review

| Pattern | Result |
|---|---|
| 1 - STOP is not a result | No new runtime result-class finding; this audit is static and local. |
| 2 - Whose kernel answered? | Out of scope; no host or namespace was contacted. |
| 3 - The leaf is not the path | No path-admission change in the round-15 QA layer. |
| 4 - Privileged child environment | No privileged or host child ran. |
| 5 - grep is not a parser | No separate finding; the grammar/coverage defects are owned by Pattern 12. |
| 6 - Read status before stdout | Clean for the five audit executions: status and stderr were captured before acceptance. |
| 7 - Nonzero read is not EOF | No reader-completion change in scope. |
| 8 - Name is not identity | No OS/resolver identity claim; source-occurrence identity is owned by Pattern 13. |
| 9 - Sentence outruns probe | **Overlay on F1-F4.** |
| 10 - Evidence that cannot fail | Published cases reproduced; **F4** is the literal evidence-record defect, and F1-F3 lack published falsification. |
| 11 - Declared instrument is not executed instrument | F3 is adjacent but is more specifically a missing analyzer disposition under Patterns 12/13. |
| 12 - Unmodeled must not disappear | **Primary F1-F3 findings.** |
| 13 - Every admitted member needs a terminal disposition | **Primary F1-F3 findings:** in-body emitters, definition occurrences, and dynamic mutation targets can lack dispositions. |

## Scope and identity

- The five audited inputs were byte-identical between anchor `957ab798` and the
  current branch head before execution.
- `RP6-P0.sh` remained unchanged at
  `sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`,
  110817 bytes.
- `SELF_QA_RP6.md` was
  `sha256=0f519f782c19a8dcc321afa98dd366d818bd28e6ca15507e2e1c42b0ba355719`.
- No host or network action occurred. No Git mutation occurred. No existing
  repository file was edited. Pre-existing unrelated working-tree changes were
  preserved. This verdict file is the sole repository write.
- This non-accepting verdict grants no freeze, dispatch, host, deployment,
  credential, broker, exchange, or trading authority.

## Minimum required repair set

1. Close the whole wrapper-line exclusion class, including additional result
   producers inside the accepted body, and publish executed D026 evidence.
2. Make function-definition identity source-occurrence-conserving so a raw
   false candidate cannot cancel a missed real definition on the same line;
   publish executed D026 evidence.
3. Give dynamically resolved targets of all admitted variable-mutating
   constructs a terminal inventory disposition, or refuse them fail-closed;
   publish executed D026 evidence.
4. Correct or narrow the round-15 report/status execution-evidence claims.
5. Rerun the five mandated harnesses verbatim and obtain the next authorized T0
   Codex verdict.
