# RP7 cap-override final owner boundary — 2026-08-15

Status: **NON-ACCEPTED / OWNER DECISION REQUIRED**.

The single owner-authorized RP7 cap-override repair is consumed. Both required
fresh T0 flagship audit slots have now executed against frozen subject commit
`2d0f24d0965c4ba7e7942dddac4fcac3bbb3240b`. Neither returned an accepting
verdict, and no further RP7 repair or audit cycle is authorized.

## Frozen identities

| artifact | bytes | SHA-256 |
|---|---:|---|
| `RP7-WPI-RO.sh` | 132886 | `a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243` |
| `SELF_QA_RP7.md` | 504144 | `72aab351fc9f0d5881bbac995985338dc983777978b1787b4b5abe3bf0fda58f` |
| `STATUS_RP7.md` | 12213 | `df44704c4099459d2860fd6ddbfc0b659b981eb4ecbe06a7f1ef89b99499ad65` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 41843 | `4e5d38d422ab836aca3e2421f0430b4cdb72680c5d34de86e33d14b2c0fd7cde` |

Filled audit prompt commit:
`d4e90cb05bfbe227d17ce6264f0d3c19d3b5337f`.

## Mandatory T0 results

| slot | exact execution | verdict | disposition |
|---|---|---|---|
| Codex | fresh ephemeral `gpt-5.6-sol`, `xhigh`, isolated `C:\R7AX` | **BLOCK** | Mandatory WSL fence unavailable in the Codex sandbox; three REQUIRED findings independently reproduced by the Lead. |
| Claude | fresh `claude-opus-5`, `xhigh`, isolated `C:\R7AC`, no resume/continue | **REQUEST_CHANGES** | Full WSL fence executed; one additional REQUIRED finding independently reproduced by the Lead. |

Claude's CLI result was successful after 1,513,688 ms and recorded the audit
work under canonical model `claude-opus-5`. Client telemetry also listed one
20-output-token Haiku utility call; it did not fill an auditor slot, produce the
verdict, or replace the explicitly selected Opus model. The isolated worktree
delta was exactly the named Claude verdict file. Its durable copy is byte-exact:
30179 bytes / SHA-256
`BA1A16E0661423AC5314A2E2561C86D65DC01D7391602B3A8335E8EE5E24F77F`.

## Lead adjudication — unresolved REQUIRED findings

### R1 — row-9 evidence bypasses the production normalization boundary

**ACCEPTED / REPRODUCED.** The production caller obtains effective
`Environment` from `systemctl show` and passes that normalized rendering to the
row-9 parser. The test instead injects the raw mid-name quote spelling directly
into fake `systemctl` output. Claude confirmed that systemd accepts the raw
mid-name quote form and that the repaired parser accepts the corresponding
normalized clean assignment. Claude's successful raw-tokenizer attack therefore
does not close the production-boundary finding.

### R2 — frozen provenance package contradicts itself

**ACCEPTED / REPRODUCED.** `STATUS_RP7.md` and current report prose record the
Lead run, while `SELF_QA_RP7.md` and an earlier report identity block still say
that no independent Lead run exists. The frozen evidence package does not carry
one coherent provenance state.

### R3 — dispatched exact-transcript contract is not satisfied

**ACCEPTED / REPRODUCED.** The kickoff requires exact transcript reproduction.
The package and Claude run instead reproduce 155 of 156 normalized lines and
exclude a run-varying mount-projection digest. That variance is technically
explained but was not authorized as an exception in the dispatched contract.

### R4 — row-6 bare-CR terminator false PASS

**ACCEPTED / INDEPENDENTLY REPRODUCED.** From the exact frozen Git blob, the
embedded production parser uses `text.split("\n")` followed by
`physical.rstrip("\r")`. Against the same fixture bytes containing one bare CR
before `[Install]`, the Lead obtained:

```text
SUBJECT bytes=132886 sha256=a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243
FIXTURE cr_bytes=1 lf_bytes=5
PARSER rc=0 stdout=[OK install_section=absent sections=2] stderr_bytes=0
SYSTEMD rc=0
bare-cr.service:4: Unknown key 'ZZZBogus' in section [Install], ignoring.
LEAD_REPRO result=PASS contradiction=systemd_real_install_vs_frozen_absent
```

Systemd 259 therefore parsed a real `[Install]` section while the frozen RP7
predicate returned the accepting `install_section=absent` disposition. This is
a source-level false PASS. Claude also supplied RED/GREEN candidate evidence,
but no candidate repair was applied because the owner-authorized cycle is
exhausted.

## What is closed

- All four frozen identities re-derived exactly from Git object bytes.
- The complete rows-1-9 fence ran against an exact LF-byte WSL materialization:
  rc 0, 156 lines, zero stderr, zero abort/collision/ERR-trap markers, and all
  nine live systemd oracle arms.
- The cap-override two-subject D026 mechanics execute historical and repaired
  blobs in separate processes with exact identity and terminal assertions.
- The frozen candidate was not modified during either audit or this
  adjudication.

These facts are useful evidence but cannot outweigh the four unresolved
REQUIRED findings or convert either flagship result into acceptance.

## Boundary and next authorized action

RP7 remains **BLOCKED at the owner boundary**. Packet 10, packet 11, and freeze
preparation cannot be filled as accepted RP7 outputs. Pathscope separately
remains at its already-recorded owner boundary; it is not reopened here.

No further writer or auditor may be launched unless Barış explicitly authorizes
a new bounded RP7 cycle. If authorized, the minimum scope is exactly R1-R4:

1. bind row-9 D026 to the real manager-normalization boundary;
2. reconcile the frozen provenance statements;
3. make transcript determinism exact or explicitly ratify its normalization;
4. repair the row-6 systemd terminator model and add bare-CR/multi-CR D026 plus
   terminator-varying live oracle coverage.

A new T0 repair would still require both fresh flagship execution audits under
the exact-model rules. All host, deployment, credential, service, broker,
exchange, ARM, order, TESTNET, mainnet, Pine, parity, MTC, and trading gates
remain closed.
