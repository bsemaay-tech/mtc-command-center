# P0-12 funding-retention local T0 acceptance record

Task WP-P012-FUNDING-RETENTION-20260911. Owner approval OD-20260911-FUNDING-1 / HIST-2026-0042. Reviewed source8fe2ede61ca8bf6cd6c564063680542e6101b276 over base d1485eee5b2cc02f85d81610d89b7ec7bbf46a6a.

Lead reconciliation: PASS for this bounded normalized-payload persistence package. Fresh exact Opus5 xhigh and Sol xhigh both PASS; each personally ran1467full/275focused tests with exit0 and independent negative checks. Mandatory Gemini3.7 corroboration completed as SUPPLEMENTAL_UNEXECUTED; read GEMINI_QUALIFICATION.md alongside its original report. Protected current-head CI and normal PR integration remain mandatory; this local record does not bypass them or grant runtime authority.

The change retains the existing eight-field FundingEventRecord.authoritative() canonical payload atomically beside each new funding ledger row when schema10 is explicitly selected. Default4, predecessor4-9 behavior, no downgrade, existing identity/digest and null semantics remain. Historical missing payloads remain unavailable; no silent backfill or venue interpretation.

Lead independently reproduced the old restart-data loss (RED), repaired restart retrieval (GREEN), a suppressed-persistence mutation failure, all1467candidate tests and275focused tests. A call-trace proved the accepted-checkpoint rollback test reaches its injected payload failure for0xfund2 once. Baseline1423tests passed. All data are synthetic; no real database, host, broker, capture or deployment was involved.

## Required findings and optional observations

No required finding remains. Sol reported no findings. Opus observations:
- Contract lines576-577 omit FUNDING_PAYLOAD_IDENTITY_MISMATCH from a non-exhaustive example list. This is optional documentation completeness; the decoder implements the refusal and independent Sol/Lead evidence covers it. The reviewed contract is preserved rather than changed for a nonblocking nit. Opus's reported lines50-52 were inaccurate.
- Required stage handoff is completed in the final factual writeback; it was deliberately Lead-owned and absent from the implementation-only candidate.
- Opus's custom tamper probe failed closed on reopen. Direct read-path damage is separately exercised by the executed focused tests and Sol's independent integrity probe. This is an evidence-limit disclosure, not an omitted required check.

Sol's baseline hash2ccb7285865f5a6794d2f5d17d4ce745118faee7 names IBKR_PAPER_BRIDGE/bridge, not the whole Bridge directory; the whole baseline Bridge tree is649284c92a269c4716100189399256eed8091993. Both were independently verified against base and the baseline checkout. Its initial command-binding exit4 collected no tests; the successful complete run is the acceptance evidence.

The earlier OpusPro attempt passed both suites but reached its subscription limit before a verdict, so it is not an accepting review. An isolated Max launch first failed before inference on PowerShell pipeline binding; the corrected fresh Max session completed with exact Opus5. Actual assistant messages all identify Opus5; no agent tool was called. Auxiliary Haiku usage appears in CLI telemetry, but it is not an accepting reviewer or model substitution. No telemetry cost estimate is presented as a PAYG charge.

The primary builder was stopped during wrap-up after unrequested Claude auto-memory writes. Scoped source/test artifacts were preserved and independently verified. Prior memory indexcontent was recovered from the actual pre-compaction read, and its newnote quarantined. Original line-ending byte identity had not been captured, so only content restoration is claimed. Subsequent Claude reviewers had auto-memory disabled for their own process. Raw private memory/provider records remain outside this repository.

Original reports are retained. MANIFEST.json identifies each public file's working bytes and canonical staged Git bytes; newline normalization does not alter the original frozen packet identity16f14641b51ecc30a953605072f18784e665038c62fc3208a22d67850217c4a1.

R34/R35 and the entire MTC v2 tree remain unchanged. All production risks/refusals and unanswered venue questions remain open. This is not raw HTTP retention, venue authenticity, full history coverage, final MTC funding export, full P012 acceptance or runtime activation.

NEXT ACTION: confirm protected PR integration, then use this prerequisite in a separately scoped funding-export proposal while authoritative venue evidence remains pending.
WAITING FOR OWNER: Nothing for this approved package.
