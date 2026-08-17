# NEXT SESSION HANDOFF — Gate A Queue D resume (2026-08-03B)

Standalone pickup for a fresh session. Written by Claude Opus 5 (Lead) after the overnight Codex
run exhausted its credit window. Companion status report:
`11_TRIAGE/GATE_A_QUEUE_D_INTEGRATION_STATUS_2026-08-03.md`.

---

## Copy-paste prompt for the new conversation

```
Read AGENTS.md, then MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md, then
MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_QUEUE_D_INTEGRATION_STATUS_2026-08-03.md,
then MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-03B.md.

Records state as of docs commit ba228339 on feature/donchian-crypto-ladder (pushed).

Context: Gate A's four blocking defects are repaired and independently accepted. They are
integrated into frozen commit ebada020 on branch codex/gate-a-integration (pushed, clean).
BOTH platform floors are closed. Windows: 1359 passed, 1 warning. Locked Linux, executed on
GATEA-STAGING: candidate 2 failed / 1357 passed versus parent 637307e8 25 failed / 1281 passed,
with ZERO new failure node IDs and 23 failures fixed; the 2 survivors are the known Python 3.12
order-state GC assertions present on the parent too. The deployment artifact was rebuilt exactly
once from that SHA into C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9\
(RELEASE_SHA ebada020..., manifest SHA-256 8FC30864...4700C9, 7059 entries), and its five
deploy/linux/*.sh carry zero CR bytes, so the defect that failed Gate A at A-2 is absent.

D025 audit state: GLM-5.2 round 1 returned BLOCK for an environmental reason (its session could
not execute). Round 2, with owner-granted permissions, executed and returned
PASS-WINDOWS-ONLY-WITH-NITS with ZERO required findings.

THE SINGLE REMAINING BLOCKER is the second flagship audit: Codex gpt-5.6-sol xhigh on ebada020.
Its prompt is already written at
MTC_COMMAND_CENTER/11_TRIAGE/CODEX_GATE_A_INTEGRATION_AUDIT_PROMPT_EBADA020_2026-08-03.md.
Nothing else stands between the project and restarting Gate A at A-0.

D025 is NOT to be relaxed or changed. Two flagships are required. Do not substitute a third
GLM round, a Lead opinion, or an owner waiver for the Codex audit unless Baris says so in writing.

I authorize you to continue autonomously through the ordered queue below. Verify every claim
yourself against the repository, the filesystem and real logs before relying on it — the previous
session's transcript is not evidence.

1. Evidence gaps: FIVE OF SIX ARE CLOSED. The only one left is the second flagship audit (1d).
   a. DONE 2026-08-03 — locked-Linux floor executed on GATEA-STAGING. Candidate ebada020
      "2 failed, 1357 passed" vs parent 637307e8 "25 failed, 1281 passed": ZERO new failure node
      IDs, 23 fixed, the 2 remaining are the known Python-3.12 order-state GC assertions present on
      the parent too. Logs C:\tmp\LINUX_FULL_EBADA020_LEAD_2026-08-03.log and
      C:\tmp\LINUX_FULL_PARENT_637307E8_LEAD_2026-08-03.log.
      HOST ACCESS, already recovered — do not re-derive it: 172.24.55.233, user gatea, identity
      C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519. Run suites with the host-locked venv
      /opt/mtc-bridge/venvs/a1dd5b46.../bin/python (pytest 9.1.1, root-owned read-only — install
      nothing). Never touch KVM2. Never read or copy key contents.
   b. DONE except its Linux line — 11_TRIAGE/GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md
      already records the merge structure, the nine-file scope, the single test_wal_state_bundle.py
      conflict with before/after and justification, the ledger LF refresh, and the Windows floor.
      Fill in its §7 Linux row once 1a produces a real log. NEVER commit to
      codex/gate-a-integration — its head must stay equal to the artifact's build SHA ebada020.
      Records go on feature/donchian-crypto-ladder.
   c. DONE 2026-08-03 — artifact identity + secret-scan record is written at
      11_TRIAGE/GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md. Manifest hash
      recomputed and matching, nine-category content-redacted scan = 0 hits, built payload shell
      scripts = 0 CR bytes. Re-verify it rather than redoing it.
   d. THE ONLY REMAINING BLOCKER. GLM-5.2 has finished: round 1 BLOCK (environmental — its session
      could not execute), round 2 with granted permissions returned PASS-WINDOWS-ONLY-WITH-NITS
      with ZERO required findings, independently reproducing 1359 passed, the artifact identity,
      the absence of the A-2 CR defect, and manifest internal consistency.
      STILL OWED: the second flagship gpt-5.6-sol xhigh audit of ebada020. Run it and ebada020 can
      be accepted. THE PROMPT IS ALREADY WRITTEN — use
      MTC_COMMAND_CENTER/11_TRIAGE/CODEX_GATE_A_INTEGRATION_AUDIT_PROMPT_EBADA020_2026-08-03.md,
      not C:\tmp\glm_round2_prompt.md (that one is addressed to GLM and carries a GLM-specific
      round-2 preamble). Detached worktree C:\GAAUD_INT_GLM is at ebada020 and clean; reuse it.
      Launch Codex only via C:\Users\BarısSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1
      (default -Account secondary). Before dispatching, confirm C:\GAAUD_INT_GLM is a trusted
      directory for that session: Codex CLI has repeatedly run sandbox: read-only and refused every
      command as blocked by policy outside a trusted project dir, which is not a quota problem and
      has already caused Gate A auditor BLOCKs.
      LAUNCH RULE: glm.ps1 creates a fresh empty CLAUDE_CONFIG_DIR per run, so an unmodified GLM
      session has no permissions and no approver and will always D025-BLOCK. Launch any GLM audit
      with an explicit permissions mode plus --add-dir for what it must read.
      Record: 11_TRIAGE/GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md.
   e. DONE 2026-08-03 — GATEA-STAGING verified live: gatea-staging, Ubuntu 24.04.4 LTS,
      Python 3.12.3, SQLite 3.45.1, reachable at 172.24.55.233.
   f. SETTLED — Barış accepted the artifact doc drift on 2026-08-03 (option a). The artifact ships
      without deploy/linux/SECURITY_BASELINE.md and 11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md.
      No rebuild. ebada020 stays the frozen build SHA. Do not reopen this.
2. Only after 1a-1d hold, transfer the frozen artifact as a single tar (never as loose files) and
   run Gate A from A-0 through A-9 per
   GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md as amended by
   GATE_A_PREREGISTRATION_ADDENDUM_A_2026-08-02.md. Stop at the first FAIL, as the runbook
   requires, and write GATE_A_RESULT_2026-08-03.md either way.
3. Write the outcome into _AI_MEMORY/GLOBAL_HANDOFF.md and NEXT_STEPS.md, and push the branches.

Hard stop — do not do any of these without a new explicit instruction from me: merge to master,
WP-V / deployment, service or runtime changes, credential handling, broker or exchange access,
ARM, orders, TESTNET, mainnet, KVM2, Pine/parity/MTC/trading changes, or any economic action.
```

---

## Facts the new session must not have to rediscover

### Records baseline

All records referenced here are committed and pushed at **`ba228339`** on
`feature/donchian-crypto-ladder`. That is the docs line — `_AI_MEMORY` and `11_TRIAGE` records are
committed there, never on `codex/gate-a-integration`.

### GATEA-STAGING access — already recovered, do not re-derive

| Item | Value |
|---|---|
| Host | `GATEA-STAGING`, verified `gatea-staging`, Ubuntu 24.04.4 LTS |
| IP | `172.24.55.233` |
| User | `gatea` |
| Identity file | `C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519` |
| Source of truth | recorded verbatim at `CODEX_TAKEOVER_HANDOFF_2026-08-02.md:125` |
| Runtime | Python 3.12.3, SQLite 3.45.1 — the locked runtime |
| Suite interpreter | `/opt/mtc-bridge/venvs/a1dd5b467b12421f632bf3d8462a7244b39b2287/bin/python`, pytest 9.1.1 |

There is no `~/.ssh/config`. `~/.ssh/` holds only `hostinger_kvm2`, which is **KVM2 — forbidden, do
not touch**. The host venv is root-owned and read-only: **install nothing, modify nothing.** Never
read, print, copy, rotate or modify key contents. `python3` on the host has no pytest — use the
locked venv path above or you will get `No module named pytest`.

### Persisted evidence logs

```
C:\tmp\LINUX_FULL_EBADA020_LEAD_2026-08-03.log        candidate  2 failed, 1357 passed
C:\tmp\LINUX_FULL_PARENT_637307E8_LEAD_2026-08-03.log parent    25 failed, 1281 passed
C:\tmp\gatea_integration_windows_full_ebada020.txt    Windows  1359 passed
C:\tmp\GLM_AUDIT_INTEGRATION_EBADA020_2026-08-03.txt        GLM round 1 (BLOCK)
C:\tmp\GLM_AUDIT_INTEGRATION_EBADA020_ROUND2_2026-08-03.txt GLM round 2 (PASS-WINDOWS-ONLY-WITH-NITS)
```

`C:\tmp\gatea-integration-linux-full-ebada020.log` is the deliberate bare-`git archive`
falsification run. **Never cite it as candidate evidence.**

### Refs (re-verify, do not trust)

```
origin/master                          637307e8   (unchanged; nothing Gate A is merged)
codex/gate-a-integration               ebada020   <- the frozen integrated candidate
codex/gate-a-3b-shm-validation         20de117f   (product 7aad0377)
codex/gate-a-build-determinism         0bdf8cf4   (product 82e92c98)
codex/gate-a-credential-free-disarmed  a0275b5c   (product 17402a58)
codex/gate-a-residual-evidence-tests   3121e7c7   (product ebb750da)
codex/gate-a-overnight-report          b5a48e6f
```

Local `master` in the main checkout is stale at `8721bce0` (78 behind, clean ancestor). Resolve
`origin/master`, never local `master`.

### Worktrees

- `C:\GATEAINTEGRATION` — `codex/gate-a-integration`, clean. Work here.
- `C:\LAB\Tradingview_LAB_CLEAN` — main checkout, branch `feature/donchian-crypto-ladder`. This is
  where `_AI_MEMORY` and `11_TRIAGE` docs are committed. It is **not** an ancestor of
  `origin/master`; that is expected for the docs line.
- 16 unrelated pre-existing dirty worktrees (`C:/KVM2*`, `C:/TSP100*`, `C:/LAB/MTC_AIONUI_PILOT`,
  `C:/CDXFAILOVER`) are outside this scope. Leave them alone.

### Artifacts

- **Current:** `C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9\` — manifest
  `8FC30864BA342E53DCFC6B2938124F91D005F02671A332580A723F38FD4700C9`, 7059 entries.
- **Superseded, do not reuse:** `C:\WPI_ARTIFACTS\1adf9ae5…\` (manifest `bfefea2f…`) — this is the
  artifact that FAILED Gate A at A-2 on 2026-08-02.

### Traps already paid for once

1. **Bare `git archive` on Windows converts to CRLF** and reproduces the original A-2 failure. The
   accepted build contract is `git -c core.eol=lf archive`. Verify zero CR bytes in
   `deploy/linux/*.sh` after every export, before transfer.
2. **A `.gitattributes` rule does not retroactively renormalise an already-checked-out file.** The
   ledger path had to be refreshed through Git's filters explicitly.
3. **Transfer as one tar, not 7,000 files** — that is what made A-0 pass on 2026-08-02.
4. **An auditor that cannot execute the suite must BLOCK** (D025). A non-executing PASS is not
   evidence.

### Roster note

Acceptance of the four source lines used Barış's explicit **no-Claude owner waiver** while Claude
was quota-blocked; executing verdicts came from `gpt-5.6-sol` xhigh and GLM-5.2. If a Claude
retrospective audit is wanted on the integrated SHA, it is a separate owner decision, not a
blocker recorded anywhere.

Launch Codex only via `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1`
(default `-Account secondary`).

### Budget warning

≈33–36 h of the 50-hour plan are estimated spent, ≈14–17 h remain, exact booking deferred to Lead
Gate-7. WP-A (3 h), WP-R (6 h) and WP-V (8 h) are all still ahead and total 17 h. **Re-plan before
committing to the remainder** — the Gate A repair queue was unbudgeted work.
