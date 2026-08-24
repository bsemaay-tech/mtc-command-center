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
- Every model is deeply immutable and carries contract version `0.1.0`. Nested
  mappings, sequences, and sets are detached from caller inputs and frozen.
  Unknown fields are rejected. Kernel/Bridge version skew is represented by
  `ContractHandshake`; consumers must refuse mismatches and co-deploy v0.
- **`model_construct()` is FORBIDDEN for contract consumers.** Pydantic's
  `model_construct()` bypasses validation by design, and instances built with it
  are neither validated nor deeply frozen. No consumer of this package may create
  a contract object with `model_construct()` (or `copy(update=...)`-style
  validation bypasses); only normal construction and `model_validate` produce
  valid, immutable contract objects. Any object made via a bypass carries no
  contract guarantee, and reviews must treat its appearance in consumer code as
  a defect. *(Documented 2026-08-25, T1 closure round: the bypass is a pydantic
  escape hatch, not a supported path — no consumer in this repository uses it.)*
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
dictionary ordering irrelevant. Identity functions accept environment lineage as
call context so exclusion can be tested directly, but never add it to a preimage.

## Build and install

Create or activate a virtual environment, then install the exact recorded tooling
under the committed constraints:

```powershell
python -m pip install --constraint .\constraints.txt pip==26.2.1
python -m pip install --constraint .\constraints.txt build==1.5.0 pytest==9.1.1 ruff==0.16.4 setuptools==84.0.0 wheel==0.48.0
```

Build an artifact from this directory using that pinned environment:

```powershell
python -m build --no-isolation
```

Install the generated wheel, not this source path:

```powershell
python -m pip install --constraint .\constraints.txt .\dist\mtc_contracts-0.1.0-py3-none-any.whl
```

Run the package tests:

```powershell
python -m pytest -q
```
