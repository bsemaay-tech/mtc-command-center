# Verdict: REQUEST_CHANGES

Round 4 closes R3-F2 and R3-F3, but R3-F1 is not closed. The new independent word
scanner still silently loses valid Bash command positions. A source or interpreter
operation after either an indexed assignment prefix or a named-file-descriptor
redirection prefix can remain invisible to both graph derivation and the new coverage
reconciliation. That permits a false RENDER PASS over a real program edge. Under the
kickoff contract, this reopens a CRITICAL finding.

Audit target: commit `28b5c06b`. TIER: T1. APPLIED AUDITOR CONTRACT: Codex
`gpt-5.6-sol` xhigh, fresh independent round-4 audit; T1 repair/re-audit cap 2. The
diff exceeds 300 lines and this flagship audit raises a finding, so the required
GLM-5.2 second opinion remains part of the T1 gate.

## Required finding

`composite_pathproof.py:1279`: **CRITICAL**: `_shell_words` preserves command position
only for numeric file-descriptor prefixes. A valid Bash named-file-descriptor prefix is
instead emitted as a leaf word; line 1286 then closes command position before the
redirection and the following command. Independently, `SHELL_ASSIGNMENT_RE` at line
1294 accepts only scalar assignment words, so a valid indexed assignment prefix is also
classified as a leaf and closes command position. The direct source/interpreter regexes
do not match through either prefix, and `_graph_word_conservation` sees no uncovered
graph word. Direct scanner-boundary probes against the committed module reproduced both
silent outcomes without creating or executing a fixture. Fix command-position
conservation for every accepted Bash assignment and redirection prefix, or STOP on each
unmodelled prefix before it can be classified as a benign leaf. Add benign RED-on-
`28b5c06b` / GREEN-after-repair regressions and independent D026 mutations for both
mechanisms, then rerun the full carried matrix without weakening a fence.

This is Pattern 12 primarily, with Pattern 5 grammar incompleteness and Pattern 9 claim
overreach as overlays. It is not covered by the report's interpreter-vocabulary
residual: the missed command word is already in the declared detection vocabulary; the
scanner loses its command position before classification.

## Executed evidence

The published 40-case matrix was run verbatim with complete fixture output redirected
outside the repository:

`CASES=40 FAILED_COUNT=0`

The three published round-4 RED comparisons were also run verbatim over byte-identical
inputs. `red_render_wrapped_source.json` changes from RENDER PASS to STOP. The
claim-level `red_freeze_wrapped_source.json` remains overall STOP on both versions, but
F3 itself now changes from PASS to STOP instead of relying on the downstream prover.
For `red_freeze_allocation_absent.json`, F5 and F6 are PASS on both versions and F10
alone changes:

`CLAIM id="F5" name="prover_output_conservation" verdict="PASS" reason="seven_counts_and_records_reconciled"`

`CLAIM id="F6" name="lexical_pathscope_disposition" verdict="PASS" reason="every_prover_result_terminal_and_fail_closed"`

`CLAIM id="F10" name="allocation_constants_reconciliation" verdict="PASS" reason="plan_allocations_and_pinned_constants_are_one_conserved_value_universe"`

`CLAIM id="F10" name="allocation_constants_reconciliation" verdict="STOP" reason="allocation_absent_from_pinned_constants"`

This verifies R3-F2's requested discriminator: no downstream STOP hides the F10 repair.
The `evil-divergent-operand` fixture body and all prohibited literals remained
quarantined; they are not reproduced here.

## R3 finding dispositions

- **R3-F1: OPEN / CRITICAL.** The published wrapper RED is genuine, but the replacement
  coverage scanner still has valid-prefix blind spots that produce the same false
  RENDER PASS mechanism.
- **R3-F2: CLOSED.** Every declared allocation receives one constants-side terminal row;
  absence moves F10 itself while F5/F6 stay PASS on both sides.
- **R3-F3: CLOSED.** The committed attribute repair is scoped to this directory. The
  four fixture globs resolve to `-text`; the two tools resolve to `text eol=lf`.

## R3-F3 durability verification

I created a local sparse checkout of exact commit `28b5c06b` with
`core.autocrlf=true`. Across the two pinned tools and every tracked file under the
round-1 through round-4 fixture globs, all 96 checked-out files had raw blob identities
equal to their committed blobs; mismatch count was zero. `pathscope_prover.py` has the
same committed blob at `10659bd5` and `28b5c06b`, its checked-out bytes equal that blob,
and the new attributes did not renormalize it. `git status --porcelain` was empty in the
isolated checkout.

The primary workspace already contained unrelated untracked artifacts before this audit,
so a repository-wide clean claim there would be false and I did not delete or alter those
files. The audited SEC102 inputs were clean before the verdict write. The source repository
was not checked out, normalized, staged, committed, or otherwise mutated; this verdict is
the only repository file created by the audit.

## Residual and thirteen-pattern adjudication

- The finite interpreter-name vocabulary is an honestly disclosed limitation only when
  the command truly falls outside the declared model. It does not cover this finding,
  where an already-recognized graph word disappears because the scanner misclassifies a
  valid prefix. That is a reachable false RENDER PASS.
- F10's conservative STOP for every plan allocation absent from constants is safe and
  honestly described. Constants-only runtime bindings remain explicitly dispositioned.
- Wrapper detection's false STOPs are conservative. They do not excuse silent loss at
  other valid command positions.
- The 28 undriven prover-adapter arms are honestly disclosed as coverage debt, not
  acceptance evidence. No new adapter-arm closure is credited in this round.
- Patterns 1, 6/7, 8, 10, and 13 hold on the executed carried cases; Pattern 10's checkout
  durability is independently closed. Patterns 2/3, 4, and 11 remain explicit lexical,
  environment, interpreter, and production blockers rather than host-identity claims.
  Patterns 5/9/12 fail for the required finding above.

## Minimum required repair

1. Make `_shell_words` preserve or conservatively refuse command position across all
   valid Bash assignment-word and redirection-prefix forms, including indexed assignments
   and named file descriptors.
2. Demonstrate RED against exact commit `28b5c06b` (or an equivalent deliberate mutation)
   and GREEN after repair for each mechanism, with claim-local evidence that R4/F3 moves.
3. Re-run the verbatim 40-case matrix and the carried mutation/grammar evidence, then send
   the bounded repair through the remaining T1 review contract and GLM-5.2 second opinion.

## Scope and hygiene attestation

No host or network was contacted. No subject shell fixture was executed. No attack fixture
was authored. No audited input, protected component, trading logic, Pine, parity, schema,
or source Git state was modified. Full fixture output stayed redirected outside the
repository; only permitted claim/verdict/count lines are quoted above.
