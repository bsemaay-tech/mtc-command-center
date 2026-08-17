# Artifact identity + secret-scan record — `ebada020` (2026-08-03)

Closes gap 3 of `GATE_A_QUEUE_D_INTEGRATION_STATUS_2026-08-03.md`. Written by Claude Opus 5 (Lead)
from first-hand execution on the frozen tree and the built payload. No transfer, install, service,
runtime, credential, broker, ARM, order, TESTNET, mainnet or economic action occurred.

---

## 1. Frozen identity

| Item | Value |
|---|---|
| Source commit | `ebada020a59edf539f60acfbb3a6bf870c8679e9` (`codex/gate-a-integration`, pushed) |
| Baseline | `origin/master` `637307e83951ffe23e768ed8e50ddaf8712b0660` |
| Artifact path | `C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9` |
| `RELEASE_SHA` marker | `ebada020a59edf539f60acfbb3a6bf870c8679e9` — equals the source commit |
| `RELEASE_SHA256SUMS` SHA-256 | `8FC30864BA342E53DCFC6B2938124F91D005F02671A332580A723F38FD4700C9` |
| Manifest entries | 7,059 |
| Tracked paths in frozen tree | 7,058 |
| Built | 2026-08-03 05:10:54 local, exactly once |

The manifest hash was recomputed independently here and matches the value recorded at build time.

## 2. Secret scan — content-redacted, `SECURITY_BASELINE.md` §2 contract

Executed over every non-binary tracked blob of the frozen tree `ebada020` with `git grep -I -l`, so
only category counts and paths could ever be emitted. No matched text was printed, copied or
persisted at any point.

| Signature category | Frozen-tree category/path hits |
|---|---:|
| Private-key block (PEM / OpenSSH / PGP) | 0 |
| AWS access key | 0 |
| GitHub token | 0 |
| Slack token | 0 |
| OpenAI token | 0 |
| Anthropic token | 0 |
| xAI token | 0 |
| Telegram bot token | 0 |
| Ethereum private key | 0 |
| **TOTAL_CATEGORY_PATH_HITS** | **0** |

Because `package.sh` builds its source tree from `git archive` of this exact commit, the scan covers
the source files that enter the payload. This reproduces the WP-I result on the new integrated tree.

## 3. Line-ending verification of the built payload — the A-2 killer

Byte-accurate 0x0D counts on the built payload, not on the repository:

| Payload file | CR bytes | LF bytes |
|---|---:|---:|
| `deploy/linux/install.sh` | **0** | 434 |
| `deploy/linux/lib/common.sh` | **0** | 222 |
| `deploy/linux/package.sh` | **0** | 172 |
| `deploy/linux/rollback.sh` | **0** | 185 |
| `deploy/linux/verify.sh` | **0** | 252 |

Across the entire `IBKR_PAPER_BRIDGE/` payload only two files contain any 0x0D byte at all —
`docs/screenshots/overview.png` and `docs/screenshots/trading.png` — which is binary image content,
not line endings. **The defect that failed Gate A at A-2 on 2026-08-02 is not present in this
payload.** That is a necessary, not sufficient, condition: A-2 still has to be executed for real.

## 4. NEW FINDING — the rebuilt artifact dropped two accepted WP-I documents

Manifest path diff against the accepted WP-I candidate artifact `1adf9ae5…` (7,060 entries):

```
present in 1adf9ae5, ABSENT from ebada020:
  IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md
  MTC_COMMAND_CENTER/11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md

present in ebada020, absent from 1adf9ae5:
  IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py     (expected — Queue C)
```

Cause, verified: both documents exist on the records branch `feature/donchian-crypto-ladder` and in
the `1adf9ae5` build line, but **never landed on `origin/master`**. `codex/gate-a-integration`
descends from `origin/master`, so the rebuild silently shipped without them.

**Impact — measured, not assumed:** neither path is referenced anywhere in `IBKR_PAPER_BRIDGE/`
source or in the Gate A runbook or Addendum A. So this is **documentation drift, not a functional
Gate A blocker.** But the artifact that Gate A would install no longer carries its own security
baseline, and the accepted WP-I evidence set is no longer self-contained inside the payload.

**Owner/Lead decision required:** either (a) accept the drift and record that the security baseline
lives only on the records branch, or (b) land the two documents onto the build line and rebuild —
which would produce a new SHA and invalidate this artifact's identity. Do not silently do (b).

## 5. Scope and boundary

Read-only inspection plus one content-redacted scan. Nothing was written into the artifact, no
branch head moved, `origin/master` is unchanged, and no host was contacted.
