# Fable verification audit — TS-P0-001..004 chain (third independent pass, consolidating)

Date: 2026-07-19
Verifier: Claude Fable 5 (orchestrator session — issued the build prompt; distinct from the
builder session, the first Fable-audit session, and the Codex cross-audit session)
Target: `C:\TSP0`, `feature/ts-p0-baseline`, HEAD `7777273f` off `008e065e`
Prior verdicts: Fable independent audit **PASS-WITH-NITS**
(`FABLE_TSP0_INDEPENDENT_AUDIT_2026-07-19.md`) → Codex cross-audit **BLOCK**
(`CODEX_TSP0_AUDIT_2026-07-19.md`)

## CONSOLIDATED VERDICT: **BLOCK stands** — Codex findings independently confirmed; repair before push/PR

This session reproduced the load-bearing claims of BOTH prior audits on real code and real
runs. The build quality claims hold (210×2, RED proofs, determinism, no-mutation, P2RT
safety). The Codex BLOCK findings also hold — and two of them break TS-P0-003's core
acceptance property, so they outrank the earlier PASS-WITH-NITS.

## Codex BLOCK findings — reproduced this session

| # | Finding | My reproduction |
| --- | --- | --- |
| F1a | Malformed persisted `window_interrupted_ts` → `_parse_ts` returns None → recorded interruption silently vanishes → **RUNNING** | Confirmed: corrupt marker + ARMED + fresh liveness ⇒ `RUNNING`. Fail-open on the exact property the task exists for (corrupt evidence must fail DOWN). |
| F1b | Future `window_last_alive_ts` → negative age always ≤ stale threshold → **RUNNING forever**, even for a dead bridge | Confirmed: `last_alive = now + 365d` ⇒ `RUNNING`. Staleness check must reject future timestamps. |
| F2 | Re-signed manifest with `"hashes": []` → `release_evidence validate` uncaught TypeError → traceback, **exit 1** (contract 0/2/3) | Confirmed earlier this session with the equivalent non-dict payload (string); list takes the identical guarded-skip → dereference path. Same class as Fable N1, correctly escalated: type validation before dereference. |
| F3 | `prod.env`, `my.secrets`, `key.txt` are opened and hashed despite the secret-safety boundary | Confirmed: `_is_secret_name` returns False for all three (patterns are prefix-anchored `^\.env…`/`^secrets?…`; `.txt` not in the extension class). Broader than Fable N2 (which named prod.env/config.env only). |

## Also verified this session (build-quality claims hold)

- Worktree facts exact; diff isolation (2 modified + 9 added, zero pre-existing tests
  touched); **210 passed from both CWDs**; RED proof reproduced and restored blob-clean.
- Real-pair integration: exit 2 with exactly three reasons incl. `source_tree_hash_mismatch`
  — the three-reason result at final HEAD is CORRECT (N3 stands corrected of record).
- Self-pair MATCH exit 0; byte-identical output across runs with pinned `--timestamp`.
- Independent read of all three production modules + additive engine/routes wiring.
- `C:\TSP0` clean at `7777273f`; P2RT HEAD `008e065e` porcelain-clean after every probe;
  bridge ARMED, run `paper-20260719185026`, reconcile fresh. Window unaffected.

## Audit-chain lesson (recorded honestly)

The first Fable audit verified the never-false-active property only over WELL-FORMED
persisted evidence (the sweep enumerates parsed values, not corrupt strings or future
clocks) and ranked the denylist/exit-code issues as nits. Codex attacked the evidence
ENCODING layer and the clock, and found the fail-open paths. This verifier's own first
code read missed F1 as well. Adversarial audits on safety code must attack the storage
representation and time domain, not only the parsed state space — fold this into future
audit checklists.

## Disposition (matches NEXT_STEPS repair list)

1. **TS-P0-003 repair (required):** malformed/unparseable window meta ⇒ DOWN (never
   RUNNING); future `last_alive_ts` ⇒ not fresh (DOWN or clamp+flag); committed
   invalid-meta and future-clock tests.
2. **TS-P0-002 repair (required):** validate container/scalar types before dereference;
   non-dict `hashes` ⇒ structured exit 2; wrong-shape tests.
3. **TS-P0-001 repair (required):** extend/document secret exclusions (`*.env`,
   `*.secrets`, decide `key.txt`); spy/no-leak tests for the new patterns.
4. Re-audit after repair (Codex per NEXT_STEPS), then the unchanged Barış gates:
   hash-scope confirm, release-contract approval (DRAFT), reset-policy confirm.
5. Push/PR of `feature/ts-p0-baseline` stays **BLOCKED** until repair + re-audit + Barış.

## Safety

Read-only + local tests + subprocess/import probes on temp data. No push/PR/merge/deploy,
no P2RT write, no scheduler/ARM/credential action. `C:\TSP0` left clean at `7777273f`;
Day 1 v1 monitoring window verified unaffected before and after.
