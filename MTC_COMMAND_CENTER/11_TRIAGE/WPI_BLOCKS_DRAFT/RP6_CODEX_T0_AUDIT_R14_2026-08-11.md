# VERDICT: REQUEST_CHANGES

TIER: **T0**. APPLIED AUDITOR CONTRACT: fresh Codex `gpt-5.6-sol`, xhigh,
Codex flagship slot; round cap 3. This is a policy-read audit of commit
`0f6b3ec9`. No new shell mutant was authored, echoed, or executed.

## Required findings

### F1 - HIGH - Patterns 12/13: the function-definition census is still line-conserving, not definition-conserving

`SELF_QA_RP6.md:11453` preserves a backslash-newline as an escaped token;
`SELF_QA_RP6.md:11537` then accepts the next tokenizer word as a
function-keyword definition name without requiring a non-empty, literal name.
The independent census at `SELF_QA_RP6.md:11952` records only candidate physical
line numbers, and assertion 16 at `SELF_QA_RP6.md:12060` compares sorted unique
line-number sets rather than stable definition identities.

That leaves two silent-loss classes inside the fence's existing definition
vocabulary. First, when a function-keyword definition's name is separated from
the keyword by a shell line continuation, Bash removes the continuation before
parsing, while this tokenizer can disposition the continuation token instead of
the actual name; the raw census and tokenizer can still report the same physical
line. Second, multiple definitions on one physical line collapse to one member
on both sides, so one missing disposition is masked by another definition on the
same line. In either class the line-level `cmp` can succeed without proving that
the actual definition name reached the wrapper/builtin/tool/prefix shadow checks.

Required repair: assign each raw definition a stable identity containing at
least physical location, ordinal, normalized name, and form; compare those
records one-for-one without `uniq`; reject empty, escaped, expanded, or otherwise
unsupported definition-name tokens as unmodeled. Publish and execute D026
RED/GREEN evidence for the continuation and same-line multiplicity classes.

### F2 - HIGH - Patterns 12/13: the inventory conservation chain silently omits admitted assignment and duplicate-composition classes

The tokenizer explicitly recognizes both direct and append-style shell
assignments at `SELF_QA_RP6.md:11549`. The inventory assignment censuses at
`SELF_QA_RP6.md:11886` and `SELF_QA_RP6.md:11896`, however, search only for a
declared variable immediately followed by direct assignment. An append-style
assignment to either declared half or to the consumed inventory therefore
receives no inventory disposition and no unmodeled record. The original direct
assignment remains count one, so the conservation chain can pass over an
inventory different from the one the block consumes.

There is a second duplicate-loss path at `SELF_QA_RP6.md:11901`: composition
references are reduced with `sort -u` and checked by set equality. Repeating a
declared half is therefore silently collapsed, even though the round-14 contract
says duplicate inventory shape fails closed. The member-duplication count at
`SELF_QA_RP6.md:11905` covers extracted members inside the two halves; it does
not restore multiplicity discarded from the consumed composition.

Required repair: inventory every assignment operator or mutating builtin that
can affect the three declared variables and fail closed on unsupported mutation;
then reconcile an ordered multiset of composition references, with exactly one
terminal disposition per assignment and per reference. Publish and execute D026
RED/GREEN evidence for append mutation and duplicate composition.

## Policy-soundness decisions

| Extractor | Decision | Reason |
|---|---|---|
| FUNCDEF | **Not fail-closed** | Assertion 16 compares unique line sets, not definition identities. It can preserve the line while losing the normalized function name or one of multiple same-line definitions (F1). |
| Tool inventory | **Not fail-closed** | Append-style mutation is in the tokenizer's assignment vocabulary but absent from the conservation census; duplicate composition references are collapsed by set normalization (F2). |
| Alias / shopt | **Fail-closed within the stated static domain** | Direct and prefixed alias builtins are recorded at classified command position, nested command substitutions are scanned, and expanded, escaped, or unknown `shopt` operands/options become unmodeled. The stated exclusion for runtime handle values and function behavior remains material. |

The round-13 property overclaims are therefore **not yet narrowed to the true
fail-closed property**. `STATUS_RP6_P0.md:78` claims exactly one `FUNCDEF`
disposition per definition, and `STATUS_RP6_P0.md:88` claims every unreadable
definition or unconserved inventory shape fails. F1 and F2 falsify those two
sentences. The same overclaim appears at `SELF_QA_RP6.md:12942`. This is the
Pattern-9 overlay on the two required extractor findings.

## Published harness execution

All five published marker-delimited harnesses were extracted from the
commit-identical `SELF_QA_RP6.md` and executed without editing their bodies.
Stdout, stderr, and return status were captured separately in a fresh local
temporary directory. Stderr was empty for all five.

```text
ASSERT_MET funcdef_census_reconciled raw_lines=26 funcdef_lines=26 paren_form=26 keyword_form=0
ASSERT_MET tool_inventory_conserved halves=2 consumed=P0_RO_TOOLS names=12 handles_bound=6 [P0_STAT=stat P0_READLINK=readlink P0_ID=id P0_GETENT=getent P0_ENV=env rl=readlink]
ASSERT_MET alias_indirection_impossible_by_construction (lexical:no_expand_aliases_no_alias_definition; semantic:alias_builtins=0 shopt_invocations=0 expand_aliases_enabled=0)
ASSERT_MET mutant=funckw bash_n=0 killed_by=no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=1,tool_shadow=0,prefix_shadow=0)
ASSERT_MET mutant=prefixkw bash_n=0 killed_by=no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=1,tool_shadow=0,prefix_shadow=1)
ASSERT_MET mutant=aliasopt bash_n=0 killed_by=tokenizer_no_unmodeled_syntax(1)
ASSERT_MET mutant=aliasdef bash_n=0 killed_by=alias_indirection_impossible(alias_builtin_executed(1))
ASSERT_MET mutant=invpartial bash_n=0 killed_by=tool_inventory_conserved(inventory_half_unextracted(P0_P0_ONLY_TOOLS))
ASSERT_MET mutant=invempty bash_n=0 killed_by=tool_inventory_conserved(inventory_half_unextracted(P0_RP7_RO_TOOLS)),no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=0,tool_shadow=UNDEFINED_EMPTY_INVENTORY,prefix_shadow=0)
R14_GRAMMAR_SUMMARY cases=38 pass=38 fail=0 result=PASS
R14_F1_RED_SUMMARY cases=57 pass=57 fail=0 result=PASS
R11_GUARDS_SUMMARY fences=21 pass=21 fail=0 result=PASS
R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS
R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL
```

Return codes were `0, 0, 0, 0, 1`; rc 1 is the published PASS condition for
`R11_R9RED`. Thus all six named round-14 mutants are killed, empty inventory is
not rendered as zero, and the published R14 RED/GREEN harness reports 57/57.
Those results verify the published cases but do not cover the residual construct
classes in F1 and F2.

## Thirteen-pattern review

| Pattern | Result |
|---|---|
| 1 - STOP is not a result | **Finding overlay:** the F1/F2 classes receive neither a modeled disposition nor an unmodeled failure. |
| 2 - Whose kernel answered? | Out of scope; no host was contacted. |
| 3 - The leaf is not the path | No path-admission change in this QA-only round. |
| 4 - Privileged child environment | No privileged or host child ran. |
| 5 - grep is not a parser | No separate finding; grammar-coverage omissions in the grep-backed censuses are owned by Pattern 12. |
| 6 - Read status before stdout | Clean: every harness return status was captured before accepting its summary. |
| 7 - Nonzero read is not EOF | No reader-completion change. |
| 8 - Name is not identity | No numeric or resolver identity claim; F1's lost definition identity is owned by Pattern 13. |
| 9 - Sentence outruns probe | **Finding overlay:** the exact-one-definition and any-unconserved-shape wording remains broader than the checks. |
| 10 - Evidence that cannot fail | Published harnesses reproduced literally and the R14 discriminator reported 57/57; it contains no falsification for F1/F2's residual classes. |
| 11 - Declared instrument is not executed instrument | **F1 overlay:** an undisposed definition name can still invalidate the builtin/prefix identity premise. |
| 12 - Unmodeled must not disappear | **Primary F1/F2 findings.** |
| 13 - Every admitted member needs a terminal disposition | **Primary F1/F2 findings:** definition identities, append assignments, and duplicate composition references are not conserved. |

## Scope and identity

- Audit anchor: `0f6b3ec93f19f17c7220b6c01a4ab081da419253`. The working copies of
  `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_R14_REPORT_2026-08-11.md`, and
  `RP6-P0.sh` were byte-identical to that commit before execution.
- `RP6-P0.sh` remained unchanged at
  `sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`.
- No host or network action occurred. No Git mutation occurred. No existing
  repository file was edited. Pre-existing unrelated working-tree changes were
  left untouched. This verdict file is the sole repository write.
- This non-accepting verdict grants no freeze, dispatch, host, deployment,
  credential, broker, exchange, or trading authority. The RP6 census hardening
  cycle and the Codex flagship slot remain open.

## Minimum required repair set

1. Make function-definition conservation identity- and multiplicity-preserving,
   fail closed on the continuation-separated-name class, and add executed D026
   RED/GREEN evidence.
2. Make inventory conservation cover append-style mutation and preserve
   composition multiplicity, with executed D026 RED/GREEN evidence.
3. Narrow the status and self-QA property text until those repairs are complete,
   rerun the five mandated harnesses, and obtain the next authorized T0 verdict.
