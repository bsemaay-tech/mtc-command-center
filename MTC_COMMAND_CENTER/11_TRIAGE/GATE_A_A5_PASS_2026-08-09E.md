# Gate A A-5 PASS — run-kit E (2026-08-09)

## Verdict

**A-5 PASS.** The preregistered E command executed exactly once and returned rc0:

```
bash /home/gatea/gatea-run-kit-20260809E-2ce41e34/gatea_A5.sh
```

Run-kit D's prior A-5 FAIL remains preserved and is not rewritten. Gate state is now:
**A-0..A-5 PASS; A-6..A-9 NOT RUN.**

## Evidence identity

- Remote: `/home/gatea/gatea-A5-20260809E.log`.
- Local preserved copy: `C:\WPI_ARTIFACTS\gatea-A5-20260809E.log`.
- Remote/local SHA-256:
  `83d947a3285a595a1df21652c8c85aa9b8e14a8a0ec2eab229f1384516fdd19c`.
- Bytes: `3284` remote and local.
- Exactly one `A-5 PASS`, one `A5_TRAP_EXIT rc=0`, one `A5_READY=yes`; zero `A5_FAIL`.

## In-script proof

- Preconditions: active; Restart=no; MainPID=187338; NRestarts=0; one loopback listener; exact
  HTTP200 credential-free DISARMED API; DB quick_check=ok, app_state=DISARMED, schema_version=4.
- Deadline guard: proc_uptime monotonic clock; `/usr/bin/timeout`; guard rc124; function-export rc0.
- Authorized SIGKILL: old PID reached MainPID=0; `/proc/187338` absent; after 3 seconds state failed;
  no listener; NRestarts=0; ExecMain result signal/status9.
- Exactly one reset-failed and one explicit start.
- Application readiness: active + nonempty loopback-only listener + exact credential-free DISARMED
  API in the same attempt; monotonic 30-second deadline; elapsed 1.1 seconds; 2 attempts; no second
  start.
- Post: MainPID=189813; NRestarts=0; Restart=no; listener PASS; API PASS; DB snapshot identical.
- Final: `A-5 PASS`; trap rc0.

## Independent postcheck

- Unit active/running, MainPID=189813, NRestarts=0, Restart=no.
- Listener count 1; non-loopback count 0.
- API HTTP200, state DISARMED, mode credential_free_disarmed, state_version1; armed,
  credentials_loaded, broker_connected, exchange_connected and network_enabled all off.
- DB quick_check ok; app_state DISARMED; schema_version4; all table counts match the expected empty
  credential-free state (meta=2, all other tables 0).
- `POSTCHECK_SAFE_STATE=PASS`.

No environment file or credential content was read. No ARM, broker/exchange, order,
TESTNET/mainnet, wallet, master merge, or economic action occurred.

## Next action

Update current memory (this record), then recover and independently verify the preregistered A-6
run-kit D command and its first-FAIL/safety contract. Run A-6 only after confirming its evidence log
is absent and the live A-5 post-state remains safe. Preserve evidence and checkpoint memory again
before A-7.
