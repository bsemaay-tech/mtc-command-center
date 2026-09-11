# R35 native Sol T0 acceptance review

Verdict: **PASS-WITH-NITS**

Route: fresh native `gpt-5.6-sol`, `xhigh`, independent read-only acceptance reviewer. This was not a subscription-backed CLI lane. I spawned no children, contacted no network/provider, accessed no credentials, edited no repository source, and mutated no Git state.

Scope: the bounded R35 two-string instrument-record prose correction and its necessary evidence/identity refresh. This verdict is not CI, merge, full P012, production, deployment, trading, or new-fact acceptance.

## Standards

PASS-WITH-NITS. The installed candidate follows the repository's T0 review, protected-path, receipt, and manual trailer rules. Commits `8f3ebe61`, `e98e13a5`, `95dbee51`, and `a593b29d` each carry `APPROVED-PATCH-PLAN: WP-P012-RECORD-PROSE-20260911`, and `TASK_HISTORY.json` contains the corresponding `APPROVED` event.

The final packet manifest SHA-256 is `3c6b66d4a6412e55cd21820a3ddd285aad3255bd39651851dc6454dbf3071bc6`; I recomputed all 7,033 listed member hashes with zero mismatch. The nested prior-review manifest is `ce231c20d713706123e40a541d70e4f57ea8db44c5cb43b2594df3c724a57361`; I recomputed all 5,604 listed member hashes with zero mismatch. All 1,354 files under final `CAND/mtc_v2` match the exact Git blobs at installed HEAD, with zero missing, extra, or mismatched members. Governance and payload packet blobs also match their corresponding Git blobs.

Optional nits:

1. `core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json:200` retains the phrase “effective increment coarser at BTC magnitudes.” It is ambiguous beside the explicit integer exception, although it does not state a mandatory 10-unit step and the corrected `field_basis.price_tick` text is accurate.
2. The full gate's owner-approved report-only declared-field check reports `manifest.section_16_review.status` as `PENDING` while the installed ratified receipt validates. This is not an acceptance blocker and changing the sealed manifest would require a new reseal; record it as a metadata consistency limitation for future authorized cleanup.

## Spec

PASS. Actual installed HEAD is `a593b29dca30c45bb8c183db04429e29d9b86e27`; `e42fa192507d77e2d1765702a4a9f54e56ad793f`, `e98e13a561d82af4c3dda0830af7d5c1a9637c0d`, and Section-16 reviewed source `95dbee5183f4256bf9cf4c5bbd893d7172bd56a9` are ancestors. The final successor changes exactly `DECISIONS.md`, the installed receipt, and the owned memory note after `95dbee51`. Core tree remains `ad06d9723484d7fa7e220096a1ec9247197f7f29`; seal remains `6f44d5beb9e2ed20fae65508bb01a01d1840258dfceb5109c9be20ab615dadd8`.

The production record changes only `/status` and `/field_basis/price_tick`, plus the detached digest. The status now matches accepted OPEN-01 addendum 16 row 42 while explicitly preserving refused production admission. The price explanation now accurately states the five-significant-figure/non-integer decimal rule and the unconditional positive-integer exception, including `100001`. Executable core is byte-identical to R34. The loader does not consume `status` or `field_basis`; evaluation still refuses null `minimum_quantity` and null `provenance.human_reviewer`. `minimum_notional` remains 10. No event/result surface or production fact changed.

I independently compared the frozen current/prior baselines: all 17 scenario directories are present and all 34 event/result surface files are byte-identical. The 27-row catalog remains 9 RED, 8 GREEN, and 10 probes. Ten OPEN items remain. Each prior receipt item's full notes are an exact prefix of its R35 successor, preserving the 27-risk inventory and six `ACCEPTED_WITH_RESIDUAL_RISK` dispositions; the sole new evidence path per item is the R35 Lead envelope.

Installed receipt SHA-256 `ed4f4f2fd74bb3c4677be95af75ff952ad2437897dccee9c02d373274bb790eb` exactly matches the ratified successor. Compared with unratified `3672ed30b9b56173104918b13d39829243508d2961a21ea05232b6df6a92815e`, only `owner_ratification.ratified` (`false` to `true`) and `signed_at` changed. The chain has 33 entries through `#35`. For each item 1-6, the installed receipt contains the corresponding original A1 JSON reason and contains none of the schema-wrong/remapped A2 JSON reasons.

Section-16 limitations remain disclosed: A1 alone read only 485/735 delta lines; same-author A2 completed actual combined coverage to 735/735 but made four successful same-session compaction-history reads outside the packet. Those reads are excluded from packet evidence. A2's wrapper corrections are valid, but its replacement JSON is not assembler input. I did not personally reread the 189 accepted R34 hunk bodies; carry-forward rests on accepted R34 judgments plus frozen identity for this limited two-string delta. Deferred R29 semantic redo remains deferred.

## Personal execution

Environment for both commands: `PYTHONPATH=C:/tmp/P012_RECORD_PROSE_20260911/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, and `TMP`/`TEMP=C:/tmp/P012_R35_NATIVE_SOL_T0_20260911/scratch`.

1. `C:/Python314/python.exe -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --root C:/tmp/P012_RECORD_PROSE_20260911/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2 --baseline-root C:/tmp/P012_PROSE_BASELINE35_20260911/CURRENT --output C:/tmp/P012_R35_NATIVE_SOL_T0_20260911/results/full_gate.json`
   - Exit `0`; 558 passed, 0 failed; zero acceptance blockers; provenance `MATCH`; 17 scenarios/34 surfaces `MATCH`; 10 probes detected; seal `6f44d5beb9e2ed20fae65508bb01a01d1840258dfceb5109c9be20ab615dadd8`.
   - Output SHA-256: `d10b0135cd20901f4732b289f0fc0e60e00856f4ef2b3a153a7f1587c0d659d6`.
2. `C:/Python314/python.exe -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_price_alignment_policy.py mtc_v2/tests/corrected_vnext/contracts/selftests/test_economic_records.py mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py -q -p no:cacheprovider --basetemp C:/tmp/P012_R35_NATIVE_SOL_T0_20260911/scratch/pytest-temp --junitxml=C:/tmp/P012_R35_NATIVE_SOL_T0_20260911/results/focused.xml`
   - Exit `0`; 113 passed in 0.49s.
   - JUnit SHA-256: `6b55b9286de7195ae386d3fcdc5ae90ffd77ac629286b55111e5d2329f0cf4c0`.

Git status was empty before execution, after execution, and after final packet inspection.

NEXT ACTION: Lead may reconcile this bounded Sol verdict with the independent Opus result and mandatory Gemini 3.7 corroboration, then proceed through current-head protected CI and the separately authorized conditional integration path.

WAITING FOR OWNER: Nothing for this bounded review.
