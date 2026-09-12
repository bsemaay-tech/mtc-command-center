# P012 Path D decision — 2026-09-12

Owner approved, in chat on 2026-09-12 (~11:00Z), the Path D acceptance-bar decision for WP-P0-12 ("Approve ABCD with suggested matrix"):

```
A. Funding   APPROVE   A1=A  A2=B (M PENDING, separate decision after N observations)  A3=A
B. Fees      APPROVE   B1=C  B2=C (5% rel; alt max(5%, 1e-6 USDC))  B3=B  B4=A   N=3 (maker, taker, near-$10)
C. Quantity  APPROVE   C1=A  C2=B (K=10)  C3=A
Account/product/interval: UNSPECIFIED until authenticated evidence exists
OPEN01/03/05/07 stay OPEN; 27 signed risks stay; Item 4 only via explicit row;
no deploy/live/TESTNET/mainnet/ARM/order/spend authority; T0 reviews, R29 redo, ratification, CI, protected merge remain.
```

Source documents (external campaign root `C:/tmp/CLAUDE_P0_JOBS/job02_p012_outbound/`): `PATH_D_DECISION_PACKET.md` sha256 `23e80c8e…2774`; `PATH_D_OWNER_REVIEW.md` sha256 `e93ef26f…7ce1`; signed record `PATH_D_DECISION_SIGNED_20260912.md`.

Meaning: a bounded risk is accepted instead of a venue fact. Three source classes are authorized for preparation: `HL_FUNDING_VENUE_REPORTED_CASH_V1` (forward-only own-account settlements, whole-interval refusal on any gap, magnitude guard with M pending), `HL_FEE_REPORTED_PER_FILL_V1` + `HL_FEE_SCHEDULE_ESTIMATOR_GUARDED_V1` (reported fee admitted, schedule as 5%-tolerance estimator, interval starts at first authenticated fill, liquidation class stays CANNOT_MAP, N=3 fills incl. maker/taker/near-$10), `HL_QTY_OWNER_GUARD_NOT_VENUE_FACT_V1` (minimum_quantity = 10 × 0.00001 BTC with mandatory provenance marker, floor rounding then guard + MinTradeNtl re-check).

Unchanged: OPEN01/03/05/07 stay OPEN; the 27 signed risks stay; Item 4 `NONE_KEEP_REFUSED` may change only through an explicit qualification row; the funding consumed-oracle question, fee rounding/fixed/minimum/liquidation rules, independent quantity floor and reduce-only exemptions remain unresolved venue facts. Supporting evidence: testnet probe 2026-09-12 (`C:/tmp/CLAUDE_P0_JOBS/laneP1_testnet_probe/P1_EVIDENCE_NOTE.md`): only the 0.00001 grid and the $10 limit-price notional rule enforced; no separate floor observed (TESTNET_OBSERVED, not a mainnet fact).

Authorizes only: one local non-accepting implementation candidate on packet §3 paths with synthetic fixtures and D026 RED/GREEN, its T0 reviews, the governance rows and the dependent-identity re-derivation. No acceptance, merge, runtime, trading or spend.
