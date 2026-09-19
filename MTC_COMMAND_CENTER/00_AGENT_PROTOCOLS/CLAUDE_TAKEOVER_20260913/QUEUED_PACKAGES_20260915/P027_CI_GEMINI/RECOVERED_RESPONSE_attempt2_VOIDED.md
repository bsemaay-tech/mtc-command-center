## Independent Read-Only T2 Corroboration Review (WP-P0-27)

**Reviewer Role:** `gemini-3.8-flash-high` (Supplemental Read-Only Corroborating Reviewer; `SUPPLEMENTAL_UNEXECUTED`).  
**Reviewed Objects:**
1. **Pull-Request #193 Workflow Diff:** `.github/workflows/research-gates.yml` (`fcac0ac6` → `a3325836`), authored under owner directive `OD-20260915-P027-CI-ADDITIONS-GO-1`, OPEN and unmerged.
2. **Acceptance Packet:** [P027_ACCEPTANCE_PACKET_20260915.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md) (recommending day-one scope acceptance).

---

### Task Part A — PR #193 Workflow Diff

| Item | Status | Packet-Relative Citations & Analysis |
|---|---|---|
| **A1** | **CORROBORATED** | [DIFF_fcac0ac6_a3325836_research-gates.diff:1-101](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L1-L101); [DIFF_STAT_fcac0ac6_a3325836.txt:1-2](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_STAT_fcac0ac6_a3325836.txt#L1-L2); [research-gates_a3325836.yml:10-18,104-135,142-176](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L10-L18); [research-gates_fcac0ac6_BASE.yml:1-93](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_fcac0ac6_BASE.yml#L1-L93).<br>• Exactly two jobs were added: `p030-checkers` on `windows-2025` and `contracts-and-lint` on `ubuntu-24.04`.<br>• Header comment was updated (lines 10–18).<br>• Existing `checkers` job (lines 37–97), `on:` triggers (lines 21–27), `permissions: contents: read` (lines 29–30), and `concurrency:` block (lines 32–34) are byte-unchanged.<br>• A workflow file cannot edit repository rulesets. Neither new job name (`p030-checkers` / `P0-30 checkers (Python 3.12, Windows)` or `contracts-and-lint` / `Contracts tests and Ruff (Python 3.12)`) collides with ruleset 21444962 required contexts (`Bridge suite (Python 3.12)` and `pine-alert-guard`). |
| **A2** | **CORROBORATED** | [research-gates_a3325836.yml:48,107,120,145,153,161-164,169-175](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L48); [ci_fcac0ac6.yml:21-46](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/ci_fcac0ac6.yml#L21-L46); [PLAN_WP_P0_27_block_lines590-602.md:5,14](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PLAN_WP_P0_27_block_lines590-602.md#L5).<br>• Diff contains zero `secrets.*` references, no `schedule:` trigger, no self-hosted runners, and no host/venue contact.<br>• `persist-credentials: false` is present on all checkouts; timeouts are present (`15m` and `10m`).<br>• **Pinning comparison:** `actions/checkout@v4` and `actions/setup-python@v5` match existing `ci.yml` conventions exactly (**consistent**). Bridge dependency installation uses `python -m pip install --require-hashes -r IBKR_PAPER_BRIDGE/requirements.lock` (**consistent**). Ruff is installed via `pip install ruff==0.16.4` without `--require-hashes` (**minor weakening** compared to hash-locked dependencies, but consistent with quick linter setup in informational jobs; graded **NIT**). The claim that `0.16.4` matches `MTC_COMMAND_CENTER/contracts/constraints.txt` is **NOT VERIFIED** (outside packet). |
| **A3** | **CORROBORATED** | [research_gates_run_34961383292_RED_checkout.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json#L1); [research_gates_run_34963602576.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json#L1); [COMMITS_55ab90b8_a3325836.txt:7-10](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/COMMITS_55ab90b8_a3325836.txt#L7-L10).<br>• In run 34961383292 (`55ab90b8`), `P0-30 checkers (Python 3.12, Windows)` failed specifically at step 2 (`Check out repository`), while the other two jobs succeeded.<br>• In run 34963602576 (`a3325836`), step 2 (`Enable long paths for the checkout` running `git config --system core.longpaths true`) preceded checkout; all three jobs completed SUCCESS.<br>• **Intermediate state:** The diff held is base→HEAD (`fcac0ac6` → `a3325836`). The intermediate state `55ab90b8` is corroborated by run JSON step structures and commit messages, but its exact intermediate tree cannot be independently viewed from git objects.<br>• `--system` vs `--global`: On an ephemeral hosted runner, `--system` correctly alters the runner's git behavior system-wide; graded **NIT** (NIT-at-most). |
| **A4** | **CORROBORATED** | [PLAN_WP_P0_27_block_lines590-602.md:5-7](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PLAN_WP_P0_27_block_lines590-602.md#L5-L7); [P027_CI_POLICY_2026-08-25.md:30,92-104](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_POLICY_2026-08-25.md#L30); [P027_ACCEPTANCE_PACKET_20260915.md:23](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L23).<br>• Scoping Ruff to clean surfaces (`tools/opsa`, `contracts`) with select rules (`E9,F821,F811,F401,F841`) while excluding surfaces with known findings (3 / 21 / 69) adheres directly to the plan’s progressive-activation doctrine ("no big-bang enablement").<br>• Packet §3 row R2 text: `"Bridge suite ✔; lint = compileall only on master; Ruff step WIRED in PR #193 (open)"` with scope `"yes (lint at the compileall level; Ruff = backlog until PR #193's T1)"`. This does not overclaim R2; it accurately demarcates `compileall` as the merged day-one lint and Ruff as unmerged backlog. |
| **A5** | **CORROBORATED** | [P027_CI_ADDITIONS_EVIDENCE_20260915.md:1-18](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md#L1-L18); [pr193_state_GREEN.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/pr193_state_GREEN.json#L1); [research_gates_run_34961383292_RED_checkout.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34961383292_RED_checkout.json#L1); [research_gates_run_34963602576.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/research_gates_run_34963602576.json#L1); [GH_QUERIES_20260915_NIGHT.txt:15](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L15).<br>• **Supported by packet JSONs:** Run IDs (34961383292, 34963602576, 34963602580, 34963602573), job names, step names and order, timestamps and job durations (P0-30 checkers: 11:30:02Z→11:30:42Z, contracts: 11:30:02Z→11:30:29Z), conclusions (RED checkout failure on 55ab90b8; SUCCESS across all jobs on a3325836), commit SHAs, PR #193 `state: OPEN`, `mergeStateStatus: CLEAN`.<br>• **NOT supported by JSONs:** Local worktree path `C:/tmp/P027_CI_20260915`, local pre-check outputs (50 contracts passes in local venv, findings counts 3/21/69), exact stdout log string (`Filename too long` is absent from JSON, though step failure is present), and PR opening timestamp (11:04Z). |

---

### Task Part B — Acceptance Packet (`P027_ACCEPTANCE_PACKET_20260915.md`)

| Item | Status | Packet-Relative Citations & Analysis |
|---|---|---|
| **B1** | **CORROBORATED** | [P027_ACCEPTANCE_PACKET_20260915.md:11-18](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L11-L18).<br>• **Clause (a):** [GH_QUERIES_20260915_NIGHT.txt:7-12,22](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L7-L12). Shows `ci.yml` blob `3394d9ff…`, 61 runs on `master` (60 success, 1 failure: run 32846169952 at `110305c0` on 2026-08-25T12:10:43Z). **CORROBORATED**.<br>• **Clause (b):** [RED_DEMO_EVIDENCE_20260915.md:8-18](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_DEMO_EVIDENCE_20260915.md#L8-L18); [PR192_state_RED.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_RED.json#L1); [PR192_state_GREEN.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_GREEN.json#L1); [CI_FAILURE_EMAIL_ARTIFACT_MASKED.md:5-18](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md#L5-L18). Draft PR #192 failed at run 34946092493, restored to green at run 34946405229, closed unmerged. E-mail receipt owner-confirmed ("yes" ~08:32Z); channel delivery artifact verified via PR #193 failure mail (`1a0a4d879a3c386d`, `notifications@github.com`). **CORROBORATED**.<br>• **Clause (c):** [GH_QUERIES_20260915_NIGHT.txt:4](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L4); [PR192_state_RED.json:1](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PR192_state_RED.json#L1). Ruleset 21444962 active, strict policy true, bypass actors 0, required contexts `Bridge suite (Python 3.12)` + `pine-alert-guard`. PR #192 was BLOCKED while red. **CORROBORATED**.<br>• **Clause (d):** [P027_ACCEPTANCE_PACKET_20260915.md:17,87](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L17). Reports 0 claims in sweep of CT13 `f1bbac40`. Execution of external grep is NOT VERIFIED, but accurately stated in packet documentation. **CORROBORATED**. |
| **B2** | **CORROBORATED** | [P027_REQUIREMENT_RECONCILIATION_20260915.md:8-9](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L8-L9); [P027_ACCEPTANCE_PACKET_20260915.md:60](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L60); [GH_QUERIES_20260915_NIGHT.txt:7-12](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/GH_QUERIES_20260915_NIGHT.txt#L7-L12).<br>• The morning reconciliation incorrectly asserted: `"across the last 200 CI runs there is no failure conclusion at all … until today no run had ever turned RED."`<br>• The night query revealed run 32846169952 at `110305c0` (2026-08-25T12:10:43Z) failed on `master`, fixed forward by `cef1d070` at 15:04:24Z.<br>• Packet §5 item 1 correctly rectifies this without changing any R-row disposition; R5 is reinforced by demonstrating historical fix-forward adherence. |
| **B3** | **CORROBORATED** | [P027_ACCEPTANCE_PACKET_20260915.md:63-78](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L63-L78).<br>• The 2026-08-25 audit records (GLM-5.3 T1 report, Codex xhigh T0 audit) reside outside the packet and are **NOT VERIFIED**.<br>• §7 recommendation preserves owner prerogative: it sets out explicit owner words (`"accept day-one scope"`, `"not yet"`, `"accept, and add the exact-flagship read first"`). It explicitly guarantees that accepting day-one does NOT merge PR #193, does NOT alter ruleset 21444962, and does NOT make `Research gates` required. |
| **B4** | **CORROBORATED** | [P027_REQUIREMENT_RECONCILIATION_20260915.md:12-33,58-60](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L12-L33); [P027_ACCEPTANCE_PACKET_20260915.md:20-43](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L20-L43).<br>• Rows updated between morning reconciliation (+ 11:42Z addendum) and packet §3:<br>  - **R2:** Incorporates addendum and PR #193 green run, noting `compileall` on `master` and Ruff as backlog until T1.<br>  - **R5:** Incorporates delivery channel artifact and historical 08-25 failure.<br>  - **R10:** Notes the three P0-30 checkers are wired in PR #193 (backlog).<br>  - **R12:** Moves contract tests from MISSING to WIRED in PR #193 (backlog until T1).<br>  - **R19:** Moves from "to be re-checked" to "HOLDS (sweep tonight)".<br>• All row state differences are fully justified by the night evidence. |
| **B5** | **CORROBORATED** | [P027_ACCEPTANCE_PACKET_20260915.md:17,87](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L17).<br>• Execution of the sweep is **NOT VERIFIED** (no execution tools).<br>• Packet §9 explicitly specifies the exact pattern list (`continuous protection|continuously protect|continuous-protection|gates repository changes|protects master|protecting master|CI protects|guard protects`, `OPS-C` × `built|running|protect|PROVEN|live`, and the four ops-check names × `PROVEN`) and exact tree target (`CT13 f1bbac40`). |
| **B6** | **CORROBORATED** | [P027_REQUIREMENT_RECONCILIATION_20260915.md:18](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/P027_REQUIREMENT_RECONCILIATION_20260915.md#L18); [RED_DEMO_EVIDENCE_20260915.md:18](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/RED_DEMO_EVIDENCE_20260915.md#L18); [PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md:34-37](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md#L34-L37).<br>• **Predecessor NIT 1 (R5 relabel):** Held at `P027_REQUIREMENT_RECONCILIATION_20260915.md:18` ("relabelled 10:25Z from IMPLEMENTED + VERIFIED").<br>• **Predecessor NIT 2 (RED demo wording):** Held at `RED_DEMO_EVIDENCE_20260915.md:18` ("Notification half CLOSED on the owner's word; an immutable artifact ... NOT on record").<br>• **Predecessor NIT 3 (P0-26 packet note):** Confirmed outside this packet. |

---

### New Findings

1. **Finding F-01 (NIT, Object 1 — Workflow Diff):**
   - **Location:** [research-gates_a3325836.yml:170](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L170); [DIFF_fcac0ac6_a3325836_research-gates.diff:95](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L95)
   - **Description:** `python -m pip install ruff==0.16.4` pins the version string without `--require-hashes`. While acceptable in an informational workflow, it is weaker than the hash-locked dependency installation used in line 162. The claim that `0.16.4` matches `MTC_COMMAND_CENTER/contracts/constraints.txt` is unverified due to read scope boundaries.
   - **Severity:** NIT.

2. **Finding F-02 (NIT, Object 1 — Workflow Diff):**
   - **Location:** [research-gates_a3325836.yml:115](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/research-gates_a3325836.yml#L115); [DIFF_fcac0ac6_a3325836_research-gates.diff:40](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/DIFF_fcac0ac6_a3325836_research-gates.diff#L40)
   - **Description:** Checkout step uses `git config --system core.longpaths true`. On GitHub-hosted runners, `--system` functions correctly and resolves long path checkouts (as demonstrated in run 34963602576), though `--global` is conventional.
   - **Severity:** NIT.

3. **Finding F-03 (NIT, Object 2 — Acceptance Packet):**
   - **Location:** [P027_ACCEPTANCE_PACKET_20260915.md:52,61](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/subject/P027_ACCEPTANCE_PACKET_20260915.md#L52)
   - **Description:** Packet §4 Item E5 references the artifact as `CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md`, whereas the source file in this packet is named [CI_FAILURE_EMAIL_ARTIFACT_MASKED.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915/sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md). Both reference identical message ID `1a0a4d879a3c386d`.
   - **Severity:** NIT.

---

### Exact Read Coverage

All reads performed using native `view_file` capped at ≤150 lines per view call:
1. `PACKET_SHA256SUMS.txt`: lines 1–24 (complete).
2. `subject/DIFF_fcac0ac6_a3325836_research-gates.diff`: lines 1–101 (complete).
3. `subject/DIFF_STAT_fcac0ac6_a3325836.txt`: lines 1–3 (complete).
4. `subject/research-gates_a3325836.yml`: lines 1–150; continuation lines 151–176 (complete).
5. `subject/research-gates_fcac0ac6_BASE.yml`: lines 1–93 (complete).
6. `subject/COMMITS_55ab90b8_a3325836.txt`: lines 1–40 (complete).
7. `subject/P027_ACCEPTANCE_PACKET_20260915.md`: lines 1–89 (complete).
8. `sources/ci_fcac0ac6.yml`: lines 1–56 (complete).
9. `sources/P027_CI_POLICY_2026-08-25.md`: lines 1–150; continuation lines 151–177 (complete).
10. `sources/PLAN_WP_P0_27_block_lines590-602.md`: lines 1–15 (complete).
11. `sources/DECISIONS_rows_P027.md`: lines 1–6 (complete).
12. `sources/P027_CI_ADDITIONS_EVIDENCE_20260915.md`: lines 1–18 (complete).
13. `sources/pr193_state_GREEN.json`: lines 1–2 (complete).
14. `sources/research_gates_run_34961383292_RED_checkout.json`: lines 1–2 (complete).
15. `sources/research_gates_run_34963602576.json`: lines 1–2 (complete).
16. `sources/GH_QUERIES_20260915_NIGHT.txt`: lines 1–25 (complete).
17. `sources/P027_REQUIREMENT_RECONCILIATION_20260915.md`: lines 1–60 (complete).
18. `sources/RED_DEMO_EVIDENCE_20260915.md`: lines 1–21 (complete).
19. `sources/PR192_state_RED.json`: lines 1–2 (complete).
20. `sources/PR192_state_GREEN.json`: lines 1–2 (complete).
21. `sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md`: lines 1–59 (complete).
22. `sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md`: lines 1–43 (complete).
23. `sources/RED_RUN_34946092493_failed_log.txt`: lines 1–56 (complete, optional read).
24. `sources/pine-defang-guard_fcac0ac6.yml`: lines 1–21 (complete, optional read).

---

### Nonempty NOT VERIFIED

- **Execution Capabilities:** No terminal commands, test executions, or scripts were run (`SUPPLEMENTAL_UNEXECUTED`).
- **Live GitHub API / External Network:** Live remote states, runner-side environments, and network connectivity were not queried directly; analysis relies on the captured JSON/text evidence copies.
- **Paths Outside Packet:** No paths outside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915` were inspected, including `MTC_COMMAND_CENTER/contracts/constraints.txt`, CT13 `f1bbac40`, `GLM_AG_P027_REPORT.md`, `WAL_CAPTURE_FIX_2026-08-25/FIX_EVIDENCE.md`, and `AGENTS.md`.
- **R19 Grep Execution:** The execution of the R19 grep sweep across the full repository tree cannot be executed by read-only reviewers.
- **Unforwarded Demo-Run Email:** Actual receipt of the 08:18Z demo failure email in the owner's mailbox remains owner-confirmed in chat; the channel delivery artifact on record is the forwarded 11:06Z PR #193 failure mail.
- **Stdout Log Details of Run 34961383292:** The exact raw string `"Filename too long"` is absent from the JSON run structure (only step failure is present).

---

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
      "object": "workflow_diff",
      "severity": "NIT",
      "location": "subject/research-gates_a3325836.yml:170",
      "description": "Ruff is installed without hash locking (--require-hashes) unlike Bridge requirements; constraints.txt parity unverified due to scope."
    },
    {
      "finding_id": "F-02",
      "object": "workflow_diff",
      "severity": "NIT",
      "location": "subject/research-gates_a3325836.yml:115",
      "description": "git config uses --system instead of --global for core.longpaths; functional on hosted runners but NIT-at-most."
    },
    {
      "finding_id": "F-03",
      "object": "acceptance_packet",
      "severity": "NIT",
      "location": "subject/P027_ACCEPTANCE_PACKET_20260915.md:52",
      "description": "Packet cites artifact filename CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md, while packet source file is named CI_FAILURE_EMAIL_ARTIFACT_MASKED.md."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
