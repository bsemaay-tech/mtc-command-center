#!/usr/bin/env python3
"""Fail-closed scaffold for the Section 10.2 composite path proof.

Round 1 implements only the ALLOCATE stage.  It proves conservation and
identity properties of an allocation plan without executing any subject file.
RENDER, FREEZE, and path-prover integration deliberately return STOP (rc 3).

The existing pathscope_prover.py is intentionally neither imported nor read.
It is represented only by the swappable PathProver interface below.
"""

from __future__ import annotations

import argparse
import dataclasses
import enum
import hashlib
import json
import posixpath
import re
import sys
from pathlib import Path
from typing import Any, Protocol, Sequence


SCHEMA = "sec102-composite-plan-v1"
RC_PASS = 0
RC_FAIL = 1
RC_STOP = 3

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
MEMBER_KEYS = frozenset({"id", "kind", "path"})
EDGE_KEYS = frozenset({"from", "to", "kind"})
REQUIREMENT_KEYS = frozenset({"name", "kind", "consumers"})
ALLOCATION_KEYS = frozenset({"name", "value"})
MEMBER_KINDS = frozenset({"shell", "python_source"})
EDGE_KINDS = frozenset({"source", "execute_source", "inline_source"})
ALLOCATION_KINDS = frozenset({"safe_component", "absolute_path"})

CLAIMS = (
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
class Composite:
    composite_id: str
    entrypoint: str
    members: tuple[Member, ...]
    edges: tuple[Edge, ...]
    requirements: tuple[AllocationRequirement, ...]
    allocations: tuple[Allocation, ...]


@dataclasses.dataclass(frozen=True)
class Plan:
    schema: str
    stage: Stage
    composites: tuple[Composite, ...]


@dataclasses.dataclass(frozen=True)
class PathProofRequest:
    stage: Stage
    composite_id: str
    component_identities: tuple[tuple[str, int, str], ...]


@dataclasses.dataclass(frozen=True)
class PathProofResult:
    verdict: Verdict
    reason: str


class PathProver(Protocol):
    """Swappable boundary; no unrepaired prover implementation is depended on."""

    def prove(self, request: PathProofRequest) -> PathProofResult:
        ...


class StubPathProver:
    """Round-1 fail-closed adapter used until a separately accepted component exists."""

    def prove(self, request: PathProofRequest) -> PathProofResult:
        del request
        return PathProofResult(Verdict.STOP, "path_prover_component_not_integrated")


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
    def __init__(self) -> None:
        self.claims = {claim_id: ClaimState(claim_id, name, reason) for claim_id, name, reason in CLAIMS}
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


def _expect_mapping(value: Any, context: str, allowed_keys: frozenset[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InputStop("plan_schema_type_error", f"{context}:expected_object")
    unknown = sorted(set(value) - allowed_keys)
    missing = sorted(allowed_keys - set(value))
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


def _parse_member(raw: Any, context: str) -> Member:
    item = _expect_mapping(raw, context, MEMBER_KEYS)
    return Member(
        _expect_string(item["id"], f"{context}.id"),
        _expect_string(item["kind"], f"{context}.kind"),
        _expect_string(item["path"], f"{context}.path"),
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
        item = _expect_mapping(raw_composite, context, COMPOSITE_KEYS)
        members = tuple(
            _parse_member(value, f"{context}.members[{index}]")
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


def _member_file_identity(plan_root: Path, relative: str) -> tuple[Verdict, str, int | None, str | None]:
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
    return Verdict.PASS, "identified", len(data), hashlib.sha256(data).hexdigest()


def _process_allocations(composite: Composite, member_ids: set[str], recorder: Recorder) -> None:
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
            recorder.record("A3", Verdict.STOP, "requirement_name_invalid")
        if requirement_counts[requirement.name] != 1:
            disposition = "FAIL"
            reasons.append("duplicate_requirement")
            recorder.record("A3", Verdict.FAIL, "duplicate_requirement")
        if requirement.kind not in ALLOCATION_KINDS:
            disposition = "STOP"
            reasons.append("allocation_kind_not_implemented")
            recorder.record("A4", Verdict.STOP, "allocation_kind_not_implemented")
        if allocation_counts.get(requirement.name, 0) == 0:
            disposition = "STOP"
            reasons.append("allocation_missing")
            recorder.record("A3", Verdict.STOP, "allocation_missing")
        elif allocation_counts[requirement.name] != 1:
            disposition = "FAIL"
            reasons.append("allocation_not_one_to_one")
            recorder.record("A3", Verdict.FAIL, "allocation_not_one_to_one")
        if not requirement.consumers:
            disposition = "FAIL"
            reasons.append("consumer_set_empty")
            recorder.record("A3", Verdict.FAIL, "consumer_set_empty")
        if len(set(requirement.consumers)) != len(requirement.consumers):
            disposition = "FAIL"
            reasons.append("consumer_duplicate")
            recorder.record("A3", Verdict.FAIL, "consumer_duplicate")
        unknown_consumers = sorted(set(requirement.consumers) - member_ids)
        if unknown_consumers:
            disposition = "FAIL"
            reasons.append("consumer_unknown")
            recorder.record("A3", Verdict.FAIL, "consumer_unknown")
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
            recorder.record("A3", Verdict.FAIL, "allocation_undeclared")
        if allocation_counts[allocation.name] != 1:
            disposition = "FAIL"
            reasons.append("allocation_duplicate")
            recorder.record("A3", Verdict.FAIL, "allocation_duplicate")
        matching = [requirement for requirement in composite.requirements if requirement.name == allocation.name]
        if len(matching) == 1:
            value_verdict, value_reason = _allocation_value_verdict(matching[0].kind, allocation.value)
            if value_verdict is not Verdict.PASS:
                disposition = value_verdict.value
                reasons.append(value_reason)
                recorder.record("A4", value_verdict, value_reason)
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

    _process_allocations(composite, member_ids, recorder)
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
        adapter="stub",
        disposition="NOT_INVOKED",
        reason="allocate_stage_has_no_path_proof_claim",
    )


def _run_unimplemented(stage: Stage, recorder: Recorder, path_prover: PathProver) -> None:
    if stage is Stage.RENDER:
        recorder.stop_all("render_stage_not_implemented_round1")
        recorder.add_row(
            "STAGE",
            stage=stage.value,
            disposition="STOP",
            reason="render_stage_not_implemented_round1",
        )
        return
    result = path_prover.prove(PathProofRequest(stage, "-", tuple()))
    recorder.stop_all(result.reason)
    recorder.add_row(
        "PATH_PROVER",
        adapter="stub",
        disposition=result.verdict.value,
        reason=result.reason,
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

    for claim_id, _, _ in CLAIMS:
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
    recorder = Recorder()
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
        else:
            _run_unimplemented(requested_stage, recorder, StubPathProver())
    return output_report(plan_argument, requested_stage, recorder, input_stop)


if __name__ == "__main__":
    sys.exit(main())
