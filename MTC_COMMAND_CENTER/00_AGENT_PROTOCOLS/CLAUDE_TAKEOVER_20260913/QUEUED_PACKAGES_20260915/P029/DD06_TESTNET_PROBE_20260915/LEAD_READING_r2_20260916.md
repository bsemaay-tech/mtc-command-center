# DD-06 testnet probe r2 — Lead reading — 2026-09-16 08:12 UTC+3 (05:12Z)

**Authority:** `OD-20260916-P029-DD06-R2-GO-1` (owner `r2 go`, 08:05 UTC+3). Script = slice 3 `1af85067` (blob `96d5052e…`, verified on KVM2 before the run). Host contact as the smoke: SSH `baris`, `sudo -n`, root-sourced env, `runuser -u mtc-bridge`, `timeout 300`, sed redaction. Console: `kvm2_dd06_probe_run_r2_OUTPUT.redacted.txt`; record on the host `/tmp/dd06_20260916T051205Z/DD06_PROBE_RECORD.json` sha256 `7f42dda1…` (4 146 B; the script redacts every address before writing, so the on-host record carries none either). Bridge service DISARMED before and after, `NRestarts 0`. Venue time used: 10 s.

## What happened (run `dd06-testnet-20260916T051205Z-r2`, exit 2, result `DD06_INCONCLUSIVE`)
| Step | Outcome | Venue text / data |
|---|---|---|
| S0 | recorded | two registered agents (`MTC-bridge-test`, `kvm2-bridge`); perp `accountValue 0.0`; **spot USDC 998.987457** (unified account) |
| S1 control order | **NOT_REFUSED — accepted** | BTC bid 0.00016 @ 68463.0 (tick-valid), resting oid `60243885325` |
| S1 control cancel | **NOT_REFUSED — cancelled** | `statuses: ["success"]`; public `openOrders` after the run: `[]` |
| withdraw3 (6 USDC → own bridge-chain address) | **REFUSED**, class UNCLASSIFIED | `Must deposit before performing actions. User: <address>` |
| usdSend (1 USDC → own account) | **REFUSED**, UNCLASSIFIED | same text |
| spotSend (1 USDC USDC → own account) | **REFUSED**, UNCLASSIFIED | same text |
| approveAgent (`dd06-probe-candidate`; key discarded unseen) | **REFUSED**, UNCLASSIFIED | same text |
| subAccountTransfer | SKIPPED (no testnet sub-account) | — |
Public check after the run (Info API, read-only): no resting order; agents unchanged (no `dd06-probe-candidate`); master spot USDC unchanged 998.987457.

## Reading (Lead; the script's own verdict stays INCONCLUSIVE by its pre-written rule)
- The agent key **can act** as an agent (the control order rested and was cancelled) and **could not** withdraw, send, or approve an agent — every fund-moving arm was refused. The refusal text is not an authorization sentence; it says the acting **user must deposit first**.
- Who is that "user"? The master account is funded (998 USDC) and had just traded through the same key, so the venue is not talking about the master. The four refused actions are *user-signed* actions (EIP-712, signed by the wallet that owns the funds); when the AGENT key signs them, the venue attributes the action to the **agent wallet's own identity**. Public reads after the run: both agent wallets (`0xfe7d…965b`, `0xfa06…8504`) hold **zero** perp and spot balances — exactly the state that yields "Must deposit before performing actions". The on-host record is address-free by design, so the "User:" value was not resolved from it; the inference rests on the two public balance reads plus the funded master.
- Consequence for DD-06: on testnet, **the Bridge's agent key cannot move the master account's funds through withdraw3 / usdSend / spotSend and cannot approve agents** — those actions run on the signer's own (empty) account. This is primary evidence *for* the agent-withdrawal restriction, but of the indirect kind (attribution, not a stated prohibition). Per packet §4 an INCONCLUSIVE run "changes nothing"; the register row stays BLOCK until the owner amends it on this reading or a sharper probe closes the inference.
- Sharper probe (owner's call, r3): put a few testnet-faucet USDC **into the agent wallet itself** and re-run; if withdraw3/usdSend then succeed from the agent's own balance while the master's 998 USDC is untouched, the attribution is proven directly (agent actions = agent's own account). Zero real-money risk; needs the owner to fund the agent address from the testnet faucet (the address is public; the Lead can put its short form in the ask).

## What this does not decide
Mainnet parity (never probed with real money); sub-account transfers (no testnet sub-account); anything about Section 19 or the Bridge's production admission.

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
