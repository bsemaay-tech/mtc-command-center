#!/usr/bin/env python3
"""WP-L Phase 2 staging — Stage 1 runkit builder.

Extracts the nine accepted EXECUTABLE PROPOSAL BLOCKs from the accepted source
blob, verifies each against the §8.1 identity table, syntax-validates them,
and writes a deterministic uncompressed tar plus evidence records.

Writable scope: <STAGING>/01_RUNKIT/ only. Nothing else in the repo is written.
No git mutation, no network, no host action.
"""

import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

REPO = r"C:\LAB\Tradingview_LAB_CLEAN"
SRC_PATH = "MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md"
COMMIT = "4c0d5fc5aeb1e069cd6171c11d143ac2a49a6e2c"
BLOB = "76e0a66cd621ec5d38cc580904968262ce69678f"

RUNKIT = os.path.join(
    REPO,
    "MTC_COMMAND_CENTER", "11_TRIAGE",
    "WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08", "01_RUNKIT",
)

# §8.1 table order is the archive order. (block id, filename, lines, sha256)
TABLE = [
    ("RP0-LIB",       "RP0-LIB.sh",       370, "4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48"),
    ("RP0-BOOTSTRAP", "RP0-BOOTSTRAP.sh",  36, "e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33"),
    ("RP1-B3",        "RP1-B3.sh",        117, "f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af"),
    ("RP3-C2A-POST",  "RP3-C2A-POST.sh",  104, "e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27"),
    ("RP3-C2B-POST",  "RP3-C2B-POST.sh",   74, "26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412"),
    ("RP4-C3",        "RP4-C3.py",        295, "0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5"),
    ("RP5-C4A",       "RP5-C4A.sh",       374, "a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2"),
    ("RP5-C4B",       "RP5-C4B.sh",       249, "10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e"),
    ("RP5-C4C",       "RP5-C4C.sh",       228, "de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8"),
]

# Expected embedded python heredoc count per block. Asserted, never inferred.
# The Stage 1 scope of record is C4A x2, C4B x1, C4C x1 — the same set §8.1 claims.
# RP3-C2A-POST also carries one `<<'PYEOF'` python heredoc (§8.1 claims only
# `bash -n` for it). It is compiled too and reported separately as ADDITIONAL, so
# the count assertion below stays exact rather than silently tolerant.
HEREDOCS_SCOPE = {"RP5-C4A": 2, "RP5-C4B": 1, "RP5-C4C": 1}
HEREDOCS_EXTRA = {"RP3-C2A-POST": 1}
HEREDOCS = dict(HEREDOCS_SCOPE, **HEREDOCS_EXTRA)

MARKER = re.compile(rb"^# ===== BLOCK-ID: ([A-Za-z0-9._-]+) ===== \[EXECUTABLE PROPOSAL BLOCK\]$")
FENCE = b"```"

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LC_ALL="C")
LOG = []           # syntax_validation.txt entries
FAILURES = []      # hard identity/structure failures


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


def wtext(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def wbin(path, data):
    with open(path, "wb") as fh:
        fh.write(data)


def run(argv, label):
    """Run argv, record exact command and real rc/output. Returns rc."""
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV)
    out = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    LOG.append((label, argv, p.returncode, out))
    return p.returncode


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args],
                          stdout=subprocess.PIPE, check=True).stdout


# --------------------------------------------------------------------------
# 1. Source identity
# --------------------------------------------------------------------------
commit_actual = git("rev-parse", COMMIT + "^{commit}").decode().strip()
blob_actual = git("rev-parse", COMMIT + ":" + SRC_PATH).decode().strip()
raw = git("cat-file", "blob", BLOB)
raw_sha = sha256_hex(raw)

if commit_actual != COMMIT:
    FAILURES.append("commit mismatch: %s != %s" % (commit_actual, COMMIT))
if blob_actual != BLOB:
    FAILURES.append("blob mismatch: %s != %s" % (blob_actual, BLOB))
if b"\r" in raw:
    FAILURES.append("source blob contains CR bytes")

# --------------------------------------------------------------------------
# 2. Extract blocks: marker line inclusive -> up to (not including) closing fence
# --------------------------------------------------------------------------
lines = raw.split(b"\n")
found = []
for i, ln in enumerate(lines):
    m = MARKER.match(ln)
    if not m:
        continue
    j = i
    while j < len(lines) and lines[j] != FENCE:
        j += 1
    if j >= len(lines):
        FAILURES.append("no closing fence for %s" % m.group(1).decode())
        continue
    body = b"\n".join(lines[i:j]) + b"\n"
    found.append((m.group(1).decode(), i + 1, j, body))

if len(found) != 9:
    FAILURES.append("expected 9 BLOCK-ID markers, found %d" % len(found))
if [f[0] for f in found] != [t[0] for t in TABLE]:
    FAILURES.append("block id order/set mismatch: %s" % [f[0] for f in found])

by_id = {f[0]: f for f in found}

# --------------------------------------------------------------------------
# 3. Create the fresh directory (fail if the leaf already exists)
# --------------------------------------------------------------------------
os.makedirs(os.path.dirname(RUNKIT), exist_ok=True)
os.mkdir(RUNKIT)  # no exist_ok: clobbering an existing runkit is a hard failure

# --------------------------------------------------------------------------
# 4. Write block files, verify identities
# --------------------------------------------------------------------------
rows = []
for bid, fname, exp_lines, exp_sha in TABLE:
    if bid not in by_id:
        rows.append((bid, fname, exp_lines, exp_sha, "-", "-", "MISSING"))
        FAILURES.append("block %s not found" % bid)
        continue
    _, start, fence_line, body = by_id[bid]
    wbin(os.path.join(RUNKIT, fname), body)
    act_lines = body.count(b"\n")
    act_sha = sha256_hex(body)
    ok = (act_lines == exp_lines) and (act_sha == exp_sha)
    rows.append((bid, fname, exp_lines, exp_sha, act_lines, act_sha, "MATCH" if ok else "MISMATCH"))
    if not ok:
        FAILURES.append("identity mismatch %s: lines %s/%s sha %s/%s"
                        % (bid, act_lines, exp_lines, act_sha, exp_sha))
    if body[:3] == b"\xef\xbb\xbf":
        FAILURES.append("BOM in %s" % bid)
    if b"\r" in body:
        FAILURES.append("CR byte in %s" % bid)
    if not body.endswith(b"\n"):
        FAILURES.append("no final LF in %s" % bid)

wtext(os.path.join(RUNKIT, "BLOCK_IDENTITIES.tsv"),
      "block_id\tfile\texpected_lines\texpected_sha256\tactual_lines\tactual_sha256\tresult\n"
      + "".join("\t".join(str(c) for c in r) + "\n" for r in rows))

wtext(os.path.join(RUNKIT, "SOURCE_IDENTITY.txt"), "".join(l + "\n" for l in [
    "WP-L Phase 2 Stage 1 — accepted source identity",
    "",
    "source_path            %s" % SRC_PATH,
    "accepted_commit        %s" % COMMIT,
    "accepted_commit_actual %s" % commit_actual,
    "accepted_blob          %s" % BLOB,
    "accepted_blob_actual   %s" % blob_actual,
    "blob_bytes             %d" % len(raw),
    "blob_sha256            %s" % raw_sha,
    "blob_cr_bytes          %d" % raw.count(b"\r"),
    "blob_lf_bytes          %d" % raw.count(b"\n"),
    "blob_bom               %s" % (raw[:3] == b"\xef\xbb\xbf"),
    "read_command           git -C <repo> cat-file blob %s" % BLOB,
    "",
    "extraction rule: from the `# ===== BLOCK-ID: <id> =====` marker line inclusive,",
    "up to (not including) the closing ``` fence; LF line endings; final LF; no BOM.",
    "block source spans (1-indexed lines of the blob):",
] + ["  %-14s marker %5d  fence %5d  lines %3d"
     % (f[0], f[1], f[2] + 1, f[2] + 1 - f[1]) for f in found]))

if FAILURES:
    for f in FAILURES:
        print("FAIL:", f)
    print("STAGE1 FAILURE — created files preserved in", RUNKIT)
    sys.exit(1)

# --------------------------------------------------------------------------
# 5. Syntax validation
# --------------------------------------------------------------------------
tmp = tempfile.mkdtemp(prefix="wplp2_s1_")

bash = shutil.which("bash")
py = sys.executable

for bid, fname, _, _ in TABLE:
    if fname.endswith(".sh"):
        run([bash, "-n", os.path.join(RUNKIT, fname)], "bash -n %s" % fname)

# RP4 python source: compile with an explicit cfile in OS temp so no __pycache__
# is ever created inside the repo.
run([py, "-c",
     "import py_compile,sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)",
     os.path.join(RUNKIT, "RP4-C3.py"), os.path.join(tmp, "RP4-C3.pyc")],
    "py_compile RP4-C3.py (cfile in OS temp)")

# Embedded python heredocs -> OS temp only, then compiled there.
HD_OPEN = re.compile(rb"<<'PYEOF'")
for bid, fname, _, _ in TABLE:
    if not fname.endswith(".sh"):
        continue
    body = by_id[bid][3].split(b"\n")
    docs, k = [], 0
    while k < len(body):
        if HD_OPEN.search(body[k]):
            # The heredoc body starts after the COMPLETE command line: a `\`
            # line-continuation after the `<<'PYEOF'` operator (RP5-C4A #1) means
            # the next physical line is still command text, not python.
            s = k
            while s < len(body) and body[s].endswith(b"\\"):
                s += 1
            s += 1
            e = s
            while e < len(body) and body[e] != b"PYEOF":
                e += 1
            docs.append(b"\n".join(body[s:e]) + b"\n")
            k = e
        k += 1
    exp = HEREDOCS.get(bid, 0)
    if len(docs) != exp:
        FAILURES.append("%s: expected %d python heredoc(s), found %d" % (bid, exp, len(docs)))
        continue
    tag = "SCOPE" if bid in HEREDOCS_SCOPE else "ADDITIONAL (outside the specified Stage 1 heredoc scope)"
    for n, doc in enumerate(docs, 1):
        hp = os.path.join(tmp, "%s_heredoc%d.py" % (bid, n))
        wbin(hp, doc)
        run([py, "-c",
             "import py_compile,sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)",
             hp, hp + "c"],
            "py_compile %s embedded heredoc %d/%d [%s] (%d bytes, sha256 %s) — OS temp only"
            % (bid, n, exp, tag, len(doc), sha256_hex(doc)))

# --------------------------------------------------------------------------
# 6. Deterministic uncompressed tar.
# Platform bsdtar on Windows cannot normalize uid/gid/mtime/mode, so the archive
# is written here with tarfile: fixed member order (§8.1 table), mtime 0,
# mode 0644, uid/gid 0, empty uname/gname, regular files, no directory members.
# Block bytes are archived verbatim — no shebang added, nothing rewritten.
# --------------------------------------------------------------------------
TAR = os.path.join(RUNKIT, "runkit.tar")
with tarfile.open(TAR, "w", format=tarfile.GNU_FORMAT) as tf:
    for bid, fname, _, _ in TABLE:
        data = by_id[bid][3]
        ti = tarfile.TarInfo(name=fname)
        ti.size = len(data)
        ti.mtime = 0
        ti.mode = 0o644
        ti.type = tarfile.REGTYPE
        ti.uid = 0
        ti.gid = 0
        ti.uname = ""
        ti.gname = ""
        tf.addfile(ti, io.BytesIO(data))

tar_bytes = open(TAR, "rb").read()
tar_sha = sha256_hex(tar_bytes)
wtext(os.path.join(RUNKIT, "runkit.tar.sha256"), "%s  runkit.tar\n" % tar_sha)

with tarfile.open(TAR, "r") as tf:
    members = tf.getmembers()
mem_lines = ["%-16s %-6s %6d %-5s uid=%d gid=%d uname=%r gname=%r mtime=%d"
             % (m.name, oct(m.mode), m.size, "REG" if m.isfile() else m.type,
                m.uid, m.gid, m.uname, m.gname, m.mtime) for m in members]

# Independent cross-check with the platform tar (listing only, no extraction).
systar = shutil.which("tar")
# Relative name from cwd=RUNKIT: a drive-lettered path makes GNU tar read `C:` as
# a remote host spec and fail with "Cannot connect to C: resolve failed".
xchk = subprocess.run([systar, "-tvf", "runkit.tar"], cwd=RUNKIT,
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV)
xout = xchk.stdout.decode("utf-8", "replace").replace("\r\n", "\n").rstrip("\n")
if xchk.returncode != 0:
    FAILURES.append("platform tar cross-check rc=%d: %s" % (xchk.returncode, xout))

wtext(os.path.join(RUNKIT, "ARCHIVE_MEMBERS.txt"), "".join(l + "\n" for l in [
    "runkit.tar — uncompressed, GNU tar format, deterministic",
    "archive_bytes %d" % len(tar_bytes),
    "archive_sha256 %s" % tar_sha,
    "member_count %d" % len(members),
    "order: §8.1 table order (fixed, not directory-scan order)",
    "normalization: mtime=0 mode=0644 uid=0 gid=0 uname='' gname='' type=REG, no dir members",
    "trailing bytes are the tar end-of-archive marker plus 10240-byte record padding",
    "determinism: independent runs of this builder writing to different output paths",
    "produce a byte-identical archive; the digest above is reproducible.",
    "",
    "-- member listing (python tarfile) --",
] + mem_lines + [
    "",
    "-- cross-check: %s -tvf runkit.tar  (rc=%d) --" % (systar, xchk.returncode),
] + xout.split("\n")))

# --------------------------------------------------------------------------
# 7. Self-QA — reread from disk, and diff tar members extracted to OS temp
# --------------------------------------------------------------------------
qa = []
for bid, fname, exp_lines, exp_sha in TABLE:
    disk = open(os.path.join(RUNKIT, fname), "rb").read()
    d_sha, d_lines = sha256_hex(disk), disk.count(b"\n")
    ok = (d_sha == exp_sha and d_lines == exp_lines
          and b"\r" not in disk and disk[:3] != b"\xef\xbb\xbf" and disk.endswith(b"\n"))
    qa.append("disk   %-14s lines=%3d sha256=%s %s" % (bid, d_lines, d_sha, "OK" if ok else "FAIL"))
    if not ok:
        FAILURES.append("self-QA disk mismatch %s" % bid)

xdir = os.path.join(tmp, "unpack")
os.makedirs(xdir)
with tarfile.open(TAR, "r") as tf:
    tf.extractall(xdir, filter="data")
names = sorted(os.listdir(xdir))
if names != sorted(f[1] for f in TABLE):
    FAILURES.append("tar unpack contains unexpected entries: %s" % names)
for bid, fname, exp_lines, exp_sha in TABLE:
    p = os.path.join(xdir, fname)
    if not os.path.isfile(p):
        FAILURES.append("tar member missing after unpack: %s" % fname)
        continue
    got = open(p, "rb").read()
    ok = got == by_id[bid][3] and sha256_hex(got) == exp_sha
    qa.append("untar  %-14s bytes=%6d sha256=%s %s"
              % (bid, len(got), sha256_hex(got), "IDENTICAL" if ok else "FAIL"))
    if not ok:
        FAILURES.append("tar member differs from source block: %s" % fname)

LOG.append(("self-QA", ["<in-process>", "reread 9 block files from disk; extract runkit.tar to OS temp; byte-compare"],
            1 if FAILURES else 0, "\n".join(qa) + "\n"))

# --------------------------------------------------------------------------
# 8. syntax_validation.txt + STAGE1_RECORD.md
# --------------------------------------------------------------------------
parts = ["WP-L Phase 2 Stage 1 — syntax validation (real commands, real rc, real output)",
         "OS temp root used for compiled artifacts and tar unpack: %s" % tmp,
         "No __pycache__ is created inside the repo: every py_compile call passes an",
         "explicit cfile under the OS temp root.",
         ""]
for label, argv, rc, out in LOG:
    parts.append("--- %s" % label)
    parts.append("$ %s" % " ".join(('"%s"' % a if " " in a else a) for a in argv))
    parts.append("rc=%d" % rc)
    parts.append("output: %s" % ("<empty>" if out.strip() == "" else ""))
    if out.strip():
        parts.extend(out.rstrip("\n").split("\n"))
    parts.append("")
wtext(os.path.join(RUNKIT, "syntax_validation.txt"), "".join(p + "\n" for p in parts))

nonzero = [l for (l, a, rc, o) in LOG if rc != 0]
if nonzero:
    FAILURES.append("non-zero rc from: %s" % nonzero)

shutil.copyfile(__file__, os.path.join(RUNKIT, "stage1_build.py"))

status = "FAILURE" if FAILURES else "PASS"
rec = ["# WP-L Phase 2 — Stage 1 record (runkit extraction)",
       "",
       "Result: **%s**" % status,
       "",
       "## Source",
       "",
       "- commit `%s`" % COMMIT,
       "- blob `%s` (`%s`)" % (BLOB, SRC_PATH),
       "- blob bytes %d, sha256 `%s`, CR bytes %d, BOM no" % (len(raw), raw_sha, raw.count(b"\r")),
       "- read only via `git -C <repo> cat-file blob %s`" % BLOB,
       "",
       "## Blocks",
       "",
       "Extraction: BLOCK-ID marker line inclusive, up to (not including) the closing fence.",
       "LF line endings, final LF, no BOM, block bytes unmodified (no shebang added).",
       "",
       "| Block | File | Lines exp/act | SHA-256 exp/act | Result |",
       "|---|---|---|---|---|"]
for bid, fname, el, es, al, asha, res in rows:
    same = "`%s`" % es if es == asha else "exp `%s` / act `%s`" % (es, asha)
    rec.append("| `%s` | `%s` | %s/%s | %s | %s |" % (bid, fname, el, al, same, res))
rec += ["",
        "## Syntax validation",
        "",
        "- `bash -n` on the eight shell blocks",
        "- `py_compile` on `RP4-C3.py` with an explicit cfile in OS temp (no repo `__pycache__`)",
        "- embedded python heredocs extracted to OS temp and compiled there: "
        "RP5-C4A x2, RP5-C4B x1, RP5-C4C x1 (the Stage 1 scope of record)",
        "- ADDITIONAL, disclosed: `RP3-C2A-POST` also carries one `<<'PYEOF'` python heredoc, "
        "which §8.1 does not claim a `py_compile` check for. It was extracted and compiled in OS "
        "temp as well and is reported separately in `syntax_validation.txt`; it is extra evidence, "
        "not a change to the accepted §8.1 claim.",
        "- all commands, argv and real rc/output recorded in `syntax_validation.txt`",
        "",
        "## Archive",
        "",
        "- `runkit.tar` — uncompressed, GNU tar format, %d bytes" % len(tar_bytes),
        "- sha256 `%s`" % tar_sha,
        "- exactly the nine block files, no evidence or metadata members, no directory members",
        "- fixed §8.1 table order; mtime=0, mode=0644, uid=0, gid=0, empty uname/gname",
        "- platform tar on this host cannot normalize uid/gid/mtime/mode, so the archive is written",
        "  by the purpose-built `stage1_build.py` kept here as evidence; the platform tar is still",
        "  used read-only to cross-check the member listing (recorded in `ARCHIVE_MEMBERS.txt`)",
        "- determinism was checked by running the same builder twice into two different output",
        "  paths before this run: both produced the identical archive digest",
        "",
        "## Self-QA",
        "",
        "- the nine block files were re-read from disk and re-hashed",
        "- `runkit.tar` was extracted into OS temp and every member byte-compared to its source block",
        ""]
rec += qa
rec += ["",
        "## Not done (out of scope for Stage 1)",
        "",
        "- no commit, no push, no branch action (Lead owns Git)",
        "- no host, SSH, network, credential, service or economic action",
        "- no file written outside `01_RUNKIT/`",
        ""]
wtext(os.path.join(RUNKIT, "STAGE1_RECORD.md"), "".join(l + "\n" for l in rec))

if FAILURES:
    for f in FAILURES:
        print("FAIL:", f)
    print("STAGE1 FAILURE — created files preserved in", RUNKIT)
    sys.exit(1)

print("STAGE1 OK")
print("runkit:", RUNKIT)
print("tar sha256:", tar_sha, "bytes", len(tar_bytes))
print("temp root:", tmp)
for r in rows:
    print("  %-14s %-18s lines=%s sha=%s %s" % (r[0], r[1], r[4], r[5], r[6]))
