# KICKOFF — GLM-5.2 T1 audit: path-scope prover round 2 (Codex is filter-blocked on this tool)

You are GLM-5.2 via the Z.AI Coding Plan route, acting as the T1 auditor for this round.
Codex `gpt-5.6-sol` — the normal flagship auditor of record — cannot audit this artifact:
its provider content filter terminates the run while merely READING `pathscope_prover.py`,
because the prover's sink-detection source contains attack grammar (forbidden-path tables,
exfil URL patterns, ssh/nss host grammar) as data. That is a concrete tooling blocker, not a
finding. Per the audit-tier policy this T1 tool has a >300-line diff, so GLM is authorized to
carry the audit; the Lead records Codex's unavailability.

Read-only: edit nothing, no git mutation, no host, no network. Audit in place at commit
`37a87046` (or the current working tree — `pathscope_prover.py` is not under concurrent
edit). Prove you changed nothing: `git status --porcelain` empty at the end.

## Bytes under audit

`pathscope_prover.py` 122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`.
`SELF_QA_PATHSCOPE.md`, `STATUS_PATHSCOPE.md`, `PATHSCOPE_REPAIR_R2_REPORT.md`.

## Round-1 findings (Codex, REQUEST_CHANGES ×9, four CRITICAL)

`PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` — silent-sink classes 1–4 (a Bash fragment reached
a filesystem/network primitive while the prover emitted no path, no UNRESOLVED, and
`verdict=PASS rc=0`); 5 (tilde false-ALLOW); 6 (lexical membership shown as unconditional
host ALLOW); 7; 8; 9.

## Round-2 evidence

`PATHSCOPE_REPAIR_R2_REPORT.md`. Structural change: `NO_PATH_COMMANDS`/`nonoption_operands()`
removed; explicit `Spec` registry declares per command every accepted option and its value
role; an unlisted option or unregistered command → a specific rc-3 coverage record. Finding 6
repaired as DISCLOSURE (`ALLOW-LEXICAL` + `symlink_resolution=not_established
mount_boundary=not_established`), symlink/mount binding recorded as residual R1 a static
reader cannot perform. Five more silent-pass classes fixed. The Lead re-ran the published
harness verbatim; stdout matched the document exactly (R2 sha256; both block digests; RED
511 / GREEN 644 lines; determinism `equal=True` for find_exec, RP6-P0, RP7-WPI-RO).

## Audit contract

1. Re-run the published harness (`SELF_QA_PATHSCOPE.md` §"How to reproduce"): confirm the 62
   fixtures + 4 real-block runs and RED-before-GREEN (D026). A canonical auditor that cannot
   execute the suite returns supplemental, not acceptance — so actually run it and record it.
2. Adversarially construct NEW Bash fragments that reach a filesystem/network primitive while
   the prover still emits no path / no coverage record / `PASS rc=0`. Any surviving silent
   sink is CRITICAL. This is the core test — the round-1 findings were exactly such fragments.
3. Judge finding 6: is `ALLOW-LEXICAL` + residual R1 an honest, explicitly-labelled limit, or
   does any run still present lexical membership as an unconditional host ALLOW? An
   honestly-scoped weaker claim is acceptable for a T1 tool whose composite proof is SEC102.
4. Verify determinism and the coverage-error (fail-closed) behaviour on an unmodeled syntax.
5. Verdict grammar: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. If you cannot execute
   the suite, say so plainly and mark your opinion supplemental — do not print PASS on a read.

Write ONE new file: `PATHSCOPE_GLM_T1_AUDIT_R2_2026-08-11.md` (GLM gates execution, so if you
cannot run the harness, mark the run steps `PENDING-LEAD-EXECUTION` and the Lead runs them).
