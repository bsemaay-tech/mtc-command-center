# Fable independent re-audit — TS-P0 BLOCK repair (Codex round) — 2026-07-20

Auditor: Claude Fable 5 (orchestrator session; distinct from builder-Codex and from the
sub-agents Codex delegated to)
Target: `C:\TSP0`, branch `feature/ts-p0-baseline`, HEAD `7777273f` + the previously
UNCOMMITTED nine-file repair diff (198+/26−)
Builder report audited: `CODEX_TSP0_BLOCK_REPAIR_REPORT_2026-07-19.md`
Blocking findings being repaired: Codex cross-audit F1a/F1b/F2/F3
(`CODEX_TSP0_AUDIT_2026-07-19.md`), independently confirmed by Fable on 2026-07-19.

## VERDICT: **PASS** — all three BLOCK findings verifiably repaired; zero new findings

Every builder claim I tested reproduced. The repair is minimal, additive, and confined to
exactly the nine claimed files. Note the delegation churn in the build (Cline failure,
stalled DeepSeek, orphan process writing `release_evidence.py` post-termination) made this
diff higher-risk than its size suggests — it was therefore read hunk-by-hunk in full; the
final state is coherent and correct regardless of authorship history.

## Reproduced this session

| Check | Result |
| --- | --- |
| Scope | HEAD `7777273f` unchanged; dirty set = exactly the 9 claimed files; no engine.py/routes.py/config/schema/protected change ✔ |
| Full suites | **218 passed** from `C:\TSP0` AND from `C:\TSP0\IBKR_PAPER_BRIDGE` (PYTHONUTF8=1) ✔ |
| RED proof | New tests vs HEAD production code (copy-aside method — no `git restore` data loss): **9 failed / 45 passed**, failures exactly the three repair areas (secret-safety, non-dict + wrong-scalar manifest types, 4× invalid-meta + future-liveness). Repaired files restored byte-exact (sha256 verified ×3) ✔ |
| F1a replay | All four window meta keys with malformed non-empty values ⇒ **DOWN** with exact `invalid_meta:<key>` (via real `Store`, not mocks) ✔ |
| F1b replay | Future `last_alive_ts` ⇒ **DOWN** `future_liveness`; exact-300s boundary still RUNNING (documented rule preserved) ✔ |
| F2 replay | Re-signed manifests: `hashes` as list/str/None ⇒ exit 2 `invalid_type:hashes`; int `release_commit` ⇒ `invalid_type:release_commit`; dict nested `hashes.config_hash` ⇒ `invalid_type:hashes.config_hash` — all structured, zero tracebacks ✔ |
| F3 replay | 10 dangerous basenames denied (`prod.env`, `my.secrets`, `key.txt`, `.env.prod`, `prod.env.local`, `my.secrets.local`, `key`, …); 9 legitimate names stay in scope (`environment.py`, `secretary.py`, `monkey.txt`, `keyboard.py`, `prod.environment`, …) ✔ |
| Overbroad-denylist attack | Hashed-file set on the REAL tree computed with old tool (from `git show HEAD:`) vs repaired tool: **identical** — no legitimate file silently dropped from drift scope; `excluded: []` on the real tree ✔ |
| Real-pair integration | exit 2; reasons exactly `[repo_commit_mismatch_expected, repo_dirty, repo_runtime_commit_mismatch, source_tree_hash_mismatch]` (`repo_dirty` correct while repair uncommitted); runtime clean + commit matches `008e065e`; config hashes equal ✔ |
| P2RT no-mutation | HEAD `008e065e`, porcelain empty after all probes ✔ |

## Code-read findings (none blocking)

- `window.py`: malformed-meta check distinguishes `None`/`""` (absent/cleared) from
  non-empty garbage — consistent with `reset_window`'s use of `""`; naive `now`
  normalized; `compute_window_state` also rejects negative age so even direct callers
  are protected. `detect_interruption` on corrupt `started_ts` does not stamp, but
  `window_status` reports `invalid_meta` DOWN, so the read model stays fail-closed.
- `check_runtime_baseline.py`: regex change is basename-anchored; no substring
  false-positives found in an adversarial name sweep.
- `release_evidence.py`: every live-compare dereference is now type-guarded; live
  comparison still runs only when structural failures are empty.

## Divergence from builder report (informational)

Builder's pre-fix RED was "6 failed / 37 passed" (B/C tests only — the A test landed
together with its code via the delegated helper). My RED against pure HEAD with the full
new test set is **9 failed / 45 passed**, which subsumes the builder's and adds the A
red. No contradiction.

## Auditor action after PASS

The repair sat uncommitted — a known data-loss hazard in this repo (an uncommitted repair
was already wiped once by a red-proof `git restore` in the TS-P1-007 round). After
issuing this PASS, the auditor committed the exact nine audited files in `C:\TSP0`
(local commit only, no push) to pin the audited state. The commit SHA is recorded in the
session log and handoffs.

## Remaining gates (unchanged)

1. N3/N4/N5 doc-level nits from the first Fable audit (small docs pass).
2. Barış: TS-P0-001 hash-scope confirm, TS-P0-002 release contract (DRAFT),
   TS-P0-003 reset policy (PROPOSED).
3. Push/PR of `feature/ts-p0-baseline`: separate explicit Barış gate.

## Safety

Read-only vs P2RT; no push/PR/merge/deploy; no scheduler/ARM/credential action; probes on
temp Stores/manifests only. Separately: the Day 1 v1 bridge window was found DOWN during
this audit (sleep-related, unrelated to any TSP0 work) — recorded as its own incident:
`INCIDENT_D1V1_SLEEP_STOP_2026-07-20.md`.
