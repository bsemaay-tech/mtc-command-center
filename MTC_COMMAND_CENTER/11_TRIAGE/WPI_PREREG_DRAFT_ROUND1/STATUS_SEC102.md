# Section 10.2 composite path-proof status

Date: 2026-08-12
Status: `ROUND-7-AUTHORED-SELF-QA-PASS-PENDING-INDEPENDENT-ACCEPTANCE`
Audit tier: T1 - local-only non-economic Python tooling and fixtures. Round 2 was audited by
the Claude flagship (verdict **BLOCK**, two CRITICAL). Round 3 repaired that BLOCK and was
audited by Codex `gpt-5.6-sol` (`SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md`, verdict
**REQUEST_CHANGES**: both CRITICALs confirmed closed, three MEDIUM findings raised). Round 4
repaired those three MEDIUMs and was audited by Codex (`SEC102_CODEX_T1_AUDIT_R4_2026-08-11.md`,
verdict **REQUEST_CHANGES**: R3-F2 and R3-F3 CLOSED, **R3-F1 reopened as CRITICAL**). Round 5
repaired that CRITICAL and was audited by Codex (`SEC102_CODEX_T1_AUDIT_R5_2026-08-11.md`,
verdict **REQUEST_CHANGES**: named-fd, indexed-assign and unmodeled-prefix confirmed closed,
**R5-F1 raised as CRITICAL** - a pathname-expanded command word still leafed a hidden
interpreter). Round 6 repaired that CRITICAL and was audited by Codex
(`SEC102_CODEX_T1_AUDIT_R6_2026-08-12.md`, verdict **REQUEST_CHANGES**, materially narrowed: the
interpreter-vocabulary residual and the conservative false stops were **ACCEPTED** as scoped
limitations, and one finding was raised - **R6-F1**, the round-6 expansion blacklist missed the
`extglob` operator family). Round 7 is the repair of R6-F1, implemented by `claude-opus-5` xhigh.
No audit or acceptance is claimed by the implementer.

## Round 7 - what changed and why

### R6-F1 - the admission test is now a WHITELIST, so incompleteness fails closed

Round 6 asked whether a command word **contained** one of a listed set of expansion
metacharacters (`*`, `?`, `[`, `]`, `{`, `}`, `~`, `\`). The round-6 audit found that this list
missed the `extglob` operator family: one-or-more `+(...)`, exactly-one `@(...)` and negated
`!(...)` carry none of the listed characters, so with `extglob` enabled
`/usr/bin/ba+(s)h library.sh` pathname-resolves to `bash`, runs the operand, and round 6
classified it as a benign leaf and returned `PASS rc 0` over an unanalysed program.

Adding three characters would have bought one round. Rounds 4, 5 and 6 each closed a class after
it was found; the regress is structural, because **while the test enumerates what is forbidden,
completeness depends on the enumeration, and no static tool can prove an enumeration of shell
operators complete.**

Round 7 inverts the direction of proof. A command word is admissible as a proven-static benign
leaf **only when every character of the raw, pre-expansion word token is in an explicit safe
set**. Any other character - a known operator, an unknown operator, or a character with no shell
meaning at all - makes the word not proven-static, so it is UNMODELED and the stage STOPs.

* **The safe set is `[A-Za-z0-9._/:-]`** (`COMMAND_WORD_STATIC_RE`), and every member is admitted
  with a stated reason, not by convenience. `composite_pathproof.py:207-268` carries the full
  justification per character; `SELF_QA_SEC102_R7.md` section 1 reproduces it as a table.
* `?`, `*`, `+`, `@` and `!` - the five `extglob` operator characters - are all excluded, which
  refuses the whole family in one rule instead of by enumeration. `%`, `=`, quote characters,
  `,`, `^`, `#` and every other character are excluded because no proof was offered that they
  cannot resolve.
* **The kickoff's illustrative safe set `[A-Za-z0-9._/+=:@%-]` does not close the finding**, and
  this is measured rather than argued: `+` and `@` in it are two of the five `extglob` operators.
  It is mutation `M2` in the self-QA, and under it two round-7 REDs return to `PASS`. The
  implemented set is strictly smaller and the difference is the repair.
* One scanner change, which decides nothing: the scanner used to split a word at `(`, so
  `ba+(s)h` reached the classifier as the three fragments `ba+`, `s`, `h`. The `(` is now
  conserved INTO the raw token unless the token is a NAME (the function-definition form
  `fixture_main()`), so the safe set adjudicates the word Bash would look up. Mutation `M3` turns
  this off and kills nothing, because the safe set already refuses `ba+`; it is published as a
  correctness fix to what the classifier is shown, not as an independent guard.
* No reason token was added or renamed. Every refusal still reports
  `source_graph_unmodeled_command_word`, so no carried expectation moved.

### The closure claim, narrowed to exactly what the predicate proves

Round 7 proves this and only this: **no command-position word containing a character outside
`[A-Za-z0-9._/:-]` is admitted as a benign leaf or promoted to a modelled graph word, and no
word made only of those characters is refused.** That property is swept over all 95 printable
ASCII characters plus a non-ASCII sample, in four positions over six bases - 1919 variants,
`SWEEP_LEAK_ADMITTED=0`, `SWEEP_LEAK_OVERREFUSED=0` - and a second pass requires the refusal to
reach a terminal STOP rather than merely a class.

It does **not** claim the safe set is provably correct for every shell. It claims that an error
in the reading of the Bash grammar now produces a false STOP instead of a false PASS. That is a
better failure direction, not a proof.

It does **not** close the interpreter vocabulary (item 8), which remains the production-gate
blocker the round-6 audit accepted as a scoped limitation.

### What round 6 changed, carried forward

Round 6 is the round that inverted the classifier's DEFAULT (a command word must earn `leaf`
rather than inherit it) and taught interpreter recognition to take the last pathname component of
any word containing a slash. Round 7 changed how "proven-static" is decided; everything else
round 6 established is carried unchanged and re-measured.

### The superseded round-6 statement

The paragraph below is the round-6 record. It is retained because the round-7 self-QA carries
round 6's batteries, and its final sentence - that the expansion character set is itself a list -
is precisely the residual round 7 closes.

### R5-F1 - the command-word policy is now closed, not enumerated (round 6)

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

### What round 7 does NOT close

The recognised-interpreter **vocabulary** is still a list, not a proof that the list is
exhaustive. A proven-static literal made only of safe-set characters that names an
executable-capable program the list does not contain is still a benign leaf. Rounds 6 and 7
closed *how a command word is admitted*; neither closed *which names are recognised*. That
remains the disclosed production blocker, accepted by the round-6 audit as a scoped limitation
at this stage, and no claim here weakens it.

## Stage coverage

### ALLOCATE

Unchanged from round 1. Six RED fixtures and one GREEN, same rc and reason tokens.
`sec102_r1_fixtures` has no worktree modification.

### RENDER

Everything round 6 implemented, with the round-6 expansion blacklist replaced by the round-7
safe-set whitelist and the round-7 word-boundary conservation, so every command word that is not
a proven-static safe-set literal reaches a named STOP.

### FREEZE

Everything round 6 implemented. FREEZE inherits the round-7 repair unchanged through the shared
`_derive_graph`, so `F3`/`F9` gain the same conservation; no FREEZE-specific code changed.

## Self-QA result (round 7)

- 58 cases, `FAILED_COUNT=0`. **All 52 round-6 cases carried unchanged in rc and reason token**;
  6 are round-7 additions. No carried fixture file was edited.
- D026 behavioural pre-feature: **4 of the 5 new RED fixtures are rc-level REDs** - `PASS rc 0`
  on `90868b86` to `STOP rc 3` under round-7 code (`+(`, `@(`, `!(`, and the unenumerated `%`).
  The fifth (`?(`) was **already `STOP rc 3` at `90868b86`** because `?` was on the round-6
  blacklist, and is carried as a control, not claimed as a new RED. The kickoff groups `?(`/`@(`
  as one class; the measured before-state is published rather than the grouping.
- Scanner boundary, both sides in one command: 49 probes, `OFF_EXPECTATION=0`. **10 forms that
  reach another program were silent on `90868b86` and are not silent now.** 13 benign forms
  remain correctly silent and 3 modelled interpreter/source forms still derive their edge, which
  is what distinguishes a repair from a blanket STOP. 9 forms are asserted as disclosed
  conservative stops so they cannot drift.
- D026 mutations: 7 discriminators run against **all 16 REDs** (5 round-7 + 7 round-6 + 4
  round-5) - a 112-cell matrix asserting its own expectation table, `OFF_EXPECTATION=0`.
  **`M1` restores the round-6 blacklist verbatim and returns exactly the four new REDs to
  `PASS`**, which is the discriminator the round-6 finding requires. `M2` does the same with the
  kickoff's illustrative safe set. `M5` widens the safe set to every printable character and
  shows the NARROWNESS carries the property. **`M3` (word-boundary conservation off) kills
  nothing** and is published as such.
- Command-word grammar battery: **all 59 round-6 forms carried**, 6 of them declared MOVED in
  advance (`"bash"`, `'source'`, `"if"` on quote characters; `2a=b`, `--opt=val`, `a-b=c` on
  `=`), plus 18 round-7 forms and a 7-form word-boundary table. `OFF_EXPECTATION=0`.
- **Fixpoint sweep: all 95 printable ASCII characters plus a non-ASCII sample, 4 positions, 6
  bases = 1919 variants. `SWEEP_LEAK_ADMITTED=0`, `SWEEP_LEAK_OVERREFUSED=0`, `SILENT_LEAK=0`.**
  The block also asserts that the safe set it measures against equals the one the module
  implements, so the sweep cannot drift from its subject.
- The round-5 prefix battery re-ran unchanged under round-7 code: 16/16 blind forms `rc 3`, 8/8
  controls `rc 0`, both round-6 disclosed stops unchanged. **No form moved between round 6 and
  round 7 in that battery.**
- The five carried round-3/round-4 discriminators all still restore their defective `PASS`.
- Python AST parse PASS; all 6 r7 JSON plans parse; all 18 r7 fixture files LF-only; every
  rendered `.sh` equals its `.in` with the fixture allocations substituted; deterministic
  repeated stdout over three runs for two new REDs and the new GREEN.
- `pathscope_prover.py` has no worktree diff; its pin is unchanged and the FREEZE GREEN
  transcript is the running proof. `sec102_r1..r6_fixtures` have no worktree diff.
- Every `powershell` block in `SELF_QA_SEC102_R7.md` was re-extracted from the document and
  re-run from a working directory OUTSIDE the repository: 10 blocks, 0 mismatched.

Literal commands and real output are in `SELF_QA_SEC102_R7.md`.

## Self-QA result (round 6, carried record)

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
required. Items 28-31 are round-6 additions; items 30 and 31 are corrected below for round 7.
Items 32-36 are round-7 additions. **Item 8 is the production-gate blocker.**

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
8. **THE PRODUCTION-GATE BLOCKER, unchanged by round 7. The command-word recognition vocabulary
   is a list, and a list can be short.** An executable-capable program absent from that list,
   written as a safe-set-only literal at a conserved command position, is still classified a
   benign leaf and derives no edge. What rounds 6 and 7 changed is the *exposure* of that
   residual: a word can only reach the vocabulary test if every character of it is proven inert,
   so an unknown name cannot be smuggled in behind an expansion of any kind. Round 5's statement
   that it "repaired how the scanner reaches a command word, not which names it recognises" is
   still true and still the residual. The round-6 audit accepted this as a scoped limitation at
   this stage; that acceptance is not a closure and round 7 does not claim to narrow it further.
   Executing an arbitrary program (`./child.sh`) is outside every modelled edge kind and always
   was.
9. Wrapper detection produces safe false stops by design: `find`, `time`, `env`, `xargs` and
   similar STOP even with harmless operands, because the composite does not model what they
   run.
10. FREEZE accepts only all-shell reachable composites. A `python_source` member STOPs at
    FREEZE and STOPs graph derivation at RENDER. The actual RO composite cannot yet PASS.
11. The analysis-unit builder supports only standalone direct `source`/`.` edges. It STOPs on
    `execute_source` and `inline_source`.
12. **CORRECTED IN ROUND 6, RESTATED IN ROUND 7.** RENDER graph analysis is intentionally
    incomplete and fail-closed. The round-5 wording said "dynamic command positions … STOP",
    which outran the predicate; the round-6 wording enumerated the expansions that STOP, which
    is what missed `extglob`. The accurate statement is now the whitelist itself:
    here-documents, line continuations, multiline quotes, command/process substitutions,
    `eval`, `alias`, every unmodelled prefix form, and **every command-position word carrying
    any character outside `[A-Za-z0-9._/:-]`** all STOP. That sentence needs no list of
    expansions, and its correctness does not depend on one. The residual is item 8: a
    safe-set-only literal outside the recognised vocabulary is still a leaf, and that is a
    vocabulary limit, not a command-position limit.
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
    checkout attributes from the committed tree. Round 7 adds `sec102_r7_fixtures/** -text` to
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
28. **Round-6 conservative false stops, superseded by the larger round-7 set in item 34.** Every
    command-position word carrying `*`, `?`, `[`, `]`, `{`, `}`, `~` or `\` now STOPs, whether
    or not Bash would actually expand that occurrence. Concretely: the `[` test builtin
    (`[ -f x ]`) STOPs, `\cat` STOPs, `~/bin/mytool` STOPs, and a subscript word without an
    `=` (`SEEN[0] "$ROOT/in.txt"`) STOPs - the last was a published round-5 control at `rc 0`.
    These are refusals, not detections, and the policy prefers a visible refusal to a proof
    that a particular occurrence was safe.
29. **Quoted occurrences are not excused.** `'*'` is a literal star to Bash but STOPs here. The
    fence reads the raw word, because deciding that quoting suppressed a specific expansion is
    the class of reasoning that produced R5-F1.
30. **SUPERSEDED IN ROUND 7, AND THE ROUND-6 CLAIM HERE WAS WRONG.** Round 6 stated that
    "`extglob`, `globstar` and similar option-enabled patterns are built from the same
    characters and are therefore covered by construction". **That sentence was false**, and the
    round-6 audit proved it: `+(`, `@(` and `!(` are built from characters the round-6 set did
    not contain. The residual it described - "the expansion character set is itself a list" -
    is exactly what round 7 removes, by inverting the test so there is no list of forbidden
    characters left to be incomplete. What replaces it is item 33.
31. **Three round-5 discriminators became non-discriminating in round 6.** `M1`, `M2` and `M3`
    no longer return their round-5 REDs to PASS, because the command-word fence catches those
    forms independently. Round 7 does not change this. The round-7 matrix runs all seven of its
    mutations against all four round-5 REDs and kills none of them, so the round-5 REDs are
    still guarded by the round-5 mechanisms and no round-7 claim rests on them.
32. **The safe set is a claim about the Bash grammar, and it is exactly as strong as one
    reading of it.** Six character classes are admitted with a stated argument each
    (`composite_pathproof.py:207-268`). No proof is offered that those arguments are correct.
    What the inversion changes is the FAILURE DIRECTION: an error in that reading now produces
    a false STOP instead of a false PASS. That is better, and it is not a proof.
33. **This is what replaces item 30.** There is no longer a list of forbidden characters that
    could be incomplete. There is a list of PERMITTED characters, and it can only be wrong by
    being too generous - a bounded, enumerable, six-entry claim an auditor can read in full -
    or too strict, which costs false stops and never a missed edge.
34. **The round-7 conservative false stops are larger than round 6's, and they are refusals,
    not detections.** New in round 7: any command word containing `+`, `@`, `%`, `=`, `,`, `^`,
    `#`, a quote character, or any non-ASCII character now STOPs. Concretely `g++`,
    `tool@1.0`, `--opt=value`, `"bash"`, `'source'`, `"if"`, `2a=b`, `a-b=c` and `cafe` with an
    accented `e` all STOP although Bash would run them harmlessly. Six of these were published
    round-6 classifications, and their movement is declared in advance in the round-7 grammar
    battery rather than discovered by an auditor.
35. **A non-NAME function definition is a new false stop.** `bin/foo() { ...; }` STOPs, because
    the scanner cannot distinguish it from an `extglob` pattern without deciding which shell
    options are set. Bash does accept some non-NAME function names; this refuses them.
36. **The word-boundary conservation covers `(` only.** A `)` abutting a word is still treated
    as a separator, because subshell and `case` syntax depend on that and no `extglob`
    construct begins at a `)`. This is an argument from the Bash grammar, not a sweep. It is
    also not load-bearing on its own: mutation `M3` turns the conservation off and kills no
    RED, because the safe set already refuses the fragments.

## Artifact identity record

The complete per-artifact byte-count and SHA-256 table is in `SEC102_R7_REPORT_2026-08-11.md`
section 6, and in `SELF_QA_SEC102_R7.md` section 10, both re-derivable by the published command.
No commit was made.
