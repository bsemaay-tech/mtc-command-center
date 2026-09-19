# LEAD_ADJUDICATION — exact gpt-5.6-sol xhigh executing review of the WP-P0-20 derived measurement plan (2026-09-15 05:22-05:36Z)

**Verdict as returned: PASS-WITH-NITS — 0 REQUIRED, 2 NITs; Q1 NIT (with a launcher condition), Q2 SOUND, Q3 SOUND.** Report `sol/SOL_DERIVED_REPORT.md` (313 lines, sha256 `96273b2918697168b4e2d331ca0e6c3e127206c796f7c3dc1d5a6670e6648865` as stated by the reviewer; Lead re-hash below). Lane: Codex Plus `secondary`, `codex exec -m gpt-5.6-sol -c model_reasoning_effort=xhigh --ephemeral --sandbox workspace-write`, cwd scratch `C:/tmp/P020_DERIVED_SOL_SCRATCH_20260915`, `launch.exit` `exit=0 start=05:22:25Z end=05:36:04Z`; usage input 2 256 671 (cached 2 142 208) / output 35 576 (reasoning 13 490).

## What the reviewer executed (verified against its report; cwd = scratch, no repository cwd)
- Identities COMPUTED on the live files and the packet copies: eight pinned digests EQUAL; `PACKET_SHA256SUMS.txt` 31 rows `PACKET_MANIFEST_ALL_MATCH`; interpreter `Python 3.12.12`.
- Tool tests on the pinned interpreter: `16 passed in 0.97s`; targeted N6-8 regression `1 passed`; scratch copy with `verified_selection` neutralised (`return dict(recorded)` before the comparison): `FAILED … DID NOT RAISE SystemExit`; restored copy `1 passed`, digest back to `0bfd1891…` — RED/GREEN/RED shown.
- Original tool re-run into the scratch: `derived.json` sha256 `d84b043a…` BYTE_IDENTICAL; second run against the same path `exit 2 REFUSED: output already exists`, file unchanged (exclusive create).
- Harness `validate_derived_plan_harness.py` on the real derived plan: PLAN_VALID (identical output to the Lead's `VALIDATE_PLAN_HARNESS_S4.txt`); five mutation arms on scratch copies each refused with the driver's own message (duplicate family, foreign family, size 4096, tampered `dataset_sha256`, `execution_status` EXECUTED); Q1 probe with all four derivation digests zeroed → still PLAN_VALID (proves the driver reads `derivation.family_order` only).
- Independent conformance helper (scratch `review_checks.py`): `TRIALS_ALL_EQUAL=True`, 15 trials, `ADDED_KEYS=["derivation"]`, `CHANGED_KEYS=["trials"]`, selection independently re-derived, `INPUT_BINDING_ALL_EQUAL=True`.
- Did NOT run `--run` or `--oneshot`; no git; no network; no write into a read-only directory (the Lead checked: benchmark dir, package dir, tool dir and derived dir mtimes unchanged — see the terminal record).

## Findings and Lead disposition
| # | Finding | Severity | Lead disposition |
|---|---|---|---|
| Sol-D-1 | driver does not validate derivation provenance (`run_bounded_benchmark.py:185-194`, `:531-543`) | NIT | Accepted with the reviewer's condition: the launcher must ASSERT installed-plan sha256 == `d84b043a…` before `--validate-plan`, immediately before `--run`, and after the run (not merely record it). `p020_measurement_run.ps1` updated to assert at all three points and to hash driver, manifest, compatibility, records + sidecars and implementation sources before and after. Same class as Gemini G37-01. |
| Sol-D-2 | `DERIVATION_RULE.md:50-51` labels stale tool/test digests (`308aa0b8…`, `4adb69a0…`) as V1.6 pins; `:44` cites old line `:167` | NIT | Documentation residual in the tool dir; carried to the next tool change (does not touch the measurement path). |
| Q2 | temporary substitution; update the `SHA256SUMS_V16.txt` plan line for the interval and restore; record pre/post digests + UTC + exact command + non-existing output root | SOUND | Adopted verbatim in the launcher. |
| Q3 | rule transcription mechanical; no degree of freedom affects what is measured | SOUND | Agrees with the Lead and Gemini. |

## Lead re-hash
See the measurement terminal record for the `Get-FileHash` of `SOL_DERIVED_REPORT.md` at launch time (the launcher gate reads the VERDICT line from the file).

Recorded by Claude Opus 5 Lead (743291).
