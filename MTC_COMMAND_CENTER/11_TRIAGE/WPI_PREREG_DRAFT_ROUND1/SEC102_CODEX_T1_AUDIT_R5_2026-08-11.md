# Verdict: REQUEST_CHANGES

Round 5 closes the reopened named-fd, indexed-assign, and unmodeled-prefix cases, but the
command-position coverage claim is still not closed. A pathname-expanded command word is
classified as a benign leaf even when Bash can resolve it to a recognized interpreter. The
following script operand is then outside both direct matchers and the independent word
conservation check. This is a silent no-edge path and therefore meets the kickoff's CRITICAL
reopening criterion.

## Scope and identity

- Audit tier: T1, independent Codex `gpt-5.6-sol` audit at xhigh effort.
- Audited commit: `7da764791d7ced174b25a5b4dd452b3655ca3d33`.
- The six named audit surfaces and all round-5 fixture bytes match that commit; the scoped
  diff from the commit was empty before the verdict was written.
- No source, fixture, Pine, parity, MTC, trading, host, or network surface was changed or
  contacted. No new attack fixture was authored. Raw fixture output was redirected outside
  the repository.

## Executed evidence

The section 3 matrix was executed verbatim from the audit directory:

```text
CASES=44 FAILED_COUNT=0
```

The three new RED fixtures were executed verbatim. Only the permitted terminal lines are
quoted below.

Named-fd:

```text
CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_command_word_not_modeled"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
```

Indexed-assign:

```text
CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_command_word_not_modeled"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
```

Unmodeled-prefix:

```text
CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
```

The section 2 scanner-boundary block also reproduced its published transcript. This is the
important causal check: named-fd is discarded as a descriptor without changing
`command_position`; indexed-assign remains an assignment word and leaves the position open;
unmodeled-prefix returns an explicit scanner reason. The STOPs above therefore do not come
from an unrelated downstream predicate.

The mutation block reproduced its declared expectation table:

```text
OFF_EXPECTATION=0
```

The full round-5 prefix battery and carried round-4 battery reproduced their published
results, including the disclosed conservative false stop. Determinism, carried GREEN-byte
identity, and artifact-identity blocks also reproduced. The external paste-and-run harness
matched every substantive block; its sole current mismatch is the historical hygiene block,
whose published output records the pre-commit modified/untracked state while the audited
artifacts are now committed. That state-dependent difference is not used as closure evidence.

## Required finding

### R5-F1 — CRITICAL — pathname-expanded command words silently bypass graph coverage

Mechanism, without reproducing an attack shell:

1. Bash permits an unquoted pathname-expansion token in command position. At runtime that
   token can resolve to a recognized interpreter, followed by a script operand.
2. `_graph_opaque_reason` at `composite_pathproof.py:1449` rejects several dynamic forms but
   not pathname expansion.
3. `_literal_shell_word` at line 1040 passes the expansion token through as a literal because
   it contains none of the few dynamic markers checked there.
4. `_command_word_class` at line 1387 consequently returns `leaf`.
5. `_graph_word_conservation` at line 1430 emits no reason for a command-position leaf, and
   the following operand is not scanned as a command word.
6. `_derive_graph` at lines 1560–1573 therefore receives neither a direct edge nor an opaque
   coverage reason. A no-edge declaration can remain apparently conserved.

I confirmed that chain with a read-only, in-memory scanner probe: the opaque gate accepted
the form, both direct matcher sets were empty, the first word was a command-position leaf,
and word conservation returned no reason. Nothing was written and no shell body was
executed.

This is not the disclosed finite interpreter-vocabulary limitation. The runtime-resolved
command is a member of the recognized interpreter class; only its source spelling is
dynamic. It also contradicts `STATUS_SEC102.md` item 12, which says dynamic command positions
STOP. Pattern 12 is primary; Patterns 5 and 9 are overlays.

Minimum repair:

1. Make every command-position word that requires shell expansion STOP before it can become
   a leaf, or model that expansion completely under a closed runtime domain. At minimum the
   repair must cover pathname expansion; brace, tilde, and option-enabled extended patterns
   must be adjudicated explicitly rather than assumed away.
2. Add D026 evidence at both scanner and full-composite boundaries: RED against the round-5
   behavior (or an equivalent mutation), GREEN after repair, exact commands, and real output.
3. Add a discriminator that fails if the new dynamic-word fence is removed while the named-fd,
   indexed-assign, and unmodeled-prefix fences remain intact.
4. Correct the dynamic-command-position statement in `STATUS_SEC102.md`, then rerun the
   44-case matrix, all three new REDs, both prefix batteries, the mutation matrix, and the
   external paste-and-run harness.

## Disclosed interpreter-vocabulary residual

The finite recognized-interpreter list is acceptable only as an explicitly synthetic,
model-scoped limitation in this round because the status and report clearly deny production
or Section 10.2 acceptance. It remains a production blocker. The eventual whole-program
claim cannot accept an unknown executable-capable command as a benign leaf; Pattern 12
requires an opaque STOP unless its behavior is modeled. A disclosure is not a control.

## Thirteen-pattern adjudication

1. STOP/PASS/FAIL ordering held on the executed round-5 arms.
2. Host and namespace identity remain explicit non-claims.
3. Host-object, symlink, and mount identity remain explicit non-claims.
4. The external interpreter/environment boundary remains a disclosed production blocker.
5. Fails for the unmodeled pathname-expansion grammar in R5-F1.
6. Probe status precedes output adjudication on the exercised paths.
7. No new incomplete-reader path was introduced.
8. Deployed identity remains lexical and explicitly scoped as such.
9. Fails because the documented dynamic-command STOP sentence outruns the predicate.
10. The required matrix, REDs, mutations, and batteries reproduced; the historical
    pre-commit hygiene transcript is not treated as current-state evidence.
11. No new declared-versus-executed instrument defect was found in the round-5 diff; the
    unpinned runtime remains disclosed.
12. Fails primarily: an unmodeled runtime command expansion disappears as a leaf.
13. Member/allocation terminal-disposition fences remain unchanged and reproduced.

## Worktree hygiene

The shared worktree was not globally clean at audit start: it already contained 57 unrelated
untracked evidence/scratch entries from other workstreams. They were preserved. A truthful
global `git status --porcelain` clean proof is therefore impossible in this session. The
audited source/fixture scope was clean against commit `7da76479`; after this audit, the only
intended status delta is this required verdict file.
