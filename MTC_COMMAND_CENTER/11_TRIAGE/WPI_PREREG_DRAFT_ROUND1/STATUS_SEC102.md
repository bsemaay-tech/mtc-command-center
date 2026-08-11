# Section 10.2 composite path-proof status

Date: 2026-08-11  
Status: `ROUND-2-AUTHORED-SELF-QA-PASS-PENDING-INDEPENDENT-ACCEPTANCE`
Audit tier: T1 - local-only non-economic Python tooling and fixtures. The implementation
diff exceeds 300 lines; the permanent T1 policy therefore requires the Claude flagship
review named in the kickoff plus the conditional GLM-5.2 second opinion. No audit or
acceptance is claimed by the implementer.

## Round 2 coverage

`composite_pathproof.py` now implements all three ordered stages.

### ALLOCATE

The round-1 ALLOCATE implementation is retained. Its six RED fixtures and common GREEN
still return the same rc and reason tokens. It remains a declaration-conservation and
local-identity stage, not a Section 10.2 proof by itself.

### RENDER

RENDER now:

1. Requires one distinct template binding per input member and emits a terminal row for
   every binding and member.
2. Revalidates the allocation requirements, allocations, and consumer references.
3. Substitutes only exact `{{NAME}}` allocation tokens, requires the token set for each
   member to equal its declared consumer set, refuses malformed/unknown tokens, and
   compares the result to the rendered member bytes exactly.
4. Re-identifies every rendered member by byte count and SHA-256.
5. Derives direct `source`/`.` and simple file-backed interpreter edges from rendered
   bytes, compares them one-for-one with the declared edge set, traverses from the entrypoint,
   and rejects cycles, unknown targets, omitted edges, and unreachable members.
6. STOPs rather than guessing on dynamic source operands and deliberately unmodeled graph
   grammar. The here-document falsification proves that text inside a here-document cannot
   manufacture a passing source edge.

The common GREEN is `green_render.json`; six claim REDs plus the here-document
falsification precede it in `SELF_QA_SEC102_R2.md`.

### FREEZE

FREEZE now:

1. Revalidates allocation closure and re-derives the graph from the frozen member bytes.
2. Requires one member pin per member and exact byte-count/SHA-256 pins for every member,
   the constants file, and the allowlist file.
3. Requires the repaired prover identity exactly: `pathscope_prover.py`, 122446 bytes,
   SHA-256 `890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`.
4. Carries the exact verified member, constants, allowlist, and prover byte snapshots into
   the adapter, so the bytes analyzed and executed as the prover are the bytes that passed
   the pins rather than a later path re-read.
5. Builds one entrypoint-driven static analysis unit. Each mechanically bound standalone
   source edge becomes a modeled readability operand plus the exact pinned child bytes.
   The generated unit is parser input only and is never executed.
6. Invokes the pinned prover snapshot and consumes its current output grammar:
   `resolved_fs_path_count`, `resolved_net_endpoint_count`, `unresolved_path_count`,
   `unresolved_endpoint_count`, `coverage_issue_count`, `provenance_issue_count`, and
   `parse_issue_count`, plus `kind=` on every `UNRESOLVED` record.
7. Reconciles count lines against every `PATH`, `ENDPOINT`, and `UNRESOLVED` record; checks
   stdout grammar, stderr, process rc, terminal verdict, terminal rc, and terminal reason;
   and refuses zero-fact PASS.
8. Maps any unresolved or coverage record to composite STOP rc 3, an outside-allowlist
   prover REJECT to composite FAIL rc 1, and only fully reconciled lexical scope to PASS
   rc 0.
9. Carries `ALLOW-LEXICAL` forward without upgrading it to host-object proof. Every valid
   prover result emits both residuals as `DISCLOSURE control=false`:
   symlink resolution not established and mount boundary not established.
10. Emits one terminal row for every input member, member pin, declared edge, proof input,
   prover record, and residual.

The primary GREEN `green_freeze.json` produces three allowed filesystem records. The
second GREEN `green_freeze_network.json` produces one allowed filesystem record and one
allowed endpoint record, proving both resolved counters and both record grammars are
consumed. Coverage STOP, forbidden FAIL, malformed prover grammar STOP, pin mismatch,
graph mismatch, missing residual, and member-conservation REDs are all executable.

## Self-QA result

- 7 ALLOCATE regression cases: all expected rc/token assertions PASS.
- 8 RENDER cases: 6 claim REDs, 1 Pattern-12 RED, and 1 GREEN all PASS assertions.
- 11 FREEZE cases: 9 REDs and 2 GREENs all PASS assertions.
- D026 exact pre-feature run: both new GREEN plans are RED against commit `73e92844`.
- D026 render mutation: disabling the exact byte comparison changes the materialisation
  RED from rc 1 to an incorrect PASS rc 0.
- D026 coverage mutation: disabling issue/terminal enforcement changes a prover rc-3
  coverage record into an incorrect composite PASS rc 0.
- Python 3.12 AST parse PASS; 19 JSON plans parse; deterministic full stdout+rc PASS for
  both common GREENs; `git diff --check` PASS.
- `pathscope_prover.py` has no worktree diff and its kickoff identity was re-derived.

Literal commands and real output are in `SELF_QA_SEC102_R2.md`.

## What remains - every item is a limitation

1. These are synthetic fixture proofs. The production P0 and RO entrypoints, RP0 library
   and bootstrap, RP6, RP7, inline Python bodies, and exact candidate `verify_lock.py` blob
   have not been supplied in an R2 plan and have not passed this tool.
2. FREEZE currently accepts only all-shell reachable composites. A `python_source` member
   STOPs. The actual RO composite therefore cannot yet PASS.
3. The analysis-unit builder supports only standalone direct `source`/`.` edges. It STOPs
   on `execute_source` and `inline_source`. The actual RO composite therefore cannot yet
   PASS.
4. RENDER graph analysis is intentionally incomplete and fail-closed. It STOPs on
   here-documents, line continuations, multiline quotes, command/process substitutions,
   `eval`, `alias`, and dynamic command positions.
5. The generated static analysis unit uses a synthetic `test -r` to preserve each bound
   source operand while substituting exact child bytes. It is not an executable or frozen
   deployment artifact.
6. Allocation-consumer checking is exact template-token conservation, not full semantic
   shell dataflow across every later use.
7. `sys.executable`, used to launch the pinned prover locally, is an external-runtime
   dependency not pinned by the plan.
8. The analysis unit and exact prover/constants/allowlist snapshots are temporary local
   files removed at adapter exit. They are not frozen artifacts; inability to create,
   write, or read them is STOP.
9. The implemented proof covers exact lexical filesystem/network operands. No closed
   runtime-descendant family or exact descendant manifest is implemented.
10. Symlink resolution and mount-boundary identity remain residual R1. Their disclosures
    are not controls and cannot support an unconditional host-path claim.
11. Bash startup sources, imported functions, inherited environment, interpreter identity,
    cwd, shell options, bootstrap PATH tools, temporary-path behavior, wrapper `/dev/null`
    opens, and RP6 exact venv binding remain production blockers from the design.
12. A prover input-read or constants/allowlist parse error does not emit seven counters;
    the composite correctly STOPs on that incomplete output grammar rather than inventing
    zeros.
13. No archive was created or frozen. No host, dispatch, execution, deployment, or
    production Section 10.2 acceptance follows from a fixture PASS.

## Artifact identity record

The complete per-artifact byte-count and SHA-256 table is in
`SEC102_R2_REPORT_2026-08-11.md`. The report cannot contain its own final hash without a
self-reference; its final identity is recorded in the implementer completion transcript
provided to the Lead. No commit was made.
