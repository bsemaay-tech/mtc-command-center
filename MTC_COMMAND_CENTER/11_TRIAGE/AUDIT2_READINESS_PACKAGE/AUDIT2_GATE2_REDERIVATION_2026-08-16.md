# Prerequisite gate 2 — Lead re-derivation — 2026-08-16

Performed by the Fable 5 Lead under the accelerated full-completion contract
(`../OWNER_DECISION_ACCELERATED_COMPLETION_2026-08-16.md`). This closes the
"gate 2 is UNKNOWN pending Lead freeze-prerequisite re-derivation" banner on
`AUDIT2_FREEZE_PREREQUISITES.md`.

Gate 2 = "Repair/design closure and final artifact acceptances". Sub-item by
sub-item, from recorded evidence — not inference:

| Sub-item | State | Record |
|---|---|---|
| RP6-P0 block | ACCEPTED-WITH-DISCLOSURE (owner-adjudicated) | `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md` + gate-2 row corrections of 2026-08-15; disclosure state retained per midday handoff state table. |
| RP7 rows 1–9 | **T0 ACCEPTED, dual flagship** on frozen candidate `80cbed461d0b0371e6eabbfff0e732e5001affaf` — `gpt-5.6-sol` xhigh PASS + `claude-opus-5` xhigh PASS-WITH-NITS, zero required repairs | `../WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md` |
| Transport set | ACCEPTED-WITH-DISCLOSURE (owner-adjudicated, predates and is unaffected by RP7 acceptance) | acceptance matrix + 2026-08-15 correction in `AUDIT2_FREEZE_PREREQUISITES.md` row 2 |
| SEC102 | ACCEPTED-WITH-DISCLOSURE, owner decision 2026-08-12 ~13:10; freeze blocker #4 CLEARED | `../WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md` |
| Pathscope | **DISPOSED by owner decision §6 (2026-08-16): supplemental-with-disclosure, OFF the critical path, no further cycle.** Not proof; closes no gate; nothing downstream may cite it as acceptance input. Its former "only remaining open sub-item" role is discharged by the owner's recorded decision, not by inference. | `../OWNER_DECISIONS_2026-08-16_MORNING.md` §6; `../WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_SUPPLEMENTAL_DISCLOSURE_V2_2026-08-16.md` |
| Bridge release integration (new since the last refresh) | **T0 ACCEPTED, dual flagship**, candidate `62bf661b065dec5b5d9895d83575581fe369252d`, suite `1360 passed` executed independently by both auditors | `../BRIDGE_RELEASE_T0_ACCEPTANCE_2026-08-16.md` |

## Derivation result

**Gate 2: SATISFIED-WITH-DISCLOSURES.** Every sub-item holds either a dual-
flagship T0 acceptance on exact bytes or an explicit owner-adjudicated
accepted-with-disclosure record; the single formerly-open sub-item (Pathscope)
is disposed by a recorded owner decision. The disclosures travel with the
freeze: any Audit 2 dispatch package must list them (RP6/transport/SEC102
disclosure records; Pathscope non-proof disclosure; chain-design V3 disclosure
of no mutation-denial evidence).

## What this does NOT change

Gates 3–6 of `AUDIT2_FREEZE_PREREQUISITES.md` remain NOT SATISFIED: the
Stage-1 two-commit freeze (now at design V3, pending its fresh T1 round),
authorized WP-I execution/closure, the pre-WP-A checkpoint freeze, and the
freeze-time ledger ratification. The binding sequence stands. No host,
credential, broker, ARM/order, TESTNET/mainnet, master-merge, deployment, or
economic authority is granted here.
