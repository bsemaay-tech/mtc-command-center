# WP-P0-29 VEN-C — Venue Due-Diligence Record

**Venue:** Hyperliquid

**Status:** DRAFT FOR OWNER REVIEW AND SIGNATURE · T2 · no authenticated read

**Review date:** 2026-08-25

**Proposed disposition:** **HOLD FOR FIRST MAINNET DEPOSIT.** The documentation package can be signed as an honest HOLD record, but the unresolved blocking criteria and live-gate venue-mapping differences cannot be signed away by this document.

**Hard boundary:** This record uses merged public-source records only. It creates or handles no credential, account access, wallet, deposit, transfer, venue contact or trading action.

## 1. Method and authority

The twelve criteria are adapted from the permanent O-16 acceptance set in brief §13.1a and implemented in the merged [WP-P0-24 append-only dependency ledger](../WP_P0_24_OSS_LEDGER_2026-08-24/DEPENDENCY_LEDGER.md). The venue facts come from the merged [WP-P0-28 verification record](../WP_P0_28_VENUE_FACTS_2026-08-25/VENUE_VERIFICATION_RECORD_2026-08-25.md) and [account-binding specification](../WP_P0_28_VENUE_FACTS_2026-08-25/ACCOUNT_BINDING_AND_FALLBACK_SPEC.md).

WP-P0-24 is cited for the criterion definitions and for its exact `hyperliquid-python-sdk 0.24.0` entry. WP-P0-28 is cited for venue behavior. A software-SDK fact is not treated as proof of venue solvency, custody, governance or account permissions.

Status meanings:

- `PASS`: cited evidence meets this documentation criterion at the review date.
- `PARTIAL`: some evidence exists, but named evidence remains missing.
- `UNKNOWN`: searched/merged sources do not establish the fact.
- `BLOCK`: the gap prevents this record from clearing a first mainnet deposit.
- `N/A`: criterion is inapplicable, with a reason. No criterion is silently dropped.

## 2. Twelve-criterion record

| # | O-16 criterion | Venue-specific evidence and proposed procedure | Status / required closure |
|---:|---|---|---|
| 1 | **Provenance** | WP-P0-28 records canonical Hyperliquid documentation and official `hyperliquid-dex/hyperliquid-python-sdk` sources, all accessed 2026-08-25, with quotes/URLs per claim. WP-P0-24 entry 0007 pins SDK `0.24.0` to commit `2fdb18f…`, PyPI artifact hashes and acquisition path. | **PASS for public documentation and SDK provenance.** This does not prove private account state. |
| 2 | **Licence and integration mode** | Integration mode is venue API plus the existing SDK behind the broker adapter. WP-P0-24 entry 0007 verifies the SDK's MIT licence and exact licence-text hash. The venue's current Terms of Service, governing entity/jurisdiction and the owner's eligibility/acceptance have not been captured by WP-P0-28. | **BLOCK before first mainnet deposit:** owner must complete the separately required one-time ToS/jurisdiction read and record date/version/decision; legal advice is outside this record. |
| 3 | **Dependency and supply chain** | WP-P0-24 entry 0007 records the SDK's 56-package/1,345-hash environment and five declared dependencies. Venue operation also depends on venue infrastructure, chain/L1 behavior, oracle/mark inputs, network access and USDC, but WP-P0-28 did not produce a complete venue dependency/failure map. | **PARTIAL / BLOCK:** accept a dated venue dependency/failure map and named monitoring/fallbacks before funding. |
| 4 | **Vulnerability review** | WP-P0-24 entry 0007 reports zero OSV advisories for SDK `0.24.0` and zero affected packages in its lock on 2026-08-24, explicitly not proof of safety. It found no repository security-policy file exposed for the SDK. No merged record establishes the venue's current security program, bounty, incident history or unresolved venue advisories. | **PARTIAL / BLOCK:** complete a dated primary-source venue security/advisory review and record exposure; a zero SDK result cannot clear the venue. |
| 5 | **Maintainer and activity** | WP-P0-24 entry 0007 observed seven SDK releases in 12 months, one human release-publisher proxy, last push/release 2026-06-04, unknown median security closure time, and no exposed SDK security-policy file. WP-P0-28 does not measure venue operator governance, key-person risk or incident-response performance. | **PARTIAL:** record venue entity/governance and security-response path; single-maintainer SDK proxy remains a named money-adjacent risk. |
| 6 | **Abandonment criteria declared in advance** | Proposed venue-abandonment/exit triggers: official service shutdown; settlement or withdrawals unavailable for **24 continuous hours** without an accepted recovery statement; official API incompatibility with the accepted adapter for **7 calendar days** without a safe path; credible unresolved HIGH/CRITICAL compromise without mitigation for **7 days**; governing terms/entity become unacceptable; or required public evidence disappears for **90 days**. Trigger means DISARM, block new deposits/risk and require owner exit review—not automatic transfer or deletion. | **PASS as a proposed procedure, pending owner signature.** A stricter incident rule wins. |
| 7 | **Update policy** | Owner/Lead refreshes this record every **90 days** and within **1 business day** of a material venue, API, wallet-expiry, IP-policy, terms, stablecoin or security event. WP-P0-24 entry 0007 separately requires monthly/event-driven SDK review and T0 treatment for protected updates unless Gate 1 proves otherwise. No automatic update. | **PASS as a proposed procedure, pending owner signature.** |
| 8 | **Incident response** | [Custody runbook §8.5](CUSTODY_RUNBOOK_DRAFT.md#85-revocation-drill-and-compromise-response) defines auto-DISARM, owner alert, revoke/choose KILL-FLATTEN-venue route, isolate, rotate, preserve evidence and reconcile; no automatic FLATTEN. [Treasury policy §6](TREASURY_POLICY_DRAFT.md#6-usdc-depeg-stance) defines USDC actions. WP-P0-24 entry 0007 says disarm/disable affected adapter or pin known-safe state first. | **PASS as policy design only.** Later implementation and drills remain required. |
| 9 | **Portability and export** | WP-P0-24 entry 0007 requires redacted open JSON protocol evidence and keeps canonical truth outside SDK objects. WP-P0-28 specifies reconciliation sources and public account addresses, but does not prove complete account statements, fills, funding, fees, positions and transfer history can be exported in an independently readable form. | **BLOCK before first mainnet deposit:** demonstrate an unauthenticated fixture or separately authorized account export path and schema sufficient for tax, reconciliation and recovery. No authenticated read is authorized here. |
| 10 | **Replacement and rollback** | WP-P0-24 entry 0007 names a separately audited direct REST/WebSocket client or prior safe SDK lock as software alternatives; package-specific rollback was not walked. No alternate venue is selected. The custody runbook's second-master fallback is same-venue topology, not venue replacement. Proposed venue exit procedure is owner DISARM → disposition of open exposure → reconcile → owner-only manual transfer; it is unwalked. | **BLOCK:** name an acceptable venue/custody fallback and walk a no-funds rehearsal before first mainnet deposit. No migration is authorized here. |
| 11 | **Evidence preservation** | Preserve this record, source URLs/access dates, public account/address metadata, terms/version record, redacted statements, reconciliation, incidents, decisions and drill evidence before retirement. Never preserve credentials or seeds. WP-P0-24 shared control E and criterion 11 require preservation before removal. | **PASS as policy design, pending owner signature.** |
| 12 | **Retirement and removal** | Venue use stops only by separate explicit owner decision. Stopping use does not authorize deletion of evidence, wallets, accounts, adapter code or records. Exact cleanup scope follows accepted reconciliation and criterion 11; no automated deletion. This mirrors WP-P0-24 shared control R and criterion 12. | **PASS as policy design, pending owner signature.** |

## 3. Venue-fact matrix carried from WP-P0-28

| Fact needed by custody/treasury | Merged status | Consequence here |
|---|---|---|
| Custom agent-wallet expiry | **VERIFIED:** explicit expiry supported up to 180 days; default undocumented (row `g`) | Policy must set an explicit expiry; runbook proposes 120 days and rotation by day 90 |
| Agent/subaccount signing model | **VERIFIED** (rows `d`–`f`) | Dedicated signer per bucket/worker is feasible as design, subject to actual slot eligibility |
| Actual subaccount eligibility | **UNKNOWN / ACCOUNT-LEVEL-ONLY / EXCLUDED** (row `s`) | No topology may be instantiated or assumed under this record |
| Testnet subaccount volume-gate behavior | **UNKNOWN** (row `r`) | Testnet procedure cannot assume mainnet parity or exemption |
| Agent-withdrawal restriction | **NOT ESTABLISHED**; binding spec claims no independent agent-withdrawal safety boundary | Treat agent wallet as able to move/endanger all reachable funds; live-gate withdrawal-disabled item remains blocked |
| Customer-configurable IP restriction | **UNKNOWN** (row `t`) | Live-gate IP-restricted item remains blocked; documented rate limiting is not substituted |
| Same-asset cross+isolated coexistence | **UNKNOWN** (row `j`) | Fail closed; do not use it as custody isolation |

## 4. Blocking closure register

No item below is performed or authorized by this draft.

| ID | Closure required before first mainnet deposit | Owner/Lead evidence |
|---|---|---|
| DD-01 | Owner ToS/entity/jurisdiction read and signed decision | `[POINTER / DATE]` |
| DD-02 | Venue dependency/failure map accepted | `[POINTER / DATE]` |
| DD-03 | Dated venue security/advisory/governance review | `[POINTER / DATE]` |
| DD-04 | Independently readable account-history/export path demonstrated under separate authority | `[POINTER / DATE]` |
| DD-05 | Named venue/custody fallback and no-funds rehearsal accepted | `[POINTER / DATE]` |
| DD-06 | Withdrawal-disabled requirement primary-source mapped and permission-proven, or gate formally amended by owner authority | `[POINTER / DATE]` |
| DD-07 | Customer-configurable IP restriction proven and configured, or gate formally amended by owner authority | `[POINTER / DATE]` |
| DD-08 | Custody ceremony and empty-wallet restore drill accepted | `[POINTER / DATE]` |
| DD-09 | Signed treasury amounts and policy in force | `[POINTER / DATE]` |

## 5. Refresh and invalidation

Proposed ordinary refresh: **90 calendar days**. Review within **1 business day** of any security incident, material outage, deposits/withdrawals restriction, terms/entity/jurisdiction change, API or wallet-policy change, SDK advisory, USDC impairment, or evidence contradiction. Any such event invalidates the current review until dispositioned.

The current record expires on **2026-11-23** if not earlier invalidated. Expiry blocks new deposits and new risk; it does not automatically move funds.

## 6. Owner review and signature

By signing, the owner acknowledges the twelve-criterion record and its current **HOLD** disposition. Signature accepts this policy record; it does not clear DD-01–DD-09, authorize a deposit, or declare live readiness.

| Decision | Owner mark |
|---|---|
| Accept the 90-day/event-driven review cadence | `[INITIAL / AMENDMENT]` |
| Accept the abandonment triggers in criterion 6 | `[INITIAL / AMENDMENT]` |
| Accept current disposition: HOLD FOR FIRST MAINNET DEPOSIT | `[INITIAL / AMENDMENT]` |
| Accept DD-01–DD-09 as blocking closure register | `[INITIAL / AMENDMENT]` |

**Owner name:** `[PRINT NAME]`

**Owner signature:** `[SIGNATURE]`

**Signed date/time and timezone:** `[YYYY-MM-DD HH:MM TZ]`

**Review version:** `[VERSION]`

**Amendments, if any:** `[ATTACH SIGNED AMENDMENT; NO SECRETS]`
