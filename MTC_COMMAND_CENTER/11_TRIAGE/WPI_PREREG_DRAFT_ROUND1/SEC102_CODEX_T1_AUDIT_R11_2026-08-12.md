# SEC102 Codex T1 audit — round 11

**Verdict: REQUEST_CHANGES.** One required MEDIUM finding remains in the evidence harness.
This verdict **does not close the SEC102 Codex flagship slot**.

Per the kickoff's standing convergence rule, this is another variant of the executed-byte class:
**do not open a round-12 harness-hardening cycle.** The Lead should take the explicit
accept-with-disclosure boundary below to the owner for adjudication.

Audit identity: Codex `gpt-5.6-sol`, fresh T1 audit, 2026-08-12. Scope commit:
`5f87cbc2600adeedf8235aa5f8f1981c97abd174`. No host, network, deployment, trading, Pine,
parity, or Git mutation was performed. Fixture output was redirected outside the repository.

## Required finding

### R11-F1 — MEDIUM — the outer Python transport is environment/import resolved, so the claimed script-byte fixpoint still has an unbound instrument

Design Defect Patterns **4 and 11**, with Patterns **9 and 12** as overlays.

The round-11 claim says that no same-session, in-model path remains by which executed script bytes
can differ from the compared bytes (`SEC102_R11_REPORT_2026-08-12.md:251-255`). That claim assumes
that the imported `subprocess.run` is the trusted CPython implementation which faithfully transports
its `input=` object. The published launch does not establish that assumption:

- The prescribed outer command is bare `python -B verify_selfqa_r11.py ...`
  (`SELF_QA_SEC102_R11.md:3255`; report line 348). `-B` disables bytecode writes; it does not
  isolate Python startup, ignore environment variables, disable `site`, or remove the script
  directory from the import path.
- The byte-extracted wrapper imports `subprocess` by name (`SELF_QA_SEC102_R11.md:2754`) and later
  calls `subprocess.run(...)` (`:3171`) after setting `payload = on_disk` (`:3153`).
- Reproducing the published launch flags returned
  `isolated=0 safe_path=0 no_site=0 ignore_environment=0`; `site` was loaded, user site was enabled,
  and the wrapper directory was the first import-search location.

A same-session actor who controls the directory in which the extracted wrapper is written, or the
Python startup/import environment, can therefore supply startup code or a shadow `subprocess`
module before the wrapper executes. That code can replace `subprocess.run`, send different or no
bytes to the child, or return fabricated rc/stdout/stderr. The wrapper can still print
`EXEC_BUFFER_IS_PINNED_READ=1`, because that is only the identity of the local object immediately
before the unbound call; it does not bind the implementation receiving that object.

This is not covered by disclosed residual 51. Residual 51 honestly says that a different program
may receive the intended bytes because `powershell.exe` is name-resolved. R11-F1 is one layer
earlier: an unbound parent runtime/import can change the bytes or fabricate completion even if the
intended PowerShell image would otherwise be selected. It is therefore another instance of the
same declared-instrument-versus-executed-instrument class, not merely the already-disclosed
interpreter-image residual.

**Required disposition — disclosure and owner decision, not round 12:**

1. Retract or narrow the unconditional statement that no same-session, in-model script-byte
   divergence path remains.
2. Put the outer Python executable, startup mode, import graph, startup environment, and standard
   library explicitly inside the trusted boundary, including the consequence that the harness does
   not bind them; then ask the owner whether to accept that boundary.
3. If the owner declines that boundary, a separately authorized design would have to bind and
   isolate the outer executor (at minimum an exact trusted interpreter route with isolated/no-site
   startup and no user-controlled import root). This audit does **not** recommend or authorize a
   round-12 implementation.

## Independently reproduced evidence

The r11 construction itself works under an honest outer Python/standard-library and PowerShell
trusted base:

- `composite_pathproof.py` has the same Git blob
  `0e00db0ef3324765118f4e313f8e1964d451bd70` at r8 `3f2c22ca`, r9 `ba929abc`, r10
  `a0ebac7b`, r11 `5f87cbc2`, and current HEAD: 129,658 bytes, SHA-256
  `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`.
- The first ten carried PowerShell fences are byte-identical between r10 and r11: `10/10`.
- The 58-case matrix ran verbatim: `CASES=58 FAILED_COUNT=0`, rc 0, stderr 0 bytes.
- Section 13b ran verbatim: rc 0, stderr 0 bytes. Its summary reproduced
  `FALSE_ACCEPT_UNDER_R10=1`, `FALSE_REJECT_UNDER_R10=1`,
  `TRANSIENT_CLOSED_UNDER_R11=2`, `CHANNEL_CONTRACT_CONSERVED=10`,
  `CHANNEL_CONTRACT_SELF_EXCLUDED=1`, `M4_CHANNEL_LOAD_BEARING=1`, and
  `D026_OFF_EXPECTATION=0`.
- The transient certified/honest pair reproduced RED under the published r10 wrapper and GREEN
  under r11. Reverting only the channel to the named `-File` form restored the false acceptance.
- The chain arm reproduced `R10_PATH_PIN_COMPLETE=1 R10_CHAIN_MIXED=1` and then
  `R11_ANCHOR=OBJECT_VOLUME_GUID/1 R11_UNAFFECTED_BY_SWAP=1`.
- The section-13c wrapper was extracted as bytes to an external directory. It returned
  `OUTER_WRAPPER_RC=0`, stderr 0 bytes, and:

  `BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 PINNED_ALL=11 LEAF_ON_CHAIN_ALL=11 NAMELESS_EXEC_ALL=11 STATUS_PROVED_COMPLETE=11 MISMATCHED=0 REJECTED=0`

- The measured chain was complete on this NTFS run:
  `CHAIN_LINKS=7 CHAIN_RELATIVE_OPENS=6 CHAIN_IDENTITIES_RECORDED=7 CHAIN_ADJACENT_PAIRS_DISTINCT=6 CHAIN_TERMINATES_AT_PINNED_DIR=1 CHAIN_COHERENT=1`.
- The full published section-13d transcript reproduced exactly: **55/55** lines, zero mismatch.
- I additionally ran the self-excluded block 11 both named and nameless. Both returned rc 0 with
  zero stderr and byte-identical stdout, closing the conservation question for that block in this
  audit run.

Within the trusted base just stated, the stdin path has no second script name or file read.
`payload` is an immutable Python `bytes` object; CPython's Windows `communicate()` writes it to the
pipe and closes stdin; PowerShell 5.1 reported UTF-8 input and executes
`ScriptBlock::Create([Console]::In.ReadToEnd())`. `ReadToEnd()` reaches EOF before construction, so
the child cannot parse a prefix while the honest parent is still writing, and it cannot read past
the closed pipe. All eleven published blocks were ASCII-only, avoiding a non-ASCII decode
ambiguity. No internal buffer-reuse, partial-write, encoding, scriptblock-construction, or
relative-open-chain divergence reproduced. R11-F1 is at the unbound executor/import boundary
around that construction.

## Adjudication of disclosed residual 51

The `powershell.exe` PATH-resolution disclosure is honest as written: it is labelled
out-of-model, is neither presented as prevention nor detection, and is materially different from
the script-byte transport once program identity is declared part of the trusted base. Closing it
would expand the work into executable-image identity and launch semantics.

That disclosure is nevertheless insufficient for acceptance because it names only the child
image. The outer Python/import boundary can subvert the transport itself and is not included in
the claimed trusted boundary. Owner acceptance would need to cover both boundaries explicitly.

## Thirteen-pattern review

| Pattern | Auditor disposition |
|---|---|
| 1 — STOP is not a result | Current run stops/rejects on all exercised failures; no new module finding. R11-F1 bypasses the intended adjudicator before that ordering. |
| 2 — Whose kernel answered? | Local Windows/NTFS-only claim is disclosed; no host claim or contact. |
| 3 — The leaf is not the path | R10 mixed-chain finding reproduced; relative volume-GUID descent terminated at the pinned work directory in r11. |
| 4 — Privileged/external child environment | **R11-F1:** outer Python startup/import environment is not isolated or bound. |
| 5 — Grammar completeness | Production prover bytes are unchanged; prior whitelist fixpoint remains conserved. |
| 6 — Status before stdout | rc and stderr precede stdout comparison; carried and direct runs reproduced. |
| 7 — Nonzero read is not EOF | PowerShell `ReadToEnd()` consumes to pipe EOF under the trusted runtime; current channel tests reproduced. |
| 8 — Name is not identity | Script object and relative chain identities reproduced; child and outer interpreter identities remain trust-boundary decisions. |
| 9 — Sentence outruns probe | **R11-F1:** "no path remains" outruns the unbound outer transport. |
| 10 — Evidence that cannot fail | RED/GREEN and M4 are discriminating and reproduced. See documentation nits below. |
| 11 — Declared instrument not executed | **R11-F1:** `subprocess.run` is declared by import, not bound as the real accepting caller. |
| 12 — Unmodeled behavior disappears | **R11-F1 overlay:** startup/import substitution has no unresolved marker or refusal. |
| 13 — Terminal disposition conservation | 58/58 and 11/11 conserved; current chain recorded all seven identities and six relative links. |

## Optional documentation nits

1. The kickoff states that the section-13d transcript matched `45/45`; the transcript actually
   contains **55** non-empty lines and independently matched **55/55**.
2. The report (`:243`) and self-adjudication (`SELF_QA_SEC102_R11.md:1860`) say the transcript
   prints no per-run temporary name, but its final `CWD=` value contains the author's UUID-stamped
   temporary path (`:3312`). Exact reproduction required reusing that published external CWD.
   This does not invalidate the 55/55 result, but the Pattern-10 wording should be narrowed.

## Slot and next action

Both original CRITICALs, R3-F2/F3, the command-word whitelist fixpoint, r7 child-completion, r8
byte-identity, r9 direct-object binding, and the r10 temporal/chain findings remain closed under
the trusted runtime used in the reproduced run. The new R11-F1 prevents an unconditional
executed-byte fixpoint and therefore prevents this audit from closing the Codex flagship slot.

**Next action:** STOP harness hardening, open no round 12, and present the expanded trusted-boundary
disclosure to the owner alongside existing residuals 41 and 51 and the owner-ratified
interpreter-vocabulary production-gate decision. The later GLM-5.2 T1 second opinion may add
detection, but it cannot convert this non-accepting flagship verdict into acceptance without the
owner's explicit boundary decision.
