#!/usr/bin/env python3
"""WP-L Phase 2 staging - Stage 1B run-kit re-freeze builder.

Derivative of 01_RUNKIT/stage1_build.py. It assembles a TEN-block run-kit with
two provenance classes and never silently mixes them:

  Class A (accepted_blob)  - eight blocks extracted from the accepted proposals
                             blob exactly as Stage 1 did, verified bit-exactly
                             against 01_RUNKIT/BLOCK_IDENTITIES.tsv.
  Class B (repair_round6)  - RP1-B3.sh (REPLACES the old block) and RPD-VERIFY.sh
                             (NEW), copied byte-identical from
                             06_B3_REPAIR/round6/ and verified against the
                             required SHA-256 fixed by the kickoff.

Build only. No host contact, no ssh/scp, no network, no transport, no execution
of any block, no git mutation (only read-only `git rev-parse` / `git cat-file`).
Writable scope: the output directory only (canonically 07_RUNKIT_B/), plus an OS
temp root for compiled artifacts, tar unpack and the determinism rebuilds so that
no __pycache__ and no scratch file ever lands in the repo.

Usage:
  stage1b_build.py            canonical build into 07_RUNKIT_B/ (spawns two
                              independent child rebuilds to demonstrate
                              determinism)
  stage1b_build.py --out DIR  secondary build into a fresh DIR (used by the
                              determinism check; spawns no children)
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
STAGING_REL = os.path.join(
    "MTC_COMMAND_CENTER", "11_TRIAGE",
    "WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08",
)
STAGING = os.path.join(REPO, STAGING_REL)

# ---- Class A source (identical to Stage 1) --------------------------------
SRC_PATH = "MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md"
COMMIT = "4c0d5fc5aeb1e069cd6171c11d143ac2a49a6e2c"
BLOB = "76e0a66cd621ec5d38cc580904968262ce69678f"

# ---- Class B source (audit-6-PASSed repair round 6) -----------------------
REPAIR_DIR = os.path.join(STAGING, "06_B3_REPAIR", "round6")
REPAIR_REL = "06_B3_REPAIR/round6"

OUT_CANONICAL = os.path.join(STAGING, "07_RUNKIT_B")

# The old RP1-B3 digest. Used here ONLY as a verification constant: it proves the
# block sitting at RP1-B3's position in the accepted blob is the one being
# superseded, and it drives the hard check that this digest carries NO payload in
# the new kit. It is never written into a block file and never enters the archive.
OLD_RP1_B3_SHA = "f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af"

# ---------------------------------------------------------------------------
# The new kit. Archive order == this table order:
#   the accepted Stage 1 (S8.1) order is preserved for the nine operator-channel
#   blocks with RP1-B3 REPLACED IN PLACE, and the new root/deploy-channel block
#   RPD-VERIFY is APPENDED as the tenth member, because S8.1 has no slot for it
#   and this builder does not reinterpret the accepted ordering.
# (block id, filename, expected lines, expected sha256, provenance, supersedes)
# ---------------------------------------------------------------------------
ACCEPTED = "accepted_blob"
REPAIR = "repair_round6"

TABLE_B = [
    ("RP0-LIB",       "RP0-LIB.sh",       370, "4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48", ACCEPTED, "-"),
    ("RP0-BOOTSTRAP", "RP0-BOOTSTRAP.sh",  36, "e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33", ACCEPTED, "-"),
    ("RP1-B3",        "RP1-B3.sh",        662, "6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc", REPAIR,   OLD_RP1_B3_SHA),
    ("RP3-C2A-POST",  "RP3-C2A-POST.sh",  104, "e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27", ACCEPTED, "-"),
    ("RP3-C2B-POST",  "RP3-C2B-POST.sh",   74, "26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412", ACCEPTED, "-"),
    ("RP4-C3",        "RP4-C3.py",        295, "0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5", ACCEPTED, "-"),
    ("RP5-C4A",       "RP5-C4A.sh",       374, "a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2", ACCEPTED, "-"),
    ("RP5-C4B",       "RP5-C4B.sh",       249, "10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e", ACCEPTED, "-"),
    ("RP5-C4C",       "RP5-C4C.sh",       228, "de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8", ACCEPTED, "-"),
    ("RPD-VERIFY",    "RPD-VERIFY.sh",    775, "3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c", REPAIR,   "-"),
]

CLASS_A_IDS = [t[0] for t in TABLE_B if t[4] == ACCEPTED]
CLASS_B_IDS = [t[0] for t in TABLE_B if t[4] == REPAIR]

# Class A blocks still present in the accepted blob but NOT shipped by this kit.
BLOB_BLOCK_IDS = ["RP0-LIB", "RP0-BOOTSTRAP", "RP1-B3", "RP3-C2A-POST",
                  "RP3-C2B-POST", "RP4-C3", "RP5-C4A", "RP5-C4B", "RP5-C4C"]

# Expected embedded python heredoc count per shell block. Asserted, never
# inferred. Class A counts are the Stage 1 counts of record. The Class B counts
# (zero) were established by direct inspection of the audit-6-PASSed round6
# files while authoring this builder and are asserted here the same way.
HEREDOCS_SCOPE = {"RP5-C4A": 2, "RP5-C4B": 1, "RP5-C4C": 1}
HEREDOCS_EXTRA = {"RP3-C2A-POST": 1}
HEREDOCS_CLASSB = {"RP1-B3": 0, "RPD-VERIFY": 0}
HEREDOCS = dict(HEREDOCS_SCOPE, **HEREDOCS_EXTRA)

MARKER = re.compile(rb"^# ===== BLOCK-ID: ([A-Za-z0-9._-]+) ===== \[EXECUTABLE PROPOSAL BLOCK\]$")
FENCE = b"```"
HD_OPEN = re.compile(rb"<<'PYEOF'")

# Files this builder writes into the output directory.
LEAF_OUTPUTS = [t[1] for t in TABLE_B] + [
    "BLOCK_IDENTITIES_B.tsv",
    "SOURCE_IDENTITY_B.txt",
    "runkit_b.tar",
    "runkit_b.tar.sha256",
    "ARCHIVE_MEMBERS_B.txt",
    "syntax_validation_b.txt",
    "STAGE1B_RECORD.md",
]
# Authored evidence text that must be pure ASCII. Block payloads are excluded:
# their bytes are inherited verbatim and are never rewritten by this builder.
MUST_BE_ASCII = ["BLOCK_IDENTITIES_B.tsv", "SOURCE_IDENTITY_B.txt",
                 "ARCHIVE_MEMBERS_B.txt", "runkit_b.tar.sha256",
                 "syntax_validation_b.txt", "stage1b_build.py"]
# The old digest must not be carried by any shipped payload.
OLD_SHA_FORBIDDEN = [t[1] for t in TABLE_B] + ["runkit_b.tar"]

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LC_ALL="C")
LOG = []           # syntax_validation_b.txt entries
FAILURES = []      # hard identity/structure failures


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


def wtext(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def wbin(path, data):
    with open(path, "wb") as fh:
        fh.write(data)


def rbin(path):
    with open(path, "rb") as fh:
        return fh.read()


def nonascii(data):
    return sum(1 for c in data if c > 127)


def run(argv, label, cwd=None):
    """Run argv, record exact command and real rc/output. Returns rc."""
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       env=ENV, cwd=cwd)
    out = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    LOG.append((label if cwd is None else "%s   (cwd=%s)" % (label, cwd),
                argv, p.returncode, out))
    return p.returncode


def pick_bash():
    """Resolve the shell used for `bash -n`, deterministically and ASCII-pathed.

    `shutil.which("bash")` can land on the WindowsApps WSL stub, which mangles
    Windows paths (and whose own path is non-ASCII on this host). Prefer the
    Git-for-Windows / MSYS bash that ships next to the platform `tar` Stage 1
    cross-checked with, then the standard Git install locations, and only then
    whatever is on PATH. Every candidate is probed before use.
    """
    cands = []
    t = shutil.which("tar")
    if t:
        cands.append(os.path.join(os.path.dirname(t), "bash.exe"))
    cands += [r"C:\Program Files\Git\usr\bin\bash.exe",
              r"C:\Program Files\Git\bin\bash.exe"]
    w = shutil.which("bash")
    if w:
        cands.append(w)
    tried = []
    for c in cands:
        if not os.path.isfile(c):
            tried.append("%s -> not present" % c)
            continue
        if nonascii(c.encode("utf-8")):
            tried.append("%s -> rejected, non-ASCII interpreter path" % c)
            continue
        probe = subprocess.run([c, "-c", "printf ok"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, env=ENV, cwd=OUT)
        if probe.returncode == 0 and probe.stdout.strip() == b"ok":
            LOG.append(("bash interpreter selection",
                        ["<in-process>", "probe candidates in fixed order, first working ASCII-pathed shell wins"],
                        0, "\n".join(tried + ["%s -> SELECTED" % c]) + "\n"))
            return c
        tried.append("%s -> probe rc=%d" % (c, probe.returncode))
    LOG.append(("bash interpreter selection",
                ["<in-process>", "probe candidates in fixed order"],
                1, "\n".join(tried + ["no usable bash found"]) + "\n"))
    return None


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args],
                          stdout=subprocess.PIPE, check=True).stdout


def checkpoint(stage):
    if FAILURES:
        for f in FAILURES:
            print("FAIL:", f)
        print("STAGE1B FAILURE at %s - created files preserved in %s" % (stage, OUT))
        sys.exit(1)


# --------------------------------------------------------------------------
# 0. Mode / output directory
# --------------------------------------------------------------------------
argv = sys.argv[1:]
if not argv:
    OUT, MODE = OUT_CANONICAL, "canonical"
elif len(argv) == 2 and argv[0] == "--out":
    OUT, MODE = os.path.abspath(argv[1]), "secondary"
else:
    print("usage: stage1b_build.py [--out DIR]")
    sys.exit(2)

SELF = os.path.abspath(__file__)

# --------------------------------------------------------------------------
# 1. Class A source identity (read-only git)
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
# 2. Extract blocks from the blob: marker line inclusive -> up to (not
#    including) the closing fence. Identical rule to Stage 1.
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

if len(found) != len(BLOB_BLOCK_IDS):
    FAILURES.append("expected %d BLOCK-ID markers in the blob, found %d"
                    % (len(BLOB_BLOCK_IDS), len(found)))
if [f[0] for f in found] != BLOB_BLOCK_IDS:
    FAILURES.append("blob block id order/set mismatch: %s" % [f[0] for f in found])

by_id = {f[0]: f for f in found}

# The superseded block must be present in the blob and must be the OLD one.
# It is verified here and then deliberately NOT shipped.
if "RP1-B3" in by_id:
    old_sha_actual = sha256_hex(by_id["RP1-B3"][3])
    if old_sha_actual != OLD_RP1_B3_SHA:
        FAILURES.append("superseded RP1-B3 in blob is not the expected old block: %s != %s"
                        % (old_sha_actual, OLD_RP1_B3_SHA))
else:
    old_sha_actual = "-"
    FAILURES.append("superseded RP1-B3 block not found in the blob")

# --------------------------------------------------------------------------
# 3. Read Class B artifacts byte-identical from 06_B3_REPAIR/round6/
# --------------------------------------------------------------------------
classb = {}
for bid, fname, exp_lines, exp_sha, prov, _sup in TABLE_B:
    if prov != REPAIR:
        continue
    src = os.path.join(REPAIR_DIR, fname)
    if not os.path.isfile(src):
        FAILURES.append("Class B source missing: %s" % src)
        continue
    data = rbin(src)
    act_sha = sha256_hex(data)
    if act_sha != exp_sha:
        FAILURES.append("Class B hash mismatch %s: %s != %s" % (bid, act_sha, exp_sha))
    classb[bid] = {"path": "%s/%s" % (REPAIR_REL, fname), "abspath": src,
                   "bytes": len(data), "sha256": act_sha, "data": data}

# --------------------------------------------------------------------------
# 4. Assemble the ten payloads and check provenance-independent invariants
# --------------------------------------------------------------------------
payload = {}
for bid, fname, exp_lines, exp_sha, prov, _sup in TABLE_B:
    if prov == ACCEPTED:
        if bid not in by_id:
            FAILURES.append("Class A block %s not found in the blob" % bid)
            continue
        payload[bid] = by_id[bid][3]
    else:
        if bid not in classb:
            continue
        payload[bid] = classb[bid]["data"]

if len(payload) != 10:
    FAILURES.append("expected 10 blocks, assembled %d" % len(payload))

old_sha_bytes = OLD_RP1_B3_SHA.encode("ascii")
for bid, data in payload.items():
    if sha256_hex(data) == OLD_RP1_B3_SHA:
        FAILURES.append("superseded payload present in the new kit as %s" % bid)
    if old_sha_bytes in data:
        FAILURES.append("superseded digest string present in payload %s" % bid)

# --------------------------------------------------------------------------
# 5. Output directory: refuse to clobber an existing output leaf
# --------------------------------------------------------------------------
if not os.path.isdir(OUT):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    os.mkdir(OUT)  # no exist_ok: clobbering an existing kit is a hard failure
    out_state = "created"
else:
    # The canonical output leaf already exists (it holds the kickoff and this
    # builder). Clobber refusal therefore applies per leaf artifact.
    clash = [n for n in LEAF_OUTPUTS if os.path.exists(os.path.join(OUT, n))]
    if clash:
        print("FAIL: refusing to clobber existing output leaf artifacts in %s: %s"
              % (OUT, ", ".join(clash)))
        print("STAGE1B FAILURE at clobber-guard - nothing written")
        sys.exit(1)
    out_state = "pre-existing (no leaf artifact present; nothing clobbered)"

# --------------------------------------------------------------------------
# 6. Write the ten block files and verify every identity
# --------------------------------------------------------------------------
rows = []
for bid, fname, exp_lines, exp_sha, prov, sup in TABLE_B:
    if bid not in payload:
        rows.append((bid, fname, exp_lines, exp_sha, "-", "-", "MISSING", prov, sup))
        continue
    data = payload[bid]
    wbin(os.path.join(OUT, fname), data)
    act_lines = data.count(b"\n")
    act_sha = sha256_hex(data)
    ok = (act_lines == exp_lines) and (act_sha == exp_sha)
    rows.append((bid, fname, exp_lines, exp_sha, act_lines, act_sha,
                 "MATCH" if ok else "MISMATCH", prov, sup))
    if not ok:
        FAILURES.append("identity mismatch %s [%s]: lines %s/%s sha %s/%s"
                        % (bid, prov, act_lines, exp_lines, act_sha, exp_sha))
    if data[:3] == b"\xef\xbb\xbf":
        FAILURES.append("BOM in %s" % bid)
    if b"\r" in data:
        FAILURES.append("CR byte in %s" % bid)
    if not data.endswith(b"\n"):
        FAILURES.append("no final LF in %s" % bid)
    if not MARKER.match(data.split(b"\n")[0]):
        FAILURES.append("first line of %s is not a BLOCK-ID marker" % bid)
    if FENCE + b"\n" in data or data.startswith(FENCE):
        FAILURES.append("fence line inside block payload %s" % bid)

wtext(os.path.join(OUT, "BLOCK_IDENTITIES_B.tsv"),
      "block_id\tfile\texpected_lines\texpected_sha256\tactual_lines\tactual_sha256"
      "\tresult\tprovenance\tsupersedes_sha256\n"
      + "".join("\t".join(str(c) for c in r) + "\n" for r in rows))

src_lines = [
    "WP-L Phase 2 Stage 1B - re-frozen run-kit source identity",
    "",
    "This kit has TWO provenance classes. Class A is unchanged accepted content.",
    "Class B is repair-cycle content. They are never mixed silently: every block",
    "carries its class in BLOCK_IDENTITIES_B.tsv.",
    "",
    "== CLASS A - accepted_blob (8 blocks) ==",
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
    "class_a_blocks         %s" % " ".join(CLASS_A_IDS),
    "",
    "extraction rule: from the `# ===== BLOCK-ID: <id> =====` marker line inclusive,",
    "up to (not including) the closing ``` fence; LF line endings; final LF; no BOM.",
    "This is the Stage 1 rule, unchanged, and the eight Class A digests match the",
    "Stage 1 table in 01_RUNKIT/BLOCK_IDENTITIES.tsv bit-exactly.",
    "block source spans (1-indexed lines of the blob):",
] + ["  %-14s marker %5d  fence %5d  lines %3d%s"
     % (f[0], f[1], f[2] + 1, f[2] + 1 - f[1],
        "   NOT SHIPPED - superseded by Class B" if f[0] == "RP1-B3" else "")
     for f in found] + [
    "",
    "superseded_block       RP1-B3",
    "superseded_sha256      %s" % old_sha_actual,
    "superseded_disposition extracted from the blob for verification only; it is not",
    "                       written to any file in this kit and is not an archive",
    "                       member. The digest above appears in this kit only in the",
    "                       evidence records and as a verification constant in",
    "                       stage1b_build.py.",
    "",
    "== CLASS B - repair_round6 (2 blocks) ==",
    "",
    "source_dir             %s" % REPAIR_REL,
    "acceptance             B3-GAP-ENV repair cycle, audit 6 PASS",
    "class_b_blocks         %s" % " ".join(CLASS_B_IDS),
    "",
]
for bid in CLASS_B_IDS:
    if bid not in classb:
        src_lines += ["  %-12s MISSING" % bid, ""]
        continue
    c = classb[bid]
    role = ("REPLACES the Stage 1 block of the same id"
            if bid == "RP1-B3" else "NEW block, not present in the Stage 1 kit")
    src_lines += [
        "  block_id             %s" % bid,
        "  path                 %s" % c["path"],
        "  bytes                %d" % c["bytes"],
        "  sha256               %s" % c["sha256"],
        "  role                 %s" % role,
        "  statement            This file is byte-identical to the audit-6-PASSed",
        "                       round6 file at %s; it was copied verbatim, byte for" % c["path"],
        "                       byte, with no rewriting of any kind.",
        "",
    ]
src_lines += [
    "copy rule: Class B blocks are read and written as raw bytes. No shebang is",
    "added, no line ending is translated, no whitespace is normalized.",
]
wtext(os.path.join(OUT, "SOURCE_IDENTITY_B.txt"), "".join(l + "\n" for l in src_lines))

checkpoint("identity verification")

# --------------------------------------------------------------------------
# 7. Syntax validation
# --------------------------------------------------------------------------
tmp = tempfile.mkdtemp(prefix="wplp2_s1b_")

bash = pick_bash()
py = sys.executable
if bash is None:
    FAILURES.append("no usable bash interpreter found for `bash -n`")
    checkpoint("bash interpreter selection")

run([bash, "--version"], "bash --version (interpreter identity)")
run([py, "-V"], "python -V (interpreter identity)")

# Run from cwd=OUT with a relative name: a drive-lettered Windows path is not
# portable across the shells that can answer to the name `bash` on this host.
for bid, fname, _, _, _, _ in TABLE_B:
    if fname.endswith(".sh"):
        run([bash, "-n", fname], "bash -n %s" % fname, cwd=OUT)

# RP4 python source: explicit cfile under the OS temp root so no __pycache__ is
# ever created inside the repo.
run([py, "-c",
     "import py_compile,sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)",
     os.path.join(OUT, "RP4-C3.py"), os.path.join(tmp, "RP4-C3.pyc")],
    "py_compile RP4-C3.py (cfile in OS temp)")

# Embedded python heredocs -> OS temp only, then compiled there.
hd_report = []
for bid, fname, _, _, prov, _sup in TABLE_B:
    if not fname.endswith(".sh"):
        continue
    body = payload[bid].split(b"\n")
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
    exp = HEREDOCS.get(bid, HEREDOCS_CLASSB.get(bid, 0))
    hd_report.append("%-14s [%-13s] expected=%d actual=%d %s"
                     % (bid, prov, exp, len(docs), "OK" if len(docs) == exp else "FAIL"))
    if len(docs) != exp:
        FAILURES.append("%s: expected %d python heredoc(s), found %d" % (bid, exp, len(docs)))
        continue
    if bid in HEREDOCS_SCOPE:
        tag = "SCOPE"
    elif bid in HEREDOCS_EXTRA:
        tag = "ADDITIONAL (outside the specified Stage 1 heredoc scope)"
    else:
        tag = "CLASS B (asserted zero)"
    for n, doc in enumerate(docs, 1):
        hp = os.path.join(tmp, "%s_heredoc%d.py" % (bid, n))
        wbin(hp, doc)
        run([py, "-c",
             "import py_compile,sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)",
             hp, hp + "c"],
            "py_compile %s embedded heredoc %d/%d [%s] (%d bytes, sha256 %s) - OS temp only"
            % (bid, n, exp, tag, len(doc), sha256_hex(doc)))

LOG.append(("embedded heredoc count assertion (all 9 shell blocks)",
            ["<in-process>", "count <<'PYEOF' openers per shell block; assert against the fixed table"],
            1 if any(r.endswith("FAIL") for r in hd_report) else 0,
            "\n".join(hd_report) + "\n"))

checkpoint("syntax validation")

# --------------------------------------------------------------------------
# 8. Deterministic uncompressed tar (Stage 1 normalization, ten members)
# --------------------------------------------------------------------------
TAR = os.path.join(OUT, "runkit_b.tar")
with tarfile.open(TAR, "w", format=tarfile.GNU_FORMAT) as tf:
    for bid, fname, _, _, _, _ in TABLE_B:
        data = payload[bid]
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

tar_bytes = rbin(TAR)
tar_sha = sha256_hex(tar_bytes)
wtext(os.path.join(OUT, "runkit_b.tar.sha256"), "%s  runkit_b.tar\n" % tar_sha)

if old_sha_bytes in tar_bytes:
    FAILURES.append("superseded digest string present in runkit_b.tar")

with tarfile.open(TAR, "r") as tf:
    members = tf.getmembers()
mem_lines = ["%-16s %-6s %6d %-5s uid=%d gid=%d uname=%r gname=%r mtime=%d"
             % (m.name, oct(m.mode), m.size, "REG" if m.isfile() else m.type,
                m.uid, m.gid, m.uname, m.gname, m.mtime) for m in members]
if len(members) != 10:
    FAILURES.append("archive member count %d != 10" % len(members))
if [m.name for m in members] != [t[1] for t in TABLE_B]:
    FAILURES.append("archive member order mismatch: %s" % [m.name for m in members])

# Independent cross-check with the platform tar (listing only, no extraction).
systar = shutil.which("tar")
# Relative name from cwd=OUT: a drive-lettered path makes GNU tar read `C:` as a
# remote host spec and fail with "Cannot connect to C: resolve failed".
xchk = subprocess.run([systar, "-tvf", "runkit_b.tar"], cwd=OUT,
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV)
xout = xchk.stdout.decode("utf-8", "replace").replace("\r\n", "\n").rstrip("\n")
if xchk.returncode != 0:
    FAILURES.append("platform tar cross-check rc=%d: %s" % (xchk.returncode, xout))

# --------------------------------------------------------------------------
# 9. Self-QA - reread from disk, and diff tar members extracted to OS temp
# --------------------------------------------------------------------------
qa = []
for bid, fname, exp_lines, exp_sha, prov, _sup in TABLE_B:
    disk = rbin(os.path.join(OUT, fname))
    d_sha, d_lines = sha256_hex(disk), disk.count(b"\n")
    ok = (d_sha == exp_sha and d_lines == exp_lines
          and b"\r" not in disk and disk[:3] != b"\xef\xbb\xbf" and disk.endswith(b"\n"))
    qa.append("disk   %-14s [%-13s] lines=%3d sha256=%s %s"
              % (bid, prov, d_lines, d_sha, "OK" if ok else "FAIL"))
    if not ok:
        FAILURES.append("self-QA disk mismatch %s" % bid)

xdir = os.path.join(tmp, "unpack")
os.makedirs(xdir)
with tarfile.open(TAR, "r") as tf:
    tf.extractall(xdir, filter="data")
names = sorted(os.listdir(xdir))
if names != sorted(t[1] for t in TABLE_B):
    FAILURES.append("tar unpack contains unexpected entries: %s" % names)
for bid, fname, exp_lines, exp_sha, prov, _sup in TABLE_B:
    p = os.path.join(xdir, fname)
    if not os.path.isfile(p):
        FAILURES.append("tar member missing after unpack: %s" % fname)
        continue
    got = rbin(p)
    ok = got == payload[bid] and sha256_hex(got) == exp_sha
    qa.append("untar  %-14s [%-13s] bytes=%6d sha256=%s %s"
              % (bid, prov, len(got), sha256_hex(got), "IDENTICAL" if ok else "FAIL"))
    if not ok:
        FAILURES.append("tar member differs from source block: %s" % fname)

LOG.append(("self-QA",
            ["<in-process>",
             "reread 10 block files from disk; extract runkit_b.tar to OS temp; byte-compare"],
            1 if FAILURES else 0, "\n".join(qa) + "\n"))

# --------------------------------------------------------------------------
# 10. Determinism - two independent child rebuilds into different paths
# --------------------------------------------------------------------------
rebuilds = []
if MODE == "canonical":
    for tag in ("a", "b"):
        rdir = os.path.join(tmp, "rebuild_" + tag)
        rc = run([py, SELF, "--out", rdir], "determinism rebuild %s (independent child process)" % tag)
        rsha = "-"
        rtar = os.path.join(rdir, "runkit_b.tar")
        if rc == 0 and os.path.isfile(rtar):
            rsha = sha256_hex(rbin(rtar))
        else:
            FAILURES.append("determinism rebuild %s failed rc=%d" % (tag, rc))
        rebuilds.append((tag, rdir, rsha))
        if rsha != tar_sha:
            FAILURES.append("determinism rebuild %s digest %s != canonical %s"
                            % (tag, rsha, tar_sha))
    det_lines = [
        "determinism: this archive was rebuilt twice by independent child processes of",
        "this builder, each writing into a different, previously non-existent output",
        "path. All three digests are identical, so an independent rebuild reproduces",
        "the archive byte-for-byte.",
        "  canonical   %s  %s" % (tar_sha, OUT),
    ] + ["  rebuild_%s   %s  %s" % (t, s, d) for t, d, s in rebuilds] + [
        "  result      %s" % ("MATCH (byte-for-byte reproducible)"
                              if all(s == tar_sha for _, _, s in rebuilds) else "MISMATCH"),
    ]
else:
    det_lines = [
        "determinism: secondary build (--out). Secondary builds spawn no child",
        "rebuilds; the canonical build compares this archive digest against its own.",
    ]

# --------------------------------------------------------------------------
# 11. ARCHIVE_MEMBERS_B.txt
# --------------------------------------------------------------------------
wtext(os.path.join(OUT, "ARCHIVE_MEMBERS_B.txt"), "".join(l + "\n" for l in [
    "runkit_b.tar - uncompressed, GNU tar format, deterministic",
    "archive_bytes %d" % len(tar_bytes),
    "archive_sha256 %s" % tar_sha,
    "member_count %d" % len(members),
    "order: Stage 1 S8.1 table order for the nine operator-channel blocks with RP1-B3",
    "  replaced in place, then the new root/deploy-channel block RPD-VERIFY appended",
    "  as the tenth member (fixed, not directory-scan order)",
    "normalization: mtime=0 mode=0644 uid=0 gid=0 uname='' gname='' type=REG, no dir members",
    "trailing bytes are the tar end-of-archive marker plus 10240-byte record padding",
    "provenance: 8 members accepted_blob, 2 members repair_round6 (RP1-B3, RPD-VERIFY)",
    "superseded: the old RP1-B3 payload (sha256 %s)" % OLD_RP1_B3_SHA,
    "  is NOT an archive member and its digest string appears nowhere in the archive",
    "",
] + det_lines + [
    "",
    "-- member listing (python tarfile) --",
] + mem_lines + [
    "",
    "-- cross-check: %s -tvf runkit_b.tar  (rc=%d) --" % (systar, xchk.returncode),
] + xout.split("\n")))

# --------------------------------------------------------------------------
# 12. syntax_validation_b.txt
# --------------------------------------------------------------------------
parts = ["WP-L Phase 2 Stage 1B - syntax validation (real commands, real rc, real output)",
         "mode: %s" % MODE,
         "output directory: %s (%s)" % (OUT, out_state),
         "OS temp root used for compiled artifacts, tar unpack and determinism rebuilds: %s" % tmp,
         "No __pycache__ is created inside the repo: every py_compile call passes an",
         "explicit cfile under the OS temp root.",
         "Checked: 9 shell blocks with bash -n, RP4-C3.py with py_compile, every embedded",
         "python heredoc compiled in OS temp, heredoc counts asserted per block, platform",
         "tar listing cross-check, self-QA%s."
         % (", and two independent determinism rebuilds" if MODE == "canonical" else ""),
         ""]
for label, cmd, rc, out in LOG:
    parts.append("--- %s" % label)
    parts.append("$ %s" % " ".join(('"%s"' % a if " " in a else a) for a in cmd))
    parts.append("rc=%d" % rc)
    parts.append("output: %s" % ("<empty>" if out.strip() == "" else ""))
    if out.strip():
        parts.extend(out.rstrip("\n").split("\n"))
    parts.append("")
parts.append("--- platform tar cross-check")
parts.append("$ %s -tvf runkit_b.tar   (cwd=%s)" % (systar, OUT))
parts.append("rc=%d" % xchk.returncode)
parts.append("output:")
parts.extend(xout.split("\n"))
parts.append("")
wtext(os.path.join(OUT, "syntax_validation_b.txt"), "".join(p + "\n" for p in parts))

nonzero = [l for (l, a, rc, o) in LOG if rc != 0]
if nonzero:
    FAILURES.append("non-zero rc from: %s" % nonzero)

# --------------------------------------------------------------------------
# 13. ASCII audit and superseded-digest occurrence audit over the kit
# --------------------------------------------------------------------------
audit = []
for name in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, name)
    if not os.path.isfile(p):
        continue
    d = rbin(p)
    na = nonascii(d)
    has_old = old_sha_bytes in d
    if name in MUST_BE_ASCII and na:
        FAILURES.append("authored evidence file %s carries %d non-ASCII byte(s)" % (name, na))
    if has_old and name in OLD_SHA_FORBIDDEN:
        FAILURES.append("superseded digest string present in shipped payload %s" % name)
    kind = ("shipped block payload (bytes inherited verbatim)"
            if name in [t[1] for t in TABLE_B] else
            "archive" if name == "runkit_b.tar" else
            "builder" if name == "stage1b_build.py" else
            "kickoff" if name.startswith("KICKOFF") else "evidence record")
    audit.append("%-28s %8d bytes  non_ascii=%-3d old_sha_string=%-5s  %s"
                 % (name, len(d), na, "yes" if has_old else "no", kind))

# --------------------------------------------------------------------------
# 14. STAGE1B_RECORD.md
# --------------------------------------------------------------------------
status = "FAILURE" if FAILURES else "PASS"
builder_sha = sha256_hex(rbin(SELF))
rec = [
    "# WP-L Phase 2 - Stage 1B record (run-kit re-freeze)",
    "",
    "Result: **%s**" % status,
    "",
    "Build only. No host contact, no ssh/scp, no transport, no execution of any block,",
    "no git mutation. Nothing was written outside `07_RUNKIT_B/` except compiled",
    "artifacts, the tar unpack and the two determinism rebuilds, which live under an OS",
    "temp root (`%s`) and never touch the repo." % tmp,
    "",
    "## What was built",
    "",
    "A ten-block run-kit with two provenance classes, plus its identity table, source",
    "identity record, deterministic archive, archive member listing, syntax validation",
    "log and this record. Archive: `runkit_b.tar`, %d bytes, sha256" % len(tar_bytes),
    "`%s`." % tar_sha,
    "",
    "## Provenance classes",
    "",
    "### Class A - `accepted_blob` (8 blocks, unchanged)",
    "",
    "Extracted from the accepted proposals blob `%s`" % BLOB,
    "(commit `%s`, `%s`)" % (COMMIT, SRC_PATH),
    "with the Stage 1 extraction rule, and verified bit-exactly against the Stage 1",
    "table `01_RUNKIT/BLOCK_IDENTITIES.tsv`: "
    + ", ".join("`%s`" % b for b in CLASS_A_IDS) + ".",
    "",
    "### Class B - `repair_round6` (2 blocks, repair-cycle artifacts)",
    "",
    "Copied byte-identical from `%s/`, which is the audit-6-PASSed" % REPAIR_REL,
    "content of the B3-GAP-ENV repair cycle:",
    "",
]
for bid in CLASS_B_IDS:
    c = classb.get(bid)
    if not c:
        rec.append("- `%s` - MISSING" % bid)
        continue
    role = "REPLACES the Stage 1 block of the same id" if bid == "RP1-B3" else "NEW block"
    rec.append("- `%s` (`%s`) - %s; %d bytes; sha256 `%s`; byte-identical to `%s`."
               % (bid, c["path"].rsplit("/", 1)[1], role, c["bytes"], c["sha256"], c["path"]))
rec += [
    "",
    "The two classes are never mixed silently: `BLOCK_IDENTITIES_B.tsv` carries a",
    "`provenance` column on every row, and `SOURCE_IDENTITY_B.txt` documents each class",
    "in its own section.",
    "",
    "## Blocks",
    "",
    "| Block | File | Provenance | Lines exp/act | SHA-256 exp/act | Supersedes | Result |",
    "|---|---|---|---|---|---|---|",
]
for bid, fname, el, es, al, asha, res, prov, sup in rows:
    same = "`%s`" % es if es == asha else "exp `%s` / act `%s`" % (es, asha)
    rec.append("| `%s` | `%s` | `%s` | %s/%s | %s | %s | %s |"
               % (bid, fname, prov, el, al, same,
                  ("`%s`" % sup) if sup != "-" else "-", res))
rec += [
    "",
    "## What changed against the Stage 1 kit",
    "",
    "- **Block added (1):** `RPD-VERIFY` (`RPD-VERIFY.sh`) - new, was not in the Stage 1",
    "  kit at all. Root/deploy-channel admission verify block, frozen and NOT executed.",
    "- **Block replaced (1):** `RP1-B3` (`RP1-B3.sh`) - the Stage 1 block",
    "  (sha256 `%s`," % OLD_RP1_B3_SHA,
    "  117 lines) is superseded by the repaired round6 block",
    "  (sha256 `%s`, 662 lines)."
    % dict((t[0], t[3]) for t in TABLE_B)["RP1-B3"],
    "- **Blocks unchanged (8):** " + ", ".join("`%s`" % b for b in CLASS_A_IDS)
    + " - identical bytes and identical digests to the Stage 1 kit.",
    "- **Archive digest changed:** Stage 1 `runkit.tar` sha256",
    "  `618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53` (9 members)",
    "  -> Stage 1B `runkit_b.tar` sha256 `%s` (%d members)." % (tar_sha, len(members)),
    "",
    "### Disposition of the superseded block",
    "",
    "The old `RP1-B3` payload is extracted from the accepted blob during the build only",
    "to prove that the block being superseded is the expected one. It is not written to",
    "any file in this kit and is not an archive member. The builder hard-fails if that",
    "digest matches any shipped payload or if the digest string appears inside any block",
    "file or inside the archive. Occurrence audit over the whole kit:",
    "",
    "```",
] + audit + [
    "```",
    "",
    "Every `old_sha_string=yes` row above is an evidence record, the builder's",
    "verification constant, or the kickoff - never a shipped payload or the archive.",
    "This record is not in the table because the table is computed before it is written;",
    "it does carry the old digest, above, as the superseded value. `non_ascii` is nonzero",
    "only for Class A payload bytes inherited verbatim from the accepted blob (and hence",
    "for the archive that carries them); every file this builder authors is pure ASCII.",
    "",
    "## Syntax validation",
    "",
    "- `bash -n` on all nine shell blocks, including both Class B blocks",
    "- `py_compile` on `RP4-C3.py` with an explicit cfile in OS temp (no repo `__pycache__`)",
    "- embedded python heredocs extracted to OS temp and compiled there: `RP5-C4A` x2,",
    "  `RP5-C4B` x1, `RP5-C4C` x1 (the Stage 1 scope of record)",
    "- ADDITIONAL, disclosed: `RP3-C2A-POST` also carries one `<<'PYEOF'` python heredoc,",
    "  which S8.1 does not claim a `py_compile` check for. It was extracted and compiled in",
    "  OS temp as well and is reported separately in `syntax_validation_b.txt`; it is extra",
    "  evidence, not a change to the accepted S8.1 claim.",
    "- the heredoc count of every shell block is asserted against a fixed table, never",
    "  inferred. The Class B expectation (zero embedded heredocs in `RP1-B3.sh` and",
    "  `RPD-VERIFY.sh`) was established by direct inspection of the audit-6-PASSed round6",
    "  files while authoring this builder and is asserted here the same way.",
    "- all commands, argv and real rc/output recorded in `syntax_validation_b.txt`",
    "",
    "## Archive",
    "",
    "- `runkit_b.tar` - uncompressed, GNU tar format, %d bytes" % len(tar_bytes),
    "- sha256 `%s`" % tar_sha,
    "- exactly the ten block files, no evidence or metadata members, no directory members",
    "- order: Stage 1 S8.1 order for the nine operator-channel blocks with `RP1-B3`",
    "  replaced in place, then `RPD-VERIFY` appended as the tenth member. S8.1 has no",
    "  slot for the new root/deploy-channel block, so the accepted ordering is preserved",
    "  rather than reinterpreted.",
    "- mtime=0, mode=0644, uid=0, gid=0, empty uname/gname, REGTYPE",
    "- platform tar on this host cannot normalize uid/gid/mtime/mode, so the archive is",
    "  written by this builder; the platform tar is still used read-only to cross-check",
    "  the member listing (recorded in `ARCHIVE_MEMBERS_B.txt`)",
    "",
    "### Determinism",
    "",
]
if MODE == "canonical":
    rec += ["- rebuilt twice by independent child processes into two different, previously",
            "  non-existent output paths; all three archive digests are identical:",
            ""] + \
           ["  - canonical `%s`" % tar_sha] + \
           ["  - rebuild_%s `%s` (`%s`)" % (t, s, d) for t, d, s in rebuilds] + [""]
else:
    rec += ["- secondary build; no child rebuilds spawned.", ""]
rec += [
    "## Self-QA",
    "",
    "- the ten block files were re-read from disk and re-hashed",
    "- `runkit_b.tar` was extracted into OS temp and every member byte-compared to its",
    "  source payload",
    "- the builder refuses to clobber an existing output leaf artifact and exits nonzero",
    "  with created files preserved on any identity, structure or syntax failure",
    "",
    "```",
] + qa + [
    "```",
    "",
    "## Transport status - NOT TRANSPORTED",
    "",
    "**This kit has NOT been transported.** No host was contacted, no ssh/scp ran, no",
    "block was executed anywhere. The kit exists only as files in `07_RUNKIT_B/`.",
    "",
    "**Transporting this kit requires a NEW preregistration.** The existing Stage 2/3",
    "preregistration is VOID for this kit: its S3 block hashes and its archive digest",
    "no longer describe what is here. `RP1-B3` has a different digest, `RPD-VERIFY` did",
    "not exist when that preregistration was written, and the archive digest changed from",
    "`618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53` to",
    "`%s`. Nothing in this kit may move to any host until a new" % tar_sha,
    "preregistration covering these ten block digests and this archive digest is",
    "approved.",
    "",
    "## Not done (out of scope for Stage 1B)",
    "",
    "- no commit, no push, no branch action, no git mutation of any kind (Lead owns Git)",
    "- no host, SSH, network, credential, service or economic action",
    "- no transport, no execution, no preregistration",
    "- nothing written outside `07_RUNKIT_B/` in the repo; `01_RUNKIT/` and",
    "  `06_B3_REPAIR/` were read only",
    "",
    "## Files in this kit",
    "",
    "- `stage1b_build.py` (sha256 `%s`) - this builder" % builder_sha,
    "- the ten block files listed above",
    "- `BLOCK_IDENTITIES_B.tsv`, `SOURCE_IDENTITY_B.txt`, `ARCHIVE_MEMBERS_B.txt`,",
    "  `syntax_validation_b.txt`, `runkit_b.tar`, `runkit_b.tar.sha256`, this record",
    "",
]
rec_text = "".join(l + "\n" for l in rec)
if nonascii(rec_text.encode("utf-8")):
    FAILURES.append("STAGE1B_RECORD.md text carries non-ASCII bytes")
wtext(os.path.join(OUT, "STAGE1B_RECORD.md"), rec_text)

# --------------------------------------------------------------------------
# 15. Result
# --------------------------------------------------------------------------
if FAILURES:
    for f in FAILURES:
        print("FAIL:", f)
    print("STAGE1B FAILURE - created files preserved in", OUT)
    sys.exit(1)

print("DONE")
print("mode:", MODE)
print("runkit:", OUT)
print("archive: runkit_b.tar  bytes %d  sha256 %s" % (len(tar_bytes), tar_sha))
print("ten block digests:")
for bid, fname, el, es, al, asha, res, prov, sup in rows:
    print("  %-14s %-18s %-13s lines=%-4s sha256=%s %s" % (bid, fname, prov, al, asha, res))
print("temp root:", tmp)
