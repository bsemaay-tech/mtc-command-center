# Section 10.2 composite path-proof status

Date: 2026-08-12
Status: `ACCEPTED-WITH-DISCLOSURE (owner decision 2026-08-12 ~13:10)`

## OWNER DECISION 2026-08-12 ~13:10 — ACCEPT WITH DISCLOSURE (binding)

The owner was presented with three options in
`SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md` and **chose Option 1, the Lead
recommendation: ACCEPT WITH DISCLOSURE.** Harness hardening is CLOSED as a work item; no round
12 is authorized. This decision was reached with Codex's explicit concurrence — its round-11
verdict states "do not open a round-12 harness-hardening cycle; the Lead should take the
accept-with-disclosure boundary to the owner for adjudication."

**What is accepted.** The production module `composite_pathproof.py` — byte-identical across
rounds 8, 9, 10, 11 and HEAD (129658 B, SHA-256
`adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`), Codex-re-derived at every
round — together with its evidence harness at round 11. All rounds 9-11 were harness-only; not
one module byte changed while the harness was hardened.

**Closed and cross-model verified:** both original CRITICALs (basename member-binding → exact
deploy-path matching; allocation ↔ constants reconciliation); the command-word WHITELIST
fixpoint (a command word is a benign leaf only if every character is in a proven-safe set —
closes extglob and every future operator at once); R3-F2/R3-F3; and the evidence-harness chain
r7 child-completion → r8 byte-identity → r9 direct-object binding → r10 transient-rebind and
mixed-chain → r11 nameless-channel construction. The 58-case module matrix and the eleven
published evidence blocks reproduce verbatim at every round.

**Accepted TRUSTED-BASE assumptions (disclosed, NOT proven — this is what "with disclosure"
means).** Each is a property of the developer machine, not of the security logic; all four
require an actor who already controls this host:

1. **The outer Python runtime** (Codex R11-F1, 2026-08-12): the `python` that runs the §13
   evidence harness, its startup mode, import graph, startup environment and standard library
   are trusted, not bound. The published launch is bare `python -B`
   (`isolated=0 safe_path=0 no_site=0 ignore_environment=0`), so an actor controlling the
   wrapper directory or the Python startup/import environment could shadow `subprocess` and
   fabricate transport or completion.
2. **The interpreter image** (residual 51): `powershell.exe` is located by name from `PATH`; a
   different program could receive the intended bytes. Codex adjudicated this disclosure
   HONEST as written — labelled out-of-model, presented as neither prevention nor detection.
3. **On-disk document vs a fresh clone** (residual 41): byte identity is asserted against the
   document as materialized on this disk, not a pinned checkout. A CRLF-materializing fresh
   clone changes the published LF/CRLF/SHA cross-check and makes block 11 fail **LOUDLY**; it
   does not pass silently.
4. **Interpreter vocabulary**: the recognized-interpreter name set is a production-gate item to
   be pinned at production-gate time, not a static-tool defect — **already owner-ratified
   2026-08-12 as decision C**.

**GLM-5.2 second-opinion evidence — ATTACHED 2026-08-12 ~14:05.**
`SEC102_GLM_T1_2ND_OPINION_2026-08-12.md`: **PASS-WITH-NITS (source-level; honestly
SUPPLEMENTAL on execution).** GLM independently re-derived the module identity and could not
defeat the command-word whitelist by adversarial source read; it confirmed both original
CRITICALs closed in code, the fail-closed direction real, exactly one execution sink, and all
four disclosed residuals honest and not dressed as controls (including Codex R11-F1). It could
not execute the harness — unattended GLM dispatch is approval-gated on this host — and it
refused to fabricate a green run, marking its execution opinion `PENDING-LEAD-EXECUTION`; the
Lead has run every published harness verbatim at each round, and Codex reproduced them
independently. One NIT, not a required repair and already inside disclosed item 8: a safe-set
leaf that re-consumes a declared member's deploy path as a literal operand is missed by the
orphan-only reachability gate — carry as successor-preregistration wording.

**Consequences.** WP-I freeze blocker #4 (SEC102) is **CLEARED** — the owner's boundary decision
is made and the model-diverse second-opinion evidence is attached. The four assumptions above must be
carried into the successor preregistration as explicit trusted-base statements, and no successor
text may present any of them as a control. If the owner later wants assumption 1 or 2 bound, that
is separately authorized design work (an exact trusted interpreter route with isolated/no-site
startup and no user-controlled import root) — **not** a continuation of this harness cycle.

---

Prior status line (superseded by the decision above):
`ROUND-11-AUTHORED-SELF-QA-PASS-PENDING-INDEPENDENT-ACCEPTANCE`
Audit tier: T1 - local-only non-economic Python tooling and fixtures. Round 2 was audited by
the Claude flagship (verdict **BLOCK**, two CRITICAL). Round 3 repaired that BLOCK and was
audited by Codex `gpt-5.6-sol` (`SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md`, verdict
**REQUEST_CHANGES**: both CRITICALs confirmed closed, three MEDIUM findings raised). Round 4
repaired those three MEDIUMs and was audited by Codex (`SEC102_CODEX_T1_AUDIT_R4_2026-08-11.md`,
verdict **REQUEST_CHANGES**: R3-F2 and R3-F3 CLOSED, **R3-F1 reopened as CRITICAL**). Round 5
repaired that CRITICAL and was audited by Codex (`SEC102_CODEX_T1_AUDIT_R5_2026-08-11.md`,
verdict **REQUEST_CHANGES**: named-fd, indexed-assign and unmodeled-prefix confirmed closed,
**R5-F1 raised as CRITICAL** - a pathname-expanded command word still leafed a hidden
interpreter). Round 6 repaired that CRITICAL and was audited by Codex
(`SEC102_CODEX_T1_AUDIT_R6_2026-08-12.md`, verdict **REQUEST_CHANGES**, materially narrowed: the
interpreter-vocabulary residual and the conservative false stops were **ACCEPTED** as scoped
limitations, and one finding was raised - **R6-F1**, the round-6 expansion blacklist missed the
`extglob` operator family). Round 7 is the repair of R6-F1. Round 7 was audited by Codex
(`SEC102_CODEX_T1_AUDIT_R7_2026-08-12.md`, verdict **REQUEST_CHANGES**, and materially narrowed
again): **the command-word whitelist was CONFIRMED a FIXPOINT for its class - the one-class
command-word regress that ran from round 4 to round 7 is over** - the interpreter-vocabulary
residual was **ACCEPTED** as an honestly disclosed production-gate decision, the conservative
false stops were **ACCEPTED** as fail-closed behaviour, and one finding was raised: **R7-F1**, in
the SELF-QA EVIDENCE HARNESS rather than in the module. Round 8 is the repair of R7-F1. Round 8
was audited by Codex (`SEC102_CODEX_T1_AUDIT_R8_2026-08-12.md`, verdict **REQUEST_CHANGES**,
narrowed again): **R7-F1 was CONFIRMED CLOSED** - the harness proves child status and adjudicates
stderr before it interprets stdout - both original CRITICALs, R3-F2/F3, and the command-word
fixpoint all stay closed, the interpreter-vocabulary limitation remains the sole disclosed
production-gate decision, and one finding was raised: **R8-F1**, again in the SELF-QA EVIDENCE
HARNESS rather than in the module. Round 9 is the repair of R8-F1. Round 9 was audited by Codex
(`SEC102_CODEX_T1_AUDIT_R9_2026-08-12.md`, verdict **REQUEST_CHANGES**): **R8-F1 was CONFIRMED
CLOSED and independently reproduced** - byte-mode extraction, write and read-back, both D026
directions, the M1 gate, all eleven blocks byte-identical, the 58-case matrix - the disclosed
round-9 residual was judged **honest**, and one finding was raised: **R9-F1**, for the third
consecutive round in the SELF-QA EVIDENCE HARNESS rather than in the module. Round 10 is the
repair of R9-F1. Round 10 was audited by Codex
(`SEC102_CODEX_T1_AUDIT_R10_2026-08-12.md`, verdict **REQUEST_CHANGES**): **direct same-object
modification and replacement under the pin was CONFIRMED CLOSED and independently reproduced** -
the real `ERROR_SHARING_VIOLATION`, both D026 directions, M1/M2/M3, all eleven blocks pinned and
byte-identical, the 58-case matrix, the section-13d transcript exact - every earlier SEC102
verdict was conserved, and **two** findings were raised: **R10-F1** (a transient DOS-device rebind
applied after the pre-launch sample and restored before the post-run sample escapes a two-sample
detector) and **R10-F2** (the leaf-to-root loop counts handles without proving one coherent
current chain) - for the fourth consecutive round in the SELF-QA EVIDENCE HARNESS rather than in
the module. Round 11 is the repair of R10-F1 and R10-F2, implemented by `claude-opus-5` xhigh. No
audit or acceptance is claimed by the implementer.

## Round 11 - what changed and why

### R10-F1 and R10-F2 - the proof was still bound to a NAME the child re-resolved, CLOSED in round 11 by removing the name

Both round-10 findings are the same defect at two depths. Round 10 handed
`powershell.exe -File <pathname>` a name and then worked to make the name trustworthy: it pinned
the leaf, pinned every component, measured the exclusion, bound the name to the pinned object, and
re-sampled the binding after the child exited. Codex r10 showed that a *transient* re-pointing of
the DOS-device/volume mapping - applied after the pre-launch sample, restored before the post-run
sample - passes both samples while the child resolves the same pathname to different bytes
(R10-F1), and that `PATH_PIN_HELD=7` records seven opens rather than one coherent current chain
(R10-F2). Design Defect Pattern 11 with Patterns 3, 6 and 9 overlays.

This was the **fourth** consecutive harness finding of one shape: round 7's harness never
established that the child *completed*; round 8's never that it was handed *this document's
bytes*; round 9's never that those bytes were *still there when the interpreter opened them*;
round 10's never that *nothing re-pointed the name between the two samples meant to notice*. Round
11 therefore does not add a third temporal sample. It removes the layer the class lives in -
**mutable name resolution** - from the only place that decides anything, the channel the
interpreter consumes. This is the same inversion that ended RP6's line-granularity regress and
SEC102's own command-word regress: replace the thing that can always be refined once more with a
construction that has no such dimension.

**The construction.** The wrapper runs
`powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command
"& ([scriptblock]::Create([Console]::In.ReadToEnd()))"` and writes to that child's standard input
the byte string it read **through the pinned handle** and compared with the fence - the identical
Python object (`EXEC_BUFFER_IS_PINNED_READ=1`), not a re-read and not a file. The child's whole
argument vector contains **no path separator** (`ARGV_PATH_SEPARATORS=0`, printed per block).
Between the compared bytes and the executed bytes there is no directory entry, no pathname, no
drive letter, no DOS device, no mount point, no junction and no volume. **Executed-byte binding is
now a property of the construction rather than the output of a detector**, so no post-run sample
is load-bearing and there is no interval for a same-session actor to occupy.

**The chain is built rather than counted** (R10-F2). The work directory is pinned first; the
wrapper then MEASURES, in both directions on a throwaway subtree of its own, the NTFS property the
chain rests on - `ANCESTOR_RENAME_NOTHING_HELD=PERMITTED/0`,
`ANCESTOR_RENAME_DESCENDANT_HELD=DENIED/5`, `HELD_DIR_ENTRY_RENAME=DENIED/32`. It derives the
stable volume-GUID path **from the held handle** (`GetFinalPathNameByHandleW`, `VOLUME_NAME_GUID`),
opens the volume root, and opens every component below it **relative to its already-pinned parent**
with `NtOpenFile` and `FILE_OPEN_REPARSE_POINT`, recording an identity per link and requiring the
descent to terminate at the pinned object: `CHAIN_LINKS=7 CHAIN_RELATIVE_OPENS=6
CHAIN_IDENTITIES_RECORDED=7 CHAIN_ADJACENT_PAIRS_DISTINCT=6 CHAIN_TERMINATES_AT_PINNED_DIR=1
CHAIN_COHERENT=1`, with a per-link disposition line. A chain that is not coherent launches no
child at all.

Every round-10 gate is **conserved behind** the new channel: the pin, the read-through-pin, the
measured `ERROR_SHARING_VIOLATION` twice per block, the name-to-object binding, and both post-run
re-measurements. Their standing changed - under round 11 they can only reject, never admit - and
that is stated rather than glossed.

### The repair is measured, not asserted - both findings reproduced against the published round-10 wrapper first

`SELF_QA_SEC102_R11.md` section 13b extracts the published round-8, round-9, round-10 and round-11
wrappers **as bytes** from the documents that publish them, prints the SHA-256 of every instrument
and every mutant, and then:

- **R10-F1, deterministic.** The work tree of the wrapper under test is addressed through a **free
  drive letter** defined with `DefineDosDevice` (no privilege - it is what `subst` does) by scoping
  `TMP`/`TEMP` for that child process only. Three declared, counted substitutions route the child
  launch through a helper that re-points the letter at a mirrored shadow tree **after** the
  pre-launch sample and restores it **before** the post-run sample; the third substitution removes
  `.resolve()`, which would canonicalise the stand-in letter back to `C:` and would not have
  protected the real `C:`-rooted pathname either. Nothing is raced.

| Case | Round 10 + TRANSIENT | Round 11 + TRANSIENT |
|---|---|---|
| `transient_certified` - publishes the marker only the shadow tree can produce | **ACCEPTED - the finding** | **REJECTED** |
| `transient_honest` - publishes the marker its own bytes produce | **REJECTED - the finding, inverted** | **ACCEPTED** |

  `FALSE_ACCEPT_UNDER_R10=1`, `FALSE_REJECT_UNDER_R10=1`, `TRANSIENT_CLOSED_UNDER_R11=2`, and
  `R10_TWO_SAMPLE_DETECTOR=CLEAN/1` - round 10 printing `POST_NAME_BOUND=1 POST_BYTES_UNCHANGED=1`
  in the very run in which it certified a transcript its compared bytes cannot produce. That line
  is R10-F1 in the detector's own words.
- **`M4_named_channel` is the control experiment.** Same remap, same round-11 wrapper, same pin,
  same chain, same post-run samples - **one constant** flipped back to `-File <pathname>`. The
  false acceptance returns (`M4_CHANNEL_LOAD_BEARING=1`), which is what makes the channel the
  repair rather than a description of one.
- **R10-F2, deterministic.** One ordinary junction (`mklink /J`, no privilege) is re-pointed at the
  exact moment round 10's leaf-to-root loop has taken the leaf and has not yet reached the
  ancestor: `R10_PATH_PIN_COMPLETE=1` with `R10_CHAIN_MIXED=1` and `R10_LIVE_LEAF_UNPINNED=1` -
  a complete-looking set spanning two chains - against `R11_ANCHOR=OBJECT_VOLUME_GUID/1` and
  `R11_UNAFFECTED_BY_SWAP=1`. Both constructions are asserted to appear **verbatim** in the
  published wrapper bytes (`CONSTRUCTIONS_VERBATIM=1`).
- **The channel contract is proved, not assumed.** Every published block is run through both
  channels and must return the same rc, the same stderr length and byte-identical stdout:
  `CHANNEL_CONTRACT_CONSERVED=10 CHANNEL_CONTRACT_SELF_EXCLUDED=1` (the block containing the arm
  cannot run inside itself; its own conservation is measured by the section-13c run).
- **Round 10's arms are carried behind the new channel.** `CONSERVED_R10_VERDICTS=6`,
  `REBIND_DENIED_UNDER_R11=2` with `INPLACE_WRITE=DENIED WINERROR=32` and `ENTRY_REPLACE=DENIED`,
  `M1_GATE_FIRED=1`, `M2_EXCLUSION_MEASURED=1`, `M3_POST_RUN_GATE_FIRED=1`,
  `D026_PIN_PRECONDITION ... PIN_TAKEN=0 WINERROR=32`, `D026_OFF_EXPECTATION=0`. `M3` is the
  clearest statement of the new standing of the old gates: the rewrite succeeds, the child still
  executes the compared buffer, and gate 4 refuses the block anyway.

No attack fixture was authored. The drive letter is released and measured released
(`D026_DEVICE RELEASED=1`); the junction is removed; every child prints one line, exits non-zero,
writes one diagnostic, or counts CR bytes in text it carries itself.

### The one thing round 11 does NOT close, stated for the Lead's stop rule

The interpreter **image** is still located by name (`powershell.exe` from `PATH`), exactly as in
rounds 7-10. A same-session actor who can change what that name resolves to can arrange for a
different program to receive the bytes, and that program could print any transcript. This is
**neither prevented nor detected**, and it is deliberately not presented as either. It is outside
the model every round of this work has used - *"were the compared bytes the bytes that were
executed"* rather than *"which program executed them"* - but it has the same accepted-divergence
shape, so it is named here and in `SEC102_R11_REPORT_2026-08-12.md` rather than left for an audit
to find. It is item 51 below.

### Round 11 changed no code

`composite_pathproof.py` is **untouched**: same `129658` B / `adbf27fd…c05a` as rounds 7-10, and
the round-11 hygiene block asserts `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0`. No
fixture was added, so `.gitattributes` is unchanged at `1630` B / `40e356f8…5077` and is also
asserted worktree-clean. Every `powershell` block in sections 2-10 of the round-11 self-QA is
byte-identical to the round-10 self-QA. Every classification, rc, reason token and transcript is
the round-7 record re-executed by the repaired harness, not a new claim.

## Round 10 - what changed and why

### R9-F1 - the check was bound to a NAME, and the interpreter resolved that name again, CLOSED in round 10

The section-13 paste-and-run wrapper published in `SELF_QA_SEC102_R9.md` created a named temporary
file, wrote the fence bytes, **closed every handle**, re-opened the *name* to read the bytes back,
compared them with the fence, and then launched `powershell.exe -File <pathname>` - which resolves
that pathname a **second** time, after the equality decision has already been made and published.
Between the two resolutions the object is unowned: a concurrent process running as the same
principal can modify it in place or replace the directory entry, and the child then executes bytes
the parent never compared while `SCRIPT_BYTES_IDENTICAL=1`, the published SHA-256 and the
published `LF`/`CRLF` counts all describe the *earlier* bytes. Design Defect Pattern 11 (the
verified object is not the instrument the production caller opens) with a Pattern 9 overlay (the
unconditional claims *"no path through the wrapper on which unproven bytes are executed"* and
*"the instrument the interpreter is handed"* outrun a name-bound check).

Codex re-ran everything from exact bytes and reproduced all of round 9's numbers, so **no round-9
measurement is retracted**. The defect is temporal, not textual: it is the *interval* between the
proof and the interpreter's consumption. It is also the third harness finding in a row of the same
shape - round 7's harness never established that the child *completed*, round 8's never
established that the child was handed *this document's bytes*, round 9's never established that
those bytes were *still there when the interpreter opened them* - so round 10 closes the CLASS,
every window between verification and consumption, rather than the instance.

Round 10 takes route (A) of the kickoff, **object pinning**, and adds three gates ahead of round
9's and one behind them:

- **0a** every component of the script's path - the directory holding it and every ancestor up to
  the volume root - is opened and HELD with share mode `FILE_SHARE_READ`, so no component of the
  name can be renamed or deleted; if any component cannot be pinned, `PATH_PIN_INCOMPLETE` and
  **no child is launched at all**;
- **0b** the script object is pinned **before it is verified** (read sharing granted so the
  interpreter can open it, **write and delete sharing withheld**), the bytes are read back
  **through that handle** rather than by re-opening the name, and Windows is **asked** for the
  write handle and the delete handle the pin should forbid and must refuse both with
  `ERROR_SHARING_VIOLATION` (32) - otherwise `SCRIPT_NOT_PINNED` / `SCRIPT_BYTES_MISMATCH` and
  **the child is never launched**;
- **0c** the pathname the child will be given is resolved once more and must reach the pinned
  object - same volume serial number, same file index - otherwise
  `SCRIPT_NOT_BOUND_TO_PINNED_OBJECT` and **the child is never launched**;
- **1, 2, 3** process status, adjudicated stderr, published-subset comparison - rounds 8 and 9,
  conserved verbatim;
- **4** the handle is held across the child's **entire lifetime**, and after it exits the
  name-to-object binding and the pinned object's bytes are **both re-measured** - otherwise
  `SCRIPT_REBOUND_UNDER_PIN` / `SCRIPT_BYTES_CHANGED_UNDER_PIN` and **stdout is never read**.

The ordering is the repair: anything that happened to the file *before* the pin is caught by the
verification that happens *after* it, and nothing can happen *after* the pin at all. The mechanism
is one Win32 call with one share mode, but **the mechanism is not the evidence**: the exclusion is
measured eleven times, once per block, because *"I passed the right share mode"* is the same class
of claim as round 8's *"I called the API that does not translate"*.

### The repair is measured, not asserted - the finding at rc level, in both directions

`SELF_QA_SEC102_R10.md` section 13b runs the **published round-9 wrapper** and the **published
round-10 wrapper**, each extracted **as bytes** from the document that publishes it with its
SHA-256 printed, over synthetic documents written outside the repository. The window is made
**deterministic rather than raced**: `HOLD` is ONE textual substitution, the *same* one applied to
both published wrappers, inserting a genuinely separate same-principal process at the exact launch
boundary - after the equality decision, before the interpreter opens the name. It changes no gate
and no comparison; it only occupies the window. That process is a harmless **rewriter** which tries
to put a different benign marker line into the temporary script, first by writing in place and
then by replacing the directory entry, and prints what Windows told it.

| Case | The child | Round 9 + HOLD | Round 10 + HOLD |
|---|---|---|---|
| `rebind_certified` | prints `compared-bytes-executed`; the document publishes the `rebound-bytes-executed` transcript only the rewrite can produce | **ACCEPTED - the finding** | **REJECTED** |
| `rebind_honest` | the same child; the document publishes the transcript its own bytes really produce | **REJECTED - the finding, inverted** | **ACCEPTED** |

`FALSE_ACCEPT_UNDER_R9=1`, `FALSE_REJECT_UNDER_R9=1`, `REBIND_DENIED_UNDER_R10=2`,
`CONSERVED_R9_VERDICTS=6`, `M1_GATE_FIRED=1`, `M2_EXCLUSION_MEASURED=1`,
`M3_POST_RUN_GATE_FIRED=1`, `D026_OFF_EXPECTATION=0`. Row 1 is Codex's finding at rc level: round
9 reports `SCRIPT_BYTES_IDENTICAL=1` and a SHA-256 of the bytes it compared, then certifies a
transcript those bytes cannot produce, because it did not run them
(`R9_ASSERTED_IDENTITY=1 REBOUND_UNDER_R9=1` in the same run). Row 2 is the same defect inverted.
Under round 10 the rewriter reports `INPLACE_WRITE=DENIED WINERROR=32` and `ENTRY_REPLACE=DENIED`
on both vectors - the operating system's real refusal, not an argument that one would occur - and
six carried round-9 children conserve every round-9 gate.

Three harness mutants keep the new gates from being branches nothing ever takes. `M2` opens the
one constant that denies writers and is caught **before the child exists**, because round 10
measures the exclusion instead of trusting its own share mode (`WRITE_OPEN_DENIED=0`,
`SCRIPT_NOT_BOUND_TO_PINNED_OBJECT`, `CHILD_NOT_LAUNCHED`). `M3` opens that constant *and* drops
the pre-launch requirement - two substitutions, both declared and counted, because that is the
only way to reach the post-run gate - and the rewrite then succeeds, the child really does execute
bytes the parent never compared, and the block is refused with `POST_BYTES_UNCHANGED=0`,
`SCRIPT_BYTES_CHANGED_UNDER_PIN`, `STDOUT_NOT_INTERPRETED`. `M1` is round 9's mutant carried:
restore the round-8 translating write path and the pre-launch byte gate still fires. A fourth
measurement takes the pin's precondition directly on the primitive: while another process holds a
writable handle on the name, the pin **cannot be taken at all**
(`D026_PIN_PRECONDITION EXISTING_WRITER=1 PIN_TAKEN=0 WINERROR=32`), and a block whose object
cannot be pinned is refused rather than launched. Round 9's `D026_WRITEPATH` measurement on the
real artifact is carried unchanged. No attack fixture was authored; every child prints one line,
exits non-zero, writes one diagnostic, or reads its own script and prints a count.

### Round 10 changed no code

`composite_pathproof.py` is **untouched**: same `129658` B / `adbf27fd…c05a` as rounds 7, 8 and 9,
and the round-10 hygiene block asserts `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0`.
No fixture was added, so `.gitattributes` is unchanged at `1630` B / `40e356f8…5077` and is also
asserted worktree-clean. Every `powershell` block in sections 2-10 of the round-10 self-QA is
byte-identical to the round-9 self-QA - including the round-8 and round-9 wording in the section-9
comments, because a re-typed carried block is not a carried block. Every classification, rc,
reason token and transcript is the round-7 record re-executed by the repaired harness, not a new
claim.

## Round 9 - what changed and why

### R8-F1 - the harness executed different bytes from the ones it published, CLOSED in round 9

The section-13 paste-and-run wrapper published in `SELF_QA_SEC102_R8.md` read the self-QA through
newline-translating text I/O and wrote every temporary `.ps1` through
`NamedTemporaryFile("w", encoding="utf-8")` without disabling newline translation. On this
Windows host a published block containing **110 LF and zero CRLF** reached the interpreter as a
file containing **110 CRLF**: the written bytes were not the extracted bytes, while sections 0
and 13 claimed byte-for-byte extraction and execution. Design Defect Pattern 10 (the declared
evidence is not the executed evidence) overlaid by Pattern 11 (the instrument under test is not
the instrument on the page).

Codex re-ran all eleven blocks from their exact bytes and obtained the same accepted results, so
**no round-8 measurement is retracted** and none of the current blocks is line-ending sensitive.
The defect is in the INSTRUMENT: a reusable verifier that certifies a byte sequence it did not
run can certify a modified, line-ending-sensitive block instead of the block on the page.

Round 9 adds a **fourth test, ahead of the other three**:

0. the temporary script's bytes, **read back from the real file**, must equal the fence's bytes -
   otherwise the block is REJECTED with `SCRIPT_BYTES_MISMATCH` and **the child is never
   launched**;
1. the child's process status must be `0` - round 8, conserved verbatim;
2. the child's stderr must be empty, or the block must be named in `STDERR_CONTRACT` with a
   written reason - round 8, conserved verbatim;
3. **only then** is stdout read and compared with the published transcript - round 8, conserved
   verbatim.

The mechanism is `read_bytes` in, a bytes regex in the middle and `write_bytes` out, but **the
mechanism is not the evidence**: the file is read back off the disk and compared with the fence,
because *"I called the API that does not translate"* is exactly the class of claim round 8 made
and could not support. Each block's SHA-256, byte count, LF count, CRLF count and non-ASCII count
are printed for every block, so the identity and the composition of the executed instrument are
published rather than merely tested.

### The repair is measured, not asserted - the finding at rc level, in both directions

`SELF_QA_SEC102_R9.md` section 13b runs the **published round-8 wrapper** (extracted
byte-for-byte from the frozen `SELF_QA_SEC102_R8.md`) and the **published round-9 wrapper**
(extracted byte-for-byte from the round-9 self-QA) over six synthetic documents written outside
the repository. Both are extracted **as bytes**, because reading the instrument through
translating I/O would be the round-8 defect one level up, and the SHA-256 of the exact bytes
executed is printed. What decides the two new cases is a harmless **sentinel child that reads its
own script file and prints how many CR bytes it contains** - the only way to measure the bytes
the interpreter was actually handed rather than the bytes the wrapper intended to hand it.

| Case | The child | Round 8 | Round 9 |
|---|---|---|---|
| `well_behaved_child` | prints the published summary, exits `0` | ACCEPTED | ACCEPTED |
| `fails_after_summary` | prints the published summary, then `exit 7` | REJECTED | REJECTED |
| `stderr_after_summary` | prints the published summary, then writes one diagnostic to stderr | REJECTED | REJECTED |
| `published_line_absent` | prints a different line | REJECTED | REJECTED |
| `crlf_transcript_certified` | sentinel; LF-only fence bytes, transcript only the **rewrite** produces | **ACCEPTED - the finding** | **REJECTED** |
| `lf_exact_bytes` | sentinel; LF-only fence bytes, transcript those bytes **really** produce | **REJECTED - the finding, inverted** | **ACCEPTED** |

`FALSE_ACCEPT_UNDER_R8=1`, `FALSE_REJECT_UNDER_R8=1`, `CONSERVED_R8_GATES=4`, `M1_GATE_FIRED=1`,
`D026_OFF_EXPECTATION=0`. Row 5 is Codex's finding at rc level: round 8 certifies a transcript
its published bytes cannot produce. Row 6 is the same defect from the other side: round 8 cannot
reproduce a document whose transcript is honest about its own bytes. Rows 1-4 are round 8's own
cases and they conserve its repair - the wrapper is not a blanket reject, and the status, stderr
and subset gates all survive unchanged.

`M1` is the published round-9 wrapper with its one repair line - `path.write_bytes(command)` -
textually replaced by the round-8 write path, applied to the published bytes rather than to a
re-typed copy, so the new gate is shown **firing** (`SCRIPT_BYTES_MISMATCH`,
`CHILD_NOT_LAUNCHED`, `SCRIPT_BYTES_IDENTICAL=0`) rather than published as a branch nothing ever
took. The block also reproduces the write path difference directly on the self-QA's own first
`powershell` fence: `SOURCE_LF=110 SOURCE_CRLF=0 WRITTEN_LF=110 WRITTEN_CRLF=110
BYTE_IDENTICAL=0` under the round-8 path, `WRITTEN_CRLF=0 BYTE_IDENTICAL=1` under the round-9
path. The children are harmless: they print a line, exit non-zero, write one diagnostic, or read
their own script file and print a count. No attack fixture was authored.

### Round 9 changed no code

`composite_pathproof.py` is **untouched**: same `129658` B / `adbf27fd…c05a` as rounds 7 and 8,
and the round-9 hygiene block asserts `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0`.
No fixture was added, so `.gitattributes` is unchanged at `1630` B / `40e356f8…5077` and is also
asserted worktree-clean. Every `powershell` block in sections 2-10 of the round-9 self-QA is
byte-identical to the round-8 self-QA - including the round-8 wording in the section-9 comments,
because a re-typed carried block is not a carried block. Every classification, rc, reason token
and transcript is the round-7 record re-executed by the repaired harness, not a new claim.

## Round 8 - what changed and why

### R7-F1 - the evidence harness read output before it proved execution

The section-13 paste-and-run wrapper published in `SELF_QA_SEC102_R7.md` extracted every
`powershell` block from the self-QA, ran it from outside the repository, and compared its stdout
with the published transcript. **It never read the child's process status and never read the
child's stderr**, and it based its own exit solely on the mismatch counter. A child could
therefore emit exactly the published subset and *then* fail, or emit an unadjudicated diagnostic,
and the wrapper would report the block reproduced. Design Defect Pattern 6 (output interpreted
before execution completeness is proved) overlaid by Pattern 10 (the reusable verifier can
false-accept).

The defect was in the INSTRUMENT, not the subject. That is the reason it is not a minor finding:
every carried GREEN in the self-QA is quoted on that harness's authority, so a harness that can
false-accept devalues the whole evidence chain behind it.

Round 8 replaces the single stdout test with **three tests in a fixed order**:

1. the child's process status must be `0`;
2. the child's stderr must be empty, or the block must be named in an explicit `STDERR_CONTRACT`
   with a written reason;
3. **only then** is stdout read and compared with the published transcript.

**The order is the repair, not the counters.** A block failing (1) or (2) is REJECTED with
`STDOUT_NOT_INTERPRETED` and reaches `continue` before the comparison exists, so there is no path
through the wrapper on which an incomplete run's output is interpreted. `RC=` and
`STDERR_BYTES=` are printed for *every* block whether it passed or not, so the real status of
each child is published rather than merely tested. `STDERR_CONTRACT` is currently **empty**,
which is its strongest form: no block published in the self-QA may write anything to stderr, and
an entry would never waive test (1), because an adjudicated diagnostic is not an adjudicated
failure.

### The repair is measured, not asserted - D026 RED before GREEN

`SELF_QA_SEC102_R8.md` section 13b runs the **published round-7 wrapper** (extracted
byte-for-byte from the frozen `SELF_QA_SEC102_R7.md`) and the **published round-8 wrapper**
(extracted byte-for-byte from the round-8 self-QA) over four synthetic documents written outside
the repository. Neither wrapper is re-typed, and the SHA-256 of the exact bytes executed is
printed, so the instrument under test is the instrument on the page.

| Case | The child | Round 7 | Round 8 |
|---|---|---|---|
| `well_behaved_child` | prints the published summary, exits `0` | ACCEPTED | ACCEPTED |
| `fails_after_summary` | prints the published summary, then `exit 7` | **ACCEPTED - the finding** | **REJECTED** |
| `stderr_after_summary` | prints the published summary, then writes one diagnostic to stderr | **ACCEPTED - the finding** | **REJECTED** |
| `published_line_absent` | prints a different line | REJECTED | REJECTED |

`RED_UNDER_R7_GREEN_UNDER_R8=2`, `D026_OFF_EXPECTATION=0`. Both REDs also report
`UNREAD_STDOUT=1`, which is the ordering measurement: the round-8 wrapper refused to interpret
the child's stdout **at all**, rather than counting the failure and comparing anyway. The two
controls are load-bearing in the other direction - round 8 is not a blanket reject, and the
round-7 subset comparison survives the repair unchanged. The children are harmless: they print a
line, exit non-zero, or write one diagnostic. No attack fixture was authored.

### Round 8 changed no code

`composite_pathproof.py` is **untouched**: same `129658` B / `adbf27fd…c05a` as round 7, and the
round-8 hygiene block asserts `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0`. No
fixture was added, so `.gitattributes` is unchanged at `1630` B / `40e356f8…5077` and is also
asserted worktree-clean. Every classification, rc, reason token and transcript in the round-8
self-QA is the round-7 record re-executed by the repaired harness, not a new claim.

## Round 7 - what changed and why

### R6-F1 - the admission test is now a WHITELIST, so incompleteness fails closed

Round 6 asked whether a command word **contained** one of a listed set of expansion
metacharacters (`*`, `?`, `[`, `]`, `{`, `}`, `~`, `\`). The round-6 audit found that this list
missed the `extglob` operator family: one-or-more `+(...)`, exactly-one `@(...)` and negated
`!(...)` carry none of the listed characters, so with `extglob` enabled
`/usr/bin/ba+(s)h library.sh` pathname-resolves to `bash`, runs the operand, and round 6
classified it as a benign leaf and returned `PASS rc 0` over an unanalysed program.

Adding three characters would have bought one round. Rounds 4, 5 and 6 each closed a class after
it was found; the regress is structural, because **while the test enumerates what is forbidden,
completeness depends on the enumeration, and no static tool can prove an enumeration of shell
operators complete.**

Round 7 inverts the direction of proof. A command word is admissible as a proven-static benign
leaf **only when every character of the raw, pre-expansion word token is in an explicit safe
set**. Any other character - a known operator, an unknown operator, or a character with no shell
meaning at all - makes the word not proven-static, so it is UNMODELED and the stage STOPs.

* **The safe set is `[A-Za-z0-9._/:-]`** (`COMMAND_WORD_STATIC_RE`), and every member is admitted
  with a stated reason, not by convenience. `composite_pathproof.py:207-268` carries the full
  justification per character; `SELF_QA_SEC102_R7.md` section 1 reproduces it as a table.
* `?`, `*`, `+`, `@` and `!` - the five `extglob` operator characters - are all excluded, which
  refuses the whole family in one rule instead of by enumeration. `%`, `=`, quote characters,
  `,`, `^`, `#` and every other character are excluded because no proof was offered that they
  cannot resolve.
* **The kickoff's illustrative safe set `[A-Za-z0-9._/+=:@%-]` does not close the finding**, and
  this is measured rather than argued: `+` and `@` in it are two of the five `extglob` operators.
  It is mutation `M2` in the self-QA, and under it two round-7 REDs return to `PASS`. The
  implemented set is strictly smaller and the difference is the repair.
* One scanner change, which decides nothing: the scanner used to split a word at `(`, so
  `ba+(s)h` reached the classifier as the three fragments `ba+`, `s`, `h`. The `(` is now
  conserved INTO the raw token unless the token is a NAME (the function-definition form
  `fixture_main()`), so the safe set adjudicates the word Bash would look up. Mutation `M3` turns
  this off and kills nothing, because the safe set already refuses `ba+`; it is published as a
  correctness fix to what the classifier is shown, not as an independent guard.
* No reason token was added or renamed. Every refusal still reports
  `source_graph_unmodeled_command_word`, so no carried expectation moved.

### The closure claim, narrowed to exactly what the predicate proves

Round 7 proves this and only this: **no command-position word containing a character outside
`[A-Za-z0-9._/:-]` is admitted as a benign leaf or promoted to a modelled graph word, and no
word made only of those characters is refused.** That property is swept over all 95 printable
ASCII characters plus a non-ASCII sample, in four positions over six bases - 1919 variants,
`SWEEP_LEAK_ADMITTED=0`, `SWEEP_LEAK_OVERREFUSED=0` - and a second pass requires the refusal to
reach a terminal STOP rather than merely a class.

It does **not** claim the safe set is provably correct for every shell. It claims that an error
in the reading of the Bash grammar now produces a false STOP instead of a false PASS. That is a
better failure direction, not a proof.

It does **not** close the interpreter vocabulary (item 8), which remains the production-gate
blocker the round-6 audit accepted as a scoped limitation.

### What round 6 changed, carried forward

Round 6 is the round that inverted the classifier's DEFAULT (a command word must earn `leaf`
rather than inherit it) and taught interpreter recognition to take the last pathname component of
any word containing a slash. Round 7 changed how "proven-static" is decided; everything else
round 6 established is carried unchanged and re-measured.

### The superseded round-6 statement

The paragraph below is the round-6 record. It is retained because the round-7 self-QA carries
round 6's batteries, and its final sentence - that the expansion character set is itself a list -
is precisely the residual round 7 closes.

### R5-F1 - the command-word policy is now closed, not enumerated (round 6)

Rounds 4 and 5 each closed one command-word or prefix form *after it was found*: a numeric file
descriptor, then a named descriptor, then an indexed assignment. The round-5 audit then found a
fourth of the same shape - `_command_word_class` classified a pathname-expanded word such as
`/usr/bin/ba*h` as a benign leaf, so the script operand behind a runtime-resolved interpreter
was scanned by nothing and RENDER returned `PASS rc 0` over an unanalysed program.

The defect was not any one missing form. It was the classifier's **default**: an unrecognised
command word became a leaf, so every form nobody had enumerated inherited "benign". Closing
forms one per round cannot reach a fixpoint against that default.

Round 6 inverts the default. A command word is admissible as a benign non-edge leaf **only**
when it is a PROVEN-STATIC literal that is not a recognised interpreter or source builtin -
one word whose spelling is already the name Bash will look up, with no expansion of any kind
between the two. Every command word that is dynamic, expandable or substituted is UNMODELED
and the stage STOPs; it can never become a leaf, whatever it would have expanded to.

* New `COMMAND_WORD_SUBSTITUTION_RE` (`$`, backtick) - parameter, command and arithmetic
  expansion. Deliberately redundant with `_graph_opaque_reason`, so no single fence carries
  this class alone.
* New `COMMAND_WORD_EXPANSION_RE` (`*`, `?`, `[`, `]`, `{`, `}`, `~`, `\`) - pathname
  expansion, brace expansion, tilde expansion, and backslash-constructed names. Applied to the
  raw word including quoted regions: quoting suppresses some of these, but a proof that this
  particular occurrence is suppressed is exactly the reasoning the policy refuses to do.
* `_command_word_class` now returns the new `unmodeled` class for every such word plus for a
  degenerate/empty word, and `_graph_word_conservation` reports it as
  `source_graph_unmodeled_command_word`. Reserved words (`{`, `}`, `[[`, `]]`, `!`, `if` …)
  and assignment prefixes are matched **before** the fence and are unaffected.
* The reserved-word test now compares the RAW word instead of its unquoted literal. Bash only
  treats `if`/`{`/`[[` as reserved when written unquoted, so `"if"` is an ordinary command
  name; reading the literal promoted it to a reserved word and kept a command position open
  that Bash had already closed.
* **Found while probing the same boundary, not named in the audit:** interpreter recognition
  took the basename only for an *absolute* path, so `bin/bash script.sh` and `./bash script.sh`
  were leaves while `/bin/bash script.sh` was recognised - the same interpreter, the same
  operand, hidden by a spelling. Recognition now takes the last pathname component of any
  command word containing a slash. This is measured, not assumed: it is a separate RED fixture
  and a separate mutation discriminator.

Nothing else moved. **All four carried GREEN transcripts are byte-identical to the audited
commit `e3906cec`**, so no fence was weakened and no output surface was added.

### What round 7 does NOT close

The recognised-interpreter **vocabulary** is still a list, not a proof that the list is
exhaustive. A proven-static literal made only of safe-set characters that names an
executable-capable program the list does not contain is still a benign leaf. Rounds 6 and 7
closed *how a command word is admitted*; neither closed *which names are recognised*. That
remains the disclosed production blocker, accepted by the round-6 audit as a scoped limitation
at this stage, and no claim here weakens it.

## Stage coverage

**Rounds 8, 9 and 10 changed no stage.** The three subsections below are the round-7 record; all
three later rounds touched only the self-QA evidence harness, and the hygiene block asserts
`composite_pathproof.py` has no worktree modification.

### ALLOCATE

Unchanged from round 1. Six RED fixtures and one GREEN, same rc and reason tokens.
`sec102_r1_fixtures` has no worktree modification.

### RENDER

Everything round 6 implemented, with the round-6 expansion blacklist replaced by the round-7
safe-set whitelist and the round-7 word-boundary conservation, so every command word that is not
a proven-static safe-set literal reaches a named STOP.

### FREEZE

Everything round 6 implemented. FREEZE inherits the round-7 repair unchanged through the shared
`_derive_graph`, so `F3`/`F9` gain the same conservation; no FREEZE-specific code changed.

## Self-QA result (round 11)

- **Both round-10 findings reproduced against the published round-10 wrapper, then closed.**
  `FALSE_ACCEPT_UNDER_R10=1`, `FALSE_REJECT_UNDER_R10=1`, `TRANSIENT_CLOSED_UNDER_R11=2`,
  `R10_TWO_SAMPLE_DETECTOR=CLEAN/1`, `M4_CHANNEL_LOAD_BEARING=1`, `R10_PATH_PIN_COMPLETE=1` with
  `R10_CHAIN_MIXED=1` against `R11_UNAFFECTED_BY_SWAP=1` and `CONSTRUCTIONS_VERBATIM=1`.
  `D026_OFF_EXPECTATION=0`, `D026_HARNESS_BLOCK_RC=0`.
- **The nameless channel's precondition proved block by block:** `CHANNEL_CONTRACT_CONSERVED=10
  CHANNEL_CONTRACT_SELF_EXCLUDED=1` - identical rc, identical stderr length and byte-identical
  stdout under `-File <pathname>` and under the pipe, for every published block that can be run
  inside the arm.
- **Round 10's evidence carried behind the new channel:** `CONSERVED_R10_VERDICTS=6`,
  `REBIND_DENIED_UNDER_R11=2` with `INPLACE_WRITE=DENIED WINERROR=32` and `ENTRY_REPLACE=DENIED`,
  `M1_GATE_FIRED=1`, `M2_EXCLUSION_MEASURED=1`, `M3_POST_RUN_GATE_FIRED=1`,
  `D026_PIN_PRECONDITION EXISTING_WRITER=1 PIN_TAKEN=0 WINERROR=32`. Each wrapper and each mutant
  is extracted **as bytes** with its SHA-256 printed, so no re-typed instrument can pass for the
  published one.
- **The write-path difference reproduced on the real artifact, carried from round 9:**
  `D026_WRITEPATH=R8_TEXTMODE SOURCE_LF=110 SOURCE_CRLF=0 WRITTEN_LF=110 WRITTEN_CRLF=110
  BYTE_IDENTICAL=0` against `D026_WRITEPATH=R11_BYTEMODE ... WRITTEN_CRLF=0 BYTE_IDENTICAL=1`.
- **One coherent current component chain, with a disposition per link:** `CHAIN_LINKS=7
  CHAIN_RELATIVE_OPENS=6 CHAIN_IDENTITIES_RECORDED=7 CHAIN_ADJACENT_PAIRS_DISTINCT=6
  CHAIN_TERMINATES_AT_PINNED_DIR=1 CHAIN_COHERENT=1 CHAIN_ANCHOR=VOLUME_GUID`, with the platform
  property it rests on measured in both directions: `ANCESTOR_RENAME_NOTHING_HELD=PERMITTED/0
  ANCESTOR_RENAME_DESCENDANT_HELD=DENIED/5 HELD_DIR_ENTRY_RENAME=DENIED/32
  ANCESTOR_CHAIN_FROZEN=1 DIR_ENTRIES_FROZEN=1`.
- **All eleven blocks re-run from outside the repository, executed from the compared buffer with
  no pathname:** `BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 PINNED_ALL=11 LEAF_ON_CHAIN_ALL=11
  NAME_BOUND_ALL=11 NAMELESS_EXEC_ALL=11 POST_NAME_BOUND_ALL=11 POST_BYTES_UNCHANGED_ALL=11
  REJECTED_ON_BYTES=0 REJECTED_ON_BINDING=0 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0
  REJECTED_ON_STDERR=0 COMPARED=11 MISMATCHED=0 REJECTED=0`, with `ARGV_PATH_SEPARATORS=0
  EXEC_BUFFER_IS_PINNED_READ=1` and `WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32` on
  every block, and `EXEC_SHA256` equal to the digest of the bytes read through the pin. Every
  block reports `CRLF=0` and `NONASCII=0`, and every block's SHA-256 is published.
- **The outer wrapper's own status, witnessed by the shell that launched it, not by itself:**
  `OUTER_WRAPPER_RC=0`, `OUTER_WRAPPER_STDERR_BYTES=0`. The published section-13d transcript was
  re-derived on the final document bytes and is byte-identical across runs.
- **No code changed.** `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0` and
  `CARRIED_CLEAN=.gitattributes WORKTREE_CHANGES=0`, alongside `pathscope_prover.py` and
  `sec102_r1..r7_fixtures`. `HYGIENE_OFF_EXPECTATION=0`.
- Every round-7/8/9/10 measurement was re-executed by the repaired harness and reproduced: the
  58-case matrix (`CASES=58 FAILED_COUNT=0`), the scanner-boundary probe, the D026 pre-feature
  block, the 112-cell mutation matrix, the grammar battery, the 1919-variant fixpoint sweep, the
  round-5 prefix battery, the five round-3/round-4 discriminators, hygiene and artifact identity.
- Round 11 added no fixture, no reason token, no output surface and no module behaviour.

Literal commands and real output are in `SELF_QA_SEC102_R11.md`.

## Self-QA result (round 10, carried record)

- **The harness's own D026: 2 rebinding children x 2 published wrappers under a deterministic
  hold, 6 carried children x 2 published wrappers, plus three mutants and the pin precondition.**
  `FALSE_ACCEPT_UNDER_R9=1`, `FALSE_REJECT_UNDER_R9=1`, `REBIND_DENIED_UNDER_R10=2`,
  `CONSERVED_R9_VERDICTS=6`, `M1_GATE_FIRED=1`, `M2_EXCLUSION_MEASURED=1`,
  `M3_POST_RUN_GATE_FIRED=1`, `D026_PIN_PRECONDITION ... PIN_TAKEN=0 WINERROR=32`,
  `D026_OFF_EXPECTATION=0`. Each wrapper is extracted **as bytes** from the document that
  publishes it and its SHA-256 printed, as is every mutant, so no re-typed instrument can pass for
  the published one.
- **The rewriter's refusal in the operating system's own numbers:** `INPLACE_WRITE=DENIED
  WINERROR=32` and `ENTRY_REPLACE=DENIED` against round 10, `REBIND_EFFECTED=1` against round 9,
  from the same separate same-principal process at the same launch boundary.
- **The write-path difference reproduced on the real artifact, carried from round 9:**
  `D026_WRITEPATH=R8_TEXTMODE SOURCE_LF=110 SOURCE_CRLF=0 WRITTEN_LF=110 WRITTEN_CRLF=110
  BYTE_IDENTICAL=0` against `D026_WRITEPATH=R10_BYTEMODE ... WRITTEN_CRLF=0 BYTE_IDENTICAL=1`, on
  the self-QA's own first `powershell` fence - the block Codex measured.
- **All eleven blocks re-run from outside the repository with their REAL byte identity, binding
  and status published:** `BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 PINNED_ALL=11
  NAME_BOUND_ALL=11 POST_NAME_BOUND_ALL=11 POST_BYTES_UNCHANGED_ALL=11 REJECTED_ON_BYTES=0
  REJECTED_ON_BINDING=0 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0
  COMPARED=11 MISMATCHED=0 REJECTED=0`, with `PATH_PIN_COMPONENTS=7 PATH_PIN_HELD=7
  PATH_PIN_COMPLETE=1` and `WRITE_OPEN_DENIED=1 DELETE_OPEN_DENIED=1 WINERROR=32/32` on every
  block. Every child was launched over an object pinned before it was verified, returned `RC=0`
  with `STDERR_BYTES=0`, was still the same object with the same bytes after it exited, and only
  then had its output compared. Every block reports `CRLF=0` and `NONASCII=0`, and every block's
  SHA-256 is published.
- **The outer wrapper's own status, witnessed by the shell that launched it, not by itself:**
  `OUTER_WRAPPER_RC=0`, `OUTER_WRAPPER_STDERR_BYTES=0`. The published section-13d transcript was
  re-derived on the final document bytes and is byte-identical across runs.
- **No code changed.** `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0` and
  `CARRIED_CLEAN=.gitattributes WORKTREE_CHANGES=0`, alongside `pathscope_prover.py` and
  `sec102_r1..r7_fixtures`. `HYGIENE_OFF_EXPECTATION=0`.
- Every round-7/8/9 measurement was re-executed by the repaired harness and reproduced: the
  58-case matrix (`CASES=58 FAILED_COUNT=0`), the scanner-boundary probe, the D026 pre-feature
  block, the 112-cell mutation matrix, the grammar battery, the 1919-variant fixpoint sweep, the
  round-5 prefix battery, the five round-3/round-4 discriminators, hygiene and artifact identity.
- Round 10 added no fixture, no reason token, no output surface and no module behaviour.

Literal commands and real output are in `SELF_QA_SEC102_R10.md`.

## Self-QA result (round 9, carried record)

- **The harness's own D026: 6 synthetic children x 2 published wrappers, plus the M1 mutant.**
  `FALSE_ACCEPT_UNDER_R8=1`, `FALSE_REJECT_UNDER_R8=1`, `CONSERVED_R8_GATES=4`,
  `M1_GATE_FIRED=1`, `D026_OFF_EXPECTATION=0`. Each wrapper is extracted **as bytes** from the
  document that publishes it and its SHA-256 printed, so no re-typed instrument can pass for the
  published one. Every case also reports `R9_BYTES_ASSERTED=1`.
- **The write-path difference reproduced on the real artifact:**
  `D026_WRITEPATH=R8_TEXTMODE SOURCE_LF=110 SOURCE_CRLF=0 WRITTEN_LF=110 WRITTEN_CRLF=110
  BYTE_IDENTICAL=0` against `D026_WRITEPATH=R9_BYTEMODE ... WRITTEN_CRLF=0 BYTE_IDENTICAL=1`, on
  the self-QA's own first `powershell` fence - the block Codex measured.
- **All eleven blocks re-run from outside the repository with their REAL byte identity and status
  published:** `BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 REJECTED_ON_BYTES=0
  STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0 COMPARED=11 MISMATCHED=0
  REJECTED=0`. Every child was launched over a file proved byte-identical to its fence, returned
  `RC=0` with `STDERR_BYTES=0`, and only then had its output compared. Every block reports
  `CRLF=0` and `NONASCII=0`, and every block's SHA-256 is published.
- **The outer wrapper's own status, witnessed by the shell that launched it, not by itself:**
  `OUTER_WRAPPER_RC=0`, `OUTER_WRAPPER_STDERR_BYTES=0`.
- **No code changed.** `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0` and
  `CARRIED_CLEAN=.gitattributes WORKTREE_CHANGES=0`, alongside `pathscope_prover.py` and
  `sec102_r1..r7_fixtures`. `HYGIENE_OFF_EXPECTATION=0`.
- Every round-7/8 measurement was re-executed by the repaired harness and reproduced: the 58-case
  matrix (`CASES=58 FAILED_COUNT=0`), the scanner-boundary probe, the D026 pre-feature block, the
  112-cell mutation matrix, the grammar battery, the 1919-variant fixpoint sweep, the round-5
  prefix battery, the five round-3/round-4 discriminators, hygiene and artifact identity.
- Round 9 added no fixture, no reason token, no output surface and no module behaviour.

Literal commands and real output are in `SELF_QA_SEC102_R9.md`.

## Self-QA result (round 8, carried record)

- **The harness's own D026: 4 synthetic children x 2 published wrappers.**
  `RED_UNDER_R7_GREEN_UNDER_R8=2`, `D026_OFF_EXPECTATION=0`, both REDs with `UNREAD_STDOUT=1`.
  Each wrapper is extracted from the document that publishes it and its SHA-256 printed, so no
  re-typed instrument can pass for the published one.
- **All eleven blocks re-run from outside the repository with their REAL status published:**
  `BLOCKS=11 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0 COMPARED=11
  MISMATCHED=0 REJECTED=0`. Every child returned `RC=0` with `STDERR_BYTES=0`, so no block relied
  on the empty `STDERR_CONTRACT` and every stdout comparison was made over a run already proved
  complete. The ten round-7 blocks are the first ten; the D026 discriminator is the eleventh.
- **The outer wrapper's own status, witnessed by the shell that launched it, not by itself:**
  `OUTER_WRAPPER_RC=0`, `OUTER_WRAPPER_STDERR_BYTES=0`. The published section-13d transcript was
  then re-derived on the final document and is byte-identical across runs.
- **No code changed.** `CARRIED_CLEAN=composite_pathproof.py WORKTREE_CHANGES=0` and
  `CARRIED_CLEAN=.gitattributes WORKTREE_CHANGES=0`, alongside `pathscope_prover.py` and
  `sec102_r1..r7_fixtures`. `HYGIENE_OFF_EXPECTATION=0`.
- Every round-7 measurement below was re-executed by the repaired harness and reproduced: the
  58-case matrix, the scanner-boundary probe, the D026 pre-feature block, the 112-cell mutation
  matrix, the grammar battery, the 1919-variant fixpoint sweep, the round-5 prefix battery, the
  five round-3/round-4 discriminators, hygiene and artifact identity.
- Round 8 added no fixture, no reason token, no output surface and no module behaviour.

Literal commands and real output are in `SELF_QA_SEC102_R8.md`.

## Self-QA result (round 7, carried record)

- 58 cases, `FAILED_COUNT=0`. **All 52 round-6 cases carried unchanged in rc and reason token**;
  6 are round-7 additions. No carried fixture file was edited.
- D026 behavioural pre-feature: **4 of the 5 new RED fixtures are rc-level REDs** - `PASS rc 0`
  on `90868b86` to `STOP rc 3` under round-7 code (`+(`, `@(`, `!(`, and the unenumerated `%`).
  The fifth (`?(`) was **already `STOP rc 3` at `90868b86`** because `?` was on the round-6
  blacklist, and is carried as a control, not claimed as a new RED. The kickoff groups `?(`/`@(`
  as one class; the measured before-state is published rather than the grouping.
- Scanner boundary, both sides in one command: 49 probes, `OFF_EXPECTATION=0`. **10 forms that
  reach another program were silent on `90868b86` and are not silent now.** 13 benign forms
  remain correctly silent and 3 modelled interpreter/source forms still derive their edge, which
  is what distinguishes a repair from a blanket STOP. 9 forms are asserted as disclosed
  conservative stops so they cannot drift.
- D026 mutations: 7 discriminators run against **all 16 REDs** (5 round-7 + 7 round-6 + 4
  round-5) - a 112-cell matrix asserting its own expectation table, `OFF_EXPECTATION=0`.
  **`M1` restores the round-6 blacklist verbatim and returns exactly the four new REDs to
  `PASS`**, which is the discriminator the round-6 finding requires. `M2` does the same with the
  kickoff's illustrative safe set. `M5` widens the safe set to every printable character and
  shows the NARROWNESS carries the property. **`M3` (word-boundary conservation off) kills
  nothing** and is published as such.
- Command-word grammar battery: **all 59 round-6 forms carried**, 6 of them declared MOVED in
  advance (`"bash"`, `'source'`, `"if"` on quote characters; `2a=b`, `--opt=val`, `a-b=c` on
  `=`), plus 18 round-7 forms and a 7-form word-boundary table. `OFF_EXPECTATION=0`.
- **Fixpoint sweep: all 95 printable ASCII characters plus a non-ASCII sample, 4 positions, 6
  bases = 1919 variants. `SWEEP_LEAK_ADMITTED=0`, `SWEEP_LEAK_OVERREFUSED=0`, `SILENT_LEAK=0`.**
  The block also asserts that the safe set it measures against equals the one the module
  implements, so the sweep cannot drift from its subject.
- The round-5 prefix battery re-ran unchanged under round-7 code: 16/16 blind forms `rc 3`, 8/8
  controls `rc 0`, both round-6 disclosed stops unchanged. **No form moved between round 6 and
  round 7 in that battery.**
- The five carried round-3/round-4 discriminators all still restore their defective `PASS`.
- Python AST parse PASS; all 6 r7 JSON plans parse; all 18 r7 fixture files LF-only; every
  rendered `.sh` equals its `.in` with the fixture allocations substituted; deterministic
  repeated stdout over three runs for two new REDs and the new GREEN.
- `pathscope_prover.py` has no worktree diff; its pin is unchanged and the FREEZE GREEN
  transcript is the running proof. `sec102_r1..r6_fixtures` have no worktree diff.
- Every `powershell` block in `SELF_QA_SEC102_R7.md` was re-extracted from the document and
  re-run from a working directory OUTSIDE the repository: 10 blocks, 0 mismatched.

Literal commands and real output are in `SELF_QA_SEC102_R7.md`.

## Self-QA result (round 6, carried record)

- 52 cases, `FAILED_COUNT=0`. **All 44 round-5 cases carried unchanged in rc and reason token**;
  8 are round-6 additions. No carried fixture file was edited.
- 7 ALLOCATE regression cases: unchanged. 22 RENDER cases: 14 carried, 8 new. 23 FREEZE cases:
  unchanged.
- D026 behavioural pre-feature: **5 of the 7 new RED fixtures are rc-level REDs** - `PASS rc 0`
  on `e3906cec` to `STOP rc 3` under round-6 code (glob, bracket-glob, brace, tilde,
  relative-path interpreter). The remaining two (parameter expansion, command substitution)
  were **already `STOP rc 3` at `e3906cec`** and are carried as controls, not claimed as new
  REDs; the kickoff's expectation that they leafed into a PASS is not what the tool does, and
  the measured before-state is published rather than the expectation.
- Scanner boundary, both sides in one command: 32 probes, `OFF_EXPECTATION=0`. **12 forms where
  Bash reaches another program were silent on `e3906cec` and are not silent now.** 8 benign
  forms remain correctly silent and 3 modelled interpreter/source forms still derive their
  edge, which is what distinguishes a repair from a blanket STOP. 4 forms are asserted as
  disclosed conservative stops so they cannot drift unnoticed.
- D026 mutations: 6 new discriminators run against **all 11 REDs** (7 round-6 + 4 round-5) - a
  66-cell matrix asserting its own expectation table, `OFF_EXPECTATION=0`. **Every mutation that
  removes a round-6 fence leaves all four round-5 REDs intact**, which is the discriminator the
  round-5 audit required.
- Command-word grammar battery: 59 declared forms plus a generative closure sweep of 180
  variants (10 expansion characters x 6 bases x 3 positions). `SWEEP_LEAKS=0`: no word carrying
  an expansion or substitution character is admitted as a leaf or promoted to a graph word.
- The round-5 prefix battery was re-run as a round-6 regression: 16 of 16 blind forms still
  `rc 3`, 8 of 9 controls still `rc 0`, and **one round-5 control moved to a disclosed
  conservative stop** (`SEEN[0] "$ROOT/in.txt"`, a bracket-expression token in command
  position). The move is published, not tuned away.
- The five carried round-3/round-4 discriminators were re-run against round-6 code and all five
  still restore their defective PASS. **Three of the five round-5 discriminators no longer
  discriminate**, because the round-6 fence independently catches their forms; each is re-probed
  and its remaining role measured - `M4` (name binding) is still solely load-bearing, and `M1`,
  `M2`, `M5` still carry precision for benign controls that flip to STOP without them.
- Python AST parse PASS; all r6 JSON plans parse; all r6 fixture bytes LF-only; deterministic
  repeated stdout over three runs for two new REDs and one new GREEN.
- `pathscope_prover.py` has no worktree diff; its pin is unchanged and the FREEZE GREEN
  transcript is the running proof. `sec102_r1..r5_fixtures` have no worktree diff.

Literal commands and real output are in `SELF_QA_SEC102_R6.md`.

## What remains - every item is a limitation

Items 1-27 carry forward from round 5, with items 8 and 12 corrected as the round-5 audit
required. Items 28-31 are round-6 additions; items 30 and 31 are corrected below for round 7.
Items 32-36 are round-7 additions. Items 37-40 are round-8 additions, items 41-44 are round-9
additions and items 45-49 are round-10 additions; all three groups are about the EVIDENCE HARNESS.
**Item 8 is the production-gate blocker, and it is the interpreter-vocabulary limitation the
round-6/7/8 audits accepted as an honestly disclosed, owner-ratified production-gate decision -
rounds 8, 9 and 10 neither close it nor worsen it.**

1. These are synthetic fixture proofs. The production P0 and RO entrypoints, RP0 library and
   bootstrap, RP6, RP7, inline Python bodies, and exact candidate `verify_lock.py` blob have
   not been supplied in a plan and have not passed this tool.
2. **The deployed identity is a declared, lexically canonical string compared for exact
   equality. It is not host-object verification.** No host was contacted. Disclosed on every
   FREEZE report as `R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED`, `control=false`.
3. Symlink resolution and mount-boundary identity remain residual R1 disclosures, not
   controls.
4. ALLOCATE declares no deployed identity and makes no whole-program path claim.
5. The composite's constants mirror is narrower than the pinned prover's parser: a constant
   whose value expands another constant is refused, not modelled.
6. A constants binding the plan does not allocate is `RUNTIME_ONLY`, not stopped. The F10
   claim sentence is narrowed so it no longer overstates this.
7. **F10 STOPs on every plan allocation absent from the pinned constants table, with no
   exemption.** A plan that legitimately declares a render-only allocation which is never a
   runtime constant will STOP. This is a chosen false stop, taken over a second modelled
   grammar.
8. **THE PRODUCTION-GATE BLOCKER, unchanged by round 7. The command-word recognition vocabulary
   is a list, and a list can be short.** An executable-capable program absent from that list,
   written as a safe-set-only literal at a conserved command position, is still classified a
   benign leaf and derives no edge. What rounds 6 and 7 changed is the *exposure* of that
   residual: a word can only reach the vocabulary test if every character of it is proven inert,
   so an unknown name cannot be smuggled in behind an expansion of any kind. Round 5's statement
   that it "repaired how the scanner reaches a command word, not which names it recognises" is
   still true and still the residual. The round-6 audit accepted this as a scoped limitation at
   this stage; that acceptance is not a closure and round 7 does not claim to narrow it further.
   Executing an arbitrary program (`./child.sh`) is outside every modelled edge kind and always
   was.
9. Wrapper detection produces safe false stops by design: `find`, `time`, `env`, `xargs` and
   similar STOP even with harmless operands, because the composite does not model what they
   run.
10. FREEZE accepts only all-shell reachable composites. A `python_source` member STOPs at
    FREEZE and STOPs graph derivation at RENDER. The actual RO composite cannot yet PASS.
11. The analysis-unit builder supports only standalone direct `source`/`.` edges. It STOPs on
    `execute_source` and `inline_source`.
12. **CORRECTED IN ROUND 6, RESTATED IN ROUND 7.** RENDER graph analysis is intentionally
    incomplete and fail-closed. The round-5 wording said "dynamic command positions … STOP",
    which outran the predicate; the round-6 wording enumerated the expansions that STOP, which
    is what missed `extglob`. The accurate statement is now the whitelist itself:
    here-documents, line continuations, multiline quotes, command/process substitutions,
    `eval`, `alias`, every unmodelled prefix form, and **every command-position word carrying
    any character outside `[A-Za-z0-9._/:-]`** all STOP. That sentence needs no list of
    expansions, and its correctness does not depend on one. The residual is item 8: a
    safe-set-only literal outside the recognised vocabulary is still a leaf, and that is a
    vocabulary limit, not a command-position limit.
13. The generated analysis unit uses a synthetic `test -r` to preserve each bound source
    operand while substituting exact child bytes. It is not an executable or frozen
    deployment artifact.
14. Allocation-consumer checking is exact template-token conservation plus
    allocation/constants value conservation plus exact deployed-path operand binding. It is
    not full semantic shell dataflow.
15. `sys.executable`, used to launch the pinned prover locally, is an external-runtime
    dependency not pinned by the plan. **Round 6 ran under Python 3.14.2**; 3.12 is no longer
    installed on this machine, so the round-4 3.12 parse is not reproduced and nothing here
    establishes behaviour under 3.12.
16. The analysis unit and the prover/constants/allowlist snapshots are temporary local files
    removed at adapter exit. They are not frozen artifacts.
17. The implemented proof covers exact lexical filesystem and network operands. No closed
    runtime-descendant family or exact descendant manifest is implemented.
18. Bash startup sources, imported functions, inherited environment, interpreter identity,
    cwd, shell options, bootstrap PATH tools, temporary-path behavior, wrapper `/dev/null`
    opens, and RP6 exact venv binding remain production blockers from the design.
19. A prover input-read or constants/allowlist parse error does not emit seven counters; the
    composite STOPs on that incomplete output grammar rather than inventing zeros.
20. **28 of 33 prover-adapter arms remain undriven** by published fixtures. Round 6 drove no
    new arm; the count and classification are unchanged from round 4.
21. **The `.gitattributes` repair is inert until the Lead commits it**, because Git reads
    checkout attributes from the committed tree. Round 7 adds `sec102_r7_fixtures/** -text` to
    the same scoped file; the round-4 demonstration of the mechanism is not re-run. **Round 8
    adds no fixture and therefore no line**, and asserts the file worktree-clean instead.
22. The `.gitattributes` covers this directory only. Every other byte-pinned artifact in the
    repository - RP6, RP7, the block files, the preregistration drafts - carries the same
    pre-existing line-ending exposure and is outside this fence.
23. No archive was created or frozen. No host, dispatch, execution, deployment, or production
    Section 10.2 acceptance follows from a fixture PASS.
24. **The prefix model is claimed complete for Bash assignment words and redirections, and that
    claim is exactly as strong as one reading of the Bash grammar.** The accepted vocabulary is
    `NAME=`, `NAME+=`, `NAME[sub]=`, `NAME[sub]+=` with a bracket-free subscript, plus numeric
    and `{name}` descriptors abutting a redirection operator. Anything outside it that
    *resembles* either shape STOPs by name. Round 6 adds a second, independent net under this
    one: a prefix that degrades into a command-position word now also faces the closed
    admissibility policy, which is measured in the round-5-fence redundancy probe.
25. **`for` / `select` / `case` are argued safe, not repaired.** They bind a name like
    `function`/`coproc`, but a separator, newline or `)` re-opens the command position before
    any body command. Two probes measure this; it is not an exhaustive enumeration of
    reserved-word syntax.
26. **Round-5 conservative false stops, carried unchanged.** `{1}>...` and any brace word
    abutting a redirection whose interior is not a plain name STOP although Bash would treat
    them as ordinary words. An `arr[...` word carrying an `=` whose subscript the model cannot
    close STOPs although a user may have meant a command name.
27. **`raw.isdigit()` was narrowed to `^[0-9]+$` in round 5.** The old test accepted Unicode
    digits. The narrowing matches Bash and loses no edge, but it is a behaviour change and is
    recorded as one.
28. **Round-6 conservative false stops, superseded by the larger round-7 set in item 34.** Every
    command-position word carrying `*`, `?`, `[`, `]`, `{`, `}`, `~` or `\` now STOPs, whether
    or not Bash would actually expand that occurrence. Concretely: the `[` test builtin
    (`[ -f x ]`) STOPs, `\cat` STOPs, `~/bin/mytool` STOPs, and a subscript word without an
    `=` (`SEEN[0] "$ROOT/in.txt"`) STOPs - the last was a published round-5 control at `rc 0`.
    These are refusals, not detections, and the policy prefers a visible refusal to a proof
    that a particular occurrence was safe.
29. **Quoted occurrences are not excused.** `'*'` is a literal star to Bash but STOPs here. The
    fence reads the raw word, because deciding that quoting suppressed a specific expansion is
    the class of reasoning that produced R5-F1.
30. **SUPERSEDED IN ROUND 7, AND THE ROUND-6 CLAIM HERE WAS WRONG.** Round 6 stated that
    "`extglob`, `globstar` and similar option-enabled patterns are built from the same
    characters and are therefore covered by construction". **That sentence was false**, and the
    round-6 audit proved it: `+(`, `@(` and `!(` are built from characters the round-6 set did
    not contain. The residual it described - "the expansion character set is itself a list" -
    is exactly what round 7 removes, by inverting the test so there is no list of forbidden
    characters left to be incomplete. What replaces it is item 33.
31. **Three round-5 discriminators became non-discriminating in round 6.** `M1`, `M2` and `M3`
    no longer return their round-5 REDs to PASS, because the command-word fence catches those
    forms independently. Round 7 does not change this. The round-7 matrix runs all seven of its
    mutations against all four round-5 REDs and kills none of them, so the round-5 REDs are
    still guarded by the round-5 mechanisms and no round-7 claim rests on them.
32. **The safe set is a claim about the Bash grammar, and it is exactly as strong as one
    reading of it.** Six character classes are admitted with a stated argument each
    (`composite_pathproof.py:207-268`). No proof is offered that those arguments are correct.
    What the inversion changes is the FAILURE DIRECTION: an error in that reading now produces
    a false STOP instead of a false PASS. That is better, and it is not a proof.
33. **This is what replaces item 30.** There is no longer a list of forbidden characters that
    could be incomplete. There is a list of PERMITTED characters, and it can only be wrong by
    being too generous - a bounded, enumerable, six-entry claim an auditor can read in full -
    or too strict, which costs false stops and never a missed edge.
34. **The round-7 conservative false stops are larger than round 6's, and they are refusals,
    not detections.** New in round 7: any command word containing `+`, `@`, `%`, `=`, `,`, `^`,
    `#`, a quote character, or any non-ASCII character now STOPs. Concretely `g++`,
    `tool@1.0`, `--opt=value`, `"bash"`, `'source'`, `"if"`, `2a=b`, `a-b=c` and `cafe` with an
    accented `e` all STOP although Bash would run them harmlessly. Six of these were published
    round-6 classifications, and their movement is declared in advance in the round-7 grammar
    battery rather than discovered by an auditor.
35. **A non-NAME function definition is a new false stop.** `bin/foo() { ...; }` STOPs, because
    the scanner cannot distinguish it from an `extglob` pattern without deciding which shell
    options are set. Bash does accept some non-NAME function names; this refuses them.
36. **The word-boundary conservation covers `(` only.** A `)` abutting a word is still treated
    as a separator, because subshell and `case` syntax depend on that and no `extglob`
    construct begins at a `)`. This is an argument from the Bash grammar, not a sweep. It is
    also not load-bearing on its own: mutation `M3` turns the conservation off and kills no
    RED, because the safe set already refuses the fragments.
37. **The harness proves each child ran to completion; it does not prove the child ran the right
    thing.** Process status `0` plus empty stderr plus a published-subset match is a far stronger
    acceptance than round 7's, and it is still an acceptance of observed output from a process
    the self-QA itself wrote. The comparison is also still a SUBSET check: a block may emit more
    than it publishes, and a declared excerpt passes on the lines it publishes. Round 8 does not
    make the published transcripts exhaustive.
38. **The empty `STDERR_CONTRACT` is a property of the round-8 self-QA, not a general rule.** A
    future round whose block legitimately writes to stderr must add a named entry with a written
    reason; the mechanism exists so such a block is adjudicated rather than silently tolerated.
    An entry never waives the process-status test.
39. **The outer wrapper's own status is adjudicated by whoever runs it, not by itself.** Section
    13e of the round-8 self-QA publishes `OUTER_WRAPPER_RC` and `OUTER_WRAPPER_STDERR_BYTES` as
    measured by the launching shell. A wrapper cannot be the sole witness to its own completion,
    and this one does not claim to be.
40. **Round 8 measures no new property of `composite_pathproof.py`.** Every classification claim
    in the round-8 self-QA is the round-7 claim re-executed. If the round-7 evidence was wrong
    about the module, round 8 does not detect that; it guarantees only that a block which *fails*
    can no longer be reported as reproduced. The command-word whitelist that Codex r7 judged a
    fixpoint is unchanged, and so is the item-8 residual underneath it.
41. **Byte identity is asserted against the self-QA as it exists on disk, not against a pinned
    checkout.** The repository root sets `* text=auto` and this clone has `core.autocrlf=true`,
    so a *fresh* Windows clone would materialise `SELF_QA_SEC102_R9.md` with CRLF line endings;
    the round-9 wrapper would then faithfully execute those CRLF bytes and its assertion would
    still hold - about different bytes. Every block's `LF` count, `CRLF` count and SHA-256 are
    therefore published in section 13d, so a checkout that differs prints different numbers
    rather than passing silently. Pinning the self-QA documents in `.gitattributes` would close
    it; **round 9 did not, because the round-9 scope fence limits `.gitattributes` to fixture
    pins.** It is recorded here for the Lead to decide, not deferred quietly.
42. **The proof is byte identity, not interpretation identity.** All eleven blocks are pure ASCII
    (`NONASCII=0` on every block), so nothing published turns on how `powershell.exe` decodes a
    UTF-8 file with no BOM. A future block carrying a non-ASCII byte would be written exactly and
    could still be *decoded* differently by the interpreter - the item-4/Pattern-4 interpreter
    boundary, unchanged and not narrowed by round 9. The sentinel likewise measures the file the
    interpreter was handed, not what the interpreter did with it.
43. **The harness mutants are mutations of the published instrument, not independent
    implementations.** They show each gate is load-bearing - `M1` restores the round-8 write path
    and the byte gate fires before the child is launched, `M2` opens the pin's share mode and the
    exclusion measurement fires before the child is launched, `M3` opens it *and* drops the
    pre-launch requirement and the post-run re-measurement fires with the child's stdout unread -
    but a mutation cannot show that no other defeating path exists.
    **The class this item failed to name in round 9 is TEMPORAL REBINDING**, and its root is
    MUTABLE NAME RESOLUTION: a check bound to a *name* while the interpreter resolves that name
    again. Round 10 claimed the class closed by pinning the object and every component of its
    name; Codex r10 showed that was still a claim about a *name* and produced two more instances
    of it (R10-F1 transient rebind, R10-F2 counted chain). **Round 11 closes the class by removing
    the layer rather than the instance**: the interpreter is handed the compared buffer itself on
    a pipe, its argument vector contains no path separator, and no name is resolved between the
    comparison and the execution - so the class has no surface left to rotate onto. Round 11 adds
    `M4_named_channel`, which flips that one constant back and shows the false acceptance return.
    Items 50-52 state what the new construction does not reach; items 45, 46 and 48 are retired or
    rewritten below to say what round 11 changed about them.
44. **Round 9 measures no new property of `composite_pathproof.py`.** Every classification claim
    in the round-9 self-QA is the round-7 claim re-executed. Round 9 guarantees only that the
    block being re-executed is the block on the page, and that a block which fails cannot be
    reported as reproduced. Items 37-40 carry unchanged.
45. **RETIRED IN ROUND 11 - it was false as written, and the construction that replaced it does
    not need it.** Round 10 wrote: *"a per-session DOS-device or mount redefinition is not
    prevented by any share mode; it is detected by the post-run re-resolution."* Codex r10 (R10-F1)
    showed the detection claim was false for a **transient** redefinition applied after the
    pre-launch sample and restored before the post-run one, and round 11 reproduces that
    false acceptance against the published round-10 wrapper
    (`FALSE_ACCEPT_UNDER_R10=1`, `R10_TWO_SAMPLE_DETECTOR=CLEAN/1`). The item is retired rather
    than reworded because under round 11 the child resolves **no name at all**: a volume or
    drive-letter redefinition, transient or persistent, cannot change which bytes it executes.
    Section 13b applies and restores exactly such a redefinition around the child and round 11's
    verdicts do not move (`TRANSIENT_CLOSED_UNDER_R11=2`). The post-run re-resolution is kept, and
    kept honest: it is now a conservative refusal, not a detection anything relies on.
46. **RETIRED AS WRITTEN AND RESTATED AS ITEM 51.** Round 10's wording - *"the interpreter binary
    is not pinned"* - understated it. The problem is not that the image is unpinned but that it is
    **located by name**, which is the one mutable resolution round 11 does not remove. See item 51,
    which states it as an out-of-model disclosure with its consequence spelled out.
47. **A concurrent writer cannot get past the pin, but it can stop the run.** If another process
    already holds a writable handle on the temporary name, the pin cannot be taken at all
    (`ERROR_SHARING_VIOLATION`) and the block is refused before the child exists (`PIN_HELD=0`,
    `SCRIPT_NOT_PINNED`); section 13b measures this on the primitive. The integrity direction is
    closed - such a run refuses loudly instead of executing unproved bytes - but this is a
    denial-of-availability surface for a hostile local principal, which is a different property.
48. **The binding is a Windows property, and the exclusion is measured for two access classes.**
    `FILE_SHARE_READ` semantics are enforced by the Windows I/O manager and the filesystem;
    nothing here establishes equivalent binding on another operating system, nor for a temporary
    directory that is not a local NTFS volume. The wrapper measures the refusal of a write-open
    and of a delete-open - the two classes that carry modify, truncate, rename and delete - which
    is a demonstration that the lock is real, not an enumeration of the access-mask space.
49. **Round 10 measures no new property of `composite_pathproof.py`.** Every classification claim
    in the round-10 self-QA is the round-7 claim re-executed. Round 10 guarantees only that the
    block being re-executed is the block on the page, that it is still that block while the
    interpreter runs it, and that a block which fails cannot be reported as reproduced. Items
    37-44 carry unchanged, and item 41's checkout residual is explicitly still open. **Round 11
    carries this item verbatim for itself**: it measures no new property of the module either.
50. **The round-10 gates are conserved but one-directional, and that is a demotion, not a
    strengthening.** The pin, the measured `ERROR_SHARING_VIOLATION`, the name-to-object binding
    and both post-run re-measurements are all still present and still terminal, but under round 11
    none of them can admit a block - the pathname they are about is not the channel the bytes
    travelled. `M3` shows this directly: the rewrite succeeds, the child still executes the
    compared buffer, and gate 4 refuses the block anyway. A conservative refusal is the right
    failure direction and it is published as that, not as a control that closes anything.
51. **The interpreter IMAGE is still located by name, and this is neither prevented nor detected.**
    `powershell.exe` is resolved from `PATH` by `subprocess.run`, exactly as in rounds 7-10. A
    same-session actor who can change what that name resolves to can arrange for a different
    program to receive the bytes, and that program could emit any transcript, including a published
    one. **Round 11 makes no claim about it and does not dress it as a control.** It is outside the
    model every round of this work has used - *"were the compared bytes the bytes that were
    executed"*, not *"which program executed them"* - but it has the same accepted-divergence shape
    as R9-F1, R10-F1 and R10-F2, so it is stated here, in the self-QA (section 11, round-11
    statement 2) and in `SEC102_R11_REPORT_2026-08-12.md` for the Lead's stop rule, rather than
    left for an audit to discover. Closing it would need the image consumed without name resolution
    too (a section handle from an already-open image), which is a different and much larger change
    than this round's scope fence permits.
52. **The nameless channel changes one contract, measured rather than hidden, and the change is
    proved harmless for every published block.** `$PSCommandPath` does not exist when there is no
    script file; no published block uses it, and the two line-ending sentinels now carry their own
    text in a here-string, which measures the same property in both channels and in both
    directions. Every other contract is proved conserved block by block
    (`CHANNEL_CONTRACT_CONSERVED=10 CHANNEL_CONTRACT_SELF_EXCLUDED=1`; the excluded block's own
    conservation is measured by the section-13c run). Also carried from round 10 and now measured:
    the run holds read handles from the volume root down to its temporary directory for the length
    of the run, which denies other processes a rename or delete of those directories and of entries
    in its work directory - an availability side effect on a shared machine, named rather than left
    to be noticed.

## Artifact identity record

The complete per-artifact byte-count and SHA-256 table is in `SEC102_R11_REPORT_2026-08-12.md`
section 6, and in `SELF_QA_SEC102_R11.md` section 10, both re-derivable by the published command.
**Every entry is byte-identical to the round-7 table**, because rounds 8, 9, 10 and 11 changed no
code and added no fixture. Round 11 publishes the SHA-256 of every executed `powershell` block in
`SELF_QA_SEC102_R11.md` section 13d, together with each block's pin state, chain membership,
channel state and the digest of the exact buffer the interpreter received - which is the same
digest, because it is the same buffer. No commit was made.
