# Supplemental Independent Detection Audit: P012 Path 1 Real-Capture Packet (2026-09-14)

- **Reviewer**: Supplemental READ-ONLY Auditor (Gemini 3.8 Flash High)
- **Subject**: [`_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md)
- **Status**: Non-accepting supplemental review. No code edited, no commands run, no network access, read-only repository inspection only.

---

## (a) Citation Verification Table

Every `file:line` citation appearing in the subject document was inspected against the frozen source packet.

| # | Subject Citation | Target File & Line | Content in Source | Audit Result |
|---|---|---|---|---|
| 1 | `REAL_OBSERVATION_INTAKE.md` "Fee package" / "Funding package" (line 6) | [`sources/REAL_OBSERVATION_INTAKE.md:15, 29`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/REAL_OBSERVATION_INTAKE.md#L15-L29) | Section headers: `## Fee package` (L15) and `## Funding package` (L29). | **EQUAL** |
| 2 | `PATH_D_DECISION_PACKET.md:25` (line 6) | [`sources/PATH_D_DECISION_PACKET.md:25`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/PATH_D_DECISION_PACKET.md#L25) | `"Path 1" (self-observation on the owner's own account) is the complement: it supplies real instances for the new rules. It is **not** part of this packet's authority.` | **EQUAL** |
| 3 | `PATH_D_DECISION_SIGNED_20260912.md:11` (line 6) | [`sources/PATH_D_DECISION_SIGNED_20260912.md:11`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/PATH_D_DECISION_SIGNED_20260912.md#L11) | `no deploy/live/TESTNET/mainnet/ARM/order/spend authority; T0 reviews, R29 redo, ratification, CI, protected merge remain.` | **EQUAL** |
| 4 | `constants.MAINNET_API_URL`, `bridge/broker/hyperliquid.py:2180` (line 16) | [`sources/hyperliquid_py_excerpt.md:88`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/hyperliquid_py_excerpt.md#L88) (orig. L2180) | `base_url = constants.TESTNET_API_URL if self.network == "testnet" else constants.MAINNET_API_URL` | **EQUAL** |
| 5 | `03_PRODUCTION_CLOSURE_MATRIX.md:32 row I-3` (line 18) | [`sources/03_PRODUCTION_CLOSURE_MATRIX.md:32`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/03_PRODUCTION_CLOSURE_MATRIX.md#L32) | `\| I-3 \| /minimum_quantity \| null; minimum_notional: 10, quantity_step: 0.00001; no quantity floor \|` | **EQUAL** |
| 6 | `step 0.00001 BTC`, `03_PRODUCTION_CLOSURE_MATRIX.md:32` (line 25) | [`sources/03_PRODUCTION_CLOSURE_MATRIX.md:32`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/03_PRODUCTION_CLOSURE_MATRIX.md#L32) | `quantity_step: 0.00001` | **EQUAL** |
| 7 | `PATH_D_DECISION_PACKET.md:93` (line 28) | [`sources/PATH_D_DECISION_PACKET.md:93`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/PATH_D_DECISION_PACKET.md#L93) | `- **Guard margins:** the estimator (taker 0.00045 / maker 0.00015 [FEE:61]) is computed alongside every admitted bill...` | **EQUAL** |
| 8 | `P012_PRODUCTION_ADMISSION_PACKET.md section 7 item 5` (line 28) | [`sources/P012_PRODUCTION_ADMISSION_PACKET.md:279-283`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/P012_PRODUCTION_ADMISSION_PACKET.md#L279-L283) | `5. Hyperliquid funding cadence is NOT VERIFIED here. The source set used for this packet says settlement cadence is not established...` | **EQUAL** |
| 9 | `REAL_OBSERVATION_INTAKE.md fee package item 4` (line 32) | [`sources/REAL_OBSERVATION_INTAKE.md:24`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/REAL_OBSERVATION_INTAKE.md#L24) | `4. ... Also provide separate authentic evidence of venue origin, account ownership/control, actual order/fill association, and capture completeness.` | **EQUAL** |
| 10 | `bridge/broker/hyperliquid.py:1566-1567, 1887, 1901` (line 38) | [`sources/hyperliquid_py_excerpt.md:10-11, 53, 67`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/hyperliquid_py_excerpt.md#L10-L67) (orig. L1566-1567, 1887, 1901) | L1566: `Info.user_fills_by_time`; L1567: `Info.user_funding_history`; L1887: `method_name="user_fills_by_time"`; L1901: `method_name="user_funding_history"`. | **EQUAL** |
| 11 | `:1579` cap citation (line 38) | [`sources/hyperliquid_py_excerpt.md:22-23`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/hyperliquid_py_excerpt.md#L22-L23) (orig. L1578-1579) | `HL_FILLS_PAGE_LIMIT = 2000` / `"""Documented maximum elements in one ``userFillsByTime`` response."""` (Note: funding history page limit is 500 at orig. L1584, L1904). | **EQUAL** (with note on funding cap) |
| 12 | `export_mtc_funding.py:1-30` (line 39) | [`sources/export_mtc_funding_py_excerpt.md:4-33`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/export_mtc_funding_py_excerpt.md#L4-L33) (orig. L0001-0030) | Describes consumption of a quiescent offline snapshot carrying retained funding payloads (schema v10). | **EQUAL** |
| 13 | `REAL_OBSERVATION_INTAKE.md items 1-5` (line 39) | [`sources/REAL_OBSERVATION_INTAKE.md:19-25`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/REAL_OBSERVATION_INTAKE.md#L19-L25) | Items 1 through 5 of Fee package requirements. | **EQUAL** |
| 14 | `OD-20260914-P020-OPUS6-1` (line 40) | [`sources/DECISIONS_rows_cited.md:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/DECISIONS_rows_cited.md#L1) | Records commitment of the final Opus slot before weekly reset (2026-09-16 20:00Z) to P020 V1.6. | **EQUAL** |
| 15 | `OD-20260914-P012-ADMISSION-Q1` (line 44) | [`sources/DECISIONS_rows_cited.md:2`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/DECISIONS_rows_cited.md#L2) | Owner designates himself as human reviewer for I-4, C-12, F-23, and experienced-human money gate. | **EQUAL** |
| 16 | `B3, owner Q5` (line 29) | [`sources/PATH_D_DECISION_SIGNED_20260912.md:7`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/PATH_D_DECISION_SIGNED_20260912.md#L7), [`sources/DECISIONS_rows_cited.md:6`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/DECISIONS_rows_cited.md#L6) | B3 = B; fee-evidence interval begins at first authenticated fill. | **EQUAL** |
| 17 | `owner Q4` (line 29) | [`sources/DECISIONS_rows_cited.md:5`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/DECISIONS_rows_cited.md#L5) | Funding interval starts at or after 2026-09-12T11:00:00Z. | **EQUAL** |
| 18 | `A1 forward-only` (line 29) | [`sources/PATH_D_DECISION_SIGNED_20260912.md:6`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/PATH_D_DECISION_SIGNED_20260912.md#L6) | A1 = A; forward-only funding settlements. | **EQUAL** |
| 19 | `owner Q3 = WAIT` (line 56) | [`sources/DECISIONS_rows_cited.md:4`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/DECISIONS_rows_cited.md#L4) | Account fee tier unverified / not declared; C-10 keeps blocking. | **EQUAL** |

---

## (b) Numeric Claims and Recomputations Table

Benchmark Price Stated: **BTC ≈ $78,000**

| Item / Claim | Packet Stated Value | Exact Recomputation | Mathematical / Sourcing Consistency |
|---|---|---|---|
| **T1 (Maker Buy size)** | `0.00016 BTC ≈ $12.5` | $0.00016 \times \$78,000 = \$12.48$ | **Consistent** ($12.48 rounds to $12.5; > $10 min notional). |
| **T2 (Taker Buy size)** | `0.00016 BTC ≈ $12.5` | $0.00016 \times \$78,000 = \$12.48$ | **Consistent** ($12.48 rounds to $12.5; > $10 min notional). |
| **T3 (Near-$10 Taker Buy size)** | `0.00013 BTC ≈ $10.1` | $0.00013 \times \$78,000 = \$10.14$ | **Consistent** ($10.14 rounds to $10.1). At step $0.00001$ BTC, $0.00012 \times 78,000 = \$9.36 < \$10$, so $0.00013$ is the exact smallest increment $> \$10$. |
| **Combined Long Position** | `~0.00045 BTC ≈ $35` | $(0.00016 + 0.00016 + 0.00013) = 0.00045\text{ BTC}$<br>$0.00045 \times \$78,000 = \$35.10$ | **Consistent** ($35.10 rounds to $35.1 ≈ $35). |
| **Margin Buffer Claim** | `about $40 of margin at 1x is plenty` | Position $35.10 at 1x isolated requires $35.10 margin. $40 provides $4.90 buffer (~14% price movement buffer). | **Consistent**. |
| **Venue Min Notional & Step** | Min notional `10`, step `0.00001 BTC` | Matches `03_PRODUCTION_CLOSURE_MATRIX.md:32` row I-3. | **Sourced**. |
| **Fee Rates Sourced** | Taker `0.00045`, Maker `0.00015` | Sourced from `PATH_D_DECISION_PACKET.md:93`. | **Sourced**. |
| **Fee Per Trade: T1 (Maker)** | Claimed `about 2–3 cents per fill` | $\$12.48 \times 0.00015 = \$0.001872$ (~**$0.19$ cents**) | **Discrepancy (Overstated)**. Overstated by ~13×. |
| **Fee Per Trade: T2 (Taker)** | Claimed `about 2–3 cents per fill` | $\$12.48 \times 0.00045 = \$0.005616$ (~**$0.56$ cents**) | **Discrepancy (Overstated)**. Overstated by ~4.5×. |
| **Fee Per Trade: T3 (Taker)** | Claimed `about 2–3 cents per fill` | $\$10.14 \times 0.00045 = \$0.004563$ (~**$0.46$ cents**) | **Discrepancy (Overstated)**. Overstated by ~5.5×. |
| **Fee Per Trade: T4 (Taker close)** | Claimed `about 2–3 cents per fill` | $\$35.10 \times 0.00045 = \$0.015795$ (~**$1.58$ cents**) | **Discrepancy (Overstated)**. Overstated by ~1.6×. |
| **Total Session Fees (T1+T2+T3+T4)** | Conflated with per-fill cost | $0.1872¢ + 0.5616¢ + 0.4563¢ + 1.5795¢ =$ **$2.7846$ cents** (~**$2.8$ cents total**) | **Conflation**. The claim of "about 2–3 cents per fill" conflates the *total session fee across all 4 fills* with the per-fill cost. Conservative direction (does not expose owner to unexpected cost). |
| **API Elements Cap** | `2000-element cap, :1579` | `HL_FILLS_PAGE_LIMIT = 2000` (fills); `HL_INFO_PAGE_LIMIT = 500` (funding). | **Sourced for fills**; funding is 500. |
| **Timestamps / Dates** | `2026-09-12T11:00:00Z` (funding lower bound); `2026-09-16 20:00Z` (Opus slot reset) | Matches signed decision, DECISIONS rows cited, and REAL_OBSERVATION_INTAKE. | **Sourced & Consistent**. |

---

## (c) Findings

### [H-01] CORRECTION: Arithmetic conflation of total trading session fees with per-fill fees
- **Severity**: CORRECTION
- **Location**: [`subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md:28`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md#L28)
- **Description**: The subject claims: `Costs: venue fee schedule estimate taker 0.00045 / maker 0.00015 (PATH_D_DECISION_PACKET.md:93, estimate only) → about 2–3 cents per fill; funding a few cents`.
  Recomputing individual fills at BTC = $78,000 shows:
  - T1 (maker $12.48 notional): $0.19 cents ($0.00187)
  - T2 (taker $12.48 notional): $0.56 cents ($0.00562)
  - T3 (taker $10.14 notional): $0.46 cents ($0.00456)
  - T4 (taker close $35.10 notional): $1.58 cents ($0.01580)
  The sum across all four trades is $2.78 cents (~2.8 cents total). Saying "about 2–3 cents per fill" states as a per-fill cost what is actually the aggregate cost of the entire trading session. While economically conservative, it is arithmetically inaccurate.

### [H-02] CORRECTION: Omission of leverage and margin mode verification from Section 2 Preconditions
- **Severity**: CORRECTION
- **Location**: [`subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md:15-18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md#L15-L18)
- **Description**: Section 3 specifies: `leverage 1x; isolated margin`. However, Section 2 ("Preconditions to confirm before any trade (read-only, 5 minutes)") lists only account existence/balance, non-testnet address, and margin adequacy ($40). It omits an explicit verification step that the user's trading interface is set to **1x leverage** and **isolated margin**. Hyperliquid perps frequently default to cross margin and higher leverage (e.g., 20x). For a non-technical owner, failing to verify isolated 1x margin before placing orders introduces the risk of cross-margining the entire account balance rather than capping risk at the stated ~$35.

### [H-03] CORRECTION: Inactionable EIP-191 message signing specification for non-technical owner
- **Severity**: CORRECTION
- **Location**: [`subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md:33`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md#L33)
- **Description**: The ownership proof proposal states: `the owner signs one plain-text message with the account wallet (EIP-191 "personal_sign", no gas, no funds moved; a wallet prompt he approves)`. The standard Hyperliquid web UI (`app.hyperliquid.xyz`) does not provide a generic arbitrary EIP-191 text message signing interface. A non-technical owner cannot execute this step without guidance on what tool or interface to use. Directing the owner to third-party web tools to sign messages carries security/phishing risks unless a secure, reviewed local utility or trusted wallet tool (e.g. MetaMask/Rabby internal sign feature) is specified.

### [H-04] NIT: Unverified external venue assertion regarding hourly funding cadence
- **Severity**: NIT
- **Location**: [`subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md:28`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md#L28)
- **Description**: The subject asserts: `Hyperliquid documents hourly funding; the repository sources leave the cadence NOT VERIFIED (P012_PRODUCTION_ADMISSION_PACKET.md section 7 item 5)`. The packet correctly hedges repository status by placing cadence in Section 8 ("Not verified / open"), but the claim that "Hyperliquid documents hourly funding" is an unsourced external fact not present in the repository evidence (where previous task prompts even assumed 8-hour intervals).

### [H-05] NIT: Element cap citation omits distinct 500-element funding page limit
- **Severity**: NIT
- **Location**: [`subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md:38`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md#L38)
- **Description**: The packet references `refuses on any non-2xx, truncation (the documented 2000-element cap, :1579)`. In [`sources/hyperliquid_py_excerpt.md:22-29, 70`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/hyperliquid_py_excerpt.md#L22-L70), the 2000-element limit (`HL_FILLS_PAGE_LIMIT = 2000`) applies exclusively to `user_fills_by_time`. For `user_funding_history`, the page limit is 500 (`HL_INFO_PAGE_LIMIT = 500`, lines 1584, 1904). The capture tool specification should explicitly acknowledge the 500-element cap for funding pagination.

### [H-06] NIT: Order inventory filtering requirement (4 planned fills vs N=3 fee intake)
- **Severity**: NIT
- **Location**: [`subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md:21-27, 39`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md#L21-L39)
- **Description**: Section 3 outlines four distinct fills: T1 (maker buy), T2 (taker buy), T3 (near-$10 taker buy), and T4 (market sell whole position). The fee package in [`sources/REAL_OBSERVATION_INTAKE.md:17`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914/sources/REAL_OBSERVATION_INTAKE.md#L17) requires `Provide exactly N=3 existing authenticated own-account native-BTC fills`. The capture tool or admission intake declaration must explicitly document which 3 fills (e.g. T1, T2, T3) are declared for the fee package, while designating T4 as closing transaction / auxiliary evidence.

---

## (d) Exact Read Coverage and Continuations

All reads were performed strictly via native `view_file` on files within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_PATH1_PACKET_20260914` (plus canonical `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md` as required by system rules). Window size remained $\le 150$ lines per call.

| # | File Path | Requested / Executed Range | Total Lines | Continuations |
|---|---|---|---|---|
| 1 | `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md` | Lines 1–150 (read 1–64) | 64 | None (completed in 1 call). |
| 2 | `.../P012_PATH1_PACKET_20260914/PACKET_SHA256SUMS.txt` | Lines 1–150 (read 1–10) | 10 | None (completed in 1 call). |
| 3 | `.../P012_PATH1_PACKET_20260914/subject/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md` | Lines 1–150 (read 1–57) | 57 | None (completed in 1 call). |
| 4 | `.../P012_PATH1_PACKET_20260914/sources/REAL_OBSERVATION_INTAKE.md` | Lines 1–48 | 49 | Continued: read lines 48–49 (complete file read). |
| 5 | `.../P012_PATH1_PACKET_20260914/sources/PATH_D_DECISION_SIGNED_20260912.md` | Lines 1–150 (read 1–20) | 20 | None (completed in 1 call). |
| 6 | `.../P012_PATH1_PACKET_20260914/sources/PATH_D_DECISION_PACKET.md` | Lines 20–35 & 85–100 | 258 | Two targeted views covering required ranges 20–30 and 85–100. |
| 7 | `.../P012_PATH1_PACKET_20260914/sources/03_PRODUCTION_CLOSURE_MATRIX.md` | Lines 28–35 | 66 | None (exact required range). |
| 8 | `.../P012_PATH1_PACKET_20260914/sources/P012_PRODUCTION_ADMISSION_PACKET.md` | Lines 260–290 | 291 | None (exact required section 7 range). |
| 9 | `.../P012_PATH1_PACKET_20260914/sources/hyperliquid_py_excerpt.md` | Lines 1–150 (read 1–99) | 99 | None (completed in 1 call; lines carry original numbers). |
| 10 | `.../P012_PATH1_PACKET_20260914/sources/export_mtc_funding_py_excerpt.md` | Lines 1–150 (read 1–44) | 44 | None (completed in 1 call; lines carry original numbers). |
| 11 | `.../P012_PATH1_PACKET_20260914/sources/DECISIONS_rows_cited.md` | Lines 1–150 (read 1–9) | 9 | None (completed in 1 call). |

---

## (e) Nonempty NOT VERIFIED Scope

1. **Owner Mainnet Account Balance & Address**: Only stated in chat by the owner on 2026-09-14 ~14:30Z ("some small real money"); on 2026-09-12 at 11:50Z the balance was recorded as $9.80 (`PATH_D_DECISION_SIGNED_20260912.md:19`). Actual mainnet balance and address remain unverified until inspected on the live venue via public Info API.
2. **Current Live BTC Minimum Notional and Size Step**: Pinned matrix values (minimum notional 10, quantity step 0.00001 BTC) date from 2026-09-11 (`03_PRODUCTION_CLOSURE_MATRIX.md:32`). Live venue values from Hyperliquid `meta` endpoint remain unverified until the session.
3. **Hyperliquid Funding Settlement Cadence**: Settlement cadence is NOT VERIFIED in the repository evidence (`P012_PRODUCTION_ADMISSION_PACKET.md:279`, `PATH_D_DECISION_PACKET.md:250`). Stated "hourly" cadence is an external assertion to be verified from captured data.
4. **Account Fee Tier Applicability**: Account fee tier is unverified (Owner Q3 = WAIT, `DECISIONS_rows_cited.md:4`). Whether referral discount applies at fill charge time is unverified until observed.
5. **Ownership Proof Tooling Acceptance**: Neither the EIP-191 signature method nor the capture tool's adapter interface has been implemented or accepted by T0 reviewers.

---

## (f) Audit Summary and Verdict

- **Hedges**: Maintained honestly in Sections 0, 2, and 8. The packet maintains that balance, cadence, fee tier, and review acceptance are unverified.
- **Authority**: Scrupulously maintained. The packet explicitly keeps `Status: PROPOSAL — nothing here is authorized, executed, accepted or admitted` (line 3) and reiterates that Path D and P012 granted zero trading/mainnet authority.
- **Division of Labour**: Unambiguous textually. The owner alone connects the wallet, clicks Buy/Sell/Confirm, and types passwords. The Lead's role in Chrome is restricted to viewing/advising without touching controls, and code contact is strictly read-only via public Info API.
- **Intake Fit**: Properly addresses N=3 fee requirements and forward funding lower bound (`2026-09-12T11:00:00Z`). Honestly identifies the architectural impedance mismatch between raw captured JSON files and `export_mtc_funding.py`'s Bridge DB schema v10 snapshot requirement.
- **Verdict Rationale**: While mathematically sound in trade sizing and meticulous in source citations, the packet requires three operational corrections before owner execution: (1) correct fee estimate conflation (H-01); (2) mandate an explicit 1x leverage / isolated margin check in Section 2 preconditions to prevent unintended account exposure (H-02); and (3) specify an actionable, safe EIP-191 signing procedure for a non-technical owner (H-03). Therefore, an adversarial audit renders **REQUEST_CHANGES**.

```json
{
  "part": "P012_PATH1_PACKET_GEMINI",
  "verdict": "REQUEST_CHANGES",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "findings": [
    {
      "id": "H-01",
      "severity": "CORRECTION",
      "summary": "Fee schedule estimate of 2-3 cents per fill conflates total session fees across 4 trades with per-fill cost."
    },
    {
      "id": "H-02",
      "severity": "CORRECTION",
      "summary": "Section 2 Preconditions omits verifying 1x leverage and isolated margin on the UI, risking cross-margin exposure."
    },
    {
      "id": "H-03",
      "severity": "CORRECTION",
      "summary": "EIP-191 personal_sign proposal is inactionable for non-technical owner because Hyperliquid UI lacks an arbitrary message signing tool."
    },
    {
      "id": "H-04",
      "severity": "NIT",
      "summary": "Assertion that Hyperliquid documents hourly funding is an external venue fact not cited from repository sources."
    },
    {
      "id": "H-05",
      "severity": "NIT",
      "summary": "Citation of 2000-element cap refers strictly to fills; funding history page limit is 500."
    },
    {
      "id": "H-06",
      "severity": "NIT",
      "summary": "Four trades are planned, requiring explicit filtering/selection to satisfy the exact N=3 fee intake declaration."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
