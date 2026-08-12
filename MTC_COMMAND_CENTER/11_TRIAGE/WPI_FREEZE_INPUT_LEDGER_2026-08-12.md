# WP-I Freeze Input Ledger - 2026-08-12

## Scope and method

This ledger reconciles the freeze-time inputs required by `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_FREEZE_INPUT_LEDGER.md`. I read current local bytes only, used read-only hashing/search, did not contact the host, did not mutate git, and did not edit any block-byte file.

Current local file identities used as anchor evidence:

| File | Local size/hash evidence |
|---|---|
| `WPI_BLOCKS_DRAFT/RP6-P0.sh` | `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`, matching the current RP6 identity row in `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:14`. |
| `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` | `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:16`. |
| `WPI_BLOCKS_DRAFT/run_p0.sh` | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:31`. |
| `WPI_BLOCKS_DRAFT/run_ro.sh` | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:32`. |
| `transport_runner.ps1` | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:33`. |
| `TRANSPORT_PLAN.tsv` | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:34`. |
| `remote_setup_wpi.sh` | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:35`. |
| `remote_extract_verify_wpi.sh` | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:36`. |
| `remote_close_tree_wpi.sh` | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:37`. |
| `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` | `22954e2f41e4ab21c04eff9ad51abdd657f628892f8dc81c983b6473f9c85bcd`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:24`. |
| `composite_pathproof.py` | `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:20`. |
| `pathscope_prover.py` | `890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`, matching `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:22`. |

Status meanings:

- `FILLED`: exact local consumer value is populated.
- `LITERAL-MARKER`: one or more current consumers still contain `<PIN-AT-FREEZE>` or `<ALLOCATE-AT-DISPATCH>`.
- `MISSING-CONSUMER`: no current consumer was found.
- `CONTRADICTED`: current records disagree in a way that changes the contract.
- `REQUIRES-HOST - not determinable locally`: the real value must come from deployment host state, credentials, mount topology, or dispatch-time execution evidence.

## Ledger table

| ID | Freeze input | Status | Consumers and reconciliation |
|---:|---|---|---|
| 1 | Allocation base `BASE_RUN` | LITERAL-MARKER | `run_p0.sh:113`, `run_ro.sh:107`, `transport_runner.ps1:80`, and `TRANSPORT_PLAN.tsv:2-13` still use `<ALLOCATE-AT-DISPATCH>`. R3 requires one allocation base for both stage names at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:40` and append-only burn-ledger handling at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:139-147`. |
| 2 | `REMOTE_BASE` | LITERAL-MARKER | `run_p0.sh:114`, `run_ro.sh:108`, `transport_runner.ps1:81`, and `TRANSPORT_PLAN.tsv:2-13` still use `<ALLOCATE-AT-DISPATCH>`. Setup consumes one remote base arg at `remote_setup_wpi.sh:221` and derives the work root at `remote_setup_wpi.sh:442`. |
| 3 | P0 `RUNID` | LITERAL-MARKER | `run_p0.sh:117` and `TRANSPORT_PLAN.tsv:5,8` still use `<ALLOCATE-AT-DISPATCH>-P0`. R3 requires allocation before final freeze at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:118` and `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:139-147`. |
| 4 | RO `RUNID` | LITERAL-MARKER | `run_ro.sh:111` and `TRANSPORT_PLAN.tsv:6,9` still use `<ALLOCATE-AT-DISPATCH>-RO`. R3 requires the same allocation family for P0 and RO at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:40`. |
| 5 | Derived evidence and runkit paths `EV_PARENT`, `EV_RUNKIT`, `EV_DIR`, `EV_LOG` | LITERAL-MARKER | P0 derives them from placeholder allocation at `run_p0.sh:118-123`; RO derives them at `run_ro.sh:112-115`; transport retrieval and bind paths still carry placeholders at `TRANSPORT_PLAN.tsv:10-13`. |
| 6 | RP7 fixed evidence root `WPI_FIXED_EVIDENCE_ROOT` | LITERAL-MARKER | RP7 literal remains `<PIN-AT-FREEZE>` at `RP7-WPI-RO.sh:116`. RP7 rejects the literal and requires `EV_DIR` to descend under it at `RP7-WPI-RO.sh:916-921`. FAM-03 requires this to be derived from the frozen allocation at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:363-372` and is owner-ratified at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:396-398`. The proof tool emits freeze input/member/conservation records at `composite_pathproof.py:2542`, `composite_pathproof.py:2728`, and `composite_pathproof.py:2743`. |
| 7 | Numeric execution identity pins `P0_EXPECT_UID`, close/setup `EXPECT_UID`, close/setup `EXPECT_GID` | REQUIRES-HOST - not determinable locally | P0 wrapper has `P0_EXPECT_UID='<PIN-AT-FREEZE>'` at `run_p0.sh:131`; setup has `EXPECT_UID` and `EXPECT_GID` markers at `remote_setup_wpi.sh:144-145`; close has the same marker class at `remote_close_tree_wpi.sh:202-203`. Setup rejects unfilled identity pins at `remote_setup_wpi.sh:200-217`; close rejects them at `remote_close_tree_wpi.sh:288-291`. |
| 8 | `P0_ATTESTED_USER_NS` | REQUIRES-HOST - not determinable locally | Embedded RP6 literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:266`; wrapper copy is `<PIN-AT-FREEZE>` at `run_p0.sh:151` and exported at `run_p0.sh:237-240`. RP6 requires wrapper presence at `RP6-P0.sh:691-700`, rejects marker grammar at `RP6-P0.sh:707-724`, requires embedded/wrapper equality at `RP6-P0.sh:733-752`, and compares live state at `RP6-P0.sh:1390-1393`. |
| 9 | `P0_ATTESTED_MNT_NS` | REQUIRES-HOST - not determinable locally | Embedded RP6 literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:267`; wrapper copy is `<PIN-AT-FREEZE>` at `run_p0.sh:152` and exported at `run_p0.sh:237-240`. Same RP6 presence, grammar, equality, and live-compare consumers apply at `RP6-P0.sh:691-724`, `RP6-P0.sh:733-752`, and `RP6-P0.sh:1390-1393`. |
| 10 | `P0_ATTESTED_PID_NS` | REQUIRES-HOST - not determinable locally | Embedded RP6 literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:268`; wrapper copy is `<PIN-AT-FREEZE>` at `run_p0.sh:153` and exported at `run_p0.sh:237-240`. Same RP6 presence, grammar, equality, and live-compare consumers apply at `RP6-P0.sh:691-724`, `RP6-P0.sh:733-752`, and `RP6-P0.sh:1390-1393`. |
| 11 | `P0_ATTESTED_NET_NS` | REQUIRES-HOST - not determinable locally | Embedded RP6 literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:269`; wrapper copy is `<PIN-AT-FREEZE>` at `run_p0.sh:154` and exported at `run_p0.sh:237-240`. Same RP6 presence, grammar, equality, and live-compare consumers apply at `RP6-P0.sh:691-724`, `RP6-P0.sh:733-752`, and `RP6-P0.sh:1390-1393`. |
| 12 | `P0_ATTESTED_ROOT_MOUNT_ID` | REQUIRES-HOST - not determinable locally | Embedded RP6 literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:270`; wrapper copy is `<PIN-AT-FREEZE>` at `run_p0.sh:155` and exported at `run_p0.sh:237-240`. RP6 rejects marker grammar at `RP6-P0.sh:707-724`, requires equality at `RP6-P0.sh:733-752`, and compares canonical root mount identity at `RP6-P0.sh:1394-1414`. |
| 13 | RP7 mount projection digest `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` / wrapper `WPI_ATTESTED_MOUNTINFO_SHA256` | REQUIRES-HOST - not determinable locally | RP7 fixed literal is `<PIN-AT-FREEZE>` at `RP7-WPI-RO.sh:96`; wrapper copy is `<PIN-AT-FREEZE>` at `run_ro.sh:142`; RP7 requires 64 hex and equality at `RP7-WPI-RO.sh:891-892`. R3 states this value fills both copies at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:41`. |
| 14 | Resolved trusted system Python and `python3` tool-map entry | REQUIRES-HOST - not determinable locally | RP6 fixed trusted Python is `<PIN-AT-FREEZE>` at `RP6-P0.sh:278`; RP7 fixed trusted Python is `<PIN-AT-FREEZE>` at `RP7-WPI-RO.sh:107`; R3 requires the same resolved non-symlink path for RP6, RP7, and both `python3` map entries at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:42`. RP6 requires `python3` to equal `P0_FIXED_TRUSTED_PYTHON` at `RP6-P0.sh:617-623`; RP7 requires the same equality at `RP7-WPI-RO.sh:880-881`. |
| 15 | `P0_VENV_ROOT` exact candidate root | FILLED | `run_p0.sh:135` is `/opt/mtc-bridge/venvs/2ce41e34d72781f5670628c9489127845272672d851d392cab36fe990470321b`. RP6 validates the supplied root at `RP6-P0.sh:488-515`, derives its interpreter at `RP6-P0.sh:759`, and asserts it before execution at `RP6-P0.sh:1871-1872`. FAM-02 is owner-ratified at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:396-398`, with the exact string recorded at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:721`. |
| 16 | `WPI_UNIT_FRAGMENT_SHA256` | LITERAL-MARKER | Wrapper copy is `<PIN-AT-FREEZE>` at `run_ro.sh:130`; RP7 expects and checks the unit fragment digest input at `RP7-WPI-RO.sh:855`. |
| 17 | `WPI_VERIFY_LOCK_SHA256` | FILLED | Wrapper copy is `36ce5ef90c8f83562c03ec1abe488e4a3f92fde91b97bb586552953327e81348` at `run_ro.sh:144`; RP7 accepts the wrapper value at `RP7-WPI-RO.sh:895-896` and later uses isolated `/usr/bin/python3 -I -S` lock parsing at `RP7-WPI-RO.sh:1206-1273`. |
| 18 | Tool pin `stat` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:289`; RP6 map binds it at `RP6-P0.sh:542`; RP7 shared map must include `stat=/usr/bin/stat` form under the exact map rules at `RP7-WPI-RO.sh:867-888`. R3 requires shared P0/RP7 entries to be identical at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 19 | Tool pin `readlink` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:290`; RP6 map binds it at `RP6-P0.sh:543`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 20 | Tool pin `env` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:291`; RP6 map binds it at `RP6-P0.sh:544`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 21 | Tool pin `find` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:292`; RP6 map binds it at `RP6-P0.sh:545`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 22 | Tool pin `sha256sum` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:293`; RP6 map binds it at `RP6-P0.sh:546`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 23 | Tool pin `systemctl` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:294`; RP6 map binds it at `RP6-P0.sh:547`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 24 | Tool pin `ss` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:295`; RP6 map binds it at `RP6-P0.sh:548`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 25 | Tool pin `curl` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:296`; RP6 map binds it at `RP6-P0.sh:549`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 26 | Tool pin `timeout` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:297`; RP6 map binds it at `RP6-P0.sh:550`; RP7 shared map rules apply at `RP7-WPI-RO.sh:867-888`; R3 requires shared equality at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 27 | P0-only tool pin `id` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:298`; RP6 map binds it at `RP6-P0.sh:551`; RP6 declares `id` P0-only at `RP6-P0.sh:355-357`. R3 permits P0-only entries while requiring shared entries to match RP7 at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 28 | P0-only tool pin `getent` | LITERAL-MARKER | RP6 fixed literal is `<PIN-AT-FREEZE>` at `RP6-P0.sh:299`; RP6 map binds it at `RP6-P0.sh:552`; RP6 declares `getent` P0-only at `RP6-P0.sh:355-357`. R3 permits P0-only entries while requiring shared entries to match RP7 at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`. |
| 29 | RP6 block/member digest `RP6_P0_SHA` | LITERAL-MARKER | Wrapper copy is `<PIN-AT-FREEZE>` at `run_p0.sh:128`; wrapper block load requires it at `run_p0.sh:219-222`; extractor member digest slot is still marker at `remote_extract_verify_wpi.sh:199`; R3 requires block/member digest conservation at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:49` and `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:422-424`. Current local block hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:14`. |
| 30 | RP7 block/member digest `RP7_WPI_RO_SHA` | LITERAL-MARKER | Wrapper copy is `<PIN-AT-FREEZE>` at `run_ro.sh:122`; wrapper block load requires it at `run_ro.sh:216-219`; extractor member digest slot is still marker at `remote_extract_verify_wpi.sh:200`; R3 requires block/member digest conservation at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:49` and `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:422-424`. Current local block hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:16`. |
| 31 | RP0-LIB member digest | LITERAL-MARKER | Wrapper copies are filled as `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` at `run_p0.sh:126` and `run_ro.sh:120`, matching R3 at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:102`; extractor member digest slot remains `<PIN-AT-FREEZE>` at `remote_extract_verify_wpi.sh:197`. |
| 32 | RP0-BOOTSTRAP member digest | LITERAL-MARKER | Wrapper copies are filled as `e7d748fdc462fa847fb8eb5ca67dc8739849a8ab5ea39a69c4aca657cc0bd11e` at `run_p0.sh:127` and `run_ro.sh:121`; extractor member digest slot remains `<PIN-AT-FREEZE>` at `remote_extract_verify_wpi.sh:198`. |
| 33 | `run_p0.sh` wrapper/member digest | LITERAL-MARKER | Transport plan op 04 stdin digest is still `<PIN-AT-FREEZE>` at `TRANSPORT_PLAN.tsv:5`; extractor member digest slot is still marker at `remote_extract_verify_wpi.sh:201`; current wrapper hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:31`. |
| 34 | `run_ro.sh` wrapper/member digest | LITERAL-MARKER | Transport plan op 05 stdin digest is still `<PIN-AT-FREEZE>` at `TRANSPORT_PLAN.tsv:6`; extractor member digest slot is still marker at `remote_extract_verify_wpi.sh:202`; current wrapper hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:32`. |
| 35 | Deterministic runkit archive bytes and SHA-256 | LITERAL-MARKER | Transport runner pinned archive entry remains `<PIN-AT-FREEZE>` at `transport_runner.ps1:96-98`; transport plan archive copy/extract entries remain marker-bound at `TRANSPORT_PLAN.tsv:3-4`; extractor expected archive byte count remains `<PIN-AT-FREEZE>` at `remote_extract_verify_wpi.sh:190` and checks archive bytes/hash at `remote_extract_verify_wpi.sh:342-358`. R3 requires six exact archive members at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:422-424`. |
| 36 | `TRANSPORT_PLAN.tsv` SHA-256 | LITERAL-MARKER | Transport runner literal is `<PIN-AT-FREEZE>` at `transport_runner.ps1:92-93`; it hashes and compares the plan at `transport_runner.ps1:513-527`. Current local plan hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:34`. |
| 37 | `remote_setup_wpi.sh` stdin digest | LITERAL-MARKER | Transport plan op 01 stdin digest remains `<PIN-AT-FREEZE>` at `TRANSPORT_PLAN.tsv:2`; current setup-script hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:35`. Setup consumes `REMOTE_BASE` at `remote_setup_wpi.sh:221`. |
| 38 | `remote_extract_verify_wpi.sh` stdin digest | LITERAL-MARKER | Transport plan op 03 stdin digest remains `<PIN-AT-FREEZE>` at `TRANSPORT_PLAN.tsv:4`; current extract-script hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:36`. Extractor consumes archive path, extract dir, and archive hash at `remote_extract_verify_wpi.sh:184-187`. |
| 39 | `remote_close_tree_wpi.sh` stdin digest | LITERAL-MARKER | Transport plan ops 07 and 08 stdin digests remain `<PIN-AT-FREEZE>` at `TRANSPORT_PLAN.tsv:8-9`; current close-script hash is anchored above from `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:37`. |
| 40 | OpenSSH `ssh.exe` program digest | REQUIRES-HOST - not determinable locally | Transport runner pins `C:\Windows\System32\OpenSSH\ssh.exe` with `<PIN-AT-FREEZE>` at `transport_runner.ps1:109-113` and verifies program pins at `transport_runner.ps1:681-699`. |
| 41 | OpenSSH `scp.exe` program digest | REQUIRES-HOST - not determinable locally | Transport runner pins `C:\Windows\System32\OpenSSH\scp.exe` with `<PIN-AT-FREEZE>` at `transport_runner.ps1:109-113` and verifies program pins at `transport_runner.ps1:681-699`. |
| 42 | SSH identity key digest | REQUIRES-HOST - not determinable locally | Transport runner names the identity file at `transport_runner.ps1:122-126`, leaves its digest `<PIN-AT-FREEZE>` at `transport_runner.ps1:129`, and verifies config pins at `transport_runner.ps1:704-722`. Credential bytes were not read locally. |
| 43 | User `known_hosts` digest | REQUIRES-HOST - not determinable locally | Transport runner names the user known-hosts path at `transport_runner.ps1:123-124`, leaves its digest `<PIN-AT-FREEZE>` at `transport_runner.ps1:130`, and verifies config pins at `transport_runner.ps1:704-722`. |
| 44 | Global `ssh_known_hosts` digest | REQUIRES-HOST - not determinable locally | Transport runner names the global known-hosts path at `transport_runner.ps1:125-126`, leaves its digest `<PIN-AT-FREEZE>` at `transport_runner.ps1:131`, and verifies config pins at `transport_runner.ps1:704-722`. |
| 45 | Close-script argv, `WORK_ROOT`, scratch, and launch-domain contract | CONTRADICTED | Current transport plan passes three args for close ops at `TRANSPORT_PLAN.tsv:8-9`; current close script requires exactly three args and assigns `EV_DIR`, `RUNID`, and `WORK_ROOT` at `remote_close_tree_wpi.sh:282-286`. A stale current record still says the composition passes two args and exits before RUNID/EV_DIR at `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167`. R3 keeps blocker 8 open until the prereg section 4.7, plan rows 07/08, derivation contract, launch-domain claim, scratch semantics, and bytes describe one byte-identical contract at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:410-414`; the blocker map keeps item 8 open at `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:20`. |

## Blocker 7 - P0 attested values are not wired

Blocker 7 is still actionable and open. The blocker map states that `run_p0.sh` wires none of the five `P0_ATTESTED_*` inputs at `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:19`. Current bytes show the wrapper defines all five values as `<PIN-AT-FREEZE>` at `run_p0.sh:151-155`, exports them at `run_p0.sh:237-240`, and prints the deploy-channel attestation line while still using placeholders at `run_p0.sh:241-243`.

The exact consumers are not missing. RP6 requires all five wrapper values at `RP6-P0.sh:691-700`, rejects unfilled marker and malformed namespace/root-mount input at `RP6-P0.sh:707-724`, requires embedded literal and wrapper equality at `RP6-P0.sh:733-752`, reads live namespace links at `RP6-P0.sh:1390-1393`, and checks root mount identity at `RP6-P0.sh:1394-1414`. R3 requires the same five row-8 values to fill both embedded RP6 literals and wrapper copies at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:43`.

What `run_p0.sh` currently does instead: it defines, exports, and logs marker strings, then sources RP6 at `run_p0.sh:245`. With current bytes, RP6 cannot produce an end-to-end P0 PASS because `STATUS_RP6_P0.md:396-397` (count field at `:274`; **citation corrected 2026-08-12 ~17:55 — it read `:311-312` when written, and round 17 plus the Lead's implementer-attribution correction shifted the line; the claim content was and is true**) records 17 remaining `<PIN-AT-FREEZE>` literals and says no end-to-end `P0 PASS` is possible with them present. **Cross-checked and CONFIRMED** by `WPI_BLOCKS_DRAFT/RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md` and independently re-derived by the Lead: 17 counts distinct `P0_FIXED_*` definitions, while a raw occurrence count returns 27 — the extra 10 are the fence/guard occurrences that enforce the refusal, so both numbers are correct with different referents. The earlier RP6 audit acceptance was a source/audit acceptance, not a host end-to-end P0 PASS, as shown by `RP6_CODEX_T0_AUDIT_R16_2026-08-12.md:1` and `RP6_CODEX_T0_AUDIT_R16_2026-08-12.md:23-26`.

## Blocker 8 - close-script contract is not reconciled

Current bytes and current transport plan now agree on a three-argument close invocation. Plan rows 07/08 pass `EV_DIR`, `RUNID`, and `WORK_ROOT` at `TRANSPORT_PLAN.tsv:8-9`; the close script requires exactly three args and assigns them at `remote_close_tree_wpi.sh:282-286`. If a stale two-argument composition were used, the script would stop at argv count before any RUNID or EV_DIR grammar validation at `remote_close_tree_wpi.sh:282-286` and `remote_close_tree_wpi.sh:295-306`.

With the current three-argument plan, argv shape itself no longer blocks. However, because close `EXPECT_UID` and `EXPECT_GID` are still `<PIN-AT-FREEZE>` at `remote_close_tree_wpi.sh:202-203`, current execution would stop at `remote_close_tree_wpi.sh:288-291` before reaching RUNID/EV_DIR validation at `remote_close_tree_wpi.sh:295-306`. After those host identity pins are filled, the current script reaches RUNID/EV_DIR grammar checks, then validates `WORK_ROOT` at `remote_close_tree_wpi.sh:308-331`.

The inherited-TMPDIR question is also byte-settled in the current script but not yet reconciled in the freeze record. The script states it uses no inherited scratch and takes `WORK_ROOT` from argv at `remote_close_tree_wpi.sh:50-58`; it constructs `WORK_ROOT_CANON/close_work_$RUNID`, proves disjointness, exports `TMPDIR` to that owned work dir, and removes it at `remote_close_tree_wpi.sh:409-500`. The launch-domain boundary remains the documented inner-child-only closure with outer SSH account-shell boundary open in `transport_runner.ps1:155-188`; the close script rejects unexpected inherited environment entries at `remote_close_tree_wpi.sh:175-193`.

The contradiction is documentary and contract-level: `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167` still records the stale two-arg mismatch, while current plan/script bytes are three-arg. The blocker remains open because R3 explicitly requires prereg section 4.7, plan rows 07/08, derivation, launch-domain claim, scratch semantics, and actual bytes to describe one byte-identical contract before freeze at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:410-414`, and the blocker map records item 8 as open at `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:20`.

## Blocker 9 - REMOTE_BASE allocation must precede RO freeze

Blocker 9 is still actionable and open. The blocker map says `REMOTE_BASE` must be allocated before the RO block is frozen at `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:21`. Current allocation-dependent consumers remain literal markers in P0 at `run_p0.sh:113-123`, RO at `run_ro.sh:107-115`, transport runner at `transport_runner.ps1:80-90`, and transport plan paths at `TRANSPORT_PLAN.tsv:2-13`.

The ordering chain is exact:

1. Allocate one burn-ledger base and derive both stage names, as required by `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:40`, `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:118`, and `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:139-147`.
2. Use that base to define `REMOTE_BASE`, `EV_PARENT`, `EV_RUNKIT`, `kit`, `work`, P0/RO evidence directories, and transport paths, matching setup arg consumption at `remote_setup_wpi.sh:221`, work-root derivation at `remote_setup_wpi.sh:442`, and transport plan rows at `TRANSPORT_PLAN.tsv:2-13`.
3. Fill RP7 `WPI_FIXED_EVIDENCE_ROOT` from the allocated evidence root before RP7 bytes are frozen, because RP7 rejects a marker evidence root and requires `EV_DIR` to descend under it at `RP7-WPI-RO.sh:916-921`.
4. Run the frozen-composite conservation proof after allocation and filling, because FAM-03 requires exact `REMOTE_BASE`, exact P0/RO RUNIDs, wrapper render, RO evidence-root constant, and composite analysis before closure at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:363-372`.

Until that sequence is performed, the RO evidence-root literal at `RP7-WPI-RO.sh:116`, wrapper allocations at `run_ro.sh:107-115`, and transport retrieval/bind paths at `TRANSPORT_PLAN.tsv:10-13` cannot be considered frozen inputs.

## Tool-map reconciliation

RP6 has a 12-entry P0 map: 9 RO-shared tools plus P0-only `id` and `getent`, with `python3` bound to the trusted Python pin. The inventory is declared at `RP6-P0.sh:355-357`, the exact-map contract at `RP6-P0.sh:517-528`, fixed-to-map assignments at `RP6-P0.sh:542-553`, and the expected count check at `RP6-P0.sh:632-639`. RP7 has a 10-entry shared map with exact entries and count checking at `RP7-WPI-RO.sh:867-888`. R3 and FAM-01 require shared equality while preserving P0-only `id/getent` at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:44-45`, with owner ratification at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:396-398`. Current bytes therefore define an intended agreement model, but all actual tool-map values still require freeze filling because wrapper maps remain `<PIN-AT-FREEZE>` at `run_p0.sh:136` and `run_ro.sh:141`.

## Summary counts

Counts use one primary status per ledger row:

| Status | Count |
|---|---:|
| FILLED | 2 |
| LITERAL-MARKER | 29 |
| MISSING-CONSUMER | 0 |
| CONTRADICTED | 1 |
| REQUIRES-HOST - not determinable locally | 13 |
| Total rows | 45 |

Actionable blockers:

- Blocker 7 remains open: five P0 attested values have real RP6 consumers, but current wrapper and embedded literals are still markers.
- Blocker 8 remains open: current plan/script bytes agree on three args, but the prereg/plan/derivation/scratch/launch-domain record is not yet reconciled and a stale two-arg record still contradicts current bytes.
- Blocker 9 remains open: allocation-dependent P0, RO, transport, and evidence-root values are still markers, and FAM-03 requires allocation before RO evidence-root freeze and composite conservation proof.
