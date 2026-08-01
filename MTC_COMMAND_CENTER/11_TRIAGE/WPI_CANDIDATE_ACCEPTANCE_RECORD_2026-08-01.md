# WP-I Candidate Acceptance Record (2026-08-01)

- Date: 2026-08-01
- Work package: WP-I — Reproducible Deps, systemd, State, Rollback, Ubuntu Staging
- Status: **LOCAL / STATIC CANDIDATE EVIDENCE ACCEPTED — GATE A HOST-BLOCKED**
- Acceptance scope: **owner-continuity / Claude-waiver acceptance scope is local/static WP-I candidate evidence only.** No Ubuntu, install, runtime, or staging evidence is accepted by this record.

## 1. Frozen identities

| Item | Value |
|---|---|
| Baseline `origin/master` | `637307e83951ffe23e768ed8e50ddaf8712b0660` |
| WPL branch | `codex/50h-wpl-verification` pushed at `d9d38d9b8e658d5853903cfc7779bc5ba56bfea2` |
| Candidate release SHA | `1adf9ae51b0ddfe81057860aec5c23bb842f5a84` |
| Stable artifact path | `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84` |
| Manifest SHA-256 | `bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02` |
| Manifest entries verified | 7,060 |
| Regular files | 7,061 |
| Bytes | 1,051,904,669 |
| Content-redacted categories | nine, all zero |

## 2. Frozen final blobs

| Artifact | Git blob OID |
|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/README.md` | `666b79d834f50433cd0cba7c88224fb674fdbb56` |
| `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` | `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md` | `20d92f4076e5cc17879408232593f493d7872ddf` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPL_PHASE1_VERIFICATION_RECORD_2026-08-01.md` | `61032d1c601dcc6c258807b004087b0d8b87fe0b` |

## 3. Main records branch cherry-picks

- `05acaadf` — static docs
- `52f33bdc` — candidate evidence
- `ad0c3dd7` — WPL record

## 4. Verification evidence

- Lead ran the exact embedded artifact verification, exit 0.
- Strict UTF-8 / stale / secret / scope checks pass.

## 5. Audit trail

- **Initial final-scope Codex `gpt-5.6-sol` xhigh audit** session
  `019fbef3-e7d6-7860-afa4-57e1ed4998be` executed all checks and returned
  `REQUEST_CHANGES` only for contradictory shell wording; the Lead reproduced
  and fixed one line.
- **Fresh Codex re-audit** session `019fbefe-b83b-70a3-9ec8-d9f56ee66d3f` hit
  the usage limit before any tool call and is **not evidence**.
- **Grok** nonexecuting / failed validation labels are explicitly discarded.
- **Fresh DeepSeek `deepseek-chat`** through `_deepseek_driver`, empty write
  allowlist, returned **PASS-WITH-NITS** after actual `4 passed in 0.46s` and
  `2 passed in 0.43s`; it independently verified all 7,060 hashes / 7,061
  files / bytes / nine zeros and the docs.
- Non-blocking nit: markdown line wrapping only.
- Local audit report `C:\tmp\wpi_candidate_deepseek_audit_report.md`, SHA-256
  `ee0f28bd33980e157f0bba2cf4a2b3db3035b4dc0442aa55c8bf772123e1358e`, 94,473
  bytes.

## 6. Acceptance

Accept **WP-L Phase 1** + **WP-I local/static/candidate evidence only**.

## 7. Gate A blocker

Gate A remains **BLOCKED** solely because no named/reachable expendable Ubuntu
24.04 staging host exists; the active KVM2 host is forbidden.

Read-only local inventory:
- Hyper-V command available but access denied;
- VirtualBox / QEMU absent;
- WSL not installed.

Static evidence is **not** Ubuntu / install / runtime evidence.

## 8. Hours and no-action boundary

- Historical hours remain **20.5 h used / 29.5 h remaining**; exact WP-L / WP-I
  booking is deferred to **Lead Gate-7**.
- No Ubuntu / service / broker / order / ARM / TESTNET order / mainnet / wallet /
  credential-value / live-capital action occurred.
