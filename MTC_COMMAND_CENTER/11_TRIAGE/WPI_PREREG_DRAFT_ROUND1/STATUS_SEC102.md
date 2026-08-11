# Section 10.2 composite path-proof status

Date: 2026-08-11
Status: `ROUND-5-AUTHORED-SELF-QA-PASS-PENDING-INDEPENDENT-ACCEPTANCE`
Audit tier: T1 - local-only non-economic Python tooling and fixtures. Round 2 was audited by
the Claude flagship (verdict **BLOCK**, two CRITICAL). Round 3 repaired that BLOCK and was
audited by Codex `gpt-5.6-sol` (`SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md`, verdict
**REQUEST_CHANGES**: both CRITICALs confirmed closed, three MEDIUM findings raised). Round 4
repaired those three MEDIUMs and was audited by Codex (`SEC102_CODEX_T1_AUDIT_R4_2026-08-11.md`,
verdict **REQUEST_CHANGES**: R3-F2 and R3-F3 CLOSED and independently verified, **R3-F1
reopened as CRITICAL**). Round 5 is the repair of that CRITICAL, implemented by `claude-opus-5`
xhigh. No audit or acceptance is claimed by the implementer.

## Round 5 - what changed and why

### R4-F1 (the reopened R3-F1 CRITICAL) - command position is now conserved across every prefix

Round 4 built an independent command-word scanner, but that scanner conserved the command
position across only two of Bash's prefix forms: scalar assignment words and **numeric** file
descriptors. Bash's command grammar allows a simple command to carry any number of assignment
words and redirections before its command word, in any order, and none of them opens or closes
a command position.

The consequence Codex reproduced on the committed module: a valid named-descriptor prefix
(`{fd}>...`) or an indexed assignment prefix (`arr[0]=...`) was emitted as a benign leaf word,
that leaf closed the command position, and a `source`/interpreter operand behind it was then
classified by nothing. The matcher's regexes do not anchor through a prefix either, so
`_graph_word_conservation` saw no uncovered graph word - RENDER returned `PASS rc 0` over an
unanalysed program. Pattern 12 primary, Pattern 5 grammar incompleteness, Pattern 9 overlay.

* `SHELL_ASSIGNMENT_RE` now models the whole Bash assignment-word grammar: `NAME=`, `NAME+=`,
  `NAME[subscript]=`, `NAME[subscript]+=`. Bash requires the name to be unquoted and to start
  the word, so `2a=b`, `a-b=c`, `"a"=b` and `--opt=val` remain command names - leaving them as
  leaves is exact, not an approximation.
* New `_redirection_prefix_class` replaces the `raw.isdigit()` test. A word abutting `<`/`>`
  is a descriptor prefix only if it is all-ASCII-digits or `{name}` - the only two forms Bash
  accepts - and both conserve the command position. An ordinary word that merely touches the
  operator (`echo>out`) is still an ordinary word, because in Bash it is.
* New `_assignment_prefix_class` is the **fail-closed fence**: a command-position word that
  opens a subscript the model cannot close and carries an `=` (`arr[idx[0]]=1`) STOPs with
  `source_graph_unmodeled_assignment_prefix` **before** it can become a leaf. A brace word in
  the exact syntactic slot of a named descriptor whose interior is not a plain name (`{1}>...`)
  STOPs with `source_graph_unmodeled_redirection_prefix`.
* **Found while probing the same boundary, not named in the audit:** `function foo { source
  lib; }` and `coproc log { source lib; }` lost the body's first command word by the identical
  mechanism, reached through a reserved word instead of a prefix. New
  `SHELL_NAME_BINDING_WORDS = {function, coproc}` conserves the command position across the
  bound name. `for`/`select`/`case` also bind a name but a separator, newline or `)` re-opens
  the command position before their body, so nothing is lost there; they are unchanged and the
  argument is measured, not assumed.

Nothing else moved. **All four GREEN transcripts are byte-identical to the audited commit
`bb02c25a`**, so no fence was weakened and no output surface was added.

## Stage coverage

### ALLOCATE

Unchanged from round 1. Six RED fixtures and one GREEN, same rc and reason tokens.
`sec102_r1_fixtures` has no worktree modification.

### RENDER

Everything round 4 implemented, plus command-position conservation across every accepted Bash
assignment word and redirection prefix and across `function`/`coproc` name binding, with a
named STOP for any prefix shape outside that model.

### FREEZE

Everything round 4 implemented. FREEZE inherits the round-5 repair unchanged through the shared
`_derive_graph`, so `F3`/`F9` gain the same conservation; no FREEZE-specific code changed.

## Self-QA result

- 44 cases, `FAILED_COUNT=0`. **All 40 round-4 cases carried unchanged in rc and reason
  token**; 4 are round-5 additions. No carried fixture file was edited.
- 7 ALLOCATE regression cases: unchanged. 14 RENDER cases: 10 carried, 4 new. 23 FREEZE cases:
  unchanged.
- D026 behavioural pre-feature: each new fixture runs over byte-identical inputs against the
  round-4 code streamed from `bb02c25a` and against round-5 code. **All four are rc-level REDs**
  - `PASS rc 0` with `R4`, `R6` and `R7` all PASS, to `STOP rc 3`.
- D026 mutations: 5 discriminators run against all 4 new REDs - a 20-cell matrix that asserts
  its own expectation table (`OFF_EXPECTATION=0`). M1 restores the numeric-only descriptor
  handling and returns only the named-fd RED to PASS; M4 removes the name binding and returns
  only the function-body RED; M3 removes the fail-closed fence and returns only the unmodelled
  RED; M2 restores round 4's full assignment handling and returns two REDs, which is correct
  and stated. M5 narrows the model but keeps the fence, and the indexed RED stays STOP with a
  different reason token - proving the two fences are independent.
- The five carried round-3 and round-4 discriminators were re-run against round-5 code and all
  five still restore their defective PASS. Ten discriminators now exist across rounds 3-5.
- Prefix grammar battery: 16 blind forms, each an independently executed round-4 `PASS rc 0`,
  all 16 killed, 0 survived; 9 benign controls `rc 0` on both sides, four of which exercise the
  repaired paths directly; 1 disclosed conservative false stop.
- The round-4 grammar battery was re-run as a regression: 32 of 32 forms still `rc 3`, 5 of 5
  controls still `rc 0`.
- Scanner-boundary probe, both sides in one command: 7 forms where Bash reaches another program
  were silent on `bb02c25a` and are not silent now; 4 forms Bash does **not** reach remain
  correctly silent, which is what distinguishes a repair from a blanket STOP.
- Python AST parse PASS; 49 JSON plans parse; all fixture bytes LF-only; deterministic repeated
  stdout for two GREENs and two new REDs; `git diff --check` rc 0 over the two modified files.
- **Every PowerShell block in `SELF_QA_SEC102_R5.md` was extracted byte-for-byte and re-executed
  from a working directory outside the repository; 12 of 12 reproduce their published output.**
  The first such run failed 12 of 12 and exposed five real defects in the evidence document,
  including one published output line that had not been obtained by running the command. All
  five are fixed and the failure is recorded rather than removed.
- `pathscope_prover.py` has no worktree diff; its pin is unchanged and the FREEZE GREEN
  transcript is the running proof.

Literal commands and real output are in `SELF_QA_SEC102_R5.md`.

## What remains - every item is a limitation

Items 1-23 below carry forward from round 4. Items 24-27 are round-5 additions.

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
   claim sentence is narrowed so it no longer overstates this.
7. **F10 STOPs on every plan allocation absent from the pinned constants table, with no
   exemption.** A plan that legitimately declares a render-only allocation which is never a
   runtime constant will STOP. This is a chosen false stop, taken over a second modelled
   grammar.
8. **The command-word detection vocabulary is a list, and a list can be short.** An
   interpreter absent from it, invoked at a genuinely conserved command position under a
   literal name, is classified a benign leaf and derives no edge. **Round 5 repaired how the
   scanner reaches a command word, not which names it recognises**, so this half of R3-F1 is
   unchanged. Executing an arbitrary program (`./child.sh`) is outside every modelled edge kind
   and always was.
9. Wrapper detection produces safe false stops by design: `find`, `time`, `env`, `xargs` and
   similar STOP even with harmless operands, because the composite does not model what they
   run.
10. FREEZE accepts only all-shell reachable composites. A `python_source` member STOPs at
    FREEZE and STOPs graph derivation at RENDER. The actual RO composite cannot yet PASS.
11. The analysis-unit builder supports only standalone direct `source`/`.` edges. It STOPs on
    `execute_source` and `inline_source`.
12. RENDER graph analysis is intentionally incomplete and fail-closed: here-documents, line
    continuations, multiline quotes, command/process substitutions, `eval`, `alias`, dynamic
    command positions, every unmodelled command form, and now every unmodelled prefix form, all
    STOP.
13. The generated analysis unit uses a synthetic `test -r` to preserve each bound source
    operand while substituting exact child bytes. It is not an executable or frozen
    deployment artifact.
14. Allocation-consumer checking is exact template-token conservation plus
    allocation/constants value conservation plus exact deployed-path operand binding. It is
    not full semantic shell dataflow.
15. `sys.executable`, used to launch the pinned prover locally, is an external-runtime
    dependency not pinned by the plan. **Round 5 ran under Python 3.14.2**; 3.12 is no longer
    installed on this machine, so the round-4 3.12 parse is not reproduced and nothing here
    establishes behaviour under 3.12.
16. The analysis unit and the prover/constants/allowlist snapshots are temporary local files
    removed at adapter exit. They are not frozen artifacts.
17. The implemented proof covers exact lexical filesystem and network operands. No closed
    runtime-descendant family or exact descendant manifest is implemented.
18. Bash startup sources, imported functions, inherited environment, interpreter identity,
    cwd, shell options, bootstrap PATH tools, temporary-path behavior, wrapper `/dev/null`
    opens, and RP6 exact venv binding remain production blockers from the design.
19. A prover input-read or constants/allowlist parse error does not emit seven counters; the
    composite STOPs on that incomplete output grammar rather than inventing zeros.
20. **28 of 33 prover-adapter arms remain undriven** by published fixtures. Round 5 drove no
    new arm; the count and classification are unchanged from round 4.
21. **The `.gitattributes` repair is inert until the Lead commits it**, because Git reads
    checkout attributes from the committed tree. Round 5 adds `sec102_r5_fixtures/** -text` to
    the same scoped file; the round-4 demonstration of the mechanism is not re-run.
22. The `.gitattributes` covers this directory only. Every other byte-pinned artifact in the
    repository - RP6, RP7, the block files, the preregistration drafts - carries the same
    pre-existing line-ending exposure and is outside this fence.
23. No archive was created or frozen. No host, dispatch, execution, deployment, or production
    Section 10.2 acceptance follows from a fixture PASS.
24. **The prefix model is claimed complete for Bash assignment words and redirections, and that
    claim is exactly as strong as one reading of the Bash grammar.** The accepted vocabulary is
    `NAME=`, `NAME+=`, `NAME[sub]=`, `NAME[sub]+=` with a bracket-free subscript, plus numeric
    and `{name}` descriptors abutting a redirection operator. Anything outside it that
    *resembles* either shape STOPs by name. A prefix form that is neither enumerated nor
    resembling would still degrade to a leaf. None is known; that is a statement about the
    implementer's knowledge, not a proof.
25. **`for` / `select` / `case` are argued safe, not repaired.** They bind a name like
    `function`/`coproc`, but a separator, newline or `)` re-opens the command position before
    any body command. Two probes measure this; it is not an exhaustive enumeration of
    reserved-word syntax.
26. **New conservative false stops, deliberately taken.** `{1}>...` and any brace word abutting
    a redirection whose interior is not a plain name STOP although Bash would treat them as
    ordinary words. An `arr[...` word carrying an `=` whose subscript the model cannot close
    STOPs although a user may have meant a command name. Both are disclosed rather than tuned
    away.
27. **`raw.isdigit()` was narrowed to `^[0-9]+$`.** The old test accepted Unicode digits, so
    `2>`-shaped words such as `<superscript-two>>out` were swallowed as descriptor prefixes.
    Bash does not do that. The narrowing matches Bash and loses no edge, but it is a behaviour
    change and is recorded as one.

## Artifact identity record

The complete per-artifact byte-count and SHA-256 table is in `SEC102_R5_REPORT_2026-08-11.md`
section 6, and in `SELF_QA_SEC102_R5.md` section 9, both re-derivable by the published command.
No commit was made.
