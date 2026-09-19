# Deep research request — Hyperliquid venue due diligence for a custody / treasury policy (public sources only)

I am preparing a custody and treasury due-diligence record for a small, non-institutional operator that intends to run an automated trading bridge against **Hyperliquid** (the decentralized perpetuals exchange, mainnet and its public testnet) through its public API and the official Python SDK (`hyperliquid-python-sdk`). I need a **dated, source-cited fact pack**, not advice. Every statement must come from a primary source (Hyperliquid official documentation, official GitHub repositories, the Hyperliquid Foundation / Hyper Foundation publications, court or regulator documents, the venue's own status or incident channels) or, where no primary source exists, from a clearly labelled secondary source with lower confidence. Do not use my account, any address, or any private data — none is provided and none is needed.

## Ground rules for the answer
1. **Cite every fact** with the URL, the page or section title, and the date you accessed it. Quote the exact sentence for anything that will be treated as a binding fact (terms, restrictions, capabilities). If a fact cannot be established from sources, write **UNKNOWN** and say what you looked for — never guess, never infer from a similar exchange.
2. Separate **VERIFIED (primary source)**, **REPORTED (secondary source)** and **UNKNOWN** in every table.
3. Dates matter: for every policy, term or capability give the version/date of the document and note if it changed in the last 12 months.
4. Keep the answer as **Markdown tables** in the sections below, followed by a short "open questions" list. No narrative essay, no recommendations about trading, position sizing or "whether to use the venue".
5. The answer will be pasted into a repository record by an engineer; write for that use (exact names, exact URLs, exact quotes).

## Section A — DD-01: Terms of service, operating entity, jurisdiction, eligibility
| Item | What I need |
|---|---|
| A1 | The current Terms of Service / user agreement for the Hyperliquid app and API: URL, version or "last updated" date, and the exact clauses on (a) prohibited or restricted jurisdictions/persons, (b) permitted use of the API / automated trading, (c) liability limits and dispute resolution, (d) the right to suspend or delist, (e) any KYC/identity requirement. |
| A2 | Which legal entity or entities publish the interface, run the validator set or the "HyperCore"/"HyperEVM" chain, and the Foundation: names, jurisdictions of incorporation, and the source for each. |
| A3 | Whether the mainnet requires any account approval, whitelist, region check (front-end geo-blocking vs API-level restriction) — quote the exact policy. |
| A4 | Any regulator action, enforcement notice or public legal proceeding involving the venue or its entities (dated, with the document). If none found, say so and list the registers you checked. |

## Section B — DD-02: Dependency and failure map
| Item | What I need |
|---|---|
| B1 | The venue's architecture dependencies an operator relies on: the L1 consensus (validator count, who runs validators, staking/HYPE role), the bridge to Arbitrum for USDC deposits/withdrawals (contract, guardians/validators, withdrawal delay windows), the oracle/mark-price inputs, the public API endpoints (REST/WebSocket) and any documented rate limits. Cite the documentation for each. |
| B2 | Documented failure modes and how the venue handles them: chain halts, bridge pauses, "withdrawals paused" events, API outages, liquidation-engine behavior under extreme moves, auto-deleveraging rules. Cite the docs; list the incidents in Section C. |
| B3 | The official status/announcement channels an operator should monitor (status page, Discord/X handles run by the team, GitHub repos), with URLs, and whether any machine-readable status feed exists. |

## Section C — DD-03: Security history, advisories, governance (last 24 months)
| Item | What I need |
|---|---|
| C1 | A dated list of security incidents, exploits, market-manipulation events, oracle incidents, bridge incidents, chain halts or forced interventions involving Hyperliquid (mainnet), each with: date, what happened, user impact (funds lost/frozen/refunded), the venue's response, and the primary source (post-mortem, official statement) plus the best secondary source. |
| C2 | Any published security audits of the L1, the bridge contracts or the API (auditor, date, scope, URL) and any bug-bounty program (platform, scope, max payout). |
| C3 | Governance: who can change protocol parameters, pause the bridge, delist markets, or freeze accounts; whether validators are permissioned; any documented emergency-power usage and the process (quote the docs). |
| C4 | The official Python SDK: repository, latest release and date, release cadence over the last 12 months, published security policy (or its absence), and any known vulnerability advisories for it or its dependencies. |

## Section D — DD-06 / DD-07: Account-level controls an operator can rely on
| Item | What I need |
|---|---|
| D1 | **API wallets / agent wallets:** what an "agent" (API wallet) key can and cannot do — exact documented capabilities (place/cancel orders, transfers between spot/perp, sub-account transfers, **withdrawals to external addresses**, agent creation). Can an agent key be scoped to *trading only* with withdrawals impossible? Quote the documentation. Note the documented expiry mechanism (max validity, default). |
| D2 | **IP allow-listing:** does the venue offer customer-configurable IP restrictions for API keys or accounts (as centralized exchanges do)? If not, say UNKNOWN/NOT OFFERED with the pages checked. Do not substitute rate limiting for this. |
| D3 | **Sub-accounts:** documented rules for creating sub-accounts (eligibility thresholds such as trading-volume requirements, maximum count, whether they exist on testnet, how transfers between master and sub-accounts work, whether an agent key can act for a sub-account). Quote each rule with its source and date. |
| D4 | **Withdrawal mechanics:** documented withdrawal fee, minimum, delay/dispute window, and any way to *disable* withdrawals at the account level; who can move funds out of an account under each key type. |
| D5 | Same-asset cross-margin and isolated-margin coexistence rules (can one asset be held both cross and isolated in one account?) and any documented margin-mode restrictions. |

## Section E — DD-05: Named fallback venues (comparison only, no recommendation)
| Item | What I need |
|---|---|
| E1 | For three candidate alternative perpetual-futures venues that an operator could switch to if Hyperliquid became unavailable (choose the three with the largest perp volume that offer a public API and a testnet or paper environment), give the same facts as A1 (terms, entity, jurisdiction, eligibility), D1 (API key scoping / withdrawal restriction), D2 (IP allow-listing) and D3 (sub-accounts), in one comparison table with sources. Mark UNKNOWN where you cannot verify. |

## Section F — Open questions
List every item above you could not close with a primary source, what you searched, and what document or venue contact would close it.

Deliver the whole answer as a single Markdown document with the section headings above. Length is not a constraint; completeness and exact citation are.
