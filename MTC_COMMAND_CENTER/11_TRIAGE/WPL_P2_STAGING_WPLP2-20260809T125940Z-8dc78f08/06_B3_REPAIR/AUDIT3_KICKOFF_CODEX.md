# AUDIT KICKOFF — round 3 closure audit (Codex, T0, final)

Same contract as the previous two audits. Round 3 was the final repair round and
implemented your complete-and-final list. Per that contract, the only admissible
REQUIRED findings now are: (a) an item of the final list not actually closed, or
(b) a regression the round-3 changes introduced. Anything else is a nit.

## Scope — read ONLY

- `audit2/AUDIT2_REPORT.md` (your final list), `ROUND3_KICKOFF.md`, `round3/` (under
  audit), `round2/` (the baseline), `../01_RUNKIT/RP0-LIB.sh` (context).

## Audit questions

1. For each final-list item 1–8: CLOSED / NOT CLOSED, with the round3 line or the
   concrete surviving failure scenario. Re-run your audit-2 refutation fixtures
   (PYTHONPATH json.py shadow, NaN manifest, unterminated mount record, two-line
   EACCES+ENOENT diagnostic, name-mapped 999:999 service owner) against round3 code
   and report actual rc/output.
2. Regression sweep over the round2→round3 diff only: anything audit 2 verified
   CLOSED that round 3 weakened or broke.
3. QA honesty: verify the corrected three-way counts on a sample; confirm D026
   command+RED/GREEN output present for the item 1–6 closure tests.

## Output

`audit3/AUDIT3_REPORT.md`: verdict first — PASS / PASS-WITH-NITS / BLOCK (a
REQUEST_CHANGES is no longer available; unresolved required findings mean BLOCK and
owner escalation) — findings ranked, then the three answers. English, ASCII only.
