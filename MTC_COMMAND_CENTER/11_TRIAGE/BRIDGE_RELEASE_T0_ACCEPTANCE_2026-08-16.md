# Bridge release integration candidate — T0 ACCEPTANCE — 2026-08-16

Status: **T0 ACCEPTED (Gate 5)** — dual-flagship, zero required repairs.

| Item | Identity |
|---|---|
| **Accepted candidate** | `62bf661b065dec5b5d9895d83575581fe369252d` |
| Tree | `e2cb5dadd1537e933460aeecd5cdcf343c31d7d0` |
| Parents | `7d4e9a96e07b34a0c3d92315912d7818168b830b` (repaired WP-I) + `2ce41e34bceb599d80af24c5c33d835820ec321b` (Gate-A) |
| Branch | `integration/bridge-release-20260815` (pushed to origin) |
| Host scope | **LOCAL RELEASE only.** No host has executed these bytes. |

## The two flagship verdicts (both executed the full suite themselves)

| Slot | Model / effort | Verdict | Findings | Suite |
|---|---|---|---|---|
| Codex | `gpt-5.6-sol` xhigh, fresh session | **PASS** | 0 REQUIRED, 0 NIT | `1360 passed, 1 warning in 180.43s`, rc 0, post-run clean |
| Claude | `claude-opus-5` xhigh, fresh session, isolated worktree `C:\AUD62A` | **PASS-WITH-NITS** | 0 REQUIRED, 4 NIT (all in prose records, none in candidate bytes) | `1360 passed, 1 warning`, rc 0, run provably mutated nothing |

Verdicts of record:
`T0_62BF_CODEX_VERDICT_2026-08-16.md` · `T0_62BF_CLAUDE_VERDICT_2026-08-16.md`.
Both independently verified: identity/parents/merge-base, 33/33 blob fence,
exact 32-path first-parent delta (set equality + rename-detection-off control),
byte-level resolution correctness, credential-string parity with Gate-A
(17 across 7 paths, derived independently from `2ce41e34`), D026 (no new
closure test; test-definition count unchanged at 957), and adversarial passes
(mode/type fence, collection-tampering controls, `.gitattributes` pin).

## Nit disposition (all repaired same day, prose only)

1. NIT-1 "replayed byte-exactly" → corrected in
   `BRIDGE_RELEASE_MERGE_EXECUTION_RECORD_2026-08-16.md`.
2. NIT-2 9/21 sub-split unreconstructable → correction banner on
   `BRIDGE_RELEASE_MERGE_RUNBOOK_INPUT_REFRESH_2026-08-16.md`; sub-split
   declared decorative, not to be quoted.
3. NIT-3 nonexistent `WPI_BLOCKS_DRAFT/` path segment → same banner.
4. NIT-4 "stale assertion" mischaracterization → corrected in the execution
   record (harmonization, not defect fix).

## Effort caveat of record

The Claude verdict states effort `xhigh` was configured by the dispatching
route (CLI flag `--effort xhigh`) and cannot be introspected in-session; no
lower-effort override was applied. The dispatch command is preserved in the
session transcript and satisfies the roster's launch-evidence requirement.

## What acceptance does and does not grant

**Does:** `62bf661b` is the accepted current Bridge release candidate for the
accelerated contract's chain — the input for the Stage-1/freeze steps and the
KVM2 deployment plan.

**Does not:** any host execution evidence for these bytes; any transfer of
Gate-A A-0..A-9 (that stays with `2ce41e34` on GATEA-STAGING); merge to
master; deployment, credential, broker/exchange, ARM, order, TESTNET/mainnet
authority. KVM2 install/start still requires the owner's separate
authorization after the read-only inventory and the single deployment plan
(accelerated contract clause 6).
