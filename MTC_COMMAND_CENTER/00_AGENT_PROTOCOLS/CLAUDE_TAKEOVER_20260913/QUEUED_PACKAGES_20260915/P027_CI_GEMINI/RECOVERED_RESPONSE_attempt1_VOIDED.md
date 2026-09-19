# T2 Independent Corroborating Review (SUPPLEMENTAL_UNEXECUTED)
**Package:** WP-P0-27 (OPS-C, repo-root CI home)  
**Reviewer:** Gemini (gemini-3.8-flash-high, read-only corroborator)  
**Date:** 2026-09-15  
**Objects under review:**
1. PR #193 workflow diff: `.github/workflows/research-gates.yml` (`fcac0ac6` → `a3325836`)
2. Acceptance packet: `P027_ACCEPTANCE_PACKET_20260915.md`

---

## (a) Task Part A — PR #193 Workflow Diff

| Item | Status | Packet-relative Citations | Corroboration Summary |
|---|---|---|---|
| **A1** | **CORROBORATED** | [`subject/DIFF_fcac0ac6_a3325836_research-gates.diff:10-101`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L10-L101)<br>[`subject/research-gates_a3325836.yml:13-35, 99-176`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L13-L35)<br>[`subject/research-gates_fcac0ac6_BASE.yml:1-93`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_fcac0ac6_BASE.yml#L1-L93) | Diff and after-file confirm exactly two jobs added: `p030-checkers` on `windows-2025` and `contracts-and-lint` on `ubuntu-24.04`, plus a header comment explaining WP-P0-27 additions. Pre-existing `checkers` job, `on:` triggers (`pull_request`/`push` to `master`), `permissions: contents: read`, and `concurrency` block are byte-identical to base. A workflow file cannot edit a repository ruleset; neither job modifies ruleset 21444962. New check display names (`P0-30 checkers (Python 3.12, Windows)` and `Contracts tests and Ruff (Python 3.12)`) do not collide with required contexts `Bridge suite (Python 3.12)` or `pine-alert-guard`. |
| **A2** | **CORROBORATED** | [`subject/DIFF_fcac0ac6_a3325836_research-gates.diff:29-101`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L29-L101)<br>[`sources/ci_fcac0ac6.yml:26-39`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/ci_fcac0ac6.yml#L26-L39)<br>[`sources/PLAN_WP_P0_27_block_lines590-602.md:5, 14`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PLAN_WP_P0_27_block_lines590-602.md#L5-L14)<br>[`sources/P027_CI_POLICY_2026-08-25.md:27-38`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_POLICY_2026-08-25.md#L27-L38) | No `secrets.*` references; no `schedule:` trigger; no self-hosted runners; no network/venue contact beyond GitHub Actions runners, actions setup, and PyPI wheels. `persist-credentials: false` is explicitly set on all checkouts (base and new). Job timeouts present (`p030-checkers`: 15 min; `contracts-and-lint`: 10 min). Pinning conventions: Bridge dependencies use `--require-hashes -r IBKR_PAPER_BRIDGE/requirements.lock` (identical to `ci.yml`); `actions/*` pinned by major tag (`@v4`, `@v5`, identical to `ci.yml`). `ruff==0.16.4` is pinned by version without `--require-hashes`; claim that this matches `MTC_COMMAND_CENTER/contracts/constraints.txt` is **NOT VERIFIED** (external file). Lack of hash verification on Ruff is graded NIT-WD-01. |
| **A3** | **CORROBORATED** | [`sources/research_gates_run_34961383292_RED_checkout.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json#L1)<br>[`sources/research_gates_run_34963602576.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json#L1)<br>[`subject/COMMITS_55ab90b8_a3325836.txt:1-13`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L1-L13)<br>[`subject/DIFF_fcac0ac6_a3325836_research-gates.diff:39-45`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L39-L45) | Run 34961383292 on commit `55ab90b8` failed in job `P0-30 checkers (Python 3.12, Windows)` at step 2 (`Check out repository`, duration 18s). Step 2 of `p030-checkers` in commit `a3325836` was preceded by `git config --system core.longpaths true`, which succeeded in run 34963602576 (9s), enabling checkout (18s) and subsequent steps to pass. Run 34963602576 completed SUCCESS across all 3 jobs. The intermediate commit-to-commit diff `55ab90b8` → `a3325836` is not directly isolated in the packet (described in commit text/evidence). Using `--system` rather than `--global` on ephemeral hosted runners is harmless (NIT-WD-02). |
| **A4** | **CORROBORATED** | [`subject/COMMITS_55ab90b8_a3325836.txt:29-33`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L29-L33)<br>[`sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md:14`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md#L14)<br>[`sources/PLAN_WP_P0_27_block_lines590-602.md:5`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PLAN_WP_P0_27_block_lines590-602.md#L5)<br>[`subject/P027_ACCEPTANCE_PACKET_20260915.md:23`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L23) | Restricting Ruff lint to clean surfaces (`tools/opsa`, `contracts`) avoids starting the informational job red, aligning with progressive activation. The packet does not overclaim R2: row R2 explicitly states `Bridge suite ✔; lint = compileall only on master; Ruff step WIRED in PR #193 (open)` and day-one scope is `yes (lint at the compileall level; Ruff = backlog until PR #193's T1)`. Accurate and fair. |
| **A5** | **CORROBORATED** | [`sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md:1-18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md#L1-L18)<br>[`sources/research_gates_run_34961383292_RED_checkout.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json#L1)<br>[`sources/research_gates_run_34963602576.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json#L1)<br>[`sources/pr193_state_GREEN.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/pr193_state_GREEN.json#L1) | **Supported by JSONs:** run 34961383292 failure on `55ab90b8`; Windows job checkout failure; run 34963602576 success on `a3325836`; job timings (`p030-checkers` 40s, `contracts-and-lint` 27s, `checkers` 13s); PR #193 state `OPEN`, `mergeStateStatus: CLEAN`, `headRefOid: a3325836...`; concurrent success of `CI` run 34963602580 and `Pine Defang Guard` run 34963602573.<br>**Not in JSONs (unverified):** exact checkout stderr text ("Filename too long"); local pre-check numbers (contracts 50 passed; dirty finding counts 3, 21, 69); local worktree path. |

---

## (b) Task Part B — Acceptance Packet

| Item | Status | Packet-relative Citations | Corroboration Summary |
|---|---|---|---|
| **B1** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:11-18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L11-L18)<br>[`sources/GH_QUERIES_20260915_NIGHT.txt:3-12, 20-24`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L3-L12)<br>[`sources/PR192_state_RED.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_RED.json#L1)<br>[`sources/PR192_state_GREEN.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_GREEN.json#L1)<br>[`sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md:1-18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md#L1-L18) | **Clause (a) CORROBORATED:** `ci.yml` blob `3394d9ff…` at `origin/master` `fcac0ac6`; check context `Bridge suite (Python 3.12)`; run histogram exactly 61 total (60 success, 1 failure: run 32846169952 at `110305c0`, 2026-08-25T12:10:43Z).<br>**Clause (b) CORROBORATED:** Draft PR #192 red demo run 34946092493 FAILURE at `Run Bridge test suite`; green run 34946405229 SUCCESS; PR closed unmerged (`mergedAt: null`). E-mail confirmed by owner chat ("yes") plus forwarded delivery channel artifact (Gmail id `1a0a4d879a3c386d`, `notifications@github.com`, run 34961383292).<br>**Clause (c) CORROBORATED:** Ruleset 21444962 `enforcement: active`, 2 required checks (`Bridge suite (Python 3.12)`, `pine-alert-guard`), strict policy `true`, 0 bypass actors; PR #192 `mergeStateStatus: BLOCKED` when red, `CLEAN` when green.<br>**Clause (d) CORROBORATED:** Holds in documentation; external CT13 tree grep execution marked NOT VERIFIED. |
| **B2** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:59-61`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L59-L61)<br>[`sources/P027_REQUIREMENT_RECONCILIATION_20260915.md:8-9`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L8-L9)<br>[`sources/GH_QUERIES_20260915_NIGHT.txt:6-12`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L6-L12)<br>[`sources/P027_CI_POLICY_2026-08-25.md:14-17, 115-121`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_POLICY_2026-08-25.md#L14-L17) | The morning reconciliation stated "across the last 200 CI runs there is no failure conclusion at all … until today no run had ever turned RED." Packet §5 item 1 correctly rectifies this from `GH_QUERIES_20260915_NIGHT.txt`: run 32846169952 at `110305c0` (2026-08-25 12:10:43Z) did fail on `master` and was repaired forward (`cef1d070`) at 15:04:24Z before ruleset creation (15:24:47Z). This does not weaken R5; rather, it provides historical precedent that `master` was repaired forward. R5 disposition remains satisfied in day-one scope. |
| **B3** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:63-77`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L63-L77) | Lineage citations (GLM-5.3 T1 audit and Codex xhigh T0 audit on 2026-08-25) are outside the packet (**NOT VERIFIED**). However, the packet §7 recommendation boundaries are strictly fenced: acceptance remains solely the owner's act; "accept day-one scope" explicitly excludes merging PR #193, excludes making `Research gates` required, and excludes changing the ruleset. |
| **B4** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:19-43`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L19-L43)<br>[`sources/P027_REQUIREMENT_RECONCILIATION_20260915.md:12-33, 58-60`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L12-L33) | Rows shifting state between the reconciliation and the packet are fully justified by the night evidence and PR #193 addendum:<br>- **R2:** reflects Ruff step wired in PR #193; day-one lint remains `compileall`.<br>- **R5:** incorporates historical red run 32846169952 and forwarded email channel artifact.<br>- **R10:** reflects 3 P0-30 checkers executing green in PR #193 (Windows).<br>- **R12:** reflects shared contracts tests executing green in PR #193.<br>- **R19:** marked HOLDS based on the evening sweep across CT13 `f1bbac40`. |
| **B5** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:17, 87`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L17) | The packet explicitly records the exact regex pattern list and tree identity (CT13 `f1bbac40`, `.md/.py/.yml/.json/.txt`, excluding `_AI_MEMORY/history/`), returning 0 continuous-protection claims. External command execution is **NOT VERIFIED**. |
| **B6** | **CORROBORATED** | [`sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md:32-37`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md#L32-L37)<br>[`sources/P027_REQUIREMENT_RECONCILIATION_20260915.md:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L18)<br>[`sources/RED_DEMO_EVIDENCE_20260915.md:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_DEMO_EVIDENCE_20260915.md#L18) | Predecessor applied NITs held in packet copies:<br>1. R5 relabelling in reconciliation line 18 explicitly carries the expanded label and caveat ("relabelled 10:25Z from 'IMPLEMENTED + VERIFIED'").<br>2. `RED_DEMO_EVIDENCE_20260915.md:18` explicitly includes "Notification half CLOSED on the owner's word; an immutable artifact (message headers / sanitized screenshot) is NOT on record".<br>3. P0-26 status note is outside this packet as noted. |

---

## (c) Findings

### Workflow Diff (`.github/workflows/research-gates.yml`)
- **NIT-WD-01** ([`subject/DIFF_fcac0ac6_a3325836_research-gates.diff:95`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L95) / [`subject/research-gates_a3325836.yml:170`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L170)):  
  **Severity: NIT**  
  `pip install ruff==0.16.4` pins Ruff by version string only without `--require-hashes` or hash constraints, diverging from the strict `--require-hashes` discipline used for Bridge dependencies. The assertion that `0.16.4` matches `MTC_COMMAND_CENTER/contracts/constraints.txt` is unverified from the packet. For an informational job, version pinning is acceptable, but hash-pinning or installing from a hash-locked constraints file is recommended before making the job required.
- **NIT-WD-02** ([`subject/DIFF_fcac0ac6_a3325836_research-gates.diff:41`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L41) / [`subject/research-gates_a3325836.yml:115`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L115)):  
  **Severity: NIT**  
  `git config --system core.longpaths true` applies at the system level. While `--global` is standard user scope, on ephemeral GitHub-hosted Windows runners `--system` succeeded and is harmless.
- **REQUIRED Findings on Workflow Diff:** None (0). Verdict: **PASS-WITH-NITS**.

### Acceptance Packet (`P027_ACCEPTANCE_PACKET_20260915.md`)
- **NIT-AP-01** ([`subject/P027_ACCEPTANCE_PACKET_20260915.md:52`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L52)):  
  **Severity: NIT**  
  Item E5 in §4 references `CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md` as the artifact path in repository triage, whereas within the evaluation packet it is staged as `sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md`. The underlying content, headers, and Gmail message id (`1a0a4d879a3c386d`) match.
- **REQUIRED Findings on Acceptance Packet:** None (0). Verdict: **PASS-WITH-NITS**.

---

## (d) Exact Read Coverage

All 22 required files plus the checksum manifest and 2 optional files were read completely using native `view_file` within the designated packet directory (`C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/`), adhering strictly to the <=150 lines per view rule:

1. [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/PACKET_SHA256SUMS.txt): lines 1–24 (complete)
2. [`subject/DIFF_fcac0ac6_a3325836_research-gates.diff`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff): lines 1–101 (complete)
3. [`subject/DIFF_STAT_fcac0ac6_a3325836.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_STAT_fcac0ac6_a3325836.txt): lines 1–3 (complete)
4. [`subject/research-gates_a3325836.yml`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml): lines 1–150; continuation lines 151–176 (complete)
5. [`subject/research-gates_fcac0ac6_BASE.yml`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_fcac0ac6_BASE.yml): lines 1–93 (complete)
6. [`subject/COMMITS_55ab90b8_a3325836.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt): lines 1–40 (complete)
7. [`subject/P027_ACCEPTANCE_PACKET_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md): lines 1–89 (complete)
8. [`sources/ci_fcac0ac6.yml`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/ci_fcac0ac6.yml): lines 1–56 (complete)
9. [`sources/P027_CI_POLICY_2026-08-25.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_POLICY_2026-08-25.md): lines 1–150; continuation lines 151–177 (complete)
10. [`sources/PLAN_WP_P0_27_block_lines590-602.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PLAN_WP_P0_27_block_lines590-602.md): lines 1–15 (complete)
11. [`sources/DECISIONS_rows_P027.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/DECISIONS_rows_P027.md): lines 1–6 (complete)
12. [`sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md): lines 1–18 (complete)
13. [`sources/pr193_state_GREEN.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/pr193_state_GREEN.json): lines 1–2 (complete)
14. [`sources/research_gates_run_34961383292_RED_checkout.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json): lines 1–2 (complete)
15. [`sources/research_gates_run_34963602576.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json): lines 1–2 (complete)
16. [`sources/GH_QUERIES_20260915_NIGHT.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt): lines 1–25 (complete)
17. [`sources/P027_REQUIREMENT_RECONCILIATION_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md): lines 1–60 (complete)
18. [`sources/RED_DEMO_EVIDENCE_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_DEMO_EVIDENCE_20260915.md): lines 1–21 (complete)
19. [`sources/PR192_state_RED.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_RED.json): lines 1–2 (complete)
20. [`sources/PR192_state_GREEN.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_GREEN.json): lines 1–2 (complete)
21. [`sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md): lines 1–59 (complete)
22. [`sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md): lines 1–43 (complete)
23. *(Optional)* [`sources/RED_RUN_34946092493_failed_log.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_RUN_34946092493_failed_log.txt): lines 1–56 (complete)
24. *(Optional)* [`sources/pine-defang-guard_fcac0ac6.yml`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/pine-defang-guard_fcac0ac6.yml): lines 1–21 (complete)

---

## (e) Nonempty NOT VERIFIED Scope

1. **Live GitHub State & Execution:** This reviewer operates under `SUPPLEMENTAL_UNEXECUTED` with no command execution or external network/GitHub API capability. All statements regarding GitHub state, ruleset 21444962 enforcement, check run statuses, and merge blockers are corroborated strictly from the static JSON and text evidence files provided in `sources/`.
2. **Intermediate Commit State (`55ab90b8`):** The packet provides the base-to-HEAD diff (`fcac0ac6` → `a3325836`). The intermediate commit `55ab90b8` is evaluated via commit text and JSON logs; the standalone intermediate commit diff was not provided.
3. **Constraints File Identity:** The assertion that `ruff==0.16.4` matches the version pinned in `MTC_COMMAND_CENTER/contracts/constraints.txt` cannot be confirmed, as that path resides outside the packet.
4. **Historical Review Lineage Documents (2026-08-25):** References to `GLM_AG_P027_REPORT.md` and Codex audit notes (`WAL_CAPTURE_FIX_2026-08-25/FIX_EVIDENCE.md`) reside outside the packet and cannot be inspected.
5. **R19 Tree Grep Execution:** The grep sweep command cited in packet §9 against CT13 tree `f1bbac40` was executed by the Lead; it cannot be re-executed by this reviewer.
6. **Raw Email Message for Demo Run 34946092493:** The failure email for the 08:18Z demo run remains owner-confirmed only; the physical forwarded email artifact provided (`CI_FAILURE_EMAIL_ARTIFACT_MASKED.md`) proves the delivery channel via PR #193 run 34961383292.
7. **`pine-alert-guard` Failure Demonstration:** The check is required by ruleset 21444962, but has never failed in the recorded CI runs; its failure handling belongs to WP-P0-23's evidence pack.

---

## (f) Fenced JSON Verdict

```json
{
  "part": "P027_CI_GEMINI",
  "verdict_workflow_diff": "PASS-WITH-NITS",
  "verdict_acceptance_packet": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "p027_dayone_gate_clauses": {
    "a": "CORROBORATED",
    "b": "CORROBORATED",
    "c": "CORROBORATED",
    "d": "CORROBORATED"
  },
  "findings": [
    {
      "id": "NIT-WD-01",
      "target": "workflow_diff",
      "severity": "NIT",
      "file_line": ".github/workflows/research-gates.yml:170",
      "description": "Ruff 0.16.4 is installed via version pin without --require-hashes, diverging from the strict hash-locking used for Bridge dependencies; claim of matching constraints.txt is unverified from packet."
    },
    {
      "id": "NIT-WD-02",
      "target": "workflow_diff",
      "severity": "NIT",
      "file_line": ".github/workflows/research-gates.yml:115",
      "description": "git config --system core.longpaths true uses system rather than user/global scope on the Windows runner; harmless on ephemeral hosted runners."
    },
    {
      "id": "NIT-AP-01",
      "target": "acceptance_packet",
      "severity": "NIT",
      "file_line": "P027_ACCEPTANCE_PACKET_20260915.md:52",
      "description": "Packet cites email artifact as CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md, while packet copy is named sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
