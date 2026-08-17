# Gate-1 Scope Record — Package 7: Official Exchange Reverification

**Date:** 2026-08-17 night · **Lead:** Claude (Fable) · **Tier: T2, read-only, documentation**
**Owner authorization:** in chat 2026-08-17 night ("start pack 7"), recorded as Decision 5 in
`OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`.
**Accepted source:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 7, §5 item 1
(accepted per `BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md`).

## Frozen scope

Produce ONE verification record for the claims: sub-account eligibility (incl. the $100k volume
gate and scaling), agent/API-wallet behavior (nonces, lifecycle, per-sub-account counts),
same-symbol netting / hedge mode, margin modes (cross/isolated/strict-isolated, coexistence,
account abstraction modes, portfolio margin), API limits (IP-based, WebSocket, address-based
sub-account treatment), and TESTNET parity of the above where stated. Per claim: status
VERIFIED / UNKNOWN / ACCOUNT-LEVEL-ONLY, official source URL, exact quoted sentence(s).

Method: official Hyperliquid documentation pages only, live-fetched by the Lead on 2026-08-17
(quote dump handed to the implementer). Zero account, API-key, wallet, login, SDK, endpoint, or
host actions. Third-party sources never upgrade a claim to VERIFIED.

## Roles and review

- Implementer: GLM-5.3 (sub-delegation; Codex Plus routes credit-exhausted).
- T2 review: one reviewer, one round, medium effort — DeepSeek (`deepseek-v4-pro`), a different
  provider from the author. Gemini read-only route available for supplemental cross-check.

## Out of scope / prohibited

Account-level checks of any kind, architecture freezes (Package 1 consumes this record later),
and everything in the standing prohibition list (VPS/host, credentials, exchange account
actions, TESTNET/MAINNET execution, ARM/orders, Pine/parity/MTC).
