# LEAD_REPRODUCTION_V14 - WP-P0-20 preselection procedure V1.4 (independent Lead reproduction, T0 round 4 roster member)

Performed by Claude Opus 5 Lead (desktop session `tradingview-lab-clean-10`, id 2c48d1), 2026-09-14 05:0xZ, in the scratch copy C:/tmp/P020_PRESELECT_LEAD_REPRO_V14_20260913/ (copied from C:/tmp/P020_PRESELECT_20260913/ by the previous Lead at 03:20Z after lane P20R5 finished, exit 0, 03:04:06Z-03:20:20Z). The lane directory was not written. No Git command other than `git rev-parse HEAD` (with command-local `GIT_CONFIG_*` safe.directory, no config written); no canonical-root write; no calibration/eligibility execution (refusal paths only); no agy.exe running.

| Step | Command | Observed | Status |
|---|---|---|---|
| 0 | git -C C:/P020_IMPL_20260912 rev-parse HEAD | b9b72f858dc830a9389517f79da5ea3c1fa6122c | EQUAL to pin |
| S | SHA256SUMS.txt checked against the repro copy (10 entries) | 10/10 OK | EQUAL |
| S2 | lane copy vs repro copy (FROZEN, preselect_profile.py, tests, PREREG, RUNBOOK, REPORT_R5, SHA256SUMS) | 7/7 SAME | EQUAL |
| 1 | pinned venv python -m pytest tests -q -p no:cacheprovider | 90 passed in 4.18s (84 in V1.3; +6 for T1-T3) | EQUAL to REPORT_R5 |
| 2 | --freeze twice in the scratch copy | sha256 f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff both runs; lane artifact digest identical | deterministic, EQUAL |
| 2b | LIMITATION line | SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A | unchanged since V1.1 |
| 4/5 | --oneshot without token | PRESELECT_REFUSED_NO_T0_REVIEW, exit 2 | refusal works |
| 4/5 | --oneshot with the dead V1.3 token 2e67f3f4... | PRESELECT_REFUSED_T0_TOKEN_MISMATCH, exit 2 | old token dead |
| 4/5 | --freeze with a token | argparse usage error "--freeze never takes a T0 authorization token", exit 2 | usage refusal works |
| O | search for CALIBRATION*/ELIGIBILITY* outputs after the refusals | none created | no shot spent |

Structural checks against the round-3 Sol findings T1-T4 (grep on preselect_profile.py, repro copy = lane bytes):
- T1: `require_t0_authorization` (:786) does one `read_bytes()` (:799), hashes that buffer (:800), compares the token, and returns `json.loads(raw), digest` (:809); `cmd_oneshot` (:1062) receives `(frozen, accepted_digest)` and `_run_oneshot` (:1072-1078) uses `accepted_digest` as `frozen_sha256` — no second open/hash of the frozen file on the execution path.
- T2: `load_plan()` is called once, inside `build_freeze` (:616, freeze path only); `verify_frozen_identity` (:456) returns the verified plan object which is passed into `_run_oneshot` (:1063-1066); the static source test at tests/test_preselect.py:1231 forbids `read_text`/`open(`/`load_plan(` inside `_run_oneshot`.
- T3: `ReservedOutputs.commit` (:557-569) writes+flushes both payloads with both handles open, aborts BOTH on any exception (`abort` :572-586 seeks/truncates/writes ABORTED/flushes every still-held handle), closes only in `finally`. Tests :1301/:1309/:1317 cover first-write, second-write and flush failures.
- T4: documentation split present: PRESELECT_RUNBOOK.md:170-172 (phase table: before any reservation / partial reservation failure / post-both-reservations transaction failure) and PRESELECTION_PREREG_V1.md:46 (T4 row).

NOT VERIFIED by this reproduction: correctness on real datasets (not executed); that the gate is clause-identical to run_bounded_benchmark._execute_trial on every input (exact T0 reviewers); Windows shared-write NIT from GK20B (not re-tested); reviewer verdicts for round 4 (pending: Grok pre-screen, Gemini 3.7, Sol on Codex Plus; exact Opus on Claude Pro only if owner D4 = YES).

Lead reproduction result: REPRODUCED. One roster member only; authorizes no execution. V1.4 token f839c960... stays unused.
