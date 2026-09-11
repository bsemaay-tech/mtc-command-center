# Supplemental Read-Only Corroboration Review: P012 R34 Price-Only Correction

- **Reviewer**: Gemini (Supplemental Read-Only Corroborator)
- **Target Repository**: `C:\LAB\Tradingview_LAB_CLEAN` (Read-only inspection; watched foreign checkout `current-20260829` @ `108ea066` not conflated with candidate)
- **Frozen Packet Context**:
  - Manifest SHA256: `2f4ac4a45f3511a4dadb7426e2007b687284474bf95bd24f4ea123d1c7b480b8`
  - Candidate HEAD: `3faed08866e122158e93c626288873ec58a42e3d`
  - Diff Base: `3e86faec032407c1af9a75f8b8852222d732f316`
  - Reviewed Ancestor: `b7975ae6c935c461c479768c5f252f930fbc1800`
  - Ratified Successor Receipt SHA256: `cf82b102ba866fa08a86d8a6cb52ed43c2e2f2b71e35b081304e09e5aa368f11`
  - Design Authority: v1.27 (`12943ca7ba1e276188ff332cea8eb87b7ca46e3ab60579437311d951e9b8a195`), Section 24
- **Reviewer Execution Status**: `SUPPLEMENTAL_UNEXECUTED` (All execution data, including Lead candidate full-gate 558 pass and focused 113 pass, is recorded strictly as context; this corroboration does not substitute for independent Opus 5 / Sol xhigh executions, Lead reconciliation, or Python 3.12 CI).

---

## 1. Price Alignment Contract & Implementation Corroboration

### A. Policy Schema & Validation (`C/mtc_v2/core/rounding.py`)
- **Schema & Strict Construction** ([`rounding.py:13-55`](file:///C:/LAB/Tradingview_LAB_CLEAN/C/mtc_v2/core/rounding.py#L13-L55)): `PriceAlignmentPolicy` is an immutable frozen dataclass with slots requiring exact types and expected values for all six fields: `id="HYPERLIQUID_PX_V1"`, `significant_figures=5`, `perp_max_decimals=6`, `size_decimals=5`, `integer_exception=True`, `positive_price_required=True`.
- **Field & Type Fencing**: `PriceAlignmentPolicy.__post_init__` verifies `type(actual) is type(expected_value)` and value equality, rejecting boolean-for-int or altered numeric values. `PriceAlignmentPolicy.from_mapping` rejects extra or missing keys via strict set equality.

### B. Integer Exactness & Domain Partitioning ([`rounding.py:57-118`](file:///C:/LAB/Tradingview_LAB_CLEAN/C/mtc_v2/core/rounding.py#L57-L118))
- **Positive Python `int` Path**: Handled via `isinstance(value, int) and not isinstance(value, bool)` in both `is_valid_price` and `align_price_to_policy`. Subclasses of `int` (e.g. `PriceInt(int)`) are properly supported, correcting the earlier rejected A1 exact-type limitation, while `bool` is strictly excluded.
- **Arbitrary Precision**: Positive integers (including `2**53 + 1`, `10**400`, `10**5000`) return the exact `int` instance without precision degradation or float conversion.
- **Non-Integer Price Domain**: Non-integer prices are validated against $\{k/10 \mid 1 \le k \le 99999\} \cup \{\text{integers} \ge 10000\}$. Below $10000$, non-integers require $scaled = decimal\_value \times 10$ to be integral.

### C. Alignment Directions & Boundary Semantics ([`rounding.py:84-118`](file:///C:/LAB/Tradingview_LAB_CLEAN/C/mtc_v2/core/rounding.py#L84-L118))
- `CEIL`: Returns the least valid price $\ge x$ (e.g., $0.01 \to 0.1$, $12345.6 \to 12346.0$).
- `FLOOR`: Returns the greatest valid price $\le x$. If $x < 0.1$, `lower is None` and raises `ValueError("price has no positive valid floor")`.
- `HALF_UP`: Nearest valid price with exact ties broken to the larger value (e.g., $1000.05 \to 1000.1$, $9999.95 \to 10000.0$). For $0 < x < 0.1$, returns $0.1$.
- **Refusals**: `bool`, nonpositive values ($\le 0$), and nonfinite floats (`inf`, `-inf`, `nan`) fail membership and raise `ValueError` on alignment.

---

## 2. Consumer Dispatch & Seams

### A. Instrument Record & Metadata Seams ([`instrument.py:178-395`](file:///C:/LAB/Tradingview_LAB_CLEAN/C/mtc_v2/core/instrument.py#L178-L395))
- **Mutual Exclusivity**: `InstrumentRecord` and `InstrumentMetadata` enforce that exactly one of `price_tick` or `price_alignment_policy` is set.
- **Legacy Behavior Intact**: When `price_tick` is provided and `price_alignment_policy` is `None`, legacy scalar rounding methods (`floor_price`, `ceil_price`, `round_price`) dispatch directly to `floor_to_grid`, `ceil_to_grid`, and `round_half_up_to_grid`.
- **Refusal Preservation**: `HYPERLIQUID-BTC-PERP-V1.3.json` maintains `minimum_quantity: null`, `minimum_notional: 10`, and `provenance.human_reviewer: null`, preserving all production admission fences.

### B. Execution, Exits, and Runner Integration
- **Economics**: `_fill_price` in [`economics.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/C/mtc_v2/core/economics.py) respects instrument policy alignment directions (`CEIL` for buys, `FLOOR` for sells).
- **Exits**: `_align_price` in [`exits.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/C/mtc_v2/core/exits.py#L185-L225) dispatches to `align_price_to_policy` when policy is present, ensuring `align_stop_price` (long=`FLOOR`, short=`CEIL`), `calc_sl`, `build_working_exit_book` (target=`HALF_UP`), and `update_protective_stop_owner` (trailing / break-even stops) consume typed policy rules correctly.
- **Runner**: [`runner.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/C/mtc_v2/core/runner.py#L597-L1941) propagates `price_alignment_policy=self.instrument.price_alignment_policy` through all stop, exit, and target constructor invocations.

---

## 3. Governance, Ratification & Section 16 Binding

1. **Owner Contextual Ratification**:
   - Owner approval ("ı approve continue" in `S16/OWNER_APPROVAL.md`) ratifies the prepared receipt chain through `#34` and the specific successor receipt SHA256 `cf82b102ba866fa08a86d8a6cb52ed43c2e2f2b71e35b081304e09e5aa368f11` (originating from unratified `26748c7b...`).
   - The approval applies strictly to the bounded price contract. It does not grant full P012 completion, production admission, or trading authority.
2. **Section 16 Status & Succession**:
   - Original Section 16 A2 report's inconsistent `CHANGED` flags remain rejected and preserved.
   - Section 16 A3 extracted report comparator correction is confirmed: all six items remain `ACCEPTED_WITH_RESIDUAL_RISK` and carry forward against prior base `3e86faec...`.
   - The probe-copy tail (8 probe copies, lines 510–990) contains only the required mechanical updates (`kernel/rounding.py` shortcut and tree OID / digest rebinding) without mutating test assertions or instrument records.
   - Lead reconciliation of the historical hunk count typo (167 vs 168 in R32 array; current total 191 hunks = 190 reused + 1 fresh) is acknowledged as a documented non-blocking clarification.
3. **Attestations & Invariants**:
   - `EXPECTED_SEAL_SHA_consumed` is noted as Lead attestation, not runtime driver consumption.
   - All 27 production risks, `NONE_KEEP_REFUSED`, and the no-trading posture remain in effect.

---

## 4. Findings, Nits, and Execution Limitations

- **Material Findings**: None. Code, tests, and diffs faithfully implement the specification in design v1.27 §24.
- **Optional Nits / Documentation Notes**:
  - The historical hunk count discrepancy (167 vs 168) in A3 Item 2 JSON is resolved by Lead reconciliation in `S16/LEAD_RECONCILIATION.md` and does not affect candidate code integrity.
- **Execution Limitations**:
  - This review is strictly `SUPPLEMENTAL_UNEXECUTED`. Full gate and focused test runs were not executed by this agent. Acceptance depends entirely on mandatory independent executions by Opus 5 and Sol xhigh, Lead reconciliation, and green CI on the protected Bridge suite (Python 3.12).

---

## 5. Corroboration Verdict

- **Bounded Scope Verdict**: **PASS-WITH-NITS**
- **Status**: **SUPPLEMENTAL_UNEXECUTED**

GEMINI_READ_ONLY_OK
