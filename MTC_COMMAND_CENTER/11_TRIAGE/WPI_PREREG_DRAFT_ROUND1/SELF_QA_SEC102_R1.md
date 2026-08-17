# Self-QA - Section 10.2 composite proof, round 1

Date: 2026-08-11  
Audit tier: T1 - bounded local-only non-economic tooling  
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`

No host, network, subprocess, shell subject, block, wrapper, preregistration draft, or
existing path prover was invoked. Python read the fixture bytes as data. The installed
runtime was CPython 3.14.2; the source also parsed with Python 3.12 grammar.

## Claims and falsifications

Round 1 makes only these ALLOCATE-stage claims. The same `green.json` proves the GREEN
side of every claim after all six RED inputs are shown.

| Claim | Exact bounded claim | RED fixture | RED verdict |
|---|---|---|---|
| A1 | The plan uses the closed v1 schema and declares the allocate stage. | `red_plan_contract.json` | STOP, rc 3: unknown schema member means the plan cannot be evaluated. |
| A2 | Each composite's declared entrypoint names exactly one declared member. | `red_entrypoint.json` | FAIL, rc 1: the named entrypoint is absent. |
| A3 | Declared requirements, allocations, and consumer references conserve one-for-one. | `red_allocation_conservation.json` | FAIL, rc 1: one required allocation appears twice. |
| A4 | Each allocated value is present, placeholder-free, and valid for its declared kind. | `red_allocation_value.json` | STOP, rc 3: an angle-bracket placeholder is unresolved. |
| A5 | Traversal from the declared entrypoint reaches every member in the declared graph. | `red_graph_conservation.json` | FAIL, rc 1: one declared member is unreachable. |
| A6 | Every declared member resolves to one non-symlink, regular in-bundle file whose size and SHA-256 can be read. | `red_component_identity.json` | STOP, rc 3: the named bytes do not exist, so identity cannot be evaluated. |

The graph and consumer sets in round 1 are declarations checked for internal
conservation. They are not yet derived from shell/Python source semantics. Consequently,
A2/A3/A5 are deliberately named `declared_*` claims in tool output and are not a Section
10.2 whole-program acceptance proof.

## Exact RED-then-GREEN command

This literal PowerShell command ran all RED fixtures first, then the common GREEN fixture,
then the two fail-closed later-stage fixtures:

```powershell
$tool='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\composite_pathproof.py'
$fx='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\sec102_r1_fixtures'
$reds=@(
  'red_plan_contract.json',
  'red_entrypoint.json',
  'red_allocation_conservation.json',
  'red_allocation_value.json',
  'red_graph_conservation.json',
  'red_component_identity.json'
)
foreach($name in $reds){
  "FIXTURE=$name PHASE=RED"
  python -B $tool allocate (Join-Path $fx $name)
  "COMMAND_RC=$LASTEXITCODE"
}
"FIXTURE=green.json PHASE=GREEN"
python -B $tool allocate (Join-Path $fx 'green.json')
"COMMAND_RC=$LASTEXITCODE"
"FIXTURE=red_render_unimplemented.json PHASE=RED"
python -B $tool render (Join-Path $fx 'red_render_unimplemented.json')
"COMMAND_RC=$LASTEXITCODE"
"FIXTURE=red_freeze_unimplemented.json PHASE=RED"
python -B $tool freeze (Join-Path $fx 'red_freeze_unimplemented.json')
"COMMAND_RC=$LASTEXITCODE"
```

## Real RED output

### A1 - closed plan contract

```text
FIXTURE=red_plan_contract.json PHASE=RED
CLAIM id="A1" name="plan_contract" verdict="STOP" reason="plan_schema_unknown_key"
CLAIM id="A2" name="declared_entrypoint_discovery" verdict="STOP" reason="plan_schema_unknown_key"
CLAIM id="A3" name="allocation_plan_conservation" verdict="STOP" reason="plan_schema_unknown_key"
CLAIM id="A4" name="allocation_value_closure" verdict="STOP" reason="plan_schema_unknown_key"
CLAIM id="A5" name="declared_graph_conservation" verdict="STOP" reason="plan_schema_unknown_key"
CLAIM id="A6" name="component_identity" verdict="STOP" reason="plan_schema_unknown_key"
INPUT disposition="STOP" reason="plan_schema_unknown_key" detail="plan:unexpected"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=allocate_stage_incomplete
COMMAND_RC=3
```

Dependent claims STOP rather than vacuously PASS when the input schema cannot be
evaluated.

### A2 - declared entrypoint discovery

```text
FIXTURE=red_entrypoint.json PHASE=RED
CLAIM id="A2" name="declared_entrypoint_discovery" verdict="FAIL" reason="entrypoint_not_declared"
CLAIM id="A5" name="declared_graph_conservation" verdict="FAIL" reason="declared_graph_not_traversable"
MEMBER composite="fixture-p0" index=0 id="entry" kind="shell" path="entry.sh" graph="FAIL" identity="IDENTIFIED" bytes=126 sha256="0d20505106e238a717a6b0729deeae093a06bc700c3bfbfac8748c6f213e13fc" disposition="FAIL"
MEMBER composite="fixture-p0" index=1 id="library" kind="shell" path="library.sh" graph="FAIL" identity="IDENTIFIED" bytes=140 sha256="35958de1f651dc3d511d0ce56360e4add762add9e93e563c0ac55a64a61d70ec" disposition="FAIL"
CONSERVATION composite="fixture-p0" input_members=2 terminal_member_rows=2 reachable_members=0 input_edges=1 terminal_edge_rows=1 input_requirements=1 terminal_requirement_rows=1 input_allocations=1 terminal_allocation_rows=1 input_consumer_references=1 terminal_consumer_rows=1
COMPOSITE_PATHPROOF verdict=FAIL rc=1 reason=allocate_stage_deviant
COMMAND_RC=1
```

### A3 - allocation conservation

```text
FIXTURE=red_allocation_conservation.json PHASE=RED
CLAIM id="A3" name="allocation_plan_conservation" verdict="FAIL" reason="allocation_duplicate,allocation_not_one_to_one"
REQUIREMENT composite="fixture-p0" index=0 name="RUNID" kind="safe_component" consumers=["entry"] disposition="FAIL" reasons=["allocation_not_one_to_one"]
ALLOCATION composite="fixture-p0" index=0 name="RUNID" value="WPI-FIXTURE-P0" disposition="FAIL" reasons=["allocation_duplicate"]
ALLOCATION composite="fixture-p0" index=1 name="RUNID" value="WPI-FIXTURE-P0-SECOND" disposition="FAIL" reasons=["allocation_duplicate"]
CONSERVATION composite="fixture-p0" input_members=1 terminal_member_rows=1 reachable_members=1 input_edges=0 terminal_edge_rows=0 input_requirements=1 terminal_requirement_rows=1 input_allocations=2 terminal_allocation_rows=2 input_consumer_references=1 terminal_consumer_rows=1
COMPOSITE_PATHPROOF verdict=FAIL rc=1 reason=allocate_stage_deviant
COMMAND_RC=1
```

### A4 - allocated value closure

```text
FIXTURE=red_allocation_value.json PHASE=RED
CLAIM id="A4" name="allocation_value_closure" verdict="STOP" reason="allocation_value_unresolved"
ALLOCATION composite="fixture-p0" index=0 name="REMOTE_BASE" value="/home/gatea/wpi_staging_<ALLOCATE>" disposition="STOP" reasons=["allocation_value_unresolved"]
CONSERVATION composite="fixture-p0" input_members=1 terminal_member_rows=1 reachable_members=1 input_edges=0 terminal_edge_rows=0 input_requirements=1 terminal_requirement_rows=1 input_allocations=1 terminal_allocation_rows=1 input_consumer_references=1 terminal_consumer_rows=1
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=allocate_stage_incomplete
COMMAND_RC=3
```

### A5 - declared graph conservation

```text
FIXTURE=red_graph_conservation.json PHASE=RED
CLAIM id="A5" name="declared_graph_conservation" verdict="FAIL" reason="declared_member_unreachable"
MEMBER composite="fixture-p0" index=0 id="entry" kind="shell" path="entry.sh" graph="REACHABLE" identity="IDENTIFIED" bytes=126 sha256="0d20505106e238a717a6b0729deeae093a06bc700c3bfbfac8748c6f213e13fc" disposition="ACCEPT"
MEMBER composite="fixture-p0" index=1 id="library" kind="shell" path="library.sh" graph="FAIL" identity="IDENTIFIED" bytes=140 sha256="35958de1f651dc3d511d0ce56360e4add762add9e93e563c0ac55a64a61d70ec" disposition="FAIL"
CONSERVATION composite="fixture-p0" input_members=2 terminal_member_rows=2 reachable_members=1 input_edges=0 terminal_edge_rows=0 input_requirements=1 terminal_requirement_rows=1 input_allocations=1 terminal_allocation_rows=1 input_consumer_references=1 terminal_consumer_rows=1
COMPOSITE_PATHPROOF verdict=FAIL rc=1 reason=allocate_stage_deviant
COMMAND_RC=1
```

### A6 - component identity

```text
FIXTURE=red_component_identity.json PHASE=RED
CLAIM id="A6" name="component_identity" verdict="STOP" reason="member_file_missing"
MEMBER composite="fixture-p0" index=0 id="entry" kind="shell" path="missing.sh" graph="REACHABLE" identity="STOP" bytes="-" sha256="-" disposition="STOP"
CONSERVATION composite="fixture-p0" input_members=1 terminal_member_rows=1 reachable_members=1 input_edges=0 terminal_edge_rows=0 input_requirements=1 terminal_requirement_rows=1 input_allocations=1 terminal_allocation_rows=1 input_consumer_references=1 terminal_consumer_rows=1
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=allocate_stage_incomplete
COMMAND_RC=3
```

## Real GREEN output

`green.json` is the GREEN member for A1-A6. All six claims pass, every declared member,
edge, requirement, allocation, and consumer reference receives a terminal row, and the
unrepaired path prover remains explicitly not invoked.

```text
FIXTURE=green.json PHASE=GREEN
COMPOSITE_PATHPROOF schema="sec102-composite-plan-v1" requested_stage="allocate" plan="MTC_COMMAND_CENTER\\11_TRIAGE\\WPI_PREREG_DRAFT_ROUND1\\sec102_r1_fixtures\\green.json"
CONTRACT pass_rc=0 fail_rc=1 stop_rc=3 precedence=STOP>FAIL>PASS
CLAIM id="A1" name="plan_contract" verdict="PASS" reason="closed_schema_and_allocate_order"
CLAIM id="A2" name="declared_entrypoint_discovery" verdict="PASS" reason="one_declared_entrypoint_per_composite"
CLAIM id="A3" name="allocation_plan_conservation" verdict="PASS" reason="declared_requirements_allocations_and_consumer_references_conserved"
CLAIM id="A4" name="allocation_value_closure" verdict="PASS" reason="allocated_values_closed_and_well_formed"
CLAIM id="A5" name="declared_graph_conservation" verdict="PASS" reason="all_declared_members_reachable_once"
CLAIM id="A6" name="component_identity" verdict="PASS" reason="all_member_bytes_locally_identified"
EDGE composite="fixture-p0" index=0 source="entry" target="library" kind="source" disposition="ACCEPT" reasons=["declared"]
MEMBER composite="fixture-p0" index=0 id="entry" kind="shell" path="entry.sh" graph="REACHABLE" identity="IDENTIFIED" bytes=126 sha256="0d20505106e238a717a6b0729deeae093a06bc700c3bfbfac8748c6f213e13fc" disposition="ACCEPT"
MEMBER composite="fixture-p0" index=1 id="library" kind="shell" path="library.sh" graph="REACHABLE" identity="IDENTIFIED" bytes=140 sha256="35958de1f651dc3d511d0ce56360e4add762add9e93e563c0ac55a64a61d70ec" disposition="ACCEPT"
REQUIREMENT composite="fixture-p0" index=0 name="REMOTE_BASE" kind="absolute_path" consumers=["entry", "library"] disposition="ACCEPT" reasons=["conserved"]
CONSUMER composite="fixture-p0" requirement_index=0 index=0 allocation="REMOTE_BASE" member="entry" disposition="ACCEPT" reasons=["declared_reference_conserved"]
CONSUMER composite="fixture-p0" requirement_index=0 index=1 allocation="REMOTE_BASE" member="library" disposition="ACCEPT" reasons=["declared_reference_conserved"]
REQUIREMENT composite="fixture-p0" index=1 name="RUNID" kind="safe_component" consumers=["entry"] disposition="ACCEPT" reasons=["conserved"]
CONSUMER composite="fixture-p0" requirement_index=1 index=0 allocation="RUNID" member="entry" disposition="ACCEPT" reasons=["declared_reference_conserved"]
ALLOCATION composite="fixture-p0" index=0 name="REMOTE_BASE" value="/home/gatea/wpi_staging_fixture" disposition="ACCEPT" reasons=["closed"]
ALLOCATION composite="fixture-p0" index=1 name="RUNID" value="WPI-FIXTURE-P0" disposition="ACCEPT" reasons=["closed"]
CONSERVATION composite="fixture-p0" input_members=2 terminal_member_rows=2 reachable_members=2 input_edges=1 terminal_edge_rows=1 input_requirements=2 terminal_requirement_rows=2 input_allocations=2 terminal_allocation_rows=2 input_consumer_references=3 terminal_consumer_rows=3
PATH_PROVER adapter="stub" disposition="NOT_INVOKED" reason="allocate_stage_has_no_path_proof_claim"
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=allocate_stage_closed
COMMAND_RC=0
```

## Later-stage STOP fences

The render stage is present in the state model but has no round-1 implementation:

```text
FIXTURE=red_render_unimplemented.json PHASE=RED
CLAIM id="A1" name="plan_contract" verdict="STOP" reason="render_stage_not_implemented_round1"
CLAIM id="A2" name="declared_entrypoint_discovery" verdict="STOP" reason="render_stage_not_implemented_round1"
CLAIM id="A3" name="allocation_plan_conservation" verdict="STOP" reason="render_stage_not_implemented_round1"
CLAIM id="A4" name="allocation_value_closure" verdict="STOP" reason="render_stage_not_implemented_round1"
CLAIM id="A5" name="declared_graph_conservation" verdict="STOP" reason="render_stage_not_implemented_round1"
CLAIM id="A6" name="component_identity" verdict="STOP" reason="render_stage_not_implemented_round1"
STAGE stage="render" disposition="STOP" reason="render_stage_not_implemented_round1"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
COMMAND_RC=3
```

The freeze stage reaches only the swappable stub boundary; it does not import or call
`pathscope_prover.py`:

```text
FIXTURE=red_freeze_unimplemented.json PHASE=RED
CLAIM id="A1" name="plan_contract" verdict="STOP" reason="path_prover_component_not_integrated"
CLAIM id="A2" name="declared_entrypoint_discovery" verdict="STOP" reason="path_prover_component_not_integrated"
CLAIM id="A3" name="allocation_plan_conservation" verdict="STOP" reason="path_prover_component_not_integrated"
CLAIM id="A4" name="allocation_value_closure" verdict="STOP" reason="path_prover_component_not_integrated"
CLAIM id="A5" name="declared_graph_conservation" verdict="STOP" reason="path_prover_component_not_integrated"
CLAIM id="A6" name="component_identity" verdict="STOP" reason="path_prover_component_not_integrated"
PATH_PROVER adapter="stub" disposition="STOP" reason="path_prover_component_not_integrated"
COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=freeze_stage_incomplete
COMMAND_RC=3
```

## Syntax, import-surface, assertion, and determinism QA

Exact syntax/import command:

```powershell
python --version
python -B -c "import ast,pathlib; p=pathlib.Path(r'$tool'); tree=ast.parse(p.read_text(encoding='utf-8'), filename=str(p), feature_version=(3,12)); names=sorted({a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}|{n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module}); print('AST_PARSE_3_12=PASS'); print('IMPORTS='+','.join(names))"
```

Real output:

```text
Python 3.14.2
AST_PARSE_3_12=PASS
IMPORTS=__future__,argparse,dataclasses,enum,hashlib,json,pathlib,posixpath,re,sys,typing
```

There is no subprocess, socket, HTTP, or third-party import.

The assertion harness required the exact rc and a claim-specific reason token for every
fixture. Real output:

```text
A1 rc=3 token=plan_schema_unknown_key ASSERT=PASS
A2 rc=1 token=entrypoint_not_declared ASSERT=PASS
A3 rc=1 token=allocation_not_one_to_one ASSERT=PASS
A4 rc=3 token=allocation_value_unresolved ASSERT=PASS
A5 rc=1 token=declared_member_unreachable ASSERT=PASS
A6 rc=3 token=member_file_missing ASSERT=PASS
GREEN rc=0 token=allocate_stage_closed ASSERT=PASS
RENDER rc=3 token=render_stage_not_implemented_round1 ASSERT=PASS
FREEZE rc=3 token=path_prover_component_not_integrated ASSERT=PASS
```

Two independent in-process invocations used the exact `green.json` command and compared
complete stdout plus rc. Real output:

```text
DETERMINISM rc1=0 rc2=0 equal=True sha1=31403fdead0e700ca706a0f442d016fdf3944a9e150eeb517eaa6436240657a5 sha2=31403fdead0e700ca706a0f442d016fdf3944a9e150eeb517eaa6436240657a5
```

## Pre-document artifact identities

These values were re-derived after the final code/fixture QA. Document identities are
derived after both documents are complete and recorded by the dispatch transcript/Lead.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `composite_pathproof.py` | 29640 | `77f1076163310f331cac3effd91ccc60aaaee841757eaea54288ca5b40472c90` |
| `sec102_r1_fixtures/entry.sh` | 126 | `0d20505106e238a717a6b0729deeae093a06bc700c3bfbfac8748c6f213e13fc` |
| `sec102_r1_fixtures/green.json` | 852 | `2804bf9c831b41fd1fa6e713f72530747a8fb72836072de7cece0bc5ae35fe79` |
| `sec102_r1_fixtures/library.sh` | 140 | `35958de1f651dc3d511d0ce56360e4add762add9e93e563c0ac55a64a61d70ec` |
| `sec102_r1_fixtures/red_allocation_conservation.json` | 529 | `f9fd2a1d563d53e8345b0e76794eab6c6c258a2763511ce45a548d808c3a02eb` |
| `sec102_r1_fixtures/red_allocation_value.json` | 499 | `3270e71e8c8695e05ca907b096dbc0a5ddf7b04262baca6f5e4f256ca1af415f` |
| `sec102_r1_fixtures/red_component_identity.json` | 470 | `b8d52e58a3434e98df92a1a8a66f888f40ab4f21a9e92990d37f5e6481f15ba0` |
| `sec102_r1_fixtures/red_entrypoint.json` | 609 | `09aac79fb10e77e173739a281fcd7000a07a615a487ca6e8793cda7c2ce66ccf` |
| `sec102_r1_fixtures/red_freeze_unimplemented.json` | 466 | `cd5cd7c9f9d4f6e184be80b52b9b4b1d63f56fb7ac1ff1ef3fd9916b31806df5` |
| `sec102_r1_fixtures/red_graph_conservation.json` | 534 | `4aafd94a1c80b2d5fcc16f9aae37781bf20c64666bceae43bdeeac76075f1655` |
| `sec102_r1_fixtures/red_plan_contract.json` | 115 | `9a37645d3e7e9ea03cf12c91d26c5c28062b537f54460407a95ff6ae4c8594f2` |
| `sec102_r1_fixtures/red_render_unimplemented.json` | 466 | `c30c5d0e5e9d1d84c2903f8bdc72a3b4ccfa54fa0d2afcad7c1c65a5ae3b4e78` |

Self-QA verdict: `IMPLEMENTER-QA-PASS`; external T1 flagship audit remains required.
