# Section 10.2 composite path-proof status

Date: 2026-08-11
Status: `ROUND-3-AUTHORED-SELF-QA-PASS-PENDING-INDEPENDENT-ACCEPTANCE`
Audit tier: T1 - local-only non-economic Python tooling and fixtures. Round 2 was audited by
the Claude flagship (`SEC102_CLAUDE_T1_AUDIT_R2_2026-08-11.md`, verdict **BLOCK**, two
CRITICAL findings). Round 3 is the repair of that BLOCK, implemented by
`claude-opus-5` xhigh; Codex `gpt-5.6-sol` audits round 3 as the independent cross-model
flagship. No audit or acceptance is claimed by the implementer.

## Round 3 - what changed and why

Round 2 emitted `PASS rc=0` for a program that at runtime sources a file whose bytes were
never read, never pinned and never analysed. Two independent constructions produced that
result. Both are closed here, independently, each with an executed behavioural falsification
against the exact round-2 code.

### F1 - deployed identity replaces basename matching

The plan schema gains a required member key `deploy_path` at RENDER and FREEZE: the absolute
canonical POSIX path the member is deployed at and referenced by. ALLOCATE keeps the round-1
member contract, because it derives nothing from bytes and makes no whole-program claim.

* A source or interpreter operand binds to a member **only** by exact equality with one
  declared `deploy_path`. Both round-2 basename lookups - in `_member_for_operand` and in
  `SubprocessPathProver._build_analysis_unit` - are deleted; there is no basename, suffix or
  in-bundle-path fallback anywhere in the tool.
* An operand that matches no declared `deploy_path` is `STOP rc 3`
  (`source_operand_deploy_identity_unbound`), never a FAIL, never a PASS, and never a
  readability-probe-only path.
* `deploy_path` must itself be absolute, canonical, control-free, placeholder-free and
  unique across members; each member gets exactly one `DEPLOY_IDENTITY` terminal row.
* An operand containing `..` is refused rather than normalised, because collapsing `..`
  lexically is unsound when any prefix is a symlink.
* New claims `R7` and `F9` (`deployed_identity_binding`) carry this property so it has its
  own falsifiable verdict rather than hiding inside the graph claim.

### F2 - allocations and `constants.env` are reconciled into one value universe

Round 2 resolved `$LIBRARY_PATH` from plan allocations to choose the member, then emitted
the operand raw so the pinned prover re-resolved the same name from `constants.env`, and
nothing compared the two.

* `constants.env` is now parsed by the composite with a deliberately narrower mirror of the
  pinned prover's own `parse_constants` grammar. An unparsable line, a duplicate name, or a
  non-literal value is `STOP`.
* Every name present in both the plan allocations and the constants table must be
  **byte-equal**; any divergence is `STOP rc 3`
  (`allocation_constants_value_divergence`) and the prover is not invoked.
* Every constants binding gets exactly one terminal `CONSTANT` row - `RECONCILED`,
  `RUNTIME_ONLY` or `STOP` - plus a `CONSTANTS_CONSERVATION` row.
* Independently, the analysis-unit builder requires, per source operand, that the allocation
  resolution, the constants resolution and the member `deploy_path` are the same string.
  This is defence in depth: it is unreachable while the reconciliation is enabled, and it
  exists so that removing the reconciliation cannot silently reopen F2.
* New claim `F10` (`allocation_constants_reconciliation`).

### F3 - RENDER no longer claims closure over members it does not model

`_derive_graph` records `member_kind_graph_derivation_not_modeled` `STOP` and blocks
derivation for any non-shell member, mirroring what FREEZE already did. RENDER can no longer
report `derived_source_graph PASS` over a `python_source` member.

### N1, N2 - the evidence contract

* The exact adapter-arm census is published and re-derivable by command: **33 arms, 5
  driven, 28 undriven**, with the undriven set classified by why it is undriven. Three arms
  that round 2 carried undriven are now driven by fixtures.
* Every falsification carries a **behavioural** pre-feature RED against the exact round-2
  code at `35a15219` - a real `PASS rc=0` over a defective program - plus a mutation
  discriminator against current code. The round-2 practice of presenting a schema rejection
  as the D026 RED is not repeated.
* Every published fence begins with `Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'`, closing
  the round-2 reproduction note that the harness mis-asserted from any other cwd.

## Stage coverage

### ALLOCATE

Unchanged from round 1. Six RED fixtures and one GREEN, all returning the same rc and reason
tokens. `sec102_r1_fixtures` has no worktree modification.

### RENDER

Everything round 2 implemented, plus:

1. Each member declares and is checked for one canonical, unique deployed identity.
2. Derived source and interpreter edges bind by exact deployed-path equality only.
3. A non-shell member STOPs graph derivation instead of being skipped.

### FREEZE

Everything round 2 implemented, plus:

1. The same deployed-identity binding, applied again to the frozen bytes.
2. The allocation/constants reconciliation, run before the prover is invocable.
3. The analysis-unit builder binds by deployed identity and requires allocation, constants
   and `deploy_path` agreement per operand.
4. A permanent `R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED` residual disclosure on every
   FREEZE report, so the word "identity" in `deployed_identity_binding` is not read as
   host-object identity.

## Self-QA result

- 37 cases, `FAILED_COUNT=0`. The 26 round-2 cases are included unchanged in rc and reason
  token; 11 are round-3 additions.
- 7 ALLOCATE regression cases: unchanged.
- 9 RENDER cases: 7 round-2 REDs, 1 new F3 RED, 1 GREEN.
- 21 FREEZE cases: 9 round-2 REDs, 9 new round-3 REDs, 1 F1 control (FAIL rc 1), 2 GREENs.
- D026 behavioural pre-feature: all three falsifications return `PASS rc=0` against the exact
  round-2 code at `35a15219` and nonzero against current code.
- D026 mutation: restoring the basename fallback, disabling the allocation/constants
  comparisons, or reverting the non-shell STOP each turns its RED fixture into an incorrect
  `PASS rc=0`.
- The F1 control proves the sinks were always catchable: with `evil/library.sh` declared as a
  member at its own `deploy_path`, the prover resolves 4 filesystem paths and 1 endpoint and
  forbids `/etc/shadow`, `/tmp/loot` and `exfil.example.invalid:443` at `rc 1`.
- Python 3.12 AST parse PASS; 33 JSON plans parse; all fixture bytes are LF-only;
  deterministic full stdout+rc PASS for both common GREENs; `git diff --check` PASS.
- `pathscope_prover.py` has no worktree diff and its kickoff identity was re-derived.

Literal commands and real output are in `SELF_QA_SEC102_R3.md`.

## Two round-2 fixtures were repointed - stated explicitly

The new reconciliation intercepts an unparsable `constants.env` at the composite level,
before the prover runs. `red_freeze_prover_grammar.json` and `red_freeze_residual.json`
previously drove their arms through `constants_bad.env`; they now drive the same arms
through an allowlist the pinned prover's own grammar refuses. Both keep their published rc
and reason token and keep their original semantics of "the prover ran and returned
degenerate output". `constants_bad.env` is retained and now drives the new
`red_freeze_constants_grammar.json`.

The two were given different allowlists deliberately - `allowlist_unparsable.txt` (`/**`)
and `allowlist_glob.txt` (`/safe/fix*ture/**`). As committed at `35a15219` those two round-2
plans were byte-identical, so the round-2 matrix asserted two different tokens against one
artifact; they are now two distinct artifacts with two distinct prover-side rejections.

## What remains - every item is a limitation

1. These are synthetic fixture proofs. The production P0 and RO entrypoints, RP0 library and
   bootstrap, RP6, RP7, inline Python bodies, and exact candidate `verify_lock.py` blob have
   not been supplied in a plan and have not passed this tool.
2. **The deployed identity is a declared, lexically canonical string compared for exact
   equality. It is not host-object verification.** No host was contacted. A plan that
   declares `deploy_path` truthfully gets a true binding; a plan that declares it falsely is
   not detected at this stage. This is disclosed on every FREEZE report as
   `R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED`, `control=false`.
3. Symlink resolution and mount-boundary identity remain residual R1. Their disclosures are
   not controls and cannot support an unconditional host-path claim.
4. ALLOCATE declares no deployed identity and makes no whole-program path claim.
5. The composite's constants mirror is narrower than the pinned prover's parser: a constant
   whose value expands another constant is refused, not modelled.
6. A constants binding the plan does not allocate is reported `RUNTIME_ONLY`, not stopped. It
   cannot influence member binding and any path or endpoint it produces is still adjudicated
   against the pinned allowlist, but it is a value the plan did not declare.
7. FREEZE accepts only all-shell reachable composites. A `python_source` member STOPs at
   FREEZE and, from this round, STOPs graph derivation at RENDER. The actual RO composite
   cannot yet PASS.
8. The analysis-unit builder supports only standalone direct `source`/`.` edges. It STOPs on
   `execute_source` and `inline_source`. The actual RO composite therefore cannot yet PASS.
9. RENDER graph analysis is intentionally incomplete and fail-closed: here-documents, line
   continuations, multiline quotes, command/process substitutions, `eval`, `alias`, and
   dynamic command positions all STOP.
10. The generated analysis unit uses a synthetic `test -r` to preserve each bound source
    operand while substituting exact child bytes. It is not an executable or frozen
    deployment artifact.
11. Allocation-consumer checking is exact template-token conservation plus
    allocation/constants value conservation plus exact deployed-path operand binding. It is
    not full semantic shell dataflow across every later use of an allocated value.
12. `sys.executable`, used to launch the pinned prover locally, is an external-runtime
    dependency not pinned by the plan.
13. The analysis unit and the exact prover/constants/allowlist snapshots are temporary local
    files removed at adapter exit. They are not frozen artifacts; inability to create, write
    or read them is STOP.
14. The implemented proof covers exact lexical filesystem and network operands. No closed
    runtime-descendant family or exact descendant manifest is implemented.
15. Bash startup sources, imported functions, inherited environment, interpreter identity,
    cwd, shell options, bootstrap PATH tools, temporary-path behavior, wrapper `/dev/null`
    opens, and RP6 exact venv binding remain production blockers from the design.
16. A prover input-read or constants/allowlist parse error does not emit seven counters; the
    composite correctly STOPs on that incomplete output grammar rather than inventing zeros.
17. 28 of 33 prover-adapter arms are carried undriven by published fixtures. The exact set
    and the reason for each class are in `SELF_QA_SEC102_R3.md` section 6.
18. A line-ending durability risk was found and is **not** fixed here, because the remedy is
    outside the round-3 scope fence: this clone has `core.autocrlf=true` under a root
    `.gitattributes` of `* text=auto`, so a fresh checkout on Windows would materialise the
    LF fixtures as CRLF and every byte pin would fail. The risk is pre-existing and applies
    to the round-2 fixture set as committed. Details and the one-line remedy are in
    `SELF_QA_SEC102_R3.md` section 8; the decision is the Lead's.
19. No archive was created or frozen. No host, dispatch, execution, deployment, or production
    Section 10.2 acceptance follows from a fixture PASS.

## Artifact identity record

The complete per-artifact byte-count and SHA-256 table is in
`SEC102_R3_REPORT_2026-08-11.md`. The report cannot contain its own final hash without a
self-reference; its final identity is recorded in the implementer completion transcript
provided to the Lead. No commit was made.
