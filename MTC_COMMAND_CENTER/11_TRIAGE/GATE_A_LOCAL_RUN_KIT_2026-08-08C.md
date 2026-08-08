# Gate A local run kit — `2ce41e34` — 2026-08-08C (evidence-checker repair only)

## Addendum — run-kit C transferred; retained-log A-3 postcheck PASS (2026-08-08)

> Newest update to this record. The "next unit" defined below was executed on `gatea-staging`: the C tar
> was transferred (B left intact) and the retained-log A-3 postcheck PASSED. This addendum records that
> execution and marks the next unit complete; it does not alter candidate acceptance, the product bits,
> the artifact, D025 acceptance, or the repair-round count. No pytest rerun; no code/scripts/artifacts/
> results/staging action/commit/push/git mutation.

**Transfer + remote verification (B intact).** Tar transferred to
`/home/gatea/gatea-run-kit-20260808C-2ce41e34.tar`. Remote direct verification on `gatea-staging`: tar
SHA-256 `4ee5ba920800ceff8f55338bcba5b388d39d2457f9970795af89c9333767f855`, `53760` bytes, exact 9
members; extracted to `/home/gatea/gatea-run-kit-20260808C-2ce41e34`; 7 manifest entries; `sha256sum -c`
all seven OK; six `bash -n` PASS; corrected remote `gatea_A3.sh`
`2bfec1c230d77d70f30bda5560f824fe970b4c2fca098d3fdda49129f2465d1c` OK.

**Retained-log A-3 postcheck — PASS (no pytest rerun).** Retained suite log
`/home/gatea/gatea-A3-suite-20260808B.log` SHA-256
`569e79c7d68623b9f2ad51ee48053a04e6938e3277398861760dc1dd8d61c848` verified. Outer retained log contains
exact `pytest rc=1`; terminal `2 failed, 1358 passed, 1 warning in 169.85s (0:02:49)` matches the
corrected anchored optional-elapsed regex; observed failures exactly equal the two permitted
`test_order_state.py` gc-referents node IDs both ways; failures `0`; `A-3 CHECKER PASS`.

**Canonical VM evidence logs.** `/home/gatea/gatea-A3-postcheck-20260808C.log` and clean replay
`/home/gatea/gatea-A3-postcheck-20260808C-clean.log`: both SHA-256
`56a80d53155ac73b39dac064260ff702532fad36562eafbbe75f28c2f6414878`, `738` bytes, byte-identical.
Clean-replay postcheck script SHA-256
`19003ef03c0ccc433990b761feee89b613497d13e3bc312b816639e67c8415f1`; runner SHA-256
`7a03c61dec9333e71d98115cb0f781b06ba2639d8a513781d600213061c6da16`; both `bash -n` rc `0` and 0 CR.

**Transport noise — recorded transparently, not concealed.** The first stdin stream via PowerShell
inserted a BOM before the shebang and printed a harmless `#!/usr/bin/env` command error outside the
captured log after the postcheck had already returned PASS (the captured log itself was clean). A second
byte-preserving Git Bash stream replay to the separate clean log had no transport error and produced the
same 738 bytes/hash/PASS. This is non-gate transport noise.

**State after postcheck.** Service reverified `inactive`, `masked`, listener 8790 absent; no credentials
loaded. Gate A IN PROGRESS after accepted A-3; A-4 has not started. Existing owner authorization covers
A-4 within the preregistered sequence; hard exclusions unchanged (credentials, broker/exchange access,
successful ARM, orders, TESTNET/mainnet, master merge, economic action).

**Next step.** `[AI: Claude]` execute the transferred C `gatea_A4.sh` under Addendum D, capturing all
seven conditions (active/running; loopback 127.0.0.1:8790 only; status durably not ARMED; application-level
exact credential-free 409 with correct X-Confirm; no broker attempt in journal/bridge.err.log/sockets;
persisted DISARMED and unchanged version; resolved running environment/start mode). Stop at first FAIL.
On failure run only read-only diagnostic as needed, then stop+mask the service and write result/memory.
On PASS update `_AI_MEMORY` before preregistering the exact A-5–A-9 commands; do not improvise them.
Preserve old `GATE_A_RESULT_2026-08-08.md`; later write `GATE_A_RESULT_2026-08-08B.md`.

## Scope — what this is, and what it is not

This is an **evidence-checker repair only.** It corrects the A-3 run-script checker that
falsely rejected an already-valid A-3 suite outcome, and freezes the corrected revision as run-kit
**C**. It **does not alter candidate acceptance, the product bits, the artifact, D025 acceptance, or
the repair-round count.** The accepted repair candidate remains
`2ce41e34bceb599d80af24c5c33d835820ec321b`. Gate A has rerun through A-3 (A-0, A-1, A-2, and A-3 passed; A-4 has not started).

**Run-kit B is preserved unchanged** (do not overwrite or delete it). C is a sibling revision that
differs from B only in the A-3 checker script and the README; the other five scripts are byte-identical
to B. Supersedes the A-3 checker in `11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08B.md` **only** for that
one checker. Continues the A-3 checkpoint recorded in the `## [GLM-5.2] 2026-08-08 — Gate A rerun
checkpoint through A-3` section of `_AI_MEMORY/GLOBAL_HANDOFF.md` and the NEWEST CHECKPOINT block of
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`.

**No transfer or remote execution is claimed here.** The C bundle was frozen and validated locally
only. During this C freeze, nothing was transferred to staging, no host contact occurred, and the
checker has **not** been re-run on staging (A-0 through A-3 of the overall rerun **did** run on
`gatea-staging` — see the A-3 rerun checkpoint; the scoping above is for the C freeze unit only).
Staging still holds the A-3 evidence from run-kit B; C is the corrected checker to
apply against that retained evidence.

## Frozen run-kit C bundle — prepared and locally validated, not transferred

- Directory: `C:\WPI_ARTIFACTS\gatea-run-kit-20260808C-2ce41e34`
- Tar: `C:\WPI_ARTIFACTS\gatea-run-kit-20260808C-2ce41e34.tar`
- Tar SHA-256: `4ee5ba920800ceff8f55338bcba5b388d39d2457f9970795af89c9333767f855`
- Tar bytes: `53760`
- Members: `9` total — one root directory plus eight files: `README.txt`, `SHA256SUMS`, and the six
  scripts.
- Manifest entries: `7` — `README.txt` plus the six scripts.

The C README begins `AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN.` and states
that the existing owner authorization covers only that bounded `gatea-staging` teardown/rerun sequence
(hard exclusions unchanged: credentials, broker/exchange access, successful ARM, orders, TESTNET/mainnet,
master merge, economic action). The bundle itself was **not transferred or executed** during this freeze
unit.

## Script hashes (frozen in the C bundle)

Only `gatea_A3.sh` changed versus B (the corrected checker). README hash changed accordingly. The
other five scripts are unchanged from B.

| Member | SHA-256 | Bytes | vs B |
|---|---|---:|---|
| `gatea_A0_A1.sh` | `0d456a8eebb0fd85eb20f08a4a67ffdf30a9fa1211a4cb4093b6f8110ebf1c11` | 5730 | unchanged |
| `gatea_A2.sh` | `07a715aa5aeec86dd81cc8fa4051f6c66f8461dacedb9e05ffc880a07a08c053` | 9717 | unchanged |
| `gatea_A3.sh` (corrected) | `2bfec1c230d77d70f30bda5560f824fe970b4c2fca098d3fdda49129f2465d1c` | 5087 | **changed** (B: `33934221…604443` / 4064) |
| `gatea_A4.sh` | `78aa7fca7bfe7eb256a562d08d61e7d16b4ffcd3b164b89a5df420a01a8fd9b4` | 16228 | unchanged |
| `gatea_A4_diag.sh` | `f75912a2298b2611d70d20998b711e1af54f1900b3af77441595de960f0f101d` | 3053 | unchanged |
| `gatea_teardown.sh` | `19016d8f0bdeffa08637f83baf84b2e9d6f41e1359b44c6faad22bcb763ec0b3` | 4839 | unchanged |
| `README.txt` | `47278c48e1e183c15013be583279dcec0e82db88174427e53ba8906fccd12883` | — | **changed** (B: `45b480ac…1353`) |

## What the corrected A-3 checker fixes

The B A-3 wrapper falsely rejected a valid A-3 suite log: its anchored predicate did not allow
pytest's optional elapsed suffix, so a real `2 failed, 1358 passed, 1 warning in 169.85s (0:02:49)`
terminal line was treated as a checker failure. This is a **run-script evidence defect**, not a
candidate failure. The C A-3 checker uses the corrected **anchored, optional-elapsed** regex. Candidate
`2ce41e34` and the product/artifact are untouched.

## Independent local validation

The frozen C tar was extracted to a unique disposable directory and verified independently:

- 8 files present; 7 manifest entries; `sha256sum -c` — **all OK**.
- All six scripts `bash -n` — **rc 0** each.
- Every shell file CR byte count — **0**.
- Corrected A-3 checker falsification (RED/GREEN) — **`10 passed, 0 failed`, rc `0`**.

**Cleanup residue:** cleanup of the disposable
`C:\tmp\gatea-c-verify-929e34808c0e47699d8964f879309072` was blocked by local command policy after
exact path verification; the directory remains isolated under `C:\tmp` and must be removed only by an
allowed exact-literal cleanup. It is **not** in either tar and **not** in the repository. Do not claim
it was removed.

## State and authorization boundary

During this run-kit C freeze unit the product candidate and the staging install were **not changed**,
and no staging host contact, transfer, teardown, install, service start, credential access,
broker/exchange access, ARM request, order, TESTNET/mainnet action, master merge, or economic action
occurred — this scopes only the C freeze unit itself; A-0 through A-3 of the overall rerun **did** run
on `gatea-staging` (see the A-3 rerun checkpoint). Gate A is **IN PROGRESS through A-3**; A-4 has **not**
started; the current accepted `2ce41e34` install is masked/inactive/not enabled with no listener and no
credentials. The owner already explicitly authorized the preregistered `gatea-staging` teardown/rerun
sequence, so no additional authorization is required to transfer run-kit C, run the retained-log A-3
postcheck, or run A-4 within that sequence. Hard exclusions remain: credentials, broker/exchange access,
successful ARM, orders, TESTNET/mainnet, master merge, and economic action.

## Next unit (precise definition)

1. **[AI: Claude] TRANSFER RUN-KIT C ONLY; DO NOT REPLACE/DELETE B.** Transfer only the run-kit C
   tar to `/home/gatea/gatea-run-kit-20260808C-2ce41e34.tar`; verify exact tar SHA-256
   `4ee5ba92…7f855`, `53760` bytes, and the exact 9-member set (root dir + 8 files); extract to
   `/home/gatea/gatea-run-kit-20260808C-2ce41e34`; run `sha256sum -c` and the six `bash -n` checks.
2. **[AI: Claude] RE-CHECK A-3 WITHOUT RERUNNING PYTEST.** Against the retained
   `/home/gatea/gatea-A3-suite-20260808B.log`: require the last non-empty line to match the corrected
   anchored optional-elapsed regex; require `/home/gatea/gatea-A3-20260808B.log` to contain the exact
   line `pytest rc=1`; require exact two-way equality between the observed `FAILED ` node-ID lines and
   the two permitted `test_order_state.py` gc-referents failures. Preserve output at
   `/home/gatea/gatea-A3-postcheck-20260808C.log`. Any mismatch is Gate A FAIL; otherwise A-3 checker
   PASS.
3. **[AI: Any] UPDATE `_AI_MEMORY/` BEFORE A-4.**
4. **[AI: Claude] RUN A-4 EXACTLY UNDER ADDENDUM D AND STOP AT FIRST FAIL.** No credentials/broker/
   successful ARM/orders/TESTNET/mainnet/master merge/economic action. Bind A-4 to the corrected step-8
   result from the B run kit.

## Safety state

The old `ebada020` staging install was **torn down** during the authorized rerun (bounded teardown
**PASS**, leftovers `0`; evidence `/home/gatea/teardown-ebada020-20260808B`). The current accepted
`2ce41e34` install is installed and verified, masked/inactive/not enabled, no listener, no credentials,
nothing armed. After A-3 checker PASS and `_AI_MEMORY` update, the next gate step is A-4 only. Preserve
the old `GATE_A_RESULT_2026-08-08.md`; later write `GATE_A_RESULT_2026-08-08B.md` for the rerun.
