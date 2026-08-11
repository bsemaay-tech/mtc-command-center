# Lead adjudication note — MERGE-CONFLICT MC-01..03 in successor draft R3

Date: 2026-08-11 ~13:20. Author: Lead (Fable session). Status: adjudication of conflict
SHAPE only; the substantive decisions remain owner-gated.

## Finding

All three MERGE-CONFLICTs registered in `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`
§4.5.4 share one shape: the R2 skeleton-gap application already wrote BINDING text for
exactly the closure that the lane-B family proposal marks
`PROPOSED — LEAD/OWNER DECISION REQUIRED`. The two texts do not disagree on content —
only on decision status. Lead verified convergence per pair:

| MC | R2 binding text | Lane-B proposal | Substantive delta |
|---|---|---|---|
| MC-01 | exact 12-entry `P0_TOOL_PINS`, no PATH fallback (R2 §2.1/§4.2) | close to twelve exact pins, delete fallback (Decision F1) | none |
| MC-02 | `P0_VENV_ROOT` = `/opt/mtc-bridge/venvs/$P0_CAND` exactly (R2 §4.2) | bind the one exact per-candidate venv root (Decision F2) | none |
| MC-03 | complete frozen-composite proof is the acceptance route; block-only results supplemental (R2 §4.4) | require complete frozen-composite derivation (Decision F3) | none |

## Adjudication

1. The three "unresolved §10.1 families" therefore collapse to a single owner ask:
   **ratify the three closures as already written in R3** (one yes/no, not three design
   decisions). Until ratified, R3 correctly refuses freeze.
2. No text change to R3 is required now. On ratification, the resolution is: delete the
   `PROPOSED` qualifiers in the three lane-B decision sections, cite this note plus the
   owner's ratification record, and clear §4.5.4.
3. If the owner REJECTS any closure, that family reopens as a real design decision and
   the corresponding R2 binding text must be reopened too — they stand or fall together.

Owner-facing wording for the morning report: "Three security settings were proposed by
one review and independently written as requirements by another — they agree. One
approval ratifies all three."
