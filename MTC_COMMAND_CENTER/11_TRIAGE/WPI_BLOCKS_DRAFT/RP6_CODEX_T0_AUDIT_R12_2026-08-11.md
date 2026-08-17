# VERDICT: REQUEST_CHANGES

## Findings

1. `SELF_QA_RP6.md:8556`: **HIGH — Pattern 12 residual in alias/function-indirection.** The tokenizer admits every otherwise-unrecognized BARE command word without establishing what that name resolves to. It scans source-defined function bodies, but it has no alias-resolution rule, no function-identity allowlist, and no conservation check from a BARE invocation to the executed command. An admissible-looking BARE word can therefore resolve through alias/function-indirection to an emitter while the lexical emitter census sees no emitter command word. Required repair: either reject alias/function-indirection and every mechanism that activates it, or model it fail-closed with an exact declared/bound/executed resolution rule. Add D026 RED/GREEN evidence for the published fence.

2. `SELF_QA_RP6.md:8490`: **HIGH — Pattern 12 residual in command/builtin-prefix.** `analyze` classifies the prefix as the command word and then clears command position; it never passes the effective operand command through `cmdword`. The special rejection for indirect execution at `SELF_QA_RP6.md:8564` therefore applies only when that token is first, not when command/builtin-prefix changes which later token Bash executes. Required repair: recognize the prefix semantics, adjudicate supported options, and recursively classify the effective command word; unsupported shapes must fail closed. Add D026 RED/GREEN evidence for the published fence.

3. `STATUS_RP6_P0.md:35`, `STATUS_RP6_P0.md:166`, `RP6_R12_REPORT_2026-08-11.md:169`, and `RP6_R12_REPORT_2026-08-11.md:314`: **MEDIUM — the replacement fail-closed claims still outrun the policy.** The earlier round-11 overclaim is textually withdrawn, but the round-12 status/report now say every other or unmodeled command-word syntax fails and that Pattern 12 is closed for command words. Findings 1 and 2 make those claims false. Required repair: after closing the policy gaps, restate the proven boundary exactly; until then, withdraw the complete/fail-closed wording for these construct classes.

## Construct-class policy disposition

| Construct class | Rejected by design? | Read-only policy reasoning |
|---|---:|---|
| arithmetic-expansion | Yes | As a whole command word it is classified as PURE_EXPANSION, but its raw form is not one of the six declared handles, so assertion 12 rejects it. In a composite command word it is CONSTRUCTED and rejected earlier. |
| ANSI-C-quoting | Yes | The tokenizer collapses it to one expansion sentinel. A whole command word reaches the undeclared PURE_EXPANSION check; a composite reaches CONSTRUCTED. |
| parameter-default | Yes | The brace form is collapsed as one expansion. Its raw form does not equal a declared handle, while any literal composition is CONSTRUCTED; nested command execution inside the brace form is separately unmodeled. |
| process-substitution | No categorical rejection | The scanner treats its operators and parentheses structurally and analyzes the inner command position. I found no class-alone route by which it makes an admissible command word resolve to an emitter, so it is not an additional required finding. The documentation should describe this as structural modeling, not rejection of the class. |
| alias/function-indirection | No | A BARE invocation is accepted without binding its runtime resolution. Finding 1. |
| command/builtin-prefix | No | The prefix consumes command position and the effective operand is not classified. Finding 2. |

## Published harness execution

All four commands were run verbatim from `WPI_BLOCKS_DRAFT` in clean Git Bash processes. Full output was captured to temporary files outside the repository. All returned rc 0.

```text
R12_GRAMMAR_SUMMARY cases=23 pass=23 fail=0 result=PASS
R12_F1_RED_SUMMARY cases=33 pass=33 fail=0 result=PASS
R11_GUARDS_SUMMARY fences=17 pass=17 fail=0 result=PASS
R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS
```

The real-byte census also recorded `unmodeled=0`, `census_lines=163`, and the expected `ASSERT_MET tokenizer_and_census_same_lines lines=163` token. These GREEN results do not exercise the two residual construct classes identified by reading.

## Load-bearing equality

Confirmed. The reusable verdict path at `SELF_QA_RP6.md:8667` marks any tokenizer-versus-grep line-set divergence bad, and the main assertion at `SELF_QA_RP6.md:8835` routes a nonzero `cmp` result to the fence failure counter. Equality is line-for-line over the normalized line sets; a divergence fails the fence.

## Finding 2 and documentation verification

The live `R10_F4` extraction contains zero copies of the stale broad sentence and one copy of the narrowed three-class sentence. Its published harness passed 16/16, so the comment-only F4 repair is complete.

The specific round-11 status overclaim is visibly corrected in place, and the round-12 report explicitly withdraws the old completeness claim. However, the replacement round-12 statements are not complete corrections because they make the broader claims identified in finding 3.

## Scope and identity

- Audit tier: **T0**; this is the fresh Codex `gpt-5.6-sol` xhigh auditor slot.
- Audited bytes: commit `0259b4a4`; all four input files were verified byte-identical to that anchor from the later workspace HEAD.
- `RP6-P0.sh` remains unchanged at SHA-256 `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`.
- No new shell mutant was authored, echoed, or executed. No host or network action occurred. No existing repository file was edited.
- This non-accepting Codex verdict does not establish T0 acceptance or dispatch authority.

## Minimum required repair set

1. Close alias/function-indirection fail-closed, with published D026 RED/GREEN evidence.
2. Close command/builtin-prefix fail-closed, with published D026 RED/GREEN evidence.
3. Correct the round-12 policy claims to the boundary actually established.
4. Re-run the mandated harnesses and obtain a fresh independent T0 re-audit within the governing round authority.
