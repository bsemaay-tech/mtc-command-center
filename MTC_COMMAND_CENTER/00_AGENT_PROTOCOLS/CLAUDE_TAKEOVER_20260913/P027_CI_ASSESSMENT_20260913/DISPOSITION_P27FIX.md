# DISPOSITION_P27FIX — audit findings from `GROK_AUDIT_REPORT.md`

| # | severity | FIXED / REBUTTED | what changed (file:line) or the exact refuting source quote |
|---|---|---|---|
| 1 | CORRECTION | FIXED | `CI_ASSESSMENT.md:63` — 8/16 MET pin `START_HERE.md:33` → `:35` |
| 2 | CORRECTION | FIXED | `CI_ASSESSMENT.md:107` — remaining P013/P020 work `START_HERE.md:41-42`/`:33` → `:43`/`:35` |
| 3 | CORRECTION | FIXED | `CI_ASSESSMENT.md:79` — WP-P0-10 T0 pin `MASTER_WORK_PACKAGE...md:386` → `:387` |
| 4 | CORRECTION | FIXED | `CI_ASSESSMENT.md:67`, `:79`, `:91` — T0 quote pin `REVIEW_POLICY.md:19` → `:20` |
| 5 | CORRECTION | FIXED | `CI_CHECK_INVENTORY.md:87` — default packet path `check_review_report.py:13-15` → `:24` |
| 6 | CORRECTION | FIXED | `CI_ASSESSMENT.md:85` — pydantic/`mtc_contracts` imports `test_p021_eligibility.py:14-16` → `:10-12` |
| 7 | CORRECTION | FIXED | `CI_CHECK_INVENTORY.md:62` — quoted `:12-14` "the binding this checks for does not yet exist"; token `NOT_BOUND` at `:28` |
| 8 | CORRECTION | FIXED | `CI_ASSESSMENT.md:19` — `ci.yml` pin `:1-11` → `:1-12` so `contents: read` is inside the range |
| 9 | CORRECTION | FIXED | `CI_CHECK_INVENTORY.md:52` — failure annotation is a later step of job `bridge` (`ci.yml:19`, `:47-48`), not a downstream job |
| 10 | CORRECTION | FIXED | `CI_CHECK_INVENTORY.md:63` — file set `generate_index.py:16-18` git-tracked-or-trackable; `--check` byte-identical `:61-65` |
| 11 | CORRECTION | FIXED | `CI_ASSESSMENT.md:9` — quoted `REVIEW_POLICY.md:6-8` prospective activation; `SESSION_LOCK.md:17-19` recorded PR #167 condition |
| 12 | CORRECTION | FIXED | `CI_ASSESSMENT.md:40`, `:231`, `:330`; `CI_CHECK_INVENTORY.md:88` — dropped "would BLOCK every push"; cited local `repo_guard.ps1:63-66` and `ci.yml:27-29`; Actions HEAD name is `REPORT.md:87` NOT VERIFIED #15 |
| 13 | CORRECTION | FIXED | `CI_CHECK_INVENTORY.md:9` — Status qualifiers documented; Vercel NOT VERIFIED retained at `:92` |
| 14 | CORRECTION | FIXED | `CI_CHECK_INVENTORY.md:90` — inert `tests.yml:3-10` paths listed; not blanket `mtc_backtest/**` |
| 15 | NIT | FIXED | `CI_ASSESSMENT.md:231` — "Local-only by design" → `MTC_REPO_GUARD_USAGE.md:7-9` local preflight bytes |
| 16 | NIT | FIXED | `CI_CHECK_INVENTORY.md:54` — `ALERT_NEEDLES` `:9`; `ALLOWLIST` `:10` |
| 17 | NIT | FIXED | `CI_CHECK_INVENTORY.md:73` — `test_compat.py` pytest `:5`, pydantic `:6` |
| 18 | NIT | FIXED | `CI_ASSESSMENT.md:37` — "keep running" → "keeps running" |

Tally: 18 findings. 18 FIXED. 0 REBUTTED. 14 CORRECTION, 4 NIT, 0 BLOCKING.
