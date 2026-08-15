Status: OPTION SCOPING ONLY — NOT A RECOMMENDATION, NOT AUTHORIZED

# Pathscope restricted-grammar option

## Top-line surviving dangerous world

This option can still admit a script that is lexically inside the allowlist while the
runtime opens an object outside it. A conforming input such as
`${CAT} "${APPROVED_ROOT}/link"` can pass when `CAT` and `APPROVED_ROOT` are pinned and
`/approved/link` is lexically allowed, yet `/approved/link` can be a symlink or a path
across a mount boundary to `/outside/payload`. The current prover expressly declares
`symlink_resolution=not_established`, `mount_boundary=not_established`, and
`host_probe=none`; its allow verdict is only `ALLOW-LEXICAL`
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md:145-151`;
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py:2936-2938`).

Therefore the restricted grammar closes the **shell-admission coverage** problem, but it
does not prove that an allowed lexical pathname resolves to an allowed runtime object.
This is a concrete dangerous admitted world. It is not another unconsumed-shell-syntax
escape; it is an existing lexical-versus-runtime limit. If the required claim is about
the object actually opened rather than the lexical argv value, this option alone does not
establish that claim.

## Decision facts

| Question | Scoped answer |
|---|---|
| Smallest non-vacuous subset | `RG-0`: comments/blanks plus one straight-line, direct simple command per line; exact `${NAME}` constant references; no general shell state or compound grammar. |
| Canonical real-block fit | **0/2 blocks accepted (0%); 2/2 rejected (100%).** |
| Complete Stage-1 proof-unit fit | **0/2 compositions accepted (0%); 2/2 rejected (100%) unchanged.** |
| Rejection | Atomic, explicit `UNANALYSABLE`, rc 3; never a partial PASS. |
| Build cost | **NO SOURCED ESTIMATE.** |
| Migration cost for real inputs | **NO SOURCED ESTIMATE.** |
| Exact proportion of Option C code that survives | **UNKNOWN.** The available snapshot establishes reuse of the test corpus and harness concept, but not a percentage and not the state of the missing fifth-cycle work. |
| Runtime path-object safety | Not proved; the counterexample above remains. |

This is the option's central cost finding: it is structurally safe at its admission
boundary and currently unusable on every real proof unit. A safe prover that rejects all
real input cannot serve as the Stage-1 freeze proof without a source migration.

## Evidence boundary and denominator

The task specification names a 2026-08-16 owner-boundary record and a fifth cycle
(`C:/tmp/lane_kick/OPTE.md:13-20`). That named file is not present in this detached
`C:\RO` snapshot. The latest owner-boundary record available here is dated 2026-08-15 and
says the then-current attempt was the **fourth** consecutive cycle
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md:61-65`).
Facts unique to the missing 2026-08-16 record, including the exact bytes and completion
state of any fifth-cycle Option C accounting implementation, are therefore **UNKNOWN**.
The 2026-08-15 material is used only where it directly establishes a fact.

There are two relevant denominators:

1. The original Pathscope kickoff explicitly calls `RP6-P0.sh` and `RP7-WPI-RO.sh` the
   two “REAL committed” blocks
   (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_PATHSCOPE_PROVER.md:27-31`).
   These are the primary real-input denominator: two files.
2. The later composite acceptance boundary is wider. It defines two complete same-shell
   proof units: `run_p0.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP6-P0.sh`, and
   `run_ro.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP7-WPI-RO.sh`; the RO graph also includes
   inline programs and `verify_lock.py`
   (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:217-223`).
   This is the freeze-relevant denominator: two compositions.

The fixture directories under `WPI_PREREG_DRAFT_ROUND1` are synthetic QA inputs, not
additional real blocks. The published QA says it ran 105 fixture cases and four
real-block cases (two blocks across two versions)
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:954`;
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:3901-3902`).
Counting those fixtures as real input would distort usability.

## The subset: `RG-0`

An empty accepted language is mathematically smaller but proves nothing useful. `RG-0`
is the smallest **non-vacuous path-bearing construct family**: a closed straight-line
language with exactly one executable shell construct, the direct simple command. It can
express the kickoff's requested small GREEN fixture based on preregistered constants
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_PATHSCOPE_PROVER.md:27-29`).
It deliberately cannot express the current operational blocks.

### 1. Byte and parse envelope

- Input is ASCII bytes only: HT, LF, and printable bytes `0x20` through `0x7e`; CR, NUL,
  non-ASCII bytes, and a missing final LF are outside the language.
- An optional first line is exactly `#!/bin/bash`.
- The parser must consume from byte zero through EOF with no error recovery, skipped
  token, implicit continuation, or parser warning. A trailing unconsumed byte makes the
  entire file `UNANALYSABLE`.
- A comment is allowed only as a whole logical line after optional horizontal space.
  Inline comments are excluded. Backslash-newline continuation is excluded.

### 2. Positive grammar

The grammar is intentionally a positive definition, not a list of dangerous forms:

```text
file          ::= [ shebang LF ] line* EOF
line          ::= H* LF
                | H* comment LF
                | H* simple H* LF
shebang       ::= "#!/bin/bash"
comment       ::= "#" printable_ascii*
simple        ::= tool (H+ operand)*
tool          ::= const_ref
operand       ::= bare_literal | quoted_template
quoted_template ::= '"' segment* '"'
segment       ::= safe_literal+ | const_ref
const_ref     ::= "${" NAME "}"
NAME          ::= [A-Z_][A-Z0-9_]*
H             ::= HT | SP
```

`safe_literal` excludes every shell metacharacter, whitespace byte, quote, backslash,
glob character, dollar form other than `const_ref`, and a leading `-`. A path or endpoint
operand must contain at least one `const_ref`; a literal-only operand is admissible only
when an exact command contract classifies it as fixed non-sink data. Constant entries are
unique, immutable, preregistered values. A tool constant must expand to one pinned absolute
executable path.

### 3. Command envelope

- Every expanded tool identity must have one exact command contract.
- A contract states the exact positional arity and the role of each operand: filesystem
  path, network endpoint, or exact fixed data.
- Every operand must be consumed once by that contract. There is no “generic command,”
  “no-path command,” unknown-command fallback, or ignored trailing argv.
- `RG-0` admits no option-shaped word, including `--`, and no option operand. A future
  option form would be a new grammar version with its own exact production and audit; it
  cannot be smuggled through the generic word rule.
- Relative paths are excluded. Paths must expand to canonical absolute lexical paths;
  endpoints must match one exact endpoint grammar. Empty values and colon/whitespace
  lists are excluded.
- Commands that interpret another program, source another file, discover plugins/config
  through implicit search, or evaluate command text are not eligible command contracts.
  Inline Python, `sh`, `bash`, `eval`, `source`, `.`, `exec`, and `env` are therefore
  outside `RG-0`.

### 4. Constructs not in the language

Because `simple` is the only executable production, all of the following are rejected at
the admission phase: shell assignments and assignment prefixes; `export`/`local`/`declare`;
functions; `if`, `case`, `for`, `while`, `until`, and `select`; `[` and `[[`; arithmetic;
arrays and subscripts; command, process, arithmetic, tilde, brace, glob, or indirect
expansion; pipelines and `&&`/`||`/`;`/`&` lists; subshells and groups; traps; redirections
and descriptor manipulation; heredocs and here-strings; option operands; sourced files;
and nested programs.

This exclusion is enforced by total parsing. It is not implemented as one regular
expression per forbidden construct. The repository's own defect catalogue requires
unmodelled analyzer syntax to fail closed and states that zero facts plus PASS is always
red (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:899-928`).

## Why the admission boundary is provable

`RG-0` supports two linked conservation checks:

1. **Byte conservation:** every byte is assigned to the shebang, whitespace, comment, a
   command/member token, LF, or EOF. Any byte outside those productions rejects the whole
   file before semantic analysis.
2. **Member conservation:** each admitted command and operand receives a stable identity
   `(file_digest, line, ordinal, byte_start, byte_end)`. Each identity reaches exactly one
   terminal state: `ALLOW-LEXICAL`, `FORBID`, fixed non-sink data, or `UNANALYSABLE`.
   Identity and segment-level constant provenance cannot be deduplicated, unioned across
   neighbors, or re-keyed by rendered value.

PASS is possible only when:

```text
consumed_bytes = file_bytes
admitted_member_ids = terminal_member_ids
count(admitted_member_ids) = count(terminal_member_ids)
every terminal state is ALLOW-LEXICAL or fixed non-sink data
```

Duplicate rendered values remain different member identities. Missing identity,
duplicate identity, provenance drift, a command-contract mismatch, or an unexplained
count change is `UNANALYSABLE`, rc 3. This is the conservation rule required by Pattern
13 (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-966`).

The gain over the current design is exact: conservation quantifies over every member of
a completely characterized accepted language. It no longer quantifies over whichever
values a permissive parser happened to recognize. The 2026-08-15 audit demonstrates why
that distinction matters: command text and a URI/list member vanished, provenance crossed
between neighbors, and duplicate/empty members collapsed
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:183-221`).

## Real-input fit and rejection cost today

Both canonical real blocks are outside `RG-0` immediately, and they also contain many
independent excluded forms:

| Real subject | Examples present in the actual source | `RG-0` result |
|---|---|---|
| `RP6-P0.sh` | shell assignments at lines 132-146; functions at 148-162; `case` at 176; `for` at 363; bracket test plus command substitution at 398; array/subscript use at 1184; option operands at 865; inline Python at 1811 | `UNANALYSABLE`, rc 3 |
| `RP7-WPI-RO.sh` | assignments at 65-98; functions at 142-166; `case` at 164; `[[` at 259; array/subscript use at 568; `for` at 612; named-fd redirection at 647; inline Python at 654-767; here-string at 1094; option operands at 927-930 | `UNANALYSABLE`, rc 3 |

Source citations for the examples are the named source lines themselves, including
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh:132-176`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh:363-398`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh:865`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh:1184`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh:1811`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:65-98`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:142-166`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:246-260`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:568-612`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:647-654`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:927-930`, and
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:1094-1096`.

The wrappers do not rescue composite usability. `run_p0.sh` has command substitution,
`if`, a function, `while`, and arithmetic by lines 45-96; `run_ro.sh` has the same forms
by lines 39-90 (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh:45-96`;
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh:39-90`). Since one excluded
construct rejects the complete file atomically, both complete proof units are outside the
subset regardless of the unseen library/bootstrap portions.

The exact decision counts are therefore:

- Historical real-block denominator: accepted `0/2 = 0%`; rejected `2/2 = 100%`.
- Composite freeze denominator: accepted `0/2 = 0%`; rejected `2/2 = 100%` unchanged.
- Physical-line or AST-node acceptance fraction: **UNKNOWN** and not an acceptance metric.
  No sourced closed-grammar parser census establishes it, and partial compatible lines do
  not make an atomically rejected file usable.

The existing prover already reports both real blocks at rc 3 under both the unresolved
allocation placeholder and a diagnostic static substitution
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md:159-162`).
`RG-0` is stricter: those blocks remain rejected even after constants are filled, until
their executed bytes are migrated into the restricted language.

A separate RG-0 projection or manifest generated from the current scripts would not fix
this. The thing proved must be the thing executed. The accepted boundary names the exact
complete same-shell compositions and calls block-only results supplemental
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:217-223`).

## Rejection semantics

The usable fail-closed behavior is an explicit, atomic disposition:

```text
PATHSCOPE file=<digest> verdict=UNANALYSABLE rc=3
reason=outside_restricted_grammar line=<n> byte=<offset> expected=<production>
```

- A lexical or grammar mismatch, unknown tool, unconsumed operand, unresolved constant,
  unsupported semantic contract, or internal parser failure produces `UNANALYSABLE`, rc
  3 for the **entire proof unit**. Partial path rows may be printed as diagnostics, but
  they can never support PASS.
- A fully analyzed path or endpoint outside the allowlist is `FORBID`, rc 1. This is a
  resolved deviant result, not inability to analyze.
- A fully analyzed, allowlisted input is PASS, rc 0.
- No raw parser/tool exit is allowed to escape. A wrapper must translate an abnormal
  internal exit into `UNANALYSABLE reason=internal_error`, rc 3 and prevent freeze.

A generic hard crash is fail-closed only if every caller reliably treats every raw status
as non-accepting. It is less usable because it identifies neither the unsupported
production nor the source span, and it risks the repository's recorded raw-status
classification problem. Explicit `UNANALYSABLE` is safer operationally and more usable
provided the freeze gate treats rc 3 as an absolute block. The original prover contract
already assigns rc 3 to parse failure and unresolved constructs
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_PATHSCOPE_PROVER.md:20-24`),
and the later composite boundary says unknown commands, unconsumed options, dynamic
construction, and conservation mismatches are rc 3 and prevent freeze
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:219-223`).

This is still a hard failure **of the proof**, just not an unstructured process failure.

## What it buys

For an input that actually belongs to `RG-0`, the option establishes all of the following:

- the parser consumed the complete file under one published positive grammar;
- no unsupported shell construct or trailing token silently disappeared;
- every admitted tool/operand had a stable identity and exactly one terminal disposition;
- duplicate values and empty/colliding identities could not collapse;
- provenance stayed attached to the exact constant-derived segment that supplied it;
- every path and endpoint exposed by an admitted exact command contract was statically
  resolved from preregistered constants and checked against the lexical allowlist; and
- PASS meant both byte conservation and member conservation held.

That turns conservation over admitted values into a real proof about a completely
characterized language. It directly removes the same-class admission holes documented by
the audit, where inputs reached zero accounting or were collapsed
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md:33-50`).

It still does **not** prove:

- that either current real block or either complete current proof unit is safe; all are
  rejected unchanged;
- runtime symlink resolution, mount binding, or opened-object identity;
- that a pinned external executable has the modeled behavior or does not read implicit
  configuration, plugins, startup files, locale data, or other paths;
- correctness or authenticity of the constants table, allowlist, frozen file identity,
  or command-contract registry;
- shell startup behavior or inherited-environment effects before the first admitted line;
- semantics of inline Python, sourced files, nested interpreters, or any other rejected
  language;
- host state, execution authority, deployment safety, or any economic property; or
- the complete composite proof unless every executed component and nested program is
  either in `RG-0` or covered by a separate closed proof joined without a gap.

The current audit likewise says host/runtime binding, symlink resolution, and mount
boundaries were not verified
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:350-356`).

## Build cost and survival of Option C work

### Sourced estimates

The available decision record estimates **6-10 hours for the earlier Option C accounting-
layer redesign**, including design, implementation, Lead execution, and one audit
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:74-87`).
That estimate is not a restricted-grammar estimate and does not include rewriting the
real scripts. Reusing it here would present a guessed number as derived.

- Restricted parser and command-contract build: **NO SOURCED ESTIMATE**.
- Rewriting both complete proof units into `RG-0` without changing their intended
  behavior: **NO SOURCED ESTIMATE**.
- Reworking QA expectations and completing the required audits: **NO SOURCED ESTIMATE**.
- Total option cost: **NO SOURCED ESTIMATE**.

Widening `RG-0` until the existing scripts pass is not a cost-free alternative. The real
sources demonstrate functions, stateful assignments, compound control flow, tests,
arrays, descriptor operations, here-strings, options, command substitution, and embedded
Python. Admitting those forms recreates a large shell-plus-nested-language semantic
surface instead of the small subset scoped here. No source provides a defensible effort
number for that wider design.

### What survives

| Existing asset | Survival under restricted grammar | Evidence and limit |
|---|---|---|
| Conservation/accounting invariant | **Survives conceptually** for RG-0 members: stable identity, segment provenance, and one terminal disposition remain the downstream rule. | The available pre-fifth-cycle implementation is not reusable as accepted evidence: its audit found disappearing members, provenance laundering, and multiplicity collapse (`PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md:183-221`). Exact later Option C code survival is **UNKNOWN** because the named 2026-08-16 record is absent. |
| Allowlist and constant inputs | The data contracts can remain inputs, but exact code reuse is **UNKNOWN**. | The original contract already takes a shell file, constants table, and allowlist (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_PATHSCOPE_PROVER.md:17-24`). RG-0 narrows how constants may enter the script. |
| Existing parser | Not acceptance authority unchanged. A total positive RG-0 parser is required. Reusable lexer/utilities: **UNKNOWN**. | The earlier Option C record said “Keep the parser,” but that option changed only the accounting layer (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:74-87`). Restricted admission is a different design. |
| Fixture corpus | **Survives as input/falsification material.** Fixtures outside RG-0 become expected `UNANALYSABLE` tests; inside fixtures still exercise path and provenance accounting. Exact unchanged assertion count: **UNKNOWN**. | The published corpus contains 105 fixture cases (`SELF_QA_PATHSCOPE.md:954`). The prior Option C decision also states that existing fixtures stay valid as regression evidence (`PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:86-87`). |
| QA runner/harness | **Harness mechanics survive**: identity checks, deterministic reruns, RED/GREEN execution, and result capture remain useful. Grammar-specific expected output must change. Exact byte or percentage reuse: **UNKNOWN**. | The prior Option C decision says the harness stays valid as regression evidence (`PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:86-87`). |
| Real proof-unit scripts | **0/2 units survive unchanged as acceptable input.** | The source census above establishes excluded constructs in both blocks and both wrappers. |

The sourced conclusion is not “most survives.” The sourced conclusion is narrower: the
test corpus, harness mechanics, and the accounting invariant remain useful; the parser's
acceptance layer changes; every real proof unit requires migration; and the exact overall
reuse percentage is **UNKNOWN**.

## Failure demonstration in full

No execution is needed to construct the surviving failure:

1. The frozen constants bind `CAT=/usr/bin/cat` and
   `APPROVED_ROOT=/approved`.
2. The exact `cat` command contract consumes one positional filesystem operand.
3. The complete RG-0 file is `${CAT} "${APPROVED_ROOT}/link"` plus LF.
4. Byte conservation and member conservation both hold. The expanded lexical path
   `/approved/link` matches the lexical allowlist `/approved/**`, so the static result is
   PASS.
5. In the runtime world, `/approved/link` is a symlink to `/outside/payload`, or
   `/approved` contains a mount that exposes an outside object. `cat` opens the outside
   object.

This failure does not falsify the closed grammar; it falsifies any stronger claim that a
closed lexical grammar by itself proves runtime object containment. The tool's current
machine-readable semantics already disclose exactly that boundary
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py:2936-2938`).
Closing it would require a separate runtime path-object binding proof, which is outside
this option and has **NO SOURCED ESTIMATE** here.

## Owner decision lines

AUTHORIZE: I authorize the RG-0 Pathscope restricted-grammar option exactly as scoped here: implement the closed parser and atomic `UNANALYSABLE` rc 3 semantics, migrate the exact Stage-1 proof-unit scripts only as necessary without changing their intended behavior, and complete the applicable T0/T1 audits before any acceptance or freeze; this grants no host, deployment, or economic action.

REJECT: I reject the RG-0 Pathscope restricted-grammar option; do not implement it or rewrite any proof-unit script for it, and leave all Pathscope and downstream authority unchanged.
