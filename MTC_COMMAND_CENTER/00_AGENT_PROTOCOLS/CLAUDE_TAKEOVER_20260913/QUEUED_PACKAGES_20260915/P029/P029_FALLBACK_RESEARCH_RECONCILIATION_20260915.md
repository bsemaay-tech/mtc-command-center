# WP-P0-29 / WP-P0-28 — fallback-venue research pack: Lead reading for DD-05 (2026-09-15 ~13:00Z, Claude Opus 5 Lead 743291)

**Input:** `C:\Users\BarışSemaay\Downloads\deep-research-fallback-venues.md` (owner-run ChatGPT deep research, delivered 2026-09-15 ~13:43 local; 176 lines, 68 320 bytes, sha256 `9f3c2ff62941bfa4…`; archived beside this file and under CT13 `QUEUED_PACKAGES_20260915/P029/CHATGPT_DEEP_RESEARCH_FALLBACK_VENUES_20260915.md`). English, plain URLs, access date 2026-09-15 on every row, VERIFIED / REPORTED / UNKNOWN discipline kept, 35 UNKNOWN rows listed in §F with what would close them. **Evidence class: SECONDARY TOOL OUTPUT** — the Lead has NOT spot-checked these rows yet (the overnight session may fetch 3-4 primary pages: OKX permissions page, Bybit key-permission page, Binance API-key FAQ, Bybit restricted list). Nothing here is accepted; DD-05 stays open until the owner names a candidate and the no-funds rehearsal is designed.

## 1. The comparison the record needs (pack labels; `[!]` = fact that changes our earlier reading)
| Control the custody record wants | OKX | Bybit | Binance (Futures) |
|---|---|---|---|
| Current Terms + date | VERIFIED: 2026-07-24 | UNKNOWN (body not retrievable) | UNKNOWN |
| Contracting entity | VERIFIED: Aux Cayes FinTech Co. Ltd., **Seychelles** (default for users outside listed local providers) | UNKNOWN | UNKNOWN |
| Restricted list (Türkiye named?) | VERIFIED list; Türkiye NOT named | VERIFIED list (§11.3); Türkiye NOT named | UNKNOWN |
| **Türkiye eligibility / local entity** | **UNKNOWN** — OKX TR is a separate Türkiye-facing service; routing global-vs-TR for a Türkiye resident not closed; perps availability on OKX TR not closed | UNKNOWN (regional redirect at registration) | UNKNOWN (Binance TR separate; TRY pairs moved to Binance TR 2025-10) |
| KYC before API/withdraw | VERIFIED required | VERIFIED "Standard" mandatory | VERIFIED required |
| Trade-only API key (no withdraw) | VERIFIED Read/Trade/Withdraw — `[!]` **`Trade` includes "funding transfer"** (internal moves between the account's wallets/sub-accounts), so a trade key is withdrawal-free but not transfer-free | VERIFIED — finest scoping: `ContractTrade` separate from `Wallet` (`AccountTransfer`, `SubMemberTransfer`, `Withdraw`) → trading without any transfer | partially VERIFIED: reading / withdraw / futures separately controlled; full matrix UNKNOWN |
| IP allow-list per key | VERIFIED up to 20 IPs (recommended, not mandatory) | binding field exists; max UNKNOWN | mandatory for withdraw permission; unrestricted keys are read-only; max UNKNOWN |
| Key expiry hygiene | VERIFIED 14-day inactivity expiry for unbound trade/withdraw keys | VERIFIED unbound keys invalid after 90 days (7 days after a password change) | UNKNOWN (no stated rotation) |
| Sub-accounts | VERIFIED 5 (Standard); OKX TR says 10 | VERIFIED 5 (20 VIP/business); key bound to a sub-uid at creation | VERIFIED 5 (regular); 30 keys per sub-account |
| Withdrawal whitelist / lock | allowlist + 24 h new-address lock VERIFIED; all-withdrawals switch UNKNOWN | whitelist, daily limit, new-address lock, "app-only withdrawals" VERIFIED; all-withdrawals switch UNKNOWN | whitelist + **Withdraw Protection** (block all on-chain withdrawals 1-7 days) VERIFIED |
| Demo / testnet with API keys | VERIFIED demo keys (exempt from expiry) | VERIFIED separate demo account + keys (`api-demo.bybit.com`) | VERIFIED Futures Demo Trading + demo API key |
| Official Python client | python-okx exists; no GitHub releases → UNKNOWN version | VERIFIED pybit 5.16.0 (2026-04-18), MIT | connector repo exists; no releases → UNKNOWN version |
| History exports (DD-04 analogue) | VERIFIED API archive endpoints (bills since 2021-02; fills; orders 3 months) with stated rate limits; UI statements 2 years; format text UNKNOWN | VERIFIED CSV/PDF exports (up to 2-5 years by dataset, 50/month) + V5 2-year history APIs | UI order-history export; full API set + retention UNKNOWN |
| Status page / machine feed | VERIFIED page + `GET /api/v5/system/status` + WS `status` channel | UNKNOWN | UNKNOWN |
| Incidents (24 months) | UNKNOWN (no archive captured) | `[!]` VERIFIED **2025-02-21 cold-wallet compromise, $1.46bn** (custody incident; withdrawals continued) | VERIFIED five order/market-data incidents of 18-66 min; uptime reports 99.97-99.98 % |
| Regulator / enforcement (24 months) | `[!]` VERIFIED **DOJ/SDNY 2025-02-24: Aux Cayes d/b/a OKX pleaded guilty (unlicensed money transmitting), >$504m penalties** | VERIFIED Malaysia SC administrative action 2024-12-11 (unregistered) | VERIFIED SEC civil action dismissed with prejudice 2025-05-29 |
| Proof of reserves | zk-STARK files, 46th report Aug 2026; auditor/cadence UNKNOWN | PoR + Hacken report after the incident; cadence UNKNOWN | PoR page; cadence/auditor UNKNOWN |
| Insurance/protection fund | OKX TR fund VERIFIED; global entity UNKNOWN | VERIFIED | VERIFIED (not insurance) |
| Scale (CoinGecko snapshot, REPORTED) | $16.9bn / OI $7.2bn | ~$10.4bn / OI ~$10.5bn | $42.9bn / OI $32.2bn |

## 2. Lead reading (comparison only; the choice is the owner's)
- **All three fail the same gate:** whether a Türkiye resident may trade perpetuals, and under which entity/terms, is UNKNOWN for each. No fallback can be "accepted" (DD-05 wording) until that is closed — by reading the local entity's terms (OKX TR / Binance TR / Bybit regional) — an owner-side read, no account needed.
- **OKX** — strongest on the operational controls the record wants (machine-readable status, archive exports, demo keys, 20-IP allow-list, forced key hygiene). Two facts to write down against it: the `Trade` permission carries internal funding transfers (mitigation: sub-account-bound keys + withdrawal allowlist + new-address lock), and the 2025 DOJ guilty plea (an AML/licensing matter, not a loss of client funds).
- **Bybit** — the cleanest key scoping (trade without any transfer) and the best documented exports/SDK; its 2025 $1.46bn cold-wallet compromise is the one custody incident in the set — relevant precisely because a fallback venue would hold our funds during a Hyperliquid outage; users were kept whole per the venue's timeline.
- **Binance** — largest and the only one publishing uptime/incident reports; strongest withdrawal lock (Withdraw Protection); but its legal facts are UNKNOWN across the board here and Türkiye users are steered to Binance TR.
- The earlier reading ("OKX best-documented") stands, with the two OKX caveats now recorded. A reasonable record: **OKX as the primary fallback candidate, Bybit as the second**, both carrying "Türkiye eligibility UNKNOWN — to be read from the local terms before any account is opened".

## 3. What happens next (no venue action of any kind)
1. Owner names the candidate(s) for DD-05 (or "none yet").
2. Lead folds §1 into the venue due-diligence addendum §D on the docs branch and drafts the P0-28 fallback spec v1 (virtual-book fallback + named-venue controls + the no-funds rehearsal outline).
3. Overnight spot-checks of 3-4 primary rows (permissions pages, restricted lists) to move the pack from SECONDARY to Lead-verified on the rows the record relies on.
4. Türkiye-eligibility read of the named venue's local terms (owner read + Lead capture with hash, as done for Hyperliquid).

Recorded by Claude Opus 5 Lead (743291). No account, credential, wallet or venue action occurred.
