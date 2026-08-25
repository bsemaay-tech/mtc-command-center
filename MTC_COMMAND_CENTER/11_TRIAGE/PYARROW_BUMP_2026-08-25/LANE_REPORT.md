# Lane X report — PyArrow 23.0.1

Date: 2026-08-25

Role: Codex implementer under Claude Lead

Branch: `fix/pyarrow-cve-bump-20260825`

Base: `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`

Push: not performed

## Implemented

- Changed only `pyarrow==23.0.0` to `pyarrow==23.0.1` in `MTC_COMMAND_CENTER/02_MTC_BACKTEST/requirements-lock.txt`; all other lockfile lines are unchanged and the pin count remains 13.
- Appended dependency-ledger entry 0015, which supersedes entry 0012 without editing any earlier entry.
- Added this lane report and `FIX_EVIDENCE.md`.

No engine/source, Pine, parity, MTC/strategy behavior, schema, host, credential, deployment, broker, or other dependency pin was changed.

## Validation summary

| Check | Real result |
|---|---|
| Fresh Python environment | Python 3.13.14 venv newly created under the Windows temp directory |
| Complete bumped lock install | PASS; `pyarrow-23.0.1` installed with the other 12 declared pins |
| Dependency consistency | `No broken requirements found.` |
| Imported version | `PYARROW_VERSION=23.0.1` |
| Real repository data source | 17,856-row OHLCV Parquet, SHA-256 `3aa0d38943e04ca907ba3c178fdd1fbfae1b7ce43f731ded6d3ccb9da9cecf01`; unchanged before/after |
| Real slice Parquet round-trip | PASS: schema, values, and bytes equal; SHA-256 `c30c574e7157c2b95a1132fb176c28badd9bbc83bf01be618edd24d295dc0a7a` |
| Real slice Arrow IPC round-trip | PASS: schema, values, and bytes equal; SHA-256 `7331fc07fa4327e30c0f68659eb64b7c48d0fcbeffc8445ca8a4fcc883534aaa` |
| Synthetic Parquet round-trip | PASS: schema, values, and bytes equal; SHA-256 `f801fa86804d90db6f06eab70eb7323265873ac6d3e07fc3edacdd0a8f5aafdd` |
| Synthetic Arrow IPC round-trip | PASS: schema, values, and bytes equal; SHA-256 `893d63203cbc9393e6f5fe068657c3367210dfbbec7bd21e07f82f1e4e4715ff` |
| Offline engine smoke | PASS: `--dry-run` loaded 128 bars, exit 0, no output path created |
| Real backtest/research execution | Not run, as required |
| OSV exact 23.0.1 query | HTTP 200, raw `{}`, vulnerability count 0 at `2026-08-25T03:42:01Z` |
| OSV advisory range | `CVE-2026-25087`; introduced `15.0.0`, fixed `23.0.1`; `23.0.0` explicitly affected |
| Exact selected wheel | `pyarrow-23.0.1-cp313-cp313-win_amd64.whl`, SHA-256 `cecfb12ef629cf6be0b1887f9f86463b0dd3dc3195ae6224e74006be4736035a` |

Full commands and real output are in `FIX_EVIDENCE.md`.

## Harness correction recorded

The first synthetic-fixture attempt failed before executing any round-trip because typed timestamp values were supplied as strings. PyArrow rejected them with `ArrowTypeError`. The fixture was corrected to timezone-aware Python `datetime` objects and the complete validation passed in a new temp subdirectory. No repository file or real-data source was changed by the failed attempt.

## RED/GREEN statement

No RED/GREEN reproduction of the native use-after-free path is feasible or claimed. There is no approved exploit fixture, and deliberately inducing a native heap UAF would be unsafe. Per the owner-directed ledger policy for this bump, the named-advisory closure evidence is OSV's fixed range plus the zero-result exact-version query and the successful real/synthetic Parquet and Arrow IPC compatibility round-trips. This is not a claim that the exploit path itself was executed.

## Handoff to Lead

- Recommended audit classification: **T0**, because a protected backtest lock and security advisory are involved.
- Lead must independently inspect the exact diff and run/reproduce proportionate validation under the T0 acceptance contract.
- No push was performed.
- The implementation commit SHA is printed in the lane completion handoff because this report is included inside that commit.
