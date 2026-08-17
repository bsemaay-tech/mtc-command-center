# Gate A A-8 remote+host preflight PASS — run-kit D, execute A-8 next (2026-08-09)

## Verdict

**A-8 PREFLIGHT PASS (both subparts); A-8 NOT YET EXECUTED.** This is a Lead-performed, read-only,
non-executing two-part preflight of the preregistered A-8 run-kit D before A-8 execution. Neither
A-8 script (`gatea_A8.sh` remote, `gatea_A8_host.ps1` Windows host) ran in this unit. Gate state is
unchanged: **A-0..A-7 PASS; A-8..A-9 NOT RUN.** `A8_REMOTE_PREFLIGHT=PASS`; `A8_HOST_PREFLIGHT=PASS`.

## Identity

- Branch starting checkpoint: `4caa553f`.
- Accepted candidate unchanged: `2ce41e34bceb599d80af24c5c33d835820ec321b`.

## Remote package (run-kit D)

- Accepted D tar: `/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar`, SHA-256
  `e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3`, 71680 bytes.
- All seven `SHA256SUMS` members verified OK.

## Remote A-8 packaged script

- Path: `/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A8.sh`.
- SHA-256 `1fa14524f1a38f0ba6a590c38a525f9689737d1d46d20be233450ff95f939d19`, 4124 bytes, CR count
  0; `bash` syntax rc0.
- Remote A-8 evidence `/home/gatea/gatea-A8-20260808D.log` is absent.

## Remote production safe-state preflight

- Service active/running, MainPID=189813, Restart=no, NRestarts=0.
- Exactly one listener: `127.0.0.1:8790`.
- API HTTP 200 credential-free DISARMED: `state_version=1`; network, exchange_conn,
  credential_lookup, exchange_enabled and arm_enabled all off.
- `ip -brief address` executable available; exact `sudo ufw status verbose` noninteractive with
  output suppressed.
- `A8_REMOTE_PREFLIGHT=PASS`.

## Host A-8 packaged script

- Path: `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34\gatea_A8_host.ps1`.
- SHA-256 `57899687707c882c425be495f5d4d53f8cccf140172c9a1ee56e899eb3f0b281`, 3195 bytes, CR0 /
  LF-only; PowerShell parser errors 0.
- Host evidence `C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log` is absent.

## Host reachability preflight

- Windows host port-22 reachability control to `172.24.55.233` passed within 3000 ms, proving host
  route/SSH control.
- Port 8790 deliberately not probed during preflight; reserved for the actual host A-8 script.
- `A8_HOST_PREFLIGHT=PASS`.

## Local evidence files

- Remote preflight: `C:\WPI_ARTIFACTS\preflight_gatea_a8_remote_d.out` and `.err`; both rc0, stderr
  empty.
- Host preflight: `C:\WPI_ARTIFACTS\preflight_gatea_a8_host_d.out` and `.err`; both rc0, stderr
  empty.

## Routing record

- Classification: Tier 4, protected Gate-A evidence documentation, owner exact-model request.
- Protected: yes, deployment/safety evidence surface; documentation only.
- Model + provider: GLM-5.2 via Z.AI Coding Plan.
- Cheaper-model rationale: exact-model owner request and protected Gate-A evidence; no cheaper tier
  used.
- Exact paths: `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A8_PREFLIGHT_2026-08-09D.md` (new),
  `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` (prepend only),
  `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (prepend after title only),
  `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (prepend newest block after
  title only).
- Context/tool budget: targeted four files and supplied evidence only; no broad scan.
- Fallback: none; no downgrade.
- External API credits: no.

## Next action

Execute the preregistered A-8 two-part sequence exactly once, in strict order:

1. Remote half:
   ```
   bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A8.sh
   ```
2. If and only if the remote rc0/evidence ends `A-8 PASS`, host half:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34\gatea_A8_host.ps1
   ```
3. A-8 PASS requires both remote `A-8 PASS` and host `port22_ok=True`, `port8790_ok=False`,
   `host_probe_ok=True`, `A8_HOST_PASS`, host rc0.
4. Preserve/hash both evidence logs, independently postcheck the safe service, and update
   `_AI_MEMORY` before A-9. On either genuine subpart FAIL do not run A-9; if the remote half fails,
   do not run the host half.

## Exclusions

No credential content, successful ARM, broker/exchange network, orders, TESTNET/mainnet, wallet,
master merge, destructive Git, or economic action occurred. No product code, scripts, tests,
Pine/parity/MTC/trading logic, schemas, or existing historical sections were changed. No SSH, Gate-A
script, test, service, package, Git, sudo, host probe, staging, or network/broker/exchange command
was run in this unit.
