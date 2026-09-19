# WP-P0-29 DD-06 — TESTNET falsification probe: step packet for the owner (PREPARED; NOT EXECUTED) — 2026-09-15 night

**Authority:** `OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1` (owner "testnet agent-withdraw test: go", ~13:10Z) = **preparation only**. **Execution needs the owner's second word on these exact steps: "probe steps approved".** Testnet only (faucet money). Host contact on KVM2 is G9 = the owner's hands or one approved command, exactly as the 2026-09-14 smoke (`OD-20260914-BRIDGE-SMOKE-GO-1`).

## 1. The question, in one line
Can the **agent (API) wallet** the Bridge uses — the key in the P4-03 environment — move money out of the account? The venue documents no explicit "agents cannot withdraw" sentence (DD-06 stays BLOCK for that reason). This probe asks the venue directly, on testnet, with the agent key the Bridge already has, and records the answers.

## 2. What was prepared (branch `feature/p029-dd06-testnet-probe-20260915`, worktree `C:/tmp/P029_DD06_20260915`, from `origin/master` `fcac0ac6`)
| Item | Path | Facts |
|---|---|---|
| Probe script (slice 2 `69377d6b`) | `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` | Bridge interpreter (`hyperliquid-python-sdk 0.24.0`); testnet URL hard-coded (`https://api.hyperliquid-testnet.xyz`); refuses `--network` ≠ testnet and refuses if `HL_LIVE_ACK` is set; credentials through the Bridge's `resolve_hyperliquid_credentials()` (env names `HL_ACCOUNT_ADDRESS`, `HL_API_WALLET_KEY` — values never printed); **refuses if the key derives to the account address itself** (a master key in the agent slot); every request/response recorded with 40-/64-hex strings redacted; write-once output dir + sha256; `--dry-run` prints the plan without credentials or network |
| Fixture tests | `IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py` | 12 tests, fake venue objects, no network: testnet/live-ack/master-key refusals; control-order sizing; all arms refused (both refusal shapes: `status: err` envelope and HTTP 4xx `ClientError`) → `DD06_REFUSALS_OBSERVED` with everything redacted; sub-account arm only when named; **a NOT-refused fund-moving arm is a FINDING and stops the sequence**; transport error → INCONCLUSIVE; control-arm rejection aborts before any transfer arm; an uncancelled control order is reported loudly; write-once output; dry-run needs no credential |
| RED arms | `LEAD_RED_ARM_m1.txt` (stop rule removed → the stop test fails), `LEAD_RED_ARM_m2.txt` (redaction removed → the redaction test fails AND `write_record` refuses to write a surviving 64-hex) | run on scratch mutant copies, never on the branch |
| Evidence | `LEAD_PYTEST_focused.txt` (12 passed on 3.12), `LEAD_PYTEST_full_bridge.txt` (full Bridge suite), `LEAD_RUFF.txt` (clean; `ruff format` applied), repo guard PASS | pinned interpreter `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe` |
| Gemini detection review | `P012_S16_REVIEWS_20260913/DD06_PROBE_GEMINI/`: attempt 1 on slice 1 → two REQUIRED + two NITs (all applied as slice 2); attempt 2 on `69377d6b` → **PASS-WITH-NITS by content (tasks 1-8 PASS; two observational NITs, no change)** — both attempts wrapper-voided (CLI 503 after the report) → SUPPLEMENTAL, uncounted; `LEAD_ADJUDICATION.md` | the Lead wrote the probe; the Lead does not accept it; T1 roster before any merge |

## 3. The steps, exactly (what runs when you say "probe steps approved")
| # | Step | Where | Who | Expected | If not |
|---|---|---|---|---|---|
| 0 | Copy the branch's `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` onto KVM2 beside the smoke release copy (`/tmp/…/IBKR_PAPER_BRIDGE/tools/`), verify its sha256 against the commit | KVM2 (`srv1856225`), SSH as `baris`, `sudo -n` | owner's hands or one approved command (G9) | digest equal | stop |
| 1 | `--dry-run` from the release venv: prints the plan, reads no credential, touches no network | KVM2 | same | plan printed | stop |
| 2 | `runuser -u mtc-bridge` with `set -a; source /etc/mtc-bridge/mtc-bridge.env` (as the smoke did): `python tools/dd06_agent_withdraw_probe.py --run-id dd06-testnet-<UTC stamp>-r1 --out /tmp/dd06_<stamp>` under `timeout 300`; stdout/stderr through the smoke's `sed` redaction (`0x`+40-hex, `0x`+64-hex) | KVM2 | same | S0 records `extraAgents` + account value; **S1 control**: resting BTC bid at 90 % of mid, smallest size ≥ $10.5 notional, then cancelled; **S2 arms** each `REFUSED`: `withdraw3` (6 USDC → the account's own address on the bridge chain — above the documented 5 USDC minimum + 1 USDC fee, so a refusal is not an amount refusal; if NOT refused, 6 test-USDC leave the venue to an address you control), `usdSend` (1 USDC → own account, a self-transfer), `spotSend` (1 USDC USDC → own account), `approveAgent` (candidate key discarded unseen); `subAccountTransfer` `SKIPPED_NO_SUB_ACCOUNT` unless you name a testnet sub-account; result `DD06_REFUSALS_OBSERVED`, exit 0 | exit 2 = a FINDING (`DD06_FINDING_NOT_REFUSED` — the probe stopped by itself) or INCONCLUSIVE/ABORTED; exit 3 = refused to start (mainnet / live-ack / master key) |
| 3 | Copy `DD06_PROBE_RECORD.json` + `.sha256` back through the same redaction; the Lead reads only the redacted copy | KVM2 → records | owner | two files | — |
| 4 | Verify on the venue UI that no order rests and no agent named `dd06-probe-candidate` exists (it would only exist if `approveAgent` was NOT refused — a finding) | testnet UI | owner | none | prune it |
Abort conditions (stop and tell the Lead): the Bridge service state changes (it must stay DISARMED / untouched as in the smoke); the control order is not cancelled (`ABORTED_CONTROL_CANCEL_FAILED` — cancel by hand); **the control order fills** (a ~10 % flash move while it rests — unlikely but possible): the probe does nothing about a position; check the testnet UI and flatten by hand before anything else; any real-money flag appears; the record contains an unredacted address (report, do not paste it).
Refusal reading (slice 2, after the Gemini detection review): the script now classifies every refusal by the venue's own words — `AUTHORIZATION` (agent/permission wording) counts for DD-06; `VALIDATION` (amount, token, nonce, self-send, sub-account existence) or `UNCLASSIFIED` makes the run `DD06_INCONCLUSIVE` even if every arm was refused; the Lead re-reads the recorded texts either way. A NOT-refused `withdraw3` means 6 test-USDC **leave the venue** to the owner's own address on the bridge chain — stated plainly, not hidden behind "own address".

## 4. What each outcome means
| Outcome | DD-06 | Record |
|---|---|---|
| `DD06_REFUSALS_OBSERVED` (every arm refused with an AUTHORIZATION-class text; control arm accepted) — **the Lead re-reads each recorded refusal text anyway** | the "agent-withdrawal restriction" gets **primary testnet evidence**: the agent key could act (control) but could not withdraw/send/approve. DD-06 can move from BLOCK to "**evidenced on testnet; mainnet parity assumed, not proven**" — the owner amends the register row; mainnet is never probed with real money | `P029/DD06_TESTNET_PROBE_20260915/` + venue addendum §E |
| `DD06_FINDING_NOT_REFUSED` | an agent could move funds (or approve agents): **DD-06 stays BLOCK with a primary finding**; the custody runbook's least-trust rule (§5 / §8.2) is confirmed necessary; the P0-28 binding spec's "no agent-withdrawal safety boundary" sentence stands with evidence | same + a decision row |
| `DD06_INCONCLUSIVE` / `ABORTED_*` | nothing changes; the Lead reads the record and proposes one re-run with the cause fixed | same |
`subAccountTransfer`: with no testnet sub-account the arm is skipped; if the owner creates one on testnet (faucet money) and passes `--sub-account 0x…`, the arm runs (1 USDC deposit into the sub-account = same owner, no external movement).

## 5. What this probe does NOT decide
- Nothing about mainnet, real funds, the Bridge's production admission (Q2/Q6 unaffected), or Section 19 items.
- It does not prove the venue's rule set is identical on mainnet; it gives dated primary evidence for the documented-nowhere behaviour.
- It does not approve a new agent from a master key (the P4-03 environment holds the agent key only; the probe refuses master keys by design). If the owner prefers a fresh named short-expiry agent for the probe, he approves it in the testnet UI and puts its key in the env — the script is indifferent.

## 6. The morning ask (one line)
"**probe steps approved**" (runs exactly §3 on testnet from P4-03) — or "change: …" — or "not now".

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`). The Lead wrote the script and does not accept it; Gemini detection + the T1 roster apply before any merge to `master`.
