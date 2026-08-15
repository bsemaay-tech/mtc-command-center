#!/usr/bin/env python3
"""Conservative static path-scope prover for frozen Bash inputs (round 2).

Two rules govern every line below.

1.  Coverage is fail-closed.  Any command, option, redirection, expansion or
    construct this tool does not model emits a specific UNRESOLVED record
    naming what could not be resolved.  Silence is never a result, an
    inability to evaluate is never a PASS, and zero facts plus PASS is a bug.

2.  The membership proof is LEXICAL ARGV SCOPE only.  The tool reads frozen
    bytes; it performs no host probe, resolves no symlink and crosses no mount
    boundary.  ``ALLOW-LEXICAL`` therefore states that the normalized argv
    string lies inside an allowlist pattern - not that the host object opened
    at run time lies inside that tree.  Binding the lexical result to a real
    host tree needs a separate symlink/mount-chain proof that this tool does
    not attempt and does not claim.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
import dataclasses
import enum
import json
import posixpath
import re
import urllib.parse
from pathlib import Path


RC_FORBIDDEN = 1
RC_PARSE = 3

NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
ASSIGN_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", re.S)
NETWORK_RE = re.compile(r"^(?:\[[0-9A-Fa-f:]+\]|[A-Za-z0-9_.-]+):[0-9]{1,5}$")
GLOB_RE = re.compile(r"[*?[]")
DEV_NET_RE = re.compile(r"^/dev/(tcp|udp)/([^/]*)/([^/]*)$")
FD_PREFIX_RE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}(?=[<>])")
# C-2: assignment-value member grammar.  A scheme URI belongs to the endpoint
# domain, not the filesystem domain, and must not be colon-split into fragments;
# an option word marks a value that a consumer reads as command text.
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
OPTION_WORD_RE = re.compile(r"^--?[A-Za-z0-9?]")
# C-3: only a URI's scheme and authority are colon-protected.  Round 4 used
# URI_SCHEME_RE to disable colon splitting for the COMPLETE value, so a mixed
# loader list whose first member happened to be a URI lost every later member.
URI_PREFIX_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^/]*")

# Issue kinds.  These are deliberately distinct fields with distinct names:
# an Issue cardinality is not a path-set cardinality (round-1 finding 8).
KIND_PARSE = "parse"
KIND_COVERAGE = "coverage"
KIND_PATH = "unresolved_path"
KIND_ENDPOINT = "unresolved_endpoint"
KIND_PROVENANCE = "provenance"
KIND_ORDER = {
    KIND_PARSE: 0,
    KIND_COVERAGE: 1,
    KIND_PATH: 2,
    KIND_ENDPOINT: 3,
    KIND_PROVENANCE: 4,
}

MAX_NESTING = 12


@dataclasses.dataclass(frozen=True)
class Token:
    text: str
    line: int
    operator: bool = False


@dataclasses.dataclass(frozen=True)
class ExpansionSegment:
    rendered_start: int
    rendered_end: int
    raw_start: int
    raw_end: int
    raw_text: str
    rendered_text: str
    origin: str
    sources: frozenset[str] = frozenset()


@dataclasses.dataclass(frozen=True)
class ExpansionTrace:
    raw_rhs: str
    rendered_text: str
    segments: tuple[ExpansionSegment, ...]


@dataclasses.dataclass(frozen=True)
class Value:
    text: str | None
    reason: str | None = None
    sources: frozenset[str] = frozenset()
    trace: ExpansionTrace | None = None

    @property
    def known(self) -> bool:
        return self.text is not None


@dataclasses.dataclass(frozen=True)
class Use:
    value: str
    line: int
    primitive: str
    expression: str
    sources: frozenset[str]
    domain: str = "fs"
    member_id: str | None = None


@dataclasses.dataclass(frozen=True)
class Issue:
    line: int
    kind: str
    reason: str
    expression: str


class DispositionKind(str, enum.Enum):
    ALLOWED_WITH_REASON = "ALLOWED_WITH_REASON"
    FORBIDDEN_WITH_REASON = "FORBIDDEN_WITH_REASON"
    UNRESOLVED_FAIL_CLOSED = "UNRESOLVED_FAIL_CLOSED"


@dataclasses.dataclass(frozen=True)
class RawSlice:
    raw_start: int
    raw_end: int
    raw_text: str
    origin: str


@dataclasses.dataclass(frozen=True)
class MemberOccurrence:
    member_id: str
    value_id: str
    reading: str
    ordinal: int
    rendered_start: int
    rendered_end: int
    raw_slices: tuple[RawSlice, ...]
    text: str
    sources: frozenset[str]
    line: int
    primitive: str
    expression: str


@dataclasses.dataclass(frozen=True)
class TerminalDisposition:
    member_id: str
    value_id: str
    disposition: DispositionKind | str
    reason: str
    rule: str | None
    candidate_domain: str | None
    candidate_value: str | None
    sources: frozenset[str]


@dataclasses.dataclass(frozen=True)
class AdmittedValue:
    value_id: str
    line: int
    site: str
    expression: str
    raw_rhs: str
    rendered_text: str | None
    trace: ExpansionTrace | None
    expected_counts: tuple[tuple[str, int], ...]
    member_ids: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class AccountingFault:
    value_id: str | None
    member_id: str | None
    reason: str


@dataclasses.dataclass
class AccountingRunContext:
    next_analyzer_ordinal: int = 0

    def allocate_analyzer_id(self) -> str:
        ordinal = self.next_analyzer_ordinal
        self.next_analyzer_ordinal += 1
        return f"A{ordinal:04d}"


@dataclasses.dataclass(frozen=True)
class Rule:
    kind: str
    value: str

    @property
    def domain(self) -> str:
        return "net" if self.kind == "network" else "fs"

    def matches(self, candidate: str, primitive: str, domain: str) -> bool:
        if domain != self.domain:
            return False
        if self.kind == "network":
            return candidate == self.value
        if self.kind == "terminal":
            return candidate == self.value and primitive == "stat"
        if self.kind == "exact":
            return candidate == self.value
        root = self.value
        return candidate == root or candidate.startswith(root + "/")

    def render(self) -> str:
        if self.kind == "tree":
            return self.value + "/**"
        if self.kind == "terminal":
            return self.value + " [terminal]"
        return self.value


class LexError(Exception):
    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line


def unquote_delimiter(word: str) -> tuple[str, bool]:
    """Return the here-document delimiter and whether it was quoted."""
    out: list[str] = []
    quoted = False
    index = 0
    while index < len(word):
        char = word[index]
        if char == "\\":
            quoted = True
            if index + 1 < len(word):
                out.append(word[index + 1])
                index += 2
                continue
            index += 1
            continue
        if char in "'\"":
            quoted = True
            closing = char
            index += 1
            while index < len(word) and word[index] != closing:
                out.append(word[index])
                index += 1
            index += 1
            continue
        out.append(char)
        index += 1
    return "".join(out), quoted


class ShellLexer:
    """Quote-aware lexer which keeps raw word spelling for safe expansion."""

    OPERATORS = (
        ";;&", "<<<", "<<-", "&>>",
        "<<", ">>", "<>", ">|", "&&", "||", ">&", "<&", "&>", "|&", ";;", ";&",
        "((", "))",
        "(", ")", "{", "}", ";", "|", "&", "<", ">", "!",
    )
    HEREDOC_OPS = {"<<", "<<-"}
    WORD_BREAK = " \t\r\n;&|()<>"

    def __init__(self, text: str) -> None:
        self.text = text
        self.n = len(text)
        self.i = 0
        self.line = 1
        self.substitutions: list[tuple[int, str]] = []

    def _harvest(self, body: str, base_line: int) -> None:
        """Record command substitutions found inside an expanded body."""
        if "$" not in body and "`" not in body:
            return
        nested = ShellLexer(body)
        try:
            nested.tokens()
        except LexError:
            return
        self.substitutions.extend(
            (base_line + nested_line - 1, nested_body)
            for nested_line, nested_body in nested.substitutions
        )

    def _balanced(self, opening: str, closing: str, command: bool) -> str:
        start = self.i
        start_line = self.line
        self.i += len(opening)
        depth = 1
        quote: str | None = None
        escaped = False
        body_start = self.i
        while self.i < self.n:
            c = self.text[self.i]
            if c == "\n":
                self.line += 1
            if escaped:
                escaped = False
                self.i += 1
                continue
            if c == "\\" and quote != "'":
                escaped = True
                self.i += 1
                continue
            if quote:
                if c == quote:
                    quote = None
                self.i += 1
                continue
            if c in "'\"":
                quote = c
                self.i += 1
                continue
            if self.text.startswith(opening, self.i):
                depth += 1
                self.i += len(opening)
                continue
            if self.text.startswith(closing, self.i):
                depth -= 1
                if depth == 0:
                    body = self.text[body_start:self.i]
                    self.i += len(closing)
                    if command:
                        self.substitutions.append((start_line, body))
                    else:
                        # Parameter fallbacks and arithmetic can execute
                        # substitutions even when the scalar never becomes a
                        # path.
                        self._harvest(body, start_line)
                    return self.text[start:self.i]
                self.i += len(closing)
                continue
            self.i += 1
        raise LexError(start_line, f"unterminated {opening} expansion")

    def _backtick(self) -> str:
        start = self.i
        start_line = self.line
        self.i += 1
        inner: list[str] = []
        while self.i < self.n and self.text[self.i] != "`":
            if self.text[self.i] == "\\" and self.i + 1 < self.n:
                inner.extend(self.text[self.i:self.i + 2])
                self.i += 2
                continue
            if self.text[self.i] == "\n":
                self.line += 1
            inner.append(self.text[self.i])
            self.i += 1
        if self.i >= self.n:
            raise LexError(start_line, "unterminated backtick substitution")
        self.i += 1
        self.substitutions.append((start_line, "".join(inner)))
        return self.text[start:self.i]

    def _is_word_operator(self, char: str) -> bool:
        """`{` and `}` are reserved words only as complete words.

        Without this guard the lexer splits `/safe/{a,b}` and invents a path,
        which is the opposite of reporting a brace expansion it cannot model.
        """
        following = self.text[self.i + 1:self.i + 2]
        return following == "" or following in self.WORD_BREAK

    def _consume_heredocs(self, pending: list[tuple[bool, str]]) -> None:
        for strip, delimiter_word in pending:
            delimiter, quoted = unquote_delimiter(delimiter_word)
            start_line = self.line
            body: list[str] = []
            while True:
                if self.i >= self.n:
                    raise LexError(
                        start_line,
                        f"unterminated here-document delimited by {delimiter}",
                    )
                end = self.text.find("\n", self.i)
                if end < 0:
                    raw_line = self.text[self.i:]
                    self.i = self.n
                else:
                    raw_line = self.text[self.i:end]
                    self.i = end + 1
                candidate = raw_line.lstrip("\t") if strip else raw_line
                if candidate.rstrip("\r") == delimiter:
                    self.line += 1
                    break
                body.append(raw_line)
                self.line += 1
                if end < 0:
                    raise LexError(
                        start_line,
                        f"unterminated here-document delimited by {delimiter}",
                    )
            if not quoted:
                # An unquoted delimiter means the body is expanded, so a
                # command substitution inside it really executes.
                self._harvest("\n".join(body), start_line)

    def tokens(self) -> list[Token]:
        result: list[Token] = []
        buf: list[str] = []
        word_line = self.line
        quote: str | None = None
        escaped = False
        pending_strip: bool | None = None
        pending_heredocs: list[tuple[bool, str]] = []

        def flush() -> None:
            nonlocal buf, pending_strip
            if buf:
                text = "".join(buf)
                result.append(Token(text, word_line))
                buf = []
                if pending_strip is not None:
                    pending_heredocs.append((pending_strip, text))
                    pending_strip = None

        while self.i < self.n:
            c = self.text[self.i]
            if quote:
                if quote == '"' and self.text.startswith("$((", self.i):
                    buf.append(self._balanced("$((", "))", command=False))
                    continue
                if quote == '"' and self.text.startswith("$(", self.i):
                    buf.append(self._balanced("$(", ")", command=True))
                    continue
                if quote == '"' and self.text.startswith("${", self.i):
                    buf.append(self._balanced("${", "}", command=False))
                    continue
                if quote == '"' and c == "`":
                    buf.append(self._backtick())
                    continue
                buf.append(c)
                if escaped:
                    escaped = False
                elif c == "\\" and quote == '"':
                    escaped = True
                elif c == quote:
                    quote = None
                if c == "\n":
                    self.line += 1
                self.i += 1
                continue

            if c in "'\"":
                if not buf:
                    word_line = self.line
                quote = c
                buf.append(c)
                self.i += 1
                continue
            if c == "\\":
                if not buf:
                    word_line = self.line
                if self.i + 1 >= self.n:
                    raise LexError(self.line, "trailing backslash")
                buf.extend(self.text[self.i:self.i + 2])
                if self.text[self.i + 1] == "\n":
                    self.line += 1
                self.i += 2
                continue
            if self.text.startswith("$((", self.i):
                if not buf:
                    word_line = self.line
                buf.append(self._balanced("$((", "))", command=False))
                continue
            if self.text.startswith("$(", self.i):
                if not buf:
                    word_line = self.line
                buf.append(self._balanced("$(", ")", command=True))
                continue
            if self.text.startswith("${", self.i):
                if not buf:
                    word_line = self.line
                buf.append(self._balanced("${", "}", command=False))
                continue
            if c == "`":
                if not buf:
                    word_line = self.line
                buf.append(self._backtick())
                continue
            if c == "\n":
                flush()
                result.append(Token("\n", self.line, True))
                self.line += 1
                self.i += 1
                if pending_heredocs:
                    self._consume_heredocs(pending_heredocs)
                    pending_heredocs = []
                continue
            if c in " \t\r":
                flush()
                self.i += 1
                continue
            if c == "#" and not buf:
                while self.i < self.n and self.text[self.i] != "\n":
                    self.i += 1
                continue
            if c == "{" and not buf:
                fd_match = FD_PREFIX_RE.match(self.text[self.i:])
                if fd_match:
                    result.append(Token(fd_match.group(0), self.line))
                    self.i += len(fd_match.group(0))
                    continue
            if c == "!" and self.i + 1 < self.n and self.text[self.i + 1] == "=":
                if not buf:
                    word_line = self.line
                buf.append("!")
                self.i += 1
                continue
            if c in "{}" and (buf or not self._is_word_operator(c)):
                if not buf:
                    word_line = self.line
                buf.append(c)
                self.i += 1
                continue
            op = next(
                (item for item in self.OPERATORS if self.text.startswith(item, self.i)),
                None,
            )
            if op:
                flush()
                result.append(Token(op, self.line, True))
                self.i += len(op)
                if op in self.HEREDOC_OPS:
                    pending_strip = op == "<<-"
                continue
            if not buf:
                word_line = self.line
            buf.append(c)
            self.i += 1
        if quote:
            raise LexError(word_line, f"unterminated {quote} quote")
        flush()
        if pending_heredocs:
            self._consume_heredocs(pending_heredocs)
        return result


def decode_ansi(text: str) -> str:
    """Decode the small ANSI-C quote subset without executing anything."""
    out: list[str] = []
    i = 0
    mapping = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\", "'": "'", '"': '"'}
    while i < len(text):
        if text[i] != "\\":
            out.append(text[i])
            i += 1
            continue
        if i + 1 >= len(text):
            raise ValueError("trailing ANSI-C escape")
        nxt = text[i + 1]
        if nxt not in mapping:
            raise ValueError(f"unsupported ANSI-C escape \\{nxt}")
        out.append(mapping[nxt])
        i += 2
    return "".join(out)


def brace_span(raw: str, start: int) -> tuple[int, bool] | None:
    """Return (end, expands) for the unquoted brace group at raw[start]."""
    depth = 0
    quote: str | None = None
    expands = False
    i = start
    while i < len(raw):
        ch = raw[i]
        if quote:
            if ch == "\\" and quote == '"' and i + 1 < len(raw):
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch == "\\":
            i += 2
            continue
        if ch in "'\"":
            quote = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
            i += 1
            continue
        if ch == "}":
            depth -= 1
            i += 1
            if depth == 0:
                return i, expands
            continue
        if depth == 1 and (ch == "," or raw.startswith("..", i)):
            expands = True
        i += 1
    return None


def expand_word(raw: str, env: dict[str, Value], allow_tilde: bool = True) -> Value:
    out: list[str] = []
    segments: list[ExpansionSegment] = []
    sources: set[str] = set()
    rendered_offset = 0

    def append_segment(
        raw_start: int,
        raw_end: int,
        rendered: str,
        origin: str,
        segment_sources: frozenset[str] = frozenset(),
    ) -> None:
        nonlocal rendered_offset
        out.append(rendered)
        item = ExpansionSegment(
            rendered_offset,
            rendered_offset + len(rendered),
            raw_start,
            raw_end,
            raw[raw_start:raw_end],
            rendered,
            origin,
            segment_sources,
        )
        if (
            origin == "literal"
            and segments
            and segments[-1].origin == "literal"
            and segments[-1].sources == segment_sources
            and segments[-1].raw_end == raw_start
            and segments[-1].rendered_end == rendered_offset
        ):
            previous = segments[-1]
            segments[-1] = dataclasses.replace(
                previous,
                rendered_end=item.rendered_end,
                raw_end=item.raw_end,
                raw_text=previous.raw_text + item.raw_text,
                rendered_text=previous.rendered_text + item.rendered_text,
            )
        else:
            segments.append(item)
        rendered_offset += len(rendered)
        sources.update(segment_sources)

    i = 0
    quote: str | None = None
    while i < len(raw):
        c = raw[i]
        if quote == "'":
            if c == "'":
                append_segment(i, i + 1, "", "quote_elision")
                quote = None
            else:
                append_segment(i, i + 1, c, "literal")
            i += 1
            continue
        if quote == '"':
            if c == '"':
                append_segment(i, i + 1, "", "quote_elision")
                quote = None
                i += 1
                continue
            if c == "\\" and i + 1 < len(raw) and raw[i + 1] in '$`"\\\n':
                rendered = "" if raw[i + 1] == "\n" else raw[i + 1]
                append_segment(i, i + 2, rendered, "escape")
                i += 2
                continue
        else:
            if raw.startswith("$'", i):
                end = i + 2
                escaped = False
                body: list[str] = []
                while end < len(raw):
                    ch = raw[end]
                    if ch == "'" and not escaped:
                        break
                    body.append(ch)
                    if ch == "\\" and not escaped:
                        escaped = True
                    else:
                        escaped = False
                    end += 1
                if end >= len(raw):
                    return Value(None, "unterminated ANSI-C quote")
                try:
                    rendered = decode_ansi("".join(body))
                except ValueError as exc:
                    return Value(None, str(exc))
                append_segment(i, end + 1, rendered, "escape")
                i = end + 1
                continue
            if c == "'":
                append_segment(i, i + 1, "", "quote_elision")
                quote = "'"
                i += 1
                continue
            if c == '"':
                append_segment(i, i + 1, "", "quote_elision")
                quote = '"'
                i += 1
                continue
            if c == "\\":
                if i + 1 >= len(raw):
                    return Value(None, "trailing escape")
                rendered = "" if raw[i + 1] == "\n" else raw[i + 1]
                append_segment(i, i + 2, rendered, "escape")
                i += 2
                continue
            if c == "~" and (i == 0 or raw[i - 1] == ":"):
                if not allow_tilde:
                    return Value(None, "tilde expansion in an unmodeled position")
                match = re.match(r"~([^/\"'\\$:]*)", raw[i:])
                spec = match.group(1) if match else ""
                if spec:
                    return Value(
                        None,
                        f"tilde expansion ~{spec} names a home directory that is not "
                        "statically known",
                    )
                home = env.get("HOME")
                if home is None or not home.known or not (home.text or "").startswith("/"):
                    return Value(
                        None,
                        "tilde expansion depends on HOME, which is not a pinned "
                        "absolute constant",
                    )
                raw_end = i + len(match.group(0) if match else "~")
                append_segment(i, raw_end, home.text or "", "parameter_expansion", home.sources)
                i = raw_end
                continue
            if c == "{":
                span = brace_span(raw, i)
                if span is not None and span[1]:
                    return Value(None, "brace expansion makes the word set dynamic")

        if raw.startswith("$((", i):
            return Value(None, "arithmetic expansion")
        if c == "`" or raw.startswith("$(", i):
            return Value(None, "command substitution")
        if raw.startswith("${", i):
            end = raw.find("}", i + 2)
            if end < 0:
                return Value(None, "unterminated parameter expansion")
            expr = raw[i + 2:end]
            if NAME_RE.fullmatch(expr):
                name, fallback, mode = expr, None, None
            else:
                match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(:-|-|:\?|\?)(.*)", expr, re.S)
                if not match:
                    return Value(None, f"unsupported parameter expansion ${{{expr}}}")
                name, mode, fallback = match.groups()
            value = env.get(name, Value(None, f"unpinned variable {name}"))
            origin = "parameter_expansion"
            if mode in (":-", "-") and (not value.known or (mode == ":-" and value.text == "")):
                value = expand_word(fallback or "", env, allow_tilde=False)
                origin = "fallback_expansion"
            elif mode in (":?", "?") and not value.known:
                return Value(None, f"required variable {name} is unpinned")
            if not value.known:
                return value
            append_segment(i, end + 1, value.text or "", origin, value.sources)
            i = end + 1
            continue
        if c == "$":
            match = re.match(r"\$([A-Za-z_][A-Za-z0-9_]*)", raw[i:])
            if match:
                name = match.group(1)
                value = env.get(name, Value(None, f"unpinned variable {name}"))
                if not value.known:
                    return value
                append_segment(
                    i,
                    i + len(match.group(0)),
                    value.text or "",
                    "parameter_expansion",
                    value.sources,
                )
                i += len(match.group(0))
                continue
            if i + 1 < len(raw) and raw[i + 1] in "0123456789@*#?$!-":
                return Value(None, f"dynamic shell parameter ${raw[i + 1]}")
        append_segment(i, i + 1, c, "literal")
        i += 1
    if quote:
        return Value(None, "unterminated quote")
    rendered_text = "".join(out)
    trace = ExpansionTrace(raw, rendered_text, tuple(segments))
    return Value(rendered_text, sources=frozenset(sources), trace=trace)


def parse_constants(path: Path) -> dict[str, Value]:
    env: dict[str, Value] = {}
    for line_no, original in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = original.strip()
        if not line or line.startswith("#"):
            continue
        match = ASSIGN_RE.fullmatch(line)
        if not match:
            raise LexError(line_no, "constants line is not KEY=VALUE")
        name, raw = match.groups()
        if name in env:
            raise LexError(line_no, f"duplicate constant {name}")
        value = expand_word(raw, env)
        if not value.known:
            raise LexError(line_no, f"constant {name} is not static: {value.reason}")
        if "\x00" in (value.text or ""):
            raise LexError(line_no, f"constant {name} contains NUL")
        env[name] = Value(
            value.text,
            sources=value.sources | frozenset({name}),
            trace=value.trace,
        )
    return env


def substitute_placeholders(text: str, env: dict[str, Value], line: int) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        value = env.get(name)
        if value is None or not value.known:
            raise LexError(line, f"allowlist placeholder {name} is unpinned")
        return value.text or ""
    return re.sub(r"<([A-Za-z_][A-Za-z0-9_]*)>", replace, text)


def canonical_path(value: str, env: dict[str, Value]) -> Value:
    if "\x00" in value or "\n" in value or "\r" in value:
        return Value(None, "path contains NUL or record separator")
    if re.search(r"<[^>]+>", value):
        return Value(None, "path contains an unresolved angle-bracket placeholder")
    if GLOB_RE.search(value):
        return Value(None, "glob expansion makes the path set dynamic")
    if value == "":
        return Value(None, "empty path operand")
    if value.startswith("/"):
        return Value(posixpath.normpath(value))
    cwd = env.get("PWD")
    if cwd and cwd.known and (cwd.text or "").startswith("/"):
        return Value(posixpath.normpath(posixpath.join(cwd.text or "", value)))
    return Value(None, "relative path depends on unpinned PWD")


def normalize_network(value: str) -> Value:
    if "://" in value:
        try:
            parsed = urllib.parse.urlsplit(value)
            if not parsed.hostname:
                return Value(None, "URL has no host")
            port = parsed.port
        except ValueError as exc:
            return Value(None, f"invalid URL: {exc}")
        if port is None:
            port = 443 if parsed.scheme == "https" else 80 if parsed.scheme == "http" else None
        if port is None:
            return Value(None, "network endpoint has no static port")
        host = f"[{parsed.hostname}]" if ":" in parsed.hostname else parsed.hostname
        return Value(f"{host}:{port}")
    if NETWORK_RE.fullmatch(value):
        host, port_text = value.rsplit(":", 1)
        port = int(port_text)
        if not 1 <= port <= 65535:
            return Value(None, "network port outside 1..65535")
        return Value(f"{host}:{port}")
    return Value(None, "network endpoint grammar")


def parse_allowlist(path: Path, env: dict[str, Value]) -> list[Rule]:
    rules: list[Rule] = []
    for line_no, original in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = original.strip()
        if not line or line.startswith("#"):
            continue
        kind = "exact"
        if line.startswith("terminal:"):
            kind, line = "terminal", line[len("terminal:"):].strip()
        elif line.startswith("tree:"):
            kind, line = "tree", line[len("tree:"):].strip()
        line = substitute_placeholders(line, env, line_no)
        if line.endswith("/**"):
            if kind == "terminal":
                raise LexError(line_no, "terminal rule cannot end in /**")
            kind, line = "tree", line[:-3]
        if "://" in line or NETWORK_RE.fullmatch(line):
            normalized = normalize_network(line)
            if not normalized.known:
                raise LexError(line_no, normalized.reason or "invalid network allowlist")
            kind, line = "network", normalized.text or ""
        else:
            normalized = canonical_path(line, env)
            if not normalized.known:
                raise LexError(line_no, normalized.reason or "invalid path allowlist")
            line = normalized.text or ""
        rule = Rule(kind, line)
        if rule in rules:
            raise LexError(line_no, f"duplicate allowlist rule {rule.render()}")
        rules.append(rule)
    if not rules:
        raise LexError(0, "allowlist is empty")
    return rules


def _words(text: str) -> frozenset[str]:
    return frozenset(item for item in text.split() if item)


@dataclasses.dataclass(frozen=True)
class Spec:
    """Complete argv grammar for one registered command.

    Every accepted option is listed with the role of its value.  An option
    that is not listed is a coverage STOP, never a silent skip: that is the
    whole repair for round-1 finding 4.
    """

    name: str
    flags: frozenset[str] = frozenset()
    path_opts: frozenset[str] = frozenset()
    net_opts: frozenset[str] = frozenset()
    shell_opts: frozenset[str] = frozenset()
    data_opts: frozenset[str] = frozenset()
    fd_opts: frozenset[str] = frozenset()
    odata_opts: frozenset[str] = frozenset()
    form_opts: frozenset[str] = frozenset()
    unmodeled_opts: frozenset[str] = frozenset()
    option_re: str | None = None
    roles: tuple[str, ...] = ()
    rest: str = "path"
    note: str = ""

    def role(self, option: str) -> str | None:
        if option in self.flags:
            return "flag"
        if option in self.path_opts:
            return "path"
        if option in self.net_opts:
            return "net"
        if option in self.shell_opts:
            return "shell"
        if option in self.data_opts:
            return "data"
        if option in self.fd_opts:
            return "fd"
        if option in self.odata_opts:
            return "odata"
        if option in self.form_opts:
            return "form"
        if option in self.unmodeled_opts:
            return "unmodeled"
        if self.option_re is not None and re.fullmatch(self.option_re, option):
            return "flag"
        return None

    def positional_role(self, index: int) -> str:
        if index < len(self.roles):
            return self.roles[index]
        return self.rest

    @property
    def path_free(self) -> bool:
        """True when no accepted form of this command can carry a path.

        Only such a command may keep silent about an operand it cannot expand:
        the operand has no route to a filesystem or network primitive through
        this argv grammar.  Every other command STOPs.
        """
        if (self.path_opts or self.net_opts or self.shell_opts or self.fd_opts
                or self.form_opts or self.unmodeled_opts):
            return False
        if any(role != "data" for role in self.roles):
            return False
        return self.rest == "data"

    @property
    def unresolved_kind(self) -> str:
        """Issue kind for an operand of this command that could not be expanded."""
        roles = set(self.roles) | {self.rest}
        if "path" in roles or "dynamic" in roles:
            return KIND_PATH
        if "net" in roles:
            return KIND_ENDPOINT
        return KIND_COVERAGE


def spec(
    name: str,
    flags: str = "",
    path: str = "",
    net: str = "",
    shell: str = "",
    data: str = "",
    fd: str = "",
    odata: str = "",
    form: str = "",
    unmodeled: str = "",
    option_re: str | None = None,
    roles: tuple[str, ...] = (),
    rest: str = "path",
    note: str = "",
) -> Spec:
    return Spec(
        name=name,
        flags=_words(flags),
        path_opts=_words(path),
        net_opts=_words(net),
        shell_opts=_words(shell),
        data_opts=_words(data),
        fd_opts=_words(fd),
        odata_opts=_words(odata),
        form_opts=_words(form),
        unmodeled_opts=_words(unmodeled),
        option_re=option_re,
        roles=roles,
        rest=rest,
        note=note,
    )


HELP = "--help --version"

SPECS: dict[str, Spec] = {}


def _register(*items: Spec) -> None:
    for item in items:
        SPECS[item.name] = item


# --- filesystem readers and writers -------------------------------------
_register(
    spec("cat", flags="-n -b -E -T -v -s -A -e -t -u --number --number-nonblank "
                      "--show-ends --show-tabs --show-all --squeeze-blank "
                      "--show-nonprinting " + HELP),
    spec("head", flags="-q -v -z --quiet --silent --verbose --zero-terminated " + HELP,
         data="-n -c --lines --bytes", option_re=r"-[0-9]+"),
    spec("tail", flags="-q -v -z -f -F --quiet --silent --verbose --zero-terminated "
                       "--follow --retry " + HELP,
         data="-n -c --lines --bytes -s --sleep-interval --pid --max-unchanged-stats",
         odata="--follow", option_re=r"-[0-9]+"),
    spec("wc", flags="-c -m -l -L -w --bytes --chars --lines --words "
                     "--max-line-length " + HELP,
         path="--files0-from"),
    spec("sha256sum", flags="-b -c -t -z --binary --check --tag --text --zero "
                            "--quiet --status --strict --warn --ignore-missing " + HELP),
    spec("sha1sum", flags="-b -c -t -z --binary --check --tag --text --zero "
                          "--quiet --status --strict --warn --ignore-missing " + HELP),
    spec("md5sum", flags="-b -c -t -z --binary --check --tag --text --zero "
                         "--quiet --status --strict --warn --ignore-missing " + HELP),
    spec("cksum", flags="-a --algorithm " + HELP),
    spec("touch", flags="-a -c -f -m -h --no-create --no-dereference --time " + HELP,
         data="-d -t --date --time", path="-r --reference"),
    spec("mkdir", flags="-p -v --parents --verbose " + HELP,
         data="-m --mode -Z --context", odata="--context"),
    spec("rmdir", flags="-p -v --parents --verbose --ignore-fail-on-non-empty " + HELP),
    spec("rm", flags="-f -i -I -r -R -v -d --force --recursive --verbose --dir "
                     "--one-file-system --no-preserve-root --preserve-root "
                     "--interactive " + HELP,
         odata="--interactive --preserve-root"),
    spec("cp", flags="-a -b -d -f -i -l -L -n -P -p -R -r -s -u -v -x -H -T -Z "
                     "--archive --backup --dereference --force --link --no-clobber "
                     "--no-dereference --recursive --symbolic-link --update --verbose "
                     "--one-file-system --no-target-directory --remove-destination "
                     "--parents --preserve --no-preserve --sparse --reflink --attributes-only " + HELP,
         path="-t --target-directory",
         data="-S --suffix --context",
         odata="--backup --preserve --no-preserve --sparse --reflink --update --context"),
    spec("mv", flags="-b -f -i -n -u -v -T -Z --backup --force --interactive "
                     "--no-clobber --update --verbose --strip-trailing-slashes "
                     "--no-target-directory " + HELP,
         path="-t --target-directory", data="-S --suffix",
         odata="--backup --update"),
    spec("ln", flags="-b -d -f -i -L -n -P -r -s -T -v --symbolic --force "
                     "--no-dereference --relative --verbose --no-target-directory "
                     "--directory --logical --physical --interactive " + HELP,
         path="-t --target-directory", data="-S --suffix", odata="--backup"),
    spec("chmod", flags="-c -f -v -R --changes --silent --quiet --verbose --recursive "
                        "--no-preserve-root --preserve-root " + HELP,
         path="--reference", roles=("data",), rest="path"),
    spec("chown", flags="-c -f -v -R -h -H -L -P --changes --silent --quiet --verbose "
                        "--recursive --dereference --no-dereference --no-preserve-root "
                        "--preserve-root " + HELP,
         path="--reference", data="--from", roles=("data",), rest="path"),
    spec("chgrp", flags="-c -f -v -R -h -H -L -P --changes --silent --quiet --verbose "
                        "--recursive --dereference --no-dereference --no-preserve-root "
                        "--preserve-root " + HELP,
         path="--reference", roles=("data",), rest="path"),
    spec("realpath", flags="-e -m -L -P -q -s -z --canonicalize-existing "
                           "--canonicalize-missing --logical --physical --quiet "
                           "--strip --no-symlinks --zero " + HELP,
         path="--relative-to --relative-base"),
    spec("dirname", flags="-z --zero " + HELP,
         note="pure string transform; operands are still reported as argv paths"),
    spec("basename", flags="-z --zero " + HELP, data="-s --suffix",
         unmodeled="-a --multiple", roles=("path", "data"), rest="data",
         note="pure string transform; operands are still reported as argv paths"),
    spec("du", flags="-a -c -h -H -k -L -l -m -P -s -S -x -0 -b -D --all --total "
                     "--human-readable --summarize --one-file-system --apparent-size "
                     "--dereference --no-dereference --null --si --si " + HELP,
         data="-d --max-depth -B --block-size -t --threshold --time --time-style",
         path="--exclude-from --files0-from", odata="--exclude --time"),
    spec("df", flags="-a -h -H -i -k -l -P -T -v --all --human-readable --inodes "
                     "--local --portability --print-type --total --si --sync "
                     "--no-sync " + HELP,
         data="-B --block-size -t --type -x --exclude-type --output", odata="--output"),
    spec("file", flags="-b -i -L -h -z -N -r -s -k -n -p -0 --brief --mime "
                       "--mime-type --mime-encoding --dereference --no-pad " + HELP,
         path="-f --files-from -m --magic-file"),
    spec("stat", flags="-L -f -t --dereference --file-system --terse " + HELP,
         data="-c --format --printf"),
    spec("tee", flags="-a -i -p --append --ignore-interrupts " + HELP,
         odata="--output-error"),
    spec("truncate", flags="-c -o --no-create --io-blocks " + HELP,
         data="-s --size", path="-r --reference"),
    spec("readlink", flags="-f -e -m -n -q -s -v -z --canonicalize "
                           "--canonicalize-existing --canonicalize-missing "
                           "--no-newline --quiet --silent --verbose --zero " + HELP),
    spec("ls", flags="-a -A -b -B -c -C -d -D -f -F -g -G -h -H -i -k -l -L -m -n -N "
                     "-o -p -q -Q -r -R -s -S -t -u -U -v -x -X -1 -Z --all "
                     "--almost-all --directory --human-readable --inode --long "
                     "--numeric-uid-gid --recursive --reverse --size --dereference "
                     "--literal --no-group --classify --escape --group-directories-first " + HELP,
         data="-w --width -T --tabsize --block-size --time-style --format --sort "
              "--indicator-style --quoting-style --hide --ignore -I",
         odata="--color --colour --time --classify --hide-control-chars --quoting-style"),
    spec("install", flags="-b -c -C -d -D -p -s -v -T --compare --directory "
                          "--preserve-timestamps --strip --verbose --no-target-directory "
                          "--backup --preserve-context " + HELP,
         path="-t --target-directory",
         data="-m --mode -o --owner -g --group -S --suffix -Z --context --strip-program",
         odata="--backup --context"),
    spec("unlink", flags=HELP),
    spec("sync", flags="-d -f --data --file-system " + HELP),
    spec("mountpoint", flags="-q -d -x --quiet " + HELP),
    spec("mktemp", flags="-d -u -q -t --directory --dry-run --quiet " + HELP,
         path="-p --tmpdir", data="--suffix", odata="--tmpdir",
         rest="dynamic",
         note="the created leaf name is not statically determined"),
    spec("sort", flags="-b -c -C -d -f -g -h -i -M -n -r -R -s -u -V -z --check "
                       "--ignore-case --numeric-sort --reverse --stable --unique "
                       "--zero-terminated --dictionary-order --general-numeric-sort "
                       "--human-numeric-sort --ignore-leading-blanks --month-sort "
                       "--random-sort --version-sort --debug " + HELP,
         path="-o --output -T --temporary-directory --files0-from",
         data="-k --key -t --field-separator -S --buffer-size --compress-program "
              "--parallel --random-source",
         odata="--check"),
    spec("uniq", flags="-c -d -D -i -u -z --count --repeated --all-repeated "
                       "--ignore-case --unique --zero-terminated " + HELP,
         data="-f --skip-fields -s --skip-chars -w --check-chars --group",
         odata="--all-repeated --group", roles=("path", "path"), rest="path"),
    spec("cut", flags="-n -s -z --complement --only-delimited --zero-terminated " + HELP,
         data="-b --bytes -c --characters -f --fields -d --delimiter "
              "--output-delimiter"),
    spec("tr", flags="-c -C -d -s -t --complement --delete --squeeze-repeats "
                     "--truncate-set1 " + HELP,
         roles=("data", "data"), rest="data",
         note="tr reads standard input only; it takes no file operand"),
)

# --- shell builtins whose complete accepted grammar carries no path ------
_register(
    spec("exit", rest="data"),
    spec("return", rest="data"),
    spec("break", rest="data"),
    spec("continue", rest="data"),
    spec("shift", rest="data"),
    spec("true", rest="data"),
    spec("false", rest="data"),
    spec(":", rest="data"),
    spec("pwd", flags="-L -P", rest="data"),
    spec("umask", flags="-p -S", rest="data"),
    spec("ulimit", flags="-H -S -a -b -c -d -e -f -i -k -l -m -n -p -q -r -s -t -u -v -x -P -R -T",
         rest="data"),
    spec("times", rest="data"),
    spec("suspend", flags="-f", rest="data"),
    # `jobs -x` substitutes job specs into a command and runs it, so it is not
    # a path-free form and must not be admitted as one.
    spec("jobs", flags="-l -n -p -r -s", unmodeled="-x", rest="data"),
    spec("bg", rest="data"),
    spec("fg", rest="data"),
    spec("disown", flags="-a -h -r", rest="data"),
    spec("wait", flags="-n -f -p", data="-p", rest="data"),
    spec("kill", flags="-l -L", data="-s -n", option_re=r"-[0-9A-Za-z]+", rest="data"),
    spec("getopts", rest="data"),
    spec("let", rest="data"),
    spec("caller", rest="data"),
    spec("type", flags="-a -f -P -p -t", rest="data"),
    spec("help", flags="-d -m -s", rest="data"),
    spec("unset", flags="-f -v -n", rest="data"),
    spec("unalias", flags="-a", rest="data"),
    spec("shopt", flags="-s -u -q -p -o", rest="data"),
    spec("set", flags="-a -b -e -E -f -h -k -m -n -p -t -u -v -x -B -C -H -P -T",
         data="-o", option_re=r"\+[a-zA-Z]+|\+o", rest="data"),
    spec("printf", data="-v", rest="data"),
    spec("echo", flags="-n -e -E", rest="data"),
    spec("id", flags="-a -g -G -n -r -u -z --group --groups --name --real --user "
                     "--zero " + HELP, rest="data"),
    spec("logname", flags=HELP, rest="data"),
    spec("whoami", flags=HELP, rest="data"),
    spec("uname", flags="-a -s -n -r -v -m -p -i -o --all --kernel-name --nodename "
                        "--kernel-release --kernel-version --machine --processor "
                        "--hardware-platform --operating-system " + HELP, rest="data"),
    spec("hostname", flags="-s -f -i -I -d -A -b " + HELP, rest="data"),
    spec("tty", flags="-s --silent --quiet " + HELP, rest="data"),
    spec("groups", flags=HELP, rest="data"),
    spec("sleep", flags=HELP, rest="data"),
    spec("seq", flags="-w --equal-width " + HELP, data="-s --separator -f --format",
         rest="data"),
    spec("date", flags="-u -R -I --utc --universal --rfc-email --rfc-2822 " + HELP,
         path="-f --file -r --reference", data="-d --date -s --set --rfc-3339 --debug",
         odata="-I --iso-8601", rest="data"),
    spec("popd", flags="-n", option_re=r"[+-][0-9]+", rest="data"),
    spec("dirs", flags="-c -l -p -v", option_re=r"[+-][0-9]+", rest="data"),
)

# --- builtins that DO carry a path or a shell string --------------------
_register(
    spec("cd", flags="-L -P -e -@", rest="path",
         note="`cd -` selects OLDPWD, which is not a preregistered constant"),
    spec("pushd", flags="-n", option_re=r"[+-][0-9]+", rest="path"),
    spec("read", flags="-r -s -e", data="-a -d -i -n -N -p -t", fd="-u", rest="data"),
    spec("mapfile", flags="-t", data="-d -n -O -s -c", fd="-u", shell="-C", rest="data"),
    spec("readarray", flags="-t", data="-d -n -O -s -c", fd="-u", shell="-C", rest="data"),
    spec("hash", flags="-l -r -t -d", path="-p", rest="data"),
    spec("history", flags="-c", path="-r -w -a -n", data="-d -p -s", rest="data"),
    spec("bind", flags="-l -p -P -s -S -v -V -X -r -u", path="-f", shell="-x",
         data="-m -q", rest="data"),
    spec("enable", flags="-a -d -n -p -s", path="-f", rest="data"),
    spec("complete", flags="-p -r -D -E -I -a -b -c -d -e -f -g -j -k -s -u -v",
         shell="-C", data="-o -A -G -W -P -S -X -F", rest="data"),
    spec("compgen", flags="-p -r -D -E -I -a -b -c -d -e -f -g -j -k -s -u -v",
         shell="-C", data="-o -A -G -W -P -S -X -F", rest="data"),
    spec("ss", flags="-n -r -a -l -o -e -m -i -p -s -4 -6 -t -u -w -x -H -O -Z -z -K "
                     "--numeric --resolve --all --listening --options --extended "
                     "--memory --processes --info --summary --tcp --udp --raw --unix "
                     "--no-header",
         path="-F --filter", data="-A --query -f --family -D --diag -N --net",
         rest="data",
         note="ss reads kernel socket tables over netlink; no argv endpoint"),
)


NO_ASSIGNMENT_EFFECT = "NO_ASSIGNMENT_EFFECT"
ASSIGNMENT_EFFECT = "ASSIGNMENT_EFFECT"
EFFECT_UNKNOWN = "EFFECT_UNKNOWN"


def parameter_assignment_effect(raw: str) -> str:
    """Classify active ${...} assignment effects without evaluating them."""
    result = NO_ASSIGNMENT_EFFECT
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(raw):
        char = raw[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and quote != "'":
            escaped = True
            index += 1
            continue
        if quote == "'":
            if char == "'":
                quote = None
            index += 1
            continue
        if char == "'":
            quote = "'"
            index += 1
            continue
        if char == '"':
            quote = None if quote == '"' else '"'
            index += 1
            continue
        if not raw.startswith("${", index):
            index += 1
            continue

        start = index
        cursor = index + 2
        depth = 1
        inner_quote: str | None = None
        inner_escaped = False
        nested = False
        while cursor < len(raw) and depth:
            current = raw[cursor]
            if inner_escaped:
                inner_escaped = False
                cursor += 1
                continue
            if current == "\\" and inner_quote != "'":
                inner_escaped = True
                cursor += 1
                continue
            if inner_quote:
                if current == inner_quote:
                    inner_quote = None
                cursor += 1
                continue
            if current in "'\"":
                inner_quote = current
                cursor += 1
                continue
            if raw.startswith("${", cursor):
                nested = True
                depth += 1
                cursor += 2
                continue
            if current == "}":
                depth -= 1
                cursor += 1
                continue
            cursor += 1
        if depth or inner_quote:
            return EFFECT_UNKNOWN
        expr = raw[start + 2:cursor - 1]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*(?::?=)", expr, re.S):
            return ASSIGNMENT_EFFECT
        if nested:
            result = EFFECT_UNKNOWN
        index = cursor
    return result


class Analyzer:
    CONTROL = {
        "if", "then", "elif", "else", "fi", "for", "while", "until", "do", "done",
        "case", "in", "esac", "select", "function",
    }
    WRAPPERS = {
        "env", "timeout", "exec", "command", "builtin", "nohup", "nice", "ionice",
        "setsid", "stdbuf", "sudo", "time", "chroot", "unbuffer",
    }
    INTERPRETERS = {
        "python", "python2", "python3", "perl", "ruby", "node", "bash", "sh",
        "dash", "zsh", "ksh", "php", "lua", "tclsh", "Rscript",
    }
    TEXT_PROGRAMS = {"awk", "gawk", "mawk", "nawk", "sed", "jq"}
    REDIRS = {
        "<", ">", ">>", "<>", ">|", "<<<", "<<", "<<-", "&>", "&>>", ">&", "<&",
    }
    SPLIT = {
        "\n", ";", ";;", ";&", ";;&", "&&", "||", "|", "|&", "&", "(", ")",
        "{", "}", "((", "))",
    }

    def __init__(
        self,
        text: str,
        env: dict[str, Value],
        rules: list[Rule] | None = None,
        depth: int = 0,
        context: AccountingRunContext | None = None,
    ) -> None:
        self.text = text
        self.env = dict(env)
        self.pinned = set(env)
        self.rules = list(rules or [])
        self.depth = depth
        self.context = context or AccountingRunContext()
        self.analyzer_id = self.context.allocate_analyzer_id()
        self.next_value_ordinal = 0
        self.uses: list[Use] = []
        self.issues: list[Issue] = []
        self.admitted_values: list[AdmittedValue] = []
        self.members: list[MemberOccurrence] = []
        self.dispositions: list[TerminalDisposition] = []
        self.accounting_faults: list[AccountingFault] = []
        self.functions: set[str] = set(
            re.findall(r"(?m)^\s*(?:function\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)\s*\{", text)
        )

    # -- recording -------------------------------------------------------
    def issue(self, line: int, kind: str, reason: str, expression: str) -> None:
        item = Issue(line, kind, reason, expression[:240])
        if item not in self.issues:
            self.issues.append(item)

    def accounting_fault(
        self,
        reason: str,
        value_id: str | None = None,
        member_id: str | None = None,
    ) -> None:
        item = AccountingFault(value_id, member_id, reason)
        if item not in self.accounting_faults:
            self.accounting_faults.append(item)

    def record_path_text(
        self,
        text: str,
        sources: frozenset[str],
        line: int,
        primitive: str,
        expression: str,
    ) -> None:
        if text == "-":
            return  # modeled: `-` is the stdin/stdout operand, not a filesystem path
        if text.startswith("/dev/tcp/") or text.startswith("/dev/udp/"):
            match = DEV_NET_RE.fullmatch(posixpath.normpath(text))
            if match is None:
                self.issue(line, KIND_ENDPOINT,
                           "bash /dev/tcp or /dev/udp redirection with unmodeled grammar",
                           expression)
                return
            proto, host, port = match.groups()
            if not host or not port:
                self.issue(line, KIND_ENDPOINT,
                           f"bash /dev/{proto} endpoint is incomplete", expression)
                return
            endpoint = normalize_network(f"{host}:{port}")
            if not endpoint.known:
                self.issue(line, KIND_ENDPOINT,
                           f"bash /dev/{proto} endpoint: {endpoint.reason}", expression)
                return
            self.uses.append(
                Use(endpoint.text or "", line, f"{primitive} /dev/{proto}",
                    expression, sources, "net")
            )
            return
        normalized = canonical_path(text, self.env)
        if not normalized.known:
            self.issue(line, KIND_PATH, normalized.reason or "unresolvable path", expression)
            return
        self.uses.append(Use(normalized.text or "", line, primitive, expression, sources, "fs"))

    def record_path(self, raw: str, line: int, primitive: str) -> None:
        value = expand_word(raw, self.env)
        if not value.known:
            self.issue(line, KIND_PATH, value.reason or "unresolvable path", raw)
            return
        self.record_path_text(value.text or "", value.sources, line, primitive, raw)

    def record_network_text(
        self,
        text: str,
        sources: frozenset[str],
        line: int,
        primitive: str,
        expression: str,
        default_port: int | None = None,
    ) -> None:
        candidate = text
        if default_port is not None and "://" not in candidate and not NETWORK_RE.fullmatch(candidate):
            host = candidate.rsplit("@", 1)[-1]
            if not host:
                self.issue(line, KIND_ENDPOINT, f"{primitive} host operand is empty", expression)
                return
            if ":" in host and not (host.startswith("[") and host.endswith("]")):
                self.issue(line, KIND_ENDPOINT,
                           f"{primitive} host operand grammar is not modeled", expression)
                return
            candidate = f"{host}:{default_port}"
        normalized = normalize_network(candidate)
        if not normalized.known:
            self.issue(line, KIND_ENDPOINT, normalized.reason or "unresolvable endpoint", expression)
            return
        self.uses.append(Use(normalized.text or "", line, primitive, expression, sources, "net"))

    def record_network(
        self, raw: str, line: int, primitive: str, default_port: int | None = None
    ) -> None:
        value = expand_word(raw, self.env)
        if not value.known:
            self.issue(line, KIND_ENDPOINT, value.reason or "unresolvable endpoint", raw)
            return
        self.record_network_text(
            value.text or "", value.sources, line, primitive, raw, default_port
        )

    def merge(self, nested: "Analyzer", line: int) -> None:
        self.uses.extend(
            dataclasses.replace(use, line=line + use.line - 1) for use in nested.uses
        )
        for item in nested.issues:
            self.issue(line + item.line - 1, item.kind, item.reason, item.expression)
        self.admitted_values.extend(
            dataclasses.replace(value, line=line + value.line - 1)
            for value in nested.admitted_values
        )
        self.members.extend(
            dataclasses.replace(member, line=line + member.line - 1)
            for member in nested.members
        )
        self.dispositions.extend(nested.dispositions)
        for fault in nested.accounting_faults:
            if fault not in self.accounting_faults:
                self.accounting_faults.append(fault)

    def analyze_shell_source(self, text: str, line: int, label: str) -> None:
        if self.depth >= MAX_NESTING:
            self.issue(line, KIND_COVERAGE,
                       f"{label}: shell nesting exceeds the modeled depth", text)
            return
        nested = Analyzer(
            text,
            self.env,
            self.rules,
            self.depth + 1,
            self.context,
        )
        nested.run()
        self.merge(nested, line)

    @staticmethod
    def _basename(command: str) -> str:
        return command.rsplit("/", 1)[-1]

    def assignment(self, token: Token) -> bool:
        match = ASSIGN_RE.fullmatch(token.text)
        if not match:
            return False
        name, rhs = match.groups()
        if name in self.pinned:
            value = expand_word(rhs, self.env)
            if not value.known or value.text != self.env[name].text:
                self.issue(token.line, KIND_COVERAGE,
                           f"script can override pinned constant {name}", token.text)
            return True
        self.env[name] = expand_word(rhs, self.env)
        return True

    def bind_assignment(
        self, token: Token, name: str, literal: str, sources: frozenset[str]
    ) -> None:
        """Bind an already-expanded NAME=VALUE, as `assignment` binds a raw one.

        The pinned-constant override check is the same in both, so a quoted
        declaration cannot silently redefine a preregistered constant either.
        """
        if name in self.pinned:
            if literal != (self.env[name].text or ""):
                self.issue(token.line, KIND_COVERAGE,
                           f"script can override pinned constant {name}", token.text)
            return
        self.env[name] = Value(literal, sources=sources)

    def analyze_declaration(self, keyword: Token, operands: list[Token]) -> None:
        """Declaration builtins, as ONE grammar with the prefix and `env` sites.

        C-4 repair (round 5): the round-4 loop gated every operand on
        `assignment(token)`, which matches ASSIGN_RE against the RAW token text.
        A quoted but perfectly ordinary declaration argument -- `export
        "LD_PRELOAD=/etc/escape.so"`, `export 'X=/safe dir/escape'` -- is a
        NAME=VALUE assignment only after expansion, so it matched nothing, fell
        past the NAME_RE arm, and disappeared with no row and no coverage
        record, while the identical `env "LD_PRELOAD=/etc/escape.so"` shape
        reached the repaired member grammar and returned rc 1. The correct
        parser existed; the declaration site simply could not reach it.

        Every operand is now expanded first and classified on the expanded word,
        so all three assignment sites -- assignment prefix, `env` wrapper,
        declaration builtin -- terminate in `record_assignment_value`. The
        unquoted arm is kept byte-identical to round 4 so the C-1 closure is
        preserved rather than re-derived, and an operand that is neither an
        option, a NAME, nor NAME=VALUE after expansion now fails closed with a
        coverage record instead of vanishing.
        """
        primitive = f"{keyword.text} assignment"
        for token in operands:
            if ASSIGN_RE.fullmatch(token.text):
                self.record_assignment_value(token, primitive)
                self.assignment(token)
                continue
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"{keyword.text} operand is not statically known: "
                           f"{value.reason}", token.text)
                continue
            rendered = value.text or ""
            if OPTION_WORD_RE.match(rendered) or rendered in {"-", "--"}:
                continue
            expanded = ASSIGN_RE.fullmatch(rendered)
            if expanded is not None:
                self.record_assignment_value(token, primitive)
                self.bind_assignment(token, expanded.group(1), expanded.group(2),
                                     value.sources)
                continue
            if NAME_RE.fullmatch(rendered):
                if rendered not in self.env:
                    self.env[rendered] = Value(
                        None, f"declared variable {rendered} has no static value"
                    )
                continue
            self.issue(token.line, KIND_COVERAGE,
                       f"{keyword.text} operand is neither an option, a NAME, nor "
                       "NAME=VALUE after expansion", token.text)

    def record_assignment_value(self, token: Token, primitive: str) -> None:
        """Admit one assignment occurrence before RHS expansion can succeed."""
        raw = token.text
        match = ASSIGN_RE.fullmatch(raw)
        if match is not None:
            raw_rhs = match.group(2)
            raw_rhs_start = match.start(2)
            value = expand_word(raw_rhs, self.env)
            trace = self._shift_trace(value.trace, raw_rhs_start, raw_rhs)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"assignment value is not statically known: {value.reason}",
                           raw)
                rendered = None
            else:
                rendered = value.text or ""
        else:
            whole = expand_word(raw, self.env)
            if not whole.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"assignment value is not statically known: {whole.reason}",
                           raw)
                return
            expanded = ASSIGN_RE.fullmatch(whole.text or "")
            if expanded is None:
                self.issue(token.line, KIND_COVERAGE,
                           "assignment word does not parse as NAME=VALUE after expansion",
                           raw)
                return
            rendered = expanded.group(2)
            raw_equal = raw.find("=")
            raw_rhs_start = raw_equal + 1 if raw_equal >= 0 else 0
            raw_rhs = raw[raw_rhs_start:]
            trace = self._slice_trace(
                whole.trace,
                expanded.start(2),
                expanded.end(2),
                raw_rhs,
            )
        self.record_assignment_members(
            rendered,
            trace,
            raw_rhs,
            raw_rhs_start,
            token.line,
            primitive,
            raw,
        )

    @staticmethod
    def _shift_trace(
        trace: ExpansionTrace | None,
        raw_offset: int,
        raw_rhs: str,
    ) -> ExpansionTrace | None:
        if trace is None:
            return None
        return ExpansionTrace(
            raw_rhs,
            trace.rendered_text,
            tuple(
                dataclasses.replace(
                    segment,
                    raw_start=segment.raw_start + raw_offset,
                    raw_end=segment.raw_end + raw_offset,
                )
                for segment in trace.segments
            ),
        )

    @staticmethod
    def _slice_trace(
        trace: ExpansionTrace | None,
        rendered_start: int,
        rendered_end: int,
        raw_rhs: str,
    ) -> ExpansionTrace | None:
        if trace is None:
            return None
        segments: list[ExpansionSegment] = []
        for segment in trace.segments:
            if segment.rendered_start == segment.rendered_end:
                if rendered_start <= segment.rendered_start <= rendered_end:
                    segments.append(
                        dataclasses.replace(
                            segment,
                            rendered_start=segment.rendered_start - rendered_start,
                            rendered_end=segment.rendered_end - rendered_start,
                        )
                    )
                continue
            left = max(rendered_start, segment.rendered_start)
            right = min(rendered_end, segment.rendered_end)
            if left >= right:
                continue
            local_left = left - segment.rendered_start
            local_right = right - segment.rendered_start
            replacements: dict[str, object] = {
                "rendered_start": left - rendered_start,
                "rendered_end": right - rendered_start,
                "rendered_text": segment.rendered_text[local_left:local_right],
            }
            if (
                segment.origin == "literal"
                and len(segment.raw_text) == len(segment.rendered_text)
            ):
                replacements.update(
                    raw_start=segment.raw_start + local_left,
                    raw_end=segment.raw_start + local_right,
                    raw_text=segment.raw_text[local_left:local_right],
                )
            segments.append(dataclasses.replace(segment, **replacements))
        rendered = trace.rendered_text[rendered_start:rendered_end]
        return ExpansionTrace(raw_rhs, rendered, tuple(segments))

    @staticmethod
    def assignment_member_kind(text: str) -> str:
        if text == "":
            return "empty"
        if URI_SCHEME_RE.match(text):
            return "net"
        if text.startswith(("/", "./", "../")):
            return "fs"
        if "/" in text and not text.startswith("-"):
            return "fs"  # ordinary relative pathname, resolved against pinned PWD
        return "bare"

    @staticmethod
    def _colon_spans(text: str) -> tuple[list[tuple[int, int]], list[int]]:
        spans: list[tuple[int, int]] = []
        separators: list[int] = []
        start = 0
        index = 0
        while index < len(text):
            if index == start:
                prefix = URI_PREFIX_RE.match(text, index)
                if prefix is not None and prefix.end() > index:
                    index = prefix.end()
                    continue
            if text[index] == ":":
                spans.append((start, index))
                separators.append(index)
                start = index + 1
                index = start
                continue
            index += 1
        spans.append((start, len(text)))
        return spans, separators

    @staticmethod
    def split_list_members(text: str) -> list[str]:
        spans, _ = Analyzer._colon_spans(text)
        return [text[start:end] for start, end in spans]

    @staticmethod
    def _trace_slices(
        trace: ExpansionTrace,
        rendered_start: int,
        rendered_end: int,
    ) -> tuple[RawSlice, ...]:
        slices: list[RawSlice] = []
        for segment in trace.segments:
            intersects = (
                segment.rendered_start < rendered_end
                and segment.rendered_end > rendered_start
            )
            zero_inside = (
                segment.rendered_start == segment.rendered_end
                and rendered_start <= segment.rendered_start <= rendered_end
            )
            if intersects or zero_inside:
                if (
                    intersects
                    and segment.origin == "literal"
                    and len(segment.raw_text) == len(segment.rendered_text)
                ):
                    left = max(rendered_start, segment.rendered_start)
                    right = min(rendered_end, segment.rendered_end)
                    local_left = left - segment.rendered_start
                    local_right = right - segment.rendered_start
                    item = RawSlice(
                        segment.raw_start + local_left,
                        segment.raw_start + local_right,
                        segment.raw_text[local_left:local_right],
                        segment.origin,
                    )
                else:
                    item = RawSlice(
                        segment.raw_start,
                        segment.raw_end,
                        segment.raw_text,
                        segment.origin,
                    )
                if not slices or slices[-1] != item:
                    slices.append(item)
        return tuple(slices)

    @staticmethod
    def _trace_sources(
        trace: ExpansionTrace,
        rendered_start: int,
        rendered_end: int,
    ) -> frozenset[str]:
        return frozenset(
            source
            for segment in trace.segments
            if segment.rendered_start < rendered_end
            and segment.rendered_end > rendered_start
            for source in segment.sources
        )

    @staticmethod
    def _raw_boundary(trace: ExpansionTrace, rendered_offset: int) -> int:
        for segment in trace.segments:
            if segment.rendered_start == rendered_offset:
                return segment.raw_start
            if segment.rendered_end == rendered_offset:
                return segment.raw_end
            if segment.rendered_start < rendered_offset < segment.rendered_end:
                return segment.raw_start
        return trace.segments[-1].raw_end if trace.segments else 0

    def _make_member(
        self,
        value_id: str,
        reading: str,
        ordinal: int,
        rendered: str,
        trace: ExpansionTrace | None,
        rendered_start: int,
        rendered_end: int,
        raw_rhs: str,
        raw_rhs_start: int,
        line: int,
        primitive: str,
        expression: str,
        semantic_pwd: bool = False,
    ) -> MemberOccurrence:
        member_id = f"{value_id}.{reading}.M{ordinal:04d}"
        if trace is None:
            raw_slices = (
                RawSlice(
                    raw_rhs_start,
                    raw_rhs_start + len(raw_rhs),
                    raw_rhs,
                    "literal",
                ),
            )
            sources = frozenset()
        elif semantic_pwd:
            boundary = self._raw_boundary(trace, rendered_start)
            raw_slices = (RawSlice(boundary, boundary, "", "semantic_pwd_substitution"),)
            pwd = self.env.get("PWD")
            sources = (
                frozenset({"PWD"})
                if "PWD" in self.pinned and pwd is not None and pwd.known
                else frozenset()
            )
        else:
            raw_slices = self._trace_slices(trace, rendered_start, rendered_end)
            sources = self._trace_sources(trace, rendered_start, rendered_end)
        return MemberOccurrence(
            member_id,
            value_id,
            reading,
            ordinal,
            rendered_start,
            rendered_end,
            raw_slices,
            rendered[rendered_start:rendered_end] if trace is not None else raw_rhs,
            sources,
            line,
            primitive,
            expression,
        )

    def _matching_rules(self, candidate: str, member: MemberOccurrence, domain: str) -> list[str]:
        return [
            rule.render()
            for rule in self.rules
            if rule.matches(candidate, member.primitive, domain)
        ]

    def _record_member_candidate(
        self,
        member: MemberOccurrence,
        candidate: str,
        domain: str,
    ) -> None:
        self.uses.append(
            Use(
                candidate,
                member.line,
                member.primitive,
                member.expression,
                member.sources,
                domain,
                member.member_id,
            )
        )

    def _classify_member(
        self,
        value: AdmittedValue,
        member: MemberOccurrence,
    ) -> TerminalDisposition:
        active_children = sum(
            count for reading, count in value.expected_counts if reading != "whole"
        ) > 0
        if value.rendered_text is None:
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.UNRESOLVED_FAIL_CLOSED,
                "opaque_assignment_expansion", None, None, None, member.sources,
            )

        kind = self.assignment_member_kind(member.text)
        candidate_domain: str | None = None
        candidate_value: str | None = None
        if kind == "net":
            normalized = normalize_network(member.text)
            candidate_domain = "net"
        elif kind == "fs" or (kind == "empty" and member.reading == "colon"):
            normalized = canonical_path("." if kind == "empty" else member.text, self.env)
            candidate_domain = "fs"
        else:
            normalized = Value(None, "no path or endpoint candidate")

        if member.reading in {"words", "word-colon"}:
            if normalized.known and candidate_domain is not None:
                candidate_value = normalized.text or ""
                self._record_member_candidate(member, candidate_value, candidate_domain)
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.UNRESOLVED_FAIL_CLOSED,
                "consumer_word_semantics_unmodeled", None,
                candidate_domain if normalized.known else None,
                candidate_value, member.sources,
            )

        if kind == "empty" and member.reading == "colon" and not normalized.known:
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.UNRESOLVED_FAIL_CLOSED,
                "member_pwd_unavailable", None, None, None, member.sources,
            )

        if candidate_domain is not None:
            if not normalized.known:
                return TerminalDisposition(
                    member.member_id, value.value_id,
                    DispositionKind.UNRESOLVED_FAIL_CLOSED,
                    "member_normalization_failed", None, None, None, member.sources,
                )
            candidate_value = normalized.text or ""
            self._record_member_candidate(member, candidate_value, candidate_domain)
            matching = self._matching_rules(candidate_value, member, candidate_domain)
            if not matching:
                return TerminalDisposition(
                    member.member_id, value.value_id,
                    DispositionKind.FORBIDDEN_WITH_REASON,
                    "member_outside_allowlist", None,
                    candidate_domain, candidate_value, member.sources,
                )
            required_sources = (
                member.sources == frozenset({"PWD"})
                if kind == "empty" and member.reading == "colon"
                else bool(member.sources)
            )
            if not required_sources:
                return TerminalDisposition(
                    member.member_id, value.value_id,
                    DispositionKind.UNRESOLVED_FAIL_CLOSED,
                    "member_exact_provenance_missing", matching[0],
                    candidate_domain, candidate_value, member.sources,
                )
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.ALLOWED_WITH_REASON,
                "member_allowlisted", matching[0],
                candidate_domain, candidate_value, member.sources,
            )

        if member.reading == "whole" and active_children:
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.ALLOWED_WITH_REASON,
                "whole_container_decomposed", None, None, None, member.sources,
            )
        if member.reading == "whole" and member.text == "":
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.ALLOWED_WITH_REASON,
                "empty_scalar_no_lexical_sink", None, None, None, member.sources,
            )
        if member.reading == "whole" and OPTION_WORD_RE.match(member.text):
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.UNRESOLVED_FAIL_CLOSED,
                "member_option_semantics_unmodeled", None, None, None, member.sources,
            )
        if member.reading == "whole":
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.ALLOWED_WITH_REASON,
                "whole_scalar_no_lexical_sink", None, None, None, member.sources,
            )
        if member.reading == "colon":
            return TerminalDisposition(
                member.member_id, value.value_id,
                DispositionKind.UNRESOLVED_FAIL_CLOSED,
                "member_consumer_search_unmodeled", None, None, None, member.sources,
            )
        return TerminalDisposition(
            member.member_id, value.value_id,
            DispositionKind.UNRESOLVED_FAIL_CLOSED,
            "member_classifier_no_terminal_rule", None, None, None, member.sources,
        )

    def record_assignment_members(
        self,
        rendered: str | None,
        trace: ExpansionTrace | None,
        raw_rhs: str,
        raw_rhs_start: int,
        line: int,
        primitive: str,
        expression: str,
    ) -> None:
        value_id = f"{self.analyzer_id}.V{self.next_value_ordinal:04d}"
        self.next_value_ordinal += 1
        text = rendered or ""
        members: list[MemberOccurrence] = []

        members.append(
            self._make_member(
                value_id, "whole", 0, text, trace, 0, len(text), raw_rhs,
                raw_rhs_start, line, primitive, expression,
            )
        )
        colon_spans, colon_separators = self._colon_spans(text) if rendered is not None else ([], [])
        if colon_separators:
            for ordinal, (start, end) in enumerate(colon_spans):
                members.append(
                    self._make_member(
                        value_id, "colon", ordinal, text, trace, start, end,
                        raw_rhs, raw_rhs_start, line, primitive, expression,
                        semantic_pwd=start == end,
                    )
                )

        word_matches = list(re.finditer(r"\S+", text)) if rendered is not None else []
        words_active = len(word_matches) >= 2 and re.search(r"\s", text) is not None
        if words_active:
            for ordinal, match in enumerate(word_matches):
                members.append(
                    self._make_member(
                        value_id, "words", ordinal, text, trace,
                        match.start(), match.end(), raw_rhs, raw_rhs_start,
                        line, primitive, expression,
                    )
                )

        word_colon_spans: list[tuple[int, int]] = []
        if words_active:
            for match in word_matches:
                local_spans, local_separators = self._colon_spans(match.group(0))
                if not local_separators:
                    continue
                word_colon_spans.extend(
                    (match.start() + start, match.start() + end)
                    for start, end in local_spans
                )
        for ordinal, (start, end) in enumerate(word_colon_spans):
            members.append(
                self._make_member(
                    value_id, "word-colon", ordinal, text, trace, start, end,
                    raw_rhs, raw_rhs_start, line, primitive, expression,
                )
            )

        expected_counts = (
            ("whole", 1),
            ("colon", len(colon_spans) if colon_separators else 0),
            ("words", len(word_matches) if words_active else 0),
            ("word-colon", len(word_colon_spans)),
        )
        value = AdmittedValue(
            value_id,
            line,
            primitive,
            expression,
            raw_rhs,
            rendered,
            trace,
            expected_counts,
            tuple(member.member_id for member in members),
        )
        dispositions = [self._classify_member(value, member) for member in members]
        self.admitted_values.append(value)
        self.members.extend(members)
        self.dispositions.extend(dispositions)
        self._validate_value_accounting(value, members, dispositions)

    @staticmethod
    def _disposition_name(disposition: DispositionKind | str) -> str:
        return disposition.value if isinstance(disposition, DispositionKind) else str(disposition)

    def _validate_reason_reading(
        self,
        value: AdmittedValue,
        member: MemberOccurrence,
        disposition: TerminalDisposition,
    ) -> None:
        name = self._disposition_name(disposition.disposition)
        active_children = sum(
            count for reading, count in value.expected_counts if reading != "whole"
        ) > 0
        member_kind = self.assignment_member_kind(member.text)

        if member.reading in {"words", "word-colon"}:
            if not (
                name == DispositionKind.UNRESOLVED_FAIL_CLOSED.value
                and disposition.reason == "consumer_word_semantics_unmodeled"
            ):
                self.accounting_fault(
                    "reason_reading_consistency_failed",
                    value.value_id,
                    member.member_id,
                )
            return

        scalar_reasons = {
            "whole_scalar_no_lexical_sink",
            "empty_scalar_no_lexical_sink",
        }
        if disposition.reason in scalar_reasons:
            scalar_shape = (
                member_kind == "bare"
                and OPTION_WORD_RE.match(member.text) is None
            )
            scalar_text = (
                member.text == ""
                if disposition.reason == "empty_scalar_no_lexical_sink"
                else member.text != "" and scalar_shape
            )
            if not (
                name == DispositionKind.ALLOWED_WITH_REASON.value
                and member.reading == "whole"
                and not active_children
                and scalar_text
                and disposition.candidate_domain is None
                and disposition.candidate_value is None
                and disposition.rule is None
            ):
                self.accounting_fault(
                    "reason_reading_consistency_failed",
                    value.value_id,
                    member.member_id,
                )
            return

        if disposition.reason == "whole_container_decomposed":
            if not (
                name == DispositionKind.ALLOWED_WITH_REASON.value
                and member.reading == "whole"
                and active_children
                and member_kind == "bare"
                and disposition.candidate_domain is None
                and disposition.candidate_value is None
                and disposition.rule is None
            ):
                self.accounting_fault(
                    "reason_reading_consistency_failed",
                    value.value_id,
                    member.member_id,
                )
            return

        if disposition.reason == "member_consumer_search_unmodeled":
            if not (
                name == DispositionKind.UNRESOLVED_FAIL_CLOSED.value
                and member.reading == "colon"
                and member_kind == "bare"
                and member.text != ""
            ):
                self.accounting_fault(
                    "reason_reading_consistency_failed",
                    value.value_id,
                    member.member_id,
                )
            return

        if disposition.reason == "member_allowlisted":
            expected = (
                normalize_network(member.text)
                if disposition.candidate_domain == "net"
                else canonical_path(
                    "." if member.reading == "colon" and member_kind == "empty"
                    else member.text,
                    self.env,
                )
                if disposition.candidate_domain == "fs"
                else Value(None, "candidate domain missing")
            )
            matching = (
                self._matching_rules(
                    disposition.candidate_value,
                    member,
                    disposition.candidate_domain,
                )
                if disposition.candidate_value is not None
                and disposition.candidate_domain in {"fs", "net"}
                else []
            )
            exact_sources = (
                member.sources == frozenset({"PWD"})
                if member.reading == "colon" and member_kind == "empty"
                else bool(member.sources)
            )
            if not (
                name == DispositionKind.ALLOWED_WITH_REASON.value
                and disposition.rule is not None
                and disposition.rule in matching
                and expected.known
                and expected.text == disposition.candidate_value
                and exact_sources
                and disposition.sources == member.sources
            ):
                self.accounting_fault(
                    "reason_reading_consistency_failed",
                    value.value_id,
                    member.member_id,
                )
            return

        if disposition.reason == "member_outside_allowlist":
            expected = (
                normalize_network(member.text)
                if disposition.candidate_domain == "net"
                else canonical_path(
                    "." if member.reading == "colon" and member_kind == "empty"
                    else member.text,
                    self.env,
                )
                if disposition.candidate_domain == "fs"
                else Value(None, "candidate domain missing")
            )
            matching = (
                self._matching_rules(
                    disposition.candidate_value,
                    member,
                    disposition.candidate_domain,
                )
                if disposition.candidate_value is not None
                and disposition.candidate_domain in {"fs", "net"}
                else []
            )
            if not (
                name == DispositionKind.FORBIDDEN_WITH_REASON.value
                and disposition.candidate_value is not None
                and disposition.candidate_domain in {"fs", "net"}
                and disposition.rule is None
                and expected.known
                and expected.text == disposition.candidate_value
                and not matching
                and disposition.sources == member.sources
            ):
                self.accounting_fault(
                    "reason_reading_consistency_failed",
                    value.value_id,
                    member.member_id,
                )
            return

        unresolved_reasons = {
            "opaque_assignment_expansion",
            "member_pwd_unavailable",
            "member_normalization_failed",
            "member_exact_provenance_missing",
            "member_option_semantics_unmodeled",
            "member_classifier_no_terminal_rule",
        }
        if disposition.reason in unresolved_reasons:
            valid = name == DispositionKind.UNRESOLVED_FAIL_CLOSED.value
            if disposition.reason == "opaque_assignment_expansion":
                valid &= value.rendered_text is None and member.reading == "whole"
            elif disposition.reason == "member_pwd_unavailable":
                valid &= member.reading == "colon" and member_kind == "empty"
            elif disposition.reason == "member_exact_provenance_missing":
                valid &= (
                    disposition.candidate_value is not None
                    and disposition.candidate_domain in {"fs", "net"}
                    and disposition.rule is not None
                    and not member.sources
                )
            elif disposition.reason == "member_option_semantics_unmodeled":
                valid &= member.reading == "whole" and OPTION_WORD_RE.match(member.text) is not None
            if not valid:
                self.accounting_fault(
                    "reason_reading_consistency_failed",
                    value.value_id,
                    member.member_id,
                )
            return

        self.accounting_fault(
            "reason_reading_consistency_failed",
            value.value_id,
            member.member_id,
        )

    def _validate_value_accounting(
        self,
        value: AdmittedValue,
        members: list[MemberOccurrence],
        dispositions: list[TerminalDisposition],
    ) -> None:
        member_ids = [member.member_id for member in members]
        disposition_ids = [item.member_id for item in dispositions]
        if not member_ids:
            self.accounting_fault("member_set_empty", value.value_id)
        if Counter(value.member_ids) != Counter(member_ids):
            self.accounting_fault("value_member_ledger_mismatch", value.value_id)
        if Counter(member_ids) != Counter(disposition_ids):
            self.accounting_fault("member_disposition_counter_mismatch", value.value_id)
        disposition_counter = Counter(disposition_ids)
        for member_id in member_ids:
            if disposition_counter[member_id] != 1:
                self.accounting_fault(
                    "member_disposition_cardinality_failed", value.value_id, member_id
                )
        for disposition in dispositions:
            if disposition.member_id not in member_ids:
                self.accounting_fault(
                    "disposition_references_unknown_member",
                    value.value_id,
                    disposition.member_id,
                )
            if not isinstance(disposition.disposition, DispositionKind):
                self.accounting_fault(
                    "disposition_enum_not_closed",
                    value.value_id,
                    disposition.member_id,
                )

        actual_counts = Counter(member.reading for member in members)
        for reading, expected in value.expected_counts:
            if actual_counts[reading] != expected:
                self.accounting_fault(
                    f"reading_cardinality_mismatch_{reading.replace('-', '_')}",
                    value.value_id,
                )

        if value.rendered_text is None:
            if value.trace is not None:
                self.accounting_fault("opaque_trace_present", value.value_id)
        elif value.trace is None:
            self.accounting_fault("expansion_trace_missing", value.value_id)
        else:
            cursor = 0
            reconstructed: list[str] = []
            for segment in value.trace.segments:
                if (
                    segment.rendered_start < 0
                    or segment.rendered_end < segment.rendered_start
                    or segment.raw_start < 0
                    or segment.raw_end < segment.raw_start
                    or segment.raw_end > len(value.expression)
                    or segment.raw_text
                    != value.expression[segment.raw_start:segment.raw_end]
                    or segment.rendered_text
                    != value.rendered_text[segment.rendered_start:segment.rendered_end]
                ):
                    self.accounting_fault("trace_range_or_substring_failed", value.value_id)
                    break
                if segment.rendered_start != cursor:
                    self.accounting_fault("trace_gap_or_overlap", value.value_id)
                    break
                reconstructed.append(segment.rendered_text)
                cursor = segment.rendered_end
            if cursor != len(value.rendered_text) or "".join(reconstructed) != value.rendered_text:
                self.accounting_fault("trace_reconstruction_failed", value.value_id)

        disposition_by_member = {
            item.member_id: item
            for item in dispositions
            if disposition_counter[item.member_id] == 1
        }
        for member in members:
            if member.value_id != value.value_id:
                self.accounting_fault(
                    "member_value_identity_mismatch", value.value_id, member.member_id
                )
            for raw_slice in member.raw_slices:
                if (
                    raw_slice.raw_start < 0
                    or raw_slice.raw_end < raw_slice.raw_start
                    or raw_slice.raw_end > len(value.expression)
                    or raw_slice.raw_text
                    != value.expression[raw_slice.raw_start:raw_slice.raw_end]
                ):
                    self.accounting_fault(
                        "member_raw_slice_failed", value.value_id, member.member_id
                    )
            if value.rendered_text is not None:
                if not (
                    0 <= member.rendered_start <= member.rendered_end <= len(value.rendered_text)
                    and member.text
                    == value.rendered_text[member.rendered_start:member.rendered_end]
                ):
                    self.accounting_fault(
                        "member_rendered_span_failed", value.value_id, member.member_id
                    )
                if value.trace is not None:
                    expected_slices = (
                        (RawSlice(
                            self._raw_boundary(value.trace, member.rendered_start),
                            self._raw_boundary(value.trace, member.rendered_start),
                            "",
                            "semantic_pwd_substitution",
                        ),)
                        if member.reading == "colon" and member.text == ""
                        else self._trace_slices(
                            value.trace, member.rendered_start, member.rendered_end
                        )
                    )
                    if member.raw_slices != expected_slices:
                        self.accounting_fault(
                            "member_raw_slice_intersection_mismatch",
                            value.value_id,
                            member.member_id,
                        )
                    expected_sources = (
                        frozenset({"PWD"})
                        if member.reading == "colon" and member.text == ""
                        and "PWD" in self.pinned
                        and self.env.get("PWD") is not None
                        and self.env["PWD"].known
                        else self._trace_sources(
                            value.trace, member.rendered_start, member.rendered_end
                        )
                    )
                    if member.sources != expected_sources:
                        self.accounting_fault(
                            "member_provenance_mismatch", value.value_id, member.member_id
                        )
            disposition = disposition_by_member.get(member.member_id)
            if disposition is not None:
                if disposition.value_id != value.value_id:
                    self.accounting_fault(
                        "disposition_value_identity_mismatch",
                        value.value_id,
                        member.member_id,
                    )
                self._validate_reason_reading(value, member, disposition)

    def validate_accounting(self) -> None:
        values_by_id: dict[str, list[AdmittedValue]] = {}
        for value in self.admitted_values:
            values_by_id.setdefault(value.value_id, []).append(value)
        for value_id, values in values_by_id.items():
            if len(values) != 1:
                self.accounting_fault("value_id_not_globally_unique", value_id)

        members_by_value: dict[str, list[MemberOccurrence]] = {}
        for member in self.members:
            members_by_value.setdefault(member.value_id, []).append(member)
        dispositions_by_value: dict[str, list[TerminalDisposition]] = {}
        for disposition in self.dispositions:
            dispositions_by_value.setdefault(disposition.value_id, []).append(disposition)
        for value in self.admitted_values:
            self._validate_value_accounting(
                value,
                members_by_value.get(value.value_id, []),
                dispositions_by_value.get(value.value_id, []),
            )

        member_counter = Counter(member.member_id for member in self.members)
        disposition_counter = Counter(item.member_id for item in self.dispositions)
        for member_id, count in member_counter.items():
            if count != 1:
                self.accounting_fault("member_id_not_globally_unique", member_id=member_id)
        if member_counter != disposition_counter:
            self.accounting_fault("global_member_disposition_counter_mismatch")
        known_member_ids = set(member_counter)
        member_values = {member.member_id: member.value_id for member in self.members}
        for disposition in self.dispositions:
            if disposition.member_id not in known_member_ids:
                self.accounting_fault(
                    "global_disposition_references_unknown_member",
                    disposition.value_id,
                    disposition.member_id,
                )
            elif member_values.get(disposition.member_id) != disposition.value_id:
                self.accounting_fault(
                    "global_disposition_value_identity_mismatch",
                    disposition.value_id,
                    disposition.member_id,
                )

    # -- generic argv grammar --------------------------------------------
    def consume_value(
        self,
        command: str,
        role: str,
        text: str,
        sources: frozenset[str],
        line: int,
        expression: str,
    ) -> None:
        if role == "path":
            self.record_path_text(text, sources, line, command, expression)
        elif role == "net":
            self.record_network_text(text, sources, line, command, expression)
        elif role == "shell":
            self.analyze_shell_source(text, line, f"{command} option")
        elif role == "fd":
            if not re.fullmatch(r"[0-9]+", text):
                self.issue(line, KIND_COVERAGE,
                           f"{command} file-descriptor operand is not a static number",
                           expression)
        elif role == "form":
            self.record_form_value(command, text, sources, line, expression)
        elif role == "dynamic":
            self.issue(line, KIND_PATH,
                       f"{command} names an object that is not statically determined",
                       expression)

    def consume_token_value(self, command: str, role: str, token: Token) -> None:
        if role == "data":
            return
        value = expand_word(token.text, self.env)
        if not value.known:
            kind = KIND_ENDPOINT if role == "net" else (
                KIND_PATH if role in ("path", "dynamic") else KIND_COVERAGE
            )
            self.issue(token.line, kind,
                       f"{command} option value is not statically known: {value.reason}",
                       token.text)
            return
        self.consume_value(command, role, value.text or "", value.sources,
                           token.line, token.text)

    def scan_args(
        self, command: str, spec_item: Spec, args: list[Token]
    ) -> list[tuple[Token, str, frozenset[str]]]:
        positionals: list[tuple[Token, str, frozenset[str]]] = []
        end_of_options = False
        index = 0
        while index < len(args):
            token = args[index]
            value = expand_word(token.text, self.env)
            if not value.known:
                effect = parameter_assignment_effect(token.text)
                if effect == ASSIGNMENT_EFFECT:
                    self.issue(
                        token.line,
                        KIND_COVERAGE,
                        "assignment_parameter_expansion_not_modeled",
                        token.text,
                    )
                elif effect == EFFECT_UNKNOWN:
                    self.issue(
                        token.line,
                        KIND_COVERAGE,
                        "parameter_expansion_effect_ambiguous",
                        token.text,
                    )
                elif not spec_item.path_free:
                    self.issue(token.line, spec_item.unresolved_kind,
                               f"{command} argument is not statically known: {value.reason}",
                               token.text)
                index += 1
                continue
            rendered = value.text or ""
            if end_of_options or not rendered.startswith("-") or rendered == "-":
                positionals.append((token, rendered, value.sources))
                index += 1
                continue
            if rendered == "--":
                end_of_options = True
                index += 1
                continue
            whole = spec_item.role(rendered)
            if whole is not None:
                index += self._apply_option(
                    command, spec_item, rendered, whole, token, args, index, None
                )
                continue
            if rendered.startswith("--"):
                name, sep, inline = rendered.partition("=")
                role = spec_item.role(name)
                if role is None:
                    self.issue(token.line, KIND_COVERAGE,
                               f"{command} has no modeled grammar for option {name}",
                               token.text)
                    index += 1
                    continue
                index += self._apply_option(
                    command, spec_item, name, role, token, args, index,
                    inline if sep else None, sources=value.sources
                )
                continue
            index += self._apply_cluster(command, spec_item, rendered, token, args, index,
                                         value.sources)
        return positionals

    def _apply_option(
        self,
        command: str,
        spec_item: Spec,
        name: str,
        role: str,
        token: Token,
        args: list[Token],
        index: int,
        inline: str | None,
        sources: frozenset[str] = frozenset(),
    ) -> int:
        if role == "unmodeled":
            self.issue(token.line, KIND_COVERAGE,
                       f"{command} option {name} changes the operand grammar in a way "
                       "this tool does not model", token.text)
            return 1
        if role == "flag":
            if inline is not None:
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} option {name} is modeled as a flag but was given "
                           "a value", token.text)
            return 1
        if role == "odata":
            if inline is not None:
                self.consume_value(command, "data", inline, sources, token.line, token.text)
            return 1
        if inline is not None:
            self.consume_value(command, role, inline, sources, token.line, token.text)
            return 1
        if index + 1 >= len(args):
            self.issue(token.line, KIND_COVERAGE,
                       f"{command} option {name} has no value operand", token.text)
            return 1
        self.consume_token_value(command, role, args[index + 1])
        return 2

    def _apply_cluster(
        self,
        command: str,
        spec_item: Spec,
        rendered: str,
        token: Token,
        args: list[Token],
        index: int,
        sources: frozenset[str],
    ) -> int:
        position = 1
        while position < len(rendered):
            option = "-" + rendered[position]
            role = spec_item.role(option)
            if role is None:
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} has no modeled grammar for option {option}",
                           token.text)
                return 1
            if role == "unmodeled":
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} option {option} changes the operand grammar in a "
                           "way this tool does not model", token.text)
                return 1
            if role == "flag":
                position += 1
                continue
            remainder = rendered[position + 1:]
            if role == "odata":
                return 1
            if remainder:
                self.consume_value(command, role, remainder, sources, token.line, token.text)
                return 1
            if index + 1 >= len(args):
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} option {option} has no value operand", token.text)
                return 1
            self.consume_token_value(command, role, args[index + 1])
            return 2
        return 1

    def dispatch_positionals(
        self,
        command: str,
        spec_item: Spec,
        positionals: list[tuple[Token, str, frozenset[str]]],
    ) -> None:
        for order, (token, rendered, sources) in enumerate(positionals):
            role = spec_item.positional_role(order)
            if role == "data":
                continue
            if role == "path":
                self.record_path_text(rendered, sources, token.line, command, token.text)
            elif role == "net":
                self.record_network_text(rendered, sources, token.line, command, token.text)
            elif role == "shell":
                self.analyze_shell_source(rendered, token.line, command)
            elif role == "dynamic":
                self.issue(token.line, KIND_PATH,
                           f"{command} operand names an object that is not statically "
                           "determined", token.text)
            else:
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} operand role {role} is not modeled", token.text)

    # -- test ------------------------------------------------------------
    PATH_UNARY = {
        "-a", "-b", "-c", "-d", "-e", "-f", "-g", "-h", "-k", "-L", "-O", "-G",
        "-N", "-p", "-r", "-s", "-S", "-u", "-w", "-x",
    }

    def analyze_test(self, tokens: list[Token]) -> None:
        for index, token in enumerate(tokens[:-1]):
            value = expand_word(token.text, self.env)
            if value.known and value.text in self.PATH_UNARY:
                self.record_path(tokens[index + 1].text, tokens[index + 1].line, "test")
        for index, token in enumerate(tokens):
            value = expand_word(token.text, self.env)
            if value.known and value.text in {"-nt", "-ot", "-ef"} and 0 < index < len(tokens) - 1:
                self.record_path(tokens[index - 1].text, tokens[index - 1].line, "test")
                self.record_path(tokens[index + 1].text, tokens[index + 1].line, "test")

    # -- wrappers ---------------------------------------------------------
    WRAPPER_SPECS: dict[str, Spec] = {
        "timeout": spec("timeout", flags="-f --foreground -v --verbose --preserve-status",
                        data="-k --kill-after -s --signal", roles=("data",), rest="data"),
        "exec": spec("exec", flags="-c -l", data="-a", rest="data"),
        "command": spec("command", flags="-p -v -V", rest="data"),
        "builtin": spec("builtin", rest="data"),
        "nohup": spec("nohup", rest="data"),
        "nice": spec("nice", data="-n --adjustment", option_re=r"-[0-9]+", rest="data"),
        "ionice": spec("ionice", flags="-t", data="-c -n -p", rest="data"),
        "setsid": spec("setsid", flags="-c -f -w", rest="data"),
        "stdbuf": spec("stdbuf", data="-i -o -e --input --output --error", rest="data"),
        "time": spec("time", flags="-p", rest="data"),
        "chroot": spec("chroot", flags="--skip-chdir", data="--userspec --groups",
                       roles=("path",), rest="data"),
    }

    def analyze_wrapped(self, command: str, args: list[Token], line: int) -> None:
        if command == "env":
            index = 0
            while index < len(args):
                value = expand_word(args[index].text, self.env)
                if not value.known:
                    self.issue(args[index].line, KIND_COVERAGE,
                               f"env argument is not statically known: {value.reason}",
                               args[index].text)
                    return
                rendered = value.text or ""
                if rendered == "--":
                    index += 1
                    break
                if rendered in {"-i", "--ignore-environment", "-0", "--null", "-v",
                                "--debug", "--"}:
                    index += 1
                    continue
                if rendered.startswith("-"):
                    if rendered in {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"}:
                        if index + 1 >= len(args):
                            self.issue(args[index].line, KIND_COVERAGE,
                                       f"env option {rendered} has no value operand",
                                       args[index].text)
                            return
                        if rendered in {"-C", "--chdir"}:
                            self.record_path(args[index + 1].text, args[index + 1].line,
                                             "env --chdir")
                        elif rendered in {"-S", "--split-string"}:
                            self.issue(args[index].line, KIND_COVERAGE,
                                       "env --split-string re-parses its operand as a "
                                       "command string; that grammar is not modeled",
                                       args[index].text)
                            return
                        index += 2
                        continue
                    name, sep, _ = rendered.partition("=")
                    if sep and name in {"-u", "--unset", "-C", "--chdir"}:
                        if name in {"-C", "--chdir"}:
                            self.consume_value("env --chdir", "path",
                                               rendered.split("=", 1)[1], value.sources,
                                               args[index].line, args[index].text)
                        index += 1
                        continue
                    self.issue(args[index].line, KIND_COVERAGE,
                               f"env has no modeled grammar for option {name}",
                               args[index].text)
                    return
                if ASSIGN_RE.fullmatch(rendered):
                    self.record_assignment_value(args[index], "env assignment")
                    index += 1
                    continue
                break
            if index >= len(args):
                self.issue(line, KIND_COVERAGE,
                           "env wrapper has no statically visible command", "env")
                return
            self.analyze_command(args[index:])
            return
        if command == "sudo":
            self.issue(line, KIND_COVERAGE,
                       "sudo changes the privilege domain of every operand below it; "
                       "that transition is not modeled", "sudo")
            operands = [
                token for token in args
                if not (expand_word(token.text, self.env).text or "").startswith("-")
            ]
            if operands:
                self.analyze_command(operands)
            return
        spec_item = self.WRAPPER_SPECS[command]
        if command == "command":
            rendered = [expand_word(token.text, self.env) for token in args]
            if any(value.known and value.text in {"-v", "-V"} for value in rendered):
                return
        start = self.scan_prefix(command, spec_item, args)
        if start is None:
            return
        if command == "timeout":
            start += 1  # the first operand is the duration, not the command
        if command == "chroot":
            if start >= len(args):
                self.issue(line, KIND_COVERAGE, "chroot has no new-root operand", command)
                return
            self.record_path(args[start].text, args[start].line, "chroot")
            start += 1
        if start >= len(args):
            if command == "exec":
                return  # `exec >file` is a pure redirection, already recorded
            self.issue(line, KIND_COVERAGE,
                       f"{command} wrapper command is not statically visible", command)
            return
        self.analyze_command(args[start:])

    def scan_prefix(
        self, command: str, spec_item: Spec, args: list[Token]
    ) -> int | None:
        """Consume a wrapper's own options and return the first operand index.

        Option scanning must stop at the wrapped command: options after it
        belong to that command's grammar, not to the wrapper's.
        """
        index = 0
        while index < len(args):
            token = args[index]
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} argument is not statically known: {value.reason}",
                           token.text)
                return None
            rendered = value.text or ""
            if rendered == "--":
                return index + 1
            if not rendered.startswith("-") or rendered == "-":
                return index
            whole = spec_item.role(rendered)
            if whole is not None:
                index += self._apply_option(
                    command, spec_item, rendered, whole, token, args, index, None
                )
                continue
            if rendered.startswith("--"):
                name, sep, inline = rendered.partition("=")
                role = spec_item.role(name)
                if role is None:
                    self.issue(token.line, KIND_COVERAGE,
                               f"{command} has no modeled grammar for option {name}",
                               token.text)
                    return None
                index += self._apply_option(
                    command, spec_item, name, role, token, args, index,
                    inline if sep else None, sources=value.sources
                )
                continue
            index += self._apply_cluster(command, spec_item, rendered, token, args,
                                         index, value.sources)
        return index

    # -- find -------------------------------------------------------------
    FIND_GLOBAL = {"-H", "-L", "-P", "-D", "-O0", "-O1", "-O2", "-O3"}
    FIND_FLAGS = {
        "-print", "-print0", "-ls", "-prune", "-quit", "-depth", "-xdev", "-mount",
        "-nouser", "-nogroup", "-empty", "-readable", "-writable", "-executable",
        "-delete", "-follow", "-true", "-false", "-daystart", "-ignore_readdir_race",
        "-noignore_readdir_race", "-noleaf", "-a", "-o", "-and", "-or", "-not",
    }
    FIND_DATA = {
        "-name", "-iname", "-type", "-xtype", "-maxdepth", "-mindepth", "-perm",
        "-user", "-group", "-uid", "-gid", "-size", "-mtime", "-mmin", "-ctime",
        "-cmin", "-atime", "-amin", "-printf", "-regex", "-iregex", "-lname",
        "-ilname", "-links", "-inum", "-path", "-ipath", "-wholename", "-iwholename",
        "-regextype", "-used", "-fstype", "-context",
    }
    FIND_PATH = {
        "-newer", "-anewer", "-cnewer", "-samefile", "-fprint", "-fprint0", "-fls",
        "-files0-from",
    }
    FIND_EXEC = {"-exec", "-execdir", "-ok", "-okdir"}

    def analyze_find(self, args: list[Token], line: int) -> None:
        index = 0
        while index < len(args):
            value = expand_word(args[index].text, self.env)
            if not value.known:
                break
            rendered = value.text or ""
            if rendered in {"-H", "-L", "-P"} or re.fullmatch(r"-O[0-9]?", rendered):
                index += 1
                continue
            if rendered == "-D":
                index += 2
                continue
            break
        while index < len(args):
            value = expand_word(args[index].text, self.env)
            if not value.known:
                self.issue(args[index].line, KIND_PATH,
                           f"find search root is not statically known: {value.reason}",
                           args[index].text)
                index += 1
                continue
            rendered = value.text or ""
            if rendered.startswith("-") or rendered in {"(", ")", "!", ","}:
                break
            self.record_path_text(rendered, value.sources, args[index].line, "find",
                                  args[index].text)
            index += 1
        while index < len(args):
            token = args[index]
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"find expression operand is not statically known: {value.reason}",
                           token.text)
                index += 1
                continue
            rendered = value.text or ""
            if rendered in {"(", ")", "!", ","} or rendered in self.FIND_FLAGS:
                index += 1
                continue
            if rendered in self.FIND_DATA:
                index += 2
                continue
            if re.fullmatch(r"-newer[a-zA-Z]{2}", rendered):
                index += 2
                continue
            if rendered in self.FIND_PATH:
                if index + 1 >= len(args):
                    self.issue(token.line, KIND_COVERAGE,
                               f"find predicate {rendered} has no operand", token.text)
                    index += 1
                    continue
                self.record_path(args[index + 1].text, args[index + 1].line,
                                 f"find {rendered}")
                index += 2 if rendered != "-fprintf" else 3
                continue
            if rendered == "-fprintf":
                if index + 1 >= len(args):
                    self.issue(token.line, KIND_COVERAGE,
                               "find -fprintf has no operand", token.text)
                    index += 1
                    continue
                self.record_path(args[index + 1].text, args[index + 1].line, "find -fprintf")
                index += 3
                continue
            if rendered in self.FIND_EXEC:
                vector: list[Token] = []
                cursor = index + 1
                terminated = False
                while cursor < len(args):
                    inner = expand_word(args[cursor].text, self.env)
                    inner_text = inner.text if inner.known else args[cursor].text
                    if inner.known and inner_text in {";", "+"}:
                        terminated = True
                        cursor += 1
                        break
                    vector.append(args[cursor])
                    cursor += 1
                if not terminated:
                    self.issue(token.line, KIND_COVERAGE,
                               f"find {rendered} vector is not terminated by ; or +",
                               token.text)
                    return
                kept: list[Token] = []
                for member in vector:
                    inner = expand_word(member.text, self.env)
                    if inner.known and "{}" in (inner.text or ""):
                        self.issue(member.line, KIND_PATH,
                                   f"find {rendered} substitutes each found pathname for "
                                   "{}; that operand set is dynamic", member.text)
                        continue
                    kept.append(member)
                if kept:
                    self.analyze_command(kept)
                index = cursor
                continue
            self.issue(token.line, KIND_COVERAGE,
                       f"find has no modeled grammar for the predicate {rendered}",
                       token.text)
            index += 1

    # -- tar / xargs -------------------------------------------------------
    TAR_SPEC = spec(
        "tar",
        flags="-c -x -t -r -u -A -d -v -z -j -J -Z -p -P -k -m -O -S -h -a -w "
              "--create --extract --get --list --append --update --catenate --diff "
              "--verbose --gzip --gunzip --bzip2 --xz --compress --auto-compress "
              "--preserve-permissions --same-permissions --absolute-names "
              "--keep-old-files --touch --to-stdout --sparse --dereference "
              "--numeric-owner --no-same-owner --same-owner --no-same-permissions "
              "--totals --one-file-system --no-recursion --recursion --interactive "
              "--ignore-zeros --delay-directory-restore --sort=name",
        path="-f --file -C --directory -T --files-from -X --exclude-from",
        data="--exclude --transform --owner --group --mode --strip-components "
             "--warning --checkpoint --checkpoint-action --sort --to-command "
             "--label --record-size --blocking-factor -b",
        odata="--totals --checkpoint",
    )
    XARGS_SPEC = spec(
        "xargs",
        flags="-0 -r -t -x -p -o --null --no-run-if-empty --verbose --exit "
              "--interactive --open-tty --show-limits",
        path="-a --arg-file",
        data="-d --delimiter -I -i --replace -n --max-args -P --max-procs -s "
             "--max-chars -L --max-lines -E -e --eof --process-slot-var",
        odata="--replace --eof",
        rest="data",
    )

    def analyze_tar(self, args: list[Token], line: int) -> None:
        if args:
            first = expand_word(args[0].text, self.env)
            if first.known and re.fullmatch(r"[cxtruAdf][A-Za-z0-9]*", first.text or ""):
                self.issue(args[0].line, KIND_COVERAGE,
                           "tar old-style option bundle without a leading dash is not "
                           "modeled", args[0].text)
                return
        positionals = self.scan_args("tar", self.TAR_SPEC, args)
        for token, rendered, sources in positionals:
            self.record_path_text(rendered, sources, token.line, "tar", token.text)

    def analyze_xargs(self, args: list[Token], line: int) -> None:
        positionals = self.scan_args("xargs", self.XARGS_SPEC, args)
        self.issue(line, KIND_COVERAGE,
                   "xargs appends operands read from standard input to the command it "
                   "runs; that operand set is not statically determined", "xargs")
        if positionals:
            self.analyze_command([item[0] for item in positionals])

    # -- network primitives ------------------------------------------------
    CURL_SPEC = spec(
        "curl",
        flags="-s -S -f -L -k -i -I -N -q -v -g -j -0 -1 -2 -4 -6 -a -B -G -h -M -O -R "
              "--silent --show-error --fail --fail-with-body --fail-early --location "
              "--location-trusted --insecure --include --head --no-buffer --disable "
              "--verbose --globoff --junk-session-cookies --append --compressed "
              "--no-progress-meter --progress-bar --path-as-is --raw --remote-time "
              "--tcp-nodelay --http1.1 --http2 --ipv4 --ipv6 --create-dirs --get "
              "--no-keepalive --tlsv1.2 --tlsv1.3 --ssl --ssl-reqd --anyauth --basic "
              "--digest --negotiate --ntlm --proxy-insecure --retry-connrefused "
              "--suppress-connect-headers --styled-output --no-alpn --no-sessionid "
              "--http1.0 --parallel --next --help --version",
        path="-o --output -K --config --cert -E --key --cacert --capath --cookie -b "
             "--cookie-jar -c -T --upload-file --netrc-file -D --dump-header --trace "
             "--trace-ascii --unix-socket --output-dir --etag-save --etag-compare "
             "--pinnedpubkey --proxy-cacert --proxy-cert --proxy-key --stderr "
             "--proxy-capath --hostpubsha256 --krb --libcurl",
        net="-x --proxy --proxy1.0 --socks5 --socks4 --socks4a --socks5-hostname "
            "--preproxy",
        form="-d --data --data-ascii --data-binary --data-urlencode -F --form",
        data="-X --request -H --header -w --write-out --connect-timeout --max-time -A "
             "--user-agent -e --referer -u --user --retry --retry-delay --retry-max-time "
             "--max-filesize --limit-rate --resolve --interface --form-string -m -C "
             "--continue-at --range -r --header-file --expect100-timeout --tls-max "
             "--proto --proto-default --proto-redir --ciphers --tlsuser --tlspassword "
             "--connect-to --abstract-unix-socket --happy-eyeballs-timeout-ms "
             "--speed-limit --speed-time --max-redirs --oauth2-bearer --proxy-user "
             "--noproxy --local-port --dns-servers --keepalive-time -y -Y -z --time-cond",
        unmodeled="-O --remote-name -J --remote-header-name --remote-name-all",
        rest="net",
    )
    WGET_SPEC = spec(
        "wget",
        flags="-q -v -nv -c -N -S -d -b -e? -4 -6 -nc -np -nH -x -k -p -r -m -E -H -L "
              "--quiet --verbose --no-verbose --continue --timestamping --server-response "
              "--spider --no-clobber --no-check-certificate --no-parent --no-host-directories "
              "--recursive --mirror --page-requisites --content-disposition --debug "
              "--force-directories --no-directories --ignore-length --inet4-only --inet6-only",
        path="-O --output-document -o --output-file -a --append-output -i --input-file "
             "-P --directory-prefix --ca-certificate --certificate --private-key "
             "--load-cookies --save-cookies --config --ca-directory --warc-file",
        data="-T --timeout -t --tries --user --password --header -U --user-agent "
             "--max-redirect --limit-rate --wait --waitretry --read-timeout "
             "--connect-timeout --dns-timeout --cut-dirs --level -l --domains "
             "--exclude-domains --accept --reject --restrict-file-names --progress",
        net="-e --execute",
        rest="net",
    )
    NC_SPEC = spec(
        "nc",
        flags="-l -v -n -z -k -4 -6 -u -C -D -d -t -r -q0",
        path="-U --unixsock",
        shell="-e -c",
        net="-x",
        data="-w -q -s -p -X -i -O -I -T -m",
        rest="data",
    )
    SSH_PATH_OPTS = {"-i", "-F", "-S", "-E"}
    SSH_DATA_OPTS = {"-l", "-c", "-m", "-Q", "-Q"}
    SSH_UNMODELED_OPTS = {"-L", "-R", "-D", "-W", "-J", "-b", "-B", "-e", "-w", "-I"}
    SSH_FLAGS = {
        "-4", "-6", "-A", "-a", "-C", "-f", "-G", "-g", "-K", "-k", "-M", "-N", "-n",
        "-q", "-s", "-T", "-t", "-V", "-v", "-X", "-x", "-Y", "-y",
    }
    SSH_INERT_OPTIONS = {
        "batchmode", "stricthostkeychecking", "connecttimeout", "serveraliveinterval",
        "serveralivecountmax", "exitonforwardfailure", "loglevel", "passwordauthentication",
        "pubkeyauthentication", "port", "requesttty", "clearallforwardings",
        "preferredauthentications", "identitiesonly", "compression",
    }

    def record_form_value(
        self, command: str, text: str, sources: frozenset[str], line: int, expression: str
    ) -> None:
        """curl form/data operands: a leading @ or =@ names a file it reads."""
        body = text
        if "=" in body:
            body = body.split("=", 1)[1]
        if body.startswith("@") or body.startswith("<"):
            self.record_path_text(body[1:], sources, line, f"{command} form", expression)

    def analyze_curl(self, args: list[Token], line: int) -> None:
        positionals = self.scan_args("curl", self.CURL_SPEC, args)
        for token, rendered, sources in positionals:
            self.record_network_text(rendered, sources, token.line, "curl", token.text)

    def analyze_wget(self, args: list[Token], line: int) -> None:
        positionals = self.scan_args("wget", self.WGET_SPEC, args)
        rendered_all = [expand_word(token.text, self.env) for token in args]
        has_output = any(
            value.known and (value.text in {"-O", "--output-document"}
                             or (value.text or "").startswith("--output-document="))
            for value in rendered_all
        )
        if not has_output:
            self.issue(line, KIND_PATH,
                       "wget without -O writes a file whose name is derived from the URL "
                       "and the working directory", "wget")
        for token, rendered, sources in positionals:
            self.record_network_text(rendered, sources, token.line, "wget", token.text)

    def analyze_netcat(self, command: str, args: list[Token], line: int) -> None:
        rendered_all = [expand_word(token.text, self.env) for token in args]
        if any(value.known and value.text in {"-l", "--listen"} for value in rendered_all):
            self.issue(line, KIND_COVERAGE,
                       f"{command} listener grammar is not modeled", command)
            return
        positionals = self.scan_args(command, self.NC_SPEC, args)
        if len(positionals) != 2:
            self.issue(line, KIND_COVERAGE,
                       f"{command} needs exactly a host and a port operand for the "
                       "modeled client grammar", command)
            return
        host_token, host, host_sources = positionals[0]
        port_token, port, port_sources = positionals[1]
        self.record_network_text(f"{host}:{port}", host_sources | port_sources,
                                 host_token.line, command, host_token.text)

    def analyze_ssh(self, args: list[Token], line: int) -> None:
        port = 22
        index = 0
        destination: tuple[Token, str, frozenset[str]] | None = None
        remote: list[Token] = []
        while index < len(args):
            token = args[index]
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"ssh argument is not statically known: {value.reason}",
                           token.text)
                return
            rendered = value.text or ""
            if destination is not None:
                remote.append(token)
                index += 1
                continue
            if rendered == "--":
                index += 1
                continue
            if rendered.startswith("-") and len(rendered) > 1:
                option = rendered[:2]
                attached = rendered[2:]
                if option in self.SSH_FLAGS and not attached:
                    index += 1
                    continue
                if option in self.SSH_UNMODELED_OPTS:
                    self.issue(token.line, KIND_ENDPOINT,
                               f"ssh option {option} carries a forwarding or bind "
                               "endpoint grammar that is not modeled", token.text)
                    return
                if option == "-p":
                    text = attached or (
                        expand_word(args[index + 1].text, self.env).text or ""
                        if index + 1 < len(args) else ""
                    )
                    if not re.fullmatch(r"[0-9]{1,5}", text):
                        self.issue(token.line, KIND_ENDPOINT,
                                   "ssh -p port is not a static number", token.text)
                        return
                    port = int(text)
                    index += 1 if attached else 2
                    continue
                if option == "-o":
                    text = attached
                    if not text and index + 1 < len(args):
                        inner = expand_word(args[index + 1].text, self.env)
                        if not inner.known:
                            self.issue(token.line, KIND_COVERAGE,
                                       "ssh -o value is not statically known", token.text)
                            return
                        text = inner.text or ""
                    key = text.split("=", 1)[0].strip().lower()
                    if key not in self.SSH_INERT_OPTIONS:
                        self.issue(token.line, KIND_COVERAGE,
                                   f"ssh -o {key} can name a path, a command or an "
                                   "endpoint; that option is not modeled", token.text)
                        return
                    if key == "port":
                        candidate = text.split("=", 1)[1] if "=" in text else ""
                        if not re.fullmatch(r"[0-9]{1,5}", candidate.strip()):
                            self.issue(token.line, KIND_ENDPOINT,
                                       "ssh -o Port is not a static number", token.text)
                            return
                        port = int(candidate)
                    index += 1 if attached else 2
                    continue
                if option in self.SSH_PATH_OPTS:
                    if attached:
                        self.consume_value("ssh", "path", attached, value.sources,
                                           token.line, token.text)
                        index += 1
                    elif index + 1 < len(args):
                        self.record_path(args[index + 1].text, args[index + 1].line, "ssh")
                        index += 2
                    else:
                        self.issue(token.line, KIND_COVERAGE,
                                   f"ssh option {option} has no value operand", token.text)
                        index += 1
                    continue
                if option in self.SSH_DATA_OPTS:
                    index += 1 if attached else 2
                    continue
                if len(rendered) > 2 and all("-" + ch in self.SSH_FLAGS for ch in rendered[1:]):
                    index += 1
                    continue
                self.issue(token.line, KIND_COVERAGE,
                           f"ssh has no modeled grammar for option {option}", token.text)
                return
            destination = (token, rendered, value.sources)
            index += 1
        if destination is None:
            self.issue(line, KIND_ENDPOINT, "ssh has no statically visible destination", "ssh")
            return
        token, rendered, sources = destination
        self.record_network_text(rendered, sources, token.line, "ssh", token.text, port)
        if remote:
            self.issue(remote[0].line, KIND_COVERAGE,
                       "ssh remote command text executes on the remote host and is "
                       "outside the local static path domain",
                       " ".join(item.text for item in remote))

    SCP_SPEC = spec(
        "scp",
        flags="-3 -4 -6 -A -B -C -O -p -q -r -T -v -d -s",
        path="-i -F -c? -S",
        data="-l -c -J -o -P",
        rest="path",
    )

    def analyze_scp(self, command: str, args: list[Token], line: int) -> None:
        port = 22
        rendered_all = [expand_word(token.text, self.env) for token in args]
        for index, value in enumerate(rendered_all):
            if value.known and value.text == "-P" and index + 1 < len(rendered_all):
                candidate = rendered_all[index + 1]
                if not candidate.known or not re.fullmatch(r"[0-9]{1,5}", candidate.text or ""):
                    self.issue(args[index].line, KIND_ENDPOINT,
                               f"{command} -P port is not a static number", args[index].text)
                    return
                port = int(candidate.text or "22")
        positionals = self.scan_args(command, self.SCP_SPEC, args)
        for token, rendered, sources in positionals:
            if rendered.startswith("/") or rendered.startswith("./") or rendered.startswith("../"):
                self.record_path_text(rendered, sources, token.line, command, token.text)
                continue
            match = re.fullmatch(r"(?:(?P<user>[^@/]+)@)?(?P<host>\[[^\]]+\]|[^:/@]+):(?P<path>.*)", rendered)
            if match:
                self.record_network_text(match.group("host"), sources, token.line,
                                         command, token.text, port)
                self.issue(token.line, KIND_PATH,
                           f"{command} remote path operand is a path on the peer host, "
                           "which this allowlist does not describe", token.text)
                continue
            self.record_path_text(rendered, sources, token.line, command, token.text)

    def analyze_getent(self, args: list[Token], line: int) -> None:
        database = "<none>"
        if args:
            value = expand_word(args[0].text, self.env)
            database = value.text if value.known else args[0].text
        self.issue(line, KIND_ENDPOINT,
                   f"getent resolves the {database} database through NSS, whose backing "
                   "service set (files, DNS, LDAP, NIS, systemd-resolved) is host "
                   "configuration and is not statically determined", "getent")

    # -- shell strings and privileged control -------------------------------
    TRAP_SPEC = spec("trap", flags="-l -p -P", rest="data")

    def analyze_trap(self, args: list[Token], line: int) -> None:
        operands: list[Token] = []
        for token in args:
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"trap argument is not statically known: {value.reason}",
                           token.text)
                return
            rendered = value.text or ""
            if rendered in {"-l", "-p", "-P"}:
                continue
            if rendered == "--":
                continue
            operands.append(token)
        if not operands:
            return
        action = expand_word(operands[0].text, self.env)
        if not action.known:
            self.issue(operands[0].line, KIND_COVERAGE,
                       "trap action is not statically known", operands[0].text)
            return
        text = action.text or ""
        if text == "-" or text == "":
            return
        if len(operands) == 1 and re.fullmatch(r"(SIG)?[A-Z][A-Z0-9]*|[0-9]+", text):
            return
        self.analyze_shell_source(text, operands[0].line, "trap action")

    def analyze_alias(self, args: list[Token], line: int) -> None:
        for token in args:
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"alias argument is not statically known: {value.reason}",
                           token.text)
                continue
            rendered = value.text or ""
            if rendered in {"-p", "--"}:
                continue
            if "=" not in rendered:
                continue
            self.analyze_shell_source(rendered.split("=", 1)[1], token.line, "alias body")

    SYSTEMCTL_SPEC = spec(
        "systemctl",
        flags="-q --quiet --no-pager --no-legend --no-ask-password --user --system "
              "--now --full -l -a --all --failed --plain --value -H? --recursive",
        path="--root",
        data="-t --type --state -p --property -o --output -n --lines --machine "
             "--signal --kill-who --job-mode --host",
        rest="data",
    )
    SYSTEMCTL_VERBS = {
        "is-active", "is-enabled", "is-failed", "is-system-running", "show",
        "status", "cat", "list-units", "list-unit-files", "list-sockets",
        "list-timers", "show-environment", "daemon-reload", "get-default",
    }

    def analyze_systemctl(self, args: list[Token], line: int) -> None:
        positionals = self.scan_args("systemctl", self.SYSTEMCTL_SPEC, args)
        if not positionals:
            return
        verb = positionals[0][1]
        if verb not in self.SYSTEMCTL_VERBS:
            self.issue(positionals[0][0].line, KIND_COVERAGE,
                       f"systemctl verb {verb} is not in the modeled read-only set and "
                       "can install, link or remove unit files", positionals[0][0].text)
            return
        for token, rendered, sources in positionals[1:]:
            if rendered.startswith(("/", "./", "../")):
                self.record_path_text(rendered, sources, token.line, "systemctl", token.text)

    # -- interpreters and program-text tools ---------------------------------
    INTERPRETER_FLAGS = {
        "-E", "-s", "-S", "-u", "-B", "-I", "-O", "-OO", "-v", "-x", "-q", "-i",
        "-b", "-d", "-t", "-W", "-w", "-n", "-p", "-l", "-e?", "-a", "-r", "-h",
        "--version", "--help", "-",
    }
    INTERPRETER_CODE = {"-c", "--command", "-e", "--eval", "--exec"}

    def analyze_interpreter(self, command: str, args: list[Token], line: int) -> None:
        index = 0
        script_seen = False
        while index < len(args):
            token = args[index]
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} argument is not statically known: {value.reason}",
                           token.text)
                index += 1
                continue
            rendered = value.text or ""
            if not script_seen and rendered in self.INTERPRETER_CODE:
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} {rendered} program text is opaque to static path "
                           "analysis and can open any path or endpoint", token.text)
                index += 2
                script_seen = True
                continue
            if not script_seen and rendered in {"-m", "--module"}:
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} -m runs a module whose code is opaque to static "
                           "path analysis", token.text)
                index += 2
                script_seen = True
                continue
            if not script_seen and rendered.startswith("-") and rendered != "-":
                if rendered in self.INTERPRETER_FLAGS:
                    index += 1
                    continue
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} has no modeled grammar for option {rendered}",
                           token.text)
                index += 1
                continue
            if not script_seen:
                self.record_path_text(rendered, value.sources, token.line, command,
                                      token.text)
                self.issue(token.line, KIND_COVERAGE,
                           f"{command} runs the program at this path; its content is not "
                           "part of the analyzed input", token.text)
                script_seen = True
                index += 1
                continue
            if rendered.startswith(("/", "./", "../")) or "://" in rendered:
                self.record_path_text(rendered, value.sources, token.line,
                                      f"{command} argv", token.text)
            index += 1

    SED_SPEC = spec(
        "sed",
        flags="-n -r -E -s -u -z --quiet --silent --regexp-extended --separate "
              "--null-data --debug --posix --follow-symlinks",
        path="-f --file",
        data="-l --line-length -e --expression",
        option_re=r"-i.*|--in-place(=.*)?",
        roles=("data",),
        rest="path",
    )
    AWK_SPEC = spec(
        "awk",
        flags="--posix --traditional --re-interval -W",
        path="-f --file --source?",
        data="-F --field-separator -v --assign",
        roles=("data",),
        rest="path",
    )
    JQ_SPEC = spec(
        "jq",
        flags="-r -n -e -s -c -j -a -M -S -C -R --raw-output --null-input --exit-status "
              "--slurp --compact-output --tab --join-output --ascii-output "
              "--monochrome-output --sort-keys --raw-input --seq --stream",
        path="-f --from-file --slurpfile --rawfile",
        data="--arg --argjson --indent --args --jsonargs",
        roles=("data",),
        rest="path",
    )
    GREP_SPEC = spec(
        "grep",
        flags="-a -b -c -E -F -G -H -h -i -I -L -l -n -o -P -q -R -r -s -U -v -w -x -z "
              "-u --extended-regexp --fixed-strings --basic-regexp --perl-regexp "
              "--ignore-case --invert-match --word-regexp --line-regexp --count "
              "--files-with-matches --files-without-match --only-matching --quiet "
              "--silent --no-messages --line-number --byte-offset --recursive "
              "--dereference-recursive --null --null-data --text --with-filename "
              "--no-filename --initial-tab --line-buffered",
        path="-f --file --exclude-from",
        data="-e --regexp -m --max-count -A --after-context -B --before-context "
             "-C --context --label --binary-files --devices --directories -d -D "
             "--include --exclude --exclude-dir --group-separator",
        odata="--color --colour --group-separator",
        option_re=r"-[0-9]+",
        roles=("data",),
        rest="path",
    )

    def analyze_program_tool(self, command: str, spec_item: Spec, args: list[Token],
                             line: int, opaque: bool) -> None:
        rendered_all = [expand_word(token.text, self.env) for token in args]
        script_supplied = any(
            value.known and (
                value.text in {"-e", "--expression", "-f", "--file", "--regexp"}
                or (value.text or "").startswith(("-e", "--expression=", "--file=", "--regexp="))
            )
            for value in rendered_all
        )
        positionals = self.scan_args(command, spec_item, args)
        for order, (token, rendered, sources) in enumerate(positionals):
            if order == 0 and not script_supplied:
                if opaque:
                    self.issue(token.line, KIND_COVERAGE,
                               f"{command} program text can open files of its own and is "
                               "not statically analyzed", token.text)
                if rendered.startswith(("/", "./", "../")):
                    self.record_path_text(rendered, sources, token.line, command, token.text)
                continue
            self.record_path_text(rendered, sources, token.line, command, token.text)
        if script_supplied and opaque:
            self.issue(line, KIND_COVERAGE,
                       f"{command} program text can open files of its own and is not "
                       "statically analyzed", command)

    # -- redirections and dispatch -------------------------------------------
    def strip_redirections(self, tokens: list[Token]) -> list[Token]:
        cleaned: list[Token] = []
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token.operator and token.text in self.REDIRS:
                if index + 1 >= len(tokens):
                    self.issue(token.line, KIND_COVERAGE, "redirection has no target",
                               token.text)
                    index += 1
                    continue
                target = tokens[index + 1]
                value = expand_word(target.text, self.env)
                rendered = value.text if value.known else target.text
                if token.text in {">&", "<&"} and re.fullmatch(r"-?|[0-9]+", rendered or ""):
                    pass  # file-descriptor duplication or close: no filesystem path
                elif token.text == "<<<":
                    pass  # here-string data is not a filesystem path
                elif token.text in {"<<", "<<-"}:
                    pass  # here-document body is stdin data, collected by the lexer
                else:
                    self.record_path(target.text, target.line,
                                     f"redirection {token.text}")
                index += 2
                continue
            if index + 1 < len(tokens) and tokens[index + 1].operator and tokens[index + 1].text in self.REDIRS:
                if re.fullmatch(r"[0-9]+|\{[A-Za-z_][A-Za-z0-9_]*\}", token.text):
                    index += 1
                    continue
            cleaned.append(token)
            index += 1
        return cleaned

    def analyze_command(self, tokens: list[Token]) -> None:
        if not tokens:
            return
        tokens = self.strip_redirections(tokens)
        if not tokens:
            return
        index = 0
        while index < len(tokens) and ASSIGN_RE.fullmatch(tokens[index].text):
            self.record_assignment_value(tokens[index], "assignment prefix")
            self.assignment(tokens[index])
            index += 1
        if index >= len(tokens):
            return
        first = tokens[index]
        if first.text in {"local", "declare", "typeset", "export", "readonly"}:
            self.analyze_declaration(first, tokens[index + 1:])
            return
        command_value = expand_word(first.text, self.env)
        if not command_value.known:
            self.issue(first.line, KIND_COVERAGE,
                       f"dynamic command name: {command_value.reason}", first.text)
            return
        command = self._basename(command_value.text or "")
        args = tokens[index + 1:]
        line = first.line
        if command in self.functions:
            # The body is analysed at its definition, where every positional use
            # is fail-closed; the call site adds no statically known path.
            return
        if command in self.CONTROL:
            return
        if command == "eval":
            self.issue(line, KIND_COVERAGE, "eval is forbidden",
                       " ".join(item.text for item in tokens))
            return
        if command in {"source", "."}:
            self.issue(line, KIND_COVERAGE,
                       "sourced file content is outside the analyzed input", command)
            for token in args:
                value = expand_word(token.text, self.env)
                if not value.known:
                    self.issue(token.line, KIND_PATH,
                               value.reason or "unresolvable path", token.text)
                    continue
                self.record_path_text(value.text or "", value.sources, token.line,
                                      command, token.text)
            return
        if command in self.WRAPPERS:
            self.analyze_wrapped(command, args, line)
            return
        if command in {"test", "[", "[["}:
            self.analyze_test(args)
            return
        if command == "find":
            self.analyze_find(args, line)
            return
        if command == "tar":
            self.analyze_tar(args, line)
            return
        if command == "xargs":
            self.analyze_xargs(args, line)
            return
        if command == "curl":
            self.analyze_curl(args, line)
            return
        if command == "wget":
            self.analyze_wget(args, line)
            return
        if command in {"nc", "ncat", "netcat"}:
            self.analyze_netcat(command, args, line)
            return
        if command == "ssh":
            self.analyze_ssh(args, line)
            return
        if command in {"scp", "sftp"}:
            self.analyze_scp(command, args, line)
            return
        if command == "getent":
            self.analyze_getent(args, line)
            return
        if command == "trap":
            self.analyze_trap(args, line)
            return
        if command == "alias":
            self.analyze_alias(args, line)
            return
        if command == "systemctl":
            self.analyze_systemctl(args, line)
            return
        if command in self.INTERPRETERS:
            self.analyze_interpreter(command, args, line)
            return
        if command == "sed":
            self.analyze_program_tool(command, self.SED_SPEC, args, line, True)
            return
        if command in {"awk", "gawk", "mawk", "nawk"}:
            self.analyze_program_tool(command, self.AWK_SPEC, args, line, True)
            return
        if command == "jq":
            self.analyze_program_tool(command, self.JQ_SPEC, args, line, False)
            return
        if command == "grep":
            self.analyze_program_tool(command, self.GREP_SPEC, args, line, False)
            return
        if command in {"cd", "pushd"}:
            for token, rendered, sources in self.scan_args(command, SPECS[command], args):
                if command == "pushd" and re.fullmatch(r"[+-][0-9]+", rendered):
                    continue
                if rendered == "-":
                    self.issue(token.line, KIND_PATH,
                               f"{command} - selects OLDPWD, which is not a "
                               "preregistered constant", token.text)
                    continue
                self.record_path_text(rendered, sources, token.line, command, token.text)
            return
        spec_item = SPECS.get(command)
        if spec_item is not None:
            positionals = self.scan_args(command, spec_item, args)
            self.dispatch_positionals(command, spec_item, positionals)
            return
        self.issue(line, KIND_COVERAGE,
                   f"opaque command {command} has no registered argv grammar", command)
        for token in args:
            value = expand_word(token.text, self.env)
            if not value.known:
                self.issue(token.line, KIND_COVERAGE,
                           f"opaque command argument: {value.reason}", token.text)
                continue
            rendered = value.text or ""
            if rendered.startswith(("/", "./", "../")) or "://" in rendered or NETWORK_RE.fullmatch(rendered):
                self.issue(token.line, KIND_COVERAGE,
                           f"opaque command {command} may forward a path or endpoint",
                           token.text)

    def analyze_tokens(self, tokens: list[Token]) -> None:
        command: list[Token] = []
        for token in tokens:
            if token.operator and token.text == "!":
                # `!` negates a pipeline only in command position; inside a test
                # it is an operand, and splitting there loses the operand.
                if command:
                    command.append(Token("!", token.line, False))
                continue
            if token.operator and token.text in self.SPLIT:
                self.analyze_command(command)
                command = []
            else:
                command.append(token)
        self.analyze_command(command)

    def strip_case_patterns(self, tokens: list[Token]) -> list[Token]:
        """Remove case selectors/patterns while retaining every arm body."""
        result: list[Token] = []
        states: list[str] = []
        for token in tokens:
            if states and states[-1] == "selector":
                if not token.operator and token.text == "in":
                    states[-1] = "pattern"
                continue
            if states and states[-1] == "pattern":
                if not token.operator and token.text == "esac":
                    states.pop()
                elif token.operator and token.text == ")":
                    states[-1] = "body"
                    result.append(Token("\n", token.line, True))
                continue
            if not token.operator and token.text == "case":
                states.append("selector")
                result.append(Token("\n", token.line, True))
                continue
            if states and states[-1] == "body":
                if not token.operator and token.text == "esac":
                    states.pop()
                    result.append(Token("\n", token.line, True))
                    continue
                if token.operator and token.text in {";;", ";&", ";;&"}:
                    states[-1] = "pattern"
                    result.append(Token("\n", token.line, True))
                    continue
            result.append(token)
        return result

    def normalize_control_tokens(self, tokens: list[Token]) -> list[Token]:
        """Turn control syntax into separators without discarding conditions."""
        result: list[Token] = []
        separators = {"if", "then", "elif", "else", "fi", "while", "until", "do", "done"}
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if (
                index + 1 < len(tokens)
                and not token.operator
                and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=", token.text)
                and tokens[index + 1].operator and tokens[index + 1].text == "("
            ):
                depth = 1
                index += 2
                while index < len(tokens) and depth:
                    if tokens[index].operator and tokens[index].text == "(":
                        depth += 1
                    elif tokens[index].operator and tokens[index].text == ")":
                        depth -= 1
                    index += 1
                result.append(Token("\n", token.line, True))
                continue
            if not token.operator and token.text == "[[":
                result.append(token)
                index += 1
                while index < len(tokens):
                    current = tokens[index]
                    if not current.operator and current.text == "]]":
                        result.append(current)
                        index += 1
                        break
                    result.append(Token(current.text, current.line, False))
                    index += 1
                else:
                    self.issue(token.line, KIND_PARSE, "unclosed [[ test", "[[")
                continue
            if not token.operator and token.text in {"for", "select"}:
                if index + 1 < len(tokens) and not tokens[index + 1].operator and NAME_RE.fullmatch(tokens[index + 1].text):
                    self.env[tokens[index + 1].text] = Value(
                        None, f"loop variable {tokens[index + 1].text} is dynamic"
                    )
                start_line = token.line
                index += 1
                depth = 0
                while index < len(tokens):
                    current = tokens[index]
                    if current.operator and current.text == "((":
                        depth += 1
                    elif current.operator and current.text == "))" and depth:
                        depth -= 1
                    elif depth == 0 and not current.operator and current.text == "do":
                        index += 1
                        break
                    index += 1
                else:
                    self.issue(start_line, KIND_PARSE, "loop header has no do terminator",
                               token.text)
                result.append(Token("\n", start_line, True))
                continue
            if token.operator and token.text == "((":
                start_line = token.line
                depth = 1
                index += 1
                while index < len(tokens) and depth:
                    if tokens[index].operator and tokens[index].text == "((":
                        depth += 1
                    elif tokens[index].operator and tokens[index].text == "))":
                        depth -= 1
                    index += 1
                if depth:
                    self.issue(start_line, KIND_PARSE, "unclosed arithmetic command", "((")
                else:
                    self.issue(start_line, KIND_COVERAGE,
                               "arithmetic command is outside the accepted scalar subset",
                               "((...))")
                result.append(Token("\n", start_line, True))
                continue
            if not token.operator and token.text in separators:
                result.append(Token("\n", token.line, True))
                index += 1
                continue
            if not token.operator and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*\+=", token.text):
                self.issue(token.line, KIND_COVERAGE,
                           "compound assignment is outside the accepted scalar subset",
                           token.text)
                result.append(Token("\n", token.line, True))
                index += 1
                continue
            result.append(token)
            index += 1
        return result

    def analyze_functions_and_top_level(self, tokens: list[Token]) -> None:
        top_level: list[Token] = []
        index = 0
        while index < len(tokens):
            is_function = (
                index + 3 < len(tokens)
                and not tokens[index].operator
                and NAME_RE.fullmatch(tokens[index].text) is not None
                and tokens[index + 1].operator and tokens[index + 1].text == "("
                and tokens[index + 2].operator and tokens[index + 2].text == ")"
                and tokens[index + 3].operator and tokens[index + 3].text == "{"
            )
            if not is_function:
                top_level.append(tokens[index])
                index += 1
                continue
            depth = 1
            end = index + 4
            while end < len(tokens) and depth:
                if tokens[end].operator and tokens[end].text == "{":
                    depth += 1
                elif tokens[end].operator and tokens[end].text == "}":
                    depth -= 1
                end += 1
            if depth:
                self.issue(tokens[index].line, KIND_PARSE, "unclosed function body",
                           tokens[index].text)
                return
            saved_env = self.env
            self.env = dict(self.env)
            self.analyze_tokens(tokens[index + 4:end - 1])
            self.env = saved_env
            index = end
        self.analyze_tokens(top_level)

    def run(self) -> tuple[list[Use], list[Issue]]:
        lexer = ShellLexer(self.text)
        try:
            tokens = lexer.tokens()
        except LexError as exc:
            self.issue(exc.line, KIND_PARSE, str(exc), "shell input")
            return self.uses, self.issues
        for left, right in zip(tokens, tokens[1:]):
            if (
                not left.operator
                and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=", left.text)
                and right.operator and right.text == "("
            ):
                self.issue(left.line, KIND_COVERAGE,
                           "array assignment is outside the accepted scalar subset",
                           left.text + "(...)")
        stack: list[Token] = []
        closing = {")": "(", "}": "{", "))": "(("}
        case_depth = 0
        in_extended_test = False
        for token in tokens:
            if not token.operator and token.text == "[[":
                in_extended_test = True
                continue
            if not token.operator and token.text == "]]":
                in_extended_test = False
                continue
            if in_extended_test:
                continue
            if not token.operator and token.text == "case":
                case_depth += 1
                continue
            if not token.operator and token.text == "esac":
                if case_depth == 0:
                    self.issue(token.line, KIND_PARSE, "unmatched shell keyword esac",
                               token.text)
                else:
                    case_depth -= 1
                continue
            if not token.operator:
                continue
            if token.text in {"(", "{", "(("}:
                stack.append(token)
            elif token.text in closing:
                if token.text == ")" and case_depth and (not stack or stack[-1].text != "("):
                    continue  # case-pattern terminator
                if not stack or stack[-1].text != closing[token.text]:
                    self.issue(token.line, KIND_PARSE,
                               f"unmatched shell delimiter {token.text}", token.text)
                else:
                    stack.pop()
        for token in stack:
            self.issue(token.line, KIND_PARSE,
                       f"unclosed shell delimiter {token.text}", token.text)
        if case_depth:
            self.issue(tokens[-1].line if tokens else 1, KIND_PARSE,
                       "unclosed shell keyword case", "case")
        normalized = self.normalize_control_tokens(self.strip_case_patterns(tokens))
        self.analyze_functions_and_top_level(normalized)
        for line, body in lexer.substitutions:
            if self.depth >= MAX_NESTING:
                self.issue(line, KIND_COVERAGE,
                           "command substitution nesting exceeds the modeled depth", body)
                continue
            nested = Analyzer(
                body,
                self.env,
                self.rules,
                self.depth + 1,
                self.context,
            )
            nested.run()
            self.merge(nested, line)
        return self.uses, self.issues


SEMANTICS_LINE = (
    "PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established "
    "mount_boundary=not_established host_probe=none"
)


VALUE_ID_PATTERN = r"A\d{4}\.V\d{4}"
MEMBER_ID_PATTERN = VALUE_ID_PATTERN + r"\.(?:whole|colon|words|word-colon)\.M\d{4}"
B64U_PATTERN = r"b64u:[A-Za-z0-9_-]*"
SOURCES_PATTERN = r"(?:-|[A-Za-z_][A-Za-z0-9_]*(?:,[A-Za-z_][A-Za-z0-9_]*)*)"
ACCOUNTING_SUMMARY_RE = re.compile(
    r"^PATHSCOPE accounting_summary=(OK|FAIL) admitted_value_count=(\d+) "
    r"member_count=(\d+) disposition_count=(\d+) accounting_fault_count=(\d+)$"
)
VALUE_ACCOUNT_RE = re.compile(
    rf"^VALUE_ACCOUNT value_id=({VALUE_ID_PATTERN}) line=(\d+) site=({B64U_PATTERN}) "
    r"member_count=(\d+) disposition_count=(\d+) conserved=(true|false)$"
)
MEMBER_RECORD_RE = re.compile(
    rf"^MEMBER member_id=({MEMBER_ID_PATTERN}) value_id=({VALUE_ID_PATTERN}) "
    rf"reading=(whole|colon|words|word-colon) ordinal=(\d+) rendered_span=(\d+):(\d+) "
    rf"raw_slices=({B64U_PATTERN}) text=({B64U_PATTERN}) sources=({SOURCES_PATTERN}) "
    rf"disposition=(ALLOWED_WITH_REASON|FORBIDDEN_WITH_REASON|UNRESOLVED_FAIL_CLOSED) "
    rf"reason=([A-Za-z][A-Za-z0-9_]*) rule=(-|{B64U_PATTERN}) "
    rf"candidate_domain=(fs|net|none) candidate_value=(-|{B64U_PATTERN})$"
)
ACCOUNTING_FAULT_RE = re.compile(
    rf"^ACCOUNTING_FAULT value_id=({VALUE_ID_PATTERN}|NONE) "
    rf"member_id=({MEMBER_ID_PATTERN}|NONE) reason=([A-Za-z][A-Za-z0-9_]*)$"
)


def b64u(text: str) -> str:
    return "b64u:" + base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii").rstrip("=")


def _raw_slices_token(raw_slices: tuple[RawSlice, ...]) -> str:
    payload = [
        {
            "origin": item.origin,
            "raw_end": item.raw_end,
            "raw_start": item.raw_start,
            "raw_text": item.raw_text,
        }
        for item in raw_slices
    ]
    return b64u(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def _accounting_records(analyzer: Analyzer) -> list[str]:
    analyzer.validate_accounting()
    members_by_value: dict[str, list[MemberOccurrence]] = {}
    for member in analyzer.members:
        members_by_value.setdefault(member.value_id, []).append(member)
    dispositions_by_value: dict[str, list[TerminalDisposition]] = {}
    for disposition in analyzer.dispositions:
        dispositions_by_value.setdefault(disposition.value_id, []).append(disposition)
    disposition_counter = Counter(item.member_id for item in analyzer.dispositions)
    disposition_by_member = {
        item.member_id: item
        for item in analyzer.dispositions
        if disposition_counter[item.member_id] == 1
    }

    value_rows: list[str] = []
    for value in analyzer.admitted_values:
        member_ids = [item.member_id for item in members_by_value.get(value.value_id, [])]
        disposition_ids = [
            item.member_id for item in dispositions_by_value.get(value.value_id, [])
        ]
        conserved = Counter(member_ids) == Counter(disposition_ids) and all(
            Counter(disposition_ids)[member_id] == 1 for member_id in member_ids
        )
        row = (
            f"VALUE_ACCOUNT value_id={value.value_id} line={value.line} "
            f"site={b64u(value.site)} member_count={len(member_ids)} "
            f"disposition_count={len(disposition_ids)} "
            f"conserved={'true' if conserved else 'false'}"
        )
        if VALUE_ACCOUNT_RE.fullmatch(row) is None:
            analyzer.accounting_fault("value_serialization_failed", value.value_id)
        else:
            value_rows.append(row)

    member_rows: list[str] = []
    for member in analyzer.members:
        disposition = disposition_by_member.get(member.member_id)
        if disposition is None or not isinstance(disposition.disposition, DispositionKind):
            continue
        sources = ",".join(sorted(member.sources)) if member.sources else "-"
        rule = b64u(disposition.rule) if disposition.rule is not None else "-"
        candidate_domain = disposition.candidate_domain or "none"
        candidate_value = (
            b64u(disposition.candidate_value)
            if disposition.candidate_value is not None
            else "-"
        )
        row = (
            f"MEMBER member_id={member.member_id} value_id={member.value_id} "
            f"reading={member.reading} ordinal={member.ordinal} "
            f"rendered_span={member.rendered_start}:{member.rendered_end} "
            f"raw_slices={_raw_slices_token(member.raw_slices)} text={b64u(member.text)} "
            f"sources={sources} disposition={disposition.disposition.value} "
            f"reason={disposition.reason} rule={rule} "
            f"candidate_domain={candidate_domain} candidate_value={candidate_value}"
        )
        if MEMBER_RECORD_RE.fullmatch(row) is None:
            analyzer.accounting_fault(
                "member_serialization_failed", member.value_id, member.member_id
            )
        else:
            member_rows.append(row)

    if len(value_rows) != len(analyzer.admitted_values):
        analyzer.accounting_fault("printed_value_record_count_mismatch")
    if (
        len(member_rows) != len(analyzer.members)
        or len(member_rows) != len(analyzer.dispositions)
    ):
        analyzer.accounting_fault("printed_member_record_count_mismatch")

    if not analyzer.admitted_values and not analyzer.accounting_faults:
        return []

    fault_rows: list[str] = []
    for fault in analyzer.accounting_faults:
        value_id = (
            fault.value_id
            if fault.value_id is not None and re.fullmatch(VALUE_ID_PATTERN, fault.value_id)
            else "NONE"
        )
        member_id = (
            fault.member_id
            if fault.member_id is not None and re.fullmatch(MEMBER_ID_PATTERN, fault.member_id)
            else "NONE"
        )
        row = (
            f"ACCOUNTING_FAULT value_id={value_id} member_id={member_id} "
            f"reason={fault.reason}"
        )
        if ACCOUNTING_FAULT_RE.fullmatch(row) is None:
            row = (
                "ACCOUNTING_FAULT value_id=NONE member_id=NONE "
                "reason=accounting_fault_serialization_failed"
            )
        fault_rows.append(row)

    summary_state = "FAIL" if analyzer.accounting_faults else "OK"
    summary = (
        f"PATHSCOPE accounting_summary={summary_state} "
        f"admitted_value_count={len(analyzer.admitted_values)} "
        f"member_count={len(analyzer.members)} "
        f"disposition_count={len(analyzer.dispositions)} "
        f"accounting_fault_count={len(fault_rows)}"
    )
    if ACCOUNTING_SUMMARY_RE.fullmatch(summary) is None:
        analyzer.accounting_fault("accounting_summary_serialization_failed")
        fault_rows.append(
            "ACCOUNTING_FAULT value_id=NONE member_id=NONE "
            "reason=accounting_summary_serialization_failed"
        )
        summary = (
            "PATHSCOPE accounting_summary=FAIL "
            f"admitted_value_count={len(analyzer.admitted_values)} "
            f"member_count={len(analyzer.members)} "
            f"disposition_count={len(analyzer.dispositions)} "
            f"accounting_fault_count={len(fault_rows)}"
        )
    return [summary] + value_rows + member_rows + fault_rows


def _minimal_accounting_failure_records(analyzer: Analyzer) -> list[str]:
    if not analyzer.accounting_faults:
        analyzer.accounting_fault("accounting_boundary_exception")
    fault_rows = [
        (
            "ACCOUNTING_FAULT value_id=NONE member_id=NONE "
            f"reason={fault.reason}"
        )
        for fault in analyzer.accounting_faults
    ]
    summary = (
        "PATHSCOPE accounting_summary=FAIL "
        f"admitted_value_count={len(analyzer.admitted_values)} "
        f"member_count={len(analyzer.members)} "
        f"disposition_count={len(analyzer.dispositions)} "
        f"accounting_fault_count={len(fault_rows)}"
    )
    return [summary] + fault_rows


def reconcile_accounting_records(analyzer: Analyzer, records: list[str]) -> bool:
    summaries = [row for row in records if row.startswith("PATHSCOPE accounting_summary=")]
    values = [row for row in records if row.startswith("VALUE_ACCOUNT ")]
    members = [row for row in records if row.startswith("MEMBER ")]
    faults = [row for row in records if row.startswith("ACCOUNTING_FAULT ")]
    known_count = len(summaries) + len(values) + len(members) + len(faults)
    if known_count != len(records):
        analyzer.accounting_fault("printed_accounting_unknown_record")
        return False
    if not analyzer.admitted_values and not analyzer.accounting_faults:
        if records:
            analyzer.accounting_fault("printed_accounting_unexpected_for_empty_run")
            return False
        return True
    if len(summaries) != 1:
        analyzer.accounting_fault("printed_accounting_summary_cardinality_failed")
        return False
    summary_match = ACCOUNTING_SUMMARY_RE.fullmatch(summaries[0])
    if summary_match is None:
        analyzer.accounting_fault("printed_accounting_summary_malformed")
        return False
    state, value_count, member_count, disposition_count, fault_count = summary_match.groups()
    valid = (
        int(value_count) == len(analyzer.admitted_values)
        and int(member_count) == len(analyzer.members)
        and int(disposition_count) == len(analyzer.dispositions)
        and int(fault_count) == len(faults)
        and all(VALUE_ACCOUNT_RE.fullmatch(row) is not None for row in values)
        and all(MEMBER_RECORD_RE.fullmatch(row) is not None for row in members)
        and all(ACCOUNTING_FAULT_RE.fullmatch(row) is not None for row in faults)
    )
    if analyzer.accounting_faults:
        valid &= state == "FAIL" and len(faults) == len(analyzer.accounting_faults)
    else:
        valid &= (
            state == "OK"
            and not faults
            and len(values) == len(analyzer.admitted_values)
            and len(members) == len(analyzer.members)
            and len(members) == len(analyzer.dispositions)
            and len({VALUE_ACCOUNT_RE.fullmatch(row).group(1) for row in values}) == len(values)
            and len({MEMBER_RECORD_RE.fullmatch(row).group(1) for row in members}) == len(members)
        )
    if not valid:
        analyzer.accounting_fault("printed_accounting_reconciliation_failed")
    return valid


def output_report(shell: Path, rules: list[Rule], analyzer: Analyzer) -> int:
    uses = analyzer.uses
    issues = analyzer.issues
    tables: dict[str, dict[str, list[Use]]] = {"fs": {}, "net": {}}
    for use in uses:
        tables[use.domain].setdefault(use.value, []).append(use)
    provenance: list[Issue] = []
    for domain, table in tables.items():
        noun = "path" if domain == "fs" else "endpoint"
        for value, value_uses in table.items():
            allowlisted = all(
                any(rule.matches(value, use.primitive, domain) for rule in rules)
                for use in value_uses
            )
            if allowlisted:
                provenance.extend(
                    Issue(use.line, KIND_PROVENANCE,
                          f"allowlisted {noun} has no preregistered-constant provenance",
                          use.expression)
                    for use in value_uses if not use.sources and use.member_id is None
                )
    all_issues = sorted(
        set(issues + provenance),
        key=lambda item: (item.line, KIND_ORDER[item.kind], item.reason, item.expression),
    )
    counts = {kind: 0 for kind in KIND_ORDER}
    for item in all_issues:
        counts[item.kind] += 1
    forbidden = False
    projection_rows: list[str] = []
    # NIT-1 (r3 audit §5): both domains carry the same lexical-argv-scope claim,
    # so both allow verdicts read ALLOW-LEXICAL.  A bare ALLOW on the endpoint
    # row implied a stronger guarantee for network than for filesystem operands.
    for domain, label, allow in (("fs", "PATH", "ALLOW-LEXICAL"), ("net", "ENDPOINT", "ALLOW-LEXICAL")):
        table = tables[domain]
        for value in sorted(table):
            per_use = [
                [rule.render() for rule in rules if rule.matches(value, use.primitive, domain)]
                for use in table[value]
            ]
            allowed = all(per_use)
            matching = sorted({rendered for matches in per_use for rendered in matches})
            verdict = allow if allowed else "FORBID"
            forbidden |= not allowed
            evidence = sorted({f"line={use.line}:{use.primitive}" for use in table[value]})
            member_evidence = [
                f"member_id={use.member_id}"
                for use in table[value]
                if use.member_id is not None
            ]
            if member_evidence:
                evidence.extend(member_evidence)
            source_names = sorted({source for use in table[value] for source in use.sources})
            rule_text = matching[0] if allowed and matching else "-"
            source_text = ",".join(source_names) if source_names else "NONE"
            projection_rows.append(
                f"{label} value={value} verdict={verdict} rule={rule_text} "
                f"sources={source_text} uses={','.join(evidence)}"
            )
    unresolved_rows = [
        (
            f"UNRESOLVED line={item.line} kind={item.kind} reason={item.reason} "
            f"expression={item.expression}"
        )
        for item in all_issues
    ]

    for disposition in analyzer.dispositions:
        if disposition.candidate_domain not in {"fs", "net"} or disposition.candidate_value is None:
            continue
        matching_uses = [
            use
            for use in analyzer.uses
            if use.member_id == disposition.member_id
            and use.domain == disposition.candidate_domain
            and use.value == disposition.candidate_value
        ]
        marker = f"member_id={disposition.member_id}"
        if len(matching_uses) != 1 or sum(row.count(marker) for row in projection_rows) != 1:
            analyzer.accounting_fault(
                "member_projection_reconciliation_failed",
                disposition.value_id,
                disposition.member_id,
            )

    try:
        accounting_rows = _accounting_records(analyzer)
    except Exception:
        analyzer.accounting_fault("accounting_boundary_exception")
        accounting_rows = _minimal_accounting_failure_records(analyzer)
    if not reconcile_accounting_records(analyzer, accounting_rows):
        try:
            accounting_rows = _accounting_records(analyzer)
        except Exception:
            accounting_rows = _minimal_accounting_failure_records(analyzer)

    print(f"PATHSCOPE shell={shell}")
    print(SEMANTICS_LINE)
    print(
        f"PATHSCOPE resolved_fs_path_count={len(tables['fs'])} "
        f"resolved_net_endpoint_count={len(tables['net'])}"
    )
    print(
        f"PATHSCOPE unresolved_path_count={counts[KIND_PATH]} "
        f"unresolved_endpoint_count={counts[KIND_ENDPOINT]} "
        f"coverage_issue_count={counts[KIND_COVERAGE]} "
        f"provenance_issue_count={counts[KIND_PROVENANCE]} "
        f"parse_issue_count={counts[KIND_PARSE]}"
    )
    for row in projection_rows + unresolved_rows + accounting_rows:
        print(row)

    if analyzer.accounting_faults:
        print("PATHSCOPE verdict=REJECT rc=3 reason=accounting_invariant_failed")
        return RC_PARSE
    if all_issues:
        print("PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete")
        return RC_PARSE
    if any(
        item.disposition == DispositionKind.UNRESOLVED_FAIL_CLOSED
        for item in analyzer.dispositions
    ):
        print("PATHSCOPE verdict=REJECT rc=3 reason=member_resolution_incomplete")
        return RC_PARSE
    if forbidden or any(
        item.disposition == DispositionKind.FORBIDDEN_WITH_REASON
        for item in analyzer.dispositions
    ):
        print("PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist")
        return RC_FORBIDDEN
    print("PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shell", type=Path, help="complete Bash input to analyze")
    parser.add_argument("constants", type=Path, help="preregistered KEY=VALUE scalar table")
    parser.add_argument("allowlist", type=Path, help="one exact, terminal:, or /** rule per line")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        shell_text = args.shell.read_text(encoding="utf-8")
        env = parse_constants(args.constants)
        rules = parse_allowlist(args.allowlist, env)
    except (OSError, UnicodeError) as exc:
        print(f"PATHSCOPE verdict=REJECT rc=3 reason=input_read_error detail={exc}")
        return RC_PARSE
    except LexError as exc:
        print(f"PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line={exc.line} detail={exc}")
        return RC_PARSE
    analyzer = Analyzer(shell_text, env, rules)
    analyzer.run()
    return output_report(args.shell, rules, analyzer)


if __name__ == "__main__":
    raise SystemExit(main())
