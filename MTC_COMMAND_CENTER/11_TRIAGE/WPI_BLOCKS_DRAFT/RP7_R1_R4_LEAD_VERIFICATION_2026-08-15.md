# RP7 R1-R4 Lead verification — 2026-08-15

## Disposition

Lead result: **ELIGIBLE FOR THE TWO FRESH T0 FLAGSHIP AUDITS**.

This is not acceptance. T0 acceptance still requires fresh independent
`claude-opus-5` and `gpt-5.6-sol`, both `xhigh`, on the same frozen candidate.

Frozen candidate commit: `80cbed461d0b0371e6eabbfff0e732e5001affaf`  
Branch: `codex/rp7-r1-r4-repair-20260815`

| artifact | Git-object bytes | Git-object SHA-256 |
|---|---:|---|
| `RP7-WPI-RO.sh` | 137981 | `4caed4aecc91cada3b8b99f8ff06d7ba0d7376b2bc07e92c298f4a7b7ca0900c` |
| `SELF_QA_RP7.md` | 585132 | `b1031cc5e71f2a19e05a400a0d3754b9cf37b5917848868e61ae0764a5b1c8ae` |
| `STATUS_RP7.md` | 19165 | `f1fbe2e1d8381b2c5d762e6c69fff2718b7f90ae8d09e8b32d1947fab8ea5a46` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 54481 | `0a434a98393a6c8ecf41a01d6696326c814c44bf69a5d51734f1b44cbe738c46` |

## Writer and scope verification

- Writer result JSON: `type=result`, `subtype=success`, `is_error=false`,
  `terminal_reason=completed`, 233 turns, exact primary model
  `claude-opus-5`; the launcher supplied `xhigh` through the isolated Claude Max
  route. The JSON records a 21-token Haiku utility call but no substitute writer.
- No RP7 writer remained active at Lead takeover.
- Pre-freeze delta was exactly the four kickoff-owned artifacts: 1756 insertions,
  427 deletions after the Lead-only provenance refresh. No other repository path
  changed.
- All four frozen artifacts are LF-only (`CR=0`). `git diff --check` was clean
  apart from Git's informational LF/CRLF checkout warnings.
- `bash --noprofile --norc -n` passed for the script and the extracted fence.
- Extracted fence SHA-256 before and after the Lead-only provenance refresh was
  unchanged: `b64c23ebcc85dece217a2128c069b7d4074cc763533319edb8a25ecf2dc06fbb`.

## Independent complete-fence reproduction

The first unadjusted WSL invocation stopped at rc 128 because the linked
worktree's `.git` file contains a Windows absolute path, which Linux Git read as
`/mnt/c/R7FINAL/C:/LAB/Tradingview_LAB_CLEAN/.git/worktrees/R7FINAL`. This was a
checkout transport failure, not a row predicate result. No candidate byte was
changed. The successful runs supplied the canonical linked-worktree Git context:

```text
GIT_DIR=/mnt/c/LAB/Tradingview_LAB_CLEAN/.git/worktrees/R7FINAL
GIT_WORK_TREE=/mnt/c/R7FINAL
```

The published fence body itself remained unedited. Two final sequential runs
retained in `C:\R7LEADTMP\evidence` produced:

| run | rc | elapsed | stdout | lines | stdout SHA-256 | stderr |
|---|---:|---:|---:|---:|---|---:|
| E | 0 | 203 s | 54284 B | 250 | `d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab` | 0 B |
| F | 0 | 203 s | 54284 B | 250 | `d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab` | 0 B |

`cmp runE.stdout runF.stdout` returned rc 0. No output editing, path replacement,
normalization, or exclusion occurred outside the fence.

The fence's documented `RP7_RAW_EVIDENCE_DIR` export proved that identical
published bytes did not hide reused internal identities:

| internal identity | run E | run F |
|---|---|---|
| scratch root | `/tmp/rp7_rows_1_9_rebuild_evidence.zCqxu93r` | `/tmp/rp7_rows_1_9_rebuild_evidence.NpQQyau8` |
| live mount projection | `aae965beaaa5cd807c06e8135af629079b933af23554ba6a17a05dac43347674` | `84e48e986ec9126ac6e26cbf962f89af272fce9c66ecfa0ceee15b242974ab13` |
| decoy projection | `4bf0575a1f5b674f1be7b143ddc97d5bc6e7d5b5665c8dbffce733ddab8d3e77` | `effd980aba59abc2bd3bc8562333aa8fe45e530b75798b8580f47f77df3a91aa` |
| raw transcript SHA-256 | `01f06adcff790af282a8b77db90e77ab12d2c65862d993e1797ba9320563f4a0` | `5e9ce28e0ae1d35afc1ba5f223a32c985ff0d88dfa31ac477c77ca9e2dd79ea8` |

The raw transcripts differed (`cmp` rc 1) on 262 lines, or 131 line pairs, while
the published transcripts remained byte-identical.

## R1-R4 adjudication

- **R1 reproduced closed for audit dispatch.** Eleven live `ENV_ORACLE` fixtures
  establish the manager normalization boundary. The raw mid-name source spelling
  is bound by row 7's exact source digest plus row 5's empty drop-ins; absent or
  mismatched source attestation STOPs, the differing same-size source digest
  FAILs, and the repaired source/control paths remain GREEN. The effective
  rendering and duplicate-policy limits are disclosed rather than overclaimed.
- **R2 reproduced closed for audit dispatch.** The three chronology tables are
  byte-identical as text and now record the later Lead run without carrying any
  earlier Lead/auditor result across byte identities. Both new auditor slots
  remain explicitly pending.
- **R3 reproduced closed for audit dispatch.** The two published outputs compare
  raw byte-identical while scratch roots, live/decoy mount digests, and raw
  transcripts differ. Count, re-derivation, path-sensitivity, fixture-byte, and
  predicate-deviation gates are present and the complete fence passed.
- **R4 reproduced closed for audit dispatch.** Bare-CR and multi-CR arms produce
  false PASS rc 0 on the named CR-blind subjects and rc 1 on repaired bytes;
  CR-only, backslash/CR/header, VT-content, LF/CRLF, trailing-space, parity,
  comment/blank, malformed-header, UTF-8/NUL, and EOF controls all completed.

Final fence summary: 43 RED/GREEN pairs, 12 single-subject controls, 23/15/65
multi-subject RED/GREEN/CONTROL over seven subjects, 14 systemd oracle fixtures,
11 environment oracle fixtures, result PASS, extracted production functions,
`block_logic_reimplemented=no`, and unchanged before/after script identity.

## Residuals and safety

- The pre-existing row-8 sandbox-pin disclosure and C1 mount-projection digest
  residual remain explicitly out of this R1-R4 scope.
- A Windows linked worktree needs explicit `GIT_DIR`/`GIT_WORK_TREE` when Linux
  Git accesses historical objects; auditors are required to materialize frozen
  Git-object bytes in run-owned Linux scratch and must treat non-execution as
  BLOCK.
- No host, deployment, credential, service, broker/exchange, ARM, order,
  TESTNET/mainnet, Pine, parity, MTC, or trading action occurred.

