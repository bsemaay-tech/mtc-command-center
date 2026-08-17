# WP-L Phase 2 — Stage 2 preregistration failure record

Result: **BLOCKED — NOT PREREGISTERED, NO REMOTE INVOCATION**

## First failure

- Required counterpart: Claude Code CLI, exact `claude-opus-5`, effort `xhigh`.
- Operation: derive the frozen candidate payload-manifest hash and create the complete immutable staging preregistration.
- The bounded implementation call ended with process rc `124` after 904 seconds and returned no completion report.
- The CLI parent timed out while a task-scoped child continued briefly. Five partial files were created in total; the two late files are included below. The validated task process was terminated before this corrected inventory was frozen.
- The candidate-manifest derivation, immutable preregistration, transport plan, transport recorder, close-tree helper, preregistration checksum set, and stage record were absent.
- Repository policy forbids the Codex Lead from replacing the required counterpart implementation. First-FAIL stopping therefore applied before any SSH or host action.

## Preserved partial files — not authorized to execute

| File | Bytes | SHA-256 |
|---|---:|---|
| `remote_extract_verify.sh` | 8270 | `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3` |
| `remote_setup.sh` | 4976 | `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5` |
| `run_b3.sh` | 4239 | `096aabb2d55b2f6174e0c4b47dab34fcfdcb7bfef6e7627acc5c4ccad43338dd` |
| `R4_5_runner.py` | 16170 | `8519e2bfc9bf2105bbb8e8c33fa4f271aa8852c7d7b18ad10286e19deddf68d5` |
| `run_r45.sh` | 3414 | `9772c02bcffb632e66b80655852f1ab935650a7a7a5164b57a22d42c18c74928` |

These are incomplete implementation evidence only. They were not accepted, transferred, sourced, or executed. Their presence grants no host authority.

## Mandatory preregistration artifacts missing at stop

- `CANDIDATE_RELEASE_SHA256SUMS` and its clean candidate-package derivation record
- `PREREGISTRATION.md` and `PREREG_SHA256SUMS.txt`
- `TRANSPORT_PLAN.tsv` and `transport_runner.ps1`
- `remote_close_tree.sh`
- a complete self-QA/stage record

Because those artifacts do not exist, no RUNID, evidence path, remote argv, stdin hash, B3 manifest hash, or support-script hash is preregistered. RP0 §1.2 therefore prohibits any remote invocation.

## Safety state

- SSH/SCP/remote invocation count: **0**
- Staging host contact: **none**
- Service stop/reboot/rollback: **none**
- Bridge/credential/ARM/order/broker/TESTNET/mainnet action: **none**
- C1, C2, C3, C4, C5, B3, and R4-5 execution: **none**
- The unrelated `tmprepo_map_inventory.md` remained untouched and untracked.
