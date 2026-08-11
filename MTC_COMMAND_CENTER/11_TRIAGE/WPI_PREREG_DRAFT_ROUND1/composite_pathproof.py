#!/usr/bin/env python3
"""Fail-closed Section 10.2 composite path proof.

The three ordered stages are deliberately separate:

* ALLOCATE closes allocation values and declared component identities.
* RENDER proves byte-exact materialisation and derives the source graph.
* FREEZE verifies frozen identities and invokes the separately repaired lexical
  path-scope prover for every reachable shell member.

The tool reads subject bytes as data.  It never executes a subject shell file.
"""

from __future__ import annotations

import argparse
import dataclasses
import enum
import hashlib
import json
import posixpath
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Protocol, Sequence


SCHEMA = "sec102-composite-plan-v1"
RC_PASS = 0
RC_FAIL = 1
RC_STOP = 3
APPROVED_PROVER_BYTES = 122446
APPROVED_PROVER_SHA256 = "890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d"

SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
PLACEHOLDER_RE = re.compile(r"<[^>]*>|\{\{[^}]*\}\}|\$\{[^}]*\}")
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")

PLAN_KEYS = frozenset({"schema", "stage", "composites"})
COMPOSITE_KEYS = frozenset(
    {
        "id",
        "entrypoint",
        "members",
        "edges",
        "allocation_requirements",
        "allocations",
    }
)
COMPOSITE_PROOF_KEYS = COMPOSITE_KEYS | frozenset({"proof"})
MEMBER_KEYS = frozenset({"id", "kind", "path"})
# RENDER and FREEZE derive the graph from bytes, so each member must additionally
# declare the absolute path it is deployed at and referenced by.  ALLOCATE derives
# nothing from bytes and keeps the round-1 member contract unchanged.
MEMBER_PROOF_KEYS = MEMBER_KEYS | frozenset({"deploy_path"})
EDGE_KEYS = frozenset({"from", "to", "kind"})
REQUIREMENT_KEYS = frozenset({"name", "kind", "consumers"})
ALLOCATION_KEYS = frozenset({"name", "value"})
RENDER_PROOF_KEYS = frozenset({"render_templates"})
RENDER_TEMPLATE_KEYS = frozenset({"member", "template"})
FREEZE_PROOF_KEYS = frozenset(
    {
        "member_pins",
        "constants",
        "constants_bytes",
        "constants_sha256",
        "allowlist",
        "allowlist_bytes",
        "allowlist_sha256",
        "prover",
        "prover_bytes",
        "prover_sha256",
    }
)
MEMBER_PIN_KEYS = frozenset({"member", "bytes", "sha256"})
MEMBER_KINDS = frozenset({"shell", "python_source"})
EDGE_KINDS = frozenset({"source", "execute_source", "inline_source"})
ALLOCATION_KINDS = frozenset({"safe_component", "absolute_path"})
RENDER_TOKEN_RE = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_COMMAND_RE = re.compile(
    r"(?:^|[;|&()])\s*(source|\.)\s+((?:'[^']*'|\"[^\"]*\"|[^\s;|&()]+))",
    re.MULTILINE,
)
EXEC_COMMAND_RE = re.compile(
    r"(?:^|[;|&()])\s*((?:/[^\s;|&()]+/)?(?:bash|sh|python(?:3(?:\.\d+)?)?))\s+"
    r"((?:'[^']*'|\"[^\"]*\"|[^\s;|&()]+))",
    re.MULTILINE,
)
# Mirrors pathscope_prover.ASSIGN_RE over a stripped, non-comment, non-empty line.
CONSTANT_ASSIGN_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", re.S)

# --- command-prefix conservation (round-5 R4-F1) ------------------------------
# Bash's command grammar lets a simple command carry a prefix before its command
# word: any number of assignment words and redirections, in any order.  A prefix
# does NOT open or close a command position - `A=1 2>err arr[0]=2 {fd}<in source lib`
# still looks up `source` as the command name.  Round 4 conserved the command
# position across scalar assignments and numeric file descriptors only, so a valid
# named-descriptor or indexed-assignment prefix was emitted as a benign leaf that
# closed the command position and hid the command word behind it (defect patterns
# 5/9/12).  The three expressions below model the whole accepted prefix vocabulary,
# and `_redirection_prefix_class` / `_assignment_prefix_class` STOP on any prefix
# shape outside it rather than letting it degrade into a leaf.
#
# An assignment word is `NAME=`, `NAME+=`, `NAME[subscript]=` or `NAME[subscript]+=`.
# Bash requires the NAME to be unquoted and to start the word, so a word that does
# not start that way (`2a=b`, `a-b=c`, `"a"=b`, `--opt=val`) is exactly a command
# name, not an assignment - those stay leaves and that is not an approximation.
SHELL_ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\[[^][]*\])?\+?=")
# A word that opens a subscript the expression above could not close - a nested or
# otherwise unmodelled subscript such as `arr[idx[0]]=1`.  Only a word that also
# carries an `=` can be an assignment at all, so requiring one costs no soundness.
SHELL_SUBSCRIPT_PREFIX_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\[")
# The two file-descriptor prefix forms, recognised only when the word abuts the
# redirection operator with no separating blank, which is what Bash requires.
NUMERIC_FD_PREFIX_RE = re.compile(r"^[0-9]+$")
NAMED_FD_PREFIX_RE = re.compile(r"^\{[A-Za-z_][A-Za-z0-9_]*\}$")
# The function-definition NAME (round-7 R6-F1).  Only two constructs put a `(`
# immediately after a word: a function definition, which Bash requires to be a NAME,
# and an option-enabled pathname pattern, which Bash requires to carry an operator
# character (`?`, `*`, `+`, `@`, `!`) immediately before the `(`.  A NAME can never
# end in one of those, so the two are decidable apart without knowing which shell
# options are set.  `_shell_words` uses this to decide whether an abutting `(` is a
# word separator or a character of the word itself.
SHELL_FUNCTION_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# --- independent command-word detection (round-4 R3-F1) ----------------------
# SOURCE_COMMAND_RE / EXEC_COMMAND_RE above are the *derivation* grammar: what the
# composite can turn into an edge.  The three sets below are the *detection*
# vocabulary, and detection is deliberately strictly broader than derivation.  A
# command word this vocabulary recognises but the derivation grammar did not match
# is a STOP, never a silent absence.  Round 3 counted coverage with a second regex
# built from the same narrow grammar as the matcher, so any form invisible to the
# matcher was equally invisible to its own coverage check (defect patterns 5/12).
#
# These sets decide which PROVEN-STATIC command words derive edges.  They are not
# the fence: since round 7 an unrecognised word is a benign leaf only when every
# character of it is in the safe set (see COMMAND_WORD_STATIC_RE), so a word outside
# these sets can no longer hide an interpreter behind an expansion of any kind.
# What the sets still bound is the disclosed residual: the VOCABULARY is a list of
# recognised interpreters, not a proof that the list is exhaustive.
GRAPH_SOURCE_WORDS = frozenset({"source", "."})
GRAPH_INTERPRETER_WORDS = frozenset(
    {
        "sh", "bash", "rbash", "dash", "ash", "ksh", "ksh88", "ksh93", "mksh",
        "pdksh", "posh", "yash", "zsh", "csh", "tcsh", "fish", "busybox",
        "python", "python2", "python3", "perl", "ruby", "node", "nodejs",
        "php", "lua", "tclsh", "wish", "expect", "awk", "gawk", "mawk", "nawk",
    }
)
GRAPH_INTERPRETER_VERSION_RE = re.compile(
    r"^(?:python|perl|ruby|node|php|lua|tclsh)\d+(?:\.\d+)*$"
)
# Words that run a command supplied as one of their own operands.  The composite
# does not model any of them, so their mere presence at a command position is a STOP.
GRAPH_WRAPPER_WORDS = frozenset(
    {
        "command", "builtin", "exec", "eval", "alias", "unalias", "trap", "env",
        "nohup", "nice", "ionice", "setsid", "stdbuf", "time", "timeout", "xargs",
        "sudo", "doas", "su", "runuser", "chroot", "unbuffer", "flock", "watch",
        "script", "parallel", "find",
    }
)
# Reserved words that end one command and re-open a command position on the same
# line.  They are not commands themselves, so they are not classified; what matters
# is that the word after them is still scanned as a command word.
SHELL_CONTROL_WORDS = frozenset(
    {
        "if", "then", "elif", "else", "fi", "while", "until", "do", "done",
        "case", "esac", "in", "for", "select", "function", "coproc",
        "{", "}", "!", "[[", "]]",
    }
)
# Reserved words whose next word binds a NAME rather than running as a command:
# `function foo { source lib; }` and `coproc foo { source lib; }`.  Round 4 let that
# name close the command position, so the first command word of the body was never
# scanned - the same silent loss as an unconserved prefix, reached through a
# reserved word instead.  The command position survives the bound name instead.
# `for`/`select`/`case` also bind a name, but a separator, newline or `)` always
# re-opens the command position before their body, so no command word is lost there.
SHELL_NAME_BINDING_WORDS = frozenset({"function", "coproc"})

# --- closed command-word admissibility (round-6 R5-F1, round-7 R6-F1) ---------
# Rounds 4 and 5 each closed ONE command-word form after it was found: a numeric
# file descriptor, then a named descriptor, then an indexed assignment.  The round-5
# audit then found a fourth - a pathname-expanded command word that Bash can resolve
# to a recognised interpreter, leafed, with the following script operand scanned by
# nothing.  Closing forms one at a time is not a fixpoint, because the classifier's
# default was "benign leaf" and every form nobody had thought of inherited it.
#
# The default is now inverted.  A command word is admissible as a benign non-edge
# leaf ONLY when it is a PROVEN-STATIC literal that is not a recognised interpreter
# or source builtin: one word whose spelling is exactly the name Bash will look up,
# with no expansion of any kind between the two.  Every command word that is
# dynamic, expandable or substituted is UNMODELED and the stage STOPs; it can never
# become a leaf, whatever it would have expanded to.  This is the same fail-closed
# principle round 5 applied to command PREFIXES, extended to the command word itself.
#
# `$` and backtick introduce parameter, command and arithmetic expansion; a word
# carrying either is dynamic.  `_graph_opaque_reason` already STOPs on most of these
# at the whole-text level, and the check below is deliberately redundant with it, so
# no single fence carries the class alone.
COMMAND_WORD_SUBSTITUTION_RE = re.compile(r"[$`]")
# --- the safe set: a WHITELIST, not a blacklist (round-7 R6-F1) ---------------
# Round 6 fenced the *remaining* expansions by listing their operator characters
# (`*`, `?`, `[`, `]`, `{`, `}`, `~`, `\`).  The round-6 audit then found the
# `extglob` family - one-or-more `+(`, exactly-one `@(`, zero-or-one `?(` and
# negated `!(` - of which only `?(` and `*(` carry a listed character.  `ba+(s)h`,
# `ba@(s)h` and `ba!(x)h` all pathname-resolve to `bash` with `extglob` enabled and
# every one of them was admitted as a benign leaf.
#
# That is not a missing entry, it is the wrong direction of proof.  A blacklist of
# operators is complete only if the list is complete, and the list is exactly what
# nobody can close: `extglob` was missed, and any option-enabled or rarely-used
# operator nobody has thought of would be missed the same way.  Round 7 inverts the
# test.  A command word is PROVEN-STATIC only when EVERY character of the raw
# (pre-expansion) word token is in the safe set below.  Any other character - known
# operator, unknown operator, or a character with no shell meaning at all - makes the
# word NOT proven-static, so it is UNMODELED and the stage STOPs.  The default for an
# unrecognised character is refusal, which is what makes this a fixpoint: a form this
# round never anticipated cannot be admitted by not having been listed.
#
# THE SAFE SET IS `[A-Za-z0-9._/:-]`, and each member is admitted because it cannot
# introduce pathname, brace, tilde, parameter, command or arithmetic expansion,
# process substitution, or quote-removal-driven resolution, in any position of a
# command word, under any shell option:
#
#   A-Z a-z 0-9  Ordinary characters.  Not metacharacters, not expansion operators,
#                not quoting characters; they can only spell a name.
#   `.`          An ordinary pathname character.  The one-character word `.` is the
#                source builtin and is classified by GRAPH_SOURCE_WORDS below, before
#                any word can be admitted as a leaf.
#   `_`          An ordinary pathname and NAME character.  Special only as the
#                variable `_`, which requires a `$` that this set does not admit.
#   `-`          Ordinary.  A leading `-` makes an option word, not an expansion.
#                Special only inside `${var-alt}`, which requires `$` and `{`.
#   `/`          The pathname separator.  It suppresses PATH, function and builtin
#                lookup rather than introducing expansion, and the classifier already
#                takes the last pathname component of any word containing one.
#   `:`          Ordinary; the one-character word `:` is the null builtin.  Special
#                only inside `${var:-alt}`, which requires `$` and `{`.
#
# Deliberately NOT in the safe set, and each exclusion is load-bearing rather than
# cautious: `?`, `*`, `+`, `@` and `!` are the five `extglob` operator characters, so
# excluding all five refuses the whole family in one rule instead of by enumeration -
# this is the round-6 finding.  `%` introduces job-specification resolution when job
# control is enabled, an option state the composite does not model.  `=` selects
# `equals` expansion in shells that implement it, and every assignment word Bash does
# recognise is classified before this test, so admitting `=` would buy nothing.  `'`
# and `"` build a name out of quote removal rather than spelling it, and `,`, `^`,
# `#`, `+` and every other printable character is refused simply because no proof was
# offered that it cannot resolve - which is the entire point of the inversion.
#
# The kickoff's illustrative set `[A-Za-z0-9._/+=:@%-]` was tested against the
# round-6 finding and does NOT close it: `+` and `@` are two of the five `extglob`
# operators, so `ba+(s)h` and `ba@(s)h` stay benign leaves under it.  That
# measurement is published as a mutation discriminator rather than argued.
#
# Applied to the raw word including quoted regions, for the round-6 reason: quoting
# suppresses some expansions, but a proof that this particular occurrence is
# suppressed is exactly the reasoning this policy refuses to do.  Reserved words
# (`{`, `}`, `[[`, `]]`, `!`) and assignment prefixes are matched before this fence
# and are therefore unaffected.
COMMAND_WORD_SAFE_SET = "A-Z a-z 0-9 . _ - / :"
COMMAND_WORD_STATIC_RE = re.compile(r"^[A-Za-z0-9._/:-]+$")

ALLOCATE_CLAIMS = (
    ("A1", "plan_contract", "closed_schema_and_allocate_order"),
    ("A2", "declared_entrypoint_discovery", "one_declared_entrypoint_per_composite"),
    (
        "A3",
        "allocation_plan_conservation",
        "declared_requirements_allocations_and_consumer_references_conserved",
    ),
    ("A4", "allocation_value_closure", "allocated_values_closed_and_well_formed"),
    ("A5", "declared_graph_conservation", "all_declared_members_reachable_once"),
    ("A6", "component_identity", "all_member_bytes_locally_identified"),
)

RENDER_CLAIMS = (
    ("R1", "render_plan_contract", "closed_schema_and_render_order"),
    ("R2", "render_template_conservation", "one_template_per_input_member"),
    ("R3", "allocation_materialisation", "every_declared_consumer_materialised_byte_exact"),
    ("R4", "derived_source_graph", "rendered_bytes_derive_the_declared_reachable_graph"),
    ("R5", "rendered_component_identity", "all_rendered_member_bytes_identified"),
    ("R6", "render_member_conservation", "every_input_member_has_one_terminal_disposition"),
    (
        "R7",
        "deployed_identity_binding",
        "every_derived_operand_equals_one_declared_member_deployed_path",
    ),
)

FREEZE_CLAIMS = (
    ("F1", "freeze_plan_contract", "closed_schema_and_freeze_order"),
    ("F2", "frozen_component_identity", "all_member_and_proof_input_pins_match"),
    ("F3", "derived_whole_program_graph", "all_members_reachable_in_derived_graph"),
    ("F4", "prover_component_identity", "repaired_prover_identity_pinned"),
    ("F5", "prover_output_conservation", "seven_counts_and_records_reconciled"),
    ("F6", "lexical_pathscope_disposition", "every_prover_result_terminal_and_fail_closed"),
    ("F7", "residual_disclosure", "symlink_and_mount_limits_carried_as_disclosures"),
    ("F8", "freeze_member_conservation", "every_input_member_has_one_terminal_disposition"),
    (
        "F9",
        "deployed_identity_binding",
        "every_derived_operand_equals_one_declared_member_deployed_path",
    ),
    (
        "F10",
        "allocation_constants_reconciliation",
        # Narrowed in round 4 to exactly what the predicate proves: every declared
        # allocation is byte-equal to a pinned constant, and every pinned constant is
        # either reconciled or explicitly carried as a runtime-only disclosure.  The
        # round-3 wording claimed one conserved universe while a plan-only allocation
        # could have no constants-side disposition at all.
        "every_plan_allocation_reconciled_and_every_pinned_constant_dispositioned",
    ),
)

class Verdict(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    STOP = "STOP"

    @property
    def rc(self) -> int:
        return {Verdict.PASS: RC_PASS, Verdict.FAIL: RC_FAIL, Verdict.STOP: RC_STOP}[self]


VERDICT_PRIORITY = {Verdict.PASS: 0, Verdict.FAIL: 1, Verdict.STOP: 2}


class Stage(enum.Enum):
    ALLOCATE = "allocate"
    RENDER = "render"
    FREEZE = "freeze"


CLAIMS_BY_STAGE = {
    Stage.ALLOCATE: ALLOCATE_CLAIMS,
    Stage.RENDER: RENDER_CLAIMS,
    Stage.FREEZE: FREEZE_CLAIMS,
}


class InputStop(Exception):
    """The plan cannot be evaluated as the declared schema."""

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(detail)
        self.reason = reason
        self.detail = detail


class DuplicateKeyStop(InputStop):
    pass


@dataclasses.dataclass(frozen=True)
class Member:
    member_id: str
    kind: str
    path: str
    # Absolute canonical POSIX path the member is deployed at and referenced by.
    # Empty only at ALLOCATE, which declares no deployed identity.
    deploy_path: str


@dataclasses.dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str


@dataclasses.dataclass(frozen=True)
class AllocationRequirement:
    name: str
    kind: str
    consumers: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class Allocation:
    name: str
    value: str


@dataclasses.dataclass(frozen=True)
class RenderTemplate:
    member_id: str
    template_path: str


@dataclasses.dataclass(frozen=True)
class MemberPin:
    member_id: str
    byte_count: int
    sha256: str


@dataclasses.dataclass(frozen=True)
class RenderProof:
    templates: tuple[RenderTemplate, ...]


@dataclasses.dataclass(frozen=True)
class FreezeProof:
    member_pins: tuple[MemberPin, ...]
    constants_path: str
    constants_bytes: int
    constants_sha256: str
    allowlist_path: str
    allowlist_bytes: int
    allowlist_sha256: str
    prover_path: str
    prover_bytes: int
    prover_sha256: str


@dataclasses.dataclass(frozen=True)
class Composite:
    composite_id: str
    entrypoint: str
    members: tuple[Member, ...]
    edges: tuple[Edge, ...]
    requirements: tuple[AllocationRequirement, ...]
    allocations: tuple[Allocation, ...]
    proof: RenderProof | FreezeProof | None


@dataclasses.dataclass(frozen=True)
class Plan:
    schema: str
    stage: Stage
    composites: tuple[Composite, ...]


@dataclasses.dataclass
class ConstantBinding:
    line: int
    name: str
    value: str | None
    disposition: str = "UNRESOLVED"
    reason: str = "unreconciled"


@dataclasses.dataclass
class AllocationBinding:
    """One terminal constants-side disposition for one declared plan allocation.

    Round 3 created rows only while walking the constants table, so a plan
    allocation the table never mentions had no row and no F10 failure while F10
    still claimed the two inputs were one conserved universe (defect patterns 9/13).
    """

    index: int
    name: str
    value: str
    disposition: str = "UNRESOLVED"
    reason: str = "unreconciled"


@dataclasses.dataclass(frozen=True)
class ShellWord:
    """One unquoted, comment-free word of a rendered shell member.

    `command_position` is True when the shell would look this word up as a command
    name: at the start of a line or list, after a separator or a reserved word, and
    after any run of variable assignments.
    """

    offset: int
    text: str
    command_position: bool


@dataclasses.dataclass(frozen=True)
class ShellMember:
    member_id: str
    logical_path: str
    deploy_path: str
    data: bytes


@dataclasses.dataclass(frozen=True)
class PathProofRequest:
    stage: Stage
    composite_id: str
    shell_members: tuple[ShellMember, ...]
    entrypoint: str
    edges: tuple[Edge, ...]
    allocations: tuple[Allocation, ...]
    constants_values: tuple[tuple[str, str], ...]
    constants_data: bytes
    allowlist_data: bytes
    prover_data: bytes


@dataclasses.dataclass(frozen=True)
class PathProofResult:
    verdict: Verdict
    reason: str
    member_results: tuple["ProverMemberResult", ...]
    residuals: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class ProverMemberResult:
    member_id: str
    verdict: Verdict
    reason: str
    process_rc: int | None
    resolved_fs_path_count: int
    resolved_net_endpoint_count: int
    unresolved_path_count: int
    unresolved_endpoint_count: int
    coverage_issue_count: int
    provenance_issue_count: int
    parse_issue_count: int
    terminal_record: str
    records: tuple[str, ...]


class PathProver(Protocol):
    """Swappable boundary; no unrepaired prover implementation is depended on."""

    def prove(self, request: PathProofRequest) -> PathProofResult:
        ...


@dataclasses.dataclass
class ClaimState:
    claim_id: str
    name: str
    pass_reason: str
    verdict: Verdict = Verdict.PASS
    reasons: set[str] = dataclasses.field(default_factory=set)

    def record(self, verdict: Verdict, reason: str) -> None:
        if verdict is Verdict.PASS:
            return
        self.reasons.add(reason)
        if VERDICT_PRIORITY[verdict] > VERDICT_PRIORITY[self.verdict]:
            self.verdict = verdict

    def render_reason(self) -> str:
        if not self.reasons:
            return self.pass_reason
        return ",".join(sorted(self.reasons))


@dataclasses.dataclass
class MemberState:
    composite_id: str
    index: int
    member: Member
    graph: str = "UNRESOLVED"
    identity: str = "UNRESOLVED"
    size: int | None = None
    sha256: str | None = None

    @property
    def disposition(self) -> str:
        if "STOP" in (self.graph, self.identity):
            return "STOP"
        if "FAIL" in (self.graph, self.identity):
            return "FAIL"
        if self.graph == "REACHABLE" and self.identity == "IDENTIFIED":
            return "ACCEPT"
        return "STOP"


@dataclasses.dataclass
class Row:
    row_type: str
    fields: tuple[tuple[str, Any], ...]

    def render(self) -> str:
        encoded = " ".join(f"{key}={json.dumps(value, ensure_ascii=True)}" for key, value in self.fields)
        return f"{self.row_type} {encoded}"


class Recorder:
    def __init__(self, stage: Stage) -> None:
        self.claim_order = tuple(claim_id for claim_id, _, _ in CLAIMS_BY_STAGE[stage])
        self.claims = {
            claim_id: ClaimState(claim_id, name, reason)
            for claim_id, name, reason in CLAIMS_BY_STAGE[stage]
        }
        self.rows: list[Row] = []

    def record(self, claim_id: str, verdict: Verdict, reason: str) -> None:
        self.claims[claim_id].record(verdict, reason)

    def add_row(self, row_type: str, **fields: Any) -> None:
        self.rows.append(Row(row_type, tuple(fields.items())))

    def stop_all(self, reason: str) -> None:
        for claim_id in self.claims:
            self.record(claim_id, Verdict.STOP, reason)

    @property
    def verdict(self) -> Verdict:
        return max((claim.verdict for claim in self.claims.values()), key=VERDICT_PRIORITY.__getitem__)


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyStop("plan_json_duplicate_key", key)
        result[key] = value
    return result


def _expect_mapping(
    value: Any,
    context: str,
    allowed_keys: frozenset[str],
    required_keys: frozenset[str] | None = None,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InputStop("plan_schema_type_error", f"{context}:expected_object")
    if required_keys is None:
        required_keys = allowed_keys
    unknown = sorted(set(value) - allowed_keys)
    missing = sorted(required_keys - set(value))
    if unknown:
        raise InputStop("plan_schema_unknown_key", f"{context}:{','.join(unknown)}")
    if missing:
        raise InputStop("plan_schema_missing_key", f"{context}:{','.join(missing)}")
    return value


def _expect_string(value: Any, context: str) -> str:
    if not isinstance(value, str):
        raise InputStop("plan_schema_type_error", f"{context}:expected_string")
    return value


def _expect_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise InputStop("plan_schema_type_error", f"{context}:expected_array")
    return value


def _parse_member(raw: Any, context: str, allowed_keys: frozenset[str]) -> Member:
    item = _expect_mapping(raw, context, allowed_keys)
    return Member(
        _expect_string(item["id"], f"{context}.id"),
        _expect_string(item["kind"], f"{context}.kind"),
        _expect_string(item["path"], f"{context}.path"),
        _expect_string(item["deploy_path"], f"{context}.deploy_path")
        if "deploy_path" in allowed_keys
        else "",
    )


def _parse_edge(raw: Any, context: str) -> Edge:
    item = _expect_mapping(raw, context, EDGE_KEYS)
    return Edge(
        _expect_string(item["from"], f"{context}.from"),
        _expect_string(item["to"], f"{context}.to"),
        _expect_string(item["kind"], f"{context}.kind"),
    )


def _parse_requirement(raw: Any, context: str) -> AllocationRequirement:
    item = _expect_mapping(raw, context, REQUIREMENT_KEYS)
    consumers = tuple(
        _expect_string(value, f"{context}.consumers[{index}]")
        for index, value in enumerate(_expect_list(item["consumers"], f"{context}.consumers"))
    )
    return AllocationRequirement(
        _expect_string(item["name"], f"{context}.name"),
        _expect_string(item["kind"], f"{context}.kind"),
        consumers,
    )


def _parse_allocation(raw: Any, context: str) -> Allocation:
    item = _expect_mapping(raw, context, ALLOCATION_KEYS)
    return Allocation(
        _expect_string(item["name"], f"{context}.name"),
        _expect_string(item["value"], f"{context}.value"),
    )


def _expect_nonnegative_int(value: Any, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise InputStop("plan_schema_type_error", f"{context}:expected_nonnegative_integer")
    return value


def _parse_render_template(raw: Any, context: str) -> RenderTemplate:
    item = _expect_mapping(raw, context, RENDER_TEMPLATE_KEYS)
    return RenderTemplate(
        _expect_string(item["member"], f"{context}.member"),
        _expect_string(item["template"], f"{context}.template"),
    )


def _parse_member_pin(raw: Any, context: str) -> MemberPin:
    item = _expect_mapping(raw, context, MEMBER_PIN_KEYS)
    return MemberPin(
        _expect_string(item["member"], f"{context}.member"),
        _expect_nonnegative_int(item["bytes"], f"{context}.bytes"),
        _expect_string(item["sha256"], f"{context}.sha256"),
    )


def _parse_proof(raw: Any, stage: Stage, context: str) -> RenderProof | FreezeProof:
    if stage is Stage.RENDER:
        item = _expect_mapping(raw, context, RENDER_PROOF_KEYS)
        templates = tuple(
            _parse_render_template(value, f"{context}.render_templates[{index}]")
            for index, value in enumerate(
                _expect_list(item["render_templates"], f"{context}.render_templates")
            )
        )
        return RenderProof(templates)
    if stage is Stage.FREEZE:
        item = _expect_mapping(raw, context, FREEZE_PROOF_KEYS)
        pins = tuple(
            _parse_member_pin(value, f"{context}.member_pins[{index}]")
            for index, value in enumerate(_expect_list(item["member_pins"], f"{context}.member_pins"))
        )
        return FreezeProof(
            pins,
            _expect_string(item["constants"], f"{context}.constants"),
            _expect_nonnegative_int(item["constants_bytes"], f"{context}.constants_bytes"),
            _expect_string(item["constants_sha256"], f"{context}.constants_sha256"),
            _expect_string(item["allowlist"], f"{context}.allowlist"),
            _expect_nonnegative_int(item["allowlist_bytes"], f"{context}.allowlist_bytes"),
            _expect_string(item["allowlist_sha256"], f"{context}.allowlist_sha256"),
            _expect_string(item["prover"], f"{context}.prover"),
            _expect_nonnegative_int(item["prover_bytes"], f"{context}.prover_bytes"),
            _expect_string(item["prover_sha256"], f"{context}.prover_sha256"),
        )
    raise InputStop("plan_stage_unknown", stage.value)


def load_plan(path: Path) -> Plan:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise InputStop("plan_read_error", type(exc).__name__) from exc
    try:
        raw = json.loads(text, object_pairs_hook=_object_without_duplicate_keys)
    except DuplicateKeyStop:
        raise
    except json.JSONDecodeError as exc:
        raise InputStop("plan_json_parse_error", f"line_{exc.lineno}_column_{exc.colno}") from exc

    document = _expect_mapping(raw, "plan", PLAN_KEYS)
    schema = _expect_string(document["schema"], "plan.schema")
    stage_text = _expect_string(document["stage"], "plan.stage")
    try:
        stage = Stage(stage_text)
    except ValueError as exc:
        raise InputStop("plan_stage_unknown", stage_text) from exc

    composites: list[Composite] = []
    for comp_index, raw_composite in enumerate(_expect_list(document["composites"], "plan.composites")):
        context = f"plan.composites[{comp_index}]"
        composite_keys = COMPOSITE_KEYS if stage is Stage.ALLOCATE else COMPOSITE_PROOF_KEYS
        member_keys = MEMBER_KEYS if stage is Stage.ALLOCATE else MEMBER_PROOF_KEYS
        item = _expect_mapping(raw_composite, context, composite_keys)
        members = tuple(
            _parse_member(value, f"{context}.members[{index}]", member_keys)
            for index, value in enumerate(_expect_list(item["members"], f"{context}.members"))
        )
        edges = tuple(
            _parse_edge(value, f"{context}.edges[{index}]")
            for index, value in enumerate(_expect_list(item["edges"], f"{context}.edges"))
        )
        requirements = tuple(
            _parse_requirement(value, f"{context}.allocation_requirements[{index}]")
            for index, value in enumerate(
                _expect_list(item["allocation_requirements"], f"{context}.allocation_requirements")
            )
        )
        allocations = tuple(
            _parse_allocation(value, f"{context}.allocations[{index}]")
            for index, value in enumerate(_expect_list(item["allocations"], f"{context}.allocations"))
        )
        composites.append(
            Composite(
                _expect_string(item["id"], f"{context}.id"),
                _expect_string(item["entrypoint"], f"{context}.entrypoint"),
                members,
                edges,
                requirements,
                allocations,
                None if stage is Stage.ALLOCATE else _parse_proof(item["proof"], stage, f"{context}.proof"),
            )
        )
    return Plan(schema, stage, tuple(composites))


def _valid_identifier(value: str) -> bool:
    return bool(SAFE_ID_RE.fullmatch(value)) and value not in {".", ".."}


def _is_placeholder(value: str) -> bool:
    return bool(PLACEHOLDER_RE.search(value))


def _allocation_value_verdict(kind: str, value: str) -> tuple[Verdict, str]:
    if value == "" or _is_placeholder(value):
        return Verdict.STOP, "allocation_value_unresolved"
    if CONTROL_RE.search(value):
        return Verdict.FAIL, "allocation_value_has_control_character"
    if kind == "safe_component":
        if not _valid_identifier(value):
            return Verdict.FAIL, "allocation_safe_component_invalid"
        return Verdict.PASS, "value_closed"
    if kind == "absolute_path":
        if not value.startswith("/") or value == "/":
            return Verdict.FAIL, "allocation_absolute_path_invalid"
        if "\\" in value or "//" in value or posixpath.normpath(value) != value:
            return Verdict.FAIL, "allocation_absolute_path_not_canonical"
        return Verdict.PASS, "value_closed"
    return Verdict.STOP, "allocation_kind_not_implemented"


def _has_cycle(entrypoint: str, adjacency: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for child in adjacency.get(node, []):
            if visit(child):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return visit(entrypoint)


def _read_relative_file(
    plan_root: Path, relative: str
) -> tuple[Verdict, str, Path | None, bytes | None]:
    if relative == "" or CONTROL_RE.search(relative) or _is_placeholder(relative):
        return Verdict.STOP, "member_path_unresolved", None, None
    if "\\" in relative or relative.startswith("/") or re.match(r"^[A-Za-z]:", relative):
        return Verdict.FAIL, "member_path_not_relative_posix", None, None
    normalized = posixpath.normpath(relative)
    if normalized != relative or normalized in {".", ".."} or normalized.startswith("../"):
        return Verdict.FAIL, "member_path_not_canonical", None, None

    candidate = plan_root.joinpath(*relative.split("/"))
    current = plan_root
    try:
        for part in relative.split("/"):
            current = current / part
            if current.is_symlink():
                return Verdict.STOP, "member_path_symlink_unresolved", None, None
        if not candidate.exists():
            return Verdict.STOP, "member_file_missing", None, None
        if not candidate.is_file():
            return Verdict.FAIL, "member_not_regular_file", None, None
        data = candidate.read_bytes()
    except OSError as exc:
        return Verdict.STOP, f"member_read_error_{type(exc).__name__}", None, None
    return Verdict.PASS, "identified", candidate.absolute(), data


def _member_file_identity(plan_root: Path, relative: str) -> tuple[Verdict, str, int | None, str | None]:
    verdict, reason, _, data = _read_relative_file(plan_root, relative)
    if data is None:
        return verdict, reason, None, None
    return verdict, reason, len(data), hashlib.sha256(data).hexdigest()


def _process_allocations(
    composite: Composite,
    member_ids: set[str],
    recorder: Recorder,
    conservation_claim: str,
    value_claim: str,
) -> None:
    requirement_counts: dict[str, int] = {}
    allocation_counts: dict[str, int] = {}
    for requirement in composite.requirements:
        requirement_counts[requirement.name] = requirement_counts.get(requirement.name, 0) + 1
    for allocation in composite.allocations:
        allocation_counts[allocation.name] = allocation_counts.get(allocation.name, 0) + 1

    requirement_names = set(requirement_counts)
    for index, requirement in enumerate(composite.requirements):
        disposition = "ACCEPT"
        reasons: list[str] = []
        if not _valid_identifier(requirement.name):
            disposition = "STOP"
            reasons.append("requirement_name_invalid")
            recorder.record(conservation_claim, Verdict.STOP, "requirement_name_invalid")
        if requirement_counts[requirement.name] != 1:
            disposition = "FAIL"
            reasons.append("duplicate_requirement")
            recorder.record(conservation_claim, Verdict.FAIL, "duplicate_requirement")
        if requirement.kind not in ALLOCATION_KINDS:
            disposition = "STOP"
            reasons.append("allocation_kind_not_implemented")
            recorder.record(value_claim, Verdict.STOP, "allocation_kind_not_implemented")
        if allocation_counts.get(requirement.name, 0) == 0:
            disposition = "STOP"
            reasons.append("allocation_missing")
            recorder.record(conservation_claim, Verdict.STOP, "allocation_missing")
        elif allocation_counts[requirement.name] != 1:
            disposition = "FAIL"
            reasons.append("allocation_not_one_to_one")
            recorder.record(conservation_claim, Verdict.FAIL, "allocation_not_one_to_one")
        if not requirement.consumers:
            disposition = "FAIL"
            reasons.append("consumer_set_empty")
            recorder.record(conservation_claim, Verdict.FAIL, "consumer_set_empty")
        if len(set(requirement.consumers)) != len(requirement.consumers):
            disposition = "FAIL"
            reasons.append("consumer_duplicate")
            recorder.record(conservation_claim, Verdict.FAIL, "consumer_duplicate")
        unknown_consumers = sorted(set(requirement.consumers) - member_ids)
        if unknown_consumers:
            disposition = "FAIL"
            reasons.append("consumer_unknown")
            recorder.record(conservation_claim, Verdict.FAIL, "consumer_unknown")
        recorder.add_row(
            "REQUIREMENT",
            composite=composite.composite_id,
            index=index,
            name=requirement.name,
            kind=requirement.kind,
            consumers=list(requirement.consumers),
            disposition=disposition,
            reasons=sorted(set(reasons)) or ["conserved"],
        )
        seen_consumers: set[str] = set()
        for consumer_index, consumer in enumerate(requirement.consumers):
            consumer_reasons: list[str] = []
            if consumer not in member_ids:
                consumer_reasons.append("consumer_unknown")
            if consumer in seen_consumers:
                consumer_reasons.append("consumer_duplicate")
            seen_consumers.add(consumer)
            recorder.add_row(
                "CONSUMER",
                composite=composite.composite_id,
                requirement_index=index,
                index=consumer_index,
                allocation=requirement.name,
                member=consumer,
                disposition="FAIL" if consumer_reasons else "ACCEPT",
                reasons=sorted(set(consumer_reasons)) or ["declared_reference_conserved"],
            )

    for index, allocation in enumerate(composite.allocations):
        disposition = "ACCEPT"
        reasons: list[str] = []
        if allocation.name not in requirement_names:
            disposition = "FAIL"
            reasons.append("allocation_undeclared")
            recorder.record(conservation_claim, Verdict.FAIL, "allocation_undeclared")
        if allocation_counts[allocation.name] != 1:
            disposition = "FAIL"
            reasons.append("allocation_duplicate")
            recorder.record(conservation_claim, Verdict.FAIL, "allocation_duplicate")
        matching = [requirement for requirement in composite.requirements if requirement.name == allocation.name]
        if len(matching) == 1:
            value_verdict, value_reason = _allocation_value_verdict(matching[0].kind, allocation.value)
            if value_verdict is not Verdict.PASS:
                disposition = value_verdict.value
                reasons.append(value_reason)
                recorder.record(value_claim, value_verdict, value_reason)
        elif matching:
            disposition = "FAIL"
            reasons.append("requirement_not_one_to_one")
        recorder.add_row(
            "ALLOCATION",
            composite=composite.composite_id,
            index=index,
            name=allocation.name,
            value=allocation.value,
            disposition=disposition,
            reasons=sorted(set(reasons)) or ["closed"],
        )


def _process_graph_and_identity(composite: Composite, plan_root: Path, recorder: Recorder) -> None:
    member_states = [MemberState(composite.composite_id, index, member) for index, member in enumerate(composite.members)]
    id_counts: dict[str, int] = {}
    path_counts: dict[str, int] = {}
    for state in member_states:
        id_counts[state.member.member_id] = id_counts.get(state.member.member_id, 0) + 1
        path_counts[state.member.path] = path_counts.get(state.member.path, 0) + 1

    member_ids = set(id_counts)
    if not member_states:
        recorder.record("A2", Verdict.STOP, "composite_has_no_members")
        recorder.record("A5", Verdict.STOP, "composite_has_no_members")
    if not _valid_identifier(composite.entrypoint):
        recorder.record("A2", Verdict.STOP, "entrypoint_identifier_invalid")
    entrypoint_count = id_counts.get(composite.entrypoint, 0)
    if entrypoint_count == 0:
        recorder.record("A2", Verdict.FAIL, "entrypoint_not_declared")
    elif entrypoint_count != 1:
        recorder.record("A2", Verdict.FAIL, "entrypoint_not_unique")

    unique_ids = all(count == 1 for count in id_counts.values())
    if not unique_ids:
        recorder.record("A5", Verdict.FAIL, "member_id_duplicate")

    adjacency: dict[str, list[str]] = {member_id: [] for member_id in member_ids}
    valid_edges = True
    seen_edges: set[tuple[str, str, str]] = set()
    for index, edge in enumerate(composite.edges):
        disposition = "ACCEPT"
        reasons: list[str] = []
        edge_key = (edge.source, edge.target, edge.kind)
        if edge.kind not in EDGE_KINDS:
            disposition = "STOP"
            reasons.append("edge_kind_not_implemented")
            recorder.record("A5", Verdict.STOP, "edge_kind_not_implemented")
            valid_edges = False
        if edge.source not in member_ids or edge.target not in member_ids:
            disposition = "FAIL"
            reasons.append("edge_endpoint_unknown")
            recorder.record("A5", Verdict.FAIL, "edge_endpoint_unknown")
            valid_edges = False
        if edge_key in seen_edges:
            disposition = "FAIL"
            reasons.append("edge_duplicate")
            recorder.record("A5", Verdict.FAIL, "edge_duplicate")
            valid_edges = False
        seen_edges.add(edge_key)
        if disposition == "ACCEPT":
            adjacency[edge.source].append(edge.target)
        recorder.add_row(
            "EDGE",
            composite=composite.composite_id,
            index=index,
            source=edge.source,
            target=edge.target,
            kind=edge.kind,
            disposition=disposition,
            reasons=sorted(set(reasons)) or ["declared"],
        )

    reachable: set[str] = set()
    graph_cycle = False
    if unique_ids and entrypoint_count == 1 and valid_edges:
        queue = [composite.entrypoint]
        while queue:
            node = queue.pop(0)
            if node in reachable:
                continue
            reachable.add(node)
            queue.extend(adjacency.get(node, []))
        graph_cycle = _has_cycle(composite.entrypoint, adjacency)
        if graph_cycle:
            recorder.record("A5", Verdict.FAIL, "declared_graph_cycle")
    else:
        recorder.record("A5", Verdict.FAIL, "declared_graph_not_traversable")

    if unique_ids and entrypoint_count == 1 and valid_edges:
        unreachable = member_ids - reachable
        if unreachable:
            recorder.record("A5", Verdict.FAIL, "declared_member_unreachable")

    for state in member_states:
        member = state.member
        if not _valid_identifier(member.member_id):
            state.graph = "STOP"
            recorder.record("A5", Verdict.STOP, "member_identifier_invalid")
        elif id_counts[member.member_id] != 1:
            state.graph = "FAIL"
        elif graph_cycle:
            state.graph = "FAIL"
        elif member.member_id in reachable:
            state.graph = "REACHABLE"
        else:
            state.graph = "FAIL"
        if member.kind not in MEMBER_KINDS:
            state.identity = "STOP"
            recorder.record("A6", Verdict.STOP, "member_kind_not_implemented")
        elif path_counts[member.path] != 1:
            state.identity = "FAIL"
            recorder.record("A6", Verdict.FAIL, "member_path_alias")
        else:
            identity_verdict, reason, size, sha256 = _member_file_identity(plan_root, member.path)
            state.identity = "IDENTIFIED" if identity_verdict is Verdict.PASS else identity_verdict.value
            state.size = size
            state.sha256 = sha256
            recorder.record("A6", identity_verdict, reason)

    for state in member_states:
        recorder.add_row(
            "MEMBER",
            composite=state.composite_id,
            index=state.index,
            id=state.member.member_id,
            kind=state.member.kind,
            path=state.member.path,
            graph=state.graph,
            identity=state.identity,
            bytes=state.size if state.size is not None else "-",
            sha256=state.sha256 if state.sha256 is not None else "-",
            disposition=state.disposition,
        )

    _process_allocations(composite, member_ids, recorder, "A3", "A4")
    consumer_count = sum(len(requirement.consumers) for requirement in composite.requirements)
    recorder.add_row(
        "CONSERVATION",
        composite=composite.composite_id,
        input_members=len(member_states),
        terminal_member_rows=len(member_states),
        reachable_members=len(reachable),
        input_edges=len(composite.edges),
        terminal_edge_rows=len(composite.edges),
        input_requirements=len(composite.requirements),
        terminal_requirement_rows=len(composite.requirements),
        input_allocations=len(composite.allocations),
        terminal_allocation_rows=len(composite.allocations),
        input_consumer_references=consumer_count,
        terminal_consumer_rows=consumer_count,
    )


def _literal_shell_word(raw: str, allocations: dict[str, str] | None = None) -> str | None:
    allocations = allocations or {}
    variable = re.fullmatch(r"['\"]?\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))['\"]?", raw)
    if variable is not None:
        return allocations.get(variable.group(1) or variable.group(2))
    if any(marker in raw for marker in ("$", "`", "$(", "${")):
        return None
    try:
        parts = shlex.split(raw, posix=True)
    except ValueError:
        return None
    if len(parts) != 1 or parts[0] == "":
        return None
    return parts[0]


def _canonical_deployed_path(value: str) -> str | None:
    """Return the value only if it is already an absolute canonical POSIX path.

    Nothing is rewritten.  A `..` component is not collapsed, because collapsing it
    lexically is unsound whenever any prefix is a symlink; such a value is simply not
    a canonical deployed identity and the caller must STOP.
    """

    if value == "" or _is_placeholder(value) or CONTROL_RE.search(value):
        return None
    if "\\" in value or "//" in value:
        return None
    if not value.startswith("/") or value == "/":
        return None
    if posixpath.normpath(value) != value:
        return None
    return value


def _deploy_path_verdict(value: str) -> tuple[Verdict, str]:
    if value == "" or _is_placeholder(value):
        return Verdict.STOP, "member_deploy_path_unresolved"
    if _canonical_deployed_path(value) is None:
        return Verdict.FAIL, "member_deploy_path_not_canonical_absolute"
    return Verdict.PASS, "deployed_identity_declared"


def _member_for_operand(operand: str, deploy_to_id: dict[str, str]) -> str | None:
    """Bind an operand to a member by EXACT declared deployed-path identity.

    There is deliberately no basename, suffix or in-bundle-path fallback: a file name
    is a label, not a file identity (defect pattern 8).  An operand that does not equal
    exactly one declared `deploy_path` binds to nothing and the caller must STOP.
    """

    identity = _canonical_deployed_path(operand)
    if identity is None:
        return None
    return deploy_to_id.get(identity)


def _parse_constants(data: bytes) -> tuple[tuple["ConstantBinding", ...], str | None]:
    """Parse the pinned constants table with a deliberately narrower mirror of the
    prover's own `parse_constants` grammar.

    The mirror is narrower on purpose: the prover expands `$NAME` inside a constant
    value against earlier constants, this parser does not model that and refuses the
    value instead of guessing it.  Anything this parser cannot classify is a STOP, so
    a divergence can never hide inside a form the composite silently skipped.
    """

    try:
        text = data.decode("utf-8")
    except UnicodeError:
        return tuple(), "constants_not_utf8"
    bindings: list[ConstantBinding] = []
    seen: set[str] = set()
    for line_number, original in enumerate(text.splitlines(), 1):
        line = original.strip()
        if not line or line.startswith("#"):
            continue
        match = CONSTANT_ASSIGN_RE.fullmatch(line)
        if match is None:
            return tuple(bindings), "constants_line_not_key_value"
        name, raw = match.groups()
        if name in seen:
            return tuple(bindings), "constants_duplicate_name"
        seen.add(name)
        bindings.append(ConstantBinding(line_number, name, _literal_shell_word(raw)))
    return tuple(bindings), None


def _allocation_rows(composite: Composite, disposition: str, reason: str) -> tuple[AllocationBinding, ...]:
    """One terminal row per declared allocation for a whole-table refusal."""

    return tuple(
        AllocationBinding(index, allocation.name, allocation.value, disposition, reason)
        for index, allocation in enumerate(composite.allocations)
    )


# An allocation the constants table never mentions is a conservation defect in F10's
# own domain, but it corrupts no value the prover re-resolves, and the analysis-unit
# builder independently refuses any operand it cannot resolve from the pinned table.
# Every other reason means the table itself is unusable, so the prover is not invoked.
NON_BLOCKING_RECONCILIATION_REASONS = frozenset({"allocation_absent_from_pinned_constants"})


def _reconcile_constants(
    composite: Composite, data: bytes
) -> tuple[
    dict[str, str] | None,
    tuple["ConstantBinding", ...],
    tuple["AllocationBinding", ...],
    tuple[str, ...],
]:
    """Reconcile the plan allocations against the pinned constants table.

    The plan allocations decide which member a source operand binds to; the prover
    re-resolves the same names from `constants.env`.  Those are two sources for one
    value universe, so every name they share must be byte-equal or the composite STOPs
    before the prover is invoked.

    Both directions are walked and both produce terminal rows.  Round 3 walked the
    constants table only, so a plan allocation the table never mentions produced no
    row and no F10 failure while F10 still claimed the two inputs were one conserved
    universe.  Every declared allocation now gets exactly one disposition, and an
    absent one is a STOP rather than an absence.
    """

    bindings, fatal = _parse_constants(data)
    reasons: list[str] = []
    if fatal is not None:
        reasons.append(fatal)
    allocation_counts: dict[str, int] = {}
    allocation_values: dict[str, str] = {}
    for allocation in composite.allocations:
        allocation_counts[allocation.name] = allocation_counts.get(allocation.name, 0) + 1
        allocation_values[allocation.name] = allocation.value
    for binding in bindings:
        if binding.value is None:
            binding.disposition = "STOP"
            binding.reason = "constants_value_not_literal"
        elif binding.name not in allocation_values:
            binding.disposition = "RUNTIME_ONLY"
            binding.reason = "not_declared_by_plan_allocations"
            continue
        elif allocation_counts[binding.name] != 1:
            binding.disposition = "STOP"
            binding.reason = "allocation_duplicate_blocks_reconciliation"
        elif binding.value != allocation_values[binding.name]:
            binding.disposition = "STOP"
            binding.reason = "allocation_constants_value_divergence"
        else:
            binding.disposition = "RECONCILED"
            binding.reason = "allocation_and_constants_byte_equal"
            continue
        reasons.append(binding.reason)

    constants_by_name = {binding.name: binding for binding in bindings}
    allocation_bindings: list[AllocationBinding] = []
    for index, allocation in enumerate(composite.allocations):
        binding = constants_by_name.get(allocation.name)
        if allocation_counts[allocation.name] != 1:
            disposition, reason = "STOP", "allocation_duplicate_blocks_reconciliation"
        elif fatal is not None:
            # The table was refused before this name could be reached, so the
            # allocation has no honest constants-side disposition.
            disposition, reason = "STOP", "constants_grammar_not_closed_for_allocation"
        elif binding is None:
            disposition, reason = "STOP", "allocation_absent_from_pinned_constants"
        elif binding.value is None:
            disposition, reason = "STOP", "constants_value_not_literal"
        elif binding.value != allocation.value:
            disposition, reason = "STOP", "allocation_constants_value_divergence"
        else:
            disposition, reason = "RECONCILED", "allocation_and_constants_byte_equal"
        allocation_bindings.append(
            AllocationBinding(index, allocation.name, allocation.value, disposition, reason)
        )
        if disposition == "STOP":
            reasons.append(reason)

    unique_reasons = tuple(sorted(set(reasons)))
    if set(unique_reasons) - NON_BLOCKING_RECONCILIATION_REASONS:
        return None, bindings, tuple(allocation_bindings), unique_reasons
    return (
        {binding.name: binding.value for binding in bindings if binding.value is not None},
        bindings,
        tuple(allocation_bindings),
        unique_reasons,
    )


def _shell_words(text: str) -> tuple[tuple[ShellWord, ...] | None, str | None]:
    """Split rendered shell bytes into words, marking every command position.

    This scanner shares no expression with SOURCE_COMMAND_RE or EXEC_COMMAND_RE.  It
    is the independent side of the coverage check required after round 3: the
    matcher says which command words became edges, this says which command words
    exist at all, and `_derive_graph` STOPs on the difference.

    It runs only over text `_graph_opaque_reason` already accepted, so here-documents,
    line continuations, substitutions and multi-line quotes are gone before it starts.

    Command position is *conserved* across every accepted command prefix — scalar and
    indexed assignment words, numeric and named file-descriptor redirections, and the
    name bound by `function`/`coproc`.  A prefix shape outside that model returns a
    STOP reason instead of degrading into a leaf, because a leaf closes the command
    position and the command word behind it would then be classified by nothing.

    Every word this scanner marks as a command position is then adjudicated by
    `_command_word_class` under a closed admissibility policy, so reaching a command
    position is enough: the word is derived, refused, or proven static, never skipped.

    Round 7 fixed the one place where the WORD BOUNDARY itself is not decidable from
    the bytes alone: a `(` abutting a word is a separator in a default shell and part
    of the word under `extglob`.  Rather than pick a reading, the scanner conserves
    the `(` into the raw token (except for the NAME-shaped function-definition form)
    and lets the admissibility policy refuse it.  The scanner decides nothing; it
    only stops handing the classifier a fragment of a word instead of the word.
    """

    words: list[ShellWord] = []
    index = 0
    length = len(text)
    command_position = True
    redirect_target_pending = False
    name_binding_pending = False
    while index < length:
        character = text[index]
        if character in " \t":
            index += 1
            continue
        if character in "\r\n":
            command_position = True
            redirect_target_pending = False
            name_binding_pending = False
            index += 1
            continue
        if character == "#":
            while index < length and text[index] != "\n":
                index += 1
            continue
        if character in ";&|":
            while index < length and text[index] in ";&|":
                index += 1
            command_position = True
            redirect_target_pending = False
            name_binding_pending = False
            continue
        if character in "()":
            index += 1
            command_position = True
            redirect_target_pending = False
            name_binding_pending = False
            continue
        if character in "<>":
            # A redirection consumes its target word without opening or closing a
            # command position, so `> out bash evil.sh` still scans `bash`.
            while index < length and text[index] in "<>&|":
                index += 1
            redirect_target_pending = True
            continue
        start = index
        quote: str | None = None
        while index < length:
            current = text[index]
            if quote is None:
                if current in " \t\r\n;&|()<>":
                    break
                if current == "\\":
                    index += 2
                    continue
                if current in "'\"":
                    quote = current
                index += 1
                continue
            if quote == "'":
                if current == "'":
                    quote = None
                index += 1
                continue
            if current == "\\":
                index += 2
                continue
            if current == '"':
                quote = None
            index += 1
        if quote is not None:
            return None, "source_graph_unterminated_quote"
        raw = text[start:min(index, length)]
        if not raw:
            return None, "source_graph_word_scan_not_progressing"
        if index < length and text[index] == "(" and not SHELL_FUNCTION_NAME_RE.fullmatch(raw):
            # WORD-BOUNDARY CONSERVATION (round-7 R6-F1).  The word ended only because
            # a `(` abuts it, and whether that `(` separates two words or lies INSIDE
            # one word is not decidable from these bytes: with `extglob` enabled
            # `ba+(s)h` is a single pathname pattern, and splitting it would hand the
            # classifier the fragments `ba+`, `s`, `h` - three invented command words,
            # none of which is the name Bash looks up.  Round 6 was blind here for
            # exactly that reason.
            #
            # The `(` is therefore conserved INTO the raw token instead of being
            # dropped, so the admissibility policy below adjudicates the token Bash
            # would use rather than a fragment of it.  This is not a second fence and
            # decides nothing on its own: it only stops the scanner from destroying
            # the evidence.  The safe set is what refuses the token, because `(` is
            # not in it - which is why restoring the round-6 blacklist puts every
            # extglob RED back to PASS even with this conservation in place.
            #
            # A function definition is the one benign construct with this shape, and
            # Bash requires a NAME for it; an extglob pattern requires `?`, `*`, `+`,
            # `@` or `!` immediately before the `(`, and no NAME ends in one of those.
            # So the NAME-shaped form keeps its round-6 treatment and nothing else does.
            raw += "("
            index += 1
        if redirect_target_pending:
            redirect_target_pending = False
            continue
        if index < length and text[index] in "<>":
            # The word abuts a redirection operator with no separating blank, so it
            # may be that redirection's file-descriptor prefix rather than an argv
            # word.  A prefix belongs to the redirection and must leave the command
            # position exactly as it found it: `2>err source lib`, `{fd}>err source
            # lib` and `{fd}<in source lib` all still run `source`.
            descriptor = _redirection_prefix_class(raw)
            if descriptor == "file_descriptor":
                continue
            if descriptor == "unmodeled":
                return None, "source_graph_unmodeled_redirection_prefix"
        if command_position and _assignment_prefix_class(raw) == "unmodeled":
            # Fail closed here rather than one line further down.  Once an unmodelled
            # prefix is emitted as a leaf it closes the command position, and the
            # command word behind it is never classified by anything - the matcher
            # does not anchor through the prefix either, so the composite would pass
            # over an unanalysed program with no uncovered word to report.
            return None, "source_graph_unmodeled_assignment_prefix"
        words.append(ShellWord(start, raw, command_position))
        word_class = _command_word_class(raw)
        if name_binding_pending and word_class == "leaf":
            # `function foo`/`coproc foo`: the word names a definition, it does not
            # run, so the command position survives it and the body's first command
            # word is still scanned.
            pass
        elif word_class not in {"assignment", "control", "wrapper"}:
            # Assignment prefixes, reserved words and command wrappers all leave the
            # command position open, so `A=1 env bash x` scans `bash` as a command word
            # too and reports every unmodelled layer rather than only the outermost one.
            command_position = False
        name_binding_pending = (
            command_position and word_class == "control" and raw in SHELL_NAME_BINDING_WORDS
        )
    return tuple(words), None


def _redirection_prefix_class(raw: str) -> str:
    """Classify a word that abuts a redirection operator.

    `file_descriptor` — a modelled prefix that belongs to the redirection and must
    not touch the command position.  `word` — an ordinary argv word that merely
    happens to touch the operator (`echo>out` runs `echo`).  `unmodeled` — a
    brace-opening word in the exact syntactic slot of a named descriptor whose
    interior is not a plain name, which the scanner refuses to guess about.
    """

    if NUMERIC_FD_PREFIX_RE.fullmatch(raw) or NAMED_FD_PREFIX_RE.fullmatch(raw):
        return "file_descriptor"
    if raw.startswith("{"):
        return "unmodeled"
    return "word"


def _assignment_prefix_class(raw: str) -> str:
    """Classify a command-position word against the accepted assignment forms."""

    if SHELL_ASSIGNMENT_RE.match(raw):
        return "assignment"
    if SHELL_SUBSCRIPT_PREFIX_RE.match(raw) and "=" in raw:
        return "unmodeled"
    return "word"


def _command_word_class(raw: str) -> str:
    """Classify one command-position word under a CLOSED admissibility policy.

    `leaf` - and only `leaf` - means "this command word is benign and derives no
    edge", so it is the one answer that must be earned.  It is returned only for a
    proven-static literal that is not a recognised interpreter or source builtin.
    `dynamic` and `unmodeled` are the two refusals; both STOP at the caller and
    neither can degrade into a leaf, so no command-word form can disappear by being
    one nobody enumerated.

    Since round 7 "proven-static" is decided by a WHITELIST: every character of the
    raw word must be in the safe set (COMMAND_WORD_STATIC_RE).  The round-6 test
    asked whether the word contained a listed expansion operator, which is complete
    only if the list is, and it was not - it missed the `extglob` family.  Under the
    whitelist an unrecognised character is a refusal by default, so no future or
    rarely-used operator can be admitted by having been left off a list.

    The reserved-word test compares the RAW word, not its unquoted literal.  Bash
    only treats `if`/`{`/`[[` as reserved when they are written unquoted, so `"if"`
    is an ordinary command name; reading the literal would have promoted it to a
    reserved word and kept a command position open that Bash had already closed.
    """

    if SHELL_ASSIGNMENT_RE.match(raw):
        return "assignment"
    if raw in SHELL_CONTROL_WORDS:
        return "control"
    if COMMAND_WORD_SUBSTITUTION_RE.search(raw):
        return "dynamic"
    if not COMMAND_WORD_STATIC_RE.fullmatch(raw):
        # The round-7 whitelist.  Not "does this word contain an operator I listed"
        # but "is every character of it one I proved cannot resolve".  A character
        # outside the safe set is refused whether or not this round knows what it
        # would do, so an operator family nobody enumerated cannot be admitted.
        return "unmodeled"
    literal = _literal_shell_word(raw)
    if literal is None:
        # Degenerate quoting or an empty word: the spelling is static but it names
        # nothing this classifier can adjudicate.
        return "unmodeled"
    # Bash looks up the last pathname component of any command word that contains a
    # slash, whether the path is absolute or relative.  Round 5 took the basename
    # only for an absolute path, so `bin/bash script.sh` was a leaf while
    # `/bin/bash script.sh` was recognised - the same interpreter, the same operand,
    # hidden by a spelling.
    if "/" in literal:
        name = posixpath.basename(literal)
        if name == "":
            return "unmodeled"
    else:
        name = literal
    if name in GRAPH_SOURCE_WORDS:
        return "graph"
    if name in GRAPH_INTERPRETER_WORDS or GRAPH_INTERPRETER_VERSION_RE.fullmatch(name):
        return "graph"
    if name in GRAPH_WRAPPER_WORDS:
        return "wrapper"
    return "leaf"


def _graph_word_conservation(
    text: str, source_matches: list[re.Match[str]], exec_matches: list[re.Match[str]]
) -> tuple[str, ...]:
    """Reconcile scanned command words against the edges the matcher derived.

    Returns every reason the two sides disagree.  Detection is broader than
    derivation on purpose, so `zsh script`, `command source lib`, `\\source lib`,
    `if source lib; then` and every other unmodelled command form reach a STOP
    instead of leaving the graph silently short an edge.

    Since round 6 the difference is not enumerated form by form: every command-position
    word that is not a proven-static benign literal produces a reason here, so a form
    this round never anticipated STOPs by default rather than by having been listed.
    Round 7 made "proven-static" a whitelist over the raw word's characters instead of
    a blacklist of expansion operators, so the default now holds for a character
    nobody enumerated, not only for a form nobody enumerated.
    """

    words, scan_reason = _shell_words(text)
    if words is None:
        return (scan_reason,) if scan_reason is not None else ("source_graph_word_scan_failed",)
    reasons: list[str] = []
    matched_commands = {match.start(1) for match in source_matches} | {
        match.start(1) for match in exec_matches
    }
    matched_operands = {match.start(2) for match in source_matches} | {
        match.start(2) for match in exec_matches
    }
    command_offsets = {word.offset for word in words if word.command_position}
    word_offsets = {word.offset for word in words}
    for word in words:
        if not word.command_position:
            continue
        word_class = _command_word_class(word.text)
        if word_class == "graph" and word.offset not in matched_commands:
            reasons.append("source_graph_command_word_not_modeled")
        elif word_class == "wrapper":
            reasons.append("source_graph_command_wrapper_not_modeled")
        elif word_class == "dynamic":
            reasons.append("source_graph_dynamic_command_not_modeled")
        elif word_class == "unmodeled":
            # A command word that was not PROVEN static: some character of it is
            # outside the safe set, so this module cannot show that the spelling is
            # already the name Bash looks up.  It is refused here rather than leafed,
            # so whatever it might resolve to - including a recognised interpreter
            # with a script operand behind it - cannot pass through unanalysed.  Note
            # the direction: the word is refused for lacking a proof, not for
            # carrying an operator this round happened to recognise.
            reasons.append("source_graph_unmodeled_command_word")
    # The matcher must never claim an edge from something the scanner does not see
    # as a command word, nor bind an operand that is not a whole word.
    if matched_commands - command_offsets:
        reasons.append("source_graph_derived_edge_not_at_command_word")
    if matched_operands - word_offsets:
        reasons.append("source_graph_derived_operand_not_a_shell_word")
    return tuple(sorted(set(reasons)))


def _graph_opaque_reason(text: str) -> str | None:
    if re.search(r"<<-?", text):
        return "source_graph_heredoc_not_modeled"
    if re.search(r"\\\r?\n", text):
        return "source_graph_line_continuation_not_modeled"
    if "$(" in text or "`" in text or "<(" in text or ">(" in text:
        return "source_graph_nested_execution_not_modeled"
    if re.search(r"(?:^|[;|&()])\s*(?:eval|alias)\b", text, re.MULTILINE):
        return "source_graph_indirect_execution_not_modeled"
    if re.search(r"(?:^|[;|&()])\s*['\"]?\$(?:\{|[A-Za-z_])", text, re.MULTILINE):
        return "source_graph_dynamic_command_not_modeled"
    quote: str | None = None
    escaped = False
    for character in text:
        if escaped:
            escaped = False
            continue
        if character == "\\" and quote != "'":
            escaped = True
            continue
        if character in {"'", '"'}:
            if quote is None:
                quote = character
            elif quote == character:
                quote = None
        if character == "\n" and quote is not None:
            return "source_graph_multiline_quote_not_modeled"
    if quote is not None:
        return "source_graph_unterminated_quote"
    return None


def _derive_graph(
    composite: Composite, plan_root: Path, recorder: Recorder, claim_id: str, identity_claim: str
) -> tuple[set[str], dict[str, str]]:
    id_counts: dict[str, int] = {}
    path_counts: dict[str, int] = {}
    for member in composite.members:
        id_counts[member.member_id] = id_counts.get(member.member_id, 0) + 1
        path_counts[member.path] = path_counts.get(member.path, 0) + 1
    member_ids = set(id_counts)
    graph_disposition = {member.member_id: "UNRESOLVED" for member in composite.members}

    if not composite.members:
        recorder.record(claim_id, Verdict.STOP, "composite_has_no_members")
        return set(), graph_disposition
    if not _valid_identifier(composite.entrypoint):
        recorder.record(claim_id, Verdict.STOP, "entrypoint_identifier_invalid")
    if id_counts.get(composite.entrypoint, 0) == 0:
        recorder.record(claim_id, Verdict.FAIL, "entrypoint_not_declared")
    elif id_counts[composite.entrypoint] != 1:
        recorder.record(claim_id, Verdict.FAIL, "entrypoint_not_unique")
    if any(count != 1 for count in id_counts.values()):
        recorder.record(claim_id, Verdict.FAIL, "member_id_duplicate")
    if any(count != 1 for count in path_counts.values()):
        recorder.record(claim_id, Verdict.FAIL, "member_path_alias")

    deploy_counts: dict[str, int] = {}
    for member in composite.members:
        deploy_counts[member.deploy_path] = deploy_counts.get(member.deploy_path, 0) + 1
    deploy_to_id: dict[str, str] = {}
    identity_blocked = False
    for index, member in enumerate(composite.members):
        identity_verdict, identity_reason = _deploy_path_verdict(member.deploy_path)
        if identity_verdict is Verdict.PASS and deploy_counts[member.deploy_path] != 1:
            identity_verdict, identity_reason = Verdict.FAIL, "member_deploy_path_alias"
        if identity_verdict is Verdict.PASS:
            deploy_to_id[member.deploy_path] = member.member_id
        else:
            identity_blocked = True
            recorder.record(identity_claim, identity_verdict, identity_reason)
        recorder.add_row(
            "DEPLOY_IDENTITY",
            composite=composite.composite_id,
            index=index,
            member=member.member_id,
            path=member.path,
            deploy_path=member.deploy_path,
            disposition="ACCEPT" if identity_verdict is Verdict.PASS else identity_verdict.value,
            reason=identity_reason,
        )
    allocation_counts: dict[str, int] = {}
    allocation_values: dict[str, str] = {}
    for allocation in composite.allocations:
        allocation_counts[allocation.name] = allocation_counts.get(allocation.name, 0) + 1
        allocation_values[allocation.name] = allocation.value
    unique_allocations = {
        name: value for name, value in allocation_values.items() if allocation_counts.get(name) == 1
    }

    derived: list[Edge] = []
    derivation_blocked = identity_blocked
    for member in composite.members:
        if member.kind != "shell":
            # A member whose outbound edges are not modeled must not disappear from the
            # graph claim.  FREEZE already refuses non-shell members; RENDER now refuses
            # to call the graph closed over them as well (defect pattern 12).
            recorder.record(claim_id, Verdict.STOP, "member_kind_graph_derivation_not_modeled")
            derivation_blocked = True
            continue
        verdict, reason, _, data = _read_relative_file(plan_root, member.path)
        if verdict is not Verdict.PASS or data is None:
            recorder.record(claim_id, verdict, reason)
            derivation_blocked = True
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeError:
            recorder.record(claim_id, Verdict.STOP, "shell_member_not_utf8")
            derivation_blocked = True
            continue
        opaque_reason = _graph_opaque_reason(text)
        if opaque_reason is not None:
            recorder.record(claim_id, Verdict.STOP, opaque_reason)
            derivation_blocked = True

        source_matches = list(SOURCE_COMMAND_RE.finditer(text))
        exec_matches = list(EXEC_COMMAND_RE.finditer(text))
        if opaque_reason is None:
            # Coverage is decided by the independent word scanner, not by a second
            # copy of the matcher's own grammar.  Opaque text has already STOPped and
            # cannot be tokenised line-wise, so it is not scanned twice.
            for reason in _graph_word_conservation(text, source_matches, exec_matches):
                recorder.record(claim_id, Verdict.STOP, reason)
                derivation_blocked = True

        source_sites = re.findall(r"(?:^|[;|&()])\s*(?:source\b|\.(?=\s))", text, re.MULTILINE)
        if len(source_matches) != len(source_sites):
            recorder.record(claim_id, Verdict.STOP, "source_syntax_not_covered")
            derivation_blocked = True
        for match in source_matches:
            operand = _literal_shell_word(match.group(2), unique_allocations)
            if operand is None:
                recorder.record(claim_id, Verdict.STOP, "source_operand_dynamic")
                derivation_blocked = True
                continue
            target = _member_for_operand(operand, deploy_to_id)
            if target is None:
                recorder.record(claim_id, Verdict.STOP, "source_operand_deploy_identity_unbound")
                recorder.record(
                    identity_claim, Verdict.STOP, "source_operand_deploy_identity_unbound"
                )
                derivation_blocked = True
                recorder.add_row(
                    "DERIVED_EDGE",
                    composite=composite.composite_id,
                    source=member.member_id,
                    target="-",
                    kind="source",
                    operand=operand,
                    disposition="STOP",
                    reason="source_operand_deploy_identity_unbound",
                )
                continue
            edge = Edge(member.member_id, target, "source")
            derived.append(edge)
            recorder.add_row(
                "DERIVED_EDGE",
                composite=composite.composite_id,
                source=edge.source,
                target=edge.target,
                kind=edge.kind,
                operand=operand,
                disposition="DERIVED",
                reason="rendered_source_site",
            )

        exec_sites = re.findall(
            r"(?:^|[;|&()])\s*(?:(?:/[^\s;|&()]+/)?(?:bash|sh|python(?:3(?:\.\d+)?)?))\b",
            text,
            re.MULTILINE,
        )
        if len(exec_matches) != len(exec_sites):
            recorder.record(claim_id, Verdict.STOP, "execute_source_syntax_not_covered")
            derivation_blocked = True
        for match in exec_matches:
            operand = _literal_shell_word(match.group(2), unique_allocations)
            if operand is None or operand.startswith("-"):
                recorder.record(claim_id, Verdict.STOP, "execute_source_operand_dynamic_or_optioned")
                derivation_blocked = True
                continue
            target = _member_for_operand(operand, deploy_to_id)
            if target is None:
                recorder.record(
                    claim_id, Verdict.STOP, "execute_source_operand_deploy_identity_unbound"
                )
                recorder.record(
                    identity_claim, Verdict.STOP, "execute_source_operand_deploy_identity_unbound"
                )
                derivation_blocked = True
                recorder.add_row(
                    "DERIVED_EDGE",
                    composite=composite.composite_id,
                    source=member.member_id,
                    target="-",
                    kind="execute_source",
                    operand=operand,
                    disposition="STOP",
                    reason="execute_source_operand_deploy_identity_unbound",
                )
                continue
            edge = Edge(member.member_id, target, "execute_source")
            derived.append(edge)
            recorder.add_row(
                "DERIVED_EDGE",
                composite=composite.composite_id,
                source=edge.source,
                target=edge.target,
                kind=edge.kind,
                operand=operand,
                disposition="DERIVED",
                reason="rendered_execute_site",
            )

    derived_keys = [(edge.source, edge.target, edge.kind) for edge in derived]
    declared_keys = [(edge.source, edge.target, edge.kind) for edge in composite.edges]
    if len(set(derived_keys)) != len(derived_keys):
        recorder.record(claim_id, Verdict.FAIL, "derived_edge_duplicate")
    if len(set(declared_keys)) != len(declared_keys):
        recorder.record(claim_id, Verdict.FAIL, "declared_edge_duplicate")
    if any(edge.kind not in EDGE_KINDS for edge in composite.edges):
        recorder.record(claim_id, Verdict.STOP, "edge_kind_not_implemented")
    if set(derived_keys) != set(declared_keys):
        recorder.record(claim_id, Verdict.FAIL, "derived_declared_graph_mismatch")
    for index, edge in enumerate(composite.edges):
        edge_key = (edge.source, edge.target, edge.kind)
        if edge.kind not in EDGE_KINDS:
            disposition, reason = "STOP", "edge_kind_not_implemented"
        elif edge.source not in member_ids or edge.target not in member_ids:
            disposition, reason = "FAIL", "edge_endpoint_unknown"
        elif edge_key not in set(derived_keys):
            disposition, reason = "FAIL", "declared_edge_not_derived"
        else:
            disposition, reason = "MATCH", "derived_from_rendered_bytes"
        recorder.add_row(
            "DECLARED_EDGE",
            composite=composite.composite_id,
            index=index,
            source=edge.source,
            target=edge.target,
            kind=edge.kind,
            disposition=disposition,
            reason=reason,
        )

    adjacency: dict[str, list[str]] = {member_id: [] for member_id in member_ids}
    graph_valid = not derivation_blocked and set(derived_keys) == set(declared_keys)
    for edge in derived:
        if edge.source not in member_ids or edge.target not in member_ids:
            graph_valid = False
            recorder.record(claim_id, Verdict.FAIL, "edge_endpoint_unknown")
        else:
            adjacency[edge.source].append(edge.target)
    reachable: set[str] = set()
    if graph_valid and id_counts.get(composite.entrypoint, 0) == 1:
        queue = [composite.entrypoint]
        while queue:
            node = queue.pop(0)
            if node in reachable:
                continue
            reachable.add(node)
            queue.extend(adjacency.get(node, []))
        if _has_cycle(composite.entrypoint, adjacency):
            recorder.record(claim_id, Verdict.FAIL, "derived_graph_cycle")
            graph_valid = False
        if reachable != member_ids:
            recorder.record(claim_id, Verdict.FAIL, "derived_member_unreachable")
            graph_valid = False
    else:
        recorder.record(claim_id, Verdict.STOP if derivation_blocked else Verdict.FAIL, "derived_graph_not_traversable")

    if derivation_blocked:
        # "every derived operand equals one declared deployed path" must not PASS over
        # a domain the derivation never closed.  The round-3 wrapper blind spot left
        # R7/F9 green precisely because no operand was derived at all (pattern 9).
        recorder.record(identity_claim, Verdict.STOP, "deployed_identity_domain_not_derived")

    for member in composite.members:
        if derivation_blocked:
            graph_disposition[member.member_id] = "STOP"
        elif graph_valid and member.member_id in reachable:
            graph_disposition[member.member_id] = "REACHABLE"
        else:
            graph_disposition[member.member_id] = "FAIL"
    recorder.add_row(
        "GRAPH_CONSERVATION",
        composite=composite.composite_id,
        input_members=len(composite.members),
        terminal_member_graph_dispositions=len(composite.members),
        terminal_deployed_identity_rows=len(composite.members),
        declared_edges=len(composite.edges),
        derived_edge_sites=len(derived),
        reachable_members=len(reachable),
    )
    return reachable, graph_disposition


def _render_member(
    composite: Composite,
    member: Member,
    template: RenderTemplate,
    plan_root: Path,
    recorder: Recorder,
) -> tuple[Verdict, str, int | None, str | None]:
    template_verdict, template_reason, _, template_data = _read_relative_file(plan_root, template.template_path)
    if template_verdict is not Verdict.PASS or template_data is None:
        recorder.record("R2", template_verdict, f"template_{template_reason}")
        return template_verdict, f"template_{template_reason}", None, None
    member_verdict, member_reason, _, rendered_data = _read_relative_file(plan_root, member.path)
    if member_verdict is not Verdict.PASS or rendered_data is None:
        recorder.record("R5", member_verdict, member_reason)
        return member_verdict, member_reason, None, None
    try:
        template_text = template_data.decode("utf-8")
    except UnicodeError:
        recorder.record("R2", Verdict.STOP, "template_not_utf8")
        return Verdict.STOP, "template_not_utf8", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()

    allocation_counts: dict[str, int] = {}
    allocation_values: dict[str, str] = {}
    for allocation in composite.allocations:
        allocation_counts[allocation.name] = allocation_counts.get(allocation.name, 0) + 1
        allocation_values[allocation.name] = allocation.value
    expected_consumers = {
        requirement.name for requirement in composite.requirements if member.member_id in requirement.consumers
    }
    token_names = RENDER_TOKEN_RE.findall(template_text)
    token_set = set(token_names)
    if "{{" in RENDER_TOKEN_RE.sub("", template_text) or "}}" in RENDER_TOKEN_RE.sub("", template_text):
        recorder.record("R3", Verdict.STOP, "render_token_malformed")
        return Verdict.STOP, "render_token_malformed", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()
    if token_set - set(allocation_values):
        recorder.record("R3", Verdict.STOP, "render_token_allocation_unknown")
        return Verdict.STOP, "render_token_allocation_unknown", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()
    if token_set != expected_consumers:
        recorder.record("R3", Verdict.FAIL, "render_consumer_token_mismatch")
        return Verdict.FAIL, "render_consumer_token_mismatch", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()
    if any(allocation_counts[name] != 1 for name in token_set):
        recorder.record("R3", Verdict.STOP, "render_allocation_not_unique")
        return Verdict.STOP, "render_allocation_not_unique", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()

    rendered_text = RENDER_TOKEN_RE.sub(lambda match: allocation_values[match.group(1)], template_text)
    expected = rendered_text.encode("utf-8")
    if RENDER_TOKEN_RE.search(rendered_text):
        recorder.record("R3", Verdict.STOP, "render_token_survived")
        return Verdict.STOP, "render_token_survived", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()
    if expected != rendered_data:
        recorder.record("R3", Verdict.FAIL, "rendered_bytes_mismatch")
        return Verdict.FAIL, "rendered_bytes_mismatch", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()
    return Verdict.PASS, "materialised_byte_exact", len(rendered_data), hashlib.sha256(rendered_data).hexdigest()


def run_render(plan: Plan, plan_path: Path, recorder: Recorder) -> None:
    if plan.schema != SCHEMA:
        recorder.stop_all("schema_version_unsupported")
        return
    if plan.stage is not Stage.RENDER:
        recorder.stop_all("stage_order_violation")
        return
    if not plan.composites:
        recorder.stop_all("composite_set_empty")
        return
    composite_counts: dict[str, int] = {}
    for composite in plan.composites:
        composite_counts[composite.composite_id] = composite_counts.get(composite.composite_id, 0) + 1
    for composite in plan.composites:
        if not _valid_identifier(composite.composite_id):
            recorder.record("R1", Verdict.STOP, "composite_identifier_invalid")
        if composite_counts[composite.composite_id] != 1:
            recorder.record("R1", Verdict.FAIL, "composite_identifier_duplicate")
        if not isinstance(composite.proof, RenderProof):
            recorder.stop_all("render_proof_contract_unavailable")
            continue
        member_ids = {member.member_id for member in composite.members}
        _process_allocations(composite, member_ids, recorder, "R2", "R3")
        binding_counts: dict[str, int] = {}
        for binding in composite.proof.templates:
            binding_counts[binding.member_id] = binding_counts.get(binding.member_id, 0) + 1
        if set(binding_counts) != member_ids or any(count != 1 for count in binding_counts.values()):
            recorder.record("R2", Verdict.FAIL, "render_template_member_not_one_to_one")
        template_path_counts: dict[str, int] = {}
        for binding in composite.proof.templates:
            template_path_counts[binding.template_path] = template_path_counts.get(binding.template_path, 0) + 1
        if any(count != 1 for count in template_path_counts.values()):
            recorder.record("R2", Verdict.FAIL, "render_template_path_alias")
        terminal_template_rows = 0
        for index, binding in enumerate(composite.proof.templates):
            reasons: list[str] = []
            if binding.member_id not in member_ids:
                reasons.append("template_member_unknown")
            if binding_counts.get(binding.member_id) != 1:
                reasons.append("template_member_not_unique")
            if template_path_counts.get(binding.template_path) != 1:
                reasons.append("template_path_alias")
            disposition = "FAIL" if reasons else "ACCEPT"
            terminal_template_rows += 1
            recorder.add_row(
                "RENDER_BINDING",
                composite=composite.composite_id,
                index=index,
                member=binding.member_id,
                template=binding.template_path,
                disposition=disposition,
                reasons=sorted(set(reasons)) or ["one_to_one"],
            )

        binding_by_member = {
            binding.member_id: binding
            for binding in composite.proof.templates
            if binding_counts.get(binding.member_id) == 1
        }
        render_results: dict[str, tuple[Verdict, str, int | None, str | None]] = {}
        for member in composite.members:
            if member.kind not in MEMBER_KINDS:
                recorder.record("R5", Verdict.STOP, "member_kind_not_implemented")
            binding = binding_by_member.get(member.member_id)
            if binding is None:
                render_results[member.member_id] = (Verdict.FAIL, "render_template_missing", None, None)
                continue
            result = _render_member(composite, member, binding, plan_path.parent, recorder)
            render_results[member.member_id] = result
            recorder.add_row(
                "RENDER_TEMPLATE",
                composite=composite.composite_id,
                member=member.member_id,
                template=binding.template_path,
                rendered=member.path,
                disposition=result[0].value,
                reason=result[1],
            )

        _, graph_dispositions = _derive_graph(composite, plan_path.parent, recorder, "R4", "R7")
        terminal_rows = 0
        for index, member in enumerate(composite.members):
            verdict, reason, byte_count, sha256 = render_results.get(
                member.member_id, (Verdict.STOP, "render_result_missing", None, None)
            )
            graph = graph_dispositions.get(member.member_id, "STOP")
            if graph == "STOP":
                disposition = "STOP"
            elif verdict is Verdict.STOP:
                disposition = "STOP"
            elif graph == "FAIL" or verdict is Verdict.FAIL:
                disposition = "FAIL"
            else:
                disposition = "ACCEPT"
            if disposition == "STOP":
                recorder.record("R6", Verdict.STOP, "render_member_stopped")
            elif disposition == "FAIL":
                recorder.record("R6", Verdict.FAIL, "render_member_rejected")
            terminal_rows += 1
            recorder.add_row(
                "RENDER_MEMBER",
                composite=composite.composite_id,
                index=index,
                id=member.member_id,
                kind=member.kind,
                path=member.path,
                deploy_path=member.deploy_path,
                graph=graph,
                materialisation=verdict.value,
                reason=reason,
                bytes=byte_count if byte_count is not None else "-",
                sha256=sha256 if sha256 is not None else "-",
                disposition=disposition,
            )
        recorder.add_row(
            "RENDER_CONSERVATION",
            composite=composite.composite_id,
            input_members=len(composite.members),
            input_templates=len(composite.proof.templates),
            terminal_template_rows=terminal_template_rows,
            terminal_member_rows=terminal_rows,
        )


def _pinned_file(
    plan_root: Path,
    relative: str,
    expected_bytes: int,
    expected_sha256: str,
) -> tuple[Verdict, str, Path | None, int | None, str | None, bytes | None]:
    if not SHA256_RE.fullmatch(expected_sha256):
        return Verdict.STOP, "pin_sha256_malformed", None, None, None, None
    verdict, reason, path, data = _read_relative_file(plan_root, relative)
    if verdict is not Verdict.PASS or path is None or data is None:
        return verdict, reason, path, None, None, None
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if len(data) != expected_bytes or actual_sha256 != expected_sha256:
        return Verdict.FAIL, "frozen_identity_mismatch", path, len(data), actual_sha256, data
    return Verdict.PASS, "frozen_identity_match", path, len(data), actual_sha256, data


class SubprocessPathProver:
    """Pinned-file adapter for the repaired pathscope prover output grammar."""

    _resolved_re = re.compile(
        r"^PATHSCOPE resolved_fs_path_count=(\d+) resolved_net_endpoint_count=(\d+)$"
    )
    _issue_re = re.compile(
        r"^PATHSCOPE unresolved_path_count=(\d+) unresolved_endpoint_count=(\d+) "
        r"coverage_issue_count=(\d+) provenance_issue_count=(\d+) parse_issue_count=(\d+)$"
    )
    _terminal_re = re.compile(r"^PATHSCOPE verdict=(PASS|REJECT) rc=([013]) reason=([^\s]+)$")
    _unresolved_re = re.compile(
        r"^UNRESOLVED line=\d+ kind=(parse|coverage|unresolved_path|unresolved_endpoint|provenance) "
    )

    def _stop_result(self, member_id: str, reason: str, rc: int | None = None) -> ProverMemberResult:
        return ProverMemberResult(member_id, Verdict.STOP, reason, rc, 0, 0, 0, 0, 0, 0, 0, "-", tuple())

    def _build_analysis_unit(self, request: PathProofRequest) -> tuple[str | None, str]:
        member_data = {member.member_id: member.data for member in request.shell_members}
        deploy_counts: dict[str, int] = {}
        for member in request.shell_members:
            identity = _canonical_deployed_path(member.deploy_path)
            if identity is None:
                return None, "analysis_unit_member_deploy_path_not_canonical_absolute"
            deploy_counts[identity] = deploy_counts.get(identity, 0) + 1
        if any(count != 1 for count in deploy_counts.values()):
            return None, "analysis_unit_member_deploy_path_ambiguous"
        deploy_to_id = {member.deploy_path: member.member_id for member in request.shell_members}
        constants_values = dict(request.constants_values)
        allocation_counts: dict[str, int] = {}
        allocation_values: dict[str, str] = {}
        for allocation in request.allocations:
            allocation_counts[allocation.name] = allocation_counts.get(allocation.name, 0) + 1
            allocation_values[allocation.name] = allocation.value
        unique_allocations = {
            name: value for name, value in allocation_values.items() if allocation_counts.get(name) == 1
        }
        declared = {(edge.source, edge.target, edge.kind) for edge in request.edges}
        visited: set[str] = set()
        stack: set[str] = set()

        def expand(member_id: str) -> tuple[str | None, str]:
            if member_id in stack:
                return None, "analysis_unit_source_cycle"
            data = member_data.get(member_id)
            if data is None:
                return None, "analysis_unit_member_path_missing"
            try:
                text = data.decode("utf-8")
            except UnicodeError:
                return None, "analysis_unit_member_read_error"
            stack.add(member_id)
            visited.add(member_id)
            output: list[str] = []
            for line in text.splitlines(keepends=True):
                sites = list(SOURCE_COMMAND_RE.finditer(line))
                if not sites:
                    output.append(line)
                    continue
                full = re.fullmatch(
                    r"(\s*)(?:source|\.)\s+((?:'[^']*'|\"[^\"]*\"|[^\s;|&()]+))\s*(?:#.*)?(?:\r?\n)?",
                    line,
                )
                if full is None or len(sites) != 1:
                    stack.remove(member_id)
                    return None, "analysis_unit_source_site_not_standalone"
                raw_operand = full.group(2)
                operand = _literal_shell_word(raw_operand, unique_allocations)
                if operand is None:
                    stack.remove(member_id)
                    return None, "analysis_unit_source_operand_dynamic"
                # The operand stays raw in the emitted unit, so the prover re-resolves it
                # from the pinned constants table.  Require the two sources to produce the
                # same string here as well as globally, so the file whose identity this
                # composite proved is the file the prover will reason about.
                constants_operand = _literal_shell_word(raw_operand, constants_values)
                if constants_operand is None:
                    stack.remove(member_id)
                    return None, "analysis_unit_source_operand_constants_unbound"
                if constants_operand != operand:
                    stack.remove(member_id)
                    return None, "analysis_unit_source_operand_constants_divergent"
                target = deploy_to_id.get(_canonical_deployed_path(operand) or "")
                if target is None:
                    stack.remove(member_id)
                    return None, "analysis_unit_source_operand_deploy_identity_unbound"
                if (member_id, target, "source") not in declared:
                    stack.remove(member_id)
                    return None, "analysis_unit_source_edge_unbound"
                child, reason = expand(target)
                if child is None:
                    stack.remove(member_id)
                    return None, reason
                indent = full.group(1)
                output.append(f"{indent}test -r {raw_operand}\n")
                output.append(f"{indent}# SEC102_BEGIN_SOURCE member={target}\n")
                output.append(child)
                if child and not child.endswith("\n"):
                    output.append("\n")
                output.append(f"{indent}# SEC102_END_SOURCE member={target}\n")
            stack.remove(member_id)
            return "".join(output), "analysis_unit_closed"

        if any(edge.kind != "source" for edge in request.edges):
            return None, "analysis_unit_non_source_edge_not_integrated"
        rendered, reason = expand(request.entrypoint)
        if rendered is None:
            return None, reason
        if visited != set(member_data):
            return None, "analysis_unit_member_conservation_mismatch"
        return rendered, "analysis_unit_closed"

    def _invoke_member(
        self,
        member_id: str,
        shell_path: Path,
        prover_path: Path,
        constants_path: Path,
        allowlist_path: Path,
    ) -> ProverMemberResult:
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(prover_path),
                    str(shell_path),
                    str(constants_path),
                    str(allowlist_path),
                ],
                cwd=shell_path.parent,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="strict",
                timeout=30,
                check=False,
            )
        except (OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
            return self._stop_result(member_id, f"prover_invocation_{type(exc).__name__}")
        if completed.stderr:
            return self._stop_result(member_id, "prover_stderr_nonempty", completed.returncode)
        lines = completed.stdout.splitlines()
        shell_headers = [line for line in lines if line.startswith("PATHSCOPE shell=")]
        semantics_headers = [line for line in lines if line.startswith("PATHSCOPE semantics=")]
        resolved_headers = [line for line in lines if line.startswith("PATHSCOPE resolved_")]
        issue_headers = [line for line in lines if line.startswith("PATHSCOPE unresolved_")]
        verdict_headers = [line for line in lines if line.startswith("PATHSCOPE verdict=")]
        semantics = [line for line in lines if line == (
            "PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established "
            "mount_boundary=not_established host_probe=none"
        )]
        resolved_lines = [match for line in lines if (match := self._resolved_re.fullmatch(line))]
        issue_lines = [match for line in lines if (match := self._issue_re.fullmatch(line))]
        terminal_lines = [match for line in lines if (match := self._terminal_re.fullmatch(line))]
        known_lines = [
            line
            for line in lines
            if line.startswith(("PATHSCOPE shell=", "PATHSCOPE semantics=", "PATHSCOPE resolved_", "PATHSCOPE unresolved_", "PATH ", "ENDPOINT ", "UNRESOLVED ", "PATHSCOPE verdict="))
        ]
        if len(known_lines) != len(lines):
            return self._stop_result(member_id, "prover_output_unknown_record", completed.returncode)
        if (
            len(shell_headers) != 1
            or len(semantics_headers) != 1
            or len(resolved_headers) != 1
            or len(issue_headers) != 1
            or len(verdict_headers) != 1
            or len(semantics) != 1
            or len(resolved_lines) != 1
            or len(issue_lines) != 1
            or len(terminal_lines) != 1
        ):
            return self._stop_result(member_id, "prover_output_grammar_incomplete", completed.returncode)
        resolved_fs, resolved_net = (int(value) for value in resolved_lines[0].groups())
        unresolved_path, unresolved_endpoint, coverage, provenance, parse = (
            int(value) for value in issue_lines[0].groups()
        )
        path_records = [line for line in lines if line.startswith("PATH ")]
        endpoint_records = [line for line in lines if line.startswith("ENDPOINT ")]
        unresolved_records = [line for line in lines if line.startswith("UNRESOLVED ")]
        if len(path_records) != resolved_fs or len(endpoint_records) != resolved_net:
            return self._stop_result(member_id, "prover_resolved_count_mismatch", completed.returncode)
        unresolved_by_kind = {
            "unresolved_path": 0,
            "unresolved_endpoint": 0,
            "coverage": 0,
            "provenance": 0,
            "parse": 0,
        }
        for line in unresolved_records:
            if line.count(" kind=") != 1:
                return self._stop_result(member_id, "prover_unresolved_kind_ambiguous", completed.returncode)
            match = self._unresolved_re.match(line)
            if match is None:
                return self._stop_result(member_id, "prover_unresolved_kind_missing", completed.returncode)
            unresolved_by_kind[match.group(1)] += 1
        if (
            unresolved_by_kind["unresolved_path"] != unresolved_path
            or unresolved_by_kind["unresolved_endpoint"] != unresolved_endpoint
            or unresolved_by_kind["coverage"] != coverage
            or unresolved_by_kind["provenance"] != provenance
            or unresolved_by_kind["parse"] != parse
        ):
            return self._stop_result(member_id, "prover_issue_count_mismatch", completed.returncode)
        for line in path_records:
            if line.count(" verdict=") != 1:
                return self._stop_result(member_id, "prover_path_disposition_ambiguous", completed.returncode)
            disposition = line.split(" verdict=", 1)[1].split(" ", 1)[0]
            if disposition not in {"ALLOW-LEXICAL", "FORBID"}:
                return self._stop_result(member_id, "prover_path_disposition_missing", completed.returncode)
        for line in endpoint_records:
            if line.count(" verdict=") != 1:
                return self._stop_result(member_id, "prover_endpoint_disposition_ambiguous", completed.returncode)
            disposition = line.split(" verdict=", 1)[1].split(" ", 1)[0]
            if disposition not in {"ALLOW", "FORBID"}:
                return self._stop_result(member_id, "prover_endpoint_disposition_missing", completed.returncode)

        terminal_verdict, terminal_rc_text, terminal_reason = terminal_lines[0].groups()
        terminal_rc = int(terminal_rc_text)
        if completed.returncode != terminal_rc:
            return self._stop_result(member_id, "prover_process_terminal_rc_mismatch", completed.returncode)
        total_issues = unresolved_path + unresolved_endpoint + coverage + provenance + parse
        has_forbid = any(" verdict=FORBID " in line for line in path_records + endpoint_records)
        if total_issues:
            verdict = Verdict.STOP
            reason = "prover_static_resolution_incomplete"
            if terminal_verdict != "REJECT" or terminal_rc != RC_STOP:
                return self._stop_result(member_id, "prover_issue_terminal_mismatch", completed.returncode)
            if terminal_reason != "static_resolution_incomplete":
                return self._stop_result(member_id, "prover_issue_reason_mismatch", completed.returncode)
        elif has_forbid:
            verdict = Verdict.FAIL
            reason = "prover_forbidden_operand"
            if terminal_verdict != "REJECT" or terminal_rc != RC_FAIL:
                return self._stop_result(member_id, "prover_forbid_terminal_mismatch", completed.returncode)
            if terminal_reason != "path_outside_allowlist":
                return self._stop_result(member_id, "prover_forbid_reason_mismatch", completed.returncode)
        else:
            verdict = Verdict.PASS
            reason = "prover_closed_and_allowlisted_lexical_scope"
            if terminal_verdict != "PASS" or terminal_rc != RC_PASS:
                return self._stop_result(member_id, "prover_pass_terminal_mismatch", completed.returncode)
            if terminal_reason != "closed_and_allowlisted_lexical_argv_scope":
                return self._stop_result(member_id, "prover_pass_reason_mismatch", completed.returncode)
        return ProverMemberResult(
            member_id,
            verdict,
            reason,
            completed.returncode,
            resolved_fs,
            resolved_net,
            unresolved_path,
            unresolved_endpoint,
            coverage,
            provenance,
            parse,
            f"{terminal_verdict}:{terminal_rc}:{terminal_reason}",
            tuple(path_records + endpoint_records + unresolved_records),
        )

    def prove(self, request: PathProofRequest) -> PathProofResult:
        if not request.shell_members:
            return PathProofResult(Verdict.STOP, "prover_shell_member_set_empty", tuple(), tuple())
        analysis_text, analysis_reason = self._build_analysis_unit(request)
        if analysis_text is None:
            result = self._stop_result(request.composite_id, analysis_reason)
            return PathProofResult(Verdict.STOP, analysis_reason, (result,), tuple())
        try:
            with tempfile.TemporaryDirectory(prefix="sec102-pathproof-") as temporary:
                temporary_root = Path(temporary)
                analysis_path = temporary_root / "whole_program.sh"
                constants_path = temporary_root / "constants.env"
                allowlist_path = temporary_root / "allowlist.txt"
                prover_path = temporary_root / "pathscope_prover.py"
                analysis_path.write_text(analysis_text, encoding="utf-8", newline="")
                constants_path.write_bytes(request.constants_data)
                allowlist_path.write_bytes(request.allowlist_data)
                prover_path.write_bytes(request.prover_data)
                results = (
                    self._invoke_member(
                        request.composite_id,
                        analysis_path,
                        prover_path,
                        constants_path,
                        allowlist_path,
                    ),
                )
        except OSError as exc:
            result = self._stop_result(request.composite_id, f"analysis_unit_{type(exc).__name__}")
            return PathProofResult(Verdict.STOP, result.reason, (result,), tuple())
        verdict = max((result.verdict for result in results), key=VERDICT_PRIORITY.__getitem__)
        total_resolved = sum(
            result.resolved_fs_path_count + result.resolved_net_endpoint_count for result in results
        )
        if verdict is Verdict.PASS and total_resolved == 0:
            verdict = Verdict.STOP
            reason = "prover_zero_facts_pass"
        elif verdict is Verdict.STOP:
            reason = "prover_member_stopped"
        elif verdict is Verdict.FAIL:
            reason = "prover_member_rejected"
        else:
            reason = "prover_members_closed_and_allowlisted_lexical_scope"
        residuals = (
            "R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED",
            "R1_MOUNT_BOUNDARY_NOT_ESTABLISHED",
        ) if all(result.terminal_record != "-" for result in results) else tuple()
        return PathProofResult(verdict, reason, results, residuals)


def run_freeze(plan: Plan, plan_path: Path, recorder: Recorder, path_prover: PathProver) -> None:
    if plan.schema != SCHEMA:
        recorder.stop_all("schema_version_unsupported")
        return
    if plan.stage is not Stage.FREEZE:
        recorder.stop_all("stage_order_violation")
        return
    if not plan.composites:
        recorder.stop_all("composite_set_empty")
        return
    composite_counts: dict[str, int] = {}
    for composite in plan.composites:
        composite_counts[composite.composite_id] = composite_counts.get(composite.composite_id, 0) + 1
    for composite in plan.composites:
        if not _valid_identifier(composite.composite_id):
            recorder.record("F1", Verdict.STOP, "composite_identifier_invalid")
        if composite_counts[composite.composite_id] != 1:
            recorder.record("F1", Verdict.FAIL, "composite_identifier_duplicate")
        if not isinstance(composite.proof, FreezeProof):
            recorder.stop_all("freeze_proof_contract_unavailable")
            continue
        proof = composite.proof
        _process_allocations(composite, {member.member_id for member in composite.members}, recorder, "F1", "F1")
        _, graph_dispositions = _derive_graph(composite, plan_path.parent, recorder, "F3", "F9")

        pin_counts: dict[str, int] = {}
        for pin in proof.member_pins:
            pin_counts[pin.member_id] = pin_counts.get(pin.member_id, 0) + 1
        member_ids = {member.member_id for member in composite.members}
        if set(pin_counts) != member_ids or any(count != 1 for count in pin_counts.values()):
            recorder.record("F2", Verdict.FAIL, "member_pin_not_one_to_one")
        terminal_pin_rows = 0
        for index, pin in enumerate(proof.member_pins):
            reasons: list[str] = []
            if pin.member_id not in member_ids:
                reasons.append("pin_member_unknown")
            if pin_counts.get(pin.member_id) != 1:
                reasons.append("pin_member_not_unique")
            if not SHA256_RE.fullmatch(pin.sha256):
                reasons.append("pin_sha256_malformed")
                recorder.record("F2", Verdict.STOP, "pin_sha256_malformed")
            terminal_pin_rows += 1
            recorder.add_row(
                "MEMBER_PIN",
                composite=composite.composite_id,
                index=index,
                member=pin.member_id,
                bytes=pin.byte_count,
                sha256=pin.sha256,
                disposition="STOP" if "pin_sha256_malformed" in reasons else "FAIL" if reasons else "ACCEPT",
                reasons=sorted(set(reasons)) or ["one_to_one_well_formed"],
            )
        pin_by_member = {
            pin.member_id: pin for pin in proof.member_pins if pin_counts.get(pin.member_id) == 1
        }
        member_snapshots: dict[str, bytes] = {}
        member_identity: dict[str, tuple[Verdict, str, int | None, str | None]] = {}
        for member in composite.members:
            pin = pin_by_member.get(member.member_id)
            if pin is None:
                member_identity[member.member_id] = (Verdict.FAIL, "member_pin_missing", None, None)
                continue
            verdict, reason, _, actual_bytes, actual_sha256, data = _pinned_file(
                plan_path.parent, member.path, pin.byte_count, pin.sha256
            )
            recorder.record("F2", verdict, reason)
            member_identity[member.member_id] = (verdict, reason, actual_bytes, actual_sha256)
            if data is not None:
                member_snapshots[member.member_id] = data

        if (
            proof.prover_path != "pathscope_prover.py"
            or proof.prover_bytes != APPROVED_PROVER_BYTES
            or proof.prover_sha256 != APPROVED_PROVER_SHA256
        ):
            recorder.record("F4", Verdict.FAIL, "approved_prover_identity_not_declared")
        proof_inputs = (
            ("constants", plan_path.parent, proof.constants_path, proof.constants_bytes, proof.constants_sha256, "F2"),
            ("allowlist", plan_path.parent, proof.allowlist_path, proof.allowlist_bytes, proof.allowlist_sha256, "F2"),
            (
                "prover",
                Path(__file__).resolve().parent,
                proof.prover_path,
                proof.prover_bytes,
                proof.prover_sha256,
                "F4",
            ),
        )
        proof_snapshots: dict[str, bytes] = {}
        proof_input_verdicts: dict[str, Verdict] = {}
        for role, input_root, relative, expected_bytes, expected_sha256, claim_id in proof_inputs:
            verdict, reason, _, actual_bytes, actual_sha256, data = _pinned_file(
                input_root, relative, expected_bytes, expected_sha256
            )
            recorder.record(claim_id, verdict, reason)
            proof_input_verdicts[role] = verdict
            if data is not None:
                proof_snapshots[role] = data
            recorder.add_row(
                "FREEZE_INPUT",
                composite=composite.composite_id,
                role=role,
                path=relative,
                expected_bytes=expected_bytes,
                actual_bytes=actual_bytes if actual_bytes is not None else "-",
                expected_sha256=expected_sha256,
                actual_sha256=actual_sha256 if actual_sha256 is not None else "-",
                disposition=verdict.value,
                reason=reason,
            )

        constants_map: dict[str, str] | None = None
        constant_bindings: tuple[ConstantBinding, ...] = tuple()
        reconciliation_reasons: tuple[str, ...] = ("constants_input_not_pinned",)
        allocation_bindings: tuple[AllocationBinding, ...] = _allocation_rows(
            composite, "STOP", "constants_input_not_pinned"
        )
        if proof_input_verdicts.get("constants") is Verdict.PASS and "constants" in proof_snapshots:
            (
                constants_map,
                constant_bindings,
                allocation_bindings,
                reconciliation_reasons,
            ) = _reconcile_constants(composite, proof_snapshots["constants"])
        for reason in reconciliation_reasons:
            recorder.record("F10", Verdict.STOP, reason)
        for index, binding in enumerate(constant_bindings):
            recorder.add_row(
                "CONSTANT",
                composite=composite.composite_id,
                index=index,
                line=binding.line,
                name=binding.name,
                value=binding.value if binding.value is not None else "-",
                disposition=binding.disposition,
                reason=binding.reason,
            )
        for binding in allocation_bindings:
            recorder.add_row(
                "ALLOCATION_RECONCILIATION",
                composite=composite.composite_id,
                index=binding.index,
                name=binding.name,
                value=binding.value,
                disposition=binding.disposition,
                reason=binding.reason,
            )
        grammar_closed = not set(reconciliation_reasons) & {
            "constants_not_utf8",
            "constants_line_not_key_value",
            "constants_duplicate_name",
            "constants_input_not_pinned",
        }
        recorder.add_row(
            "CONSTANTS_CONSERVATION",
            composite=composite.composite_id,
            grammar="closed" if grammar_closed else "not_closed",
            plan_allocations=len(composite.allocations),
            parsed_bindings=len(constant_bindings),
            terminal_constant_rows=len(constant_bindings),
            terminal_allocation_rows=len(allocation_bindings),
            reconciled=sum(1 for item in constant_bindings if item.disposition == "RECONCILED"),
            runtime_only=sum(1 for item in constant_bindings if item.disposition == "RUNTIME_ONLY"),
            stopped=sum(1 for item in constant_bindings if item.disposition == "STOP"),
            allocations_reconciled=sum(
                1 for item in allocation_bindings if item.disposition == "RECONCILED"
            ),
            allocations_stopped=sum(
                1 for item in allocation_bindings if item.disposition == "STOP"
            ),
        )

        invocable = (
            all(role in proof_snapshots for role in ("constants", "allowlist", "prover"))
            and all(proof_input_verdicts.get(role) is Verdict.PASS for role in ("constants", "allowlist", "prover"))
            and all(member.member_id in member_snapshots for member in composite.members)
            and all(result[0] is Verdict.PASS for result in member_identity.values())
            and all(value == "REACHABLE" for value in graph_dispositions.values())
            and constants_map is not None
        )
        if any(member.kind != "shell" for member in composite.members):
            recorder.record("F6", Verdict.STOP, "non_shell_member_analyzer_not_integrated")
            invocable = False
        if invocable and constants_map is not None:
            shell_members = tuple(
                ShellMember(
                    member.member_id,
                    member.path,
                    member.deploy_path,
                    member_snapshots[member.member_id],
                )
                for member in composite.members
            )
            result = path_prover.prove(
                PathProofRequest(
                    Stage.FREEZE,
                    composite.composite_id,
                    shell_members,
                    composite.entrypoint,
                    composite.edges,
                    composite.allocations,
                    tuple(sorted(constants_map.items())),
                    proof_snapshots["constants"],
                    proof_snapshots["allowlist"],
                    proof_snapshots["prover"],
                )
            )
        else:
            result = PathProofResult(Verdict.STOP, "prover_prerequisite_not_closed", tuple(), tuple())
        recorder.record("F5", result.verdict, result.reason)
        recorder.record("F6", result.verdict, result.reason)

        for member_result in result.member_results:
            recorder.add_row(
                "PROVER_MEMBER",
                composite=composite.composite_id,
                member=member_result.member_id,
                process_rc=member_result.process_rc if member_result.process_rc is not None else "-",
                resolved_fs_path_count=member_result.resolved_fs_path_count,
                resolved_net_endpoint_count=member_result.resolved_net_endpoint_count,
                unresolved_path_count=member_result.unresolved_path_count,
                unresolved_endpoint_count=member_result.unresolved_endpoint_count,
                coverage_issue_count=member_result.coverage_issue_count,
                provenance_issue_count=member_result.provenance_issue_count,
                parse_issue_count=member_result.parse_issue_count,
                terminal=member_result.terminal_record,
                disposition=member_result.verdict.value,
                reason=member_result.reason,
            )
            for index, record in enumerate(member_result.records):
                recorder.add_row(
                    "PROVER_RECORD",
                    composite=composite.composite_id,
                    member=member_result.member_id,
                    index=index,
                    record=record,
                    disposition="ACCOUNTED",
                )

        required_residuals = {
            "R1_SYMLINK_RESOLUTION_NOT_ESTABLISHED",
            "R1_MOUNT_BOUNDARY_NOT_ESTABLISHED",
        }
        if set(result.residuals) != required_residuals:
            recorder.record("F7", Verdict.STOP, "prover_residual_disclosure_missing")
        for residual in sorted(required_residuals):
            disclosed = residual in result.residuals
            recorder.add_row(
                "RESIDUAL",
                composite=composite.composite_id,
                id=residual,
                disposition="DISCLOSURE" if disclosed else "STOP",
                control=False,
                reason="lexical_prover_does_not_establish_host_object_binding",
            )
        # The deployed identity this stage compares is a declared, lexically canonical
        # string.  No host was contacted, so nothing here establishes that the object
        # living at that path is the pinned member.  Disclosed always, never a control.
        recorder.add_row(
            "RESIDUAL",
            composite=composite.composite_id,
            id="R2_DEPLOYED_PATH_HOST_OBJECT_NOT_ESTABLISHED",
            disposition="DISCLOSURE",
            control=False,
            reason="deploy_path_is_declared_and_lexically_compared_not_host_verified",
        )

        terminal_rows = 0
        for index, member in enumerate(composite.members):
            identity_verdict, identity_reason, actual_bytes, actual_sha256 = member_identity.get(
                member.member_id, (Verdict.STOP, "member_identity_missing", None, None)
            )
            graph = graph_dispositions.get(member.member_id, "STOP")
            prover_verdict = result.verdict
            disposition = max(
                (
                    identity_verdict,
                    Verdict.PASS if graph == "REACHABLE" else Verdict.STOP if graph == "STOP" else Verdict.FAIL,
                    prover_verdict,
                ),
                key=VERDICT_PRIORITY.__getitem__,
            )
            recorder.record("F8", disposition, f"freeze_member_{disposition.value.lower()}")
            terminal_rows += 1
            recorder.add_row(
                "FREEZE_MEMBER",
                composite=composite.composite_id,
                index=index,
                id=member.member_id,
                path=member.path,
                deploy_path=member.deploy_path,
                graph=graph,
                identity=identity_verdict.value,
                identity_reason=identity_reason,
                prover=prover_verdict.value,
                bytes=actual_bytes if actual_bytes is not None else "-",
                sha256=actual_sha256 if actual_sha256 is not None else "-",
                disposition=disposition.value,
            )
        recorder.add_row(
            "FREEZE_CONSERVATION",
            composite=composite.composite_id,
            input_members=len(composite.members),
            member_pins=len(proof.member_pins),
            terminal_member_pin_rows=terminal_pin_rows,
            input_allocations=len(composite.allocations),
            terminal_allocation_rows=len(allocation_bindings),
            terminal_constant_rows=len(constant_bindings),
            prover_member_results=len(result.member_results),
            terminal_member_rows=terminal_rows,
            residual_rows=len(required_residuals) + 1,
        )


def run_allocate(plan: Plan, plan_path: Path, recorder: Recorder) -> None:
    if plan.schema != SCHEMA:
        recorder.stop_all("schema_version_unsupported")
        return
    if plan.stage is not Stage.ALLOCATE:
        recorder.stop_all("stage_order_violation")
        return
    if not plan.composites:
        recorder.record("A1", Verdict.STOP, "composite_set_empty")
        for claim_id in ("A2", "A3", "A4", "A5", "A6"):
            recorder.record(claim_id, Verdict.STOP, "composite_set_unavailable")
        return

    composite_counts: dict[str, int] = {}
    for composite in plan.composites:
        composite_counts[composite.composite_id] = composite_counts.get(composite.composite_id, 0) + 1
    for composite in plan.composites:
        if not _valid_identifier(composite.composite_id):
            recorder.record("A1", Verdict.STOP, "composite_identifier_invalid")
        if composite_counts[composite.composite_id] != 1:
            recorder.record("A1", Verdict.FAIL, "composite_identifier_duplicate")
        _process_graph_and_identity(composite, plan_path.parent, recorder)

    recorder.add_row(
        "PATH_PROVER",
        adapter="not_applicable",
        disposition="NOT_INVOKED",
        reason="allocate_stage_has_no_path_proof_claim",
    )


def output_report(plan_argument: str, requested_stage: Stage, recorder: Recorder, input_stop: InputStop | None) -> int:
    print(
        "COMPOSITE_PATHPROOF "
        f"schema={json.dumps(SCHEMA)} requested_stage={json.dumps(requested_stage.value)} "
        f"plan={json.dumps(plan_argument, ensure_ascii=True)}"
    )
    print("CONTRACT pass_rc=0 fail_rc=1 stop_rc=3 precedence=STOP>FAIL>PASS")
    if input_stop is not None:
        recorder.stop_all(input_stop.reason)
        recorder.add_row("INPUT", disposition="STOP", reason=input_stop.reason, detail=input_stop.detail)

    for claim_id in recorder.claim_order:
        claim = recorder.claims[claim_id]
        print(
            "CLAIM "
            f"id={json.dumps(claim.claim_id)} name={json.dumps(claim.name)} "
            f"verdict={json.dumps(claim.verdict.value)} reason={json.dumps(claim.render_reason())}"
        )
    for row in recorder.rows:
        print(row.render())

    verdict = recorder.verdict
    reason = {
        Verdict.PASS: f"{requested_stage.value}_stage_closed",
        Verdict.FAIL: f"{requested_stage.value}_stage_deviant",
        Verdict.STOP: f"{requested_stage.value}_stage_incomplete",
    }[verdict]
    print(f"COMPOSITE_PATHPROOF verdict={verdict.value} rc={verdict.rc} reason={reason}")
    return verdict.rc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=[stage.value for stage in Stage])
    parser.add_argument("plan", help="UTF-8 JSON composite plan")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    requested_stage = Stage(args.stage)
    plan_argument = args.plan
    plan_path = Path(plan_argument)
    recorder = Recorder(requested_stage)
    input_stop: InputStop | None = None
    plan: Plan | None = None
    try:
        plan = load_plan(plan_path)
    except InputStop as exc:
        input_stop = exc

    if plan is not None:
        if plan.stage is not requested_stage:
            recorder.stop_all("requested_stage_plan_stage_mismatch")
        elif requested_stage is Stage.ALLOCATE:
            run_allocate(plan, plan_path, recorder)
        elif requested_stage is Stage.RENDER:
            run_render(plan, plan_path, recorder)
        else:
            run_freeze(plan, plan_path, recorder, SubprocessPathProver())
    return output_report(plan_argument, requested_stage, recorder, input_stop)


if __name__ == "__main__":
    sys.exit(main())
