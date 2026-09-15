# W299 KERNEL probe re-pin report

Date: 2026-09-02
Actor: Codex implementer lane
Status: IMPLEMENTER COMPLETE; pending Lead two-party pin, independent digest verification, reseal,
baseline regeneration, in-repo manifest refresh, and canonical re-drive

## Scope and result

The nine named KERNEL probe variants were mechanically re-derived from the final committed
`mtc_v2/core` tree:

`e8e250589d6b5a887e6f1a77874405836772d4bd`

Every variant contains the exact 119-member base tree plus its existing one-line
`KERNEL_FILE_PATCH`. The base-to-variant member sets are identical and the only changed member in
each variant is `economics.py`. Every `modification.patch` is byte-identical to HEAD, so every
recorded `patch_sha256` is unchanged. `expected_failed_check` and
`expected_first_changed_node` are unchanged for all nine probes.

No core source, Pine, catalog/contract, harness, golden, input, expected, baseline, or seal byte was
changed. Nothing was pushed.

## Digest pairs for the Lead

The Lead must independently recompute these values from the committed variant bytes and must not
copy this lane's measurements.

| Probe | Modified-copy digest | Modification-manifest SHA-256 |
|---|---|---|
| `PROBE-P012-01-A` | `7b93a0dd06421ae979d0dc6736402d778cada45d2fc7aba4767ebb029093d12a` | `a2329ab11a87751862453cad8942332b3b54108c9f294656635a7eb9f849c87e` |
| `PROBE-P012-01-B` | `d8eae81dbcc4648a1a8dafa65c890e713eed965129002118c14330abb6c9aad6` | `cab810b62324678258bea30250788bb8f4c6097d75d50bdf3ad075664beff762` |
| `PROBE-P012-02-A` | `ff4592347f00b7187513665a07c02d4d7108909de9796cb6fd7527da2d4d941f` | `eebbcde982c72aec02584714cfbba0bf10468249576411649a2bbb0617d1240f` |
| `PROBE-P012-04-A` | `dc313ee4328eecaad6ef34408cd4ab4838254589e213e4448c3540f71cf5ba92` | `9f44a7cd0ed4b6984232455bfe118904d05eefa7976f96127caf67a4cdc64102` |
| `PROBE-P012-05-A` | `216152ca35050558068fc24e1d64df7473296a6b7048c1b3515720dbf8f8d294` | `684637b72cf10ceaf740452b46878427bce8dd33855c64ec23670e9e5b9cc81c` |
| `PROBE-P012-05-B` | `009890b989aeba839d40585a6b1a489a1e26ae0928d543fbba56a7b449ac1b79` | `ecb0bc2559c65ed920128adb085ff1c97726f7595ca002748e5c70563c7824da` |
| `PROBE-P012-06-A` | `fa51d604ef31863ae91f932ef32e95b2a9d72a0a924acdb0406fcadc4f371841` | `f54132eda453169414d4e7c16e70edfe257f55ccb3f1ec1c7bfc2f1e59610902` |
| `PROBE-P012-07-A` | `ea91b62f48edbb9ff15072a763f7255daf88c067bcab9645e7d3b4fc5b63e4da` | `c9f81cec21a789f4131f333a501b8260ef8ca3ede884df6b197eef3ab9a6a1e5` |
| `PROBE-P012-08-A` | `48e63ab55bbd160d0d5f2b50747aac65674af91893dc35ce796d6bd1cfc8b95a` | `d976769490645ea5fefefbe7e44b0921807bdc561b3f9e77293601f8068823c9` |

## Per-file pins

The final base `economics.py` SHA-256 is
`2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` for every probe.

| Probe | Patched `economics.py` SHA-256 | Unchanged patch SHA-256 |
|---|---|---|
| `PROBE-P012-01-A` | `77b919ff11b5d8109447135f8d1f4b8e9abc1256270644fd33132036b0b75a17` | `e63171a8789d8f674dfac194e05a050ed0d853cfd59e3f3b1edfb177eb23651c` |
| `PROBE-P012-01-B` | `8f849953ecece375ec5435268208fe8edc3628b93f24658455ae6e4662795cde` | `2dd219c0daaf553ea2a326a7405af2a9ae863e023b50b73b1ed2afc70b3f4b07` |
| `PROBE-P012-02-A` | `2d7f79328ccb7f3f9d8be670fe4fd00c44cf2500bc6684bebbbb37789111dda0` | `ff79c24d66200a0601127da2cc4cbfcb7f58a614f6062e8d40f760a57c87069e` |
| `PROBE-P012-04-A` | `ea81ad343a31b73fd6788a7a400633f34739f933fc8e9ba073dcdaf6efa0db88` | `969dc7c3771cdb73ab74115305a649437b57321b62e0735c87929922c446ae50` |
| `PROBE-P012-05-A` | `855a020f908542256236ee4df4c4a15d66985b01e3b22542a332c90ddf213e5c` | `74a2ca6813bdd032000b3b07d7ac38dca3134433157ecc94e3c533e7581bba89` |
| `PROBE-P012-05-B` | `15fb0998a62bf9faa24958e0567a079b2e6507493a6a60242b6908c83788bc31` | `bb8a7259bce5872c9e41531095c5394048070c30623e9777581f597c24fcc291` |
| `PROBE-P012-06-A` | `3439ce5f4673957773e5794c9a739ece8656e85b3df98fa12ccc30803d4c9180` | `5dd7a081ef14538d5ff21ca24cee2a9ad52056949edf0779fbad6e16346e2e37` |
| `PROBE-P012-07-A` | `19783a5ec51d34952fd4c22a8435758149455e7dda47f12fe6727a3d325a1a46` | `57f9c4d2c0d7003f25ca42c371d74ae9be4c2f6e1a7207bc35a0b6521d49c2c6` |
| `PROBE-P012-08-A` | `51e7a42faeab322234312d38a5bf49351c15ad6c3fb2cf98b469dee931da5264` | `cabe3f20c12a5fd5d730c46d13e26e97133e4680dce711ac32e565ee6eb1e4eb` |

## Implementer verification

- All prerequisite marker files existed before the build: `W283R_DONE.txt`, `W285_DONE.txt`, and
  `W284_DONE.txt`.
- Each probe was built from its own fresh `git -c core.autocrlf=false archive` scratch export of the
  final base tree.
- `git -c core.autocrlf=false apply --check --unidiff-zero` passed for all nine unchanged patches.
- A second full replay independently recomputed the verifier's canonical tree manifests, required
  exact canonical JSON bytes, compared every member byte to a fresh patched export, and returned
  `ALL_9_REPLAYS_PASS`.
- Each replay measured 119 regular files, zero symlinks, no additions/deletions/renames/type changes,
  and exactly one changed path: `economics.py`.
- Diff-scope inspection found zero forbidden paths, zero changed patch files, and zero deleted probe
  members.
- `git diff --check` passed.

The live catalog and sealed in-repo manifest still contain the pre-W299 digest pairs by design.
Therefore a canonical probe/gate run is not claimed in this implementer lane: it must follow the
Lead's independent catalog update, different-family byte verification, seal #12, baseline rebuild,
and in-repo manifest refresh specified in W299 steps 3-6.
