"""Tests for generate_index.py (pytest + stdlib only).

Covers: dotfile extension semantics, the .NET word-sort key on a crafted
list (expected order derived from the documented rule), cell
truncation/escaping, heading/body extraction, and a --check round-trip
against a temporary git repository (never the real repository).
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().with_name("generate_index.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("generate_index", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


gi = _load_module()


# ---------------------------------------------------------------------------
# Dotfile / .NET GetExtension semantics
# ---------------------------------------------------------------------------


def test_dotfile_single_dot_has_whole_name_as_extension():
    stem, ext = gi.split_stem_and_extension(".gitignore")
    assert stem == ""
    assert ext == ".gitignore"


def test_dotfile_row_topic_and_summary():
    row = gi.build_row("/does/not/matter", ".gitignore")
    assert row == "| `.gitignore` | - | .gitignore | GITIGNORE file |"


def test_normal_file_extension_unaffected():
    stem, ext = gi.split_stem_and_extension("report.md")
    assert (stem, ext) == ("report", ".md")


def test_no_extension_file_unaffected():
    stem, ext = gi.split_stem_and_extension("README")
    assert (stem, ext) == ("README", "")


def test_dotfile_with_second_dot_is_not_special_cased():
    # Two dots total -> falls through to plain os.path.splitext, matching
    # .NET's "last dot to end of string" rule, which agrees with splitext
    # here (only the pure-leading-dot shape needs the special case).
    stem, ext = gi.split_stem_and_extension(".env.local")
    assert (stem, ext) == (".env", ".local")


# ---------------------------------------------------------------------------
# .NET word-sort key
# ---------------------------------------------------------------------------


def test_dotnet_sort_key_crafted_order():
    # Rule under test (see dotnet_word_sort_key docstring):
    #   1. '-' is stripped out entirely before comparing.
    #   2. Remaining chars rank: '_', '/', '\\', '.' (0) < digits (1)
    #      < everything else, case-insensitively (2).
    #   3. Ties break on the original (unstripped) string.
    #
    # Expected order derived by hand from that rule:
    #   "a-b"   -> stripped "ab"  -> [(2,'a'), (2,'b')]
    #   "a_b"   -> stripped "a_b" -> [(2,'a'), (0,'_'), (2,'b')]
    #   "a.b"   -> stripped "a.b" -> [(2,'a'), (0,'.'), (2,'b')]
    #   "a1b"   -> stripped "a1b" -> [(2,'a'), (1,'1'), (2,'b')]
    #   "aB"    -> stripped "aB"  -> [(2,'a'), (2,'b')]  (case-folded)
    #   "ab"    -> stripped "ab"  -> [(2,'a'), (2,'b')]
    # After the first char 'a' ties across all six, the second element's
    # category decides: '_' and '.' (category 0, compared by raw char code,
    # '.' = 0x2E < '_' = 0x5F) come before digits (category 1, '1'), which
    # come before letters (category 2: 'b' from "a-b"/"aB"/"ab" all equal
    # once case-folded, so those three tie and fall back to the raw string
    # for a stable, deterministic order).
    items = ["a1b", "a_b", "a.b", "a-b", "aB", "ab"]
    expected = ["a.b", "a_b", "a1b", "a-b", "aB", "ab"]
    assert sorted(items, key=gi.dotnet_word_sort_key) == expected


def test_dotnet_sort_key_ignores_hyphen_entirely():
    # "a-b" and "ab" compare identically once '-' is stripped, so the tie
    # breaks on the raw (unstripped) string -> "a-b" sorts before "ab"
    # because '-' (0x2D) < 'b' (0x62) in the raw-string tiebreak.
    assert sorted(["ab", "a-b"], key=gi.dotnet_word_sort_key) == ["a-b", "ab"]


def test_dotnet_sort_key_case_insensitive_for_letters():
    assert sorted(["Banana", "apple"], key=gi.dotnet_word_sort_key) == ["apple", "Banana"]


def test_dotnet_sort_key_digits_before_letters():
    assert sorted(["b1", "1b"], key=gi.dotnet_word_sort_key) == ["1b", "b1"]


# ---------------------------------------------------------------------------
# Cell cleaning: truncation + escaping
# ---------------------------------------------------------------------------


def test_clean_cell_escapes_pipes():
    assert gi.clean_cell("a|b", 180) == "a\\|b"


def test_clean_cell_collapses_whitespace_and_trims():
    assert gi.clean_cell("  a   b\t\nc  ", 180) == "a b c"


def test_clean_cell_none_is_empty_string():
    assert gi.clean_cell(None, 180) == ""


@pytest.mark.parametrize("limit", [180, 120])
def test_clean_cell_truncates_with_ellipsis(limit):
    # 180 is the path/summary column limit, 120 the topic column limit.
    value = "x" * (limit + 50)
    result = gi.clean_cell(value, limit)
    assert len(result) == limit
    assert result.endswith("...")
    assert result[: limit - 3] == "x" * (limit - 3)


def test_clean_cell_exact_limit_not_truncated():
    value = "x" * 180
    assert gi.clean_cell(value, 180) == value


# ---------------------------------------------------------------------------
# Date extraction
# ---------------------------------------------------------------------------


def test_file_date_hyphenated():
    assert gi.file_date("REPORT_2026-08-25.md") == "2026-08-25"


def test_file_date_underscored():
    assert gi.file_date("REPORT_2026_08_25.md") == "2026-08-25"


def test_file_date_plain_digits():
    assert gi.file_date("REPORT20260825.md") == "2026-08-25"


def test_file_date_none_found():
    assert gi.file_date("README.md") == "-"


# ---------------------------------------------------------------------------
# Heading / body extraction
# ---------------------------------------------------------------------------


def test_build_row_extracts_heading_and_body(tmp_path):
    target = tmp_path / "note.md"
    target.write_text(
        "\n> a blockquote to skip\n# My Heading\n\nFirst real body line.\nSecond line.",
        encoding="utf-8",
    )
    row = gi.build_row(str(tmp_path), "note.md")
    assert "My Heading" in row
    assert "First real body line." in row


def test_build_row_skips_fences_and_rules_for_body(tmp_path):
    target = tmp_path / "note.md"
    target.write_text("# Heading\n```\n---\n| table row |\nActual body.", encoding="utf-8")
    row = gi.build_row(str(tmp_path), "note.md")
    assert "Actual body." in row


def test_build_row_no_heading_falls_back_to_extension_summary(tmp_path):
    target = tmp_path / "plain.txt"
    target.write_text("just some text\nmore text\n", encoding="utf-8")
    row = gi.build_row(str(tmp_path), "plain.txt")
    assert "just some text" in row


def test_build_row_unreadable_file_reports_exception_type(tmp_path):
    target = tmp_path / "bad.md"
    # Invalid UTF-8 byte sequence triggers UnicodeDecodeError under strict
    # decoding, exercising the "Unreadable during index generation" path.
    target.write_bytes(b"\xff\xfe\x00# not valid utf-8 heading\x80\x81")
    row = gi.build_row(str(tmp_path), "bad.md")
    assert "Unreadable during index generation:" in row


def test_build_row_non_text_extension_uses_extension_summary(tmp_path):
    target = tmp_path / "data.bin"
    target.write_bytes(b"\x00\x01\x02")
    row = gi.build_row(str(tmp_path), "data.bin")
    assert row == "| `data.bin` | - | data | BIN file |"


# ---------------------------------------------------------------------------
# --check round-trip against a temporary git repo
# ---------------------------------------------------------------------------


def _run_git(args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


@pytest.fixture
def temp_git_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _run_git(["init", "-q"], cwd=repo)
    _run_git(["config", "user.email", "test@example.com"], cwd=repo)
    _run_git(["config", "user.name", "Test"], cwd=repo)

    (repo / "alpha.md").write_text("# Alpha Heading\nAlpha body.\n", encoding="utf-8")
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    sub = repo / "sub"
    sub.mkdir()
    (sub / "beta_2026-01-02.txt").write_text("beta body line\n", encoding="utf-8")

    _run_git(["add", "alpha.md", ".gitignore", "sub/beta_2026-01-02.txt"], cwd=repo)
    _run_git(["commit", "-q", "-m", "seed"], cwd=repo)
    return repo


def test_check_reports_mismatch_when_index_missing(temp_git_repo):
    output = temp_git_repo / "INDEX.md"
    lines, files = gi.build_index_lines(str(temp_git_repo), str(output))
    content = gi.render_content(lines)
    assert len(files) == 3

    exit_code = gi.run_check(str(output), content)
    assert exit_code == 1
    assert not output.exists()  # --check must write nothing


def test_check_round_trip_write_then_check_ok(temp_git_repo):
    output = temp_git_repo / "INDEX.md"

    exit_code = gi.main(["--root", str(temp_git_repo), "--output", str(output)])
    assert exit_code == 0
    assert output.exists()

    exit_code = gi.main(["--root", str(temp_git_repo), "--output", str(output), "--check"])
    assert exit_code == 0


def test_check_detects_drift_after_source_file_changes(temp_git_repo):
    output = temp_git_repo / "INDEX.md"
    assert gi.main(["--root", str(temp_git_repo), "--output", str(output)]) == 0

    # Change tracked content (git ls-files still lists it; row content changes).
    (temp_git_repo / "alpha.md").write_text("# Alpha Heading\nChanged body.\n", encoding="utf-8")

    exit_code = gi.main(["--root", str(temp_git_repo), "--output", str(output), "--check"])
    assert exit_code == 1
    # --check must not overwrite the on-disk file.
    assert "Changed body." not in output.read_text(encoding="utf-8")


def test_write_mode_is_deterministic(temp_git_repo, tmp_path):
    # Write outside the indexed root so the first run's output file does not
    # itself become a newly-untracked, newly-indexed file for the second run.
    out1 = tmp_path / "out1.md"
    out2 = tmp_path / "out2.md"
    gi.main(["--root", str(temp_git_repo), "--output", str(out1)])
    gi.main(["--root", str(temp_git_repo), "--output", str(out2)])
    assert out1.read_bytes() == out2.read_bytes()


def test_output_file_excluded_from_its_own_index(temp_git_repo):
    output = temp_git_repo / "INDEX.md"
    # Track an INDEX.md-named file too, to prove the generator excludes
    # whatever the *current* --output path resolves to, not just a literal
    # "INDEX.md" string match.
    _run_git(["add", "-A"], cwd=temp_git_repo)
    _lines, files = gi.build_index_lines(str(temp_git_repo), str(output))
    assert "INDEX.md" not in files


def test_index_content_is_utf8_no_bom_lf_single_trailing_newline(temp_git_repo):
    output = temp_git_repo / "INDEX.md"
    gi.main(["--root", str(temp_git_repo), "--output", str(output)])
    raw = output.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")  # no UTF-8 BOM
    assert b"\r\n" not in raw  # LF only
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    raw.decode("utf-8")  # must be valid UTF-8


def test_write_mode_prints_expected_message(temp_git_repo, capsys):
    output = temp_git_repo / "INDEX.md"
    gi.main(["--root", str(temp_git_repo), "--output", str(output)])
    captured = capsys.readouterr()
    assert captured.out.strip() == f"Indexed 3 files into {output}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
