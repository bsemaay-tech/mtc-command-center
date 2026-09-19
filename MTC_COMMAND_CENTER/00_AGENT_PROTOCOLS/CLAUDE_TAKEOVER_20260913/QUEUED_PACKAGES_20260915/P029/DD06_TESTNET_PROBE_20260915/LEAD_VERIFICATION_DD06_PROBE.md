# LEAD_VERIFICATION — WP-P0-29 DD-06 testnet falsification probe, candidate `69377d6b9b3322266c1716c78d82cc68d62ac8ef` (slice 2) — 2026-09-15 15:26Z

**Authority:** `OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1` (owner "testnet agent-withdraw test: go", ~13:10Z, relayed by session 4) = PREPARATION only. **Result: prepared by the Lead (disclosed), green, committed on `feature/p029-dd06-testnet-probe-20260915` from `origin/master` `fcac0ac6` (slice 1 `71cde24e`, slice 2 `69377d6b`), pushed; NOT executed; NOT reviewed by a flagship; NOT accepted.** Execution needs the owner's second word ("probe steps approved") and runs from the KVM2-P4-03 environment on TESTNET.

| Item | Fact |
|---|---|
| Files (2 added, 0 modified) | `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` (558 lines), `IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py` (347 lines) |
| Refuses to start when | `--network` ≠ testnet; `HL_LIVE_ACK` present; the key in `HL_API_WALLET_KEY` derives to `HL_ACCOUNT_ADDRESS` (a master key) |
| Sequence | S0 `extraAgents` + `user_state` (recorded); S1 control: resting BTC bid at 90 % of mid, smallest size ≥ $10.5 notional, then cancel (must be accepted; else `ABORTED_*`); S2 arms: `withdraw3` 6 USDC → own bridge-chain address, `usdSend` 1 USDC → self, `spotSend` 1 USDC USDC → self, `subAccountTransfer` (only with `--sub-account`), `approveAgent` (candidate key discarded unseen) |
| Classification (slice 2) | outcome REFUSED / NOT_REFUSED / INCONCLUSIVE / ERROR per arm; every REFUSED arm gets `refusal_class` from the venue's text — AUTHORIZATION (counts) / VALIDATION / UNCLASSIFIED (do not count); result `DD06_REFUSALS_OBSERVED` only if all arms refused with AUTHORIZATION; a NOT_REFUSED fund-moving arm → `DD06_FINDING_NOT_REFUSED` and the sequence stops |
| Record | write-once JSON + sha256; 40/64-hex redaction; `write_record` refuses to persist a surviving 64-hex or 0x-40-hex string |
| Tests (pinned Bridge 3.12; ASCII basetemp) | slice 1 `12 passed`, slice 2 **`14 passed`** (`LEAD_PYTEST_focused_slice2.txt`); full Bridge suite at `69377d6b`: **`1612 passed, 1 skipped`** (`LEAD_PYTEST_full_bridge_slice2.txt`); at `71cde24e`: 1610 passed |
| RED arms (scratch mutants) | m1 stop rule removed → the stop test fails; m2 redaction removed → the redaction test AND the write-once test fail (`write_record` refuses a surviving 64-hex); m3 classifier "everything is AUTHORIZATION" → both classification tests fail |
| Ruff / format / guard | clean / applied / `RESULT: PASS` (`LEAD_RUFF_slice2.txt`, `LEAD_GUARD_slice2.txt`) |
| Gemini detection | attempt 1 on `71cde24e` VOIDED (CLI 503 after a partial report; 22 reads, 9 read failures; SUPPLEMENTAL): F-1/F-2 REQUIRED, F-3/F-4 NIT — all applied in slice 2; attempt 2 on `69377d6b` running in the 15:26Z chain |
| Owner packet | `DD06_TESTNET_PROBE_STEP_PACKET_20260915.md` (steps 0-4, abort conditions incl. a filled control order, outcome semantics, "what this probe does NOT decide") |

## Known limits (stated, not hidden)
- The probe cannot answer the sub-account arm without a testnet sub-account (skipped by default).
- A self-send refusal could be a validation refusal; slice 2 classifies it as such and makes the run INCONCLUSIVE rather than counting it.
- Mainnet parity is assumed, never proven; DD-06 can move to "evidenced on testnet" at most.

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
