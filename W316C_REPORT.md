# W316C manifest #14b and observed-artifact refresh report

Date: 2026-09-03  
Actor: Codex lane  
Status: **REFUSED BEFORE PROBE EVALUATION**  
Canonical refusal count: **1**

The lane preconditions were measured before writes on the required worktree and branch at the
required clean start HEAD `443457d7`; the predecessor marker contained `exit=0` and the Lead marker
existed. These were the four start conditions specified by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316C_MANIFEST_14B_OBSERVED_REFRESH.md:5-8`;
`C:\tmp\LANE_PROMPTS_20260828\W316B_DONE.txt:1`).

The permitted write scope is the copied manifest, the ten named observed artifacts, the two
receipts, and this report (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316C_MANIFEST_14B_OBSERVED_REFRESH.md:23-43`).

## Bundle SHA-256 comparison

The manifest was copied byte-for-byte. Its bundle and in-repo SHA-256 values are equal. Every
other named member also compared equal before observe mode: catalog, derivations, anchor, generated
anchor sidecar bytes, 17 goldens, and 17 inputs. These are the exact categories required by the
lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316C_MANIFEST_14B_OBSERVED_REFRESH.md:23-27`).

| Item | Bundle SHA-256 | In-repo SHA-256 | Equal |
|---|---|---|---|
| `contracts/CONTRACT_TABLES_MANIFEST.json` | `f89cee3a11cd01d3a8c785c262073df3e2441d95027d472b153e800b7454cca2` | `f89cee3a11cd01d3a8c785c262073df3e2441d95027d472b153e800b7454cca2` | yes |
| `contracts/scenario_catalog.json` | `555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14` | `555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14` | yes |
| `contracts/DERIVATIONS.md` | `8eeacb17be2a1d3d5c6f4cfb741dccde13a864f91ab3152aa04d5a115330dcd2` | `8eeacb17be2a1d3d5c6f4cfb741dccde13a864f91ab3152aa04d5a115330dcd2` | yes |
| `contracts/implementation_anchor.json` | `7ddfda98a88cd1d1e1c0d8853974b10cbc51b3e240d7bf4b9635d37559b18b2a` | `7ddfda98a88cd1d1e1c0d8853974b10cbc51b3e240d7bf4b9635d37559b18b2a` | yes |
| `contracts/implementation_anchor.json.sha256` (generated expected bytes) | `6929eb7b3c388c4ce081877158c8d06480a318dbb9afab15b0131ae30340b09f` | `6929eb7b3c388c4ce081877158c8d06480a318dbb9afab15b0131ae30340b09f` | yes |
| `golden/corrected_vnext/RULE2-01-GREEN.json` | `38b79ef1cd114724c63e665f3f0e18a478e0693b79ee49356426561a6aaa597a` | `38b79ef1cd114724c63e665f3f0e18a478e0693b79ee49356426561a6aaa597a` | yes |
| `golden/corrected_vnext/RULE2-01-RED.json` | `74f6f80cd44f7f980c3f0b332681bcc34e0a4f5a21bf567c84a17b14aacc38fa` | `74f6f80cd44f7f980c3f0b332681bcc34e0a4f5a21bf567c84a17b14aacc38fa` | yes |
| `golden/corrected_vnext/RULE2-02-GREEN.json` | `aefa016537dd342e307a974c97b513fcbd1c9ef140ef7bfaee5a62b648b6a146` | `aefa016537dd342e307a974c97b513fcbd1c9ef140ef7bfaee5a62b648b6a146` | yes |
| `golden/corrected_vnext/RULE2-02-RED.json` | `b6b4e4bfb21c162cdee84e49762357f543afc6bf72320765748d70bdc030388d` | `b6b4e4bfb21c162cdee84e49762357f543afc6bf72320765748d70bdc030388d` | yes |
| `golden/corrected_vnext/RULE2-03-GREEN.json` | `c10b5e71d7c84ccdc8668cb081ba5b394d3fbeba2119a0a53eeb96c9f4fea880` | `c10b5e71d7c84ccdc8668cb081ba5b394d3fbeba2119a0a53eeb96c9f4fea880` | yes |
| `golden/corrected_vnext/RULE2-03-RED.json` | `e04ddf0cdd14c68076ddd1b081467ee21fafb836d7a51751990bfb361b1bb724` | `e04ddf0cdd14c68076ddd1b081467ee21fafb836d7a51751990bfb361b1bb724` | yes |
| `golden/corrected_vnext/RULE2-04-GREEN.json` | `7309d4cbe1445cea9d8ccb4ca44bc91e81e45fd8c157fa3daed3b295561ba7f7` | `7309d4cbe1445cea9d8ccb4ca44bc91e81e45fd8c157fa3daed3b295561ba7f7` | yes |
| `golden/corrected_vnext/RULE2-04-RED.json` | `50a990c2005ade1fa5db41cdd00f7bd194e0e89db1f3cd1b24d3d71e693aa85c` | `50a990c2005ade1fa5db41cdd00f7bd194e0e89db1f3cd1b24d3d71e693aa85c` | yes |
| `golden/corrected_vnext/RULE2-05-GREEN.json` | `26bbb48caf2fb2c5f9f13f08f23664ede89f31c9bfa337d9b878ab68ffa19798` | `26bbb48caf2fb2c5f9f13f08f23664ede89f31c9bfa337d9b878ab68ffa19798` | yes |
| `golden/corrected_vnext/RULE2-05-RED.json` | `88197710a9a767a130d794dbbebe56a81fe9ef990081d3c15171b574e25dbc9a` | `88197710a9a767a130d794dbbebe56a81fe9ef990081d3c15171b574e25dbc9a` | yes |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | `c05a51eb1e03b8864c495a3d48d3ccd722a2d598489038f055d755f32cb31de0` | `c05a51eb1e03b8864c495a3d48d3ccd722a2d598489038f055d755f32cb31de0` | yes |
| `golden/corrected_vnext/RULE2-06-GREEN.json` | `45f10ddb072e19b2dae4473e09c6af74268bef11bb64247eea94dc8d0538cda2` | `45f10ddb072e19b2dae4473e09c6af74268bef11bb64247eea94dc8d0538cda2` | yes |
| `golden/corrected_vnext/RULE2-06-RED.json` | `9d9d3a9748571d63c8790d9b7ef5df398ed945f75c59b7148975debfe167a581` | `9d9d3a9748571d63c8790d9b7ef5df398ed945f75c59b7148975debfe167a581` | yes |
| `golden/corrected_vnext/RULE2-07-GREEN.json` | `1acd5a74f98d22165971486d6a2ede029f58bf984f85181617055ca473644a4a` | `1acd5a74f98d22165971486d6a2ede029f58bf984f85181617055ca473644a4a` | yes |
| `golden/corrected_vnext/RULE2-07-RED.json` | `e4d966eee8587ca3d645e3abd9a98847daf8f41a3743250563624975f926435b` | `e4d966eee8587ca3d645e3abd9a98847daf8f41a3743250563624975f926435b` | yes |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `08a559422eca70cb302f1381f2abbd409dd3c8482fdb58db47cdda5528e4de32` | `08a559422eca70cb302f1381f2abbd409dd3c8482fdb58db47cdda5528e4de32` | yes |
| `golden/corrected_vnext/RULE2-08-RED.json` | `2157c03fc52daa9183d14e5a1552d6dec58eb4d90024701bd49abb7487f98c4b` | `2157c03fc52daa9183d14e5a1552d6dec58eb4d90024701bd49abb7487f98c4b` | yes |
| `contracts/inputs/RULE2-01-GREEN.json` | `996cbef54286db4d9bda23af36dad54329073399025355ad6b497fa38deb8107` | `996cbef54286db4d9bda23af36dad54329073399025355ad6b497fa38deb8107` | yes |
| `contracts/inputs/RULE2-01-RED.json` | `ac61cd315d29981a83f0ebcf994e0cbd8d7fcc7ea7e76301ed5f9c7757f0bc36` | `ac61cd315d29981a83f0ebcf994e0cbd8d7fcc7ea7e76301ed5f9c7757f0bc36` | yes |
| `contracts/inputs/RULE2-02-GREEN.json` | `9c9e822dd7c1f5011c0ac7d87e301b2148b0086c8329f8fd6ddb8cd43f36c2af` | `9c9e822dd7c1f5011c0ac7d87e301b2148b0086c8329f8fd6ddb8cd43f36c2af` | yes |
| `contracts/inputs/RULE2-02-RED.json` | `77349d5eed0b241c5489f0ac41e7e3f246c65b072ec7aead314e2bfd6228ee2d` | `77349d5eed0b241c5489f0ac41e7e3f246c65b072ec7aead314e2bfd6228ee2d` | yes |
| `contracts/inputs/RULE2-03-GREEN.json` | `484f085f198891debb83192976458258ba797d7742e36cc52af3c4189d60d65f` | `484f085f198891debb83192976458258ba797d7742e36cc52af3c4189d60d65f` | yes |
| `contracts/inputs/RULE2-03-RED.json` | `6d7c760889e772cba939c88935a3dde64e50fdc6018b5894d0c2e24ab58b0f6b` | `6d7c760889e772cba939c88935a3dde64e50fdc6018b5894d0c2e24ab58b0f6b` | yes |
| `contracts/inputs/RULE2-04-GREEN.json` | `178a0fe11bf27991a9fbc53bfa3cca339099ea6a8b62d5f6380cd9cc74b27b3a` | `178a0fe11bf27991a9fbc53bfa3cca339099ea6a8b62d5f6380cd9cc74b27b3a` | yes |
| `contracts/inputs/RULE2-04-RED.json` | `49e9837646daab0cf289933a6d80143427f674ca9d17d18cde1c9fa0d40f42b7` | `49e9837646daab0cf289933a6d80143427f674ca9d17d18cde1c9fa0d40f42b7` | yes |
| `contracts/inputs/RULE2-05-GREEN.json` | `ffa8487767b21c8f973eac93b38af2586448f929edb41bcdd3fe201824a73b13` | `ffa8487767b21c8f973eac93b38af2586448f929edb41bcdd3fe201824a73b13` | yes |
| `contracts/inputs/RULE2-05-RED.json` | `baa8683a2577a9c53dafffbe16013c23d2e69adb2084ce460db3ab4941c78acd` | `baa8683a2577a9c53dafffbe16013c23d2e69adb2084ce460db3ab4941c78acd` | yes |
| `contracts/inputs/RULE2-06-EQUAL-PRICE-RED.json` | `0c65c82b911f3a510d074df00bc81335bb3397697e96f422f5c05267e4ea085c` | `0c65c82b911f3a510d074df00bc81335bb3397697e96f422f5c05267e4ea085c` | yes |
| `contracts/inputs/RULE2-06-GREEN.json` | `c334b07011bd538e7b9d02de451abbd5f389da8cf7392da64fed7dfc941dd4e2` | `c334b07011bd538e7b9d02de451abbd5f389da8cf7392da64fed7dfc941dd4e2` | yes |
| `contracts/inputs/RULE2-06-RED.json` | `8c62e57e0584207d99ab6d581a91535d341b65df46b362dc402a48da702f1f68` | `8c62e57e0584207d99ab6d581a91535d341b65df46b362dc402a48da702f1f68` | yes |
| `contracts/inputs/RULE2-07-GREEN.json` | `be3bb8f1b666a006ff59b8a4c1b7e60764bb9065b8b129a0ea36cbadbd9c81a6` | `be3bb8f1b666a006ff59b8a4c1b7e60764bb9065b8b129a0ea36cbadbd9c81a6` | yes |
| `contracts/inputs/RULE2-07-RED.json` | `8cd6299bb2322add2d651cc7cfeb404cbc774cd45f8a4426bde0caae17ff182e` | `8cd6299bb2322add2d651cc7cfeb404cbc774cd45f8a4426bde0caae17ff182e` | yes |
| `contracts/inputs/RULE2-08-GREEN.json` | `6c349e8bf180e63dddb34834aa13098f9d723aecdff6b02d328aa6b55996a939` | `6c349e8bf180e63dddb34834aa13098f9d723aecdff6b02d328aa6b55996a939` | yes |
| `contracts/inputs/RULE2-08-RED.json` | `4bc3cc7402e1eb8dde4416fd698a9d2a46b5477aa9d5e7a10061aa7f8b281c4d` | `4bc3cc7402e1eb8dde4416fd698a9d2a46b5477aa9d5e7a10061aa7f8b281c4d` | yes |

## Committed observed-artifact snapshot before observe mode

The pre-run snapshot contained 34 files. The ten rows later changed are independently corroborated
by the prior gate's committed/live digest pairs (`W316B_GATE_REPORT.md:165-174`).

| Observed file | Before SHA-256 |
|---|---|
| `1.0.0/RULE2-01-GREEN.json` | `87eb63912e6ee20688fed3c0a89aff6feb4cc2c3b9d3379f2929d619ca7e3a90` |
| `1.0.0/RULE2-01-RED.json` | `17b6c62e837b71754fa99f0373d6874583fba86c0120410b6c309f7c10ade3d7` |
| `1.0.0/RULE2-02-GREEN.json` | `a0d248f3b743fcf16aa8adc30ec7dee0c3aa921456daa37ff7189dc19c1e09b3` |
| `1.0.0/RULE2-02-RED.json` | `4fb71f522b9c572b084a1ddd2979ca77d22eebf679301904c883b408659c22d6` |
| `1.0.0/RULE2-03-GREEN.json` | `881666b1121994efedf6223c3029f0faf4aaed5cc907ee1fbe3012883b1c780c` |
| `1.0.0/RULE2-03-RED.json` | `908611f184d39f14c2a0e5d5bac2676942c067feb6e346905ddb5bb04f1cc30c` |
| `1.0.0/RULE2-04-GREEN.json` | `56ce32e633318108a2a8818e40edabcd3b1a368332a30f53057fb44aacf78cde` |
| `1.0.0/RULE2-04-RED.json` | `a2de179a98790cced40081a339d0597ad77b55b5a56b9c9fe1728eb27982b273` |
| `1.0.0/RULE2-05-GREEN.json` | `80ba0a807f0297a050a6e9108b811df2309a5e2a060289c521716b536d94c125` |
| `1.0.0/RULE2-05-RED.json` | `74b3a00ae616e2f3695cf2bc002a26e2636487f5cc7bdc5ac3c9a581ea193770` |
| `1.0.0/RULE2-06-EQUAL-PRICE-RED.json` | `68a5c2dc469564e349def87cc7b4d8c92a44be098599fed3c3cda2496b6378f1` |
| `1.0.0/RULE2-06-GREEN.json` | `503e38461805cfdab8df0ec891fc580a918db84b107f5c60bb91069699352cd8` |
| `1.0.0/RULE2-06-RED.json` | `7487f91c55252ef11b38d9e467a7a6fe4dfec522bf6b731c1012bae3cad1e1b4` |
| `1.0.0/RULE2-07-GREEN.json` | `90bdd44db8c79daf9587953d6dc7498cb567e5d8d3420a53942810a6c487ef94` |
| `1.0.0/RULE2-07-RED.json` | `6b241a6e10aa1b02185d2a71389178ef68ddf78ddd3c294214163e7813589668` |
| `1.0.0/RULE2-08-GREEN.json` | `1cd41861f6b665f7253919bef718fc379d135edbbb7d8b00178f40da6e53b06a` |
| `1.0.0/RULE2-08-RED.json` | `999a1906c2d85076b41def95bde9458c6e20a33d72fddabf3d67547e15f614f7` |
| `2.0.0/RULE2-01-GREEN.json` | `1113f66d7d88f797b3323a1b57b837c4d4aa5f6dd6f62d20228888887f4c3e0b` |
| `2.0.0/RULE2-01-RED.json` | `fbd5992e00068c3eb93b381a227e5a02a86b781fad6d88095e006b056d0789af` |
| `2.0.0/RULE2-02-GREEN.json` | `9917fc19e532b8270627ac3441b57595de8860f4514029a9165a404982a816f7` |
| `2.0.0/RULE2-02-RED.json` | `ba2754f634ad9cb4863bf4bb64f0934625fd7c8baa32a479a34d6849620974dc` |
| `2.0.0/RULE2-03-GREEN.json` | `aa83ed9e5a890e29e44f096122dd7979bc907c7c7b4428e192842c1129411fa1` |
| `2.0.0/RULE2-03-RED.json` | `a1264b700be7d1f802b76e7aa30547e7b172889c6db82a532e33f42f7d9ac1f2` |
| `2.0.0/RULE2-04-GREEN.json` | `4db68f72f05d8838b91f797c20aedee7f8c21a4e6e14716db381bba91dc94263` |
| `2.0.0/RULE2-04-RED.json` | `121f5992a4f646144919bf8648db2ad27a322cffc6ae799d19eb76e1c9935c7b` |
| `2.0.0/RULE2-05-GREEN.json` | `cc0e13be73973452f5c6fe4a62f32ed632cfcee44ad7bce08009bde7dca7718c` |
| `2.0.0/RULE2-05-RED.json` | `68aba58f34e5c27bd0bdbaa6380eecb5a2077dcbd510ca8f9831083372f98d2c` |
| `2.0.0/RULE2-06-EQUAL-PRICE-RED.json` | `02ee55725025424718166167e23156a8ad132f6a9add2a8e3ab019a4f0f47c45` |
| `2.0.0/RULE2-06-GREEN.json` | `bcb54b660996f5593166c90cb5e577e31057d8662eceb0ef6743066d7791e619` |
| `2.0.0/RULE2-06-RED.json` | `c05cdf34e3138934024adb6dafa5e33f3e6b3cbf82bec69e9be37e2319ad27e8` |
| `2.0.0/RULE2-07-GREEN.json` | `f1b0a077548e253522d3bc743ed88e4418708fd834e644003ec4eaf59ba8d749` |
| `2.0.0/RULE2-07-RED.json` | `ae1ffc99de661571d4c575c062f1ab6fea185e018d61c29f275867829b02df92` |
| `2.0.0/RULE2-08-GREEN.json` | `cb1805a1f8cffcd27dd782725ae9bb19321125d9a51a1109e889a20ece2e7544` |
| `2.0.0/RULE2-08-RED.json` | `3a7ea9774b288b23f9c5f30a5c420ee53fc40b1b8d986bc1f61800dbefece46d` |

## Observe materialization

Observe mode was invoked once with the supported `--output` option. It returned exit 0, wrote a
non-accepting observe receipt, and enumerated the scenario results
(`W316C_OBSERVE_RECEIPT.json:508-515`). Exactly the ten lane-named observed artifacts changed;
the before/live pairs below are also present in the immediately preceding canonical evidence
(`W316B_GATE_REPORT.md:165-174`). No other observed file differed after the run.

| Changed observed file | Before SHA-256 | After SHA-256 |
|---|---|---|
| `1.0.0/RULE2-06-RED.json` | `7487f91c55252ef11b38d9e467a7a6fe4dfec522bf6b731c1012bae3cad1e1b4` | `a6bb6f4494d61cfdc1a1580a168d2f3132a2a2b4ea8c51e21bef24e359a0321b` |
| `2.0.0/RULE2-06-RED.json` | `c05cdf34e3138934024adb6dafa5e33f3e6b3cbf82bec69e9be37e2319ad27e8` | `ff8844dbd9384a0707e79437ecfa70c6b7b6729983c6b8889ae52aed7af2d1b0` |
| `1.0.0/RULE2-06-EQUAL-PRICE-RED.json` | `68a5c2dc469564e349def87cc7b4d8c92a44be098599fed3c3cda2496b6378f1` | `9359db82501e0c7afb241dd8c0380edb15f92d06ae8e80426ea0cf88e1527daf` |
| `2.0.0/RULE2-06-EQUAL-PRICE-RED.json` | `02ee55725025424718166167e23156a8ad132f6a9add2a8e3ab019a4f0f47c45` | `81c21f6310cf81401e4bafedeefdce34fbf69a6f2089d983edbeec6416503230` |
| `1.0.0/RULE2-06-GREEN.json` | `503e38461805cfdab8df0ec891fc580a918db84b107f5c60bb91069699352cd8` | `83bf72adae56c27cbad59f085fde295480d79b47ab7e9a027bf524faec7f35cf` |
| `2.0.0/RULE2-06-GREEN.json` | `bcb54b660996f5593166c90cb5e577e31057d8662eceb0ef6743066d7791e619` | `939d02522a2da18945f80fe4d564849bcefe96958aae635453e513da0b796dd7` |
| `1.0.0/RULE2-08-RED.json` | `999a1906c2d85076b41def95bde9458c6e20a33d72fddabf3d67547e15f614f7` | `b85b7cd9f4cebffeb10dbacd53242ad75efeddce3b0df92126636e5e03411e52` |
| `2.0.0/RULE2-08-RED.json` | `3a7ea9774b288b23f9c5f30a5c420ee53fc40b1b8d986bc1f61800dbefece46d` | `e9e3086ca88aa6dfe07ae87bfc3a720f6473c23d9270ba3788dabf2a3dd21e12` |
| `1.0.0/RULE2-08-GREEN.json` | `1cd41861f6b665f7253919bef718fc379d135edbbb7d8b00178f40da6e53b06a` | `a5fafd305ee8a0b4c64f646219f077c23990fcc95f2bf927566f35d7adc2dd2f` |
| `2.0.0/RULE2-08-GREEN.json` | `cb1805a1f8cffcd27dd782725ae9bb19321125d9a51a1109e889a20ece2e7544` | `94f8caa71209039939a23449f65e7e6c70c025b1ed2906c5047f26edafe54e32` |

## Canonical gate

The prescribed full-gate command was invoked exactly once. It returned exit 2 before the comparison
pipeline and emitted one singular refusal with the refused claim label
(`W316C_GATE_RECEIPT.json:2-7`). The harness did not write the requested output file on this early
exception, so the stdout JSON emitted by that one invocation was saved verbatim as
`W316C_GATE_RECEIPT.json`; no second gate invocation occurred. The verifier writes `--output` only
inside its normal `try` path but writes early `GateRefusal` JSON only to stdout
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4151-4155`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4164-4171`).

## Full refusal list, verbatim

The receipt has no `refusals` array. Its complete singular refusal receipt is quoted verbatim
(`W316C_GATE_RECEIPT.json:1-8`):

```json
{
  "claim_label": "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusal": {
    "check_id": "EXPECTED_PROVENANCE_EXCEPTION_INVALID",
    "detail": "record base=108ea066a710ff7ef5c09246903fe3d523da1d56 manifest base=5e8e579410ee55008bfd2d2d85054fd1d782f32c"
  }
}
```

## Unexpected refusal detail

| Refusal | Pointer | First value | Second value |
|---|---|---|---|
| `EXPECTED_PROVENANCE_EXCEPTION_INVALID` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:18` | exception-record base `108ea066a710ff7ef5c09246903fe3d523da1d56` | manifest base `5e8e579410ee55008bfd2d2d85054fd1d782f32c` (`CONTRACT_TABLES_MANIFEST.json:553,564`) |

No refusal was repaired, as required for an unexpected result
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316C_MANIFEST_14B_OBSERVED_REFRESH.md:37-39`).

## Probe table

The canonical receipt contains no probe results because the gate refused during expected-source
provenance validation. A DETECTED or NOT DETECTED result, measured failed check, or measured first
changed node for this run is therefore **NOT VERIFIED**; prior-run outcomes are not substituted
(`W316C_GATE_RECEIPT.json:1-8`; `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:20-23`). The
expected checks below come from the current sealed catalog.

| Probe | Result | Expected failed check | Measured failed check | First changed node |
|---|---|---|---|---|
| `PROBE-P012-01-A` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2207`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-01-B` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2228`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-02-A` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2249`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-03-A` | NOT VERIFIED (not evaluated) | `RECORD_IDENTITY_PREFLIGHT` (`scenario_catalog.json:2270`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-04-A` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2291`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-05-A` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2312`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-05-B` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2333`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-06-A` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2354`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-07-A` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2375`) | NOT VERIFIED | NOT VERIFIED |
| `PROBE-P012-08-A` | NOT VERIFIED (not evaluated) | `CORRECTED_EXPECTATION` (`scenario_catalog.json:2396`) | NOT VERIFIED | NOT VERIFIED |

## Discrepancies

1. The prompt predicts five residual refusals after the manifest and observed refresh. The measured
   gate instead stopped earlier with one `EXPECTED_PROVENANCE_EXCEPTION_INVALID` refusal because
   `expected_provenance_exceptions.json` still records base `108ea066...` while manifest #14b records
   `5e8e5794...` (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316C_MANIFEST_14B_OBSERVED_REFRESH.md:37-39`;
   `W316C_GATE_RECEIPT.json:4-7`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:18`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:553,564`).
2. The prompt requires the full refusal list and probe table. The actual receipt contains a singular
   `refusal` and no probe data, so this report quotes the singular refusal and marks every current-run
   probe outcome NOT VERIFIED rather than reusing earlier results
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316C_MANIFEST_14B_OBSERVED_REFRESH.md:35-40`;
   `W316C_GATE_RECEIPT.json:1-8`; `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:20-23`).
3. The full-gate command accepted `--output`, but an early `GateRefusal` bypassed the output-writing
   branch and wrote only stdout. The already-emitted stdout was therefore saved by hand as the gate
   receipt, without a second invocation
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4151-4155`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4164-4171`).
4. The prompt describes the anchor sidecar as a bundle member, but the bundle contains no literal
   `.sha256` sidecar. The comparison used the established generated expected bytes: lowercase SHA-256
   of the bundle anchor followed by one LF (`W316B_GATE_REPORT.md:25-31`).

No kernel, harness, golden, input, catalog, probe, design, Pine, parity, broker, host, network, or
live-trading byte was intentionally changed beyond the exact lane-named manifest and observed paths
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316C_MANIFEST_14B_OBSERVED_REFRESH.md:17-20,41-43`). No push,
PR, merge, destructive Git operation, or other assistant/model invocation occurred
(`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7,25-36`).
