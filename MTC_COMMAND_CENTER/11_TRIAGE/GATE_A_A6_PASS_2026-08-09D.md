# Gate A A-6 PASS — run-kit D (2026-08-09)

## Verdict

**A-6 PASS.** The preregistered D command executed exactly once:

```
bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A6.sh
```

SSH returned rc0. Transport stdout and stderr were both empty because the script redirects its own
output to its no-clobber evidence log. Gate state is now: **A-0..A-6 PASS; A-7..A-9 NOT RUN.**
A-7 was not executed and is not claimed to pass.

## Identity

- Branch checkpoint before this unit: `b8776ca6`.
- Accepted candidate unchanged: `2ce41e34bceb599d80af24c5c33d835820ec321b`.

## Evidence identity

- Remote: `/home/gatea/gatea-A6-20260808D.log`.
- Local preserved copy: `C:\WPI_ARTIFACTS\gatea-A6-20260808D.log`.
- Remote/local SHA-256 identical:
  `75ed426247c2a26f6c4377f8e910826ecb4f0669565f292d538df65f2e52488c`.
- Bytes: `2007`.
- Markers: exactly one `A-6 PASS`, exactly one `A6_TRAP_EXIT rc=0`, exactly four `RESULT=PASS`;
  zero `A6_FAIL`, zero `RESULT=FAIL`.

## In-script proof

- Production before and after: active, MainPID 189813 unchanged, exact API HTTP200 state DISARMED,
  mode credential_free_disarmed, state_version 1; all network/exchange/credential/ARM flags off.
- In-process isolated temp app: engine present; notifier_disabled=true; engine_state DISARMED;
  engine_mode dry_run; reconcile_ready True; reconcile_error None;
  status_deferred_event_queue_depth=0; queued_events_len=0; MockBroker connected with orders=0,
  fills=0, position=None; engine stopped; `RESULT=PASS`.
- Temp DB: quick_check ok; app_state DISARMED; schema_version 4.
- Temp directory `/home/gatea/gatea-A6-temp.FLfBfh` was cleaned by the script.

## Scope boundary

A-6 asserts empty-broker startup: no raise, no hang, no leftover queue. It does **not** assert
queue-drain-under-load and does **not** assert full reconcile — the schema-4 baseline disables full
reconcile.

## Independent postcheck

Accepted postcheck returned rc0; artifact `C:\WPI_ARTIFACTS\postcheck_gatea_a6_d.v2.out`
(stderr file empty). All of the following passed:

- Evidence log hash, byte count and marker counts as recorded above.
- Cleanup: zero `/home/gatea/gatea-A6-temp.*` leftovers.
- Production service active/running, MainPID 189813, Restart=no, NRestarts=0.
- Exactly one `127.0.0.1:8790` listener.
- Exact credential-free DISARMED API.

## Verifier note

The first independent postcheck attempted one extra direct read-only open of
`/var/lib/mtc-bridge/bridge.db` as unprivileged `gatea`, after all preceding assertions had already
passed. SQLite returned `unable to open database file`. This is a verifier permission defect, not an
A-6 failure: A-6 targets only its own isolated temp DB, and production PID and API were unchanged.
That extra out-of-contract production-DB probe was removed and the accepted v2 postcheck passed.
A-7 itself preregisteredly uses sudo for the production persisted-state check.

## Hardening contract held

- No `/api/arm` call; the environment file was not opened.
- Six process environment keys were removed/discarded before bridge imports, with no values printed,
  copied, persisted or retained.
- The injected MockBroker with `bars=[]` prevented the credential resolver and any broker/exchange
  network activity.
- Notifier absent/disabled is bound into the PASS assertion.

## Routing record

- Classification: Tier 4, protected Gate-A evidence documentation, owner exact-model request.
- Protected: yes, deployment/safety evidence surface; documentation only.
- Model + provider: Claude Opus 5 via Claude Code.
- Cheaper-model rationale: exact-model owner request and protected Gate-A evidence.
- Exact paths: `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A6_PASS_2026-08-09D.md` (new),
  `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` (prepend only),
  `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (prepend after title only),
  `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (prepend newest block after
  title only).
- Context/tool budget: targeted four files and supplied evidence only; no broad scan.
- Fallback: none; no downgrade.
- External API credits: no.

## Next action

1. Before A-7, independently verify the exact accepted D kit A-7 identity and syntax, that the A-7
   evidence log is absent, that the service is safe, and that the preregistered sudo permissions
   A-7 needs are noninteractive and available without printing protected content.
2. Update `_AI_MEMORY` with that preflight checkpoint before execution.
3. Execute A-7 exactly once:

```
bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A7.sh
```

4. Preserve and hash the evidence, then independently postcheck. On genuine A-7 FAIL, do not run
   A-8.

## Exclusions

No credential content, successful ARM, broker/exchange network, orders, TESTNET/mainnet, wallet,
master merge, destructive Git, or economic action occurred. No product code, run-kit scripts, tests,
Pine/parity/MTC/trading logic, schemas, or existing historical sections were changed. This
documentation unit ran no SSH, Gate-A script, test, service, package, Git, staging, or
network/broker/exchange command; the A-6 execution and postchecks above were Lead-performed.
