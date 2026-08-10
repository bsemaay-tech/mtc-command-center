# OWNER DECISION — AUDIT TIER POLICY, CADENCE, AND 50H LEDGER RATIFICATION (2026-08-09)

Authority: Barış, 2026-08-09, explicit chat authorization ("evet — varsayılan yol 1 → 2 → 3"),
relayed by the Claude Lead session. This record is binding on all agents (Codex, Claude
Lead/Max, GLM, DeepSeek) for the remainder of the 50-hour programme unless Barış revises it.

## PERMANENCE ADDENDUM (2026-08-10)

Barış explicitly extended this decision from the 50-hour programme to a **repo-wide permanent
default** until revised. `AGENTS.md` § AUDIT TIER POLICY — PERMANENT DEFAULT is the canonical
operational copy; this file remains the rationale/history record.

## 1. 50-hour ledger ratification (closes the budget-evidence blocker)

`GATE_A_50H_LEDGER_RECONSTRUCTION_2026-08-09.md` concluded the exact used/remaining balance is
NOT REPRODUCIBLE from records. Owner resolution:

- **Ratified baseline: 20.5 h used / 29.5 h remaining, effective at WP-L Phase 2 start.**
  (The last reproducible pre-WP-L point. All unreconstructable post-WP-L-Phase-1 work is
  absorbed into this baseline by owner decision — no retroactive booking, no further
  reconstruction work.)
- Ledger reconstruction is **CLOSED**. From now on hours are booked **prospectively per work
  package** at each WP closeout (Lead Gate-7 style), never retroactively.
- The budget-evidence blocker in `GATE_A_POST_GATE_ROADMAP_AUTHORITY_DISCOVERY_2026-08-09.md`
  §6 is **cleared** by this ratification.

## 2. Audit tier policy (binding)

Rationale: post-Gate-A, flagship multi-model audit rounds were applied to documentation and
provenance work, burning ~10 h wall-clock and significant subscription quota on non-product
surfaces. Owner directive: **speed without quality loss** — reserve heavy audit for surfaces
where a defect is dangerous or expensive; lighten everything else.

| Tier | Surfaces | Auditors | Effort | Max rounds |
|------|----------|----------|--------|------------|
| **T0** | Economic/live: deploy scripts, systemd units, `verify.sh`, credential/secret handling, ARM path, broker/exchange code, teardown scripts, anything touching staging/production hosts | 2 independent flagships: `claude-opus-5` + Codex `gpt-5.6-sol` | xhigh | 3 |
| **T1** | Product code (non-economic): bridge logic, tests, tools, run-kit **scripts** | 1 flagship (alternate Claude/Codex per round) + GLM-5.2 second opinion ONLY if the flagship raises findings or the diff exceeds ~300 lines | high | 2 |
| **T2** | Docs, handoffs, provenance records, prereg text, run-kit **documentation**, evidence write-ups | **Single reviewer, single round.** GLM-5.2 preferred; DeepSeek acceptable; flagship at medium effort only if neither is available | medium | 1 |
| **T3** | Checkpoints, indexes, typo/format fixes, status stamps | Implementer self-verification only. No model audit. | — | 0 |

Escalation rule: a T2 finding that touches **deployed-artifact identity** (SHAs, hashes,
candidate identity, release manifests) escalates **that finding only** to a single-flagship T1
verification — never a full multi-model round.

Effort discipline: **xhigh is T0-only.** No xhigh sessions for T1/T2/T3 work.

## 3. Audit cadence (binding)

- **Model audits run at work-package boundaries, not per-step.** Canonical points: WP-L Phase 2
  close, WP-I staging verification close, **Audit 2 (Gate-5)** — which stays two-flagship
  because it freezes the pre-WP-A SHA — and WP-A close.
- Inside a WP: script gates (Gate-A style, first-FAIL), implementer self-verification, and
  no-clobber evidence logs replace per-step model audits. T0 surface changes are the sole
  exception — they are audited immediately regardless of cadence.
- Expected effect: ~60–70% fewer model-audit rounds with unchanged coverage at the points that
  decide promotion.

## 4. Current provenance repair (immediate application)

- The in-flight `claude-opus-5` doc-only provenance repair round **completes as started**.
- Acceptance check afterwards: **one Codex round, single pass** (Codex raised the
  REQUEST_CHANGES, so Codex closes it). **No 4-model re-audit.** GLM/DeepSeek are not invoked
  for this item.

## 5. Process correction — meta-artifacts are never separately audited (added ~11:30)

Applying §2–§3 to the WP-L P2 proposal-repair chain, by owner authority:

- **Prompts, checklists, dispatch packages, repair specs, and other process artifacts are T3**:
  implementer/Lead self-check only. They are never given their own model-audit rounds. The
  2026-08-09 morning chain (9 meta-documents, ~3 h, audits of prompts and checklists of repairs)
  must not be repeated.
- The pending "fresh Claude/Codex/GLM package re-audit" round demanded before the Claude proposal
  repair is **WAIVED**. The Claude counterpart repair (round 1/3) is dispatched directly against
  the frozen spec `9ac60ac6` + hardened prompt, by the Lead, now.
- Rigor concentrates where it belongs: the **repaired proposal document** (the artifact whose
  scripts would eventually touch the staging host) receives the full T0-grade review — Lead
  verification with reproduced falsifications, then Codex flagship re-audit. That bar is unchanged
  from the repair spec §9; only the audit-of-process layers above it are removed.
- `WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md` (F1–F9) is recognized as the **single
  authorized round-1 audit** of the proposals; its findings stand.

## 6. Unchanged boundaries

This decision changes audit process only. Still requiring explicit separate Barış
authorization: WP-V, KVM2 production deployment, master merge, credential loading, broker or
exchange access, ARM, orders, TESTNET/mainnet, any economic action, deletion of the old payload
archive. First-FAIL stopping and evidence no-clobber rules stand.
