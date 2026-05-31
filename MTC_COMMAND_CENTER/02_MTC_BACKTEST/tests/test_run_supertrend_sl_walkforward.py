from scripts.run_supertrend_sl_walkforward import PROFILE_SPACE_FILES, resolve_space_file


def test_resolve_space_file_uses_profile_default():
    assert resolve_space_file("atr", "") == PROFILE_SPACE_FILES["atr"]
    assert resolve_space_file("pct", "") == PROFILE_SPACE_FILES["pct"]
    assert resolve_space_file("swing_plus_atr", "") == PROFILE_SPACE_FILES["swing_plus_atr"]
    assert resolve_space_file("swing_atr", "") == PROFILE_SPACE_FILES["swing_atr"]


def test_resolve_space_file_respects_override():
    assert resolve_space_file("atr", "configs/spaces/custom.json") == "configs/spaces/custom.json"
