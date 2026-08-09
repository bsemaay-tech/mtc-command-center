# WP-L PHASE 2 DISPATCH PROMPT (2026-08-09) — owner-authorized

Paste-ready dispatch for Codex (`gpt-5.6-sol`, via `Invoke-CodexForClaude.ps1 -Account
secondary`). Do not dispatch while the provenance repair acceptance round (per
`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §4) is still open.

---

## Authorization

Barış, 2026-08-09, explicit: **WP-L Phase 2 and WP-I staging verification are authorized to
start**, in the canonical post-Gate-A order recorded in
`GATE_A_POST_GATE_ROADMAP_AUTHORITY_DISCOVERY_2026-08-09.md` §3 (WP-L Phase 2 → WP-I staging
verification → Audit 2 → WP-A). The 50h budget blocker is cleared by the ledger ratification in
`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §1 (baseline 20.5 h used / 29.5 h remaining; book
actual hours prospectively at WP closeout).

**Audit process for all work under this dispatch follows the tier policy in
`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §2–3.** No per-step flagship audits; script gates +
self-verification inside the WP; model audit at WP boundary; Audit 2 stays two-flagship.

## Scope

1. **WP-L Phase 2** — Ubuntu revalidation of all ported paths on the **retained expendable
   `GATEA-STAGING` host** (the same host Gate A accepted; do NOT provision a new host, do NOT
   touch KVM2). Candidate identity is frozen: `2ce41e34bceb599d80af24c5c33d835820ec321b` — any
   change to it requires a new Gate-A-style acceptance, not this dispatch.
2. **WP-I staging verification** — complete the staging verification items on the same host.
3. **Stop before Audit 2.** Prepare the frozen checkpoint SHA/artifact list for Audit 2 and
   hand off; Audit 2 dispatch is a separate step.

## Hard constraints (unchanged)

- Bridge stays **DISARMED**, credential-free, loopback-only (`127.0.0.1:8790`).
- Forbidden: credential loading, successful ARM, orders, broker/exchange contact,
  TESTNET/mainnet, master merge, WP-V/KVM2 actions, deletion of the old payload archive.
- First-FAIL stopping; no-clobber evidence logs; preserve evidence before any teardown;
  final report per `MTC_REPO_GUARD_PROTOCOL.md`.
- Commit checkpoints to `feature/donchian-crypto-ladder`; update
  `_AI_MEMORY/GLOBAL_HANDOFF.md` + `NEXT_STEPS.md` at WP boundaries (T3 — no audit).

## Hour booking

Record actual hours for WP-L Phase 2 and WP-I at their closeouts against the ratified 29.5 h
remaining. If projected total for WP-L P2 + WP-I + Audit 2 + WP-A exceeds remaining budget,
STOP and surface to Barış before starting the overrunning item.
