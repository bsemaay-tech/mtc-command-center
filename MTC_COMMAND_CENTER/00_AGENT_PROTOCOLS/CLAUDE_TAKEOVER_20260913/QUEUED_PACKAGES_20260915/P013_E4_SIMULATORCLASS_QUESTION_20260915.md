# WP-P0-13 E-4 — question to the identity-contract owner (WP-P0-20): `SimulatorClass` enum vs string twins — filed 2026-09-15 18:5xZ

**Authority to ask:** owner chat `G yes` (18:25Z) → `OD-20260915-P013-E4-ASK-1`. This file asks; it changes no code and decides nothing. The addressee is whoever answers for the P0-20 identity contract (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py`) in the next P0-20 slot (Wednesday exact-Opus lane 1/2 adjudication, or the P0-20 package Lead); the answer is recorded as a DECISIONS row or a P0-20 record, and folded into the P0-13 plan (V5 row E-4) by the P0-13 writer slice.

## The two locations (verified 18:5xZ in the P0-13 contract worktree `C:/tmp/P013_CONTRACT_V2_20260912` @ `da1fb184`)
| Where | Bytes |
|---|---|
| `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:263-265` | `class SimulatorClass(str, Enum):` with members `SIGNAL_SCREEN_ONLY = "SIGNAL_SCREEN_ONLY"`, `FULL_KERNEL_SIMULATION = "FULL_KERNEL_SIMULATION"` |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:55-56` | module-level string constants `SIGNAL_SCREEN_ONLY = "SIGNAL_SCREEN_ONLY"`, `FULL_KERNEL_SIMULATION = "FULL_KERNEL_SIMULATION"`; the module imports `compute_evaluation_run_hash` from `mtc_contracts.identity` (`:28`) but NOT `SimulatorClass` |
| Tests | no test in `mtc_v2/trial_catalog/tests/` asserts the string twins equal the enum members (plan V5 `P13M:471-477`) |
| Note | on `master` (`fcac0ac6`) the contracts `identity.py` is 154 lines and carries no `SimulatorClass`; the enum exists on the P0-13 contract branch (`da1fb184`) — the question is therefore about the CONTRACT DESIGN before merge, not about master bytes |

## The question (one line)
Should `SimulatorClass` stay a closed `str` enum owned by `mtc_contracts.identity`, with `stages_conservation_identity.py` importing and using the enum members (no string twins), or is the twin-string vocabulary intentional (e.g., to keep the stage module free of the contracts import surface) — in which case the contract needs a test that pins the twins to the enum values so the two can never drift?

## Options, for the answer
| Option | Effect |
|---|---|
| E1 enum is the single owner | `stages_conservation_identity.py` imports `SimulatorClass` and drops the two constants; every consumer compares against the enum; one-line change + the existing tests |
| E2 twins intentional | keep both; add `test_simulator_class_vocabulary_matches_contract` asserting `{SIGNAL_SCREEN_ONLY, FULL_KERNEL_SIMULATION} == {m.value for m in SimulatorClass}` in the contract's test suite (fails the day one side changes) |
| E3 something else | say what and why |
Lead reading (not a recommendation the owner must take): E2 costs nothing now and protects the merge; E1 is cleaner if the stage module is allowed to import the contracts package (it already imports `compute_evaluation_run_hash` from it, so the import surface argument does not hold).

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
