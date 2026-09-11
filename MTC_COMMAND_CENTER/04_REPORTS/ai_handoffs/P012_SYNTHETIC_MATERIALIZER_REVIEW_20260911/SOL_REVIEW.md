PASS — all five prior findings are closed on candidate `c5d9e4144449c09fffb607d09650329402d54bec`.

Key personal evidence:

- Exact-old RED: `23 failed, 3 controls passed`.
- Candidate GREEN: `26 passed`.
- Full focused module: `161 passed, 1 pre-existing skip`.
- Mandatory documented subprocess CLI: passed.
- Both verification scripts: exit 0.
- Final source hashes match; Git worktree remains clean.
- Full Bridge suite was reused from Lead evidence, not rerun.

Full report: [REPORT.md](C:/P012_MATERIALIZER_QA_97489_20260911/review2/sol/REPORT.md)
---
Lead-preserved exact detailed report extracted from the final REPORT.md diff in the reviewer execution log; output-last-message replaced its scratch file. Full raw log is retained in the delivery bundle.

# PASS

Fresh independent T0 delta re-review of D1 candidate
`c5d9e4144449c09fffb607d09650329402d54bec` against fixed point
`97489fde2c3e66e2cafc911553b1504f8da8b6a5`.

Reviewer/model/effort: **Sol / xhigh**. I read no current peer verdicts and used
no agents or alternate routes. This was limited to the corrective delta, its
changed functions/callers, the five prior findings, and the one factual docs
clarification. It was not a whole-package re-audit.

## Standards

No actionable delta-only standards finding. The strict JSON behavior is shared
by the two affected decoding paths rather than duplicated; the new validation
guards fail closed before publication; and `git diff --check` exited 0. The
contract sentence at `docs/26_FULL_RECONCILIATION_CONTRACT.md:642-644` accurately
states the exact supplied-symbol interval inventory already enforced by the
implementation. The previously optional unused diagnostic-field cleanup was
intentionally unchanged and is not an acceptance blocker.

## Spec — five closure verdicts

All five prior findings are personally **GREEN** on this candidate.

| ID | Current closure | Personal exact-old RED | Personal candidate GREEN |
|---|---|---|---|
| A — repository/MTC containment | `tools/export_mtc_funding.py:1212-1267` finds the owning repository from directory or file `.git` metadata, rejects any staging path under another Git checkout/worktree, and rejects case-insensitive `MTC_COMMAND_CENTER` ancestry before writes. | 5 behavioral failures: repository sibling MTC path, actual owned MTC production parent, foreign `.git` directory, foreign worktree-style `.git` file, and foreign MTC tree. The external non-repository control passed. | All 6 containment cases passed, including the external control. `verify_round2.py` independently returned `CANDIDATE_STAGING_UNSAFE` for the actual owned MTC parent, and that target remained absent. |
| B — duplicate retained row with NaN/+Inf/-Inf | `tools/export_mtc_funding.py:517-552` checks every retained payload scalar before duplicate folding at lines 837/853, so nonfinite values become `CANDIDATE_NONFINITE_VALUE` rather than an escaped serializer error. | 3 behavioral failures, one for each of NaN, +Inf, and -Inf; each escaped as `ValueError`. | All 3 passed; `verify_round2.py` also observed `CANDIDATE_NONFINITE_VALUE`. |
| C — duplicate JSON members at every depth | `tools/export_mtc_funding.py:435-453` installs a duplicate-rejecting `object_pairs_hook`; `_load_packet` uses it at lines 1159-1171. Python invokes the hook for every decoded object. | 4 behavioral failures: contradictory duplicate keys at packet, coverage, binding, and provenance depth were accepted and published. | All 4 passed with `CANDIDATE_PACKET_INVALID`, report-only refusal, and no candidate. |
| D — nonfinite source-witness JSON | `_verify_source_witness` uses strict decoding and translates decode/canonicalization failures at `tools/export_mtc_funding.py:650-685`. | 3 behavioral failures: NaN, Infinity, and -Infinity each escaped as `ValueError` and produced no deterministic refusal report. | All 3 passed with `CANDIDATE_BINDING_INVALID`, a refusal report, and no candidate. |
| E — RFC3339 offset ranges/calendar overflow | `_parse_instant` validates hour/minute ranges and translates timestamp arithmetic overflow at `tools/export_mtc_funding.py:276-325`. | 8 behavioral failures: 6 impossible offsets were accepted and 2 calendar-edge cases escaped as `OverflowError`. Both legal `+23:59`/`-23:59` exact-byte controls passed. | All 10 passed. The legal controls preserved candidate SHA-256 `6ca9299ec0312259a4e6d7812d251ea82bc0b90a193f264f6fdceddea1923e28`. |

The RED run loaded the byte-exact archived old exporter
`C:/tmp/P012_D1D2_20260911/path_guard_fix/before/export_mtc_funding.py`
(SHA-256 `df64caa3aac393349dd753676373bb3e864c012cd3bac259e91bea11b13ec0ea`)
through the private `sol/red_old_plugin.py`. Because that archive is outside its
original package, the plugin restored `ROOT` to the frozen candidate's
`IBKR_PAPER_BRIDGE` directory. All pytest temporary paths were under this
external `sol` folder, so ambient `C:/tmp/.git` could not fake containment
failures. Result: **23 failed, 3 controls passed, 136 deselected**, exit 1; no
collection, missing-helper, or schema errors. The identical current selection
was **26 passed, 136 deselected**, exit 0.

## Personal execution

All commands used
`C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -B`,
`PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`, and pytest
`-p no:cacheprovider`. Basetemps and outputs were exclusively below this `sol`
folder.

- `verify_candidate.py --output-dir sol/baseline`: exit 0. Its eight
  expectations passed, including exact bytes/order/digest domains, partial-write
  cleanup, and actual consumer nonadmission. It reported the current source
  unchanged.
- `verify_round2.py --output-dir sol/repairs`: exit 0, result `PASS`. It observed
  the five expected refusal codes and the legal-offset exact-byte control.
- Full focused source module: exit 0, **161 passed, 1 skipped** in 4.96 s. The
  sole skip is the pre-existing OS symlink-permission case; no new skip or waiver
  was introduced.
- Exact-old selected regression run: expected exit 1, **23 failed, 3 passed,
  136 deselected** in 1.90 s.
- Candidate selected regression run: exit 0, **26 passed, 136 deselected** in
  1.64 s.
- Mandatory real documented subprocess CLI, run explicitly by test name: exit
  0, **1 passed** in 1.24 s.
- `git diff --check 97489fde...c5d9e414`: exit 0.

Before and after execution, HEAD was exactly
`c5d9e4144449c09fffb607d09650329402d54bec`, `git status --porcelain` was empty,
and all three supplied SHA-256/Git-blob pairs matched `SOURCE_HASHES.json`:

- exporter: `d0686e8a...a1659a5` / `f12570e7...6ca854`
- focused tests: `e8b9c1f4...1a84927` / `c9e6c31d...e961b`
- contract docs: `5940075f...c5efe1` / `759e7a82...12fb`

## Reused unchanged evidence and limitations

I reused, without rerunning or re-auditing, the named first-round Opus/Sol
reports and `review/COMBINED_ROUND1.json`: exact candidate byte/numeric/time
inspection, quiescence RED/GREEN, partial-write behavior, current-production
consumer nonadmission, real Windows junction refusal, and the earlier relevant
mutants. I also treated Lead's exact-candidate full Bridge result
of **1628 passed, 1 skipped, 1 existing warning** as Lead evidence, not personal
execution; the full suite was not rerun because this delta introduced no new
concern requiring it.

This PASS is only for the full D1 candidate through the bounded corrective delta
and reused unchanged evidence. It does not accept WP-P0-12, production,
publication, merge, venue/economic facts, R34/R35/PR178, C10/funding, or redo R29
semantics. Source, Git, config, memory, and network remained read-only; scratch
writes were confined to `review2/sol`.

**Summary:** Standards 0 findings; Spec 0 remaining findings. Verdict: **PASS**.
