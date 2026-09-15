# W349 Report — re-seal #16 copy refresh and canonical gate

## Verdict

The in-repo expected-bundle copies were refreshed and committed at content commit
`63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5`. The copied manifest records seal
`40aaf7da2a67753b74922576111cf1aede911c9de1815f6d34a04d22f8666fab` and the anchor records the
same seal (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:565-568`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`).

The one canonical `full-gate` invocation refused with 3 entries in its full refusal list and 2
acceptance blockers; 9 of 10 probes were `DETECTED` (`W349_GATE_RECEIPT.json:2-36,143-148,505-715`).
No refusal was fixed. The receipt has no `OBSERVED_EXTRA_MEMBER` entry in its complete refusal array
(`W349_GATE_RECEIPT.json:677-715`).

## Preconditions, routing, and scope

The lane required a clean non-`master` worktree at `78da7991`, plus `RESEAL16_DONE.txt` and
`W300E_DONE.txt` with `exit=0` (`C:/tmp/LANE_PROMPTS_20260828/LANE_W349_COPIES_SEAL16_GATE.md:3-6`).
The measured start was branch `feature/wp-p0-12-corrected-vnext-20260831`, full HEAD
`78da7991d7069f26aaab89f90184ac086c2d8bbf`, and an empty porcelain status. The two marker files
were present; the baseline marker contained `exit=0`, and the re-seal marker records the seal,
base, design digest prefix, line count, and moved-member hashes
(`C:/tmp/LANE_PROMPTS_20260828/W300E_DONE.txt:1`;
`C:/tmp/LANE_PROMPTS_20260828/RESEAL16_DONE.txt:1-22`).

Primary changes are under `MTC_COMMAND_CENTER/01_MTC_PROJECT/**`, so the routed stage is the MTC
build stage (`CONTEXT_MAP.md:8-10`). Scope is T0 because protected expected economic artifacts are
being replaced under explicit owner decisions 147/149/151. No Pine, core kernel, baseline, broker,
venue, host, deploy, or live path was changed. The lane expressly authorized only the bundle-copy
paths and forbade `--mode observe` (`C:/tmp/LANE_PROMPTS_20260828/LANE_W349_COPIES_SEAL16_GATE.md:13-20`).

The fresh design measured SHA-256
`5c657ec93c714b59d56a9ca99e7f42005061ceaad6f8d2889e2d691af3381c09` and 1800 lines. Those values
match both the copied manifest's operative design pin and the gate's sealed producer identity
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-18`;
`W349_GATE_RECEIPT.json:1985-1992`). The operative version is v1.17; see `## Discrepancies`.

## Refreshed copy SHA-256 table

Every row below was measured from the named source and destination after copying. All 19 manifest
members match both the source bytes and their manifest pins; the manifest supplies each exact
path, SHA-256, and byte count
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:62-158`).

| File | Source SHA-256 | Destination SHA-256 | Result |
|---|---|---|---|
| `DERIVATIONS.md` | `0be3a60721e7cfb2eaefc6e2f01277309c64f8c136d0e809d893322b154ec34d` | `0be3a60721e7cfb2eaefc6e2f01277309c64f8c136d0e809d893322b154ec34d` | byte-identical |
| `scenario_catalog.json` | `3ca90039dbecdc8b0902ba2acabd87db5476da15c493ce74979b434cdba656ff` | `3ca90039dbecdc8b0902ba2acabd87db5476da15c493ce74979b434cdba656ff` | byte-identical |
| `golden/corrected_vnext/RULE2-01-GREEN.json` | `27891e5eddc7e604e2087e9d39c9266d5825cefc16ea4a5c7672be57357d7458` | `27891e5eddc7e604e2087e9d39c9266d5825cefc16ea4a5c7672be57357d7458` | byte-identical |
| `golden/corrected_vnext/RULE2-01-RED.json` | `3cf30e13db25a99093d9087c374c05dabbc6ca0a33ad6cebdfdd1d28df42b94d` | `3cf30e13db25a99093d9087c374c05dabbc6ca0a33ad6cebdfdd1d28df42b94d` | byte-identical |
| `golden/corrected_vnext/RULE2-02-GREEN.json` | `5cf90e11a1b5251d7615cd9001a35ec5673d7297ac716d4f6448a9292bd7a822` | `5cf90e11a1b5251d7615cd9001a35ec5673d7297ac716d4f6448a9292bd7a822` | byte-identical |
| `golden/corrected_vnext/RULE2-02-RED.json` | `82c4651527a16c0daa21927ec7ae643ad0a5041eeebf3314f36b84a2435a10a0` | `82c4651527a16c0daa21927ec7ae643ad0a5041eeebf3314f36b84a2435a10a0` | byte-identical |
| `golden/corrected_vnext/RULE2-03-GREEN.json` | `46b93e223eb7e5733ba5ef6d7e50345f5665437d9552c8852a8d2c04b9f631b9` | `46b93e223eb7e5733ba5ef6d7e50345f5665437d9552c8852a8d2c04b9f631b9` | byte-identical |
| `golden/corrected_vnext/RULE2-03-RED.json` | `d475b8096699a1df6d0985f4b67eeda86c6b96dca36778da683fc859058e96b0` | `d475b8096699a1df6d0985f4b67eeda86c6b96dca36778da683fc859058e96b0` | byte-identical |
| `golden/corrected_vnext/RULE2-04-GREEN.json` | `5384c298d0d103b67b8d9968267a4a4b736f5c75430cf623f61e80f0a9f025c5` | `5384c298d0d103b67b8d9968267a4a4b736f5c75430cf623f61e80f0a9f025c5` | byte-identical |
| `golden/corrected_vnext/RULE2-04-RED.json` | `f31e3b879599e4fbc621fd4410944896a39aeac9411c59dff42164d8eb87b2b3` | `f31e3b879599e4fbc621fd4410944896a39aeac9411c59dff42164d8eb87b2b3` | byte-identical |
| `golden/corrected_vnext/RULE2-05-GREEN.json` | `b68bf0bb5975cc06c3f47fdf795221c8e255b88c9329f770558d97af2b7732f8` | `b68bf0bb5975cc06c3f47fdf795221c8e255b88c9329f770558d97af2b7732f8` | byte-identical |
| `golden/corrected_vnext/RULE2-05-RED.json` | `9a59aada281a548192e18e0333fad3fadfa8c19cbd17d603943a453a98193242` | `9a59aada281a548192e18e0333fad3fadfa8c19cbd17d603943a453a98193242` | byte-identical |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | `49c845eb7234e464dd29fea2dd79bae2aba1289afc2f8cff8c0d94729e89d590` | `49c845eb7234e464dd29fea2dd79bae2aba1289afc2f8cff8c0d94729e89d590` | byte-identical |
| `golden/corrected_vnext/RULE2-06-GREEN.json` | `1df73f308d3695f16ba1ee27fac598fea58cd0509c41da478af270293e20fb75` | `1df73f308d3695f16ba1ee27fac598fea58cd0509c41da478af270293e20fb75` | byte-identical |
| `golden/corrected_vnext/RULE2-06-RED.json` | `6dcbefed552d175a25f7668e430d873715d7846782c34d33c8569bf2e4bde9ab` | `6dcbefed552d175a25f7668e430d873715d7846782c34d33c8569bf2e4bde9ab` | byte-identical |
| `golden/corrected_vnext/RULE2-07-GREEN.json` | `f23d1d83007ce27f2094dcb6931021a4850c8a48d7e509da458e18d1efbe92ac` | `f23d1d83007ce27f2094dcb6931021a4850c8a48d7e509da458e18d1efbe92ac` | byte-identical |
| `golden/corrected_vnext/RULE2-07-RED.json` | `b26e0fafe9b61f319c25174792d735a0fe9a85cb9458cfa5addd7d992b1df1c4` | `b26e0fafe9b61f319c25174792d735a0fe9a85cb9458cfa5addd7d992b1df1c4` | byte-identical |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `fec568d4d5912668816b91bd9ddce31757a9a38464b276e2a061380782ff0803` | `fec568d4d5912668816b91bd9ddce31757a9a38464b276e2a061380782ff0803` | byte-identical |
| `golden/corrected_vnext/RULE2-08-RED.json` | `5260d9eec444fe59e7af0acef79785d1981dd9f43de125353cbd9966e4f33aa1` | `5260d9eec444fe59e7af0acef79785d1981dd9f43de125353cbd9966e4f33aa1` | byte-identical |

There were no unchanged-before-copy “other” manifest members: all 19 member files differed from the
starting in-repo copies and therefore all 19 were refreshed. The re-seal record names exactly those
19 changed members (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:932-957`).

The two copied control files and regenerated sidecar also match their measured source values:

| File | Source SHA-256 | Destination SHA-256 | Result | Evidence |
|---|---|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `df191ff4b8f318c9b6d0efc11cc218b32bce486dd1f2d6be26a46f3f0648bb51` | `df191ff4b8f318c9b6d0efc11cc218b32bce486dd1f2d6be26a46f3f0648bb51` | byte-identical | `C:/tmp/LANE_PROMPTS_20260828/RESEAL16_DONE.txt:21` |
| `implementation_anchor.json` from `IMPLEMENTATION_ANCHOR_DRAFT.json` | `267603d720158630b2aed5610f34e927fe8ccd6440b5d962b35ae11125dcef82` | `267603d720158630b2aed5610f34e927fe8ccd6440b5d962b35ae11125dcef82` | byte-identical | `C:/tmp/LANE_PROMPTS_20260828/RESEAL16_DONE.txt:22`; `W349_GATE_RECEIPT.json:1992` |
| `implementation_anchor.json.sha256` | `267603d720158630b2aed5610f34e927fe8ccd6440b5d962b35ae11125dcef82` | `267603d720158630b2aed5610f34e927fe8ccd6440b5d962b35ae11125dcef82` | regenerated and matches anchor | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1` |

The content commit staged exactly these 22 paths, and `git diff --check` returned exit 0 before the
commit. Its subject uses v1.17 under the repository-wins clause:
`chore(mtc-v2): refresh in-repo bundle copies to re-seal #16 and pin design v1.17 (decisions 147/149/151)`.

## Canonical gate

Exactly one invocation was issued from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W349_GATE_RECEIPT.json
```

The receipt confirms `mode: full-gate`, a refused claim label, 17 scenarios, 10 probes, and 34
non-stale observed pins (`W349_GATE_RECEIPT.json:143-148,226,289-503,505-675`). The process returned
1 and wrote `W349_GATE_RECEIPT.json`; it was not rerun. `--mode observe` was not invoked, consistent
with the lane's prohibition (`C:/tmp/LANE_PROMPTS_20260828/LANE_W349_COPIES_SEAL16_GATE.md:20-26`).

## Full refusal list — verbatim

The following is the complete `refusals` value copied verbatim from
`W349_GATE_RECEIPT.json:677-715`:

```json
"refusals": [
  {
    "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
    "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
  },
  {
    "check_id": "EXPECTED_PATH_CHANGED_AFTER_BASE",
    "count": 19,
    "detail": "19 expected paths changed after the implementation base",
    "pointer": "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json",
    "pointers": [
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-GREEN.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md",
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json"
    ]
  },
  {
    "check_id": "PROBE_NOT_DETECTED",
    "comparator_first_differing_node": "/RESULT_SURFACE/admitted",
    "measured_failed_check": "CLOSED_SET_VIOLATION",
    "scenario_id": "PROBE-P012-02-A"
  }
],
```

## Probe table

| Probe | Base scenario | Expected failed check | Measured failed check | Expected first changed node | Comparator first differing node | Status | Evidence |
|---|---|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `RULE2-01-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W349_GATE_RECEIPT.json:506-522` |
| `PROBE-P012-01-B` | `RULE2-01-GREEN` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W349_GATE_RECEIPT.json:523-539` |
| `PROBE-P012-02-A` | `RULE2-02-GREEN` | `CORRECTED_EXPECTATION` | `CLOSED_SET_VIOLATION` | `/RESULT_SURFACE/admitted` | `/RESULT_SURFACE/admitted` | `NOT_DETECTED` | `W349_GATE_RECEIPT.json:540-556` |
| `PROBE-P012-03-A` | `RULE2-03-RED` | `RECORD_IDENTITY_PREFLIGHT` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | same | `DETECTED` | `W349_GATE_RECEIPT.json:557-573` |
| `PROBE-P012-04-A` | `RULE2-04-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W349_GATE_RECEIPT.json:574-590` |
| `PROBE-P012-05-A` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W349_GATE_RECEIPT.json:591-607` |
| `PROBE-P012-05-B` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `DETECTED` | `W349_GATE_RECEIPT.json:608-624` |
| `PROBE-P012-06-A` | `RULE2-06-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/exit_id` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W349_GATE_RECEIPT.json:625-641` |
| `PROBE-P012-07-A` | `RULE2-07-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fee_events/1/liquidity_role` | `/EVENT_SURFACE/cash_events/1/signed_delta` | `DETECTED` | `W349_GATE_RECEIPT.json:642-658` |
| `PROBE-P012-08-A` | `RULE2-08-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W349_GATE_RECEIPT.json:659-675` |

Measured total: 9 `DETECTED`, 1 `NOT_DETECTED` (`W349_GATE_RECEIPT.json:505-675`).

## Discrepancies

1. The lane repeatedly says the operative design pin is v1.16 and prescribes a v1.16 commit subject
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W349_COPIES_SEAL16_GATE.md:1,8-9,17-18,21`). The copied
   manifest's controlling `design.version` is v1.17, its measured hash/line pin is
   `5c657ec9...`/1800, its seal reason says the pin moves to v1.17, and its latest re-seal row says
   `design_pin: v1.17`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-17,565-568,932-957`).
   The fresh design measurement matches v1.17 (`W349_GATE_RECEIPT.json:1988-1992`). Under common
   clause C-2, the content commit subject therefore says v1.17. No bundle bytes were edited.
2. The copied bundle has stale internal v1.16 prose despite its operative v1.17 pin: the re-seal #16
   revision/effect fields say v1.16, and the anchor's acceptance statement also says v1.16
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:558-562`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:30-33`).
   The lane authorized byte-for-byte copying, not repair, so these source-authored residues were
   preserved and not fixed.
3. The lane predicted an 18-path provenance refusal
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W349_COPIES_SEAL16_GATE.md:24-26`). The gate measured 19:
   all 17 goldens, `DERIVATIONS.md`, and `scenario_catalog.json`
   (`W349_GATE_RECEIPT.json:683-707`). No refusal was fixed.
