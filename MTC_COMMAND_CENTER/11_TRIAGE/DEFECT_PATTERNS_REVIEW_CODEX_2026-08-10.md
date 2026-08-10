# AMEND: 7 changes

The ten-pattern set is still useful, but it is no longer complete and two boundaries have
blurred enough to cost review precision. Make seven changes:

1. merge Pattern 7 into Pattern 6 as the reader-completion subtype of the same
   status-before-semantics rule;
2. narrow Pattern 5 to grammar completeness inside a modeled input or argv contract;
3. narrow Pattern 9 to claim-to-predicate mismatch and treat it as an overlay, not the
   primary home of every false outcome;
4. narrow Pattern 10 to falsifiability and literal reproducibility of evidence;
5. add **The declared instrument is not the executed instrument**;
6. add **What the analyzer does not model must not disappear**; and
7. add **Every admitted member needs a terminal disposition**.

The two silent-omission candidates are therefore **two patterns**, not one. An analyzer
that has no model for a sink needs a coverage-completeness rule. A pipeline that enumerates
an object and then drops, overwrites or changes its identity needs a universe-conservation
rule. They have different falsifications and different repairs. Neither is the same as
Pattern 10: Pattern 10 asks whether evidence could turn red; these ask whether the subject
of the evidence reached adjudication at all.

## Distinctness review

- **Patterns 6 and 7 collapse in practice.** A nonzero `read` treated as EOF is the
  record-reader instance of interpreting output before proving producer completion. The
  same review question catches partial `find`, an early listener FAIL, an unterminated
  final record and a hard read error. Keep the Bash-specific cases as a subsection under
  Pattern 6; delete Pattern 7 as a separate top-level pattern.
- **Pattern 5 is too broad as written.** “If the input has structure, parse it whole” can
  be stretched to cover Patterns 6 and 7 and both new omission patterns. Restrict it to
  the correctness and totality of the grammar chosen for an input already recognized as
  belonging to that grammar: JSON keys, shell argv/options, diagnostics, records and
  tokenization. Registry coverage and cross-stage conservation belong elsewhere.
- **Pattern 9 currently matches almost everything.** Every defect can be restated as a
  sentence that outruns a probe. Keep it only where the defective surface is the emitted
  token, comment, report or contract sentence. If executable semantics are wrong, give the
  executable defect another primary home and cite Pattern 9 only as a cross-reference.
- **Patterns 9 and 10 remain distinct after that narrowing.** Pattern 9 asks whether a
  claim is entailed by the predicate. Pattern 10 asks whether the offered evidence could
  have failed and can be rerun literally. Today supplied independent hits for both.
- **Pattern 4 and the declared-but-unbound instrument are distinct.** Pattern 4 assumes a
  child is reached and asks what environment, interpreter and startup code influence it.
  The new pattern asks whether the real accepting caller reached the declared binding gate
  at all. `-I -S` can be correct and still protect nothing if an unbound program is the
  object interpreting those flags.
- **Pattern 1 and silent omission are distinct.** Pattern 1 classifies an encountered
  condition as PASS, FAIL or STOP. Silent omission prevents the condition or object from
  reaching any outcome branch, so a later PASS is manufactured by absence.

## Per-pattern hit evidence and reviewer question

### Pattern 1 - “STOP is not a result”

**Hit today.** `TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md` F3 drove a mixed
`No such file or directory; Permission denied` diagnostic and the close script emitted
`CLOSE_FAIL reason=evidence_dir_absent`, rc 1. The observation was ambiguous and therefore
not evaluable. The same report's F4 drove a real RO cleanup deviation after an unrelated
P0 close STOP and the global prerequisite flag demoted the completed rc-1 observation to
not-evaluable. `RP6_CODEX_AUDIT_R6_2026-08-10.md` A9 added two more direct instances: an
rc-0 multiline `stat` response became a wrong-kind FAIL, and an rc-0 empty `readlink -f`
response became a canonical-path FAIL, although neither producer result had valid shape.

**Concrete review question.** What exactly was observed before this branch selected PASS,
FAIL or STOP, and would the same output class keep that verdict if its diagnostic text,
record order or producer shape changed without changing host state?

### Pattern 2 - “Whose kernel answered?”

**Hit today.** `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` F6 reported lexical
`posixpath.normpath()` membership as unconditional host-path `ALLOW`, although no kernel
object, symlink chain or mount topology had been observed. The answer came from a lexical
model and was presented in the host-object domain. The RP6 and RP7 flagship reports also
show that this question remained load-bearing: their namespace checks passed only after
explicit caller/service/deploy-attested domain binding.

**Concrete review question.** Which exact host, user/mount/PID/network namespace and
privilege domain produced this value, and what evidence outside that domain binds it to
the domain named by the claim?

### Pattern 3 - “The leaf is not the path”

**Hit today.** The same pathscope F6 is a direct instance: `/safe/link/passwd` was called
`ALLOW` using lexical membership alone, with no proof that `link` was not a symlink and no
mount-chain proof. `SEC101_RECONCILIATION_CODEX_2026-08-10.md` independently required exact
ancestor and access-mode coverage and refused to widen the evidence-root rule merely
because a descendant string was lexical.

**Concrete review question.** For every accepted leaf, did this same block establish every
ancestor, symlink decision and relevant mount boundary at the time the leaf was used, or
did it verify only the final spelling?

### Pattern 4 - “The privileged child brought its own environment”

**Hit today.** `RP7_CODEX_T0_AUDIT_2026-08-10.md` F1 showed that `python -I` still imports
`site`; a `.pth` in the candidate venv executed before both adjudicators and wrote a marker.
`TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md` F1 independently showed bare remote `bash`
selected from PATH and absolute `/usr/bin/bash` influenced by inherited `BASH_ENV`; both
plants forged `SETUP PASS`. Its F2 showed inherited `TMPDIR=$EV_DIR` caused the close
script to create and hash its own temporary files inside the evidence tree while printing
`wrote_into_evidence_tree=0`.

**Concrete review question.** For every child process, which bytes choose the executable,
startup modules/files, environment, cwd and temporary directory, and can any subject under
test influence one of those before the intended predicate runs?

### Pattern 5 - “grep is not a parser”

**Hit today.** `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` F2-F4 and F7 found partial argv
grammars: ordinary `ssh`/`getent hosts` operands vanished, `find -exec` was not recursively
parsed, `--option=PATH` was discarded, and `<>` was tokenized as two unrelated operators.
`RP6_CLAUDE_REAUDIT_R5_2026-08-10.md` F2/F3 showed expansion before grammar validation:
`id -G` values such as `0*` and pin values such as `/usr/bin/sta*` changed meaning with cwd
contents. `RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` F2 showed that readable METADATA was not
the same as a parsed, nonempty and unique package identity.

**Concrete review question.** Once this input is assigned a grammar, does the parser
consume and validate every token, option, record and duplicate rule before semantics, and
does any unknown or ambiguous form STOP rather than fall through?

**Boundary amendment.** This pattern owns malformed or partially parsed data within a
recognized grammar. It does not own the absence of a command/sink adapter (new analyzer
coverage pattern) or a member dropped between two otherwise valid stages (new universe
conservation pattern).

### Pattern 6 - “Read the status before the stdout”

**Hit today.** `RP7_CODEX_T0_AUDIT_2026-08-10.md` F2 supplied the decisive fixture: the
same wildcard and malformed listener rows returned rc 1 or rc 3 solely from record order,
because semantic FAIL ran before the table reached clean EOF. `RP6_CODEX_AUDIT_R6_2026-08-10.md`
A9 likewise classified rc-0 producer values before establishing that the successful
output had a valid single-record shape.

**Concrete review question.** Before any value or mismatch is interpreted, have rc,
stderr, timeout, complete input consumption, final-record termination and output grammar
all been adjudicated; and can permuting records change only the evidence order, never the
verdict?

### Pattern 7 - “Nonzero read is not end of file”

**No new primary hit.** Today's listener defect is broader Pattern 6: the malformed record
was present and would have been seen, but an earlier semantic FAIL pre-empted it. The
current RP6/RP7 reports explicitly exercised unterminated and read-error cases and found
the repaired readers holding. After ten further rounds, no new defect required the
standalone Pattern 7 question.

**Concrete review question.** Merge into Pattern 6: what distinguishes clean EOF, a
populated final record, malformed termination and a hard read error, and is semantics
deferred until one of those states is proved?

### Pattern 8 - “The name is not the identity”

**Hit today, as a disclosed residual rather than a required verdict.**
`TRANSPORT_CLAUDE_FINAL_AUDIT_2026-08-10.md` N-d found that
`remote_close_tree_wpi.sh` still compares `%U:%G` with `gatea:gatea`, while setup had been
repaired to numeric `%u:%g`. The process contract deliberately kept that class-3 change
out of the close-script derivation, but the defect pattern correctly exposed the residual
on the evidence-binding operation.

**Concrete review question.** Is this comparison against the numeric/kernel identity the
claim names, or against a label supplied by NSS, PATH, a visible PID, a dictionary key or
another resolver whose identity is not bound?

### Pattern 9 - “The sentence outruns the probe”

**Hit today.** `RP6_CLAUDE_FINAL_AUDIT_2026-08-10.md` and the R5 re-audit falsified the
claim that deleting `-S` must produce a named STOP: a hostile `.pth` exited before the
child self-check, forged version `9.9`, wrote a marker and still produced rc 0. RP6 R6 A10
found further claim gaps: `pinned_timeout` without a mandatory timeout pin, unique
`deadline_exceeded` attribution for ambiguous rc 124, and site-startup nonexecution
claimed while interpreter behavior remained unattested. Pathscope F6 emitted
`closed_and_allowlisted` for lexical-only and incomplete coverage. Transport F2 printed
`wrote_into_evidence_tree=0` after writing there through `TMPDIR`.

**Concrete review question.** Underline every noun, adjective and mechanism token in the
claim; for each one, point to the predicate that establishes exactly that word and no
weaker substitute.

**Boundary amendment.** Use Pattern 9 as the primary home only when the code may be safe
for a narrower claim but the comment, log token, report or contract overstates it. For a
false executable outcome, use the relevant executable pattern first and cite Pattern 9 as
a cross-reference.

### Pattern 10 - “Evidence that cannot fail”

**Hit today.** `RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` F1 found a QA loop that redeclared a
ten-tool list and tested the helper directly, so it never exercised the real nine-tool
`wpi_main` caller; F3 found the published “Exact command” was literal
`bash <fence-file>`, which exits 2. `RP6_CODEX_AUDIT_R6_2026-08-10.md` A11 found unanchored
ranges that re-entered on Markdown prose, stale line ranges, and a current fence whose
descendant kept the command from terminating inside the audit bound. Pathscope F9 found
that the real-block 1/37 and 4/65 diagnostics had no literal setup, extraction, identity
or invocation commands. The hostile-`.pth` mutation also proved that a cooperating
mutation was not evidence for an adversarial startup claim.

**Concrete review question.** What minimal mutation should make this evidence fail, was
that RED actually observed, and can a fresh shell execute the recorded command literally
from declared inputs to reproduce the GREEN without edits, placeholders, line drift or
inherited state?

**Boundary amendment.** This pattern is about the proof artifact, not ordinary runtime
coverage. A runtime member silently skipped belongs to universe conservation even if the
QA also failed to notice it.

## Proposed merged pattern

## Pattern 6 - “No semantics before completion”

**The mistake.** A producer's values are interpreted before the producer's status,
diagnostics and complete input consumption have been adjudicated. Partial output, an early
record, a populated final record, a malformed terminator or a hard read error is therefore
read as a finished observation.

**Why it survives casual review.** stdout contains a plausible value and the loop or tool
appears to terminate normally. Shell idioms make EOF, error and partial completion look
alike, while an early semantic mismatch appears decisive enough to return immediately.
The missing predicate is temporal: every individual line may be parsed correctly, yet the
program has not proved it saw the whole input.

**Concrete instances.**

1. RP7 emitted `B6_FAIL reason=nonloopback_listener` when the wildcard row came first but
   `B6_STOP reason=listener_inventory_unreadable_or_unparseable` when the same later
   malformed row came first (`RP7_CODEX_T0_AUDIT_2026-08-10.md` F2).
2. RP6 sanitized an rc-0 multiline `stat` response and converted it to a wrong-kind FAIL,
   and compared an rc-0 empty `readlink -f` response as a canonical path, before proving
   output shape (`RP6_CODEX_AUDIT_R6_2026-08-10.md` A9).
3. Earlier fixtures remain canonical subtypes: partial `find` output before a traversal
   error, an unterminated final mount record skipped by `while read`, and a directory read
   error treated as clean zero-record EOF.

**The falsification.** Supply two tables with identical records in opposite order: one
semantic deviation and one malformed or unreadable later record. Both runs must STOP with
the same reason class. Then supply a final populated record without LF and a source that
raises a hard read error; neither may be treated as clean EOF. For scalar tools, return rc
0 with empty, multiline and non-printable output and require a reasoned STOP before any
comparison.

**The rule.** Make the producer transaction explicit: capture stdout, stderr, rc and
elapsed time; distinguish timeout, nonzero status, clean EOF, populated final record,
malformed termination and hard read failure; validate the complete output grammar; only
then apply semantic PASS/FAIL rules. During parsing, accumulate facts rather than return a
semantic verdict. A permutation of records may change neither evaluability nor outcome.

---

## Proposed new pattern - “The declared instrument is not the executed instrument”

**The mistake.** A tool, interpreter, helper or prerequisite is pinned, validated,
projected and documented, but the real accepting caller does not pass that object through
the binding gate. The claim is produced by an executable or function whose identity was
never established.

**Why it survives casual review.** Every component exists on the page: a pin parser, a
tool-binding function, a required-count check, an isolation flag and a QA loop. Reviewers
verify each component independently. The missing fact is reachability from the production
caller. A helper-level test can even prove the binder works while the real caller omits
one member.

**Concrete instances.**

1. RP7 accepted, projected and required `python3`, but `wpi_main` bound only nine tools;
   the unbound program forged `OK fields=8`, wrote a marker and reached `RP7 PASS`
   (`RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` F1).
2. RP6 printed `pinned_timeout` although its accepted one-entry pin set required only
   Python; the timeout object producing the bound was not required to be pinned
   (`RP6_CODEX_AUDIT_R6_2026-08-10.md` A10).
3. The transport plan pinned the local SSH client but invoked bare remote `bash`; a PATH
   plant or `BASH_ENV` startup file, outside the pinned program domain, forged the remote
   program marker (`TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md` F1).

**The falsification.** Replace exactly the declared instrument with a deviant executable
that writes a marker and emits the accepted terminal grammar. Drive the real top-level
caller, not the helper. If the marker appears or the accepting line is reached before the
binder rejects the object, the declaration is ornamental.

**The rule.** For every accepting claim, trace the dynamic call path backward to a binding
event for every executable, helper and function that can produce it. Derive the production
instrument inventory from the caller once; do not redeclare it in QA. Require an exact
one-to-one set comparison between declared, bound and executed instruments, and mutation-
test the real caller by removing or replacing each member.

---

## Proposed new pattern - “What the analyzer does not model must not disappear”

**The mistake.** A static analyzer, policy engine or dispatcher encounters a command,
option, redirection or nested program form outside its model and emits neither a resolved
fact nor an unresolved marker. Empty output is then read as proof that no sink or risk
exists.

**Why it survives casual review.** Modeled happy paths produce detailed, deterministic
rows, so the tool looks comprehensive. The registry of known commands and options is
mistaken for a proof that the language is covered. Shortcuts such as “no-path command” or
“ignore options” make common fixtures quiet, and determinism merely reproduces the same
omission.

**Concrete instances.**

1. `pushd "$ROOT"` and `trap 'cat /etc/passwd' EXIT` produced zero resolved paths, zero
   unresolved issues and `PATHSCOPE verdict=PASS rc=0`.
2. `ssh "$HOST"` and `getent hosts "$HOST"` silently lost their endpoints.
3. `find "$ROOT" -exec cat /etc/passwd \;` reported only the allowed root; curl upload,
   tar output and cp target paths supplied as `--name=value` likewise disappeared.
4. The unsupported `<>` token produced an invented target rather than a specific coverage
   refusal (`PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` F1-F4 and F7).

**The falsification.** For every registered command and shell construction, add one
unmodeled-but-valid path or endpoint form and one nested sink. Delete an adapter or insert
an unknown option. The tool must emit a specific unresolved coverage record and rc 3; zero
facts plus PASS is always red.

**The rule.** Coverage is a fail-closed property. Maintain an explicit grammar matrix for
commands, options, redirections, nesting and implicit endpoints. A recognized primitive
with any unconsumed token or unsupported semantic form must STOP with a coverage reason.
Unknown commands capable of executing or opening anything are opaque sinks, not no-op
commands. Report modeled coverage separately from resolved path counts, and never infer
absence of risk from absence of analyzer output.

---

## Proposed new pattern - “Every admitted member needs a terminal disposition”

**The mistake.** A stage declares or enumerates a universe, but a later stage silently
drops, overwrites, reinterprets or fails to bind one member. The reduced universe passes,
so absence from the result is mistaken for absence from the subject.

**Why it survives casual review.** Each stage is locally plausible: enumeration prints the
right count, preflight proves bytes readable, a library returns a convenient dictionary,
and comparison succeeds over what remains. Nobody checks conservation across stage
boundaries. Dictionary overwrite and library skip behavior are especially quiet because
they return valid data structures and rc 0.

**Concrete instances.**

1. RP7 preflight admitted two readable `*.dist-info` directories. The verifier silently
   skipped the one whose METADATA lacked `Name`, compared one package and emitted parity
   PASS (`RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` F2).
2. The same verifier overwrote duplicate canonical package names in a dictionary, so two
   admitted objects could become one compared identity.
3. RP6 validated pathname-expanded `id -G` items but reconciled the raw string against the
   forbidden-GID ledger. A raw `0*` could be rendered `form=numeric_only` from the expanded
   item while the forbidden numeric identity disappeared from the later whole-word
   intersection (`RP6_CLAUDE_REAUDIT_R5_2026-08-10.md` F2).

**The falsification.** Add one malformed-but-readable member, two members that canonicalize
to the same key, and one member whose representation changes between validation and
comparison. The terminal accounting must show one disposition per input member and must
STOP on missing identity, duplicate identity, representation drift or an unexplained count
change. A final PASS over fewer members is red.

**The rule.** Declare the universe once, assign every member a stable identity, and carry
that identity unchanged through preflight, parse, normalization and comparison. Enforce a
conservation equation at every boundary: input members equal accepted plus rejected plus
explicitly unresolved members, with no overwrite and no implicit filter. PASS requires
every admitted member to reach exactly one terminal disposition.

## Recommended deletions

Delete only standalone **Pattern 7** after its concrete instances and falsifications are
moved under the merged Pattern 6. It had no new primary hit in today's evidence, and its
review question is already required to answer Pattern 6 correctly.

Do **not** delete Patterns 2, 3 or 8 merely because today's required findings were sparse.
Pattern 2's domain question and Pattern 3's path-chain question both caught the pathscope
overclaim, while Pattern 8 exposed a still-carried name-based identity residual in the
transport set. Do not delete Pattern 9 either; narrow it to a claim-audit overlay. That
preserves its strong RP6 `-S` falsification without allowing it to become the universal
label for every defect.
