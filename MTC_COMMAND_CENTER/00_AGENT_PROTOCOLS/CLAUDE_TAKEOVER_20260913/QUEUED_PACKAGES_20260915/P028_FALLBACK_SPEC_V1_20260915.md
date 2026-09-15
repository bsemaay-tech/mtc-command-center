# WP-P0-28 / WP-P0-29 — Fallback specification v1 (draft, 2026-09-15 night)

**Status:** DRAFT v1 · documentation only · T2 · prepared by the Claude Opus 5 Lead (session 5, `03c6c8`) as the "fallback spec" the package map names ("accepted before WP-V2B-03 starts"). It supplements — never edits — the accepted `ACCOUNT_BINDING_AND_FALLBACK_SPEC.md` (2026-08-25, merge `6d1136a9`) and the venue due-diligence record + its 2026-09-15 addendum (docs branch `8cf9e960`). Nothing here authorizes an account, credential, wallet, transfer, order, testnet or mainnet action; every number below is quoted from a dated record or marked `[OWNER]` / `UNKNOWN`.

This document has two halves because the plan has two fallbacks: **(A) the binding-mode fallback** inside the primary venue (virtual books instead of sub-accounts — Q6, spec §4), and **(B) the venue fallback** (a named second venue plus a no-funds rehearsal — due-diligence criterion 10 / DD-05).

---

## A. Binding-mode fallback: `VIRTUAL_BOOK` — designated by evidence, not yet activated

### A1. The evidence (2026-09-15 08:31-08:33Z, run `p028-eligibility-20260915-r1`, `OD-20260915-P028-READ-GO-1`)
| Field | Value | Source |
|---|---|---|
| `userRole.role` | `user` (master account) | public Info read, attempt 2, `CAPTURE_OK` / `CAPTURE_VERIFY_OK`, both passes byte-identical on every user-scoped field |
| sub-accounts | **0** (`subAccounts: null`) | same |
| user volume in the 15-day window the API returns | **$91.28** (all on 2026-09-14 = the Path 1 fills) | `userFees.dailyUserVlm`, DERIVED sum |
| venue rule | "Up to 10 sub-accounts can be created after reaching $100,000 in volume" | `hyperliquid-docs/trading/sub-accounts`, read 2026-09-15 |
| Lead reading | **NOT ELIGIBLE (windowed evidence); lifetime volume UNKNOWN** (the API exposes no lifetime figure; the owner declared Sunday's fills his first) | `LEAD_TERMINAL_P028_ELIGIBILITY_r1.md` |
| Evidence class | **NONACCEPTING** — the wrapper `capture_own_account_eligibility.py` is Lead-written and unreviewed (it reuses the reviewed tool `af921d75` for every custody primitive); roster: exact Opus (Wed lane 2 addendum) + exact Sol (Sep 19) + Gemini delta | same |

### A2. Which trigger fired, and what "accepted evidence" means here
Spec §4 lists three triggers; the read speaks to **trigger 1 (volume-gate ineligibility)**. Spec §4 also says "An UNKNOWN is not silently converted into eligibility" and requires *accepted* evidence. Tonight's state is therefore:
- **Designated:** `VIRTUAL_BOOK` is the mode WP-V2B-03 must plan for on this account. Nothing else is consistent with the read.
- **Not activated:** no binding record exists (none may exist before WP-V2B-03 and before this spec is accepted), and the evidence that would satisfy "accepted" is the roster-reviewed capture — row `s` of the venue-fact matrix moves from EXCLUDED to "captured 2026-09-15, NOT ELIGIBLE (windowed), NONACCEPTING" and then to VERIFIED only after the roster.
- **Not a policy change:** Q6 (sub-accounts preferred) stands; the fallback was specified in advance exactly so that this moment needs no re-decision (spec §4 "never selected ad hoc during an incident").

### A3. What WP-V2B-03 receives from this half (parameters; none invented)
| Item | v1 value | Who fixes it |
|---|---|---|
| Binding mode for every risk bucket on this account | `VIRTUAL_BOOK` (spec §2 `binding_mode`), one book per risk bucket; per-strategy books only "where capacity allows" — in virtual mode capacity is an accounting choice, so per-strategy books are permitted **only if** the owner's bucket definitions ask for them | `[OWNER]` via WP-V2B-01's bucket definitions ("the owner's bucket definitions" are a WP-V2B-01 input; none exist yet) |
| Number and names of books | = number of accepted risk buckets; `virtual_book_id` = `vbook-<risk_bucket_id>-v<n>` (proposal; globally unique, never reused per spec §2) | WP-V2B-03 design, on the accepted bucket list |
| Venue account | one master account `0x1E26…AC49` (public address; spec §2 `venue_account_address`); `subaccount_address` absent | fixed by the read |
| Agent wallets | spec §3 requires a dedicated agent wallet per binding; in virtual mode all books sign through the **same** master account, so "dedicated per book" cannot be enforced at the venue — the constraint becomes **one agent wallet per worker identity** (spec §2 `worker_id`), expiry explicit and ≤ 180 days (record row, verified), never a default | WP-P0-29 rotation policy (`[OWNER]` interval) |
| Same-symbol rule, funding/fee/liquidation allocation, reconciliation invariants | spec §6, §7, §8 (VIRTUAL_BOOK) apply unchanged; the one-way / no-hedge venue fact (row verified 2026-08-25) is the reason the same-sign rule exists | already specified; WP-V2B-03 implements and proves |
| Margin mode per symbol | uniform across books sharing a symbol (spec §6 rule 5) because same-asset cross+isolated coexistence is row `j` = UNKNOWN (still UNKNOWN after the 2026-09-15 research) | stays a constraint until row `j` is closed |
| Fee tier to assume in cost models | taker 4.5 bps / maker 1.5 bps, 4 % referral discount (dated 2026-09-15; first owner-attested fee evidence) — for WP-P0-12 C-10 the Q3 "Wait" ruling stands; this spec only points at the number | P0-12 Lead lane |

### A4. Migration path (virtual → sub-accounts), pre-specified so it is never improvised
1. Precondition: a **new** accepted eligibility read shows ≥ $100,000 volume (or sub-accounts already provisioned) — the same tool, a new `run_id`, the same roster path.
2. Owner word to (re)instantiate the preferred topology (Q6 default) — a decision row, not a chat aside.
3. Per spec §4: each virtual binding is **retired** and a `SUBACCOUNT` successor created (`predecessor_binding_id` set); if any book carries open exposure, WP-V2B-10's closed no-orphan menu applies **before** the successor may take new risk. No book is "moved" — exposure is either flat at the switch or dispositioned explicitly.
4. The venue-side steps (creating sub-accounts, approving agent wallets) are the owner's acts (G6/T0), never the model's.
Reverse direction (sub-account → virtual, e.g. a venue restriction appears): the same retire-and-succeed rule; trigger 3.

### A5. What this half does NOT settle (open until named owners act)
- The bucket list and per-bucket capital/limits (WP-V2B-01, owner input) — without them the book count is undefined.
- Whether the owner *wants* to route volume through this account to reach the threshold (a choice with cost; not asked tonight).
- Rows `j` (mixed margin) and `t` (customer IP allow-list) — UNKNOWN; `r` (testnet gate) — UNKNOWN; none blocks virtual mode.

---

## B. Venue fallback: candidate controls, the choice, and the no-funds rehearsal

### B1. Why a second venue is in scope at all
Due-diligence criterion 10 (record 2026-08-25): **"BLOCK: name an acceptable venue/custody fallback and walk a no-funds rehearsal before first mainnet deposit."** Criterion 6 defines when the primary venue would be abandoned (service shutdown; withdrawals unavailable 24 h without an accepted recovery statement; API incompatibility 7 days; unresolved HIGH/CRITICAL compromise 7 days; unacceptable terms/entity; public evidence gone 90 days) and what abandonment means (**DISARM, block new deposits/risk, owner exit review — not automatic transfer or deletion**). The fallback venue therefore exists for **continuity of the research/paper loop and an orderly exit**, not for hot failover of live positions.

### B2. Candidate comparison — the controls the custody record wants (from the owner-run deep research of 2026-09-15, Lead reading `P029_FALLBACK_RESEARCH_RECONCILIATION_20260915.md`; evidence class SECONDARY unless marked Lead-verified)
| Control | OKX | Bybit | Binance (Futures) |
|---|---|---|---|
| Türkiye eligibility / contracting entity for a Türkiye resident | **UNKNOWN** (OKX TR is a separate service; global-vs-TR routing not closed) | UNKNOWN (regional redirect) | UNKNOWN (Binance TR separate) |
| Trade-only API key, no withdrawal | yes — but `Trade` includes internal funding transfers (mitigation: sub-account-bound key + withdrawal allowlist + 24 h new-address lock) | yes — finest scoping (`ContractTrade` separate from every `Wallet` permission) | partial (unrestricted keys read-only; withdraw permission needs an IP list) |
| IP allow-list per key | up to 20 IPs, recommended | field exists; max UNKNOWN | mandatory for withdraw keys; max UNKNOWN |
| Key hygiene | 14-day inactivity expiry for unbound trade/withdraw keys | unbound keys invalid after 90 days | UNKNOWN |
| Sub-accounts | 5 (Standard) | 5 (20 VIP) | 5 (regular) |
| Withdrawal lock | allowlist + 24 h new-address lock | whitelist + daily limit + new-address lock + app-only | whitelist + Withdraw Protection (block all 1-7 days) |
| Demo / testnet keys | demo keys (exempt from expiry) | separate demo account + keys | Futures demo + demo API key |
| History exports (DD-04 analogue) | API archive endpoints (bills since 2021-02; fills; orders 3 months) | CSV/PDF exports 2-5 years + V5 2-year history APIs | UI export; API retention UNKNOWN |
| Status feed | page + `GET /api/v5/system/status` + WS `status` | UNKNOWN | UNKNOWN |
| Incidents / enforcement (24 months) | DOJ/SDNY 2025-02-24 guilty plea (AML/licensing), >$504 m | 2025-02-21 cold-wallet compromise $1.46 bn (users kept whole per venue) | five 18-66 min incidents; SEC action dismissed 2025-05-29 |
**Lead reading (unchanged from the reconciliation):** all three fail the same gate — Türkiye eligibility is UNKNOWN for each; **OKX** strongest on operational controls with two recorded caveats; **Bybit** cleanest key scoping and best exports, one custody incident; **Binance** largest, strongest withdrawal lock, legal facts UNKNOWN. A reasonable record: OKX primary candidate, Bybit second — **the choice is the owner's (DD-05 one-liner, open; default tonight: prepare around OKX without naming it chosen).**

### B3. Acceptance conditions for a named fallback venue (what must be true before DD-05 can read "accepted")
1. **Eligibility closed:** the local entity's terms (OKX TR / Bybit regional / Binance TR) read by the owner and captured by the Lead with a hash, exactly as done for Hyperliquid on 2026-09-15 (`TERMS_CAPTURE_RECORD_20260915.json`); the entity, governing law, restricted-persons clause and perpetuals availability recorded with dates.
2. **Controls verified at the primary source** (not the research pack): the API-permission page, the IP-allow-list page, the withdrawal-lock page and the export page of the named venue re-read by the Lead and quoted (moves the rows from SECONDARY to Lead-verified).
3. **Adapter feasibility, read-only:** the venue's public instrument metadata and account-state shapes mapped onto the Bridge's frozen-metadata and reconciliation vocabulary (WP-P0-04 contracts) on paper — a table, no code — so that "compatible with the accepted adapter design" is a checked claim, not a hope.
4. **No-funds rehearsal walked (B4) and recorded.**
5. **Owner signature** on the DD-05 row with the pointer and date.

### B4. No-funds rehearsal — outline (nothing here runs tonight; every step is a separately worded owner act)
The rehearsal walks the **venue exit procedure** of criterion 10 ("owner DISARM → disposition of open exposure → reconcile → owner-only manual transfer") **with zero funds anywhere**, proving the steps exist and are documented, and records what is NOT proven.
| Step | What is rehearsed | Funds involved | Proof recorded | Known limits (state them, never paper over) |
|---|---|---|---|---|
| R1 DISARM | the Bridge is put in DISARMED and stays there | none | the deployed store state + the owner's command evidence | **the mainnet triple-lock / kill path is inert on schema v4** (`engine.kill()` latches only on v9; deployed store is v4 — 2026-08-28 finding); DISARM is the operator state, not a proven flatten. The rehearsal must say this in its own words. |
| R2 Disposition | the WP-V2B-10 no-orphan menu is walked on paper for a hypothetical open position | none | the written disposition choice per menu item | WP-V2B-10 is not built; the rehearsal proves the *decision path*, not an executed FLATTEN |
| R3 Reconcile | the P0-12 read-only reconciliation route is run against the primary account (as on 2026-09-15 Path 1 capture) | none | capture record, byte-identical passes | already demonstrated once (r1); repeat with a fresh `run_id` |
| R4 Manual transfer | the owner's transfer path (venue → owner wallet → fallback venue) is written step by step with the dwell times (24 h new-address lock etc.) and the addresses' provenance | **none — no transfer is executed**; addresses may be provisioned read-only (a demo/testnet key with zero balance) | the written runbook section + a demo-key read proving API reachability and permission scope | a transfer with real funds is never part of the rehearsal |
| R5 Evidence | criterion 11 preservation list applied to the rehearsal artefacts | none | hashes, dates, record pointers | — |
Rehearsal acceptance: T1 review of the record (Gemini corroboration + one flagship); the DD-05 row then carries the pointer. Anything in R1-R5 that turns out impossible without funds is written as a residual on the row, not omitted.

### B5. What this half does NOT do
Opens no account; requests no key; reads no authenticated endpoint; names no venue as chosen; changes no policy; the Türkiye-eligibility read is the owner's (his residency, his terms).

---

## C. Acceptance checks for this v1 (what a reviewer confirms)
- Half A introduces no new policy: every rule is a citation of spec §2-§9 or of the eligibility read; the mode is "designated, not activated"; the evidence class is stated as NONACCEPTING until the roster; the migration path is retire-and-succeed per §4.
- Half B names the criterion-10 BLOCK verbatim, lists the candidates without choosing, states the Türkiye-eligibility UNKNOWN for all three, and outlines a rehearsal that moves no funds and cites the schema-v4 kill-path limit rather than implying protection.
- No secret, address beyond the public short form, or credential appears.

## D. Files
- This draft: run root `P028_ELIGIBILITY_PACKET_20260915/P028_FALLBACK_SPEC_V1_20260915.md` → CT13 `QUEUED_PACKAGES_20260915/P028_FALLBACK_SPEC_V1_20260915.md`.
- Inputs: `ACCOUNT_BINDING_AND_FALLBACK_SPEC.md` (2026-08-25); `VENUE_DUE_DILIGENCE_RECORD.md` criteria 6, 10, 11; `P028_ELIGIBILITY_CAPTURE_20260915/LEAD_TERMINAL_P028_ELIGIBILITY_r1.md`; `P029_FALLBACK_RESEARCH_RECONCILIATION_20260915.md`; `VENUE_DUE_DILIGENCE_ADDENDUM_2026-09-15.md` (docs branch).
- Next: fold B2 into the venue addendum §D (docs branch; block E of the night); v2 after the owner's DD-05 word and the roster's review of the eligibility wrapper.
