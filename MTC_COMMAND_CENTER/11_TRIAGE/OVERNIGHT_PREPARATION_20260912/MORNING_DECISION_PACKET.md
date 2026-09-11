# Morning implementation decision packet

**Recommended next: authorize the two-file P0-30 offline replay fix.** P0-21's isolated helpers are a second independent option. No full package is accepted or newly authorized by this preparation.

Window: **12 September 2026, 00:59:28–08:59:28 Europe/Chisinau** (11 September 21:59:28–12 September 05:59:28 UTC). Actual completion and stop reason are in [RUN_STATE](RUN_STATE.md).

| Package | Concrete next unit | Required start condition | Recommendation |
|---|---|---|---|
| **P0-30** | Correct identical-bar replay through `ingest`; preserve conflict, gap, forming-bar and no-network fences | New bounded approval for root `market_data_collector.py` and `check_market_data_collector.py`, exclusive writer and required review | **Start first.** The mismatch is independently reproduced. |
| **P0-21** | Isolated policy, classification and gap-measurement helpers with synthetic tests; admission remains refused and four limits unset | Approve the exact helper/test files in the implementation map | **Optional parallel start** with P0-30; no overlapping files. |
| **P0-13** | Freeze parameter/search-space identities, per-trial artifact binding and completed-run receipts; reuse the existing reader | Protected P0-04 scope plus P0-20 release of shared identity files; full writer also needs accepted P0-20 evidence | **Queue the contract prerequisite.** |
| **P0-22** | Family-resolution and interval helpers; later observation-ledger/leakage integration | Early helpers require an explicit isolated scope; full integration needs P0-13 and independent completeness/anchor producers | **Queue full integration behind P0-13.** |

The [implementation map](IMPLEMENTATION_MAP.md) gives ordered files, exclusive ownership, acceptance conditions and one recommended resolution for each dependency. The P0-30 watchdog/backup adapters are later slices consuming unchanged P0-26 interfaces; no separate P0-26 implementation is proposed.

Verified findings:

- **P0-13:** a foreign branch has working schema/reader/search code; three existing tests pass. A full writer and independent commit-admission path are missing.
- **P0-21:** seven diagnostic checks intentionally refuse readiness; 12 provisional fields are recorded and four remain open. Fresh checks matched all 17 historical files and 4,105,966 rows with no internal cadence faults. This is Binance research evidence, not Hyperliquid admission or a chosen gap limit.
- **P0-22:** existing contracts and 63 registry rows are reusable. They do not implement a family resolver, observation ledger or completeness proof.
- **P0-30:** its offline checker passes with zero network attempts. Archive replay no-ops; identical replay through ingest refuses. The proposed correction must inspect duplicates without writing an incoming bar before gap validation.
- **P0-26:** 33 local tests pass. Process heartbeat, market freshness and consistent backup boundaries remain distinct interfaces.

P0-20's freeze receipt and all three member hashes were independently verified. Its Lead confirms no new policy carrier and no change to the six-member evaluation hash. The freeze supports candidate implementation; **full downstream integration still waits for P0-20 acceptance**. P0-12's final research closure arrived before delivery: all 44 listed file hashes and its three unchanged production records were verified. No admitted interface changed; production funding refusal remains.

Detailed decision material: [claims and source coverage](CLAIM_LEDGER.md), [24 proposed fixtures](FIXTURE_BANK.md), [Lead interface decisions](LEAD_DECISIONS.md), and reports [P0-13](P013.md), [P0-21](P021.md), [P0-22](P022.md), [P0-30](P030.md). Existing executed checks and proposed target fixtures are explicitly separated. Expected fixture hashes/arithmetic were independently derived; full package acceptance was not performed.

**NEXT ACTION:** approve the exact P0-30 offline replay unit and, optionally, the separate P0-21 helper slice.

**WAITING FOR OWNER:** Nothing to finish preparation. The next build scopes require authorization; production and operational gates remain separate.
