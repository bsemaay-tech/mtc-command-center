# Gate-1 Scope Record — Package 1: V2 Architecture Contract Pack

**Date:** 2026-08-17 night · **Lead:** Claude (Fable) · **Tier: T2, documentation only**
**Owner authorization:** in chat 2026-08-17 night ("start packages 1+2"), recorded as Decision 5
in `OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`.
**Accepted source:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 1, §5 item 2
(accepted per `BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md`).

## Frozen scope

One architecture contract pack split exactly as the accepted backlog requires:

- **Section A — settled locally:** worker identity, store model, Portfolio Guardian veto
  semantics.
- **Section B — CONDITIONED ON Package 7 output:** worker boundary, feed topology, subaccount
  eligibility/fallback, agent-wallet behavior, same-symbol netting, margin mode, API limits.
  Section B decisions cite the Package 7 verification record where it answers them and remain
  explicitly unfrozen wherever Package 7 reports UNKNOWN or ACCOUNT-LEVEL-ONLY.

Documentation only; no code, no runtime wiring, no live exchange assumptions beyond the
Package 7 record. `docs/30` citations follow the accepted (HEAD `033546fb`) convention.

## Sequencing

Authoring starts after the Package 7 verification record exists (same night), so Section B can
consume it. Package 2 runs in parallel and is independent.

## Roles and review

- Implementer: GLM-5.3 (sub-delegation). T2 review: DeepSeek (`deepseek-v4-pro`), one round,
  medium — different provider from the author. Gemini read-only route as supplemental cross-check.

## Out of scope / prohibited

Freezing any Section B decision beyond what Package 7 verified; implementation of any kind; and
the standing prohibition list (VPS/host, credentials, exchange account actions, TESTNET/MAINNET,
ARM/orders, Pine/parity/MTC, frozen-V1 mutation).
