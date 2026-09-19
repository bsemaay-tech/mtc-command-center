# LEAD_ADJUDICATION — lane 8 (optional): exact `claude-opus-5` xhigh T0 read of the WP-P0-12 intake accepting half `9ef072a8` — 2026-09-17 14:2x-14:5x UTC+3

**Lane:** `OPUS_QUEUE_20260916/P012INTAKE/opus/run.ps1`, Claude PRO profile, launched by hand 13:55 UTC+3 after the P031 third read; 13:55-14:23 (10:55:02-11:23:22Z); 210 turns → the launcher's turn cap (`error_max_turns`, exit 1) hit right after the reviewer wrote its complete 335-line report with the `VERDICT:` line (its last actions were tail checks of the report) — **counted** (lane 3 attempt 3 precedent: a deliberate verdict written before the cut).
**Verdict as returned:** `VERDICT: REQUEST_CHANGES` — **1 REQUIRED** (REQUIRED-1: the D-6 completion check names `coverage.fills_witness` as the position source on the accepting no-fills branch where the payments' own `szi` supplied the position; untested; three mutants survive) + 8 NITs. Sections 1-8 VERIFIED: explicit admission with no toggle, fences intact (both profiles), D-1..D-6 refuse 17/17 of the reviewer's own failing inputs, the 1-s tolerance reproduced (+0.999 accepted / +1.000 refused), the r1 dry run byte-identical to the Lead's four digests (refused at D-4 as recorded), the format-only parent AST-identical, scope and safety clean, the two changed adapter assertions a correction in the right direction.

## Lead reproduction and repair
Reproduced (`S4_ACCEPTING_HALF/LEAD_REPRO_lane8_REQUIRED1.txt`) and repaired as the disclosed builder → **`a871e429`** (see `S4_ACCEPTING_HALF/REPAIR_R1_20260917/LEAD_VERIFICATION_P012_INTAKE_R1.md`: RED = the reviewer's three mutants each fail exactly the two new tests; GREEN 232; full suite 1669; Gemini delta `P012_INTAKE_R1_GEMINI`). Citations of REQUIRED-1 (`export_mtc_funding.py:1222-1232`, `:1259-1264`, `:178-183`) EXACT at the `9ef072a8` blob. NITs 1-8 carried to one follow-up slice after the Sol read (NIT-6 also needs an owner sentence on the payment-stamp window before the next capture is commissioned — r2's [07:00Z, 11:00Z) window ends flat, so it is unaffected).

## Standing
Lane 8 re-pinned to `a871e429`; attempt 1 archived; attempt 2 CAPPED at once (Pro 429, resets 18:00 UTC+3) → relaunch on the 18:01 alarm; Sol (Sat 2026-09-19) generates from the pin that stands. The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
