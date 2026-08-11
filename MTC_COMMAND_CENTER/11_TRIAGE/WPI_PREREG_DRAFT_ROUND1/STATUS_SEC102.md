# Section 10.2 composite path-proof status

Date: 2026-08-11  
Status: `ROUND-1-AUTHORED-PENDING-CLAUDE-T1-AUDIT`  
Audit tier: T1 - local-only non-economic Python tooling and fixtures; no host, network,
deployment, runtime, broker, trading, Pine, parity, MTC, or protected-schema action.

## Round 1 coverage

`composite_pathproof.py` provides the scaffold for the design's
allocate -> render -> freeze sequence and implements only ALLOCATE end to end.

The ALLOCATE stage currently enforces:

1. A strict `sec102-composite-plan-v1` JSON envelope, including duplicate-key refusal,
   closed key sets, exact types, and stage agreement.
2. One declared entrypoint member per composite.
3. One-to-one declared allocation requirements and supplied allocations; duplicate,
   missing, and undeclared allocations cannot pass.
4. Placeholder-free lexical validation for `safe_component` and `absolute_path` values.
   An absent or unresolved value is STOP, not PASS or FAIL.
5. Entrypoint-driven traversal of the declared component graph, with duplicate IDs,
   invalid edges, cycles, and unreachable members rejected.
6. One terminal row per declared member, edge, requirement, allocation, and consumer
   reference. Conservation counts are emitted in the report.
7. Local byte identity for every declared member: relative canonical in-bundle path,
   no symlink in its path chain, regular file, byte count, and SHA-256.
8. A deterministic line report with explicit claim rows and the fixed verdict contract:
   PASS rc 0, observed deviance FAIL rc 1, inability to evaluate STOP rc 3, with STOP
   taking precedence.
9. A swappable `PathProver` protocol and fail-closed stub. The existing unrepaired
   `pathscope_prover.py` is not imported, read, or executed by this tool.

The six claimed ALLOCATE properties each have an executable RED fixture, followed by one
common GREEN fixture that proves all six. Render and freeze have executable STOP fixtures.
Exact commands, rc values, real output, syntax/import checks, deterministic-output proof,
and artifact identities are in `SELF_QA_SEC102_R1.md`.

## Later rounds required

Round 2 must implement RENDER:

- consume an accepted allocation record and materialize every allocated/fill value into
  the stage entrypoint, wrapper, block pins, and other consumers;
- prove no placeholder/default survives and no value changes representation;
- derive source, execute-source, and nested-source edges from the rendered bytes rather
  than trusting the plan's declared graph;
- cover inline programs and the exact file-backed `verify_lock.py` source;
- re-identify the resulting rendered bytes and conserve producer/consumer bindings.

Round 3 or later must implement FREEZE and prover-component integration:

- bind the entry interpreter, argv, environment, cwd, shell options, startup behavior,
  bootstrap helpers, and exact executed-tool inventory;
- build the final ordered component manifest from the rendered bytes and freeze all
  identities before analysis or invocation;
- integrate only a separately repaired and T1-accepted path-prover component through the
  `PathProver` interface;
- prove complete command/option/redirection/nested-program coverage, exact lexical
  filesystem/network operands, and named closed runtime families;
- apply the Section 10.1 allowlist without confusing lexical scope with host-object,
  symlink, mount, namespace, or runtime-descendant proof;
- add D026 mutation/falsification evidence for each production claim and run a fresh T1
  audit of the integrated local tool.

No archive may be frozen on the strength of round 1.

## Known limitations - each is a limitation, not a control

1. Round 1 is not a Section 10.2 proof and is not dispatch, freeze, or host evidence.
2. The fixtures are synthetic. No current RP6, RP7, wrapper, bootstrap, candidate blob,
   or real preregistration plan was analyzed.
3. `entrypoint` is selected from a plan field. Round 1 does not discover the production
   entrypoint from transport or executable source semantics.
4. Graph edges are declared plan data. Their presence is checked for conservation but is
   not mechanically derived from `source`, `.`, interpreter, inline-code, or exec sites.
5. Consumer references are declared plan data. Round 1 checks their uniqueness and member
   existence but does not prove that source producers and consumers use those values.
6. Shell and Python files are opaque bytes. Round 1 performs no language parse, dataflow,
   function reachability, option grammar, redirection, endpoint, or path-sink analysis.
7. Only the allocation kinds `safe_component` and `absolute_path` are implemented. Any
   other allocation kind STOPs.
8. Only declared member kinds `shell` and `python_source`, and edge kinds `source`,
   `execute_source`, and `inline_source`, are recognized. Recognition does not establish
   source semantics.
9. The safe-component and absolute-path predicates are lexical only. They do not allocate
   remote objects, prove uniqueness on a host, establish create-once behavior, or inspect
   symlink/mount/namespace state.
10. Member identities describe local fixture bytes at read time. They are not Git-object,
    candidate-archive, transport, host, or immutable freeze identities.
11. Local symlink paths are refused, but no host-object identity, intermediate mount, or
    time-of-check/time-of-use claim is made.
12. Render is unimplemented and always STOPs with
    `render_stage_not_implemented_round1`.
13. Freeze is unimplemented and always STOPs through
    `path_prover_component_not_integrated`.
14. The `PathProver` interface is only a boundary. The stub never returns PASS and no
    repaired path prover is integrated.
15. No exact source-derived path, network operand, allowlist disposition, runtime family,
    external-runtime boundary, or grammar-coverage record is produced.
16. Bash startup sources, imported functions, aliases, PATH, TMPDIR, cwd, interpreter
    identity, executable bindings, and launch namespaces are not evaluated.
17. The report is stdout only. It does not create, render, hash, bind, or freeze a manifest
    artifact.
18. No subject file is executed. A clean fixture result says only that the bounded
    allocation-plan checks passed.

## Artifact identities

The following identities were re-derived after code/fixture QA. The `SELF_QA` identity was
derived before this status file was created. This status file cannot contain its own final
hash; its final size/SHA-256 is recorded in the implementer completion transcript supplied
to the Lead.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `composite_pathproof.py` | 29640 | `77f1076163310f331cac3effd91ccc60aaaee841757eaea54288ca5b40472c90` |
| `SELF_QA_SEC102_R1.md` | 17290 | `e6fef1656db5ab516ae0deccf60998f1dd9cbfbb2d4b533ccc406ba1f057b572` |
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

Round-1 acceptance remains with the Claude Lead's fresh T1 flagship audit. No commit,
network, host contact, or authority expansion occurred.
