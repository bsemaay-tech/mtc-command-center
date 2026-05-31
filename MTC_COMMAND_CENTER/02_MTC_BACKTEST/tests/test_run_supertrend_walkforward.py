from scripts.run_supertrend_walkforward import PROFILE_SPACE_FILES, resolve_space_file


def test_resolve_space_file_uses_profile_default():
    assert resolve_space_file("high_atr", "") == PROFILE_SPACE_FILES["high_atr"]
    assert resolve_space_file("short_atr", "") == PROFILE_SPACE_FILES["short_atr"]


def test_resolve_space_file_respects_override():
    assert resolve_space_file("high_atr", "configs/spaces/custom.json") == "configs/spaces/custom.json"
