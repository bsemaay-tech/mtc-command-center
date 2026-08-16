# KVM2 deployment package — ACCEPTED — 2026-08-16

Status: **T0 ACCEPTED** under the owner's round-4 override + confirmation-pass
contract (`OWNER_DECISION_ROUND4_FINAL_2026-08-16.md`,
`OWNER_DECISION_CONFIRMATION_PASS_2026-08-16.md`). Awaiting ONLY the owner's
§3 installation-authorization sentence. KVM2 untouched.

## The accepted package (final pins)

| Item | Identity |
|---|---|
| Candidate | `acdf4e379fb60ee319854acae19fd3eaf7db71a2` (tip `integration/bridge-release-20260815`; lineage 62bf661b→be689537→a7460784→acdf4e37) |
| Suite | `1376 passed, 1 warning` — executed independently by implementer, Lead, and BOTH final reviewers |
| Payload | `C:\tmp\payload-acdf4e37`; manifest sha `e74c59fec82d49090d5ba56d4bf18f1cc0dbdd93375c0c82c07ab44b211530bf` |
| Plan V6 (final bytes) | 7342 B, sha256 `c41b4cab97f460be3ac5e5fcd24f47b308819e97169c513c65a87b33bb4d16a5` |
| Command annex (final bytes) | 31980 B, sha256 `5a3f92e68514681dd94a913bc00a7f6964ab8efa98a6904be8c507f738761d7a` |
| Launcher v4 | `KVM2_RUNKIT/Open-BridgeDashboard.ps1`, 9277 B, sha256 `ac68196b4ae99e12892898c0a5bfb2d7d2249fc2bb476619a4c2bdaaebf2a1b5` |

## Acceptance chain

- Rounds 1–3: 17 → 10 → 10 REQUIRED findings, every one repaired and its
  repair verified by re-attack; six full verdicts committed.
- Round 4 (final pair, owner materiality standard): candidate + launcher +
  annex commands fully accepted by both flagships; 2 material plan-text
  findings remained (Codex REQUIRED-1/2; Claude REQUIRED-1 = Codex R-1).
- Confirmation pass (owner-scoped): both prescribed repairs applied
  (`3bf5cccd`), focused RED/GREEN recorded, and **both flagships CONFIRMED
  both closures** (`CONFIRM_CODEX_2026-08-16.md`,
  `CONFIRM_CLAUDE_2026-08-16.md`) — Codex reproduced the four-arm cleanup
  RED/GREEN independently; Claude verified only the four intended files
  changed between `17d304c9..3bf5cccd`.
- Disclosed follow-up register (non-blocking, owner standard): the items in
  the two final verdicts' DISCLOSED sections — chiefly D3-phase wording
  harmonization — must be resolved before the D3 sentence is drafted.

## What happens next (in order, each separately gated)

1. **Owner signs the Plan V6 §3 sentence** (the only signable copy).
2. Execution of annex stages 1–3.5 under that sentence (install stays masked,
   never started, credential-free).
3. Later: owner's separate first-start sentence → one DISARMED start →
   D3 dashboard verification matrix (needs its own D3 sentence for auditd).
4. Later: TESTNET secret provisioning (owner-only), Dashboard V2 package.

Mainnet, real money, ARM, orders, live trading: forbidden throughout.
