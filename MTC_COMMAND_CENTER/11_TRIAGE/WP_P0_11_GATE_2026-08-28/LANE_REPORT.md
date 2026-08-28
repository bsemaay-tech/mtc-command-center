# WP-P0-11 `P011-LC-GATE-v2` authority re-pin report

Date: 2026-08-28

Branch: `feature/wp-p0-11-kernel-legacy-compatible-20260825`

Worktree: `C:\WPP011_20260825`

Tier: T0 because this evidence gate protects later economic-kernel work. Two independent flagship
audits remain required; the implementer issues no acceptance verdict.

## Outcome

**Gate outcome: STOP.** `P011-LC-GATE-v2` is an owner-authorized authority re-pin and candidate
artifact set. Seven applicable rows remain STOP, and no kernel consolidation, protected
implementation, subject comparison, or live/runtime action was performed.

## Premise 1 - authority diff

| Identity | Git blob OID | CRLF SHA-256 |
|---|---|---|
| v1 pinned P0-09 authority | `f96b53258488eb85b0d67509766c3c19f7bdf0bf` | `6464e6f01a05109816a0433b78ac6eccc50260b77b89093f2444773db6c01068` |
| current-master / v2 P0-09 authority | `1c39ab939dfcf5589e5ec8fba4af8966947a67fc` | `7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249` |

`master` at `85c3e17f97efa1ba83ef9c679de319a50ad3be04` resolves the capability-table
path to blob `1c39ab93...a67fc`. Independent byte hashing reproduced both CRLF hashes.

`git diff f96b5325... 1c39ab93...` reports 119 insertions, 100 deletions, and 93 hunks.
Classification of those hunks found 75 citation-only replacements, 16 source-provenance rewrites
around moved or retired WP-P0-23 surfaces, and two added citation-audit metadata blocks. The latter
two state explicitly that no row claim, canonical rule, chosen implementation, fixture oracle, or
expected value was rewritten. Direct inspection found no rule, oracle, or expected-value change.
Premise 1 therefore holds; no substantive authority change was absorbed into this gate version.

## Stage-1 identities and signature

- Legacy manifest: `1bc01646e9a00a4ee62c22c6ce1416ed03648e97351e792ae82bbbaff95f52d7`.
- Observation schema: `c18fb1622ab38b374d65a1304994f0e9f5d8993f948e75d99694bdfceb5fdb2e`.
- Profiles: Supertrend `c1570317e0dd9ffc2eb9d4ad652891bce65e3ff2007cbbcbba1523ddb33b78f0`;
  Range Filter `35d40915d9813265d1cc1f4474a770471d3ea443e5a67b12ccb4f9e7270944d8`.
- Final receipt: `a31128f1e292c6f70c8204847494e40c38edc9af685f72a21486c90027f61bb1`.
- New external anchor `C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v2.owner-signed.json`:
  `5ab2fd766dec878046ade9e35972ace8eea5c6860f47dc8c719a4b7a55059149`.
- Signature basis: `C:\tmp\LANE_PROMPTS_20260828\OWNER_AUTH_P011_GATE_V2.md`, SHA-256
  `d5da5c81df38de31b629605cd972ce3d9df19185573f6d4018782cae8f2b2ef3`, owner words verbatim:
  **"Bump to v2 now"**.
- **The v1 anchor is retained untouched** at
  `C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v1.owner-signed.json`, SHA-256
  `eb6a600ff9609789465118a217845c7cac6f8b09f7ecaee2a93242f1f16ec15c`.

## Double build

Fresh outputs: `C:\tmp\p011_gate_v2_run1_20260828` and
`C:\tmp\p011_gate_v2_run2_20260828`. Each profile produced 48,077 observations, for 96,154 total.
All canonical artifacts are byte-identical across the two builds:

| Artifact | Run 1 SHA-256 | Run 2 SHA-256 |
|---|---|---|
| `mtc_v2_legacy_sequence.jsonl` | `727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e` | same |
| `final_states.json` | `045f11c34e5713dcec97987f14f26b8e9a72011d44b91806b382680fbe1e622a` | same |
| `row_corroboration.json` | `9d6abe9265f8b332db429c6bc3f8144545902bb03fc44fd60de3bf970a195f0e` | same |
| `baseline_manifest.json` | `62d1ef5fc90b36b6c8caec9388a229ec897dca95ca99f2ba9b979f9c20e6cecc` | same |

The unchanged sequence hash is expected: the authority diff changed citations, not rules or data.
The v2 comparator self-test records 76/76 RED and 76/76 restored GREEN; matrix SHA-256 is
`1bfa108ed6b547af92af6bf08c70da8a7363598278747f78259f3958c88c3a3d`.

## Complete C01-C42 re-verification

Comparison against recorded branch SHA `9e8a69b32a3460c9a08e8977db99bd7dfe4e5788` found every row behavior
and disposition identical: **33 GREEN, 7 STOP, 2 policy-only (C25/C27), 134/134 expected leaves,
33 mutation REDs, and 69 RED mismatches**.

- C28-C30 remain STOP because no executable Pine producer was authorized; no Pine was run.
- C32/C34/C35/C42 remain authority-contradiction STOPs.
- No STOP row turned GREEN or changed behavior in the other direction.
- Canonical row hashes: results `1cb5b6ec...7555b`, corroboration `e17f8841...08c8a`, unresolved
  `a89d46ef...dcd48`, batch `2767f39d...4967e`.
- Contract mutations remain 3 FAIL + 1 STOP. Structural evidence records 17/17 expected attacks
  and 17/17 expected restorations, SHA-256 `121a96a0...55a7e`.

## Scope and audit boundary

Writes are confined to this gate package, the new v2 external anchor, and the Markdown hours
ledger. Implementation A/B, Pine, `MTC_V2`, backtest, adapters, kernel, schemas, host, broker,
venue, credentials, and live/testnet surfaces were not edited or invoked. No live dependency was
present. The package is committed and pushed only as an audit candidate; two independent flagship
audits decide any later acceptance, and the gate remains **STOP**.
