# AUDIT KICKOFF — round 2 adversarial re-audit (Codex, T0, round 2 of max 3)

Same contract as `AUDIT1_KICKOFF_CODEX.md`: authorized private-repo test-infra design
audit, refute-not-confirm, local fixtures allowed, no remote host contact, write
exactly one output file `audit2/AUDIT2_REPORT.md` next to this file.

## Scope — read ONLY

- `AUDIT1_KICKOFF_CODEX.md`, `audit1/AUDIT1_REPORT.md` (your round-1 findings),
  `ROUND2_KICKOFF.md` (the binding change map), `round2/` (the deliverables under
  audit), `../01_RUNKIT/RP1-B3.sh` and `../01_RUNKIT/RP0-LIB.sh` (baselines),
  `../03_TRANSPORT/B3_STOP_ADJUDICATION.md`.

## Audit questions

1. **Finding closure**: for each of F1–F6, N1, and must-change items O1/O2/O3/O5 —
   CLOSED / PARTIALLY CLOSED / NOT CLOSED / REGRESSED, with the exact round2 line that
   closes it or the concrete failure scenario that still defeats it. Re-run your
   audit-1 refutation fixtures against the round-2 code (the decoy-JSON manifest, the
   symlinked-parent fixture, the name-mapped ownership case) and report actual rc and
   output.
2. **New-defect sweep**: the round-2 code added a python3 JSON verifier, a mount
   predicate, namespace binding, and no-temp classifiers. Attack the NEW code the same
   way you attacked round 1 — injection through the environment of the python child,
   parser behavior on huge/weird-encoding files, /proc parsing edge cases, the
   variable-capture stderr classifiers (multi-line diagnostics, embedded newlines,
   locale), sweep behavior without its temp file.
3. **No-weakening check**: diff round1 → round2 and confirm nothing that passed round
   1 got weaker; classify every delta as finding-closure / justified / unjustified.
4. **QA honesty**: verify the new three-way arm accounting (run/stubbed/inherited) by
   sampling at least 5 arms including at least 2 from the NEW code paths.

## Output

`audit2/AUDIT2_REPORT.md`: verdict first (PASS / PASS-WITH-NITS / REQUEST_CHANGES /
BLOCK), findings ranked most severe first with file+line, concrete failure scenario,
minimal fix; then the four question answers. English, ASCII only. Remember: round 3 is
the LAST repair round available — a REQUEST_CHANGES here must carry a change list that
is complete and final.
