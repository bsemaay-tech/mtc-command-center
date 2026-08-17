# Gate A A-7 PASS — run-kit D (2026-08-09)

## Verdict

**A-7 PASS.** The preregistered D command executed exactly once:

```
bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A7.sh
```

SSH returned rc0. Transport stdout and stderr were both empty because the script redirects its own
output to its no-clobber evidence log. Gate state is now: **A-0..A-7 PASS; A-8..A-9 NOT RUN.**
A-8 was not executed and is not claimed to pass.

## Identity

- Branch checkpoint before this unit: `519223e2`.
- Accepted candidate unchanged: `2ce41e34bceb599d80af24c5c33d835820ec321b`.

## Evidence identity

- Remote: `/home/gatea/gatea-A7-20260808D.log`.
- Local preserved copy: `C:\WPI_ARTIFACTS\gatea-A7-20260808D.log`.
- Remote/local SHA-256 identical:
  `09443b51fe01498e6530d8729b73bf2e26671b24b2a7e7b1085f8a700bbb2bf5`.
- Bytes: `4269`.
- Markers: exactly one `A-7 PASS`, exactly one `A7_TRAP_EXIT rc=0`, exactly one `RESULT=PASS`;
  zero `A7_FAIL`, zero `RESULT=FAIL`.

## In-script proof

- API: HTTP200; state DISARMED; mode credential_free_disarmed; state_version 1; reconcile_ready
  False (expected here, and not required to be true); reconcile_error None; all
  network/exchange/credential/ARM flags off.
- Production DB via the preregistered read-only sudo path: quick_check ok; app_state DISARMED;
  schema_version 4.
- Explicit cross-source equality asserted in-script:
  `A7_db_app_eq_api_state=DISARMED==DISARMED`.
- Point-in-time documented log identity:
  - `bridge.log` — 1554 B, mode 600, owner root:root, SHA-256
    `efda2d198673d9fb01d37c394f6d27644faf728bc4c19baf60884e78f548d02d`.
  - `bridge.err.log` — 597 B, mode 600, owner root:root, SHA-256
    `0b9067659ea67dd8fcb0f9f2c59cd8bf22ca850db739f33e9889b46706b7d207`.
- Journal query succeeded with exactly 22 payload lines bounded by begin/end markers;
  `A7_journal_credgrep=not performed (forbidden by contract)`. The raw journal payload was
  deliberately not printed into Lead task output.

## Independent postcheck

Accepted postcheck returned rc0; artifact `C:\WPI_ARTIFACTS\postcheck_gatea_a7_d.v2.out`
(stderr file empty). All of the following passed:

- Evidence log hash, byte count and marker counts as recorded above.
- Exact credential-free DISARMED API.
- Production DB quick_check, app_state and schema_version.
- Explicit evidence equality of the DB and API state.
- Journal line count and begin/end bounds.
- Current `bridge.log` and `bridge.err.log` regular and non-empty.
- Production service active/running, PID 189813, Restart=no, NRestarts=0.
- Exactly one loopback listener.

## Verifier note

The first postcheck passed the API and production DB assertions, then stopped because it
over-strictly required the current mutable `bridge.log` hash to equal A-7's point-in-time snapshot.
Independent GET status checks append benign lines: the current `bridge.log` grew 1554 → 1616 →
1678 B, and its hash at the accepted v2 run was
`d6bb3a2a8c22775fc3a68c1a5fb43a44cf62edce648263a57ee9b51cfb8b13ab`. `bridge.err.log` remained
597 B with the same hash throughout. This is a verifier-design defect, not an A-7 failure. V2
validates the authoritative snapshot identity inside the immutable A-7 evidence, and separately
checks that the current logs are regular and non-empty, instead of demanding that a live
append-only log stay byte-identical. No raw log content was printed.

## Contract held

- No `/api/arm` call.
- The environment file was not opened.
- No `/api/health` call.
- No credential grep and no credential content read.
- Production inspection was read-only.

## Routing record

- Classification: Tier 4, protected Gate-A evidence documentation, owner exact-model request.
- Protected: yes, deployment/safety evidence surface; documentation only.
- Model + provider: Claude Opus 5 via Claude Code.
- Cheaper-model rationale: exact-model owner request and protected Gate-A evidence.
- Exact paths: `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A7_PASS_2026-08-09D.md` (new),
  `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` (prepend only),
  `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (prepend after title only),
  `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (prepend newest block after
  title only).
- Context/tool budget: targeted four files and the supplied evidence only; no broad scan.
- Fallback: none; no downgrade.
- External API credits: no.

## Next action

1. Preflight both accepted D A-8 scripts — `gatea_A8.sh` (remote) and `gatea_A8_host.ps1` (Windows
   host) — verifying their exact hashes and syntax, that the remote and host evidence paths are
   absent, that the service is safe, and that the required host and SSH connectivity exist. Do not
   execute A-8 during preflight.
2. Update `_AI_MEMORY` before execution.
3. Execute the preregistered A-8 remote + host sequence exactly once, preserve and hash both
   evidence logs, then independently postcheck. On genuine A-8 FAIL, do not run A-9.

## Exclusions

No credential content, successful ARM, broker/exchange network, orders, TESTNET/mainnet, wallet,
master merge, destructive Git, or economic action occurred. No product code, run-kit scripts, tests,
Pine/parity/MTC/trading logic, schemas, or existing historical sections were changed. This
documentation unit ran no SSH, Gate-A script, test, service, package, Git, staging, or
network/broker/exchange command; the A-7 execution and postchecks above were Lead-performed.

## Self-QA

- Four allowed paths only; all older content preserved byte-for-byte.
- Gate state stated as A-0..A-7 PASS with A-8..A-9 NOT RUN; no A-8 execution or PASS claimed.
- Hashes, byte counts, marker counts, PID and log sizes transcribed from the supplied verified
  facts without rounding or paraphrase.
- Verifier defect recorded as a verifier-design defect, not an A-7 failure.
- No credential, raw log or journal payload content reproduced.
