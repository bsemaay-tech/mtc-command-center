import pandas as pd
import pytest

from scripts.first_divergence_finder import find_first_mismatch


def test_find_first_mismatch_returns_first_bad_row():
    df = pd.DataFrame(
        [
            {"tv_seq": 1, "all_core_match": True},
            {"tv_seq": 2, "all_core_match": False},
            {"tv_seq": 3, "all_core_match": False},
        ]
    )
    row = find_first_mismatch(df)
    assert row is not None
    assert int(row["tv_seq"]) == 2


def test_find_first_mismatch_none_when_clean():
    df = pd.DataFrame([{"tv_seq": 1, "all_core_match": True}])
    assert find_first_mismatch(df) is None


def test_find_first_mismatch_requires_column():
    df = pd.DataFrame([{"tv_seq": 1}])
    with pytest.raises(ValueError):
        find_first_mismatch(df)


def test_find_first_mismatch_is_stable_with_unsorted_rows():
    df = pd.DataFrame(
        [
            {"tv_seq": 3, "py_seq": 3, "all_core_match": False},
            {"tv_seq": 1, "py_seq": 1, "all_core_match": False},
            {"tv_seq": 2, "py_seq": 2, "all_core_match": False},
        ]
    )
    row = find_first_mismatch(df)
    assert row is not None
    assert int(row["tv_seq"]) == 1
