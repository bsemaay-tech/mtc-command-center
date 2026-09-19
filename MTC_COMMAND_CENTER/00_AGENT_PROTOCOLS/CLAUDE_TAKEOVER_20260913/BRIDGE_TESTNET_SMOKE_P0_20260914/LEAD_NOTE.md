# Hyperliquid TESTNET P0 smoke (`tools/smoke_p0.py`) — executed once under the owner's word "smoke GO" — 2026-09-14 14:05Z

Authorization: owner chat, verbatim **`smoke GO`** (~14:03Z), on the lever presented after KVM2-P4-03 (`OD-20260914-BRIDGE-P403-PROVISIONED-1`); documented in `IBKR_PAPER_BRIDGE/docs/06_HYPERLIQUID_SETUP.md` section 5 ("the agent runs this only with your explicit in-session approval — it is an exchange action (even though it is testnet/fake money)"). Row `OD-20260914-BRIDGE-SMOKE-GO-1`.

## How it ran (script `kvm2_smoke_p0_run.sh.txt`, console `kvm2_smoke_p0_run_OUTPUT.redacted.txt`)
- Host KVM2 (`srv1856225`), SSH as `baris`, `sudo -n`. Release `be007fd802bbfd2eb181d66038c374865d1562ee` copied to `/tmp/smoke_p0_20260914T140527Z/IBKR_PAPER_BRIDGE` — tree digest of the copy **equals** the release tree (`f10fa611be30bf90fc8d2ac9efc0a728131caf0d5f447203e8145fef69420c64`, sha256 over the sorted per-file sha256 list); the copy exists only because the tool writes `docs/p0_smoke_log.json` under its own tree and the release tree is read-only (`555 root:root`). Copy chowned to `mtc-bridge`; `docs/` made writable.
- Credentials: root sourced `/etc/mtc-bridge/mtc-bridge.env` (`set -a`), then `runuser -u mtc-bridge` ran the release venv Python (`3.12.3`) on `tools/smoke_p0.py` once under `timeout 300`; the two values existed only in that process environment; nothing echoed; every byte leaving the host passed `sed` redaction of `0x`+40-hex (addresses) and `0x`+64-hex.
- The bridge SERVICE was not touched: before and after `mtc-bridge-first-start.service` active, `NRestarts 0`, `/api/status` `DISARMED` / `credential_free_disarmed`. No ARM. No mainnet (`network="testnet"` is hard-coded in the tool; `HL_LIVE_ACK` absent).

## Result: **PASS**, 12/12 steps, 14:05:28Z → 14:05:40Z (12 s)
| Step | Status |
|---|---|
| `credential_source` | PASS |
| `connect` | PASS |
| `account` | PASS |
| `candles` | PASS |
| `meta_and_plan` | PASS |
| `place_atomic_normalTpsl` | PASS |
| `verify_open_orders` | PASS |
| `modify_stop` | PASS |
| `cancel_owned_orders` | PASS |
| `verify_cleanup` | PASS |
| `partial_fill_guard` | PASS |
| `disconnect` | PASS |

- Testnet account (faucet money): equity 998.987457, available margin 998.987457 (fake USDC); `account_mode` unifiedAccount.
- Market data: three real 1h BTC candles from testnet (12:00Z, 13:00Z, 14:00Z; last close 78420.0).
- Order plan: LONG BTC resting limit at 70578.0 (90 % of market — cannot fill), qty 0.00017 BTC = $12.00 notional, native SL trigger 69160.0 → modified to 69510.0; grouping `normalTpsl` (the tool's own scope; the setup doc's `positionTpsl` wording is the older name); both orders visible in `open_orders` (oids 60109082440 / 60109082441), both cancelled, cleanup verified empty, no position change (`partial_fill_guard` flattened nothing), disconnect clean.
- Log: `/tmp/smoke_p0_20260914T140527Z/IBKR_PAPER_BRIDGE/docs/p0_smoke_log.json` on the host, sha256 `323c2fbd01decd9c19c26b5b269a2f577c934d55d9c6069f46f26a25187d7d09` (4,375 bytes, UNREDACTED — contains the public account address); the copy recorded here (`p0_smoke_log.REDACTED.json`) has the address replaced by `0x[REDACTED_ADDRESS]` and therefore has a different digest by design.

## What this is and is not
- It IS the first real testnet exchange evidence for the Bridge plumbing (connect with the API wallet, account, candles, atomic entry+SL placement, resting SL visible, modify, cancel, cleanup) — the P0 smoke the setup document defines.
- It is NOT production evidence: fake money, testnet order book; per the P012 production-admission packet (owner question 2, recommended NO) testnet informs preparation only and closes no Section-19 row or signed risk. It does not change the service's start mode, does not admit the steady profile, does not ARM anything, and grants no live-trading authority.
- Residuals: the tool ran from a scratch copy, not from the sealed release path (byte-identity proven, but the path differs); the scratch copy stays on the host under `/tmp` for evidence (no secrets in it; env values were never written to disk); `install_manifest.json` remains the install-time snapshot.
