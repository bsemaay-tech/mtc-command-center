# FRESH-SESSION HANDOFF — WP-I run-kit, 2026-08-11 ~11:50 midday

Paste this whole file as the first message of a new session. Self-contained. Supersedes
`NEW_SESSION_KICKOFF_2026-08-10_EVENING.md` and `MORNING_HANDOFF_2026-08-11.md` for current
state; those remain the older record.

Repo `C:\LAB\Tradingview_LAB_CLEAN`, branch `feature/donchian-crypto-ladder`. You are the
Lead: orchestrate, verify, adjudicate, commit. You do NOT author or audit the heavy
artifacts yourself. Read in order: this file, then `AGENTS.md`, then
`_AI_MEMORY/START_HERE.md`, then the routing and defect-pattern files named below.

---

## 1. OWNER DECISIONS — 2026-08-11, BINDING, DO NOT RE-ASK

Full record: `OWNER_DECISIONS_2026-08-11.md`.

1. **§8.2 rows 1–9: BUILD ALL NINE.** Implemented as two new sections inside RP7-WPI-RO.sh
   (smallest correct shape). **Hard rule:** do NOT add them until RP7's current bytes hold
   two flagship acceptances — adding scope to bytes under audit accepts superseded bytes.
   Cost carried: +3–6 rounds, most likely 4.
2. **Ledger ratified** through 2026-08-11 morning: **~34.8 h used of 50, ~15.2 h remain**
   (`LEDGER_STATUS_2026-08-10.md`, ratification update). Next owner flag when <10 h remain.
3. **NIM/DeepSeek routing verdict** (owner asked): NIM cannot author (write-tool-dead through
   the wrapper — read/analysis only). DeepSeek can author a NARROW round only as last resort
   when GLM is also out, Lead verifying every byte; never as auditor, never for transport or
   a from-scratch block. Neither may fill the Codex/second-flagship slot — that forges the
   two-flagship guarantee.

Standing grants #1–#7 from the prior kickoff remain in force (host-contact authority, budget
lift, root for `RPD-VERIFY`, attestation option (a), T0 round-cap lifted for the block set).
Still hard-gated: credential load, ARM, orders, broker/exchange, TESTNET/mainnet, master
merge, WP-V/KVM2, host mutation beyond a run's own evidence tree.

---

## 2. ACCOUNT WINDOWS — measured 2026-08-11 11:43

| Slot | Account | State | Back |
|---|---|---|---|
| Codex flagship / analysis (both lanes) | Codex Pro `-Account free`, Codex Plus `-Account fourth` | **both LIVE** | — |
| Implementer + Claude flagship | **Claude Pro** default `.claude` | **WEEKLY cap hit** | **2026-08-12 23:00** (~1.5 days) |
| Implementer | **GLM-5.2** `Invoke-GlmTask.ps1` | 5h window spent | **13:50 today** |
| Emergency flagship | Claude Max `Invoke-ClaudeMax.ps1` | untouched | available |
| Last-resort narrow coder | DeepSeek `_deepseek_driver/ds_agent.py --task <f>` | live (~$2.90) | — |

**The bottleneck is implementer lanes.** With Claude Pro on a weekly cap, **GLM is the only
routine implementer** (Codex audits, cannot implement its own audit targets). Plan around
GLM's 5h windows; use both Codex lanes for audits + analysis continuously.

Dispatch patterns (verbatim):
- Codex: `$a=@('exec','--dangerously-bypass-approvals-and-sandbox','-m','gpt-5.6-sol','-c','model_reasoning_effort=xhigh',$short); & "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" -Account free -CodexArgs $a` (pass a short quote-free pointer to a kickoff file; Codex reads the file).
- GLM: `& 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GlmTask.ps1' -RepositoryPath 'C:\LAB\Tradingview_LAB_CLEAN' -TaskFile <kickoff> -PermissionMode acceptEdits -OutputReport <out>` — GLM gates execution, so it marks QA `PENDING-LEAD-EXECUTION` and the Lead runs the harnesses.
- Claude Pro: `claude --print <pointer> --model claude-opus-5 --effort xhigh --no-session-persistence --dangerously-skip-permissions`.

---

## 3. PER-ARTIFACT STATE — head commit is `da78d99c`

### RP7-WPI-RO.sh — round 8 accepted-with-5, round 9 kickoff banked
- Round-8 bytes `11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4`, 99903 B,
  commit `bb8546e6`.
- Cycle: r5 BLOCK-then-repaired → r6 BLOCK 4 → r7 BLOCK 4 → r8 **BLOCK 5**. Findings are
  narrowing; r8's repairs (descriptor binding, restored two-outcome assertion, withdrawn
  overclaim) were all confirmed real by the auditor.
- **NEXT: round 9** — kickoff `KICKOFF_RP7_REPAIR_R9.md`, five findings. The BLOCK one:
  `ro.status.body` is still an outside-tree write + false-PASS primitive; a disclosure is not
  a control; bind the fetched object to the created leaf. Needs an implementer lane (GLM or
  Claude Pro when back).

### RP6-P0.sh — round 10a partial preserved, round 10b pending
- **Partial** bytes `a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617`,
  107252 B, commit `da78d99c`. Claude Pro died on its weekly cap mid-round-10; the partial is
  syntactically clean and the whole fence set still passes (no regression) BUT has no report
  and F1–F4 are not confirmed closed. See `RP6_R10A_LEAD_NOTE_2026-08-11.md`.
- Round-9 review verdict was **REQUEST_CHANGES ×4** (`RP6_CODEX_T0_AUDIT_R9_2026-08-11.md`):
  F1 the published `R9_GRAMMAR` command never ran the harness; F2 grammar closure; F3
  malformed followed-target reaches rc 1; F4 an unreachable relabelled line.
- **NEXT: round 10b** — kickoff `KICKOFF_RP6_REPAIR_R10.md`. Confirm the F1 fix by running
  the published command VERBATIM, write the missing report, confirm F2/F3/F4. GLM at 13:50.

### Transport set — round 4 REBUILT, awaiting Codex re-audit (updated 2026-08-11, Max lane)
- Round 4 is complete: report `TRANSPORT_R4_REPORT_2026-08-11.md`, status
  `STATUS_TRANSPORT.md`, evidence `SELF_QA_TRANSPORT.md` §R4. All eight items (F1–F4,
  T5–T8) implemented with executed RED/GREEN; no `PENDING-LEAD-EXECUTION` item.
- The `cf049b6b` close-script edit was treated as SUPERSEDED per the Lead addendum; the
  rebuild started from the round-3 bytes at `78173bfd`. Its pieces are dispositioned
  individually in §3 of the report (kept/dropped, with a second latent defect recorded).
- Six `ssh_stdin` rows now carry a frozen `env -i` launch domain the runner enforces
  verbatim; ops 07/08 take the run-owned `<BASE>/work` root op 01 allocates; provenance is
  bound per operation; cleanup prerequisites are per branch, and Codex's decisive fixture
  goes GREEN (`deviant=1`, `TR_RUN FAIL`). `run_p0.sh` wires the five `P0_ATTESTED_*`
  values — proved against the real `RP6-P0.sh` gate bytes. `WPI_INTERPRETER_TARGET` is gone.
- **NEXT: Codex T0 re-audit** against the identities in §4 of the report. Two Lead items:
  ratify derivation classes 5 and 6, and accept the F1 residual scoping (a `BASH_ENV`
  startup plant that exits is closed on the plan/runner side, not inside a script).
- Nothing was committed; nothing was dispatched. `TRANSPORT_R4_MAX_RUN_2026-08-11.log` was
  held open by the dispatcher and could not be written by the session.

### §10.2 path-scope prover — unsound, repair banked
- Codex T1 → **REQUEST_CHANGES ×9** (4 CRITICAL silent-sink classes). Repair kickoff
  `WPI_PREREG_DRAFT_ROUND1/KICKOFF_PATHSCOPE_REPAIR_R2.md`.
- Design note `SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md`: even repaired it cannot close a
  block alone — needs one entrypoint-driven whole-program proof per stage, allocate→render→
  freeze order. This is new tooling, several rounds.

### Preregistration — assembly not started
- Skeleton review NEEDS-WORK ×13 (`SKELETON_REVIEW_CODEX_2026-08-10.md`); RUNID review
  NEEDS-WORK ×6 (`RUNID_MINTING_REVIEW_CODEX_2026-08-11.md`); §10.1 reconciliation (11 EXTEND
  + 3 unresolved, `SEC101_RECONCILIATION_CODEX_2026-08-10.md`); circular attestation order
  needs the two-commit fix. All must land in the successor preregistration before freeze.

---

## 4. FREEZE BLOCKER MAP — 10 items, none was known 2 days ago

1. RP6, RP7, transport each accepted by BOTH flagships — all three open.
2. Rows 1–9 built into RP7 (owner: ALL NINE) — after RP7 dual acceptance.
3. §10.2 prover made sound (repair banked).
4. §10.2 composite whole-program proof built (design accepted).
5. §10.1: 11 extensions + access-qualifier grammar; 3 families unresolved.
6. Attestation/preregistration/commit order de-circularised (two-commit fix).
7. `run_p0.sh` wires the five `P0_ATTESTED_*` inputs.
8. Close-script contract and bytes reconciled.
9. `REMOTE_BASE` allocated BEFORE the RO block is frozen.
10. Audit-2 readiness package refreshed (NEEDS-UPDATE ×20).

Only after all ten: Stage-1 freeze → host run (P0→RO→attestation→`RPD-VERIFY` as root) →
WP-I closure → Audit 2.

---

## 5. LESSONS THIS CYCLE PAID FOR — binding on the Lead

- **A disclosure is not a control.** A truthful note beside an unqualified claim leaves the
  claim false. RP7's `ro.status.body` residual proved this across three rounds.
- **Run the published command VERBATIM**, not a convenient extraction. RP6's `R9_GRAMMAR`
  command piped a harness into `bash --noprofile --norc "$mutant"`, so Bash ran the mutant
  file and ignored stdin — confident output from the wrong program. The Lead's extract-and-run
  had reported it green. Both forms now run; any disagreement is a finding.
- **A carried regression fence changes only with a per-change discriminating-power argument.**
  RP7 r7 weakened `rc 0` to `rc=[0-9]*` and justified it with a false claim about the old
  test. Verify every claim about old code by executing it.
- **Never credit an item as implemented on the strength of a comment claiming it.** Transport
  reported classes 5/6 done while the bytes stopped at their own launch check.
- **Verify a driving finding yourself before making it binding scope**, and don't stop at the
  first layer — Codex twice went deeper than the Lead's check on the same item.
- **Defect patterns are now 13** (`DESIGN_DEFECT_PATTERNS_2026-08-10.md`); numbering is frozen
  permanently. Patterns 11/12/13 (declared≠executed instrument; unmodelled-must-not-disappear;
  every-member-needs-a-disposition) predicted later findings.
- **Windows autocrlf:** never `git checkout` a block file; use `git cat-file blob <sha>:<p> > <p>`.
  Count CR with `tr -cd '\r' < f | wc -c`, never `grep -c $'\r'`.
- **Codex content filter** kills fixture-heavy RP7 reviews (~260–275k tokens). Split into
  narrow bands (grammar/ordering/evidence separate from interpreter/namespace/escape); the
  grammar bands complete, the fixture bands die. Not a prompt problem — it's the work product.
- **Commit exact file sets, never `git add .`.** Repo hook flips HEAD to master between calls;
  inline `git checkout feature/... && git add <paths> && git commit`.

---

## 6. STATE HYGIENE AT HANDOFF

- No agents running. Both Codex lanes free. Two partials are committed and labelled: RP6 r10a
  (`da78d99c`) and the concurrent session's transport edit (`cf049b6b`) — neither is accepted.
- Untracked noise in `git status`: `_r4_logic.py`, `_r4_selfqa_harness.ps1`, WPL_P2 evidence
  dirs, `tmprepo_map_inventory.md`, various `*_RUN_*.log`. None committed; safe to leave.
- **A four-hour idle gap happened overnight** (04:32→08:49) because wake timers weren't
  re-armed after the last round. If running autonomously, always schedule the next wake before
  ending a turn.

---

## 7. IMMEDIATE NEXT ACTIONS for the fresh session

1. At 13:50, dispatch **RP6 round 10b** to GLM (`KICKOFF_RP6_REPAIR_R10.md`).
2. Then **RP7 round 9** — needs an implementer; if GLM is busy on RP6 and Claude Pro is still
   capped, this waits, or DeepSeek takes it as a narrow last resort with full Lead verification.
3. Keep both Codex lanes on preregistration assembly: apply the 13 skeleton gaps, the 6 RUNID
   changes, the §10.1 reconciliation, and the two-commit ordering fix into the successor
   preregistration draft.
4. Transport round-4 rebuild is the largest remaining block — schedule a strong implementer
   lane for it, not DeepSeek.
5. End every response with numbered next steps + a chosen default; owner-facing asks in plain
   non-technical language. Book ledger time honestly; flag at <10 h remaining.
