# Paste this as the first message of the next Claude Code session (project C:\LAB\Tradingview_LAB_CLEAN)

You are the P0 Claude Lead, session 7. Owner = Barış (non-technical; English output; owner-facing times in UTC+3; you run tools for him).

Read, in this order, before doing anything: (1) your memory `MEMORY.md` head and `p0-claude-lead-session-2026-09-16-day` (Wed→Sat sections) plus the permanent lessons `review-lane-mutant-armed-a-live-tool`, `partial-read-is-not-a-measurement`, `red-evidence-on-the-pinned-interpreter`; (2) `C:/tmp/CLAUDE_P0_RUN_20260913/HANDOFF_20260919_SESSION7.md` (copy in `%TEMP%\CLAUDE_HANDOFF_20260919_P0_SESSION7.md` and CT13); (3) the tails of `C:/tmp/CLAUDE_P0_RUN_20260913/RUN_STATE.md` and `C:/tmp/OPUS_QUEUE_20260916/QUEUE_LOG.txt`. Then `ListAgents` + mtimes to make sure no other Lead session is alive.

Standing rules are binding (section 1 of the handoff): no host contact, no deploy, no trading, no mainnet actions, no spend beyond subscriptions, no git and no shell cwd inside any worktree while `agy.exe` runs, guard PASS before every commit with exact staged paths, the Lead never accepts its own code, the DD-06 lane SAFETY RULE, RED evidence on the pinned interpreter.

Do, in this order:
1. Lane 4 (P0-26 slice read) is done: PASS-WITH-NITS, adjudicated in `P026/LEAD_ADJUDICATION_P026_NIT_T0.md`; the owner has one open one-liner `P26-EVID A|B` (default B).
2. Repair the P0-30 NIT slice per `OPUS_QUEUE_20260916/P030/LEAD_ADJUDICATION_P030_NIT_T0.md` (F-1: derive the nesting depth at test time, one arm per layer, RED on BOTH the pinned Python 3.12 venv and 3.14; F-2 guard the adapter's third parse site; F-3 receipt-side race arm; F-4/F-5), correct the record, Gemini delta, exact-Opus re-read (lane 3 attempt 5). If it cannot land before 18:47, re-pin lane 3 to `45a7f50e` for Sol.
3. Sat 18:47 local: Codex/Sol reset → `make_sol_lane.ps1` per handoff section 4 (P031 → P1CAP → P030 → P026 → P021S1 → DD06 (SAFETY RULE in the brief) → P012INTAKE → P0-20 record → P027CI retrospective); adjudicate each; record to CT13 in waves; keep the handoff and memory current.
4. Only after those: the drafted P0-12 capture-tool NIT slice (`P1CAP_NIT_SLICE_PREP_20260918/`, unapplied), then the P0-21 S1 / P0-31 semantic / P0-12 intake NIT slices as the handoff lists.

Report to the owner in plain English: what finished, what is left per package, and anything that needs him (currently only `P26-EVID A|B`, not urgent; the DD-06 probe run r4 needs his separate word later, after the execution documents are re-issued).
