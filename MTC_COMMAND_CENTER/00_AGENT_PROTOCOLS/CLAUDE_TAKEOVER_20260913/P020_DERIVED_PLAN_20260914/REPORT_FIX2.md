# P20DERIVFIX report

## Diff summary

- N6-8 fixed in `C:/tmp/P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py:80`: transcribed `lexicographic_first_matching` from `C:/tmp/P020_PRESELECT_20260913/preselect_profile.py:412-443` into the derivation tool, adapting only the refusal exception/code to `DERIVE_REFUSED_SELECTION_MISMATCH`.
- `C:/tmp/P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py:107` re-derives the recorded `selection` from calibration `eligibility_matrix_binary_only`; `C:/tmp/P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py:162` makes the existing input check return only that verified selection.
- `C:/tmp/P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py:230` records `derivation.selection_rederived: true`.
- N6-6 fixed at `C:/tmp/P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py:165`: removed the dead `base_plan` parameter from `derive_trials`; the call site now passes only `frozen` and `selection`.
- Tests now include the real matrix shape in the happy fixture at `C:/tmp/P020_PLAN_DERIVE_20260913/tests/test_derive_benchmark_plan.py:67`, assert `selection_rederived` at `:145`, and add the consistently rewritten matrix+selection refusal at `:216`.
- `C:/tmp/P020_PLAN_DERIVE_20260913/DERIVATION_RULE.md:5` documents the new `DERIVE_REFUSED_SELECTION_MISMATCH` refusal; `:7` documents `selection_rederived: true`.
- `C:/tmp/P020_PLAN_DERIVE_20260913/SHA256SUMS.txt` refreshed, LF-only.

## RED/GREEN pair

Command:

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -m pytest tests/test_derive_benchmark_plan.py::test_refuses_consistently_rewritten_matrix_and_selection tests/test_derive_benchmark_plan.py::test_happy_path -q -p no:cacheprovider
```

Output:

```text
..                                                                       [100%]
2 passed in 0.06s
```

The RED arm is `test_refuses_consistently_rewritten_matrix_and_selection`: it rewrites both records' selections and the calibration matrix so the old cross-file/five-distinct/frozen-family checks pass, then asserts refusal with `DERIVE_REFUSED_SELECTION_MISMATCH`. The GREEN arm is `test_happy_path`: the fixture pair derived from the real rule passes unchanged and emits `selection_rederived: true`.

## Full pytest

Command:

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
```

Output:

```text
................                                                         [100%]
16 passed in 0.28s
```

## SHA256SUMS.txt

```text
0bfd18915a0952cbf8bd1058b5d560a5cd30558a3f2f6d2ae6706947152289d7  derive_benchmark_plan.py
185af7b237d11d6e9365716c4ff127eedc967d4a91f82b9107e016d95ad4c22a  tests/test_derive_benchmark_plan.py
40e1773f4c5f953444ce5d082ef9ec7d496df86f7eff9d67240d471198d589a7  DERIVATION_RULE.md
8394279ef22e6d6ea410f73d4d633c88c46d810cfafbffe07d354d70099075bb  REPORT.md
8467360c2c03ae0d0e57903208ff1a896a9dc9104640b7e98006812f16ccbcfe  REPORT_FIX1.md
```

Verification:

```text
derive_benchmark_plan.py: OK
tests/test_derive_benchmark_plan.py: OK
DERIVATION_RULE.md: OK
REPORT.md: OK
REPORT_FIX1.md: OK
```

Line endings: `CR=0 LF=5`.

## NOT VERIFIED

- Not reviewed.
- No derivation was executed on the real `C:/tmp/P020_PRESELECT_20260913/PRESELECTION_CALIBRATION.json` or `C:/tmp/P020_PRESELECT_20260913/PRESELECTION_ELIGIBILITY.json`.
- `--oneshot` was not run.
