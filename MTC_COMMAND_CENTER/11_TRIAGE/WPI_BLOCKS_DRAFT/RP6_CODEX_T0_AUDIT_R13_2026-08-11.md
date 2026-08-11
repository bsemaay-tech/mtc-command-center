# VERDICT: REQUEST_CHANGES

## Required findings

### F1 — HIGH — Pattern 12 residual: one valid function-definition class is not inventoried, so builtin/prefix shadowing remains admissible

`SELF_QA_RP6.md:9778,9886-9895` treats `function` as a reserved word but records a
`FUNCDEF` only when the candidate name is followed by the parenthesized declarator.
The valid non-parenthesized `function`-keyword definition class therefore produces no
`FUNCDEF` record. If its name is an admitted builtin or one of the three prefix names,
the name is accepted by the builtin/prefix policy while assertion 15 never sees a
definition to compare against `builtin_names.txt`.

This is the construct-class residual the policy read was required to decide. A block
function can still shadow the builtin emitter used by the wrappers, or can shadow
`command`/`builtin`/`exec` so that Bash resolves the word as a function while the
tokenizer strips it as a prefix. The published parenthesized wrapper-shadow mutant is
killed, but it does not establish closure over the other admitted Bash definition
class. No new mutant was constructed or executed in this audit.

Required repair: make function-definition recognition complete for every Bash form the
fence admits, or emit an unmodeled record for every unsupported form. Derive the raw
definition census once, require every definition to reach exactly one `FUNCDEF`
disposition, bind the prefix words themselves against the no-shadow invariant, and add
published D026 RED/GREEN evidence for this construct class.

### F2 — HIGH — Pattern 12/13 residual: tool-shadow coverage becomes empty without failing closed

`SELF_QA_RP6.md:10146-10148` derives tool names with two exact line-shape `sed`
patterns. At `:10219-10224`, an empty extraction is assigned `n_sht=0`; there is no
required count, no reconciliation to the resolved-handle inventory, and no unresolved
disposition. A future inventory representation outside those two patterns therefore
silently removes the tool-shadow universe. A recognized function definition carrying a
tool name is then admitted through the `FUNCDEF` set while assertion 15 reports zero
tool shadows.

The current bytes do extract twelve names and the published tool-shadow mutant is
killed. That GREEN proves the current fixture, not the fail-closed policy claimed for an
unmodeled inventory shape. This exact limitation is disclosed in the round-13 status and
report, but disclosure is not a control.

Required repair: conservation-bind the declared tool inventory to the extracted tool-name
set and to the runtime handle set. Empty, partial, duplicate, or unrecognized inventory
syntax must produce an unmodeled failure, never `tool_shadow=0`. Add published D026
RED/GREEN evidence for inventory-shape drift plus tool shadow.

### F3 — HIGH — Pattern 12 residual: alias absence is checked lexically, not semantically

`SELF_QA_RP6.md:10159-10165` rejects a non-comment literal `expand_aliases` token and one
literal alias-definition spelling. It does not classify the arguments of the admitted
`shopt` and `alias` builtins. Constructed or runtime-valued option/definition operands can
therefore make alias expansion and an alias definition effective without either lexical
pattern appearing. An alias can then replace an otherwise admitted bare word.

For the exact audited bytes and their published clean non-interactive launch path, alias
indirection is absent: the block, wrapper, pinned library, and pinned bootstrap contain no
alias enablement or definition, and the launch uses `env -i` plus `bash --noprofile
--norc`. The required question, however, is whether the R13 policy closes the construct
class by design. It does not; the current fixture is clean while the policy remains
fail-open to unmodeled alias-control operands.

Required repair: either reject every executable alias-definition command and every
`shopt` form not proven unrelated to alias expansion, or model their operands with a
complete fail-closed grammar. Add published D026 RED/GREEN evidence for the unmodeled
operand class.

## Policy-soundness decisions by required class

| Class | Decision | Reason |
|---|---|---|
| Alias | **Not closed by design** | Clean on the audited launch and bytes, but the assertion is a lexical search and does not bind constructed/runtime alias-control operands (F3). |
| Function-shadow | **Not closed by design** | The non-parenthesized `function`-keyword definition class is not recorded as `FUNCDEF`; builtin and prefix names can therefore escape the shadow census (F1). |
| Tool-shadow | **Not closed by design** | The current twelve-name extraction works, but an unrecognized inventory shape becomes an empty successful shadow universe (F2). |
| `command`/`builtin`/`exec` prefix | **Option parser locally sound; class not closed overall** | The explicit prefix scanner handles `command -p`, lookup forms, redirections, recursion, and fails unsupported options closed. Its premise that the prefix word resolves to the builtin is false while F1 remains open. |

The answer to the kickoff's Pattern-12 question is therefore yes: an admissible-looking
word can still resolve through the function-shadow or alias classes to a different
emitter path. The gaps are stated only by construct class; this audit authored, echoed,
and executed no new emitter mutant.

## Published harness execution

All five commands were extracted and run verbatim from `SELF_QA_RP6.md` in
`WPI_BLOCKS_DRAFT`. Stdout/stderr were captured to files under the local temporary
directory; stderr was empty for all five.

```text
R13_TOKENIZER        fragments=20 emit_sites=163 unmodeled=0 runtime_cmdwords=16 funcdefs=26 prefix_operands=2 bare_cmdwords=294
ASSERT_MET alias_indirection_impossible_by_construction (no_expand_aliases_no_alias_definition)
ASSERT_MET bare_command_words_bound distinct=34 funcs=26
ASSERT_MET no_wrapper_shadow p0_stop_defs=1 p0_fail_defs=1 builtin_shadow=0 tool_shadow=0 tool_names=12
ASSERT_MET mutant=alias bash_n=0 killed_by=alias_indirection_impossible(alias_expand_aliases_enabled)
ASSERT_MET mutant=shadow bash_n=0 killed_by=no_wrapper_shadow(p0_stop=2,p0_fail=1,builtin_shadow=0,tool_shadow=0)
ASSERT_MET mutant=cmdprefix bash_n=0 killed_by=runtime_command_words_declared(1)
ASSERT_MET mutant=toolshadow bash_n=0 killed_by=no_wrapper_shadow(p0_stop=1,p0_fail=1,builtin_shadow=0,tool_shadow=1)
R13_GRAMMAR_SUMMARY cases=30 pass=30 fail=0 result=PASS
R13_F1_RED_SUMMARY cases=35 pass=35 fail=0 result=PASS
R11_GUARDS_SUMMARY fences=19 pass=19 fail=0 result=PASS
R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS
R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL
```

Return codes were `0, 0, 0, 0, 1` respectively; rc 1 is the documented PASS condition
for `R11_R9RED`. `R13_F1_RED` mechanically showed R12-blind and R13-caught for all four
published classes: four of four in each direction, with four of four claimed kill checks.
This confirms the published evidence exactly; it does not close F1-F3, which are different
construct classes found by the required policy read.

## Documentation claim

The two round-12 overclaims were textually corrected in place and the delivered round-12
report was corrected by reference. That part is complete. The replacement round-13
property at `STATUS_RP6_P0.md:61-70` is not yet the true property: it says alias
indirection is impossible, no definition shadows a builtin/tool, and every unmodeled
construct fails. F1-F3 falsify those completeness statements. Pattern 9 therefore remains
as an overlay finding until the policy closes or the wording is narrowed to the exact
recognized construct set.

## Thirteen-pattern review

| Pattern | Result |
|---|---|
| 1 — STOP is not a result | Clean for this QA-only round; process statuses are reported separately from block outcomes. |
| 2 — Whose kernel answered? | Clean/currently out of scope; no host was contacted and the launch-domain fact used for alias analysis was read from the published frozen route. |
| 3 — The leaf is not the path | No new path-admission claim. |
| 4 — Privileged child environment | No host/privileged child ran; published harnesses used clean local Bash processes. |
| 5 — grep is not a parser | No new structured-data admission; the shell-coverage defects are classified under Pattern 12. |
| 6 — Read status before stdout | Clean: each harness rc was captured before its summary was accepted. |
| 7 — Nonzero read is not EOF | No new reader claim in the audited change. |
| 8 — Name is not identity | F1/F2 concern runtime command identity, primarily Pattern 11/12; no numeric host-identity change. |
| 9 — Sentence outruns probe | **Finding:** the round-13 completeness wording outruns the actual construct coverage. |
| 10 — Evidence that cannot fail | Published evidence reproduced; D026 is green for the four published classes. It does not cover F1-F3. |
| 11 — Declared instrument is not executed instrument | **Finding overlay:** the prefix token is not bound to the builtin when the missed function-definition class shadows it. |
| 12 — Unmodeled must not disappear | **Primary findings F1-F3.** |
| 13 — Every admitted member needs a terminal disposition | **Finding overlay F2:** an unrecognized tool-inventory member set collapses to empty with no unresolved disposition. |

## Scope and identity

- Audit tier: **T0**; fresh Codex `gpt-5.6-sol` xhigh auditor slot.
- Audit anchor: commit `0015a7fa`. All four audited files in the workspace were verified
  byte-identical to that commit before execution.
- `RP6-P0.sh` is unchanged across round 13 and remains SHA-256
  `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`,
  110817 bytes, zero CR bytes.
- No host or network action occurred. No Git mutation occurred. No existing repository
  file was edited. This verdict file is the sole repository write.
- This non-accepting verdict grants no freeze, dispatch, host, deployment, credential,
  broker, exchange, or trading authority.

## Minimum required repair set

1. Close the unrecorded function-definition class and bind the three prefix words against
   the complete no-shadow census; add executed D026 RED/GREEN evidence.
2. Make tool-name extraction conservation-bound and fail closed on empty/partial/unmodeled
   inventory shapes; add executed D026 RED/GREEN evidence.
3. Make alias enablement/definition analysis semantic or reject every unproven form; add
   executed D026 RED/GREEN evidence.
4. Narrow the status/report property until, or after, the three policy gaps are closed,
   then re-run the mandated harnesses and obtain the next authorized T0 verdict.
