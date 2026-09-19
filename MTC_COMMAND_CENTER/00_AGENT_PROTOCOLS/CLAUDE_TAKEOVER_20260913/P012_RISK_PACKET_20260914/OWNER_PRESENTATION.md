# P012 production-admission packet — owner presentation (2026-09-14, Claude Opus 5 Lead, session b9df29)

Packet: `P012_PRODUCTION_ADMISSION_PACKET.md` in this directory (sha256 `50a6cbbc939016eba54f559da51c63e6940c2c5b858306862ac4bb27c178f4c4`, 290 lines, 235 citations). Written by Codex Pro Spark under `OD-20260914-P012-RISK-PACKET-1` (`TASK.md`), first audited by Gemini 3.8 (`GEMINI_AUDIT_1/` — REQUEST_CHANGES, 3 BLOCKING), corrected by Codex Plus gpt-5.5 (`TASK_FIX1.md`, `DISPOSITION_FIX1.md`), re-audited by Gemini 3.8 (`GEMINI_AUDIT_B2/` — **PASS**, all nine findings RESOLVED, 115/115 citations EQUAL, no new findings; the Lead's own mechanical citation check agrees, `GEMINI_AUDIT_B/LEAD_CITATION_CHECK.md`). Nothing below is acceptance, admission, deployment or trading authority; answering these questions closes NOTHING by itself — each answer only gives the next evidence step an actor or a rule.

## What stands between the P012 kernel and "production admission" (plain words)
- 10 open Section-19 rows and 27 signed residual risks, all waiting on REAL evidence from the venue (own-account fills, funding settlements, fee bills). None of it exists yet. Testnet money is fake; the production rows need the real account later.
- A qualified/experienced human must review the completed records before the first money-exposed release (`REVIEW_POLICY.md` lines 73-76). The sources do NOT say who that person is.
- Gate order on KVM2 (`deploy/linux/README.md` 137-148): P4-03 secret provisioning (your hands; Toolkit button 5) → one first DISARMED start → rollback proofs → P5-05/P5-05A ARM, each with its own sentence from you; none implied by the previous one.

## The 7 questions the packet puts to you (packet section 6; recommended answer first)
1. **Who is the qualified human reviewer** for the instrument/cost/funding records (I-4, C-12, F-23) and the money gate? — Recommended: **name the person**. If you intend to be that person, say so explicitly; the policy is met only if you fit its wording ("an experienced engineer"). Consequence: without a name these items stay open; naming someone does not let model output replace the review.
2. **May testnet evidence count for production admission?** — Recommended: **NO**. Testnet informs preparation only; production fee/funding rows wait for authenticated own-account evidence.
3. **Which real account fee tier applies (C-10)?** — Recommended: **WAIT**. Tier evidence is collected but not incorporated; declaring a tier now would invent applicability.
4. **Funding period semantics (F-13)?** — Recommended: keep funding separate from the fee boundary; signed rule A1 (forward-only, own account; the whole interval starts at or after 2026-09-12T11:00:00Z), M pending until at least one observation. Consequence: no retroactive funding admission.
5. **Fee interval boundary (C-6)?** — Recommended: keep the signed B3 rule — fee evidence starts at the first authenticated own-account fill; a fee boundary only, not the funding interval.
6. **Order of venue/KVM2 captures?** — Recommended: follow the gate order exactly (P4-03 → DISARMED start → rollback → ARM separately); no shortcuts. Consequence: each of your sentences stays scoped; nothing here authorizes ARM, monitoring, backup provider, firewall or mainnet.
7. **Accept estimated costs before native billing evidence?** — Recommended: **NO**. The reported fee stays the admitted cost; the schedule stays a guarded estimator; missing fee fields stay refused.

## Not verified / not in the packet (the packet says so itself, section 7)
- The Hyperliquid funding cadence (8-hour) is NOT established in the sources used.
- "Five residual obligations" are counted, not enumerated anywhere by that name; risks 24-27 are grouped, not individually named; the 27 count is quoted, not recomputed.
- No credential, wallet, key or env value was read.

## What happens after you answer
Your words are recorded verbatim in CT13 `DECISIONS.md` (one row per question). Then the evidence steps run in gate order — the next one is yours: run Toolkit button `5 - TESTNET Secret Provisioning (KVM2).cmd` and say "provisioned".
