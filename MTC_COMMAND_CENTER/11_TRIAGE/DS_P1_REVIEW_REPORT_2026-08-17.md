# DeepSeek run report  (2026-08-17T22:25:37)

## Completion report
All four inputs read and cross-checked. Review complete.

## SPEC-COMPLIANCE TABLE

| # | p1_spec required content | Present | Substantive | Location / notes |
|---|---|---|---|---|
| 1 | Header: artifact = Package 1 architecture contract pack, T2 documentation, governs FUTURE separately-gated T0, nothing activates | YES | YES | Header + "Explicit non-authorization"; repeated activation denial |
| 2 | Header: worktree HEAD hash | YES | YES | `b08aab35f7625e481c4a06f47ceffd1fd0740216`, with docs/30 HEAD-parity note and disclosed pointer drift (`docs/01:761`→`:795`) |
| 3 | Section A — worker identity (tuple, uniqueness/immutability, P&L/state/order-identity separation, docs/23-consistent) | YES | YES | A.1: 7-field tuple, never-reuse `worker_id`, active-tuple uniqueness, retire+successor immutability, per-worker ledgers/state namespaces, dual-identity extension via new domain version, flagged docs/23 schema-v3 tension |
| 4 | Section A — store model (settled per docs/30 OR OPEN with options, consequences, labeled recommendation) | YES | YES | A.2: OPEN per `docs/30:320-322`/`:899`; three options + consequences; recommendation explicitly labeled "a recommendation, NOT a decision"; decision stays OPEN |
| 5 | Section A — Guardian veto semantics (inputs, 3-tier scope, precedence vs worker-local, fail-closed, thresholds later) | YES | YES | A.3: read-only evidence-derived inputs, per-order/pause/global tiers, risk-reducing exits excluded, veto-not-mutate, AND-gate precedence, fail-closed no-new-entries, thresholds deferred to later owner gate |
| 6 | Section B — all eight conditioned decisions | YES | YES | B.1 worker boundary, B.2 feed topology, B.3 subaccount fallback, B.4 subaccount eligibility, B.5 agent-wallet assignment, B.6 same-symbol netting, B.7 margin mode, B.8 API-limit budget — each with stateable-now + unfrozen/blockers |
| 7 | Section B — single-account/virtual-book fallback stated as DEFAULT until account eligibility separately established (volume gate claim a + s) | YES | YES | B.3 "EXPLICIT DEFAULT (per Gate-1)"; subaccount topology framed as UPGRADE branch; B.4–B.8 assume it |
| 8 | Section B — 1200 weight/min IP budget and 10-connection WS cap treated as VPS-shared resources (claims n, o); per-worker budget allocation mandated | YES | YES | B.1 and B.8 both state VPS-wide sharing across ALL workers and mandate a central allocator with per-worker budgets |
| 9 | Explicit non-authorization section | YES | YES | Documentation-only; standing prohibitions restated (no VPS/host, credentials, exchange-account/wallet/subaccount actions, TESTNET/MAINNET, ARM/orders, Pine/parity/MTC, V1 mutation) |
| 10 | Self-verification section | YES | YES | Section-B provenance, repo provenance, flagged resolutions (docs/23 domain version, A12 semantics, A4 caveat), read-only discipline, counts |

## SECTION-A FINDINGS

- **Worker identity (A.1) — settled, cited, no finding.** The 7-field tuple, per-field rationale, uniqueness rules (surrogate `worker_id` never reused; active natural-key uniqueness; same-symbol lever gated CLOSED by B.6), immutability (retire + successor, no inheritance), and separation rules are all contract text with specific citations (`docs/30`, `docs/21`, `docs/23`). The docs/23 interaction is handled correctly: dual identity is extended via a NEW domain version, the single-strategy schema-v3 pin is flagged as a protected future-T0 migration, and `docs/23` is not contradicted or modified.
- **Store model (A.2) — OPEN, correctly labeled, no disguised decision.** The pack cites `docs/30:320-322`/`:899` as the genuine leave-open authority, presents three options with consequences, and labels the hybrid recommendation explicitly as "a recommendation, NOT a decision." The decision itself is stated to stay OPEN and "NOT frozen by this pack." This is the compliant alternative under review requirement (B).
- **Guardian veto semantics (A.3) — settled semantics, no thresholds, no finding.** Inputs are read-only and evidence-derived (reconciliation opt-in flagged as unavailable until a future gate); three veto tiers; risk-reducing exits outside veto scope; "vetoes but does not mutate" with citations (`docs/30:284-285`, `:628-632`, `:840-841`); AND-gate precedence with worker-local risk; fail-closed defaults (no new entries, exits never blocked, logged reasons); all numeric thresholds explicitly deferred. Settled as contract text with citations throughout.

## SECTION-B EVIDENCE-TRACE FINDINGS

No evidence-trace violations found. Every exchange-behavior statement in B.1–B.8 traces to a P7 claim id whose status is VERIFIED, and the [V]/[E] evidence levels are reproduced correctly:

- **Claims n/o shared-resource framing:** "aggregated weight limit of 1200 per minute" cited as n [V]; WS caps (10 connections / 30 new/min / 1000 subscriptions / 10 unique users / 2000 msg/min / 100 inflight) cited as o [E]-only, exactly as P7 row o states. Both are treated as VPS-shared across all workers (B.1, B.8) — required check satisfied.
- **Fallback default:** B.3 quotes claim a [V] verbatim and ties the DEFAULT virtual-book branch to claim s (ACCOUNT-LEVEL-ONLY), with migration blocked on s and r. Required check satisfied.
- **Same-symbol netting:** B.6 keeps h UNKNOWN as the primary blocker (with j, s, virtual-book validation, and the supervised account-level check also named) and preserves the conservative closure without asserting any netting mechanic. Required check satisfied — the netting stance is unfrozen; only reopening is conditioned on verified mechanics.
- **Claim-by-claim trace:** a–g, i, k, l, m, n, p all cited with [V] quotes matching the P7 table verbatim; [E]-only rows o and q are flagged as [E]-only with the P7 §0 verbatim-confirmation pass named as a freeze precondition; c and r sub-scope UNKNOWNs and the l residual UNKNOWN are reproduced accurately; s is used only as an ACCOUNT-LEVEL-ONLY blocker. The third-party one-way-netting consensus appears only as a named non-source. No statement leans on a fact absent from the P7 record.

## REQUIRED FINDINGS

none

## NITS

1. **B.6 heading uses "REMAINS CLOSED" instead of the "UNFROZEN" label used by the other seven subsections.** The body does contain an "Unfrozen — blocking items" list and the closure is the conservative, non-exchange-dependent status quo (reopening is what requires verified mechanics), so this is not a required finding — but re-titling to something like "UNFROZEN (conservative closure preserved)" would remove ambiguity.
2. **B.7 introduces one blocker not present as a P7 claim row:** "which abstraction mode the actual account is in … an account-level fact in the same family as s." The pack transparently flags that "no row covers it" and uses it only to keep the decision unfrozen, so it is a conservative gap statement, not a relied-upon exchange fact — but it slightly extends P7's ACCOUNT-LEVEL-ONLY inventory by analogy.
3. **Repo line citations (docs/30, docs/23, docs/21, bridge/app.py, requirements.in) are not independently verifiable from the four review inputs**, which are the only files in scope for this read-only slot. They are present, specific, internally consistent, and the pack discloses its worktree HEAD and the one pointer drift; accepted as-present.

VERDICT: ACCEPT

## Files written: []

## Full transcript

### system
You are DeepSeek operating as a sandboxed code-editing subagent in the repo C:\LAB\Tradingview_LAB_CLEAN. You can ONLY touch files via the provided tools. Writes are restricted to an allowlist; protected files (Pine/parity/schemas) are refused. NEVER attempt git/commit/push. Make the minimal edits the task specifies, verify with py_compile + run_python, then call finish() with the EXACT report structure the task asks for. If a write is DENIED, do not work around it — report it.

### user
File paths are relative to the repository root C:/LAB/Tradingview_LAB_CLEAN - all four input files are in the _night_review_inputs/ folder; read them with those exact relative paths and do not search elsewhere. You are the OFFICIAL T2 reviewer (one reviewer, one round, read-only) for the Package 1 V2 architecture contract pack. Write no files. Inputs: the pack, its authoring spec (p1_spec.md), the Gate-1 scope record, and the accepted Package 7 verification record (the pack's ONLY admissible source of exchange facts). Review requirements: (A) Spec compliance: every required-content item of p1_spec.md present and substantive (header with worktree HEAD; Section A with worker identity, store model, Guardian veto semantics; Section B with all eight conditioned decisions; non-authorization; self-verification). (B) Section-A discipline: worker identity and Guardian semantics must be settled contract text with citations; the store model must be either settled per docs/30 direction or presented as OPEN with options and a clearly-labeled recommendation - a disguised decision is a required finding. (C) Section-B evidence discipline: every exchange-behavior statement must trace to a claim id the P7 record marks VERIFIED (respecting its [V]/[E] evidence levels); any statement relying on an UNKNOWN or ACCOUNT-LEVEL-ONLY claim, or on facts absent from the P7 record, is a required finding. Verify specifically: the single-account/virtual-book fallback is stated as the DEFAULT until account eligibility is separately established (volume gate, claim a + s); same-symbol netting stance stays unfrozen (claim h UNKNOWN); the 1200 weight/min IP budget and 10-connection WebSocket cap are treated as VPS-shared resources (claims n, o). (D) Freeze discipline: every Section-B decision must be explicitly unfrozen with its blocking item named; any frozen exchange-dependent decision is a required finding. (E) Authorization creep: any sentence granting implementation authority is a required finding. Report format: SPEC-COMPLIANCE TABLE, SECTION-A FINDINGS, SECTION-B EVIDENCE-TRACE FINDINGS, REQUIRED FINDINGS (numbered, or 'none'), NITS, FINAL LINE exactly 'VERDICT: ACCEPT' or 'VERDICT: REQUEST_CHANGES'.

### assistant tool_call run_python
{"code": "import os\nfor root, dirs, files in os.walk('C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs'):\n    for f in files:\n        print(os.path.join(root, f))\n"}

### assistant tool_call run_python
{"code": "import os\nprint(os.listdir('C:/LAB/Tradingview_LAB_CLEAN'))\n"}

### tool
returncode=0
stdout=C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\GATE1_PACKAGE1_V2_ARCHITECTURE_CONTRACT_2026-08-17.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\GATE1_PACKAGE2_MTC_INTEGRATION_CONTRACT_2026-08-17.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\GATE1_PACKAGE7_EXCHANGE_REVERIFICATION_2026-08-17.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\p1_spec.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\P1_V2_ARCHITECTURE_CONTRACT_PACK.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\P2_MTC_INTEGRATION_CONTRACT_PACK.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\p2_spec.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\P7_EXCHANGE_REVERIFICATION_RECORD.md
C:/LAB/Tradingview_LAB_CLEAN/_night_review_inputs\p7_official_quotes_dump.md

stderr=

### tool
returncode=0
stdout=['%SystemDrive%', '.agents', '.chatgpt-instructions.md', '.claude', '.codex', '.codex_worktrees', '.cursorrules', '.git', '.gitattributes', '.gitignore', '.impeccable', '.pytest_cache', '.ruff_cache', 'AGENTS.md', 'apply_migration.py', 'AUDIT_REPORT_CODEX.md', 'CHATGPT_MEMORY_PROMPT.md', 'CLAUDE.md', 'docs', 'GEMINI.md', 'graphify-out', 'IBKR_PAPER_BRIDGE', 'MCC_COMMAND_CENTER', 'mtc_cli', 'MTC_COMMAND_CENTER', 'README.md', 'Temp', 'tmprepo_map_inventory.md', 'verify_migration.ps1', '_deepseek_driver', '_night_review_inputs']

stderr=

### assistant tool_call read_file
{"path": "_night_review_inputs/P1_V2_ARCHITECTURE_CONTRACT_PACK.md"}

### assistant tool_call read_file
{"path": "_night_review_inputs/p1_spec.md"}

### assistant tool_call read_file
{"path": "_night_review_inputs/GATE1_PACKAGE1_V2_ARCHITECTURE_CONTRACT_2026-08-17.md"}

### assistant tool_call read_file
{"path": "_night_review_inputs/P7_EXCHANGE_REVERIFICATION_RECORD.md"}

### tool
# Package 1 — V2 Architecture Contract Pack (T2, documentation only)

**Date:** 2026-08-17 (night) · **Implementer:** GLM-5.3 (sub-delegated)
**Artifact:** Package 1 architecture contract pack — **T2, documentation only.** It governs
FUTURE, separately-gated T0 implementation. **Nothing in this pack activates, deploys, wires,
or authorizes any code, host, credential, account, TESTNET/MAINNET, ARM, order, or economic
action.** Where evidence is missing, UNKNOWN is preserved, never smoothed over.

**Gate-1 scope:** `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE1_V2_ARCHITECTURE_CONTRACT_2026-08-17.md`
(owner-authorized start 2026-08-17 night, Decision 5 in
`OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`).
**Accepted demand:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 1, §5 item 2; §3 rows
"Multi-strategy workers", "Subaccounts and same-symbol isolation", "Portfolio Guardian",
"Worker identity and storage separation".
**Section-B authority:** `C:\tmp\night\P7_EXCHANGE_REVERIFICATION_RECORD.md` (claim ids a–s).
Section B relies ONLY on facts that record marks VERIFIED; where it says UNKNOWN or
ACCOUNT-LEVEL-ONLY, the corresponding decision stays explicitly UNFROZEN with the blocking item
named.
**T2 review slot (per Gate-1):** one reviewer, one round, medium effort — DeepSeek
(`deepseek-v4-pro`).

## Citation conventions and provenance

- **Worktree HEAD (cited tree for every repo citation below):**
  `b08aab35f7625e481c4a06f47ceffd1fd0740216` (read-only `git rev-parse HEAD` in `C:\V2PACKS`,
  a clean worktree of merged master).
- `docs/30:<lines>` = `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`
  at that HEAD. Verified: `git diff 033546fb HEAD -- <docs/30>` is empty, so every docs/30 line
  number below is valid under BOTH the accepted backlog's HEAD convention (backlog §1,
  `033546fb08baad2aa606bf6cb96e08ca64a04a5d`) and this worktree's HEAD.
- Pointer-drift note: backlog §3 cites `docs/01_ARCHITECTURE.md:761` for the
  Postgres/Redis/Docker deferral; at this HEAD that fact sits at `docs/01_ARCHITECTURE.md:795`
  (line drift only; the deferral fact itself is unchanged).
- P7 claim ids (a–s) refer to the P7 record's claim table; evidence levels `[V]` (dump-marked
  verbatim official sentence) and `[E]` (dump page-extraction) are the P7 record's own tags
  (P7 §0). No exchange fact in this pack comes from anywhere except the P7 record.
- Current runtime truth cited at the same HEAD: `bridge/app.py`, `requirements.in`.

## Inputs used

1. Gate-1 scope record (above).
2. Accepted backlog `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` (§3 evidence rows, §4 Package 1,
   §5 fastest-safe-order item 2).
3. P7 verification record `C:\tmp\night\P7_EXCHANGE_REVERIFICATION_RECORD.md` (Section-B
   authority).
4. `docs/30` ranges 131-164 (A2 workers), 166-201 (A3 subaccounts), 203-254 (A4 same-symbol),
   256-291 (A5 Guardian), 293-326 (A6 identity/state), 892-905 (A12 open questions); plus 50-59
   (V1 scope), 84-86 (architecture diagram), 628-632 / 732 / 840-841 (veto-not-mutate).
5. `docs/23_ORDER_IDENTITY_CONTRACT.md` (dual identity model, schema v3, reservation protocol);
   `docs/21_WINDOW_STATE_CONTRACT.md` (evidence-derived state); `docs/22_ORDER_STATE_CONTRACT.md`
   (order-state machine, status PROPOSED); `docs/26_FULL_RECONCILIATION_CONTRACT.md:2-4`
   (reconciliation opt-in, inert on default v4).
6. `bridge/app.py:98-110` (loopback app, default store init), `:134-155` (single RiskConfig incl.
   exposure thresholds `:149-154`), `:158-174` (one `BridgeEngine`, fixed `KeltnerTrailEma8`,
   one `RiskEngine`), `:191-208` (Mock CSV broker or Hyperliquid testnet, fixed BTC, leverage 1);
   `requirements.in:26-35` (direct deps: no Postgres/Redis/Docker driver).

Current runtime truth this pack builds from, per the accepted backlog §3: the runtime constructs
exactly one engine, one strategy, one risk engine (`bridge/app.py:158-174`); V1 is one strategy,
one symbol, one timeframe (`docs/30:50-59`); Postgres/Redis/Docker are deferred to v2
(`docs/01_ARCHITECTURE.md:795`; `requirements.in:26-35` has no such dependency today).

---

# Section A — Settled locally (contract text, citations, no exchange dependency)

These decisions are settled **locally** per the accepted backlog §4 Package 1 ("Settle worker
identity, store model and Portfolio Guardian veto semantics locally"). They are contract text
for future T0 implementers, not implementation, and not activation.

## A.1 Worker identity contract — SETTLED

**Decision.** Every V2 worker carries exactly this identity tuple:

```
(worker_id, strategy_id, symbol, timeframe, strategy_version, config_hash, account_label)
```

1. **`worker_id`** — the surrogate identifier. Unique within a deployment for all time,
   including retired workers; **never reused**. Assigned at worker creation; the only field
   ever displayed or logged as "the" worker name by default.
2. **`strategy_id`** — identifies the frozen, approved strategy package the worker executes.
   The Bridge consumes approved packages; it does not develop strategies (`docs/30:52-54`).
3. **`symbol`** — normalized uppercase, matching the canonical-encoding convention of
   `docs/23:18-19` ("normalized uppercase symbol").
4. **`timeframe`** — the worker's bar timeframe. Its presence in the tuple settles the A6/A12
   granularity question (see "Resolutions flagged" below): a worker is one
   strategy+symbol+timeframe(+config+partition) instance — the finest grain A6 floats — because
   A6 requires separate books per strategy, symbol, AND timeframe (`docs/30:310-311`).
5. **`strategy_version`** — version of the frozen strategy package the worker runs.
6. **`config_hash`** — deterministic content hash over the worker's frozen configuration
   preimage (strategy parameters + the worker's risk profile). The preimage is encoded per the
   `docs/23:42-47` canonical rules (deterministic JSON, sorted keys, compact separators, UTF-8,
   `ensure_ascii=False`, `allow_nan=False`, `float.hex()` floats, negative-zero normalized,
   NaN/Infinity rejected), and digests are never trusted alone — equality checks compare exact
   preimages and digest/preimage mismatch fails closed (`docs/23:49-53`).
7. **`account_label`** — a **logical** label for the execution partition the worker trades
   through (a subaccount slot or a virtual-book partition). It is NOT a credential, NOT an
   address, NOT a key; secrets never enter identity. Its resolution to real exchange resources
   is exchange-dependent and therefore Section B territory (B.3-B.5), conditioned on P7.

**Uniqueness rules.**

- `worker_id` is unique forever (active + retired); retirement never frees an id.
- Among **active** workers, the full tuple
  `(strategy_id, symbol, timeframe, strategy_version, config_hash, account_label)` is unique —
  no two active workers share a complete natural key. Two active workers MAY share
  strategy+symbol+timeframe under **different** `account_label`s: that is precisely A4's
  same-symbol isolation lever (`docs/30:235-238`) — and it is gated CLOSED today by B.6.
- `(strategy_id, symbol, account_label)` with differing `timeframe` = two distinct workers with
  distinct books; whether they may run concurrently in one partition is still governed by the
  same-symbol closure (B.6).

**Immutability rules.**

- All seven fields are immutable for the worker's lifetime. Any change — new strategy version,
  edited config (new `config_hash`), symbol or timeframe change, account relabel — means
  **retire the worker and create a successor** with a NEW `worker_id`. A successor may record a
  lineage link to its predecessor for reporting only; it never inherits the predecessor's
  identity, open reservations, or ledger continuity.
- Rationale: A6's restart question ("which orders, which P&L, and which state belong to which
  strategy — particularly after a restart?", `docs/30:298-300`) is only answerable if a
  worker's books describe one unchanging configuration story; mid-flight mutation would also
  break docs/23's premise that the same canonical intent receives the same durable identity
  across restart and run-id changes (`docs/23:5-8`).

**Separation of per-worker P&L, state, and order identity.**

- **P&L:** each worker owns a P&L ledger keyed by `worker_id`. Realized and unrealized
  attribution never crosses workers. Portfolio P&L is computed by summation ABOVE the workers
  (Guardian / dashboard), never by sharing one ledger — the shared-ledger failure mode is A6's
  "one strategy's loss counted against another's limits" (`docs/30:302-304`).
- **State:** each worker has its own state namespace (position state, cooldowns, protective
  state, window/liveness state). Per-worker window state stays **evidence-derived** on the
  `docs/21:16-18` model — derived from that worker's persisted evidence with a staleness rule,
  never an in-memory claim; unreadable evidence reports DOWN, never a fabricated active state
  (`docs/21:37-42`).
- **Order identity:** docs/23's dual-identity model **extends, it is not replaced**:
  - The canonical intent preimage must include the worker's identity fields (at minimum
    `worker_id`; equivalently the natural-key fields plus `account_label`) under a **new
    domain version** (an `intent-v2`-style domain string). This guarantees two workers can
    never alias to one `intent_id`, and one worker's replay cannot reserve another worker's
    order. Uniqueness/immutability semantics carry over unchanged: same canonical intent →
    same durable identity across restarts and run-id changes; same intent with a different
    request → `IdentityCollisionError`; reservation committed before any broker I/O
    (`docs/23:127-137`).
  - `request_id` remains the broker cloid seed (`docs/23:162-167`); because it derives from the
    intent, worker identity entering the intent preimage also keeps two workers from minting
    colliding exchange cloids.
  - **Tension flagged (not changed):** schema v3 pins `intent_version` to
    `'ts-p1-002-intent-v1'` (`docs/23:63`) and its canonical intent embeds a single stable
    strategy id, `keltner_trail_ema8` (`docs/23:18`) — a deliberate single-strategy assumption.
    Multi-worker identity requires a new domain version plus migration: protected future T0
    work under its own contract. This pack modifies nothing.
  - Per-worker separation is enforced **by identity content** (the tuple inside the preimage),
    not by a tag column alone — A6's warning is that shared state with a strategy tag is "one
    missing filter" away from silently mixing strategies (`docs/30:316-317`).

## A.2 Store model — OPEN (options, consequences, labeled recommendation)

**Why OPEN:** docs/30 settles the *separation requirement* but deliberately leaves the store
question open: "The store question itself (per-worker SQLite vs. central Postgres) is
deliberately left open in A12; the *separation requirement* is decided regardless of which
store wins" (`docs/30:320-322`; A12 lists it at `docs/30:899`). The separation requirement of
A.1 is therefore binding whichever option is later chosen; the store itself is NOT decided
here.

**Options and consequences.**

1. **Per-worker SQLite (one store per worker).**
   - Strongest storage-level isolation: one worker's corruption or bug is confined to its own
     file — A6's "fully separate stores per worker — strongest isolation, harder aggregate
     reporting and more moving parts to back up and reconcile" (`docs/30:318-319`).
   - Aggregate portfolio reads (Guardian, dashboard) must fan out over N stores or go through
     an aggregation layer; backups and schema migrations run N times, with version-skew risk
     between workers.
   - Keeps today's dependency footprint (SQLite is stdlib; `requirements.in:26-35` contains no
     external database driver; `docs/01_ARCHITECTURE.md:795` defers Postgres/Redis/Docker to
     v2).
2. **Central store (single Postgres; per-worker schemas or enforced tenancy).**
   - One aggregate query surface — easiest for the Guardian and the V2 dashboard; single
     migration point; one backup.
   - Shared failure domain: one corrupt or mis-migrated store puts every worker's evidence at
     risk; tenancy must be structural (separate schemas / row-level separation), because the
     tag-column alternative is exactly A6's "one missing filter silently mixes strategies"
     (`docs/30:316-317`).
   - New infrastructure and ops surface (service, backups, credentials); today explicitly
     deferred (`docs/01_ARCHITECTURE.md:795`) and absent from `requirements.in:26-35`.
3. **Hybrid: per-worker SQLite as worker-local source of truth + a small supervisor-owned
   central store holding only (a) the worker registry / identity tuples and (b) the aggregate
   portfolio snapshot the Guardian reads.**
   - Keeps the correctness-critical ledgers (P&L, state, order identity) in per-worker
     isolation while giving the Guardian and dashboard a single read surface.
   - The central snapshot must be DERIVED from worker evidence (never an independent truth that
     can drift), on the same evidence-derived-not-claimed principle as `docs/21:16-18`, with an
     explicit freshness/reconciliation policy; and it adds one more component to define.

**RECOMMENDATION (clearly labeled: a recommendation, NOT a decision).** Option 3 — hybrid,
per-worker SQLite source-of-truth stores plus a supervisor-owned registry/aggregate store —
because it satisfies A6's separation requirement regardless of which long-term store wins,
preserves the current dependency footprint (no new external service on the V2 critical path),
and still gives the Guardian one read surface without placing all workers in a single failure
domain. Escalation to a central Postgres remains open as a later, separately gated decision if
aggregate load or operations demand it. The decision itself stays OPEN per `docs/30:899` and is
NOT frozen by this pack.

## A.3 Portfolio Guardian veto semantics — SETTLED (semantics only; no thresholds)

**Decision (contract text).** A Portfolio Guardian sits ABOVE the workers
(`docs/30:273-277`; architecture diagram `docs/30:84-86`). Workers manage their own strategy;
the Guardian manages the portfolio (`docs/30:276-277`).

**Inputs it reads (read-only; the Guardian mutates nothing):**

- Per-worker derived exposure (gross/net by symbol and direction), per-worker realized and
  unrealized P&L, and per-worker leverage/margin utilization — from each worker's own books
  (A.1/A.2), as derived snapshots, never worker self-claims as sole truth (evidence-derived
  principle, `docs/21:16-18`).
- Aggregate portfolio exposure, loss, concentration, and correlation inputs — the sums the
  Guardian exists to bound ("five workers each risking a 'small' amount, all long, all
  correlated, is one large undiversified bet that no single worker can see",
  `docs/30:261-269`).
- Worker liveness/window state per worker (`docs/21:16-34`).
- Account-level truth from reconciliation, when and only when that opt-in capability is
  activated under its own future gate — full reconciliation is implemented but opt-in and
  inert on the default v4 schema (`docs/26:2-4`; backlog §3 row "Full reconciliation and
  authoritative risk": activation/migration is T0 behind a T2 activation contract first).
  **Dependency flagged:** until that activation, the Guardian's account-truth input is
  unavailable and the Guardian may run only on worker-derived snapshots, fail-closed (below).

**Veto scope — three tiers:**

1. **Per-order veto:** refuse an individual worker's order intent before submission.
2. **Per-worker pause:** stop ONE worker from initiating new entries; that worker keeps
   managing and protecting existing positions (exits continue; books stay current).
3. **Global halt:** stop new entries across ALL workers (portfolio circuit breaker).

Veto domain = **risk-increasing actions** (new entries, adds, risk-increasing order changes).
**Risk-reducing exits (stop-loss, take-profit, close) are outside veto scope:** the Guardian's
mandate is to bound "total exposure, loss, leverage, concentration, and correlation"
(`docs/30:274-275`); a veto against an exit would increase the very quantities it exists to
bound. Lifting a pause/halt is an operator action, outside this pack.

**Vetoes, never mutations.** At every tier the Guardian "vetoes but does not mutate"
(`docs/30:284-285`): it never resizes an order, never rewrites a stop or quantity, never edits
economic intent (`docs/30:628-632`, `:840-841`). Whether a veto may ever become a resize is
answered "not without an explicit parity contract" (`docs/30:289-291`, `:732`) — out of scope
here and NOT opened.

**Precedence vs worker-local risk — AND-gate, Guardian outranks:**

- An order proceeds only if BOTH accept: worker-local risk first (the per-worker continuation
  of today's single-runtime RiskEngine checks, `bridge/app.py:134-155`, exposure thresholds at
  `:149-154`), Guardian second, synchronously in the order path — an order is not submitted
  until the Guardian accepts, because a post-hoc check would permit the exposure the Guardian
  exists to bound.
- Guardian veto always outranks worker acceptance; Guardian acceptance NEVER substitutes for
  worker-local rejection (the Guardian is not a rubber stamp over a worker whose own risk
  said no).

**Fail-closed defaults:**

- If the Guardian cannot evaluate — unreachable, missing or stale aggregate snapshot, broken
  worker→Guardian channel — the default is **no new entries**. There is no silent
  Guardian-bypass mode.
- Guardian unavailability never blocks protective exits (blocking them would increase risk).
- Every veto, at every tier, produces a logged, operator-visible reason ("veto reasons must be
  logged and visible", `docs/30:286`).

**Thresholds arrive later.** All numeric thresholds, their calibration, and residual
interaction details are unresolved and belong to a later owner-gated package
(`docs/30:288-289`, A12 `docs/30:902`). This pack fixes no numbers.

---

# Section B — CONDITIONED ON Package 7 (nothing here is frozen beyond P7 evidence)

Eight decisions, one subsection each. Each states (i) what P7-VERIFIED facts let us say NOW,
with the claim id, and (ii) what stays UNFROZEN with the exact blocking UNKNOWN /
ACCOUNT-LEVEL-ONLY item. Per Gate-1: **the fallback (virtual books / single-account
partitioning) is the DEFAULT design branch until account eligibility is separately
established** — stated explicitly in B.3 and assumed by B.4-B.8.

## B.1 Worker boundary — UNFROZEN

**Stateable now (P7):**

- Whatever the boundary, one VPS shares the IP-based REST budget — "aggregated weight limit of
  1200 per minute" (claim **n** [V]) — and the WebSocket caps — max 10 connections, 1000
  subscriptions (claim **o** [E]) — across ALL workers. The boundary choice buys **no**
  IP-level API capacity; a central capacity allocation is required regardless of boundary
  (mandated framing; see B.8).
- Address-based budgets "sub-accounts treated as separate users" (claim **p** [V]): IF the
  boundary is eventually coupled to per-worker subaccounts, address-level budget separation
  follows — but this account's subaccount availability is ACCOUNT-LEVEL-ONLY (claim **s**).
- Non-exchange design direction already fixed independently of P7: preferred deployment is one
  VPS / one shared release with isolated workers, NOT one host per strategy
  (`docs/30:150-152`); one process with shared in-process state is rejected (`docs/30:158-159`).

**Unfrozen — blocking items:**

- The boundary itself (separate OS process / separate container / in-process task with
  enforced state separation, and what each guarantees when one worker fails) is a docs/30 A12
  open point (`docs/30:895-898`). No P7 row answers it — P7 verifies exchange documentation,
  not OS isolation semantics; this is a design-side open point, not an exchange UNKNOWN.
- Boundary sizing calibrated on testnet measurements — blocked by **r** (UNKNOWN: whether
  rate limits differ on testnet).
- A subaccount-per-worker boundary — blocked by **s** (ACCOUNT-LEVEL-ONLY) and the volume gate
  (claim **a**) not yet established for this account.

## B.2 Feed topology — UNFROZEN

**Stateable now (P7):**

- WebSocket limits are IP-shared: max 10 connections; 30 new connections/min; 1000
  subscriptions; 10 unique users across user-specific subscriptions; 2000 messages/min sent;
  100 inflight posts (claim **o**, evidence level [E] only — P7 §0). Consequence statable now:
  an unbounded per-worker-feed topology (each worker holding its own connections and
  subscriptions) consumes the shared caps linearly with worker count and cannot be the
  default; a shared feed / fan-out layer (few connections, internal distribution to workers)
  is the only topology consistent with the verified caps without a per-worker connection
  budget engineered to fit inside 10 total.
- REST-polling feeds draw from the same shared 1200 weight/min IP budget (claim **n** [V]).
- The "10 unique users" user-specific-subscription cap interacts with how many distinct
  account streams (master + subaccounts) exist — which depends on subaccount availability
  (claim **s**).

**Unfrozen — blocking items:**

- The shared-vs-per-worker choice is A12's first open question (`docs/30:894`) — design-side,
  not answerable by P7.
- Any freeze leaning on the exact WS numbers — claim **o** rests on [E] extraction text only;
  P7 §0 recommends a verbatim-sentence confirmation pass (still T2, docs-only) before
  freezing figures that depend on them.
- Calibration from testnet — blocked by **r** (UNKNOWN: testnet parity of limits).
- User-stream count design — blocked by **s** (ACCOUNT-LEVEL-ONLY).

## B.3 Subaccount fallback — UNFROZEN mechanics; the fallback is the DEFAULT branch (stated now, per Gate-1)

**Stateable now (P7):**

- Subaccounts are conditional by design, volume-gated: "Up to 10 sub-accounts can be created
  after reaching $100,000 in volume"; "Every additional $100M in volume enables the ability to
  create 1 additional sub-account, up to a maximum of 50 sub-accounts" (claim **a** [V]).
  Therefore the one-independent-risk-bucket-per-subaccount model of docs/30 A3
  (`docs/30:182-184`) cannot be assumed available (P7 §2, first bullet).
- **EXPLICIT DEFAULT (per Gate-1):** because the volume gate makes subaccount availability
  conditional and this account's gate status is not established (claim **s**), the DEFAULT V2
  design branch is the **fallback: a single account with internal partitioning — virtual
  books** — which is A3's documented alternative ("Single account + internal virtual books —
  no exchange-side eligibility question, but every ownership guarantee then rests on our own
  code", `docs/30:190-192`). The subaccount topology is the UPGRADE branch, not the default.
  All Section-B design work (B.4-B.8) assumes the single-account default until eligibility is
  established under a future owner gate.

**Unfrozen — blocking items:**

- The fallback's internal mechanics: a virtual-book model "must prove ownership through
  partial fills, liquidations, funding, and restarts before it can be trusted. That proof is
  the whole cost." (`docs/30:244-246`); A12 keeps the fallback open (`docs/30:901`). Needs its
  own design+validation package (T2 contract first, then T0 implementation).
- Any migration to the subaccount branch — blocked by **s** (ACCOUNT-LEVEL-ONLY: the actual
  account's cumulative volume / current eligibility) and **r** (UNKNOWN: whether the gate
  itself differs on testnet).
- Under the default fallback, same-symbol concurrency stays closed (B.6).

## B.4 Subaccount eligibility — UNFROZEN for this account

**Stateable now (P7):**

- Gate mechanics (claim **a** [V]): $100,000 volume → up to 10 sub-accounts; +1 per additional
  $100M; hard maximum 50.
- Fee treatment (claim **b** [V]): "Sub-accounts share the same fee tiers as the master
  account, but referral discounts do not apply to sub-accounts."
- Under portfolio margin: "Sub-accounts are still treated separately under portfolio margin."
  (claims **c**/**l** [V]).
- API-wallet quota grows with subaccounts: "The number of API wallets available starts at 3
  for all master accounts and increases by 2 per sub-account" (claim **d** [V]) — relevant to
  B.5.

**Unfrozen — blocking items:**

- THIS account's current eligibility and wallet count — **s** (ACCOUNT-LEVEL-ONLY; answerable
  only by an account-level check under its own future owner gate, T0).
- General sub-account margin/clearinghouse treatment outside portfolio margin — **c**
  sub-scope UNKNOWN (the sub-accounts page does not address it; P7 row c negative evidence).
- Whether the gate/counts differ on testnet — **r** UNKNOWN.

## B.5 Agent-wallet assignment — model stateable; actions and counts UNFROZEN

**Stateable now (P7):**

- "A master account can approve API wallets to sign on behalf of the master account or any of
  the sub-accounts" and "It's recommended to use separate API wallets for different
  subaccounts" (claim **e** [V]); sub-accounts have no private keys and actions are signed by
  the master (or approved API wallet) with `vaultAddress` set to the sub-account address
  (claim **e**, that sentence at [E] level).
- Wallet count baseline 3, +2 per sub-account (claim **d** [V]) — wallet-per-worker feasibility
  scales with subaccount count, hence with claim **a** and **s**.
- "Nonces are tracked per signer" and "The 100 highest nonces are stored per address" (claim
  **f** [V]); validity band (T − 2 days, T + 1 day) at [E] level.
- Lifecycle: "Generate a new agent wallet on future use to avoid unexpected behavior" (claim
  **g** [V]); wallets can expire, be pruned, or be deregistered (claim **g** [E]).

Contract-model statements these facts support now (documentation only):

1. Wherever subaccount partitions exist, the assignment model is **one dedicated API wallet per
   worker/partition** — docs/30 A3's "separate API / agent wallet" (`docs/30:183-184`) aligned
   with claim e's official recommendation.
2. The wallet↔partition binding is recorded through the worker identity's `account_label`
   (A.1); keys and secrets never enter identity.
3. Signer wallets must NOT be shared across workers without an explicit nonce coordinator:
   claim f makes the 100-nonce window per signer, so two workers driving one signer contend on
   one window.
4. Claim g's lifecycle rules make wallet health (registered / not expired / not pruned) a
   worker-health input, and regenerate-on-reuse is mandatory policy, not preference.

**Unfrozen — blocking items:**

- Any actual wallet creation, approval, or registration — an account action: prohibited here;
  future T0 owner gate.
- This account's current wallet count — depends on **s** (ACCOUNT-LEVEL-ONLY).
- The exact `vaultAddress` field behavior — [E]-level evidence only (claim e); verbatim
  confirmation pass (P7 §0) before any code leans on it.
- Whether wallet rules differ on testnet — **r** UNKNOWN.

## B.6 Same-symbol netting stance — REMAINS CLOSED (conservative stance preserved)

**Stateable now (P7):**

- The stance itself: **same-symbol concurrency within one account partition remains CLOSED.**
  This preserves docs/30 A4's status ("Same-symbol concurrency stays closed until either
  separate subaccounts are confirmed available or a virtual-book model is designed *and
  validated*, **and** until the netting mechanics above are reverified", `docs/30:250-254`)
  against the P7 outcome: P7 performed the re-verification A4 demanded (`docs/30:220-227`) and
  the official pages fetched do NOT establish netting/hedge mode — claim **h** UNKNOWN; the
  third-party one-way-netting consensus is explicitly NOT evidence and is not cited as such
  (P7 rows h, §4).
- Note: the closure is conservative and does NOT depend on A4's netting description being
  verified. Under h UNKNOWN, either netting or one-position-per-asset could be true; both are
  unsafe for two strategies sharing one partition without proven ownership separation. Only
  REOPENING concurrency would require verified mechanics.

**Unfrozen — blocking items:**

- **h** UNKNOWN (same-symbol netting / hedge mode) — primary blocker.
- **j** UNKNOWN (cross+isolated coexistence on one asset) — same per-asset account-mechanics
  family.
- The "separate subaccounts confirmed available" precondition — **s** (ACCOUNT-LEVEL-ONLY).
- A validated virtual-book model — does not exist yet (`docs/30:244-246`; B.3).
- Any supervised account-level check of same-symbol behavior — ACCOUNT-LEVEL-ONLY under its
  own future owner gate (P7 §2, last bullet).

## B.7 Margin-mode stance — facts inventoried; per-worker assignment UNFROZEN

**Stateable now (P7):**

- "Cross margin is the default, which allows for maximal capital efficiency by sharing
  collateral between all other cross margin positions."; isolated margin is supported;
  "Some assets are strict isolated" with margin non-removable (claim **i** [V]).
- "Max leverage varies by asset, ranging from 3x to 40x. Maintenance margin is half of the
  initial margin at max leverage."; user-settable leverage is any integer 1..max (claim **m**
  [V]).
- Mode ceilings (claim **k** [V]): "Portfolio margin and unified account are limited to 50k
  user actions per day. Standard mode has no such restrictions."; portfolio margin unifies
  spot and perps and is "a generalization of cross margin" with access fragments ">$5M in
  weighted volume or account value >$10k" and "<$25M" plus supply/borrow caps at [E] level
  (claim **l** [V]/[E]; residual UNKNOWN: no explicit alpha/live designation on the page).
- Design consequence statable NOW: the exchange default (cross, shared collateral) pulls
  AGAINST per-worker risk-bucket isolation. In the DEFAULT single-account fallback (B.3),
  cross margin shares collateral across all workers' positions in the account, so per-worker
  risk boundaries inside one account cannot rely on exchange-side margin separation. A V2
  worker margin-mode assignment must therefore be an explicit decision in a later package —
  never an inherited exchange default. (V1 runtime context: today's runtime is fixed at
  leverage 1, `bridge/app.py:207`, with `max_leverage` default 1 in risk config,
  `bridge/app.py:147`.)

**Unfrozen — blocking items:**

- The per-worker margin-mode assignment — blocked by **j** UNKNOWN (cross+isolated
  coexistence on one asset), the h-family per-asset mechanics, and the account-mode question:
  which abstraction mode the actual account is in is NOT established by the P7 record (no row
  covers it; an account-level fact in the same family as **s**).
- Whether portfolio-margin/unified's 50k-actions/day ceiling (claim **k**) would bind a
  multi-worker action volume — computable only after worker count and action rates are known
  (later package); PM eligibility for THIS account is an account fact (thresholds verified in
  claim **l**, account status not).
- **l** residual UNKNOWN (alpha/live designation) — relevant if PM were ever considered.

## B.8 API-limit budget model — shared-resource framing stateable; numbers UNFROZEN

**Stateable now (P7), and mandated by Gate-1:**

- The IP-based "aggregated weight limit of 1200 per minute" (claim **n** [V]) and the
  WebSocket caps — max 10 connections, 1000 subscriptions, 30 new connections/min, 2000
  messages/min, 100 inflight posts (claim **o** [E]) — are **shared VPS-wide resources across
  ALL workers, whatever the worker-process boundary ends up being** (Gate-1 shared-infrastructure
  framing; P7 §2 last bullet). Therefore the budget model MUST be a **central allocator**: one
  shared admission/token-bucket layer for REST weight and one connection/subscription registry
  for WebSocket, granting explicit **per-worker budgets** with a headroom policy and a defined
  overload behavior (defer or reject — never silently exceed). No worker may hold its own
  independent connection-to-the-exchange budget.
- REST weight mechanics (claim **n**): exchange request weight `1 + floor(batch_length / 40)`;
  info weights 2 / 20 / 60 by type; per-item surcharges — "additional rate limit weight per 20
  items returned" ([V] fragment) — candleSnapshot per 60 items; explorer weight 40 (these
  fragments [E] except the quoted one).
- Address-based budgets separate per address: "sub-accounts treated as separate users";
  "1 request per 1 USDC traded cumulatively"; "initial buffer of 10000 requests"; throttled to
  one request per 10 seconds when limited (claim **p** [V] for the first three, throttle [E]).
  So address-level capacity accrues per partition (subaccount separation gains budgets), while
  the IP-level budget and WS caps never do (P7 §2).
- Order allowances (claim **q**, [E] only): open orders 1000 + 1 per 5M USDC volume, cap 5000;
  cancels `min(limit + 100000, limit * 2)` — quantities to be tracked per account partition in
  the budget model.

**Unfrozen — blocking items:**

- Exact per-worker budget numbers and overload thresholds — claims **o** and **q** rest on [E]
  extraction text only; P7 §0 recommends a verbatim-sentence confirmation pass (T2, docs-only)
  before any freeze that leans on those exact figures.
- Calibration from testnet measurements — **r** UNKNOWN (testnet parity of limits).
- Per-address budget reality for THIS account — **s** (how many sub-accounts/addresses exist is
  account-level only).

---

# Explicit non-authorization

- This pack is **documentation only** (T2). It governs FUTURE, separately-gated T0
  implementation packages; **nothing activates, nothing is wired, no code is written or
  changed**, and no part of this pack may be read as permission to implement.
- Standing prohibitions unchanged and in force for anything following from this pack: no
  VPS/host actions, no credentials, no exchange account actions (including wallet or
  subaccount creation), no TESTNET or MAINNET activity, no ARM and no orders, no
  Pine/parity/MTC changes, no mutation of the frozen V1 candidate (Gate-1 "Out of scope /
  prohibited"; backlog §1: V1 stays untouched and isolated).
- **Nothing is frozen beyond evidence.** Section A settles contract semantics only, with
  numeric thresholds and all implementation explicitly deferred; Section B freezes nothing —
  each of its eight decisions remains UNFROZEN, with the blocking UNKNOWN or
  ACCOUNT-LEVEL-ONLY item named inline. UNKNOWN stays UNKNOWN; no third-party material was
  used to upgrade any claim (the one-way-netting consensus appears only as a named non-source).
- No exchange fact in this pack originates from model memory; every exchange-dependent
  statement cites the P7 record's claim table. Where the P7 record's evidence is [E]-level
  (rows o, q, and named [E] fragments in e, f, g, l, n, p, r), that level is stated inline and
  the freeze stays open pending the verbatim-confirmation pass P7 §0 recommends.

# Self-verification

- **Section-B provenance:** every exchange-dependent statement above carries a P7 claim id;
  statuses used are exactly the P7 record's (VERIFIED / UNKNOWN / ACCOUNT-LEVEL-ONLY). Where P7
  says UNKNOWN (h, j; sub-scopes of c and r; the residual note in l) or ACCOUNT-LEVEL-ONLY (s),
  the corresponding decision is stated UNFROZEN with the blocker named — none is frozen.
- **Repo provenance:** all repo citations were read at worktree HEAD
  `b08aab35f7625e481c4a06f47ceffd1fd0740216`. docs/30 was verified byte-identical to the
  backlog's citation HEAD `033546fb...` (empty `git diff`), so docs/30 line references are valid
  under both conventions. The one pointer drift found (backlog's `docs/01:761` → `:795` at this
  HEAD, same fact) is disclosed in the header, not silently re-cited.
- **No contradictions with the accepted backlog or docs/21/22/23; deliberate resolutions
  flagged, not smuggled:**
  1. docs/23 schema v3 pins a single-strategy identity domain (`docs/23:18`, `:63`); A.1
     extends identity to the worker tuple via a NEW domain version and flags the required
     migration as protected future T0 — docs/23 is not contradicted or modified.
  2. docs/30 A12 lists worker-identity granularity (`docs/30:900`) and Guardian/worker-risk
     interaction (`docs/30:288-289`) as open; A.1 and A.3 resolve their SEMANTICS under the
     accepted backlog's explicit authorization to settle them locally (backlog §4 Package 1),
     while store model (`docs/30:899`), worker boundary (`:895-898`), feed topology (`:894`),
     and subaccount fallback (`:901`) remain open/conditioned exactly as docs/30 and the
     backlog require.
  3. A.4's netting description itself carries docs/30's own re-verification caveat
     (`docs/30:220-227`); B.6 relies on the FAILED verification (h UNKNOWN) to preserve closure,
     not on the unverified description.
- **Read-only discipline:** repositories were treated as read-only; the only git command run
  was read-only `git rev-parse` / `git diff`; no handoff, config, or repo file was modified. The
  only file written by this task is this pack: `C:\tmp\night\P1_V2_ARCHITECTURE_CONTRACT_PACK.md`.
- **Counts:** Section A — 3 decision areas: 2 settled (A.1 worker identity, A.3 Guardian veto
  semantics), 1 deliberately OPEN with a labeled recommendation (A.2 store model). Section B —
  8 decision areas, all conditioned on P7 and unfrozen (worker boundary, feed topology,
  subaccount fallback, subaccount eligibility, agent-wallet assignment, same-symbol netting,
  margin mode, API-limit budget model), with the single-account/virtual-book fallback stated
  as the DEFAULT branch until account eligibility is separately established.


### tool
# TASK: Package 1 — V2 Architecture Contract Pack (T2, documentation only)

You are the implementer for Package 1 under a Claude Lead. Owner-authorized start; Gate-1 scope:
`C:\V2PACKS\MTC_COMMAND_CENTER\11_TRIAGE\GATE1_PACKAGE1_V2_ARCHITECTURE_CONTRACT_2026-08-17.md`
(read it first). Repositories are READ-ONLY for you.

## Inputs (read-only; primary repo view = C:\V2PACKS, a clean worktree of merged master)

1. Accepted backlog: `C:\V2PACKS\MTC_COMMAND_CENTER\11_TRIAGE\BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`
   (§4 Package 1; §3 rows: multi-strategy workers, subaccounts/same-symbol isolation, Portfolio
   Guardian, worker identity and storage separation).
2. **Package 7 verification record (your Section-B authority):**
   `C:\tmp\night\P7_EXCHANGE_REVERIFICATION_RECORD.md` — Section B may rely ONLY on facts this
   record marks VERIFIED; where it says UNKNOWN or ACCOUNT-LEVEL-ONLY, the corresponding
   decision stays explicitly UNFROZEN with the blocking item named.
3. Design source: `C:\V2PACKS\IBKR_PAPER_BRIDGE\docs\30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`
   — at least ranges 131-164 (workers), 166-201 (subaccounts), 203-254 (same-symbol), 256-291
   (Guardian), 293-326 and 892-905 (worker identity/storage). Cite as `docs/30:<lines>` with the
   worktree HEAD noted in your header.
4. Current runtime truth for citations: `C:\V2PACKS\IBKR_PAPER_BRIDGE\bridge\app.py` (single
   engine/strategy/risk construction), `C:\V2PACKS\IBKR_PAPER_BRIDGE\requirements.in`.

## Output (write ONLY this file)

`C:\tmp\night\P1_V2_ARCHITECTURE_CONTRACT_PACK.md`

## Required content

1. **Header:** artifact = Package 1 architecture contract pack, T2 documentation; governs FUTURE
   separately-gated T0 implementation; nothing activates; worktree HEAD hash (read-only
   `git rev-parse HEAD` in C:\V2PACKS permitted).
2. **Section A — settled locally** (decide these; contract text with citations):
   - **Worker identity:** the identity tuple every worker carries (id, strategy, symbol,
     timeframe, version, config hash, account label), uniqueness/immutability rules, and how
     per-worker P&L/state/order identity separate (consistent with docs/23 order identity).
   - **Store model:** per-worker SQLite vs central store — decide per docs/30's cited direction;
     if docs/30 genuinely leaves it open, present the decision as OPEN with options, consequences,
     and a recommendation (clearly labeled recommendation, not decision).
   - **Portfolio Guardian veto semantics:** Guardian-above-workers contract — inputs it reads,
     veto scope (per-order, per-worker pause, global), precedence vs worker-local risk,
     fail-closed default, and that its thresholds arrive in a later owner-gated package.
3. **Section B — CONDITIONED ON Package 7** (one subsection per decision): worker boundary,
   feed topology, subaccount fallback, subaccount eligibility, agent-wallet assignment,
   same-symbol netting stance, margin-mode stance, API-limit budget model. For each: what the
   P7 record VERIFIED lets us state now (with the quote's claim id), what stays UNFROZEN and
   the exact blocking UNKNOWN / ACCOUNT-LEVEL-ONLY item. The volume-gate fact means: design the
   fallback (virtual books / single-account partitioning) as the DEFAULT until account
   eligibility is separately established; state that explicitly.
   Shared-infrastructure facts to incorporate: one VPS shares the IP-based 1200 weight/min REST
   budget and the 10-connection WebSocket cap across all workers (P7 claims n, o) — the API-limit
   budget model must allocate these as shared resources with per-worker budgets, whatever the
   worker-process boundary ends up being.
4. **Explicit non-authorization** and **self-verification** sections as in your Gate-1 record:
   documentation only, nothing frozen beyond evidence, UNKNOWN preserved, citations everywhere.

## Hard constraints

- Write nothing except the single output file. Repos read-only. No exchange facts from memory —
  only the P7 record and cited repo lines. UNKNOWN stays UNKNOWN. English only.
- Do not contradict the accepted backlog or docs/21/22/23 contracts; flag tensions instead.

Final message: short summary + output path + counts (Section A decisions settled, Section B
decisions conditioned/unfrozen).


### tool
# Gate-1 Scope Record — Package 1: V2 Architecture Contract Pack

**Date:** 2026-08-17 night · **Lead:** Claude (Fable) · **Tier: T2, documentation only**
**Owner authorization:** in chat 2026-08-17 night ("start packages 1+2"), recorded as Decision 5
in `OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`.
**Accepted source:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 1, §5 item 2
(accepted per `BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md`).

## Frozen scope

One architecture contract pack split exactly as the accepted backlog requires:

- **Section A — settled locally:** worker identity, store model, Portfolio Guardian veto
  semantics.
- **Section B — CONDITIONED ON Package 7 output:** worker boundary, feed topology, subaccount
  eligibility/fallback, agent-wallet behavior, same-symbol netting, margin mode, API limits.
  Section B decisions cite the Package 7 verification record where it answers them and remain
  explicitly unfrozen wherever Package 7 reports UNKNOWN or ACCOUNT-LEVEL-ONLY.

Documentation only; no code, no runtime wiring, no live exchange assumptions beyond the
Package 7 record. `docs/30` citations follow the accepted (HEAD `033546fb`) convention.

## Sequencing

Authoring starts after the Package 7 verification record exists (same night), so Section B can
consume it. Package 2 runs in parallel and is independent.

## Roles and review

- Implementer: GLM-5.3 (sub-delegation). T2 review: DeepSeek (`deepseek-v4-pro`), one round,
  medium — different provider from the author. Gemini read-only route as supplemental cross-check.

## Out of scope / prohibited

Freezing any Section B decision beyond what Package 7 verified; implementation of any kind; and
the standing prohibition list (VPS/host, credentials, exchange account actions, TESTNET/MAINNET,
ARM/orders, Pine/parity/MTC, frozen-V1 mutation).


### tool
# Package 7 — Official Exchange Reverification Record (T2, read-only)

**Date:** 2026-08-17 (night) · **Implementer:** GLM-5.3 (sub-delegated; per Gate-1 scope record)
**Artifact:** Package 7 verification record — T2, read-only, documentation only.
**Gate-1 scope:** `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE7_EXCHANGE_REVERIFICATION_2026-08-17.md`
(owner-authorized start 2026-08-17 night, Decision 5).
**Accepted demand:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 7, §3 row
"Subaccounts and same-symbol isolation".
**T2 review slot (per Gate-1):** one reviewer, one round, medium effort — DeepSeek (`deepseek-v4-pro`).

**Method:** official Hyperliquid documentation pages, live-fetched by the Claude Lead on
2026-08-17 (two collection passes). The evidence is the Lead's preserved quote dump at
`C:\tmp\night\p7_official_quotes_dump.md` — the ONLY source of official-page evidence used here.
The implementer performed ZERO account, API-key, wallet, login, SDK, endpoint, or host actions,
and no web/network access of any kind. Repositories were read-only. Third-party sources NEVER
upgrade a claim to VERIFIED; none were used (the dump's explicitly forbidden third-party
netting consensus is nowhere cited as evidence).

## 0. Conventions used in this record

- Statuses are exactly the three mandated values: **VERIFIED** (official evidence exists in the
  dump), **UNKNOWN** (the official pages fetched do not establish it), **ACCOUNT-LEVEL-ONLY**
  (only an account action could answer; separately owner-gated, T0).
- Evidence levels, tagged on every quote (all evidence text below is copied character-exact
  from the dump — never paraphrased):
  - **[V]** = sentence the dump marks as a verbatim quote from the official page (quoted text
    inside the dump's bullets).
  - **[E]** = the dump's page-extraction text (the Lead's fetch-tool extraction of the official
    page, not marked verbatim in the dump).
- VERIFIED requires dump evidence from an official page. Where a row's only evidence is [E]
  (no [V] sentence exists in the dump), the row says so explicitly; a verbatim-sentence
  confirmation pass (still T2, docs-only) is recommended before any Package 1 freeze that leans
  on those exact numbers.
- Where a single claim bundles sub-scopes with different evidence (c, r — and one residual note
  in l), the status is given per sub-scope; no fourth status is introduced.

## 1. Claim table

| # | Claim | Status | Official source | Evidence (exact dump text; [V] = verbatim official sentence, [E] = dump page-extraction) |
|---|---|---|---|---|
| a | Sub-account creation eligibility (volume gate, counts, scaling) | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts | [V] "Up to 10 sub-accounts can be created after reaching $100,000 in volume" · [V] "Every additional $100M in volume enables the ability to create 1 additional sub-account, up to a maximum of 50 sub-accounts" |
| b | Sub-account fee treatment | **VERIFIED** | same page (D1) | [V] "Sub-accounts share the same fee tiers as the master account, but referral discounts do not apply to sub-accounts" |
| c | Sub-account clearinghouse/margin treatment (incl. under portfolio margin) | **VERIFIED** (sub-scope: under portfolio margin) · **UNKNOWN** (general clearinghouse/margin treatment of sub-accounts outside portfolio margin) | portfolio-margin page (D7); sub-accounts page (D1) | [V] "Sub-accounts are still treated separately under portfolio margin." · Negative evidence [E] (D1): "Page does NOT address: technical creation steps, transfer rules, margin/clearinghouse treatment, testnet vs mainnet differences." Dump gap 5: "Sub-account margin/clearinghouse treatment details beyond D7's 'treated separately': limited." |
| d | API-wallet counts per master and per sub-account | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts (D1) | [V] "The number of API wallets available starts at 3 for all master accounts and increases by 2 per sub-account" · [E] (D2): "No explicit total API-wallet limit stated ON THIS PAGE (but see D1's count rule)." The quote expresses a master-account quota that grows +2 per sub-account; no separate independently-sized per-sub-account quota is stated. |
| e | API-wallet signing authority for sub-accounts (no private keys, vaultAddress) | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets (D2) | [V] "A master account can approve API wallets to sign on behalf of the master account or any of the sub-accounts" · [V] "It's recommended to use separate API wallets for different subaccounts" · [E] "Sub-accounts do not have private keys; actions for a sub-account are signed by the master (or an approved API wallet) with the vaultAddress field set to the sub-account address." |
| f | API-wallet nonce rules (per-signer tracking, 100-nonce window, validity band) | **VERIFIED** | same page (D2) | [V] "Nonces are tracked per signer, which is the user address if signed with private key of the address, or the agent address if signed with an API wallet" · [V] "The 100 highest nonces are stored per address" · [E] validity band: "nonces must fall within (T - 2 days, T + 1 day) of block timestamp" |
| g | API-wallet lifecycle (expiry, pruning, deregistration, regeneration guidance) | **VERIFIED** | same page (D2) | [V] regeneration guidance: "Generate a new agent wallet on future use to avoid unexpected behavior" · [E] "Removal scenarios: unnamed wallet deregistered when a new unnamed one is approved; wallets can expire; wallets pruned when the registering account no longer has funds." |
| h | Same-symbol netting / hedge mode (simultaneous long+short on one asset) | **UNKNOWN** | pages fetched that fail to establish it: margining (D4), perpetual-assets (D5) | Negative evidence [E] (D4): "Page does NOT address: cross+isolated coexistence on one asset; simultaneous long and short (hedge mode)." · [E] (D5): "Page does NOT discuss position netting, one-position-per-asset, opposing orders reducing positions, or hedge mode." · Dump gap 1: "Same-symbol netting / hedge mode: no official sentence found (third-party consensus says one-way netting per account; NEVER cite that as VERIFIED)." No official sentence exists in the dump; the third-party consensus is NOT evidence and is NOT cited as such. |
| i | Cross vs isolated margin defaults and strict-isolated assets | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining (D4) | [V] "Cross margin is the default, which allows for maximal capital efficiency by sharing collateral between all other cross margin positions." · [V] "Isolated margin is also supported, which allows an asset's collateral to be constrained to that asset." · [V] "Some assets are strict isolated, which functions the same as isolated margin with the additional constraint that margin cannot be removed." |
| j | Cross+isolated coexistence on the same asset | **UNKNOWN** | margining page (D4) | Negative evidence [E] (D4): "Page does NOT address: cross+isolated coexistence on one asset; simultaneous long and short (hedge mode)." Dump gap 2: "Cross+isolated coexistence on the same asset: not addressed." |
| k | Account abstraction modes and their operational limits (50k actions/day etc.) | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/account-abstraction-modes (D6) | [V] Unified Account: "single balance for each asset. This balance collateralizes all cross margin positions in that asset and is unified with spot balance in that asset" · [V] Portfolio Margin: "single portfolio unifying all eligible assets, which are currently HYPE, BTC, USDC, USDT" · [V] Manual/Standard: "separate perp and spot balances, separate DEX balances. Cross margin applies to each DEX separately" · [V] "Builder code addresses must be in standard mode to accrue builder fees" · [V] "Portfolio margin and unified account are limited to 50k user actions per day. Standard mode has no such restrictions." · [V] API note (on unified/portfolio-margin modes): "all balances and holds in the spot clearinghouse state. Individual perp dex user states are not meaningful." · [E] "DEX Abstraction (discontinued)" |
| l | Portfolio margin status, eligibility thresholds, sub-account treatment | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/portfolio-margin (D7) | [V] "Under portfolio margin, a user's spot and perps trading are unified for greater capital efficiency." · [V] "Sub-accounts are still treated separately under portfolio margin." · [V] described as "a generalization of cross margin" · [V] access fragments: ">$5M in weighted volume or account value >$10k" and "<$25M" · [E] "plus supply/borrow caps" · Residual UNKNOWN (noted, not a row split): "No explicit alpha/live designation on the page." |
| m | Leverage ranges and maintenance-margin rule | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/perpetual-assets (D5) + margining (D4) | [V] "Max leverage varies by asset, ranging from 3x to 40x. Maintenance margin is half of the initial margin at max leverage." · [V] "Leverage can be set by a user to any integer between 1 and the max leverage. Max leverage depends on the asset." |
| n | IP-based REST rate limits and weights | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits (D3) | [V] "aggregated weight limit of 1200 per minute" · [E] "exchange request weight `1 + floor(batch_length / 40)`; info weights 2 / 20 / 60 by type; per-item surcharges ("additional rate limit weight per 20 items returned"; candleSnapshot per 60 items); explorer weight 40" (the fragment "additional rate limit weight per 20 items returned" is [V]) |
| o | WebSocket connection/subscription/message limits | **VERIFIED** (evidence level: [E] only — no verbatim sentence preserved in the dump) | same page (D3) | [E] "max 10 connections; 30 new connections/min; 1000 subscriptions; 10 unique users across user-specific subscriptions; 2000 messages/min sent; 100 inflight posts" |
| p | Address-based limits and sub-accounts-as-separate-users treatment | **VERIFIED** | same page (D3) | [V] "sub-accounts treated as separate users" · [V] "1 request per 1 USDC traded cumulatively" · [V] "initial buffer of 10000 requests" · [E] "throttled to one request per 10 seconds when limited" |
| q | Open-order and cancel allowances | **VERIFIED** (evidence level: [E] only — no verbatim sentence preserved in the dump) | same page (D3) | [E] "cancels `min(limit + 100000, limit * 2)`; open orders 1000 + 1 per 5M USDC volume, cap 5000" |
| r | TESTNET parity of the above (base URL, faucet, whether gates/limits differ) | **VERIFIED** (sub-scope: base URL + faucet mechanics, [E] only) · **UNKNOWN** (whether the sub-account volume gate, API-wallet counts, or rate limits differ on testnet) | https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/testnet-faucet + https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api (D8) | [E] "Testnet faucet requires a mainnet deposit on the same address; claims 1,000 mock USDC at app.hyperliquid-testnet.xyz/drip." · [E] "API: same requests work against testnet base URL `https://api.hyperliquid-testnet.xyz` (mainnet: `https://api.hyperliquid.xyz`)." · [E] "NOT stated anywhere fetched: whether the sub-account volume gate, API-wallet counts, or rate limits differ on testnet." |
| s | The actual trading account's cumulative volume / current sub-account eligibility | **ACCOUNT-LEVEL-ONLY** | n/a — not a documentation fact | Dump gap 4: "The actual trading account's cumulative volume / sub-account eligibility: account fact — ACCOUNT-LEVEL-ONLY by definition." Answerable only by an account-level check under its own future owner gate (T0). No such action was performed. |

**Row tally (19 rows):** VERIFIED 16 · UNKNOWN 2 (h, j) · ACCOUNT-LEVEL-ONLY 1 (s).
Sub-scope caveats inside VERIFIED rows: c general sub-account margin/clearinghouse treatment and
r testnet parity of gates/limits remain UNKNOWN; l carries a noted residual UNKNOWN
(alpha/live designation). Evidence level: 13 of the 16 VERIFIED rows carry at least one
dump-marked verbatim official sentence; rows o and q (and r's VERIFIED sub-scope) rest on
[E] extraction text only.

## 2. Implications for Package 1 (advisory only — freezes nothing)

Package 1's exchange-dependent Section-B subset (backlog §4 Package 1, §5 item 2: subaccount
eligibility/fallback, agent-wallet behavior, same-symbol netting, margin mode, API limits,
worker-boundary and feed-topology choices) is conditioned on this record. This section informs;
all freeze decisions remain with Package 1's own gate.

**Now informed by VERIFIED facts:**
- Subaccount-per-worker isolation is **conditional by design**: sub-accounts are volume-gated
  (10 after $100k; +1 per $100M; cap 50 — row a). The one-risk-bucket-per-subaccount model in
  `docs/30` cannot be assumed available; a fallback (e.g. virtual books under one account) must
  stay a first-class design branch until the actual account's gate status is established (row s).
- Agent-wallet pattern is documentation-aligned (rows d, e, f, g): master-level wallets
  (baseline 3, +2 per sub-account), master-approved signing on behalf of sub-accounts,
  recommended separate API wallets per sub-account, per-signer nonce tracking with a 100-nonce
  window, and a wallet lifecycle (expiry/pruning/deregistration + regenerate-on-reuse) that
  belongs in the worker-identity contract.
- Margin-mode defaults (rows i, m): cross is the exchange default; isolated and strict-isolated
  exist; leverage is 1..asset-max (3x–40x) with maintenance margin = half of initial at max
  leverage — relevant to any per-worker margin-mode and leverage-cap specification.
- Mode ceilings (rows k, l): portfolio margin and unified account are capped at 50k user
  actions/day; standard mode is not; sub-accounts remain separate under portfolio margin; PM
  eligibility is threshold-gated (" >$5M in weighted volume or account value >$10k", "<$25M").
- API-limit topology (rows n, o, p, q): the IP-based 1200/min weight budget and the WebSocket
  10-connection / 1000-subscription caps are shared per IP (a real shared constraint for a
  single-VPS multi-worker topology), while address-based budgets treat sub-accounts as separate
  users — per-worker address-level isolation gains budgets, but the IP-level budget and WS
  connection cap must be shared/planned across workers.

**Still blocked on UNKNOWNs (not freezable from this record):**
- Same-symbol netting / hedge mode (h) — same-symbol concurrency stays closed pending verified
  exchange mechanics and subaccount or virtual-book proof (backlog §3).
- Cross+isolated coexistence on one asset (j).
- General sub-account margin/clearinghouse treatment beyond "treated separately under portfolio
  margin" (c, general sub-scope).
- TESTNET parity of the volume gate, wallet counts, and rate limits (r) — testnet-derived
  evidence cannot be assumed to transfer to mainnet gates/limits.

**ACCOUNT-LEVEL-ONLY (each listed under its own future owner gate, T0):**
- The actual account's cumulative volume → current sub-account eligibility and current wallet
  count (row s).
- Any supervised account-level check of same-symbol behavior (h) should the documentation dig
  stay dry — per the addendum, only such a separately gated check could resolve it.

## 3. Addendum reconciliation (each lead in `HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md`)

- §2.1 Sub-accounts volume-gated (quotes + conditional-availability implication, testnet-UNKNOWN
  preserved): **confirmed** — all four D1 sentences appear verbatim in the dump; testnet gate
  remains UNKNOWN.
- §2.2 API wallets (signing, nonces, lifecycle, separate-wallet recommendation): **confirmed** —
  D2 verbatim sentences cover signing authority, per-signer nonces, the 100-nonce store and the
  separate-wallet recommendation; the (T − 2 days, T + 1 day) band and the removal scenarios are
  present in the dump at [E] extraction level (substance confirmed, evidence level noted).
- §2.3 Margin modes (cross default, isolated, strict isolated, leverage 1..max, 3x–40x,
  maintenance = half initial at max, HIP-3 no-cross, coexistence/hedge not addressed):
  **confirmed** — D4/D5 verbatim; both "not addressed" notes remain accurate.
- §2.4 API rate limits (1200/min IP weight, request weights, WS limits, address-based treatment,
  accrual/buffer/throttle, cancel and open-order allowances; shared-IP/shared-WS implication):
  **confirmed** — "aggregated weight limit of 1200 per minute" and "sub-accounts treated as
  separate users" verbatim; the remaining numbers confirmed at [E] extraction level.
- §3.1 Same-symbol netting / hedge mode UNKNOWN: **still unknown** — no official sentence in the
  dump; third-party consensus correctly excluded.
- §3.2 TESTNET parity of gates/counts/limits: **still unknown** — explicitly "NOT stated
  anywhere fetched".
- §3.3 Cross+isolated coexistence on one asset: **still unknown** — D4 explicitly does not
  address it.
- §3.4 Current account's own eligibility: **still unknown** from documentation; classified
  ACCOUNT-LEVEL-ONLY in this record (account fact; own future T0 owner gate).

## 4. Self-verification

- Every VERIFIED claim above carries dump evidence text copied character-exact from
  `C:\tmp\night\p7_official_quotes_dump.md`, never paraphrased. 13 of the 16 VERIFIED rows are
  anchored by at least one dump-marked verbatim official sentence; the rows that rest on dump
  page-extraction text only (o, q, and r's VERIFIED sub-scope) are explicitly flagged as such
  inline.
- Every claim not backed by dump text is labeled UNKNOWN or ACCOUNT-LEVEL-ONLY (rows h, j, s;
  plus the flagged sub-scopes of c and r and the residual note in l). UNKNOWN stays UNKNOWN.
- Third-party material (the one-way-netting consensus) appears only as a forbidden non-source
  named in negative evidence; it never upgrades any claim to VERIFIED.
- No account, API-key, wallet, login, SDK, endpoint, host, or network action of any kind was
  performed by the implementer; repositories were treated as read-only; the only file written is
  this record.


### assistant
All four inputs read and cross-checked. Review complete.

## SPEC-COMPLIANCE TABLE

| # | p1_spec required content | Present | Substantive | Location / notes |
|---|---|---|---|---|
| 1 | Header: artifact = Package 1 architecture contract pack, T2 documentation, governs FUTURE separately-gated T0, nothing activates | YES | YES | Header + "Explicit non-authorization"; repeated activation denial |
| 2 | Header: worktree HEAD hash | YES | YES | `b08aab35f7625e481c4a06f47ceffd1fd0740216`, with docs/30 HEAD-parity note and disclosed pointer drift (`docs/01:761`→`:795`) |
| 3 | Section A — worker identity (tuple, uniqueness/immutability, P&L/state/order-identity separation, docs/23-consistent) | YES | YES | A.1: 7-field tuple, never-reuse `worker_id`, active-tuple uniqueness, retire+successor immutability, per-worker ledgers/state namespaces, dual-identity extension via new domain version, flagged docs/23 schema-v3 tension |
| 4 | Section A — store model (settled per docs/30 OR OPEN with options, consequences, labeled recommendation) | YES | YES | A.2: OPEN per `docs/30:320-322`/`:899`; three options + consequences; recommendation explicitly labeled "a recommendation, NOT a decision"; decision stays OPEN |
| 5 | Section A — Guardian veto semantics (inputs, 3-tier scope, precedence vs worker-local, fail-closed, thresholds later) | YES | YES | A.3: read-only evidence-derived inputs, per-order/pause/global tiers, risk-reducing exits excluded, veto-not-mutate, AND-gate precedence, fail-closed no-new-entries, thresholds deferred to later owner gate |
| 6 | Section B — all eight conditioned decisions | YES | YES | B.1 worker boundary, B.2 feed topology, B.3 subaccount fallback, B.4 subaccount eligibility, B.5 agent-wallet assignment, B.6 same-symbol netting, B.7 margin mode, B.8 API-limit budget — each with stateable-now + unfrozen/blockers |
| 7 | Section B — single-account/virtual-book fallback stated as DEFAULT until account eligibility separately established (volume gate claim a + s) | YES | YES | B.3 "EXPLICIT DEFAULT (per Gate-1)"; subaccount topology framed as UPGRADE branch; B.4–B.8 assume it |
| 8 | Section B — 1200 weight/min IP budget and 10-connection WS cap treated as VPS-shared resources (claims n, o); per-worker budget allocation mandated | YES | YES | B.1 and B.8 both state VPS-wide sharing across ALL workers and mandate a central allocator with per-worker budgets |
| 9 | Explicit non-authorization section | YES | YES | Documentation-only; standing prohibitions restated (no VPS/host, credentials, exchange-account/wallet/subaccount actions, TESTNET/MAINNET, ARM/orders, Pine/parity/MTC, V1 mutation) |
| 10 | Self-verification section | YES | YES | Section-B provenance, repo provenance, flagged resolutions (docs/23 domain version, A12 semantics, A4 caveat), read-only discipline, counts |

## SECTION-A FINDINGS

- **Worker identity (A.1) — settled, cited, no finding.** The 7-field tuple, per-field rationale, uniqueness rules (surrogate `worker_id` never reused; active natural-key uniqueness; same-symbol lever gated CLOSED by B.6), immutability (retire + successor, no inheritance), and separation rules are all contract text with specific citations (`docs/30`, `docs/21`, `docs/23`). The docs/23 interaction is handled correctly: dual identity is extended via a NEW domain version, the single-strategy schema-v3 pin is flagged as a protected future-T0 migration, and `docs/23` is not contradicted or modified.
- **Store model (A.2) — OPEN, correctly labeled, no disguised decision.** The pack cites `docs/30:320-322`/`:899` as the genuine leave-open authority, presents three options with consequences, and labels the hybrid recommendation explicitly as "a recommendation, NOT a decision." The decision itself is stated to stay OPEN and "NOT frozen by this pack." This is the compliant alternative under review requirement (B).
- **Guardian veto semantics (A.3) — settled semantics, no thresholds, no finding.** Inputs are read-only and evidence-derived (reconciliation opt-in flagged as unavailable until a future gate); three veto tiers; risk-reducing exits outside veto scope; "vetoes but does not mutate" with citations (`docs/30:284-285`, `:628-632`, `:840-841`); AND-gate precedence with worker-local risk; fail-closed defaults (no new entries, exits never blocked, logged reasons); all numeric thresholds explicitly deferred. Settled as contract text with citations throughout.

## SECTION-B EVIDENCE-TRACE FINDINGS

No evidence-trace violations found. Every exchange-behavior statement in B.1–B.8 traces to a P7 claim id whose status is VERIFIED, and the [V]/[E] evidence levels are reproduced correctly:

- **Claims n/o shared-resource framing:** "aggregated weight limit of 1200 per minute" cited as n [V]; WS caps (10 connections / 30 new/min / 1000 subscriptions / 10 unique users / 2000 msg/min / 100 inflight) cited as o [E]-only, exactly as P7 row o states. Both are treated as VPS-shared across all workers (B.1, B.8) — required check satisfied.
- **Fallback default:** B.3 quotes claim a [V] verbatim and ties the DEFAULT virtual-book branch to claim s (ACCOUNT-LEVEL-ONLY), with migration blocked on s and r. Required check satisfied.
- **Same-symbol netting:** B.6 keeps h UNKNOWN as the primary blocker (with j, s, virtual-book validation, and the supervised account-level check also named) and preserves the conservative closure without asserting any netting mechanic. Required check satisfied — the netting stance is unfrozen; only reopening is conditioned on verified mechanics.
- **Claim-by-claim trace:** a–g, i, k, l, m, n, p all cited with [V] quotes matching the P7 table verbatim; [E]-only rows o and q are flagged as [E]-only with the P7 §0 verbatim-confirmation pass named as a freeze precondition; c and r sub-scope UNKNOWNs and the l residual UNKNOWN are reproduced accurately; s is used only as an ACCOUNT-LEVEL-ONLY blocker. The third-party one-way-netting consensus appears only as a named non-source. No statement leans on a fact absent from the P7 record.

## REQUIRED FINDINGS

none

## NITS

1. **B.6 heading uses "REMAINS CLOSED" instead of the "UNFROZEN" label used by the other seven subsections.** The body does contain an "Unfrozen — blocking items" list and the closure is the conservative, non-exchange-dependent status quo (reopening is what requires verified mechanics), so this is not a required finding — but re-titling to something like "UNFROZEN (conservative closure preserved)" would remove ambiguity.
2. **B.7 introduces one blocker not present as a P7 claim row:** "which abstraction mode the actual account is in … an account-level fact in the same family as s." The pack transparently flags that "no row covers it" and uses it only to keep the decision unfrozen, so it is a conservative gap statement, not a relied-upon exchange fact — but it slightly extends P7's ACCOUNT-LEVEL-ONLY inventory by analogy.
3. **Repo line citations (docs/30, docs/23, docs/21, bridge/app.py, requirements.in) are not independently verifiable from the four review inputs**, which are the only files in scope for this read-only slot. They are present, specific, internally consistent, and the pack discloses its worktree HEAD and the one pointer drift; accepted as-present.

VERDICT: ACCEPT
