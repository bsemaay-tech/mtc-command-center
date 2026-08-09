# WP-L Phase 2 Stage 2 — R4-5 runner (PREREGISTERED, one-use).
"""D026 function-level Arm 1 falsification for RP4-C3 `restore_into`.

SCOPE CLAIM — the ONLY thing this runner is offered as evidence for:

    the two-line `dst_path.is_symlink()` Fail guard inside RP4-C3
    `restore_into` is load-bearing. Delete exactly those two lines and a
    DANGLING SYMLINK destination is followed: a real SQLite database is
    written at the link target, outside the restore root, while the link
    itself is left looking untouched.

It claims nothing else. It is NOT a C3 run: no bundle is verified, no
`verify_bundle` is called, no manifest/db/invariants hash is adjudicated, no
candidate release tree is imported, no accepted-bundle path is required. It
touches no service, no unit, no credential, no port and no network.

Both arms are exercised at FUNCTION level against byte-exact extracted RP4-C3
bytes: GREEN calls the accepted function itself, RED calls a mutant that
differs from it by exactly the two deleted guard lines and nothing else.

rc contract:
  0 = both arms produced their preregistered expected outcome
  1 = an arm contradicted its preregistered expected outcome
  3 = could not evaluate (never re-read as a pass)

Artifacts are PRESERVED: the /tmp/r45.* root is never cleaned up, on any path.
"""

import difflib
import hashlib
import importlib.util
import os
import sqlite3
import stat
import sys
import tempfile
from pathlib import Path

PASS_RC, FAIL_RC, STOP_RC = 0, 1, 3

# Stage 1 frozen identity of the accepted block.
RP4_SHA256 = "0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5"
RP4_LINES = 295

# The exact two lines the RED mutant removes, and nothing else.
GUARD_COND = "if dst_path.is_symlink():"
GUARD_RAISE_PREFIX = 'raise Fail(f"restore destination is a symlink:'

SQLITE_MAGIC = b"SQLite format 3\x00"

_LOG = []


class Stop(Exception):
    """Could not evaluate. Never re-read as an arm outcome."""


class Contradiction(Exception):
    """An arm did not produce its preregistered expected outcome."""


def out(msg):
    print(msg, flush=True)
    _LOG.append(str(msg))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_module(name: str, path: Path):
    """Import a file by absolute path. Module-level code in RP4-C3 is imports,
    constants and defs only; its `__main__` guard keeps `main()` unrun."""
    try:
        spec = importlib.util.spec_from_file_location(name, str(path))
        if spec is None or spec.loader is None:
            raise Stop(f"module_spec_unavailable path={path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    except Stop:
        raise
    except Exception as exc:
        raise Stop(f"module_import_failed path={path} {exc.__class__.__name__}: {exc}") from exc
    return module


def derive_mutant(text: str):
    """Mechanically delete ONLY the two-line symlink guard inside restore_into.

    No rewrite, no reformat, no re-indent, no other edit. The deletion is
    located structurally (inside `def restore_into`), proven unique in the whole
    file, and the byte delta is asserted to be exactly the two removed lines.
    """
    lines = text.split("\n")

    def_hits = [i for i, line in enumerate(lines) if line.startswith("def restore_into(")]
    if len(def_hits) != 1:
        raise Stop(f"restore_into_def_not_unique count={len(def_hits)}")
    start = def_hits[0]

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith(("def ", "class ", "if __name__")):
            end = i
            break

    inner = [
        i
        for i in range(start + 1, end - 1)
        if lines[i].strip() == GUARD_COND
        and lines[i + 1].strip().startswith(GUARD_RAISE_PREFIX)
    ]
    everywhere = [i for i, line in enumerate(lines) if line.strip() == GUARD_COND]
    if len(inner) != 1 or len(everywhere) != 1 or inner[0] != everywhere[0]:
        raise Stop(
            f"guard_not_uniquely_located inner={inner} file_wide={everywhere} "
            f"restore_into_span=({start},{end})"
        )

    j = inner[0]
    removed = lines[j:j + 2]
    mutant = "\n".join(lines[:j] + lines[j + 2:])

    delta = len(text.encode("utf-8")) - len(mutant.encode("utf-8"))
    expected_delta = len((removed[0] + "\n" + removed[1] + "\n").encode("utf-8"))
    if delta != expected_delta:
        raise Stop(f"mutation_delta_unexpected delta={delta} expected={expected_delta}")

    return mutant, removed, j


def make_source_db(path: Path) -> None:
    """A real SQLite database, not a stub file."""
    try:
        conn = sqlite3.connect(str(path))
        conn.execute("CREATE TABLE r45_rows (id INTEGER PRIMARY KEY, note TEXT NOT NULL)")
        conn.executemany(
            "INSERT INTO r45_rows (id, note) VALUES (?, ?)",
            [(1, "wpl-p2-r45-arm1"), (2, "restore-into-guard"), (3, "d026")],
        )
        conn.execute("PRAGMA journal_mode=DELETE")
        conn.commit()
        conn.close()
    except (OSError, sqlite3.Error) as exc:
        raise Stop(f"source_db_creation_failed {exc.__class__.__name__}: {exc}") from exc


def build_arm(root: Path, label: str):
    """A disjoint arm root holding a dest/ whose `restored.db` is a DANGLING
    symlink pointing at an ABSENT outside/target.db."""
    arm = root / label
    dest = arm / "dest"
    outside = arm / "outside"
    try:
        arm.mkdir(mode=0o700)
        dest.mkdir(mode=0o700)
        outside.mkdir(mode=0o700)
        target = outside / "target.db"
        link = dest / "restored.db"
        os.symlink(str(target), str(link))
    except OSError as exc:
        raise Stop(f"arm_setup_failed label={label} {exc.__class__.__name__}: {exc}") from exc
    if not link.is_symlink():
        raise Stop(f"arm_link_not_symlink label={label} path={link}")
    if os.path.exists(str(link)):
        raise Stop(f"arm_link_not_dangling label={label} path={link}")
    if os.path.lexists(str(target)):
        raise Stop(f"arm_target_present_before_run label={label} path={target}")
    return arm, dest, outside, target, link


def link_state(link: Path):
    return {
        "islink": link.is_symlink(),
        "readlink": os.readlink(str(link)) if link.is_symlink() else None,
        "lexists": os.path.lexists(str(link)),
        "resolves": os.path.exists(str(link)),
    }


def report_state(label: str, when: str, link: Path, target: Path) -> dict:
    st = link_state(link)
    tgt_present = os.path.lexists(str(target))
    tgt_mode = None
    tgt_size = None
    tgt_head = None
    if tgt_present:
        info = os.lstat(str(target))
        tgt_mode = stat.filemode(info.st_mode)
        tgt_size = info.st_size
        with open(str(target), "rb") as handle:
            tgt_head = handle.read(len(SQLITE_MAGIC))
    out(
        f"R45_{label}_{when} link={link} islink={st['islink']} "
        f"readlink={st['readlink']} link_resolves={st['resolves']} "
        f"target={target} target_present={tgt_present} target_mode={tgt_mode} "
        f"target_size={tgt_size} target_magic={tgt_head!r}"
    )
    st.update({"target_present": tgt_present, "target_size": tgt_size, "target_head": tgt_head})
    return st


def run_red(module, source_db: Path, link: Path, target: Path) -> None:
    """EXPECTED (the defect the guard prevents): restore_into RETURNS, the
    dangling link is followed, and a real SQLite database appears at the
    OUTSIDE target, with the symlink itself unchanged."""
    before = report_state("RED", "pre", link, target)
    out(f"R45_RED_command mutant.restore_into(mutant.open_readonly({source_db!s}), {link!s})")
    try:
        src_conn = module.open_readonly(source_db)
    except Exception as exc:
        raise Stop(f"red_source_open_failed {exc.__class__.__name__}: {exc}") from exc
    dst_conn = None
    try:
        dst_conn = module.restore_into(src_conn, link)
    except module.Fail as exc:
        raise Contradiction(f"red_arm_raised_Fail: {exc}") from exc
    except module.Stop as exc:
        raise Stop(f"red_arm_unevaluable: {exc}") from exc
    except Exception as exc:
        raise Stop(f"red_arm_unexpected_exception {exc.__class__.__name__}: {exc}") from exc
    finally:
        src_conn.close()
        if dst_conn is not None:
            dst_conn.close()
    out("R45_RED_outcome restore_into=returned exception=none")

    after = report_state("RED", "post", link, target)
    if not after["target_present"]:
        raise Contradiction(f"red_target_absent path={target}")
    info = os.lstat(str(target))
    if not stat.S_ISREG(info.st_mode):
        raise Contradiction(f"red_target_not_regular path={target} mode={stat.filemode(info.st_mode)}")
    if info.st_size <= 0:
        raise Contradiction(f"red_target_empty path={target} size={info.st_size}")
    if after["target_head"] != SQLITE_MAGIC:
        raise Contradiction(f"red_target_not_sqlite path={target} head={after['target_head']!r}")
    try:
        probe = sqlite3.connect(f"file:{target}?mode=ro", uri=True)
        rows = probe.execute("SELECT count(*) FROM r45_rows").fetchone()[0]
        probe.close()
    except sqlite3.Error as exc:
        raise Contradiction(f"red_target_not_readable_sqlite {exc.__class__.__name__}: {exc}") from exc
    out(f"R45_RED_target_rows={rows}")
    if not after["islink"] or after["readlink"] != before["readlink"]:
        raise Contradiction(
            f"red_symlink_mutated before={before['readlink']} after={after['readlink']}"
        )
    out(f"R45_RED expected_outcome=observed target_written_outside_restore_root={target}")


def run_green(module, source_db: Path, link: Path, target: Path) -> None:
    """EXPECTED (the accepted behaviour): restore_into raises the exact Fail
    `restore destination is a symlink: <path>`, which RP4-C3 `main` classifies
    as inner rc 1; the outside target stays ABSENT and the link is unchanged."""
    before = report_state("GREEN", "pre", link, target)
    out(f"R45_GREEN_command exact.restore_into(exact.open_readonly({source_db!s}), {link!s})")
    try:
        src_conn = module.open_readonly(source_db)
    except Exception as exc:
        raise Stop(f"green_source_open_failed {exc.__class__.__name__}: {exc}") from exc
    raised = None
    returned = None
    try:
        returned = module.restore_into(src_conn, link)
    except module.Fail as exc:
        raised = exc
    except module.Stop as exc:
        raise Stop(f"green_arm_unevaluable: {exc}") from exc
    except Exception as exc:
        raise Stop(f"green_arm_unexpected_exception {exc.__class__.__name__}: {exc}") from exc
    finally:
        src_conn.close()
        if returned is not None:
            returned.close()

    if raised is None:
        raise Contradiction("green_arm_returned_without_Fail")
    expected_msg = f"restore destination is a symlink: {link}"
    out(f"R45_GREEN_outcome exception=Fail message={str(raised)!r}")
    if str(raised) != expected_msg:
        raise Contradiction(f"green_message_differs actual={str(raised)!r} expected={expected_msg!r}")

    inner_rc = module.FAIL_RC
    out(f"R45_GREEN_classified inner_rc={inner_rc} (RP4-C3 main maps Fail -> FAIL_RC)")
    if inner_rc != 1:
        raise Contradiction(f"green_inner_rc={inner_rc} expected=1")

    after = report_state("GREEN", "post", link, target)
    if after["target_present"]:
        raise Contradiction(f"green_target_created path={target}")
    if not after["islink"] or after["readlink"] != before["readlink"]:
        raise Contradiction(
            f"green_symlink_mutated before={before['readlink']} after={after['readlink']}"
        )
    out("R45_GREEN expected_outcome=observed target_absent=yes symlink_unchanged=yes")


def main(argv) -> int:
    root = None
    try:
        if len(argv) != 2:
            raise Stop(f"usage R4_5_runner.py <exact RP4-C3.py path> argc={len(argv) - 1}")
        rp4_path = Path(argv[1])
        if not rp4_path.is_file() or rp4_path.is_symlink():
            raise Stop(f"rp4_path_not_regular_file path={rp4_path}")

        actual_sha = sha256_file(rp4_path)
        out(f"R45_rp4 path={rp4_path} sha256={actual_sha} expected={RP4_SHA256}")
        if actual_sha != RP4_SHA256:
            raise Stop(f"rp4_sha256_mismatch actual={actual_sha} expected={RP4_SHA256}")

        raw = rp4_path.read_bytes()
        text = raw.decode("utf-8")
        line_count = text.count("\n")
        out(f"R45_rp4 bytes={len(raw)} lines={line_count} expected_lines={RP4_LINES}")
        if line_count != RP4_LINES:
            raise Stop(f"rp4_line_count={line_count} expected={RP4_LINES}")

        root = Path(tempfile.mkdtemp(prefix="r45.", dir="/tmp"))
        os.chmod(str(root), 0o700)
        out(f"R45_root={root} preserved=yes cleanup=never")

        mutant_dir = root / "mutant"
        mutant_dir.mkdir(mode=0o700)
        mutant_text, removed, guard_index = derive_mutant(text)
        mutant_path = mutant_dir / "RP4-C3_mutant_no_symlink_guard.py"
        mutant_path.write_bytes(mutant_text.encode("utf-8"))
        mutant_sha = sha256_file(mutant_path)
        out(f"R45_mutant path={mutant_path} sha256={mutant_sha}")
        out(f"R45_mutant removed_lines={guard_index + 1}-{guard_index + 2} count=2")
        for offset, line in enumerate(removed):
            out(f"R45_mutant removed[{offset}]={line!r}")
        diff_text = "".join(
            difflib.unified_diff(
                text.splitlines(keepends=True),
                mutant_text.splitlines(keepends=True),
                fromfile=f"accepted/{rp4_path.name}",
                tofile=f"mutant/{mutant_path.name}",
                n=3,
            )
        )
        (mutant_dir / "mutant.diff").write_bytes(diff_text.encode("utf-8"))
        out("R45_mutant_diff_begin")
        for line in diff_text.splitlines():
            out(line)
        out("R45_mutant_diff_end")
        out(f"R45_mutant_diff_sha256={sha256_bytes(diff_text.encode('utf-8'))}")

        exact_mod = load_module("rp4_exact", rp4_path)
        mutant_mod = load_module("rp4_mutant", mutant_path)

        source_dir = root / "source"
        source_dir.mkdir(mode=0o700)
        source_db = source_dir / "source.db"
        make_source_db(source_db)
        out(f"R45_source_db={source_db} sha256={sha256_file(source_db)} bytes={source_db.stat().st_size}")

        _, _, _, red_target, red_link = build_arm(root, "red")
        _, _, _, green_target, green_link = build_arm(root, "green")
        out(f"R45_arms red_root={root / 'red'} green_root={root / 'green'} disjoint=yes")

        run_red(mutant_mod, source_db, red_link, red_target)
        run_green(exact_mod, source_db, green_link, green_target)

        out("R45 PASS arms=red,green both_expected_outcomes=observed")
        out("R45_SCOPE claim=guard-scope-only: the two-line dst_path.is_symlink Fail "
            "guard in RP4-C3 restore_into is load-bearing. No C3 verdict, no bundle "
            "verification, no manifest/db/invariants adjudication is claimed.")
        rc = PASS_RC
    except Contradiction as exc:
        out(f"R45_FAIL reason={exc}")
        rc = FAIL_RC
    except Stop as exc:
        out(f"R45_STOP reason={exc}")
        rc = STOP_RC
    except Exception as exc:  # never silently become a pass
        out(f"R45_STOP reason=unhandled {exc.__class__.__name__}: {exc}")
        rc = STOP_RC

    if root is not None:
        out(f"R45_ARTIFACTS_PRESERVED root={root} rc={rc}")
        try:
            (root / "R45_SUMMARY.txt").write_bytes(("\n".join(_LOG) + "\n").encode("utf-8"))
        except OSError as exc:
            out(f"R45_NOTE summary_write_failed {exc.__class__.__name__}: {exc}")
    else:
        out(f"R45_ARTIFACTS_PRESERVED root=<none allocated> rc={rc}")
    print(f"R45_RC={rc}", flush=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
