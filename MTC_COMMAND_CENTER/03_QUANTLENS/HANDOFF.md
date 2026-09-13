# QuantLens handoff

## Current state — 2026-08-25

- No new research run or strategy implementation is authorized by WP-P0-05.
- The archived journals' newest repository-wide state says Wayfinder planning is complete; package
  implementation generally requires fresh G1 acceptance and exact owner `G1-IA`.
- Existing owner decisions D004–D015 remain indexed in root `DECISIONS.md`; read the linked full
  record only when one governs the scoped strategy/run.
- The replaced 2026-05-30 handoff explicitly marked its 28.7% OOS/top-performer table inflated and
  unreliable (single split, arithmetic rather than compounded returns, missing data, no multiple-
  testing correction, no minimum-trade filter). Its corrected cited reports found zero statistically
  distinguishable configurations; do not resurrect the old table or backlog as current evidence.
- Next task must name exact strategy, data bundle, symbol/timeframe, task class, run gates, output
  path, and promotion boundary before execution.

## [Claude lane C] 2026-09-06 — aggregate night report renamed (D4)

- Changed: `tools/night_runs/AGGREGATE_night_2026-06-02.json` (Markdown content, 40,534 B) renamed
  via `git mv` to `AGGREGATE_night_2026-06-02.md`; bytes unchanged (sha256 8aa9bd4a…0b354a).
  No duplicate `.md` existed (the 2026-06-03 aggregate is a different 20-iteration report).
- References to the old `.json` name remain unedited in `MIGRATION_LEDGER.json`, the WP_P0_01
  inventory CSVs, the WPL_P2 SHA256SUMS list, `lessons_archive/OVERNIGHT_LESSONS_2026-06-03.md`, and
  the archived session log; none is a code path.
- NEXT ACTION: none; update the ledger/inventory rows only if a future inventory refresh is authorized.
- WAITING FOR OWNER: Nothing.

## P0-22 reduced local research tracker — 2026-09-13

- Product candidate `1bdb7f8c958815b74b1635770294b39c6ced1425` adds fixture-only local
  `register`, `disclose`, and `status` commands under the frozen reduced contract. It is six local
  commits ahead of base `42f99571`; no push, PR, merge, P0-13 integration, or shared-schema change.
- Lead replay: Python 3.14 compile and 27 focused tests PASS; QuantLens discovery 83/83 PASS;
  pytest 167 tests plus 826 subtests PASS. Synthetic status remains `LOCAL_LOG_ONLY` and
  `ACCESS_COMPLETENESS_UNVERIFIED`; no `LIVE_CANDIDATE` or clean-window claim is produced.
- Exact independent reviews on the same candidate: `gpt-5.6-sol` xhigh PASS;
  `claude-opus-5` xhigh PASS-WITH-NITS; `gemini-3.7-flash-high` supplemental PASS. Three allowed
  T0 repair rounds were consumed; detailed evidence and the repeatable demo are under
  `C:\tmp\P022_LEAD_20260912`.
- Limits remain: local SQLite history is mutable, reader coverage and independent clock/access
  evidence are incomplete, historical unlogged reads cannot be reconstructed, family identity is
  not canonical, and full-window binding/admission/promotion/live eligibility are unresolved.
- NEXT ACTION: integrate this local commit only through the normal PR/CI path when separately
  authorized; upgrade to full P0-22 only after accepted P0-13 and the remaining assurance work.
- WAITING FOR OWNER: Nothing.
