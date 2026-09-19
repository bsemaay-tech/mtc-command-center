# LEAD_ADJUDICATION - P030_R2_GEMINI (gemini-3.8-flash-high DETECTION/delta review of the WP-P0-30 NIT-slice repair round 2, d426e79f -> b4df1413) - Sat 2026-09-19 09:49-09:54 UTC+3

**Envelope:** `status=SUCCESS`, conversation `bab62220-a851-4329-9176-cdf1f5bfd80f`, 298 s, 1 turn, usage input 921,468 / output 44,668 / thinking 26,365 (cache read 6.5 M); launcher `exit=0 actual_exit=0`; the `GEMINI_READ_ONLY_OK` sentinel closes the response. Report extracted to `REPORT_RESPONSE_UTF8.md` (22,626 chars) verbatim from the envelope.

**Native-read audit** (`NATIVE_READ_AUDIT_attempt1.json`, from the CLI transcript store against the packet `P030_R2_20260919`, 40 files + SHA256SUMS): **74 native reads over 41 unique files, 0 outside the packet, 0 displayed-content mismatches, 0 failures.** Every REQUIRED read of the prompt is present: the complete diff (3 windows), commit, blob OIDs, all four subject files at the named ranges, the slice-read adjudication, the attempt-4 Opus report (F-1..F-5 section), the R2 verification record complete, and all 29 `LEAD_*.txt` (first lines + tails; the four long adapter logs partially, as allowed).

**Verdict as written:** **PASS** - F-1 CLOSED, F-2 CLOSED, F-3 CLOSED, F-4 CLOSED, F-5 CLOSED; `derived_fence_sound_on_pinned_312: true`; `walk_guard_mutant_survives_anywhere: false`; findings: none (0 REQUIRED, 0 NIT).

**Lead checks on the report (grep-verified against the packet bytes):**
- Its trace of `nesting_arms()` on the pinned 3.12 reproduces the Lead numbers exactly: first depth 996 (= recursion limit minus the four search frames) + 64 = walk 1060; parser 2998 + 64 = 3062; and it explains the in-arm values (1049 / 3044) by the runner frame delta - consistent with `LEAD_REPRO_R2_nesting_arms_py312.txt` and the RED files.
- Its frame counts for the code under test (exporter 4, capture 3, manifest 5, config/receipt 4-5) match the call chains; one function name in the manifest chain (`_restore_isolated_prefix`) is an approximation - the real path goes through `_isolated_restore_inputs`/`_restore_manifest_snapshot` (adapter `:538-580`, a range the reviewer did not open). Documentary imprecision in the review, not a defect in the candidate; the arm's RED files show the manifest arm is reached.
- Adversarial section answers every probe the prompt set (monotonicity, hook interference, dict nesting via hooks, parser-below-walk interpreters -> honest skip-by-name, clamp, 0 skips on both interpreters) with reasoning that matches the bytes.
- Preservation: it confirms the adapter diff is semantic lines + tests only and the refusal codes/order/receipt fields unchanged (consistent with `DIFF_d426e79f_b4df1413.patch`).
- NOT VERIFIED is non-empty and honest (no execution; POSIX branch read only; no live pipelines).

**Disposition:** **COUNTED PASS** (evidence class SUPPLEMENTAL_UNEXECUTED). Roster for `b4df1413` so far: Gemini PASS (this) + Lead reproduction (nine mutants RED on both interpreters). Next: lane 3 attempt 5 = exact-Opus read of `b4df1413` (repair round 1 of the slice read's cap 3), then Sol on the same bytes tonight. The Lead never accepts its own code.

Recorded by Claude Fable 5.1 Lead (session 7, `18c1b8`) at 2026-09-19T06:57:07Z; machine stamps in `OPUS_QUEUE_20260916/QUEUE_LOG.txt`.
