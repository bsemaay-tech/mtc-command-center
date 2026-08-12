# Open questions for the Audit 2 dispatcher

Status: NOT READY FOR DISPATCH. [refreshed 2026-08-12]

[refreshed 2026-08-12] These are only the decisions or inputs that remain open for the
dispatching Lead. This readiness assembly makes no audit, acceptance, host, or authority
decision.

## Closed decisions - do not reopen at dispatch

- [refreshed 2026-08-12] **Audit roster:** Audit 2 is T0 and requires exactly two fresh,
  independent xhigh flagships: Claude `claude-opus-5` and Codex `gpt-5.6-sol`. GLM is not
  silently added. The former supplemental-versus-omitted question is CLOSED.
- [refreshed 2026-08-12] **Section 8.2 rows 1-9:** BUILD ALL NINE, only after RP7 has
  dual-flagship acceptance. Source: `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-11.md`.
- [refreshed 2026-08-12] **Section 10.1 FAM-01..03 / MC-01..03:** owner-ratified on
  2026-08-12. Source and implementation contract:
  `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`
  plus `LEAD_MC_ADJUDICATION_2026-08-11.md`. Frozen-composite implementation remains a
  freeze gate.
- [refreshed 2026-08-12] **Transport F1:** the outer SSH account-shell boundary remains
  honestly OPEN and is owner-ratified as accept-with-disclosure, not a freeze blocker.
- [refreshed 2026-08-12] **SEC102 interpreter vocabulary:** owner-ratified as a disclosed
  production-gate item, not an open static-tool defect.

## 1. How to keep the two flagship sessions independent

[refreshed 2026-08-12] Open operational choice: create two separate audit-only
worktrees at the same full frozen SHA, issue fresh standalone prompts, and seal both initial
verdicts before sharing either output. Record worktree path, `git rev-parse HEAD`, and empty
`git status --porcelain` before and after each session. A shared worktree or a second auditor
who sees the first verdict weakens independence and should not be selected.

## 2. Mandated suite command and exact baseline

[refreshed 2026-08-12] Open dispatch blocker: no authoritative freeze-time command,
counts, accepted anomaly IDs, or output signatures exist. Stop dispatch until all fields in
`AUDIT2_AUDITOR_SESSION_INPUTS.md` section 5 are pinned from one frozen-SHA source. Do not
infer the earlier two-failure description.

## 3. Final D026 map for current WP-I work

[refreshed 2026-08-12] Open dispatch blocker: the corrected older WP-L/B3 mappings are
present, but the complete current RP6, RP7, transport, SEC102, pathscope, and future rows
1-9 map is not. Require exact RED command/output, pre-fix or mutation identity, GREEN
command/output, and final accepted identity per closure test. Current audit REDs without
accepted GREEN remain open; helper-only or non-literal evidence remains supplemental.

## 4. Freeze-time ledger ratification

[refreshed 2026-08-12] Open dispatch blocker: the current record is about 40 h used of
50, explicitly an estimate requiring owner ratification. The owner waived the 10-hour
remaining stop gate on 2026-08-11 with honest booking; that waiver is not a freeze-time
ledger signature. Book remaining work and obtain one exact owner-ratified source.

## 5. Access to immutable transport and WP-I evidence at audit time

[refreshed 2026-08-12] Open operational choice after evidence exists: provide each
auditor an immutable read-only snapshot with exact root identity and recomputation
instructions, or separately authorize read-only access to the create-once roots. Copied
digest strings alone do not satisfy recomputation. No new access authority is created here.

## 6. Freeze identity and unchanged-bits statement

[refreshed 2026-08-12] Open dispatch blocker: generate the full pre-WP-A SHA,
base-to-freeze diff, frozen file list, candidate/artifact/manifest identities, and either a
verified unchanged-bits statement or an exact diff. Reusing a pre-freeze working-tree
description is not acceptable.

## 7. Final authority consolidation

[refreshed 2026-08-12] Open dispatch blocker: carry every existing WP-I owner grant and
hard exclusion into one final authority record, and separately identify any still-required
go/no-go. Technical interlocks, the budget-stop waiver, and this package do not substitute
for that record.
