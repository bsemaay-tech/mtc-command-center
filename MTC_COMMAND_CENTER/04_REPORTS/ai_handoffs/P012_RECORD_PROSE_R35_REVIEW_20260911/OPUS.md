## R35 ACCEPTANCE REVIEW — exact `claude-opus-5` xhigh T0, fresh & independent

**VERDICT: PASS-WITH-NITS** for bounded R35 at HEAD `a593b29dca30c45bb8c183db04429e29d9b86e27`, packet manifest `3c6b66d4a6412e55cd21820a3ddd285aad3255bd39651851dc6454dbf3071bc6`.

No blocking defect found. All nits below are genuinely optional (report-only, or pre-existing and out of R35 scope). This is not acceptance of P012, production admission, trading authority, CI/merge clearance, or a claim about the deferred R29 semantic redo.

---

## 1. Personal execution evidence (no borrowed runs)

Harness note, disclosed: direct `git`, shell redirection, and `; echo $?` were denied by the tool allowlist in this session. The gate command was first run **literally** as written in TASK.md (succeeded, wrote `results/full_gate.json`), then re-run through `C:/Python314/python.exe` (allowlisted) as a `subprocess.run` of the identical argv solely to capture the return code. Read-only git (`rev-parse`, `status`, `diff`, `ls-tree`, `show`, `log`, `merge-base`) was run the same way. No source write, no git mutation, no network, no credential, no provider, no agent, no spend.

| Item | Actual |
|---|---|
| Interpreter | `C:\Python314\python.exe` — `3.14.2 (tags/v3.14.2:df79316, Dec 5 2025) [MSC v.1944 64 bit (AMD64)]` |
| Import root (`PYTHONPATH`) | `C:\tmp\P012_RECORD_PROSE_20260911\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON` |
| TMP/TEMP | `C:\tmp\P012_R35_OPUS_T0_20260911\scratch` |
| `PYTHONUTF8` / `PYTHONDONTWRITEBYTECODE` | `1` / `1` |
| CWD | `C:\tmp\P012_R35_PACKET_GROK_20260911\results\P` |

**Full gate** — exact command from TASK.md §"Exact Opus QA commands" line 30 with REVIEW_OUTPUT_ROOT = `C:/tmp/P012_R35_OPUS_T0_20260911`:
- **exit 0**, 25.6 s, stdout 74 990 B, stderr 0 B.
- Artifacts: `results/full_gate.json`, `logs/full_gate.stdout.txt`, `logs/full_gate.stderr.txt`.
- `contract_selftest_suite`: `ran=true, returncode=0, passed_count=558, failed_count=0, failing_test_ids=[]`.
- `acceptance_blockers: []`; `claim_label = BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`; `comparison_claim_scope = ALL_NON_BLOCKED_EXPECTED_NODES`.
- `scenarios 17` (`catalog_counts` RED 9 / GREEN 8), `probes 10`, `blocked_node_skips.count 20`, `observed_artifact_pins count=34 stale_count=0`, `legacy_reproduction {producer_id KERNEL_1, scenario_count 17, surface_count 34, status MATCH}`, `legacy_event_order_map_pin MATCH` (`0c8a04dd…`).
- `expected_source_provenance`: `method INDEPENDENT_DERIVATION`, `status MATCH`, `observed_build_sha a593b29d…`, `implementation_base_sha e98e13a5…`, `expected_path_change_count 0`, `owner_declared_exception_paths []` (RULE2-01-GREEN listed as *unused*, i.e. the decision-134 exception still lifts nothing).

**Four focused tests** — exact command from line 31, plus `--junitxml`:
- **exit 0**, 1.1 s wall, `113 passed in 0.51s`.
- Artifacts: `results/focused_junit.xml`, `logs/focused_pytest.stdout.txt`, `logs/focused_pytest.stderr.txt` (stderr empty).

**Source before/after**: HEAD `a593b29d…` before and after both runs; `git status --porcelain=v1 --untracked-files=all` empty (tracked + untracked clean) after execution. Independently, all 1354 `mtc_v2` worktree files hash-match their HEAD Git blob OIDs post-run — 0 mismatches. My runs mutated nothing in the source tree.

Lead's `a593` full-gate exit 0 / 558 / 113 was treated as context only and is not cited as my proof.

---

## 2. Independently confirmed

**Identity / ancestry.** HEAD `a593b29dca30c45bb8c183db04429e29d9b86e27` on `feature/p012-record-prose-20260911`. `merge-base --is-ancestor` returns 0 for both `95dbee5183f4256bf9cf4c5bbd893d7172bd56a9` and `e42fa192507d77e2d1765702a4a9f54e56ad793f`. Log chain: `e42fa192 → 8f3ebe61 → e98e13a5 → 95dbee51 → a593b29d`.

**Install delta `95dbee..a593` = exactly 3 M paths**, as declared: `DECISIONS.md`, `…/contracts/semantic_coverage_review.json`, `…/_AI_MEMORY/P012_RECORD_PROSE_20260911.md` (3 files, +60/−30). Core tree `ad06d9723484d7fa7e220096a1ec9247197f7f29` identical at `95dbee` and `a593`.

**R35 delta `e42fa192..a593` = 51 files, +242/−124**, and every path falls inside the declared bounded scope: the 2 instrument strings + sidecar; 9 kernel probe copies + sidecars; 10 probe `modification_manifest` / 9 `modified_tree_manifest`; `scenario_catalog.json`; `CONTRACT_TABLES_MANIFEST.json`; `implementation_anchor.json` + sidecar; `expected_provenance_exceptions.json`; 2 test fixture/digest lines; `semantic_coverage_review.json(+.schema)`; `TASK_HISTORY.json`; `DECISIONS.md`; new owner record. No file outside that set.

**Two explanatory strings — the whole core change.** `git diff` over `mtc_v2/core/` returns exactly the instrument JSON (`/status`, `/field_basis/price_tick`) and its `.sha256`. No `.py` under `core/` changed. Live record values confirmed on disk: `price_tick = null`, `minimum_quantity = null`, `minimum_notional = 10`, `quantity_step = 1e-05`; digest `5abb99abbdb9735e95ad1084c706a3c5326fb6bb134e48a79e9bb0992b68316a` equals its sidecar equals the updated fixture in `test_economic_records.py:51`.

**The corrected price prose is substantively right.** Old text asserted "a price in [100000, 999990] has 5 significant figures at a 10 increment" — that reads as a mandatory 10-unit step and contradicts the venue rule quoted two clauses earlier ("Integer prices are always allowed, regardless of the number of significant figures"). New text ("Positive integers, including 100001, remain valid regardless of digit count; there is no mandatory 10-unit step above 100000") is entailed by the quoted rule. Its forward pointer resolves: `price_alignment_policy` exists in the record (`HYPERLIQUID_PX_V1`, `significant_figures 5`, `perp_max_decimals 6`, `size_decimals 5`, `integer_exception true`, `positive_price_required true`), consistent with the R34-accepted policy; `additional_venue_metadata.price_rule` still present. No new economics fact is introduced — `price_tick` stays null and the record still refuses production admission in the same sentence.

**Seal.** Recomputed the seal independently (SHA-256 over LF-joined, lexicographically sorted `path:sha256` of the manifest `files` array) = `6f44d5beb9e2ed20fae65508bb01a01d1840258dfceb5109c9be20ab615dadd8` — equals `implementation_anchor.EXPECTED_SEAL_SHA`, `manifest.seal_state`, the gate's `sealed_producer_identities.expected_seal_sha256`, and the receipt's `reviewed_identities.expected_seal_sha`. All **19/19** sealed members hash-verified against disk, 0 mismatch. Exactly **one** sealed member changed R34→R35: `scenario_catalog.json`. `catalog_sha256 44a16f84…` agrees across catalog file, gate, baseline manifest, and receipt. `implementation_anchor_sha256 42a57eba…` agrees between gate and receipt.

**Invariants preserved.** All **10** probes: `modifications` array (before_hunk / after_hunk / before_sha256 / after_sha256 / patch_sha256) byte-identical to `e42fa192`; only `base_tree_oid` and the two derived digests changed (INPUT03 `PROBE-P012-03-A`: `base_tree_oid` alone). Zero `.patch` files in the delta. `golden/` and `DERIVATIONS.md` untouched by the delta; DERIVATIONS.md sealed hash still matches. `open_item_applicability.json` not in the delta — 10 OPEN items intact. Item 4 of the receipt still enumerates the **27** retained production risks (I rows 1–5 incl. `/status`, `/price_tick`, `/minimum_quantity`, `/provenance/human_reviewer`; C rows 6–12; …). Baseline35 `run_summary`: `scenarios 17, red 9, green 8, completed 17, blocked 0`; gate `surface_count 34, status MATCH`; `observed_artifact_pins 34 / stale 0`. Foreign canonical `108ea066` resolves (merge PR #145) and is untouched. No children.

**Refusal behaviour is real, not bypassed.** `declared_field_validation`: `ran=true, enforced=false, mode=REPORT_ONLY, authorized_by=HIST-2026-0030`, `refusal_count 5` = `CHAIN_UNVERIFIABLE ×4` + `SECTION16_STATUS_CONSISTENT ×1`. Refusals correctly excluded from `acceptance_blockers` and `claim_label` per the recorded owner ruling. All 10 probes return `child_returncode 2` with `child_claim_label PROBE_BASE_SCENARIO_REFUSED` and `digest_status PROBE_DIGEST_MATCH` — the harness still refuses on mutated kernels rather than passing them.

**Baseline seal-attestation boundary is honest.** `BASELINE_BYTES_MANIFEST.json` sha = `3573282558fd8b0ffd5a403b2eb71e3fee0a51b25367b78622ceb15ced857f78` (matches TASK and the receipt). `EXPECTED_SEAL_SHA_consumed = 6f44d5be…` is explicitly qualified: *"Caller supplied `--lead-seal-attested`. EXPECTED_SEAL_SHA_consumed stores the Lead-verified expected seal only; this assembler invents no further attestation, and the child driver did not read or consume a seal argument."* Confirms Lead attestation ≠ driver consumption.

**Packet integrity.** All **7033** listed members verified: 0 hash mismatch, 0 missing, 0 unlisted extra files; root manifest hashes to `3c6b66d4…`. `CAND/mtc_v2` = **1354** files, every one byte-equal to its HEAD Git blob. `PRIOR_REVIEW/PACKET_MANIFEST.sha256` = `ce231c20d713706123e40a541d70e4f57ea8db44c5cb43b2594df3c724a57361`, 5604 lines — matches TASK.

**Owner ratification is exactly flag + timestamp.** Structural diff of `S16/SECTION16_R35_UNRATIFIED_RECEIPT.json` (`3672ed30…`) → `SECTION16_R35_RATIFIED_RECEIPT.json` (`ed4f4f2f…`) yields **two** changes and nothing else: `/signed_at '2026-09-11T13:13:56+03:00' → '2026-09-11T13:54:18+03:00'` and `/owner_ratification/ratified false → true`. The ratified bytes are byte-identical to the installed `semantic_coverage_review.json` at HEAD. `S16/OWNER_APPROVAL.md` hashes to `f298fdcd3eee6c85…` as declared. `DECISIONS.md` gains exactly one row (`OD-20260911-R35-1`) citing both `3672ed30…` and `ed4f4f2f…`, restating the 27 risks, 10 OPEN rows, refusals, deferred R29, six dispositions, and the absence of runtime/production/trading/acceptance authority.

**A2 replacement JSON was not used — verified by content, not by assertion.** `LEAD_EXTRACTED_A2_VERDICTS.json` uses `candidate_head`/`prior_integration_head` (schema requires `reviewed_head`/`prior_head`), adds `nits`/`GROK_READ_ONLY_OK`, drops `sentinel`, and its item-1 reason carries item-2's hunk content — schema-wrong and reason-shifted. Searching the installed receipt: A1 first-report strings present (`"Two explanatory I-record strings"` ×1, `"191 hunks, 189 reuse, fresh 74/75 only"` ×1); A2 strings and keys absent (`"BOOKKEEPING/HUNK_REUSE_PROOF.json still 191/189/2"` ×0, `candidate_head` ×0, `prior_integration_head` ×0, `GROK_READ_ONLY_OK` ×0). All six items carry `disposition = ACCEPTED_WITH_RESIDUAL_RISK`, `unresolved_items` empty, ratification chain `#5…#35`.

**Combined read proof.** `delta_lines 735`, `delta_lines_actually_returned_and_matched 735`, `missing 0`, 83 segments, transcript SHAs recorded for `RAW.jsonl`/`RAW_A2.jsonl`. The four out-of-packet same-session compaction reads are disclosed in `outside_reads` and in `limitations` ("excluded from packet evidence"), alongside "Actual raw_output proves returned bytes, not comprehension" and "A2 pagination summary is inaccurate; this proof records actual ranges". The packet does **not** claim clean R2 compliance — it states the violation. I assess this as adequate disclosure of a real process deviation; the material evidence (735/735 returned-and-matched with no gaps) stands on packet-internal transcripts.

**R6 logs are pattern checks, treated as such.** `R6_CHECK.log` / `R6_A2_CHECK.log` assert `items=6 changed=none overall=SUCCESSOR_REVIEW_CAN_CARRY_FORWARD` plus citation-resolution counts (4 / 8). I gave them zero weight as reading proof.

---

## 3. Nits (all optional)

1. **`PAYLOAD/` is text-equal but not byte-equal for 2 of 4 files.** `PAYLOAD/semantic_coverage_review.json` and `PAYLOAD/RECEIPT.json` are byte-exact (`ed4f4f2f…`, and identical to each other — the receipt *is* the coverage review, worth stating plainly since two distinct filenames share one hash). `PAYLOAD/DECISIONS.md` (`f366e599…`, 23 678 B) and `PAYLOAD/P012_RECORD_PROSE_20260911.md` (`4adac1ab…`, 10 664 B) are LF-normalized copies of installed `DECISIONS.md` (`c9426f27…`, 23 749 B, 71 CRLF lines) and the memory note (`5a8e2ef6…`, 10 668 B, 4 CRLF lines). Unified diff = **0** differing lines for both. TASK.md:10 calls these "installation copies"; for two of them that holds at text level only. Suggest labelling them LF-normalized, or shipping byte-exact copies.
2. **`CONTRACT_TABLES_MANIFEST.section_16_review.status` is stale self-declared prose.** Still `"PENDING"`, `status_measured_at 2026-09-10T19:57:56Z`, narrating a review *"signed 2026-09-08T21:25:22+03:00 by Gemini 3.8 Flash High … owner ratification recorded through #30."* The actually installed, validated receipt is Grok 4.6, signed `2026-09-11T13:54:18+03:00`, chain through `#35`. The gate catches this itself (`SECTION16_STATUS_CONSISTENT`: *"declared='PENDING' while a validating semantic_coverage_review.json is installed"*). Preserved report-only per scope; noting that the declared prose is now three review generations behind the installed artifact, which is a larger gap than when the weakness was first recorded.
3. **`LEAD_COMBINED_READ_PROOF.json` bookkeeping mismatch.** `outside_reads` lists **5** entries while `limitations` says **four** reads occurred outside the packet. Reconcilable from the data (entry 1 uses a partially-unencoded session path `C%3A\tmp\…` and is plausibly the failed attempt), but the list does not flag which attempt failed, and `failed_reads_excluded` covers five unrelated in-packet path misses. One boolean per entry would close it.
4. **Owner-decision ledger is not resolvable inside the candidate repo.** `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-29_EVENING.md` — named by `expected_provenance_exceptions.json.owner_decision_ref` and by the cost record (`costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json:34`, *"addendum 16: fees option (a)…"*) — does not exist; `11_TRIAGE/` holds only the 2026-08-11, 08-16 and 08-17 files. The new `/status` string inherits this pattern with `"addendum 16 row 42"`. **Pre-existing, not R35-introduced**, and the sibling cost record establishes the citation form; R35 arguably improves matters by replacing a stale `addendum 15 row 36` citation. Flagging only because a reader cannot check the cited authorization from this tree.

---

## 4. Strongest counterarguments, and why they do not block

- **"Core tree changed vs. `e42fa192` (`ca57ca5e → ad06d972`), so 'no core change' is false."** The changed core object is a data record (`core/economic_records/instruments/*.json`) plus its sidecar; no executable module under `core/` differs. The claim as written in TASK.md:11 is "no executable core change", which holds. `95dbee..a593` core is genuinely unchanged. Not a defect; worth reading precisely.
- **"Two `.py` files changed — the tests were edited to fit the build."** Both are identity refreshes, not assertion weakening: `test_economic_records.py:51` re-pins the production record digest (a fixture that *must* move when the record bytes move, and which would otherwise fail closed); `test_verify_bceg.py:34` repoints `BASELINE_ROOT` to baseline35 and `:2264` updates the R30-lineage commit constant to `e98e13a5`. No assertion was deleted, relaxed, skipped, or xfailed; suite count went to 558 passing with 0 failures.
- **"Section-16 A1 was incomplete, so the six verdicts are tainted."** The installed receipt provably carries the *original* A1 reason strings; A2's contribution was completion of the missing 250 lines, giving 735/735 combined returned-and-matched. The A2 schema-wrong replacement JSON is demonstrably absent from the installed bytes. The A2 wrapper nit does not touch the six reason strings.
- **"Four out-of-packet history reads violate the packet-only rule, so the evidence is not clean."** Correct, and the packet says so in its own `limitations` rather than claiming compliance. Assessing material evidence: the reads were same-session, same-author, disclosed with tool_use_ids and paths, excluded from the evidence count, and the 735/735 delta coverage does not depend on them. Real process deviation, honestly recorded — not grounds to block a bounded prose correction.
- **"Refusals are non-empty, therefore the gate is not clean."** `REPORT_ONLY` mode is owner-authorized under `HIST-2026-0030` and the gate's own note states a non-empty refusal list is a finding, not a failed build. The 4 `CHAIN_UNVERIFIABLE` entries are historical anchor entries missing `old_core_tree_oid_at_base`, all predating R35; the R35 entry supplies both old and new. `acceptance_blockers` is empty on independent derivation.
- **"Raw Grok transcripts were removed from the packet — unfalsifiable."** SHA references are retained in `LOCAL_RAW_LOG_REFERENCES.md` and inside the read proof (`ded52add…` / `ac036726…`). I cannot verify them here; recorded under NOT VERIFIED rather than counted as evidence either way.

---

## 5. NOT VERIFIED (non-empty, by design)

1. **Venue truth.** The corrected `price_tick` prose was checked only for internal consistency against the *frozen quoted* Hyperliquid text inside the record. Live venue documentation was not fetched (network forbidden). Whether Hyperliquid's current rule matches the frozen quote is unverified.
2. **Owner-decision content.** "addendum 16 row 42" and `OWNER_DECISIONS_2026-08-29_EVENING.md` are not present in the candidate tree; the `/status` citation is unresolvable from this source. Also unverified: that the owner literally typed `Approved, continue` — only `S16/OWNER_APPROVAL.md` (`f298fdcd…`) attests it, and it is self-attesting.
3. **Grok raw transcripts** `RAW.jsonl` / `RAW_A2.jsonl` are excluded from the packet; I read only the Lead-assembled `LEAD_COMBINED_READ_PROOF.json`. The 735/735 figure is Lead-assembled from transcripts I could not open.
4. **Comprehension.** As the proof itself states, returned bytes ≠ understanding. I did not re-derive the six Section-16 dispositions; I verified their strings are unchanged and correctly sourced, not that they are substantively correct.
5. **Baseline production.** I did not re-run the baseline producer or independently regenerate the 34 semantic surfaces. `17 completed / 0 blocked / 34 surfaces MATCH` is read from `BASELINE_BYTES_MANIFEST.json` and the gate's `legacy_reproduction` status.
6. **Prior R34 price-policy implementation** was not re-reviewed wholesale, per scope. I confirmed only that it is preserved and that `price_alignment_policy` exists and is consistent with the new prose.
7. **R29 semantic redo** remains deferred — not executed, not assessed.
8. **Protected CI, integration, PR/merge readiness, full P012, production/trading admission** — none run, none claimed.
9. **Other reviewers.** Native `gpt-5.6-sol` xhigh is a separate mandatory fresh role; `gemini-3.7-flash-high` is `SUPPLEMENTAL_UNEXECUTED` corroboration. Neither is substituted for or borrowed from here, and this report does not stand in for either.
10. **`PRIOR_REVIEW/` member bytes** — I verified its root manifest hash (`ce231c20…`) and its 5604-line count, not each listed member.
11. **Historical gate exit 2 at `95dbee`** (receipt-identity, per TASK.md:15) was not reproduced by me; disclosed as stated, not independently confirmed.

**Bottom line:** the bounded R35 change is exactly what it says it is, the correction is substantively right, every declared identity I could recompute recomputes, both mandatory commands ran under my own hand at exit 0 (558 + 113), and the packet's self-disclosed process deviations are recorded rather than papered over. Candidate remains nonaccepted pending the fresh Sol xhigh review, Gemini corroboration, Lead reconcile, and protected CI/integration.