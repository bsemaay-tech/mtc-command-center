# WP-P0-29 VEN-C — Venue Due-Diligence Record, dated addendum 2026-09-15 (T2; for owner acceptance)

**Status:** DRAFT ADDENDUM · T2 · public sources only · no authenticated read · NOT signed. It amends nothing in the signed record of 2026-08-25; it supplies dated evidence for the owner's later closure decisions on DD-01, DD-02, DD-03 and DD-05, and confirms DD-06/DD-07 stay BLOCK.

**Sources and their classes**
- `[P]` the venue's public documentation pages, read on 2026-09-15 by the Lead (Claude Opus 5, session 743291) — the rendered Terms of Use (`https://app.hyperliquid.xyz/terms`, "Last updated on June 15, 2026", 33 520 characters, sha256 `28df55bf91a77c7e2a9e9c115ffeca1bc4d10b4d35cfec54aa2fa54309c034bb`), `hyperliquid-docs/trading/sub-accounts`, `hyperliquid-docs/for-developers/api/exchange-endpoint`, `github.com/hyperliquid-dex/hyperliquid-python-sdk/releases`.
- `[R]` the owner-run ChatGPT deep-research fact pack of 2026-09-15 (archived in the takeover records as `QUEUED_PACKAGES_20260915/P029/CHATGPT_DEEP_RESEARCH_OUTPUT_20260915.md`; each row names its primary URL and access date; one row — "SDK version 0.1.6" — was found WRONG and is not carried). `[R]` rows are the pack's claims labelled by the pack itself (VERIFIED with a primary URL / REPORTED secondary / UNKNOWN); they are not the Lead's readings unless marked `[P]`.
- Reconciliation: `00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/QUEUED_PACKAGES_20260915/P029/P029_RESEARCH_RECONCILIATION_20260915.md`.

## A. DD-01 — Terms of Use, entity, jurisdiction, eligibility (`[P]` unless marked)
**Closure (2026-09-15):** the owner read the Terms and restated the five facts (14:41Z, `OD-20260915-P029-DD01-READ-1`) and gave the register's decision word "proceed to the next gate" (18:25Z, `OD-20260915-P029-DD01-PROCEED-1`); the register's DD-01 closure pointer is filled on the takeover branch. The record's disposition HOLD FOR FIRST MAINNET DEPOSIT is unchanged — DD-02..DD-09 remain, DD-06/DD-07 BLOCK.

| Fact | Reading (verbatim where quoted) | Record effect |
|---|---|---|
| Interface publisher | "The Interface is made available by **Hyperliquid Corp.** ("Company", "we", "us" or "our")." | Contracting counterparty for the web interface named. Jurisdiction of incorporation: **not stated** in the Terms → UNKNOWN (separate registry item). |
| Scope of the counterparty | §1.1 "The Company does not own, control, or operate Hyperliquid"; §1.2 "The Company is solely a provider of the Interface." | The chain/API has no contracting entity in this document; SDK/API use is not "the Interface". |
| Regulatory status | §1.3 "Neither the Interface nor Hyperliquid are licensed, approved, authorized, endorsed, or registered by any governmental authority or regulatory body in any jurisdiction." | Record as an unregulated venue. |
| Restricted Persons | §1.6 (a) United States of America or Ontario, Canada; (b) "jurisdictions subject to applicable economic and trade sanctions or export control laws and regulations"; (c) citizens of Restricted Territories regardless of location. §1.9: the user determines lawfulness and must not disguise location (§3.1.5 VPN/proxy prohibition). | No enumerated country list beyond US/Ontario; Türkiye not named. The owner's own determination under §1.9 is part of the DD-01 decision. |
| Automation | §3.1.8 prohibits bots/scripts that "exceed reasonable usage, bypass rate limits, cause denial-of-service conditions, or disrupt" the systems. | Automated trading is not prohibited as such; no affirmative licence sentence exists (`[R]` A1(b) stands). |
| Suspension right | §6.2 "the Company reserves the right to suspend or terminate your participation in any feature on the Interface in its sole discretion" | Interface-level only. |
| Irreversibility | §6.4 "Transactions processed by Hyperliquid are irreversible." | Note for the custody runbook. |
| Changes | §7.2 changes effective on posting; the "last updated" date is revised. | The record's §5 refresh rule must watch this date (currently June 15, 2026). |
| Liability cap | §10.3 "in an amount exceeding **$100.00**" | Record. |
| Law / forum | §11.4 "governed by … the laws of **England and Wales**"; binding arbitration under the **LCIA** rules in London, single arbitrator; §11.2 class-action waiver; §11.3 notice to `support@hyperliquid.zendesk.com` within 30 days; no US court. | Record. |
| Front-end geo-block `[R]` | restricted-jurisdiction page observed by the pack (VERIFIED) | consistent with §1.6. API-level geo enforcement UNKNOWN `[R]`. |
| Enforcement search `[R]` | CFTC / SEC / DOJ / FINRA public searches on 2026-09-15 returned no responsive enforcement document | UNKNOWN, not "none". |

**DD-01 remains the owner's read-and-signed decision.** This section is the evidence; the decision line stays `[POINTER / DATE]` until he gives it.

## B. DD-02 — dependency and failure map (dated 2026-09-15; `[R]` with primary URLs unless marked `[P]`)
| Dependency | Fact (pack label) | Failure mode / unknown |
|---|---|---|
| L1 consensus | HyperBFT (HotStuff-derived); execution split HyperCore (on-chain order books, cancels, trades, liquidations) / HyperEVM (VERIFIED) | chain-halt recovery authority and runbook: UNKNOWN |
| Validator set | permissionless independent validators (VERIFIED); active count: UNKNOWN; 10k HYPE self-delegation, >2/3 stake quorum, jailing by vote, ~90-minute epochs, no automatic slashing (VERIFIED) | quorum honesty assumption; count not published |
| USDC path | **CCTP native minting is now the preferred path; the legacy Arbitrum bridge is deprecated (<10 % of HyperCore USDC)** (VERIFIED) — new since 2026-08-25 | treasury policy deposit path must be re-read from the primary page before any deposit decision |
| Legacy bridge | contract `0x2df1c51e09aecf9cacb7bc98cb1742757f163df7`, source `Bridge2.sol`; deposit minimum 5 USDC; withdrawal needs the user wallet signature, arrival 3-4 min (VERIFIED) | signer threshold, guardian set, dispute window, pause authority: UNKNOWN |
| Oracle | validators publish spot oracle prices ~every 3 s from 8 CEX sources (weighted median), final = stake-weighted median (VERIFIED) | CEX outages / manipulation feed through; no operator control |
| API | REST `POST https://api.hyperliquid.xyz/exchange`; WS `wss://api.hyperliquid.xyz/ws`; rate limits: 1200 weight/min per IP; WS 10 connections, 1000 subscriptions, 2000 msgs/min, 100 inflight POSTs; address buffer 10 000 actions then ~1 request per 1 USDC traded (VERIFIED) | "Disconnection from API servers may happen periodically and without announcement" (VERIFIED) — reconnect + snapshot required |
| Liquidation / ADL | maintenance margin = half of initial at max leverage; market close then backstop at 2/3; ADL ranks counterparties by PnL and leverage (VERIFIED) | — |
| Channels | hyperfoundation.org, X @HyperliquidX / @HyperFND, Telegram announcements, Discord `open-ticket` (VERIFIED) | **no status page or machine-readable status feed found** (UNKNOWN) |
| SDK `[P]` | `hyperliquid-python-sdk` releases 0.18.0 (2025-08-12) … 0.24.0 (2026-06-04): seven in twelve months — agrees with WP-P0-24 entry 0007 | the pack's "0.1.6" row was wrong; not carried |

## C. DD-03 — security, advisories, governance (24-month window 2024-09-15 → 2026-09-15; `[R]`)
| Item | Fact (pack label) | Gap |
|---|---|---|
| Incident archive | none central; announcements via X/Telegram | inventory below is NOT exhaustive |
| JELLY (March 2025) | no primary record retrieved → UNKNOWN in the pack | primary post-mortem still needed |
| API outage (July 2025) | no primary record retrieved → UNKNOWN | same |
| POPCAT (2025-11-12) | REPORTED (secondary): HLP ~$4.9m net loss; brief bridge pause; no user-fund loss reported | primary post-mortem needed |
| Insider allegation (Dec 2025) | REPORTED (secondary); not a chain exploit | — |
| Audits | bridge contract audited by Zellic — two PDFs listed (2308 first, 2312 final) (VERIFIED existence) | PDF contents, dates, scope, remediation NOT analysed; L1 / API audits: UNKNOWN |
| Bug bounty | run by Hyper Foundation; Critical "<1M USDC"; KYC/KYB required (VERIFIED) | — |
| Governance | validator jailing by vote; HIP-3 deployer slashing by stake-weighted vote (VERIFIED); general protocol-upgrade/parameter authority, bridge-pause and account-freeze authority: UNKNOWN | no explicit "cannot freeze accounts" invariant found |

**DD-03 consequence:** a dated review with named gaps, not a complete one. Acceptable to the owner only as "dated partial review; gaps listed"; the two missing primary incident records are the next research item.

## D. DD-05 — fallback venue comparison (`[R]`; comparison only, no recommendation is a policy act)
| Venue | Trade-only key | IP allow-list | Sub-accounts | Test env | Legal facts |
|---|---|---|---|---|---|
| OKX | Read / Trade / Withdraw permissions (VERIFIED) | up to 20 IPs per key (VERIFIED); keys with trade/withdraw and no IP binding expire after 14 days' inactivity | key bound to a sub-account (VERIFIED) | demo-trading keys (VERIFIED) | contracting entity / jurisdiction UNKNOWN |
| Binance | permissioned keys (`TRADE`) (VERIFIED partial) | UNKNOWN | UNKNOWN | futures testnet UNKNOWN in the pack | UNKNOWN |
| Bybit | key creation documented (48-hour post-registration restriction) (VERIFIED) | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
The pack states this is a candidate set, not a volume ranking. The Lead's reading for the owner's choice: OKX is the only candidate whose controls match this record's DD-06/DD-07 wants in documentation.

### D2. Second pass — the owner-run fallback-venue deep research of 2026-09-15 (`[R]`; reconciliation `QUEUED_PACKAGES_20260915/P029/P029_FALLBACK_RESEARCH_RECONCILIATION_20260915.md`; `[!]` = changes an earlier reading)
| Control the record wants | OKX | Bybit | Binance (Futures) |
|---|---|---|---|
| Current Terms + date | VERIFIED 2026-07-24 | UNKNOWN (body not retrievable) | UNKNOWN |
| Contracting entity | VERIFIED Aux Cayes FinTech Co. Ltd., Seychelles (default for users outside listed local providers) | UNKNOWN | UNKNOWN |
| Restricted list names Türkiye? | VERIFIED list; not named | VERIFIED list (§11.3); not named | UNKNOWN |
| **Türkiye eligibility / local entity** | **UNKNOWN** — OKX TR is a separate service; global-vs-TR routing for a Türkiye resident not closed | UNKNOWN (regional redirect) | UNKNOWN (Binance TR separate; TRY pairs moved 2025-10) |
| KYC before API / withdraw | VERIFIED required | VERIFIED "Standard" mandatory | VERIFIED required |
| Trade-only key (no withdraw) | VERIFIED — `[!]` `Trade` includes internal funding transfers between the account's wallets/sub-accounts | VERIFIED — finest scoping (`ContractTrade` separate from every `Wallet` permission) | partial — unrestricted keys read-only; withdraw permission needs an IP list |
| IP allow-list per key | VERIFIED up to 20 IPs (recommended) | field exists; max UNKNOWN | mandatory for withdraw keys; max UNKNOWN |
| Key expiry hygiene | VERIFIED 14-day inactivity expiry for unbound trade/withdraw keys | VERIFIED unbound keys invalid after 90 days (7 after a password change) | UNKNOWN |
| Sub-accounts | VERIFIED 5 (Standard); OKX TR 10 | VERIFIED 5 (20 VIP/business); key bound at creation | VERIFIED 5 (regular); 30 keys per sub-account |
| Withdrawal whitelist / lock | allowlist + 24 h new-address lock VERIFIED | whitelist, daily limit, new-address lock, app-only withdrawals VERIFIED | whitelist + Withdraw Protection (block all 1-7 days) VERIFIED |
| Demo / testnet keys | VERIFIED demo keys (exempt from expiry) | VERIFIED separate demo account + keys | VERIFIED Futures demo + demo API key |
| Official Python client | python-okx; release version UNKNOWN | VERIFIED pybit 5.16.0 (2026-04-18), MIT | connector repo; version UNKNOWN |
| History exports (DD-04 analogue) | VERIFIED API archive endpoints (bills since 2021-02; fills; orders 3 months) | VERIFIED CSV/PDF exports 2-5 years + V5 2-year APIs | UI export; API retention UNKNOWN |
| Status page / machine feed | VERIFIED page + `GET /api/v5/system/status` + WS `status` | UNKNOWN | UNKNOWN |
| Incidents (24 months) | UNKNOWN (no archive captured) | `[!]` VERIFIED 2025-02-21 cold-wallet compromise, $1.46 bn (withdrawals continued; users kept whole per the venue) | VERIFIED five order/market-data incidents of 18-66 min; uptime 99.97-99.98 % |
| Regulator / enforcement (24 months) | `[!]` VERIFIED DOJ/SDNY 2025-02-24 guilty plea (unlicensed money transmitting), >$504 m | VERIFIED Malaysia SC action 2024-12-11 | VERIFIED SEC civil action dismissed 2025-05-29 |
| Proof of reserves | zk-STARK files, 46th report Aug 2026; auditor/cadence UNKNOWN | PoR + Hacken report after the incident; cadence UNKNOWN | PoR page; cadence/auditor UNKNOWN |
| Scale (CoinGecko, REPORTED) | $16.9 bn / OI $7.2 bn | ~$10.4 bn / OI ~$10.5 bn | $42.9 bn / OI $32.2 bn |

Lead reading (comparison only; the choice is the owner's DD-05 one-liner): all three fail the same gate — Türkiye eligibility is UNKNOWN for each and must be read from the local entity's terms before any account is opened; **OKX** is strongest on the operational controls this record wants, now with two recorded caveats (`Trade` carries internal transfers — mitigated by sub-account-bound keys + withdrawal allowlist + new-address lock; the 2025 DOJ plea); **Bybit** has the cleanest key scoping and the best-documented exports/SDK, and the one custody incident in the set; **Binance** is the largest and the only one publishing uptime reports, with legal facts UNKNOWN. A reasonable record: OKX primary candidate, Bybit second. The acceptance conditions for a named fallback and the no-funds rehearsal outline are in the P0-28 fallback specification v1 (`QUEUED_PACKAGES_20260915/P028_FALLBACK_SPEC_V1_20260915.md`).

## E. DD-06 / DD-07 — confirmed undocumented on Hyperliquid (`[R]`, `[P]` for S2)
- Agent (API) wallets: named-agent expiry ≤ 180 days (default UNKNOWN); 1 unnamed + 3 named per account, +2 named per sub-account; nonce window (T−2 d, T+1 d); pruned agents must not be reused (`[P]` exchange-endpoint page). **No sentence prohibits withdrawals by an agent wallet** (`[P]`); "agent cannot withdraw" is secondary-reported only. Legacy `withdraw3` requires the user wallet signature (`[R]` VERIFIED).
- Account-level "disable withdrawals" toggle: NOT DOCUMENTED. Customer-configurable IP allow-list: NOT DOCUMENTED (per-IP rate limits only).
- **DD-06 and DD-07 stay BLOCK**; the only exits remain a primary capability matrix (not found) or a formal owner amendment of the live gate.
- **Testnet falsification probe (evening of 2026-09-15, `[P]` primary, testnet):** under the owner's words "testnet agent-withdraw test: go" (preparation) and "probe steps approved" (execution), the Lead ran `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` once from the KVM2-P4-03 environment with the Bridge's agent key (never a master key) against `api.hyperliquid-testnet.xyz`: run `dd06-testnet-20260915T183321Z-r1` **aborted at its own control arm** — the venue rejected the agent's harmless resting order with `Price must be divisible by tick size` (a script rounding defect, corrected as slice 3 `1af85067`), so **no transfer arm (`withdraw3`, `usdSend`, `spotSend`, `approveAgent`) was exercised and DD-06 gained no evidence either way**; nothing rested, no agent was added, the Bridge stayed DISARMED. S0 of that run did record two pre-existing named agents on the testnet account (`MTC-bridge-test`, `kvm2-bridge`) and a unified-account balance held in spot USDC (perp `accountValue` reads 0.0 for such accounts). A corrected re-run (r2) waits for the owner's word; its outcome semantics are fixed in `QUEUED_PACKAGES_20260915/P029/DD06_TESTNET_PROBE_20260915/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md` §4 (only AUTHORIZATION-class refusals count; mainnet parity is never assumed proven).

## F. Matrix rows (record §3)
`g` unchanged (re-verified); `j`, `r`, `t` unchanged (UNKNOWN / NOT DOCUMENTED); `s` — the owner's own account read of 2026-09-15 (`p028-eligibility-20260915-r1`): NOT ELIGIBLE (0 sub-accounts, windowed volume $91.28) — to be entered after the roster reviews the capture wrapper.

Prepared by the Claude Opus 5 Lead (743291). No credential, key, wallet, deposit, transfer, venue contact or trading action occurred; the browser read a public page without connecting any wallet.
