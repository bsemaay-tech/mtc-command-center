Both commands re-executed with explicit exit codes captured. Review complete — final report below.

---

# T0 OPUS INDEPENDENT REVIEW — P012 price-only successor

**Verdict: PASS-WITH-NITS** (bounded synthetic-only price correction only)

## 1. Exact source and packet under review

| Item | Value | How I verified |
|---|---|---|
| Candidate HEAD | `3faed08866e122158e93c626288873ec58a42e3d` | Gate `expected_source_provenance.observed_build_sha` (INDEPENDENT_DERIVATION, status MATCH); ledger `candidate_head`; all 1360 git-blob entries carry `git_head` = this SHA (single distinct value) |
| Diff base | `3e86faec032407c1af9a75f8b8852222d732f316` | `DIFF.patch` header set, 95 changed paths enumerated |
| Packet manifest | SHA256 `2f4ac4a45f3511a4dadb7426e2007b687284474bf95bd24f4ea123d1c7b480b8` | Recomputed over `PACKET_MANIFEST.sha256` — **exact match** |
| Tracked `mtc_v2` subtree | 1354 files under `C/mtc_v2/` | Counted — **exact match** |
| Worktree | `C:/tmp/P012_PRICE_20260910` | 1360/1360 tracked blobs compared packet↔live |

**Independent byte/identity validation (no borrowed proof):**
- All 1414 ledger entries: packet file SHA256 matches ledger — **0 mismatches**.
- All 1360 git-blob entries: I recomputed the Git blob OID (`sha1("blob <len>\0" + bytes)`) from packet bytes — **0 mismatches**. Packet bytes therefore reproduce the recorded object identities, not merely a re-hash of a copy.
- I recomputed the **core tree OID** myself by rebuilding Git tree objects bottom-up from the 119 `core/` blob OIDs (mode 100644, Git name-sort with `/` suffix for subtrees): `ca57ca5e0487f92e05fa68d8217fdde486877a2c` — **matches** the ledger and the receipt's `reviewed_identities.core_tree_oid`. This independently establishes that the core tree at candidate HEAD is identical to the Section-16 reviewed ancestor's core tree, without trusting a builder attestation.

**Nine identities — verified against actual current bytes (8 of 9 directly):**

| Identity | Receipt `reviewed_identities` | My independent measurement |
|---|---|---|
| `core_tree_oid` | `ca57ca5e…677a2c` | recomputed from blob OIDs — MATCH |
| `expected_seal_sha` | `54f41e72…bedebad` | gate `sealed_producer_identities` — MATCH |
| `implementation_anchor_sha256` | `9b58661e…a389a22f9` | SHA256 of `implementation_anchor.json` — MATCH |
| `catalog_sha256` | `d8b37780…bcd95e02` | SHA256 of `scenario_catalog.json` — MATCH |
| `design_file_sha256` / `design_version` | `12943ca7…e9b8a195` / v1.27 | SHA256 of packet `D/` **and** live design file — MATCH (both) |
| `harness_sha256` | `c78ee467…bf2ffc570` | SHA256 of `verify_bceg.py`, packet and live — MATCH (both) |
| `baseline_manifest_sha256` | `15bab160…d2b74517678` | ledger `B/BASELINE_BYTES_MANIFEST.json` entry — MATCH |
| sealed-member base | `1aab804d3383b87871811560c5fa58b41608a402` | gate `expected_source_provenance.implementation_base_sha` — MATCH |
| `worktree_head_commit` (b797 ancestor) | `b7975ae6c935c461c479768c5f252f930fbc1800` | **not directly verifiable by me** — see §6 |

**Receipt binding:** the installed `tests/corrected_vnext/contracts/semantic_coverage_review.json` hashes to **`cf82b102ba866fa08a86d8a6cb52ed43c2e2f2b71e35b081304e09e5aa368f11`**, byte-identical in packet `C/` and live worktree. `S16/ORIGINAL_UNRATIFIED_RECEIPT.json` hashes to **`26748c7b7e09aa4830f507d023a54e7f7aa570c836e607dd2377bb9f42adf2f6`**. I diffed the two: the delta is **exactly** `"ratified": false → true` and `"signed_at": 2026-09-11T05:05:17+03:00 → 2026-09-11T09:41:16+03:00` — 11 unified-diff lines, no other change. This is precisely the claimed successor delta. Items 1–6 all carry `ACCEPTED_WITH_RESIDUAL_RISK` (6 occurrences), `unresolved_items` is empty, ratification chain runs `#5`…`#34`.

## 2. Commands I personally executed

Executable `C:\Python314\python.exe`, **Python 3.14.2** (tags/v3.14.2:df79316, MSC v.1944 64-bit). Import root `C:\tmp\P012_PRICE_20260910\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\__init__.py` (supervisor `PYTHONPATH`; `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`, `TMP=C:\tmp\P012_R34_OPUS_T0_20260911\scratch`).

**(a) Full gate** — `REVIEW_OUTPUT_ROOT` substituted with `C:/tmp/P012_R34_OPUS_T0_20260911`:
```
C:/Python314/python.exe -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --root C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2 --baseline-root C:/tmp/P012_PRICE_BASELINE34_20260911/CURRENT --output C:/tmp/P012_R34_OPUS_T0_20260911/results/full_gate.json
```
**Exit code 0** (23.77 s). Result file `results/full_gate.json` (74,920 bytes), real.
- `claim_label` = `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`; `acceptance_blockers` = `[]`
- `contract_selftest_suite`: **passed_count 558, failed_count 0, failing_test_ids [], returncode 0**
- scenarios: 17 — 8 `GREEN_SHARED_PROJECTION_EQUAL`, 9 `REFUSED_DECLARED_DIVERGENCE`
- probes: 10 — all `PROBE_DIGEST_MATCH`, all `PROBE_BASE_SCENARIO_REFUSED`, child rc 2 (expected RED semantics)
- `legacy_reproduction` MATCH (17 scenarios / 34 surfaces); `legacy_event_order_map_pin` MATCH; 34 observed artifact pins, committed == live-run SHA256
- `blocked_node_skips` 20, all `BLOCKED-DESIGN-UNENUMERATED` at `/RESULT_SURFACE/metrics`
- `declared_field_validation`: REPORT_ONLY (HIST-2026-0030), refusal_count 5 — see §5

**(b) Four focused tests:**
```
C:/Python314/python.exe -m pytest <…>/selftests/test_price_alignment_policy.py <…>/test_economic_records.py <…>/test_results_corrected.py <…>/test_w285_kernel_remaining.py -q -p no:cacheprovider --basetemp C:/tmp/P012_R34_OPUS_T0_20260911/scratch/pytest-temp
```
**Exit code 0** (1.04 s). **113 passed, 0 failed, 0 skipped, 0 errors.** Confirmed the current selection is 113, not the earlier 97. Evidence: `results/focused_tests.junit.xml` (`tests="113" errors="0" failures="0" skipped="0"`), `results/focused_collect.junit.xml`, and `results/EXECUTION_EXIT_CODES.json` recording both argv vectors and both return codes.

Exit codes were captured through a `subprocess` wrapper because shell redirection and compound commands are denied in my sandbox; the argv vectors in `EXECUTION_EXIT_CODES.json` are the published commands verbatim. Both were also run directly as foreground invocations with the same results. No evidence is borrowed from the Lead or any other reviewer.

## 3. Substantive price-policy review (independently derived expectations)

I derived the domain from the task statement, **not** from the implementation: valid = `{k/10 | 1≤k≤99999}` ∪ `{positive integers ≥ 10000}`; CEIL = least valid ≥ x; FLOOR = greatest valid ≤ x (refuse if none); HALF_UP = nearest, larger on exact tie.

**Counterexample search (my scratch, source untouched):** built an exact-`Decimal` reference model and compared all three directions against `align_price_to_policy` over 200,021 exactly-representable inputs (the 0.001-grid across `(0, 200]` plus targeted boundaries `0.01/0.05/0.09/0.1/0.14/0.15/0.16/9999.85/9999.9/9999.90001/9999.94/9999.95/9999.96/9999.99/10000/10000.4/10000.5/10000.6/10001/123456.789/1e20`). I also asserted every returned value is itself a member of the valid set. **0 mismatches.**

Key behaviors confirmed against `core/rounding.py:83-115`:
- Sub-tenth band: `0 < x < 0.1` → CEIL `0.1`, HALF_UP `0.1`, FLOOR raises `"price has no positive valid floor"` (`rounding.py:101,108-109`). The `lower_units >= 1` guard is what makes FLOOR refuse rather than return `0.0`.
- Grid crossover at 10000: for `x ∈ (9999.9, 10000)` the tenth-grid branch yields `upper = 100000/10 = 10000.0`, the correct next valid member; `9999.95` → FLOOR `9999.9`, CEIL `10000.0`, HALF_UP `10000.0` (tie → larger). Verified identical to my model.
- Tie handling uses `decimal_value - lower >= upper - decimal_value` (`rounding.py:113`), i.e. larger on exact tie — `1234.55 → 1234.6`, `1000.05 → 1000.1`, `10000.5 → 10001`. `42.04 → 42.0` (non-tie, nearest).

**Integer exactness** (`rounding.py:92-95`): probed `1, 5, 9999, 10000, 2**53+1, 10**400, 10**4096+7`, an `int` subclass at `2**53+1` and `7`, and an `IntEnum` member, across all three directions — every result satisfied `r == v`, `type(r) is type(v)`, **and `r is v`** (identity preserved). This is the corrected integer implementation; the rejected A1 "exact-type" variant would have broken exactly these subclass cases. Policy and direction validation run **before** the integer fast path (`rounding.py:88-91` precede `:92`), and I confirmed a malformed policy or bad direction still raises for integer inputs — no bypass.

**Refusals preserved — 0 violations across all probes:**
- Nonpositive: `0, -1, -10000, 0.0, -0.5`, and `int`-subclass `0`/`-3` → `ValueError` in all three directions.
- Bool: `True` refused (`isinstance(value, bool)` guard at `rounding.py:58,69,92`); `is_valid_price(True)` is `False`.
- Nonfinite: `nan, inf, -inf` refused (`rounding.py:61-62`).
- Non-Python-number residuals: `'1.0'`, `Decimal('1.0')`, `Fraction(1,2)`, `complex`, `None`, `list` all refused (`rounding.py:58`) — `Decimal` and `Fraction` are deliberately outside the accepted domain.
- Direction: `'floor'`, `'CEILING'`, `''`, `None`, `0`, `'HALF_DOWN'` refused (`rounding.py:90-91`).
- Policy object: `None`, str, bare dict, `object()` refused (`rounding.py:88-89`); `is_valid_price(1.0, None)` is `False`.
- Policy fields (`rounding.py:21-33`): all ten mutations refused, including the `type(actual) is not type(expected_value)` strictness in both directions — `significant_figures=True` refused (bool≠int), `integer_exception=1` refused (int≠bool), `significant_figures=5.0` refused (float≠int), plus wrong-value and `False` cases.
- **Unknown production fields**: `from_mapping` requires `set(raw) == fields` (`rounding.py:45-46`) — an added `admission_status` key is refused, as is a missing key and a non-Mapping argument.

**Direction and dispatch** (not just examples):
- `core/exits.py:185-224`: `align_stop_price` maps `side='long' → FLOOR`, `side='short' → CEIL`, unknown side → `ValueError`. `_align_price` refuses when **both** `price_tick` and `price_alignment_policy` are supplied (`"price_tick conflicts with price_alignment_policy"`) and when **neither** is (`"price alignment is absent"`). TP path dispatches `HALF_UP` (`exits.py:295-302, 314-321`). Verified live: long `9999.94 → 9999.9`, short `9999.94 → 10000.0`, short `0.05 → 0.1`, long `0.05` refuses; conflict and absent both refuse; legacy scalar path unchanged (`1.019/tick 0.01 → 1.01`, `1.011 → 1.02`).
- `core/instrument.py:364-412`: `InstrumentMetadata.__post_init__` enforces XOR of `price_tick`/`price_alignment_policy` and rejects an untyped (dict) policy. `round_price`/`floor_price`/`ceil_price` dispatch to `HALF_UP`/`FLOOR`/`CEIL` under a policy, else the legacy grid. Verified live, including that the legacy default (`price_tick=0.01`, policy `None`) still constructs and still returns `1.005 → 1.01`.
- `core/instrument.py:216-226, 326-340`: record-level XOR refusal (`REFUSED_INCOMPLETE_INSTRUMENT_RECORD`) and loader-level conflict refusal; `price_tick` is only number-validated when non-null, so a null tick no longer forces a refusal while a policy is present.
- `core/runner.py`: five call sites (`:600, :1014, :1568, :1815, :1944`) thread `price_alignment_policy=self.instrument.price_alignment_policy` alongside the existing `price_tick` — additive wiring only, no reordering or arithmetic change.
- **Legacy scalar behavior unchanged**: `round_half_up_to_grid`, `floor_to_grid`, `ceil_to_grid`, `floor_qty_to_step` are untouched (`rounding.py:118-145`) and still refuse non-positive ticks; verified numerically.

**Test strength — not weakened.** The 113 collected IDs cover membership (incl. `9999.95-False`, `10000.1-False`, `inf`, `nan`), integer exactness at `i53`/`i400`/`i5000`, int-subclass at `s53`/`s400`, explicit `test_positive_integer_does_not_bypass_policy_or_direction_validation`, neighbor/direction triples incl. the `9999.95 → 9999.9/10000/10000` crossover and the `1234.55`/`1000.05` ties, `test_no_positive_floor_neighbor_refuses_but_ceil_and_nearest_use_point_one`, six nonpositive/bool/nonfinite refusals, eight constructor field-type refusals, extra-field refusal, metadata and exits dispatch, `test_legacy_scalar_rounding_is_unchanged`, loader `unknown`/`malformed`/`scalar-policy-conflict` refusals, and `test_policy_does_not_admit_other_incomplete_production_facts[minimum-quantity|human-review]`. I edited no source or test and weakened no expectation; my counterexample work lived entirely in my own scratch and, where it overlapped, independently reproduced rather than relaxed these expectations.

## 4. Preserved production boundaries — confirmed

Read directly from `core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json`:
- `price_tick: null` (was already null; `field_basis.price_tick` documents it as RULE-DERIVED, NON-SCALAR)
- `minimum_quantity: null`; `provenance.human_reviewer: null`; `minimum_notional: 10`
- `price_alignment_policy` present with exactly the six supported fields and **no `admission_status`** key
- `status: "PROVISIONAL v1.3 — awaiting owner one-word approval (addendum 15 row 36)"` — still not admitted

Receipt Item 4 retains the **27** production residual risks verbatim (I rows 1–5, C rows 6–12, F rows 13–23, run-manifest 24–27), the R30 Lead restatement reading `oracle_price`/`oracle_price_source` for the old `mark_price` names, `P012_SYNTHETIC_ONLY_NON_PRODUCTION_MILESTONE_V1`, exactly 0 scenarios consuming production records, all ten Section-19 rows OPEN, and the five integration obligations. `NONE_KEEP_REFUSED`, fees/funding/goldens/DERIVATIONS and every production refusal are unchanged. **No production fact is inferred from this synthetic gate success.**

## 5. Material findings

**F1 — `CONTRACT_TABLES_MANIFEST.json` Section-16 metadata is stale (non-blocking, pre-existing, gate-flagged).**
`tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json` → `section_16_review.status` reads `"PENDING"` while its own adjacent `statement` says the review *has* been performed and is installed. The gate itself raises this as `SECTION16_STATUS_CONSISTENT` ("declared='PENDING' while a validating semantic_coverage_review.json is installed"). Beyond the status field, the `statement` is stale in two further respects: it describes the receipt as *"signed 2026-09-08T21:25:22+03:00 by Gemini 3.8 Flash High … ratification recorded through #30"*, whereas the receipt actually installed is signed `2026-09-11T09:41:16+03:00`, reviewer Grok 4.6, chain through `#34`. `status_measured_at` is `2026-09-10T19:57:56Z`, i.e. this predates the successor. Report-only by owner ruling HIST-2026-0030, contributes no acceptance blocker, and touches no price behavior. Correcting it means editing a sealed-manifest field, which is outside this bounded price-only correction — **for Lead tracking, not a change request against this candidate.**

**F2 — four `CHAIN_UNVERIFIABLE` anchor refusals (non-blocking, pre-existing).**
`anchor.base_repin_history.core_tree` transitions `0→1`…`3→4` each record a `new_core_tree_oid_at_base` with no `old_core_tree_oid_at_base`, so the transition is uncheckable in either direction. Report-only; consistent with the Item-1 L14 anchor-ancestry residual already named in the receipt. Unchanged by this successor.

**F3 — four tracked governance files differ between committed bytes and working tree (benign, fully explained).**
`DECISIONS.md`, `09_DOCS/ACCEPTANCE_CRITERIA.md`, `04_REPORTS/ai_handoffs/P012_PRICE_POLICY_PLAN.md`, `00_AGENT_PROTOCOLS/SECTION16_PACKET_STANDARD.md` are byte-different between the packet (= committed blob, LF) and the live worktree (CRLF). I confirmed the difference is **purely line endings**: identical line counts, zero unified-diff lines, and `equal_after_crlf_norm == True` for all four. `.gitattributes` pins `mtc_v2/**/*.{py,json,sha256,patch,md}` to `eol=lf` but leaves these four under plain `* text=auto`, so Windows checkout materialises them CRLF while the blob stays LF — the expected clean state. **No `core/` or `tests/` file is affected**: 1356 of 1360 tracked blobs are byte-identical packet↔worktree, and the four exceptions are documentation outside the gate's hashed surface.

No finding of mine contradicts the preserved A2 rejection or the A3 comparator correction; I did not re-open Section 16 and did not reinterpret the owner approval as semantic evidence.

## 6. Unverified limitations (explicit)

1. **Git was unavailable to me.** Every `git` invocation was permission-denied in this session, so I could not personally run `git status`, `git merge-base`, or `git rev-parse`. Consequently I did **not** independently verify (a) that the worktree is clean, (b) that `b7975ae6…` is an ancestor of `3faed088…`, or (c) that the b797→candidate delta is exactly the three installation paths. **Mitigation:** I recomputed all 1360 blob OIDs and the full `core` tree OID from bytes and got `ca57ca5e…`, matching both the ledger and the receipt — which independently establishes the core-tree-unchanged property that the b797 receipt identity depends on, and the gate independently derived `observed_build_sha = 3faed088…` with `expected_path_change_count 0`. The ancestry *relation* itself rests on the builder's proof, not mine.
2. **Baseline legacy `EXPECTED_SEAL_SHA_consumed` is a Lead attestation.** I verified the seal value `54f41e72…` matches across gate output and receipt; I did **not** verify that the baseline driver consumed the seal. Treated as attestation, not evidence.
3. Section 16 was not repeated; the A2/A3 originals and `LEAD_RECONCILIATION.md` were left untouched and unattributed to any new reviewer.
4. Historical probe bodies were validated by byte/OID identity and by the gate's own probe execution (10/10 `PROBE_DIGEST_MATCH`, base-scenario-refused, rc 2) rather than by wholesale re-reading unchanged probe sources.
5. Mandatory `gemini-3.7-flash-high` corroboration and the second flagship (`gpt-5.6-sol`) are not part of this report and were not run by me.
6. My sandbox denied shell redirection, `cd`-compounds, inline env prefixes, and over-long commands; I worked within it using the tools' native `--output`/`--junit-xml` flags and a `subprocess` wrapper. This affected only *how* evidence files were written, not what was executed — the argv vectors match the published commands.

## 7. Disposition

**PASS-WITH-NITS** for this bounded, synthetic-only, price-only correction.

Both mandatory commands were executed by me personally and both returned **exit 0** (full gate: 558 contract selftests passed, 0 blockers; focused: 113 passed). The ratified receipt `cf82b102…` is installed and differs from the approved original `26748c7b…` by exactly the ratified flag and the signing timestamp. Eight of the nine identities were re-derived from actual bytes and match, including a from-scratch reconstruction of the core tree OID. The price domain, the three directions, integer exactness including subclasses, and every required refusal class behave as independently derived, with zero counterexamples across 200,021 model-checked inputs plus targeted boundary probes. Production refusals and the 27 residuals are intact.

**Nits (genuinely optional — none blocks this candidate):** F1 manifest Section-16 status/statement staleness and F2 anchor chain gaps are both pre-existing, both report-only by owner ruling, and both require touching sealed artifacts to fix; F3 is a cosmetic line-ending artifact in four documentation files with no effect on any hashed surface. Acting on none of them changes this verdict.

**This report claims no merge, no CI result, no full-P012 acceptance, no production admission, and no trading, deployment, credential, or operational authority.** The candidate remains nonaccepted pending the second flagship review, Gemini corroboration, Lead reconciliation, and current-head protected Bridge-suite Python 3.12 CI with authorized integration.

**Evidence files written (all real, under my `REVIEW_OUTPUT_ROOT`):** `results/full_gate.json` (74,920 B), `results/focused_tests.junit.xml` (20,935 B, `tests="113"`), `results/focused_collect.junit.xml`, `results/EXECUTION_EXIT_CODES.json`.