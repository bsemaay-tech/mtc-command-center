# Verdict: REQUEST_CHANGES

Three required findings remain. The two round-2 CRITICAL defects are closed on the
audited bytes, and I found no route that reopens either of them as a final FREEZE PASS.
However, RENDER can still claim graph closure over a valid shell form that its detector
does not model, F10 can report PASS before every plan allocation has a constants-side
disposition, and the published evidence is not reproducible from a fresh Windows checkout.

Audit target: commit `35860a0a`, T1, Codex flagship independent round 3. The current
worktree copies of every audited input are byte-identical to that commit; the later HEAD
adds only the kickoff file within this workstream.

## Required findings

### R3-F1 — MEDIUM — RENDER's coverage check shares the graph detector's blind spot

`composite_pathproof.py:84-92` recognizes only direct source and direct interpreter
commands. `_graph_opaque_reason` at lines 1066-1095 stops several unsupported shell
constructs, but it does not stop valid command-wrapper forms. `_derive_graph` then compares
the matches from one direct-source regex with a site count built from substantially the
same grammar at lines 1182-1230. A form invisible to the first detector is also invisible
to its purported coverage check.

Mechanism: place a source or interpreter operation behind a valid shell command wrapper.
RENDER sees neither a derived edge nor an uncovered site. A plan that declares only the
entry member and no edge can therefore leave R4, R6, and R7 at PASS even though the
rendered bytes reach another program. This is the same class as round-2 F3: an unmodeled
graph member disappears before conservation is checked.

The separately pinned path-scope prover does recognize wrapper commands and fails closed
when sourced content is outside its analyzed input, so this does not currently produce a
final FREEZE PASS. It is nevertheless a false RENDER PASS and contradicts the status
claim that incomplete RENDER graph analysis is fail-closed.

Required repair:

1. Make RENDER emit STOP for every valid source/interpreter wrapper form it does not
   integrate, rather than deriving coverage from the same narrow regex used for matches.
2. Add a benign wrapper regression that is RED against commit `35860a0a` and GREEN after
   the repair, plus an independent mutation discriminator under D026.
3. Re-run the complete carried matrix without weakening any existing assertion.

### R3-F2 — MEDIUM — F10 passes without a terminal disposition for every plan allocation

`_reconcile_constants` at lines 1018-1063 iterates constants bindings. It reconciles shared
names and explicitly accounts for constants-only names, but it creates no terminal row and
no F10 failure for a plan allocation absent from the constants table.

The published missing-constant fixture already demonstrates the claim defect without any
new fixture. Its safe terminal evidence is:

`CLAIM id="F10" name="allocation_constants_reconciliation" verdict="PASS" reason="plan_allocations_and_pinned_constants_are_one_conserved_value_universe"`

`COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete`

The overall STOP comes from F5/F6 in the analysis-unit builder, not from F10. Therefore the
system remains fail-closed for that fixture, but F10's PASS sentence is false: one plan
allocation has no constants-side disposition while the claim says the two inputs are one
conserved value universe. This is Patterns 9 and 13.

Required repair:

1. Give every plan allocation exactly one constants-side terminal disposition, including
   the absent case, and make F10 STOP when an allocation that can affect prover semantics
   is absent.
2. If constants-only runtime values remain intentionally allowed, narrow the F10 claim to
   the exact domain actually proved and retain their explicit terminal rows.
3. Add a D026 test whose discriminator asserts F10 itself changes from PASS to STOP; a
   downstream F5/F6 STOP is supplemental and does not close this claim defect.

### R3-F3 — MEDIUM — clean Windows checkout changes pinned fixture bytes

The disclosed line-ending risk applies and is reproducible:

- repository `.gitattributes` is `* text=auto`;
- this clone has `core.autocrlf=true`;
- all 31 tracked round-3 fixture files are `attr/text=auto`, with LF in the index and the
  current worktree;
- applying Git's checkout filters with `core.autocrlf=true` changed every representative
  class tested: shell member, constants table, allowlist, and JSON plan;
- the representative byte deltas were +6, +5, +1, and +30 respectively.

The committed pins describe the LF blobs, so a fresh Windows checkout materializes
different bytes and the published FREEZE matrix cannot reproduce. This is not a false
PASS, but it is a required Pattern-10 evidence-durability repair because the acceptance
harness is claimed as literal paste-and-run evidence.

Required repair: expand the scope to add a repository attribute that preserves fixture
bytes exactly, then demonstrate the matrix from a fresh checkout/configuration with
automatic CRLF conversion enabled. Do not merely document a local clone prerequisite.

## Reproduction and D026 evidence

Raw fixture transcripts were captured only in temporary audit files, compared, and
removed. No attack-shaped body or prohibited literal is reproduced here.

- Published 37-case matrix: command rc 0; 37 assertion lines; 37 PASS; 0 FAIL;
  `CASES=37 FAILED_COUNT=0`.
- Published behavioural pre-feature fence: three pre-feature PASS/rc-0 outcomes and three
  repaired STOP/rc-3 outcomes. The normalized real transcript exactly matched the
  published transcript.
- Published mutation fence: all three mutations restored the defective PASS behavior.
  The normalized real transcript exactly matched the published transcript.
- Published real-mapping, adapter-arm census, and syntax/grammar/determinism blocks:
  each returned rc 0 and each normalized real transcript exactly matched its published
  transcript.
- D026 classification of the three new round-3 tests: deploy-identity binding VERIFIED;
  allocation/constants divergence VERIFIED; non-shell RENDER STOP VERIFIED. Each has an
  executed pre-feature RED, repaired GREEN, and mutation discriminator.

## Round-2 finding dispositions

### F1 CRITICAL — CLOSED on the tested direct-source domain

Operand-to-member binding is exact declared deployed-path equality at both graph derivation
and analysis-unit construction. Basename fallback is gone. `evil-divergent-operand` reaches
STOP/rc 3, while its published control proves that the real child bytes are analyzable when
declared under the exact identity. R3-F1 above is a graph-grammar coverage defect; it does
not restore basename binding.

### F2 CRITICAL — CLOSED for shared-name divergence

Every name present in both plan allocations and the pinned constants table must be
byte-equal before prover invocation, and the analysis-unit builder repeats the operand
comparison. The published divergence case reaches STOP/rc 3 and the mutation discriminator
returns it to the old PASS. R3-F2 is a claim/domain-conservation defect, not a surviving
shared-name divergence.

### F3 MEDIUM — PARTIALLY CLOSED

Non-shell members now STOP at RENDER, and the new regression is properly falsified.
R3-F1 shows that the broader rule remains incomplete: another valid shell graph form can
still disappear from RENDER's detector and its coverage count together.

### N1 / N2

N1's adapter-arm census is reproducible. Twenty-eight of 33 arms remain undriven as
disclosed; I found no evidence that the census itself is false. N2 is closed for the three
round-3 regressions because the behavioural pre-feature and mutation evidence executed.

## Honest residual adjudication

The deployed identity remains a declared canonical lexical string, not a verified host
object. That weaker claim is acceptable for this synthetic stage because the composite
does not contact a host, the source-level claim says lexical equality, and every FREEZE
report emits the permanent host-object residual with `control=false`. The disclosure must
not be consumed later as deployment-object identity evidence.

The unpinned local interpreter, inherited environment, startup behavior, runtime descendants,
and non-integrated production members remain explicit production blockers. I did not treat
them as new round-3 findings because this artifact makes no production acceptance claim.

## Thirteen-pattern assessment

| Pattern | Assessment |
|---|---|
| 1 | Inability is generally STOP; held in the executed matrix. |
| 2 | No kernel/host identity claim is made in this local fixture stage. |
| 3 | Host leaf/object identity is explicitly residual, not claimed. |
| 4 | Local interpreter/environment remains disclosed and outside production acceptance. |
| 5 | R3-F1: modeled grammar is incomplete for valid wrapper forms. |
| 6/7 | Output grammar, process rc, counts, and records are reconciled before acceptance. |
| 8 | Exact deployed-path identity closes the basename defect on modeled forms. |
| 9 | R3-F2: F10's sentence outruns its predicate. |
| 10 | R3-F3: the evidence is not durable across a clean Windows checkout. |
| 11 | Pinned prover bytes versus unpinned interpreter remains an explicit production blocker. |
| 12 | R3-F1: an unmodeled graph form disappears at RENDER. |
| 13 | R3-F2: a plan-only allocation lacks an F10 terminal disposition. |

## Scope and hygiene attestation

- No host or network was contacted.
- Subject shell fixtures were read as analyzer input and never executed.
- No audited input, protected component, trading logic, Pine, parity, schema, or Git state
  was modified.
- Only this verdict file was authored. Temporary audit transcripts and helper files were
  removed.
- `git diff --exit-code 35860a0a..HEAD` is clean for every audited input; the sole later
  workstream change is the kickoff.
- The repository-wide `git status --porcelain` was already non-empty before this audit due
  to foreign untracked files owned by other active workstreams. I preserved them. A global
  clean-worktree attestation would therefore be false; the scoped audited-input cleanliness
  attestation above is the strongest honest proof available in this shared worktree.

