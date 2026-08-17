"""Tests for the Package 4 owner analysis-package generator.

Stdlib + pytest only. No network. All runtime-generated fixtures are created
inside ``tmp_path`` by each test; the only committed fixtures live under
``fixtures/src/``.
"""

import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG))

import generate_analysis_package as gap

FIXTURES = PKG / "fixtures"
SRC = FIXTURES / "src"

COMMITTED_INPUTS = [
    SRC / "sample_settings.txt",
    SRC / "app_config.txt",
    SRC / "notes_with_creds.md",
    SRC / "hex_addresses.log",
]

# Every obviously synthetic planted value -> the redaction kind that must
# replace it. The full value must never appear un-redacted in the bundle.
PLANTED_SECRETS = {
    # fixtures/src/sample_settings.txt
    "FAKE-PASSWORD-do-NOT-use-0001": "assignment",
    "FAKE-TOKEN-qwerty-4567890123": "assignment",
    # fixtures/src/app_config.txt
    "FAKEKEY000000000000000000": "assignment",
    "FAKETOKEN000000000000000000": "assignment",
    "FAKEPASSWORD000000000000000000": "assignment",
    "FAKESECRET000000000000000000": "assignment",
    # fixtures/src/notes_with_creds.md
    "FAKEBEARER000000000000000000000000": "bearer",
    "AKIAFAKE000000000001": "aws_key_id",
    "FAKECOMMENTPASSWORD00000000000000": "assignment",
    "FAKECOMMENTTOKEN00000000000000": "assignment",
    "FAKECOMMENTSECRET00000000000000": "assignment",
    # fixtures/src/hex_addresses.log
    "0x0123456789abcdef0123456789abcdef01234567": "hex_address",
    "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef": "hex_address",
    "0123456789ABCDEF0123456789ABCDEF01234567": "long_token",
    "FakeBase64Token9G7H5J3K1L8M2N4P6Q0R7S9T3U5V8W2X4Y6Z0A1B2C3D4E5F6G7H8J9K0L1M2N3P4Q5R6S7T8U9V0W1X2Y3Z4": "long_token",
}

EXPECTED_COUNTS = {
    "assignment": 9,
    "aws_key_id": 1,
    "bearer": 1,
    "hex_address": 2,
    "long_token": 2,
}


def _run_bundle(tmp_path, inputs, timestamp="2026-08-18T00:00:00Z", output="bundle.md"):
    cfg = {
        "timestamp": timestamp,
        "output": output,
        "inputs": [str(p) for p in inputs],
    }
    out_path, stats = gap.generate_bundle(cfg, tmp_path)
    text = (tmp_path / output).read_text(encoding="utf-8")
    return out_path, stats, text


def test_every_planted_secret_redacted_and_markers_counted(tmp_path):
    _, _, text = _run_bundle(tmp_path, COMMITTED_INPUTS)

    for secret in PLANTED_SECRETS:
        assert secret not in text, "planted secret leaked: %r" % secret

    for kind, expected in EXPECTED_COUNTS.items():
        marker = "[REDACTED:%s]" % kind
        actual = text.count(marker)
        assert actual == expected, "%s: expected %d markers, found %d" % (
            kind, expected, actual)

    assert "Total redactions: 15" in text


def test_oversize_file_truncated_at_byte_cap(tmp_path):
    # 'z' filler on purpose: 'a' runs are valid hex and would (correctly) be
    # redacted as long hex tokens, collapsing the content.
    big = tmp_path / "oversize.txt"
    big.write_text(
        "START_KEEP_ME\n" + ("z" * gap.MAX_FILE_BYTES) + "\nEND_TRUNCATED_AWAY\n",
        encoding="ascii",
    )
    assert big.stat().st_size > gap.MAX_FILE_BYTES

    _, _, text = _run_bundle(tmp_path, [big])

    assert "START_KEEP_ME" in text
    assert "END_TRUNCATED_AWAY" not in text
    assert "truncated (byte cap)" in text
    assert "- Included: 204800 bytes" in text


def test_line_cap_truncates_to_4000_lines(tmp_path):
    linecap = tmp_path / "linecap.txt"
    lines = ["line_%04d payload\n" % i for i in range(1, 5001)]
    linecap.write_text("".join(lines), encoding="ascii")
    assert linecap.stat().st_size < gap.MAX_FILE_BYTES

    _, _, text = _run_bundle(tmp_path, [linecap])

    assert "line_0001" in text
    assert "line_4000" in text
    assert "line_4001" not in text
    assert "line_5000" not in text
    assert "truncated (line cap)" in text
    assert " 4000 lines" in text


def test_null_byte_binary_file_excluded(tmp_path):
    binary = tmp_path / "binary.txt"
    binary.write_bytes(b"hello\x00world" + (b"\x00" * 100))

    _, _, text = _run_bundle(tmp_path, [binary])

    assert "binary (null-byte sniff in first 8192 bytes)" in text
    # No file section at all may exist (headings display full paths).
    assert not any(ln.startswith("## File:") for ln in text.splitlines())


def test_binary_extension_denylist_excluded(tmp_path):
    png = tmp_path / "image.png"
    png.write_text("plain text with a .png suffix", encoding="ascii")

    _, _, text = _run_bundle(tmp_path, [png])

    assert "binary (extension denylist: .png)" in text
    assert not any(ln.startswith("## File:") for ln in text.splitlines())


def test_total_content_cap_omits_later_files(tmp_path):
    files = []
    for i in range(11):
        p = tmp_path / ("f%02d.txt" % i)
        p.write_text("x" * (gap.MAX_FILE_BYTES + 100), encoding="ascii")
        files.append(p)

    _, stats, text = _run_bundle(tmp_path, files)

    # Section headings display full paths, so match on the basename suffix of
    # actual "## File:" section lines (an omitted file still appears in the
    # header inventory, which must not count as a section).
    sections = [ln for ln in text.splitlines() if ln.startswith("## File:")]
    assert "omitted: total content cap" in text
    assert any(ln.endswith("f00.txt`") for ln in sections)
    assert any(ln.endswith("f09.txt`") for ln in sections)
    assert not any(ln.endswith("f10.txt`") for ln in sections)
    assert stats["total_bytes"] <= gap.MAX_TOTAL_BYTES


def test_deterministic_output_for_fixed_timestamp(tmp_path):
    inputs = COMMITTED_INPUTS
    ts = "2026-08-18T00:00:00Z"

    gap.generate_bundle(
        {"timestamp": ts, "output": "out1.md",
         "inputs": [str(p) for p in inputs]},
        tmp_path,
    )
    gap.generate_bundle(
        {"timestamp": ts, "output": "out2.md",
         "inputs": [str(p) for p in inputs]},
        tmp_path,
    )

    assert (tmp_path / "out1.md").read_bytes() == (tmp_path / "out2.md").read_bytes()


def _write_cfg(tmp_path, cfg):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    return cfg_path


def test_missing_allowlisted_input_exits_2(tmp_path):
    missing = tmp_path / "missing.txt"
    cfg_path = _write_cfg(tmp_path, {
        "timestamp": "2026-08-18T00:00:00Z",
        "output": "out.md",
        "inputs": [str(missing)],
    })

    rc = gap.main(["--config", str(cfg_path)])

    assert rc == 2
    assert not (tmp_path / "out.md").exists()


def test_credential_store_named_directly_exits_2(tmp_path):
    env = tmp_path / ".env"
    env.write_text("FAKE=1", encoding="ascii")
    cfg_path = _write_cfg(tmp_path, {
        "timestamp": "2026-08-18T00:00:00Z",
        "output": "out.md",
        "inputs": [str(env)],
    })

    rc = gap.main(["--config", str(cfg_path)])

    assert rc == 2
    assert not (tmp_path / "out.md").exists()


def test_dotfile_named_directly_exits_2(tmp_path):
    hidden = tmp_path / ".hidden.txt"
    hidden.write_text("FAKE=1", encoding="ascii")
    cfg_path = _write_cfg(tmp_path, {
        "timestamp": "2026-08-18T00:00:00Z",
        "output": "out.md",
        "inputs": [str(hidden)],
    })

    rc = gap.main(["--config", str(cfg_path)])

    assert rc == 2
    assert not (tmp_path / "out.md").exists()


def test_unknown_config_key_exits_2(tmp_path):
    cfg_path = _write_cfg(tmp_path, {
        "timestamp": "2026-08-18T00:00:00Z",
        "output": "out.md",
        "inputs": [str(SRC / "sample_settings.txt")],
        "extra_unknown_key": 1,
    })

    rc = gap.main(["--config", str(cfg_path)])

    assert rc == 2
    assert not (tmp_path / "out.md").exists()
