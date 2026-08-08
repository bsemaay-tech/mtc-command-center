# GATE A — run-kit D packaged, transferred, extracted, and verified (2026-08-09); A-5..A-9 NOT RUN

> **STATUS: A-0..A-4 PASS. A-5..A-9 remain NOT RUN.** This checkpoint records only that the
> Lead-accepted run-kit D **source** was packaged, transferred to `gatea-staging`, extracted, and
> independently re-verified. **No Gate-A script (A-5..A-9) was executed** during packaging,
> transfer, extraction, or verification. No gate result beyond A-0..A-4 PASS is claimed. Next
> executable action is **A-5 first**, strict order, stop at first genuine FAIL.

This is a **bounded documentation checkpoint by GLM-5.2** in the isolated worktree `C:\GADTR` on
branch `codex/gatea-d-transfer-checkpoint`. The packaging/transfer/extraction/verification actions
recorded here were **authorized staging actions performed by the Lead** under the owner-approved
preregistered `gatea-staging` Gate A rerun sequence, and their results are recorded — not performed
or mutated — by this documentation unit. No product code or product artifact changed; no credential,
broker/exchange access, successful ARM, order, TESTNET/mainnet, wallet, master merge, or economic
action is authorized or occurred. Hard exclusions unchanged.

---

## 1. Pre-checkpoint state (exactly as recorded)

| Item | Value |
|---|---|
| Active integration branch before this task | `feature/donchian-crypto-ladder` |
| Branch checkpoint SHA | `acc41e732d0825058e25e7e89652d61811a8cde6` (`acc41e73`) |
| Accepted source candidate (unchanged) | `2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Run-kit D source (committed) | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/` |
| Preregistration (Lead-accepted) | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` |
| Last completed gate state | **A-0 PASS · A-1 PASS · A-2 PASS · A-3 PASS · A-4 PASS · A-5..A-9 NOT RUN** |

Kit members committed under `GATE_A_RUN_KIT_D_2026-08-08/` (7 content files): `README.txt`,
`gatea_A5.sh`, `gatea_A6.sh`, `gatea_A7.sh`, `gatea_A8.sh`, `gatea_A8_host.ps1`, `gatea_A9.sh`.

---

## 2. Local REJECTED package — `git archive` CRLF export (preserved, not transferred)

A first packaging attempt used `git archive`, which exported CRLF line endings. It was **rejected
before transfer** and is preserved as evidence so it is never confused with the accepted package.

| Item | Value |
|---|---|
| Rejected directory | `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.rejected-crlf` |
| Rejected tar | `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.rejected-crlf.tar` |
| Rejected tar SHA-256 | `66ce7a1e148d17626f68962ccdd3bb6bcacdf4c49a6eb815713caa64899634a8` |
| Rejected tar bytes | `71680` |
| Reason | `git archive` exported CRLF; rejected before transfer |

This is the documented A-2 trap (bare `git archive` on Windows converts to CRLF) surfacing again at
packaging time. It was caught and rejected locally; it was never transferred to staging.

---

## 3. Accepted package — rebuilt from raw committed blobs (`git cat-file blob`)

To avoid worktree/archive line-ending conversion entirely, the accepted package was rebuilt from the
**raw committed blobs** with `git cat-file blob` (reading straight from the object database, not the
working tree or `git archive`). This guarantees LF bytes from the committed source.

| Item | Value |
|---|---|
| Accepted directory | `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34` |
| Accepted tar | `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.tar` |
| Accepted tar SHA-256 | `e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3` |
| Accepted tar bytes | `71680` |
| Exact tar member count | `9` (root directory entry **plus 8 files**) |
| Extracted file count | `8` |
| Manifest lines (`SHA256SUMS`) | `7` |

**Accepted package contents (8 files; 9 tar members incl. root):**

| # | Member | Role |
|---|---|---|
| 1 | `README.txt` | kit header / invocation / validation / frozen facts |
| 2 | `gatea_A5.sh` | A-5 unclean SIGKILL / manual-restart consistency |
| 3 | `gatea_A6.sh` | A-6 empty-startup reconcile dry-run |
| 4 | `gatea_A7.sh` | A-7 read-only status / persisted-state / log evidence |
| 5 | `gatea_A8.sh` | A-8 loopback binding proof (remote/VM side) |
| 6 | `gatea_A8_host.ps1` | A-8 host reachability probe (Windows host side) |
| 7 | `gatea_A9.sh` | A-9 content-redacted secret scan |
| 8 | `SHA256SUMS` | manifest (7 lines — the 7 content files above) |

**Local verification of the accepted package (all passed):**

- All 7 manifest hashes verified.
- All members CR count `0` (LF-only).
- Bash syntax checks passed; PowerShell parser check passed; embedded Python syntax checks passed.

---

## 4. Staging transfer + extraction (same SHA-256 / bytes / member set)

| Item | Value |
|---|---|
| Remote tar path | `/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar` |
| Remote extraction path | `/home/gatea/gatea-run-kit-20260808D-2ce41e34` |
| Transfer integrity | exact same SHA-256 `e8a52e3c…5e0d3`, `71680` bytes, exact member set preserved |

The transferred tar preserves byte-for-byte the accepted local tar.

---

## 5. First remote verifier — transport defect (recorded transparently, not a package/Gate-A failure)

After extraction, the **first** remote re-verification attempt had a **PowerShell-to-SSH quoting
defect** and emitted:

```
test: \\8: integer expression expected
```

This is a **verifier transport defect** (shell quoting of the verifier command across the
PowerShell→SSH boundary), **not** a package defect and **not** a Gate-A failure. **No Gate-A script
ran** during this attempt. It is recorded transparently rather than concealed. A clean remote
re-verification (§6) was then performed and passed.

---

## 6. Clean remote re-verification — PASS

A clean remote re-verification of the extracted kit at
`/home/gatea/gatea-run-kit-20260808D-2ce41e34` **passed**:

- All **7** manifest members verified.
- `bash -n` passed for A5, A6, A7, A8, A9.
- Exact extracted file count **8** and exact member set.
- Manifest lines **7**.
- Every file CR count **0**.

**Per-member byte / LF-count evidence:**

| Member | Bytes | LF count |
|---|---|---|
| `README.txt` | 13934 | 197 |
| `SHA256SUMS` | 551 | 7 |
| `gatea_A5.sh` | 9719 | 261 |
| `gatea_A6.sh` | 13863 | 283 |
| `gatea_A7.sh` | 6191 | 139 |
| `gatea_A8.sh` | 4124 | 108 |
| `gatea_A8_host.ps1` | 3195 | 87 |
| `gatea_A9.sh` | 3937 | 109 |

**Embedded Python blocks compiled:**

| Script | Embedded Python blocks compiled |
|---|---|
| `gatea_A5.sh` | 3 |
| `gatea_A6.sh` | 3 |
| `gatea_A7.sh` | 2 |
| `gatea_A8.sh` | 1 |
| `gatea_A8_host.ps1` | (PowerShell — no embedded Python) |
| `gatea_A9.sh` | 0 |

---

## 7. Staging safety — unchanged after transfer/verification

After transfer and verification the staging host remained safe and unchanged:

- Service **active/static**.
- Exact **credential-free DISARMED** status.
- **No credentials.**
- **No broker.**
- State version **1**.

This is the A-5 prerequisite state (DISARMED, active/static, loopback-only, no broker/credentials),
preserved through the package/transfer/verify unit. **No run-kit script was executed** during
packaging, transfer, extraction, or verification.

---

## 8. Gate status after this checkpoint

| Gate | Status |
|---|---|
| A-0 · A-1 · A-2 · A-3 · A-4 | **PASS** |
| A-5 · A-6 · A-7 · A-8 · A-9 | **NOT RUN** |

---

## 9. Next steps contract (A-5 first)

1. **Execute A-5 only** from `/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh`.
2. **Preserve and inspect** `/home/gatea/gatea-A5-20260808D.log`; independently verify
   service/API/DB/listener/systemd state before assigning a verdict.
3. **Stop on the first genuine FAIL** and perform the preregistered safe response; **do not run A-6.**
4. If A-5 passes, **update the relevant `MTC_COMMAND_CENTER/_AI_MEMORY` files** before starting A-6.
5. **Continue one gate at a time** under the existing preregistration. Hard exclusions remain: no
   credentials, broker/exchange, successful ARM, orders, TESTNET/mainnet, wallet, master merge, or
   economic action.

---

## 10. Reproduction / orientation (another lead, without trusting the handoff)

**Companion records (read order):**

- `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` — exact paths, per-gate criteria, shared
  script contract, first-FAIL response, GLM routing record, Lead correction/repair tables, final
  Lead acceptance.
- `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt` — invocation, local validation, transfer +
  remote verification, execution order, post-run evidence-log hashing.
- `11_TRIAGE/GATE_A_A4_PASS_2026-08-08C.md` — A-4 PASS (prerequisite state for A-5).
- `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`,
  `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` — live state (newest section first).

**Re-hash the two local artifacts to confirm identity (read-only):**

- Accepted: `SHA-256 e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3`, `71680` bytes
  at `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.tar`.
- Rejected (CRLF): `SHA-256 66ce7a1e148d17626f68962ccdd3bb6bcacdf4c49a6eb815713caa64899634a8`,
  `71680` bytes at `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.rejected-crlf.tar`.

**Re-verify the extracted remote kit (commands documented in the committed kit README; read-only on
the kit, not Gate-A execution):** against
`/home/gatea/gatea-run-kit-20260808D-2ce41e34/` — `sha256sum -c SHA256SUMS` (all OK); the five
`bash -n` checks (`gatea_A5.sh`..`gatea_A9.sh`); CR-byte count `0` for every member; expect exactly
8 files, 7 manifest lines, and the byte/LF counts in §6.

**A-5 entry point (DO NOT RUN until authorized as the next unit):**
`/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh`, evidence log
`/home/gatea/gatea-A5-20260808D.log`.

---

## 11. Scope, safety, and routing

- **Documentation only.** GLM-5.2 edited only the four task-named files (this report plus the three
  memory/handoff prepends). No source, tests, scripts, manifests, credentials, trading/Pine/parity/
  MTC logic, or any other file changed.
- **No execution.** No Gate-A script, SSH/SCP command, service operation, test, package build,
  deployment, or Git command was executed by this documentation unit. The packaging/transfer/
  extraction/verification actions recorded were authorized Lead staging actions performed under the
  preregistered sequence.
- **Routing (per `AGENTS.md` §GLM SUPPLEMENTAL ROUTING):** Tier 4 — protected Gate-A evidence tooling
  + docs; GLM-5.2 via Z.AI Coding Plan (owner exact-model request + protected safety-evidence
  surface). No external API credits; no fallback/downgrade. GLM does not replace the mandatory audit
  roster; this is documentation/tooling, not a Gate-5 audit.
- **Hard exclusions unchanged:** no credential value, broker/exchange access, successful ARM, order,
  TESTNET/mainnet, wallet, master merge, or economic action. The service intentionally remains
  active/static, loopback-only, credential-free DISARMED, `state_version=1`, no broker/credentials —
  the prerequisite for A-5.
