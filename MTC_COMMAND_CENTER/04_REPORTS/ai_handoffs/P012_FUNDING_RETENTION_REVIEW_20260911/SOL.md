# WP-P012-FUNDING-RETENTION-20260911 — Sol T0 acceptance review

## Verdict

**PASS** for the exact bounded funding-payload-retention package at candidate `8fe2ede61ca8bf6cd6c564063680542e6101b276` over base `d1485eee5b2cc02f85d81610d89b7ec7bbf46a6a`.

Reviewer role: fresh independent accepting reviewer, exact `gpt-5.6-sol`, `xhigh`. This reviewer was not a builder or repair author. Native Sol is transparently not an additional subscription-backed CLI worker.

This verdict accepts only the local additive schema-v10 persistence/evidence scope in the frozen packet. It does not accept R34/R35 again, broader P012, venue facts, raw HTTP evidence, production readiness, deployment, trading, or live data.

## Findings

### Required findings

None.

### Optional findings

None.

## Frozen identity and scope verification

- `C:/tmp/P012_FUNDING_PACKET_20260911/MANIFEST.json` SHA-256: `16f14641b51ecc30a953605072f18784e665038c62fc3208a22d67850217c4a1`.
- Manifest verification: 61/61 members present; every declared byte count and SHA-256 matched.
- Packet/source binding: 20/20 `PACKET.json` Git blob identities matched candidate Git objects.
- Source checkout before and after execution: branch `feature/p012-funding-evidence-retention`, HEAD `8fe2ede61ca8bf6cd6c564063680542e6101b276`, tree `de404d406ffe1c05f0012a529d87df47eefb2f64`, empty `git status --porcelain=v1 --untracked-files=all`.
- Candidate MTC v2 tree: `e648a48534270a1ed98799734fc9f587aea7d09e` (unchanged R34/R35 surface).
- Candidate Bridge code tree: `c0ad3706d460377a44fe13ce32dff37b668d9274`; tests tree: `fcb4788d7e1e26323a2acdd703e448b7d9eeea7a`.
- `FundingEventRecord`/canonical digest source blob remained `3598f95f4c3829b85e096d4da09caee8c5e8539f`; broker normalization blob remained `8b7d616a2b421eb56f6abca1db6d8b3e26d2538d`.
- Exact diff: nine declared paths, 1,617 insertions and 8 deletions. The five implementation/test/doc paths, three governance paths, and the approved `test_partial_fill_protection.py` target `10 -> 11` repair are the only changes. `git diff --check` passed.
- No `.pytest_cache` directory was created in the source tree.

## Standards review

No documented-standard breach or material baseline code smell was found. The change follows the existing Store migration/transaction/topology-validation patterns, keeps the default schema target at v4, treats v10 as an additive successor for all predecessor capability predicates, and preserves no-downgrade behavior. DDL topology, integrity, foreign keys, retained rows, and append-only triggers are revalidated on reopen. Migration failure rolls back the additive object and version bump, then records only the exception class in the existing meta-evidence style.

The retention write is reached from the real `finalize_reconcile_attempt()` transaction through `_append_funding_event_locked()`. It applies to every newly inserted funding ledger row, including evidence from a nonaccepted composite attempt. A failure propagates through the existing transaction rollback before an accepted checkpoint or pointer can advance. Replay returns only after verifying the immutable ledger digest; identity conflict aborts the transaction without altering either durable row.

## Specification review

The diff implements the approved behavior without a wider economic or venue interpretation:

- Schema v10 stores exactly the existing eight-field `FundingEventRecord.authoritative()` canonical JSON and repeats the existing digest. `bridge/engine/types.py` is unchanged, and the independently specified fixture reproduced digest `77fb9ccfc5d2dddf90d53b7e2c924b5b240e849cb934dc1633734c3a62bd4a73`.
- New v10 rows retain payload and ledger atomically. Exact replay remains one ledger row and one payload row; changed identity remains a conflict. Historical v4-v9 rows are neither backfilled nor reconstructed and return explicit unavailability.
- Verified read distinguishes inactive schema, unknown event, unavailable history, malformed/noncanonical JSON, domain drift, digest damage, and identity damage. Optional nulls remain null.
- Migration/reopen validation fails closed on missing/altered topology, orphans, integrity/foreign-key failure, malformed retained content, and failed version transition.
- No broker normalization, risk/order/KILL/economic logic, runtime default, MTC v2 content, raw HTTP representation, price/oracle/coverage claim, or production field was added.

## Personally executed evidence

Interpreter: `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe`, Python 3.12.12. Every run used `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, external `TEMP`/`TMP`, `-p no:cacheprovider`, and an external `--basetemp` where pytest was used.

| Check | Actual result | Exit | Evidence |
|---|---:|---:|---|
| Full Bridge suite, exact documented ignore | 1,467 passed; 0 failed; 0 errors; 0 skipped; one existing Starlette deprecation warning | 0 | `results/full.stdout.txt`, `results/full.stderr.txt`, `results/full.xml`; JUnit SHA-256 `4ece5db368299bdc00e7e3c584fd93f0727b47ae4433fe782dc3e961cc21d205` |
| Focused retention/store/reconciliation suite | 275 passed; 0 failed; 0 errors; 0 skipped | 0 | `results/focused.stdout.txt`, `results/focused.stderr.txt`, `results/focused.xml`; JUnit SHA-256 `4a3e5b19a0923fae810337adcfbb4d957585d5c07d3048da38b242fa68e92dbe` |
| Baseline restart probe on Bridge tree `2ccb7285865f5a6794d2f5d17d4ce745118faee7` | normalized fields unrecoverable after restart (expected RED) | 1 | `results/retention_baseline.*` |
| Candidate restart probe | exact normalized payload recovered after restart (GREEN) | 0 | `results/retention_candidate.*` |
| Persistence-suppression mutant in reviewer scratch | restart assertion failed as required; 1 failed | 1 | `results/persistence_mutant.*`; JUnit SHA-256 `ab8d9d9a31c0ec897abaee6c62aea5a2e1b46ddbf5286e7667afdf57651c1278` |
| Checkpoint causality probe | actual payload-write fault hook reached once for `0xfund2`; test passed | 0 | `results/checkpoint_causality.*` |
| Independent integrity/retention probe | retained nonaccepted evidence; inactive/unknown/unavailable and malformed/domain/digest/identity outcomes all reproduced; frozen fixture digest matched | 0 | `results/independent_integrity.*` |

The first attempted full-suite command did not collect tests: PowerShell split the JUnit option value into a positional path, producing exit 4 and `file or directory not found ...full.xml`. I corrected only that invocation syntax and reran from the same clean candidate. That pre-collection failure is not counted as suite evidence; the table records the subsequent complete run. Its temporary stdout/stderr filenames were overwritten by the successful run, so this qualification preserves the observed failure rather than presenting reconstructed raw logs.

## Source guards

- Before: `source_guard_before.txt` — clean candidate and exact candidate/Bridge/tests trees.
- After: `source_guard_after.txt` — same branch, HEAD and tree; clean status; exact MTC v2/Bridge/tests identities; `git diff --check` exit 0; no source pytest cache.
- All test databases, mutation copies, basetemp paths, stdout/stderr/JUnit files, and probes were confined to `C:/tmp/P012_FUNDING_SOL_T0_20260911`.

## Limitations and remaining gates

- All execution used synthetic local SQLite data. No network, host, broker, credential, account, TESTNET/mainnet, production database, API, paid route, or live action was used.
- I did not rerun the 1,423-test base full suite. I verified its frozen packet record and independently reproduced the retention RED against a checkout whose Bridge tree exactly equals the candidate base Bridge tree. Candidate acceptance does not rely on the base count because I personally ran the complete candidate suite and focused suite.
- This review does not establish Hyperliquid venue meaning, authenticity, history completeness, settlement-oracle association, or final MTC funding mapping.
- This Sol PASS is one required T0 flagship verdict. Exact Opus acceptance, mandatory Gemini corroboration reconciliation, independent Lead acceptance, current-head protected CI, and the authorized normal integration gates remain separate.

NEXT ACTION: Lead reconciles this report with the exact Opus and Gemini records, rechecks the candidate identity, then runs protected current-head CI before any normal integration.

WAITING FOR OWNER: Nothing.
