# Path-scope prover status

Status: `REPAIRED-R3-PENDING-REAUDIT`

**Round 3 (2026-08-13).** The Claude Pro T1 execution audit
(`PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`) returned REQUEST_CHANGES with one CRITICAL,
C-1: assignment-prefix/declaration/`env` assignment values were silently dropped, so an
out-of-allowlist loader path returned `PASS rc=0`. Round 3 (GLM-5.2 source-level implementer,
`PATHSCOPE_GLM_T1_R3_REPAIR_REPORT_2026-08-13.md`) adds `record_assignment_value` at the
three holes — fail-closed on the construct, not a variable-name allowlist. **Lead executed
the full harness 2026-08-13: rc 0; all seven P9 fixtures confirmed (five silent sinks now
RED `PASS rc=0` → GREEN `rc=1` with the path visible; two controls hold); both real blocks
still rc=3 deterministically.** New identity: 124251 B, SHA-256
`0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7`. Disclosed residual:
bare sonames (`LD_PRELOAD=libc.so`) are not path-shaped and stay lexical-contract-outside —
flagged for the re-auditor's call. Fresh T1 execution re-audit over the r3 bytes is the
pending step; implementers so far are `claude-opus-5` (r2) and GLM-5.2 (r3), so the
re-auditor must be neither.

Round 1 status was `AUTHORED-PENDING-AUDIT`. `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`
returned `REQUEST_CHANGES: 9`, four of them CRITICAL silent-sink-loss. Round 2 is the
repair; the disposition of every finding is in `PATHSCOPE_REPAIR_R2_REPORT.md` and the
executed RED/GREEN evidence is in `SELF_QA_PATHSCOPE.md`.

Audit tier: T1 — local-only Stage-1 static analysis; no host, network, trading, Pine,
parity, MTC, deployment, transport, or runtime action. Codex remains the auditor of
record; this round was implemented by `claude-opus-5`, so the re-audit must not be.

Identity of the repaired artefact: 122446 B,
SHA-256 `890016F0B9A8CDE4EED33F8733F69055471B07C6096F6BC07450457E6C52AF1D`.
Round-1 bytes for the RED column: 49820 B,
SHA-256 `3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6`,
git blob `3f0820a9a6412f769b59b23a41df3bc6808bf6dc`.

Design: quote-aware complete-input Bash lexer with here-document collection, pinned scalar
expansion with provenance, an explicit per-command argv grammar registry, filesystem and
network sink extraction as two separate domains, lexical path normalization, exact/tree/
terminal allowlist verdicts, and fail-closed rc 3 for every unmodeled command, option,
redirection, expansion or construct.

**What the proof is.** The membership claim is *lexical argv scope*: after constant and
variable expansion the normalized argv string lies inside a §10.1 pattern. Every run
prints this in machine form —
`PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established
mount_boundary=not_established host_probe=none` — and the allow verdict token is
`ALLOW-LEXICAL`, not `ALLOW`. The tool reads frozen bytes and performs no host probe, so
it cannot establish that an intermediate component is not a symlink or a mount crossing to
an object outside that tree. Binding the lexical result to a real host tree needs a
separate symlink/mount-chain proof that this tool does not attempt and does not claim.

**Counts changed shape.** `resolved_count`/`unresolved_count` are gone. A run now prints
`resolved_fs_path_count`, `resolved_net_endpoint_count`, `unresolved_path_count`,
`unresolved_endpoint_count`, `coverage_issue_count`, `provenance_issue_count` and
`parse_issue_count` as distinct fields, and every `UNRESOLVED` line carries `kind=`. Any
consumer that parsed the two round-1 fields must be updated.

**Current real-block results are unchanged in direction.** Against the draft's
`<ALLOCATE-AT-DISPATCH>` placeholder both blocks still STOP at rc 3 before analysis;
with the disclosed non-authoritative static `REMOTE_BASE` substituted for diagnostic depth
both still reach rc 3. The tool was not tuned to admit either block.
