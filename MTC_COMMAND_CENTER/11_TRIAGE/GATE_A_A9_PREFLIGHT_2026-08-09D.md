# Gate A A-9 redaction-aware preflight PASS — run-kit D, execute A-9 next (2026-08-09)

## Verdict

**A-9 PREFLIGHT PASS; A-9 NOT YET EXECUTED.** This is a Lead-performed, read-only, non-executing
preflight of the preregistered A-9 run-kit D before A-9 execution. The A-9 script (`gatea_A9.sh`)
did not run in this unit, and the real release and `/etc` scan roots were not scanned. Gate state is
unchanged: **A-0..A-8 PASS; A-9 NOT RUN.** `A9_PREFLIGHT=PASS`. GLM-5.2 only edited documentation
(the four task-named files) and recorded this Lead-performed preflight; it did not run any SSH,
Gate-A script, grep/scan, sudo, test, service, package, Git, staging, or network/broker/exchange
command.

## Identity

- Branch starting checkpoint: `0641c534`.
- Accepted candidate unchanged: `2ce41e34bceb599d80af24c5c33d835820ec321b`.

## Remote package (run-kit D)

- Accepted D tar: `/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar`, SHA-256
  `e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3`, 71680 bytes.
- All seven `SHA256SUMS` members verified OK.

## Remote A-9 packaged script

- Path: `/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A9.sh`.
- SHA-256 `2c7e73be6c1a5b5352d9ab2580967a54e3d91fb8fe567d7a0d59f25296fada4d`, 3937 bytes, CR count
  0; `bash` syntax rc0.
- A-9 evidence `/home/gatea/gatea-A9-20260808D.log` is absent.
- Zero `/home/gatea/gatea-A9-err.*` leftovers before preflight and after cleanup.

## Scan roots and static contract

- Exact real scan roots verified present and readable: the release directory
  `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` and `/etc/mtc-bridge`.
- The accepted script excludes the venv and `/home/gatea`.
- Static contract verified: exactly nine canonical category names in canonical order; the scan
  command is `sudo grep -RIlE --binary-files=without-match -e $ere -- $REL $ETC`; per-category rc
  and count are recorded; on a hit only the matching file path list is emitted.
- A-9 truthfully reads bytes in the exact real roots, including the root-readable environment file,
  but emits only category counts and matching file paths — never matched text or values. Any
  category count > 0 is FAIL/BLOCK; any rc > 1 is FAIL.

## Permission/redaction falsification

- One disposable `/home/gatea/gatea-A9-preflight.<6>` temp containing a single synthetic token-like
  line was created. The exact `grep -l` command returned exactly that synthetic file path and no
  matched text or value; the synthetic value was never printed.
- The real release and `/etc` roots were not scanned during the preflight.
- The temp file and directory were removed with guarded nonrecursive cleanup;
  `grep_path_only_fixture_falsification=true`; post-cleanup there were no `A9-preflight` or
  `A9-err` leftovers.

## Remote production safe-state preflight

- Service active/running, MainPID=189813, Restart=no, NRestarts=0.
- Exactly one listener: `127.0.0.1:8790` (loopback only).
- API HTTP 200 credential-free DISARMED: `state_version=1`; all external and ARM flags off.

## Local evidence files

- A-9 preflight: `C:\WPI_ARTIFACTS\preflight_gatea_a9_d.out` and `.err`; both rc0, stderr empty;
  `A9_PREFLIGHT=PASS`.

## Routing record

- Classification: Tier 4, protected Gate-A evidence documentation, owner exact-model request.
- Protected: yes, deployment/safety evidence surface; documentation only.
- Model + provider: GLM-5.2 via Z.AI Coding Plan.
- Cheaper-model rationale: exact-model owner request and protected Gate-A evidence; no cheaper tier
  used.
- Exact paths: `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PREFLIGHT_2026-08-09D.md` (new),
  `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` (prepend only),
  `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (prepend after title only),
  `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (prepend newest block after
  title only).
- Context/tool budget: targeted four files and supplied evidence only; no broad scan.
- Fallback: none; no downgrade.
- External API credits: no.

## Next action

Execute the preregistered A-9 script exactly once, only after this preflight checkpoint:

1. Run once:
   ```
   bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A9.sh
   ```
2. Preserve/hash `/home/gatea/gatea-A9-20260808D.log` locally. Inspect only the structured
   per-category rc/count and matching file paths; never matched text or value.
3. PASS requires nine categories, each rc=1 and matches=0, `A9_any_hit=0`, exactly one `A-9 PASS`,
   trap rc0, no `A9_FAIL`/grep-error blocks, and no temp leftover. Any hit or nonzero error is
   FAIL/BLOCK and Gate A is not complete.
4. Independently postcheck the safe service and update `_AI_MEMORY` with the final Gate A verdict.
   Do not clean the old deployment or start another gate until the final checkpoint is accepted.

## Exclusions

No credential content, successful ARM, broker/exchange network, orders, TESTNET/mainnet, wallet,
master merge, destructive Git, or economic action occurred. No product code, scripts, tests,
Pine/parity/MTC/trading logic, schemas, or existing historical sections were changed. No SSH, Gate-A
script, grep/scan, test, service, package, Git, sudo, staging, or network/broker/exchange command
was run in this unit.
