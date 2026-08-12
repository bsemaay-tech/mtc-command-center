# KICKOFF — GLM-5.2: cross-check the freeze-input ledger's RP6 claims (the unverified half)

You are GLM-5.2 via the Z.AI route. **You are running UNATTENDED — do not ask for approval, do
not write a plan and stop. Execute directly and write your verdict file.** Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except your verdict file, no git
mutation, no host, no network.

## Why this exists
`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md` was produced by Codex on `-Account free`, which resolves
to **`gpt-5.5`** — a weaker model than the `gpt-5.6-sol` used elsewhere. Its transport and RP7
claims have since been independently cross-checked and both held up (see
`WPI_BLOCKS_DRAFT/TRANSPORT_GLM_ADVANCE_READ_AUDIT_2026-08-12.md` and
`RP7_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`; the transport check even found a *second* staleness
the ledger had only half-flagged). **The RP6 half has not been cross-checked**, and it carries
the most consequential claim in the document.

Today also produced a live reminder that this matters: an advance read-audit asserted the RP6
census admits a variable-mutating `eval`, and that claim was **false** — the fence already
refuses it. Assume nothing; read the bytes.

## The claim to verify
Ledger §"Blocker 7" states, in substance:

- `run_p0.sh` defines all five `P0_ATTESTED_*` values as `<PIN-AT-FREEZE>` (`:151-155`), exports
  them (`:237-240`), and prints the deploy-channel attestation line while still using
  placeholders (`:241-243`), then sources RP6 (`:245`).
- RP6 requires all five wrapper values (`RP6-P0.sh:691-700`), rejects unfilled markers and
  malformed namespace/root-mount input (`:707-724`), requires embedded-literal ↔ wrapper equality
  (`:733-752`), reads live namespace links (`:1390-1393`), and checks root-mount identity
  (`:1394-1414`).
- **The consequential part:** with `STATUS_RP6_P0.md` recording *17 remaining `<PIN-AT-FREEZE>`
  literals*, **RP6 cannot produce an end-to-end P0 PASS**, so the Codex r16 acceptance is a
  **source/audit acceptance, not a host end-to-end PASS.**

## What to check
1. **Every cited line number.** The ledger's `file:line` citations were written before round 17
   added content to `SELF_QA_RP6.md` and before the Lead corrected `STATUS_RP6_P0.md`. Confirm
   each citation still points at what it claims, and report any that have drifted.
2. **The literal count.** A Lead spot-check counted **27** occurrences of `<PIN-AT-FREEZE>` in
   `RP6-P0.sh`, not 17. Resolve this discrepancy: is 17 a count of *distinct pins* versus 27
   *occurrences*, is it a count in a different file, is it stale, or is it simply wrong? State
   the correct number, what it counts, and where the "17" came from.
3. **The load-bearing conclusion.** Is it true that RP6 cannot reach an end-to-end P0 PASS in the
   current state? Trace the actual refusal path — which check fires first on unfilled markers,
   and does anything downstream of it still run? This determines whether the Codex r16 acceptance
   may ever be described as an end-to-end PASS, which is an Audit-2-relevant distinction.
4. **Whether the ledger overstates or understates.** Both directions are findings. If the ledger
   is right, say so plainly — a confirmation is a useful result, not a non-result.

## Verdict
Prefix `CROSS-CHECK`. State clearly: CONFIRMED / CONFIRMED-WITH-CORRECTIONS / REFUTED, then the
corrected statement of fact the Lead should carry into the blocker map. This is a source read;
mark any step you could not execute `PENDING-LEAD-EXECUTION` and **never fabricate a green run.**

Write ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/LEDGER_RP6_CLAIMS_GLM_CROSSCHECK_2026-08-12.md`.
