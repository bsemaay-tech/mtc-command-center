# Self-QA - Section 10.2 composite proof, round 3

Date: 2026-08-11
Audit tier: T1 - bounded local-only non-economic Python tooling and fixtures
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`
Input commit: `35a15219`. Implementer: `claude-opus-5` xhigh (Max account), acting on the
round-2 Claude flagship audit `SEC102_CLAUDE_T1_AUDIT_R2_2026-08-11.md` (verdict `BLOCK`).

This is implementer self-QA, not Gate-5 acceptance. The owning Lead must execute the
published harness verbatim before audit dispatch and independently inspect the actual diff.
Codex `gpt-5.6-sol` audits round 3 as the independent cross-model flagship.

Every fenced block below begins with `Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'` and uses
no undeclared shell state, so each block is literally paste-and-run from any working
directory. This closes the round-2 reproduction note (the round-2 harness silently
mis-asserted `rc 2` from any other cwd).

No remote host, network request, shell subject, block, wrapper, preregistration draft,
broker, trading surface, Pine file, parity file, schema, deployment action, or Git write was
invoked. `sec102_r3_fixtures/evil/library.sh` contains `cat /etc/shadow` and a `curl` to
`exfil.example.invalid` as **static fixture text**; it is parsed as data by the pinned
prover and is never executed. `.invalid` is a reserved, unresolvable TLD. The only
subprocess is the pinned CPython invocation of the pinned `pathscope_prover.py`.

## 1. What round 3 changed

| Round-2 finding | Repair | New RED |
|---|---|---|
| F1 CRITICAL - operand bound to a member by **basename**, so analysed bytes are not the sourced bytes | New required schema key `deploy_path` per member at RENDER/FREEZE; operand binds only by exact canonical deployed-path equality; both basename lookups deleted; unbound operand is STOP | `red_freeze_deploy_identity.json` |
| F2 CRITICAL - plan allocations and `constants.env` are two unreconciled value sources | `constants.env` parsed with a narrower mirror of the prover's own grammar; every shared name must be byte-equal or the composite STOPs before the prover is invoked; the analysis-unit builder additionally requires allocation value == constants value == `deploy_path` per source operand | `red_freeze_allocation_constants.json` |
| F3 MEDIUM - RENDER claimed graph closure while silently skipping non-shell members | `_derive_graph` records `member_kind_graph_derivation_not_modeled` STOP and blocks derivation, mirroring what FREEZE already did | `red_render_non_shell_member.json` |
| N1 - undriven adapter arms uncounted | Exact census published in section 6; three previously undriven arms now driven by fixtures | `red_freeze_execute_source_edge.json`, `red_freeze_source_site_not_standalone.json`, `red_freeze_zero_facts.json` |
| N2 - D026 RED was schema-level, not behavioural | Every falsification now carries a **behavioural** pre-feature RED against the exact round-2 code at `35a15219` plus a mutation discriminator against current code | section 3, section 4 |

Two round-2 fixtures were repointed and two allowlist fixtures were added, because the new
allocation/constants reconciliation now intercepts an unparsable `constants.env` at the
composite level, before the prover runs. `red_freeze_prover_grammar.json` and
`red_freeze_residual.json` previously drove their arms through `constants_bad.env`; they now
drive the same arms through an allowlist the pinned prover's own grammar refuses, so both
keep their published rc and reason token **and** keep their original semantics of "the
prover ran and returned degenerate output". `constants_bad.env` is retained and now drives
the new `red_freeze_constants_grammar.json`.

The two repointed fixtures were given **different** allowlists on purpose:
`red_freeze_prover_grammar.json` uses `allowlist_unparsable.txt` (`/**`, which reduces to an
empty path rule) and `red_freeze_residual.json` uses `allowlist_glob.txt`
(`/safe/fix*ture/**`, refused by the prover's glob check). As committed at `35a15219` those
two round-2 plans were **byte-identical** - both SHA-256 `d78d431f...5d53` - so the round-2
matrix asserted two different tokens against one artifact. They are now two distinct
artifacts driven by two distinct prover-side rejections.

## 2. Literal all-case assertion command

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r1='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
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
  @('freeze',$r2,'green_freeze_network.json',0,'resolved_net_endpoint_count=1')
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
if($failed){exit 1}
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
CASES=37 FAILED_COUNT=0
```

Command rc: `0`. The 26 round-2 cases are included unchanged in rc and reason token; the 11
new cases are round-3 additions.

## 3. D026 RED before GREEN - behavioural pre-feature falsification

This is the round-2 N2 repair. Each falsification is expressed twice: once in the round-2
member schema, run against the **exact round-2 code streamed from `35a15219`** (no file is
checked out or overwritten), and once in the round-3 schema against current code. The
round-2 run is a real behavioural PASS over a defective program, not a schema rejection.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$fx=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures').Path
$old='35a15219:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
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
  @('freeze','prefeature_freeze_deploy_identity.json','red_freeze_deploy_identity.json'),
  @('freeze','prefeature_freeze_allocation_constants.json','red_freeze_allocation_constants.json'),
  @('render','prefeature_render_non_shell_member.json','red_render_non_shell_member.json'))){
  $stage=$case[0]; $before=$case[1]; $after=$case[2]
  "D026 STAGE=$stage PREFEATURE=$before REPAIRED=$after"
  $out=($driver | python -B - $tool $old $stage (Join-Path $fx $before))
  $rcBefore=$LASTEXITCODE
  $out | Where-Object { $_ -match '^(DERIVED_EDGE |PROVER_RECORD |COMPOSITE_PATHPROOF verdict=)' }
  $out=(& python -B $tool $stage (Join-Path $fx $after))
  $rcAfter=$LASTEXITCODE
  $out | Where-Object { $_ -match '^(DERIVED_EDGE |COMPOSITE_PATHPROOF verdict=)' }
  "RC_PREFEATURE=$rcBefore RC_REPAIRED=$rcAfter"
}
```

Real output:

```text
D026 STAGE=freeze PREFEATURE=prefeature_freeze_deploy_identity.json REPAIRED=red_freeze_deploy_identity.json
DERIVED_EDGE composite="fixture-divergent" source="entry" target="library" kind="source" operand="/safe/fixture/evil/library.sh" disposition="DERIVED" reason="rendered_source_site"
PROVER_RECORD composite="fixture-divergent" member="fixture-divergent" index=0 record="PATH value=/safe/fixture/WPI-FIXTURE-FREEZE/input.txt verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=ROOT,RUNID uses=line=10:cat" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-divergent" member="fixture-divergent" index=1 record="PATH value=/safe/fixture/evil/library.sh verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=LIBRARY_PATH uses=line=5:test" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-divergent" member="fixture-divergent" index=2 record="PATH value=/safe/fixture/shared.txt verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=ROOT uses=line=8:cat" disposition="ACCOUNTED"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
DERIVED_EDGE composite="fixture-divergent" source="entry" target="-" kind="source" operand="/safe/fixture/evil/library.sh" disposition="STOP" reason="source_operand_deploy_identity_unbound"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
D026 STAGE=freeze PREFEATURE=prefeature_freeze_allocation_constants.json REPAIRED=red_freeze_allocation_constants.json
DERIVED_EDGE composite="fixture-p0" source="entry" target="library" kind="source" operand="/safe/fixture/library.sh" disposition="DERIVED" reason="rendered_source_site"
PROVER_RECORD composite="fixture-p0" member="fixture-p0" index=0 record="PATH value=/safe/fixture/WPI-FIXTURE-FREEZE/input.txt verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=ROOT,RUNID uses=line=10:cat" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-p0" member="fixture-p0" index=1 record="PATH value=/safe/fixture/shared.txt verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=ROOT uses=line=8:cat" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-p0" member="fixture-p0" index=2 record="PATH value=/safe/fixture/somewhere/else/library.sh verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=LIBRARY_PATH uses=line=5:test" disposition="ACCOUNTED"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
DERIVED_EDGE composite="fixture-p0" source="entry" target="library" kind="source" operand="/safe/fixture/library.sh" disposition="DERIVED" reason="rendered_source_site"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
D026 STAGE=render PREFEATURE=prefeature_render_non_shell_member.json REPAIRED=red_render_non_shell_member.json
DERIVED_EDGE composite="fixture-ro" source="entry" target="verifier" kind="execute_source" operand="/safe/fixture/verifier.py" disposition="DERIVED" reason="rendered_execute_site"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
DERIVED_EDGE composite="fixture-ro" source="entry" target="verifier" kind="execute_source" operand="/safe/fixture/verifier.py" disposition="DERIVED" reason="rendered_execute_site"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
RC_PREFEATURE=0 RC_REPAIRED=3
```

Read the F1 pair carefully: under round-2 code the derived edge claims `entry -> library`
while the operand is `/safe/fixture/evil/library.sh`, and the only fact the prover ever
learned about that path is `uses=line=5:test` - a readability probe. The bytes it analysed
were the pinned benign `library` member. That is the round-2 F1 defect reproduced
mechanically. Under round-3 code the same operand binds to nothing and the composite STOPs.

The F2 pair is the two-source defect: one `DERIVED_EDGE` row says `/safe/fixture/library.sh`
and one `PROVER_RECORD` row in the same report says
`/safe/fixture/somewhere/else/library.sh`, at `rc 0`.

## 4. D026 mutation discriminators against current code

Each mutation disables exactly the production comparison the corresponding new RED fixture
is supposed to depend on. The file on disk is never changed.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$fx=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures').Path

# --- F1: restore a basename fallback in both binding sites -------------------
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
$rc=$LASTEXITCODE
$out | Where-Object { $_ -match '^(CLAIM id="F9"|DERIVED_EDGE |COMPOSITE_PATHPROOF verdict=)' }
"MUTANT_RC=$rc REQUIRED_RED_RC=3"

# --- F2: disable both allocation/constants comparisons -----------------------
$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
mutations = {
  "        elif binding.value != allocation_values[binding.name]:":
    "        elif False and binding.value != allocation_values[binding.name]:",
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
$rc=$LASTEXITCODE
$out | Where-Object { $_ -match '^(CLAIM id="F10"|PROVER_RECORD .*LIBRARY_PATH|COMPOSITE_PATHPROOF verdict=)' }
"MUTANT_RC=$rc REQUIRED_RED_RC=3"

# --- F3: revert the non-shell graph STOP to the round-2 silent skip ----------
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
$rc=$LASTEXITCODE
$out | Where-Object { $_ -match '^(CLAIM id="R4"|RENDER_MEMBER .*verifier|COMPOSITE_PATHPROOF verdict=)' }
"MUTANT_RC=$rc REQUIRED_RED_RC=3"
```

Real output:

```text
MUTATION=F1_basename_fallback_restored CASE=red_freeze_deploy_identity.json
CLAIM id="F9" name="deployed_identity_binding" verdict="PASS" reason="every_derived_operand_equals_one_declared_member_deployed_path"
DERIVED_EDGE composite="fixture-divergent" source="entry" target="library" kind="source" operand="/safe/fixture/evil/library.sh" disposition="DERIVED" reason="rendered_source_site"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
MUTANT_RC=0 REQUIRED_RED_RC=3
MUTATION=F2_allocation_constants_comparisons_disabled CASE=red_freeze_allocation_constants.json
CLAIM id="F10" name="allocation_constants_reconciliation" verdict="PASS" reason="plan_allocations_and_pinned_constants_are_one_conserved_value_universe"
PROVER_RECORD composite="fixture-p0" member="fixture-p0" index=2 record="PATH value=/safe/fixture/somewhere/else/library.sh verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=LIBRARY_PATH uses=line=5:test" disposition="ACCOUNTED"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
MUTANT_RC=0 REQUIRED_RED_RC=3
MUTATION=F3_non_shell_graph_stop_reverted CASE=red_render_non_shell_member.json
CLAIM id="R4" name="derived_source_graph" verdict="PASS" reason="rendered_bytes_derive_the_declared_reachable_graph"
RENDER_MEMBER composite="fixture-ro" index=1 id="verifier" kind="python_source" path="verifier.py" deploy_path="/safe/fixture/verifier.py" graph="REACHABLE" materialisation="PASS" reason="materialised_byte_exact" bytes=74 sha256="1a2963fbf1b560d5e3cad96669971edce15f6186a11785c80a2f7cf1d0d256ba" disposition="ACCEPT"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
MUTANT_RC=0 REQUIRED_RED_RC=3
```

The unmutated fixtures return `rc 3` in the all-case matrix above; therefore each RED
discriminates on the intended comparison and not on some other property of its plan.

## 5. Real prover mapping output, round-3 cases

The filtering is part of the command, so the quoted output is literal output of the
published command rather than an edited excerpt.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
foreach($name in @('red_freeze_deploy_identity.json','red_freeze_divergent_control.json','red_freeze_zero_facts.json')){
  "CASE=$name"
  $out=(& python -B $tool freeze (Join-Path $r3 $name))
  $rc=$LASTEXITCODE
  $out | Where-Object { $_ -match '^(DERIVED_EDGE |PROVER_MEMBER |PROVER_RECORD |RESIDUAL |COMPOSITE_PATHPROOF verdict=)' }
  "COMMAND_RC=$rc"
}
```

Real output:

```text
CASE=red_freeze_deploy_identity.json
DERIVED_EDGE composite="fixture-divergent" source="entry" target="-" kind="source" operand="/safe/fixture/evil/library.sh" disposition="STOP" reason="source_operand_deploy_identity_unbound"
RESIDUAL composite="fixture-divergent" id="R1_MOUNT_BOUNDARY_NOT_ESTABLISHED" disposition="STOP" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-divergent" id="R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED" disposition="STOP" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-divergent" id="R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="deploy_path_is_declared_and_lexically_compared_not_host_verified"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
COMMAND_RC=3
CASE=red_freeze_divergent_control.json
DERIVED_EDGE composite="fixture-divergent-control" source="entry" target="library" kind="source" operand="/safe/fixture/evil/library.sh" disposition="DERIVED" reason="rendered_source_site"
PROVER_MEMBER composite="fixture-divergent-control" member="fixture-divergent-control" process_rc=1 resolved_fs_path_count=4 resolved_net_endpoint_count=1 unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0 terminal="REJECT:1:path_outside_allowlist" disposition="FAIL" reason="prover_forbidden_operand"
PROVER_RECORD composite="fixture-divergent-control" member="fixture-divergent-control" index=0 record="PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=8:cat" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-divergent-control" member="fixture-divergent-control" index=1 record="PATH value=/safe/fixture/WPI-FIXTURE-FREEZE/input.txt verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=ROOT,RUNID uses=line=11:cat" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-divergent-control" member="fixture-divergent-control" index=2 record="PATH value=/safe/fixture/evil/library.sh verdict=ALLOW-LEXICAL rule=/safe/fixture/** sources=LIBRARY_PATH uses=line=5:test" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-divergent-control" member="fixture-divergent-control" index=3 record="PATH value=/tmp/loot verdict=FORBID rule=- sources=NONE uses=line=9:curl" disposition="ACCOUNTED"
PROVER_RECORD composite="fixture-divergent-control" member="fixture-divergent-control" index=4 record="ENDPOINT value=exfil.example.invalid:443 verdict=FORBID rule=- sources=ROOT uses=line=9:curl" disposition="ACCOUNTED"
RESIDUAL composite="fixture-divergent-control" id="R1_MOUNT_BOUNDARY_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-divergent-control" id="R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-divergent-control" id="R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="deploy_path_is_declared_and_lexically_compared_not_host_verified"
COMPOSITE_PATHPROOF verdict=FAIL rc=1 reason=freeze_stage_deviant
COMMAND_RC=1
CASE=red_freeze_zero_facts.json
PROVER_MEMBER composite="fixture-zero" member="fixture-zero" process_rc=0 resolved_fs_path_count=0 resolved_net_endpoint_count=0 unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0 terminal="PASS:0:closed_and_allowlisted_lexical_argv_scope" disposition="PASS" reason="prover_closed_and_allowlisted_lexical_scope"
RESIDUAL composite="fixture-zero" id="R1_MOUNT_BOUNDARY_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-zero" id="R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-zero" id="R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="deploy_path_is_declared_and_lexically_compared_not_host_verified"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
COMMAND_RC=3
```

`red_freeze_divergent_control.json` is the control for F1 and is the reason the F1 RED means
something. It is the same entry bytes and the same allocation, with the real
`evil/library.sh` declared as a member at its own `deploy_path`. The operand then binds by
exact identity, the analysis unit carries the real 95-byte child, and the prover resolves
four filesystem paths and one endpoint, forbidding `/etc/shadow`, `/tmp/loot` and
`exfil.example.invalid:443`. The sinks are catchable; round 2 simply never showed them to
the prover.

`red_freeze_zero_facts.json` drives the Pattern-12 rule directly: the pinned prover returns
`PASS:0` with zero resolved facts and the composite still refuses at `rc 3`.

## 6. Adapter-arm census - the round-2 N1 repair

Exact counts, re-derived by the published command rather than asserted:

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
      + sorted(base.glob("sec102_r3_fixtures/red_*.json"))
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

**5 of 33 adapter arms are driven by a published fixture. 28 are carried undriven.** They
are not one category, and this document does not call any of them driven:

| Undriven class | Count | Why it is not driven |
|---|---|---|
| Prover-output reconciliation arms (`prover_stderr_nonempty`, `prover_output_unknown_record`, `prover_resolved_count_mismatch`, `prover_unresolved_kind_*`, `prover_issue_*`, `prover_*_disposition_*`, `prover_process_terminal_rc_mismatch`, `prover_forbid_*`, `prover_pass_*`) | 17 | Each requires the **pinned** prover to contradict its own output grammar. No plan can produce them while `pathscope_prover.py` is pinned at 122446 B / `890016f0...af1d`. Round 2 drove the equivalent claim by mutation instead, and that mutation is still in `SELF_QA_SEC102_R2.md`. |
| Analysis-unit arms shadowed by an earlier composite STOP (`analysis_unit_member_*`, `analysis_unit_source_cycle`, `analysis_unit_source_edge_unbound`, `analysis_unit_source_operand_dynamic`, `analysis_unit_source_operand_deploy_identity_unbound`, `analysis_unit_source_operand_constants_divergent`) | 10 | The same condition is caught earlier - by `_derive_graph`, by the member pins, or by the F10 reconciliation - so the builder's own copy of the check is defence in depth and never reached. `analysis_unit_source_operand_constants_divergent` in particular is unreachable **by construction** while F10 is enabled; it exists so that removing F10 does not silently reopen F2. |
| `prover_shell_member_set_empty` | 1 | `run_freeze` only invokes the adapter when every declared member has a verified snapshot, so an empty shell-member set cannot reach it. |

Three arms that round 2 carried undriven are now driven by fixtures:
`analysis_unit_non_source_edge_not_integrated`, `analysis_unit_source_site_not_standalone`
and `prover_zero_facts_pass`. The first two are the arms that enforce STATUS limitations 3
and 4; the third is the Pattern-12 zero-fact guard.

## 7. Syntax, grammar, determinism, and protected-component checks

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
$r3='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r3_fixtures'
python -B -c "import ast,pathlib; p=pathlib.Path(r'$tool'); t=ast.parse(p.read_text(encoding='utf-8'),filename=str(p),feature_version=(3,12)); names=sorted({a.name.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.Import) for a in n.names}|{n.module.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.ImportFrom) and n.module}); print('AST_PARSE_3_12=PASS'); print('IMPORTS='+','.join(names))"
python -B -c "import json,pathlib; files=sorted(pathlib.Path(r'$r2').glob('*.json'))+sorted(pathlib.Path(r'$r3').glob('*.json')); [json.loads(p.read_text(encoding='utf-8')) for p in files]; print(f'JSON_PARSE=PASS count={len(files)}')"
python -B -c "import pathlib; bad=[p.as_posix() for p in list(pathlib.Path(r'$r2').rglob('*'))+list(pathlib.Path(r'$r3').rglob('*')) if p.is_file() and b'\r' in p.read_bytes()]; print('FIXTURE_LF_ONLY='+('PASS' if not bad else 'FAIL '+','.join(bad)))"
git diff --check -- $tool $r2 $r3
"DIFF_CHECK_RC=$LASTEXITCODE"
"PROVER_WORKTREE_DIFF_BEGIN"
git diff --name-only -- 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py'
"PROVER_WORKTREE_DIFF_END"
git status --porcelain -- 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r1_fixtures'
"R1_FIXTURE_STATUS_END"
$determinism=@'
import hashlib, io, pathlib, sys, contextlib
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
code = compile(source, str(path), "exec")
for stage, plan in (("render", sys.argv[2]), ("freeze", sys.argv[3])):
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
    print(f"DETERMINISM stage={stage} rc1={codes[0]} rc2={codes[1]} "
          f"equal={digests[0] == digests[1]} sha1={digests[0]} sha2={digests[1]}")
'@
$determinism | python -B - $tool (Join-Path $r2 'green_render.json') (Join-Path $r2 'green_freeze.json')
```

Real output. One elision is declared: the `git diff --check` line also writes Git's
repository-wide `warning: ... LF will be replaced by CRLF the next time Git touches it`
advisory to stderr, one line per modified file (18 lines in this run). Those advisory lines
are omitted from the quoted block below and are explained in section 8; nothing else is
removed.

```text
AST_PARSE_3_12=PASS
IMPORTS=__future__,argparse,dataclasses,enum,hashlib,json,pathlib,posixpath,re,shlex,subprocess,sys,tempfile,typing
JSON_PARSE=PASS count=33
FIXTURE_LF_ONLY=PASS
DIFF_CHECK_RC=0
PROVER_WORKTREE_DIFF_BEGIN
PROVER_WORKTREE_DIFF_END
R1_FIXTURE_STATUS_END
DETERMINISM stage=render rc1=0 rc2=0 equal=True sha1=c2fdb5bf0af1f5c9d1c8ab7b2536e46db4d06a29a05aba2a9abe8970c24f33f8 sha2=c2fdb5bf0af1f5c9d1c8ab7b2536e46db4d06a29a05aba2a9abe8970c24f33f8
DETERMINISM stage=freeze rc1=0 rc2=0 equal=True sha1=be48a5fe83eaabb0e50c0887b43a8bc95531f7b6938e7909acbf74526c8379da sha2=be48a5fe83eaabb0e50c0887b43a8bc95531f7b6938e7909acbf74526c8379da
```

`pathscope_prover.py` has no worktree diff and `sec102_r1_fixtures` has no status entry, so
the round-1 ALLOCATE baseline is byte-unchanged. The prover identity was independently
re-derived as 122446 bytes and SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`.

## 8. Note to the Lead - a line-ending durability risk found while running section 7

This is outside the round-3 repair scope and is **not applied**; it is reported because it
affects whether the Lead can reproduce this matrix after a fresh checkout.

```powershell
Set-Location 'C:\LAB\Tradingview_LAB_CLEAN'
git config core.autocrlf
git ls-files --eol MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r2_fixtures/entry.sh
```

```text
true
i/lf    w/lf    attr/text=auto          MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r2_fixtures/entry.sh
```

The repository root `.gitattributes` sets `* text=auto` and this clone sets
`core.autocrlf=true`. Every fixture is LF in the index and LF in the current worktree, which
is why all pins match today. A **fresh checkout or clone on Windows would materialise these
files as CRLF**, changing every member, constants and allowlist byte count, and the whole
FREEZE matrix would then fail with `frozen_identity_mismatch`. The one-line remedy is a
`.gitattributes` entry marking the fixture trees binary, e.g.
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r*_fixtures/** -text`. That
file is outside the round-3 scope fence, so the decision is the Lead's. The risk is
pre-existing: it applies equally to the round-2 fixture set as committed at `35a15219`.

## 9. Limitations - disclosures, not controls

1. The FREEZE PASS is lexical static proof only. It does not establish the host object
   behind a path. Symlink and mount-boundary non-establishment are emitted as R1 residual
   disclosures with `control=false`.
2. **The deployed identity this round adds is a declared, lexically canonical string
   compared for exact equality. It is not host-object verification.** No host was contacted.
   Every FREEZE report now carries `R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED` as a
   permanent `control=false` disclosure. A plan that declares `deploy_path` truthfully gets
   a true binding; a plan that declares it falsely is not detected by this stage.
3. Operand-to-member binding requires the operand to be **already** absolute and lexically
   canonical. A `..` component is never collapsed, because collapsing it lexically is
   unsound when any prefix is a symlink. Such an operand STOPs rather than binding.
4. ALLOCATE does not declare or check `deploy_path`. It remains a declaration-conservation
   and local-identity stage and makes no whole-program path claim, so the round-1 fixture
   set is untouched.
5. The constants mirror is deliberately **narrower** than the pinned prover's
   `parse_constants`: the prover expands `$NAME` inside a constant value against earlier
   constants, and this mirror refuses such a value with `constants_value_not_literal`
   instead of modelling it. That is a safe false stop, not claimed coverage.
6. A constants binding whose name the plan does not allocate is reported as
   `RUNTIME_ONLY` and counted in `CONSTANTS_CONSERVATION`, not stopped. It cannot influence
   member binding, because a source operand only resolves through plan allocations, and any
   path or endpoint it produces is still adjudicated against the pinned allowlist. It is
   nonetheless a value the plan did not declare, and it is disclosed as such.
7. FREEZE accepts only composites whose reachable members are all shell source. Any
   `python_source` member STOPs at FREEZE, and from this round also STOPs graph derivation
   at RENDER. The actual RO composite still cannot PASS.
8. The analysis-unit builder supports standalone direct `source`/`.` edges only.
   `execute_source` and `inline_source` edges STOP before prover invocation, now driven by
   `red_freeze_execute_source_edge.json`.
9. RENDER graph derivation intentionally STOPs on here-documents, line continuations,
   multiline quotes, command/process substitutions, `eval`, `alias`, and dynamic command
   positions. These are safe false stops.
10. The analysis unit replaces each bound standalone source statement with a synthetic
    `test -r` operand plus the exact pinned child bytes. The operand is left **raw**, so the
    prover must re-resolve it from the pinned constants; that is what makes the F10
    reconciliation load-bearing rather than decorative. The unit is parser input only and is
    never executed.
11. Allocation-consumer conservation proves declared template-token materialisation,
    allocation/constants value conservation, and exact deployed-path binding of source
    operands. It is not a full shell dataflow proof for every use of an allocated value.
12. The adapter carries verified byte snapshots into the invocation, but the local
    `sys.executable` used to launch the pinned prover is an external-runtime dependency not
    pinned by the plan.
13. The adapter creates and removes a temporary local directory holding the analysis unit
    and the exact prover, constants and allowlist snapshots. Those files are not frozen
    artifacts; a temp creation or write failure is STOP.
14. Runtime-selected descendants and external-runtime internal opens remain outside the
    exact lexical set. No runtime-family manifest is implemented.
15. A prover input-read or constants/allowlist parse error yields only the prover's terminal
    rc-3 line, not the seven count records. The composite treats that incomplete grammar as
    STOP; it never defaults absent counts to zero.
16. No archive was created or frozen. A fixture FREEZE PASS is not permission to dispatch,
    contact a host, or claim the production Section 10.2 gate closed.
