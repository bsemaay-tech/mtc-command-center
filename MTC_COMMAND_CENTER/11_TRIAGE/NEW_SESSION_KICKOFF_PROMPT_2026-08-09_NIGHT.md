# NEW-SESSION KICKOFF PROMPT (paste this into a fresh Claude session verbatim)

> Maintained by the night Lead at each milestone. If the running session dies (model
> drop Fable→Opus, crash, sleep), paste the block below into a new session as the
> first message. It is self-contained.

---

Continuous autonomous Lead session, overnight, repo `C:\LAB\Tradingview_LAB_CLEAN`,
branch `feature/donchian-crypto-ladder`. You are the SINGLE WRITER — before any
dispatch, verify no other live Claude/Codex writer session is driving the staging
pipeline.

Read in order (all under `MTC_COMMAND_CENTER/`):
1. `11_TRIAGE/STANDING_AUTONOMY_AUTHORITY_2026-08-09.md` — BINDING: never idle on
   reversible/in-repo work; repair cycles auto-continue past round 3 on narrow
   survivors; no AskUserQuestion for reversible repo decisions; delegate all heavy
   work (Claude Max implement, Codex xhigh audit, GLM review, DeepSeek mechanical);
   spend Max credits to converge. HARD GATES owner-only: host mutation, running any
   block against a real host, credentials, ARM, orders, broker, TESTNET/mainnet,
   master merge, WP-V/KVM2, payload-archive deletion.
2. `_AI_MEMORY/GLOBAL_HANDOFF.md` newest section + `_AI_MEMORY/NEXT_STEPS.md` top
   section — live state and pick-up points.
3. `11_TRIAGE/OVERNIGHT_HANDOFF_2026-08-09_STAGE3.md` §STANDING RULES + §Operating
   rules (delegate invocation syntax lives there: Invoke-ClaudeMax.ps1 /
   Invoke-CodexForClaude.ps1 -Account secondary / Invoke-GlmAudit.ps1).
4. `11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/06_B3_REPAIR/` — the
   B3 repair cycle unit (rounds, audits, cycle record with owner authorizations).

Then: set up a self-paced /loop (5–10 min checks, re-arm before every wait), verify
`powercfg` sleep=0 AC+DC, and continue the pipeline from wherever
`_AI_MEMORY/NEXT_STEPS.md` top section says it stands. Commit+push exact file sets at
every checkpoint (repo guard first; never `git add .`). English only. End every
response with numbered next steps + a chosen default path; owner-asks in plain
language. Morning ~06:30: summary + push notification. Update
`_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`, and THIS file at every
milestone so the next fresh session resumes cleanly.

---

## Milestone log (newest first — update on every milestone)

- 2026-08-09 ~23:10: round 6 consumed + committed (`3a358ffa`). Section 4 now literally
  paste-and-run (absolute `B`, `QA="$(mktemp -d)"`, helpers+preludes restated inline);
  code freeze re-verified by `cmp` on all three files. FINAL auto-round audit 6
  dispatched (`be5qijups`) — it must paste-and-run the blocks itself. On PASS → B3
  repair ACCEPTED → Stage 1B runkit re-freeze → WP-L P2 unit closure. On same-class
  BLOCK → escalate to owner (do NOT open round 7); the kickoff asks the auditor to
  classify the residue as document-fixable vs inherent MSYS/D026 limit.
- 2026-08-09 ~22:55: audit 5 BLOCK, converging — code+arithmetic PASS, sole survivor
  = section-4 SELF_QA setup block not copy-paste runnable. Tight doc round 6 dispatched
  (Max, `b4ld284dy`) to make it runnable; code hash-frozen. Committed `158bb953`.
  CONVERGENCE STOP: if audit 6 BLOCKs again same-class → escalate to owner (MSYS
  literal-D026 tooling limit), do NOT auto-round 7. On PASS → Stage 1B re-freeze.
- 2026-08-09 ~22:40: round 5 consumed + committed (`fd193857`). Code freeze verified
  by cmp/hash (RP1-B3 `6f3ea022`, RPD-VERIFY `3b9e78e8`, DESIGN_NOTES byte-identical);
  only SELF_QA.md rewritten. Narrow Codex doc re-audit 5 dispatched (`audit5/`). Next:
  on PASS the whole B3 repair is accepted → Stage 1B runkit re-freeze (repaired
  RP1-B3 + new RPD-VERIFY → new BLOCK_IDENTITIES → new runkit.tar via a re-run of the
  Stage 1 builder pointed at the round5 blocks) → WP-L P2 unit closure record.
- 2026-08-09 ~22:30: audit 4 = code CLOSED (finding 1), sole survivor is DOC-only
  (finding 2, SELF_QA exact-command recording). Per standing authority = narrow
  doc/QA survivor → auto-continue, NOT owner escalation. Doc-only round 5 dispatched
  to Max (task, rewrites round5/SELF_QA.md only; code files pre-copied byte-identical,
  hash-enforced). Committed `d5f0177e`. Next: consume round 5 → verify code hashes
  unchanged (RP1-B3 `6f3ea022`, RPD-VERIFY `3b9e78e8`) → narrow doc re-audit → on
  PASS Stage 1B re-freeze.
- 2026-08-09 ~22:15: B3 round 4 consumed + committed (`04eddf90`); diff vs round 3 =
  exactly the two fixes (read-error STOP in both blocks; D026 QA). Narrow Codex
  closure audit 4 dispatched. Next: on PASS → Stage 1B runkit re-freeze (repaired
  RP1-B3 + new RPD-VERIFY → new block identities → new tar) → WP-L P2 unit closure.
- 2026-08-09 ~22:05: GLM WP-I draft review integrated as round 1.1 (F1
  interpreter-exec STOP added to rows 18/19 + preflight; N1 reused-script
  disposition; N2 listener wording; SELF_QA addendum). B3 round 4 (Max) still in
  flight — next: consume it → narrow Codex closure audit → Stage 1B re-freeze.
- 2026-08-09 ~21:50: GLOBAL_HANDOFF + NEXT_STEPS updated; B3 round 4 (Max) and GLM
  WP-I draft review both in flight. Next: consume round 4 → narrow Codex closure
  audit → Stage 1B re-freeze on PASS.
- 2026-08-09 ~21:35: owner authorized bounded B3 round 4 in-session; dispatched.
- 2026-08-09 ~21:15: B3 cycle BLOCK-at-round-3 recorded (`0020ee7f`); full-night
  record `b451b106`; prepared round-4 kickoff `9098cd12`.
- 2026-08-09 evening: Stage 3 B3 STOP adjudicated (`7e9d1c4a`); Stage 3B R4-5 PASS
  (`ee49a945`); backlog items 2–5 done (`f5c6eb25`, `3b4ba676`, `d8599764`).
