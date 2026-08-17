#!/usr/bin/env python3
"""Owner Analysis-Package Generator -- Bridge V2 Package 4 (first increment).

Bounded, redacted, read-only export of an explicitly allowlisted set of local
files/directories into ONE self-describing Markdown bundle, for the documented
manual Codex-subscription workflow (paste/upload one readable file).

Scope contract:
    MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE4_ANALYSIS_PACKAGE_GENERATOR_2026-08-18.md

Guarantees (enforced, not promised):
- stdlib only; NO network-capable imports (no urllib/http/socket/requests/ssl).
- NO clock reads: the generation timestamp is caller-supplied via --config, so
  identical config + inputs produce a byte-identical bundle.
- NO reading of real credential stores or dotfiles: explicit denylist of
  credential-store filenames, dotfile pruning during directory walks, and a
  hard refusal when such a path is named directly in the allowlist.
- Bounds enforced and recorded in the bundle header: 200 KB per file,
  4000 lines per file, 2 MB total bundle, binary exclusion via extension
  denylist + null-byte sniff of the first 8192 bytes.
- Pattern-based secret redaction: every match becomes `[REDACTED:<kind>]`,
  with per-kind counts in the header.
- Loud failure (exit code 2 + message on stderr) on any configuration or
  allowlist violation. Nothing is ever skipped silently; every input shows up
  in the inventory with an explicit disposition.

Exit codes: 0 = bundle written; 2 = configuration/allowlist/bounds error.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Bounds (Gate-1 frozen scope)
# ---------------------------------------------------------------------------

MAX_FILE_BYTES = 200 * 1024           # per-file byte cap (200 KB)
MAX_TOTAL_BYTES = 2 * 1024 * 1024     # total bundle cap (2 MB)
MAX_LINES = 4000                      # per-file line cap
HEADER_RESERVE = 32768                # header allowance inside the total cap
CONTENT_BUDGET = MAX_TOTAL_BYTES - HEADER_RESERVE
NULL_SNIFF_BYTES = 8192               # binary sniff window

BINARY_EXTENSIONS = frozenset((
    ".7z", ".avi", ".bin", ".bmp", ".class", ".dat", ".db", ".dll", ".eot",
    ".exe", ".gif", ".gz", ".ico", ".jar", ".jpeg", ".jpg", ".mov", ".mp3",
    ".mp4", ".o", ".pdf", ".png", ".pyc", ".so", ".sqlite", ".tar", ".ttf",
    ".wasm", ".woff", ".woff2", ".zip",
))

CREDENTIAL_STORE_NAMES = frozenset((
    ".env", ".env.local", ".env.production", ".netrc", ".npmrc",
    "auth.json", "credentials.json", "id_rsa", "id_ed25519",
))

LANG_BY_SUFFIX = {
    ".py": "python", ".md": "markdown", ".json": "json", ".txt": "text",
    ".log": "text", ".yml": "yaml", ".yaml": "yaml", ".js": "javascript",
    ".ts": "typescript", ".sh": "bash", ".ps1": "powershell", ".ini": "ini",
    ".cfg": "ini", ".toml": "toml", ".csv": "csv", ".html": "html",
    ".css": "css", ".sql": "sql",
}


class PackageError(Exception):
    """Loud, user-facing configuration / allowlist / bounds failure."""


# ---------------------------------------------------------------------------
# Redaction engine (Gate-1 kinds, fixed order, per-kind counts)
# ---------------------------------------------------------------------------

_ASSIGN_RE = re.compile(
    r"(?i)\b(?P<name>(?:[a-z0-9]+[_-])?(?:key|token|password|secret)s?)"
    r"\s*(?P<kq>['\"])?\s*(?P<sep>[=:])\s*"
    r"(?P<q>['\"])?(?P<val>[^\s'\"\[\]]{4,})(?P=q)?"
)

_AWS_RE = re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")

_HEX_ADDR_RE = re.compile(r"(?i)\b0x(?:[0-9a-f]{64}|[0-9a-f]{40})\b")

_BEARER_RE = re.compile(r"(?i)(\bbearer\s+)[A-Za-z0-9\-._~+/]{8,}={0,2}")

_HEX_TOKEN_RE = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{32,}(?![0-9A-Fa-f])")

_B64_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{40,}={0,2}(?![A-Za-z0-9+/=])"
)

REDACTION_KINDS = (
    ("assignment",
     "`key=` / `token=` / `password=` / `secret=` values (incl. prefixed forms like `api_key`)"),
    ("aws_key_id",
     "AWS-style access key ids (`AKIA`/`ASIA` + 16 upper alnum)"),
    ("hex_address",
     "`0x`-prefixed 40- or 64-hex addresses and keys"),
    ("bearer",
     "HTTP `Bearer` credentials"),
    ("long_token",
     "long hex (>=32 chars) or base64-like (>=40 chars) tokens"),
)


def _assign_repl(m):
    name = m.group("name")
    kq = m.group("kq") or ""
    sep = m.group("sep")
    return "%s%s%s [REDACTED:assignment]" % (name, kq, sep)


def _b64_repl(m):
    original = m.group(0)
    core = original.rstrip("=")
    has_digit = any(c.isdigit() for c in core)
    has_upper = any(c.isupper() for c in core)
    has_lower = any(c.islower() for c in core)
    if has_digit and has_upper and has_lower:
        return "[REDACTED:long_token]"
    return original  # not base64-like; leave untouched (not counted)


class Redactor:
    """Applies the Gate-1 redaction kinds in a fixed order; counts per kind.

    Markers are bracket-delimited on purpose: every value charset excludes
    brackets, so an already-inserted `[REDACTED:<kind>]` marker can never be
    re-matched (and re-counted) by a later rule.
    """

    def __init__(self):
        self.counts = {}

    def _sub(self, kind, regex, repl, text):
        def fn(m):
            out = repl(m) if callable(repl) else repl
            if out != m.group(0):
                self.counts[kind] = self.counts.get(kind, 0) + 1
            return out
        return regex.sub(fn, text)

    def redact(self, text):
        text = self._sub("assignment", _ASSIGN_RE, _assign_repl, text)
        text = self._sub("aws_key_id", _AWS_RE,
                         lambda m: "[REDACTED:aws_key_id]", text)
        text = self._sub("hex_address", _HEX_ADDR_RE,
                         lambda m: "[REDACTED:hex_address]", text)
        text = self._sub("bearer", _BEARER_RE,
                         lambda m: m.group(1) + "[REDACTED:bearer]", text)
        text = self._sub("long_token", _HEX_TOKEN_RE,
                         lambda m: "[REDACTED:long_token]", text)
        text = self._sub("long_token", _B64_TOKEN_RE, _b64_repl, text)
        return text


def redact_text(text):
    """Convenience wrapper for unit tests: (redacted_text, per-kind counts)."""
    r = Redactor()
    return r.redact(text), r.counts


# ---------------------------------------------------------------------------
# Config loading (strict: unknown keys are refused, never silently ignored)
# ---------------------------------------------------------------------------

ALLOWED_CONFIG_KEYS = ("timestamp", "output", "inputs")


def load_config(config_path):
    p = Path(config_path)
    try:
        text = p.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise PackageError("cannot read config file %r: %s" % (str(p), exc))
    try:
        cfg = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PackageError("config is not valid JSON: %s" % exc)
    if not isinstance(cfg, dict):
        raise PackageError("config root must be a JSON object")
    unknown = sorted(set(cfg) - set(ALLOWED_CONFIG_KEYS))
    if unknown:
        raise PackageError(
            "unknown config keys %s; allowed keys: %s"
            % (unknown, list(ALLOWED_CONFIG_KEYS)))
    for key in ALLOWED_CONFIG_KEYS:
        if key not in cfg:
            raise PackageError("missing required config key: %r" % key)
    ts = cfg["timestamp"]
    if not isinstance(ts, str) or not ts.strip():
        raise PackageError(
            "'timestamp' must be a non-empty string (caller-supplied; this "
            "generator never reads the clock)")
    out = cfg["output"]
    if not isinstance(out, str) or not out.strip():
        raise PackageError("'output' must be a non-empty path string")
    inputs = cfg["inputs"]
    if (not isinstance(inputs, list) or not inputs
            or not all(isinstance(x, str) and x.strip() for x in inputs)):
        raise PackageError(
            "'inputs' must be a non-empty list of path strings "
            "(the explicit allowlist; there are no defaults)")
    return cfg


# ---------------------------------------------------------------------------
# Input collection (allowlist-only, denylist-enforced, deterministic order)
# ---------------------------------------------------------------------------

@dataclass
class Candidate:
    display: str
    path: Path


@dataclass
class Prepared:
    display: str
    path: Path
    disposition: str
    orig_bytes: int
    orig_lines: int
    incl_bytes: int
    incl_lines: int
    content: str
    counts: dict = field(default_factory=dict)


def _norm(path_string):
    return str(path_string).replace("\\", "/")


def _is_within(child, root):
    try:
        return os.path.commonpath([os.path.normcase(str(child)),
                                   os.path.normcase(str(root))]) \
            == os.path.normcase(str(root))
    except ValueError:
        return False  # different drives -> definitely outside


def collect_candidates(cfg, config_dir, output_real):
    """Resolve the allowlist to a deterministically ordered file list.

    Returns (candidates, exclusions) where exclusions is a list of
    (display, reason) rows for everything deliberately not read.
    Raises PackageError on any allowlist violation (missing path, credential
    store named directly, symlink escaping its allowlisted root).
    """
    candidates = []
    exclusions = []
    seen_real = set()

    def note(display, reason):
        exclusions.append((display, reason))

    for raw in cfg["inputs"]:
        given = Path(raw)
        resolved = given if given.is_absolute() else config_dir / given
        if not resolved.exists():
            raise PackageError(
                "allowlisted input does not exist: %r (resolved: %s)"
                % (raw, resolved))
        real = Path(os.path.realpath(resolved))
        if real.is_dir():
            _walk_dir(_norm(raw), real, candidates, exclusions,
                      seen_real, output_real)
        elif real.is_file():
            base = resolved.name.lower()
            if base in CREDENTIAL_STORE_NAMES:
                raise PackageError(
                    "allowlisted input %r is a credential-store filename; "
                    "refusing to read it (boundary rule)" % raw)
            if base.startswith("."):
                raise PackageError(
                    "allowlisted input %r is a dotfile; refusing to read it "
                    "(boundary rule)" % raw)
            real_key = os.path.normcase(str(real))
            if real_key in seen_real:
                note(_norm(raw), "excluded: duplicate of an earlier "
                                 "allowlist entry")
                continue
            seen_real.add(real_key)
            if real_key == os.path.normcase(str(output_real)):
                note(_norm(raw), "excluded: output path (self-exclusion)")
                continue
            candidates.append(Candidate(display=_norm(raw), path=real))
        else:
            raise PackageError(
                "allowlisted input is neither a file nor a directory: %r "
                "(resolved: %s)" % (raw, resolved))

    candidates.sort(key=lambda c: c.display)
    return candidates, exclusions


def _walk_dir(root_display, root_real, candidates, exclusions,
              seen_real, output_real):

    def rec(dir_path, display_prefix, visited):
        try:
            names = sorted(os.listdir(dir_path))
        except OSError as exc:
            raise PackageError(
                "cannot list allowlisted directory %s: %s" % (dir_path, exc))
        for name in names:
            full = Path(dir_path) / name
            display = "%s/%s" % (display_prefix, name)
            if name.startswith("."):
                kind = "directory" if full.is_dir() else "file"
                exclusions.append(
                    (display, "excluded: dotfile/hidden %s (boundary rule)"
                     % kind))
                continue
            if full.is_symlink():
                target = Path(os.path.realpath(full))
                if not _is_within(target, root_real):
                    raise PackageError(
                        "symlink escapes allowlist root: %s -> %s "
                        "(refusing to follow)" % (display, target))
            real_key = os.path.normcase(str(os.path.realpath(full)))
            if full.is_dir():
                if real_key in visited:
                    exclusions.append(
                        (display, "excluded: symlink cycle / repeated "
                                  "directory"))
                    continue
                visited.add(real_key)
                rec(full, display, visited)
                continue
            if real_key in seen_real:
                exclusions.append(
                    (display, "excluded: duplicate of an earlier allowlist "
                              "entry"))
                continue
            seen_real.add(real_key)
            if real_key == os.path.normcase(str(output_real)):
                exclusions.append(
                    (display, "excluded: output path (self-exclusion)"))
                continue
            real_base = Path(os.path.realpath(full)).name
            if (name.lower() in CREDENTIAL_STORE_NAMES
                    or real_base.lower() in CREDENTIAL_STORE_NAMES
                    or real_base.startswith(".")):
                exclusions.append(
                    (display, "excluded: credential-store filename "
                              "(boundary rule; checked on both the entry "
                              "name and the symlink-resolved name)"))
                continue
            candidates.append(Candidate(display=display,
                                        path=Path(os.path.realpath(full))))

    rec(root_real, root_display, {os.path.normcase(str(root_real))})


# ---------------------------------------------------------------------------
# Read + bound + redact one file
# ---------------------------------------------------------------------------

def prepare_file(cand):
    """Return (Prepared, None) or (None, binary_reason)."""
    try:
        size = cand.path.stat().st_size
        with open(cand.path, "rb") as fh:
            head = fh.read(NULL_SNIFF_BYTES)
            why_binary = None
            suffix = cand.path.suffix.lower()
            if suffix in BINARY_EXTENSIONS:
                why_binary = "binary (extension denylist: %s)" % suffix
            elif b"\x00" in head:
                why_binary = "binary (null-byte sniff in first %d bytes)" \
                             % NULL_SNIFF_BYTES
            if why_binary is not None:
                return None, why_binary
            fh.seek(0)
            raw = fh.read(MAX_FILE_BYTES + 1)  # +1 byte detects over-cap
    except OSError as exc:
        raise PackageError("cannot read allowlisted file %s: %s"
                           % (cand.display, exc))

    text = raw.decode("utf-8", errors="replace")
    orig_lines = len(text.splitlines())

    truncated_byte = size > MAX_FILE_BYTES
    if truncated_byte:
        text = text[:MAX_FILE_BYTES]

    lines = text.splitlines(keepends=True)
    truncated_line = len(lines) > MAX_LINES
    if truncated_line:
        text = "".join(lines[:MAX_LINES])

    counts_total = Redactor()
    text = counts_total.redact(text)

    if truncated_byte and truncated_line:
        disposition = "truncated (byte+line caps)"
    elif truncated_byte:
        disposition = "truncated (byte cap)"
    elif truncated_line:
        disposition = "truncated (line cap)"
    else:
        disposition = "included"

    return Prepared(
        display=cand.display,
        path=cand.path,
        disposition=disposition,
        orig_bytes=size,
        orig_lines=orig_lines,
        incl_bytes=len(text.encode("utf-8")),
        incl_lines=len(text.splitlines()),
        content=text,
        counts=counts_total.counts,
    ), None


# ---------------------------------------------------------------------------
# Bundle rendering
# ---------------------------------------------------------------------------

def _fence_for(content):
    longest = 0
    for m in re.finditer(r"`+", content):
        if len(m.group(0)) > longest:
            longest = len(m.group(0))
    return "`" * max(4, longest + 1)


def _fmt_counts(counts):
    if not counts:
        return "none"
    return ", ".join(
        "%s=%d" % (kind, counts[kind])
        for kind, _ in REDACTION_KINDS if kind in counts)


def render_section(p):
    fence = _fence_for(p.content)
    lang = LANG_BY_SUFFIX.get(p.path.suffix.lower(), "")
    body = p.content if p.content.endswith("\n") else p.content + "\n"
    # Concatenation, not %-formatting: file content may itself contain '%'.
    return (
        "---\n\n"
        "## File: `" + p.display + "`\n\n"
        "- Disposition: " + p.disposition + "\n"
        "- Original: %d bytes, %d lines\n" % (p.orig_bytes, p.orig_lines)
        + "- Included: %d bytes, %d lines\n" % (p.incl_bytes, p.incl_lines)
        + "- Redactions: " + _fmt_counts(p.counts) + "\n\n"
        + fence + lang + "\n" + body + fence + "\n\n"
    )


def render_header(cfg, included, exclusions, omitted, kind_totals, stats):
    L = []
    L.append("# Analysis Package Bundle")
    L.append("")
    L.append("- **Generated (caller-supplied timestamp):** %s" % cfg["timestamp"])
    L.append("- **Generator:** `IBKR_PAPER_BRIDGE/tools_v2/analysis_package/"
             "generate_analysis_package.py` (stdlib-only, no network imports, "
             "no clock reads)")
    L.append("- **Mode:** bounded, redacted, read-only export of explicitly "
             "allowlisted inputs; output is handed over manually")
    L.append("- **Scope contract:** Gate-1 record "
             "`MTC_COMMAND_CENTER/11_TRIAGE/"
             "GATE1_PACKAGE4_ANALYSIS_PACKAGE_GENERATOR_2026-08-18.md`")
    L.append("")
    L.append("## Bounds applied")
    L.append("")
    L.append("| Bound | Value |")
    L.append("|---|---|")
    L.append("| Per-file byte cap | %d bytes (200 KB) |" % MAX_FILE_BYTES)
    L.append("| Per-file line cap | %d lines |" % MAX_LINES)
    L.append("| Total bundle cap | %d bytes (2 MB) |" % MAX_TOTAL_BYTES)
    L.append("| Content budget | %d bytes (total cap minus %d-byte header "
             "reservation) |" % (CONTENT_BUDGET, HEADER_RESERVE))
    L.append("| Binary exclusion | extension denylist + null-byte sniff of "
             "first %d bytes |" % NULL_SNIFF_BYTES)
    L.append("")
    L.append("Binary extension denylist: %s"
             % " ".join(sorted(BINARY_EXTENSIONS)))
    L.append("")
    L.append("## Redaction summary (per kind)")
    L.append("")
    L.append("| Kind | Pattern | Replacements |")
    L.append("|---|---|---|")
    for kind, desc in REDACTION_KINDS:
        L.append("| %s | %s | %d |" % (kind, desc, kind_totals.get(kind, 0)))
    L.append("")
    L.append("Total redactions: %d" % sum(kind_totals.values()))
    L.append("")
    L.append("## Allowlisted inputs (as given in config)")
    L.append("")
    L.append("| # | Path | Type |")
    L.append("|---|---|---|")
    for i, raw in enumerate(cfg["inputs"], 1):
        L.append("| %d | `%s` | allowlist entry |" % (i, _norm(raw)))
    L.append("")
    L.append("## Input inventory")
    L.append("")
    L.append("| # | Path | Disposition | Orig bytes | Orig lines |"
             " Incl bytes | Incl lines |")
    L.append("|---|---|---|---|---|---|---|")
    for i, p in enumerate(included, 1):
        L.append("| %d | `%s` | %s | %d | %d | %d | %d |"
                 % (i, p.display, p.disposition, p.orig_bytes, p.orig_lines,
                    p.incl_bytes, p.incl_lines))
    for i, (display, reason) in enumerate(exclusions + omitted,
                                          len(included) + 1):
        L.append("| %d | `%s` | %s | - | - | - | - |"
                 % (i, display, reason))
    L.append("")
    L.append("Bundle stats: %d files included (%d truncated), %d excluded, "
             "%d omitted for total cap; %d content bytes of %d budget. "
             "The bundle size before the footer is stated in the footer "
             "(a final size cannot be known before the bundle is rendered)."
             % (stats["included"], stats["truncated"], stats["excluded"],
                stats["omitted"], stats["content_bytes"], CONTENT_BUDGET))
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def generate_bundle(cfg, config_dir):
    out_given = Path(cfg["output"])
    out_path = out_given if out_given.is_absolute() else config_dir / out_given
    output_real = Path(os.path.realpath(out_path))

    candidates, exclusions = collect_candidates(cfg, config_dir, output_real)

    prepared = []
    for cand in candidates:
        prep, why_binary = prepare_file(cand)
        if prep is None:
            exclusions.append((cand.display, "excluded: %s" % why_binary))
        else:
            prepared.append(prep)

    used = 0
    included = []
    omitted = []
    for p in prepared:
        if used + p.incl_bytes > CONTENT_BUDGET:
            omitted.append(
                (p.display,
                 "omitted: total content cap (%d more bytes would exceed "
                 "the %d-byte budget)" % (p.incl_bytes, CONTENT_BUDGET)))
            continue
        used += p.incl_bytes
        included.append(p)

    kind_totals = {}
    for p in included:
        for kind, n in p.counts.items():
            kind_totals[kind] = kind_totals.get(kind, 0) + n

    stats = {
        "included": len(included),
        "truncated": sum(1 for p in included if p.disposition != "included"),
        "excluded": len(exclusions),
        "omitted": len(omitted),
        "content_bytes": used,
        "redaction_total": sum(kind_totals.values()),
    }

    body = "".join(render_section(p) for p in included)
    header = render_header(cfg, included, exclusions, omitted,
                           kind_totals, stats)
    pre_footer = header + body
    pre_footer_bytes = len(pre_footer.encode("utf-8"))
    footer = ("\n---\n\nFooter: bundle size before this footer: %d bytes "
              "(total cap %d bytes; the footer itself adds the final few "
              "bytes and is included in the enforced total).\n"
              % (pre_footer_bytes, MAX_TOTAL_BYTES))
    bundle_text = pre_footer + footer
    stats["total_bytes"] = len(bundle_text.encode("utf-8"))
    if stats["total_bytes"] > MAX_TOTAL_BYTES:
        raise PackageError(
            "internal bounds error: rendered bundle is %d bytes, over the "
            "%d-byte total cap (header reservation exhausted; reduce the "
            "number of allowlisted inputs)"
            % (stats["total_bytes"], MAX_TOTAL_BYTES))

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(bundle_text)
    except OSError as exc:
        raise PackageError("cannot write output bundle %s: %s"
                           % (out_path, exc))
    return out_path, stats


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(
        prog="generate_analysis_package.py",
        description="Bounded, redacted, read-only analysis-package bundle "
                    "generator (Bridge V2 Package 4, T1).")
    parser.add_argument(
        "--config", required=True,
        help="path to the JSON config: allowlisted 'inputs' (files/dirs), "
             "'output' bundle path, caller-supplied 'timestamp' string")
    args = parser.parse_args(argv)
    try:
        cfg = load_config(args.config)
        config_dir = Path(args.config).resolve().parent
        out_path, stats = generate_bundle(cfg, config_dir)
    except PackageError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    print("OK wrote %s (%d bytes; %d included, %d truncated, %d excluded, "
          "%d omitted; %d redactions)"
          % (out_path, stats["total_bytes"], stats["included"],
             stats["truncated"], stats["excluded"], stats["omitted"],
             stats.get("redaction_total", 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
