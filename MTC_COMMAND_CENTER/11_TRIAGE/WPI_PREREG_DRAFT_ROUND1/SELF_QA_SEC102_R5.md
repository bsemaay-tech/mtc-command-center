# SELF-QA — SEC102 composite path proof, round 5

Implementer: `claude-opus-5` xhigh (Max account). Date: 2026-08-11. Input commit: `bb02c25a`
(byte-identical `composite_pathproof.py` to the audited `28b5c06b` — verified in section 1).
No audit or acceptance is claimed here. No commit was made. No host or network was contacted.
No fixture shell was executed. Every command below is literal, starts with an absolute
`Set-Location`, and is therefore cwd-robust.

## 1. The finding, the repair, and where each piece of evidence lives

Codex round 4 (`SEC102_CODEX_T1_AUDIT_R4_2026-08-11.md`) returned **REQUEST_CHANGES** with one
CRITICAL: `composite_pathproof.py:1279` conserved the command position only for *numeric*
file-descriptor prefixes and only for *scalar* assignment words. A valid named-descriptor
prefix (`{fd}>…`) or indexed assignment prefix (`arr[0]=…`) was emitted as a benign leaf, that
leaf closed the command position, and a `source`/interpreter operand behind it was then
classified by nothing — no edge, no uncovered graph word, RENDER `PASS rc 0` over an
unanalysed program.

| Piece | Where |
|---|---|
| The audited baseline is the same code the kickoff names | section 1, below |
| The defect measured at the scanner boundary, before and after | section 2 |
| Four new REDs: `PASS rc 0` on `bb02c25a` → `STOP rc 3` after the repair | section 4 |
| Independent mutation discriminator per mechanism, 5×4 cell matrix | section 5 |
| 16-form prefix grammar battery + 9 controls + 1 disclosed false stop | section 6 |
| Round-4 grammar battery re-run as a round-5 regression | section 6b |
| The five carried round-3/round-4 discriminators, still discriminating | section 7 |
| 44-case matrix, `FAILED_COUNT=0`, all 40 carried cases unchanged | section 3 |
| Determinism, AST/JSON/LF hygiene, attribute resolution, worktree scope | section 8 |
| Artifact byte counts and SHA-256 | section 9 |
| Honest residual scope | section 10 |

**The baseline is the audited code.** The kickoff names `bb02c25a` as input; Codex audited
`28b5c06b`. Both carry the same module byte-for-byte, so the pre-feature side of every D026
comparison below is the exact code Codex audited:

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$p='MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$audited=(git rev-parse "28b5c06b:$p")
$kickoff=(git rev-parse "bb02c25a:$p")
"BLOB_AT_AUDITED_28b5c06b=$audited"
"BLOB_AT_KICKOFF_INPUT_bb02c25a=$kickoff"
"BASELINE_IS_THE_AUDITED_CODE=$($audited -eq $kickoff)"
```

Real output:

```text
BLOB_AT_AUDITED_28b5c06b=5adf679969c404fc8a64902721ef5419e5f0ec3d
BLOB_AT_KICKOFF_INPUT_bb02c25a=5adf679969c404fc8a64902721ef5419e5f0ec3d
BASELINE_IS_THE_AUDITED_CODE=True
```

### What changed in the code

1. **`SHELL_ASSIGNMENT_RE` now models the whole Bash assignment-word grammar** —
   `NAME=`, `NAME+=`, `NAME[subscript]=`, `NAME[subscript]+=`. Bash requires the NAME to be
   unquoted and to start the word, so `2a=b`, `a-b=c`, `"a"=b` and `--opt=val` are command
   names, not assignments; leaving them as leaves is exact, not an approximation.
2. **`_redirection_prefix_class`** replaces the `raw.isdigit()` test. A word abutting `<`/`>`
   is a file-descriptor prefix only if it is all-ASCII-digits or `{name}` — the only two forms
   Bash accepts. Both conserve the command position. An ordinary word that merely touches the
   operator (`echo>out`) is still a word.
3. **`_assignment_prefix_class`** is the fail-closed fence. A command-position word that opens
   a subscript the model could not close *and* carries an `=` (`arr[idx[0]]=1`) returns
   `source_graph_unmodeled_assignment_prefix` **before** it can become a leaf. A brace word in
   the exact syntactic slot of a named descriptor whose interior is not a plain name (`{1}>…`)
   returns `source_graph_unmodeled_redirection_prefix`.
4. **`SHELL_NAME_BINDING_WORDS = {function, coproc}`** — the word after these reserved words
   binds a name, it does not run. Round 4 let that name close the command position, so
   `function foo { source lib; }` lost the body's first command word by the identical
   mechanism, reached through a reserved word instead of a prefix. This was **not** in the
   round-4 finding; it was found by probing the same boundary and is measured in section 2.
   `for`/`select`/`case` also bind a name, but a separator, newline or `)` always re-opens the
   command position before their body, so nothing is lost there and they are left alone.

Nothing else moved. The four GREEN transcripts are byte-identical to `bb02c25a` (section 8),
so no fence was weakened and no output surface was added.

## 2. The defect measured at the scanner boundary, both sides, one command

This is the direct answer to the audit's method: the module is loaded twice — once from the
worktree, once streamed from `bb02c25a` — and asked what it sees. `SILENT_NO_EDGE` is true
when the module reports **no edge, no uncovered command word and no opaque reason** over
bytes that reach another program: the exact shape of a false RENDER PASS.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$old='bb02c25a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$probe=@'
import importlib.util, pathlib, subprocess, sys, types
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
# (label, rendered bytes, does Bash actually reach another program here?)
CASES = [
    ("named_fd_out",        '{fd}>/dev/null source "$LIB"\n',        True),
    ("named_fd_in",         '{fd}</dev/null source "$LIB"\n',        True),
    ("indexed_assign",      'SEEN[0]=1 source "$LIB"\n',             True),
    ("indexed_append",      'SEEN[0]+=1 source "$LIB"\n',            True),
    ("nested_subscript",    'SEEN[IDX[0]]=1 source "$LIB"\n',        True),
    ("function_body",       'function foo { source "$LIB"; }\n',     True),
    ("coproc_named_body",   'coproc log { source "$LIB"; }\n',       True),
    ("numeric_fd_out",      '2>/dev/null source "$LIB"\n',           True),
    ("scalar_assign",       'A=1 source "$LIB"\n',                   True),
    ("paren_function_body", 'foo() { source "$LIB"; }\n',            True),
    ("for_loop_body",       'for f in a b; do source "$LIB"; done\n', True),
    ("word_then_redirect",  'echo>out source "$LIB"\n',              False),
    ("brace_word_command",  '{fd} source "$LIB"\n',                  False),
    ("subscript_no_equals", 'SEEN[0] hello\n',                       False),
    ("plain_leaf",          'cat "$ROOT/in.txt"\n',                  False),
]
def silent(module, text):
    """True when the module sees no edge, no uncovered word and no opaque reason."""
    if module._graph_opaque_reason(text) is not None:
        return False
    src = list(module.SOURCE_COMMAND_RE.finditer(text))
    exe = list(module.EXEC_COMMAND_RE.finditer(text))
    return not src and not exe and not module._graph_word_conservation(text, src, exe)
bad = 0
for label, text, reaches in CASES:
    before, after = silent(old, text), silent(new, text)
    ok = (not after) if reaches else True
    bad += not ok
    print(f"PROBE={label:20s} BASH_REACHES_ANOTHER_PROGRAM={str(reaches):5s} "
          f"bb02c25a_SILENT_NO_EDGE={str(before):5s} R5_SILENT_NO_EDGE={str(after):5s} "
          f"{'OK' if ok else 'STILL_SILENT'}")
print(f"PROBES={len(CASES)} REACHING_FORMS_STILL_SILENT_UNDER_R5={bad}")
sys.exit(0 if bad == 0 else 1)
'@
$probe | python -B - $tool $old
"PROBE_RC=$LASTEXITCODE"
```

Real output:

```text
PROBE=named_fd_out         BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=False OK
PROBE=named_fd_in          BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=False OK
PROBE=indexed_assign       BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=False OK
PROBE=indexed_append       BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=False OK
PROBE=nested_subscript     BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=False OK
PROBE=function_body        BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=False OK
PROBE=coproc_named_body    BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=False OK
PROBE=numeric_fd_out       BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=False R5_SILENT_NO_EDGE=False OK
PROBE=scalar_assign        BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=False R5_SILENT_NO_EDGE=False OK
PROBE=paren_function_body  BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=False R5_SILENT_NO_EDGE=False OK
PROBE=for_loop_body        BASH_REACHES_ANOTHER_PROGRAM=True  bb02c25a_SILENT_NO_EDGE=False R5_SILENT_NO_EDGE=False OK
PROBE=word_then_redirect   BASH_REACHES_ANOTHER_PROGRAM=False bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=True  OK
PROBE=brace_word_command   BASH_REACHES_ANOTHER_PROGRAM=False bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=True  OK
PROBE=subscript_no_equals  BASH_REACHES_ANOTHER_PROGRAM=False bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=True  OK
PROBE=plain_leaf           BASH_REACHES_ANOTHER_PROGRAM=False bb02c25a_SILENT_NO_EDGE=True  R5_SILENT_NO_EDGE=True  OK
PROBES=15 REACHING_FORMS_STILL_SILENT_UNDER_R5=0
PROBE_RC=0
```

Read the table honestly. Rows 1–7 are the defect: seven forms where Bash reaches another
program and `bb02c25a` was silent. Rows 8–11 confirm the prefixes round 4 *did* conserve are
unaffected. **Rows 6 and 7 are the reserved-word variant the round-4 finding did not name**;
they are the same silent loss and are repaired here. Rows 12–15 are the counter-evidence that
matters most: `echo>out source "$LIB"`, `{fd} source "$LIB"` and `SEEN[0] hello` are all still
`SILENT_NO_EDGE=True` under round-5 code, and that is **correct** — in each of them Bash runs
the first word as the command and `source` is one of its arguments, so no edge exists to lose.
The repair distinguishes prefixes from words; it does not simply STOP on unusual punctuation.

## 3. Literal all-case assertion command — 44 cases

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r1='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
$r4='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures'
$r5='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures'
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
  @('render',$r5,'red_render_function_body_source.json',3,'source_graph_command_word_not_modeled')
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
CASES=44 FAILED_COUNT=0
```

Command rc: `0`. **All 40 round-4 cases are carried with their rc and reason token unchanged**;
four are round-5 additions. No prior fixture file was edited — `git status --porcelain` over
`sec102_r1_fixtures`, `sec102_r2_fixtures`, `sec102_r3_fixtures`, `sec102_r4_fixtures` and
`pathscope_prover.py` is empty (section 8).

## 4. D026 RED before GREEN — behavioural pre-feature falsification

Each new fixture is run twice over **byte-identical plan and member inputs**; only the program
changes. The pre-feature side is the exact `bb02c25a` code streamed from Git — no file is
checked out or overwritten.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r5=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures').Path
$old='bb02c25a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$driver=@'
import pathlib, subprocess, sys
tool = pathlib.Path(sys.argv[1])
source = subprocess.run(["git", "show", sys.argv[2]], capture_output=True, text=True,
                        check=True, encoding="utf-8").stdout
sys.argv = [str(tool), sys.argv[3], sys.argv[4]]
namespace = {"__name__": "__main__", "__file__": str(tool)}
exec(compile(source, str(tool), "exec"), namespace)
'@
foreach($plan in @('red_render_named_fd_source.json','red_render_indexed_assign_source.json','red_render_unmodeled_prefix.json','red_render_function_body_source.json')){
  "D026 FIXTURE=$plan (identical bytes on both sides; only the code differs)"
  "  --- bb02c25a code streamed from git ---"
  $out=($driver | python -B - $tool $old 'render' (Join-Path $r5 $plan))
  $rcBefore=$LASTEXITCODE
  $out | Where-Object { $_ -match '^(CLAIM id="R(4|6|7)"|COMPOSITE_PATHPROOF verdict=)' } | ForEach-Object { "  $_" }
  "  --- round-5 code on disk ---"
  $out=(& python -B $tool 'render' (Join-Path $r5 $plan))
  $rcAfter=$LASTEXITCODE
  $out | Where-Object { $_ -match '^(CLAIM id="R(4|6|7)"|COMPOSITE_PATHPROOF verdict=)' } | ForEach-Object { "  $_" }
  "RC_PREFEATURE=$rcBefore RC_REPAIRED=$rcAfter"
}
```

Real output:

```text
D026 FIXTURE=red_render_named_fd_source.json (identical bytes on both sides; only the code differs)
  --- bb02c25a code streamed from git ---
  CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
  CLAIM id="R6" name="render_member_conservation" verdict="PASS" reason="every_input_member_has_one_terminal_disposition"
  CLAIM id="R7" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
  COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
  --- round-5 code on disk ---
  CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_command_word_not_modeled"
  CLAIM id="R6" name="render_member_conservation" verdict="STOP" reason="render_member_stopped"
  CLAIM id="R7" name="deployed_identity_binding" verdict="STOP" reason="deployed_identity_domain_not_derived"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
D026 FIXTURE=red_render_indexed_assign_source.json (identical bytes on both sides; only the code differs)
  --- bb02c25a code streamed from git ---
  CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
  CLAIM id="R6" name="render_member_conservation" verdict="PASS" reason="every_input_member_has_one_terminal_disposition"
  CLAIM id="R7" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
  COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
  --- round-5 code on disk ---
  CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_command_word_not_modeled"
  CLAIM id="R6" name="render_member_conservation" verdict="STOP" reason="render_member_stopped"
  CLAIM id="R7" name="deployed_identity_binding" verdict="STOP" reason="deployed_identity_domain_not_derived"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
D026 FIXTURE=red_render_unmodeled_prefix.json (identical bytes on both sides; only the code differs)
  --- bb02c25a code streamed from git ---
  CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
  CLAIM id="R6" name="render_member_conservation" verdict="PASS" reason="every_input_member_has_one_terminal_disposition"
  CLAIM id="R7" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
  COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
  --- round-5 code on disk ---
  CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix"
  CLAIM id="R6" name="render_member_conservation" verdict="STOP" reason="render_member_stopped"
  CLAIM id="R7" name="deployed_identity_binding" verdict="STOP" reason="deployed_identity_domain_not_derived"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
D026 FIXTURE=red_render_function_body_source.json (identical bytes on both sides; only the code differs)
  --- bb02c25a code streamed from git ---
  CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
  CLAIM id="R6" name="render_member_conservation" verdict="PASS" reason="every_input_member_has_one_terminal_disposition"
  CLAIM id="R7" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
  COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
  --- round-5 code on disk ---
  CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_command_word_not_modeled"
  CLAIM id="R6" name="render_member_conservation" verdict="STOP" reason="render_member_stopped"
  CLAIM id="R7" name="deployed_identity_binding" verdict="STOP" reason="deployed_identity_domain_not_derived"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
```

Block rc: `3` — PowerShell propagates the exit code of the last native command, and the last
command is a deliberate `rc 3` RED. The assertions here are the printed `RC_PREFEATURE` /
`RC_REPAIRED` pairs and the quoted claim verdicts, not the block rc.

**All four are rc-level REDs**, not claim-level ones. Each hides one `source "$LIBRARY_PATH"`
behind a different mechanism, each declares `"edges": []`, and each was a genuine `PASS rc 0`
on the audited commit with `R4`, `R6` **and** `R7` all PASS — the exact false-PASS shape the
audit described. The bodies are:

| Fixture | The hiding line | Repaired STOP |
|---|---|---|
| `red_render_named_fd_source` | `{fd}>/dev/null source "$LIBRARY_PATH"` | `source_graph_command_word_not_modeled` |
| `red_render_indexed_assign_source` | `SEEN[0]=1 source "$LIBRARY_PATH"` | `source_graph_command_word_not_modeled` |
| `red_render_unmodeled_prefix` | `SEEN[IDX[0]]=1 source "$LIBRARY_PATH"` | `source_graph_unmodeled_assignment_prefix` |
| `red_render_function_body_source` | `function reload { source "$LIBRARY_PATH"; }` | `source_graph_command_word_not_modeled` |

The third one is the fail-closed case the kickoff asked for specifically: the prefix is a valid
Bash assignment with a nested subscript, the model does not cover it, and the scanner says so
by name instead of calling it a leaf.

## 5. D026 mutation discriminators — 5 mutations × 4 REDs

Each mutation disables exactly one production comparison. The file on disk is never changed:
the mutated source is compiled and executed in memory. Every mutation is run against **every**
round-5 RED, so the matrix also proves each RED depends on its own mechanism and not on a
neighbour's. `EXPECTED_KILLS` is declared in the script and asserted, so a discriminator that
kills the wrong case fails the block rather than being read past.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r5=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r5_fixtures').Path
$mutants=@'
import contextlib, io, pathlib, re, sys
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
MUTATIONS = {
  "M1_redirection_prefix_numeric_only":    [(REDIRECTION_MODEL, REDIRECTION_ROUND4)],
  "M2_assignment_prefix_round4_restored":  [(ASSIGN_RE_R5, ASSIGN_RE_R4), (UNMODELED_FENCE, "")],
  "M3_unmodeled_prefix_fence_deleted":     [(UNMODELED_FENCE, "")],
  "M4_name_binding_conservation_deleted":  [(NAME_BINDING, '        if False and name_binding_pending and word_class == "leaf":')],
  "M5_assignment_model_narrowed_fence_kept": [(ASSIGN_RE_R5, ASSIGN_RE_R4)],
}
EXPECTED_KILLS = {
  "M1_redirection_prefix_numeric_only": {"named_fd"},
  "M2_assignment_prefix_round4_restored": {"indexed_assign", "unmodeled_prefix"},
  "M3_unmodeled_prefix_fence_deleted": {"unmodeled_prefix"},
  "M4_name_binding_conservation_deleted": {"function_body"},
  "M5_assignment_model_narrowed_fence_kept": set(),
}
CASES = [("named_fd", "red_render_named_fd_source.json"),
         ("indexed_assign", "red_render_indexed_assign_source.json"),
         ("unmodeled_prefix", "red_render_unmodeled_prefix.json"),
         ("function_body", "red_render_function_body_source.json")]
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
print("BASELINE unmutated round-5 code on disk")
for label, plan in CASES:
    rc, reason = run(SOURCE, FX / plan)
    print(f"  CASE={label:16s} RC={rc} R4_REASON={reason}")
wrong = 0
for name, edits in MUTATIONS.items():
    mutated = SOURCE
    for old, new in edits:
        assert mutated.count(old) == 1, (name, old[:60])
        mutated = mutated.replace(old, new)
    print(f"MUTATION={name}")
    for label, plan in CASES:
        rc, reason = run(mutated, FX / plan)
        restored = rc == 0
        wrong += restored != (label in EXPECTED_KILLS[name])
        print(f"  CASE={label:16s} RC={rc} "
              f"{'RED_RESTORED_TO_PASS' if restored else 'still_stopped':20s} R4_REASON={reason}")
print(f"MUTATIONS={len(MUTATIONS)} CELLS={len(MUTATIONS) * len(CASES)} OFF_EXPECTATION={wrong}")
sys.exit(0 if wrong == 0 else 1)
'@
$mutants | python -B - $tool $r5
"MUTATION_MATRIX_RC=$LASTEXITCODE"
```

Real output:

```text
BASELINE unmutated round-5 code on disk
  CASE=named_fd         RC=3 R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=indexed_assign   RC=3 R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=unmodeled_prefix RC=3 R4_REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  CASE=function_body    RC=3 R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
MUTATION=M1_redirection_prefix_numeric_only
  CASE=named_fd         RC=0 RED_RESTORED_TO_PASS R4_REASON=rendered_bytes_derive_the_declared_reachable_graph
  CASE=indexed_assign   RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=unmodeled_prefix RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  CASE=function_body    RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
MUTATION=M2_assignment_prefix_round4_restored
  CASE=named_fd         RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=indexed_assign   RC=0 RED_RESTORED_TO_PASS R4_REASON=rendered_bytes_derive_the_declared_reachable_graph
  CASE=unmodeled_prefix RC=0 RED_RESTORED_TO_PASS R4_REASON=rendered_bytes_derive_the_declared_reachable_graph
  CASE=function_body    RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
MUTATION=M3_unmodeled_prefix_fence_deleted
  CASE=named_fd         RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=indexed_assign   RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=unmodeled_prefix RC=0 RED_RESTORED_TO_PASS R4_REASON=rendered_bytes_derive_the_declared_reachable_graph
  CASE=function_body    RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
MUTATION=M4_name_binding_conservation_deleted
  CASE=named_fd         RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=indexed_assign   RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=unmodeled_prefix RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  CASE=function_body    RC=0 RED_RESTORED_TO_PASS R4_REASON=rendered_bytes_derive_the_declared_reachable_graph
MUTATION=M5_assignment_model_narrowed_fence_kept
  CASE=named_fd         RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
  CASE=indexed_assign   RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  CASE=unmodeled_prefix RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
  CASE=function_body    RC=3 still_stopped        R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
MUTATIONS=5 CELLS=20 OFF_EXPECTATION=0
MUTATION_MATRIX_RC=0
```

The block asserts its own expectation table: `OFF_EXPECTATION=0` means every one of the 20
cells landed where the script said it should before it ran.

Four things to read here.

**M1 is literally the repair the kickoff asked to be falsified**: restore the numeric-only
file-descriptor handling and the named-fd RED returns to `PASS rc 0`, while the other three
REDs stay STOP. The named-descriptor mechanism is independently discriminated.

**M2 restores round 4's assignment handling** — scalar-only model *and* no fail-closed fence —
and it returns **two** REDs to PASS. That is correct and is stated rather than hidden: with the
round-4 code both `SEEN[0]=1` and `SEEN[IDX[0]]=1` are leaves, so both fixtures were round-4
false passes. M3 then separates them: deleting only the fence returns the unmodelled RED to
PASS and leaves the indexed RED stopped, because the widened model alone already conserves it.

**M5 is the layering discriminator.** Narrowing the assignment model back to scalar-only while
*keeping* the fence leaves the indexed RED stopped — but its reason token moves from
`source_graph_command_word_not_modeled` to `source_graph_unmodeled_assignment_prefix`. The two
fences are independent: if the model is wrong, the tool still refuses rather than passing. This
is why the round-5 code has both and not just the wider regex.

**M4** discriminates the `function`/`coproc` name binding on its own and touches nothing else.

## 6. Prefix grammar battery — 16 blind forms, 9 controls, 1 disclosed false stop

Four fixtures prove the defects exist. This battery bounds them. Each blind form is valid Bash
that reaches another program, is a genuine `bb02c25a` `PASS rc 0`, and must be `rc 3` under
round-5 code. The controls prove the repair is not "STOP on anything unusual" — four of them
exercise the repaired paths directly with benign operands. All fixtures are generated into an
OS temporary directory and removed; nothing is written to the repository.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$old='bb02c25a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$battery=@'
import json, pathlib, subprocess, sys, tempfile
TOOL = pathlib.Path(sys.argv[1]).resolve()
OLD = sys.argv[2]
# Valid Bash that reaches another program, hidden behind a command prefix or a
# name-binding reserved word.  Every one is a real bb02c25a PASS rc 0.
BLIND = [
    ("named_fd_out",            '{fd}>/dev/null source "$LIBRARY_PATH"'),
    ("named_fd_in",             '{fd}</dev/null source "$LIBRARY_PATH"'),
    ("named_fd_append",         '{fd}>>/safe/fixture/out.log source "$LIBRARY_PATH"'),
    ("named_fd_dup",            '{fd}>&2 source "$LIBRARY_PATH"'),
    ("named_fd_bash",           '{fd}>/dev/null bash /safe/fixture/library.sh'),
    ("named_fd_after_scalar",   'LC_ALL=C {fd}>/dev/null source "$LIBRARY_PATH"'),
    ("indexed_assign",          'SEEN[0]=1 source "$LIBRARY_PATH"'),
    ("indexed_append",          'SEEN[0]+=1 source "$LIBRARY_PATH"'),
    ("indexed_quoted_sub",      'SEEN["a b"]=1 source "$LIBRARY_PATH"'),
    ("indexed_assign_bash",     'SEEN[0]=1 bash /safe/fixture/library.sh'),
    ("indexed_then_scalar",     'SEEN[0]=1 LC_ALL=C source "$LIBRARY_PATH"'),
    ("nested_subscript",        'SEEN[IDX[0]]=1 source "$LIBRARY_PATH"'),
    ("function_body_source",    'function reload { source "$LIBRARY_PATH"; }'),
    ("function_body_bash",      'function run { bash /safe/fixture/library.sh; }'),
    ("coproc_named_body",       'coproc logger { source "$LIBRARY_PATH"; }'),
    ("every_prefix_at_once",    'LC_ALL=C {fd}>/dev/null SEEN[0]=1 source "$LIBRARY_PATH"'),
]
# Benign forms that must stay rc 0 on BOTH sides: the repair must not be "STOP on
# anything that looks unusual".  The last four exercise the repaired paths directly.
CONTROLS = [
    ("operand_named_bash",      'echo bash'),
    ("word_containing_bash",    'cat "$ROOT/notes.bash"'),
    ("numeric_fd_redirection",  'cat "$ROOT/in.txt" 2> /safe/fixture/err.log'),
    ("leaf_with_dot_in_path",   'cat /safe/fixture/a.sh.b'),
    ("comment_mentions_source", '# source /safe/fixture/library.sh'),
    ("indexed_assign_leaf",     'SEEN[0]=1 cat "$ROOT/in.txt"'),
    ("named_fd_leaf",           '{fd}>/dev/null cat "$ROOT/in.txt"'),
    ("subscript_word_no_equal", 'SEEN[0] "$ROOT/in.txt"'),
    ("word_abutting_redirect",  'cat>/safe/fixture/out.log'),
]
# Conservative refusals: Bash would NOT reach another program here, but the prefix
# slot is one the scanner cannot model, so it STOPs rather than guessing.  Published
# as false stops, not as defect kills.
FALSE_STOPS = [
    ("brace_non_name_fd",       '{1}>/dev/null cat "$ROOT/in.txt"'),
]
DRIVER = """
import pathlib, subprocess, sys
tool = pathlib.Path(sys.argv[1])
source = subprocess.run(["git", "show", sys.argv[2]], capture_output=True, text=True,
                        check=True, encoding="utf-8").stdout
sys.argv = [str(tool), sys.argv[3], sys.argv[4]]
exec(compile(source, str(tool), "exec"), {"__name__": "__main__", "__file__": str(tool)})
"""
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
def run_old(plan):
    return subprocess.run([sys.executable, "-B", "-c", DRIVER, str(TOOL), OLD, "render", str(plan)],
                          capture_output=True, text=True).returncode
def run_new(plan):
    done = subprocess.run([sys.executable, "-B", str(TOOL), "render", str(plan)],
                          capture_output=True, text=True)
    reason = "-"
    for line in done.stdout.splitlines():
        if line.startswith('CLAIM id="R4"'):
            reason = line.split("reason=", 1)[1].strip('"')
    return done.returncode, reason
killed = survived = controls_ok = stops_ok = 0
with tempfile.TemporaryDirectory(prefix="sec102-r5-grammar-") as tmp:
    root = pathlib.Path(tmp)
    for name, body in BLIND:
        plan = build(root, name, body)
        old_rc = run_old(plan)
        new_rc, reason = run_new(plan)
        verdict = "KILLED" if (old_rc == 0 and new_rc == 3) else "SURVIVED"
        killed += verdict == "KILLED"
        survived += verdict == "SURVIVED"
        print(f"FORM={name} R4_RC={old_rc} R5_RC={new_rc} {verdict} R5_REASON={reason}")
    print(f"BLIND_FORMS={len(BLIND)} KILLED={killed} SURVIVED={survived}")
    for name, body in CONTROLS:
        plan = build(root, name, body)
        old_rc = run_old(plan)
        new_rc, _ = run_new(plan)
        good = old_rc == 0 and new_rc == 0
        controls_ok += good
        print(f"CONTROL={name} R4_RC={old_rc} R5_RC={new_rc} {'PASS' if good else 'FAIL'}")
    print(f"CONTROLS={len(CONTROLS)} PASSED={controls_ok}")
    for name, body in FALSE_STOPS:
        plan = build(root, name, body)
        old_rc = run_old(plan)
        new_rc, reason = run_new(plan)
        good = old_rc == 0 and new_rc == 3
        stops_ok += good
        print(f"FALSE_STOP={name} R4_RC={old_rc} R5_RC={new_rc} {'AS_DESIGNED' if good else 'UNEXPECTED'} R5_REASON={reason}")
    print(f"FALSE_STOPS={len(FALSE_STOPS)} AS_DESIGNED={stops_ok}")
sys.exit(0 if survived == 0 and controls_ok == len(CONTROLS) and stops_ok == len(FALSE_STOPS) else 1)
'@
$battery | python -B - $tool $old
"BATTERY_RC=$LASTEXITCODE"
```

Real output:

```text
FORM=named_fd_out R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=named_fd_in R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=named_fd_append R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=named_fd_dup R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=named_fd_bash R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=named_fd_after_scalar R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=indexed_assign R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=indexed_append R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=indexed_quoted_sub R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=indexed_assign_bash R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=indexed_then_scalar R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=nested_subscript R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_unmodeled_assignment_prefix
FORM=function_body_source R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=function_body_bash R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=coproc_named_body R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=every_prefix_at_once R4_RC=0 R5_RC=3 KILLED R5_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND_FORMS=16 KILLED=16 SURVIVED=0
CONTROL=operand_named_bash R4_RC=0 R5_RC=0 PASS
CONTROL=word_containing_bash R4_RC=0 R5_RC=0 PASS
CONTROL=numeric_fd_redirection R4_RC=0 R5_RC=0 PASS
CONTROL=leaf_with_dot_in_path R4_RC=0 R5_RC=0 PASS
CONTROL=comment_mentions_source R4_RC=0 R5_RC=0 PASS
CONTROL=indexed_assign_leaf R4_RC=0 R5_RC=0 PASS
CONTROL=named_fd_leaf R4_RC=0 R5_RC=0 PASS
CONTROL=subscript_word_no_equal R4_RC=0 R5_RC=0 PASS
CONTROL=word_abutting_redirect R4_RC=0 R5_RC=0 PASS
CONTROLS=9 PASSED=9
FALSE_STOP=brace_non_name_fd R4_RC=0 R5_RC=3 AS_DESIGNED R5_REASON=derived_graph_not_traversable,source_graph_unmodeled_redirection_prefix
FALSE_STOPS=1 AS_DESIGNED=1
BATTERY_RC=0
```

**16 of 16 blind forms killed, 0 survived; 9 of 9 controls still PASS on both
sides; the 1 disclosed false stop behaves as designed.** Every one of the 16 is an
independently executed `bb02c25a` `PASS rc 0` — the battery is 16 more pre-feature REDs, not 16
assertions about round-5 alone.

The one false stop is stated rather than counted as a kill. `{1}>/dev/null cat …` is a word
followed by a redirection in real Bash — `{1}` is not a valid descriptor name, so Bash runs a
command called `{1}` — and nothing is reached. The scanner refuses it anyway, because a brace
word in the exact syntactic slot of a named descriptor is a shape it cannot model. That is a
chosen false stop, and it is the only one the battery found.

### 6b. The round-4 battery, re-run as a round-5 regression

The 32 forms round 4 killed must still be `rc 3`, and its 5 controls must still be `rc 0`,
under round-5 code. (The full 32-form list and its round-3-vs-round-4 evidence are in
`SELF_QA_SEC102_R4.md` section 5; this run asserts only that round 5 regressed none of them.)

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$carried=@'
import json, pathlib, subprocess, sys, tempfile
TOOL = pathlib.Path(sys.argv[1]).resolve()
BLIND = [
    ("command_source",         'command source "$LIBRARY_PATH"'),
    ("builtin_source",         'builtin source "$LIBRARY_PATH"'),
    ("command_dot",            'command . "$LIBRARY_PATH"'),
    ("command_dash_p_source",  'command -p source "$LIBRARY_PATH"'),
    ("escaped_source",         '\\source "$LIBRARY_PATH"'),
    ("single_quoted_source",   "'source' \"$LIBRARY_PATH\""),
    ("double_quoted_source",   '"source" "$LIBRARY_PATH"'),
    ("if_source",              'if source "$LIBRARY_PATH"; then :; fi'),
    ("then_source",            'if true; then source "$LIBRARY_PATH"; fi'),
    ("brace_group_source",     '{ source "$LIBRARY_PATH"; }'),
    ("while_source",           'while source "$LIBRARY_PATH"; do break; done'),
    ("and_list_command",       'true && command source "$LIBRARY_PATH"'),
    ("bang_source",            '! source "$LIBRARY_PATH"'),
    ("env_bash",               'env bash /safe/fixture/library.sh'),
    ("env_absolute_bash",      '/usr/bin/env bash /safe/fixture/library.sh'),
    ("exec_bash",              'exec bash /safe/fixture/library.sh'),
    ("sudo_bash",              'sudo bash /safe/fixture/library.sh'),
    ("nohup_bash",             'nohup bash /safe/fixture/library.sh'),
    ("nice_bash",              'nice -n 5 bash /safe/fixture/library.sh'),
    ("time_bash",              'time bash /safe/fixture/library.sh'),
    ("timeout_bash",           'timeout 5 bash /safe/fixture/library.sh'),
    ("xargs_sh",               'xargs -n1 sh /safe/fixture/library.sh'),
    ("trap_source",            "trap 'source /safe/fixture/library.sh' EXIT"),
    ("assignment_prefix_bash", 'LC_ALL=C bash /safe/fixture/library.sh'),
    ("redirect_first_bash",    '> /safe/fixture/out.log bash /safe/fixture/library.sh'),
    ("zsh_member",             'zsh /safe/fixture/library.sh'),
    ("dash_member",            'dash /safe/fixture/library.sh'),
    ("ksh_member",             'ksh /safe/fixture/library.sh'),
    ("busybox_sh_member",      'busybox sh /safe/fixture/library.sh'),
    ("python2_member",         'python2 /safe/fixture/verifier.py'),
    ("perl_member",            'perl /safe/fixture/verifier.pl'),
    ("node_member",            'node /safe/fixture/verifier.js'),
]
CONTROLS = [
    ("operand_named_bash",       'echo bash'),
    ("word_containing_bash",     'cat "$ROOT/notes.bash"'),
    ("fd_redirection",           'cat "$ROOT/in.txt" 2> /safe/fixture/err.log'),
    ("leaf_with_dot_in_path",    'cat /safe/fixture/a.sh.b'),
    ("comment_mentions_source",  '# source /safe/fixture/library.sh'),
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
    return subprocess.run([sys.executable, "-B", str(TOOL), "render", str(plan)],
                          capture_output=True, text=True).returncode
held = ok = 0
with tempfile.TemporaryDirectory(prefix="sec102-r5-carried-") as tmp:
    root = pathlib.Path(tmp)
    for name, body in BLIND:
        rc = run_new(build(root, name, body))
        held += rc == 3
        if rc != 3:
            print(f"REGRESSED FORM={name} R5_RC={rc}")
    print(f"CARRIED_R4_BLIND_FORMS={len(BLIND)} STILL_RC3={held}")
    for name, body in CONTROLS:
        rc = run_new(build(root, name, body))
        ok += rc == 0
        if rc != 0:
            print(f"REGRESSED CONTROL={name} R5_RC={rc}")
    print(f"CARRIED_R4_CONTROLS={len(CONTROLS)} STILL_RC0={ok}")
sys.exit(0 if held == len(BLIND) and ok == len(CONTROLS) else 1)
'@
$carried | python -B - $tool
"CARRIED_BATTERY_RC=$LASTEXITCODE"
```

Real output:

```text
CARRIED_R4_BLIND_FORMS=32 STILL_RC3=32
CARRIED_R4_CONTROLS=5 STILL_RC0=5
CARRIED_BATTERY_RC=0
```

Command rc: `0`.

## 7. The five carried discriminators, re-run against round-5 code

Round 3 published three mutation discriminators and round 4 published two. All five must still
restore their defective PASS under round-5 code; if one stopped discriminating, its RED would
have quietly become dependent on the round-5 repair instead of on its own comparison.

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

Command rc: `0`. Ten discriminators now exist across rounds 3–5 (3 + 2 + 5), and all ten
restore the defective PASS they are supposed to guard.

## 8. Hygiene, determinism and scope

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$d='MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1'
git check-attr text eol -- "$d/sec102_r5_fixtures/entry_named_fd_source.sh" "$d/sec102_r5_fixtures/red_render_named_fd_source.json" "$d/composite_pathproof.py" "$d/pathscope_prover.py"
$carried=(git status --porcelain -- "$d/sec102_r1_fixtures" "$d/sec102_r2_fixtures" "$d/sec102_r3_fixtures" "$d/sec102_r4_fixtures" "$d/pathscope_prover.py")
"CARRIED_INPUT_WORKTREE_CHANGES=$(@($carried).Count)"
git diff --check -- "$d/composite_pathproof.py" "$d/.gitattributes"
"GIT_DIFF_CHECK_RC=$LASTEXITCODE"
git status --porcelain -- "$d/composite_pathproof.py" "$d/.gitattributes" "$d/sec102_r5_fixtures"
```

Real output:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_named_fd_source.sh: text: unset
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_named_fd_source.sh: eol: unspecified
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/red_render_named_fd_source.json: text: unset
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/red_render_named_fd_source.json: eol: unspecified
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py: text: set
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py: eol: lf
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py: text: set
MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py: eol: lf
CARRIED_INPUT_WORKTREE_CHANGES=0
warning: in the working copy of 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes', LF will be replaced by CRLF the next time Git touches it
GIT_DIFF_CHECK_RC=0
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes
 M MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/
```

Read verbatim, with nothing filed off:

* The round-5 fixture tree resolves to `text: unset`, i.e. the `-text` rule added to the scoped
  `.gitattributes` — the same durability treatment rounds 1–4 already have. The two pinned
  tools still resolve to `text eol=lf`, so the round-4 R3-F3 repair is not regressed.
* `CARRIED_INPUT_WORKTREE_CHANGES=0`: `git status --porcelain` over the four carried fixture
  trees and `pathscope_prover.py` printed nothing. No carried input was edited this round.
* `git diff --check` is **scoped to the two files this round modified** and returns rc `0`. It
  emits one LF→CRLF advisory for `.gitattributes`, which is not byte-pinned by anything and
  whose content Git reads regardless of line endings. The scoping is deliberate: an unscoped
  `git diff --check` in this worktree also reports the concurrent Max lane's RP6 files, whose
  advisories appear or not depending on Git's index stat cache — output this round does not own
  and cannot make reproducible.
* The only paths this round changed are `composite_pathproof.py`, `.gitattributes` and the new
  `sec102_r5_fixtures/` tree, plus the three evidence documents. That is the kickoff's fence.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$hygiene=@'
import ast, hashlib, json, pathlib, subprocess, sys
D = pathlib.Path("MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1")
TOOL = D / "composite_pathproof.py"
print("PYTHON=" + sys.version.split()[0])
ast.parse(TOOL.read_text(encoding="utf-8"), filename=str(TOOL))
print(f"AST_PARSE=PASS FILE={TOOL.name}")
plans = sorted(p for t in ("r1", "r2", "r3", "r4", "r5")
               for p in (D / f"sec102_{t}_fixtures").glob("*.json"))
for p in plans:
    json.loads(p.read_text(encoding="utf-8"))
print(f"JSON_PLANS_PARSED={len(plans)}")
crlf = [str(p) for t in ("r1", "r2", "r3", "r4", "r5")
        for p in sorted((D / f"sec102_{t}_fixtures").rglob("*"))
        if p.is_file() and b"\r" in p.read_bytes()]
print(f"FIXTURE_FILES_WITH_CR={len(crlf)} {crlf}")
tool_cr = b"\r" in TOOL.read_bytes()
print(f"TOOL_HAS_CR={tool_cr}")
def digest(stage, plan):
    done = subprocess.run([sys.executable, "-B", str(TOOL), stage, str(plan)],
                          capture_output=True, text=True)
    return done.returncode, len(done.stdout.splitlines()), hashlib.sha256(done.stdout.encode()).hexdigest()
DETERMINISM = [
    ("render", D / "sec102_r2_fixtures/green_render.json"),
    ("freeze", D / "sec102_r2_fixtures/green_freeze.json"),
    ("render", D / "sec102_r5_fixtures/red_render_named_fd_source.json"),
    ("render", D / "sec102_r5_fixtures/red_render_unmodeled_prefix.json"),
]
stable = 0
for stage, plan in DETERMINISM:
    a = digest(stage, plan)
    b = digest(stage, plan)
    stable += a == b
    print(f"DETERMINISM CASE={plan.name} RC={a[0]} LINES={a[1]} SHA256={a[2]} REPEAT_IDENTICAL={a == b}")
print(f"DETERMINISM_CASES={len(DETERMINISM)} STABLE={stable}")
'@
$hygiene | python -B -
```

Real output:

```text
PYTHON=3.14.2
AST_PARSE=PASS FILE=composite_pathproof.py
JSON_PLANS_PARSED=49
FIXTURE_FILES_WITH_CR=0 []
TOOL_HAS_CR=False
DETERMINISM CASE=green_render.json RC=0 LINES=31 SHA256=c2fdb5bf0af1f5c9d1c8ab7b2536e46db4d06a29a05aba2a9abe8970c24f33f8 REPEAT_IDENTICAL=True
DETERMINISM CASE=green_freeze.json RC=0 LINES=51 SHA256=b4be9a4ce33609e38d7ad83997a8f9d0637fb045ed69025441e1a70f5ee26cbb REPEAT_IDENTICAL=True
DETERMINISM CASE=red_render_named_fd_source.json RC=3 LINES=25 SHA256=83c567dfdfd06e676480e2807b88ef83f433b28ee4ff7fff0fa3b7f3dd1d71d1 REPEAT_IDENTICAL=True
DETERMINISM CASE=red_render_unmodeled_prefix.json RC=3 LINES=25 SHA256=7338f1c1d383ba0c662533a57d8cf4bb339b1cf179b7ba0e4414f46f7a3b377a REPEAT_IDENTICAL=True
DETERMINISM_CASES=4 STABLE=4
```

**Interpreter disclosure, stated rather than glossed.** `SELF_QA_SEC102_R4.md` recorded a
Python 3.12 AST parse. This machine now offers only 3.14.2 (default) and 3.13; 3.12 is not
installed, so the round-5 parse ran under **3.14.2** and the whole 44-case matrix ran under the
same interpreter. `sys.executable` remains an unpinned external-runtime dependency (residual
15, unchanged). Nothing here establishes behaviour under 3.12.

### The four GREEN transcripts did not move

The strongest single check that no fence was weakened: run every GREEN under `bb02c25a` and
under round-5 code over identical inputs and compare the whole stdout.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$cmp=@'
import hashlib, pathlib, subprocess, sys
D = pathlib.Path("MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1")
TOOL = D / "composite_pathproof.py"
OLD = "bb02c25a:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py"
DRIVER = """
import pathlib, subprocess, sys
tool = pathlib.Path(sys.argv[1])
source = subprocess.run(["git", "show", sys.argv[2]], capture_output=True, text=True,
                        check=True, encoding="utf-8").stdout
sys.argv = [str(tool), sys.argv[3], sys.argv[4]]
exec(compile(source, str(tool), "exec"), {"__name__": "__main__", "__file__": str(tool)})
"""
CASES = [("allocate", D / "sec102_r1_fixtures/green.json"),
         ("render", D / "sec102_r2_fixtures/green_render.json"),
         ("freeze", D / "sec102_r2_fixtures/green_freeze.json"),
         ("freeze", D / "sec102_r2_fixtures/green_freeze_network.json")]
same = 0
for stage, plan in CASES:
    old = subprocess.run([sys.executable, "-B", "-c", DRIVER, str(TOOL), OLD, stage, str(plan)],
                         capture_output=True, text=True)
    new = subprocess.run([sys.executable, "-B", str(TOOL), stage, str(plan)],
                         capture_output=True, text=True)
    a = hashlib.sha256(old.stdout.encode()).hexdigest()
    b = hashlib.sha256(new.stdout.encode()).hexdigest()
    same += a == b
    print(f"GREEN={plan.name} R4_RC={old.returncode} R5_RC={new.returncode} "
          f"R4_SHA256={a[:16]} R5_SHA256={b[:16]} BYTE_IDENTICAL={a == b}")
print(f"GREEN_TRANSCRIPTS={len(CASES)} UNCHANGED_FROM_bb02c25a={same}")
'@
$cmp | python -B -
```

Real output:

```text
GREEN=green.json R4_RC=0 R5_RC=0 R4_SHA256=573a928b1d7f5f42 R5_SHA256=573a928b1d7f5f42 BYTE_IDENTICAL=True
GREEN=green_render.json R4_RC=0 R5_RC=0 R4_SHA256=c2fdb5bf0af1f5c9 R5_SHA256=c2fdb5bf0af1f5c9 BYTE_IDENTICAL=True
GREEN=green_freeze.json R4_RC=0 R5_RC=0 R4_SHA256=b4be9a4ce33609e3 R5_SHA256=b4be9a4ce33609e3 BYTE_IDENTICAL=True
GREEN=green_freeze_network.json R4_RC=0 R5_RC=0 R4_SHA256=9e618af5e46a6e4b R5_SHA256=9e618af5e46a6e4b BYTE_IDENTICAL=True
GREEN_TRANSCRIPTS=4 UNCHANGED_FROM_bb02c25a=4
```

Round 5 adds no output surface and changes no accepted transcript. Unlike round 4 — which moved
the FREEZE GREEN digest — every GREEN here is byte-identical to the audited commit.

## 9. Artifact identity

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$identity=@'
import hashlib, pathlib
D = pathlib.Path("MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1")
targets = [D / "composite_pathproof.py", D / ".gitattributes"]
targets += sorted((D / "sec102_r5_fixtures").iterdir())
targets += [D / "SELF_QA_SEC102_R5.md", D / "STATUS_SEC102.md", D / "SEC102_R5_REPORT_2026-08-11.md"]
for p in targets:
    raw = p.read_bytes()
    print(f"ARTIFACT {p.as_posix()} bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")
'@
$identity | python -B -
```

Real output for the code, attributes and fixtures (the three evidence documents are re-derived
by the same command; their table is in `SEC102_R5_REPORT_2026-08-11.md` section 6):

```text
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py bytes=116867 sha256=25cb8a174e7515c8e4caa7f2157780e69f37d11331abc62330d8018dfebdcc5c
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes bytes=1563 sha256=a195360ec2fd769a3f355dae22b9b3ed1e736d6cf5b5d494fa12f795c7249dc9
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_function_body_source.sh bytes=191 sha256=27f231e8eb9e29d5133bd541174c098202c9706423b896f56d5cd1a33271843f
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_function_body_source.sh.in bytes=176 sha256=e71c7e32cad2e922fe4028cdea3ff464cb3ba014917c780c8a17c38f1c6e800c
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_indexed_assign_source.sh bytes=173 sha256=4ddb3aaabb23ce8370bab7ff50826e01dd7af0308ca310021bd8bcd320c70bd5
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_indexed_assign_source.sh.in bytes=158 sha256=da60202ca51e31ddf085b578bfd13cc091736716ed88bca356034472e4b557d3
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_named_fd_source.sh bytes=178 sha256=ab48e178890070eeadcb649b66946e3585fb10cd78b4ae41593a2e9762f1aa3d
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_named_fd_source.sh.in bytes=163 sha256=a0cda206662094c8f6c07f27284406ca789f016bd7d4ede45162bf43b20dc8ce
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_unmodeled_prefix.sh bytes=178 sha256=8bcbb81abd4e74074b3e3708982af7764f9698861d7e0049862067092714815f
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/entry_unmodeled_prefix.sh.in bytes=163 sha256=c5262e6cc90cf5fcfc8dabddc8d1f680fa262ba297344f6f010c20a8d5dac4fd
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/red_render_function_body_source.json bytes=914 sha256=4733e10e870a59702fb70c15d5cdb06446a5c0b3603bf976cdae2bf93f23730c
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/red_render_indexed_assign_source.json bytes=917 sha256=39b1cc60259ad2c1335b3c92362250c1c1807caf19a8897c504ede27b44c47bc
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/red_render_named_fd_source.json bytes=899 sha256=052e7651bba1e8de317c6f60c0a5ae99681962637fb3532fd148fe41458df13e
ARTIFACT MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r5_fixtures/red_render_unmodeled_prefix.json bytes=909 sha256=ce26e20ba13b9bbb0252dadd202c0edf42241ae24b2a7a0dbbf47774c6b9cd78
```

`pathscope_prover.py` was not touched and its pin (`122446` B /
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`) is unchanged; the FREEZE
GREEN transcript above is the running proof of it.

## 10. Honest residual scope — what round 5 does NOT close

Round 4's residual list (`STATUS_SEC102.md`, items 1–23) carries forward unchanged except where
noted. Round-5-specific residuals:

1. **The command-word detection vocabulary is still a list.** Round 5 repaired *how the scanner
   reaches* a command word, not *which names it recognises*. An interpreter absent from the
   32-name vocabulary, invoked at a genuinely conserved command position under a literal name,
   is still classified a benign leaf and derives no edge. This is the surviving half of R3-F1
   and it is unchanged by this round.
2. **Executing an arbitrary program (`./child.sh`, `/opt/tool`) is outside every modelled edge
   kind** and always was. It is a leaf, not a STOP.
3. **The prefix model is now claimed complete for Bash assignment words and redirections, and
   that claim is exactly as strong as my reading of the Bash grammar.** The accepted vocabulary
   is: `NAME=`, `NAME+=`, `NAME[sub]=`, `NAME[sub]+=` with a bracket-free subscript; numeric and
   `{name}` descriptors abutting `< > >> >& <& >| <>`. Anything outside that which *looks like*
   a prefix STOPs by name. If the grammar has a prefix form I have not enumerated **and** it
   does not resemble either shape, it would still degrade to a leaf. I know of none; that is a
   statement about my knowledge, not a proof.
4. **`for` / `select` / `case` are argued safe, not fixed.** They bind a name like
   `function`/`coproc`, but a separator, newline or `)` re-opens the command position before
   any body command, so no command word is lost. Section 2 rows `for_loop_body` and
   `paren_function_body` measure this. It is an argument backed by two probes, not by
   exhaustive enumeration of reserved-word syntax.
5. **New false stops, deliberately taken.** `{1}>…` and any brace word abutting a redirection
   whose interior is not a plain name STOP even though Bash would treat them as ordinary words
   (section 6). `arr[…` words carrying an `=` that the subscript model cannot close STOP even
   if a user meant a command name. Both are conservative and both are disclosed rather than
   tuned away.
6. **`raw.isdigit()` → `^[0-9]+$` is a deliberate narrowing.** The old test accepted Unicode
   digits, so `²>out` was swallowed as a descriptor prefix. Bash does not do that: `²` is an
   ordinary word. The new behaviour matches Bash, and in that form Bash reaches no other
   program either way, so no edge is created or lost.
7. **Nothing about the analysis-unit builder, the prover adapter arms, deployed-path host
   identity, or production composites changed.** The 28 undriven prover-adapter arms remain
   undriven; round 5 drove no new arm and claims no adapter closure.
8. **This is still a synthetic fixture proof.** No production entrypoint, no archive, no host,
   no dispatch, no Section 10.2 acceptance follows from any PASS here.

## 11. Thirteen-pattern self-adjudication

* **Pattern 12 (primary).** The finding and the repair are both "what the analyzer does not
  model must not disappear". Two prefix shapes were unmodelled and vanished silently; they now
  either resolve (modelled) or STOP by name (unmodelled). Zero facts plus PASS over
  `{fd}>… source lib` was exactly the red state Pattern 12 predicts.
* **Pattern 5.** The round-4 assignment expression was a partial grammar over a modelled input
  contract. It is now the full Bash assignment-word grammar plus an explicit refusal for
  anything outside it.
* **Pattern 9 (overlay).** Round 4's status text said command position was conserved across
  "assignment prefixes"; it was conserved across *scalar* assignment prefixes. The sentence
  outran the code. The round-5 wording in section 10 item 3 states exactly what the model
  covers and labels the completeness claim as a reading of the grammar rather than a proof.
* **Pattern 10.** Every command in this document is complete and was executed as written from
  an absolute `Set-Location`: no template, no placeholder, no `<FIX>`, no undeclared shell
  state, and no block abbreviated by reference. Section 12 records the paste-and-run
  verification of that claim. The mutation matrix asserts its own expectation table and the
  batteries assert their own counters, so neither can pass by being read charitably.
* **Pattern 13.** Unchanged from round 4: one terminal disposition per member, per allocation,
  per constants binding. Round 5 adds no new universe.
* **Patterns 1, 6/7, 8, 11.** Untouched by this round; no new instance and no new claim.
* **Patterns 2, 3, 4.** Still explicit non-claims: no host, no namespace, no privilege domain,
  no symlink or mount-boundary resolution.

## 12. Paste-and-run verification of this document

Pattern 10's rule is that evidence which cannot be re-executed as written is not evidence, and
`[AUDIT6 sec. 2]` set the standard: extract the fenced bodies without changing a character and
run them in a fresh process. This document was checked that way rather than by re-reading it.

The harness below extracts **every** ` ```powershell ` fence byte-for-byte, writes it to a
temporary `.ps1`, runs it under a fresh `powershell -NoProfile -NonInteractive -File` **from a
working directory outside the repository**, and compares the combined stdout+stderr to the
` ```text ` fence that follows it. Running from outside the repository is what proves the
"cwd-robust" claim rather than asserting it.

```python
# harness — run as: python -B <this-file> <self-qa.md> <cwd-outside-the-repo> 12
import pathlib, re, subprocess, sys, tempfile
DOC = pathlib.Path(sys.argv[1])
CWD = pathlib.Path(sys.argv[2])              # deliberately NOT the repository
PARTIAL = set(int(x) for x in sys.argv[3:])  # blocks whose published output is a subset
text = DOC.read_text(encoding="utf-8")
FENCE = re.compile(r"```(powershell|text)\n(.*?)```", re.S)
blocks = [(m.group(1), m.group(2)) for m in FENCE.finditer(text)]
pairs = []
for i, (kind, body) in enumerate(blocks):
    if kind != "powershell":
        continue
    expected = blocks[i + 1][1] if i + 1 < len(blocks) and blocks[i + 1][0] == "text" else None
    pairs.append((len(pairs) + 1, body, expected))
exact = differs = 0
with tempfile.TemporaryDirectory(prefix="paste-and-run-") as tmp:
    for number, script, expected in pairs:
        path = pathlib.Path(tmp) / f"block{number}.ps1"
        path.write_text(script, encoding="utf-8")
        done = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-File", str(path)],
                              capture_output=True, text=True, cwd=str(CWD))
        got = [l.rstrip() for l in (done.stdout + done.stderr).splitlines() if l.strip()]
        want = [l.rstrip() for l in (expected or "").splitlines() if l.strip()]
        if number in PARTIAL:
            ok = set(want) <= set(got)
            status = "PUBLISHED_SUBSET_PRESENT" if ok else "SUBSET_MISSING"
        else:
            ok = sorted(want) == sorted(got)
            status = "OUTPUT_MATCHES_PUBLISHED" if ok else "OUTPUT_DIFFERS"
        exact += ok; differs += not ok
        print(f"BLOCK={number} RC={done.returncode} LINES={len(got)} {status}")
        if not ok:
            for line in [l for l in want if l not in got][:6]:
                print(f"  ONLY_IN_DOCUMENT: {line}")
            for line in [l for l in got if l not in want][:6]:
                print(f"  ONLY_IN_RUN:      {line}")
print(f"POWERSHELL_BLOCKS={len(pairs)} MATCHED={exact} DIFFERED={differs}")
sys.exit(0 if differs == 0 else 1)
```

Real output:

```text
BLOCK=1 RC=0 LINES=3 OUTPUT_MATCHES_PUBLISHED
BLOCK=2 RC=0 LINES=17 OUTPUT_MATCHES_PUBLISHED
BLOCK=3 RC=0 LINES=45 OUTPUT_MATCHES_PUBLISHED
BLOCK=4 RC=0 LINES=48 OUTPUT_MATCHES_PUBLISHED
BLOCK=5 RC=0 LINES=32 OUTPUT_MATCHES_PUBLISHED
BLOCK=6 RC=0 LINES=30 OUTPUT_MATCHES_PUBLISHED
BLOCK=7 RC=0 LINES=3 OUTPUT_MATCHES_PUBLISHED
BLOCK=8 RC=0 LINES=7 OUTPUT_MATCHES_PUBLISHED
BLOCK=9 RC=0 LINES=14 OUTPUT_MATCHES_PUBLISHED
BLOCK=10 RC=0 LINES=10 OUTPUT_MATCHES_PUBLISHED
BLOCK=11 RC=0 LINES=5 OUTPUT_MATCHES_PUBLISHED
BLOCK=12 RC=0 LINES=17 PUBLISHED_SUBSET_PRESENT
POWERSHELL_BLOCKS=12 MATCHED=12 DIFFERED=0
```

Three honest notes on this section.

**It found real defects in my own document, which is the point.** The first run reported
`MATCHED=0 DIFFERED=12`. Causes, all fixed above: block 1 used `$input`, a PowerShell reserved
variable, so it printed an empty value — **and its published "real output" carried a full blob
hash I had not obtained by running it**; blocks 2, 5 and 6 published output that omitted the
final assertion line; block 9's unscoped `git diff --check` reported a concurrent lane's files
whose advisories depend on Git's index stat cache. A document read carefully instead of
executed would have shipped all five.

**Block 12 is a declared subset, not an exact match.** The artifact-identity command lists the
three evidence documents as well as the code and fixtures, and a document cannot contain its
own SHA-256. Its published output covers the code, the attributes and the fixture tree exactly;
the document row set is re-derived by the Lead from the same command. The full table is in
`SEC102_R5_REPORT_2026-08-11.md` section 6.

**Self-reference, stated.** The final harness run was made with this document complete except
for the output fence directly above, which was then pasted in. Pasting it changed no
` ```powershell ` fence and no block's behaviour, so every line above remains the output of the
document as published. The Lead can settle it by re-running the harness — that is the check.
