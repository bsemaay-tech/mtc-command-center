# LEAD_ADJUDICATION — lane 6 (optional): exact `claude-opus-5` xhigh T0 read of the WP-P0-21 S1 catalogue-only slice `7fecf204` — 2026-09-17 18:4x-19:1x UTC+3

**Lane:** `OPUS_QUEUE_20260916/P021S1/opus/run.ps1`, Claude PRO profile, launched by hand 18:22 UTC+3 after lane 8's second read; 18:22-18:42 (15:21:48-15:42:33Z), launcher exit 0, 153 turns, no 429; report `ATTEMPT1_REQUEST_CHANGES_7fecf204/OPUS_T0_REPORT.md`, 250 lines; its own mutants on scratch copies (ready-fence, 13 value mutations), both RED arms reproduced with a control arm, fidelity table of the four pins against the DECISIONS row and the S2 packet.
**Verdict as returned:** `VERDICT: REQUEST_CHANGES` — **2 REQUIRED**: REQUIRED-1 the pinned B-05 definition is not the ratified M-C (Lead-authored "mean absolute R-multiple" / "side/size class" instead of M-A signed return-fraction mean with count and std + M-B intent agreement at the same bar independent of P&L, each with its own tolerance; the R-multiple unit depends on the OPEN blocker B-04, not wired); REQUIRED-2 one `divergence_tolerance` where M-C makes B-06 two numbers. Five NITs. Also recorded: the counted Gemini review of `7fecf204` graded the definition EQUAL against its own quoted evidence — "two reviewers agreeing is not corroboration".

## Lead reproduction and repair
- Citations: `p021_readiness_rules.py:206-212`, `:274`, `:276`, `:191`, `:211`, `:275`, `:418`, `:414-416`, `:63-66`, `:62`, `:178-182`, `:244`, `:246`, `:336-338`, `:291-293`, `:172-184`, `:84-170`; `test_strategy_type_policy_set.py:21-57`, `:56`; `P021_GAP_TABLE_20260915.md:33`, `:58`; packet §4 rows — read against the `7fecf204` bytes and the CT13 packet; the definition mismatch is plain on the page (the reviewer's fidelity walk is correct on every point).
- Repaired as the disclosed builder → **`eada65ed`** (`P021_S1_20260915/REPAIR_R1_20260917/LEAD_VERIFICATION_P021_R1.md`): M-A/M-B verbatim, M-C composed of them, two B-06 numbers, self-check honesty (N-1), provenance pins (N-2), the fence extended; four mutants RED (46-47 failed), GREEN 59 / 108 subtests, self-check exit 0, Ruff 0 new, guard PASS; Gemini `P021_R1_GEMINI` PASS (word-by-word zero substantive differences; the fence cannot pass for the wrong reason; artifact fixture untouched).

## NITs — disposition
| # | Finding | Disposition |
|---|---|---|
| N-1 | self-check hard-coded S2 line | **fixed in `eada65ed`** (values interpolated; the gap_ratio_max mutant now prints its own value) |
| N-2 | S2 provenance unpinned | **fixed in `eada65ed`** (three pins) |
| N-3 | the B-13 carrier field `dataset_manifest_hash` named nowhere | carried (record it as a DATA_QUALITY limit or name the deferral in the S3 packet) |
| N-4 | ready-fence guarantee narrower than the brief's phrasing | recorded here: `validate_catalog` refuses only when BOTH `missing_numbers` and `missing_rules` are empty; an open number is itself a refusal anchor — no change |
| N-5 | closed number appended by tuple rebinding | carried (fold into the literal with the next slice) |
| NOT VERIFIED 3 | the accepted policy-set artifact's hash lives only inside the test that asserts it | carried: record `p021pol-v1:4a807136…` in the P021 records outside the test |

## Standing
Lane 6 re-pinned to `eada65ed`; attempt 1 archived; the second exact-Opus read after lane 7 (Pro window permitting) or on the next reset; Sol (Sat) reads the pin that stands. Roster for acceptance: exact Opus + exact Sol + Gemini + Lead reproduction, then the owner; the Lead built both the slice and the repair and accepts nothing.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
