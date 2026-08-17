# Gate A A-8 PASS — run-kit D (2026-08-09)

## Verdict

**A-8 PASS**, from both halves of the preregistered two-part unit. Gate state is now:
**A-0..A-8 PASS; A-9 NOT RUN.** A-9 was not executed and is not claimed to pass.

## Identity

- Branch checkpoint before this unit: `8cba7897`.
- Accepted candidate unchanged: `2ce41e34bceb599d80af24c5c33d835820ec321b`.

## Remote half

Executed exactly once:

```
bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A8.sh
```

SSH returned rc0. Transport stdout and stderr were both empty because the script redirects its own
output to its no-clobber evidence log.

### Remote evidence identity

- Remote: `/home/gatea/gatea-A8-20260808D.log`.
- Local preserved copy: `C:\WPI_ARTIFACTS\gatea-A8-20260808D.log`.
- Remote/local SHA-256 identical:
  `a7ef34a18145aee61196110dda6882c80992e189573003eb7fbf1119f829f0d7`.
- Bytes: `1087`.
- Markers: exactly one `A-8 PASS`, exactly one `A8_TRAP_EXIT rc=0`, exactly one `RESULT=PASS`;
  zero `A8_FAIL`, zero `RESULT=FAIL`.

### Remote in-script proof

- Socket enumeration succeeded: `ss_rc=0`.
- `listener_count` 1.
- `local_addresses` exactly `127.0.0.1:8790`.
- Non-loopback, wildcard and VM-IP listener lists all empty.
- Firewall query succeeded: `A8_ufw_rc=0`.
- IP and UFW evidence was captured inside the evidence log; the raw payload is deliberately not
  reproduced here.

## Host half

Executed exactly once from the accepted packaged path:

```
powershell -NoProfile -ExecutionPolicy Bypass -File C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34\gatea_A8_host.ps1
```

Returned rc0 with empty command stderr. Command stdout included exactly `port22_ok=True`, an empty
`port22_err`, `port8790_ok=False`, `port8790_err=timeout_3000ms`, `host_probe_ok=True`, and
`A8_HOST_PASS`.

### Host evidence identity

- Host evidence: `C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log`.
- SHA-256: `abad3225fe530c00c1ef60a9cd46a0048fa1cac40135525484389d2703fee2e6`.
- Bytes: `321`.
- Encoding: UTF-8 without BOM; CR count 0, LF-only line endings.
- Content: the fixed VM, candidate and timeout values, plus the same boolean results as the command
  stdout.
- Accuracy note: `A8_HOST_PASS` is a **command stdout** marker. It is not stored inside the host
  evidence log, and is not claimed to be.

## Independent postchecks

### Remote postcheck

rc0; artifact `C:\WPI_ARTIFACTS\postcheck_gatea_a8_remote_d.out`, stderr empty. It confirmed the
remote evidence hash, byte count, marker counts and binding assertions; the exact credential-free
DISARMED API; and the production service active/running at PID 189813, Restart=no, NRestarts=0,
with exactly one loopback listener. Result: `A8_REMOTE_POSTCHECK=PASS`.

### Host postcheck

rc0; artifact `C:\WPI_ARTIFACTS\postcheck_gatea_a8_host_d.out`, stderr empty. It confirmed the host
evidence hash, byte count, absence of BOM and CR count 0; that the command stdout includes
`A8_HOST_PASS`; and an independent `TcpClient` reprobe returning port 22 True and port 8790 False.
Result: `A8_HOST_POSTCHECK=PASS`.

## Combined acceptance

A-8 PASS required both halves: the remote evidence ending `A-8 PASS`, and the host half at rc0 with
all required booleans plus `A8_HOST_PASS`. Both held, so **A-8 PASS**.

## Contract held

- No `/api/arm` call.
- The environment file was not opened.
- No credential content read.
- No broker, exchange, order or economic action.
- Networking and firewall evidence gathering was read-only.

## Routing record

- Classification: Tier 4, protected Gate-A evidence documentation, owner exact-model request.
- Protected: yes, deployment/safety evidence surface; documentation only.
- Model + provider: Claude Opus 5 via Claude Code.
- Cheaper-model rationale: exact-model owner request and protected Gate-A evidence.
- Exact paths: `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A8_PASS_2026-08-09D.md` (new),
  `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` (prepend only),
  `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (prepend after title only),
  `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (prepend newest block after
  title only).
- Context/tool budget: targeted four files and the supplied evidence only; no broad scan.
- Fallback: none; no downgrade.
- External API credits: no.

## Next action

1. Preflight the accepted D A-9 script: identity and syntax, absence of the remote A-9 log, a safe
   service, the exact scan roots and command permissions, and the output-redaction contract. A-9
   truthfully reads bytes under the release directory and `/etc/mtc-bridge`, including the
   environment file, but may emit only category counts and matching paths — never matched text or
   values.
2. Update `_AI_MEMORY` before execution.
3. Execute A-9 exactly once, and only after the preflight checkpoint. Preserve and hash its
   evidence, and inspect only counts and paths — never matched content. A genuine A-9 hit or
   failure is BLOCK/FAIL and stops Gate A completion.

## Exclusions

No credential content, successful ARM, broker/exchange network, orders, TESTNET/mainnet, wallet,
master merge, destructive Git, or economic action occurred. No product code, run-kit scripts, tests,
Pine/parity/MTC/trading logic, schemas, or existing historical sections were changed. This
documentation unit ran no SSH, Gate-A script, test, service, package, Git, staging, or
network/broker/exchange command; the A-8 executions and postchecks above were Lead-performed.

## Self-QA

- Four allowed paths only; all older content preserved byte-for-byte.
- Gate state stated as A-0..A-8 PASS with A-9 NOT RUN; no A-9 execution or PASS claimed.
- Hashes, byte counts, marker counts, PID and probe results transcribed from the supplied verified
  facts without rounding or paraphrase.
- `A8_HOST_PASS` recorded as command stdout, explicitly not as evidence-log content.
- No credential content and no raw IP/UFW payload reproduced.
