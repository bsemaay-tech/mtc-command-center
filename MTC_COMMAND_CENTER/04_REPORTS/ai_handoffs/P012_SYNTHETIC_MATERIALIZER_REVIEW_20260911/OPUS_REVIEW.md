REPORT.md is held open by the route harness, so the report goes to stdout only (as instructed).

---

# T0 DELTA RE-REVIEW — P0-12 D1 materializer (fresh, Opus 5 xhigh)

Candidate `c5d9e4144449c09fffb607d09650329402d54bec` (base `97489fde…`)

## VERDICT: **PASS**
Scope: the corrective delta over the D1 candidate, synthetic-only. Not a WP-P0-12, production, publication or merge acceptance.

## Identity / clean tree (checked before and after all work)
`HEAD c5d9e414…`, `git status --porcelain` empty both times. Worktree sha256 matched `SOURCE_HASHES.json` exactly for all three paths (`d0686e8a…` tool, `e8b9c1f4…` tests, `5940075f…` docs); git blobs `f12570e7 / c9e6c31d / 759e7a82` also matched. The owned MTC production parent still contains no `__P012_PREFLIGHT_ONLY_NEVER_CREATE`. All scratch stayed under `review2/opus`.

## Personally executed (Python 3.12.12, `-B`, `-p no:cacheprovider`, external basetemp)

| # | Run | Result |
|---|-----|--------|
| 1 | `lead_checks/verify_candidate.py --output-dir opus/baseline` | **EXIT 0**; staged sha `6ca9299e…`; `CANDIDATE_COVERAGE_INVALID` / `CANDIDATE_BINDING_INVALID` / `CANDIDATE_INVENTORY_MISMATCH`; partial write → `CANDIDATE_STAGING_FAILED` with no published or scratch artifact; consumer non-admission true |
| 2 | `lead/verify_round2.py --output-dir opus/repairs` | **EXIT 0**; five refusals `CANDIDATE_STAGING_UNSAFE`, `CANDIDATE_NONFINITE_VALUE`, `CANDIDATE_PACKET_INVALID`, `CANDIDATE_BINDING_INVALID`, `CANDIDATE_TIMESTAMP_INVALID`; legal-offset exact bytes = `6ca9299e…`, which I independently cross-checked equals the baseline candidate staged in run 1 |
| 3 | Focused module, `--basetemp opus/pytest` | **EXIT 0 — 161 passed / 1 skipped** (my own count). Named subset `-v`: 36 passed / 1 skipped / 125 deselected; all ten named new tests PASSED; `test_the_documented_command_line_works_as_written` (real subprocess) PASSED; the only skip is the pre-existing OS symlink-permission one. Grep confirms no ambient-Git-hiding autouse fixture and no extra documented-CLI skip |
| 4 | RED private mirror (old `df64caa3…` + byte-identical current tests, mirrored ROOT/`parents[2]` layout, external basetemp) | **24 failed / 137 passed / 1 skipped** |
| 4b | GREEN mirror (identical harness, candidate exporter `d0686e8a…`) | **1 failed / 160 passed / 1 skipped** |
| 5 | Own probes | `_parse_instant` edges; junction-style `.git` ancestry → `CANDIDATE_STAGING_UNSAFE`, staging not created |

RED breakdown: **23 failures are exactly the five classes** (6 invalid offsets, 2 calendar overflow, 3 duplicate-nonfinite, 4 duplicate-JSON depths, 3 nonfinite witness, 5 containment) with **3 controls green under old code** (legal ±23:59 ×2, external non-repository staging) — matching the builder's 23/3 without my relying on their log. The 24th failure is `test_current_production_loader_cannot_admit_the_candidate` failing on `ModuleNotFoundError: mtc_v2.core.instrument` because my private mirror has no `mtc_v2` package; it reproduces identically in the GREEN mirror and passes in the real tree, so it is an environment artifact and is not counted. I deliberately mirrored the MTC path into scratch rather than letting the old code run against the real tree — old `_prepare_staging` creates the directory, which would have been a write into frozen source.

## The five classes, closed
- **A — Containment** (`tools/export_mtc_funding.py:1212-1229`, `1252-1266`). OLD: CLI exit **0** and staged under `repository/MTC_COMMAND_CENTER`, a foreign `.git` directory, a `.git` worktree file, and an `MTC_COMMAND_CENTER` tree; `_prepare_staging` **did not raise** for the owned production funding parent. NEW: `CANDIDATE_STAGING_UNSAFE` before any write, staging absent; junction `.git` also refused; external non-repository staging still accepted (proven by a passing control on an external basetemp, so ambient `C:/tmp/.git` cannot have faked anything).
- **B — Duplicate retained nonfinite** (`:549-552`, ahead of `_fold_unique` at `:853`). OLD: `ValueError('Out of range float values are not JSON compliant: nan/inf/-inf')` escaped the pure builder. NEW: `CANDIDATE_NONFINITE_VALUE` at validation, i.e. before folding.
- **C — Duplicate JSON members** (`:439-453` via `_load_packet:1167`). OLD: CLI exit **0**, silent last-wins at packet, coverage, binding and provenance depth. NEW: `CANDIDATE_PACKET_INVALID` + report, no candidate file. `object_pairs_hook` applies at every nesting depth.
- **D — Nonfinite source witness** (`:448-453` `parse_constant`, `:665-682` canonicalization guard). OLD: `ValueError` escaped the CLI. NEW: `CANDIDATE_BINDING_INVALID` with a written report and no candidate file.
- **E — RFC3339 offsets** (`:300-317`). OLD: `+99:99`, `-99:99`, `±24:00`, `±00:60` were silently accepted and produced the *baseline* bytes `6ca9299e…` — a garbage offset folded onto a valid instant; calendar-edge offsets escaped `OverflowError`. NEW: `CANDIDATE_TIMESTAMP_INVALID` for both, and since the regex is fixed-width `[+-]\d{2}:\d{2}` the `>23 / >59` guard covers the entire admitted space. Valid time/numerics unchanged: legal `±23:59` still converts exactly to the identical baseline bytes, and my probe shows overflow refuses even for a 1-minute offset at year 0001/9999.

**Docs sentence is factually correct**: rows are enumerated by symbol only (`bridge/store/db.py:9860-9873`, no time predicate) and an extra out-of-interval retained row refuses with `CANDIDATE_INVENTORY_MISMATCH` (executed in run 1). No local-time filtering exists.

## Evidence reused (not re-executed)
`COMBINED_ROUND1.json` findings A–E, `opus_pro/REPORT.md` and `sol/REPORT.md` for unchanged behavior, Lead's full Bridge 1628 passed / 1 skip / 1 pre-existing warning on this exact source, and the earlier independent real-junction refusal.

## Limitations
Synthetic fixtures only — no venue, economic, completeness or billing claim. Full Bridge suite not rerun (no new concern required it). A true *symlink* `.git` could not be created under this account (same OS limit as the pre-existing skip) and was not tested; the junction and `.git`-worktree-file forms were. No R34/R35/PR178/C10/funding or R29 re-audit, no new venue or economic facts, no new skip or waiver. The opusD unused-diagnostic-field cleanup remains optional and untouched; not actionable.
