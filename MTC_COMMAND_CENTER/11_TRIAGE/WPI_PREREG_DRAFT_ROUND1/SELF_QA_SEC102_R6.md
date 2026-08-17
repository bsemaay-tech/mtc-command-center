# SELF-QA — SEC102 composite path proof, round 6

Implementer: `claude-opus-5` xhigh (Max account). Date: 2026-08-11. Input commit: `e3906cec`
(byte-identical `composite_pathproof.py` to the audited `7da76479` — verified in section 1).
No audit or acceptance is claimed here. No commit was made. No host or network was contacted.
No fixture shell was executed. Every command below is literal, starts with an absolute
`Set-Location`, and is therefore cwd-robust.

## 1. The finding, the repair, and where each piece of evidence lives

Codex round 5 (`SEC102_CODEX_T1_AUDIT_R5_2026-08-11.md`) returned **REQUEST_CHANGES** with one
CRITICAL, R5-F1: a pathname-expanded command word is classified as a benign leaf even when Bash
can resolve it to a recognised interpreter, so the following script operand is outside both
direct matchers and the independent word-conservation check — a silent no-edge RENDER
`PASS rc 0` over an unanalysed program.

This was the fourth command-word/prefix form found this way (round 4: numeric fd; round 5:
named fd, indexed assignment; round 5 audit: pathname expansion). The defect is not any one
missing form. It is the classifier's **default**: an unrecognised command word became a leaf, so
every form nobody enumerated inherited "benign". Round 6 inverts that default instead of adding
a fifth special case.

| Piece | Where |
|---|---|
| The audited baseline is the same code the kickoff names | section 1, below |
| The defect measured at the scanner boundary, both sides, 32 probes | section 2 |
| 52-case matrix, `FAILED_COUNT=0`, all 44 carried cases unchanged | section 3 |
| D026 pre-feature: 5 rc-level REDs, 2 measured carried STOPs, 1 GREEN control | section 4 |
| 6 mutation discriminators × 11 REDs = 66 cells, `OFF_EXPECTATION=0` | section 5 |
| Command-word grammar battery: 59 declared forms + 180-variant closure sweep | section 6 |
| Round-5 prefix battery re-run, and the one control that MOVED | section 7a |
| Five carried round-3/round-4 discriminators, still discriminating | section 7b |
| Three round-5 discriminators that stopped discriminating, and why | section 7c |
| Carried GREEN byte identity, determinism, hygiene, scope | section 8 |
| Artifact byte counts and SHA-256 | section 9 |
| Honest residual scope, including the new false stops | section 10 |
| Thirteen-pattern self-adjudication | section 11 |
| Paste-and-run verification of this document | section 12 |

**The baseline is the audited code.** The kickoff names `e3906cec` as input; Codex audited
`7da76479`. Both carry the same module byte-for-byte, so the pre-feature side of every D026
comparison below is the exact code Codex audited:

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$p='MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$audited=(git rev-parse "7da76479:$p")
$kickoff=(git rev-parse "e3906cec:$p")
"BLOB_AT_AUDITED_7da76479=$audited"
"BLOB_AT_KICKOFF_INPUT_e3906cec=$kickoff"
"BASELINE_IS_THE_AUDITED_CODE=$($audited -eq $kickoff)"
```

Real output:

```text
BLOB_AT_AUDITED_7da76479=dfac6ab21a413dfe3c9eab5359bc46e0b85e53fa
BLOB_AT_KICKOFF_INPUT_e3906cec=dfac6ab21a413dfe3c9eab5359bc46e0b85e53fa
BASELINE_IS_THE_AUDITED_CODE=True
```

### What changed in the code

1. **`COMMAND_WORD_SUBSTITUTION_RE = [$` + backtick + `]`** — parameter, command and arithmetic
   expansion in a command word. Deliberately redundant with `_graph_opaque_reason`, so no single
   fence carries this class alone.
2. **`COMMAND_WORD_EXPANSION_RE = [*?\[\]{}~\\]`** — pathname expansion, brace expansion, tilde
   expansion, and backslash-constructed names. Applied to the RAW word including quoted regions:
   quoting suppresses some of these, but a proof that this particular occurrence is suppressed is
   exactly the reasoning that produced R5-F1.
3. **`_command_word_class` is now a closed admissibility policy.** `leaf` — the one answer that
   means "benign, derives no edge" — is returned only for a proven-static literal that is not a
   recognised interpreter or source builtin. Everything else is `dynamic` or the new `unmodeled`,
   and both STOP. Assignment prefixes and reserved words are matched **before** the fence, so
   `SEEN[0]=1`, `{`, `}`, `[[` and `]]` are unaffected.
4. **`_graph_word_conservation` reports the new class** as `source_graph_unmodeled_command_word`.
5. **The reserved-word test now compares the RAW word**, not its unquoted literal. Bash only
   treats `if`/`{`/`[[` as reserved when written unquoted, so `"if"` is an ordinary command name;
   reading the literal promoted it to a reserved word and kept a command position open that Bash
   had already closed.
6. **Found while probing the same boundary, not named in the audit:** interpreter recognition
   took the basename only for an *absolute* path, so `bin/bash script.sh` and `./bash script.sh`
   were benign leaves while `/bin/bash script.sh` was recognised — the same interpreter, the same
   operand, hidden by a spelling. Recognition now takes the last pathname component of any
   command word containing a slash. This is measured, not asserted: it has its own RED fixture
   (`red_render_relative_interpreter.json`) and its own mutation discriminator (`M2`).

Nothing else moved. The four carried GREEN transcripts are byte-identical to `e3906cec`
(section 8), so no fence was weakened and no output surface was added.

## 2. The defect measured at the scanner boundary, both sides, one command

The module is loaded twice — once from the worktree, once streamed from `e3906cec` — and asked
what it sees. `SILENT_NO_EDGE` is true when the module reports **no edge, no uncovered command
word and no opaque reason** over bytes that reach another program: the exact shape of a false
RENDER PASS. Four expectation classes are declared, so the block fails if the repair became a
blanket STOP as easily as if it missed a form:

* `REACHES` — Bash reaches another program and the composite models no edge; must not be silent.
* `DERIVES` — the modelled interpreter/source form; must still derive its edge after the repair.
* `BENIGN` — Bash reaches nothing; must stay silent, i.e. no over-STOP.
* `DISCLOSED` — benign in Bash but refused by the closed policy; asserted so the conservative
  stop stays visible instead of drifting.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$old='e3906cec:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$probe=@'
import pathlib, subprocess, sys, types
TOOL = pathlib.Path(sys.argv[1]); OLD = sys.argv[2]
def load(name, source):
    module = types.ModuleType(name)
    module.__file__ = str(TOOL)
    sys.modules[name] = module
    exec(compile(source, str(TOOL), "exec"), module.__dict__)
    return module
new = load("cpp_new", TOOL.read_text(encoding="utf-8"))
old = load("cpp_old", subprocess.run(["git", "show", OLD], capture_output=True, text=True,
                                     check=True, encoding="utf-8").stdout)
# (label, rendered bytes, expectation)
#   REACHES  - Bash reaches another program at this command word and the composite models no
#              edge for it; the module must NOT be silent
#   DERIVES  - the modelled interpreter/source form; the module must derive an edge and must
#              still derive it after the repair
#   BENIGN   - Bash reaches nothing; the module must stay silent, i.e. no over-STOP
#   DISCLOSED- benign in Bash but refused by the closed policy; asserted so the conservative
#              stop stays visible instead of drifting
CASES = [
    ("glob_star_interpreter",     "/usr/bin/ba*h /safe/fixture/library.sh\n",                   "REACHES"),
    ("glob_question_interpreter", "/usr/bin/pytho? /safe/fixture/verifier.py\n",                "REACHES"),
    ("glob_bracket_interpreter",  "/usr/bin/[b]ash /safe/fixture/library.sh\n",                 "REACHES"),
    ("brace_interpreter",         "/usr/bin/{ba,z}sh /safe/fixture/library.sh\n",               "REACHES"),
    ("tilde_interpreter",         "~/bin/bash /safe/fixture/library.sh\n",                      "REACHES"),
    ("relative_interpreter",      "bin/bash /safe/fixture/library.sh\n",                        "REACHES"),
    ("dot_relative_interpreter",  "./bash /safe/fixture/library.sh\n",                          "REACHES"),
    ("relative_wrapper",          "bin/env bash /safe/fixture/library.sh\n",                    "REACHES"),
    ("glob_wrapper",              "en* bash /safe/fixture/library.sh\n",                        "REACHES"),
    ("glob_after_assign_prefix",  "A=1 /usr/bin/ba*h /safe/fixture/library.sh\n",               "REACHES"),
    ("glob_after_named_fd",       "{fd}>/dev/null /usr/bin/ba*h /safe/fixture/library.sh\n",    "REACHES"),
    ("glob_in_function_body",     "function reload { /usr/bin/ba*h /safe/fixture/library.sh; }\n", "REACHES"),
    ("escaped_interpreter",       "\\bash /safe/fixture/library.sh\n",                          "REACHES"),
    ("quoted_interpreter",        "\"bash\" /safe/fixture/library.sh\n",                        "REACHES"),
    ("param_interpreter",         "A=1 ${SHELL_BIN} /safe/fixture/library.sh\n",                "REACHES"),
    ("param_bare_interpreter",    "A=1 $SHELL_BIN /safe/fixture/library.sh\n",                  "REACHES"),
    ("substitution_interpreter",  "$(printf bash) /safe/fixture/library.sh\n",                  "REACHES"),
    ("modelled_interpreter_edge", "/usr/bin/bash /safe/fixture/library.sh\n",                   "DERIVES"),
    ("modelled_bare_interpreter", "bash /safe/fixture/library.sh\n",                            "DERIVES"),
    ("modelled_source_builtin",   "source /safe/fixture/library.sh\n",                          "DERIVES"),
    ("static_leaf",               "cat \"$ROOT/in.txt\"\n",                                     "BENIGN"),
    ("absolute_static_leaf",      "/bin/cat /safe/fixture/in.txt\n",                            "BENIGN"),
    ("relative_static_leaf",      "bin/verify_marker /safe/fixture/in.txt\n",                   "BENIGN"),
    ("group_command",             "{ /bin/cat /safe/fixture/in.txt; }\n",                       "BENIGN"),
    ("function_body_leaf",        "function reload { /bin/cat /safe/fixture/in.txt; }\n",       "BENIGN"),
    ("double_bracket_test",       "[[ -f /safe/fixture/in.txt ]]\n",                            "BENIGN"),
    ("assign_prefix_leaf",        "A=1 /bin/cat /safe/fixture/in.txt\n",                        "BENIGN"),
    ("named_fd_leaf",             "{fd}>/dev/null /bin/cat /safe/fixture/in.txt\n",             "BENIGN"),
    ("test_builtin_bracket",      "[ -f /safe/fixture/in.txt ]\n",                              "DISCLOSED"),
    ("escaped_leaf",              "\\cat /safe/fixture/in.txt\n",                               "DISCLOSED"),
    ("tilde_leaf",                "~/bin/verify_marker /safe/fixture/in.txt\n",                 "DISCLOSED"),
    ("glob_leaf",                 "/safe/fixture/*.tool /safe/fixture/in.txt\n",                "DISCLOSED"),
]
def matchers(module, text):
    return (list(module.SOURCE_COMMAND_RE.finditer(text)),
            list(module.EXEC_COMMAND_RE.finditer(text)))
def silent(module, text):
    """True when the module sees no edge, no uncovered command word and no opaque reason."""
    if module._graph_opaque_reason(text) is not None:
        return False
    src, exe = matchers(module, text)
    return not src and not exe and not module._graph_word_conservation(text, src, exe)
def derives(module, text):
    src, exe = matchers(module, text)
    return bool(src or exe) and not module._graph_word_conservation(text, src, exe)
bad = 0
newly = 0
for label, text, expectation in CASES:
    before, after = silent(old, text), silent(new, text)
    if expectation == "BENIGN":
        ok = after
    elif expectation == "DERIVES":
        ok = (not after) and derives(old, text) and derives(new, text)
    else:
        ok = not after
    if expectation == "REACHES" and before and not after:
        newly += 1
    bad += not ok
    print(f"PROBE={label:26s} EXPECT={expectation:9s} e3906cec_SILENT_NO_EDGE={str(before):5s} "
          f"R6_SILENT_NO_EDGE={str(after):5s} {'OK' if ok else 'OFF_EXPECTATION'}")
print(f"PROBES={len(CASES)} OFF_EXPECTATION={bad} NEWLY_CLOSED_BY_R6={newly}")
sys.exit(0 if bad == 0 else 1)
'@
$probe | python -B - $tool $old
"PROBE_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
PROBE=glob_star_interpreter      EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=glob_question_interpreter  EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=glob_bracket_interpreter   EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=brace_interpreter          EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=tilde_interpreter          EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=relative_interpreter       EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=dot_relative_interpreter   EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=relative_wrapper           EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=glob_wrapper               EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=glob_after_assign_prefix   EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=glob_after_named_fd        EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=glob_in_function_body      EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=escaped_interpreter        EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=quoted_interpreter         EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=param_interpreter          EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=param_bare_interpreter     EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=substitution_interpreter   EXPECT=REACHES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=modelled_interpreter_edge  EXPECT=DERIVES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=modelled_bare_interpreter  EXPECT=DERIVES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=modelled_source_builtin    EXPECT=DERIVES   e3906cec_SILENT_NO_EDGE=False R6_SILENT_NO_EDGE=False OK
PROBE=static_leaf                EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=absolute_static_leaf       EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=relative_static_leaf       EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=group_command              EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=function_body_leaf         EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=double_bracket_test        EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=assign_prefix_leaf         EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=named_fd_leaf              EXPECT=BENIGN    e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=True  OK
PROBE=test_builtin_bracket       EXPECT=DISCLOSED e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=escaped_leaf               EXPECT=DISCLOSED e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=tilde_leaf                 EXPECT=DISCLOSED e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBE=glob_leaf                  EXPECT=DISCLOSED e3906cec_SILENT_NO_EDGE=True  R6_SILENT_NO_EDGE=False OK
PROBES=32 OFF_EXPECTATION=0 NEWLY_CLOSED_BY_R6=12
PROBE_BLOCK_RC=0
```

Command rc: `0`. **Twelve forms that reach another program were silent on the audited code and
are not silent now.** Eight benign forms stay silent and three modelled forms still derive their
edge, so this is a repair and not a blanket STOP. Four forms are published as conservative stops
(section 10, residual 28) rather than tuned away.

Note the honest asymmetry in the `REACHES` group: five forms (`escaped_`, `quoted_`, `param_`,
`param_bare_`, `substitution_`) were **already** not silent at `e3906cec`. They are kept in the
block as carried controls, not counted as newly closed, and `NEWLY_CLOSED_BY_R6=12` counts only
the forms that actually changed.

## 3. Literal all-case assertion command — 52 cases

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r1='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
$r4='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures'
$r5='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures'
$r6='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r6_fixtures'
$cases=@(
  @('allocate',$r1,'red_plan_contract.json',3,'plan_schema_unknown_key'),
  @('allocate',$r1,'red_entrypoint.json',1,'entrypoint_not_declared'),
  @('allocate',$r1,'red_allocation_conservation.json',1,'allocation_not_one_to_one'),
  @('allocate',$r1,'red_allocation_value.json',3,'allocation_value_unresolved'),
  @('allocate',$r1,'red_graph_conservation.json',1,'declared_member_unreachable'),
  @('allocate',$r1,'red_component_identity.json',3,'member_file_missing'),
  @('allocate',$r1,'green.json',0,'allocate_stage_closed'),
  @('render',$r2,'red_render_contract.json',3,'plan_schema_unknown_key'),
  @('render',$r2,'red_render_template_conservation.json',1,'render_template_member_not_one_to_one'),
  @('render',$r2,'red_render_materialisation.json',1,'rendered_bytes_mismatch'),
  @('render',$r2,'red_render_graph_dynamic.json',3,'source_operand_dynamic'),
  @('render',$r2,'red_render_identity.json',3,'member_file_missing'),
  @('render',$r2,'red_render_member_disposition.json',1,'render_member_rejected'),
  @('render',$r2,'red_render_heredoc_false_edge.json',3,'source_graph_heredoc_not_modeled'),
  @('render',$r3,'red_render_non_shell_member.json',3,'member_kind_graph_derivation_not_modeled'),
  @('render',$r2,'green_render.json',0,'render_stage_closed'),
  @('freeze',$r2,'red_freeze_contract.json',3,'plan_schema_unknown_key'),
  @('freeze',$r2,'red_freeze_member_pin.json',3,'frozen_identity_mismatch'),
  @('freeze',$r2,'red_freeze_graph.json',3,'derived_declared_graph_mismatch'),
  @('freeze',$r2,'red_freeze_prover_pin.json',3,'approved_prover_identity_not_declared'),
  @('freeze',$r2,'red_freeze_prover_grammar.json',3,'prover_output_grammar_incomplete'),
  @('freeze',$r2,'red_freeze_coverage.json',3,'coverage_issue_count=2'),
  @('freeze',$r2,'red_freeze_forbidden.json',1,'prover_forbidden_operand'),
  @('freeze',$r2,'red_freeze_residual.json',3,'prover_residual_disclosure_missing'),
  @('freeze',$r2,'red_freeze_member_disposition.json',3,'non_shell_member_analyzer_not_integrated'),
  @('freeze',$r3,'red_freeze_deploy_identity.json',3,'source_operand_deploy_identity_unbound'),
  @('freeze',$r3,'red_freeze_deploy_path_invalid.json',3,'member_deploy_path_not_canonical_absolute'),
  @('freeze',$r3,'red_freeze_deploy_path_alias.json',3,'member_deploy_path_alias'),
  @('freeze',$r3,'red_freeze_allocation_constants.json',3,'allocation_constants_value_divergence'),
  @('freeze',$r3,'red_freeze_constants_grammar.json',3,'constants_line_not_key_value'),
  @('freeze',$r3,'red_freeze_constants_operand_unbound.json',3,'analysis_unit_source_operand_constants_unbound'),
  @('freeze',$r3,'red_freeze_execute_source_edge.json',3,'analysis_unit_non_source_edge_not_integrated'),
  @('freeze',$r3,'red_freeze_source_site_not_standalone.json',3,'analysis_unit_source_site_not_standalone'),
  @('freeze',$r3,'red_freeze_zero_facts.json',3,'prover_zero_facts_pass'),
  @('freeze',$r3,'red_freeze_divergent_control.json',1,'prover_forbidden_operand'),
  @('freeze',$r2,'green_freeze.json',0,'freeze_stage_closed'),
  @('freeze',$r2,'green_freeze_network.json',0,'resolved_net_endpoint_count=1'),
  @('render',$r4,'red_render_wrapped_source.json',3,'source_graph_command_wrapper_not_modeled'),
  @('freeze',$r4,'red_freeze_wrapped_source.json',3,'source_graph_command_word_not_modeled'),
  @('freeze',$r4,'red_freeze_allocation_absent.json',3,'allocation_absent_from_pinned_constants'),
  @('render',$r5,'red_render_named_fd_source.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r5,'red_render_indexed_assign_source.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r5,'red_render_unmodeled_prefix.json',3,'source_graph_unmodeled_assignment_prefix'),
  @('render',$r5,'red_render_function_body_source.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r6,'red_render_glob_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_bracket_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_brace_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_tilde_command_word.json',3,'source_graph_unmodeled_command_word'),
  @('render',$r6,'red_render_relative_interpreter.json',3,'source_graph_command_word_not_modeled'),
  @('render',$r6,'red_render_param_command_word.json',3,'source_graph_dynamic_command_not_modeled'),
  @('render',$r6,'red_render_substitution_command_word.json',3,'source_graph_nested_execution_not_modeled'),
  @('render',$r6,'green_render_static_leaf.json',0,'render_stage_closed')
)
$failed=0
foreach($case in $cases){
  $stage=$case[0]; $dir=$case[1]; $name=$case[2]
  $want=[int]$case[3]; $token=$case[4]
  $out=(& python -B $tool $stage (Join-Path $dir $name)) -join "`n"
  $got=$LASTEXITCODE
  $ok=($got -eq $want -and $out.Contains($token))
  if(-not $ok){$failed++}
  "CASE=$name STAGE=$stage RC=$got EXPECTED=$want TOKEN=$token ASSERT=$(if($ok){'PASS'}else{'FAIL'})"
}
"CASES=$($cases.Count) FAILED_COUNT=$failed"
if($failed){exit 1}else{exit 0}
```

Real output:

```text
CASE=red_plan_contract.json STAGE=allocate RC=3 EXPECTED=3 TOKEN=plan_schema_unknown_key ASSERT=PASS
CASE=red_entrypoint.json STAGE=allocate RC=1 EXPECTED=1 TOKEN=entrypoint_not_declared ASSERT=PASS
CASE=red_allocation_conservation.json STAGE=allocate RC=1 EXPECTED=1 TOKEN=allocation_not_one_to_one ASSERT=PASS
CASE=red_allocation_value.json STAGE=allocate RC=3 EXPECTED=3 TOKEN=allocation_value_unresolved ASSERT=PASS
CASE=red_graph_conservation.json STAGE=allocate RC=1 EXPECTED=1 TOKEN=declared_member_unreachable ASSERT=PASS
CASE=red_component_identity.json STAGE=allocate RC=3 EXPECTED=3 TOKEN=member_file_missing ASSERT=PASS
CASE=green.json STAGE=allocate RC=0 EXPECTED=0 TOKEN=allocate_stage_closed ASSERT=PASS
CASE=red_render_contract.json STAGE=render RC=3 EXPECTED=3 TOKEN=plan_schema_unknown_key ASSERT=PASS
CASE=red_render_template_conservation.json STAGE=render RC=1 EXPECTED=1 TOKEN=render_template_member_not_one_to_one ASSERT=PASS
CASE=red_render_materialisation.json STAGE=render RC=1 EXPECTED=1 TOKEN=rendered_bytes_mismatch ASSERT=PASS
CASE=red_render_graph_dynamic.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_operand_dynamic ASSERT=PASS
CASE=red_render_identity.json STAGE=render RC=3 EXPECTED=3 TOKEN=member_file_missing ASSERT=PASS
CASE=red_render_member_disposition.json STAGE=render RC=1 EXPECTED=1 TOKEN=render_member_rejected ASSERT=PASS
CASE=red_render_heredoc_false_edge.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_heredoc_not_modeled ASSERT=PASS
CASE=red_render_non_shell_member.json STAGE=render RC=3 EXPECTED=3 TOKEN=member_kind_graph_derivation_not_modeled ASSERT=PASS
CASE=green_render.json STAGE=render RC=0 EXPECTED=0 TOKEN=render_stage_closed ASSERT=PASS
CASE=red_freeze_contract.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=plan_schema_unknown_key ASSERT=PASS
CASE=red_freeze_member_pin.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=frozen_identity_mismatch ASSERT=PASS
CASE=red_freeze_graph.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=derived_declared_graph_mismatch ASSERT=PASS
CASE=red_freeze_prover_pin.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=approved_prover_identity_not_declared ASSERT=PASS
CASE=red_freeze_prover_grammar.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=prover_output_grammar_incomplete ASSERT=PASS
CASE=red_freeze_coverage.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=coverage_issue_count=2 ASSERT=PASS
CASE=red_freeze_forbidden.json STAGE=freeze RC=1 EXPECTED=1 TOKEN=prover_forbidden_operand ASSERT=PASS
CASE=red_freeze_residual.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=prover_residual_disclosure_missing ASSERT=PASS
CASE=red_freeze_member_disposition.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=non_shell_member_analyzer_not_integrated ASSERT=PASS
CASE=red_freeze_deploy_identity.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=source_operand_deploy_identity_unbound ASSERT=PASS
CASE=red_freeze_deploy_path_invalid.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=member_deploy_path_not_canonical_absolute ASSERT=PASS
CASE=red_freeze_deploy_path_alias.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=member_deploy_path_alias ASSERT=PASS
CASE=red_freeze_allocation_constants.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=allocation_constants_value_divergence ASSERT=PASS
CASE=red_freeze_constants_grammar.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=constants_line_not_key_value ASSERT=PASS
CASE=red_freeze_constants_operand_unbound.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=analysis_unit_source_operand_constants_unbound ASSERT=PASS
CASE=red_freeze_execute_source_edge.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=analysis_unit_non_source_edge_not_integrated ASSERT=PASS
CASE=red_freeze_source_site_not_standalone.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=analysis_unit_source_site_not_standalone ASSERT=PASS
CASE=red_freeze_zero_facts.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=prover_zero_facts_pass ASSERT=PASS
CASE=red_freeze_divergent_control.json STAGE=freeze RC=1 EXPECTED=1 TOKEN=prover_forbidden_operand ASSERT=PASS
CASE=green_freeze.json STAGE=freeze RC=0 EXPECTED=0 TOKEN=freeze_stage_closed ASSERT=PASS
CASE=green_freeze_network.json STAGE=freeze RC=0 EXPECTED=0 TOKEN=resolved_net_endpoint_count=1 ASSERT=PASS
CASE=red_render_wrapped_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_wrapper_not_modeled ASSERT=PASS
CASE=red_freeze_wrapped_source.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_freeze_allocation_absent.json STAGE=freeze RC=3 EXPECTED=3 TOKEN=allocation_absent_from_pinned_constants ASSERT=PASS
CASE=red_render_named_fd_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_indexed_assign_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_unmodeled_prefix.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_assignment_prefix ASSERT=PASS
CASE=red_render_function_body_source.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_glob_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_bracket_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_brace_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_tilde_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_unmodeled_command_word ASSERT=PASS
CASE=red_render_relative_interpreter.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_command_word_not_modeled ASSERT=PASS
CASE=red_render_param_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_dynamic_command_not_modeled ASSERT=PASS
CASE=red_render_substitution_command_word.json STAGE=render RC=3 EXPECTED=3 TOKEN=source_graph_nested_execution_not_modeled ASSERT=PASS
CASE=green_render_static_leaf.json STAGE=render RC=0 EXPECTED=0 TOKEN=render_stage_closed ASSERT=PASS
CASES=52 FAILED_COUNT=0
```

Command rc: `0`. **All 44 round-5 cases are carried with their rc and reason token unchanged**;
eight are round-6 additions. No prior fixture file was edited (section 8).

## 4. D026 RED before GREEN — behavioural pre-feature falsification

Every round-6 plan runs over byte-identical inputs against the audited code streamed from
`e3906cec` and against the worktree code. The declared roles are asserted, so a case that is not
the kind of case it claims to be fails the block.

**The kickoff asked for four new REDs: glob, parameter expansion, command substitution, tilde.
Only two of those four are actually rc-level REDs.** Parameter expansion and command
substitution were *already* `STOP rc 3` at `e3906cec` — the first through the command-word
`dynamic` class, the second through `_graph_opaque_reason`'s nested-execution gate. The kickoff's
premise that they leafed a hidden interpreter into a PASS is not what the tool does. Rather than
retro-fit a fixture to the expectation, the measured before-state is published and those two are
carried as `CARRIED_STOP` controls. Three further rc-level REDs found while bounding the class
(bracket-glob, brace, relative-path interpreter) take the count to five.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r6=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r6_fixtures').Path
$old='e3906cec:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$prefeature=@'
import contextlib, io, pathlib, re, subprocess, sys
TOOL = pathlib.Path(sys.argv[1]); FX = pathlib.Path(sys.argv[2]); OLD = sys.argv[3]
NEW_SOURCE = TOOL.read_text(encoding="utf-8")
OLD_SOURCE = subprocess.run(["git", "show", OLD], capture_output=True, text=True,
                            check=True, encoding="utf-8").stdout
# (plan, declared role, expected rc on e3906cec, expected rc under round 6)
CASES = [
    ("red_render_glob_command_word.json",         "NEW_RED",       0, 3),
    ("red_render_bracket_command_word.json",      "NEW_RED",       0, 3),
    ("red_render_brace_command_word.json",        "NEW_RED",       0, 3),
    ("red_render_tilde_command_word.json",        "NEW_RED",       0, 3),
    ("red_render_relative_interpreter.json",      "NEW_RED",       0, 3),
    ("red_render_param_command_word.json",        "CARRIED_STOP",  3, 3),
    ("red_render_substitution_command_word.json", "CARRIED_STOP",  3, 3),
    ("green_render_static_leaf.json",             "GREEN_CONTROL", 0, 0),
]
R4 = re.compile(r'^CLAIM id="R4".*reason="([^"]*)"', re.MULTILINE)
def run(source, plan):
    buffer = io.StringIO(); argv = sys.argv[:]
    sys.argv = [str(TOOL), "render", str(plan)]
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(source, str(TOOL), "exec"), {"__name__": "__main__", "__file__": str(TOOL)})
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = argv
    found = R4.search(buffer.getvalue())
    return code, (found.group(1) if found else "-")
off = 0
new_reds = 0
for name, role, want_old, want_new in CASES:
    old_rc, old_reason = run(OLD_SOURCE, FX / name)
    new_rc, new_reason = run(NEW_SOURCE, FX / name)
    ok = old_rc == want_old and new_rc == want_new
    off += not ok
    new_reds += role == "NEW_RED" and old_rc == 0 and new_rc == 3
    print(f"CASE={name}")
    print(f"  ROLE={role} EXPECT_e3906cec_RC={want_old} GOT={old_rc}  EXPECT_R6_RC={want_new} GOT={new_rc} "
          f"{'OK' if ok else 'OFF_EXPECTATION'}")
    print(f"  e3906cec_R4={old_reason}")
    print(f"  R6_R4={new_reason}")
print(f"CASES={len(CASES)} RC_LEVEL_NEW_REDS={new_reds} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$prefeature | python -B - $tool $r6 $old
"PREFEATURE_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
CASE=red_render_glob_command_word.json
  ROLE=NEW_RED EXPECT_e3906cec_RC=0 GOT=0  EXPECT_R6_RC=3 GOT=3 OK
  e3906cec_R4=rendered_bytes_derive_the_declared_reachable_graph
  R6_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_bracket_command_word.json
  ROLE=NEW_RED EXPECT_e3906cec_RC=0 GOT=0  EXPECT_R6_RC=3 GOT=3 OK
  e3906cec_R4=rendered_bytes_derive_the_declared_reachable_graph
  R6_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_brace_command_word.json
  ROLE=NEW_RED EXPECT_e3906cec_RC=0 GOT=0  EXPECT_R6_RC=3 GOT=3 OK
  e3906cec_R4=rendered_bytes_derive_the_declared_reachable_graph
  R6_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_tilde_command_word.json
  ROLE=NEW_RED EXPECT_e3906cec_RC=0 GOT=0  EXPECT_R6_RC=3 GOT=3 OK
  e3906cec_R4=rendered_bytes_derive_the_declared_reachable_graph
  R6_R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
CASE=red_render_relative_interpreter.json
  ROLE=NEW_RED EXPECT_e3906cec_RC=0 GOT=0  EXPECT_R6_RC=3 GOT=3 OK
  e3906cec_R4=rendered_bytes_derive_the_declared_reachable_graph
  R6_R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
CASE=red_render_param_command_word.json
  ROLE=CARRIED_STOP EXPECT_e3906cec_RC=3 GOT=3  EXPECT_R6_RC=3 GOT=3 OK
  e3906cec_R4=derived_graph_not_traversable,source_graph_dynamic_command_not_modeled
  R6_R4=derived_graph_not_traversable,source_graph_dynamic_command_not_modeled
CASE=red_render_substitution_command_word.json
  ROLE=CARRIED_STOP EXPECT_e3906cec_RC=3 GOT=3  EXPECT_R6_RC=3 GOT=3 OK
  e3906cec_R4=derived_graph_not_traversable,source_graph_nested_execution_not_modeled
  R6_R4=derived_graph_not_traversable,source_graph_nested_execution_not_modeled
CASE=green_render_static_leaf.json
  ROLE=GREEN_CONTROL EXPECT_e3906cec_RC=0 GOT=0  EXPECT_R6_RC=0 GOT=0 OK
  e3906cec_R4=rendered_bytes_derive_the_declared_reachable_graph
  R6_R4=rendered_bytes_derive_the_declared_reachable_graph
CASES=8 RC_LEVEL_NEW_REDS=5 OFF_EXPECTATION=0
PREFEATURE_BLOCK_RC=0
```

Command rc: `0`. Five rc-level REDs, each `PASS rc 0` with `R4`, `R6` and `R7` all PASS on the
audited code, each `STOP rc 3` now. The GREEN control proves the same policy still admits a
proven-static non-interpreter leaf — including `/bin/cat` and the slash-relative
`bin/verify_marker`, which is what the round-6 basename change could plausibly have broken.

## 5. D026 mutation discriminators — 6 mutations × 11 REDs

Each mutation disables exactly one production comparison; the file on disk is never changed, the
mutated source is compiled and executed in memory. Every mutation is run against **all eleven**
REDs — the seven round-6 fixtures and the four round-5 fixtures — so the matrix also answers the
round-5 audit's required discriminator directly: **every mutation that removes a round-6 fence
leaves `named_fd`, `indexed_assign`, `unmodeled_prefix` and `function_body` intact.**
`EXPECTED_KILLS` is declared in the script and asserted.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r5=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures').Path
$r6=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r6_fixtures').Path
$mutants=@'
import contextlib, io, pathlib, re, sys
TOOL = pathlib.Path(sys.argv[1]); FX5 = pathlib.Path(sys.argv[2]); FX6 = pathlib.Path(sys.argv[3])
SOURCE = TOOL.read_text(encoding="utf-8")
EXPANSION_FENCE = ('    if COMMAND_WORD_EXPANSION_RE.search(raw):\n'
                   '        return "unmodeled"\n')
SUBSTITUTION_FENCE = ('    if COMMAND_WORD_SUBSTITUTION_RE.search(raw):\n'
                      '        return "dynamic"\n')
BASENAME_R6 = ('    if "/" in literal:\n'
               '        name = posixpath.basename(literal)\n'
               '        if name == "":\n'
               '            return "unmodeled"\n'
               '    else:\n'
               '        name = literal\n')
BASENAME_R5 = '    name = posixpath.basename(literal) if literal.startswith("/") else literal\n'
UNMODELED_REPORT = (
    '        elif word_class == "unmodeled":\n'
    '            # A command word Bash expands before looking it up.  It is refused here\n'
    '            # rather than leafed, so whatever it would have expanded to - including a\n'
    '            # recognised interpreter with a script operand behind it - cannot pass\n'
    '            # through unanalysed.\n'
    '            reasons.append("source_graph_unmodeled_command_word")\n')
EXPANSION_RE_R6 = 'COMMAND_WORD_EXPANSION_RE = re.compile(r"[*?\\[\\]{}~\\\\]")'
EXPANSION_RE_NARROW = 'COMMAND_WORD_EXPANSION_RE = re.compile(r"[*?]")'
MUTATIONS = {
  "M1_expansion_fence_deleted":        [(EXPANSION_FENCE, "")],
  "M2_basename_absolute_only":         [(BASENAME_R6, BASENAME_R5)],
  "M3_unmodeled_reason_deleted":       [(UNMODELED_REPORT, "")],
  "M4_round5_classifier_restored":     [(EXPANSION_FENCE, ""), (BASENAME_R6, BASENAME_R5)],
  "M5_expansion_class_narrowed":       [(EXPANSION_RE_R6, EXPANSION_RE_NARROW)],
  "M6_substitution_fence_deleted":     [(SUBSTITUTION_FENCE, "")],
}
EXPECTED_KILLS = {
  "M1_expansion_fence_deleted":    {"glob", "bracket", "brace"},
  "M2_basename_absolute_only":     {"relative"},
  "M3_unmodeled_reason_deleted":   {"glob", "bracket", "brace", "tilde"},
  "M4_round5_classifier_restored": {"glob", "bracket", "brace", "tilde", "relative"},
  "M5_expansion_class_narrowed":   {"bracket", "brace"},
  "M6_substitution_fence_deleted": set(),
}
CASES = [("glob",             FX6, "red_render_glob_command_word.json"),
         ("bracket",          FX6, "red_render_bracket_command_word.json"),
         ("brace",            FX6, "red_render_brace_command_word.json"),
         ("tilde",            FX6, "red_render_tilde_command_word.json"),
         ("relative",         FX6, "red_render_relative_interpreter.json"),
         ("param",            FX6, "red_render_param_command_word.json"),
         ("substitution",     FX6, "red_render_substitution_command_word.json"),
         ("named_fd",         FX5, "red_render_named_fd_source.json"),
         ("indexed_assign",   FX5, "red_render_indexed_assign_source.json"),
         ("unmodeled_prefix", FX5, "red_render_unmodeled_prefix.json"),
         ("function_body",    FX5, "red_render_function_body_source.json")]
R4 = re.compile(r'^CLAIM id="R4".*reason="([^"]*)"', re.MULTILINE)
def run(source, plan):
    buffer = io.StringIO(); argv = sys.argv[:]
    sys.argv = [str(TOOL), "render", str(plan)]
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(source, str(TOOL), "exec"), {"__name__": "__main__", "__file__": str(TOOL)})
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = argv
    found = R4.search(buffer.getvalue())
    return code, (found.group(1) if found else "-")
off = 0
print("BASELINE unmutated round-6 code on disk")
for label, root, name in CASES:
    code, reason = run(SOURCE, root / name)
    state = "STOP" if code == 3 else ("PASS" if code == 0 else f"rc{code}")
    if code != 3:
        off += 1
    print(f"  BASELINE RED={label:16s} rc={code} {state} R4={reason}")
for mutation, edits in MUTATIONS.items():
    mutated = SOURCE
    applied = 0
    for old, new in edits:
        if mutated.count(old) != 1:
            print(f"MUTATION={mutation} ANCHOR_NOT_UNIQUE count={mutated.count(old)}")
            off += 1
            continue
        mutated = mutated.replace(old, new, 1)
        applied += 1
    if applied != len(edits) or mutated == SOURCE:
        print(f"MUTATION={mutation} NOT_APPLIED")
        off += 1
        continue
    killed = set()
    rows = []
    for label, root, name in CASES:
        code, reason = run(mutated, root / name)
        if code == 0:
            killed.add(label)
            rows.append(f"{label}=KILLED")
        elif code == 3:
            rows.append(f"{label}=SURVIVES")
        else:
            rows.append(f"{label}=ANOMALY_rc{code}")
            off += 1
    ok = killed == EXPECTED_KILLS[mutation]
    if not ok:
        off += 1
    print(f"MUTATION={mutation}")
    print(f"  EXPECTED_KILLS={sorted(EXPECTED_KILLS[mutation])} OBSERVED_KILLS={sorted(killed)} "
          f"{'OK' if ok else 'OFF_EXPECTATION'}")
    print("  " + " ".join(rows))
print(f"MUTATIONS={len(MUTATIONS)} REDS={len(CASES)} CELLS={len(MUTATIONS)*len(CASES)} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$mutants | python -B - $tool $r5 $r6
"MUTATION_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
BASELINE unmutated round-6 code on disk
  BASELINE RED=glob             rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=bracket          rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=brace            rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=tilde            rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_command_word
  BASELINE RED=relative         rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
  BASELINE RED=param            rc=3 STOP R4=derived_graph_not_traversable,source_graph_dynamic_command_not_modeled
  BASELINE RED=substitution     rc=3 STOP R4=derived_graph_not_traversable,source_graph_nested_execution_not_modeled
  BASELINE RED=named_fd         rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
  BASELINE RED=indexed_assign   rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
  BASELINE RED=unmodeled_prefix rc=3 STOP R4=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  BASELINE RED=function_body    rc=3 STOP R4=derived_graph_not_traversable,source_graph_command_word_not_modeled
MUTATION=M1_expansion_fence_deleted
  EXPECTED_KILLS=['brace', 'bracket', 'glob'] OBSERVED_KILLS=['brace', 'bracket', 'glob'] OK
  glob=KILLED bracket=KILLED brace=KILLED tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M2_basename_absolute_only
  EXPECTED_KILLS=['relative'] OBSERVED_KILLS=['relative'] OK
  glob=SURVIVES bracket=SURVIVES brace=SURVIVES tilde=SURVIVES relative=KILLED param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M3_unmodeled_reason_deleted
  EXPECTED_KILLS=['brace', 'bracket', 'glob', 'tilde'] OBSERVED_KILLS=['brace', 'bracket', 'glob', 'tilde'] OK
  glob=KILLED bracket=KILLED brace=KILLED tilde=KILLED relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M4_round5_classifier_restored
  EXPECTED_KILLS=['brace', 'bracket', 'glob', 'relative', 'tilde'] OBSERVED_KILLS=['brace', 'bracket', 'glob', 'relative', 'tilde'] OK
  glob=KILLED bracket=KILLED brace=KILLED tilde=KILLED relative=KILLED param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M5_expansion_class_narrowed
  EXPECTED_KILLS=['brace', 'bracket'] OBSERVED_KILLS=['brace', 'bracket'] OK
  glob=SURVIVES bracket=KILLED brace=KILLED tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
MUTATION=M6_substitution_fence_deleted
  EXPECTED_KILLS=[] OBSERVED_KILLS=[] OK
  glob=SURVIVES bracket=SURVIVES brace=SURVIVES tilde=SURVIVES relative=SURVIVES param=SURVIVES substitution=SURVIVES named_fd=SURVIVES indexed_assign=SURVIVES unmodeled_prefix=SURVIVES function_body=SURVIVES
```

```text
MUTATIONS=6 REDS=11 CELLS=66 OFF_EXPECTATION=0
MUTATION_BLOCK_RC=0
```

Command rc: `0`. Reading the matrix honestly:

* **M1** removes the expansion fence and kills glob, bracket and brace. `tilde` survives it,
  because the round-6 basename change independently recognises `~/bin/bash` as an interpreter —
  two round-6 mechanisms overlap on that form, and the matrix shows it rather than implying a
  one-to-one mapping.
* **M2** restores absolute-only basename recognition and kills only `relative`, which is what
  makes that fixture a discriminator for a mechanism the audit did not name.
* **M3** classifies expansion words correctly but stops reporting them, and kills all four
  expansion REDs — the reporting branch is load-bearing, not decoration.
* **M4** reverts both round-6 classifier changes together and kills all five new REDs.
* **M5** narrows the expansion character class to `*?` only and kills exactly bracket and brace,
  so each metacharacter family is separately load-bearing.
* **M6 kills nothing, and that is published as a redundancy, not a pass.** The substitution fence
  is genuinely redundant: `${SHELL_BIN}` is also caught by the brace characters, `$(…)` by
  `_graph_opaque_reason`. It is kept because relying on one fence per class is what produced
  four rounds of reopenings.

## 6. Command-word grammar battery — 59 declared forms and a 180-variant closure sweep

The fixtures prove the defect existed. This battery bounds the policy. The table asserts the
class of 59 hand-chosen forms; the sweep then asserts the **closure property** the policy is
supposed to have: no word carrying an expansion or substitution character is admitted as a
`leaf` or promoted to a `graph` word, in any position, over any base — including bases that are
themselves recognised interpreters.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$battery=@'
import pathlib, sys, types
TOOL = pathlib.Path(sys.argv[1])
module = types.ModuleType("cpp_battery")
module.__file__ = str(TOOL)
sys.modules["cpp_battery"] = module
exec(compile(TOOL.read_text(encoding="utf-8"), str(TOOL), "exec"), module.__dict__)
classify = module._command_word_class
# (raw command word, expected class, why)
TABLE = [
    ("source",             "graph",      "modelled source builtin"),
    (".",                  "graph",      "modelled source builtin"),
    ("bash",               "graph",      "recognised interpreter"),
    ("/usr/bin/bash",      "graph",      "absolute interpreter path"),
    ("bin/bash",           "graph",      "relative interpreter path, round-6 basename"),
    ("./bash",             "graph",      "dot-relative interpreter path, round-6 basename"),
    ("python3.11",         "graph",      "versioned interpreter"),
    ("/opt/py/python3",    "graph",      "absolute versioned interpreter"),
    ("zsh",                "graph",      "recognised, deliberately outside the edge grammar"),
    ("\"bash\"",           "graph",      "quoted interpreter is still proven static"),
    ("'source'",           "graph",      "quoted source builtin is still proven static"),
    ("env",                "wrapper",    "runs a command from its own operands"),
    ("bin/env",            "wrapper",    "relative wrapper path, round-6 basename"),
    ("xargs",              "wrapper",    "runs a command from its own operands"),
    ("eval",               "wrapper",    "runs a command from its own operands"),
    ("cat",                "leaf",       "proven-static non-interpreter"),
    ("/bin/cat",           "leaf",       "proven-static absolute non-interpreter"),
    ("bin/verify_marker",  "leaf",       "proven-static relative non-interpreter"),
    ("_helper",            "leaf",       "proven-static non-interpreter"),
    ("-f",                 "leaf",       "operand of a reserved word, not an expansion"),
    ("\"if\"",             "leaf",       "quoted reserved word is an ordinary command name"),
    ("2a=b",               "leaf",       "not an assignment word: a command name"),
    ("--opt=val",          "leaf",       "not an assignment word: a command name"),
    ("a-b=c",              "leaf",       "not an assignment word: a command name"),
    ("if",                 "control",    "reserved word"),
    ("then",               "control",    "reserved word"),
    ("fi",                 "control",    "reserved word"),
    ("while",              "control",    "reserved word"),
    ("{",                  "control",    "group open, matched before the expansion fence"),
    ("}",                  "control",    "group close, matched before the expansion fence"),
    ("[[",                 "control",    "conditional open, matched before the expansion fence"),
    ("]]",                 "control",    "conditional close, matched before the expansion fence"),
    ("!",                  "control",    "reserved word"),
    ("function",           "control",    "reserved word that binds a name"),
    ("coproc",             "control",    "reserved word that binds a name"),
    ("A=1",                "assignment", "scalar assignment prefix"),
    ("A+=1",               "assignment", "append assignment prefix"),
    ("SEEN[0]=1",          "assignment", "indexed assignment prefix"),
    ("SEEN[0]+=1",         "assignment", "indexed append assignment prefix"),
    ("$FOO",               "dynamic",    "parameter expansion"),
    ("${FOO}",             "dynamic",    "braced parameter expansion"),
    ("x$FOO",              "dynamic",    "embedded parameter expansion"),
    ("$(",                 "dynamic",    "command substitution"),
    ("`cmd`",              "dynamic",    "backtick command substitution"),
    ("$((1+1))",           "dynamic",    "arithmetic expansion"),
    ("ba*h",               "unmodeled",  "pathname expansion"),
    ("/usr/bin/ba*h",      "unmodeled",  "pathname expansion over an absolute path"),
    ("pytho?",             "unmodeled",  "single-character pathname expansion"),
    ("[b]ash",             "unmodeled",  "bracket-expression pathname expansion"),
    ("{ba,z}sh",           "unmodeled",  "brace expansion"),
    ("~/bin/bash",         "unmodeled",  "tilde expansion"),
    ("~",                  "unmodeled",  "tilde expansion"),
    ("\\bash",             "unmodeled",  "backslash-constructed name"),
    ("\\cat",              "unmodeled",  "backslash-constructed name, DISCLOSED conservative stop"),
    ("[",                  "unmodeled",  "test builtin, DISCLOSED conservative stop"),
    ("]",                  "unmodeled",  "test terminator, DISCLOSED conservative stop"),
    ("~/bin/verify_marker","unmodeled",  "benign tilde tool, DISCLOSED conservative stop"),
    ("''",                 "unmodeled",  "degenerate quoting: names nothing adjudicable"),
    ("dir/",               "unmodeled",  "empty basename: names nothing adjudicable"),
]
off = 0
for raw, expected, why in TABLE:
    actual = classify(raw)
    ok = actual == expected
    off += not ok
    print(f"WORD={raw!r:24s} EXPECT={expected:11s} ACTUAL={actual:11s} "
          f"{'OK' if ok else 'OFF_EXPECTATION'}  # {why}")
# Generative closure sweep: no word carrying an expansion or substitution character may be
# admitted as a benign leaf or promoted to a modelled graph word, in any position, over any
# base - including bases that are themselves recognised interpreters.
SPECIALS = ["*", "?", "[", "]", "{", "}", "~", "\\", "$", "`"]
BASES = ["cat", "bash", "source", "/bin/cat", "/usr/bin/bash", "bin/bash"]
sweep = 0
leaked = []
for base in BASES:
    for character in SPECIALS:
        for label, word in (("prefix", character + base),
                            ("suffix", base + character),
                            ("middle", base[:1] + character + base[1:])):
            sweep += 1
            actual = classify(word)
            if actual not in {"dynamic", "unmodeled"}:
                leaked.append((word, label, actual))
off += len(leaked)
for word, label, actual in leaked:
    print(f"SWEEP_LEAK WORD={word!r} POSITION={label} CLASS={actual}")
print(f"TABLE_FORMS={len(TABLE)} SWEEP_FORMS={sweep} SWEEP_LEAKS={len(leaked)} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$battery | python -B - $tool
"BATTERY_BLOCK_RC=$LASTEXITCODE"
```

Real output (final four lines quoted; the 59 per-form lines all end `OK` and are reproduced by
the command):

```text
TABLE_FORMS=59 SWEEP_FORMS=180 SWEEP_LEAKS=0 OFF_EXPECTATION=0
BATTERY_BLOCK_RC=0
```

The four entries labelled `DISCLOSED conservative stop` are the price of the closed policy and
are carried as residual 28, not presented as detections.

## 7. Carried batteries and discriminators

### 7a. The round-5 prefix battery, re-run under round-6 code

All 16 blind forms must still STOP and the benign controls must still pass. **One round-5
control moved**, and it is declared in the script rather than dropped: `SEEN[0] "$ROOT/in.txt"`
was a published `rc 0` control in round 5 and is a `rc 3` disclosed conservative stop now,
because `SEEN[0]` is a bracket-expression pathname-expansion token in command position.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$carried=@'
import json, pathlib, subprocess, sys, tempfile
TOOL = pathlib.Path(sys.argv[1]).resolve()
# The round-5 battery, re-run under round-6 code.  Every form keeps the round-5
# expectation except the one declared MOVED below.
BLIND = [
    ("named_fd_out",            '{fd}>/dev/null source "$LIBRARY_PATH"', 3),
    ("named_fd_in",             '{fd}</dev/null source "$LIBRARY_PATH"', 3),
    ("named_fd_append",         '{fd}>>/safe/fixture/out.log source "$LIBRARY_PATH"', 3),
    ("named_fd_dup",            '{fd}>&2 source "$LIBRARY_PATH"', 3),
    ("named_fd_bash",           '{fd}>/dev/null bash /safe/fixture/library.sh', 3),
    ("named_fd_after_scalar",   'LC_ALL=C {fd}>/dev/null source "$LIBRARY_PATH"', 3),
    ("indexed_assign",          'SEEN[0]=1 source "$LIBRARY_PATH"', 3),
    ("indexed_append",          'SEEN[0]+=1 source "$LIBRARY_PATH"', 3),
    ("indexed_quoted_sub",      'SEEN["a b"]=1 source "$LIBRARY_PATH"', 3),
    ("indexed_assign_bash",     'SEEN[0]=1 bash /safe/fixture/library.sh', 3),
    ("indexed_then_scalar",     'SEEN[0]=1 LC_ALL=C source "$LIBRARY_PATH"', 3),
    ("nested_subscript",        'SEEN[IDX[0]]=1 source "$LIBRARY_PATH"', 3),
    ("function_body_source",    'function reload { source "$LIBRARY_PATH"; }', 3),
    ("function_body_bash",      'function run { bash /safe/fixture/library.sh; }', 3),
    ("coproc_named_body",       'coproc logger { source "$LIBRARY_PATH"; }', 3),
    ("every_prefix_at_once",    'LC_ALL=C {fd}>/dev/null SEEN[0]=1 source "$LIBRARY_PATH"', 3),
]
CONTROLS = [
    ("operand_named_bash",      'echo bash', 0),
    ("word_containing_bash",    'cat "$ROOT/notes.bash"', 0),
    ("numeric_fd_redirection",  'cat "$ROOT/in.txt" 2> /safe/fixture/err.log', 0),
    ("leaf_with_dot_in_path",   'cat /safe/fixture/a.sh.b', 0),
    ("comment_mentions_source", '# source /safe/fixture/library.sh', 0),
    ("indexed_assign_leaf",     'SEEN[0]=1 cat "$ROOT/in.txt"', 0),
    ("named_fd_leaf",           '{fd}>/dev/null cat "$ROOT/in.txt"', 0),
    ("word_abutting_redirect",  'cat>/safe/fixture/out.log', 0),
]
# Declared in advance: forms whose round-5 disposition CHANGES under the round-6
# closed command-word policy, and the round-5 false stop that is carried unchanged.
DISCLOSED_STOPS = [
    ("subscript_word_no_equal", 'SEEN[0] "$ROOT/in.txt"', 3,
     "MOVED: round-5 control rc 0 -> round-6 disclosed conservative stop; SEEN[0] is a "
     "bracket-expression pathname-expansion token in command position"),
    ("brace_non_name_fd",       '{1}>/dev/null cat "$ROOT/in.txt"', 3,
     "CARRIED: round-5 disclosed false stop, unchanged"),
]
def build(root, name, body):
    template = ("#!/usr/bin/env bash\nROOT='{{REMOTE_BASE}}'\nRUNID='{{RUNID}}'\n"
                f"{body}\n" 'cat "$ROOT/$RUNID/input.txt"\n').encode()
    rendered = (template.replace(b"{{REMOTE_BASE}}", b"/safe/fixture")
                        .replace(b"{{RUNID}}", b"WPI-FIXTURE-FREEZE"))
    (root / f"{name}.sh.in").write_bytes(template)
    (root / f"{name}.sh").write_bytes(rendered)
    plan = {"schema": "sec102-composite-plan-v1", "stage": "render", "composites": [{
        "id": "grammar", "entrypoint": "entry",
        "members": [{"id": "entry", "kind": "shell", "path": f"{name}.sh",
                     "deploy_path": "/safe/fixture/entry.sh"}],
        "edges": [],
        "allocation_requirements": [
            {"name": "REMOTE_BASE", "kind": "absolute_path", "consumers": ["entry"]},
            {"name": "RUNID", "kind": "safe_component", "consumers": ["entry"]}],
        "allocations": [{"name": "REMOTE_BASE", "value": "/safe/fixture"},
                        {"name": "RUNID", "value": "WPI-FIXTURE-FREEZE"}],
        "proof": {"render_templates": [{"member": "entry", "template": f"{name}.sh.in"}]}}]}
    path = root / f"{name}.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    return path
def run_new(plan):
    done = subprocess.run([sys.executable, "-B", str(TOOL), "render", str(plan)],
                          capture_output=True, text=True)
    reason = "-"
    for line in done.stdout.splitlines():
        if line.startswith('CLAIM id="R4"'):
            reason = line.split("reason=", 1)[1].strip('"')
    return done.returncode, reason
off = 0
with tempfile.TemporaryDirectory(prefix="sec102-r6-carried-") as tmp:
    root = pathlib.Path(tmp)
    for group, rows in (("BLIND", BLIND), ("CONTROL", CONTROLS)):
        for name, body, want in rows:
            rc, reason = run_new(build(root, name, body))
            ok = rc == want
            off += not ok
            print(f"{group}={name:26s} EXPECT_RC={want} R6_RC={rc} "
                  f"{'OK' if ok else 'OFF_EXPECTATION'} R6_REASON={reason}")
    for name, body, want, note in DISCLOSED_STOPS:
        rc, reason = run_new(build(root, name, body))
        ok = rc == want
        off += not ok
        print(f"DISCLOSED={name:24s} EXPECT_RC={want} R6_RC={rc} "
              f"{'OK' if ok else 'OFF_EXPECTATION'} R6_REASON={reason}")
        print(f"    NOTE {note}")
print(f"BLIND={len(BLIND)} CONTROLS={len(CONTROLS)} DISCLOSED={len(DISCLOSED_STOPS)} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$carried | python -B - $tool
"CARRIED_BATTERY_RC=$LASTEXITCODE"
```

Real output (tail; every per-form line ends `OK`):

```text
DISCLOSED=subscript_word_no_equal  EXPECT_RC=3 R6_RC=3 OK R6_REASON=derived_graph_not_traversable,source_graph_unmodeled_command_word
    NOTE MOVED: round-5 control rc 0 -> round-6 disclosed conservative stop; SEEN[0] is a bracket-expression pathname-expansion token in command position
DISCLOSED=brace_non_name_fd        EXPECT_RC=3 R6_RC=3 OK R6_REASON=derived_graph_not_traversable,source_graph_unmodeled_redirection_prefix
    NOTE CARRIED: round-5 disclosed false stop, unchanged
BLIND=16 CONTROLS=8 DISCLOSED=2 OFF_EXPECTATION=0
CARRIED_BATTERY_RC=0
```

### 7b. The five carried round-3 and round-4 discriminators

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r3=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures').Path
$r4=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures').Path
$carried=@'
import contextlib, io, pathlib, sys
TOOL = pathlib.Path(sys.argv[1]); R3 = pathlib.Path(sys.argv[2]); R4 = pathlib.Path(sys.argv[3])
SOURCE = TOOL.read_text(encoding="utf-8")
DISCRIMINATORS = [
  ("R3F1_basename_fallback_restored", "freeze", R3 / "red_freeze_deploy_identity.json", {
    "    return deploy_to_id.get(identity)":
      "    if identity in deploy_to_id:\n        return deploy_to_id[identity]\n"
      "    fallback = [value for key, value in deploy_to_id.items()\n"
      "                if posixpath.basename(key) == posixpath.basename(operand)]\n"
      "    return fallback[0] if len(fallback) == 1 else None",
    "                target = deploy_to_id.get(_canonical_deployed_path(operand) or \"\")":
      "                target = _member_for_operand(operand, deploy_to_id)"}),
  ("R3F2_allocation_constants_comparisons_disabled", "freeze", R3 / "red_freeze_allocation_constants.json", {
    "        elif binding.value != allocation_values[binding.name]:":
      "        elif False and binding.value != allocation_values[binding.name]:",
    "        elif binding.value != allocation.value:":
      "        elif False and binding.value != allocation.value:",
    "                if constants_operand != operand:":
      "                if False and constants_operand != operand:"}),
  ("R3F3_non_shell_graph_stop_reverted", "render", R3 / "red_render_non_shell_member.json", {
    "            recorder.record(claim_id, Verdict.STOP, \"member_kind_graph_derivation_not_modeled\")\n"
    "            derivation_blocked = True\n            continue": "            continue"}),
  ("R4F1_command_word_conservation_deleted", "render", R4 / "red_render_wrapped_source.json", {
    "            for reason in _graph_word_conservation(text, source_matches, exec_matches):":
      "            for reason in ():"}),
  ("R4F2_absent_allocation_disposition_reverted", "freeze", R4 / "red_freeze_allocation_absent.json", {
    "        elif binding is None:\n            disposition, reason = \"STOP\", \"allocation_absent_from_pinned_constants\"":
      "        elif binding is None:\n            disposition, reason = \"RECONCILED\", \"allocation_and_constants_byte_equal\""}),
]
restored = 0
for name, stage, plan, mutations in DISCRIMINATORS:
    mutated = SOURCE
    for old, new in mutations.items():
        assert mutated.count(old) == 1, (name, old[:50])
        mutated = mutated.replace(old, new)
    buffer = io.StringIO(); argv = sys.argv[:]
    sys.argv = [str(TOOL), stage, str(plan)]
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(mutated, str(TOOL), "exec"), {"__name__": "__main__", "__file__": str(TOOL)})
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = argv
    restored += code == 0
    print(f"MUTATION={name} CASE={plan.name} MUTANT_RC={code} REQUIRED_RED_RC=3 "
          f"{'RED_RESTORED_TO_PASS' if code == 0 else 'DISCRIMINATOR_BROKEN'}")
print(f"CARRIED_DISCRIMINATORS={len(DISCRIMINATORS)} RESTORED_DEFECTIVE_PASS={restored}")
sys.exit(0 if restored == len(DISCRIMINATORS) else 1)
'@
$carried | python -B - $tool $r3 $r4
"CARRIED_DISCRIMINATOR_RC=$LASTEXITCODE"
```

Real output:

```text
MUTATION=R3F1_basename_fallback_restored CASE=red_freeze_deploy_identity.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R3F2_allocation_constants_comparisons_disabled CASE=red_freeze_allocation_constants.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R3F3_non_shell_graph_stop_reverted CASE=red_render_non_shell_member.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R4F1_command_word_conservation_deleted CASE=red_render_wrapped_source.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
MUTATION=R4F2_absent_allocation_disposition_reverted CASE=red_freeze_allocation_absent.json MUTANT_RC=0 REQUIRED_RED_RC=3 RED_RESTORED_TO_PASS
CARRIED_DISCRIMINATORS=5 RESTORED_DEFECTIVE_PASS=5
CARRIED_DISCRIMINATOR_RC=0
```

Command rc: `0`. All five still restore their defective PASS.

### 7c. Three round-5 discriminators stopped discriminating — measured, not asserted

Re-running round 5's own mutation block verbatim under round-6 code, `M1`, `M2` and `M3` no
longer return their round-5 REDs to PASS. This is not a lost guard: the round-6 command-word
fence catches `{fd}`, `SEEN[0]=1` and `SEEN[IDX[0]]=1` independently once the round-5 prefix
model is removed, because all three carry brace or bracket characters. The block below measures
what each round-5 fence still uniquely carries, using a **benign control** — the round-5 model is
what keeps those forms out of a false STOP.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r5=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures').Path
$redundancy=@'
import contextlib, io, json, pathlib, re, sys, tempfile
TOOL = pathlib.Path(sys.argv[1]); FX = pathlib.Path(sys.argv[2])
SOURCE = TOOL.read_text(encoding="utf-8")
REDIRECTION_MODEL = (
    '    if NUMERIC_FD_PREFIX_RE.fullmatch(raw) or NAMED_FD_PREFIX_RE.fullmatch(raw):\n'
    '        return "file_descriptor"\n'
    '    if raw.startswith("{"):\n'
    '        return "unmodeled"\n'
    '    return "word"\n')
REDIRECTION_ROUND4 = (
    '    if NUMERIC_FD_PREFIX_RE.fullmatch(raw):\n'
    '        return "file_descriptor"\n'
    '    return "word"\n')
ASSIGN_RE_R5 = 'SHELL_ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\\[[^][]*\\])?\\+?=")'
ASSIGN_RE_R4 = 'SHELL_ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\\+?=")'
UNMODELED_FENCE = ('    if SHELL_SUBSCRIPT_PREFIX_RE.match(raw) and "=" in raw:\n'
                   '        return "unmodeled"\n')
NAME_BINDING = '        if name_binding_pending and word_class == "leaf":'
# (round-5 mutation, edits, RED probed, expected RED rc under round-6, expected reason
#  fragment, benign control probed, expected control rc, what the round-5 fence still carries)
PROBES = [
 ("M1_redirection_prefix_numeric_only", [(REDIRECTION_MODEL, REDIRECTION_ROUND4)],
  "red_render_named_fd_source.json", 3, "source_graph_unmodeled_command_word",
  ("named_fd_leaf", '{fd}>/dev/null cat "$ROOT/in.txt"'), 3,
  "soundness now redundant; the round-5 model still carries PRECISION for the benign control"),
 ("M2_assignment_prefix_round4_restored", [(ASSIGN_RE_R5, ASSIGN_RE_R4), (UNMODELED_FENCE, "")],
  "red_render_indexed_assign_source.json", 3, "source_graph_unmodeled_command_word",
  ("indexed_assign_leaf", 'SEEN[0]=1 cat "$ROOT/in.txt"'), 3,
  "soundness now redundant; the round-5 model still carries PRECISION for the benign control"),
 ("M3_unmodeled_prefix_fence_deleted", [(UNMODELED_FENCE, "")],
  "red_render_unmodeled_prefix.json", 3, "source_graph_unmodeled_command_word",
  ("indexed_assign_leaf", 'SEEN[0]=1 cat "$ROOT/in.txt"'), 0,
  "soundness now redundant; contributes the precise prefix reason, not the STOP itself"),
 ("M4_name_binding_conservation_deleted",
  [(NAME_BINDING, '        if False and name_binding_pending and word_class == "leaf":')],
  "red_render_function_body_source.json", 0, "-",
  ("indexed_assign_leaf", 'SEEN[0]=1 cat "$ROOT/in.txt"'), 0,
  "STILL SOLELY LOAD-BEARING: a bound name carries no expansion character, so no other fence sees it"),
 ("M5_assignment_model_narrowed_fence_kept", [(ASSIGN_RE_R5, ASSIGN_RE_R4)],
  "red_render_indexed_assign_source.json", 3, "source_graph_unmodeled_assignment_prefix",
  ("indexed_assign_leaf", 'SEEN[0]=1 cat "$ROOT/in.txt"'), 3,
  "kills nothing, as in round 5; still carries PRECISION for the benign control"),
]
R4RE = re.compile(r'^CLAIM id="R4".*reason="([^"]*)"', re.MULTILINE)
def run(source, stage, plan):
    buffer = io.StringIO(); argv = sys.argv[:]
    sys.argv = [str(TOOL), stage, str(plan)]
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(source, str(TOOL), "exec"), {"__name__": "__main__", "__file__": str(TOOL)})
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = argv
    found = R4RE.search(buffer.getvalue())
    return code, (found.group(1) if found else "-")
def build(root, name, body):
    template = ("#!/usr/bin/env bash\nROOT='{{REMOTE_BASE}}'\nRUNID='{{RUNID}}'\n"
                f"{body}\n" 'cat "$ROOT/$RUNID/input.txt"\n').encode()
    rendered = (template.replace(b"{{REMOTE_BASE}}", b"/safe/fixture")
                        .replace(b"{{RUNID}}", b"WPI-FIXTURE-FREEZE"))
    (root / f"{name}.sh.in").write_bytes(template)
    (root / f"{name}.sh").write_bytes(rendered)
    plan = {"schema": "sec102-composite-plan-v1", "stage": "render", "composites": [{
        "id": "grammar", "entrypoint": "entry",
        "members": [{"id": "entry", "kind": "shell", "path": f"{name}.sh",
                     "deploy_path": "/safe/fixture/entry.sh"}],
        "edges": [],
        "allocation_requirements": [
            {"name": "REMOTE_BASE", "kind": "absolute_path", "consumers": ["entry"]},
            {"name": "RUNID", "kind": "safe_component", "consumers": ["entry"]}],
        "allocations": [{"name": "REMOTE_BASE", "value": "/safe/fixture"},
                        {"name": "RUNID", "value": "WPI-FIXTURE-FREEZE"}],
        "proof": {"render_templates": [{"member": "entry", "template": f"{name}.sh.in"}]}}]}
    path = root / f"{name}.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    return path
off = 0
with tempfile.TemporaryDirectory(prefix="sec102-r6-redundancy-") as tmp:
    root = pathlib.Path(tmp)
    for name, edits, red, want_rc, want_reason, control, want_control_rc, note in PROBES:
        mutated = SOURCE
        for old, new in edits:
            assert mutated.count(old) == 1, (name, old[:48])
            mutated = mutated.replace(old, new, 1)
        rc, reason = run(mutated, "render", FX / red)
        control_plan = build(root, control[0], control[1])
        control_rc, _ = run(mutated, "render", control_plan)
        ok = rc == want_rc and (want_reason == "-" or want_reason in reason) and control_rc == want_control_rc
        off += not ok
        print(f"R5_MUTATION={name}")
        print(f"  RED={red} EXPECT_RC={want_rc} RC={rc} REASON={reason}")
        print(f"  CONTROL={control[0]} EXPECT_RC={want_control_rc} RC={control_rc} "
              f"{'(flipped by the mutation)' if want_control_rc == 3 else '(unchanged)'}")
        print(f"  ROLE_UNDER_ROUND6={note}")
        print(f"  {'OK' if ok else 'OFF_EXPECTATION'}")
print(f"ROUND5_FENCES_PROBED={len(PROBES)} OFF_EXPECTATION={off}")
sys.exit(0 if off == 0 else 1)
'@
$redundancy | python -B - $tool $r5
"REDUNDANCY_BLOCK_RC=$LASTEXITCODE"
```

Real output:

```text
R5_MUTATION=M1_redirection_prefix_numeric_only
  RED=red_render_named_fd_source.json EXPECT_RC=3 RC=3 REASON=derived_graph_not_traversable,source_graph_unmodeled_command_word
  CONTROL=named_fd_leaf EXPECT_RC=3 RC=3 (flipped by the mutation)
  ROLE_UNDER_ROUND6=soundness now redundant; the round-5 model still carries PRECISION for the benign control
  OK
R5_MUTATION=M2_assignment_prefix_round4_restored
  RED=red_render_indexed_assign_source.json EXPECT_RC=3 RC=3 REASON=derived_graph_not_traversable,source_graph_unmodeled_command_word
  CONTROL=indexed_assign_leaf EXPECT_RC=3 RC=3 (flipped by the mutation)
  ROLE_UNDER_ROUND6=soundness now redundant; the round-5 model still carries PRECISION for the benign control
  OK
R5_MUTATION=M3_unmodeled_prefix_fence_deleted
  RED=red_render_unmodeled_prefix.json EXPECT_RC=3 RC=3 REASON=derived_graph_not_traversable,source_graph_unmodeled_command_word
  CONTROL=indexed_assign_leaf EXPECT_RC=0 RC=0 (unchanged)
  ROLE_UNDER_ROUND6=soundness now redundant; contributes the precise prefix reason, not the STOP itself
  OK
R5_MUTATION=M4_name_binding_conservation_deleted
  RED=red_render_function_body_source.json EXPECT_RC=0 RC=0 REASON=rendered_bytes_derive_the_declared_reachable_graph
  CONTROL=indexed_assign_leaf EXPECT_RC=0 RC=0 (unchanged)
  ROLE_UNDER_ROUND6=STILL SOLELY LOAD-BEARING: a bound name carries no expansion character, so no other fence sees it
  OK
R5_MUTATION=M5_assignment_model_narrowed_fence_kept
  RED=red_render_indexed_assign_source.json EXPECT_RC=3 RC=3 REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  CONTROL=indexed_assign_leaf EXPECT_RC=3 RC=3 (flipped by the mutation)
  ROLE_UNDER_ROUND6=kills nothing, as in round 5; still carries PRECISION for the benign control
  OK
ROUND5_FENCES_PROBED=5 OFF_EXPECTATION=0
REDUNDANCY_BLOCK_RC=0
```

Command rc: `0`. The consequence is recorded as residual 31: the four round-5 REDs no longer test
exactly one mechanism each.

## 8. Hygiene, determinism and carried GREEN byte identity

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$old='e3906cec:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$r1='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r6='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r6_fixtures'
$greens=@(
  @('allocate',(Join-Path $r1 'green.json')),
  @('render',  (Join-Path $r2 'green_render.json')),
  @('freeze',  (Join-Path $r2 'green_freeze.json')),
  @('freeze',  (Join-Path $r2 'green_freeze_network.json'))
)
$driver=@'
import pathlib, subprocess, sys
tool = pathlib.Path(sys.argv[1])
source = subprocess.run(["git", "show", sys.argv[2]], capture_output=True, text=True,
                        check=True, encoding="utf-8").stdout
sys.argv = [str(tool), sys.argv[3], sys.argv[4]]
exec(compile(source, str(tool), "exec"), {"__name__": "__main__", "__file__": str(tool)})
'@
$driver | Out-File -FilePath "$env:TEMP\sec102_r6_old_driver.py" -Encoding utf8
function Get-Sha([string]$text){
  [BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes($text))).Replace('-','').ToLower()
}
$diff=0
foreach($g in $greens){
  $new=(& python -B $tool $g[0] $g[1]) -join "`n"
  $prev=(& python -B "$env:TEMP\sec102_r6_old_driver.py" (Resolve-Path $tool).Path $old $g[0] $g[1]) -join "`n"
  $hn=Get-Sha $new; $ho=Get-Sha $prev
  if($hn -ne $ho){$diff++}
  "GREEN=$(Split-Path $g[1] -Leaf) STAGE=$($g[0]) e3906cec_SHA256=$ho R6_SHA256=$hn IDENTICAL=$($hn -eq $ho)"
}
"CARRIED_GREEN_TRANSCRIPTS=$($greens.Count) DIFFERING=$diff"
$det=0
foreach($n in @('red_render_glob_command_word.json','red_render_tilde_command_word.json','green_render_static_leaf.json')){
  $h=@(); 1..3 | ForEach-Object { $h += Get-Sha ((& python -B $tool render (Join-Path $r6 $n)) -join "`n") }
  $u=($h | Select-Object -Unique).Count
  if($u -ne 1){$det++}
  "DETERMINISM=$n RUNS=3 UNIQUE_TRANSCRIPTS=$u SHA256=$($h[0]) STABLE=$($u -eq 1)"
}
"DETERMINISM_UNSTABLE=$det"
Remove-Item "$env:TEMP\sec102_r6_old_driver.py"
if($diff -or $det){exit 1}else{exit 0}
```

Real output:

```text
GREEN=green.json STAGE=allocate e3906cec_SHA256=c8357e393220669e9fe6de2054973a59b140900f54cb49dc26bf2269a92d45de R6_SHA256=c8357e393220669e9fe6de2054973a59b140900f54cb49dc26bf2269a92d45de IDENTICAL=True
GREEN=green_render.json STAGE=render e3906cec_SHA256=d86819ab525c1a4842c4688123be5575292c7aab2cbaf962256eee957a3e2c24 R6_SHA256=d86819ab525c1a4842c4688123be5575292c7aab2cbaf962256eee957a3e2c24 IDENTICAL=True
GREEN=green_freeze.json STAGE=freeze e3906cec_SHA256=1c35df7442dd3abc87f3c1594d6d5298feed22ce45a818956318fcbd97776b2a R6_SHA256=1c35df7442dd3abc87f3c1594d6d5298feed22ce45a818956318fcbd97776b2a IDENTICAL=True
GREEN=green_freeze_network.json STAGE=freeze e3906cec_SHA256=0841ad58191a1f2175d9fef5259b9bb67a79ce24797302f1c20d0dd63f4d3486 R6_SHA256=0841ad58191a1f2175d9fef5259b9bb67a79ce24797302f1c20d0dd63f4d3486 IDENTICAL=True
CARRIED_GREEN_TRANSCRIPTS=4 DIFFERING=0
DETERMINISM=red_render_glob_command_word.json RUNS=3 UNIQUE_TRANSCRIPTS=1 SHA256=d3418fd14ad5c09b4ca01200e4d6b66f105bf61613c9364fe37331cf72e39ded STABLE=True
DETERMINISM=red_render_tilde_command_word.json RUNS=3 UNIQUE_TRANSCRIPTS=1 SHA256=74e36f434e295966b0a44f9022d85c76121891c5ddcfee707ffdf8dfa1adda65 STABLE=True
DETERMINISM=green_render_static_leaf.json RUNS=3 UNIQUE_TRANSCRIPTS=1 SHA256=4729dd51f8866b5ccd12562a9ac7ca1d88fad780bd53ae9e0ce753be4492dca1 STABLE=True
DETERMINISM_UNSTABLE=0
```

Command rc: `0`. The four carried GREEN transcripts are byte-identical to the audited commit.

The fixture and attribute hygiene block, including the check that every rendered `.sh` equals its
own `.in` with the fixture allocations substituted — so a hand-typo in a fixture cannot silently
disagree with what RENDER proves:

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$hygiene=@'
import ast, json, pathlib, sys
CR = bytes([13])
D = pathlib.Path("MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1")
bad = 0
tool = D / "composite_pathproof.py"
raw = tool.read_bytes()
try:
    ast.parse(raw.decode("utf-8"), filename=str(tool))
    print("AST_PARSE=composite_pathproof.py OK")
except SyntaxError as exc:
    bad += 1
    print(f"AST_PARSE=composite_pathproof.py FAILED {exc}")
tool_cr = raw.count(CR)
bad += tool_cr
print(f"TOOL_CR_BYTES={tool_cr} TOOL_LF_ONLY={tool_cr == 0}")
fixtures = sorted((D / "sec102_r6_fixtures").iterdir())
plans = [p for p in fixtures if p.suffix == ".json"]
parsed = 0
for plan in plans:
    try:
        json.loads(plan.read_text(encoding="utf-8"))
        parsed += 1
    except Exception as exc:
        bad += 1
        print(f"JSON_PARSE={plan.name} FAILED {exc}")
print(f"R6_JSON_PLANS={len(plans)} PARSED={parsed}")
with_cr = [p.name for p in fixtures if CR in p.read_bytes()]
bad += len(with_cr)
print(f"R6_FIXTURE_FILES={len(fixtures)} FILES_WITH_CR={with_cr}")
# Every rendered .sh must equal its .in with the fixture allocations substituted, so a
# hand-edited fixture cannot silently disagree with what RENDER proves.
ALLOC = {b"{{REMOTE_BASE}}": b"/safe/fixture", b"{{RUNID}}": b"WPI-FIXTURE-FREEZE",
         b"{{LIBRARY_PATH}}": b"/safe/fixture/library.sh"}
pairs = 0
for template in [p for p in fixtures if p.name.endswith(".sh.in")]:
    expected = template.read_bytes()
    for token, value in ALLOC.items():
        expected = expected.replace(token, value)
    actual = template.with_suffix("").read_bytes()
    pairs += 1
    if expected != actual:
        bad += 1
        print(f"RENDER_PAIR={template.name} MISMATCH")
print(f"R6_TEMPLATE_RENDER_PAIRS={pairs} MISMATCHED=0" if bad == 0 else f"R6_TEMPLATE_RENDER_PAIRS={pairs}")
attrs = (D / ".gitattributes").read_text(encoding="utf-8")
has_rule = "sec102_r6_fixtures/** -text" in attrs
bad += not has_rule
print(f"GITATTRIBUTES_HAS_R6_RULE={has_rule}")
print(f"HYGIENE_DEFECTS={bad}")
sys.exit(0 if bad == 0 else 1)
'@
$hygiene | python -B -
"HYGIENE_RC=$LASTEXITCODE"
```

Real output:

```text
AST_PARSE=composite_pathproof.py OK
TOOL_CR_BYTES=0 TOOL_LF_ONLY=True
R6_JSON_PLANS=8 PARSED=8
R6_FIXTURE_FILES=24 FILES_WITH_CR=[]
R6_TEMPLATE_RENDER_PAIRS=8 MISMATCHED=0
GITATTRIBUTES_HAS_R6_RULE=True
HYGIENE_DEFECTS=0
HYGIENE_RC=0
```

Scope. Only files inside the kickoff's fence were touched; `pathscope_prover.py` and every
round-1..5 fixture tree have no worktree diff:

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$D='MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1'
"PROVER_UNTOUCHED=$((git status --porcelain "$D/pathscope_prover.py").Length -eq 0)"
"CARRIED_FIXTURES_UNTOUCHED=$((git status --porcelain "$D/sec102_r1_fixtures" "$D/sec102_r2_fixtures" "$D/sec102_r3_fixtures" "$D/sec102_r4_fixtures" "$D/sec102_r5_fixtures").Length -eq 0)"
"OUT_OF_SCOPE_TRACKED_MODIFICATIONS:"
git status --porcelain --untracked-files=no | Where-Object { $_ -notmatch 'WPI_PREREG_DRAFT_ROUND1' }
"TRACKED_MODIFICATIONS_IN_SCOPE:"
git status --porcelain --untracked-files=no -- $D
```

Real output (state-dependent — see the note below):

```text
PROVER_UNTOUCHED=True
CARRIED_FIXTURES_UNTOUCHED=True
OUT_OF_SCOPE_TRACKED_MODIFICATIONS:
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md
TRACKED_MODIFICATIONS_IN_SCOPE:
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py
```

The three in-scope modifications plus the new untracked `sec102_r6_fixtures/`,
`SELF_QA_SEC102_R6.md` and `SEC102_R6_REPORT_2026-08-11.md` are the complete round-6 delta.

**The one out-of-scope line is not this lane's.** `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` is owned by
the concurrent RP6 Max lane, which the kickoff explicitly fences off; it was not read, written,
checked out, reset or stashed here. This block is the only state-dependent transcript in this
document, because a shared worktree carries other lanes' work; it is excluded from the
paste-and-run comparison in section 12 for that reason and is not used as closure evidence.

## 9. Artifact identity

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$identity=@'
import hashlib, pathlib
D = pathlib.Path("MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1")
targets = [D / "composite_pathproof.py", D / ".gitattributes"]
targets += sorted((D / "sec102_r6_fixtures").iterdir())
for p in targets:
    raw = p.read_bytes()
    print(f"ARTIFACT {p.as_posix()} bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")
'@
$identity | python -B -
```

Real output:

```text
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py bytes=121837 sha256=14a76dfcf69288aa3fe7ee4ef2c26241fb48a31012a6064b85fcfe0a17d8fa1a
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes bytes=1613 sha256=507837ae736af42ed93772576186af15ba8d83c3f9f85305e144414caa3aa7b2
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_brace_command_word.sh bytes=188 sha256=14b07cd9d232b885cb24131c7aaf62ca4a348c452c5fb2f86b623ef2267252a0
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_brace_command_word.sh.in bytes=165 sha256=f74af7092ce2918e6a7d244196fa88560c72a881d6b1d64a640a79aad7b272d1
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_bracket_command_word.sh bytes=186 sha256=a486c0552cdfcab93cd787625d68adae2e844d1e6ab2ab18f1338dd6f3d4a0c7
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_bracket_command_word.sh.in bytes=163 sha256=06178f0d7cdddec070637a4453dc3fef5268a5d7c27a7722529d55aeb83769fb
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_glob_command_word.sh bytes=184 sha256=22b9c3c68d0b950b24c1fbcad6017236d150e944c44d99eaa0ae9c278da5415e
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_glob_command_word.sh.in bytes=161 sha256=106922ad1d9db6f6cc016575991413c60424337ad167fc9451926c4dfccf045e
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_param_command_word.sh bytes=187 sha256=7e94ae0079ad47f42fc8790f7457d8aade6fc22055573d4e3e13edfa88fb4e52
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_param_command_word.sh.in bytes=164 sha256=f17065a00e5fbffe9d4c07ab312602a736abc177352a2980b545c9c6dd865525
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_relative_interpreter.sh bytes=179 sha256=ba64d796a3aacab27021981e6e135832af540ed1d1d849d2892b1a3aee2c9d82
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_relative_interpreter.sh.in bytes=156 sha256=2fdb8d78c26382aa1f6f820e01557b778bf16f6bbea0b86a34fdb7bf13845f9d
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_static_leaf.sh bytes=168 sha256=2a050f0426b31173112bfcb83657f9c30fc6320f5522f07d2a1cab70ae50988c
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_static_leaf.sh.in bytes=153 sha256=8296712a80d0390b27322feb07a8ee42292b8c9a5fc5ee78266eddefbf4faee7
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_substitution_command_word.sh bytes=185 sha256=7a95e429d6154235e71604d9c584843f2c912bc05581e106771f1caba40b827e
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_substitution_command_word.sh.in bytes=162 sha256=8d11e89859945bc0b098adfa91a7bcf6e2f021c1134a28921358dfc0de57d0d6
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_tilde_command_word.sh bytes=181 sha256=f33d27da1ed3409c6386ef46258536e28cd6404404002a89cc96961eb92aadc4
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_tilde_command_word.sh.in bytes=158 sha256=4b11c4cf3a4bd64c9ad2045127f447a14ada3a79424f933ab1da859089e3b12e
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/green_render_static_leaf.json bytes=1330 sha256=67cd0e2ba32ffb6c7a50e235f6e314399830883bb9f66b302c7994cc6ce2e422
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_brace_command_word.json bytes=1351 sha256=2fc4b96fd3d3afce21d0e2894f6e434b50ab02e3eb08c6fc12f44585be9063f9
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_bracket_command_word.json bytes=1357 sha256=593d1840dfbf6540a082a2cd37f24b7ff9db24f23630fbb4bc457ad328bce7f3
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_glob_command_word.json bytes=1348 sha256=8016282c7870f298fba609e7db1ea7d820f1ab9c376d01639d1c2a58dcc1ced4
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_param_command_word.json bytes=1351 sha256=c4884948fe4507366d80852e3e2bc75998b6ad4f9a64ebdfcd8f6c09cd38fe6f
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_relative_interpreter.json bytes=1357 sha256=b5a0915f6572822ce4f020a2aba84693b0dc9aa2bacf01cbbea8e9e0d6ce1848
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_substitution_command_word.json bytes=1372 sha256=e59ec51d38c2645019c8c503f7424ccd755e94895df45a97dc9316792f812de8
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_tilde_command_word.json bytes=1351 sha256=6231a7cb4b51248013dea769f895f2b75982be7d17d7f3b2f669ec7384149faa
```

`pathscope_prover.py` was not touched and its pin (`122446` B /
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`) is unchanged; the FREEZE
GREEN transcript above is the running proof of it.

The three evidence documents (`SELF_QA_SEC102_R6.md`, `STATUS_SEC102.md`, and
`SEC102_R6_REPORT_2026-08-11.md`) are re-derived by adding them to the `targets` list in the
command above. Their SHA-256 values are deliberately **not** transcribed here: a document cannot
contain its own digest, and a partially self-referential table is exactly what Pattern 10 warns
about. The Lead derives all three at commit time.

## 10. Honest residual scope — what round 6 does NOT close

The full carried list is `STATUS_SEC102.md` items 1–31. The round-6-specific residuals:

1. **The recognised-interpreter VOCABULARY is still a list.** This is the residual the round-5
   audit restated as a production blocker, and round 6 does **not** close it. A proven-static
   literal naming an executable-capable program the list does not contain is still a benign leaf.
   What changed is the residual's *exposure*: a word can only reach the vocabulary test if its
   spelling is already the name Bash will look up, so an unknown name can no longer be smuggled
   in behind an expansion. Narrower is not closed.
2. **The expansion character set is itself a list.** `*?[]{}~\` covers the expansions Bash
   performs on a command word before lookup as the implementer reads the grammar. `extglob`,
   `globstar` and similar option-enabled patterns are built from the same characters and are
   therefore covered by construction, but no proof is offered that the set is complete for every
   shell option. This is a strictly smaller residual than round 5's, not zero.
3. **New conservative false stops, larger than round 5's.** The `[` test builtin, `\cat`,
   `~/bin/mytool`, a subscript word without an `=`, and any command word containing a
   glob/brace/tilde/backslash character now STOP whether or not Bash would expand that
   occurrence. One of these was a published round-5 control at `rc 0` (section 7a).
4. **Quoted occurrences are not excused.** `'*'` is a literal star to Bash but STOPs here.
5. **Three round-5 discriminators became non-discriminating** (section 7c). The round-5 REDs no
   longer test exactly one mechanism each.
6. **Two of the four fixtures the kickoff named are not new REDs** (section 4). Parameter
   expansion and command substitution were already fail-closed at `e3906cec`.
7. Everything outside the command-word boundary is unchanged: FREEZE still accepts only all-shell
   composites, the analysis unit still supports only standalone `source`/`.` edges, the deployed
   identity is still lexical, and no host was contacted.

## 11. Thirteen-pattern self-adjudication

1. **STOP/PASS/FAIL ordering.** STOP outranks FAIL outranks PASS; every new refusal is a STOP
   with a named reason, and the 52-case matrix asserts the exact rc per case.
2. **Host and namespace identity.** Explicit non-claims; nothing here contacts a host.
3. **Host-object, symlink, mount identity.** Explicit non-claims, carried as R1/R2 disclosures.
4. **External interpreter/environment boundary.** Still a disclosed production blocker; the
   interpreter vocabulary residual is restated in section 10 rather than narrowed by wording.
5. **Grammar incompleteness.** This is the pattern round 6 targets. The command-word grammar is
   no longer enumerated; the closure sweep (section 6) is the evidence that the default is now
   refusal. Residual 2 records that the character set is still a reading of the grammar.
6. **Probe status before output adjudication.** Unchanged; the prover adapter still checks
   process status before parsing.
7. **No new incomplete-reader path.** No reader changed.
8. **Deployed identity is lexical.** Unchanged and explicitly scoped.
9. **Claim wording vs predicate.** The round-5 `STATUS` sentence that dynamic command positions
   STOP outran the predicate; it is corrected in `STATUS_SEC102.md` item 12 with the exact list
   of what STOPs and the exact residual that does not.
10. **Declared vs executed evidence.** Every block in this document is literal and was executed;
    section 12 re-executes them from outside the repository. The scope block's output is the one
    state-dependent transcript and is labelled as such.
11. **Instrument defects.** The round-6 changes are in the classifier the evidence measures, so
    section 2 loads both modules independently and section 5 mutates the production source rather
    than trusting it.
12. **Unmodelled behaviour disappearing.** The primary pattern. `leaf` must now be earned; every
    other command-word outcome is a named STOP.
13. **Terminal-disposition conservation.** Unchanged; member, allocation and constant rows still
    each carry exactly one terminal disposition.

## 12. Paste-and-run verification of this document

Every fenced `powershell` block in this file is extracted byte-for-byte, written to a `.ps1`
outside the repository, executed from a working directory outside the repository, and its output
compared with the ```text block published under it. Blocks whose published transcript is a
declared excerpt (sections 6, 7a) are compared on their final summary lines; the scope block is
excluded and labelled, because its transcript depends on unrelated lanes' worktree state.

The harness itself is written outside the repository and is reproduced here in full so the Lead
can re-run it without trusting this document:

```python
#!/usr/bin/env python3
"""Extract every fenced powershell block from SELF_QA_SEC102_R6.md, run it from a working
directory OUTSIDE the repository, and compare its output with the published transcript.

A fence in any language other than `text` ends the current block's transcript association, so
this file's own listing inside the document cannot be mistaken for a published transcript.  The
fence marker is built with chr(96) so this source contains no literal triple backtick and is
therefore safe to publish inside the very document it parses.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tempfile

DOC = pathlib.Path(sys.argv[1])
OUTSIDE = pathlib.Path(sys.argv[2])
text = DOC.read_text(encoding="utf-8")
TICKS = chr(96) * 3
FENCE = re.compile(TICKS + r"([a-z]*)\n(.*?)" + TICKS, re.S)

blocks: list[tuple[str, list[str]]] = []
current: list[str] | None = None
for match in FENCE.finditer(text):
    kind, body = match.group(1), match.group(2)
    if kind == "powershell":
        current = []
        blocks.append((body, current))
    elif kind == "text" and current is not None:
        current.append(body)
    elif kind != "text":
        current = None

EXCLUDED = "OUT_OF_SCOPE_TRACKED_MODIFICATIONS"
mismatched = excluded = compared = 0
for index, (command, published) in enumerate(blocks, 1):
    lines = command.strip().splitlines()
    label = lines[1][:70] if len(lines) > 1 else "?"
    if EXCLUDED in command:
        excluded += 1
        print(f"BLOCK={index:02d} EXCLUDED_STATE_DEPENDENT {label}")
        continue
    if not published:
        print(f"BLOCK={index:02d} NO_PUBLISHED_TRANSCRIPT {label}")
        mismatched += 1
        continue
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8") as handle:
        handle.write(command)
        script = handle.name
    done = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
         "-File", script],
        cwd=str(OUTSIDE), capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    pathlib.Path(script).unlink()
    actual = [line.rstrip() for line in done.stdout.splitlines()]
    want = [line.rstrip() for chunk in published for line in chunk.splitlines()]
    missing = [line for line in want if line not in actual]
    compared += 1
    if missing:
        mismatched += 1
        print(f"BLOCK={index:02d} MISMATCH published_lines={len(want)} missing={len(missing)} {label}")
        for line in missing[:6]:
            print(f"    MISSING: {line}")
    else:
        print(f"BLOCK={index:02d} REPRODUCED published_lines={len(want)} {label}")

print(f"BLOCKS={len(blocks)} COMPARED={compared} EXCLUDED={excluded} MISMATCHED={mismatched}")
sys.exit(0 if mismatched == 0 else 1)
```

Real output, run with the current working directory set to a scratch folder outside
`C:\LAB\Tradingview_LAB_CLEAN`:

```text
BLOCK=01 REPRODUCED published_lines=3 $p='MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pat
BLOCK=02 REPRODUCED published_lines=34 $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=03 REPRODUCED published_lines=53 $tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_
BLOCK=04 REPRODUCED published_lines=34 $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=05 REPRODUCED published_lines=32 $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=06 REPRODUCED published_lines=2 $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=07 REPRODUCED published_lines=6 $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=08 REPRODUCED published_lines=7 $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=09 REPRODUCED published_lines=27 $tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROU
BLOCK=10 REPRODUCED published_lines=9 $tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_
BLOCK=11 REPRODUCED published_lines=8 $hygiene=@'
BLOCK=12 EXCLUDED_STATE_DEPENDENT $D='MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1'
BLOCK=13 REPRODUCED published_lines=26 $identity=@'
BLOCKS=13 COMPARED=12 EXCLUDED=1 MISMATCHED=0
PASTE_RUN_RC=0
```

Every block reproduces. Two published transcripts were **wrong on the first pass and are recorded
as having been wrong**: the section-4 GREEN control's `R6_R4` line and the section-7c `M5` control
line had been transcribed by hand rather than copied from the run. Both were corrected against
the real output before this harness passed. That is the failure mode this harness exists to catch,
so the correction is reported rather than removed.
