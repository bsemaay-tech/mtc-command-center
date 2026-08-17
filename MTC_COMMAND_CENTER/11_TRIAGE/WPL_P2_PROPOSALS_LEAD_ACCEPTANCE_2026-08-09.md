# WP-L P2 command-gap proposals — Lead acceptance record (2026-08-09)

## Verdict

**ACCEPTED** by the Lead under explicit owner authority (Barış, 2026-08-09, decision "1" in chat:
owner reopened the exhausted cycle for the single required correction and defined the audit as
Lead verification against the round-3 re-audit's own reproduced values).

## Basis

- Codex final re-audit `f291aba7` (`WPL_P2_PROPOSALS_REAUDIT_ROUND3_2026-08-09.md`): RR2-1..RR2-4
  all reproduced closed; two complete harness runs 41/41 outcomes clean rc 0; no regression of the
  round-1/round-2 closures; all BLOCKED items (C1, C2 scenario dependencies, C5, R4-5) remain
  honestly declared. Sole required finding RR3-1: stale §8.1 identity row for `RP0-LIB`.
- RR3-1 correction applied in this commit: §8.1 row now `370` /
  `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48`.
- Lead independent reproduction (this session, documented extraction convention "from the
  `BLOCK-ID` marker up to, not including, the closing fence, LF endings"): `370` lines, SHA-256
  `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` — bit-identical to the
  re-audit's fresh extraction. The other eight §8.1 digests were already verified exact by the
  round-3 re-audit.

## Chain of custody

`779bd038` draft → audit F1–F9 (`b5a6ce53`) → repair r1 `7194b895` → re-audit r1 `1dad3196`
(R1–R5) → repair r2 `75ee8912` → re-audit r2 `fc06632e` (RR2-1..4) → repair r3 `909ab8f7` →
final re-audit r3 `f291aba7` (RR3-1 only) → this Lead correction + acceptance.

## Scope of this acceptance

Design acceptance of the proposal document only. Extraction of scripts into the WP-L P2
implementation unit may proceed per `WPL_PHASE2_DISPATCH_PROMPT_2026-08-09.md`. This record grants
no host, credential, broker, ARM/order, TESTNET/mainnet, master-merge, WP-V/KVM2, or economic
authority; per-mutation gating inside the staging unit stands. C1/C2-baseline/C5/R4-5 remain
BLOCKED as documented; R4-5 is expected to close trivially on the staging host's Linux during WP-L
P2 (real symlink support).
