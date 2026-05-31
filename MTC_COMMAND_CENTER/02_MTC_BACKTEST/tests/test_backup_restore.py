from pathlib import Path

from scripts.backup_restore import create_backup, restore_backup


def test_backup_restore_roundtrip(tmp_path: Path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    file_a = src_dir / "a.txt"
    file_a.write_text("hello", encoding="utf-8")

    out_dir = tmp_path / "out"
    archive = create_backup(out_dir, [src_dir])
    assert archive.exists()

    restore_dir = tmp_path / "restore"
    restore_backup(archive, restore_dir)
    restored = restore_dir / "src" / "a.txt"
    assert restored.exists()
    assert restored.read_text(encoding="utf-8") == "hello"
