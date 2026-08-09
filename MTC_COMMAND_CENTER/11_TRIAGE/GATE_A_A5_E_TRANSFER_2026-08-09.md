# Gate A A5 run-kit E — transfer and remote verification (2026-08-09)

## Transfer

- Host: existing key-only `gatea-staging` target (`gatea@172.24.55.233`); no credential value read
  or printed.
- Remote tar: `/home/gatea/gatea-run-kit-20260809E-2ce41e34.tar`.
- Remote extraction: `/home/gatea/gatea-run-kit-20260809E-2ce41e34`.
- E evidence log: `/home/gatea/gatea-A5-20260809E.log`.
- Pre-transfer all three paths were absent. SCP rc0; no overwrite occurred.

## Remote package verification

- Tar SHA-256 verified against
  `895fe530f4fe85b9dc0c86332776899c88492197c2748c1de14f950f0e6f1cef`.
- Exact five archive members; exact four extracted files.
- `SHA256SUMS`: README, script and test all OK.
- `gatea_A5.sh`: mode 0755, Bash syntax rc0, 25066 B / 497 LF / CR0.
- README: 35289 B / 495 LF / CR0.
- Test: 59469 B / 1265 LF / CR0.
- Manifest: 248 B / 3 LF / CR0.
- Extracted Linux regression: Bash `/usr/bin/bash`, GNU coreutils timeout 9.4, guard rc124;
  boundary equality and past-deadline scenarios PASS; `SUMMARY total=29 passed=29 failed=0`,
  `RESULT=GREEN`, rc0.

The first inline SSH verification command lost quoting around summary assertions and returned rc1
after tar/manifest/E-GREEN output; it did not alter the package or service. A strict `bash -s`
verifier then exposed a locale-dependent file-order assertion, which was made deterministic with
`LC_ALL=C`; final full remote verification returned rc0 and `REMOTE_EXTRACT_VERIFY=PASS`. These were
verification-wrapper failures, not package or test failures.

## Immediate pre-A5 safe-state snapshot

- E evidence log absent.
- Unit `mtc-bridge-first-start.service`: ActiveState=active, SubState=running,
  MainPID=187338, NRestarts=0, Restart=no.
- Listener count 1; non-loopback count 0.
- API HTTP 200; exact state DISARMED; mode credential_free_disarmed; state_version=1.
- armed, credentials_loaded, broker_connected, exchange_connected, network_enabled all off.
- `PREFLIGHT_SAFE_STATE=PASS`.

No environment file or credential content was read. No service command, SIGKILL, restart, ARM,
broker/exchange, order, TESTNET/mainnet, wallet, or economic action occurred in this unit.

## Next action

Run A-5 exactly once:

```
bash /home/gatea/gatea-run-kit-20260809E-2ce41e34/gatea_A5.sh
```

Preserve `/home/gatea/gatea-A5-20260809E.log` regardless of result. First genuine FAIL stops A-6.
After the run, copy/hash the evidence locally, independently verify final service/API/listener state,
and update `_AI_MEMORY` before any A-6 action.
