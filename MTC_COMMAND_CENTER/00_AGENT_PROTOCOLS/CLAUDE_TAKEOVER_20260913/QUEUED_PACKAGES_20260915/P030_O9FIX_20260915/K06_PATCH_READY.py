"""K-06 (Gemini delta NIT, 2026-09-15 16:15Z) — ready-to-apply, NOT applied: tighten the message regex per arm in
`check_p030_archive_exporter.py::test_source_line_invalid_for_overflow_and_nan_literals` so an overflow token that were
re-classified as unparseable JSON would fail the test. Apply only on the Wednesday exact-Opus reviewer's word (then commit,
re-run the checker, re-pin lane 3 to the new HEAD, grep the old SHA to 0, and re-read the brief prose)."""
import pathlib
import sys

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "C:/tmp/P030_INTEGRATION_20260913/check_p030_archive_exporter.py")
raw = path.read_bytes()
nl = b"\r\n" if b"\r\n" in raw else b"\n"
text = raw.decode("utf-8")
old = (
    '            for name, line in (\n'
    '                ("overflow.jsonl", b\'{"open":1e999}\\n\'),\n'
    '                ("nan.jsonl", b\'{"open":NaN}\\n\'),\n'
    '                ("nested.jsonl", b\'{"a":{"b":[1,-1e999]}}\\n\'),\n'
    '            ):\n'
    '                source = root / name\n'
    '                source.write_bytes(line)\n'
    '                self._refused("source_line_invalid", "non-finite|not parseable", source, root)\n'
).replace("\n", nl.decode())
new = (
    '            for name, line, message in (\n'
    '                ("overflow.jsonl", b\'{"open":1e999}\\n\', "carries a non-finite number"),\n'
    '                ("nan.jsonl", b\'{"open":NaN}\\n\', "not parseable JSON"),\n'
    '                ("nested.jsonl", b\'{"a":{"b":[1,-1e999]}}\\n\', "carries a non-finite number"),\n'
    '            ):\n'
    '                source = root / name\n'
    '                source.write_bytes(line)\n'
    '                self._refused("source_line_invalid", message, source, root)\n'
).replace("\n", nl.decode())
if text.count(old) != 1:
    print("REFUSE: the K-06 arm is not exactly as expected (count=%d) — read the file before applying" % text.count(old))
    sys.exit(2)
if "--apply" not in sys.argv:
    print("DRY RUN: patch would apply cleanly to", path, "(pass --apply to write)")
    sys.exit(0)
path.write_bytes(text.replace(old, new).encode("utf-8"))
print("APPLIED to", path)
# Lead dry run 2026-09-15 16:29Z: applied to a scratch copy of 153edee9's five P030 files + opsa tools → checker "Ran 20 tests … OK",
# D-13 RED RAW REFUSAL / GREEN EXPORTED CAPTURE: PASS. Not applied to the branch (would force a lane-3 re-pin for a NIT).
