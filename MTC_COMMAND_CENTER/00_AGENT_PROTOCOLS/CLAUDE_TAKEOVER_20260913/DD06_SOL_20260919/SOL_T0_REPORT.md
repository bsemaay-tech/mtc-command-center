# DD-06 T0 Independent Review — gpt-5.6-sol xhigh

Candidate: `a46da0aa7a4ea3a58fb00c5e293e10b60307687d`  
Base: `fcac0ac6`  
Review mode: documentary code/record review plus offline fixture tests on scratch copies only. I did not invoke the probe's real `main()`, construct a real venue SDK object, read the registry, place a live acknowledgement/run token/credential in the shell environment, or contact testnet/mainnet.

## Verified identities

| Check | Command / evidence | Result |
|---|---|---|
| Computed HEAD | `git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 rev-parse HEAD` | `a46da0aa7a4ea3a58fb00c5e293e10b60307687d` — exact pin |
| Scope from base | `git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 diff --name-only fcac0ac6 a46da0aa --` | Exactly `IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py` and `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` |
| Tool SHA-256 | `Get-FileHash -Algorithm SHA256 ...dd06_agent_withdraw_probe.py` | `66125f5dbdf4cd1442e6991e70f7eaa0c2df25c7149349dfbe55d19006293c0b` |
| Test SHA-256 | `Get-FileHash -Algorithm SHA256 ...test_dd06_agent_withdraw_probe.py` | `d667762961e66e89bb41099cc1e54feed96a227bb84a31e213dab96a2e61f89a` |
| Round-4 delta | `git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 diff acd79b52 a46da0aa -- <the two paths>` | Only arm order, undetermined fund-arm handling/wording, plan text, and their tests changed. `_paid`, `_attribute`, both execution gates, redaction/write guards, and the `offline` fixture have no delta hunks. |

## Review matrix

| Item | Verdict | File:line evidence and independent reading |
|---|---|---|
| 1. No mainnet path / no key leak | **Verified, one NIT** | `tools/dd06_agent_withdraw_probe.py:73` hard-codes the testnet URL; `:259-279` implements the network/live-ack and run-token gates; `:835-850` executes both before credential resolution and SDK imports/construction; `:282-287,850` refuses a master key before venue SDK objects; `:98-118,301-334` redacts 40/64-hex before record insertion; `:760-793` provides write-once output and final surviving-hex refusal. Tests at `tests/test_dd06_agent_withdraw_probe.py:124-137,463-576` exercise these controls under the offline tripwires. `del api_key` at tool line 849 is not a meaningful erasure boundary and is not test-fenced: my deletion mutant still passed 32/32 (NIT N-1). |
| 2. Funds cannot leave silently | **Verified for control flow** | Amounts and fund-arm membership are at tool `:78-96`; runtime order B and destinations are at `:605-671`; a NOT_REFUSED fund arm re-reads balances and stops at `:682-701`; ERROR and INCONCLUSIVE fund arms re-read, label, skip later arms, and return at `:702-737`. The owner packet states plainly that non-refused `withdraw3` moves 6 test-USDC off venue (`DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:20-26`). Tests pin stop behavior at test `:249-280,333-391`. Required round-4 mutants killed the branch, return, and order regressions. |
| 3. Classification honesty | **REQUIRED finding R-1** | Response envelopes are separated at tool `:177-209`; explicit validation text reaches `refusal_class=VALIDATION`, does not increment `authorization_refusals` at `:673-681`, and therefore ends `DD06_INCONCLUSIVE` at `:738-747`, as pinned by test `:312-330`. However, `classify_refusal_text` checks broad authorization substrings first (`"not allowed"`, `"agent"`) at tool `:212-256`. My fake-only checks prove `"Withdrawal amount not allowed"` and `"Invalid agent name"` both become AUTHORIZATION, despite the same strings containing the classifier's validation markers. Thus validation-shaped refusals can be counted as DD-06 evidence. |
| 4. Control arm | **Verified** | `control_order_size` delegates to the Bridge helper at tool `:290-298`. The helper at `bridge/broker/hyperliquid.py:72-89` rounds down with the `6 - szDecimals` decimal quantum and significant-figure quantum. For BTC `szDecimals=5`, `76974.0 * 0.9 = 69276.6` is quantized down to `69270.0`; the raw r1 record proves the old `69276.6` rejection. For mids 10,000 through 11,111.11..., the target is 9,000–9,999.99... and the 0.1 quantum permits at most five significant digits; once the target is at least 10,000, the helper's high-price guard makes the quantum at least 10 (with integral prices accepted directly). The r1 six-significant-figure decimal cannot recur for a BTC mid at least 10,000. Test `:140-159` pins the real r1 point and representative bounds. |
| 5. Fixtures versus reality | **Partly representative; R-1 matters** | Fixtures carry both top-level refusal shapes, per-status order errors, clean ok envelopes, the installed SDK's 2xx/non-JSON `{"error": ...}` shape, unified-account `accountValue=0.0` plus spot USDC, partial/unreadable reads, and the exact r3 balance direction (`tests/...:31-111,162-185,361-391,580-772`). They still do not carry every venue refusal sentence or every transfer/status envelope, balance-read lag, concurrent balance/PnL movement, or a second post-arm snapshot. Unknown fund-arm envelopes now stop conservatively, but broad text markers can make a validation refusal look like primary authorization evidence (R-1), and one-shot/amount-threshold attribution can misname unrelated balance drift (NIT N-2). |
| 6. Scope and suites | **Focused suite verified; full suite documentary** | Scope is exactly two files. My mandated pinned-interpreter run on the byte-identical scratch copy produced **32 passed in 0.71s**. The original slice-3 record `LEAD_PYTEST_full_bridge_slice3.txt:1-31` says 1614 passed / 1 skipped; the current round-4 record `REPAIR_R4_20260918/LEAD_FULL_BRIDGE_SUITE_R4.txt:1-30` says 1630 passed / 1 skipped. I did not independently rerun the full Bridge suite under the binding safety rule. |
| Operator abort behavior | **REQUIRED finding R-2** | `_attempt` correctly re-raises `KeyboardInterrupt/SystemExit` at tool `:301-319`, and `_balances` does so at `:337-362`. The initial S0 reads instead catch `BaseException` at `:490-541`. A fake `extra_agents()` raising `KeyboardInterrupt` was swallowed and `run_probe` continued rather than raising before signed arms. The existing test at test `:775-788` covers only an abort inside a falsification arm, so it misses the S0 path. |

## Raw run-record closure

- r1 (`kvm2_dd06_probe_run_OUTPUT.redacted.txt:1-63`) was TESTNET, exited 2 as `ABORTED_CONTROL_ARM_NOT_ACCEPTED`, and recorded `limit_px=69276.6` with `statuses[].error = "Price must be divisible by tick size"`; no transfer arm appears.
- r2 (`kvm2_dd06_probe_run_r2_OUTPUT.redacted.txt:1-129`) accepted and cancelled the rounded control order, then recorded every fund/approval arm as REFUSED with `"Must deposit before performing actions"`; all texts were UNCLASSIFIED and the result was `DD06_INCONCLUSIVE`.
- r3 (`kvm2_dd06_probe_run_r3_OUTPUT.redacted.txt:1-124`) accepted/cancelled the control, saw withdraw3 and usdSend refused, then accepted spotSend and stopped. The public-read record (`LEAD_PUBLIC_READS_after_r3.txt:1-9`) shows agent spot USDC 14.0→13.0 and master 983.987457→984.987457, plus the 1 USDC spotTransfer ledger event: the agent moved its own 1 USDC.

## Independent scratch runs

All commands used the pinned interpreter and scratch-local module/test copies. The only non-scratch import path was the read-only Bridge package. No `HL_*` variable or run token was set by a reviewer shell command. Every `main()` test retained the `offline` fixture, which deletes credential variables and replaces the resolver plus both SDK constructors with tripwires; the suite's live-ack refusal test temporarily monkeypatches `HL_LIVE_ACK` only inside that protected test process to prove the refusal.

Baseline:

```powershell
# cwd C:\tmp\SOL_DD06_SCRATCH\dd06_baseline
$env:PYTHONPATH='C:\tmp\SOL_DD06_SCRATCH\dd06_baseline;C:\tmp\P029_DD06_20260915\IBKR_PAPER_BRIDGE'
& 'C:\tmp\P012_FUNDING_PY312_20260911\Scripts\python.exe' -m pytest tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/tmp/SOL_DD06_SCRATCH/bt_sol_baseline_20260919
```

Output: `32 passed in 0.71s`.

The four mutant runs used the same command, with cwd/PYTHONPATH changed to the named scratch directory:

| Scratch arm | Mutation | Output |
|---|---|---|
| `dd06_m1_drop_inconclusive` | `outcome in ("ERROR", "INCONCLUSIVE")` → ERROR only | **1 failed, 31 passed**; `test_unclassifiable_response_on_fund_arm_is_measured_and_stops` observed ordinary `DD06_INCONCLUSIVE` instead of the fund-arm unclassified stop label |
| `dd06_m2_no_stop` | post-reread `return record` → `continue` | **2 failed, 30 passed**; both transport-error and unclassifiable-response tests observed later arms executed/refused instead of skipped |
| `dd06_m3_withdraw_first` | moved runtime withdraw3 arm back before usdSend | **4 failed, 28 passed**; all-refused order, NOT_REFUSED stop, transport-error stop, and unclassifiable stop tests all detected the regression |
| `dd06_m4_no_del` | deleted `del api_key` | **32 passed**; confirms the line is unpinned and should not be described as an enforced security control |

An expanded fake-only check suite added two positive assertions: an INCONCLUSIVE `approveAgent` ends in ordinary `DD06_INCONCLUSIVE`, and `_paid` uses thresholds 3.0 for withdraw3 and 0.5 for 1-USDC arms while a master increase never counts as payment. Output: **34 passed in 0.65s**.

Independent negative checks:

| Check | Command suffix | Output |
|---|---|---|
| Validation text must not become authorization evidence | `-k sol_validation_text_cannot_count_as_authorization_evidence` | **2 failed, 34 deselected**: both `Withdrawal amount not allowed` and `Invalid agent name` returned AUTHORIZATION instead of VALIDATION |
| S0 operator abort must stop before signed arms | `-k sol_operator_abort_during_s0_extra_agents_stops_before_signed_arms` | **1 failed, 36 deselected**: `pytest.raises(KeyboardInterrupt)` reported `DID NOT RAISE` |

## Findings

### REQUIRED R-1 — validation-shaped refusals can be promoted to DD-06 authorization evidence

At `tools/dd06_agent_withdraw_probe.py:212-256`, authorization markers are tested before validation markers and include context-free substrings such as `not allowed` and `agent`. At `:677-681,738-747`, any such classification increments the authorization count used to emit `DD06_REFUSALS_OBSERVED`. The two independent counterexamples above fail on the candidate. This violates the brief's requirement that a VALIDATION refusal never count as DD-06 evidence.

Required repair: use signer-specific authorization phrases/structure instead of context-free tokens, or make ambiguous overlap conservative (`VALIDATION`/`UNCLASSIFIED`), and add negative tests for at least the two reproduced phrases plus a whole-run case proving they end `DD06_INCONCLUSIVE`.

### REQUIRED R-2 — a one-shot operator abort during S0 identity is swallowed and signed arms continue

At `tools/dd06_agent_withdraw_probe.py:490-541`, the S0 `extra_agents`, `user_state`, and `spot_user_state` blocks catch `BaseException` without first re-raising `KeyboardInterrupt/SystemExit`. The fake `extra_agents` abort test proves the abort does not escape. Because that read is not repeated by `_balances`, the function proceeds through control and falsification arms.

Required repair: re-raise `KeyboardInterrupt/SystemExit` before each broad S0/control-plan catch (as `_attempt` and `_balances` already do), and fence an S0 abort with a test that also asserts no exchange call occurred.

### NIT N-1 — `del api_key` is an unpinned gesture

Deleting tool line 849 leaves all 32 fixtures green. Python `del` removes one name, not all copies of secret material; it is fine as hygiene but should not be claimed as a tested no-leak control.

### NIT N-2 — one snapshot plus a half-amount threshold can misattribute unrelated drift

`_paid` at tool `:365-393` treats any readable accountValue/spot decrease of at least half the arm amount as payment, and `_reread_both_wallets` at `:448-477` takes one immediate snapshot. A sufficiently large mark-to-market decline or concurrent transfer can therefore trigger `DD06_FINDING_MASTER_FUNDS_MOVED`; conversely, read lag can miss the immediate attribution. The stop/result remains conservative and the finding tells the operator to inspect the ledger, so I grade this a NIT for this testnet probe, not another REQUIRED.

### NIT N-3 — ERROR/INCONCLUSIVE findings embed contradictory “was NOT refused” text

The undetermined branch at tool `:702-737` correctly names the response channel, but then embeds `_attribute` text from `:402-445`, whose every branch begins from “was NOT refused.” For an ERROR or unclassifiable response, acceptance/refusal is unknown. Split movement attribution wording from the NOT_REFUSED premise.

### NIT N-4 — non-fund `approveAgent` INCONCLUSIVE has no explanatory finding

The extra check confirms the requested ordinary `DD06_INCONCLUSIVE` result, but `finding` remains `None`. The recorded step is sufficient to diagnose it, though a short end-state explanation would make the record less ambiguous.

## NOT VERIFIED

- The real probe was not run. No credential, registry, SDK construction, network, testnet, or mainnet action was attempted.
- Mainnet parity remains unproven by design.
- The full Bridge suite was not rerun by me; I verified the raw Lead records reporting 1614/1 on slice 3 and 1630/1 on the current round.
- Ruff was not run by me under the binding shell restriction. `REPAIR_R4_20260918/LEAD_VERIFICATION_DD06_R4.md:6-22` records Ruff 7, all pre-existing, and both changed files formatted; this is documentary evidence only.
- Venue response wording, eventual balance consistency, and ledger attribution beyond the supplied redacted records remain venue-shaped facts, not fixture-proven facts.

VERDICT: REQUEST_CHANGES
