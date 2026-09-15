# P012 R34 price correction: Lead review acceptance

The approved price correction implements the supported `HYPERLIQUID_PX_V1` price lattice and preserves positive Python integers and integer subclasses without float conversion. Owner ratification is installed. At 2026-09-11, the Lead accepts the **bounded synthetic price-correction review only**, at source `3faed08866e122158e93c626288873ec58a42e3d` against merged base `3e86faec032407c1af9a75f8b8852222d732f316`. Protected CI and normal integration are separate gates. This document does not accept full P012, production data or trading.

## Independent reviews and execution

| Role | Original report | Result | Personally executed checks |
|---|---|---|---|
| Exact Claude Opus 5, xhigh | [Opus](OPUS.md) | PASS-WITH-NITS | Full gate 558 passed / 0 failed, exit 0; focused 113 passed, exit 0 |
| Exact GPT-5.6 Sol, xhigh | [Sol terminal](SOL.md), [detailed report](SOL_DETAILED.md) | PASS | Full gate 558 passed / 0 failed, exit 0; focused 113 passed, exit 0 |
| Exact Gemini 3.7 Flash High | [Gemini](GEMINI.md) | PASS-WITH-NITS | SUPPLEMENTAL_UNEXECUTED; required corroboration only |
| Lead | [Full gate](LEAD_FULL_GATE.json), [source proof](LEAD_SOURCE_PROOF.json) | Bounded review accepted | Full gate 558 passed / 0 failed, exit 0; focused 113 passed, exit 0 |

The focused tests overlap the full gate suite; these counts are not added together. Both flagships reviewed the same frozen packet (`2f4ac4a45f3511a4dadb7426e2007b687284474bf95bd24f4ea123d1c7b480b8`). The Lead independently matched all 1,415 packet members, 1,360 Git blob identities, the complete 1,354-file tracked `mtc_v2` subtree, and the original 2,792-member Section-16 packet. The [manifest](REVIEW_MANIFEST.json) pins original report bytes and distinguishes provider confirmation from exact CLI dispatch evidence. No native subagent or paid-API fallback was used.

The first Sol acceptance attempt timed out without execution evidence or a verdict. It remains incomplete, never accepting. A fresh Sol run changed approach to execute the mandated QA first and completed successfully. Gemini's first large-input invocation exited 1 without a report; a smaller, explicitly labelled delivery of the same packet's exact excerpts completed through the unchanged guarded helper. Neither completed Opus nor completed Section 16 was repeated. Original preparation failures, raw reports and corrections remain preserved locally.

## Ratification and unchanged identities

The owner said **"ı approve continue"** after a plain-English explanation of the price-only decision and retained checks. Approved original receipt SHA256 `26748c7b7e09aa4830f507d023a54e7f7aa570c836e607dd2377bb9f42adf2f6` becomes successor `cf82b102ba866fa08a86d8a6cb52ed43c2e2f2b71e35b081304e09e5aa368f11` through changes only to `owner_ratification.ratified` and `signed_at`. Every substantive verdict, qualification, evidence identity and the chain through #34 is unchanged.

The Lead directly verified that reviewed `b7975ae6c935c461c479768c5f252f930fbc1800` is an ancestor of the candidate and the successor changes exactly the installed receipt, the DECISIONS row and the owned resume note. Core tree `ca57ca5e0487f92e05fa68d8217fdde486877a2c`, seal `54f41e7268442e1167946b587a5920a5ffe4baf99e4aa8964ef69e766bedebad`, anchor, harness, catalog, current baseline and design v1.27 are unchanged. Opus disclosed inability to execute Git ancestry commands; Lead and Sol separately verified the actual Git relation. Passing tests alone were not treated as acceptance.

## Findings and preserved corrections

No material price-candidate finding remains. Opus's F1 stale Section-16 manifest status/statement and F2 four incomplete historical anchor transitions are unchanged diagnostics under `HIST-2026-0030`: mode `REPORT_ONLY`, `enforced=false`, five diagnostics total. They remain tracked, not silently repaired or waived. Opus F3 is pure CRLF/LF normalization in four non-sealed documentation files; the Lead verified it directly. Original reports are not rewritten.

Gemini's generated `file:///C:/LAB/Tradingview_LAB_CLEAN/C/...` links are not live candidate paths. Its `C/mtc_v2/...` citations refer to the supplied frozen-packet excerpts, not the foreign canonical checkout. Observations carried from A3 or Lead context are not new full-file reads. Its verdict remains supplemental and unexecuted. Original A2 inconsistent flags, A3 comparator correction and the separate Lead correction of the historical 167/168 typo remain distinct.

For the earlier Sol exploratory replacement-count observation, a count of two alone does not establish a mutation defect. The Lead separately verified PROBE-P012-04-A `kernel/economics.py` byte-identical to C33 `b4e44964f38391518d0c5c5d04f2b41fb4d08237`; this is separate from the instrument-record policy-object change described in Sol's report. Current probe identities and refusal behavior pass the full gate. No source change or suppressed finding follows from that exploratory count.

The baseline field `EXPECTED_SEAL_SHA_consumed` is explicitly a Lead attestation, not proof that the baseline driver consumed the seal. The actual baseline bytes and 34 semantic surfaces remain preserved. G5/G6 use this same frozen scope, executed checks, input-validation/refusal review and evidence-integrity checks; no redundant security-review loop or auditor waiver is inferred.

## Boundary and integration

All six Section-16 dispositions remain `ACCEPTED_WITH_RESIDUAL_RISK`. All **27 production risks**, **ten open Section-19 rows**, and the **five distinct integration duties** remain; these are not interchangeable counts. `NONE_KEEP_REFUSED`, unknown `minimum_quantity`, null human reviewer, minimum notional 10, deferred R29 final-production semantic redo and every production refusal are unchanged. Economics, configuration, goldens and DERIVATIONS are unchanged from the merged base. No production capture, wallet/account action, deployment, trading, paid acquisition or new economic fact is authorized by this review.

This closeout adds only review/evidence documentation and updates the owned resume note. Before integration the Lead must verify its `mtc_v2` Git tree still equals reviewed source, then require `Bridge suite (Python 3.12)` green on the actual final PR head and merge normally with an exact-head guard. CI success or merge is not claimed by this pre-integration record; consult the PR's actual checks and merge receipt. Preserve foreign checkouts and original evidence.

NEXT ACTION: current-head protected Bridge CI and normal authorized PR integration of the bounded price correction.
WAITING FOR OWNER: Nothing for this authorized continuation. Later production-data decisions remain separate.
