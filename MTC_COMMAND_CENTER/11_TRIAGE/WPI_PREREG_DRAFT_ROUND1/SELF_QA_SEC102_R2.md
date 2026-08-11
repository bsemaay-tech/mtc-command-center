# Self-QA - Section 10.2 composite proof, round 2

Date: 2026-08-11  
Audit tier: T1 - bounded local-only non-economic Python tooling and fixtures  
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`

This is implementer self-QA, not Gate-5 acceptance. The owning Lead must execute the
published harness verbatim before audit dispatch and independently inspect the actual
diff. The implementation diff exceeds 300 lines, so the T1 policy also requires the
conditional GLM-5.2 second-opinion slot after the flagship review.

No remote host, network request, shell subject, block, wrapper, preregistration draft,
broker, trading surface, Pine file, parity file, schema, deployment action, or Git write
was invoked. The `entry_network.sh` fixture contains a URL as static text; it was parsed
as data and was never executed. The only subprocess is the pinned CPython invocation of
the pinned `pathscope_prover.py`; that prover reads shell, constants, and allowlist bytes
as data.

## Implemented claims

### RENDER

| Claim | Bounded claim | RED fixture | Expected RED |
|---|---|---|---|
| R1 | The strict v1 envelope declares the render stage. | `red_render_contract.json` | STOP rc 3 |
| R2 | Every input member has exactly one distinct template binding. | `red_render_template_conservation.json` | FAIL rc 1 |
| R3 | Every declared consumer token is substituted byte-for-byte and no token survives. | `red_render_materialisation.json` | FAIL rc 1 |
| R4 | Direct, modeled source edges are derived from rendered bytes and reach all members. | `red_render_graph_dynamic.json` | STOP rc 3 |
| R5 | Every rendered member is a readable, regular, non-symlink in-bundle file with identity. | `red_render_identity.json` | STOP rc 3 |
| R6 | Every input member gets one terminal render disposition. | `red_render_member_disposition.json` | FAIL rc 1 |

`red_render_heredoc_false_edge.json` is an additional Pattern-12 falsification. A line
that merely says `source library.sh` inside a here-document must not manufacture a graph
edge. The graph derivation STOPs because here-document semantics are outside its modeled
grammar.

### FREEZE and prover integration

| Claim | Bounded claim | RED fixture | Expected RED |
|---|---|---|---|
| F1 | The strict v1 envelope declares the freeze stage and allocations remain closed. | `red_freeze_contract.json` | STOP rc 3 |
| F2 | Every member, constants file, and allowlist file matches its frozen byte count and SHA-256. | `red_freeze_member_pin.json` | overall STOP rc 3; observed pin mismatch is FAIL |
| F3 | The graph re-derived from frozen bytes reaches every member. | `red_freeze_graph.json` | overall STOP rc 3; graph claim FAIL |
| F4 | The invoked prover is exactly 122446 bytes and SHA-256 `890016f0...af1d`. | `red_freeze_prover_pin.json` | overall STOP rc 3; identity claim FAIL |
| F5 | The adapter reconciles both resolved counters, all five issue counters, every record, and the terminal/process rc. | `red_freeze_prover_grammar.json` | STOP rc 3 |
| F6 | Prover coverage/unresolved is STOP; outside-allowlist is FAIL; only closed lexical scope is PASS. | `red_freeze_coverage.json`, `red_freeze_forbidden.json` | STOP rc 3; FAIL rc 1 |
| F7 | Symlink and mount non-establishment are explicit residual disclosures, never controls. | `red_freeze_residual.json` | STOP rc 3 |
| F8 | Every input member gets one terminal freeze disposition. | `red_freeze_member_disposition.json` | STOP rc 3 |

`green_freeze_network.json` separately drives the new network counter and `ENDPOINT`
record grammar without contacting the endpoint.

## Literal all-case assertion command

This exact command was executed after the final code changes. RED cases precede their
stage GREEN. The two additional cases are included after the claim matrix.

```powershell
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$r1='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$r2='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
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
CASE=green_freeze.json STAGE=freeze RC=0 EXPECTED=0 TOKEN=freeze_stage_closed ASSERT=PASS
CASE=green_freeze_network.json STAGE=freeze RC=0 EXPECTED=0 TOKEN=resolved_net_endpoint_count=1 ASSERT=PASS
```

Command rc: `0`.

## Real prover mapping output

The following literal command reports only the adapter summary, residual, and terminal
records. The filtering is part of the command, so the quoted output is literal output of
the published command rather than an edited excerpt.

```powershell
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$fx='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
foreach($name in @('red_freeze_coverage.json','red_freeze_forbidden.json','green_freeze_network.json')){
  "CASE=$name"
  python -B $tool freeze (Join-Path $fx $name) |
    Select-String -Pattern '^PROVER_MEMBER |^RESIDUAL |^COMPOSITE_PATHPROOF verdict='
  "COMMAND_RC=$LASTEXITCODE"
}
```

Real output:

```text
CASE=red_freeze_coverage.json
PROVER_MEMBER composite="fixture-p0" member="fixture-p0" process_rc=3 resolved_fs_path_count=2 resolved_net_endpoint_count=0 unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=2 provenance_issue_count=0 parse_issue_count=0 terminal="REJECT:3:static_resolution_incomplete" disposition="STOP" reason="prover_static_resolution_incomplete"
RESIDUAL composite="fixture-p0" id="R1_MOUNT_BOUNDARY_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-p0" id="R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
COMMAND_RC=3
CASE=red_freeze_forbidden.json
PROVER_MEMBER composite="fixture-p0" member="fixture-p0" process_rc=1 resolved_fs_path_count=3 resolved_net_endpoint_count=0 unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0 terminal="REJECT:1:path_outside_allowlist" disposition="FAIL" reason="prover_forbidden_operand"
RESIDUAL composite="fixture-p0" id="R1_MOUNT_BOUNDARY_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-p0" id="R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
COMPOSITE_PATHPROOF verdict=FAIL rc=1 reason=freeze_stage_deviant
COMMAND_RC=1
CASE=green_freeze_network.json
PROVER_MEMBER composite="fixture-network" member="fixture-network" process_rc=0 resolved_fs_path_count=1 resolved_net_endpoint_count=1 unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0 terminal="PASS:0:closed_and_allowlisted_lexical_argv_scope" disposition="PASS" reason="prover_closed_and_allowlisted_lexical_scope"
RESIDUAL composite="fixture-network" id="R1_MOUNT_BOUNDARY_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
RESIDUAL composite="fixture-network" id="R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED" disposition="DISCLOSURE" control=false reason="lexical_prover_does_not_establish_host_object_binding"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
COMMAND_RC=0
```

## D026 RED before GREEN

### Exact round-1 behavior

The exact round-1 code at commit `73e92844` was streamed from Git into Python; no file was
checked out or overwritten. Both new GREEN plans are RED against that exact pre-feature
behavior.

```powershell
$old='73e92844:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py'
$fx='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
foreach($case in @(@('render','green_render.json'),@('freeze','green_freeze.json'))){
  $stage=$case[0]; $name=$case[1]
  "D026_PREFX CASE=$name"
  git show $old | python -B - $stage (Join-Path $fx $name) |
    Select-String -Pattern '^INPUT |^COMPOSITE_PATHPROOF verdict='
  "COMMAND_RC=$LASTEXITCODE EXPECTED_CURRENT_GREEN=0"
}
```

Real output:

```text
D026_PREFX CASE=green_render.json
INPUT disposition="STOP" reason="plan_schema_unknown_key" detail="plan.composites[0]:proof"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
COMMAND_RC=3 EXPECTED_CURRENT_GREEN=0
D026_PREFX CASE=green_freeze.json
INPUT disposition="STOP" reason="plan_schema_unknown_key" detail="plan.composites[0]:proof"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
COMMAND_RC=3 EXPECTED_CURRENT_GREEN=0
```

The current-code GREEN results are in the all-case harness: render rc 0 and freeze rc 0.

### Render byte-comparison mutation

This in-memory mutation disables the one production comparison that distinguishes a
wrong rendered byte stream. The file on disk is not changed.

```powershell
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$plan=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures\red_render_materialisation.json').Path
$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
old = "if expected != rendered_data:"
assert source.count(old) == 1
source = source.replace(old, "if False and expected != rendered_data:")
sys.argv = [str(path), "render", sys.argv[2]]
namespace = {"__name__": "__main__", "__file__": str(path)}
exec(compile(source, str(path), "exec"), namespace)
'@
$out=($driver | python -B - $tool $plan)
$rc=$LASTEXITCODE
$out | Select-String -Pattern '^CLAIM id="R3"|^COMPOSITE_PATHPROOF verdict='
"MUTANT_RC=$rc REQUIRED_RED_RC=1"
```

Real output:

```text
CLAIM id="R3" name="allocation_materialisation" verdict="PASS" reason="every_declared_consumer_materialised_byte_exact"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
MUTANT_RC=0 REQUIRED_RED_RC=1
```

The unmutated fixture returns FAIL rc 1 with `rendered_bytes_mismatch`; therefore the RED
fixture discriminates on the intended byte comparison.

### Coverage/terminal mapping mutation

This in-memory mutation disables the production issue branch and its PASS-terminal checks.
It proves that the coverage fixture would catch a composite that converted a prover STOP
into PASS.

```powershell
$tool=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py').Path
$plan=(Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures\red_freeze_coverage.json').Path
$driver=@'
import pathlib, sys
path = pathlib.Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
mutations = {
  "if total_issues:": "if False and total_issues:",
  "if terminal_verdict != \"PASS\" or terminal_rc != RC_PASS:": "if False and (terminal_verdict != \"PASS\" or terminal_rc != RC_PASS):",
  "if terminal_reason != \"closed_and_allowlisted_lexical_argv_scope\":": "if False and terminal_reason != \"closed_and_allowlisted_lexical_argv_scope\":"
}
for old, new in mutations.items():
  assert source.count(old) == 1, old
  source = source.replace(old, new)
sys.argv = [str(path), "freeze", sys.argv[2]]
namespace = {"__name__": "__main__", "__file__": str(path)}
exec(compile(source, str(path), "exec"), namespace)
'@
$out=($driver | python -B - $tool $plan)
$rc=$LASTEXITCODE
$out | Select-String -Pattern '^CLAIM id="F5"|^CLAIM id="F6"|^PROVER_MEMBER |^COMPOSITE_PATHPROOF verdict='
"MUTANT_RC=$rc REQUIRED_RED_RC=3"
```

Real output:

```text
CLAIM id="F5" name="prover_output_conservation" verdict="PASS" reason="seven_counts_and_records_reconciled"
CLAIM id="F6" name="lexical_pathscope_disposition" verdict="PASS" reason="every_prover_result_terminal_and_fail_closed"
PROVER_MEMBER composite="fixture-p0" member="fixture-p0" process_rc=3 resolved_fs_path_count=2 resolved_net_endpoint_count=0 unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=2 provenance_issue_count=0 parse_issue_count=0 terminal="REJECT:3:static_resolution_incomplete" disposition="PASS" reason="prover_closed_and_allowlisted_lexical_scope"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=freeze_stage_closed
MUTANT_RC=0 REQUIRED_RED_RC=3
```

The unmutated fixture returns STOP rc 3 and records both coverage issues.

## Syntax, grammar, determinism, and protected-component checks

Literal command:

```powershell
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$fx='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r2_fixtures'
python -B -c "import ast,pathlib; p=pathlib.Path(r'$tool'); t=ast.parse(p.read_text(encoding='utf-8'),filename=str(p),feature_version=(3,12)); names=sorted({a.name.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.Import) for a in n.names}|{n.module.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.ImportFrom) and n.module}); print('AST_PARSE_3_12=PASS'); print('IMPORTS='+','.join(names))"
python -B -c "import json,pathlib; files=sorted(pathlib.Path(r'$fx').glob('*.json')); [json.loads(p.read_text(encoding='utf-8')) for p in files]; print(f'JSON_PARSE=PASS count={len(files)}')"
git diff --check -- $tool $fx
"DIFF_CHECK_RC=$LASTEXITCODE"
git diff --name-only -- 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py'
```

Real output after the final fixture set:

```text
AST_PARSE_3_12=PASS
IMPORTS=__future__,argparse,dataclasses,enum,hashlib,json,pathlib,posixpath,re,shlex,subprocess,sys,tempfile,typing
JSON_PARSE=PASS count=19
DIFF_CHECK_RC=0
```

The final command printed nothing: `pathscope_prover.py` has no worktree diff. Its identity
was independently re-derived as 122446 bytes and SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`.

Two in-process invocations of each GREEN used identical argv and compared complete stdout
plus rc. Real output:

```text
DETERMINISM stage=render rc1=0 rc2=0 equal=True sha1=1d68f18223168e5cf0d725713e791f4458064c4b22f5ce4ac8dbdc1dd3e88206 sha2=1d68f18223168e5cf0d725713e791f4458064c4b22f5ce4ac8dbdc1dd3e88206
DETERMINISM stage=freeze rc1=0 rc2=0 equal=True sha1=c4d187813a690621641adb26e542f7f71d2c2a78b280e00fc8715d95553f6370 sha2=c4d187813a690621641adb26e542f7f71d2c2a78b280e00fc8715d95553f6370
```

These determinism hashes predate only documentation writes; code and fixture bytes were
unchanged after this run.

## Limitations - disclosures, not controls

1. The FREEZE PASS is lexical static proof only. It does not establish the host object
   behind a path. Both symlink and mount-boundary non-establishment are emitted as R1
   residual disclosures with `control=false`.
2. The implemented GREENs are synthetic fixtures. No RP6, RP7, transport wrapper,
   bootstrap, inline Python body, candidate `verify_lock.py`, or successor preregistration
   was analyzed or frozen.
3. FREEZE currently accepts only composites whose reachable members are all shell source.
   Any `python_source` member STOPs with
   `non_shell_member_analyzer_not_integrated`. This means the actual RO composite cannot
   yet PASS.
4. The static analysis-unit builder supports standalone direct `source`/`.` edges only.
   `execute_source` and `inline_source` edges STOP before prover invocation. The actual RO
   composite therefore remains outside the passing subset.
5. RENDER graph derivation intentionally STOPs on here-documents, line continuations,
   multiline quotes, command/process substitutions, `eval`, `alias`, and dynamic command
   positions. These are safe false stops, not claimed coverage.
6. The analysis-unit builder replaces each mechanically bound standalone source statement
   with a synthetic `test -r` operand plus the exact pinned child bytes. This unit is input
   to a static parser only and is never executed. It is not a deployable shell artifact.
7. Allocation-consumer conservation proves declared template-token materialization and
   direct source-operand binding; it is not a full shell dataflow proof for every use of an
   allocated value.
8. The adapter pins `pathscope_prover.py`, constants, allowlist, and member bytes and then
   carries those exact verified byte snapshots into the invocation. The current local
   `sys.executable` used to launch the prover snapshot is an external-runtime dependency
   and is not itself pinned by the plan.
9. The adapter creates a temporary local directory containing the whole-program analysis
   unit plus exact prover, constants, and allowlist snapshots, then removes it through
   `TemporaryDirectory`. Those files are not part of the frozen artifact set. A temp
   creation or write failure is STOP.
10. Runtime-selected descendants and external-runtime internal opens remain outside the
    exact lexical set. The current fixtures exercise exact filesystem paths and one static
    endpoint; no runtime-family manifest is implemented.
11. A prover input-read or constants/allowlist parse error currently has only the prover's
    terminal rc-3 line, not the seven count records. The composite treats that incomplete
    grammar as STOP; it never defaults absent counts to zero.
12. No archive was created or frozen. A fixture FREEZE PASS is not permission to dispatch,
    contact a host, or claim the production Section 10.2 gate closed.
