# Section 10.2 composite path-proof status

Date: 2026-08-11
Status: `ROUND-6-AUTHORED-SELF-QA-PASS-PENDING-INDEPENDENT-ACCEPTANCE`
Audit tier: T1 - local-only non-economic Python tooling and fixtures. Round 2 was audited by
the Claude flagship (verdict **BLOCK**, two CRITICAL). Round 3 repaired that BLOCK and was
audited by Codex `gpt-5.6-sol` (`SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md`, verdict
**REQUEST_CHANGES**: both CRITICALs confirmed closed, three MEDIUM findings raised). Round 4
repaired those three MEDIUMs and was audited by Codex (`SEC102_CODEX_T1_AUDIT_R4_2026-08-11.md`,
verdict **REQUEST_CHANGES**: R3-F2 and R3-F3 CLOSED, **R3-F1 reopened as CRITICAL**). Round 5
repaired that CRITICAL and was audited by Codex (`SEC102_CODEX_T1_AUDIT_R5_2026-08-11.md`,
verdict **REQUEST_CHANGES**: named-fd, indexed-assign and unmodeled-prefix confirmed closed,
**R5-F1 raised as CRITICAL** - a pathname-expanded command word still leafed a hidden
interpreter). Round 6 is the repair of that CRITICAL, implemented by `claude-opus-5` xhigh.
No audit or acceptance is claimed by the implementer.

## Round 6 - what changed and why

### R5-F1 - the command-word policy is now closed, not enumerated

Rounds 4 and 5 each closed one command-word or prefix form *after it was found*: a numeric file
descriptor, then a named descriptor, then an indexed assignment. The round-5 audit then found a
fourth of the same shape - `_command_word_class` classified a pathname-expanded word such as
`/usr/bin/ba*h` as a benign leaf, so the script operand behind a runtime-resolved interpreter
was scanned by nothing and RENDER returned `PASS rc 0` over an unanalysed program.

The defect was not any one missing form. It was the classifier's **default**: an unrecognised
command word became a leaf, so every form nobody had enumerated inherited "benign". Closing
forms one per round cannot reach a fixpoint against that default.

Round 6 inverts the default. A command word is admissible as a benign non-edge leaf **only**
when it is a PROVEN-STATIC literal that is not a recognised interpreter or source builtin -
one word whose spelling is already the name Bash will look up, with no expansion of any kind
between the two. Every command word that is dynamic, expandable or substituted is UNMODELED
and the stage STOPs; it can never become a leaf, whatever it would have expanded to.

* New `COMMAND_WORD_SUBSTITUTION_RE` (`$`, backtick) - parameter, command and arithmetic
  expansion. Deliberately redundant with `_graph_opaque_reason`, so no single fence carries
  this class alone.
* New `COMMAND_WORD_EXPANSION_RE` (`*`, `?`, `[`, `]`, `{`, `}`, `~`, `\`) - pathname
  expansion, brace expansion, tilde expansion, and backslash-constructed names. Applied to the
  raw word including quoted regions: quoting suppresses some of these, but a proof that this
  particular occurrence is suppressed is exactly the reasoning the policy refuses to do.
* `_command_word_class` now returns the new `unmodeled` class for every such word plus for a
  degenerate/empty word, and `_graph_word_conservation` reports it as
  `source_graph_unmodeled_command_word`. Reserved words (`{`, `}`, `[[`, `]]`, `!`, `if` …)
  and assignment prefixes are matched **before** the fence and are unaffected.
* The reserved-word test now compares the RAW word instead of its unquoted literal. Bash only
  treats `if`/`{`/`[[` as reserved when written unquoted, so `"if"` is an ordinary command
  name; reading the literal promoted it to a reserved word and kept a command position open
  that Bash had already closed.
* **Found while probing the same boundary, not named in the audit:** interpreter recognition
  took the basename only for an *absolute* path, so `bin/bash script.sh` and `./bash script.sh`
  were leaves while `/bin/bash script.sh` was recognised - the same interpreter, the same
  operand, hidden by a spelling. Recognition now takes the last pathname component of any
  command word containing a slash. This is measured, not assumed: it is a separate RED fixture
  and a separate mutation discriminator.

Nothing else moved. **All four carried GREEN transcripts are byte-identical to the audited
commit `e3906cec`**, so no fence was weakened and no output surface was added.

### What round 6 does NOT close

The recognised-interpreter **vocabulary** is still a list, not a proof that the list is
exhaustive. A proven-static literal that names an executable-capable program the list does not
contain is still a benign leaf. Round 6 closed *how a command word is admitted*; it did not
close *which names are recognised*. That remains the disclosed production blocker Codex
restated in the round-5 audit, and no claim here weakens it.

## Stage coverage

### ALLOCATE

Unchanged from round 1. Six RED fixtures and one GREEN, same rc and reason tokens.
`sec102_r1_fixtures` has no worktree modification.

### RENDER

Everything round 5 implemented, plus the closed command-word admissibility policy and
slash-relative interpreter recognition, with a named STOP for every command word that is not a
proven-static benign literal.

### FREEZE

Everything round 5 implemented. FREEZE inherits the round-6 repair unchanged through the shared
`_derive_graph`, so `F3`/`F9` gain the same conservation; no FREEZE-specific code changed.

## Self-QA result

- 52 cases, `FAILED_COUNT=0`. **All 44 round-5 cases carried unchanged in rc and reason token**;
  8 are round-6 additions. No carried fixture file was edited.
- 7 ALLOCATE regression cases: unchanged. 22 RENDER cases: 14 carried, 8 new. 23 FREEZE cases:
  unchanged.
- D026 behavioural pre-feature: **5 of the 7 new RED fixtures are rc-level REDs** - `PASS rc 0`
  on `e3906cec` to `STOP rc 3` under round-6 code (glob, bracket-glob, brace, tilde,
  relative-path interpreter). The remaining two (parameter expansion, command substitution)
  were **already `STOP rc 3` at `e3906cec`** and are carried as controls, not claimed as new
  REDs; the kickoff's expectation that they leafed into a PASS is not what the tool does, and
  the measured before-state is published rather than the expectation.
- Scanner boundary, both sides in one command: 32 probes, `OFF_EXPECTATION=0`. **12 forms where
  Bash reaches another program were silent on `e3906cec` and are not silent now.** 8 benign
  forms remain correctly silent and 3 modelled interpreter/source forms still derive their
  edge, which is what distinguishes a repair from a blanket STOP. 4 forms are asserted as
  disclosed conservative stops so they cannot drift unnoticed.
- D026 mutations: 6 new discriminators run against **all 11 REDs** (7 round-6 + 4 round-5) - a
  66-cell matrix asserting its own expectation table, `OFF_EXPECTATION=0`. **Every mutation that
  removes a round-6 fence leaves all four round-5 REDs intact**, which is the discriminator the
  round-5 audit required.
- Command-word grammar battery: 59 declared forms plus a generative closure sweep of 180
  variants (10 expansion characters x 6 bases x 3 positions). `SWEEP_LEAKS=0`: no word carrying
  an expansion or substitution character is admitted as a leaf or promoted to a graph word.
- The round-5 prefix battery was re-run as a round-6 regression: 16 of 16 blind forms still
  `rc 3`, 8 of 9 controls still `rc 0`, and **one round-5 control moved to a disclosed
  conservative stop** (`SEEN[0] "$ROOT/in.txt"`, a bracket-expression token in command
  position). The move is published, not tuned away.
- The five carried round-3/round-4 discriminators were re-run against round-6 code and all five
  still restore their defective PASS. **Three of the five round-5 discriminators no longer
  discriminate**, because the round-6 fence independently catches their forms; each is re-probed
  and its remaining role measured - `M4` (name binding) is still solely load-bearing, and `M1`,
  `M2`, `M5` still carry precision for benign controls that flip to STOP without them.
- Python AST parse PASS; all r6 JSON plans parse; all r6 fixture bytes LF-only; deterministic
  repeated stdout over three runs for two new REDs and one new GREEN.
- `pathscope_prover.py` has no worktree diff; its pin is unchanged and the FREEZE GREEN
  transcript is the running proof. `sec102_r1..r5_fixtures` have no worktree diff.

Literal commands and real output are in `SELF_QA_SEC102_R6.md`.

## What remains - every item is a limitation

Items 1-27 carry forward from round 5, with items 8 and 12 corrected as the round-5 audit
required. Items 28-31 are round-6 additions.

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
8. **CORRECTED IN ROUND 6. The command-word recognition vocabulary is a list, and a list can be
   short.** An executable-capable program absent from that list, written as a proven-static
   literal at a conserved command position, is still classified a benign leaf and derives no
   edge. What round 6 changed is the *exposure* of that residual: a word can now only reach
   the vocabulary test if its spelling is already the name Bash will look up, so an unknown
   name can no longer be smuggled in behind an expansion. Round 5's statement that it "repaired
   how the scanner reaches a command word, not which names it recognises" is still true and
   still the residual. Executing an arbitrary program (`./child.sh`) is outside every modelled
   edge kind and always was.
9. Wrapper detection produces safe false stops by design: `find`, `time`, `env`, `xargs` and
   similar STOP even with harmless operands, because the composite does not model what they
   run.
10. FREEZE accepts only all-shell reachable composites. A `python_source` member STOPs at
    FREEZE and STOPs graph derivation at RENDER. The actual RO composite cannot yet PASS.
11. The analysis-unit builder supports only standalone direct `source`/`.` edges. It STOPs on
    `execute_source` and `inline_source`.
12. **CORRECTED IN ROUND 6.** RENDER graph analysis is intentionally incomplete and fail-closed.
    The round-5 wording said "dynamic command positions … STOP", which outran the predicate:
    a pathname-expanded command word did not STOP, it leafed. The accurate statement is now:
    here-documents, line continuations, multiline quotes, command/process substitutions,
    `eval`, `alias`, every unmodelled prefix form, and **every command-position word that is
    not a proven-static literal** - parameter/command/arithmetic expansion, pathname
    expansion, brace expansion, tilde expansion, backslash-constructed names, degenerate
    quoting - all STOP. The residual is item 8: a proven-static literal outside the recognised
    vocabulary is still a leaf, and that is a vocabulary limit, not a command-position limit.
13. The generated analysis unit uses a synthetic `test -r` to preserve each bound source
    operand while substituting exact child bytes. It is not an executable or frozen
    deployment artifact.
14. Allocation-consumer checking is exact template-token conservation plus
    allocation/constants value conservation plus exact deployed-path operand binding. It is
    not full semantic shell dataflow.
15. `sys.executable`, used to launch the pinned prover locally, is an external-runtime
    dependency not pinned by the plan. **Round 6 ran under Python 3.14.2**; 3.12 is no longer
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
20. **28 of 33 prover-adapter arms remain undriven** by published fixtures. Round 6 drove no
    new arm; the count and classification are unchanged from round 4.
21. **The `.gitattributes` repair is inert until the Lead commits it**, because Git reads
    checkout attributes from the committed tree. Round 6 adds `sec102_r6_fixtures/** -text` to
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
    *resembles* either shape STOPs by name. Round 6 adds a second, independent net under this
    one: a prefix that degrades into a command-position word now also faces the closed
    admissibility policy, which is measured in the round-5-fence redundancy probe.
25. **`for` / `select` / `case` are argued safe, not repaired.** They bind a name like
    `function`/`coproc`, but a separator, newline or `)` re-opens the command position before
    any body command. Two probes measure this; it is not an exhaustive enumeration of
    reserved-word syntax.
26. **Round-5 conservative false stops, carried unchanged.** `{1}>...` and any brace word
    abutting a redirection whose interior is not a plain name STOP although Bash would treat
    them as ordinary words. An `arr[...` word carrying an `=` whose subscript the model cannot
    close STOPs although a user may have meant a command name.
27. **`raw.isdigit()` was narrowed to `^[0-9]+$` in round 5.** The old test accepted Unicode
    digits. The narrowing matches Bash and loses no edge, but it is a behaviour change and is
    recorded as one.
28. **New conservative false stops, deliberately taken and larger than round 5's.** Every
    command-position word carrying `*`, `?`, `[`, `]`, `{`, `}`, `~` or `\` now STOPs, whether
    or not Bash would actually expand that occurrence. Concretely: the `[` test builtin
    (`[ -f x ]`) STOPs, `\cat` STOPs, `~/bin/mytool` STOPs, and a subscript word without an
    `=` (`SEEN[0] "$ROOT/in.txt"`) STOPs - the last was a published round-5 control at `rc 0`.
    These are refusals, not detections, and the policy prefers a visible refusal to a proof
    that a particular occurrence was safe.
29. **Quoted occurrences are not excused.** `'*'` is a literal star to Bash but STOPs here. The
    fence reads the raw word, because deciding that quoting suppressed a specific expansion is
    the class of reasoning that produced R5-F1.
30. **The expansion character set is itself a list.** It covers the expansions Bash performs on
    a command word before lookup as the implementer reads the grammar. `extglob`, `globstar`
    and similar option-enabled patterns are built from the same characters and are therefore
    covered by construction, but no proof is offered that the character set is complete for
    every shell option. This is a strictly smaller residual than round 5's, not zero.
31. **Three round-5 discriminators became non-discriminating.** `M1`, `M2` and `M3` no longer
    return their round-5 REDs to PASS, because the round-6 command-word fence catches those
    forms independently. This is defence in depth, not a lost guard: each is re-probed, and the
    round-5 mechanisms are shown to still carry precision for benign controls. It does mean the
    round-5 REDs no longer test only one mechanism, and that is recorded rather than hidden.

## Artifact identity record

The complete per-artifact byte-count and SHA-256 table is in `SEC102_R6_REPORT_2026-08-11.md`
section 6, and in `SELF_QA_SEC102_R6.md` section 9, both re-derivable by the published command.
No commit was made.
