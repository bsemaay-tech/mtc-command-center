# Path-scope prover status

Status: `OPTION-C-IMPLEMENTED-PENDING-FRESH-FLAGSHIP-AUDIT`

**Option C implementation (2026-08-15; audit tier T1).** The accepted accounting redesign
is implemented in `pathscope_prover.py` and integrated into
`composite_pathproof.py`. It keeps the parser/traversal surface, but replaces assignment
value reporting with immutable expansion traces, ordered occurrence ledgers, stable global
IDs, exact member-local provenance, a closed terminal-disposition enum, two-phase
conservation checks, strict additive serialization, and fail-closed reporting. The
composite adapter now parses only the named new prefixes, independently reconciles the
ledgers and mandatory projection, forwards every accounting record, and implements the
accounting-fault and zero-generic-issue member-unresolved arms.

The edited harness was extracted verbatim from `SELF_QA_PATHSCOPE.md` and executed from
`C:\PSC`: outer rc 0, stderr 0 bytes. Historical RED hashes and frozen R5's retired GREEN
hash reproduced; two complete candidate runs were byte-identical; 60 required blocks were
byte-identical to R5; and among 109 existing cases exactly the two V2-authorized return
codes changed (`c2_benign_words` 0→3, `c3_colon_whole` 1→3). Frozen-R5 RED and current
GREEN were measured for all admission/F1/F2/F3/adjacent attacks. All 23 required mutation
arms (25 checks) were discriminating, including missing/duplicate/unknown disposition,
identity/provenance/reason/cardinality faults, composite grammar faults, and compatibility
mutations. CPython 3.14.2 executes the sources and all three parse at Python 3.12 grammar;
an actual Python 3.12 runtime is unavailable (`py -3.12 -V` rc 103).

This is implementation evidence, not acceptance. Owner decision D1 authorizes one fresh
flagship execution audit and no implementation repair round if it returns a required
finding. No host, network, deployment, service, trading, Pine, parity, MTC, broker,
credential, push, merge, or economic action occurred. The pre-existing composite
`ENDPOINT verdict=ALLOW-LEXICAL` versus `ALLOW` acceptance mismatch remains disclosed and
unchanged because V2 residual 11.10 expressly excludes it.

**Round 5 (2026-08-14) — the final owner-authorized repair.** The Codex T1 execution audit
of the committed round-4 candidate `2fb3eac05f8da716609549179a7961aa692eae6b`
(`PATHSCOPE_CAP_OVERRIDE_CODEX_T1_AUDIT_2026-08-13.md`) returned REQUEST_CHANGES with three
required findings. **C-3:** `record_assignment_members` still dropped admitted readings — a
whitespace list with a later relative member, a URI-shaped loader list with a later
absolute member, a colon-bearing whole-pathname reading, an empty-only loader list
(`LD_LIBRARY_PATH=:`), and executable command text without `/` (`GIT_SSH_COMMAND="ssh
-v"`) — each returning `PASS rc=0` with zero terminal accounting. **C-4:** the declaration
builtins gated every operand on a RAW `ASSIGN_RE` match, so `export
"LD_PRELOAD=/etc/escape.so"` and `export 'X=/safe dir/escape'` never reached the repaired
grammar that the identical `env` shape did reach. **Portability:** the published harness did
not reproduce its recorded transcripts and determinism digests under its literal command.

Round 5 (`claude-opus-5` implementer, effort high;
`PATHSCOPE_FINAL_OVERRIDE_REPAIR_REPORT_2026-08-14.md`) closes all three. The member
grammar is now one rule — the whole value is always a candidate and members are added,
never substituted; a multi-word value is a live word list when any word is option-shaped
or any word carries `/`; `split_list_members` protects only a URI's `scheme://authority`
span; a relative value carrying `:` is still a pathname reading; an empty list member is
*resolved* to the pinned PWD instead of vanishing, and fails closed when PWD is unpinned.
`analyze_declaration` classifies every declaration operand on its **expanded** form, so the
assignment prefix, the `env` wrapper and all five declaration builtins terminate in one
parser, and an operand that is neither an option, a NAME, nor NAME=VALUE after expansion
now emits a coverage record instead of being ignored.

**Executed by the implementer 2026-08-14.** Every required finding was first reproduced
against the committed pre-repair blob `55ea3a852f7781d03d57483f554c1b8ac62007c6`, then
closed against the repaired bytes, through the real prover. The RED column of the new
eighteen-fixture P11 family is that committed blob, extracted and run by the harness
itself. Seven single-line mutations of the round-5 source were executed and every one
destroys a claimed property, including MUT-A which falsifies the quoted-space regression
guard. Regression surface against the round-4 blob: 109 cases run, **84 byte-identical, 25
differ** — 15 P11 fixtures, 8 P10 fixtures, 1 base fixture and `RP7-WPI-RO`; every changed
fence is itemised with its discriminating-power proof, and no FORBID row was lost anywhere.
`RP6-P0` is byte-identical; `RP7-WPI-RO` moves `unresolved_path_count` 34 → 35 at line 681
and stays rc 3. Both blocks remain rc 3 in both constants modes.

**The harness portability defect is closed at the root, not papered over.** The cause was
measured: the harness never pinned the child interpreter's stdout encoding, so `python`
used the locale encoding (`cp1254`) whenever the ambient `PYTHONIOENCODING` was unset,
PowerShell decoded that stream as UTF-8, and the `ı` in the user profile path was
destroyed — leaving `.Replace($QA, '<QA>')` matching nothing and the user path embedded in
every transcript. Re-running the round-4 command against the round-4 bytes with
`PYTHONIOENCODING` removed reproduces all five of the auditor's observed digests exactly
(`b3119f99…5620`, `f77f6714…4d81`, `b2f153c2…f611`, `8ce5571b…1ecf`, `c0e4b807…f452`). The
round-5 harness pins `PYTHONUTF8`/`PYTHONIOENCODING`/`[Console]::OutputEncoding`, drives
the prover from the fixture directory with relative arguments so no user path can enter a
transcript at all, extracts blobs and computes blob ids in process instead of through
`cmd /c`, and aborts with `TRANSCRIPT_LEAK` if a scratch path appears anyway. The published
fence was extracted from `SELF_QA_PATHSCOPE.md` without changing a character and run twice
— once with UTF-8 I/O and code page 65001, once with `PYTHONIOENCODING`/`PYTHONUTF8`
removed and both the code page and `[Console]::OutputEncoding` forced to `windows-1254` —
and produced byte-identical stdout, transcript digests and determinism digests. This is not
two broken runs agreeing: the round-4 harness demonstrably diverges in the second
environment and the round-5 harness does not.

New identity: 137520 B, SHA-256
`28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C`. Disclosed residual is
unchanged in kind and now stated with one addition: a member with no `/` and no option
shape carries no argv pathname and gets no row; an option word carrying an **attached**
pathname (`-I/usr/include`) is not decomposed and is disclosed inside the coverage reason
text itself; and the union-of-readings model remains deliberately conservative, so values
like `MSG="denied /etc/secret"` over-reject. This round is the single repair authorized by
`WPI_OWNER_DECISION_PATHSCOPE_FINAL_OVERRIDE_2026-08-14.md`; exactly one fresh independent
`gpt-5.6-sol` high execution audit follows it, and no further cycle is authorized without a
new owner decision. **Not accepted and not committed by this implementer session.**

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
record; rounds 2, 4 and 5 were implemented by `claude-opus-5` and round 3 by GLM-5.2, so
the re-audit must be neither.

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
