# WP-L Phase 2 Stage 2 — candidate payload-manifest derivation (READ-ONLY).
"""Reconstruct, byte-for-byte, the `RELEASE_SHA256SUMS` file that the candidate's
own `IBKR_PAPER_BRIDGE/deploy/linux/package.sh` emits for the frozen candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b`, and print its sha256.

That sha256 is the value `install.sh` records as `release_manifest_sha256` in
`/etc/mtc-bridge/install_manifest.json` (install.sh:112-114, :410) and therefore
the value `RP1-B3` requires as the preregistered `B3_RELEASE_MANIFEST_SHA256`.

WHY THIS DERIVATION AND NOT `package.sh`
    `package.sh` refuses to run unless the repository HEAD *is* the release sha
    and the worktree is clean; it then exports the commit with `git archive`
    into a directory outside the worktree. Running it here would mean moving
    HEAD off the working branch. This script never does that. It reads the
    frozen commit's objects directly with `git show <sha>:<path>` and never
    reads, resolves or mutates HEAD, any ref, any branch, the index, or any
    working-tree file. That is strictly stronger than package.sh's own
    precondition: a dirty or unrelated worktree cannot influence the result.

WHAT MAKES THE RECONSTRUCTION EXACT

  1. package.sh exports with `git -c core.autocrlf=false -c core.eol=lf archive`,
     so every exported file carries the blob bytes as stored in git. `git show
     <sha>:<path> --` yields those same bytes, and this script PROVES it for
     every single file rather than assuming it: it recomputes git's own object
     id over the bytes it received -- sha1("blob <len>\0" + bytes) -- and
     requires it to equal the object id `git ls-tree` recorded for that path.
     A single altered, added, dropped or line-ending-converted byte changes
     that id. The declared blob length is checked as well.

     The trailing `--` is load-bearing on Windows: without it git treats the
     argument as a possible working-tree filename and stats it, which fails
     with ENAMETOOLONG on the deepest paths in this repository. With it the
     argument is unambiguously a revision, so the working tree is never
     consulted for any file.
  2. package.sh writes `<out>/RELEASE_SHA` containing `printf '%s\n' <sha>`
     BEFORE generating the manifest, so `./RELEASE_SHA` is a manifest member.
  3. The manifest is generated as
         find . -type f '!' -name RELEASE_SHA256SUMS -print0 | sort -z
            | xargs -0 sha256sum > RELEASE_SHA256SUMS
     under `LC_ALL=C`, from the payload root. Member names are therefore spelled
     `./<path>` and ordered by C-locale byte comparison.

     THE SEPARATOR IS BUILD-HOST DEPENDENT and both forms are real. GNU
     sha256sum writes `<64 hex><space><space><name>` in text mode (its default
     on Linux) and `<64 hex><space>*<name>` in binary mode (its default where
     text and binary differ, i.e. Windows/git-bash). The candidate's own
     consumers strip either -- `sed -E 's/^[0-9a-f]{64} [ *]//'` at
     install.sh:116 and common.sh:135. This script computes BOTH renderings of
     the same content and reports both digests; `--rendering` selects which one
     is written out. The default is `binary`, because that is the rendering
     whose digest matches the real frozen payload for this candidate (see the
     corroboration note below).

     CORROBORATION -- this is not a guess. The offline A-0 identity check run
     against the REAL frozen payload tar for this candidate on 2026-08-08
     (`11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08B.md`) recorded manifest SHA
     `edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26` over
     `7059 manifest entries`. The binary rendering computed here reproduces that
     digest and that entry count exactly, from objects only, without ever
     touching the tar. That agreement is what makes the pinned
     `B3_RELEASE_MANIFEST_SHA256` a derived value rather than a quoted one.
  4. `git archive` reproduces the commit tree exactly: no `export-ignore` and no
     `export-subst` attribute exists at the candidate (`.gitattributes` carries
     only `* text=auto` plus one `eol=lf` pin), and package.sh independently
     re-asserts that the exported inventory and sizes equal the commit tree.

FAIL-CLOSED PREDICATES (any one of these makes the derived value untrustworthy,
so it is refused instead of emitted)

  * the pinned sha does not resolve to a commit object, or resolves to a
    different object id;
  * any tree entry is not a regular-file blob (a symlink, gitlink or special
    entry would make package.sh die at `assert_regular_directory_tree`);
  * any path contains a newline or a backslash -- GNU sha256sum escapes such
    names and prefixes the line with a backslash, so the naive line form would
    no longer be byte-exact;
  * any path's basename is `RELEASE_SHA256SUMS` (it would be excluded by the
    `! -name` filter) or the tree already carries `RELEASE_SHA` (package.sh
    would overwrite it);
  * `git show` returns a byte count, or bytes whose recomputed git object id,
    differ from what `git ls-tree --long` recorded for that blob;
  * the repository's object format is not the sha1 form this object-id proof
    reconstructs;
  * a CR byte appears in a file package.sh requires to be LF-only (it would
    die before ever writing a manifest), or either LF-required inventory is
    empty.

NOTHING ELSE HAPPENS HERE. No network, no host, no ssh, no service, no
credential, no write outside the single `--out` file, no git write of any kind.

rc contract:  0 = derived,  1 = fidelity predicate refused,  3 = could not
evaluate. A non-zero rc never leaves a partial manifest behind at `--out`.
"""

import argparse
import hashlib
import os
import subprocess
import sys

CANDIDATE = "2ce41e34bceb599d80af24c5c33d835820ec321b"

PASS_RC, FAIL_RC, STOP_RC = 0, 1, 3

# package.sh: LF is required for every file under deploy/linux, and for every
# *.sh anywhere else in the payload.
LF_REQUIRED_DEPLOY_PREFIX = b"./IBKR_PAPER_BRIDGE/deploy/linux/"
LF_REQUIRED_SUFFIX = b".sh"

ALLOWED_MODES = (b"100644", b"100755")

# GNU sha256sum separators: text mode (Linux default) vs binary mode
# (Windows/git-bash default). Both are accepted by the candidate's own parsers.
SEPARATORS = {"text": b"  ", "binary": b" *"}

# The manifest digest recorded for the REAL frozen payload tar of this candidate
# by the offline A-0 identity check in GATE_A_LOCAL_RUN_KIT_2026-08-08B.md. It is
# not an input to anything -- it is reported alongside the derived digests so the
# agreement (or a future disagreement) is visible in the run's own output.
CORROBORATING_A0_MANIFEST_SHA256 = \
    "edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26"
CORROBORATING_A0_ENTRIES = 7059


class Fail(Exception):
    """A fidelity predicate refused the derivation."""


class Stop(Exception):
    """Could not evaluate. Never re-read as a derived value."""


def out(msg):
    print(msg, flush=True)


def git(repo, args, allow_binary=True):
    """Run one read-only git command and return raw stdout bytes."""
    cmd = ["git", "-C", repo] + args
    try:
        proc = subprocess.run(cmd, capture_output=True)
    except OSError as exc:
        raise Stop("git_spawn_failed args=%s %s: %s"
                   % (args[:2], exc.__class__.__name__, exc)) from exc
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip().replace("\n", " ")
        raise Stop("git_failed args=%s rc=%s detail=%s"
                   % (args[:2], proc.returncode, detail))
    if not allow_binary and proc.stderr:
        detail = proc.stderr.decode("utf-8", "replace").strip().replace("\n", " ")
        raise Stop("git_stderr_on_success args=%s detail=%s" % (args[:2], detail))
    return proc.stdout


def require_commit(repo):
    fmt = git(repo, ["rev-parse", "--show-object-format"]).decode("ascii").strip()
    if fmt != "sha1":
        raise Stop("object_format=%s expected=sha1 (object-id proof assumes it)" % fmt)
    kind = git(repo, ["cat-file", "-t", CANDIDATE]).decode("ascii").strip()
    if kind != "commit":
        raise Stop("candidate_object_kind=%s expected=commit" % kind)
    resolved = git(repo, ["rev-parse", "--verify", CANDIDATE + "^{commit}"])
    resolved = resolved.decode("ascii").strip()
    if resolved != CANDIDATE:
        raise Stop("candidate_resolves_to=%s expected=%s" % (resolved, CANDIDATE))
    out("DERIVE_candidate sha=%s object=commit resolved=self object_format=%s"
        % (CANDIDATE, fmt))


def git_blob_oid(data):
    """Git's own object id for a blob: sha1("blob <len>\\0" + bytes)."""
    header = ("blob %d" % len(data)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + data).hexdigest()


def inventory(repo):
    """`git ls-tree -r -z --long <sha>` -> [(path, size, oid)], plus checks."""
    raw = git(repo, ["ls-tree", "-r", "-z", "--long", CANDIDATE])
    records = [r for r in raw.split(b"\x00") if r]
    if not records:
        raise Stop("empty_tree_inventory candidate=%s" % CANDIDATE)
    entries = []
    for record in records:
        if b"\t" not in record:
            raise Stop("unparsable_ls_tree_record=%r" % record[:120])
        meta, path = record.split(b"\t", 1)
        fields = meta.split()
        if len(fields) != 4:
            raise Stop("unparsable_ls_tree_meta=%r" % meta[:120])
        mode, objtype, oid, size = fields
        if objtype != b"blob":
            raise Fail("non_blob_tree_entry type=%s path=%s"
                       % (objtype.decode(), path.decode("utf-8", "replace")))
        if mode not in ALLOWED_MODES:
            raise Fail("non_regular_file_mode mode=%s path=%s"
                       % (mode.decode(), path.decode("utf-8", "replace")))
        if b"\n" in path or b"\\" in path:
            raise Fail("path_would_be_escaped_by_sha256sum path=%r" % path)
        if path.split(b"/")[-1] == b"RELEASE_SHA256SUMS":
            raise Fail("tree_carries_RELEASE_SHA256SUMS path=%s"
                       % path.decode("utf-8", "replace"))
        if path == b"RELEASE_SHA":
            raise Fail("tree_carries_RELEASE_SHA_that_package_sh_overwrites")
        try:
            size_int = int(size)
        except ValueError:
            raise Stop("unparsable_blob_size=%r path=%r" % (size, path))
        oid_text = oid.decode("ascii")
        if len(oid_text) != 40 or oid_text.strip("0123456789abcdef"):
            raise Stop("unparsable_blob_oid=%r path=%r" % (oid, path))
        entries.append((path, size_int, oid_text))
    out("DERIVE_inventory blobs=%d modes=%s"
        % (len(entries), sorted({m.decode() for m in ALLOWED_MODES})))
    return entries


def lf_required(name):
    """package.sh's two LF-required inventories, over payload-root names."""
    if name.startswith(LF_REQUIRED_DEPLOY_PREFIX):
        return "deploy"
    if name.endswith(LF_REQUIRED_SUFFIX):
        return "sh"
    return None


def derive(repo, out_path, rendering, progress_every):
    require_commit(repo)
    entries = inventory(repo)

    # `printf '%s\n' "${RELEASE_SHA}" > "${OUT}/RELEASE_SHA"`, written before the
    # manifest is generated, so it is a manifest member.
    members = [(b"./RELEASE_SHA", None, None)]
    members.extend((b"./" + path, size, oid) for path, size, oid in entries)

    # LC_ALL=C `sort -z` over NUL-terminated `find` records == byte-order sort.
    members.sort(key=lambda item: item[0])
    if len({name for name, _, _ in members}) != len(members):
        raise Fail("duplicate_member_name_in_payload")

    lines = []
    deploy_lf_count = 0
    sh_lf_count = 0
    total_bytes = 0
    for index, (name, size, oid) in enumerate(members, start=1):
        if size is None:
            data = (CANDIDATE + "\n").encode("ascii")
        else:
            rel = name[2:].decode("utf-8")
            # The trailing `--` forces revision interpretation; the working tree
            # is never consulted for this or any other path.
            data = git(repo, ["show", CANDIDATE + ":" + rel, "--"])
            if len(data) != size:
                raise Fail("blob_bytes_differ path=%s got=%d ls_tree=%d"
                           % (rel, len(data), size))
            got_oid = git_blob_oid(data)
            if got_oid != oid:
                raise Fail("blob_object_id_differs path=%s got=%s ls_tree=%s"
                           % (rel, got_oid, oid))
        kind = lf_required(name)
        if kind is not None:
            if b"\r" in data:
                raise Fail("cr_byte_in_lf_required_file name=%s"
                           % name.decode("utf-8", "replace"))
            if kind == "deploy":
                deploy_lf_count += 1
            else:
                sh_lf_count += 1
        total_bytes += len(data)
        lines.append((hashlib.sha256(data).hexdigest().encode("ascii"), name))
        if progress_every and index % progress_every == 0:
            out("DERIVE_progress hashed=%d/%d bytes=%d"
                % (index, len(members), total_bytes))

    if deploy_lf_count <= 0:
        raise Fail("no_deploy_lf_required_files_found")
    if sh_lf_count <= 0:
        raise Fail("no_sh_lf_required_files_found")
    out("DERIVE_lf_required deploy=%d other_sh=%d cr_bytes=0"
        % (deploy_lf_count, sh_lf_count))

    renderings = {}
    for label, sep in SEPARATORS.items():
        body = b"".join(digest + sep + name + b"\n" for digest, name in lines)
        renderings[label] = (body, hashlib.sha256(body).hexdigest())
        out("DERIVE_rendering %s bytes=%d sha256=%s"
            % (label, len(body), renderings[label][1]))

    binary_sha = renderings["binary"][1]
    out("DERIVE_corroboration a0_recorded_sha256=%s a0_entries=%d "
        "binary_matches=%s entries_match=%s"
        % (CORROBORATING_A0_MANIFEST_SHA256, CORROBORATING_A0_ENTRIES,
           binary_sha == CORROBORATING_A0_MANIFEST_SHA256,
           len(lines) == CORROBORATING_A0_ENTRIES))

    blob, manifest_sha = renderings[rendering]
    out("DERIVE_selected rendering=%s sha256=%s" % (rendering, manifest_sha))

    if os.path.lexists(out_path):
        raise Fail("out_path_already_exists path=%s" % out_path)
    tmp_path = out_path + ".partial"
    try:
        with open(tmp_path, "wb") as handle:
            handle.write(blob)
        os.rename(tmp_path, out_path)
    except OSError as exc:
        raise Stop("manifest_write_failed path=%s %s: %s"
                   % (out_path, exc.__class__.__name__, exc)) from exc
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    out("DERIVE_object_id_proof blobs_verified=%d method=sha1(blob_len_nul_bytes)"
        % (len(members) - 1))
    out("DERIVE_members total=%d payload_bytes_hashed=%d"
        % (len(members), total_bytes))
    out("DERIVE_manifest path=%s bytes=%d" % (out_path, len(blob)))
    out("DERIVE_manifest_sha256 %s" % manifest_sha)
    out("DERIVE_first_line %r" % blob[:blob.index(b"\n") + 1])
    out("DERIVE_last_line %r" % blob[blob.rindex(b"\n", 0, -1) + 1:])
    out("DERIVE PASS candidate=%s rendering=%s release_manifest_sha256=%s"
        % (CANDIDATE, rendering, manifest_sha))
    return PASS_RC


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--repo", required=True,
                        help="git repository that carries the frozen candidate commit")
    parser.add_argument("--out", required=True,
                        help="output manifest path; must not already exist")
    parser.add_argument("--rendering", choices=sorted(SEPARATORS), default="binary",
                        help="sha256sum separator rendering to write out "
                             "(both digests are always reported)")
    parser.add_argument("--progress-every", type=int, default=1000)
    args = parser.parse_args(argv[1:])
    try:
        return derive(args.repo, args.out, args.rendering, args.progress_every)
    except Fail as exc:
        out("DERIVE_FAIL reason=%s" % exc)
        return FAIL_RC
    except Stop as exc:
        out("DERIVE_STOP reason=%s" % exc)
        return STOP_RC
    except Exception as exc:  # never silently become a derived value
        out("DERIVE_STOP reason=unhandled %s: %s" % (exc.__class__.__name__, exc))
        return STOP_RC


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
