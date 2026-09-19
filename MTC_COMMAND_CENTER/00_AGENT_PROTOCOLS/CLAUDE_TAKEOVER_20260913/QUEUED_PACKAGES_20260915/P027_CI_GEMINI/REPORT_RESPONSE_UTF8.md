# T2 Corroboration Review: WP-P0-27 (OPS-C, repo-root CI home)
**Reviewer:** Gemini (Supplemental Read-Only Corroborating Reviewer; `SUPPLEMENTAL_UNEXECUTED`)  
**Date:** 2026-09-15  
**Review Objects:**  
1. PR #193 workflow diff: [`.github/workflows/research-gates.yml`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml) (`fcac0ac6` → `a3325836`, OPEN and unmerged)  
2. Acceptance packet: [`P027_ACCEPTANCE_PACKET_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md) (documentary recommendation for day-one scope)

---

## (a) Part A Table: PR #193 Workflow Diff

| Item | Status | Citations & Corroboration Details |
|---|---|---|
| **A1** | **CORROBORATED** | [`subject/DIFF_fcac0ac6_a3325836_research-gates.diff:1-101`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L1-L101), [`subject/DIFF_STAT_fcac0ac6_a3325836.txt:1-3`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_STAT_fcac0ac6_a3325836.txt#L1-L3), [`subject/research-gates_fcac0ac6_BASE.yml:1-93`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_fcac0ac6_BASE.yml#L1-L93), [`subject/research-gates_a3325836.yml:1-176`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L1-L176). The diff adds exactly two jobs: `p030-checkers` on `windows-2025` (`:104-134`) and `contracts-and-lint` on `ubuntu-24.04` (`:142-175`), plus the header comment update (`:10-18`). The existing `checkers` job (`:37-98`), `on:` triggers (`:21-27`), `permissions: contents: read` (`:29-30`), and `concurrency:` block (`:32-34`) are byte-unchanged from BASE (`:16-92`). A workflow file cannot edit repository rulesets (which are configured via repository admin settings/API). Neither added job name (`P0-30 checkers (Python 3.12, Windows)`, `Contracts tests and Ruff (Python 3.12)`) collides with ruleset 21444962 required contexts (`Bridge suite (Python 3.12)` and `pine-alert-guard`; [`sources/GH_QUERIES_20260915_NIGHT.txt:4`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L4)). |
| **A2** | **CORROBORATED** | [`subject/research-gates_a3325836.yml:21-34,104-175`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L21-L34), [`sources/PLAN_WP_P0_27_block_lines590-602.md:5,14`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PLAN_WP_P0_27_block_lines590-602.md#L5). Zero `secrets.*` references exist; triggers are `pull_request` and `push` to `master` only (no `schedule:`); runners are GitHub-hosted (`windows-2025`, `ubuntu-24.04`); no external network contact beyond PyPI pip install and official Actions; `persist-credentials: false` is set on every checkout (`:48, 120, 153`); timeouts are explicit (`timeout-minutes: 15` on `p030-checkers`, `10` on `contracts-and-lint`). Compared to [`sources/ci_fcac0ac6.yml:27,32,38`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/ci_fcac0ac6.yml#L27): `actions/*` pin by major tag (`actions/checkout@v4`, `actions/setup-python@v5`), matching existing convention; the Bridge lock install uses `--require-hashes` (`:162-163`), byte-identical to `ci.yml:38-39`. Ruff pins `ruff==0.16.4` (`:170`) by version without hashes; the claim that this equals `MTC_COMMAND_CENTER/contracts/constraints.txt` cannot be verified directly (file is outside packet; **NOT VERIFIED**). Unhashed pip install in an informational gate is a minor convention softening graded as **NIT** (N-01), not a blocker. |
| **A3** | **CORROBORATED** | [`sources/research_gates_run_34961383292_RED_checkout.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json#L1), [`sources/research_gates_run_34963602576.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json#L1), [`subject/COMMITS_55ab90b8_a3325836.txt:7-10`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L7-L10). Run 34961383292 failed on headSha `55ab90b8` at job `P0-30 checkers (Python 3.12, Windows)` step 2 (`Check out repository`), while the other two jobs succeeded. In run 34963602576 (`a3325836`), step 2 `Enable long paths for the checkout` ran `git config --system core.longpaths true` before step 3 checkout, and all three jobs completed `success`. The intermediate commit diff (`55ab90b8` → `a3325836`) is not a standalone diff in the packet (only base→HEAD diff is provided); intermediate state is corroborated via commit text and run 34961383292 step metadata, but the isolated intermediate patch is **NOT directly verified**. `--system` scope succeeds on hosted Windows runners due to elevated privileges; graded as **NIT** (N-02). |
| **A4** | **CORROBORATED** | [`subject/COMMITS_55ab90b8_a3325836.txt:31-32`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L31-L32), [`subject/research-gates_a3325836.yml:61-66,172-175`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L61-L66), [`sources/P027_CI_POLICY_2026-08-25.md:92-104`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_POLICY_2026-08-25.md#L92-L104), [`subject/P027_ACCEPTANCE_PACKET_20260915.md:23`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L23). Progressive activation avoids introducing perpetually red checks. Scoping Ruff to currently clean surfaces (`MTC_COMMAND_CENTER/tools/opsa` and `MTC_COMMAND_CENTER/contracts`) adheres to this principle. Packet row R2 states: `| R2 | day-one job = Bridge suite + light lint | Bridge suite ✔; lint = compileall only on master; Ruff step WIRED in PR #193 (open) | yes (lint at the compileall level; Ruff = backlog until PR #193's T1) |`. This accurately acknowledges that `master` carries only `compileall`, while Ruff is wired in unmerged PR #193 and remains in the progressive backlog until PR #193 passes T1 review. No overclaim. |
| **A5** | **CORROBORATED** | [`sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md:1-18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md#L1-L18). Supported by packet JSONs: (1) Run 34961383292 failure on `55ab90b8` at checkout step; (2) Run 34963602576 success on `a3325836` with job start/end timestamps and durations (`p030-checkers` 40s, `contracts-and-lint` 27s, `checkers` 13s); (3) PR #193 state `OPEN`, `mergeStateStatus: CLEAN`, check rollup all SUCCESS ([`sources/pr193_state_GREEN.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/pr193_state_GREEN.json#L1)); (4) Associated run IDs (34963602580 for `CI`, 34963602573 for `Pine Defang Guard`). Claims NOT in GitHub JSONs: local worktree path `C:/tmp/P027_CI_20260915`, local test counts (50 contracts tests), pre-check finding counts (3 / 21 / 69), local pre-commit guard `LEAD_GUARD_CI_PR.txt` (**NOT VERIFIED**). |

---

## (b) Part B Table: Acceptance Packet (`P027_ACCEPTANCE_PACKET_20260915.md`)

| Item | Status | Citations & Corroboration Details |
|---|---|---|
| **B1** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:11-18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L11-L18):<br>• Clause (a) **CORROBORATED**: `ci.yml` blob `3394d9ff…` at `fcac0ac6`; run histogram shows 61 runs total, 60 success, 1 failure (`110305c0` on 2026-08-25T12:10:43Z; [`sources/GH_QUERIES_20260915_NIGHT.txt:7-12,21-22`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L7-L12)).<br>• Clause (b) **CORROBORATED**: Draft PR #192 run 34946092493 `FAILURE` on `Bridge suite (Python 3.12)` (`assert False`), run 34946405229 `SUCCESS` after probe removal ([`sources/RED_DEMO_EVIDENCE_20260915.md:8-11`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_DEMO_EVIDENCE_20260915.md#L8-L11), [`sources/RED_RUN_34946092493_failed_log.txt:40-42`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_RUN_34946092493_failed_log.txt#L40-L42)). PR closed unmerged (`mergedAt: null`; [`sources/GH_QUERIES_20260915_NIGHT.txt:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L18)). Notification: owner chat confirmation ("yes", ~08:32Z) + delivery channel artifact from PR #193 run 34961383292 (`notifications@github.com`, Gmail id `1a0a4d879a3c386d`; [`sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md:5-15`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md#L5-L15)).<br>• Clause (c) **CORROBORATED**: Ruleset 21444962 active, `strict_required_status_checks_policy: true`, contexts `Bridge suite (Python 3.12)` + `pine-alert-guard`, 0 bypass actors ([`sources/GH_QUERIES_20260915_NIGHT.txt:4`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L4)); PR #192 red state was `mergeStateStatus: BLOCKED` ([`sources/PR192_state_RED.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_RED.json#L1)), fixed state `CLEAN` ([`sources/PR192_state_GREEN.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_GREEN.json#L1)).<br>• Clause (d) **CORROBORATED**: Documented sweep over CT13 `f1bbac40` found 0 claims of continuous protection; execution of the sweep itself is **NOT VERIFIED**. |
| **B2** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:60`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L60), [`sources/P027_REQUIREMENT_RECONCILIATION_20260915.md:8-9`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L8-L9), [`sources/GH_QUERIES_20260915_NIGHT.txt:7-12`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L7-L12). The documents contradict each other: the morning reconciliation claimed "no failure conclusion at all ... never turned RED", whereas the night API query revealed run 32846169952 at `110305c0` (2026-08-25T12:10:43Z) failed. Packet §5 item 1 correctly rectifies this erratum against `GH_QUERIES_20260915_NIGHT.txt`. The correction does not invalidate or weaken any row disposition; for R5, it confirms that the "master never stays red; fix forward" discipline was exercised in a live incident on 2026-08-25 (repaired in 2 h 54 min by `cef1d070` before ruleset activation). |
| **B3** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:64-68,70-78`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L64-L68). The 2026-08-25 review records (`GLM_AG_P027_REPORT.md`, `WAL_CAPTURE_FIX_2026-08-25/FIX_EVIDENCE.md`) are outside the packet and **NOT VERIFIED**. Packet §7 explicitly keeps acceptance as the owner's sovereign decision ("Acceptance of WP-P0-27 is the owner's act on the Lead's recommendation", "This packet accepts nothing"), clearly defines outcomes for owner responses ("accept day-one scope", "not yet", "accept, and add the exact-flagship read first"), and explicitly excludes PR #193 from acceptance (PR #193 remains unmerged and requires separate T1 review before merge). |
| **B4** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:22-42`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L22-L42) vs [`sources/P027_REQUIREMENT_RECONCILIATION_20260915.md:14-33,58-60`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L14-L33). Exactly the expected 5 rows moved based on night evidence and PR #193:<br>• **R2**: Moved from PARTIAL to "Bridge suite ✔; lint = compileall only on master; Ruff step WIRED in PR #193 (open)" (day-one scope: yes, at compileall level).<br>• **R5**: Moved from "PROBE-VERIFIED (draft PR #192)" to include the forwarded email delivery channel artifact and the historical 2026-08-25 incident.<br>• **R10**: Moved from PARTIAL/dependent to include three P0-30 checkers wired in PR #193 (backlog).<br>• **R12**: Moved from MISSING to wired in PR #193 (backlog until T1).<br>• **R19**: Re-checked and confirmed holding via night sweep. |
| **B5** | **CORROBORATED** | [`subject/P027_ACCEPTANCE_PACKET_20260915.md:17,87`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L17). Packet §9 states the exact regex pattern list (`"continuous protection|continuously protect|continuous-protection|gates repository changes|protects master|protecting master|CI protects|guard protects"` + `OPS-C` × `built|running|protect|PROVEN|live` + 4 ops-checks × `PROVEN`) and exact tree identity (CT13 `f1bbac40`, excluding `_AI_MEMORY/history/`). Execution of the sweep command is **NOT VERIFIED** (external execution). |
| **B6** | **CORROBORATED** | [`sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md:33-37`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md#L33-L37). Predecessor NIT F-01 held at [`sources/P027_REQUIREMENT_RECONCILIATION_20260915.md:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L18) (R5 relabelled from "IMPLEMENTED + VERIFIED" to "IMPLEMENTED; RED path PROBE-VERIFIED..."). Predecessor NIT F-02 held at [`sources/RED_DEMO_EVIDENCE_20260915.md:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_DEMO_EVIDENCE_20260915.md#L18) ("Notification half CLOSED on the owner's word; an immutable artifact ... is NOT on record"). Predecessor NIT F-03 is outside this packet. |

---

## (c) Findings

### Object 1: PR #193 Workflow Diff (`.github/workflows/research-gates.yml`)
- **Verdict:** **PASS-WITH-NITS** (0 REQUIRED, 2 NITs)
- **N-01 (NIT)** — [`subject/research-gates_a3325836.yml:170`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L170): `python -m pip install ruff==0.16.4` installs Ruff without `--require-hashes` (unlike `IBKR_PAPER_BRIDGE/requirements.lock` at line 162). While pinning an exact version satisfies progressive activation for an informational check, a future hardening round before promoting to a required check should pin hashes.
- **N-02 (NIT)** — [`subject/research-gates_a3325836.yml:115`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L115): `git config --system core.longpaths true` executes with `--system` scope. Hosted runners have administrator privileges so this step succeeds, but `--global` is standard for unprivileged runner environments.

### Object 2: Acceptance Packet (`P027_ACCEPTANCE_PACKET_20260915.md`)
- **Verdict:** **PASS-WITH-NITS** (0 REQUIRED, 1 NIT)
- **N-03 (NIT)** — [`subject/P027_ACCEPTANCE_PACKET_20260915.md:57`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L57): §4 Item E10 cites `CI_PR193/P027_CI_ADDITIONS_EVIDENCE_20260915.md`. In the verification packet this is `sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md`. A trivial provenance reference difference.

---

## (d) Exact Native Read Coverage

All reads performed with native `view_file` (max 150 lines per view) inside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915`:

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
23. Optional: [`sources/RED_RUN_34946092493_failed_log.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_RUN_34946092493_failed_log.txt): lines 1–56 (complete)
24. Optional: [`sources/pine-defang-guard_fcac0ac6.yml`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/pine-defang-guard_fcac0ac6.yml): lines 1–21 (complete)

---

## (e) Non-Empty NOT VERIFIED Scope

1. **No Live Execution or Network/API Access:** Live GitHub API state, repository settings, live ruleset configuration, and actual runner executions cannot be independently executed or queried.
2. **Repository Files Outside Packet:** Canonical repository files (e.g. `MTC_COMMAND_CENTER/contracts/constraints.txt` to verify the Ruff pin, `MTC_COMMAND_CENTER/contracts/tests`, `tools/opsa/test_opsa.py`, `AGENTS.md`) cannot be opened.
3. **Historical 2026-08-25 Audit Artifacts:** `GLM_AG_P027_REPORT.md` and WAL lane audit records are outside the packet.
4. **Intermediate Git Commit Patch:** The exact isolated diff between intermediate commit `55ab90b8` and `a3325836` is not directly isolated (only base→HEAD diff is in the packet).
5. **R19 Grep Sweep Execution:** The grep command over CT13 `f1bbac40` reported in packet §9 cannot be run by a read-only unexecuted reviewer.
6. **Delivery of Demo-Run E-mail:** The specific e-mail for demo run 34946092493 is confirmed by owner word only; the forwarded artifact proves the GitHub notification delivery channel via run 34961383292.

---

## (f) JSON Verdict

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
      "id": "N-01",
      "severity": "NIT",
      "target": "workflow_diff",
      "file_line": "subject/research-gates_a3325836.yml:170",
      "description": "Ruff is installed without --require-hashes (unlike requirements.lock in the same job); acceptable for an informational gate, but hash-locking should be added in a hardening pass."
    },
    {
      "id": "N-02",
      "severity": "NIT",
      "target": "workflow_diff",
      "file_line": "subject/research-gates_a3325836.yml:115",
      "description": "git config core.longpaths true uses --system scope; succeeds on hosted runners due to admin privileges, but --global is more standard."
    },
    {
      "id": "N-03",
      "severity": "NIT",
      "target": "acceptance_packet",
      "file_line": "subject/P027_ACCEPTANCE_PACKET_20260915.md:57",
      "description": "Item E10 lists path as CI_PR193/P027_CI_ADDITIONS_EVIDENCE_20260915.md whereas packet copy is located under sources/."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
