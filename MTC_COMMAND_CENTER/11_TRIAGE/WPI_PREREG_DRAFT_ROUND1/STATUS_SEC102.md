# Section 10.2 composite path-proof status

Date: 2026-08-11
Status: `ROUND-4-AUTHORED-SELF-QA-PASS-PENDING-INDEPENDENT-ACCEPTANCE`
Audit tier: T1 - local-only non-economic Python tooling and fixtures. Round 2 was audited by
the Claude flagship (verdict **BLOCK**, two CRITICAL). Round 3 repaired that BLOCK and was
audited by Codex `gpt-5.6-sol` (`SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md`, verdict
**REQUEST_CHANGES**: both CRITICALs confirmed closed, three MEDIUM findings raised). Round 4
is the repair of those three MEDIUMs, implemented by `claude-opus-5` xhigh. No audit or
acceptance is claimed by the implementer.

## Round 4 - what changed and why

### R3-F1 - the graph coverage check no longer shares the matcher's blind spot

Round 3 matched source/interpreter commands with two regexes anchored at `(?:^|[;|&()])`,
then "checked coverage" by counting sites with a second regex built from the same grammar. A
form invisible to the matcher was equally invisible to its own coverage check, so
`command source "$LIB"` produced no edge, no uncovered site, and `R4`/`R6`/`R7` PASS at
`rc 0` over bytes that reach another program.

* A new independent lexer (`_shell_words`) tokenises the rendered bytes and marks every
  command position - after separators, reserved words, assignment prefixes, wrappers and
  redirections, not only after four punctuation characters.
* `_command_word_class` classifies each command-position word against a **detection
  vocabulary that is deliberately broader than the derivation grammar**: 32 interpreter
  names plus a version pattern, `source`/`.`, and 26 command wrappers.
* `_graph_word_conservation` STOPs on every disagreement between the two sides -
  `source_graph_command_word_not_modeled`, `source_graph_command_wrapper_not_modeled`,
  `source_graph_dynamic_command_not_modeled`,
  `source_graph_derived_edge_not_at_command_word`,
  `source_graph_derived_operand_not_a_shell_word`.
* The scanner runs only where `_graph_opaque_reason` already passed, so here-documents and
  continuations still STOP first and are never tokenised as code.
* FREEZE inherits the same repair through the shared `_derive_graph`.
* Same-shape hole closed while here: `R7`/`F9` used to PASS vacuously whenever derivation was
  blocked, because "every derived operand" is trivially true over an empty set. They now STOP
  with `deployed_identity_domain_not_derived`.

### R3-F2 - every plan allocation has exactly one terminal constants-side disposition

Round 3 walked the constants table only, so a plan allocation the table never mentioned had
no row and no F10 failure while F10 claimed both inputs were one conserved value universe.

* `_reconcile_constants` now walks both directions and emits one
  `ALLOCATION_RECONCILIATION` row per declared allocation.
* An allocation absent from the pinned constants table is `STOP`
  (`allocation_absent_from_pinned_constants`) **on F10 itself**, with no "can this affect
  prover semantics" exemption - such an exemption would need a second modelled grammar over
  shell text, and its gaps would reopen R3-F1's pattern.
* The F10 claim sentence is narrowed from
  `plan_allocations_and_pinned_constants_are_one_conserved_value_universe` to
  `every_plan_allocation_reconciled_and_every_pinned_constant_dispositioned`.
* Constants-only names remain `RUNTIME_ONLY` with explicit rows; the narrowed claim no longer
  overstates them.
* Deliberate asymmetry: an absent allocation STOPs F10 but does not withhold the constants
  map from the prover, because absence corrupts no value the prover re-resolves and the
  analysis-unit builder refuses independently. Every other reconciliation failure still
  blocks prover invocation.

### R3-F3 - the published evidence survives a fresh Windows checkout

New `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes`, scoped to that
directory: `sec102_r1..r4_fixtures/** -text` for the pinned blobs, `text eol=lf` for
`pathscope_prover.py` and `composite_pathproof.py` (byte-stable but still diffable). Proven
by three real `core.autocrlf=true` clones of a throw-away repository that mirrors this one:

| Arm | Byte-changed files | Matrix |
|---|---:|---|
| no `.gitattributes` (the round-3 state) | 96 of 96 | 13 of 40 fail |
| `sec102_r*_fixtures/** -text` only | 2 of 96 | 10 of 40 fail |
| published scoped `.gitattributes` | 0 of 96 | 40 of 40 pass, transcript identical |

The second arm is the kickoff's own sketch, and it is still RED: `pathscope_prover.py` is
`attr/text=auto` too, arrives at 125222 B against its 122446 B pin, and `green_freeze.json`
fails `F4 frozen_identity_mismatch`. The two tool lines are load-bearing. **No byte of
`pathscope_prover.py` was modified** - only how Git materialises it. The scope question is
flagged for the Lead in `SEC102_R4_REPORT_2026-08-11.md`; if the tool lines are rejected,
R3-F3 stays open.

## Stage coverage

### ALLOCATE

Unchanged from round 1. Six RED fixtures and one GREEN, same rc and reason tokens.
`sec102_r1_fixtures` has no worktree modification.

### RENDER

Everything round 3 implemented, plus:

1. Command-position coverage is decided by an independent lexer, not by a second copy of the
   matcher's grammar.
2. Any wrapper, any unmodelled interpreter, and any dynamic command word STOPs.
3. `R7` cannot PASS over a derivation that was blocked.

### FREEZE

Everything round 3 implemented, plus:

1. The same command-word conservation, applied again to the frozen bytes (`F3`/`F9`).
2. One terminal `ALLOCATION_RECONCILIATION` row per declared allocation, with an absent
   allocation stopping `F10` itself.
3. Two new conservation counters each on `CONSTANTS_CONSERVATION` and
   `FREEZE_CONSERVATION`.

## Self-QA result

- 40 cases, `FAILED_COUNT=0`. **All 37 round-3 cases carried unchanged in rc and reason
  token**; 3 are round-4 additions. No carried fixture file was edited.
- 7 ALLOCATE regression cases: unchanged.
- 10 RENDER cases: 9 carried (8 REDs + 1 GREEN), 1 new round-4 RED.
- 23 FREEZE cases: 21 carried (9 round-2 REDs, 9 round-3 REDs, the round-3 F1 control at
  FAIL rc 1, and 2 GREENs), 2 new round-4 REDs.
- D026 behavioural pre-feature: each new fixture runs over byte-identical inputs against the
  round-3 code streamed from `10659bd5` and against round-4 code. `red_render_wrapped_source`
  and `red_freeze_allocation_absent` both go `PASS rc 0` -> `STOP rc 3`.
  `red_freeze_wrapped_source` is a **claim-level** RED (`F3` PASS -> STOP at unchanged
  `rc 3`) and is labelled as such rather than presented as an rc flip.
- **R3-F2's discriminator isolates F10.** For `red_freeze_allocation_absent`, `F5` and `F6`
  are PASS on both sides; only `F10` moves. There is no downstream STOP to hide behind.
- Grammar battery: 32 wrapper/blind-spot forms, each an executed round-3 `PASS rc 0`, all
  32 killed, 0 survived; 5 benign controls `rc 0` on both sides.
- D026 mutation: 5 discriminators, all restoring the defective PASS - the 2 new ones plus the
  3 carried from round 3. The carried `F2` mutation needed one extra line because the
  allocation-side walk is a genuinely independent second comparison.
- Python 3.12 AST parse PASS; 35 JSON plans parse; all fixture bytes LF-only; deterministic
  full stdout+rc for the RENDER GREEN, the FREEZE GREEN and one new RED; `git diff --check`
  PASS.
- The RENDER GREEN output digest is byte-identical to round 3. The FREEZE GREEN digest moved,
  accounted for by the new allocation rows, the new counters, and the narrowed F10 sentence.
- `pathscope_prover.py` has no worktree diff; its pinned identity was re-derived.

Literal commands and real output are in `SELF_QA_SEC102_R4.md`.

## What remains - every item is a limitation

1. These are synthetic fixture proofs. The production P0 and RO entrypoints, RP0 library and
   bootstrap, RP6, RP7, inline Python bodies, and exact candidate `verify_lock.py` blob have
   not been supplied in a plan and have not passed this tool.
2. **The deployed identity is a declared, lexically canonical string compared for exact
   equality. It is not host-object verification.** No host was contacted. Disclosed on every
   FREEZE report as `R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED`, `control=false`.
3. Symlink resolution and mount-boundary identity remain residual R1 disclosures, not
   controls.
4. ALLOCATE declares no deployed identity and makes no whole-program path claim.
5. The composite's constants mirror is narrower than the pinned prover's parser: a constant
   whose value expands another constant is refused, not modelled.
6. A constants binding the plan does not allocate is `RUNTIME_ONLY`, not stopped. The F10
   claim sentence is now narrowed so it no longer overstates this.
7. **F10 STOPs on every plan allocation absent from the pinned constants table, with no
   exemption.** A plan that legitimately declares a render-only allocation which is never a
   runtime constant will STOP. This is a chosen false stop, taken over a second modelled
   grammar.
8. **The command-word detection vocabulary is a list, and a list can be short.** An
   interpreter absent from it, invoked at a command position under a literal name, is
   classified a benign leaf and derives no edge. This is the residual R3-F1 surface - much
   smaller than round 3's three names at four punctuation positions, but not zero. Executing
   an arbitrary program (`./child.sh`) is outside every modelled edge kind and always was.
9. Wrapper detection produces safe false stops by design: `find`, `time`, `env`, `xargs` and
   similar STOP even with harmless operands, because the composite does not model what they
   run.
10. FREEZE accepts only all-shell reachable composites. A `python_source` member STOPs at
    FREEZE and STOPs graph derivation at RENDER. The actual RO composite cannot yet PASS.
11. The analysis-unit builder supports only standalone direct `source`/`.` edges. It STOPs on
    `execute_source` and `inline_source`.
12. RENDER graph analysis is intentionally incomplete and fail-closed: here-documents, line
    continuations, multiline quotes, command/process substitutions, `eval`, `alias`, dynamic
    command positions, and now every unmodelled command form, all STOP.
13. The generated analysis unit uses a synthetic `test -r` to preserve each bound source
    operand while substituting exact child bytes. It is not an executable or frozen
    deployment artifact.
14. Allocation-consumer checking is exact template-token conservation plus
    allocation/constants value conservation plus exact deployed-path operand binding. It is
    not full semantic shell dataflow.
15. `sys.executable`, used to launch the pinned prover locally, is an external-runtime
    dependency not pinned by the plan.
16. The analysis unit and the prover/constants/allowlist snapshots are temporary local files
    removed at adapter exit. They are not frozen artifacts.
17. The implemented proof covers exact lexical filesystem and network operands. No closed
    runtime-descendant family or exact descendant manifest is implemented.
18. Bash startup sources, imported functions, inherited environment, interpreter identity,
    cwd, shell options, bootstrap PATH tools, temporary-path behavior, wrapper `/dev/null`
    opens, and RP6 exact venv binding remain production blockers from the design.
19. A prover input-read or constants/allowlist parse error does not emit seven counters; the
    composite STOPs on that incomplete output grammar rather than inventing zeros.
20. **28 of 33 prover-adapter arms remain undriven** by published fixtures. Round 4 drove no
    new arm; the count and classification are unchanged and re-derived in
    `SELF_QA_SEC102_R4.md` section 7.
21. **The `.gitattributes` repair is inert until the Lead commits it**, because Git reads
    checkout attributes from the committed tree. The demonstration proves it by committing
    inside a throw-away repository; this repository has no commit from this round.
22. The `.gitattributes` covers this directory only. Every other byte-pinned artifact in the
    repository - RP6, RP7, the block files, the preregistration drafts - carries the same
    pre-existing line-ending exposure and is outside this fence. That is a disclosure to the
    Lead, not a claim that those are safe.
23. No archive was created or frozen. No host, dispatch, execution, deployment, or production
    Section 10.2 acceptance follows from a fixture PASS.

## Artifact identity record

The complete per-artifact byte-count and SHA-256 table is in `SEC102_R4_REPORT_2026-08-11.md`
and in `SELF_QA_SEC102_R4.md` section 9, both re-derivable by the published command. No
commit was made.
