# WP-S — MINIMUM S3, AUDIT 1 ROUND 2: NON-ACCEPTING (2026-07-31)

**Status: STOPPED pending an owner decision on the round bound.** One required finding remains,
both canonical auditors converge on it, and it is well-specified. No further repair round has been
started.

**Lead:** Claude `claude-opus-5`. **Implementer:** Codex CLI `gpt-5.6-sol` xhigh.
**Authorisation:** `11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md`.
Companion record: `11_TRIAGE/WPS_TSP1009B_S2_CLOSURE_RECORD_2026-07-31.md`.

## 1. Artifact chain

| Commit | Meaning | Suite |
|---|---|---|
| `678e8b94` | original blocked S2 artifact (entry floor) | 2F / 1113P |
| `d3a45529` | S2 round 1 — non-accepting (introduced R1) | 2F / 1117P |
| **`0c65a731`** | **S2 round 2 — ACCEPTED**, both auditors PASS-WITH-NITS, 0 required | 2F / 1118P |
| `c26b00a4` | S3 round 1 — non-accepting, **6 required findings** | 2F / 1125P |
| **`e78eff59`** | **S3 round 2 — non-accepting, 1 required finding** | 2F / 1131P |

Branch `feature/ts-p1-009b-s2-closure`, worktree `C:/WPS`, all pushed. Every suite figure was
independently reproduced by the Lead and by both auditors. The two failures are the pre-existing
stale KVM2 ledger hash and the stale `schema_version == "2"` expectation, both confirmed to fail
identically on the `origin/master` Bridge tree and both outside the frozen allowlist.

## 2. Audit 1 verdict history

| Sub-loop | Round | Artifact | Codex `gpt-5.6-sol` xhigh | Claude `claude-opus-5` xhigh | Net |
|---|---|---|---|---|---|
| S2 | 1 | `d3a45529` | BLOCK (environmental; 0 code defects) | REQUEST_CHANGES (R1) | non-accepting |
| S2 | 2 | `0c65a731` | PASS-WITH-NITS | PASS-WITH-NITS | **ACCEPTED** |
| S3 | 1 | `c26b00a4` | REQUEST_CHANGES (6 required) | REQUEST_CHANGES (1 required) | non-accepting |
| S3 | 2 | `e78eff59` | REQUEST_CHANGES (1 required) | REQUEST_CHANGES (1 required) | non-accepting |

## 3. The remaining required finding — both auditors, same defect

**F4's identity containment is incomplete.** Round 2 added a guard for three predicates —
`group_id` non-empty, `trade_id` non-null, trade row present — and quarantines those as
`KILL_LIFECYCLE_IDENTITY_MISSING`. Those three cases are genuinely contained and were verified
fail-closed for new risk (trade stays open, ARM blocked, ACK unreachable, operator-visible event).

But the guard checks a **different identity set than the store does**, so schema-admitted rows still
reach an uncontained exception on the `drain_queued_events` → `sync_broker_state` → `reconcile()` →
unguarded `BridgeEngine.start()` chain — the R1 startup wedge, with **zero durable evidence**.

Four live reproductions across the two auditors:

| Input | Outcome |
|---|---|
| Non-empty but **dangling** `group_id` (no matching `kill_requests.episode_id`) | `KILL_LIFECYCLE_DEFERRAL_RECORD_FAILED` out of `start()`; `queue_depth=1`; `event codes: {}` |
| v8 DB with a `KILL_FLATTEN` order, migrated via the supported `initialize(target_schema_version=9)` | same; `kill_requests` rows `0`, because `_migrate_v8_to_v9` preserves the predecessor census by design |
| `trade_id="not-an-integer"` | **`ValueError`** out of `start()` — `int(trade_id)` runs at `orders.py:3123` *before* validation; no evidence |
| Default schema **v4** and v8 | `KILL_SCHEMA_INACTIVE` out of `start()` via `_require_kill_schema()`; no evidence |
| Two-`Store` interleaving clearing `group_id` between the early guard and the second lookup | reaches the supposedly dead `RuntimeError("KILL_LIFECYCLE_DEFERRAL_IDENTITY_MISSING")` — **it is not dead** |

Root cause: `orders.group_id` is plain nullable `TEXT` with **no foreign key** to
`kill_requests(episode_id)` (`db.py:807`), `insert_order()` accepts nulls, and the v8→v9 migration
preserves predecessor `orders` rows into an empty `kill_requests` table. The guard validates
*shape*; `record_kill_lifecycle_deferral` additionally requires the episode to be **durably bound**.

The contract doc added this round asserts the opposite — it claims an order "missing its episode …
is quarantined … without unwinding startup". That is precisely the case the guard does not test, so
the documentation is currently wrong about a safety property.

**Required repair (both auditors agree on the shape):** parse and validate the order's episode and
trade identity **safely and durably** before any accounting or deferral — including a
`kill_requests` existence check and a non-raising integer parse — then quarantine and consume
invalid identities without an uncontained exception, and eliminate the residual `RuntimeError`.

## 4. Where the two auditors disagreed, and the resolution

They split on whether F2's propagation is correct. Reconciled, both are right about different
reason codes:

- **`KILL_STALE_EVIDENCE_RECORD_FAILED`** — a genuine EP-4 evidence-store fault. Propagation is
  defensible: the process stops taking new risk while durable state stays `KILLED`. A contained
  operations state would improve availability, but minimum S3 does not require it. **The Lead's
  original reading holds for this code.**
- **`KILL_LIFECYCLE_DEFERRAL_RECORD_FAILED` and `KILL_SCHEMA_INACTIVE`** — reached from ordinary
  schema-admitted *identity data* on a healthy, writable database, and the unwind writes zero
  evidence. Propagation here is wrong; these must be quarantined earlier. **This is §3, and it is
  where the Lead's reading was over-broad.**

The deferral allowlist itself (`KILL_EPOCH_REQUIRED`, `KILL_EPOCH_STALE_WRITE`) is confirmed by both
auditors as the correct and complete set of deferrable conflicts.

## 5. What round 2 genuinely repaired

Confirmed by both auditors against the real source, with independent probes:

- **F1** — suppression now consults durable trade state; the cross-writer strand is closed. Non-kill
  and unbound events fall through instead of being suppressed.
- **F3** — `_synced_fills` binds the full delivery identity; a differing payload is quarantined as
  `FILL_ID_CONFLICT` instead of vanishing. Exact-redelivery dedup is behaviourally unchanged.
- **F5** — every `return True` in `_ingest_fill` routes through `_mark_fill_consumed`; the
  `CONFLICT` branch pops the deferred entry explicitly. No leak. (`order is None` retains both queue
  and map entries in sync, so it cannot strand.)
- **F6** — the deleted S2 assertion is restored at `test_engine_dryrun.py:1106`. **Zero `-` lines in
  `tests/` across the whole S3 delta** — independently verified by the Lead and by an auditor.
- **F4** — contained for the three shape predicates it does check; incomplete for durable binding
  (§3).
- **F2** — mechanism correct (reason-code allowlist replacing catch-by-class); consequence correct
  for the evidence-store fault, wrong for identity data (§4).

Test quality this round is genuine: F1/F2/F4/F5 all use two distinct `Store` instances over shared
storage. F3's single store is correct because the mechanism under test is the in-memory
`_synced_fills` shortcut. No tautological or incidentally-passing test was found — a real
improvement on round 1, where F3's case passed only because of an accidental ordering.

**S2 non-regression confirmed intact** by both auditors: `_canonical_trade_close_values`; the exact
`!=` + type evidence comparison; the deliberate `exit_qty`/`entry_qty` `abs_tol=1e-12`
**completeness** tolerance; `BEGIN IMMEDIATE` + `_assert_kill_epoch_in_tx`; and the `return False`
deferral. A stale epoch still rolls back both writes, still records EP-4 evidence, and still raises
to the store's caller.

## 6. THE OWNER DECISION — how the round bound applies

This is the reason work stopped rather than continuing into another repair.

Plan §25 defines **Audit 1 as one checkpoint** covering "S2 closure and minimum S3", and §23a/§20
cap it at "maximum three non-accepting repair/re-audit rounds per audit checkpoint; after the third
non-accepting verdict, stop and report to the owner — do not enter a fourth round."

Two defensible readings:

| Reading | Count | Consequence |
|---|---|---|
| **Strict** — one checkpoint, count every non-accepting verdict | S2 r1 + S3 r1 + S3 r2 = **3, exhausted** | Stop now. WP-S ends non-accepting at `e78eff59`. Everything downstream stays gated: §23b step 7 makes WP-L Phase 1 conditional on Audit 1 accepting. |
| **Looser** — S2's loop terminated *successfully*, and §16 requires two separate accepting verdicts, so S3 is its own loop | S3 r1 + r2 = **2, one round left** | One final repair round on the single well-specified finding in §3. |

**Lead recommendation: the looser reading.** A round bound exists to stop thrash on an unresolvable
problem. S2 did not thrash — it resolved and was accepted by both canonical auditors. S3's remaining
defect is a single, precisely characterised, well-scoped repair that both auditors describe the same
way. The Lead did not adopt this reading unilaterally, because the strict reading is genuinely
plausible and choosing the interpretation that permits continued spending is not the Lead's call.

Under either reading, **no fourth S3 round** will be started without a fresh explicit decision.

## 7. Hour and funding accounting — stated, not absorbed

| Activity | Budgeted | Actual |
|---|---:|---:|
| S2 blocker repair (rounds 1–2) | 4 h | 4.0 h |
| Audit-1 first pass (S2 accepting verdict) | 2 h | 2.0 h |
| S3 implementation | 4 h | 4.0 h |
| S3 Gate-5 first pass | 2 h | 2.0 h |
| **WP-S subtotal** | **12 h** | **12.0 h — allocation fully consumed** |
| S3 round-2 repair | — | **1.5 h from CONTINGENCY** (Lead sign-off recorded here) |
| S3 round-1 and round-2 re-audits | — | **2.0 h from WP-R** audit reserve |

Funding follows §20/§22: repairs from contingency, re-audits from WP-R, never the reverse, and
contingency never funds audit work. Contingency consumed **1.5 / 5 h**; WP-R consumed **2.0 / 6 h**.
Contingency is a hard ceiling — if it exhausts while a safety requirement is unfunded, that is a
BLOCK and an owner report, per §22.

Approximate AI spend on WP-S to date: **~$85**. Of that, **~$25 was wasted** by a Lead tooling
defect — see §8.

## 8. Lead tooling defect — recorded honestly

`resilient_dispatch.sh` decides whether a run succeeded by testing whether the output file was
written. The S3 round-1 Codex audit was dispatched through it **without `-o <out_file>` in the codex
argv**, so every run wrote its verdict only to the log, `$OUT` stayed empty, and the wrapper judged
each a "lost run" and retried. **Five complete `xhigh` audits were paid for and discarded.** The
verdict was recovered intact from the log, so no evidence was lost — only budget.

Fixed at commit `5f0cf2fb`+: the wrapper now refuses to start unless the output path appears in the
command arguments. A missing output flag is a usage error, never a retry loop.

## 9. Safety statement

No implementation outside the frozen allowlist. No risk threshold invented or changed. No
credential, wallet secret, API key, host, IP, or private path written or sent to any model — the
docs diffs were independently secret-scanned clean. Default schema target remains v4; no migration
was added or executed. No Pine, parity, MTC strategy, or protected-scope file touched. No bridge
start against a real broker, no network, staging, Ubuntu execution, VPS, deployment, TESTNET, ARM,
or live-capital action occurred. Both audit worktrees were verified clean with unchanged HEAD after
each audit, so no auditor edited the artifact it judged.
