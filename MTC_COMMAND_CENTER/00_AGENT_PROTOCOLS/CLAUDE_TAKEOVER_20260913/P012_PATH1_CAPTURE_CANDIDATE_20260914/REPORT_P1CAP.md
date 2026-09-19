# P012 Path 1 Own-Account Capture Report

Status: BUILT, SOURCE-ONLY, NONACCEPTING. No network call was made in this session, no venue data was captured, no account was accepted, and no production adapter was built.

Git note: the requested local commit was not created because `git add` failed to create `C:/LAB/Tradingview_LAB_CLEAN/.git/worktrees/P1CAP_20260914/index.lock` under the read-only `.git` admin path exposed to this sandbox. The attempted command staged only the exact requested paths.

## Design Conformance

| Packet promise | Implementation evidence |
|---|---|
| Use the same read-only SDK surface as the broker | Broker uses `Info.user_fills_by_time` and `Info.user_funding_history`: `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\broker\hyperliquid.py:1887`, `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\broker\hyperliquid.py:1901`. Tool imports `Info` only: `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:23`. |
| Select mainnet/testnet base URL from SDK constants | Broker selection is at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\broker\hyperliquid.py:2180`; tool selection is at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:125`. |
| No Exchange, no key, no signing for capture | Broker imports `Exchange` for write-capable operation at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\broker\hyperliquid.py:2176`; the new tool test asserts the capture tool has no `hyperliquid.exchange`/`Exchange` string at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tests\test_capture_own_account_evidence.py:220`. The capture refuses if `HL_API_WALLET_KEY` is present at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:414`. |
| Preserve immutable original response bytes with sidecars and manifest entries | The SDK subclass captures `response.content` before JSON parsing at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:68`; sidecar verification is implemented at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:403`. |
| Page fills/funding and refuse truncation at documented caps | Broker cap constants are `2000` and `500` at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\broker\hyperliquid.py:1578` and `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\broker\hyperliquid.py:1584`; tool constants match at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:27` and `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:28`. Paging chooses the method/limit at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:259`. |
| Re-query fills/funding and compare identities | The test covers matching pass1/pass2 identities at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tests\test_capture_own_account_evidence.py:108` and mismatch refusal at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tests\test_capture_own_account_evidence.py:140`. |
| Capture account state / clearinghouseState-equivalent read | SDK `Info.user_state` posts `clearinghouseState`; the tool calls `user_state` at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:315`. |
| Derived fill/funding views are labelled and separate | Derived fill rows are labelled at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:335`; derived funding rows are labelled at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:365`. |
| Ownership signature is optional but verified when supplied | Missing ownership evidence is recorded at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:391`; supplied signature recovery is checked at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\capture_own_account_evidence.py:393`. |
| Self-contained signing page, no transaction, no external scripts | The page requests accounts at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\path1_sign_ownership.html:42` and calls only `personal_sign` at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\path1_sign_ownership.html:48`. It is 58 lines. |
| Funding production remains unavailable without approved real binding schema | Existing exporter states production mode remains unavailable until approved schema/source-event digest work exists: `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tools\export_mtc_funding.py:26`. |

## Refusal Codes

- `CAPTURE_REFUSED_KEY_PRESENT`
- `CAPTURE_REFUSED_TRUNCATED`
- `CAPTURE_REFUSED_REQUERY_MISMATCH`
- `CAPTURE_REFUSED_QUERY_FAILED`
- `CAPTURE_REFUSED_MALFORMED`
- `CAPTURE_REFUSED_BAD_ADDRESS`
- `CAPTURE_REFUSED_SIDECAR_MISMATCH`
- `CAPTURE_REFUSED_OWNERSHIP_SIGNATURE`

## Test Output

Focused new tests:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py -q
..........                                                               [100%]
10 passed in 0.88s
```

Existing Bridge suite, unchanged command from `IBKR_PAPER_BRIDGE`:

```text
python -m pytest --ignore=TSP1009B.pytest_tmp_s1r1
====== 33 failed, 1605 passed, 1 skipped, 1 warning in 166.54s (0:02:46) ======
```

The failures are all pre-existing `tests/test_mtc_funding_export.py` staging-location refusals in this sandbox run: pytest placed `tmp_path` under a Git checkout, and `export_mtc_funding.py` refused with `CANDIDATE_STAGING_UNSAFE`. A second attempt to move `TMP`/`TEMP` outside the repo was denied by the environment and again produced the same 33 failure count:

```text
====== 33 failed, 1605 passed, 1 skipped, 1 warning in 162.62s (0:02:42) ======
```

## Not Verified

- No live Hyperliquid mainnet/testnet call was made.
- No account ownership was accepted.
- No capture artifact from a real account was produced.
- No file-source adapter into `export_mtc_funding.py --mode PRODUCTION` was built.
- No production candidate, booking, funding M decision, schema activation, host/deploy action, order, or trade occurred.

## Narrow Adapter Proposal For Reviewers

The narrow adapter should consume a reviewed `CAPTURE_MANIFEST.json` plus original response bytes, verify every sidecar, and emit schema-v10 retained funding payload rows only after an explicit owner-approved production binding schema exists.

Minimum retained-row shape should match the closed row the exporter tests hand to the pure function: `event_id`, `symbol`, `attribution`, `ledger_effective_ts`, `payload_digest`, `payload`, and `payload_reason` at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\tests\test_mtc_funding_export.py:119`. The retained payload itself must be exactly `FundingEventRecord.authoritative()` fields: `event_id`, `symbol`, `amount_usdc`, `effective_ts`, `source`, `funding_rate`, `position_szi`, and `n_samples` at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\engine\types.py:1040`. Store retrieval already refuses missing schema-v10 capability and damaged retained bytes at `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\store\db.py:9898` and `C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE\bridge\store\db.py:9919`.

The adapter should add no order association, interval completion, account ownership, or venue-origin fact unless those facts are separately present and hash-bound in the reviewed capture packet.
