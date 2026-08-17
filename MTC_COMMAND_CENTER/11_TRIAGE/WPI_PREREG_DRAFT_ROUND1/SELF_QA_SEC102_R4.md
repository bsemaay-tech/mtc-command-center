# Self-QA - Section 10.2 composite proof, round 4

Date: 2026-08-11
Audit tier: T1 - bounded local-only non-economic Python tooling and fixtures
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`
Input commit: `10659bd5`. Implementer: `claude-opus-5` xhigh (Max account), acting on the
round-3 Codex flagship audit `SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md` (verdict
`REQUEST_CHANGES`, three MEDIUM findings). Codex audits round 4.

This is implementer self-QA, not Gate-5 acceptance. The owning Lead must execute the
published harness verbatim before audit dispatch and independently inspect the actual diff.

Every fenced block below begins with `Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'` and uses
no undeclared shell state, so each block is literally paste-and-run from any working
directory.

No remote host, network request, shell subject, block, wrapper, preregistration draft,
broker, trading surface, Pine file, parity file, schema, deployment action, or Git write to
this repository was invoked. `sec102_r3_fixtures/evil/library.sh` contains `cat /etc/shadow`
and a `curl` to `exfil.example.invalid` as **static fixture text**; it is parsed as data by
the pinned prover and is never executed. `.invalid` is a reserved, unresolvable TLD. The
only subprocesses are the pinned CPython invocation of the pinned `pathscope_prover.py`, and
- in section 6 only - `git` against a throw-away repository created under the OS temporary
directory. Section 6 creates and clones that temporary repository; it does not `init`, `add`,
`commit`, `checkout`, `reset` or `stash` anything in `C:\LAB\Tradingview_LAB_CLEAN`.

## 1. What round 4 changed

| Round-3 finding | Repair | New RED |
|---|---|---|
| R3-F1 MEDIUM - RENDER's coverage check shares the graph detector's blind spot, so a source/interpreter operation behind a valid command wrapper leaves no edge **and** no uncovered site | Coverage is no longer counted with a second regex built from the matcher's own grammar. A new independent scanner (`_shell_words`) tokenises the rendered bytes and marks every command position; `_graph_word_conservation` STOPs on any command word the *detection* vocabulary recognises but the *derivation* grammar did not match, on any command wrapper at all, and on any dynamic command word. Detection is deliberately strictly broader than derivation. | `red_render_wrapped_source.json`, plus `red_freeze_wrapped_source.json` (claim-level) and a 32-form grammar battery in section 5 |
| R3-F2 MEDIUM - F10 reports PASS before every plan allocation has a constants-side disposition | `_reconcile_constants` now walks **both** directions. Every declared allocation gets exactly one terminal `ALLOCATION_RECONCILIATION` row; an allocation the pinned constants table never mentions is `STOP allocation_absent_from_pinned_constants` on F10 itself. The F10 claim sentence is narrowed to what the predicate actually proves. | `red_freeze_allocation_absent.json` |
| R3-F3 MEDIUM - a clean Windows checkout changes the pinned bytes, so the published matrix cannot reproduce | New `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes`, scoped to this directory, pins the checked-out bytes of all four fixture trees and of the two pinned tools. Section 6 demonstrates a real `core.autocrlf=true` clone reproducing the matrix. | section 6, three arms |

Two decisions inside these repairs are the implementer's and are called out for the auditor:

**R3-F2, option (1) taken, and taken unconditionally.** The audit allowed "make F10 STOP
when an allocation that can affect prover semantics is absent". Round 4 STOPs on *every*
absent allocation and does not implement an "affects prover semantics" carve-out. Deciding
that a name cannot affect prover semantics requires modelling every way a shell can
reference a name - which is a second modelled grammar, and an incomplete one would reopen
exactly the Pattern-5/12 hole that R3-F1 is about. A hard rule needs no such model.
Constants-only names remain allowed and keep their explicit `RUNTIME_ONLY` rows, and the
F10 claim sentence is narrowed to say only that (audit option 2 applied to that half).

**R3-F3, the scope is two lines wider than the kickoff sketched, and that is load-bearing.**
The kickoff's example covered `sec102_r*_fixtures/**` only. Section 6's second arm runs
exactly that example and it is still RED: `pathscope_prover.py` is `attr/text=auto` like
everything else, a fresh Windows checkout materialises it at 125222 B instead of the pinned
122446 B, and `green_freeze.json` then fails `F4 frozen_identity_mismatch` - 10 of the 40
cases fail. The published `.gitattributes` therefore also pins `pathscope_prover.py` and
`composite_pathproof.py`, with `text eol=lf` rather than `-text` so both remain textually
diffable for review. **No byte of `pathscope_prover.py` was modified**; only how Git
materialises it. If the Lead judges this outside the fence, the honest consequence is that
R3-F3 cannot be closed, and that should be recorded rather than papered over.

## 2. Literal all-case assertion command

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r1='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
$r4='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures'
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
  @('freeze',$r4,'red_freeze_allocation_absent.json',3,'allocation_absent_from_pinned_constants')
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
CASES=40 FAILED_COUNT=0
```

Command rc: `0`. **All 37 round-3 cases are carried with their rc and reason token
unchanged**; three are round-4 additions. No prior fixture file was edited: `git status` for
`sec102_r1_fixtures`, `sec102_r2_fixtures` and `sec102_r3_fixtures` is empty (section 8).

A round-3 harness defect is fixed here and is worth flagging because it would have misled a
re-runner. The round-3 block ended with `if($failed){exit 1}`, so with `$failed -eq 0` the
block's own exit status was whatever the *last* `python` invocation returned. Round 3 got
away with it because its last case was a `rc 0` GREEN. Round 4's last case is a `rc 3` RED,
so the block now ends `if($failed){exit 1}else{exit 0}` and its rc is a real assertion.

## 3. D026 RED before GREEN - behavioural pre-feature falsification

Each new fixture is run twice over **byte-identical plan and member inputs**; only the
program changes. The pre-feature side is the exact round-3 code streamed from `10659bd5`
(no file is checked out or overwritten).

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r4=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures').Path
$old='10659bd5:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$driver=@'
import pathlib, subprocess, sys
tool = pathlib.Path(sys.argv[1])
source = subprocess.run(["git", "show", sys.argv[2]], capture_output=True, text=True,
                        check=True, encoding="utf-8").stdout
sys.argv = [str(tool), sys.argv[3], sys.argv[4]]
namespace = {"__name__": "__main__", "__file__": str(tool)}
exec(compile(source, str(tool), "exec"), namespace)
'@
foreach($case in @(
  @('render','red_render_wrapped_source.json','^(CLAIM id="R(4|6|7)"|COMPOSITE_PATHPROOF verdict=)'),
  @('freeze','red_freeze_wrapped_source.json','^(CLAIM id="F(3|6)"|COMPOSITE_PATHPROOF verdict=)'),
  @('freeze','red_freeze_allocation_absent.json','^(CLAIM id="F(5|6|10)"|ALLOCATION_RECONCILIATION .*REMOTE_BASE|COMPOSITE_PATHPROOF verdict=)'))){
  $stage=$case[0]; $plan=$case[1]; $filter=$case[2]
  "D026 STAGE=$stage FIXTURE=$plan (identical bytes on both sides; only the code differs)"
  "  --- round-3 code streamed from $($old.Split(':')[0]) ---"
  $out=($driver | python -B - $tool $old $stage (Join-Path $r4 $plan))
  $rcBefore=$LASTEXITCODE
  $out | Where-Object { $_ -match $filter } | ForEach-Object { "  $_" }
  "  --- round-4 code on disk ---"
  $out=(& python -B $tool $stage (Join-Path $r4 $plan))
  $rcAfter=$LASTEXITCODE
  $out | Where-Object { $_ -match $filter } | ForEach-Object { "  $_" }
  "RC_PREFEATURE=$rcBefore RC_REPAIRED=$rcAfter"
}
```

Real output:

```text
D026 STAGE=render FIXTURE=red_render_wrapped_source.json (identical bytes on both sides; only the code differs)
  --- round-3 code streamed from 10659bd5 ---
  CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
  CLAIM id="R6" name="render_member_conservation" verdict="PASS" reason="every_input_member_has_one_terminal_disposition"
  CLAIM id="R7" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
  COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
  --- round-4 code on disk ---
  CLAIM id="R4" name="derived_source_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled"
  CLAIM id="R6" name="render_member_conservation" verdict="STOP" reason="render_member_stopped"
  CLAIM id="R7" name="deployed_identity_binding" verdict="STOP" reason="deployed_identity_domain_not_derived"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
D026 STAGE=freeze FIXTURE=red_freeze_wrapped_source.json (identical bytes on both sides; only the code differs)
  --- round-3 code streamed from 10659bd5 ---
  CLAIM id="F3" name="derived_whole_program_graph" verdict="PASS" reason="all_members_reachable_in_derived_graph"
  CLAIM id="F6" name="lexical_pathscope_disposition" verdict="STOP" reason="prover_member_stopped"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
  --- round-4 code on disk ---
  CLAIM id="F3" name="derived_whole_program_graph" verdict="STOP" reason="derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled"
  CLAIM id="F6" name="lexical_pathscope_disposition" verdict="STOP" reason="prover_prerequisite_not_closed"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
RC_PREFEATURE=3 RC_REPAIRED=3
D026 STAGE=freeze FIXTURE=red_freeze_allocation_absent.json (identical bytes on both sides; only the code differs)
  --- round-3 code streamed from 10659bd5 ---
  CLAIM id="F5" name="prover_output_conservation" verdict="PASS" reason="seven_counts_and_records_reconciled"
  CLAIM id="F6" name="lexical_pathscope_disposition" verdict="PASS" reason="every_prover_result_terminal_and_fail_closed"
  CLAIM id="F10" name="allocation_constants_reconciliation" verdict="PASS" reason="plan_allocations_and_pinned_constants_are_one_conserved_value_universe"
  COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
  --- round-4 code on disk ---
  CLAIM id="F5" name="prover_output_conservation" verdict="PASS" reason="seven_counts_and_records_reconciled"
  CLAIM id="F6" name="lexical_pathscope_disposition" verdict="PASS" reason="every_prover_result_terminal_and_fail_closed"
  CLAIM id="F10" name="allocation_constants_reconciliation" verdict="STOP" reason="allocation_absent_from_pinned_constants"
  ALLOCATION_RECONCILIATION composite="fixture-absent" index=0 name="REMOTE_BASE" value="/safe/fixture" disposition="STOP" reason="allocation_absent_from_pinned_constants"
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
```

Block rc: `3`. PowerShell propagates the exit code of the last native command, and the last
command is a deliberate `rc 3` RED. The assertions in this section are the printed
`RC_PREFEATURE` / `RC_REPAIRED` pairs and the quoted claim verdicts, not the block rc.

Three things to read carefully:

**R3-F1, the rc-level RED.** `red_render_wrapped_source.json` declares one member and no
edges. Its rendered bytes contain `command source "$LIBRARY_PATH"`, which the shell executes
as the `source` builtin. Round-3 code derives no edge, counts no uncovered site, and reports
`R4`, `R6` **and** `R7` PASS at `rc 0` - the exact false-PASS shape the audit described.
Round-4 code STOPs, and `R7` no longer PASSes vacuously over a domain that was never derived.

**R3-F1, the claim-level RED.** `red_freeze_wrapped_source.json` is the same bytes at FREEZE.
Round-3 code already returned `rc 3` - but from `F6 prover_member_stopped`, i.e. from the
separately pinned prover, while `F3` still claimed
`all_members_reachable_in_derived_graph` PASS. That is the audit's point that the composite's
own graph claim was false even though the system stayed fail-closed downstream. Round 4
STOPs at `F3` itself. This case is published as a **claim-level** RED, not an rc-level one,
and the matrix asserts it on the `source_graph_command_word_not_modeled` token rather than
pretending the rc changed.

**R3-F2 isolates F10.** For `red_freeze_allocation_absent.json` the prover still runs and
`F5` and `F6` are PASS on **both** sides. The only claim that moves is `F10`. The audit
required that a downstream F5/F6 STOP must not be offered as the discriminator; here there
is no downstream STOP at all, so the composite's `rc 3` is attributable to F10 alone.

## 4. D026 mutation discriminators against current code

Each mutation disables exactly the production comparison its RED fixture is supposed to
depend on. The file on disk is never changed. Sections 4a and 4b are the two round-4
additions; section 4c re-runs the three round-3 discriminators against round-4 code.

### 4a-4b - the two new discriminators

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$r4=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures').Path

# --- R3-F1: delete the independent command-word conservation ------------------
$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
mutations = {
  "            for reason in _graph_word_conservation(text, source_matches, exec_matches):":
    "            for reason in ():",
}
for old, new in mutations.items():
  assert source.count(old) == 1, old
  source = source.replace(old, new)
sys.argv = [str(path), sys.argv[2], sys.argv[3]]
namespace = {"__name__": "__main__", "__file__": str(path)}
exec(compile(source, str(path), "exec"), namespace)
'@
"MUTATION=R4F1_command_word_conservation_deleted CASE=red_render_wrapped_source.json"
$out=($driver | python -B - $tool 'render' (Join-Path $r4 'red_render_wrapped_source.json'))
$rc=$LASTEXITCODE
$out | Where-Object { $_ -match '^(CLAIM id="R(4|6|7)"|COMPOSITE_PATHPROOF verdict=)' }
"MUTANT_RC=$rc REQUIRED_RED_RC=3"

# --- R3-F2: restore the round-3 silent absence --------------------------------
$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
mutations = {
  "        elif binding is None:\n            disposition, reason = \"STOP\", \"allocation_absent_from_pinned_constants\"":
    "        elif binding is None:\n            disposition, reason = \"RECONCILED\", \"allocation_and_constants_byte_equal\"",
}
for old, new in mutations.items():
  assert source.count(old) == 1, old
  source = source.replace(old, new)
sys.argv = [str(path), sys.argv[2], sys.argv[3]]
namespace = {"__name__": "__main__", "__file__": str(path)}
exec(compile(source, str(path), "exec"), namespace)
'@
"MUTATION=R4F2_absent_allocation_disposition_reverted CASE=red_freeze_allocation_absent.json"
$out=($driver | python -B - $tool 'freeze' (Join-Path $r4 'red_freeze_allocation_absent.json'))
$rc=$LASTEXITCODE
$out | Where-Object { $_ -match '^(CLAIM id="F10"|ALLOCATION_RECONCILIATION .*REMOTE_BASE|COMPOSITE_PATHPROOF verdict=)' }
"MUTANT_RC=$rc REQUIRED_RED_RC=3"
```

Real output:

```text
MUTATION=R4F1_command_word_conservation_deleted CASE=red_render_wrapped_source.json
CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
CLAIM id="R6" name="render_member_conservation" verdict="PASS" reason="every_input_member_has_one_terminal_disposition"
CLAIM id="R7" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
MUTANT_RC=0 REQUIRED_RED_RC=3
MUTATION=R4F2_absent_allocation_disposition_reverted CASE=red_freeze_allocation_absent.json
CLAIM id="F10" name="allocation_constants_reconciliation" verdict="PASS" reason="every_plan_allocation_reconciled_and_every_pinned_constant_dispositioned"
ALLOCATION_RECONCILIATION composite="fixture-absent" index=0 name="REMOTE_BASE" value="/safe/fixture" disposition="RECONCILED" reason="allocation_and_constants_byte_equal"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
```

### 4c - the three round-3 discriminators, re-run against round-4 code

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$fx=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures').Path

$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
mutations = {
  "    return deploy_to_id.get(identity)":
    "    if identity in deploy_to_id:\n        return deploy_to_id[identity]\n"
    "    fallback = [value for key, value in deploy_to_id.items()\n"
    "                if posixpath.basename(key) == posixpath.basename(operand)]\n"
    "    return fallback[0] if len(fallback) == 1 else None",
  "                target = deploy_to_id.get(_canonical_deployed_path(operand) or \"\")":
    "                target = _member_for_operand(operand, deploy_to_id)",
}
for old, new in mutations.items():
  assert source.count(old) == 1, old
  source = source.replace(old, new)
sys.argv = [str(path), "freeze", sys.argv[2]]
namespace = {"__name__": "__main__", "__file__": str(path)}
exec(compile(source, str(path), "exec"), namespace)
'@
"MUTATION=F1_basename_fallback_restored CASE=red_freeze_deploy_identity.json"
$out=($driver | python -B - $tool (Join-Path $fx 'red_freeze_deploy_identity.json'))
"MUTANT_RC=$LASTEXITCODE REQUIRED_RED_RC=3"
$out | Where-Object { $_ -match '^(CLAIM id="F9"|DERIVED_EDGE |COMPOSITE_PATHPROOF verdict=)' }

$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
mutations = {
  "        elif binding.value != allocation_values[binding.name]:":
    "        elif False and binding.value != allocation_values[binding.name]:",
  "        elif binding.value != allocation.value:":
    "        elif False and binding.value != allocation.value:",
  "                if constants_operand != operand:":
    "                if False and constants_operand != operand:",
}
for old, new in mutations.items():
  assert source.count(old) == 1, old
  source = source.replace(old, new)
sys.argv = [str(path), "freeze", sys.argv[2]]
namespace = {"__name__": "__main__", "__file__": str(path)}
exec(compile(source, str(path), "exec"), namespace)
'@
"MUTATION=F2_allocation_constants_comparisons_disabled CASE=red_freeze_allocation_constants.json"
$out=($driver | python -B - $tool (Join-Path $fx 'red_freeze_allocation_constants.json'))
"MUTANT_RC=$LASTEXITCODE REQUIRED_RED_RC=3"
$out | Where-Object { $_ -match '^(CLAIM id="F10"|PROVER_RECORD .*LIBRARY_PATH|COMPOSITE_PATHPROOF verdict=)' }

$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
mutations = {
  "            recorder.record(claim_id, Verdict.STOP, \"member_kind_graph_derivation_not_modeled\")\n"
  "            derivation_blocked = True\n            continue":
    "            continue",
}
for old, new in mutations.items():
  assert source.count(old) == 1, old
  source = source.replace(old, new)
sys.argv = [str(path), "render", sys.argv[2]]
namespace = {"__name__": "__main__", "__file__": str(path)}
exec(compile(source, str(path), "exec"), namespace)
'@
"MUTATION=F3_non_shell_graph_stop_reverted CASE=red_render_non_shell_member.json"
$out=($driver | python -B - $tool (Join-Path $fx 'red_render_non_shell_member.json'))
"MUTANT_RC=$LASTEXITCODE REQUIRED_RED_RC=3"
$out | Where-Object { $_ -match '^(CLAIM id="R4"|RENDER_MEMBER .*verifier|COMPOSITE_PATHPROOF verdict=)' }
```

Real output:

```text
MUTATION=F1_basename_fallback_restored CASE=red_freeze_deploy_identity.json
MUTANT_RC=0 REQUIRED_RED_RC=3
CLAIM id="F9" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
DERIVED_EDGE composite="fixture-divergent" source="entry" target="library" kind="source" operand="/safe/fixture/evil/library.sh" disposition="DERIVED" reason="rendered_source_site"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
MUTATION=F2_allocation_constants_comparisons_disabled CASE=red_freeze_allocation_constants.json
MUTANT_RC=0 REQUIRED_RED_RC=3
CLAIM id="F10" name="allocation_constants_reconciliation" verdict="PASS" reason="every_plan_allocation_reconciled_and_every_pinned_constant_dispositioned"
PROVER_RECORD composite="fixture-p0" member="fixture-p0" index=2 record="PATH value=/safe/fixture/somewhere/else/library.sh verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=LIBRARY_PATH uses=line=5:test" disposition="ACCOUNTED"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
MUTATION=F3_non_shell_graph_stop_reverted CASE=red_render_non_shell_member.json
MUTANT_RC=0 REQUIRED_RED_RC=3
CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
RENDER_MEMBER composite="fixture-ro" index=1 id="verifier" kind="python_source" path="verifier.py" deploy_path="/safe/fixture/verifier.py" graph="REACHABLE" materialisation="PASS" reason="materialised_byte_exact" bytes=74 sha256="1a2963fbf1b560d5e3cad96669971edce15f6186a11785c80a2f7cf1d0d256ba" disposition="ACCEPT"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
```

All five mutants restore the defective PASS, so each RED discriminates on the intended
comparison and not on some other property of its plan.

The round-3 `F2` discriminator needed **one extra line** in round 4
(`elif binding.value != allocation.value:`). That is not a weakening: the allocation-side
walk added for R3-F2 is a genuinely independent second comparison of the same two value
sources, and the discriminator has to disable both copies before the old PASS returns. The
round-3 two-line mutation now leaves the fixture RED, which is the correct behaviour.

## 5. R3-F1 grammar battery - detection is broader than derivation

The single `command source` fixture proves the defect exists. This battery bounds it. Each
of the 32 forms below is valid shell that reaches another program, is a genuine round-3
`PASS rc 0`, and must be `rc 3` under round-4 code. The 5 controls prove the check is not
simply "STOP on everything": each is benign, and each is `rc 0` on both sides. All fixtures
are generated into an OS temporary directory and removed; nothing is written to the repo.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$old='10659bd5:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$battery=@'
import json, pathlib, subprocess, sys, tempfile
TOOL = pathlib.Path(sys.argv[1]).resolve()
OLD = sys.argv[2]
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
    return done.returncode, done.stdout
killed = survived = ok = 0
with tempfile.TemporaryDirectory(prefix="sec102-r4-grammar-") as tmp:
    root = pathlib.Path(tmp)
    for name, body in BLIND:
        plan = build(root, name, body)
        old_rc = run_old(plan)
        new_rc, out = run_new(plan)
        reason = "-"
        for line in out.splitlines():
            if line.startswith('CLAIM id="R4"'):
                reason = line.split("reason=", 1)[1].strip('"')
        verdict = "KILLED" if (old_rc == 0 and new_rc == 3) else "SURVIVED"
        killed += verdict == "KILLED"
        survived += verdict == "SURVIVED"
        print(f"FORM={name} R3_RC={old_rc} R4_RC={new_rc} {verdict} R4_REASON={reason}")
    print(f"BLIND_FORMS={len(BLIND)} KILLED={killed} SURVIVED={survived}")
    for name, body in CONTROLS:
        plan = build(root, name, body)
        old_rc = run_old(plan)
        new_rc, _ = run_new(plan)
        good = old_rc == 0 and new_rc == 0
        ok += good
        print(f"CONTROL={name} R3_RC={old_rc} R4_RC={new_rc} {'PASS' if good else 'FAIL'}")
    print(f"CONTROLS={len(CONTROLS)} PASSED={ok}")
sys.exit(0 if survived == 0 and ok == len(CONTROLS) else 1)
'@
$battery | python -B - $tool $old
"BATTERY_RC=$LASTEXITCODE"
```

Real output:

```text
FORM=command_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=builtin_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=command_dot R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=command_dash_p_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_wrapper_not_modeled
FORM=escaped_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=single_quoted_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=double_quoted_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=if_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=then_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=brace_group_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=while_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=and_list_command R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=bang_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=env_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=env_absolute_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=exec_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=sudo_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=nohup_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=nice_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_wrapper_not_modeled
FORM=time_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled,source_graph_command_wrapper_not_modeled
FORM=timeout_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_wrapper_not_modeled
FORM=xargs_sh R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_wrapper_not_modeled
FORM=trap_source R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_wrapper_not_modeled
FORM=assignment_prefix_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=redirect_first_bash R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=zsh_member R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=dash_member R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=ksh_member R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=busybox_sh_member R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=python2_member R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=perl_member R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
FORM=node_member R3_RC=0 R4_RC=3 KILLED R4_REASON=derived_graph_not_traversable,source_graph_command_word_not_modeled
BLIND_FORMS=32 KILLED=32 SURVIVED=0
CONTROL=operand_named_bash R3_RC=0 R4_RC=0 PASS
CONTROL=word_containing_bash R3_RC=0 R4_RC=0 PASS
CONTROL=fd_redirection R3_RC=0 R4_RC=0 PASS
CONTROL=leaf_with_dot_in_path R3_RC=0 R4_RC=0 PASS
CONTROL=comment_mentions_source R3_RC=0 R4_RC=0 PASS
CONTROLS=5 PASSED=5
```

Command rc: `0`. **32 of 32 blind forms killed, 0 survived; 5 of 5 controls still PASS.**
Every one of the 32 is an independently executed round-3 `PASS rc 0` - the battery is 32
more pre-feature REDs, not 32 assertions about round-4 alone.

Read the reason column: some forms are caught by the wrapper rule, some by the command-word
rule, most by both. `zsh`, `dash`, `ksh`, `busybox`, `python2`, `perl` and `node` are caught
because the *detection* vocabulary contains interpreters the *derivation* grammar cannot
model - which is the entire design point. `EXEC_COMMAND_RE` models only `bash`, `sh` and
`python`/`python3[.N]`; anything else that executes a program file is now a STOP rather than
an absence.

## 6. R3-F3 fresh-checkout durability demonstration

Three arms, all built from the same audited bytes, all cloned with `core.autocrlf=true`,
which is what a fresh Windows checkout does. Each arm mirrors the real repository by putting
`* text=auto` at the throw-away repository root. `TRANSCRIPT_EQUALS_AUDITED` compares the
clone's entire 41-line matrix transcript against the audited worktree's, line for line.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$demo=@'
import hashlib, pathlib, shutil, subprocess, sys, tempfile
REPO = pathlib.Path(sys.argv[1]).resolve()
SRC = REPO / "MTC_COMMAND_CENTER" / "11_TRIAGE" / "WPI_PREREG_DRAFT_ROUND1"
FIXTURES = [f"sec102_r{n}_fixtures" for n in (1, 2, 3, 4)]
TOOLS = ["composite_pathproof.py", "pathscope_prover.py"]
SKIP = {".impeccable", "__pycache__", ".git"}
CASES = [
 ("allocate", 1, "red_plan_contract.json", 3, "plan_schema_unknown_key"),
 ("allocate", 1, "red_entrypoint.json", 1, "entrypoint_not_declared"),
 ("allocate", 1, "red_allocation_conservation.json", 1, "allocation_not_one_to_one"),
 ("allocate", 1, "red_allocation_value.json", 3, "allocation_value_unresolved"),
 ("allocate", 1, "red_graph_conservation.json", 1, "declared_member_unreachable"),
 ("allocate", 1, "red_component_identity.json", 3, "member_file_missing"),
 ("allocate", 1, "green.json", 0, "allocate_stage_closed"),
 ("render", 2, "red_render_contract.json", 3, "plan_schema_unknown_key"),
 ("render", 2, "red_render_template_conservation.json", 1, "render_template_member_not_one_to_one"),
 ("render", 2, "red_render_materialisation.json", 1, "rendered_bytes_mismatch"),
 ("render", 2, "red_render_graph_dynamic.json", 3, "source_operand_dynamic"),
 ("render", 2, "red_render_identity.json", 3, "member_file_missing"),
 ("render", 2, "red_render_member_disposition.json", 1, "render_member_rejected"),
 ("render", 2, "red_render_heredoc_false_edge.json", 3, "source_graph_heredoc_not_modeled"),
 ("render", 3, "red_render_non_shell_member.json", 3, "member_kind_graph_derivation_not_modeled"),
 ("render", 2, "green_render.json", 0, "render_stage_closed"),
 ("freeze", 2, "red_freeze_contract.json", 3, "plan_schema_unknown_key"),
 ("freeze", 2, "red_freeze_member_pin.json", 3, "frozen_identity_mismatch"),
 ("freeze", 2, "red_freeze_graph.json", 3, "derived_declared_graph_mismatch"),
 ("freeze", 2, "red_freeze_prover_pin.json", 3, "approved_prover_identity_not_declared"),
 ("freeze", 2, "red_freeze_prover_grammar.json", 3, "prover_output_grammar_incomplete"),
 ("freeze", 2, "red_freeze_coverage.json", 3, "coverage_issue_count=2"),
 ("freeze", 2, "red_freeze_forbidden.json", 1, "prover_forbidden_operand"),
 ("freeze", 2, "red_freeze_residual.json", 3, "prover_residual_disclosure_missing"),
 ("freeze", 2, "red_freeze_member_disposition.json", 3, "non_shell_member_analyzer_not_integrated"),
 ("freeze", 3, "red_freeze_deploy_identity.json", 3, "source_operand_deploy_identity_unbound"),
 ("freeze", 3, "red_freeze_deploy_path_invalid.json", 3, "member_deploy_path_not_canonical_absolute"),
 ("freeze", 3, "red_freeze_deploy_path_alias.json", 3, "member_deploy_path_alias"),
 ("freeze", 3, "red_freeze_allocation_constants.json", 3, "allocation_constants_value_divergence"),
 ("freeze", 3, "red_freeze_constants_grammar.json", 3, "constants_line_not_key_value"),
 ("freeze", 3, "red_freeze_constants_operand_unbound.json", 3, "analysis_unit_source_operand_constants_unbound"),
 ("freeze", 3, "red_freeze_execute_source_edge.json", 3, "analysis_unit_non_source_edge_not_integrated"),
 ("freeze", 3, "red_freeze_source_site_not_standalone.json", 3, "analysis_unit_source_site_not_standalone"),
 ("freeze", 3, "red_freeze_zero_facts.json", 3, "prover_zero_facts_pass"),
 ("freeze", 3, "red_freeze_divergent_control.json", 1, "prover_forbidden_operand"),
 ("freeze", 2, "green_freeze.json", 0, "freeze_stage_closed"),
 ("freeze", 2, "green_freeze_network.json", 0, "resolved_net_endpoint_count=1"),
 ("render", 4, "red_render_wrapped_source.json", 3, "source_graph_command_wrapper_not_modeled"),
 ("freeze", 4, "red_freeze_wrapped_source.json", 3, "source_graph_command_word_not_modeled"),
 ("freeze", 4, "red_freeze_allocation_absent.json", 3, "allocation_absent_from_pinned_constants"),
]
def tracked_files():
    for name in TOOLS:
        yield pathlib.PurePosixPath(name)
    for fixture in FIXTURES:
        for path in sorted((SRC / fixture).rglob("*")):
            if path.is_file() and not (SKIP & set(path.relative_to(SRC).parts)):
                yield pathlib.PurePosixPath(path.relative_to(SRC).as_posix())
def digest(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()
def matrix(root):
    lines, failed = [], 0
    for stage, fixture, name, want, token in CASES:
        plan = root / f"sec102_r{fixture}_fixtures" / name
        done = subprocess.run(
            [sys.executable, "-B", str(root / "composite_pathproof.py"), stage, str(plan)],
            capture_output=True, text=True)
        ok = done.returncode == want and token in done.stdout
        failed += not ok
        lines.append(f"CASE={name} STAGE={stage} RC={done.returncode} EXPECTED={want} "
                     f"TOKEN={token} ASSERT={'PASS' if ok else 'FAIL'}")
    lines.append(f"CASES={len(CASES)} FAILED_COUNT={failed}")
    return lines, failed
FILES = list(tracked_files())
BASELINE = {name: digest(SRC / name) for name in FILES}
baseline_lines, baseline_failed = matrix(SRC)
print(f"AUDITED_WORKTREE files={len(FILES)} matrix_failed={baseline_failed}")
FIXTURES_ONLY = b"".join(f"sec102_r{n}_fixtures/** -text\n".encode() for n in (1, 2, 3, 4))
ARMS = (("no_gitattributes_round3_state", None),
        ("fixtures_only_gitattributes", FIXTURES_ONLY),
        ("published_scoped_gitattributes", (SRC / ".gitattributes").read_bytes()))
for arm, scoped in ARMS:
    with tempfile.TemporaryDirectory(prefix="sec102-r4-eol-") as tmp:
        root = pathlib.Path(tmp)
        origin, clone = root / "origin", root / "clone"
        (origin / "round1").mkdir(parents=True)
        (origin / ".gitattributes").write_bytes(b"* text=auto\n")
        for name in FILES:
            target = origin / "round1" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SRC / name, target)
        if scoped is not None:
            (origin / "round1" / ".gitattributes").write_bytes(scoped)
        env = ["-c", "user.name=sec102-r4-demo", "-c", "user.email=sec102-r4@invalid"]
        subprocess.run(["git", "init", "-q", str(origin)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(origin), "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(origin)] + env + ["commit", "-q", "-m", "sec102 r4 durability demo"],
                       check=True, capture_output=True)
        subprocess.run(["git", "-c", "core.autocrlf=true", "clone", "-q", str(origin), str(clone)],
                       check=True, capture_output=True)
        checked_out = clone / "round1"
        changed = [name for name in FILES if digest(checked_out / name) != BASELINE[name]]
        lines, failed = matrix(checked_out)
        print(f"ARM={arm} autocrlf=true checked_out_files={len(FILES)} "
              f"byte_changed_files={len(changed)} MATRIX_FAILED_COUNT={failed} "
              f"TRANSCRIPT_EQUALS_AUDITED={lines == baseline_lines}")
        for name in changed[:4]:
            was, now = BASELINE[name], digest(checked_out / name)
            print(f"  CHANGED {name} committed_bytes={was[0]} checked_out_bytes={now[0]} "
                  f"delta=+{now[0] - was[0]} sha_equal={was[1] == now[1]}")
        if len(changed) > 4:
            print(f"  ... and {len(changed) - 4} further byte-changed files")
'@
$demo | python -B - 'C:\LAB\Tradingview_LAB_CLEAN'
"DEMO_RC=$LASTEXITCODE"
```

Real output:

```text
AUDITED_WORKTREE files=96 matrix_failed=0
ARM=no_gitattributes_round3_state autocrlf=true checked_out_files=96 byte_changed_files=96 MATRIX_FAILED_COUNT=13 TRANSCRIPT_EQUALS_AUDITED=False
  CHANGED composite_pathproof.py committed_bytes=111239 checked_out_bytes=113808 delta=+2569 sha_equal=False
  CHANGED pathscope_prover.py committed_bytes=122446 checked_out_bytes=125222 delta=+2776 sha_equal=False
  CHANGED sec102_r1_fixtures/entry.sh committed_bytes=126 checked_out_bytes=130 delta=+4 sha_equal=False
  CHANGED sec102_r1_fixtures/green.json committed_bytes=852 checked_out_bytes=885 delta=+33 sha_equal=False
  ... and 92 further byte-changed files
ARM=fixtures_only_gitattributes autocrlf=true checked_out_files=96 byte_changed_files=2 MATRIX_FAILED_COUNT=10 TRANSCRIPT_EQUALS_AUDITED=False
  CHANGED composite_pathproof.py committed_bytes=111239 checked_out_bytes=113808 delta=+2569 sha_equal=False
  CHANGED pathscope_prover.py committed_bytes=122446 checked_out_bytes=125222 delta=+2776 sha_equal=False
ARM=published_scoped_gitattributes autocrlf=true checked_out_files=96 byte_changed_files=0 MATRIX_FAILED_COUNT=0 TRANSCRIPT_EQUALS_AUDITED=True
```

Command rc: `0`.

- **Arm 1 reproduces R3-F3 exactly.** Round-3's state, cloned on Windows: all 96 files change
  bytes and 13 of 40 cases fail. This is not a prediction; the clone happened.
- **Arm 2 is the kickoff's own example**, `sec102_r*_fixtures/** -text` and nothing else. The
  fixture blobs survive, but the two pinned tools do not: `pathscope_prover.py` arrives at
  125222 B against a pin of 122446 B, and 10 of 40 cases still fail. This is the measurement
  behind the scope decision recorded in section 1.
- **Arm 3 is the published `.gitattributes`.** Zero byte changes across all 96 files, `40/40`
  with `FAILED_COUNT=0`, and the clone's whole matrix transcript is line-for-line identical
  to the audited worktree's. The repair is an attribute, not a documented prerequisite.

The attribute has effect only once the Lead commits it, because Git reads checkout
attributes from the committed tree. The demonstration above commits it inside a throw-away
repository to prove that; nothing was committed here.

## 7. Adapter-arm census - carried forward unchanged

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$census=@'
import pathlib, re, subprocess, sys
tool = pathlib.Path(sys.argv[1])
source = tool.read_text(encoding="utf-8")
adapter = source[source.index("class SubprocessPathProver"):source.index("def run_freeze")]
arms = sorted(set(re.findall(r'_stop_result\([^,]+,\s*"([a-z0-9_]+)"', adapter))
              | set(re.findall(r'return None, "([a-z0-9_]+)"', adapter))
              | {"prover_shell_member_set_empty", "prover_zero_facts_pass"})
base = tool.parent
plans = sorted(base.glob("sec102_r1_fixtures/*.json")) \
      + sorted(base.glob("sec102_r2_fixtures/*.json")) \
      + sorted(base.glob("sec102_r3_fixtures/red_*.json")) \
      + sorted(base.glob("sec102_r4_fixtures/red_*.json"))
seen = set()
for plan in plans:
    for stage in ("allocate", "render", "freeze"):
        out = subprocess.run([sys.executable, "-B", str(tool), stage, str(plan)],
                             capture_output=True, text=True).stdout
        seen |= set(re.findall(r"[a-z][a-z0-9_]{6,}", out))
driven = [arm for arm in arms if arm in seen]
undriven = [arm for arm in arms if arm not in seen]
print(f"ADAPTER_ARMS_TOTAL={len(arms)} DRIVEN={len(driven)} UNDRIVEN={len(undriven)}")
print("DRIVEN=" + ",".join(driven))
print("UNDRIVEN=" + ",".join(undriven))
'@
$census | python -B - $tool
```

Real output:

```text
ADAPTER_ARMS_TOTAL=33 DRIVEN=5 UNDRIVEN=28
DRIVEN=analysis_unit_non_source_edge_not_integrated,analysis_unit_source_operand_constants_unbound,analysis_unit_source_site_not_standalone,prover_output_grammar_incomplete,prover_zero_facts_pass
UNDRIVEN=analysis_unit_member_conservation_mismatch,analysis_unit_member_deploy_path_ambiguous,analysis_unit_member_deploy_path_not_canonical_absolute,analysis_unit_member_path_missing,analysis_unit_member_read_error,analysis_unit_source_cycle,analysis_unit_source_edge_unbound,analysis_unit_source_operand_constants_divergent,analysis_unit_source_operand_deploy_identity_unbound,analysis_unit_source_operand_dynamic,prover_endpoint_disposition_ambiguous,prover_endpoint_disposition_missing,prover_forbid_reason_mismatch,prover_forbid_terminal_mismatch,prover_issue_count_mismatch,prover_issue_reason_mismatch,prover_issue_terminal_mismatch,prover_output_unknown_record,prover_pass_reason_mismatch,prover_pass_terminal_mismatch,prover_path_disposition_ambiguous,prover_path_disposition_missing,prover_process_terminal_rc_mismatch,prover_resolved_count_mismatch,prover_shell_member_set_empty,prover_stderr_nonempty,prover_unresolved_kind_ambiguous,prover_unresolved_kind_missing
```

**Still 5 of 33 driven, 28 carried undriven.** Round 4 drove no new adapter arm and this
document does not claim otherwise. The classification of the undriven set is unchanged from
`SELF_QA_SEC102_R3.md` section 6 and remains valid: 17 prover-output reconciliation arms are
unreachable while `pathscope_prover.py` is pinned, 10 analysis-unit arms are shadowed by an
earlier composite STOP, and `prover_shell_member_set_empty` cannot be reached from
`run_freeze`. The round-4 repairs shadow *more* of them, not fewer, because a wrapper form
now STOPs at `_derive_graph` before the adapter is reached.

## 8. Syntax, grammar, determinism, and protected-component checks

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
$r4='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r4_fixtures'
python -B -c "import ast,pathlib; p=pathlib.Path(r'$tool'); t=ast.parse(p.read_text(encoding='utf-8'),filename=str(p),feature_version=(3,12)); names=sorted({a.name.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.Import) for a in n.names}|{n.module.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.ImportFrom) and n.module}); print('AST_PARSE_3_12=PASS'); print('IMPORTS='+','.join(names))"
python -B -c "import json,pathlib; files=sorted(pathlib.Path(r'$r2').glob('*.json'))+sorted(pathlib.Path(r'$r3').glob('*.json'))+sorted(pathlib.Path(r'$r4').glob('*.json')); [json.loads(p.read_text(encoding='utf-8')) for p in files]; print(f'JSON_PARSE=PASS count={len(files)}')"
python -B -c "import pathlib; bad=[p.as_posix() for p in list(pathlib.Path(r'$r2').rglob('*'))+list(pathlib.Path(r'$r3').rglob('*'))+list(pathlib.Path(r'$r4').rglob('*')) if p.is_file() and b'\r' in p.read_bytes()]; print('FIXTURE_LF_ONLY='+('PASS' if not bad else 'FAIL '+','.join(bad)))"
git diff --check -- $tool $r2 $r3
"DIFF_CHECK_RC=$LASTEXITCODE"
"PROVER_WORKTREE_DIFF_BEGIN"
git diff --name-only -- 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py'
"PROVER_WORKTREE_DIFF_END"
git status --porcelain -- 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r1_fixtures' 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r2_fixtures' 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r3_fixtures'
"CARRIED_FIXTURE_STATUS_END"
$determinism=@'
import hashlib, io, pathlib, sys, contextlib
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
code = compile(source, str(path), "exec")
for stage, plan in (("render", sys.argv[2]), ("freeze", sys.argv[3]), ("freeze", sys.argv[4])):
    digests, codes = [], []
    for _ in range(2):
        buffer = io.StringIO()
        sys.argv = [str(path), stage, plan]
        namespace = {"__name__": "__main__", "__file__": str(path)}
        with contextlib.redirect_stdout(buffer):
            try:
                exec(code, namespace)
            except SystemExit as exc:
                codes.append(exc.code)
        digests.append(hashlib.sha256(buffer.getvalue().encode("utf-8")).hexdigest())
    print(f"DETERMINISM stage={stage} plan={pathlib.Path(plan).name} rc1={codes[0]} rc2={codes[1]} "
          f"equal={digests[0] == digests[1]} sha={digests[0]}")
'@
$determinism | python -B - $tool (Join-Path $r2 'green_render.json') (Join-Path $r2 'green_freeze.json') (Join-Path $r4 'red_freeze_allocation_absent.json')
```

Real output. One elision is declared, exactly as in round 3: the `git diff --check` line also
writes Git's repository-wide `warning: ... LF will be replaced by CRLF the next time Git
touches it` advisory to stderr, one line per modified file. Those advisory lines are omitted
below; nothing else is removed. They are the same root cause section 6 repairs, and they are
why the scoped `.gitattributes` matters.

```text
AST_PARSE_3_12=PASS
IMPORTS=__future__,argparse,dataclasses,enum,hashlib,json,pathlib,posixpath,re,shlex,subprocess,sys,tempfile,typing
JSON_PARSE=PASS count=35
FIXTURE_LF_ONLY=PASS
DIFF_CHECK_RC=0
PROVER_WORKTREE_DIFF_BEGIN
PROVER_WORKTREE_DIFF_END
CARRIED_FIXTURE_STATUS_END
DETERMINISM stage=render plan=green_render.json rc1=0 rc2=0 equal=True sha=c2fdb5bf0af1f5c9d1c8ab7b2536e46db4d06a29a05aba2a9abe8970c24f33f8
DETERMINISM stage=freeze plan=green_freeze.json rc1=0 rc2=0 equal=True sha=b4be9a4ce33609e38d7ad83997a8f9d0637fb045ed69025441e1a70f5ee26cbb
DETERMINISM stage=freeze plan=red_freeze_allocation_absent.json rc1=3 rc2=3 equal=True sha=5e3c36df4d22765eae1ad35c3d49484368304d2d2aefe950c6035a124d69e9e2
```

`pathscope_prover.py` has no worktree diff. `sec102_r1_fixtures`, `sec102_r2_fixtures` and
`sec102_r3_fixtures` all have empty `git status` output, so **no carried fixture was edited
in round 4**; every round-4 file is new and lives in `sec102_r4_fixtures`.

Two output digests to compare against round 3. The RENDER GREEN digest is
`c2fdb5bf...f33f8`, **byte-identical to round 3** - the new word conservation changes nothing
about a plan whose graph was already fully modelled. The FREEZE GREEN digest moved from
`be48a5fe...79da` to `b4be9a4c...6cbb`; that is expected and accounted for: FREEZE reports now
carry one `ALLOCATION_RECONCILIATION` row per declared allocation, two extra
`CONSTANTS_CONSERVATION` counters, two extra `FREEZE_CONSERVATION` counters, and the narrowed
F10 claim sentence.

## 9. Artifact identity record

Re-derived, not asserted:

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1'
python -B -c "import hashlib,pathlib; ps=[pathlib.Path('composite_pathproof.py'),pathlib.Path('.gitattributes')]+sorted(p for p in pathlib.Path('sec102_r4_fixtures').iterdir() if p.is_file()); [print(f'{p.as_posix()} bytes={len(p.read_bytes())} sha256={hashlib.sha256(p.read_bytes()).hexdigest()}') for p in ps]"
```

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `composite_pathproof.py` | 111239 | `24823c911490ac5d1984b3e5306278402b979418bd9bd9cc0e78d9ca471d362a` |
| `.gitattributes` | 1482 | `a93508e67d670df06bc6f75ce60e443e655018fe50f35f17cdd6987bf49ffc77` |
| `sec102_r4_fixtures/allowlist.txt` | 17 | `a011e924851560c9b91b92c2d3802a893b3d96fbff47efc2dd5db560f371a62b` |
| `sec102_r4_fixtures/constants.env` | 126 | `63d21caa85c6418449b3d5ccfba5b2990144709ece2ab2c2d0ddf2dfce35a572` |
| `sec102_r4_fixtures/constants_no_remote_base.env` | 100 | `6a98596fe084e00f91010e735d52cba64dc1172159027441c24bf6a533d03ab9` |
| `sec102_r4_fixtures/entry.sh` | 163 | `8618ccad69b8e4df4b3c232cff3ab1324fcf84fac970aafa876b09e9feb2a340` |
| `sec102_r4_fixtures/entry_wrapped_source.sh` | 171 | `82d8ccef42dcb7fe4add1d886a27a1052c256bc7589692508e92a73d80eeaacc` |
| `sec102_r4_fixtures/entry_wrapped_source.sh.in` | 156 | `8164de33f0f507c43dea521b574606686520537231af5e0e4c7c1dba234c1039` |
| `sec102_r4_fixtures/library.sh` | 43 | `b96bb4475e27d0767daf8f774ce92976eb1af1f1bbd937260682bfef7b8a4656` |
| `sec102_r4_fixtures/red_freeze_allocation_absent.json` | 1680 | `22445be0ec0c81c35ca4f7a903c36085648247f6f20f464f24abf2fb4cf0c804` |
| `sec102_r4_fixtures/red_freeze_wrapped_source.json` | 1400 | `00f72c874dbf719076898c67b5cdf24114ae26cf7321777c8f7fc16f01adbf73` |
| `sec102_r4_fixtures/red_render_wrapped_source.json` | 896 | `2136c797526ca6f477e8170d746a6161d4d9a269d94067f651ad048cb02048c8` |

`sec102_r4_fixtures/entry.sh`, `library.sh`, `allowlist.txt` and `constants.env` are
byte-identical copies of the round-2/round-3 originals (same SHA-256s), placed in the
round-4 directory only because a plan resolves member and proof-input paths relative to
itself. `pathscope_prover.py` remains 122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`, and was not touched.

## 10. Limitations - disclosures, not controls

Every round-3 limitation still stands unless listed as changed below. Round 4 adds these.

1. **The word scanner is a model, and it is honest about being one.** `_shell_words` is not
   a shell parser. It is a lexer with a deliberate bias: everything it cannot classify as a
   benign leaf command at a command position is a STOP. Its failure mode is over-detection,
   never silent acceptance. The round-3 coverage check failed the other way, which is why a
   wrapper disappeared from both the matcher and its own coverage count.
2. The scanner runs only on text `_graph_opaque_reason` already accepted. Here-documents,
   line continuations, substitutions, `eval`/`alias` at a command position and multi-line
   quotes STOP before it, and are not scanned twice; a here-document body would otherwise be
   tokenised as if it were code.
3. The detection vocabulary is a list, and a list can be short. An interpreter not in
   `GRAPH_INTERPRETER_WORDS` and not matching `GRAPH_INTERPRETER_VERSION_RE`, used at a
   command position with a literal name, is classified as a benign leaf command and derives
   no edge. That is the residual R3-F1 surface. It is smaller than round 3's - which modelled
   only `bash`, `sh` and `python[3[.N]]` at four punctuation positions - but it is not zero.
   Executing an arbitrary program (`./child.sh`, `myprog`) is outside every modelled edge
   kind and always was; the composite makes no claim about it, and the pinned prover
   adjudicates the argv paths it can see.
4. Wrapper detection produces safe false stops by design. `find`, `time`, `env`, `xargs` and
   friends STOP even when their operands are harmless, because the composite does not model
   what they run.
5. **F10 now STOPs on every plan allocation absent from the pinned constants table**, with no
   "can this affect prover semantics" exemption. A composite whose plan legitimately declares
   a render-only allocation that is never a runtime constant will STOP and must either add
   the constant or drop the allocation. This is a deliberate false stop, chosen over a
   second modelled grammar.
6. A constants binding the plan does not allocate is still `RUNTIME_ONLY`, not a STOP, and
   the F10 claim sentence now says only what is proved: every allocation reconciled, every
   constant dispositioned. It does not claim the two inputs are one universe.
7. An allocation absent from constants STOPs F10 but does **not** withhold the constants map
   from the prover, because absence corrupts no value the prover re-resolves and the
   analysis-unit builder refuses independently any operand it cannot resolve from the pinned
   table. Every other reconciliation failure still blocks prover invocation. The composite
   verdict is already STOP in both cases, so nothing can be accepted on this path.
8. `R7`/`F9` now STOP whenever graph derivation was blocked, instead of PASSing vacuously
   over a domain no operand ever entered.
9. **The `.gitattributes` repair is inert until the Lead commits it.** Git reads checkout
   attributes from the committed tree, so a clone made before that commit still materialises
   CRLF. Section 6 proves the attribute works by committing it inside a throw-away
   repository; this repository has no commit from this round.
10. The `.gitattributes` covers this directory only. Every other byte-pinned artifact
    elsewhere in the repository - RP6, RP7, the block files, the preregistration drafts -
    has the same pre-existing exposure and is outside this fence. That is a disclosure to the
    Lead, not a claim that those are safe.
11. Round 4 drove no new prover-adapter arm. 28 of 33 remain undriven, per section 7.
12. Nothing in round 4 changes the permanent residual: the deployed identity is a declared,
    lexically canonical string, not a host-verified object. No host was contacted.
