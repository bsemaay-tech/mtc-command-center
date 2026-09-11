# Independent T0 Reviewer Report — WP-P012-FUNDING-RETENTION-20260911

**Reviewer:** fresh accepting T0, `claude-opus-5` xhigh, isolated first-party Claude Max. Not the implementer, not the repair author. No model/effort fallback occurred; the mandated suites were personally executed.

## Verdict: **PASS**

---

## 1. Identity and integrity

| Item | Result |
|---|---|
| Packet `MANIFEST.json` sha256 | `16f14641b51ecc30a953605072f18784e665038c62fc3208a22d67850217c4a1` ✓ matches brief |
| Packet members | 61, **0 missing, 0 mismatched, 0 unlisted files** ✓ |
| Source HEAD | `8fe2ede61ca8bf6cd6c564063680542e6101b276` ✓ candidate |
| Parent | `d1485eee5b2cc02f85d81610d89b7ec7bbf46a6a` ✓ base |
| Branch | `feature/p012-funding-evidence-retention` ✓ |
| Worktree | `git status --porcelain` empty **before and after** all work ✓ |
| Bridge code tree | `c0ad3706d460377a44fe13ce32dff37b668d9274` ✓ |
| Tests tree | `fcb4788d7e1e26323a2acdd703e448b7d9eeea7a` ✓ |
| MTC core `mtc_v2` tree | `e648a48534270a1ed98799734fc9f587aea7d09e` ✓ unchanged (resolved to `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2`) |
| Other MTC subtrees | byte-identical to base except `02_TASKS` and `_AI_MEMORY` (both explicitly approved writeback) ✓ |

Packet re-verified after execution: same manifest digest, 61 members, 0 mismatched. No source/packet/Git/memory writes were made; all my writes are under `C:/tmp/P012_FUNDING_OPUS_MAX_T0_A2_20260911/{results,scratch}`.

Diff scope = 9 files, +1617/−8, exactly the approved five implementation/test/doc paths plus the approved governance writeback and the approved same-scope corrective path. No broker/normalization, types.py, risk, order, or MTC-core change.

## 2. Suites I personally executed

Runner: `subprocess.run(..., cwd='C:/tmp/P012_FUNDING_RETENTION_20260911/IBKR_PAPER_BRIDGE')`, interpreter `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe` (3.12.12), env `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, `TEMP`/`TMP` → my scratch, `-p no:cacheprovider`, external `--basetemp`.

**Full routed Bridge suite**
```
python -m pytest --ignore=TSP1009B.pytest_tmp_s1r1 -q -p no:cacheprovider \
  --basetemp=<A2>/scratch/basetemp_full --junitxml=<A2>/results/junit_full.xml
```
→ **1467 passed, 0 failed, 0 errors, 0 skipped — exit 0**, 117.13 s. JUnit `tests="1467" failures="0" errors="0"`. Matches Lead's 1467/0.

**Focused suite**
```
python -m pytest tests/test_funding_payload_retention.py tests/test_store.py \
  tests/test_reconciliation.py -q -p no:cacheprovider \
  --basetemp=<A2>/scratch/basetemp_focused --junitxml=<A2>/results/junit_focused.xml
```
→ **275 passed, 0 failed — exit 0**, 18.86 s. Matches Lead's 275/0.

Artifacts saved: `results/full_suite.log`, `results/junit_full.xml`, `results/focused_suite.log`, `results/junit_focused.xml` (each log carries CMD, CWD, EXIT).

## 3. Independent negative / retention / migration evidence

I adapted **only** the hardcoded output destination in `probes/retention_probe.py:55` (Lead scratch → my scratch); no Lead/builder file was overwritten. I also wrote my own probe (`scratch/a2_probe.py`) driving the real `Store` API, not the candidate's own tests.

**Gap reproduction (RED/GREEN), same probe, two checkouts**
- baseline `C:/tmp/P012_RECORD_PROSE_20260911` @ v6 → **RED, exit 1**: `retrieval API present: False`, `recovered payload: None`.
- candidate @ v10 → **GREEN, exit 0**: all three normalized fields recovered after close/reopen.
- Decisive cross-check: the ledger `payload_digest` is **identical** on both checkouts — `134490130a396d3087fb32fc5fd5eccf7f7a8513f63ebad5f4641e439d6620f9` — so the eight-field `authoritative()` domain and digest are provably unchanged.
- The probe's attempt is `accepted=False` / `INCOMPLETE`: retention on a **nonaccepted composite attempt** confirmed.

**My own probe: 24/24 checks passed, exit 0** (`results/probe_a2_acceptance.log`)

| Acceptance property | Observed |
|---|---|
| Default target stays v4; capability inactive | `schema_version=4`, `funding_payload_retention_enabled() is False` |
| Verified read distinguishes inactive capability | `FUNDING_PAYLOAD_SCHEMA_INACTIVE` |
| …unknown event | `FUNDING_PAYLOAD_EVENT_UNKNOWN` |
| …unavailable historical payload | returns `None` (not an error, not a fabrication) |
| …damage | reopen fails closed: `MIGRATION_FAILED: v10 retained payload invalid: FUNDING_PAYLOAD_DIGEST_MISMATCH` on parseable-but-edited JSON |
| v9→v10 opt-in migration | `schema_version=10`; historical ledger row **byte-identical**; `COUNT(*) funding_event_payloads == 0` (no backfill) |
| No downgrade | reopening a v10 store with `target=4` stays `10` |
| Nulls stay null | `funding_rate/position_szi/n_samples` all `None`; no `0` substitution |
| Exactly 8 fields | retained dict `== event.authoritative()`, 8 keys |
| Replay idempotent | 1 ledger row, 1 payload row; `funding_total` `-2.5 → -2.5` |
| Identity conflict | `FUNDING_EVENT_IDENTITY_CONFLICT`; both rows bit-for-bit unmodified |
| Atomicity on retained-payload failure | injected failure in `_append_funding_payload_locked` → ledger rows `0`, payload rows `0`, `reconcile_checkpoints` `0`, checkpoint pointer unchanged (`None → None`) |
| Append-only | `UPDATE`/`DELETE` abort with `FUNDING_PAYLOAD_APPEND_ONLY` |

**Fixture oracle is independent, not output-derived:** plain `hashlib.sha256` over the frozen canonical bytes at `tests/test_funding_payload_retention.py:533-535` reproduces `77fb9ccfc5d2dddf90d53b7e2c924b5b240e849cb934dc1633734c3a62bd4a73` (`:538`) — computed by me without any repository function.

## 4. Diff inspection (key points)

- `bridge/store/db.py:9097-9104` — retention is invoked only after a **new** ledger INSERT, inside the enclosing `BEGIN IMMEDIATE` opened at `db.py:8574` (commit `:8747`, rollback `:8749`), which also covers checkpoint insertion. Atomicity is structural, not incidental.
- `db.py` `_migrate_v9_to_v10` — single `BEGIN IMMEDIATE`; pre-existing-object guard; predecessor census equality; explicit `retained != 0 → MigrationError`; `rowcount == 1` version bump; rollback plus a secret-safe failure marker.
- `_decode_funding_payload` — ledger digest is the authority; refuses on digest mismatch, unparseable JSON, wrong domain, non-canonical re-serialization, digest non-reproduction, and identity mismatch.
- `_all_table_census(exclude=...)` preserves the previous v8→v9 default (`exclude=None` → `_KILL_EVIDENCE_OBJECTS`), so predecessor behavior is untouched.
- Capability predicates extended additively (`full_reconcile`/`durable_risk`/`exposure_controls`/`kill_evidence` all include v10); `funding_payload_retention_enabled()` is v10-exact.
- `tests/test_partial_fill_protection.py:2429` — `10 → 11` only, assertions unchanged; matches the approved same-scope corrective path and `tests/test_store.py:480`.
- `DECISIONS.md` and `TASK_HISTORY.json` are pure appends (`OD-20260911-FUNDING-1`, `HIST-2026-0042`); no collision, prefix preserved.
- Doc §12 states the limits correctly: normalized not raw, no venue authenticity/coverage/oracle association, no new identity, no risk/order/KILL change.

## 5. Findings

**Mandatory findings: none.**

**Optional nits (do not block; no required finding is concealed here):**
1. `IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:50-52` lists `FUNDING_PAYLOAD_DIGEST_MISMATCH`, `_MALFORMED`, `_DOMAIN_MISMATCH` but omits `FUNDING_PAYLOAD_IDENTITY_MISMATCH`, which the code does raise (`bridge/store/db.py`, `_decode_funding_payload`, identity branch). Doc-only completeness.
2. `APPROVED_SCOPE.md:42` names `IBKR_PAPER_BRIDGE/HANDOFF.md` as required governance writeback; it is absent from this candidate diff (the other three writeback paths are present). Lead owns writeback — flagging for reconciliation, not a code defect.
3. In my tamper case the store failed closed at reopen before the verified-read path could be exercised on that same DB; the read-path refusal for tampered bytes is covered by the candidate's own focused tests and by code inspection, not separately by my probe.

## 6. Limitations of this review

- All databases were synthetic and throwaway under my own root. No host, credential/profile read, network, broker, production DB, paid API, deployment, capture or trading. No other agents were used.
- I verified behavior at this commit with this Python 3.12.12 venv on Windows; I did not run Linux CI, and protected current-head CI remains a separate gate.
- The call-trace/mutant/nonfinite artifacts in `evidence/` were read as context; I independently reproduced the baseline-gap RED, candidate GREEN and the acceptance-case matrix myself rather than relying on them.
- R34/R35 were not re-audited or resealed; no reseal or old-acceptance audit was performed.
- The prior unfinished Pro attempt was not adopted in any form; every count above is from my own execution.