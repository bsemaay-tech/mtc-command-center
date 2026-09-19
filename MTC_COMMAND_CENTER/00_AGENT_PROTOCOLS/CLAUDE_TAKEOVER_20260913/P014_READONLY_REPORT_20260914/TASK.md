# TASK P14RO2 - WP-P0-14 small reproducible READ-ONLY report (owner decisions F YES 2026-09-13 + OD-20260914-P014-RO-1)

Owner authorization: "F YES" (2026-09-13) = the small reproducible read-only report that the P0-14 sequencing amendment allows (Minimum Explorer stays deferred behind core Bridge engineering). Scope fixed by the owner on 2026-09-14 (row `OD-20260914-P014-RO-1`, `C:/CT13/DECISIONS.md`): the report answers exactly two questions from read-only data:

- **Q-A.** Which candidate families currently exist in the P0-31 fixture lifecycle ledger, with their lifecycle state and the recorded rejection reasons (`failing_checks` / refusal codes where present)?
- **Q-B.** What does the P0-13 trial catalog contract currently contain (types, fields, refusal reasons, test coverage), and does any real catalog DATA exist?

No package work, no Explorer implementation, no product code, no new semantics. A report and a reproducer only.

## Inputs (read-only; copy what you need into cwd first)
- P0-31 ledger reader: `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py` (worktree HEAD `c76043b92c70c9f79a6d06630c0896ebe73e68a1`; do not run git there). Its CLI: `python p031_lifecycle_ledger.py report <ledger.sqlite>` opens the ledger in SQLite read-only mode and prints the status report. Read `render_status_report` and the `lifecycle_events` schema to know the fields (candidate id / family, state, `check_set_purpose`, `failing_checks`, `unresolved_lifecycle_contracts`, `fixture_only`, `accepted`).
- P0-31 fixture ledgers (Lead evidence, read-only, copy before reading): `C:/tmp/P031_LEAD_20260912/fixture_demo_r9/fixture-ledger.sqlite` (also `fixture-ledger.restored.sqlite`, `fixture-ledger.backup.sqlite`, `fixture-status-report.json`). These are FIXTURE data (`source_kind = 'FIXTURE'`, `fixture_only=true`, `accepted=false`): the report must say so in its first paragraph.
- P0-31 scope/status: `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/11_TRIAGE/P031_M1_SCOPE_AND_STATUS.md`.
- P0-13 catalog contract: `C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py` (worktree HEAD `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd`) and its tests `C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py`; P0-13 handoff `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md` (says the full catalog writer is excluded and nonaccepted). Report whether any catalog data file exists in that worktree (search for files the contract would write; if none, say NONE FOUND).
- Sequencing authority: `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/START_HERE.md` line 54 (quote it).

## Deliverables (all inside cwd `C:/tmp/P014_RO_20260914/`; nothing else)
1. `P014_READONLY_REPORT.md` — first paragraph: what this is (fixture data; nothing accepted; sequencing amendment preserved). Then **Q-A**: a table `| candidate / family | current lifecycle state | last transition | check_set_purpose | failing_checks / rejection reason | source (file:line or command) |` built from the ledger reader's output and/or read-only SQL (`sqlite3` with `?mode=ro`); event counts per state; the `unresolved_lifecycle_contracts` list the reader prints. Then **Q-B**: the contract's public types with their fields (one row per class: name, fields, purpose from the docstring), the refusal reasons enum, the number of tests in the test file, and the answer to "does any real catalog data exist?" with the search you ran. Every number traceable to a `absolute/path:line` or to a reproducible command over the copied files.
2. `reproduce_report.py` — standard library only (sqlite3, json, ast, pathlib); regenerates Q-A and Q-B tables deterministically from the copied inputs and prints them; run it once and paste its output verbatim into `REPORT.md`.
3. `REPORT.md` — what was built, the verbatim reproducer output, the interpreter used, a non-empty NOT VERIFIED (fixture data only; no live candidates; no catalog data; nothing accepted; no Explorer), and `SHA256SUMS.txt` (LF) covering the three deliverables and the copied inputs.
Finish by printing the produced files with byte counts.

## Boundaries (binding)
- Read-only everywhere except your working directory (cwd). Never write, delete or move a file outside cwd. Copy inputs into cwd before opening them with sqlite.
- Never run any Git command (`git status` included) in any repository: a review helper watches the shared repository store. Worktree HEADs are quoted above; do not verify them with git.
- No network, no package installs, no host contact, no credential, no deployment, no message sent, no schedule installed, no trading. Nothing you write is a decision, acceptance or authorization; write "owner decision" items as questions with a recommended answer.
- Cite every factual claim as `absolute/path:line` and quote the line; a claim you cannot cite goes into a non-empty NOT VERIFIED section. Never invent a citation. Read the cited line before writing the citation.
- Recorded owner routing: this lane runs on the Codex Pro Spark bucket (`gpt-5.3-codex-spark`); do not delegate, spawn agents, or call other providers.
