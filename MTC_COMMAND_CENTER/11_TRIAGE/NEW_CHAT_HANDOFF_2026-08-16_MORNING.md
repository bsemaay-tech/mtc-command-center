# New-chat handoff — morning of 2026-08-16

## Copy-paste prompt

```text
Work in C:\R7FINAL as the Lead on branch codex/rp7-r1-r4-repair-20260815. Read root AGENTS.md, MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md, the top entry of GLOBAL_HANDOFF.md, SESSION_LOCK.md, and MTC_COMMAND_CENTER/11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-16_MORNING.md first. Verify HEAD, a clean worktree, and no active writer before doing anything. Three owner decisions are pending and every WP-I lane is stopped behind the first of them: the Pathscope Option A/B/C/D choice, the narrow read-only host-and-credential confirmation, and the Packet 11 ledger signature. Do not choose any of them yourself, do not rerun or repair Pathscope, and do not treat any consumed one-shot override as reusable. RP7 rows 1-9 stay T0 accepted at 80cbed46 - do not touch those bytes. Preserve D026, audit tiers, single-writer locks, exact-model rules, and every host/deployment/credential/service/broker/ARM/order/TESTNET/mainnet/Pine/parity/MTC/trading gate. Do not touch the dirty primary checkout C:\LAB\Tradingview_LAB_CLEAN.
```

## Simple dashboard

Owner-facing version, plain language:
https://claude.ai/code/artifact/7ceb461c-ba2a-49bb-bceb-a50aa5beddf2

| Area | State | Plain-language meaning |
|---|---|---|
| RP7 rows 1-9 | **GREEN — accepted** | Dual T0 flagship acceptance at `80cbed46`, zero required repairs. Untouched tonight. |
| RP6 / transport / SEC102 | **GREEN with disclosure** | Owner-accepted earlier. Independent of the RP7 acceptance; do not attribute them to it. |
| Pathscope | **RED — owner boundary** | The authorized retry executed and returned REQUEST_CHANGES with three REQUIRED findings. Lane stopped. Four options priced. |
| Freeze gate 2 | **AMBER — one item** | Pathscope is now the only open sub-item. Everything else in gate 2 closed. |
| Host authority | **RED — newly surfaced** | The written grants conflict; under the narrower reading the read-only staging capture cannot proceed without one new owner sentence. |
| Packet 10 | **AMBER — measured** | Suite is `2 failed, 1019 passed` at `ddc8a9c8`, both root-caused, repairs prepared on a branch. Still needs the frozen-SHA run in the locked environment. |
| Packet 11 | **AMBER — awaiting signature** | ~63.75 h measured with reproduction commands. Refresh the figure at the real freeze checkpoint before signing. |
| Bridge release | **AMBER — designed** | The Gate-A accepted candidate is stranded outside master. Integration route chosen, 21-41 labor hours, nothing executed. |
| Stage 1 / Audit 2 / WP-A | **BLOCKED** | Behind decisions 1 and 2. |

## The three owner decisions

Exact sentences are in
`AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md` §3.

1. **Pathscope disposition** — one of Options A/B/C/D in
   `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md`. Lead
   recommends **C**, the accounting-layer redesign, because three prior
   shape-recognition repairs each closed their named findings and each failed the
   next sweep. Blocks Stage 1, Audit 2, WP-A.
2. **Narrow host-and-credential confirmation** — G1/G3/G6 authorize read-only
   contact with `GATEA-STAGING`, but the same source records that credential load
   was *not* granted and the transport plan needs a pinned SSH identity. Under
   the narrower reading those grants cannot be spent. Blocks grant-#6 capture,
   WP-I ops 01-12, Packet 9 host evidence, WP-I closure.
3. **Packet 11 ledger signature** — after the figure is refreshed at the real
   freeze checkpoint. The current candidate is ~63.75 h.

Two further decisions belong to the deploy stage, not to WP-I: the KVM2-specific
TESTNET wallet, and the risk-state continuity policy at cutover.

## What happened on 2026-08-15 evening

- **Pathscope retry executed.** First audit of these bytes to actually run the
  mandated suite; header confirmed `sandbox: danger-full-access`. REQUEST_CHANGES,
  three REQUIRED findings (F1 command text and URI/list members with zero terminal
  accounting; F2 provenance laundered across members; F3 duplicate/empty collapse),
  no nits. Lane stopped per the owner's standing instruction.
- **The 2026-08-14 audit contract was unsatisfiable** — it mixed Git-object and
  working-tree identities. Corrected to a dual-form table; the retry reproduced
  both forms exactly. Same ambiguity independently caused Packet 10 anomaly A1.
- **Packet 10 baseline** measured twice, both anomalies root-caused; repairs
  prepared on `codex/bridge-suite-anomaly-repairs-20260815` (`6c746b65`) and
  **accepted at T1** — Claude `claude-opus-5` returned PASS-WITH-NITS, four nits,
  zero required, at `7d4e9a96`. Not merged. Lead disposition:
  `BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md`.
  **Operational catch from NIT-1:** the `ledger_schema.json` blob is unchanged
  between base and repair, so an existing Windows checkout that only fetches this
  commit keeps its stale CRLF copy and the failure recurs. `C:\P10BASE` is in that
  state now. After taking the commit into any existing Windows checkout, run once:
  `git checkout -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json`
- **Packet 11** measured with reproduction commands.
- **Freeze map reconciled** — gate 2 open only on Pathscope.
- **Authority consolidated** — closes dispatcher question 7 and surfaced decision 2.
- **Deploy path priced** — 55-105 hands-on hours to a first DISARMED KVM2 start.
  Two schedule-moving facts: the Gate-A accepted candidate `2ce41e34` is not in
  `origin/master`, so its A-0..A-9 pass cannot transfer; and the deployment gate
  is step 9 of the canonical sequence, downstream of WP-I, Audit 2, WP-A and
  Audit 3, not a parallel track.

## Operational notes for the next Lead

- **Put the no-sub-delegation clause in every Codex kickoff, and run the guard.**
  Dispatched lanes spawned Claude Code children six times tonight, four of them
  *after* the clause was added. `C:\tmp\claude_guard2.ps1` kills only
  `claude.exe` whose parent is `codex.exe`, so your own Claude CLI runs survive.
- Codex routes `secondary`, `free` and `fourth` were all authenticated and usable
  tonight; `--dangerously-bypass-approvals-and-sandbox` is required or the lane
  silently gets `sandbox: read-only`.
- Lane worktrees created tonight and still present: `C:\PSRETRY`, `C:\P10BASE`,
  `C:\P11LED`, `C:\BRDG`, `C:\FRZMAP`, `C:\AUTHCON`, `C:\RELDES`, `C:\P10FIX`.
  All are detached at `ddc8a9c8`/`678d4be2` except `P10FIX`, which holds the
  repair branch. Prune the read-only ones when convenient; keep `P10FIX`.

## Boundaries

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, or economic action
was authorized or performed. Every consumed one-shot override stays consumed.
