# KICKOFF — B3 repair round 5 (DOCUMENTATION ONLY)

Continuing under owner standing authority (auto-continue on narrow doc/QA survivors).
Audit 4 CLOSED the code (finding 1) and left exactly one REQUIRED survivor: finding 2,
a D026 evidence-recording defect in `SELF_QA.md`. This round fixes ONLY that file.
Write the deliverable into `round5/`. ASCII only. English only.

## Absolute code-freeze constraint (verify before you finish)

`RP1-B3.sh`, `RPD-VERIFY.sh`, `DESIGN_NOTES.md` in `round5/` MUST be byte-identical
copies of the `round4/` versions. Their SHA-256 must remain:

- `RP1-B3.sh` = `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc`
- `RPD-VERIFY.sh` = `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c`
- `DESIGN_NOTES.md` = byte-identical to `round4/DESIGN_NOTES.md`

Copy them straight over; do not edit them. If you find a code bug, do NOT fix it here —
STOP and report it (a code change would re-open the code audit). This round is closed
to code by construction.

## Inputs (read these, nothing else)

- This file; `audit4/AUDIT4_REPORT.md` (findings 1 and 2 + nit 2); `round4/SELF_QA.md`
  (the file to repair); `round4/RP1-B3.sh` and `round4/RPD-VERIFY.sh` (the code the QA
  describes — read to record its exact commands, do not modify).

## The only permitted change — rewrite `round5/SELF_QA.md`

For EVERY closure test in the QA (audit 4 flagged items 1, 4, 5, 6 specifically, but
sweep them all), replace every parameterized recipe with the LITERAL exact executable
command that produced the recorded output:

1. **No placeholders in any command block**: no `<FIX>`, `<CASE>`, `<PRE>/<SRC>/<FILE>`,
   `<FN>`, `<FX>`, `STUB_CASE=<CASE>`. Each RED and each GREEN test shows the actual
   command string as run (concrete paths may be normalized to a clearly-declared token
   like `<QA>` for the scratch root ONLY, as the auditor itself did — but the command
   structure, filenames, env vars and STUB_CASE values must be literal).
2. **No hidden state dependence**: audit 4 item-1 flagged that the cwd RED command
   reuses a `$QA/arm.sh` that a later GREEN step overwrote. Make every test
   self-contained: each command block rebuilds exactly the arm/fixture it needs, so
   running the recorded commands top-to-bottom reproduces every stated output. If two
   tests need different `arm.sh` contents, write both constructions out in full.
3. **Item 4**: record the three concrete commands (NaN, Infinity, -Infinity), not one
   templated command plus a value table.
4. **Item 6**: record the concrete command for each STUB_CASE value used
   (`twoline`/`oneline2`/`wrapper`/`wrongpath`), not `STUB_CASE=<CASE>`.
5. **Nit 2**: narrow the disclosed mid-table read-error limitation wording to "a read
   error that populates no field after one or more complete records" (a partially
   populated record is already caught by the `truncated=1` arm and STOPs).
6. Fix the section-6.13/subcount arithmetic to the auditor's verified totals
   (43 A / 119 B / 3 C; RP1 21A/64B; RPD 22A/55B; 6.13 labelled 11) if any count is
   still off.
7. Keep the honest-limitation disclosures; do not delete any truthful caveat.
8. Correct `SELF_QA.md:409-411`'s claim so it accurately describes what is recorded
   (every command block IS the exact command executed) — and make that true.

## Deliverable

`round5/` containing exactly four files: `RP1-B3.sh`, `RPD-VERIFY.sh`,
`DESIGN_NOTES.md` (all three byte-identical to round 4), and the rewritten
`SELF_QA.md`. No hidden files. Print DONE plus the four SHA-256s so the Lead can
confirm the three code/doc files are unchanged and only `SELF_QA.md` moved.
