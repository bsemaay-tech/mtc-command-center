# RP6-P0 — status: ROUND-12-REPAIRED-PENDING-T0-REAUDIT (two R11 findings closed, executed; no block byte changed)

Updated 2026-08-11 by the round-12 implementer (Claude Max, `claude-opus-5`,
xhigh, fresh session). Audit tier unchanged: **T0** (host/execution-domain
preflight). Codex `gpt-5.6-sol` is this block's auditor of record; the T0
re-audit of these bytes is pending. The block remains a draft: not frozen, not
accepted, not dispatchable, and not authorised for host execution.

Full disposition: `RP6_R12_REPORT_2026-08-11.md`. Evidence: `SELF_QA_RP6.md`
§ROUND 12.

**`RP6-P0.sh` is UNCHANGED this round — not one byte.** Both round-11 findings
are QA-layer: the census the audit falsified is a harness in `SELF_QA_RP6.md`,
and the stale overclaim is a comment inside another harness in the same file.
The mutated bytes the audit certified were a temporary copy; the defect was that
the fence could not see a valid emitter syntax, not that the block contains one.
The block's identity is re-derived below and is byte-identical to the audited
subject `5132bacd…`.

**The two round-11 findings, both UPHELD and both closed:**

- **F1** (HIGH) — the "broader independent" census was still a line-oriented
  grep for the CONTIGUOUS text `p0_stop`/`p0_fail` or the contiguous result
  literal, so a command word assembled from adjacent quoted and unquoted
  segments (`p0_s""top`) was valid, reachable, emitted `P0_STOP` at rc 3 — and
  vanished from the census, which reported `unmodeled=0` while the fence
  returned rc 0 on the mutated bytes. **Repaired by replacing the mechanism, not
  by widening the pattern.** `R12_GRAMMAR` supersedes `R11_GRAMMAR`, carries all
  eight round-11 assertions and all seven round-11 mutants forward unchanged, and
  puts a **tokenizer** in front of the grep: it tracks quote state, resolves
  backslash escapes, joins line continuations, collapses expansions, recurses
  into every `$( )` and into the `trap` action, locates command POSITIONS, and
  applies a fail-closed source-style policy that admits a command word only as
  BARE, a single complete QUOTED_LITERAL, or a whole-word PURE_EXPANSION drawn
  from a declared six-handle RO-tool set. Every other command-word syntax, and
  every construct it does not model, makes the fence FAIL. Four new assertions
  carry it, including one that requires the tokenizer's emitter line set to equal
  the grep census's line set **line for line**. `R12_F1_RED` runs the whole
  published round-11 fence and the whole published round-12 fence over the same
  mutated bytes and records RED (round 11 returns rc 0 and certifies them) versus
  GREEN (round 12 returns nonzero), for three command-word-fragmentation forms
  each proven to be valid shell and to really emit at rc 3.
- **F2** (MEDIUM) — the live `R10_F4` harness comment still said "Every input
  class that leaves the binding unset is shown" and then listed three. Pattern 9,
  in the exact defect class round 11 was closing. **Repaired in place, comment
  only**: it now says "unreachable for the three input classes this fence
  executes" and keeps the explicit list. No harness widening; `R10_F4` still
  returns `cases=16 pass=16 fail=0 result=PASS`. The repair is six lines
  replacing six lines, so every `guard_at_line` recorded by `R11_GUARDS` stays
  valid.

**Round-11 wording corrected, not just superseded.** The audit named
`STATUS_RP6_P0.md:20-21` and `RP6_R11_REPORT_2026-08-11.md:86-90` as overstating
the property as fail-closed. The status sentence is corrected in place in the
round-11 section below. The round-11 report is a delivered record of what that
round claimed and is not in this round's scope fence, so it is corrected in
`RP6_R12_REPORT_2026-08-11.md` rather than rewritten — the same treatment round
11 gave the round-10 report.

**What the census property now is, exactly:** every command word in the block is
BARE, a single complete QUOTED_LITERAL, or a whole-word PURE_EXPANSION drawn from
the declared RO-tool handle set. For the first two the name is contiguous in the
source, so the emitter census is complete over them; for the third the name is a
**runtime value the fence does not and cannot evaluate**, which is why the set of
invocable variables is pinned instead of the value. Any other command-word
syntax, and any construct the tokenizer does not model, makes the fence FAIL
rather than pass silently. It does **not** make the derivation understand new
syntax, and `R12_F1_RED`'s last case asserts that the round-12 parser alone is
exactly as blind as round 11's.

**Artefact identity — all executed in the round-12 session:**

```text
sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330   (UNCHANGED)
bytes=110817                                                              (UNCHANGED)
bash_n=0                      (GNU bash 5.2.37(1)-release, x86_64-pc-msys; GNU Awk 5.3.2)
cr_bytes=0                    (RP6-P0.sh, SELF_QA_RP6.md, STATUS_RP6_P0.md, the prereg draft)
line_endings=LF_only
emit_sites=163                (162 p0_stop/p0_fail wrapper sites + 1 direct ERR-trap printf)
line_census=163               (round-11 contiguous-text rule; unmodeled=0)
token_census=163              (round-12 command-position rule; unmodeled=0, 20 scanned fragments)
census_line_sets=IDENTICAL    (asserted by cmp, not by comparing totals)
runtime_cmdwords=16 sites / 6 distinct, all in the declared RO-tool handle set
declared_tuples=149           (prereg §8.1.1, UNCHANGED; closed against the block by R12_GRAMMAR)
decl_block_sha256=31f8315c5028f5ee3a7ada2a2690000e7b490685c6fe0e9c6117ab33b6da59e5   (markers included, as round 11 quoted it — identical)
freeze_gate_literal_count=17  (unchanged; 12 tool pins + 5 attestation values, all <PIN-AT-FREEZE>)
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667…9aa01aad bytes=70941
```

**QA execution status: EXECUTED — nothing PENDING, nothing fabricated.** All
twenty-four published commands of the round-12 mandated set were run verbatim in
this session in a local Git Bash `--noprofile --norc` process, against the final
bytes.

```text
24 published commands             -> 23 at rc 0, R11_R9RED at rc 1 (its PASS condition)
R12_GRAMMAR_SUMMARY  cases=23 pass=23 fail=0 result=PASS
R12_F1_RED_SUMMARY   cases=33 pass=33 fail=0 result=PASS
R11_GUARDS_SUMMARY   fences=17 pass=17 fail=0 result=PASS   (15 -> 17: the two round-12 fences added)
R10_F4_QA_SUMMARY    cases=16 pass=16 fail=0 result=PASS    (F2 is comment-only)
R11_F1_RED / R11_F3 / R10_F3 / R9_GRAMMAR and every legacy fence -> carried unchanged, all PASS
R11_GRAMMAR (SUPERSEDED)          -> rc 0, still passes; insufficient, not broken. Out of the mandated set
R10_GRAMMAR (SUPERSEDED in R11)   -> rc 1, re-run and recorded, not hidden
```

**Residuals carried into the re-audit, named not closed:**

1. `R12_GRAMMAR` is a *static source* fence. Its tokenizer models the shell
   dialect this block is written in and fails closed on what it does not model.
   That is a refusal to certify, not a proof of equivalence to bash's own parser.
   `shellcheck` is not installed here and was not run.
2. Assertion 12 pins **which** variables may be invoked as command words. It
   cannot establish **what** they hold at run time — the same runtime/static
   boundary residual round 11 carried, now made executable rather than narrated.
3. The `%F` token set pinned by the round-11 F2 repair is GNU coreutils' complete
   `file_type()` return set. On a non-GNU producer an out-of-set token STOPs at
   rc 3 instead of being reported as host deviation — the intended fail-closed
   direction, but not a claim that this block can classify another producer's
   vocabulary.
4. `P0_STATE_UID` / `P0_STATE_GID` / `P0_EXPECT_UID` input integrity. The block
   constrains these to positive decimals and cannot establish that the prelude
   carried the preregistered numerics; §2 preregisters no numeric for
   `P0_EXPECT_UID` at all. Freeze-gate/owner band.
5. `R10_F4`'s reachability result covers the **three** input classes it executes
   on *this* control flow — the wording F2 corrected — not every early-stop class
   and not every future edit, which is why the assertion is kept rather than
   deleted.
6. `RP6_R10_REPORT_2026-08-11.md:362-369` and `RP6_R11_REPORT_2026-08-11.md:86-90`
   carry the superseded "every input class" and "fail-closed" wordings. Both are
   corrected in `RP6_R12_REPORT_2026-08-11.md` rather than rewritten: a delivered
   audit-round report records what that round claimed, and the kickoff scope fence
   does not list either as writable.

The freeze gate still has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

## Prior status — round 11 (four R9/R10 findings closed; superseded by round 12)

Updated 2026-08-11 by the round-11 implementer (Claude Max, `claude-opus-5`,
xhigh, fresh session). Audit tier unchanged: **T0** (host/execution-domain
preflight). Codex `gpt-5.6-sol` is this block's auditor of record; the T0
re-audit of these bytes is pending. The block remains a draft: not frozen, not
accepted, not dispatchable, and not authorised for host execution.

Full disposition: `RP6_R11_REPORT_2026-08-11.md`. Evidence: `SELF_QA_RP6.md`
§ROUND 11.

**The four round-10 findings, all UPHELD and all closed:**

- **F1** (HIGH) — the grammar fence was fail-OPEN twice over. Coverage was
  measured with the same lexical restriction it was meant to check, so an
  executable emitter in another valid quoting form vanished from both counts;
  and per-field value unions destroyed each site's field correlation, so a
  semantic relabel of one site was invisible. **Repaired:** the declaration is
  now one line per **correlated site tuple** (149 tuples / 163 sites in prereg
  §8.1.1), and coverage is censused by a broader independent rule.
  **Corrected in round 12 (Codex round-11 audit, finding 1):** this bullet used
  to end "…that FAILS CLOSED on any emitter syntax the parser cannot read". That
  overstated it. The round-11 census failed closed only on a syntax the parser
  cannot read *that a contiguous text search still finds*; a command word
  assembled from adjacent quoted and unquoted segments (`p0_s""top`) was valid,
  reachable, emitted `P0_STOP`, and disappeared from the census entirely. The
  fail-closed property is real only from round 12, where a tokenizer decides it
  over command POSITIONS — see the round-12 section at the top of this file.
  `R11_GRAMMAR` carries all
  ten round-10 assertions and all five round-10 mutants forward unchanged and
  adds four assertions and the two mutants the audit named. `R11_F1_RED` executes
  the **round-10** mechanism on the same mutants and records that it is invariant
  under both — the RED half D026 requires.
- **F2** (HIGH) — an unrecognised printable `%F` token became a host-state FAIL at
  rc 1. **Repaired at both classification sites** (followed target and leaf): the
  complete GNU coreutils `file_type()` token set is pinned; a recognised
  non-regular kind still FAILs at rc 1, an unrecognised token STOPs at rc 3 under
  `link_target_kind_unrecognized` / `path_probe_kind_unrecognized`. `R11_F3`: 85
  cases, RED reproduces the audit's exact rc-1 line at both sites.
- **F3** (HIGH) — the published R9 RED recipe returned rc 0 because cleanup ran
  last, and the ten own-status guards were prose plus a transcript. **Repaired:**
  `R11_R9RED` cleans up in an EXIT trap and exits WITH the RED harness's status
  (**its PASS condition is rc 1**); `R11_GUARDS` is an executable, self-checking
  falsification fence over **fifteen** fences, replacing the transcript.
- **F4** (MEDIUM) — the F4 evidence prose outran the executed predicate. **Every
  claim narrowed, none extended**, claim by claim in `SELF_QA_RP6.md` §F4. The
  block comment now says the mutant neutralises **two** gates (not three) and
  that the harness runs **three** input classes (not "every input class that
  leaves the binding unset"). The pin parser's other early-stop classes —
  malformed entry, unknown tool, duplicate, non-absolute, whitespace, glob
  metacharacter, non-python frozen path — are named as NOT executed.

**Artefact identity — all executed in the round-11 session:**

```text
sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
bytes=110817
bash_n=0                      (GNU bash 5.2.37(1)-release, x86_64-pc-msys)
cr_bytes=0                    (tr -cd '\r' < RP6-P0.sh | wc -c)
line_endings=LF_only
emit_sites=163                (162 p0_stop/p0_fail wrapper sites + 1 direct ERR-trap printf)
broad_census=163              (round-11 rule, independent of quoting; unmodeled=0)
declared_tuples=149           (prereg §8.1.1, closed against the block by R11_GRAMMAR)
decl_block_sha256=31f8315c5028f5ee3a7ada2a2690000e7b490685c6fe0e9c6117ab33b6da59e5
entry_sha256=a090ae73…4fad0617 / 107252 B (round 10, commit 71a62cc8, matches the kickoff)
freeze_gate_literal_count=17  (unchanged; 12 tool pins + 5 attestation values, all <PIN-AT-FREEZE>)
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667…9aa01aad bytes=70941
```

**QA execution status: EXECUTED — nothing PENDING, nothing fabricated.** All
twenty-three published commands of the round-11 mandated set were run verbatim in
this session in a local Git Bash `--noprofile --norc` process. Every round-11
transcript in `SELF_QA_RP6.md` was re-run against the final bytes and reproduces
byte-for-byte.

```text
23 published commands             -> 22 at rc 0, R11_R9RED at rc 1 (its PASS condition)
R11_GRAMMAR_SUMMARY  cases=15 pass=15 fail=0 result=PASS
R11_F1_RED_SUMMARY   cases=17 pass=17 fail=0 result=PASS
R11_F3_QA_SUMMARY    cases=85 pass=85 fail=0 result=PASS
R11_GUARDS_SUMMARY   fences=15 pass=15 fail=0 result=PASS
R11_R9RED            R9_GRAMMAR cases=5 pass=2 fail=3 result=FAIL -> recipe exit=1
R10_F3 / R10_F4 / R9_GRAMMAR      -> carried unchanged, all PASS on the round-11 bytes
R10_GRAMMAR (SUPERSEDED)          -> rc 1, recorded not hidden; out of the mandated set
```

**Residuals carried into the re-audit, named not closed:**

1. `R11_GRAMMAR` is a *static source* grammar. The census makes coverage fail
   closed over emitter **syntax**; it still cannot constrain what a `<name>`
   class evaluates to at run time. **Corrected in round 12:** the first half of
   that sentence was false as written — see the F1 bullet above and the round-12
   section at the top of this file. The second half stands and is still a
   residual.
2. The `%F` token set pinned by F2 is GNU coreutils' complete `file_type()`
   return set. On a non-GNU producer an out-of-set token now STOPs at rc 3
   instead of being reported as host deviation — the intended fail-closed
   direction, but not a claim that this block can classify another producer's
   vocabulary.
3. `P0_STATE_UID` / `P0_STATE_GID` / `P0_EXPECT_UID` input integrity. The block
   constrains these to positive decimals and cannot establish that the prelude
   carried the preregistered numerics; §2 preregisters no numeric for
   `P0_EXPECT_UID` at all. Freeze-gate/owner band.
4. `R10_F4`'s reachability result covers the **three** input classes it executes
   on *this* control flow — not every early-stop class and not every future edit,
   which is why the assertion is kept rather than deleted.
5. `RP6_R10_REPORT_2026-08-11.md:362-369` carries the same "every input class"
   overclaim. It is corrected in `RP6_R11_REPORT_2026-08-11.md` rather than
   rewritten: a delivered audit-round report records what that round claimed, and
   the kickoff scope fence does not list it as writable.

The freeze gate still has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

## Prior status — round 10 (four R9 findings closed; superseded by round 11)

Block bytes at that round: `a090ae73…4fad0617`, 107252 B, commit `71a62cc8`.
Prereg §8.1.1 then declared 89 forms / 161 emit sites. Full disposition:
`RP6_R10_REPORT_2026-08-11.md`; evidence in `SELF_QA_RP6.md` rounds 10 and 10B.

**Round 10 ran in two sittings.** Round 10a (Claude Pro) wrote the repairs and
died on its weekly cap before recording any output, leaving twelve `@…@`
placeholders, no report and no status update — preserved as commit `da78d99c`,
explicitly not round 10. Round 10b (Claude Max, this sitting) confirmed each
repair by execution, filled all twelve placeholders with real captured output,
wrote the report and this file. **No `RP6-P0.sh` byte was changed in 10b**: F1–F4
are closed on the 10a bytes.

**The four round-9 findings, all UPHELD and all closed:**

- **F1** (HIGH) — the published `R9_GRAMMAR` command did not run the harness. Fixed
  with `-s --`; the mandated sweep then found six more published commands with an
  unanchored `sed` range and ten fences that printed `result=FAIL` while exiting 0.
  All repaired. All 19 published commands plus the RED twin now run **verbatim and
  as an extracted body with identical rc and identical summary line**, and all ten
  own-status guards were **falsified** (fail counter forced nonzero → rc 1), not
  merely grepped.
- **F2** (HIGH) — declared and executable grammar not closed. Preregistration
  §8.1.1 now declares the complete P0 result grammar (**89 forms, 161 emit sites**);
  the new `R10_GRAMMAR` fence re-derives it from the block bytes and diffs both
  directions, with five mutants that each kill it.
- **F3** (HIGH) — a malformed followed-target `%F` response reached rc 1.
  `p0_probe_kind` now adjudicates the raw response for empty / multi-line /
  non-printable shape **before** `P0_FKIND` is assigned. `R10_F3`: GREEN rc 3 on the
  real bytes, RED reproduces the audit's exact rc-1 line.
- **F4** (MEDIUM) — the round-9b relabelling was convenient, not established. The
  round-9 claim is **withdrawn**. The line now carries `internal_invariant_unmet`,
  naming the predicate it actually tests; `R10_F4` proves unreachability on the
  unmutated bytes and reaches the line on a mutant whose two consuming gates are
  neutralised.

**Artefact identity — all executed in the round-10b session:**

```text
sha256=a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617
bytes=107252
bash_n=0                      (GNU bash 5.2.37(1)-release, x86_64-pc-msys)
cr_bytes=0                    (tr -cd '\r' < RP6-P0.sh | wc -c)
line_endings=LF_only
emit_sites=161                (160 p0_stop/p0_fail wrapper sites + 1 direct ERR-trap printf)
declared_forms=89             (prereg §8.1.1, closed against the block by R10_GRAMMAR)
entry_sha256=08e0a935…adbcf10c / 104683 B (round 9, commit 9bc25721)
freeze_gate_literal_count=17  (unchanged; 12 tool pins + 5 attestation values, all <PIN-AT-FREEZE>)
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667…9aa01aad bytes=70941
```

**QA execution status: EXECUTED — nothing PENDING, nothing fabricated.** Every
published command was run in this session in a local Git Bash `--noprofile --norc`
process, in both the verbatim and the extracted form, with `BASH_ENV`/`ENV`
confirmed unset. The per-command evidence is in `SELF_QA_RP6.md` §1e; the
guard-falsification transcript and the round-9 reproductions are in §ROUND 10B.

```text
19 published commands + RED twin   -> all forms agree on rc and summary line
R10_GRAMMAR_SUMMARY cases=10 pass=10 fail=0 result=PASS
R10_F3_QA_SUMMARY   cases=14 pass=14 fail=0 result=PASS
R10_F4_QA_SUMMARY   cases=16 pass=16 fail=0 result=PASS
R9_GRAMMAR_SUMMARY  cases=5  pass=5  fail=0 result=PASS   (GREEN)
R9_GRAMMAR_SUMMARY  cases=5  pass=2  fail=3 result=FAIL   (RED twin, rc 1)
```

**Residuals carried into the re-audit, named not closed:**

1. `R10_GRAMMAR` is a *static source* grammar. It constrains prefixes, reasons,
   field names, field order and every literal value and `detail=` token; it cannot
   constrain what a `<name>` class evaluates to at run time.
2. `P0_STATE_UID` / `P0_STATE_GID` / `P0_EXPECT_UID` input integrity. The block
   constrains these to positive decimals and cannot establish that the prelude
   carried the preregistered numerics; §2 preregisters no numeric for
   `P0_EXPECT_UID` at all. Freeze-gate/owner band.
3. `R10_F4`'s reachability result is about *this* control flow, not about every
   future edit — which is why the assertion is kept rather than deleted.
4. The round-9 report's "174 call sites" figure is withdrawn; the entry-state
   figure is 159 (the auditor's count, confirmed), and the round-10 figure is 161.

The freeze gate still has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

## Prior status — round 9 (grammar-drift close, superseded by round 10)


Updated 2026-08-11 by the round-9 implementer (Claude, fresh session). Audit tier
unchanged: **T0** (host/execution-domain preflight). Codex is this block's
auditor of record; the T0 re-audit of these bytes is pending. The block remains a
draft: not frozen, accepted, dispatchable, or authorised for host execution.
Full disposition + sweep table: `RP6_REPAIR_R9_REPORT.md`; R9 harness in
`SELF_QA_RP6.md` §R9.

**Round 9 closed the grammar drift at the second emit site.** The post-loop
python3-binding backstop (`:668`) previously emitted an undeclared second shape
of `input_pin_freeze_unfilled` (`detail=
trusted_python_pin_omitted_freeze_gate_load_bearing`) — a round-5 relic left
undeclared because round 7's correction-7 omission loop (`:632-637`) made that
gate unreachable. The backstop now emits the **declared** `input_pin_omitted
tool=python3 detail=every_preregistered_tool_requires_one_frozen_pin` token
(matching the omission loop verbatim). `input_pin_freeze_unfilled` now has
exactly one declared shape, at one live site (`:616`, fixed in 9a). The preceding
F1 comment was rewritten to match. No control-flow/variable/structural change;
**no draft byte touched** (the draft already declares `input_pin_omitted`). The
closure is NOT "declare a second form" (the condition is already declared, and
the site is unreachable so a second form could not be RED/GREEN-proven) and NOT
"emit the :616 line" (the deploy-channel value is filled when the backstop is
reached, so that would be a lie). See the report for the full adjudication.

**Round 9a (commit `ab53a012`, already applied)** closed the generic in-loop
site (`:616` emits `name=$P0_FROZEN_CONST_NAME`); the `RP6_R4_D026`
`PIN_FREEZE_EXACT` assert then matched the preregistered line character for
character and all eight fences went green for the first time on `e7ca9ff1…`
(103808 B). 9a left the second site, the sweep, and the report/QA/status layer
open; 9b closes all three.

**Emit-site sweep:** every `p0_stop`/`p0_fail` site (174, lines `:399`-`:1753`)
cross-checked against `WPI_PREREGISTRATION_DRAFT.md` §8.1 rows 1-9. Exactly one
deviation found — the post-loop backstop — fixed this round. No other site emits
an undeclared reason or `detail=`, and no site where the draft looks wrong.

**Artefact identity (round-9 bytes; bash -n / harness re-run PENDING Lead execution;
CR bytes verified 0 in-session):**

```text
sha256=08e0a93562bb04f4f78bac77d973a26da5b609aa305491d3bfa51743adbcf10c
bytes=104683
bash_n=PENDING-LEAD-EXECUTION   (session gates bash; change is comment + one string literal at an unreachable site)
cr_bytes=0 (verified: tr -cd '\r' < RP6-P0.sh | wc -c)
line_endings=LF_only
relic_residual=0 (grep -c trusted_python_pin_omitted_freeze_gate_load_bearing RP6-P0.sh)
pre_9b_sha256=e7ca9ff1e6d44b838b6d8bfddbb24bb68e2642b9f65abfc941f9482e465a0839 (9a commit ab53a012, 103808 B)
freeze_gate_literal_count=17 (unchanged)
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

**QA execution is PENDING-LEAD-EXECUTION.** This session gates `bash` (every
`bash -n`/`sed … | bash` returned *requires approval* — the same blocker rounds
5-8 recorded), so the round-9 run is recorded PENDING, not fabricated (kickoff
PENDING clause + AGENTS.md D026). The Lead must, in an unhindered Git Bash
against `08e0a935…` / 104683 B:

```text
bash -n RP6-P0.sh                                                          -> expect rc 0
sed -n '/R9_GRAMMAR_HARNESS_BEGIN/,/R9_GRAMMAR_HARNESS_END/p' SELF_QA_RP6.md | bash --noprofile --norc
  -> expect R9_GRAMMAR_SUMMARY cases=5 pass=5 fail=0 result=PASS   (GREEN)
# D026 RED twin: restore the relic at the post-loop gate in a temp copy, re-run the harness with $1=that copy
  -> expect result=FAIL   (RED)
# the eight 9a fences by anchored marker, all rc 0 (unchanged by this edit):
#   RP6_R4_D026 / RP6_FULLBLOCK_D026 / R7_F2 / R7_F3 / R7_C3 / C13_R3_BACKSTOP / F2_FREEZE_GATE / C13_R4B
```

Expected: `bash -n` rc 0; `R9_GRAMMAR_SUMMARY … result=PASS`; the eight fences at
their recorded green summaries. Until the Lead runs these, the round-9 evidence
is supplemental.

The freeze gate still has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

## Prior status — round 8 (evidence-only, superseded by round 9)

Updated 2026-08-11 by the round-8 implementer (Claude, fresh session). Round 8 is
an **evidence-only** round: it repairs the two legacy fences that failed the Lead's
round-7 QA execution (`RP6_R7_LEAD_QA_EXECUTION_2026-08-10.md`) and writes no
block byte. Audit tier unchanged: **T0** (host/execution-domain preflight). The
block remains a draft: not frozen, accepted, dispatchable, or authorised for host
execution. Full disposition: `RP6_REPAIR_R8_REPORT.md`; harnesses + R8 section in
`SELF_QA_RP6.md`.

**`RP6-P0.sh` is UNCHANGED this round** — SHA-256
`fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`, 103071 B, 0 CR
bytes (re-derived this session by read-only tools; byte-identical to the round-7
commit `d9d7420f`). `bash -n` was not re-run (this session gates `bash`), but no
block byte was touched, so the round-7 `bash -n` rc 0 stands. If the block itself
were believed to need a change, this round would stop and report rather than
change it; it does not.

**Round-7 Lead QA result (the input to this round).** The Lead ran every fence by
anchored marker after round 7: the three R7 harnesses (4/4, 4/4, 8/8) and three
legacy fences (`C13_R3_BACKSTOP`, `F2_FREEZE_GATE`, `C13_R4B`) PASS. Two legacy
fences FAIL (rc 1) — `RP6_FULLBLOCK_D026` (7 s, no summary) and `RP6_R4_D026`
(41 s, `findings=4`) — both from `P0_FIXED_STAT: unbound variable` in their
landmark-sliced test arms: correction 7's frozen `P0_FIXED_*` literals
(`RP6-P0.sh:266-299`) fall outside the slices, and the extracted pin loop
references them under `set -u`.

**Round-8 repairs (`SELF_QA_RP6.md` only).**

- **Repair 1 — arm construction that survives block growth.** `build_f4_arm`
  (FULLBLOCK) and `build_pin_arm` (R4) now define every `P0_FIXED_*` literal their
  slices reference (the pin arm also mirrors the block's `P0_TOOL_COUNT_EXPECTED`
  derivation, another correction-7 value the slice reads), and each carries a
  build-time assertion that every `P0_FIXED_*` the slice references is defined —
  so a future round that adds a new frozen literal fails the build LOUDLY instead
  of emitting a silently-broken arm. Not a hand-widened slice.
- **F7_TOOL_POST — classified: block correct, fence fixture stale (fixed).**
  Correction 7 deleted the unpinned `command -v` fallback, so the F7 tool arm's
  empty `P0_TOOL_PINS` now STOPs at `tool_pin_unpinned` before the `[ -x ]` check
  that emits the R2-F1 `tool_not_evaluable … rc=na` token. Prereg §8.1 row 1 still
  carries `tool_not_evaluable tool=getent path=<p> rc=<n|na> detail=<d>
  mechanism=<m>` and its round-7 amendment defines `tool_pin_unpinned` for the
  unpinned case — so the block is right and the fixture is stale. The arm now pins
  `getent` to the fixture path; the PRE arm is unaffected (the pre-repair resolver
  kept the fallback).
- **R4 GREEN count — stale under correction 7 (fixed).** `$RP7PINS` supplied ten
  pins and asserted `count=10`; correction 7 requires twelve (row 1: `input_pin_omitted`,
  `input_pin_count_unexpected … expected=12`). `$RP7PINS` now carries all twelve
  (`id`/`getent` appended) and the GREEN assertion reads `count=12`. Block correct,
  fence stale.

**QA execution is PENDING-LEAD-EXECUTION.** This session gates the `bash`
interpreter (every `bash <script>`, `bash -n`, `bash -c`, `sed … | bash` returned
*requires approval* — same blocker the round-7 Claude and GLM sessions recorded),
so the round-8 re-run of the two repaired fences is recorded PENDING, not
fabricated (per the kickoff clause and AGENTS.md D026). Expected: both rc 0 / PASS.
Until the Lead re-runs them, the round-8 evidence is supplemental.

The freeze gate still has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

## Round-7 block change (superseded — rounds 9, 10 and 11 changed block bytes)

Updated 2026-08-10 by the round-7 implementer (Claude, fresh session) for the
five Codex round-6 audit required corrections (`RP6_CODEX_AUDIT_R6_2026-08-10.md`,
REQUEST_CHANGES, rows A4/A8/A9/A10/A11). Audit tier: **T0** (host/execution-domain
preflight). Codex is this block's auditor of record for these corrections, so
implementer/auditor separation holds. Round 7 is authorised by owner grant #7
(2026-08-10), which lifts the T0 round cap for this block set — rounds continue
until both flagships accept; the acceptance standard is unchanged. The block
remains a draft: not frozen, accepted, dispatchable, or authorised for host
execution.

**QA execution is PENDING-LEAD-EXECUTION.** This Claude session's Bash tool gates
`bash -n`, script execution, `sha256sum` and `wc` (every `bash -n`/`bash -c`/
heredoc and the artefact hash/byte tools returned *requires approval*). Per the
kickoff's PENDING-LEAD-EXECUTION clause and AGENTS.md D026, the evidence is
recorded as PENDING rather than fabricated. The Lead must, in an unhindered Git
Bash against the round-7 bytes:

```text
tr -cd '\r' < RP6-P0.sh | wc -c                                       -> 0 (DONE in-session)
sha256sum < RP6-P0.sh                                                 -> fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd (DONE)
wc -c < RP6-P0.sh                                                     -> 103071 (DONE)
bash -n RP6-P0.sh                                                     -> PENDING (session gates bash)
sed -n '/^# R7_F2_HARNESS_BEGIN$/,/^# R7_F2_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '/^# R7_F3_HARNESS_BEGIN$/,/^# R7_F3_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '/^# R7_C3_HARNESS_BEGIN$/,/^# R7_C3_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
the five marker-migrated legacy fences (C13_R3_BACKSTOP / RP6_FULLBLOCK_D026 /
  F2_FREEZE_GATE / RP6_R4_D026 / C13_R4B) by anchored marker, all rc 0
```

Expected: `R7_F2_QA_SUMMARY cases=4 … PASS`, `R7_F3_QA_SUMMARY cases=4 … PASS`,
`R7_C3_QA_SUMMARY cases=4 … PASS`, and the five legacy fences at their recorded
PASS summaries. Until these run, the round-7 evidence is supplemental (A11).

Round-7 disposition (Codex round-6 audit A4/A8/A9/A10/A11 + correction 7) — full
record in `RP6_REPAIR_R7_REPORT.md`; harnesses + marker migration in
`SELF_QA_RP6.md` §R7:

- **C1 / A4 (R5-F2) — REPAIRED.** `type -t` → `builtin type -t` (matches
  RP7-WPI-RO.sh:646-647), defeating a caller-defined `type(){…}`. Comment and
  `P0_prereq` narrowed to "required functions present and exercised", not RP0-LIB
  provenance. D026 harness `R7_F2` (PENDING).
- **C2 / A8 (R6-F3) — REPAIRED.** Outer pin parse wrapped in a caller-noglob
  save/restore, so a crafted cwd holding `stat=/usr/bin/stat` can no longer
  rewrite `stat=/usr/bin/sta*` before the charset gate. D026 harness `R7_F3`
  (PENDING) adds the exact whole-token crafted-cwd case.
- **C3 / A9 — REPAIRED.** `p0_probe_kind` and `p0_assert_venv_root` adjudicate
  rc-0 producer SHAPE (empty/multiline/non-printable/non-absolute) as rc 3 STOP
  before any rc-1 object verdict. D026 harness `R7_C3` (PENDING), both arms.
- **C4 / A10 — REPAIRED.** rc 124 relabelled
  `manager_query_rc124_timeout_reached_or_child_exit_124` (wrapper can't
  distinguish a child's own 124); interpreter isolation expressed as requested
  flags + child-reported state (binary provenance unbound); `pinned_timeout`
  honest via correction 7's mandatory timeout pin; python3 mandatory documented.
  Prereg §8.1 row 9 amended.
- **C5 / A11 — REPAIRED (re-run PENDING).** All eight fences carry unique
  anchored marker pairs; recorded commands are marker-based; R4 D026 POST
  assertions updated for the renamed tokens. The R4-fence open handle and the
  full re-run are pending Lead execution.
- **C6 — REPAIRED.** `RP6_REPAIR_R4_REPORT.md` stale `-S` "cannot be silently
  undone" claim replaced with the round-6 truth.
- **C7 — REPAIRED.** Exactly one frozen pin required per tool (twelve total),
  each equal to its frozen literal; omissions/extras/mismatches rejected;
  unpinned `command -v` fallback DELETED. Freeze-gate literals: **6 → 17**. Prereg
  §8.1 row 1 amended.

Current executable identity (round-7 bytes; hash/bytes/bash-n PENDING Lead
execution; CR bytes verified 0 by construction):

```text
sha256=fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd
bytes=103071
bash_n=PENDING-LEAD-EXECUTION
cr_bytes=0 (verified: tr -cd '\r' < RP6-P0.sh | wc -c)
line_endings=LF_only
bom=none
superseded_round6_sha256=75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570
superseded_round6_bytes=93421
freeze_gate_literal_count=17 (was 6; +11 per-tool path literals, correction 7)
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

The freeze gate now has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.

---

# Prior status history — round 6 (REPAIRED-PENDING-T0-REAUDIT, superseded by round 7)

Updated 2026-08-10 by the round-6 implementer (GLM-5.2, fresh session) for the
three Claude flagship re-audit findings (`RP6_CLAUDE_REAUDIT_R5_2026-08-10.md`
F1–F3). Audit tier: **T0** (host/execution-domain preflight). GLM-5.2 implemented
only; Claude is this block's auditor for these findings, so implementer/auditor
separation holds (GLM-5.2 also implemented round 5, which is permitted). Round 6
is authorised by owner grant #7 (2026-08-10), which lifts the T0 round cap for
this block set — rounds continue until both flagships accept; the acceptance
standard is unchanged. The block remains a draft: not frozen, accepted,
dispatchable, or authorised for host execution.

**QA execution was PENDING at implementer hand-off; the Lead has now EXECUTED it.**
The GLM-5.2 session gates `bash -n` and script execution (same blocker the C13
and round-5 GLM rounds recorded), so it recorded the R6 evidence as PENDING
rather than fabricate output — the correct behaviour under D026. The Lead ran all
of it in an unhindered Git Bash on 2026-08-10 against the round-6 bytes
`75db028e…` / 93421 B:

```text
bash -n RP6-P0.sh                  -> rc 0, BASH_N=PASS
CR bytes (tr -cd '\r' | wc -c)     -> 0
R6-F1 adversarial .pth             -> R6_F1_QA_SUMMARY cases=3  pass=3  fail=0 result=PASS
R6-F2 gids grammar + noglob        -> R6_F2_QA_SUMMARY cases=10 pass=10 fail=0 result=PASS
R6-F3 pin-glob + p0_lookup         -> R6_F3_QA_SUMMARY cases=7  pass=7  fail=0 result=PASS
five prior mandated fences, all rc 0 against the NEW bytes:
  backstop        C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS
  full-block D026 RP6_FULLBLOCK_D026_SUMMARY … result=PASS
  freeze gate     F2_FREEZE_GATE_QA_SUMMARY placeholder_rc=3 filled_fixture_rc=0 result=PASS
  R4 D026         RP6_R4_D026_SUMMARY findings=4 pth_forge=real_venv
                  manager_bound=real_timeout inventory_basis=23e55667@d6a976aa result=PASS
  C13 R4b         C13_R4B_ARM_QA_SUMMARY cases=27 result=PASS
```

**Lead finding — fence addressing is fragile and MUST be fixed before freeze.**
The five prior fences are addressed by absolute LINE RANGES. Round 6 grew this
file, so the recorded ranges `2545,2989` and `3353,3518` now cut into prose: they
returned `rc 2` / no summary on first run and looked like regressions. They are
not — re-run at their true boundaries (R4 D026 `2553,3007`; C13 R4b `3379,3544`)
both return `result=PASS` at rc 0. Every future round shifts them again. The R5
and R6 harnesses already use `BEGIN`/`END` markers and are immune. **Action for
the next round: give all five prior fences marker pairs and record marker-based
invocations instead of line numbers.** A freeze whose evidence cannot be re-run
by a third party is not freeze-grade evidence.

Round-6 disposition (Claude re-audit findings F1–F3) — full record in
`RP6_REPAIR_R6_REPORT.md`; harnesses + expected polarity in `SELF_QA_RP6.md` §R6.
The disposition of EVERY finding is stated explicitly, including non-repairs:

- **F1 (MEDIUM, carried from round 4 — round 5 left it unaddressed) — REPAIRED
  in scope; one site out of scope, disclosed.** The false "` -S` cannot be
  silently deleted / it produces a named STOP" claim is retracted at every
  in-scope site (the block's interpreter-section comment, `SELF_QA_RP6.md`'s R4
  prose and arm note, and the round-4 F1 bullet below) and restated truthfully:
  the child's `sys.flags` self-check guards only ACCIDENTAL flag-word loss (it
  runs inside the `-c` body); a HOSTILE `.pth` that `os._exit(0)`s at `site`
  startup defeats it, so ` -S` — not the self-check — is the load-bearing control
  that contains a hostile venv. The cooperating fixture is superseded by an
  ADVERSARIAL `.pth` (writes marker + forged `P0PY` line + `os._exit(0)`); under
  it the no-`-S` mutant is NOT caught (rc 0, marker created, forged accepted
  line, no STOP), which the claim now states plainly. The fourth site the audit
  named, `RP6_REPAIR_R4_REPORT.md:88`, is NOT in this round's four-file allowlist
  and was left untouched/stale, flagged for the Lead.
- **F2 (MEDIUM, NEW) — REPAIRED.** The raw `id -G` `gids` capture is now
  grammar-gated against `*[!0-9[:space:]]*` BEFORE any expansion, and the
  per-item split runs under `set -f` — the F3 pattern applied to `gids`. `*`,
  `0*`, `?` now STOP as `group_query_not_evaluable … response_not_decimal_gid_list`
  identically in an empty and a numeric-named cwd; the false `form=numeric_only`
  and the laundered whole-word intersection are gone; `HONEST_ROOT_GROUP`
  (`1001 0`) still STOPs with `capability_wider_than_ledger gid=0`.
- **F3 (LOW/MEDIUM, NEW) — REPAIRED.** The pin-path charset gate refuses `*`,
  `?`, `[` (`expected=printable_without_glob_metacharacters`); `p0_lookup`'s
  unquoted map split runs under `set -f`; the "deliberate and safe" comment now
  certifies safety against pathname expansion, not only word splitting.
- **Codex round-5 F1/F2/F3 — unchanged, still CLOSED** (no round-6 edit touches
  the pin post-loop gate, the `type -t` prerequisite, or the `P0_FORBIDDEN_GIDS`
  gate). **Round-4 nits 1-6 and round-5 nit 3 — still open (optional)**,
  untouched as permitted. Nit 1 (`set +f` restores to block-default ON, not
  caller-saved state) now spans three pairs; a full save/restore remains a future
  optional hardening.

Current executable identity (round-6 bytes; QA PENDING Lead execution):

```text
sha256=75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570
bytes=93421
bash_n=PASS (Lead-executed 2026-08-10, rc 0)
line_endings=LF_only
bom=none
superseded_round5_sha256=490e3e4edfec811dee3dc90c6693e8ebeb865eb946a431ff017de58e66f0ce5f
superseded_round5_bytes=89029
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

The freeze gate is unchanged in COUNT (still six `<PIN-AT-FREEZE>` literals), so
no end-to-end `P0 PASS` is possible and nothing here is dispatchable regardless
of this round's verdict.

---

# Prior status history — round 5 (REPAIRED-PENDING-T0-REAUDIT, superseded by round 6)

Updated 2026-08-10 by the round-5 implementer (GLM-5.2, fresh session) for the
three Codex final-audit findings (`RP6_CODEX_FINAL_AUDIT_2026-08-10.md` F1–F3).
Audit tier: **T0** (host/execution-domain preflight). GLM-5.2 implemented only;
it did not audit this block, so implementer/auditor separation holds. The
round-4 Codex audit closed the four round-4 findings, but its independent
whole-block sweep returned a non-accepting T0 verdict with three NEW required
repairs (F1 HIGH freeze-gate polarity; F2/F3 MEDIUM). Round 5 closes those three.
**Cap note:** the final-audit report itself states it "authorizes no additional
repair/audit round," and T0 is capped at 3; this round is therefore presented
for Lead adjudication of whether the owner amendment covering round 4 extends to
this round. Acceptance still requires fresh independent `claude-opus-5` xhigh
and `gpt-5.6-sol` xhigh verdicts. The block remains a draft: not frozen,
accepted, dispatchable, or authorised for host execution.

**QA execution was PENDING at implementer hand-off; the Lead has now EXECUTED it.**
The GLM-5.2 session gates `bash -n` and script execution (same blocker the C13
GLM-5.2 round recorded), so it recorded the evidence as PENDING rather than
fabricate output — the correct behaviour under D026. The Lead ran all of it in an
unhindered Git Bash on 2026-08-10 against the round-5 bytes `490e3e4e…` / 89029 B:

```text
bash -n RP6-P0.sh                      -> rc 0, BASH_N=PASS
CR bytes (tr -cd '\r' | wc -c)         -> 0
R5-F1 python3 freeze-gate polarity     -> R5_F1_QA_SUMMARY cases=6 pass=6 fail=0 result=PASS
R5-F2 RP0 symbol type assertion        -> R5_F2_QA_SUMMARY cases=4 pass=4 fail=0 result=PASS
R5-F3 forbidden-GID grammar + set -f   -> R5_F3_QA_SUMMARY cases=5 pass=5 fail=0 result=PASS
five prior mandated fences, all rc 0:
  952,1035    backstop            cases=4  PASS
  1678,2068   full-block D026     RP6_FULLBLOCK_D026_SUMMARY … result=PASS
  2286,2319   freeze-literal gate PASS
  2545,2989   R4 D026             PASS
  3353,3518   C13 R4b             C13_R4B_ARM_QA_SUMMARY cases=27 result=PASS
```

No regression: every `ASSERT_UNMET`/`FAIL` token in those transcripts sits on a
pre-fix or mutant variant (the intended RED polarity) — none on a repaired or
current variant, verified by filtering the transcripts. QA is therefore real
executed evidence, not design intent, and the block is ready for T0 re-audit
dispatch.

Round-5 disposition (Codex final-audit findings F1–F3) — full record in
`RP6_REPAIR_R5_REPORT.md`; harnesses + expected polarity in `SELF_QA_RP6.md` §R5:

- **F1 (HIGH) — REPAIRED IN THE BLOCK.** After the pin-parse loop, REQUIRE
  `P0_TRUSTED_PYTHON_BOUND=yes`, so omitting the `python3` pin is a named rc-3
  STOP (`input_pin_freeze_unfilled tool=python3 …
  detail=trusted_python_pin_omitted_freeze_gate_load_bearing`) rather than a
  bypass. Freeze-gate polarity is now correct: omission STOPs, presence (with the
  deploy-channel value filled) passes. The in-loop placeholder gate
  (`detail=deploy_channel_value_never_derived_here`) is preserved unchanged.
- **F2 (MEDIUM) — REPAIRED IN THE BLOCK.** The two RP0-symbol prerequisite
  checks now use an exact builtin `type -t … = function` assertion instead of
  `command -v`, so a PATH executable (or alias) of the same name is rejected at
  rc 3 (`… detail=not_a_shell_function`) and — critically — is never called,
  closing the pre-inventory child-execution channel. Genuine sourced functions
  still pass. (`command -v` remains correct inside `p0_resolve_tool`, where the
  intent is to resolve a PATH tool to an absolute path.)
- **F3 (MEDIUM) — REPAIRED IN THE BLOCK.** `P0_FORBIDDEN_GIDS` is now
  grammar-gated against `*[!0-9[:space:]]*` BEFORE any expansion, and both split
  loops (the input gate and the capability intersection loop) run with pathname
  expansion disabled (`set -f`). A wildcard or any non-digit/non-space byte is a
  STOP (`input_charset … expected=decimal_digits_and_separators_only`)
  regardless of cwd; valid lists are still admitted.

Current executable identity (round-5 bytes; QA EXECUTED by the Lead, see above):

```text
sha256=490e3e4edfec811dee3dc90c6693e8ebeb865eb946a431ff017de58e66f0ce5f
bytes=89029
bash_n=PASS (Lead-executed 2026-08-10, rc 0)
line_endings=LF_only
bom=none
superseded_round4_sha256=e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6
superseded_round4_bytes=85540
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

The freeze gate is unchanged in COUNT (still six `<PIN-AT-FREEZE>` literals); F1
makes the sixth one (`P0_FIXED_TRUSTED_PYTHON`) load-bearing by construction
instead of by operator choice.

---

# Prior status history — round 4 and earlier (REPAIRED-PENDING-AUDIT, do not treat as accepted)

Updated 2026-08-10 by the round-4 implementer (`claude-opus-5` xhigh, fresh
session). Audit tier: **T0** (host/execution-domain preflight). The second-flagship
Codex T0 audit of the round-3 bytes (`RP6_CODEX_T0_AUDIT_2026-08-10.md`) returned
**BLOCK on 4** — one executed security failure (the "read-only" interpreter probe
ran unverified venv startup code), one executed availability failure (row 9 could
hang with no reasoned STOP), and two exact frozen-contract mismatches. **Round 4
exceeds the recorded T0 cap under explicit owner authorisation**, granted for the
identical venv site-startup security class already resolved on RP7 (2026-08-10
~17:15) and extended to RP6-P0 by the Lead. Acceptance still requires fresh
independent `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh verdicts. The block
remains a draft: not frozen, accepted, dispatchable, or authorised for host
execution.

Round-4 executable identity (superseded by the round-5 bytes above):

```text
sha256=e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6
bytes=85540
bash_n=PASS
line_endings=LF_only
bom=none
superseded_round3_sha256=2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e
superseded_round3_bytes=71743
frozen_ro_basis=RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

Round-4 disposition (Codex T0 findings 1-4) — full record in
`RP6_REPAIR_R4_REPORT.md`, evidence in `SELF_QA_RP6.md`:

- **F1 (HIGH) — CLOSED (interpreter isolation); the `-S` sub-claim was NARROWED
  in round 6.** The interpreter probe runs `-I -S`, not `-I`. `-I` implies
  `-E`/`-P`/`-s` but not `-S`, so the previous bytes imported `site` and
  executed the judged venv's `*.pth` `import` lines before the `-c` body. The
  child also refuses to report a version unless `sys.flags.isolated` and
  `sys.flags.no_site` are both set. Round 6 retracts this bullet's earlier
  sentence that this means deleting ` -S` "yields a named
  `interpreter_startup_not_isolated` STOP instead of a silent hole": that holds
  only against a COOPERATING `.pth` (no `os._exit`); a HOSTILE `.pth` that
  `os._exit(0)`s before the `-c` body defeats the self-check, so ` -S` (not the
  self-check) is the load-bearing control (see round 6 / R6-F1). Every other
  false sentence was corrected here in round 4: the `MUTATION SURFACE` header,
  the "nothing is written" comment, and `P0_claim … mutation=none_in_this_block`,
  which becomes `mutation=no_filesystem_write_primitive_in_this_shell_source`,
  with `behaviour_inside_any_executed_tool_binary` added to `does_not_establish`.
  Falsified on a REAL venv with a REAL executable `.pth`: pre-fix bytes create the
  marker and still print the accepted line; repaired bytes do not.
- **F2 (MEDIUM) — CLOSED.** Row 9 is bounded by the pinned `timeout` placed INSIDE
  the cleared environment (`env -i LC_ALL=C <timeout> --signal=TERM
  --kill-after=5s 10s <systemctl> …`). rc 124/137/125 map to
  `manager_query_deadline_exceeded` / `manager_query_killed_after_deadline` /
  `bounding_wrapper_failed`, all under `system_manager_unreachable` at exit 3, with
  `budget_s` and a diagnostic-only `elapsed_s` recorded. Falsified with a real
  stalling shim: the pre-fix arm needed an external kill and emitted zero
  `P0_STOP` lines; the repaired arm returns its own bounded STOP with no external
  kill.
- **F3 (MEDIUM) — CLOSED.** The RO inventory is regenerated from the FROZEN RP7
  executable: the ten tools it pins (`stat readlink env find sha256sum systemctl
  ss curl timeout python3`) plus the P0-only `id` and `getent`. `grep` and `awk`
  are dropped — neither stage invokes them. `timeout` is now a resolved
  first-class tool; `python3` is inventoried, never executed by P0, and its pin is
  bound to the new `P0_FIXED_TRUSTED_PYTHON` freeze-gate literal with a
  python3-only canonicalisation allowance for the `/usr/bin/python3` symlink. A
  drift test re-derives the RO half from the frozen bytes; the auditor's own
  `input_pin_unknown_tool … tool=timeout` line is reproduced on the pre-fix bytes
  and a complete RP7 pin set is now accepted (`count=10 trusted_python_pin=yes`).
- **F4 (LOW/MED) — CLOSED.** `p0_resolve_passwd` exports `P0_PW_RC`, read from the
  last capture field so even a NUL-corrupted capture keeps the resolver's real
  status; both `identity_unresolvable` callers emit `rc=<n|na>`. The
  valid-no-match token was aligned by preregistering
  `state_account_resolution_unexpected` verbatim in §8.1 row 3 rather than
  changing the block, because positive absence of a dynamically allocated account
  is a host observation, not an inability to evaluate. Eight exact-WHOLE-LINE
  assertions (not substrings) cover rc-0 parse error, rc-2 no-match, rc-2
  diagnostic and other-nonzero for both accounts, each with its RED twin.

Round-3 disposition (re-audit R2 findings 1-3, nits 1-2) — full record in
`RP6_REPAIR_R3_REPORT.md`:

- **R2-F1 (MEDIUM):** the non-executable-tool STOP no longer asserts an
  invocation status it never observed. It now emits
  `tool_not_evaluable tool=<t> path=<resolved> rc=na
  detail=access_builtin_x_denied mechanism=access_builtin_x` — required token
  kept, resolved path restored, fabricated `rc=126` gone. Prereg §8.1 row 1 was
  amended to `rc=<n|na>` because P0 decides executability with shell builtins
  only and never invokes an inventory tool, so no arm of this block can carry an
  honest invocation status.
- **R2-F2 (MEDIUM):** the repair's own D026 evidence reproduces again. The
  full-block fence's RED side is pinned to the immutable `0bbc3591`
  (`= 90d8d447^`) instead of the moving `HEAD`, for both the block and the prereg
  draft, and all four recorded transcripts were re-executed and replaced. Three
  reproduce byte-identically; the fence matches after normalizing only its random
  `mktemp` root.
- **R2-F3 (LOW/MED):** row 8 now discriminates a crafted `/proc`. Each namespace
  link's followed device is compared against the root object's device — a
  namespace inode lives on the anonymous `nsfs` superblock, so a fabrication
  allocated on the root filesystem is refused as
  `namespace_link_on_root_filesystem`. Because a fabrication on any *other*
  filesystem would still pass, the evidence line states
  `procfs_identity=not_established` and the terminal claim carries
  `procfs_mount_identity_of_the_namespace_links` in `does_not_establish`.
- **Nit 1:** the `(os error 2)` classifier alternative was **dropped**, not kept,
  and its provenance corrected (see F1 below).
- **Nit 2:** the block header now names the GNU-producer assumption explicitly.

Full-block repair disposition:

- F1: the filesystem diagnostic classifier now accepts only the exact absolute
  `$P0_STAT` argv[0] prefix and the controlled C-locale GNU coreutils
  `stat`/`statx` forms. Both real-lstat missing-object arms flip from unclassified
  STOP rc 3 to the required host FAIL rc 1. **Corrected in round 3 (R2 nit 1):**
  the `(os error 2)` alternative this bullet used to call "the observed ENOENT
  form" was never observed here. `(os error N)` is a Rust `std::io::Error`
  rendering from uutils coreutils, and uutils prefixes its messages with the
  *basename* of `argv[0]`, so an absolute prefix combined with that suffix is
  unreachable. Round 3 deleted the alternative. The residual is stated in the
  block header: on a uutils host the whole class returns fail-closed at rc 3
  `path_probe_unclassified` rather than FAIL, and the shape must be re-pinned
  before such a host is preregistered.
- F2: P0 now requires frozen deploy-channel pins for user/mount/PID/network
  namespaces plus `stat -c '%d:%i' /`, validates the prelude values with reasoned
  rc-3 pre-checks and `:?` backstops, compares every live identity, and gates the
  manager query behind the comparison. Missing/unreadable input is
  `execution_domain_unattested`; mismatch is `execution_domain_mismatch`.
- F3: repeated separators in `P0_VENV_ROOT` STOP as
  `input_not_canonical_spelling` before any host object verdict.
- F4: duplicate/conflicting tool pins STOP as
  `prereg_input_malformed name=P0_TOOL_PINS duplicate=<tool>`; the count is now
  the count of distinct accepted tools.
- F5: every readlink producer uses `-v`; failed captures have nonempty bracketed
  `detail=` plus an explicit diagnostic-shape token.
- F6: getent capture uses NUL-delimited `mapfile` records with an out-of-band rc
  record; NUL emitted by the producer creates an extra record and becomes
  `identity_unresolvable` via `nul_byte_in_merged_capture`, never no-match.
- F7: `tool_not_evaluable` and `group_query_not_evaluable` are executable reason
  tokens. Every `identity_unexpected` line now uses
  `observed_numeric=<u:g> expected_numeric=<u:g> account=<a>`; §8.1 row 3 was
  aligned without changing row 9.

**Freeze gate — mandatory, same class as RP7. SIX literals after round 4.** The
following embedded literals remain `<PIN-AT-FREEZE>` and deliberately prevent an
end-to-end `P0 PASS`:

- `P0_FIXED_ATTESTED_USER_NS`
- `P0_FIXED_ATTESTED_MNT_NS`
- `P0_FIXED_ATTESTED_PID_NS`
- `P0_FIXED_ATTESTED_NET_NS`
- `P0_FIXED_ATTESTED_ROOT_MOUNT_ID`
- `P0_FIXED_TRUSTED_PYTHON` — **new in round 4**, the same deploy-channel value
  RP7 carries as `WPI_FIXED_TRUSTED_PYTHON`: the resolved non-symlink leaf behind
  `/usr/bin/python3`, because no symlinked object is admissible as a bound RO tool
  and both RO accepting adjudicators execute that exact object.

Before freeze/dispatch, the root-authorised deploy channel must mint the four exact
`readlink /proc/<attested-host-pid>/ns/<kind>` tokens, the exact
`stat -c '%d:%i' /` identity and the resolved trusted-python leaf, embed each
literal, supply identical prelude values, and re-run the whole block on the
intended guest. No value may be learned or re-pinned from the login session being
tested. `P0_MANAGER_QUERY_BUDGET_S=10` and `P0_MANAGER_QUERY_KILL_AFTER_S=5` are
NOT freeze-gate inputs — they are frozen design literals with real values, held in
the block precisely so the environment under test cannot raise its own deadline.

Local evidence, all executed in round 4 against `e93d07ad…` / 85540 B. The five
mandated fences and their results:

```text
sed -n '952,1035p'   SELF_QA_RP6.md  -> rc 0, backstop cases=4 PASS
sed -n '1678,2068p'  SELF_QA_RP6.md  -> rc 0, 39 ASSERT_MET, full-block PASS
sed -n '2286,2319p'  SELF_QA_RP6.md  -> rc 0, freeze-literal gate PASS
sed -n '2545,2989p'  SELF_QA_RP6.md  -> rc 0, 102 ASSERT_MET / 0 UNMET, R4 D026 PASS
sed -n '3353,3518p'  SELF_QA_RP6.md  -> rc 0, C13_R4B cases=27 PASS
```

The two older C13 fences (lines 664-787 and 1181-1346) assert the pre-round-4
`identity_unresolvable` grammar and are therefore RED against these bytes ON
PURPOSE — the exact assertions that break are the lines that lacked the mandatory
`rc=` field. They are retained as round records, their failing output is recorded
in `SELF_QA_RP6.md`, and they are superseded by the R4b harness, which carries all
27 of their cases with the corrected grammar. Both new fences were re-extracted
from the document and re-run: extraction byte-identical, both green, transcripts
reproduce after normalising the random `mktemp` root, with the single documented
exception of the F2 deadline arm's diagnostic-only `elapsed_s` (10 vs 11 s), which
no assertion reads. No host, SSH, network, deployment, backtest, broker, or trading
action occurred, and no commit was made.

---

# Prior status history — REPAIRED-PENDING-AUDIT, do not treat as accepted

Updated by the Codex implementer on 2026-08-10 under owner amendment A2/A2a. The
repair and its local falsification evidence are ready for independent Lead review;
the block is not frozen, accepted, dispatchable, or authorised for host execution.

- **F1 — REPAIRED BY HONEST DISCLOSURE.** The false fixed child count was removed.
  The header and terminal evidence now state the mixed environment, PATH-resolution,
  inherited-cwd and inherited-or-unset-TMPDIR surface, and explicitly do not claim
  round-1.4 probe-execution-environment binding. Full binding needs new preregistered
  inputs and is outside this bounded repair.
- **F2 — CLOSED BY LEAD ADJUDICATION; NO BLOCK CHANGE.** The existing STOP polarity
  remains correct under draft round 1.4's numeric-identity rows.
- **F3 — REPAIRED BY EXPLICIT RESIDUAL DISCLOSURE.** The terminal evidence now says
  P0 does not establish interpreter intermediate-component or symlink-target binding.
  Learning a target at runtime would violate row 18; accepting one requires a future
  preregistered target chain.
- **F4 — REPAIRED.** `:?` fail-closed backstops now follow the rc-3 pre-checks for
  `P0_EXPECT_UID`, `P0_FORBIDDEN_GIDS`, and `P0_VENV_ROOT`.

`SELF_QA_RP6.md` records literal local commands and real RED/GREEN output. No host
was contacted; no ssh, network, backtest, deployment, or trading action was run.

## C13 round — getent resolution arm (GLM-5.2 implementer, 2026-08-10)

Added by GLM-5.2 as IMPLEMENTER under the bounded C13 kickoff (round-1.4
section 8.1 rows 1–3, repair C13; Lead-adjudicated real conformance gap). Status
stays **REPAIRED-PENDING-AUDIT** — the Codex (G5) audit is outstanding, so the
block remains not frozen, not accepted, not dispatchable, and not authorised for
host execution.

- **C13 — IMPLEMENTED; QA EXECUTION PENDING.** Added one arm to `RP6-P0.sh`: a
  pinned-absolute `getent` (added to the inventory as the 12th RO tool) resolves
  `gatea` and `mtc-bridge`, each record parsed whole under the passwd grammar
  (Pattern 5; duplicate/multiline/malformed → ambiguous → STOP), admitting on
  NUMERIC uid/gid only (Pattern 8) with names as diagnostics. rc contract per
  the kickoff and the F2 polarity: getent missing/error/unparsable/duplicate →
  `identity_unresolvable` rc 3; `gatea` numeric mismatch → `identity_unexpected`
  rc 3; `mtc-bridge` valid no-match (rc 2) or numeric mismatch →
  `state_account_resolution_unexpected` rc 3. Two new preregistered inputs
  `P0_STATE_UID` (999) / `P0_STATE_GID` (988) use the same `p0_require_uint`
  rc-3 pre-check + `:?` backstop as `P0_EXPECT_UID` (F4 pattern). Claim lines
  updated honestly (11→12 tools; adds
  `name_to_numeric_resolution_of_gatea_and_mtc_bridge_via_getent`; discloses
  `nss_source_identity_of_getent_resolution`; `getent` joins the inherited-env
  set). Read-only scope, the 0/1/3 contract, STOP-vs-FAIL truthfulness, and all
  existing arms are preserved.
- **QA NOT YET EXECUTED — concrete harness blocker.** The GLM-5.2 implementer
  session's Bash tool gates interpreter/script execution (every `bash -n`,
  `bash -c`, path-script run, process substitution, brace heredoc, and
  off-tree write returned *requires approval* and was not approved this turn).
  `SELF_QA_RP6.md` therefore contains the paste-and-run RED/GREEN + backstop
  commands and the real final SHA-256/byte count, but the RED/GREEN real output
  and `bash -n` are marked **PENDING**, not fabricated. Per AGENTS.md the
  implementer reports this blocker rather than silently substituting fake
  evidence (D026 / Pattern 10; the GLM known-failure-mode of AGENTS.md rule 4).
- **Artefact (real, computed in-session).** Repaired `RP6-P0.sh` SHA-256
  `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109
  bytes (baseline `6c5b8945…766f7`, 44979 bytes). Three files touched only
  (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file); nothing committed.

**Required to close C13:** run the C13 commands in `SELF_QA_RP6.md` in an
unhindered Git Bash process (or have Codex run them at G5), paste the real
RED/GREEN output, and confirm `bash -n` PASS — then the Codex G5 audit.

**Lead QA execution, 2026-08-10 — the blocker above is CLEARED.** The Lead ran
the full C13 QA in an unhindered Git Bash: arm RED/GREEN 5/5 CASE_OK (GREEN
rc 0; four REDs rc 3 with the exact preregistered reason tokens); backstop
2/2 GREEN after a Lead harness correction (the drafted C13 backstop caller fed
`sed` no input and its summary was ungated — both defects recorded with the
as-drafted failing run in `SELF_QA_RP6.md`, then fixed); `bash -n` PASS; hash
and byte count re-verified identical to the implementer's record
(`cfdb23b8…`, 54109 B). Real outputs pasted into `SELF_QA_RP6.md`. Remaining
to close: the independent Codex G5 audit of the C13 arm.

## C13 round 3 — Codex audit repair (Claude Opus 5 implementer, 2026-08-10)

The Codex G5 audit of the C13 arm returned **BLOCK, 3 findings**
(`RP6_C13_CODEX_AUDIT_2026-08-10.md`: V2/V3/V5 FAIL, V1/V4/V6 PASS). GLM-5.2, the
C13 implementer, is quota-blocked, so Claude Opus 5 executed this bounded repair
round as implementer; it neither authored nor audited the C13 arm. Status stays
**REPAIRED-PENDING-AUDIT** — the block is not frozen, not accepted, not
dispatchable, and not authorised for host execution, and the Codex re-audit is
outstanding.

- **F1 (HIGH) — REPAIRED IN THE BLOCK.** `p0_resolve_passwd` accepts getent
  `rc 2` as `nomatch` only when the complete merged capture is empty, this
  interface's exact valid-no-match shape. `rc 2` carrying any byte (NSS
  diagnostic, partial record, module warning) is now `error`, so the caller emits
  `identity_unresolvable … rc 3` instead of asserting a positive absence it never
  observed. `P0_PW_DIAG` on the surviving no-match path records
  `empty_capture_at_rc2`. All other parser arms and both caller `case` statements
  are byte-identical, and the genuine `mtc-bridge` valid no-match still yields
  `state_account_resolution_unexpected observed_numeric=absent` (regression-tested).
- **F2 (MEDIUM) — REPAIRED IN THE QA.** The two earlier C13 fences are re-labelled
  SUPPLEMENTAL in place, and two D026 harnesses were added and executed locally.
  Harness 1 (16 cases) no longer calls the arm: it appends the block's own
  top-level driver lines, matched as exact whole lines out of the source bytes, so
  the block decides whether the arm runs; it then runs one assertion set across
  three variants — R3-repaired bytes, pre-R3 bytes (`cbaf3ec8`, `cfdb23b8…`), and
  bytes with the production integration call deleted. Deleting that call takes all
  three arm assertions to `ASSERT_UNMET`; the pre-repair bytes fail every F1
  assertion and are separately recorded emitting the defective
  `observed_numeric=absent` verdict. Harness 2 (4 cases) adds the mutation that
  removes each new `:?` backstop itself. Both harnesses check assertion POLARITY,
  so a surviving mutant fails the run.
- **F3 (MEDIUM) — REPAIRED IN THE BLOCK.** The "NUMERIC IDENTITY ONLY" header no
  longer claims that no name is looked up or captured and that the block asks the
  resolver database nothing. It states the truth: admission is numeric only and no
  name is ever compared or asserted; two names ARE queried via the pinned
  `getent passwd`; the returned name/gecos/home/shell fields are diagnostics no
  verdict depends on; NSS source identity is not established.
- **Artefact (real, computed in-session, Git Bash).** Repaired `RP6-P0.sh`
  SHA-256 `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`,
  55467 bytes (pre-R3 `cfdb23b8…`, 54109 bytes; diff 34 insertions / 12
  deletions, one file). `bash -n` rc 0, `BASH_N=PASS`. Harness 1 process rc 0,
  `C13_R3_ARM_QA_SUMMARY cases=16 result=PASS`; harness 2 process rc 0,
  `C13_R3_BACKSTOP_QA_SUMMARY … cases=4 result=PASS`. Both fenced commands in
  `SELF_QA_RP6.md` were re-run from the document itself and diffed byte-for-byte
  against the pasted output.
- **Scope.** Four files touched (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file,
  `RP6_C13_REPAIR_R3_REPORT.md`); nothing committed; no host contacted and no
  network command run. Read-only scope, the rc 0/1/3 contract, and every
  pre-existing arm are preserved.

**Required to close C13:** the independent Codex re-audit of the R3 bytes
`ef205e20…` (55467 B) against `RP6_C13_CODEX_AUDIT_2026-08-10.md`. — DONE: that
re-audit ran and returned BLOCK with 2 findings; see the round-4 section below,
which supersedes this requirement.

## C13 round 4 — Codex re-audit repair (Claude Opus 5 implementer, 2026-08-10)

The Codex re-audit of the R3 bytes returned **BLOCK, 2 findings**
(`RP6_C13_REAUDIT_CODEX_2026-08-10.md`: V1 and V4 FAIL, V2/V3/V5 PASS). This is the
last bounded round under the T0 cap. Claude Opus 5 executed it as implementer; it
neither authored nor audited the C13 arm. Status stays **REPAIRED-PENDING-AUDIT** —
the block is not frozen, not accepted, not dispatchable, and not authorised for host
execution.

- **Finding 1 (HIGH) — REPAIRED IN THE BLOCK.** `p0_resolve_passwd` captured getent
  with a plain `$( … )`, which deletes trailing newlines, so the `[ -n "$raw" ]`
  emptiness test could not tell a truly empty rc-2 capture from a newline-only one
  and admitted the latter as a valid no-match. The capture now appends a sentinel
  byte INSIDE the substitution and strips it afterwards, so the complete merged
  stream survives; `had_bytes` is decided on those preserved bytes before any
  normalization. A newline-only rc-2 capture is now `error` with
  `P0_PW_DIAG=newline_only_capture_at_rc2`, and the caller emits
  `identity_unresolvable … rc 3` for both accounts. getent sits on the left of `||`
  inside the substitution so an inherited `set -e` cannot kill the subshell before
  the sentinel is written, and its own rc is carried out by re-exiting the subshell
  with it. If the sentinel is missing anyway, the capture was truncated by something
  other than getent and the outcome is `error` / `capture_sentinel_lost` — fail
  closed, never a no-match. After the emptiness question is answered `raw` is
  normalized back to the value plain command substitution used to produce, so the
  rc-0 record parse and every diagnostic string are byte-identical to the
  R3-audited behaviour.
- **Finding 2 (MEDIUM) — NO REPAIR, LEAD-ADJUDICATED.** The extra committed
  provenance log was added by the Lead at commit time, not by the round-3
  implementer; the Lead recorded it as an accepted Lead-side deviation. Out of this
  round's scope; the file was not touched.
- **Same-pattern sweep.** `p0_resolve_passwd` is the only site in the block that
  adjudicates rc 2 as its own outcome (one `2)` case arm in the file). Every other
  capture site treats any non-zero rc as an error, and every other emptiness test —
  e.g. `p0_capture_numeric`'s `[ -n "$raw" ] || p0_stop identity_probe_empty` —
  fails CLOSED, so newline stripping there can only cause a STOP, never a false
  admission. No other site was changed.
- **QA (real, local Git Bash, D026).** `SELF_QA_RP6.md` harness 1 was extended, not
  replaced: all sixteen R3 cases verbatim, plus a fourth source variant `prer4` (the
  committed R3 bytes `ef205e20…`), three newline-only rc-2 shim modes
  (`mtc_rc2_newline`, `mtc_rc2_newlines3`, `gatea_rc2_newline`), the `nocall`
  mutation applied to the new case as well, and a probe that prints the auditor's own
  markers. Result: `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS`, process rc 0, 25
  `CASE_OK` + 2 `PROBE_OK`, zero `CASE_BAD`. The new fixture is GREEN on R4 bytes
  (`identity_unresolvable … detail=[newline_only_capture_at_rc2]` rc 3) and RED on
  the R3 bytes, which are separately recorded emitting the defect
  (`state_account_resolution_unexpected … observed_numeric=absent`). The probe
  reproduces `FALSE_NOMATCH_REPRODUCED=yes` / `REQUIRED_ERROR_OUTCOME_PRESENT=no` on
  R3 bytes and `no` / `yes` on R4 bytes. Harness 2 was re-run unchanged against the
  R4 bytes: process rc 0, `C13_R3_BACKSTOP_QA_SUMMARY … cases=4 result=PASS`.
- **Artefact (real, computed in-session, Git Bash).** Repaired `RP6-P0.sh` SHA-256
  `bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf`, 57441 bytes
  (pre-R4 `ef205e20…`, 55467 bytes; diff 36 insertions / 5 deletions, one file).
  `bash -n RP6-P0.sh` rc 0, `BASH_N=PASS`. The extended harness was re-run from the
  document itself (`sed -n '1159,1324p' SELF_QA_RP6.md | bash --noprofile --norc`)
  and its pasted output is that run.
- **Scope.** Four files touched (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file,
  `RP6_C13_REPAIR_R3_REPORT.md`); nothing committed; no host contacted and no network
  command run. Read-only scope, the rc 0/1/3 contract, and every pre-existing arm are
  preserved.

**Required to close C13:** the independent Codex re-audit of the R4 bytes
`bff3c86e…` (57441 B) against `RP6_C13_REAUDIT_CODEX_2026-08-10.md`.
