# W316 re-seal #14 and design-v1.15 in-repo refresh report

Date: 2026-09-03
Actor: Codex implementer lane
Status: **COPY COMPLETE; CANONICAL GATE REFUSED ON ITS EARLY PATH**
Finding count: **2**

The final working tree contains byte-for-byte copies of the four bundle artifacts, the regenerated
anchor sidecar, the two differing RULE2-08 goldens, and the five named differing scenario inputs.
The one permitted canonical gate was invoked before the conditional golden/input refresh was
complete. It refused at the first stale member, so it did not evaluate the seal, anchor, probe pins,
probes, review record, or provenance record. This report does not claim package acceptance
(`W316_GATE_RECEIPT.json:1-8`;
`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:32-37`).

## Scope, routing, and preflight

The required markers reported `exit=0` for W315 and W300C, and the Lead marker named re-seal #14
(`C:\tmp\LANE_PROMPTS_20260828\W315_DONE.txt:1`;
`C:\tmp\LANE_PROMPTS_20260828\W300C_DONE.txt:1`;
`C:\tmp\LANE_PROMPTS_20260828\RESEAL14_DONE.txt:1`). Before the first write, the measured branch
was `feature/wp-p0-12-corrected-vnext-20260831`, HEAD was
`af97ec8c13c9e54b8279e607144bbbfded27528b`, and `git status --short` was empty, matching the lane's
hard start gate (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:3-8`).

Gate-1 classification is **T1**: the writes are non-economic verifier contract/golden/input copies
inside an owner-gated MTC path, with no kernel, strategy, Pine, parity, broker, host, deploy,
credential, or live write. T1 is the repository category for non-economic product code/scripts
(`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md:20-31`). C-1 required this lane to work without
another assistant or model, so no independent model audit was invoked and no acceptance verdict is
claimed (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).

The lane's five contract-copy paths, conditional golden/input paths, receipt, and report were the
only in-repo write scope. No kernel, harness, probe, or design byte was writable
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:13-27,36-41`).

## Design and baseline measurements

The design file was measured directly with `Get-FileHash -Algorithm SHA256` and `Get-Content`:

```text
sha256=137180aee4834fa6b87932e289d7ce8cf56d9471c08e7b53982445598347c62f
lines=1664
bytes=195089
```

Those measured SHA-256 and line-count values equal the bundle's v1.15 design pin
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-17`).
The refreshed anchor records re-seal #14
`a58b6dea753976a778413dca3e2cc13d47d2dee9b241bdc7d7cff9a04e3b5eba`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:1-7,30-33`).
The baseline manifest consumes that same seal and catalog digest, and records 17 completed / 0
blocked (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:9-25`).

## Byte-for-byte copy evidence

`Get-FileHash -Algorithm SHA256` was run after the final copy state. Every source/destination pair
below is equal. The sidecar is 65 bytes, contains the lowercase anchor digest plus one LF, and has no
CR (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`).

| In-repo file | Bundle source/generated SHA-256 | In-repo SHA-256/value | Action |
|---|---|---|---|
| `contracts/CONTRACT_TABLES_MANIFEST.json` | `659493143e626730c2ae6a2ebc59c658c60639fdf26cc0bedf7116b1135b0450` | `659493143e626730c2ae6a2ebc59c658c60639fdf26cc0bedf7116b1135b0450` | copied |
| `contracts/scenario_catalog.json` | `555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14` | `555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14` | copied |
| `contracts/DERIVATIONS.md` | `8eeacb17be2a1d3d5c6f4cfb741dccde13a864f91ab3152aa04d5a115330dcd2` | `8eeacb17be2a1d3d5c6f4cfb741dccde13a864f91ab3152aa04d5a115330dcd2` | copied |
| `contracts/implementation_anchor.json` | `7ddfda98a88cd1d1e1c0d8853974b10cbc51b3e240d7bf4b9635d37559b18b2a` | `7ddfda98a88cd1d1e1c0d8853974b10cbc51b3e240d7bf4b9635d37559b18b2a` | copied |
| `contracts/implementation_anchor.json.sha256` | anchor digest `7ddfda98a88cd1d1e1c0d8853974b10cbc51b3e240d7bf4b9635d37559b18b2a` | sidecar value `7ddfda98a88cd1d1e1c0d8853974b10cbc51b3e240d7bf4b9635d37559b18b2a` | regenerated |
| `golden/corrected_vnext/RULE2-06-RED.json` | `9d9d3a9748571d63c8790d9b7ef5df398ed945f75c59b7148975debfe167a581` | `9d9d3a9748571d63c8790d9b7ef5df398ed945f75c59b7148975debfe167a581` | already equal; not copied |
| `golden/corrected_vnext/RULE2-08-RED.json` | `2157c03fc52daa9183d14e5a1552d6dec58eb4d90024701bd49abb7487f98c4b` | `2157c03fc52daa9183d14e5a1552d6dec58eb4d90024701bd49abb7487f98c4b` | copied |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `08a559422eca70cb302f1381f2abbd409dd3c8482fdb58db47cdda5528e4de32` | `08a559422eca70cb302f1381f2abbd409dd3c8482fdb58db47cdda5528e4de32` | copied |
| `contracts/inputs/RULE2-06-EQUAL-PRICE-RED.json` | `0c65c82b911f3a510d074df00bc81335bb3397697e96f422f5c05267e4ea085c` | `0c65c82b911f3a510d074df00bc81335bb3397697e96f422f5c05267e4ea085c` | copied |
| `contracts/inputs/RULE2-06-RED.json` | `8c62e57e0584207d99ab6d581a91535d341b65df46b362dc402a48da702f1f68` | `8c62e57e0584207d99ab6d581a91535d341b65df46b362dc402a48da702f1f68` | copied |
| `contracts/inputs/RULE2-06-GREEN.json` | `c334b07011bd538e7b9d02de451abbd5f389da8cf7392da64fed7dfc941dd4e2` | `c334b07011bd538e7b9d02de451abbd5f389da8cf7392da64fed7dfc941dd4e2` | copied |
| `contracts/inputs/RULE2-08-RED.json` | `4bc3cc7402e1eb8dde4416fd698a9d2a46b5477aa9d5e7a10061aa7f8b281c4d` | `4bc3cc7402e1eb8dde4416fd698a9d2a46b5477aa9d5e7a10061aa7f8b281c4d` | copied |
| `contracts/inputs/RULE2-08-GREEN.json` | `6c349e8bf180e63dddb34834aa13098f9d723aecdff6b02d328aa6b55996a939` | `6c349e8bf180e63dddb34834aa13098f9d723aecdff6b02d328aa6b55996a939` | copied |

The source and destination evidence is the first line of each named bundle and in-repo file. The
manifest independently records the three relevant golden digests
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:133-157`),
and the refreshed catalog records the five input digests
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:1154,1346,1539,1998,2126`).

The prescribed five-file diff stat before the first commit was:

```text
 .../contracts/CONTRACT_TABLES_MANIFEST.json        |  312 +---
 .../tests/corrected_vnext/contracts/DERIVATIONS.md |  883 +++++++++++
 .../contracts/implementation_anchor.json           |   24 +-
 .../contracts/implementation_anchor.json.sha256    |    2 +-
 .../contracts/scenario_catalog.json                | 1558 +++++++++++++++++++-
 5 files changed, 2467 insertions(+), 312 deletions(-)
```

The final twelve refreshed content files, measured against pre-lane HEAD `af97ec8c`, are:

```text
 .../golden/corrected_vnext/RULE2-08-GREEN.json     |   14 +-
 .../golden/corrected_vnext/RULE2-08-RED.json       |   32 +-
 .../contracts/CONTRACT_TABLES_MANIFEST.json        |  312 +---
 .../tests/corrected_vnext/contracts/DERIVATIONS.md |  883 +++++++++++
 .../contracts/implementation_anchor.json           |   24 +-
 .../contracts/implementation_anchor.json.sha256    |    2 +-
 .../contracts/inputs/RULE2-06-EQUAL-PRICE-RED.json |    2 +-
 .../contracts/inputs/RULE2-06-GREEN.json           |    2 +-
 .../contracts/inputs/RULE2-06-RED.json             |    2 +-
 .../contracts/inputs/RULE2-08-GREEN.json           |    2 +-
 .../contracts/inputs/RULE2-08-RED.json             |    2 +-
 .../contracts/scenario_catalog.json                | 1558 +++++++++++++++++++-
 12 files changed, 2498 insertions(+), 337 deletions(-)
```

`git diff --check` returned 0. The prescribed first commit is
`d574a4054f054ed51ffc9ecc0ead77264ae8e2ec`, with subject
`chore(mtc-v2): refresh in-repo bundle copies to re-seal #14 and pin design v1.15`. Its staged
set contained exactly the five contract paths and each staged copied blob equalled its bundle-source
blob. The later conditional copies are necessarily part of the report/receipt commit; see
Discrepancy 3.

## Canonical gate — exactly one invocation

The only canonical-gate invocation was made from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN --output C:\WP012BUILD\W316_GATE_RECEIPT.json
```

It returned exit 2. The verifier's exception path writes only stdout, not `--output`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4164-4171`),
so the stdout JSON was persisted as required. Receipt SHA-256:
`26a49b6d4701f7bfd2e63a5596e3c11581cc2d586cfa83719f6ec8ba7e9a9e37`.

### Full refusal list, verbatim

The early path emitted a singular `refusal` rather than the later pipeline's `refusals` array. This
is the complete receipt verbatim (`W316_GATE_RECEIPT.json:1-8`):

```json
{
  "claim_label": "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusal": {
    "check_id": "EXPECTED_MEMBER_DIGEST_MISMATCH",
    "detail": "golden/corrected_vnext/RULE2-08-GREEN.json"
  }
}
```

The manifest expected SHA-256
`08a559422eca70cb302f1381f2abbd409dd3c8482fdb58db47cdda5528e4de32`; the in-repo file at the
gate commit measured
`6ad9432df9bcc1ef8d7f5ec31fcb2a5c7b30a7c80c56095c74aaeb6a24e91b97`.
The pointer and expected value are independently present in the receipt and manifest
(`W316_GATE_RECEIPT.json:4-6`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:148-151`).
The second value is the direct pre-copy `Get-FileHash` measurement recorded before the differing
file was replaced.

After the refusal, the two differing RULE2-08 goldens and five catalog-pinned inputs were copied.
A supplemental PowerShell check over the final bytes measured: 19 manifest members, 0 member
mismatches, computed seal equal to the recorded seal, design pin equal, anchor seal equal, anchor
sidecar equal, 27 catalog rows, 0 catalog-input mismatches, and baseline seal/catalog equal. These
checks are not a substitute for the consumed canonical gate invocation. The verifier performs the
design check before its member loop and cannot compute the seal or reach the anchor after a member
digest refusal (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2226-2271`).

## Probe table

No probe evaluated `DETECTED` or `NOT DETECTED`. The gate refused before it constructed the
comparison pipeline, which is the caller that would produce the probe receipts
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4108-4150`).
The expected checks/nodes below are the sealed catalog declarations
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2193-2398`).

| Probe | Gate result | Expected failed check | Expected changed node |
|---|---|---|---|
| `PROBE-P012-01-A` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` |
| `PROBE-P012-01-B` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` |
| `PROBE-P012-02-A` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/RESULT_SURFACE/admitted` |
| `PROBE-P012-03-A` | refused before probe evaluation | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` |
| `PROBE-P012-04-A` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` |
| `PROBE-P012-05-A` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` |
| `PROBE-P012-05-B` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` |
| `PROBE-P012-06-A` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/exit_id` |
| `PROBE-P012-07-A` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fee_events/1/liquidity_role` |
| `PROBE-P012-08-A` | refused before probe evaluation | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` |

## Findings

### F-01 — The one gate ran before all conditional golden copies were synchronized

The gate found `RULE2-08-GREEN.json` at the manifest pointer with expected SHA-256
`08a559422eca70cb302f1381f2abbd409dd3c8482fdb58db47cdda5528e4de32` and measured in-repo
SHA-256 `6ad9432df9bcc1ef8d7f5ec31fcb2a5c7b30a7c80c56095c74aaeb6a24e91b97`.
The verifier refuses immediately when a listed member's digest or byte size differs
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2245-2265`;
`W316_GATE_RECEIPT.json:4-6`). The file is now copied and equals the manifest value, but the lane
explicitly authorizes only one gate invocation, so no post-correction gate evidence exists
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:3-4,32-37`).

### F-02 — `files[]` omits the five inputs that the refreshed catalog pins

The prompt conditions input copying on those inputs appearing in manifest `files[]`
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:24-26`). The manifest's
complete 19-member list contains only DERIVATIONS, the catalog, and 17 goldens—no input path
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:62-158`).
The refreshed catalog nevertheless pins all five exact bundle-input digests, and the five in-repo
copies initially differed
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:1154,1346,1539,1998,2126`).
Under C-2, the repository's executable contract won and those five exact prompt-named inputs were
copied (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`). Final static comparison measured
zero catalog-input mismatches, but the canonical gate did not reach input validation.

## Discrepancies

1. **The prompt's shortened repository path does not exist at the worktree root.** The copies live
   below `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/`; that repository path was used under
   C-2 (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:13-27`;
   `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`).
2. **The prompt names only `RULE2-06-RED.json` as a golden path, while its parenthetical says the two
   RULE2-08 goldens changed.** The manifest lists both RULE2-08 goldens, and the gate proved the
   GREEN copy differed (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:24-26`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:148-157`;
   `W316_GATE_RECEIPT.json:4-6`). Both differing RULE2-08 goldens were copied.
3. **The prescribed copy/commit/gate order was not achieved for conditional files.** The first
   commit `d574a405` contains the five main contract files, but the two RULE2-08 goldens and five
   inputs were identified and copied only after the one gate refused. They are included with the
   receipt/report commit. The gate was not rerun because the lane allows one invocation
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:29-37`).
4. **The input-copy condition disagrees with the repository.** Manifest `files[]` contains no input,
   but the refreshed catalog pins five differing input copies. F-02 records both sides and the C-2
   disposition (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:24-26`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:62-158`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:1154,1346,1539,1998,2126`).
5. **The gate prediction is false for the measured invocation.** The gate did not reach seal,
   anchor, probe-pin, probe, review, or provenance evaluation; it refused at a member digest
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316_REFRESH_COPIES_SEAL14_PIN_V113.md:32-35`;
   `W316_GATE_RECEIPT.json:1-8`).
6. **Normal governance write-back/audit defaults conflict with the lane's tighter scope.** The stage
   normally calls for a T1 independent audit and `HANDOFF.md` write-back, while C-1 forbids another
   model and the lane permits only its named bytes. No `HANDOFF.md` byte was changed and no
   independent acceptance is claimed (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md:15-37`;
   `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/OUTPUTS.md:3-9`;
   `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7,25-31`).

## Verification and handoff

- The first commit is `d574a4054f054ed51ffc9ecc0ead77264ae8e2ec`; its five staged paths were
  exact, `git diff --cached --check` returned 0, source/staged blob OIDs matched, and the repository
  guard returned PASS.
- The final supplemental static checks measured 19/19 manifest members equal, computed/recorded seal
  equal, design pin equal, anchor/sidecar equal, 27 catalog rows with zero input mismatches, and
  baseline seal/catalog equal. These checks do not upgrade the refused gate receipt.
- The canonical gate was invoked exactly once and returned exit 2; its complete durable receipt is
  `W316_GATE_RECEIPT.json:1-8`.
- No kernel, harness, probe, design, Pine, parity, broker, host, network, or live byte was changed. No
  push, PR, merge, hook bypass, destructive Git action, or other assistant/model invocation occurred
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7,25-39`).
