# LEAD_ADJUDICATION — lane 8, attempt 3: second exact `claude-opus-5` xhigh T0 read of the WP-P0-12 intake accepting half at `a871e429` (T0 repair round 1) — 2026-09-17 18:2x UTC+3

**Lane history:** attempt 1 (`9ef072a8`, 13:55-14:23) REQUEST_CHANGES on REQUIRED-1 → Lead repair `a871e429` (Gemini `P012_INTAKE_R1_GEMINI` PASS); attempt 2 (14:33) CAPPED at once; **attempt 3** launched 18:02 on the reopened Pro window: 18:02-18:20 (15:01:55-15:20:36Z), launcher exit 0, 131 turns, no 429; report `opus/OPUS_REPORT.md`, 443 lines.
**Verdict as returned:** `VERDICT: PASS-WITH-NITS` — **0 REQUIRED**; REQUIRED-1 CLOSED by the reviewer's own three mutants (a/b/c each RED with no collateral failures; §6a), four further mutants of the D-1/D-2/D-6 fences all caught (§6b), RED arm on the pre-slice bytes (§6c), 23 own failing inputs refused, the r1 dry run byte-identical and still refused at D-4, the format-only parent PROVEN, scope and safety VERIFIED, the owner's address in no output. NITs 1-9 + NIT-A.

## Lead reproduction
| Check | Result |
|---|---|
| Citations — exporter `:131`, `:640-644`, `:893`, `:1224-1227`, `:1626`, `:1661-1662`, `:1781`, `:1797-1800`, `:2125-2129`; adapter `:48`, `:512-513`, `:612`; adapter test `:132-135` | **EXACT** at `a871e429` |
| NIT-A reproduced (the adapter declares an exporter outcome it never checks) | `LEAD_REPRO_lane8_attempt3_NITA.txt`: the r2 gap report declares `export_tool_outcome_today.refusal_code = CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`; the exporter on the same draft packet refuses `CANDIDATE_EVIDENCE_KIND_MISMATCH` (default profile) / `CANDIDATE_COVERAGE_INVALID` (real profile; the draft coverage carries `witness_reasons`, `witness_rule`) — **CONFIRMED**; declared-but-unchecked family (two producers, nothing compares them; the adapter test compares a literal to a literal) |
| NIT-6 (window start side unruled) | read against the design: D-6 (i) admits the payment stamped ≤ 1 s past `end` because it settles the last interval; by the same settled-interval reading a payment stamped inside the first second of `start` settles the PREVIOUS interval and should be out — today it is in by stamp. r2 (start 07:00Z, first payment 08:00Z) unaffected; r1 unaffected | **owner one-liner `D6-START A|B`** — A = keep "by stamp" (a payment at start+≤1 s belongs to the window) / B = settled-interval semantics on both sides (exclude it; mirror of the end rule). **Recommended: B** |

## NITs — disposition (carried; pin `a871e429` NOT moved before the Sol read)
| # | Finding | Disposition |
|---|---|---|
| NIT-1 (c) | unknown-kind refusal message names only `SYNTHETIC_FIXTURE` under the real profile | follow-up slice (message names the caller's profile + known profiles) |
| NIT-2 (c) | half-open tolerance band `[end, end+1 s)` undocumented (+1.000 s refused) | follow-up slice (docstring + `effective_interval` note) |
| NIT-3 (c) | `production_mode` reason text, `report_kind`, `inputs.synthetic_schedule_id` are synthetic-era labels on a real run | follow-up slice |
| NIT-4 (c) | adapter D-1 gloss + stale `UNRESOLVED:D-n` labels in the draft packet | follow-up slice (one sweep) |
| NIT-5 (c) | the D-4 `"derived"` substring blacklist is cosmetic (a back-derived price behind a well-formed locator is accepted — the declared limit) | follow-up slice (describe as cosmetic or drop; the O-1 slice makes D-4 real) |
| NIT-6 (c) | window START side unruled | **owner `D6-START A|B`** |
| NIT-7 | `binding_notes.settlement_rate_source/time_source` emit `SYNTHETIC_BINDING_ONLY` inside the real candidate; untested on the real path | follow-up slice (+ test) |
| NIT-8 | CLI `--help` still says "SYNTHETIC_ONLY" above `--evidence-kind` | follow-up slice |
| NIT-9 | Bridge payload values are never compared with the captured venue row (only the timestamp is flagged) | follow-up slice: add the value-agreement note or state the non-comparison in `evidence_limitations` |
| NIT-A | adapter's declared exporter outcome is false (pre-existing at `004a0711`); reproduced | follow-up slice: the adapter computes the outcome by calling the exporter (or the test compares to the exporter's actual refusal) — the pattern exists ten lines below in the same test |

## Standing
The accepting half `a871e429` now carries: exact-Opus PASS-WITH-NITS (second read), Gemini PASS (delta) + the slice-4 Gemini PASS-WITH-NITS on `9ef072a8`, the Lead's reproductions. Roster still needs exact Sol (Sat 2026-09-19) before anything is accepted; the Lead built it and cannot accept. One follow-up slice after Sol: NITs 1-5, 7-9, A + the O-1 oracle fill when the owner says `build`; `D6-START` per the owner's letter.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
