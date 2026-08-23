# Old Package 1 §A.2 and Package 7 — Scope Extraction from the 2026-08-17 Bridge V2 Backlog

**Wayfinder ticket:** #52, "Research: extract old Package 1 §A.2 and Package 7 scope from the
2026-08-17 backlog"
**Method:** local repository reading only — no network access, no code changed, no host
contacted. All citations are `file:line` against either this branch's worktree
(`research/old-package-extraction`, based on accepted commit `764da27f`) or an explicitly named
other ref, retrieved read-only via `git show <ref>:<path>`.

## The two questions, stated sharply

- **Q1 — Package 7 ("Official exchange reverification"):** what does it verify, what does it
  output, and under what conditions does it stand — both as originally *scoped* in the
  2026-08-17 backlog and as it stands *today*?
- **Q2 — Package 1 §A.2 ("store model")**: what is Package 1's contract-pack scope overall, and
  specifically — verbatim — what does its §A.2 subsection ask about the worker-state store, and
  what is that decision's status?

**Framing that governs the answer to both** (see §6 for the full evidence): the word "old" in
this ticket's own title is not incidental. The 2026-08-23 wayfinder macro gap audit
(`WAYFINDER_MACRO_GAP_AUDIT_2026-08-23.md`, on branch `feature/wayfinder-gap-audit-20260823`)
found that the accepted master brief still cites "Package 7 exchange reverification (Q6)" and
"Package 1 §A.2 store decision" by name as Bridge-V2 dependencies, but **neither package exists
in the current 69-package delivery plan** — they are "**dangling dependencies inherited from the
retired 2026-08-17 package scheme**." Both packages were, however, actually authored and
T2-accepted that same night as documentation records (§4 below) — so "old" means *superseded by
a later planning generation*, not *never done*.

---

## 1. Package 7 — full definition and scope (verbatim)

### 1.1 As scoped in the accepted backlog

`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md:127-132`:

> ### Package 7 — Official exchange reverification
>
> **Tier: T2, read-only.** Verify current subaccount, agent-wallet, same-symbol
> netting, margin-mode and API-limit facts before V2 architecture relies on
> them. Package 1's exchange-dependent decisions are explicitly conditioned on
> this package's output (see Package 1 and Section 5).

The same file's evidence row names the read-only precondition explicitly
(`BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md:57`, row "Subaccounts and same-symbol isolation"):

> Official-document verification is read-only **T2** and must precede any freeze of these
> decisions (Package 7); account, wallet, exchange and broker work is **T0**.

### 1.2 Fuller scope (kickoff-prep draft)

`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md:605-611` (Scope):

> **Scope.** Verify current subaccount, agent-wallet, same-symbol netting,
> margin-mode, and API-limit facts before V2 architecture relies on them.
> Package 1's exchange-dependent decisions are explicitly conditioned on this
> package's output. ([BACKLOG] §4 Package 7; §3 row "Subaccounts and
> same-symbol isolation": official-document verification is read-only T2 and
> must precede any freeze of these decisions; account, wallet, exchange, and
> broker work is T0.)

**Outputs, per the acceptance criteria** (`BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md:634-643`):

> **Acceptance criteria.** Done means: (a) a verification record listing every
> required claim (subaccount eligibility and volume gate, agent-wallet
> behavior, same-symbol netting/hedge mode, margin mode, API limits) with, per
> claim, the official source (URL plus quoted sentence), and a status of
> VERIFIED / UNKNOWN / ACCOUNT-LEVEL-ONLY; (b) every UNKNOWN stays UNKNOWN
> rather than being filled from third-party or stale sources; (c) every
> ACCOUNT-LEVEL-ONLY item is listed under its own future owner gate with the
> note that account/wallet/exchange work is T0 ([BACKLOG] §3); (d) the record
> passes one T2 review — single reviewer, single round, medium effort
> ([TIERS] §2).

**Explicit prohibitions** (`BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md:623-632`): "Read-only
verification from official public documentation only... No account-level checks... No SDK
calls, no endpoints, no credentials, no host contact, no TESTNET/MAINNET, no ARM/orders, and no
freezing of any Package 1 decision (freezing belongs to Package 1, after this record exists)."

### 1.3 What it actually produced (the completed output — not on this branch)

Package 7 was carried out that same night and its output committed to `master` at commit
`887ec60f` as `MTC_COMMAND_CENTER/11_TRIAGE/P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md`
(150 lines) plus a companion `P7_OFFICIAL_QUOTES_DUMP_2026-08-17.md`. **This file does not exist
on the `research/old-package-extraction` branch (764da27f) or on `master`'s ancestor at the
backlog's own commit — it was retrieved read-only via `git show master:...`.**

Header (`master:MTC_COMMAND_CENTER/11_TRIAGE/P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md:1-17`,
commit `887ec60f`):

> # Package 7 — Official Exchange Reverification Record (T2, read-only)
>
> **Method:** official Hyperliquid documentation pages, live-fetched by the Claude Lead on
> 2026-08-17 (two collection passes). The evidence is the Lead's preserved quote dump at
> `C:\tmp\night\p7_official_quotes_dump.md` — the ONLY source of official-page evidence used
> here. The implementer performed ZERO account, API-key, wallet, login, SDK, endpoint, or host
> actions, and no web/network access of any kind.

Output shape and result tally (`master:...P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md:61`):

> **Row tally (19 rows):** VERIFIED 16 · UNKNOWN 2 (h, j) · ACCOUNT-LEVEL-ONLY 1 (s).

The 19-row claim table covers exactly the domains named in the backlog scope: subaccount
eligibility/volume gate (row a), fee treatment (b), sub-account margin treatment (c), API-wallet
counts (d), signing authority (e), nonce rules (f), wallet lifecycle (g), same-symbol netting/
hedge mode (h, **UNKNOWN**), cross/isolated margin defaults (i), cross+isolated coexistence (j,
**UNKNOWN**), account-abstraction modes (k), portfolio-margin status (l), leverage ranges (m),
IP-based REST limits (n), WebSocket limits (o), address-based limits (p), open-order/cancel
allowances (q), TESTNET parity (r), and the account's actual current eligibility (s,
**ACCOUNT-LEVEL-ONLY**).

What the record explicitly hands forward to Package 1
(`master:...P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md:68-73`):

> Package 1's exchange-dependent Section-B subset (backlog §4 Package 1, §5 item 2: subaccount
> eligibility/fallback, agent-wallet behavior, same-symbol netting, margin mode, API limits,
> worker-boundary and feed-topology choices) is conditioned on this record. This section
> informs; all freeze decisions remain with Package 1's own gate.

---

## 2. Package 1 — contract-pack definition and the §A.2 store decision (verbatim)

### 2.1 Package 1's overall scope, as accepted in the backlog

`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md:77-86`:

> ### Package 1 — V2 architecture contract pack
>
> **Tier: T2.** Settle worker identity, store model and Portfolio Guardian veto
> semantics locally. Worker boundary, feed topology and subaccount fallback —
> and every decision that depends on exchange behavior (subaccount eligibility,
> agent-wallet behavior, same-symbol netting, margin mode, API limits) — are
> **CONDITIONED ON Package 7 output**: they must not be frozen from stale or
> unverified assumptions, and their freeze waits for Package 7's official
> verification record. Documentation only; no code or live exchange assumptions
> without current official evidence.

Kickoff-prep restates the split explicitly in its dispatch-prompt constraints
(`BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md:167-172`):

> Split the pack into (A) non-exchange-dependent decisions (worker identity,
> store model, Guardian veto semantics) and (B) exchange-dependent decisions
> (subaccount eligibility/fallback, agent-wallet behavior, same-symbol
> netting, margin mode, API limits, worker boundary, feed topology).
> Section B decisions must be written as CONDITIONED ON Package 7 output and
> must NOT be frozen; cite [T2-STATUS] finding 2.

**Note on where "§A.2" actually lives:** neither the backlog nor the kickoff-prep draft uses
"A.2" notation anywhere — they only name a two-way split into "(A)" and "(B)". The literal
`§A.2` heading exists **only inside Package 1's own completed output document**,
`P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md`, where Section A's three settled/open items are
numbered A.1, A.2, A.3 (confirmed by grep — see §5 below for why this matters).

### 2.2 §A.2 "Store model" — verbatim, in full

Package 1's completed output was committed to `master` at commit `887ec60f` as
`MTC_COMMAND_CENTER/11_TRIAGE/P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md` (580 lines).
**This file does not exist on the `research/old-package-extraction` branch (764da27f)** —
retrieved read-only via `git show master:...`.

`master:MTC_COMMAND_CENTER/11_TRIAGE/P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md:159-205`,
commit `887ec60f` (the section heading through its full text):

> ## A.2 Store model — OPEN (options, consequences, labeled recommendation)
>
> **Why OPEN:** docs/30 settles the *separation requirement* but deliberately leaves the store
> question open: "The store question itself (per-worker SQLite vs. central Postgres) is
> deliberately left open in A12; the *separation requirement* is decided regardless of which
> store wins" (`docs/30:320-322`; A12 lists it at `docs/30:899`). The separation requirement of
> A.1 is therefore binding whichever option is later chosen; the store itself is NOT decided
> here.
>
> **Options and consequences.**
>
> 1. **Per-worker SQLite (one store per worker).**
>    - Strongest storage-level isolation: one worker's corruption or bug is confined to its own
>      file — A6's "fully separate stores per worker — strongest isolation, harder aggregate
>      reporting and more moving parts to back up and reconcile" (`docs/30:318-319`).
>    - Aggregate portfolio reads (Guardian, dashboard) must fan out over N stores or go through
>      an aggregation layer; backups and schema migrations run N times, with version-skew risk
>      between workers.
>    - Keeps today's dependency footprint (SQLite is stdlib; `requirements.in:26-35` contains no
>      external database driver; `docs/01_ARCHITECTURE.md:795` defers Postgres/Redis/Docker to
>      v2).
> 2. **Central store (single Postgres; per-worker schemas or enforced tenancy).**
>    - One aggregate query surface — easiest for the Guardian and the V2 dashboard; single
>      migration point; one backup.
>    - Shared failure domain: one corrupt or mis-migrated store puts every worker's evidence at
>      risk; tenancy must be structural (separate schemas / row-level separation), because the
>      tag-column alternative is exactly A6's "one missing filter silently mixes strategies"
>      (`docs/30:316-317`).
>    - New infrastructure and ops surface (service, backups, credentials); today explicitly
>      deferred (`docs/01_ARCHITECTURE.md:795`) and absent from `requirements.in:26-35`.
> 3. **Hybrid: per-worker SQLite as worker-local source of truth + a small supervisor-owned
>    central store holding only (a) the worker registry / identity tuples and (b) the aggregate
>    portfolio snapshot the Guardian reads.**
>    - Keeps the correctness-critical ledgers (P&L, state, order identity) in per-worker
>      isolation while giving the Guardian and dashboard a single read surface.
>    - The central snapshot must be DERIVED from worker evidence (never an independent truth
>      that can drift), on the same evidence-derived-not-claimed principle as `docs/21:16-18`,
>      with an explicit freshness/reconciliation policy; and it adds one more component to
>      define.
>
> **RECOMMENDATION (clearly labeled: a recommendation, NOT a decision).** Option 3 — hybrid,
> per-worker SQLite source-of-truth stores plus a supervisor-owned registry/aggregate store —
> because it satisfies A6's separation requirement regardless of which long-term store wins,
> preserves the current dependency footprint (no new external service on the V2 critical path),
> and still gives the Guardian one read surface without placing all workers in a single failure
> domain. Escalation to a central Postgres remains open as a later, separately gated decision if
> aggregate load or operations demand it. **The decision itself stays OPEN per `docs/30:899` and
> is NOT frozen by this pack.**

The pack's own self-verification count confirms §A.2 is the one deliberately-undecided item
(`master:...P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md:575-577`):

> **Counts:** Section A — 3 decision areas: 2 settled (A.1 worker identity, A.3 Guardian veto
> semantics), 1 deliberately OPEN with a labeled recommendation (A.2 store model).

For context, §A.2 sits alongside two *settled* siblings in the same pack: **A.1 Worker identity
contract — SETTLED** (a 7-field immutable tuple:
`worker_id, strategy_id, symbol, timeframe, strategy_version, config_hash, account_label`,
`master:...P1...md:71-77`) and **A.3 Portfolio Guardian veto semantics — SETTLED (semantics
only; no thresholds)** (three veto tiers, "vetoes but does not mutate,"
`master:...P1...md:207-211`). Only the store model was left open.

---

## 3. Every dependency statement linking Package 1 decisions to Package 7 output

1. **Backlog, Package 1's own definition** (`BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md:81-84`):
   "every decision that depends on exchange behavior (subaccount eligibility, agent-wallet
   behavior, same-symbol netting, margin mode, API limits) — are **CONDITIONED ON Package 7
   output**... their freeze waits for Package 7's official verification record."
2. **Backlog, Package 7's own definition** (`BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md:130-132`):
   "Package 1's exchange-dependent decisions are explicitly conditioned on this package's
   output (see Package 1 and Section 5)."
3. **Backlog §5, fastest safe order, items 1-2** (`BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md:144-152`):
   "Start **Package 7** first. Its read-only official Hyperliquid verification gates every
   exchange-dependent decision below... The exchange-dependent subset of **Package 1** ... is
   **CONDITIONED ON Package 7 output** and must not be frozen before that verification is on
   record."
4. **Backlog §3, "Subaccounts and same-symbol isolation" row**
   (`BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md:57`): "Official-document verification is
   read-only **T2** and must precede any freeze of these decisions (Package 7)."
5. **T2 acceptance record, FINDING-2, resolved**
   (`BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md:101-113`): confirms the conditioned
   set is identical across all four backlog locations (Package 1, Package 7, §5, and the §3
   subaccounts row) and that "no location freezes exchange behavior from stale assumptions."
6. **Package 1's own completed output, Section B header**
   (`master:...P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md:276-282`, commit `887ec60f`):
   "# Section B — CONDITIONED ON Package 7 (nothing here is frozen beyond P7 evidence)... Per
   Gate-1: the fallback (virtual books / single-account partitioning) is the DEFAULT design
   branch until account eligibility is separately established."
7. **Package 1's Section-B authority line**
   (`master:...P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md:15-18`): "**Section-B authority:**
   `C:\tmp\night\P7_EXCHANGE_REVERIFICATION_RECORD.md` (claim ids a–s). Section B relies ONLY on
   facts that record marks VERIFIED; where it says UNKNOWN or ACCOUNT-LEVEL-ONLY, the
   corresponding decision stays explicitly UNFROZEN with the blocking item named."
8. **Package 7's own completed output, §2**
   (`master:...P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md:70-73`, commit `887ec60f`):
   "Package 1's exchange-dependent Section-B subset ... is conditioned on this record. This
   section informs; all freeze decisions remain with Package 1's own gate."
9. **Master architecture brief, roadmap dependency rows** (both the working-tree copy and the
   accepted `764da27f` branch — see §5): "Package 7 exchange reverification (Q6). Package 1
   §A.2 store decision." listed as a `Dependencies` row for both Bridge V2 (combined) and V2B.

Important scope distinction: **§A.2 (the store model) is explicitly NOT one of the
exchange-dependent Section-B items conditioned on Package 7.** §A.2 lives in Section A
("Settled locally... no exchange dependency," `master:...P1...md:65-69`) and is OPEN for a
different reason — docs/30 itself defers the store choice (`docs/30:899,320-322`), independent
of any exchange fact. The Package-7-conditioned items are Section B's eight decisions (worker
boundary, feed topology, subaccount fallback, subaccount eligibility, agent-wallet assignment,
same-symbol netting, margin mode, API-limit budget model) — not §A.2. The master brief's
roadmap rows (dependency #9 above) cite Package 7 and Package 1 §A.2 as **two separate, both
still-open** prerequisites for Bridge V2, not as one item depending on the other.

---

## 4. Status — were Packages 1 and 7 accepted?

**Yes, both were authored and accepted as T2 documentation records the same night** (2026-08-17),
distinctly from the separate question of whether §A.2's internal store choice was *decided*
(it was deliberately left open, by design).

### 4.1 Backlog itself (the document defining Package 1/7's scope)

`BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md:12`: **"Verdict: ACCEPT"** (GLM-5.3
official T2 reviewer, one round, per Decision 4 in the owner-decisions record).

### 4.2 Owner authorization to start

`OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md:57-60` (Decision 5):

> - **Package 7** (official exchange reverification, T2 read-only, public docs only): STARTED.
> - **Package 1** (V2 architecture contract pack, T2; exchange-dependent half conditioned on
>   Package 7's record): STARTED.

### 4.3 The completed Package 1/7/2 output documents — accepted

`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_PACKAGES_712_T2_ACCEPTANCE_2026-08-17.md` (master,
commit `887ec60f`) records all three as **ACCEPT**:

| Package | Committed file | Verdict |
|---|---|---|
| 7 — Official exchange reverification | `P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md` | **ACCEPT** |
| 1 — V2 architecture contract pack | `P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md` | **ACCEPT** |
| 2 — MTC integration contract pack | `P2_MTC_INTEGRATION_CONTRACT_PACK_2026-08-17.md` | **ACCEPT** |

Reviewer was DeepSeek `deepseek-v4-pro` (different provider from the GLM-5.3 author), one round
each, zero required findings on all three; a Gemini 3.7 Flash cross-check returned
`CROSSCHECK_CLEAN`. Package 1's specific verdict text
(`master:BRIDGE_V2_PACKAGES_712_T2_ACCEPTANCE_2026-08-17.md`, "### Package 1 — VERDICT: ACCEPT"):

> Section A: worker identity settled (7-field immutable tuple), Guardian veto semantics settled
> (3 tiers, veto-not-mutate, fail-closed, thresholds deferred), **store model correctly OPEN
> with a labeled recommendation.** Section B: all 8 exchange-dependent decisions conditioned on
> the P7 record and explicitly unfrozen...

And the acceptance record's explicit scope of what "accepted" does *not* mean
(`master:BRIDGE_V2_PACKAGES_712_T2_ACCEPTANCE_2026-08-17.md`, "What acceptance means"):

> Packages 7, 1, 2 are accepted **T2 documentation records**. They freeze contract text and
> verification statuses only. They authorize **no** implementation, wiring, schema migration,
> activation, account/wallet/exchange action, TESTNET/MAINNET activity, ARM/orders, Pine/MTC/
> parity change, deployment, or host contact. Package 1's Section-B decisions remain unfrozen
> pending their named blockers...

### 4.4 §A.2 specifically — never decided, still open as of 2026-08-23

Despite the pack's acceptance, §A.2's own choice among its three options was never made. The
owner-memory working file records this as a standing, still-open gate on at least three later
dates:

- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:126` (2026-08-17 night, "AFTER THE 2026-08-17
  NIGHT RUN, PART 2"): "2. Pick the Package 1 §A.2 store-model option (OPEN with labeled
  recommendation)."
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:94-96,110-111` (2026-08-18 entries): "Open owner
  gates unchanged: ... **P1 §A.2 store-model choice** ..." (listed twice, unresolved both times).
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:31-32` (2026-08-23, quoting the wayfinder gap
  audit): "old Package 1 §A.2 store decision — both cited by the accepted brief §17.2, neither
  exists in the 69-package plan." *(This is the AI-memory file's own working note reflecting the
  audit; NEXT_STEPS.md is a live working file, not itself an accepted artifact — treat this line
  as a pointer to the audit report quoted directly in §6, not as independent evidence.)*

No file located in this repository records an owner pick among Options 1/2/3 of §A.2. The
decision remains **OPEN**.

---

## 5. Cross-check against the Master Architecture Brief

The task specified checking `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` for
"Package 7" and "A.2" citations, and warned that the current working-tree copy (on
`codex/bridge-help-wiki`) may differ from the accepted branch. It does differ substantially —
a full-file diff between the working copy and the accepted `764da27f` version is **5,794 lines**
— but the two specific dependency citations below are byte-identical in both, just at different
line numbers (the accepted version is longer due to unrelated intervening edits):

| | Working tree (`codex/bridge-help-wiki`, dirty) | Accepted branch (`764da27f`) |
|---|---|---|
| §17.2 (combined V2) Dependencies row | line 2045 | line 2597 |
| §17.2b (V2B) Dependencies row | line 2069 | line 2623 |

Both read, verbatim, identically in each version
(`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2597`, accepted branch):

> | **Dependencies** | Phase 0 complete. Package 7 exchange reverification (Q6). Package 1 §A.2
> store decision. |

and (`...md:2623`, accepted branch, §17.2b V2B):

> | **Dependencies** | V2A accepted. Package 7 exchange reverification (Q6). Package 1 §A.2 store
> decision. |

The brief's owner-decisions index also carries the same pairing forward at
`...md:57` (working tree) / present identically in the accepted branch's decisions index:
"**Q6** | Account binding decided after Package 7; subaccounts preferred | §10.2, §17.2", and
the answered-decision text itself
(accepted branch `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1847`):

> **Account binding — [OWNER — Q6]:** decide after Package 7's official Hyperliquid
> verification, then prefer **one subaccount + separate API/agent wallet per independent
> strategy or risk bucket** where reliably supported. Fallback (virtual books inside one
> account) must be specified before it is needed, not during an incident.

**No section of the master brief itself is labeled "§A.2"** (its own Appendix A, at line 2302 in
the accepted branch, has no A.2 subsection) — confirming that every "§A.2" reference anywhere in
the brief is a citation *into* the Package 1 output document, not a self-reference. `grep -n
"A\.2|§A"` across the entire brief (both versions) returns matches only at the two dependency
rows above plus the Q6 index/DL-10 rows (`...md:2766`, accepted branch, "**DL-10** | Account
binding decided after Package 7 verification; prefer Hyperliquid subaccounts where reliably
supported. *(Q6)*") — none of which define what §A.2 is; they only depend on it by name.

---

## 6. The "old" / dangling-dependency finding (why this ticket exists)

The 2026-08-23 wayfinder macro gap audit (`WAYFINDER_MACRO_GAP_AUDIT_2026-08-23.md`, branch
`feature/wayfinder-gap-audit-20260823`, commit `6888b416`) is the direct source of this ticket's
"old Package 1 §A.2 and Package 7" framing. Its finding, in full
(`master`-adjacent branch `feature/wayfinder-gap-audit-20260823:...WAYFINDER_MACRO_GAP_AUDIT_2026-08-23.md:45-46`):

> **B-GAP-1 · Two dependencies of the accepted brief point at packages that no longer exist —
> internal defect, blocking Q6.**
> Brief §17.2 lists as Bridge-V2 dependencies: "**Package 7 exchange reverification (Q6)**" and
> "**Package 1 §A.2 store decision**". Those IDs come from the retired 2026-08-17 scheme
> (`11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`: Package 7 = *Official exchange
> reverification*, "start Package 7 first"; Package 1 = *V2 architecture contract pack*, its
> exchange-dependent decisions "explicitly conditioned on Package 7's output"). The 69-package
> plan contains **neither** (grep: zero hits for "Package 7", "reverification", "§A.2").
> Consequence: **Q6 — subaccounts vs virtual books, i.e. the answer to venue position netting —
> is waiting on a verification task that no current package owns**, while WP-V2B-03
> (multi-worker) and the bucket design proceed without it.

Its proposed (unauthorized, findings-only) remedy
(`...WAYFINDER_MACRO_GAP_AUDIT_2026-08-23.md:109-110`):

> - **VEN-A Exchange reverification + account-binding design** — rescues old Package 7; closes
>   Q6 (subaccounts vs virtual books **including the fallback spec**), designs
>   per-strategy-versus-venue-net reconciliation. **Must be accepted before WP-V2B-03
>   (multi-worker) starts** — a dependency the current plan is missing.
> - **VEN-B State-store decision** — rescues old Package 1 §A.2 so the brief's dependency line
>   points at something real again.

And the plain-language owner ask (`...WAYFINDER_MACRO_GAP_AUDIT_2026-08-23.md:130`):

> **Two old prerequisites fell out of the new plan** — the official exchange re-check (old
> "Package 7") and the storage decision (old "Package 1 §A.2"). The accepted brief still depends
> on both by name. They need new homes; without the first one, the "one account or many
> sub-accounts" question can never be answered.

That audit report is explicitly **"FINDINGS AND PROPOSALS ONLY"** — it "adds no requirement, no
safeguard, no package and no number to the canonical set," and VEN-A/VEN-B are not yet
authorized (`...WAYFINDER_MACRO_GAP_AUDIT_2026-08-23.md:5,97-99`).

**Reconciling this with §4 above:** the two findings are not in tension. Package 7 and Package 1
§A.2 *were* completed and T2-accepted as documentation on 2026-08-17 (the actual verification
record and contract pack exist and were reviewed). What the 2026-08-23 audit found is a
**planning-generation gap**, not a missing-work gap: when the 69-package delivery plan
(`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`) was built on 2026-08-22, it did
not carry forward a package that owns (a) resolving §A.2's still-open store choice, or (b) any
follow-on Package-7-style reverification that a later, more mature account state might need
(e.g., the ACCOUNT-LEVEL-ONLY items — claim **s**, actual sub-account eligibility — were never
resolved because they require an account-level check that is separately owner-gated and never
authorized). The master brief's dependency rows point at package IDs from a scheme that the plan
itself replaced, which is why the audit calls them "dangling."

---

## Summary answers

1. **Package 7** verifies official Hyperliquid documentation facts (subaccount eligibility/volume
   gate, agent-wallet rules, same-symbol netting, margin modes, API rate limits) via a read-only
   T2 claim table with VERIFIED/UNKNOWN/ACCOUNT-LEVEL-ONLY status per claim; its actual output
   (`P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md`, master `887ec60f`) verified 16 of 19
   claims, left same-symbol netting (h) and cross+isolated coexistence (j) UNKNOWN, and marked
   the account's actual eligibility (s) ACCOUNT-LEVEL-ONLY. Condition: read-only, official public
   docs only, zero account/wallet/network actions; gates Package 1's exchange-dependent
   (Section B) decisions.
2. **Package 1 §A.2** is the "store model" item inside Package 1's Section A (settled-locally,
   non-exchange-dependent decisions). It presents three options (per-worker SQLite / central
   Postgres / hybrid), names Option 3 (hybrid) as a labeled recommendation, and explicitly states
   the choice itself "is NOT decided here" — it stays OPEN per the Bridge's own design doc
   (`docs/30:899`). It was never exchange-conditioned; it is open by the Bridge design doc's own
   deferral, not by Package 7.
3. Both the 2026-08-17 backlog (defining these packages) and the actual Package 1/7 output
   documents were **T2-accepted** the same night. The §A.2 *choice itself* was never made and
   remains open through at least 2026-08-23.
4. As of the 2026-08-23 wayfinder macro gap audit, both are "dangling dependencies" — still
   named in the accepted master brief's roadmap, absent from the current 69-package plan, with
   unauthorized rescue proposals (VEN-A, VEN-B) pending an owner decision.

## Sources (all local, read-only)

- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_PACKAGE_KICKOFF_PREP_2026-08-17.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`
  (working tree on `codex/bridge-help-wiki`, and accepted branch `764da27f`)
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` (working tree, for status pointers only)
- `master:MTC_COMMAND_CENTER/11_TRIAGE/P1_V2_ARCHITECTURE_CONTRACT_PACK_2026-08-17.md`
  (commit `887ec60f`)
- `master:MTC_COMMAND_CENTER/11_TRIAGE/P7_EXCHANGE_REVERIFICATION_RECORD_2026-08-17.md`
  (commit `887ec60f`)
- `master:MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_PACKAGES_712_T2_ACCEPTANCE_2026-08-17.md`
  (commit `887ec60f`)
- `feature/wayfinder-gap-audit-20260823:MTC_COMMAND_CENTER/11_TRIAGE/WAYFINDER_MACRO_GAP_AUDIT_2026-08-23.md`
  (commit `6888b416`)
