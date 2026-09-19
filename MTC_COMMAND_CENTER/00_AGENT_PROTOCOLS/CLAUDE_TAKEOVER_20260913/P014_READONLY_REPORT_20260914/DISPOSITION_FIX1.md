# DISPOSITION_FIX1

Lane P14FIX1G (SuperGrok). Input audit: `C:/tmp/CLAUDE_P0_RUN_20260913/laneGKP14_grok_audit/GROK_P14_REPORT.md`. Scope unchanged: exactly Q-A and Q-B; fixture data only; read-only; no product code. Nothing here is a decision, acceptance, or authorization.

| # | severity | disposition FIXED / REBUTTED (with evidence) / NOT APPLICABLE | what changed (file:line) |
| --- | --- | --- | --- |
| 1 | CORRECTION | FIXED | reproduce_report.py:30 escapes pipe characters in every table cell; P014_READONLY_REPORT.md:69 keeps Sha256 BitOr None=None escaped; REPORT.md:25 pastes live stdout including that escaped field |
| 2 | CORRECTION | FIXED | P014_READONLY_REPORT.md:85 quotes Sha256 BitOr None = None from trial_catalog.py:192 and the docstring 'absent by design for screening'; Q-B row fields at P014_READONLY_REPORT.md:69 |
| 3 | CORRECTION | FIXED | P014_READONLY_REPORT.md:5 cites json:16; P014_READONLY_REPORT.md:6 cites json:10; P014_READONLY_REPORT.md:7 cites json:82; P014_READONLY_REPORT.md:8 cites P031_M1_SCOPE_AND_STATUS.md:718; no longer json:2/:17 |
| 4 | CORRECTION | FIXED | reproduce_report.py:181 stores Assign.lineno; Q-B alias source is trial_catalog.py:238 (P014_READONLY_REPORT.md:74); no longer mod.body[0].lineno |
| 5 | CORRECTION | FIXED | reproduce_report.py:208 supplies whitespace-collapsed docstring text; TerminalTrialReceipt P014_READONLY_REPORT.md:82; LineageOriginReceipt P014_READONLY_REPORT.md:69 |
| 6 | CORRECTION | FIXED | P014_READONLY_REPORT.md:31 lists the 3-item snapshot; P014_READONLY_REPORT.md:37 lists the 7-item reader source; P014_READONLY_REPORT.md:52 quotes the CLI error; seven derived from p031_lifecycle_ledger.py:1259-1267 |
| 7 | CORRECTION | FIXED | reproduce_report.py:346 is the Q-A table cell; derivation reproduce_report.py:97 and the following check_set_purpose() call |
| 8 | CORRECTION | FIXED | REPORT.md:21 records the full pinned interpreter path |
| 9 | CORRECTION | FIXED | P014_READONLY_REPORT.md:21 cites the 1/1/1 event-count command; P014_READONLY_REPORT.md:89 states 29 = def test_*; P014_READONLY_REPORT.md:59 cites trial_catalog.py:39-63 |
| 10 | NIT | FIXED | P014_READONLY_REPORT.md, REPORT.md, DISPOSITION_FIX1.md, SHA256SUMS.txt, reproduce_report.py written UTF-8 no BOM with LF (Python write_bytes) |
| 11 | NIT | FIXED | reproduce_report.py:8 / reproduce_report.py:9: `collections.Counter` removed; imports are ast, json, sqlite3, pathlib only |
| 12 | NIT | FIXED | P014_READONLY_REPORT.md:89 states 29 = def test_* and collection 40; suite was not collected; reproduce_report.py:414 |
