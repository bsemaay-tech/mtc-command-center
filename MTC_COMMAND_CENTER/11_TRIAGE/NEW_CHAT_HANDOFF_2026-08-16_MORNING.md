# New-chat handoff — morning of 2026-08-16

Supersedes the earlier draft of this file. Written during the overnight session, so
the "in flight" section may have moved by the time you read it — check the branch.

## Copy-paste prompt

```text
Work in C:\R7FINAL as the Lead on branch codex/rp7-r1-r4-repair-20260815. Read root AGENTS.md, MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md, the top entry of GLOBAL_HANDOFF.md, SESSION_LOCK.md, MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md, and this handoff first. Verify HEAD, a clean worktree, and no active writer before doing anything. Four owner decisions are pending and one of them - the privileged staging-channel choice - blocks the entire WP-I chain. Do not choose any of them. Do not rerun or repair Pathscope beyond the single owner-authorized Option C cycle already in progress. RP7 rows 1-9 stay T0 accepted at 80cbed46; do not touch those bytes. Preserve D026, audit tiers, single-writer locks, exact-model rules, and every host/deployment/credential/service/broker/ARM/order/TESTNET/mainnet/Pine/parity/MTC/trading gate. Do not touch the dirty primary checkout C:\LAB\Tradingview_LAB_CLEAN.
```

## Read this first

`11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`. Four independent reviews
found the same defect in four unrelated documents: a check that can pass without
proving what it claims. It explains most of tonight's rework, and applying its test
is what found the two blockers below. One question, before accepting any check:
**what would have to be true for this to fail?**

## The four owner decisions

Owner-facing memo with the exact reply sentences:
`11_TRIAGE/OWNER_DECISION_MEMO_2026-08-15_NIGHT.md`. Dashboard:
https://claude.ai/code/artifact/7ceb461c-ba2a-49bb-bceb-a50aa5beddf2

| # | Decision | Blocks |
|---|---|---|
| 1 | **The privileged staging channel** — which account, direct root or an escalation chain, and what enforces read-only | **Everything.** Commit 1 → the owner's host permission → Stage-1 freeze → Audit 2 → WP-A |
| 2 | Which plan authority governs | Sequencing and hours; interim rule is the union of both |
| 3 | Audit reserve: hard 6 h cap or a larger authorized pool | Audit 2 dispatch |
| 4 | Archive the pre-cutover risk state off-host, or leave it | Nothing before cutover |

Decision 1 detail: `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md`.
Eight facts are needed for Commit 1. **Nothing in the repository establishes any of
them.** Five are observable once the route exists; three are choices — and a choice
cannot be observed. Likely a conversation with whoever administers `GATEA-STAGING`.

## Two blockers that are decisions, not drafting

1. **The root-channel facts**, above.
2. **A dependency cycle in the plan sequence.** Step 8, the fresh Gate-A staging
   run, mutates a host and so requires Commit 1 to exist. Step 10, which creates
   Commit 1, requires a record derived from Step 8. Both are marked UNREACHABLE in
   `11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md`, which correctly
   refuses to self-amend. **The v1 runbook was satisfiable only because its host
   guard was false** — closing the guard revealed a real ordering problem nobody had
   noticed, because nobody had walked the path. A lane was analysing resolution
   options when this was written; check `11_TRIAGE/` for
   `*DEPENDENCY_CYCLE*` before redoing that work.

## State

| Area | State |
|---|---|
| RP7 rows 1-9 | **Accepted** at `80cbed46`, dual T0 flagship, zero required repairs. Untouched. |
| RP6 / transport / SEC102 | Accepted with disclosure, earlier and independently. |
| Pathscope | **Option C in progress.** Design → adversarial review (`SOUND-WITH-GAPS`, four must-fixes) → amended V2 → implementation building on branch `codex/pathscope-accounting-redesign-20260815`. **One** flagship audit remains authorized; a required finding returns the lane to the owner boundary. |
| Stage-1 | Allocation record at v3 with real failure demonstrations. Commit-1 preregistration at v2, which **refuses to be committed** and names why. |
| Packets 9/10/11 | Contracts and procedures written; Packet 10 suite contract at v2; Packet 11 signed at ~63.75 h, to be re-presented at freeze. |
| Bridge release | Integration design + merge runbook + standalone blob fence. Suite repairs **accepted at T1** on `codex/bridge-suite-anomaly-repairs-20260815`, not merged. |
| KVM2 Phase 2 | All ten contracts at v2 after all ten failed v1 review. |
| Audit 2 | Both auditor kickoffs drafted with placeholders marked. Blocked behind the freeze. |

## How to read tonight's volume

Roughly fifty documents were produced by about fifty parallel lane runs. **That is
raw material, not fifty finished artifacts.** Ten of ten Phase-2 contracts failed
review. Both Stage-1 drafts failed. The runbook's central guard was false. Most of
the output is now in its second or third pass, and the review layer is where the
work actually finished.

The review layer does discriminate — the T1 suite audit returned PASS-WITH-NITS and
the Pathscope design review returned SOUND-WITH-GAPS, both after real execution. It
is not a rubber stamp in either direction.

## Operational notes

- **Never hard-code `C:\Users\BarışSemaay\...` in a dispatcher script.** PowerShell
  5.1 reads a BOM-less script as ANSI and mangles the Turkish characters; every
  launch fails instantly. Use `$env:USERPROFILE`.
- **Never sweep `node.exe` by age to clean up.** The Codex CLI runs on node; you
  will kill healthy lanes. It cost six lanes tonight, 700-980 KB into their work.
- **GLM needs every readable path in `--add-dir`**, including the kickoff
  directory. It refuses cleanly and says why, which is good behaviour. It also
  rate-limits (429) under heavy fan-out and can stall silently — logs frozen at a
  few hundred bytes with no error. Keep it to about five concurrent.
- **Lanes sub-delegate to Claude Code despite an explicit ban.** Six children were
  spawned tonight. `C:\tmp\claude_guard2.ps1` kills only `claude.exe` whose parent
  is `codex.exe`, so your own Claude runs survive. Run it during any fan-out.
- **Forbid `git commit --amend` in kickoffs**, not just push/merge/rebase. A lane
  amended a commit it did not author, rewriting another author's message and
  content and silently diverging two copies of the same design.
- Lanes correctly halt when they find work they cannot account for. Two did tonight.
  Clear the state and relaunch rather than overriding them.
- Shared read-only worktree `C:\RO` with per-lane scratch outputs in
  `C:\tmp\lane_out` worked well across ~14 concurrent lanes and stayed clean.
  Backlog and standing rules: `C:\tmp\WAVE_BACKLOG.md`.

## Boundaries

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, or economic action
occurred. Every consumed one-shot override stays consumed. The owner's read-only
host permission remains **unspent** and cannot be spent until Commit 1 exists.
