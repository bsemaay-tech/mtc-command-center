from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Mapping, Sequence


SCENARIO_TOP_LEVEL_KEYS = frozenset(
    {
        "scenario_id",
        "producer_adapter",
        "complete_inputs",
        "literal_expected_observation",
        "literal_expected_final_state",
        "expectation_derivation",
        "comparison_rule",
        "clean_producer_corroboration",
        "producer_mutation",
    }
)

EXPECTED_ROW_POSITIONS = {f"C{index:02d}": index - 1 for index in range(1, 43)}

_CONSUMER_BY_FIELD = {
    "scenario_id": "scenario_identity_comparator",
    "producer_adapter": "scenario_identity_comparator",
    "complete_inputs": "producer_input_binding",
    "literal_expected_observation": "recursive_exact_comparator",
    "literal_expected_final_state": "recursive_exact_comparator",
    "expectation_derivation": "expectation_provenance_verifier",
    "comparison_rule": "recursive_exact_comparator",
    "clean_producer_corroboration": "authority_execution",
    "producer_mutation": "producer_mutation_restoration",
}


class ScenarioBindingError(RuntimeError):
    pass


class ScenarioShapeError(ScenarioBindingError):
    pass


class ScenarioValueError(ScenarioBindingError):
    pass


class ManifestRowError(ScenarioBindingError):
    pass


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], path: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ScenarioShapeError(
            f"{path} exact key-set mismatch: missing={missing} extra={extra}"
        )


def _require_type(value: Any, expected: type, path: str) -> None:
    if type(value) is not expected:
        raise ScenarioShapeError(
            f"{path} type mismatch: expected={expected.__name__} actual={type(value).__name__}"
        )


@dataclass(frozen=True)
class ExpectationProvenance:
    method: str
    source: Mapping[str, Any]
    producer_output_may_not_rebless_expected: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> ExpectationProvenance:
        _require_exact_keys(
            value,
            {"method", "source", "producer_output_may_not_rebless_expected"},
            "$.expectation_derivation",
        )
        _require_type(value["method"], str, "$.expectation_derivation.method")
        _require_type(value["source"], dict, "$.expectation_derivation.source")
        _require_type(
            value["producer_output_may_not_rebless_expected"],
            bool,
            "$.expectation_derivation.producer_output_may_not_rebless_expected",
        )
        return cls(
            method=value["method"],
            source=deepcopy(value["source"]),
            producer_output_may_not_rebless_expected=value[
                "producer_output_may_not_rebless_expected"
            ],
        )

    def as_mapping(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "source": deepcopy(dict(self.source)),
            "producer_output_may_not_rebless_expected": self.producer_output_may_not_rebless_expected,
        }


@dataclass(frozen=True)
class ProducerCorroboration:
    status: str
    required: bool
    authority_names: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> ProducerCorroboration:
        _require_exact_keys(
            value,
            {"status", "required", "authority_names"},
            "$.clean_producer_corroboration",
        )
        _require_type(value["status"], str, "$.clean_producer_corroboration.status")
        _require_type(value["required"], bool, "$.clean_producer_corroboration.required")
        _require_type(
            value["authority_names"], list, "$.clean_producer_corroboration.authority_names"
        )
        if any(type(item) is not str for item in value["authority_names"]):
            raise ScenarioShapeError(
                "$.clean_producer_corroboration.authority_names must contain only strings"
            )
        return cls(
            status=value["status"],
            required=value["required"],
            authority_names=tuple(value["authority_names"]),
        )

    def as_mapping(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "required": self.required,
            "authority_names": list(self.authority_names),
        }


@dataclass(frozen=True)
class MutationCriteria:
    mutation_id: str
    source_seam: str
    mutation: str
    required_red: str
    restored_green: str
    status: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> MutationCriteria:
        keys = {
            "mutation_id",
            "source_seam",
            "mutation",
            "required_red",
            "restored_green",
            "status",
        }
        _require_exact_keys(value, keys, "$.producer_mutation")
        for key in sorted(keys):
            _require_type(value[key], str, f"$.producer_mutation.{key}")
        return cls(**{key: value[key] for key in keys})

    def as_mapping(self) -> dict[str, Any]:
        return {
            "mutation_id": self.mutation_id,
            "source_seam": self.source_seam,
            "mutation": self.mutation,
            "required_red": self.required_red,
            "restored_green": self.restored_green,
            "status": self.status,
        }


@dataclass(frozen=True)
class ScenarioContract:
    scenario_id: str
    producer_adapter: str
    complete_inputs: Mapping[str, Any]
    literal_expected_observation: Mapping[str, Any]
    literal_expected_final_state: Mapping[str, Any]
    expectation_derivation: ExpectationProvenance
    comparison_rule: str
    clean_producer_corroboration: ProducerCorroboration
    producer_mutation: MutationCriteria
    consumer_by_field: Mapping[str, str] = field(
        default_factory=lambda: dict(_CONSUMER_BY_FIELD), repr=False
    )

    def __post_init__(self) -> None:
        _require_type(self.scenario_id, str, "$.scenario_id")
        _require_type(self.producer_adapter, str, "$.producer_adapter")
        _require_type(self.complete_inputs, dict, "$.complete_inputs")
        _require_type(
            self.literal_expected_observation, dict, "$.literal_expected_observation"
        )
        _require_type(
            self.literal_expected_final_state, dict, "$.literal_expected_final_state"
        )
        _require_type(self.comparison_rule, str, "$.comparison_rule")
        _require_exact_keys(
            self.consumer_by_field,
            set(SCENARIO_TOP_LEVEL_KEYS),
            "ScenarioContract.consumer_by_field",
        )
        if any(type(item) is not str for item in self.consumer_by_field.values()):
            raise ScenarioShapeError("ScenarioContract consumers must be named strings")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> ScenarioContract:
        _require_type(value, dict, "$")
        _require_exact_keys(value, set(SCENARIO_TOP_LEVEL_KEYS), "$")
        for key in (
            "scenario_id",
            "producer_adapter",
            "comparison_rule",
        ):
            _require_type(value[key], str, f"$.{key}")
        for key in (
            "complete_inputs",
            "literal_expected_observation",
            "literal_expected_final_state",
        ):
            _require_type(value[key], dict, f"$.{key}")
        return cls(
            scenario_id=value["scenario_id"],
            producer_adapter=value["producer_adapter"],
            complete_inputs=deepcopy(value["complete_inputs"]),
            literal_expected_observation=deepcopy(value["literal_expected_observation"]),
            literal_expected_final_state=deepcopy(value["literal_expected_final_state"]),
            expectation_derivation=ExpectationProvenance.from_mapping(
                value["expectation_derivation"]
            ),
            comparison_rule=value["comparison_rule"],
            clean_producer_corroboration=ProducerCorroboration.from_mapping(
                value["clean_producer_corroboration"]
            ),
            producer_mutation=MutationCriteria.from_mapping(value["producer_mutation"]),
        )

    def as_mapping(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "producer_adapter": self.producer_adapter,
            "complete_inputs": deepcopy(dict(self.complete_inputs)),
            "literal_expected_observation": deepcopy(
                dict(self.literal_expected_observation)
            ),
            "literal_expected_final_state": deepcopy(dict(self.literal_expected_final_state)),
            "expectation_derivation": self.expectation_derivation.as_mapping(),
            "comparison_rule": self.comparison_rule,
            "clean_producer_corroboration": self.clean_producer_corroboration.as_mapping(),
            "producer_mutation": self.producer_mutation.as_mapping(),
        }


@dataclass(frozen=True)
class ManifestScenarioSource:
    manifest: Mapping[str, Any]
    row_id: str
    expected_position: int | None = None
    scenario_index: int = 0
    require_single_scenario: bool = True


@dataclass(frozen=True)
class DeclaredLeaf:
    path: str
    value: Any
    expected_consumer: str


@dataclass(frozen=True)
class BindingLedger:
    contract: ScenarioContract
    declared_leaves: tuple[DeclaredLeaf, ...]
    bound_paths: tuple[str, ...]


@dataclass(frozen=True)
class ConsumerEvidence:
    consumer: str
    declaration_paths: tuple[str, ...]
    evidence: Mapping[str, Any]


@dataclass(frozen=True)
class ExecutionEvidence:
    comparators: tuple[ConsumerEvidence, ...] = ()
    authority_executions: tuple[ConsumerEvidence, ...] = ()
    mutation_restorations: tuple[ConsumerEvidence, ...] = ()

    def records(self) -> tuple[ConsumerEvidence, ...]:
        return self.comparators + self.authority_executions + self.mutation_restorations


@dataclass(frozen=True)
class ConsumedLeaf:
    path: str
    consumer: str
    evidence: Mapping[str, Any]


@dataclass(frozen=True)
class ConsumptionLedger:
    binding: BindingLedger
    consumed_leaves: tuple[ConsumedLeaf, ...]


def lookup_manifest_row(
    manifest: Mapping[str, Any], row_id: str, expected_position: int | None = None
) -> Mapping[str, Any]:
    rows = manifest.get("rows")
    if type(rows) is not list:
        raise ManifestRowError("manifest rows must be a list")
    for index, row in enumerate(rows):
        if type(row) is not dict:
            raise ManifestRowError(
                f"manifest row must be an object: position={index} actual={type(row).__name__}"
            )
    matches = [
        (index, row) for index, row in enumerate(rows) if row.get("row_id") == row_id
    ]
    if not matches:
        raise ManifestRowError(f"manifest row id is absent: {row_id}")
    if len(matches) != 1:
        raise ManifestRowError(f"manifest row id is duplicated: {row_id}")
    position, row = matches[0]
    if expected_position is not None and position != expected_position:
        raise ManifestRowError(
            f"manifest row position mismatch for {row_id}: expected={expected_position} actual={position}"
        )
    return row


def manifest_scenario(source: ManifestScenarioSource) -> Mapping[str, Any]:
    row = lookup_manifest_row(source.manifest, source.row_id, source.expected_position)
    scenarios = row.get("scenarios")
    if type(scenarios) is not list:
        raise ScenarioShapeError(f"{source.row_id} scenarios must be a list")
    if source.require_single_scenario and len(scenarios) != 1:
        raise ScenarioShapeError(
            f"{source.row_id} must contain exactly one scenario: actual={len(scenarios)}"
        )
    if source.scenario_index < 0 or source.scenario_index >= len(scenarios):
        raise ScenarioShapeError(
            f"{source.row_id} scenario index is absent: {source.scenario_index}"
        )
    scenario = scenarios[source.scenario_index]
    if type(scenario) is not dict:
        raise ScenarioShapeError(
            f"{source.row_id} scenario must be an object: index={source.scenario_index}"
        )
    return scenario


def verify_manifest_row_positions(manifest: Mapping[str, Any], row_ids: Sequence[str]) -> None:
    rows = manifest.get("rows")
    if type(rows) is not list or len(rows) != len(row_ids):
        actual = len(rows) if type(rows) is list else type(rows).__name__
        raise ManifestRowError(
            f"manifest row count mismatch: expected={len(row_ids)} actual={actual}"
        )
    for expected_position, row_id in enumerate(row_ids):
        lookup_manifest_row(manifest, row_id, expected_position)


def _leaf_items(value: Any, path: str = "$") -> list[tuple[str, Any]]:
    if type(value) is dict:
        if not value:
            return [(path, {})]
        leaves: list[tuple[str, Any]] = []
        for key in sorted(value):
            leaves.extend(_leaf_items(value[key], f"{path}.{key}"))
        return leaves
    if type(value) is list:
        if not value:
            return [(path, [])]
        leaves = []
        for index, item in enumerate(value):
            leaves.extend(_leaf_items(item, f"{path}[{index}]"))
        return leaves
    return [(path, value)]


def _bind_exact(expected: Any, actual: Any, path: str = "$") -> None:
    if type(expected) is not type(actual):
        raise ScenarioValueError(
            f"declaration path {path} type differs: expected={type(expected).__name__} "
            f"actual={type(actual).__name__}"
        )
    if type(expected) is dict:
        expected_keys = set(expected)
        actual_keys = set(actual)
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        if missing or extra:
            raise ScenarioShapeError(
                f"declaration path {path} exact key-set mismatch: missing={missing} extra={extra}"
            )
        for key in sorted(expected):
            _bind_exact(expected[key], actual[key], f"{path}.{key}")
        return
    if type(expected) is list:
        if len(expected) != len(actual):
            raise ScenarioValueError(
                f"declaration path {path} length differs: expected={len(expected)} actual={len(actual)}"
            )
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            _bind_exact(expected_item, actual_item, f"{path}[{index}]")
        return
    if expected != actual:
        raise ScenarioValueError(
            f"declaration path {path} value differs: expected={expected!r} actual={actual!r}"
        )


def bind_scenario(
    manifest_scenario: Mapping[str, Any] | ManifestScenarioSource,
    contract: ScenarioContract,
) -> BindingLedger:
    scenario = (
        manifest_scenario
        if isinstance(manifest_scenario, Mapping)
        else manifest_scenario_from_manifest(manifest_scenario)
    )
    if type(scenario) is not dict:
        raise ScenarioShapeError("manifest scenario must be an object")
    _require_exact_keys(scenario, set(SCENARIO_TOP_LEVEL_KEYS), "$")
    expected = contract.as_mapping()
    _bind_exact(expected, scenario)
    declared = tuple(
        DeclaredLeaf(
            path=path,
            value=deepcopy(value),
            expected_consumer=contract.consumer_by_field[path.split(".", 2)[1].split("[", 1)[0]],
        )
        for path, value in _leaf_items(expected)
    )
    paths = tuple(path for path, _value in _leaf_items(scenario))
    return BindingLedger(contract=contract, declared_leaves=declared, bound_paths=paths)


def manifest_scenario_from_manifest(source: ManifestScenarioSource) -> Mapping[str, Any]:
    return manifest_scenario(source)


def consume_execution(
    binding: BindingLedger, execution: ExecutionEvidence
) -> ConsumptionLedger:
    declarations = {item.path: item for item in binding.declared_leaves}
    consumed: dict[str, ConsumedLeaf] = {}
    for record in execution.records():
        if not record.declaration_paths:
            raise ScenarioBindingError(
                f"consumer {record.consumer} names no declaration paths"
            )
        for path in record.declaration_paths:
            declaration = declarations.get(path)
            if declaration is None:
                raise ScenarioBindingError(
                    f"consumer {record.consumer} names undeclared path {path}"
                )
            if path in consumed:
                raise ScenarioBindingError(
                    f"declaration path {path} was consumed more than once: "
                    f"first={consumed[path].consumer} second={record.consumer}"
                )
            if record.consumer != declaration.expected_consumer:
                raise ScenarioBindingError(
                    f"declaration path {path} expected consumer "
                    f"{declaration.expected_consumer}, received {record.consumer}"
                )
            consumed[path] = ConsumedLeaf(
                path=path,
                consumer=record.consumer,
                evidence=deepcopy(dict(record.evidence)),
            )
    return ConsumptionLedger(
        binding=binding,
        consumed_leaves=tuple(consumed[path] for path in sorted(consumed)),
    )


def require_complete(consumption: ConsumptionLedger) -> None:
    declared = {item.path: item for item in consumption.binding.declared_leaves}
    bound = set(consumption.binding.bound_paths)
    consumed = {item.path for item in consumption.consumed_leaves}
    declared_paths = set(declared)
    if declared_paths != bound:
        missing = sorted(declared_paths - bound)
        extra = sorted(bound - declared_paths)
        raise ScenarioBindingError(
            f"binding conservation failed: missing_bound={missing} extra_bound={extra}"
        )
    missing_consumers = sorted(declared_paths - consumed)
    if missing_consumers:
        path = missing_consumers[0]
        raise ScenarioBindingError(
            f"declaration path {path} reached no consumer; expected "
            f"{declared[path].expected_consumer}"
        )
    extra_consumers = sorted(consumed - declared_paths)
    if extra_consumers:
        raise ScenarioBindingError(
            f"consumption conservation failed: undeclared_consumed={extra_consumers}"
        )
    if len(declared_paths) != len(consumption.consumed_leaves):
        raise ScenarioBindingError(
            "consumption conservation failed: duplicate terminal dispositions"
        )


@lru_cache(maxsize=1)
def verifier_scenario_contracts() -> Mapping[str, ScenarioContract]:
    from stage1_freeze import build_legacy_manifest

    manifest = build_legacy_manifest()
    contracts: dict[str, ScenarioContract] = {}
    for row in manifest["rows"]:
        if row["disposition"] != "APPLICABLE":
            continue
        scenarios = row["scenarios"]
        if len(scenarios) != 1:
            raise ScenarioShapeError(
                f"verifier literals for {row['row_id']} must contain exactly one scenario"
            )
        contracts[row["row_id"]] = ScenarioContract.from_mapping(next(iter(scenarios)))
    return contracts


def verifier_scenario_contract(row_id: str) -> ScenarioContract:
    contract = verifier_scenario_contracts().get(row_id)
    if contract is None:
        raise ManifestRowError(f"verifier scenario contract is absent: {row_id}")
    return ScenarioContract.from_mapping(contract.as_mapping())
