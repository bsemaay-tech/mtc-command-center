# Independent Read-Only T2 Corroboration Review: WP-P0-27

**Reviewer Model:** Gemini 3.8 Flash (High)  
**Role:** Independent Read-Only T2 Corroborating Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Scope of Review:**  
1. Pull-request #193 workflow diff: `.github/workflows/research-gates.yml` (`fcac0ac6` → `a3325836`, OPEN / unmerged)  
2. Acceptance packet: `P027_ACCEPTANCE_PACKET_20260915.md` (recommends owner acceptance of WP-P0-27 day-one scope)

---

## (a) Task Part A — Pull Request #193 Workflow Diff

| Item | Status | Key Evidence & Citations | Analysis & Findings |
|---|---|---|---|
| **A1** | **CORROBORATED** | [`DIFF_fcac0ac6_a3325836_research-gates.diff:10-16,29-60,67-101`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L10-L16)<br>[`DIFF_STAT_fcac0ac6_a3325836.txt:1-2`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_STAT_fcac0ac6_a3325836.txt#L1-L2)<br>[`research-gates_a3325836.yml:13-18,104-135,142-176`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L13-L18)<br>[`research-gates_fcac0ac6_BASE.yml:1-93`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_fcac0ac6_BASE.yml#L1-L93)<br>[`GH_QUERIES_20260915_NIGHT.txt:4`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L4) | • Exactly two jobs were added: `p030-checkers` (Windows) and `contracts-and-lint` (Ubuntu), plus an updated header comment. Diff stat confirms 84 insertions, 1 deletion in 1 file.<br>• Pre-existing `checkers` job, `on:` triggers, `permissions: contents: read`, and `concurrency` block are byte-unchanged.<br>• **Ruleset 21444962 alteration:** A workflow YAML file cannot alter repository rulesets. The ruleset requires `Bridge suite (Python 3.12)` and `pine-alert-guard`. Neither new job name (`P0-30 checkers (Python 3.12, Windows)`, `Contracts tests and Ruff (Python 3.12)`) collides with the required contexts. |
| **A2** | **CORROBORATED** | [`research-gates_a3325836.yml:21-34,48-49,120-121,153-154,162-164,170`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L21-L34)<br>[`PLAN_WP_P0_27_block_lines590-602.md:5,14`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PLAN_WP_P0_27_block_lines590-602.md#L5)<br>[`ci_fcac0ac6.yml:27-29,37-39`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/ci_fcac0ac6.yml#L27-L29)<br>[`COMMITS_55ab90b8_a3325836.txt:30-31`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L30-L31) | • Zero `secrets.*`, no `schedule:` trigger, no self-hosted runners (`windows-2025`, `ubuntu-24.04`), timeouts present (15 min, 10 min), `persist-credentials: false` on all checkouts.<br>• Network contact limited to PyPI and GitHub actions.<br>• **Pinning conventions:**<br>  - `actions/*` pinned by major tag (`@v4`, `@v5`): consistent with `ci.yml`.<br>  - Bridge install uses `--require-hashes -r IBKR_PAPER_BRIDGE/requirements.lock`: consistent with `ci.yml`.<br>  - Ruff install pins `ruff==0.16.4` by version only without hashes: minor weakening vs lockfile hermeticity, but acceptable for an informational job (**NIT**). Claimed equality to `MTC_COMMAND_CENTER/contracts/constraints.txt` is **NOT VERIFIED** (external file). |
| **A3** | **CORROBORATED** | [`research_gates_run_34961383292_RED_checkout.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json#L1)<br>[`research_gates_run_34963602576.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json#L1)<br>[`COMMITS_55ab90b8_a3325836.txt:7-10`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L7-L10)<br>[`research-gates_a3325836.yml:115`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L115) | • RED run 34961383292 failed on `P0-30 checkers (Windows)` at step 2 (`Check out repository`), while the other two jobs succeeded.<br>• Commit `a3325836` added `git config --system core.longpaths true` before checkout.<br>• GREEN run 34963602576 completed with `conclusion: success` on all three jobs.<br>• Intermediate commit `55ab90b8` tree itself is not provided as an isolated diff in the packet (**NOT VERIFIED**), but is documented by commit logs and the RED run `headSha`.<br>• Using `--system` is valid and sufficient on an ephemeral hosted runner (**NIT-at-most**). |
| **A4** | **CORROBORATED** | [`COMMITS_55ab90b8_a3325836.txt:31-33`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L31-L33)<br>[`P027_CI_ADDITIONS_EVIDENCE_20260915.md:14`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md#L14)<br>[`P027_ACCEPTANCE_PACKET_20260915.md:23`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L23)<br>[`P027_REQUIREMENT_RECONCILIATION_20260915.md:15`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L15) | • Narrow Ruff scope (`tools/opsa`, `contracts`) avoids starting red while enforcing light lint progressively.<br>• Packet R2 row verbatim: `\| R2 \| day-one job = Bridge suite + light lint \| Bridge suite ✔; lint = compileall only on master; Ruff step WIRED in PR #193 (open) \| yes (lint at the compileall level; Ruff = backlog until PR #193's T1) \|`.<br>• The packet does not overclaim R2: it explicitly states that on `master`, lint remains `compileall` only, and Ruff is backlog pending PR #193 merge. |
| **A5** | **CORROBORATED** | [`P027_CI_ADDITIONS_EVIDENCE_20260915.md:1-16`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md#L1-L16)<br>[`pr193_state_GREEN.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/pr193_state_GREEN.json#L1)<br>[`research_gates_run_34961383292_RED_checkout.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json#L1)<br>[`research_gates_run_34963602576.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json#L1) | • **Corroborated by packet JSONs:** PR #193 open, `mergeStateStatus: CLEAN`, run 34961383292 failure on Windows checkout, run 34963602576 success on all 3 jobs with exact timestamps (P0-30: 11:30:02Z→11:30:42Z; Contracts/Ruff: 11:30:02Z→11:30:29Z).<br>• **Not verifiable from JSONs:** Local execution counts (50 contracts tests in P020 venv; Ruff 3 / 21 / 69 findings on unscoped surfaces) and pre-commit guard `LEAD_GUARD_CI_PR.txt` (**NOT VERIFIED**). |

---

## (b) Task Part B — Acceptance Packet (`P027_ACCEPTANCE_PACKET_20260915.md`)

| Item | Status | Key Evidence & Citations | Analysis & Findings |
|---|---|---|---|
| **B1** | **CORROBORATED** | [`P027_ACCEPTANCE_PACKET_20260915.md:11-18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L11-L18)<br>[`GH_QUERIES_20260915_NIGHT.txt:4,7-12,18,22`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L4)<br>[`PR192_state_RED.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_RED.json#L1)<br>[`PR192_state_GREEN.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_GREEN.json#L1)<br>[`CI_FAILURE_EMAIL_ARTIFACT_MASKED.md:8-18,23`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md#L8-L18) | **Four acceptance gates (§2):**<br>• **Clause (a): CORROBORATED.** `ci.yml` blob `3394d9ff…` at `fcac0ac6`; histogram of 61 master runs shows 60 success, 1 failure (`110305c0` at 2026-08-25T12:10:43Z).<br>• **Clause (b): CORROBORATED.** PR #192 red probe run 34946092493 failure; green run 34946405229 success; PR closed unmerged; notification supported by chat "yes" and channel artifact `CI_FAILURE_EMAIL_ARTIFACT_MASKED.md` (sender `notifications@github.com`, run 34961383292).<br>• **Clause (c): CORROBORATED.** Ruleset 21444962 active, strict, 0 bypass actors, requiring `Bridge suite (Python 3.12)` and `pine-alert-guard`; PR #192 BLOCKED when red, CLEAN when green.<br>• **Clause (d): CORROBORATED.** R19 sweep documented over CT13 `f1bbac40` showing 0 continuous-protection claims (unexecuted by reviewer, documentary custody holds). |
| **B2** | **CORROBORATED** | [`P027_ACCEPTANCE_PACKET_20260915.md:59-61`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L59-L61)<br>[`P027_REQUIREMENT_RECONCILIATION_20260915.md:8-9,18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L8-L9)<br>[`GH_QUERIES_20260915_NIGHT.txt:7-12`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L7-L12) | • Packet §5 item 1 correctly rectifies the reconciliation's claim ("never turned RED") against `GH_QUERIES_20260915_NIGHT.txt` (failed run 32846169952 at `110305c0`).<br>• This correction does not weaken R5; rather, it corroborates that master was fixed forward within 2 h 54 min prior to ruleset enforcement, leaving the R-row dispositions unchanged. |
| **B3** | **CORROBORATED** | [`P027_ACCEPTANCE_PACKET_20260915.md:63-78`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L63-L78) | • Review lineage citations (GLM-5.3 T1 slot and Codex T0 audit) are historical and **NOT VERIFIED** (external files).<br>• §7 recommendation strictly bounds authority: acceptance is reserved for the owner; PR #193 is explicitly excluded from the acceptance object and left open for separate T1 review. |
| **B4** | **CORROBORATED** | [`P027_ACCEPTANCE_PACKET_20260915.md:23,26,31,33,40`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L23)<br>[`P027_REQUIREMENT_RECONCILIATION_20260915.md:15,18,23,25,32,58-60`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L15) | • Differences between packet §3 and the morning reconciliation are fully justified by the night evidence and addendum:<br>  - **R2:** Updated to note Ruff is wired in PR #193 (open).<br>  - **R5:** Updated to include the single historical 08-25 red incident and channel artifact.<br>  - **R10:** Updated to note three P0-30 checkers wired in PR #193.<br>  - **R12:** Updated from MISSING to WIRED in PR #193.<br>  - **R19:** Updated from "to be re-checked" to "HOLDS (sweep tonight)". |
| **B5** | **CORROBORATED** | [`P027_ACCEPTANCE_PACKET_20260915.md:17,87`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L17) | • The packet explicitly provides the exact grep pattern list and the tree identity swept (`CT13 f1bbac40`).<br>• Execution of the sweep is **NOT VERIFIED** by this reviewer, but documentary integrity is confirmed. |
| **B6** | **CORROBORATED** | [`PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md:33-36`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md#L33-L36)<br>[`P027_REQUIREMENT_RECONCILIATION_20260915.md:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L18)<br>[`RED_DEMO_EVIDENCE_20260915.md:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_DEMO_EVIDENCE_20260915.md#L18) | • Predecessor NIT 1 (R5 relabelled from "IMPLEMENTED + VERIFIED") held in `P027_REQUIREMENT_RECONCILIATION_20260915.md:18`.<br>• Predecessor NIT 2 ("closed on the owner's word" and noting lack of immutable artifact) held in `RED_DEMO_EVIDENCE_20260915.md:18`.<br>• Predecessor NIT 3 relates to P0-26, which is outside this packet. |

---

## (c) Findings and Grading

### Object (1): PR #193 Workflow Diff (`.github/workflows/research-gates.yml`)
- **F-01 (NIT): Unhashed pip install pin for Ruff.**  
  [`subject/research-gates_a3325836.yml:170`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L170): `python -m pip install ruff==0.16.4` pins by version but omits `--require-hashes`, unlike the Bridge installation (`IBKR_PAPER_BRIDGE/requirements.lock`). For an informational job, this is acceptable, but it constitutes a minor hermeticity weakening. The referenced constraint file (`MTC_COMMAND_CENTER/contracts/constraints.txt`) cannot be verified from the packet.
- **F-02 (NIT): Absence of intermediate commit diff.**  
  [`subject/COMMITS_55ab90b8_a3325836.txt:1-13`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L1-L13): The provided diff is base-to-HEAD (`fcac0ac6` → `a3325836`). The intermediate state at `55ab90b8` (which failed the Windows checkout) is substantiated by run JSON metadata and commit logs, but the exact commit tree diff for `55ab90b8` was not packaged.

**Verdict on Workflow Diff:** `PASS-WITH-NITS` (0 REQUIRED findings).

### Object (2): Acceptance Packet (`P027_ACCEPTANCE_PACKET_20260915.md`)
- **F-03 (NIT): Documentary reliance on unexecuted grep sweep.**  
  [`subject/P027_ACCEPTANCE_PACKET_20260915.md:17,87`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L17): Clause 2(d) / §9:87 records the R19 sweep across tree `f1bbac40`. The reviewer can verify the documentation and pattern specification, but cannot independently execute the command across the canonical repository. The packet appropriately treats this as an acceptance-step assertion by the Lead.

**Verdict on Acceptance Packet:** `PASS-WITH-NITS` (0 REQUIRED findings).

---

## (d) Exact Read Coverage with Ranges and Continuations

All 22 packet files plus the checksum index were completely read natively using `view_file` (≤150 lines per slice):
1. `PACKET_SHA256SUMS.txt`: lines 1–24 (complete)
2. `subject/DIFF_fcac0ac6_a3325836_research-gates.diff`: lines 1–101 (complete)
3. `subject/DIFF_STAT_fcac0ac6_a3325836.txt`: lines 1–3 (complete)
4. `subject/research-gates_a3325836.yml`: lines 1–150; continuation lines 151–176 (complete)
5. `subject/research-gates_fcac0ac6_BASE.yml`: lines 1–93 (complete)
6. `subject/COMMITS_55ab90b8_a3325836.txt`: lines 1–40 (complete)
7. `subject/P027_ACCEPTANCE_PACKET_20260915.md`: lines 1–89 (complete)
8. `sources/ci_fcac0ac6.yml`: lines 1–56 (complete)
9. `sources/P027_CI_POLICY_2026-08-25.md`: lines 1–150; continuation lines 151–177 (complete)
10. `sources/PLAN_WP_P0_27_block_lines590-602.md`: lines 1–15 (complete)
11. `sources/DECISIONS_rows_P027.md`: lines 1–6 (complete)
12. `sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md`: lines 1–18 (complete)
13. `sources/pr193_state_GREEN.json`: lines 1–2 (complete)
14. `sources/research_gates_run_34961383292_RED_checkout.json`: lines 1–2 (complete)
15. `sources/research_gates_run_34963602576.json`: lines 1–2 (complete)
16. `sources/GH_QUERIES_20260915_NIGHT.txt`: lines 1–25 (complete)
17. `sources/P027_REQUIREMENT_RECONCILIATION_20260915.md`: lines 1–60 (complete)
18. `sources/RED_DEMO_EVIDENCE_20260915.md`: lines 1–21 (complete)
19. `sources/PR192_state_RED.json`: lines 1–2 (complete)
20. `sources/PR192_state_GREEN.json`: lines 1–2 (complete)
21. `sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md`: lines 1–59 (complete)
22. `sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md`: lines 1–43 (complete)
*Optional reads completed:*
23. `sources/RED_RUN_34946092493_failed_log.txt`: lines 1–56 (complete)
24. `sources/pine-defang-guard_fcac0ac6.yml`: lines 1–21 (complete)

---

## (e) Nonempty NOT VERIFIED

The following items cannot be corroborated from the read-only packet copies:
1. **Live GitHub State & Execution:** Live verification of GitHub API endpoints, ruleset enforcement, and active webhook delivery.
2. **Intermediate Git Tree of Commit `55ab90b8`:** Isolated tree diff for `55ab90b8` (only base-to-HEAD diff `fcac0ac6` → `a3325836` is present).
3. **External Constraint Pin:** `MTC_COMMAND_CENTER/contracts/constraints.txt` establishing the pinned version `0.16.4` for Ruff.
4. **Local Execution Metrics:** Local pytest and Ruff finding tallies (3 / 21 / 69) reported in `P027_CI_ADDITIONS_EVIDENCE_20260915.md:14`.
5. **Local Pre-Commit Guard Log:** `LEAD_GUARD_CI_PR.txt` cited in `P027_CI_ADDITIONS_EVIDENCE_20260915.md:8`.
6. **Historical Audit Artifacts (2026-08-25):** `GLM_AG_P027_REPORT.md` and Codex xhigh T0 audit `WAL_CAPTURE_FIX_2026-08-25/FIX_EVIDENCE.md`.
7. **R19 Full Tree Grep:** Independent execution of the R19 search pattern across canonical repository tree `f1bbac40`.
8. **Demo-Run Notification Email:** The specific e-mail for demo run 34946092493 remains owner-confirmed; immutable artifact on record is for run 34961383292.
9. **Failing Behavior of `pine-alert-guard`:** No red run of `pine-alert-guard` exists on record.
10. **Predecessor NIT 3:** Disposition of `P026_DEPLOYMENT_AND_DRILL_DECISION_PACKET_20260915.md` (outside this packet).

---

## (f) Formal JSON Verdict

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
      "finding_id": "F-01",
      "severity": "NIT",
      "object": "workflow_diff",
      "citation": "subject/research-gates_a3325836.yml:170",
      "description": "Ruff is installed via pip with an exact version pin (ruff==0.16.4) but without --require-hashes, slightly weakening dependency hermeticity vs Bridge lockfile. Constraint file MTC_COMMAND_CENTER/contracts/constraints.txt is not in packet."
    },
    {
      "finding_id": "F-02",
      "severity": "NIT",
      "object": "workflow_diff",
      "citation": "subject/COMMITS_55ab90b8_a3325836.txt:1-13",
      "description": "The packet contains only base-to-HEAD diff (fcac0ac6 to a3325836); the intermediate tree at 55ab90b8 is documented by commit logs and run metadata but lacks an intermediate diff file."
    },
    {
      "finding_id": "F-03",
      "severity": "NIT",
      "object": "acceptance_packet",
      "citation": "subject/P027_ACCEPTANCE_PACKET_20260915.md:17,87",
      "description": "R19 sweep pattern and tree identity are fully documented, but the grep execution cannot be rerun by a read-only reviewer restricted to the packet directory."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
