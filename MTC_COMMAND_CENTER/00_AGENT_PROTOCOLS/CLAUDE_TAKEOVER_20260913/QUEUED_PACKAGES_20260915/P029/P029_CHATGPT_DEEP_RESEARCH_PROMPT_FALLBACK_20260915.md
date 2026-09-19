# Deep-research prompt — fallback venue comparison for a custody/treasury record (paste into ChatGPT deep research)

Copy everything below the line into ChatGPT (deep research mode). Do not add account names, addresses, balances or any personal data. Save the answer as `deep-research-fallback-venues.md` and tell the Lead the path.

---

You are producing a dated, source-cited fact pack that compares three centralized derivatives venues — **OKX, Binance (Futures), Bybit** — as *fallback venues* for a small, automated, API-driven perpetual-futures operation whose primary venue is Hyperliquid. The fact pack feeds a custody/treasury due-diligence record; it must be honest about what is unknown. It is NOT a recommendation and NOT financial or legal advice.

**Rules**
1. Research cut-off: today; state the date. Access date on every source.
2. **Write in English.** Do not use inline citation markers; give plain URLs (title, URL, document date if published, access date) in a "Source" column.
3. Evidence classes, per cell: **VERIFIED (primary)** = the venue's own official terms, documentation, help centre, API docs, status page or a regulator's register; **REPORTED (secondary)** = reputable third-party report when no primary exists; **UNKNOWN** = not established. Never guess. Never promote a secondary source to VERIFIED. Prefer a short verbatim quote for any binding rule (restricted jurisdictions, permissions, limits).
4. Quote the exact permission names, limits and clause numbers as written on the source page. If a page is region-specific (e.g., OKX has regional entities), say which entity/page you read.
5. Do not open, create or use any account, and do not include any account data.

**Section A — Legal and eligibility (per venue)**
For each venue: the current global Terms of Service URL and its stated "last updated" date; the contracting legal entity named in the terms and its jurisdiction of incorporation; the exact restricted/prohibited jurisdictions clause (verbatim list); whether residents of **Türkiye** are eligible under the current terms and whether a separate local entity/terms applies to Türkiye (quote it); KYC tiers required for API trading and for withdrawals; whether derivatives/perpetuals are available to Türkiye residents; any regulator registration or enforcement action in the last 24 months (name the regulator and the document; UNKNOWN if none found — do not write "none exists").

**Section B — Account and API controls (per venue)**
The API key permission matrix exactly as documented (e.g., Read / Trade / Withdraw / Transfer / sub-account flags); whether a key can be created with trade permission and NO withdrawal or transfer permission; IP allow-list per key (max addresses; whether it is mandatory for trade or withdraw permission; expiry rules for keys without IP binding); API key expiry/rotation rules; sub-account creation rules (count, eligibility) and whether a key can be bound to one sub-account; whether a withdrawal address whitelist and an account-level "disable withdrawals" switch exist; testnet/demo environment (URL, whether it needs a separate account, whether demo API keys exist); the official Python SDK or API client (repo URL, latest release and date, licence).

**Section C — Records and exports (per venue)**
Whether a full, independently readable account history can be exported (trades/fills, funding payments, fees, transfers, positions): the export path (UI and/or API endpoint), formats (CSV/JSON), retention limits (how far back), and rate limits on history endpoints. Quote the endpoint names.

**Section D — Operational reliability (per venue)**
Official status page URL and whether it offers a machine-readable feed (RSS/Atom/JSON); documented API rate limits for orders and account queries; documented maintenance windows; publicly documented incidents/outages in the last 24 months with dates (primary announcements preferred; secondary reports labelled REPORTED); proof-of-reserves publication (URL, cadence, auditor) if any; documented insurance/protection fund for derivatives.

**Section E — Scale (dated)**
For each venue, 24-hour perpetual/derivatives volume and open interest from one named data source with its timestamp (REPORTED), and the venue's own published figures if any (VERIFIED). State clearly that this is a snapshot, not a ranking method.

**Section F — Open questions**
A table of every UNKNOWN cell above with: what was searched, why it did not close, and which document or primary contact would close it.

**Output format**
One table per section with columns: Item | Venue | Status (VERIFIED / REPORTED / UNKNOWN) | Fact (verbatim quote where a rule is binding) | Source (title, URL, document date, access date). Keep it factual and compact; no recommendations, no scores, no "best" language.
