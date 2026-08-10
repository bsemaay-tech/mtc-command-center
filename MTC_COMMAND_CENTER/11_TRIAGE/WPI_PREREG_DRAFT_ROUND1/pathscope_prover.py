#!/usr/bin/env python3
"""Conservative static path-scope prover for frozen Bash inputs.

The prover deliberately accepts a small, explicit scalar subset.  Anything that
could change a path without being statically known is a STOP (exit 3), not an
empty result or a guessed expansion.
"""

from __future__ import annotations

import argparse
import dataclasses
import posixpath
import re
import sys
import urllib.parse
from pathlib import Path


RC_FORBIDDEN = 1
RC_PARSE = 3
NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
ASSIGN_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", re.S)
NETWORK_RE = re.compile(r"^(?:\[[0-9A-Fa-f:]+\]|[A-Za-z0-9_.-]+):[0-9]{1,5}$")
GLOB_RE = re.compile(r"[*?[]")


@dataclasses.dataclass(frozen=True)
class Token:
    text: str
    line: int
    operator: bool = False


@dataclasses.dataclass(frozen=True)
class Value:
    text: str | None
    reason: str | None = None
    sources: frozenset[str] = frozenset()

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


@dataclasses.dataclass(frozen=True)
class Issue:
    line: int
    reason: str
    expression: str


@dataclasses.dataclass(frozen=True)
class Rule:
    kind: str
    value: str

    def matches(self, candidate: str, primitive: str) -> bool:
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


class ShellLexer:
    """Quote-aware lexer which keeps raw word spelling for safe expansion."""

    OPERATORS = (
        ";;&", "<<<", "<<-", "&>>", ">>", "<<", "&&", "||", ">&", "<&",
        "&>", "|&", ";;", ";&", "((", "))", "(", ")", "{", "}", ";",
        "|", "&", "<", ">", "!",
    )

    def __init__(self, text: str) -> None:
        self.text = text
        self.n = len(text)
        self.i = 0
        self.line = 1
        self.substitutions: list[tuple[int, str]] = []

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
                    elif "$" in body or "`" in body:
                        # Parameter fallbacks can execute substitutions even when
                        # the containing scalar never becomes a path.
                        nested = ShellLexer(body)
                        nested.tokens()
                        self.substitutions.extend(
                            (start_line + nested_line - 1, nested_body)
                            for nested_line, nested_body in nested.substitutions
                        )
                    return self.text[start:self.i]
                self.i += len(closing)
                continue
            self.i += 1
        raise LexError(start_line, f"unterminated {opening} expansion")

    def tokens(self) -> list[Token]:
        result: list[Token] = []
        buf: list[str] = []
        word_line = self.line
        quote: str | None = None
        escaped = False

        def flush() -> None:
            nonlocal buf
            if buf:
                result.append(Token("".join(buf), word_line))
                buf = []

        while self.i < self.n:
            c = self.text[self.i]
            if quote:
                if quote == '"' and self.text.startswith("$(", self.i):
                    if self.text.startswith("$((", self.i):
                        buf.append(self._balanced("$((", "))", command=False))
                    else:
                        buf.append(self._balanced("$(", ")", command=True))
                    continue
                if quote == '"' and self.text.startswith("${", self.i):
                    buf.append(self._balanced("${", "}", command=False))
                    continue
                if quote == '"' and c == "`":
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
                    buf.append(self.text[start:self.i])
                    self.substitutions.append((start_line, "".join(inner)))
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
            if self.text.startswith("$(", self.i):
                if not buf:
                    word_line = self.line
                if self.text.startswith("$((", self.i):
                    buf.append(self._balanced("$((", "))", command=False))
                else:
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
                buf.append(self.text[start:self.i])
                self.substitutions.append((start_line, "".join(inner)))
                continue
            if c == "\n":
                flush()
                result.append(Token("\n", self.line, True))
                self.line += 1
                self.i += 1
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
                fd_match = re.match(r"\{[A-Za-z_][A-Za-z0-9_]*\}", self.text[self.i:])
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
            op = next((item for item in self.OPERATORS if self.text.startswith(item, self.i)), None)
            if op:
                flush()
                result.append(Token(op, self.line, True))
                self.i += len(op)
                continue
            if not buf:
                word_line = self.line
            buf.append(c)
            self.i += 1
        if quote:
            raise LexError(word_line, f"unterminated {quote} quote")
        flush()
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


def expand_word(raw: str, env: dict[str, Value]) -> Value:
    out: list[str] = []
    sources: set[str] = set()
    i = 0
    quote: str | None = None
    while i < len(raw):
        c = raw[i]
        if quote == "'":
            if c == "'":
                quote = None
            else:
                out.append(c)
            i += 1
            continue
        if quote == '"':
            if c == '"':
                quote = None
                i += 1
                continue
            if c == "\\" and i + 1 < len(raw) and raw[i + 1] in '$`"\\\n':
                if raw[i + 1] != "\n":
                    out.append(raw[i + 1])
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
                    out.append(decode_ansi("".join(body)))
                except ValueError as exc:
                    return Value(None, str(exc))
                i = end + 1
                continue
            if c == "'":
                quote = "'"
                i += 1
                continue
            if c == '"':
                quote = '"'
                i += 1
                continue
            if c == "\\":
                if i + 1 >= len(raw):
                    return Value(None, "trailing escape")
                if raw[i + 1] != "\n":
                    out.append(raw[i + 1])
                i += 2
                continue

        if c == "`" or raw.startswith("$(", i):
            return Value(None, "command substitution")
        if raw.startswith("$((", i):
            return Value(None, "arithmetic expansion")
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
            if mode in (":-", "-") and (not value.known or (mode == ":-" and value.text == "")):
                value = expand_word(fallback or "", env)
            elif mode in (":?", "?") and not value.known:
                return Value(None, f"required variable {name} is unpinned")
            if not value.known:
                return value
            out.append(value.text or "")
            sources.update(value.sources)
            i = end + 1
            continue
        if c == "$":
            match = re.match(r"\$([A-Za-z_][A-Za-z0-9_]*)", raw[i:])
            if match:
                name = match.group(1)
                value = env.get(name, Value(None, f"unpinned variable {name}"))
                if not value.known:
                    return value
                out.append(value.text or "")
                sources.update(value.sources)
                i += len(match.group(0))
                continue
            if i + 1 < len(raw) and raw[i + 1] in "0123456789@*#?$!-":
                return Value(None, f"dynamic shell parameter ${raw[i + 1]}")
        out.append(c)
        i += 1
    if quote:
        return Value(None, "unterminated quote")
    return Value("".join(out), sources=frozenset(sources))


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
        env[name] = Value(value.text, sources=value.sources | frozenset({name}))
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
    if value.startswith("/"):
        return Value(posixpath.normpath(value))
    if value.startswith("./") or value.startswith("../") or value not in ("", "-"):
        cwd = env.get("PWD")
        if cwd and cwd.known and (cwd.text or "").startswith("/"):
            return Value(posixpath.normpath(posixpath.join(cwd.text or "", value)))
        return Value(None, "relative path depends on unpinned PWD")
    return Value(None, "empty path")


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
        if "://" in line:
            normalized = normalize_network(line)
            if not normalized.known:
                raise LexError(line_no, normalized.reason or "invalid network allowlist")
            kind, line = "network", normalized.text or ""
        elif NETWORK_RE.fullmatch(line):
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


class Analyzer:
    FS_ALL_ARGS = {
        "cat", "head", "tail", "wc", "sha256sum", "sha1sum", "md5sum", "touch",
        "mkdir", "rmdir", "rm", "unlink", "cp", "mv", "ln", "chmod", "chown",
        "chgrp", "realpath", "dirname", "basename", "du", "df", "file", "tar",
        "install", "truncate", "tee", "readlink",
    }
    NET_COMMANDS = {"curl", "wget", "nc", "ncat", "netcat", "ssh", "scp", "sftp"}
    NO_PATH_COMMANDS = {
        "alias", "bg", "bind", "caller", "compgen", "complete",
        "disown", "enable", "exit", "fc", "fg", "getent", "getopts", "hash", "help",
        "history", "id", "jobs", "kill", "let", "mapfile", "popd", "pushd", "read",
        "readarray", "shopt", "ss", "suspend", "systemctl", "times", "trap", "type",
        "ulimit", "umask", "unalias", "unset", "wait",
    }
    CONTROL = {
        "if", "then", "elif", "else", "fi", "for", "while", "until", "do", "done",
        "case", "in", "esac", "select", "function", "return", "break", "continue",
        "set", "shift", "true", "false", ":", "time", "coproc",
    }
    REDIRS = {"<", ">", ">>", "<<<", "<<", "<<-", "&>", "&>>", ">&", "<&"}
    SPLIT = {"\n", ";", ";;", ";&", ";;&", "&&", "||", "|", "|&", "&", "!", "(", ")", "{", "}", "((", "))"}

    def __init__(self, text: str, env: dict[str, Value]) -> None:
        self.text = text
        self.env = dict(env)
        self.pinned = set(env)
        self.uses: list[Use] = []
        self.issues: list[Issue] = []
        self.functions: set[str] = set(re.findall(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)\s*\{", text))

    def issue(self, line: int, reason: str, expression: str) -> None:
        item = Issue(line, reason, expression[:240])
        if item not in self.issues:
            self.issues.append(item)

    def record_path(self, raw: str, line: int, primitive: str) -> None:
        value = expand_word(raw, self.env)
        if not value.known:
            self.issue(line, value.reason or "unresolvable path", raw)
            return
        normalized = canonical_path(value.text or "", self.env)
        if not normalized.known:
            self.issue(line, normalized.reason or "unresolvable path", raw)
            return
        self.uses.append(Use(normalized.text or "", line, primitive, raw, value.sources))

    def record_network(self, raw: str, line: int, primitive: str) -> None:
        value = expand_word(raw, self.env)
        if not value.known:
            self.issue(line, value.reason or "unresolvable endpoint", raw)
            return
        normalized = normalize_network(value.text or "")
        if not normalized.known:
            self.issue(line, normalized.reason or "unresolvable endpoint", raw)
            return
        self.uses.append(Use(normalized.text or "", line, primitive, raw, value.sources))

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
                self.issue(token.line, f"script can override pinned constant {name}", token.text)
            return True
        self.env[name] = expand_word(rhs, self.env)
        return True

    def nonoption_operands(self, args: list[Token], option_values: set[str] | None = None) -> list[Token]:
        option_values = option_values or set()
        result: list[Token] = []
        take_value = False
        options = True
        for token in args:
            value = expand_word(token.text, self.env)
            rendered = value.text if value.known else token.text
            if take_value:
                take_value = False
                continue
            if options and rendered == "--":
                options = False
                continue
            key = (rendered or "").split("=", 1)[0]
            if options and key in option_values and "=" not in (rendered or ""):
                take_value = True
                continue
            if options and (rendered or "").startswith("-") and rendered != "-":
                continue
            result.append(token)
        return result

    def analyze_test(self, tokens: list[Token]) -> None:
        path_unary = {"-a", "-b", "-c", "-d", "-e", "-f", "-g", "-h", "-k", "-L", "-O", "-G", "-N", "-p", "-r", "-s", "-S", "-u", "-w", "-x"}
        for index, token in enumerate(tokens[:-1]):
            value = expand_word(token.text, self.env)
            if value.known and value.text in path_unary:
                self.record_path(tokens[index + 1].text, tokens[index + 1].line, "test")
        for index, token in enumerate(tokens):
            value = expand_word(token.text, self.env)
            if value.known and value.text in {"-nt", "-ot", "-ef"} and 0 < index < len(tokens) - 1:
                self.record_path(tokens[index - 1].text, tokens[index - 1].line, "test")
                self.record_path(tokens[index + 1].text, tokens[index + 1].line, "test")

    def analyze_wrapped(self, command: str, args: list[Token], line: int) -> None:
        if command == "env":
            index = 0
            while index < len(args):
                value = expand_word(args[index].text, self.env)
                rendered = value.text if value.known else args[index].text
                if rendered == "--":
                    index += 1
                    break
                if rendered in {"-i", "--ignore-environment", "-0", "--null"}:
                    index += 1
                    continue
                if (rendered or "").startswith("-"):
                    if rendered in {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"}:
                        if rendered in {"-C", "--chdir"} and index + 1 < len(args):
                            self.record_path(args[index + 1].text, args[index + 1].line, "env --chdir")
                        index += 2
                    else:
                        index += 1
                    continue
                if ASSIGN_RE.fullmatch(rendered or ""):
                    index += 1
                    continue
                break
            if index >= len(args):
                self.issue(line, "env wrapper has no statically visible command", "env")
                return
            self.analyze_command(args[index:])
            return
        if command == "timeout":
            operands = self.nonoption_operands(args, {"-k", "--kill-after", "-s", "--signal"})
            if len(operands) < 2:
                self.issue(line, "timeout wrapper command is not statically visible", "timeout")
                return
            self.analyze_command(operands[1:])
            return
        if command == "exec":
            operands = self.nonoption_operands(args, {"-a"})
            if operands:
                self.analyze_command(operands)
            return
        if command == "command":
            rendered = [expand_word(token.text, self.env) for token in args]
            if any(value.known and value.text in {"-v", "-V"} for value in rendered):
                return
            operands = self.nonoption_operands(args)
            if operands:
                self.analyze_command(operands)

    def analyze_command(self, tokens: list[Token]) -> None:
        if not tokens:
            return
        # Redirections are filesystem sinks regardless of the command.
        cleaned: list[Token] = []
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token.operator and token.text in self.REDIRS:
                if index + 1 >= len(tokens):
                    self.issue(token.line, "redirection has no target", token.text)
                    index += 1
                    continue
                target = tokens[index + 1]
                value = expand_word(target.text, self.env)
                rendered = value.text if value.known else target.text
                if token.text not in {">&", "<&"} or not re.fullmatch(r"-?|[0-9]+", rendered or ""):
                    if token.text == "<<<":
                        pass  # here-string data is not a filesystem path
                    elif token.text in {"<<", "<<-"}:
                        self.issue(token.line, "here input is outside the accepted static path subset", target.text)
                    else:
                        self.record_path(target.text, target.line, f"redirection {token.text}")
                index += 2
                continue
            # File-descriptor prefixes such as 2> and {fd}< are not arguments.
            if index + 1 < len(tokens) and tokens[index + 1].operator and tokens[index + 1].text in self.REDIRS:
                if re.fullmatch(r"[0-9]+|\{[A-Za-z_][A-Za-z0-9_]*\}", token.text):
                    index += 1
                    continue
            cleaned.append(token)
            index += 1
        tokens = cleaned
        if not tokens:
            return

        index = 0
        while index < len(tokens) and self.assignment(tokens[index]):
            index += 1
        if index >= len(tokens):
            return
        if tokens[index].text in {"local", "declare", "typeset", "export", "readonly"}:
            for token in tokens[index + 1:]:
                if token.text.startswith("-"):
                    continue
                if not self.assignment(token) and NAME_RE.fullmatch(token.text) and token.text not in self.env:
                    self.env[token.text] = Value(None, f"declared variable {token.text} has no static value")
            return

        command_value = expand_word(tokens[index].text, self.env)
        if not command_value.known:
            self.issue(tokens[index].line, f"dynamic command name: {command_value.reason}", tokens[index].text)
            return
        command = self._basename(command_value.text or "")
        args = tokens[index + 1:]
        if command in self.CONTROL or command in self.NO_PATH_COMMANDS or command in {"printf", "echo"}:
            return
        if command == "eval":
            self.issue(tokens[index].line, "eval is forbidden", " ".join(t.text for t in tokens))
            return
        if command in {"source", "."}:
            self.issue(tokens[index].line, "sourced values are outside the closed scalar input set", command)
            for operand in self.nonoption_operands(args):
                self.record_path(operand.text, operand.line, command)
            return
        if command in {"env", "timeout", "exec", "command"}:
            self.analyze_wrapped(command, args, tokens[index].line)
            return
        if command in {"test", "[", "[["}:
            self.analyze_test(args)
            return
        if command == "stat":
            for operand in self.nonoption_operands(args, {"-c", "--format", "--printf"}):
                self.record_path(operand.text, operand.line, command)
            return
        if command == "find":
            for operand in self.nonoption_operands(args):
                value = expand_word(operand.text, self.env)
                rendered = value.text if value.known else operand.text
                if (rendered or "").startswith(("/", "./", "../")):
                    self.record_path(operand.text, operand.line, command)
                else:
                    break
            return
        if command in self.FS_ALL_ARGS or command == "cd":
            option_values = {
                "tar": {"-C", "--directory", "-f", "--file", "-T", "--files-from"},
                "install": {"-m", "--mode", "-o", "--owner", "-g", "--group"},
                "head": {"-n", "--lines", "-c", "--bytes"},
                "tail": {"-n", "--lines", "-c", "--bytes", "-s", "--sleep-interval"},
            }.get(command, set())
            for operand in self.nonoption_operands(args, option_values):
                self.record_path(operand.text, operand.line, command)
            return
        if command == "curl":
            path_options = {"-o", "--output", "--cookie", "--cookie-jar", "--cert", "--key", "--cacert", "--capath", "--config", "-K"}
            skip_options = {"-X", "--request", "-w", "--write-out", "--connect-timeout", "--max-time", "-H", "--header", "-d", "--data", "--data-raw", "--retry"}
            take: str | None = None
            for token in args:
                value = expand_word(token.text, self.env)
                rendered = value.text if value.known else token.text
                if take == "path":
                    self.record_path(token.text, token.line, command)
                    take = None
                    continue
                if take == "skip":
                    take = None
                    continue
                key = (rendered or "").split("=", 1)[0]
                if key in path_options:
                    if "=" in (rendered or ""):
                        raw = token.text.split("=", 1)[1]
                        self.record_path(raw, token.line, command)
                    else:
                        take = "path"
                    continue
                if key in skip_options:
                    if "=" not in (rendered or ""):
                        take = "skip"
                    continue
                if (rendered or "").startswith("-") or rendered == "--":
                    continue
                self.record_network(token.text, token.line, command)
            return
        if command in self.NET_COMMANDS:
            for operand in self.nonoption_operands(args):
                value = expand_word(operand.text, self.env)
                if value.known and ("://" in (value.text or "") or NETWORK_RE.fullmatch(value.text or "")):
                    self.record_network(operand.text, operand.line, command)
                elif command in {"scp", "sftp"}:
                    self.issue(operand.line, "remote-path grammar needs an explicit transport parser", operand.text)
            return
        if command.startswith("python"):
            # Inline Python is opaque; every post-code path-like argv is captured,
            # while an unresolved argv is a STOP.
            after_code = False
            for arg_index, token in enumerate(args):
                value = expand_word(token.text, self.env)
                rendered = value.text if value.known else ""
                if after_code:
                    if not value.known:
                        self.issue(token.line, value.reason or "opaque interpreter argv", token.text)
                    elif rendered.startswith(("/", "./", "../")):
                        self.record_path(token.text, token.line, command)
                    continue
                if rendered == "-c" and arg_index + 1 < len(args):
                    after_code = True
            return
        if command in self.functions:
            # Function bodies are scanned separately. Positional dataflow is not
            # guessed; any path use of $1/$2 in the body is reported there.
            return
        # An opaque command receiving a path/endpoint could itself be a wrapper.
        self.issue(tokens[index].line, f"opaque command {command} has no registered path-argument contract", command)
        for token in args:
            value = expand_word(token.text, self.env)
            rendered = value.text if value.known else ""
            if not value.known and ("$" in token.text or "`" in token.text):
                self.issue(token.line, f"opaque command argument: {value.reason}", token.text)
            elif rendered.startswith(("/", "./", "../")) or "://" in rendered or NETWORK_RE.fullmatch(rendered):
                self.issue(token.line, f"opaque command {command} may forward a path or endpoint", token.text)

    def analyze_tokens(self, tokens: list[Token]) -> None:
        command: list[Token] = []
        for token in tokens:
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
                    self.issue(token.line, "unclosed [[ test", "[[")
                continue
            if not token.operator and token.text in {"for", "select"}:
                if index + 1 < len(tokens) and not tokens[index + 1].operator and NAME_RE.fullmatch(tokens[index + 1].text):
                    self.env[tokens[index + 1].text] = Value(None, f"loop variable {tokens[index + 1].text} is dynamic")
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
                    self.issue(start_line, "loop header has no do terminator", token.text)
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
                    self.issue(start_line, "unclosed arithmetic command", "((")
                else:
                    self.issue(start_line, "arithmetic command is outside the accepted scalar subset", "((...))")
                result.append(Token("\n", start_line, True))
                continue
            if not token.operator and token.text in separators:
                result.append(Token("\n", token.line, True))
                index += 1
                continue
            if not token.operator and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*\+=", token.text):
                self.issue(token.line, "compound assignment is outside the accepted scalar subset", token.text)
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
                self.issue(tokens[index].line, "unclosed function body", tokens[index].text)
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
            self.issue(exc.line, str(exc), "shell input")
            return self.uses, self.issues
        for left, right in zip(tokens, tokens[1:]):
            if (
                not left.operator
                and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=", left.text)
                and right.operator and right.text == "("
            ):
                self.issue(left.line, "array assignment is outside the accepted scalar subset", left.text + "(...)")
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
                    self.issue(token.line, "unmatched shell keyword esac", token.text)
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
                    self.issue(token.line, f"unmatched shell delimiter {token.text}", token.text)
                else:
                    stack.pop()
        for token in stack:
            self.issue(token.line, f"unclosed shell delimiter {token.text}", token.text)
        if case_depth:
            self.issue(tokens[-1].line if tokens else 1, "unclosed shell keyword case", "case")
        normalized = self.normalize_control_tokens(self.strip_case_patterns(tokens))
        self.analyze_functions_and_top_level(normalized)
        for line, body in lexer.substitutions:
            nested = Analyzer(body, self.env)
            nested.run()
            self.uses.extend(dataclasses.replace(use, line=line + use.line - 1) for use in nested.uses)
            self.issues.extend(dataclasses.replace(issue, line=line + issue.line - 1) for issue in nested.issues)
        return self.uses, self.issues


def output_report(shell: Path, rules: list[Rule], uses: list[Use], issues: list[Issue]) -> int:
    by_value: dict[str, list[Use]] = {}
    for use in uses:
        by_value.setdefault(use.value, []).append(use)
    provenance_issues: list[Issue] = []
    for value, value_uses in by_value.items():
        allowlisted = all(any(rule.matches(value, use.primitive) for rule in rules) for use in value_uses)
        if allowlisted:
            provenance_issues.extend(
                Issue(use.line, "allowlisted path has no preregistered-constant provenance", use.expression)
                for use in value_uses if not use.sources
            )
    all_issues = sorted(set(issues + provenance_issues), key=lambda item: (item.line, item.reason, item.expression))
    print(f"PATHSCOPE shell={shell}")
    print(f"PATHSCOPE resolved_count={len(by_value)} unresolved_count={len(all_issues)}")
    forbidden = False
    for value in sorted(by_value):
        per_use = [
            [rule.render() for rule in rules if rule.matches(value, use.primitive)]
            for use in by_value[value]
        ]
        allowed = all(per_use)
        matching = sorted({rendered for matches in per_use for rendered in matches})
        verdict = "ALLOW" if allowed else "FORBID"
        forbidden |= not allowed
        evidence = sorted({f"line={use.line}:{use.primitive}" for use in by_value[value]})
        source_names = sorted({source for use in by_value[value] for source in use.sources})
        rule_text = matching[0] if allowed and matching else "-"
        source_text = ",".join(source_names) if source_names else "NONE"
        print(f"PATH value={value} verdict={verdict} rule={rule_text} sources={source_text} uses={','.join(evidence)}")
    for issue in all_issues:
        print(f"UNRESOLVED line={issue.line} reason={issue.reason} expression={issue.expression}")
    if all_issues:
        print("PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete")
        return RC_PARSE
    if forbidden:
        print("PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist")
        return RC_FORBIDDEN
    print("PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted")
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
    uses, issues = Analyzer(shell_text, env).run()
    return output_report(args.shell, rules, uses, issues)


if __name__ == "__main__":
    raise SystemExit(main())
