# Dashboard inputs

- Accepted screen/route contract and the exact API/read-model schema used by the changed view.
- Final visual reference: `../11_TRIAGE/ui_references/google_strategy_intelligence_v2_final`.
- Representative fixtures for healthy, missing, stale, malformed, and unevaluable states.
- Root `DECISIONS.md`, including D002 and accepted read-only ADRs.
- For impact changes, query a scoped code graph before changing API/web boundaries.

Never use production secrets, broker credentials, or live endpoints as UI fixtures.
