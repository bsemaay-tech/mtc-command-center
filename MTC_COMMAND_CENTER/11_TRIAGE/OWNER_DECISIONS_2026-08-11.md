# Owner decisions — 2026-08-11 (Barış, in chat)

Two binding decisions and one routing question answered. Recorded here so the fresh session
treats them as settled, not open.

## Decision 1 — §8.2 rows 1–9: BUILD ALL NINE

Owner chose **all nine**, per the recommendation in
`WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md`.

Consequences now binding:
- Rows 1–9 are implemented as **two new sections inside RP7-WPI-RO.sh** (the smallest correct
  shape from the analysis, §D.1) — not a new block, not a new transport op, no RUNID churn.
- **Hard sequencing constraint:** rows 1–9 may NOT be added to RP7 until its current bytes
  hold **two flagship acceptances**. Adding scope to bytes under audit produces an acceptance
  of superseded bytes. So: finish the RP7 round cycle to dual acceptance first, THEN open the
  rows 1–9 addition as its own repair-and-review sequence.
- Honest cost carried into every estimate: **3–6 further repair-plus-two-flagship rounds,
  most likely 4**, on top of RP7's current path.
- All nine are read-only, none needs root, the ten pinned tools suffice (§C).
- Freeze remains blocked until rows 1–9 are implemented and accepted, OR — not chosen — were
  formally deferred. Deferral is off the table; build is the decision.

## Decision 2 — ledger: the unratified time is RATIFIED

Owner ratified the ~10 h of previously unsigned ledger time (the ~4.4 h booked for
2026-08-10 daytime plus the overnight/ morning orchestration since). Update
`LEDGER_STATUS_2026-08-10.md` accordingly; the balance is now owner-signed through
2026-08-11 morning. Continue booking honestly; flag again only when the remaining balance
against the 50 h ceiling drops below 10 h.

## Routing question answered — can NVIDIA / DeepSeek fill coder or Codex-auditor slots?

Owner asked whether NVIDIA NIM and DeepSeek can be used as implementer ("coder") and as the
Codex-auditor slot while Claude Pro is on its weekly cap (out until 2026-08-12 23:00).

**As the Codex / second-flagship auditor slot — NO.** The two-flagship T0 contract exists
because the two flagship families have different blind spots; the single biggest find of the
whole project (the venv-interpreter hole that survived three Claude rounds) came from that
difference. NIM and DeepSeek are not flagship-grade. Using them as the second flagship would
forge the guarantee — it would produce an acceptance that reads as independent but is not,
which is worse than a missing acceptance. The same reason Claude Max is not used to fill the
Codex slot applies with more force here.

**As implementer ("coder") — NIM NO, DeepSeek NARROWLY, as a last resort only.**
- **NVIDIA NIM: NO.** Verified record (`AI_ACCOUNT_AND_MODEL_ROUTING.md` §7 trap): through
  the claude-CLI wrapper NIM *narrates but never engages file-write tools* — it produced
  zero deliverables on an authoring task. It is read/analysis only. It cannot author a block.
- **DeepSeek: usable, but weak for this work.** Probed live 2026-08-11 (`--selftest` →
  `PONG`, model `deepseek-chat`). It CAN drive an authoring loop via
  `_deepseek_driver/ds_agent.py --task <file>`. But: (a) these WP-I blocks are the hardest
  security-critical shell in the repo, not the mechanical/bulk work DeepSeek is routed for;
  (b) balance was ~$2.90 and will not sustain many rounds; (c) it has never been a
  protected-surface implementer. **Permitted use:** a single NARROW, fully-specified repair
  round (e.g. RP6 round 10b, whose kickoff enumerates every finding and command) ONLY when
  GLM is also unavailable, with the Lead verifying every byte and every published command
  before commit. **Never as auditor, never for a from-scratch block, never for transport's
  operational rebuild.**

**Practical consequence for the day:** the routine implementer lane is **GLM alone**
(returns 13:50) until Claude Pro's weekly reset. Codex (both lanes live) keeps doing audits
and analysis. If a second implementer round is needed while GLM is also spent, DeepSeek is
the last-resort coder for a narrow round; otherwise the queue simply waits on the next GLM
window. Claude Max stays reserved for a genuine acceptance-critical block only.
