# DD-06 testnet probe r3 — Lead reading — 2026-09-16 12:0x UTC+3 (09:0xZ)

**Authority:** `OD-20260916-P029-DD06-R3-GO-1` (owner `r3 go`, 11:5x UTC+3) after the owner funded the `kvm2-bridge` agent wallet himself from his own testnet wallet (14.0 USDC, fee 1.0, 08:57:33Z; guide given in chat). Script = slice 3 `1af85067` unchanged (blob `96d5052e…`, verified on KVM2 before the run, mode 0444). Host contact = r2's shape (`kvm2_dd06_probe_run_r3.sh`: SSH `baris` via the Windows OpenSSH client, `sudo -n`, root-sourced env, `runuser -u mtc-bridge`, `timeout 300`, sed redaction on the way out). Console: `kvm2_dd06_probe_run_r3_OUTPUT.redacted.txt`; on-host record `/tmp/dd06_20260916T090046Z/DD06_PROBE_RECORD.json` sha256 `e13b8939…` (3 688 B; address-free by design). Service DISARMED before and after, `NRestarts 0`. Venue time used: 12 s (09:00:47-09:00:59Z).

## Pre-written reading rule (chat + DECISIONS row, before the run)
Agent account = classic (no `tokenToAvailableAfterMaintenance`), 14.0 USDC spot / 0 perp; master 983.987457 spot. withdraw3/usdSend draw on perp USDC → VALIDATION-class refusals expected, non-decisive. spotSend 1 USDC → if NOT_REFUSED the script stops with `DD06_FINDING_NOT_REFUSED`; the public balances decide whose funds moved: agent 14.0→13.0 with master +1 = the agent's OWN funds (attribution proven); master decreasing = restriction FALSIFIED.

## What happened (run `dd06-testnet-20260916T090046Z-r3`, exit 2, script result `DD06_FINDING_NOT_REFUSED`)
| Step | Outcome | Venue text / data |
|---|---|---|
| S0 | recorded | two registered agents; master spot USDC 983.987457 |
| S1 control order | NOT_REFUSED — accepted | resting oid `60256197751` (tick-valid, as r2) |
| S1 control cancel | NOT_REFUSED — cancelled | `statuses: ["success"]` |
| withdraw3 (6 USDC → master's bridge-chain address) | REFUSED, UNCLASSIFIED | `Error withdrawing from bridge` |
| usdSend (1 USDC → master) | REFUSED, **VALIDATION** | `Insufficient balance for withdrawal.` — the venue checked the SIGNER's (agent's) perp balance (0), not the master's |
| spotSend (1 USDC USDC → master) | **NOT_REFUSED** | `{"response": {"type": "default"}, "status": "ok"}` → stop rule fired |
| approveAgent | SKIPPED_AFTER_FINDING | — |
| subAccountTransfer | SKIPPED (no testnet sub-account) | — |

## Public reads after the run (Info API, read-only, `LEAD_PUBLIC_READS_after_r3.txt`, 09:01:19Z)
- **agent `0xfa06…8504`: spot USDC 14.0 → 13.0**; perp 0.0.
- **master `0x1E26…AC49`: spot USDC 983.987457 → 984.987457** (+1.0).
- agent ledger: `spotTransfer` 09:00:58Z `user = 0xfa06…8504` (the agent), `destination = 0x1e26…ac49` (the master), 1.0 USDC, fee 0.0.
- master `openOrders []`; master `extraAgents` unchanged (`MTC-bridge-test`, `kvm2-bridge`); agent `extraAgents []`.

## Reading (Lead)
1. **The attribution is proven directly.** A fund-moving action signed with the Bridge's agent key acts on the **agent wallet's own account**: the agent's spot balance fell by exactly the sent amount and the master's rose by it; the venue's ledger names the agent as `user`. The r2 inference ("Must deposit" = the signer's own empty account) is confirmed by the r3 balance movement.
2. **The master's funds were never reachable through the agent key** in r1/r2/r3: withdraw3 and usdSend failed for lack of balance **on the agent's account** while the master held 983-998 USDC the whole time; spotSend moved only what the agent itself held.
3. **DD-06 restriction (the Bridge's agent key cannot withdraw or send the master account's funds): VERIFIED on testnet with direct evidence.** Mainnet is not probed (never with real money); the same venue rule (user-signed actions attribute to the signing wallet) is what the probe exercised, so the reading transfers as venue behaviour, not as a mainnet measurement.
4. The script's own label `DD06_FINDING_NOT_REFUSED` was written for the dangerous case ("an arm moved funds") and cannot tell whose funds moved; the pre-written rule + public balances did that. Probe follow-up (not now): a slice that reads both balances before/after and classifies OWN_FUNDS_MOVED vs MASTER_FUNDS_MOVED.

## What the owner may now do (one-liner; default = nothing moves)
`DD-06 amend` → the Lead changes the P0-29 register row DD-06 from BLOCK to "RESTRICTION VERIFIED on testnet (probe r3, 2026-09-16, direct evidence); mainnet not probed; Bridge agent key cannot move master funds" and folds the r1-r3 outcomes into the venue addendum §E on the docs branch. Without the word the row stays BLOCK.

## Residue on testnet
The agent wallet keeps 13.0 testnet USDC (harmless; useful if a further arm is ever needed). No order rests; no agent was added; the Bridge service was untouched.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
