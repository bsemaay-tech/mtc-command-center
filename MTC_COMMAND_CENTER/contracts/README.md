# MTC Contracts

`mtc-contracts` is the versioned, schema-only boundary shared by future MTC
research and execution components. Version `0.1.0` defines data shapes and
identity formulae. It performs no sizing, allocation, Guardian, reconciliation,
lifecycle, admission, promotion, broker, or trading action.

## Contract rules

- `SizingRequest` is kernel-emitted and snapshot-independent. It accepts exactly
  one request constant matching one of four normalized methods. It rejects all
  unknown fields, including account, bucket, policy-binding, proposed,
  authorized, executable, and result quantities/notionals.
- `SOURCE_DEFINED` is `sizing_source_class` provenance only. It is never a fifth
  runtime sizing method. A normalizable rule is represented by its compiled
  native `SizingRequest`; a non-normalizable rule uses `MissingRuleRecord` with
  status `NOT_EXPRESSIBLE` and a versioned named substitute.
- Every model is immutable and carries contract version `0.1.0`. Unknown fields
  are rejected. Kernel/Bridge version skew is represented by
  `ContractHandshake`; consumers must refuse mismatches and co-deploy v0.
- Every numeric policy/freshness/window threshold is `[OPEN]` (`None`) unless
  separately owner-ratified. Consumers must treat unset as fail-closed. These
  models record shapes and do not apply thresholds.
- Python version, dependency lockfile, and OS are deliberately excluded from
  `package_hash`, `evaluation_run_hash`, and `deployment_identity_hash`. Evidence
  carries `EnvironmentLineage` alongside those hashes. Environment changes need
  a bit-identical golden-suite re-run before evidence continues.
- Admission records are immutable and bind an exact `deployment_identity_hash`:
  `SHADOW_ELIGIBLE` admits only `FORWARD_SHADOW`; `PAPER_ELIGIBLE` only
  `INTERNAL_PAPER`; `TESTNET_ELIGIBLE` exactly `INTERNAL_PAPER` and
  `EXCHANGE_TESTNET`; `PROMOTED` exactly `MAINNET` and `LIMITED_LIVE`.

## Identity encoding

The mathematical `SHA256(A ‖ B …)` formulae are encoded as canonical UTF-8 JSON
objects with fixed component names, lexicographically sorted keys, compact
separators, decimal values rendered as strings, enum values rendered as strings,
and timestamps rendered as ISO 8601. This makes field boundaries unambiguous and
dictionary ordering irrelevant. Environment lineage is not an accepted argument
to any identity-hash function.

## Build and install

Build an artifact from this directory:

```powershell
python -m build
```

Install the generated wheel, not this source path:

```powershell
python -m pip install .\dist\mtc_contracts-0.1.0-py3-none-any.whl
```

Run the package tests:

```powershell
python -m pytest -q
```
