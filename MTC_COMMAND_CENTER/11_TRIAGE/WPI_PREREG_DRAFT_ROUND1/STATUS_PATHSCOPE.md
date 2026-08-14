# Path-scope prover status

Status: `REPAIRED-R4-PENDING-REAUDIT`

**Round 4 (2026-08-13).** The Codex T1 execution re-audit of the round-3 bytes
(`PATHSCOPE_CODEX_T1_EXEC_AUDIT_R3_2026-08-13.md`) returned REQUEST_CHANGES with one
CRITICAL, **C-2**: `record_assignment_value` recorded a value only when the complete
rendered value started with `/`, `./` or `../`, and then only as one whole blob — so loader
lists with a later absolute member, bare first members, whitespace word lists, ordinary
relative pathnames, empty list members, option-carrying command text and URI-shaped values
all returned `PASS rc=0` with the out-of-allowlist lexeme absent. The Lead separately
reproduced a false PASS in an incomplete first repair attempt, where a naive `str.split()`
turned the single quoted pathname `/safe dir/escape` into two allowed paths. Round 4
(`claude-opus-5` implementer, effort high; `PATHSCOPE_CAP_OVERRIDE_REPAIR_REPORT_2026-08-13.md`)
replaces the first-character test with `record_assignment_members`: a URI goes to the
endpoint domain, colon members are parsed on every value including one starting with `/`,
the whole-value reading is kept alongside the members, a whitespace word list is decided on
grammar (never on the variable name) and fails closed with a specific coverage record, and
an empty member is fail-closed only when the same value also carries a path member — so
`IFS=:` stays benign by grammar. **Executed by the implementer 2026-08-13: the published
harness runs rc 0, stderr 0 bytes; RED_R1 660 lines, GREEN 1363 lines, and a new RED_R3 150
lines produced by running the eighteen new C-2 fixtures against the committed round-3 blob
`e600a107f2e2a790653cc544a94cd7436b7b070a`, so the RED column is measured pre-repair bytes,
not a prediction. Twelve fixtures move rc 0 → rc 1/3 with the sink printed; five controls
hold; `c2_quoted_space` holds rc 1 as a regression guard, falsified by mutation MUT-A.** All
seven round-3 P9 fixtures are byte-identical under round 3 and round 4. Regression surface
against the round-3 blob: 17 of 87 fixture cases differ (14 C-2 fixtures + 3 endpoint cases
carrying only the `ALLOW` → `ALLOW-LEXICAL` NIT-1 label); `RP6-P0` is byte-identical and
`RP7-WPI-RO` gains exactly one coverage record, both still rc 3. The three documentary nits
from §5 of the r3 verdict are cleared. New identity: 131599 B, SHA-256
`553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB`. Disclosed residual is
now narrow and exact: a member containing **no `/`** (bare soname, scalar, tool name)
carries no argv pathname and gets no row; and the union-of-readings model is deliberately
conservative, so a value like `MSG="denied /etc/secret"` over-rejects. This round is the
single owner-authorized T1 cap override (`WPI_OWNER_DECISIONS_2026-08-13.md` §4); one fresh
T1 flagship execution re-audit is the pending step, and it must be neither `claude-opus-5`
nor GLM-5.2. **Not accepted and not committed by this implementer session.**

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
record; rounds 2 and 4 were implemented by `claude-opus-5` and round 3 by GLM-5.2, so the
re-audit must be neither.

Identity of the round-2 artefact: 122446 B,
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
