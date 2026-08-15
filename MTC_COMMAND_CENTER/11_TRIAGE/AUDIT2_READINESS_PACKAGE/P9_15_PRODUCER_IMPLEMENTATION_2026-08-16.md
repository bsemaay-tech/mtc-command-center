# P9-15 producer implementation — blocked specification disposition

Status: **BLOCK — NOT IMPLEMENTED, NOT TESTED, NOT ACCEPTED**.

Audit tier at Gate 1: **T1** (a bounded local, non-economic Python producer and
test suite). The lane explicitly prohibited sub-delegation and self-acceptance, so
no independent audit was dispatched. Work stopped before Gate 2 because the
assigned artifact contract and the normative specification cannot both be
satisfied.

## Scope actually performed

This lane performed read-only specification reconciliation and wrote this one
report. It did not create a producer or falsification suite. It performed no host,
network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge, push, or economic action.

The stop is required by the lane instruction: if the specification is wrong or
under-determined, stop and write that up instead of improvising.
`C:/tmp/lane_kick/P9IMP.md:51-52`

## Blocking contradictions and unknowns

### 1. The required artifact sets and locations are mutually exclusive

The lane requires one self-contained Python producer under
`WPI_PREREG_DRAFT_ROUND1/` and a second Python falsification suite.
`C:/tmp/lane_kick/P9IMP.md:22-24`

The normative specification says the implementation consists of **exactly three**
Commit-2 artifacts under `AUDIT2_READINESS_PACKAGE/`: a PowerShell runner, a
Python inventory child, and a JSON policy.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:13-23`

The hard write allowlist permits only the two lane files and this report.
`C:/tmp/lane_kick/P9IMP.md:54-58` It therefore forbids creating two of the three
normative implementation artifacts and requires the Python artifact at a path
different from the path frozen by the specification.

### 2. A lone Python file cannot implement the specified top-level trust boundary

The exact public entry point is a pinned PowerShell runner with eight mandatory
named parameters.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:30-49`
The runner, not the Python child, owns invocation validation, tool/artifact pin
checks, process-stream capture, wrapper-failure classification, evidence-envelope
creation, and finalization.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:23-25`

The exact child argv binds the Python file and separate policy at their
`AUDIT2_READINESS_PACKAGE` paths and requires a Git executable plus P9-06 pin
record and its SHA-256.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:104-130`
Moving the child, embedding the policy, or replacing the PowerShell envelope with
Python would change the exact interface and trust boundary. No authorized mapping
defines those deviations.

### 3. The semantic egress policy is deliberately unknown

The specification says the exhaustive egress grammar matrix is **UNKNOWN** and
must be supplied by the reviewed, frozen `p9_15_policy.json`; the implementation
must not guess or silently omit missing constructs.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:150-160`
It repeats that the final policy bytes remain unknown and that a real PASS is
unavailable until they are settled.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:530-535`

No `p9_15_policy.json`, `p9_15_runner.ps1`, or `p9_15_inventory.py` exists at the
current branch tip. Embedding an invented policy in a self-contained Python file
would select new security and egress semantics without authorization.

### 4. The requested evidence cannot be produced through the specified caller

The normative falsification contract requires driving the real top-level runner,
including replacement/removal of a declared instrument, an unknown network sink,
a canonical dependency duplicate, and a failed blob read.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:518-528`
The lane forbids creating that runner and separate policy. A reduced test harness
around a different one-file program would not falsify the specified production
path and would be the self-confirming pattern the task expressly rejects.

The replay command likewise names the normative Python and policy paths and
requires the P9-06 pin inputs.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:500-516`
Consequently, there are no honest two-run hashes, GREEN output, or RED
demonstrations to report. None were fabricated.

## Commands and real output

Initial branch and cleanliness check:

```powershell
git branch --show-current
git rev-parse HEAD
git status --porcelain
```

```text
codex/p9-15-producer-20260816
c7a4383b7b556b9f39b5819bf54fb6a60f51109c
```

The absent third line is the real empty porcelain status.

Search for already-frozen producer/policy artifacts:

```powershell
rg --files MTC_COMMAND_CENTER | rg -i 'p9_15_(runner|inventory|policy)|packet9.*policy|egress.*policy'
```

```text
NO_MATCHES
```

Confirm that none of the proposed artifacts or this implementation report was
tracked at the starting `HEAD`:

```powershell
git ls-tree -r --name-only HEAD -- `
  MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1 `
  MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE |
  rg -i 'p9_15_(runner|inventory|policy)|P9_15_PRODUCER_IMPLEMENTATION'
```

```text
NO_MATCHES
```

No producer command was run because there is no contract-compliant producer to
run. No determinism hashes or RED demonstrations exist.

## What no producer currently verifies

Because no implementation was created, this lane verifies none of the proposed
P9-15 semantic properties: Git-tree completeness, dependency pins, secret
category/path hits, egress classification, conservation, canonical serialization,
ordering, tool or artifact identity, evidence finalization, exit-code mapping, or
independent replay.

This report verifies only that the assigned and normative contracts conflict at
the cited lines and that the required policy/runner/producer artifacts were absent
from the starting commit.

## Required decision before implementation

One coherent contract must be selected and frozen:

1. **Implement the normative three-artifact design.** Expand the write allowlist to
   the exact runner, inventory, policy, falsification-suite, and report paths;
   supply the reviewed exhaustive policy grammar and P9-06 pin-record fixture; and
   retain the exact runner/child/replay interfaces.
2. **Replace the normative design with a one-file design.** Revise the specification
   to define the new file path, top-level argv, pinning and envelope ownership,
   embedded-policy bytes and versioning, output/finalization behavior, verifier
   command, and falsification entry point.

Until one option is authorized, implementation would be an unreviewed contract
change rather than execution of the written specification.
