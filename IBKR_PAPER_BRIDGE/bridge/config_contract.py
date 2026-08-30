"""Fail-closed configuration contract for the production Bridge startup path.

The configured and implemented setting universes have independent producers:
YAML leaves come from :class:`YamlLeafWalker`; implemented paths come only
from immutable bound objects inspected by :class:`BoundFieldWalker`.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field, fields, is_dataclass
from difflib import get_close_matches
from enum import Enum
import hashlib
import math
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Callable, ClassVar, Generic, Mapping, TypeVar

import yaml

from bridge.store.db import Store


T = TypeVar("T")
_MISSING = object()
APPROVED_CONFIG_BYTES = 324
APPROVED_CONFIG_SHA256 = "a96fecd10d6966c3e93a829ec4d75869a0851f0136a06e85ab45c255ee0f5842"
REQUIRED_V2_EXPLICIT_LEAF_PATHS = frozenset(
    {
        "broker.data_restore_timeout_s",
        "broker.reconnect_attempts",
        "broker.reconnect_base_delay_s",
        "risk.max_consecutive_losses",
        "risk.max_daily_loss_pct",
        "risk.max_leverage",
        "risk.max_position_notional_pct",
        "risk.min_order_usd",
        "risk.min_stop_distance_pct",
        "risk.reconcile_max_consecutive_failures",
        "risk.risk_pct_per_trade",
    }
)
_DRY_RUN_INTERNAL_OVERRIDE_PATHS = frozenset({"risk.max_position_notional_pct"})
_VALID_KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


class RefusalKind(str, Enum):
    FAIL = "STARTUP_FAIL"
    STOP = "STARTUP_STOP"


class ApplyMode(str, Enum):
    RESTART_ONLY = "restart_only"


class Provenance(str, Enum):
    EXPLICIT = "explicit"
    INTERNAL_DEFAULT = "internal_default"
    INTERNAL_MODE_OVERRIDE = "internal_mode_override"


@dataclass(frozen=True)
class Capability:
    identity: str
    gate_method: str | None = None
    min_schema: int | None = None

    def is_active(self, snapshot: "CapabilitySnapshot") -> bool:
        if self.identity == "always":
            return True
        if self.identity == "durable_risk":
            return snapshot.durable_risk
        if self.identity == "exposure_controls":
            return snapshot.exposure_controls
        raise ValueError(f"unknown capability identity {self.identity!r}")

    @property
    def requirement(self) -> str:
        return "always" if self.min_schema is None else f"schema>={self.min_schema}"


ALWAYS = Capability("always")
DURABLE_RISK = Capability(
    "durable_risk", "durable_risk_controls_enabled", min_schema=7
)
EXPOSURE_CONTROLS = Capability(
    "exposure_controls", "exposure_controls_enabled", min_schema=8
)


@dataclass(frozen=True)
class CapabilitySnapshot:
    schema_version: int
    durable_risk: bool
    exposure_controls: bool


@dataclass(frozen=True)
class ConfigIssue:
    kind: RefusalKind
    classification: str | None = None
    setting: str | None = None
    subject: str | None = None
    reason: str | None = None
    suggestion: str | None = None
    action: str | None = None
    actual_schema: int | None = None
    requires: str | None = None
    actual_mode: str | None = None

    def render(self) -> str:
        parts = [self.kind.value]
        if self.classification is not None:
            parts.append(f"class={self.classification}")
        if self.subject is not None:
            parts.append(f"subject={self.subject}")
        if self.setting is not None:
            parts.append(f"setting={self.setting}")
        if self.reason is not None:
            parts.append(f"reason={self.reason}")
        if self.suggestion is not None:
            parts.append(f"suggestion={self.suggestion}")
        if self.actual_schema is not None:
            parts.append(f"actual_schema={self.actual_schema}")
        if self.requires is not None:
            parts.append(f"requires={self.requires}")
        if self.actual_mode is not None:
            parts.append(f"actual_mode={self.actual_mode}")
        if self.action is not None:
            parts.append(f"action={self.action}")
        return " ".join(parts)


class StartupConfigRefusal(RuntimeError):
    """Typed startup refusal containing deterministic, value-free diagnostics."""

    def __init__(self, issues: list[ConfigIssue] | tuple[ConfigIssue, ...]):
        ordered = tuple(
            sorted(
                issues,
                key=lambda issue: (
                    issue.setting or "",
                    issue.subject or "",
                    issue.classification or "",
                    issue.reason or "",
                ),
            )
        )
        self.issues = ordered
        kind = (
            RefusalKind.STOP
            if any(issue.kind is RefusalKind.STOP for issue in ordered)
            else RefusalKind.FAIL
        )
        summary = f"{kind.value} summary refused={len(ordered)}"
        super().__init__("\n".join([*(issue.render() for issue in ordered), summary]))


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or _VALID_KEY.fullmatch(key) is None:
            raise ValueError("unsupported_key")
        if key in mapping:
            raise ValueError(f"duplicate_key:{key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


class YamlLeafWalker:
    """Parse captured YAML bytes and emit every scalar or scalar-list leaf."""

    @classmethod
    def parse(cls, raw: bytes) -> dict[str, Any]:
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise StartupConfigRefusal(
                [
                    ConfigIssue(
                        RefusalKind.FAIL,
                        classification="INVALID_DOCUMENT",
                        subject="config",
                        reason="not_utf8",
                        action="correct_candidate_and_retry",
                    )
                ]
            ) from exc
        try:
            document = yaml.load(text, Loader=_UniqueKeyLoader)
        except (yaml.YAMLError, ValueError) as exc:
            reason = str(exc) if isinstance(exc, ValueError) else "yaml_syntax"
            raise StartupConfigRefusal(
                [
                    ConfigIssue(
                        RefusalKind.FAIL,
                        classification="INVALID_DOCUMENT",
                        subject="config",
                        reason=reason,
                        action="correct_candidate_and_retry",
                    )
                ]
            ) from exc
        if not isinstance(document, dict):
            raise StartupConfigRefusal(
                [
                    ConfigIssue(
                        RefusalKind.FAIL,
                        classification="INVALID_DOCUMENT",
                        subject="config",
                        reason="root_not_mapping",
                        action="correct_candidate_and_retry",
                    )
                ]
            )
        leaves: dict[str, Any] = {}
        cls._walk(document, (), leaves)
        return leaves

    @classmethod
    def _walk(
        cls, value: Any, path: tuple[str, ...], leaves: dict[str, Any]
    ) -> None:
        if isinstance(value, dict):
            if not value:
                cls._invalid(path, "empty_mapping")
            for key, child in value.items():
                if not isinstance(key, str) or _VALID_KEY.fullmatch(key) is None:
                    cls._invalid((*path, str(key)), "unsupported_key")
                cls._walk(child, (*path, key), leaves)
            return
        normalized = ".".join(path)
        if not normalized:
            cls._invalid(path, "missing_leaf_path")
        if isinstance(value, list):
            if any(isinstance(item, (dict, list, set, tuple)) for item in value):
                cls._invalid(path, "unsupported_list_container")
        elif not (value is None or isinstance(value, (str, bool, int, float))):
            cls._invalid(path, "unsupported_scalar")
        if normalized in leaves:
            cls._invalid(path, "duplicate_path")
        leaves[normalized] = value

    @staticmethod
    def _invalid(path: tuple[str, ...], reason: str) -> None:
        raise StartupConfigRefusal(
            [
                ConfigIssue(
                    RefusalKind.FAIL,
                    classification="INVALID_DOCUMENT",
                    setting=".".join(path) or None,
                    reason=reason,
                    action="correct_candidate_and_retry",
                )
            ]
        )


@dataclass(frozen=True)
class TakenValue(Generic[T]):
    path: str
    value: T = field(repr=False)
    conversion: str
    provenance: Provenance
    apply_mode: ApplyMode
    capability: Capability
    capability_active: bool
    mode_active: bool
    active: bool
    valid: bool


Validator = Callable[[Any], bool]


class SettingsReader:
    """Perform typed reads without registering any implemented-setting path."""

    def __init__(
        self,
        leaves: Mapping[str, Any],
        capabilities: CapabilitySnapshot,
        *,
        mode: str,
    ) -> None:
        self._leaves = leaves
        self._capabilities = capabilities
        self._mode = mode
        self.issues: list[ConfigIssue] = []

    def take(
        self,
        path: str,
        converter: type[T],
        *,
        default: T,
        capability: Capability = ALWAYS,
        validator: Validator | None = None,
        active_modes: frozenset[str] | None = None,
        mode_override: T | object = _MISSING,
    ) -> TakenValue[T]:
        explicit = path in self._leaves
        raw = self._leaves[path] if explicit else default
        valid = True
        try:
            value = self._convert(raw, converter)
            if validator is not None and not validator(value):
                raise ValueError("range")
        except (TypeError, ValueError):
            value = default
            valid = False
            if explicit:
                self.issues.append(
                    ConfigIssue(
                        RefusalKind.FAIL,
                        classification="INVALID_VALUE",
                        setting=path,
                        reason="type_or_range",
                        action="correct_candidate_and_retry",
                    )
                )

        capability_active = capability.is_active(self._capabilities)
        mode_active = active_modes is None or self._mode in active_modes
        provenance = Provenance.EXPLICIT if explicit else Provenance.INTERNAL_DEFAULT
        if not mode_active and mode_override is not _MISSING:
            value = mode_override  # type: ignore[assignment]
            provenance = Provenance.INTERNAL_MODE_OVERRIDE

        if explicit and valid and not capability_active:
            self.issues.append(
                ConfigIssue(
                    RefusalKind.FAIL,
                    classification="KNOWN_INERT_SCHEMA",
                    setting=path,
                    actual_schema=self._capabilities.schema_version,
                    requires=capability.requirement,
                    action="remove_or_obtain_separate_schema_and_config_approval",
                )
            )
        if explicit and valid and not mode_active:
            self.issues.append(
                ConfigIssue(
                    RefusalKind.FAIL,
                    classification="KNOWN_INERT_MODE",
                    setting=path,
                    actual_mode=self._mode,
                    action="remove_or_use_an_approved_consuming_mode",
                )
            )
        return TakenValue(
            path=path,
            value=value,
            conversion=converter.__name__,
            provenance=provenance,
            apply_mode=ApplyMode.RESTART_ONLY,
            capability=capability,
            capability_active=capability_active,
            mode_active=mode_active,
            active=capability_active
            and (mode_active or (not explicit and mode_override is not _MISSING)),
            valid=valid,
        )

    @staticmethod
    def _convert(raw: Any, converter: type[T]) -> T:
        if converter is float:
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                raise TypeError
            value = float(raw)
            if not math.isfinite(value):
                raise ValueError
            return value  # type: ignore[return-value]
        if converter is int:
            if isinstance(raw, bool) or not isinstance(raw, int):
                raise TypeError
            return raw  # type: ignore[return-value]
        if converter is bool:
            if not isinstance(raw, bool):
                raise TypeError
            return raw  # type: ignore[return-value]
        if converter is str:
            if not isinstance(raw, str):
                raise TypeError
            return raw  # type: ignore[return-value]
        raise TypeError(f"unsupported converter {converter!r}")


def _suggest_path(path: str, candidates: tuple[str, ...]) -> str | None:
    namespace = path.split(".", 1)[0]
    same_namespace = tuple(
        candidate
        for candidate in candidates
        if candidate.split(".", 1)[0] == namespace
    )
    matches = get_close_matches(path, same_namespace, n=1, cutoff=0.6)
    return matches[0] if matches else None


@dataclass(frozen=True)
class BoundRiskInputs:
    SETTING_NAMESPACE: ClassVar[str] = "risk"

    policy_id: TakenValue[str]
    risk_pct_per_trade: TakenValue[float]
    max_daily_loss_pct: TakenValue[float]
    max_intraday_drawdown_pct: TakenValue[float]
    equity_floor_usdc: TakenValue[float]
    max_position_notional_pct: TakenValue[float]
    min_stop_distance_pct: TakenValue[float]
    min_order_usd: TakenValue[float]
    max_leverage: TakenValue[int]
    max_consecutive_losses: TakenValue[int]
    coin_enabled: TakenValue[bool]
    feed_stale: TakenValue[bool]
    app_armed: TakenValue[bool]
    direction: TakenValue[str]
    size_decimals: TakenValue[int]
    exposure_policy_id: TakenValue[str]
    max_symbol_gross_pct: TakenValue[float]
    max_portfolio_gross_pct: TakenValue[float]
    max_wallet_margin_util_pct: TakenValue[float]
    max_effective_leverage: TakenValue[float]
    min_liquidation_distance_pct: TakenValue[float]

    def unwrap_all(self, target: type[T]) -> T:
        return _unwrap_all(self, target)


@dataclass(frozen=True)
class BoundBrokerInputs:
    SETTING_NAMESPACE: ClassVar[str] = "broker"

    reconnect_attempts: TakenValue[int]
    reconnect_base_delay_s: TakenValue[float]
    data_restore_timeout_s: TakenValue[float]

    def unwrap_all(self, target: type[T]) -> T:
        return _unwrap_all(self, target)


@dataclass(frozen=True)
class BoundRiskEngineStartInputs:
    SETTING_NAMESPACE: ClassVar[str] = "risk"

    reconcile_max_consecutive_failures: TakenValue[int]

    def unwrap_all(self, target: type[T]) -> T:
        return _unwrap_all(self, target)


@dataclass(frozen=True)
class BoundEngineStartInputs:
    broker: BoundBrokerInputs
    risk: BoundRiskEngineStartInputs


@dataclass(frozen=True)
class BrokerEngineStartOptions:
    reconnect_attempts: int
    reconnect_base_delay_s: float
    data_restore_timeout_s: float


@dataclass(frozen=True)
class RiskEngineStartOptions:
    reconcile_max_consecutive_failures: int


@dataclass(frozen=True)
class BoundSetting:
    producer: str
    path: str
    value: Any = field(repr=False)
    conversion: str
    provenance: Provenance
    apply_mode: ApplyMode
    capability: Capability


class BoundFieldWalker:
    """Emit paths only from fields physically present on final frozen objects."""

    @classmethod
    def walk(cls, *roots: object) -> tuple[dict[str, BoundSetting], list[ConfigIssue]]:
        emitted: dict[str, BoundSetting] = {}
        issues: list[ConfigIssue] = []
        for root in roots:
            cls._walk_object(root, emitted, issues)
        return emitted, issues

    @classmethod
    def _walk_object(
        cls,
        obj: object,
        emitted: dict[str, BoundSetting],
        issues: list[ConfigIssue],
    ) -> None:
        if not is_dataclass(obj):
            raise TypeError("bound root must be a dataclass instance")
        namespace = getattr(type(obj), "SETTING_NAMESPACE", None)
        if namespace is None:
            for member in fields(obj):
                cls._walk_object(getattr(obj, member.name), emitted, issues)
            return
        for member in fields(obj):
            taken = getattr(obj, member.name)
            if not isinstance(taken, TakenValue):
                issues.append(
                    ConfigIssue(
                        RefusalKind.STOP,
                        subject="config_binding",
                        setting=f"{namespace}.{member.name}",
                        reason="bound_field_not_taken_value",
                        action="repair_source_binding_and_retry",
                    )
                )
                continue
            expected_path = f"{namespace}.{member.name}"
            if taken.path != expected_path:
                issues.append(
                    ConfigIssue(
                        RefusalKind.STOP,
                        subject="config_binding",
                        setting=expected_path,
                        reason="field_path_mismatch",
                        action="repair_source_binding_and_retry",
                    )
                )
                continue
            if not taken.active or not taken.valid:
                continue
            if expected_path in emitted:
                issues.append(
                    ConfigIssue(
                        RefusalKind.STOP,
                        subject="config_binding",
                        setting=expected_path,
                        reason="duplicate_bound_path",
                        action="repair_source_binding_and_retry",
                    )
                )
                continue
            emitted[expected_path] = BoundSetting(
                producer="BoundFieldWalker",
                path=expected_path,
                value=taken.value,
                conversion=taken.conversion,
                provenance=taken.provenance,
                apply_mode=taken.apply_mode,
                capability=taken.capability,
            )


@dataclass(frozen=True)
class ConfiguredLeaf:
    producer: str
    path: str
    value: Any = field(repr=False)


@dataclass(frozen=True)
class ValidatedRuntimeSettings:
    config_path: Path
    config_sha256: str
    schema_version: int
    mode: str
    risk: BoundRiskInputs
    engine_start: BoundEngineStartInputs
    configured_rows: tuple[ConfiguredLeaf, ...]
    declared_leaf_paths: tuple[str, ...]
    bound_setting_paths: tuple[str, ...]
    settings: Mapping[str, BoundSetting]
    modeled_settings: Mapping[str, TakenValue[Any]]

    def effective_view(self) -> dict[str, Any]:
        view: dict[str, Any] = {}
        for path in sorted(self.settings):
            setting = self.settings[path]
            namespace, leaf = path.split(".", 1)
            view.setdefault(namespace, {})[leaf] = {
                "value": setting.value,
                "provenance": setting.provenance.value,
                "apply_mode": setting.apply_mode.value,
                "capability": setting.capability.identity,
            }
        view["_meta"] = {
            "schema_version": self.schema_version,
            "mode": self.mode,
            "config_sha256": self.config_sha256,
        }
        return view


@dataclass(frozen=True)
class UpdateRefusal:
    classification: str
    setting: str
    reason: str | None = None
    suggestion: str | None = None
    actual_schema: int | None = None
    requires: str | None = None
    actual_mode: str | None = None

    def as_detail(self) -> dict[str, Any]:
        detail: dict[str, Any] = {
            "class": self.classification,
            "setting": self.setting,
        }
        for name in (
            "reason",
            "suggestion",
            "actual_schema",
            "requires",
            "actual_mode",
        ):
            value = getattr(self, name)
            if value is not None:
                detail[name] = value
        return detail


@dataclass(frozen=True)
class UpdateDecision:
    accepted: bool
    refusals: tuple[UpdateRefusal, ...]


def classify_runtime_update(
    validated: ValidatedRuntimeSettings, payload: Mapping[str, Any]
) -> UpdateDecision:
    """Classify a proposed update without applying or recording any value."""

    if not isinstance(payload, Mapping):
        return UpdateDecision(
            False,
            (UpdateRefusal("INVALID_DOCUMENT", "<root>", reason="root_not_mapping"),),
        )
    leaves: dict[str, Any] = {}
    try:
        YamlLeafWalker._walk(dict(payload), (), leaves)
    except StartupConfigRefusal:
        return UpdateDecision(
            False,
            (UpdateRefusal("INVALID_DOCUMENT", "<root>", reason="invalid_payload_shape"),),
        )
    refusals: list[UpdateRefusal] = []
    modeled_paths = tuple(validated.modeled_settings)
    for path in sorted(leaves):
        taken = validated.modeled_settings.get(path)
        if taken is None:
            suggestion = _suggest_path(path, modeled_paths)
            refusals.append(
                UpdateRefusal(
                    "UNKNOWN_KEY",
                    path,
                    reason="no_bound_runtime_field",
                    suggestion=suggestion,
                )
            )
        elif not taken.capability_active:
            refusals.append(
                UpdateRefusal(
                    "KNOWN_INERT_SCHEMA",
                    path,
                    actual_schema=validated.schema_version,
                    requires=taken.capability.requirement,
                )
            )
        elif not taken.mode_active:
            refusals.append(
                UpdateRefusal(
                    "KNOWN_INERT_MODE", path, actual_mode=validated.mode
                )
            )
        else:
            refusals.append(
                UpdateRefusal("RESTART_ONLY", path, reason="managed_candidate_restart_required")
            )
    return UpdateDecision(False, tuple(refusals))


def construct_bridge_engine(
    validated: ValidatedRuntimeSettings,
    *,
    run_id: str,
    broker: Any,
    store: Store,
    strategy: Any,
    notifier: Any,
    state: str,
    mode: str,
    on_update: Callable[[str, object], object] | None,
) -> Any:
    """Own every settings-bearing constructor argument for the running engine."""

    from bridge.engine.engine import BridgeEngine
    from bridge.engine.risk import RiskConfig, RiskEngine

    risk_config = validated.risk.unwrap_all(RiskConfig)
    broker_options = validated.engine_start.broker.unwrap_all(BrokerEngineStartOptions)
    risk_start_options = validated.engine_start.risk.unwrap_all(RiskEngineStartOptions)
    return BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=strategy,
        risk_engine=RiskEngine(risk_config),
        notifier=notifier,
        state=state,
        mode=mode,
        on_update=on_update,
        reconcile_max_consecutive_failures=(
            risk_start_options.reconcile_max_consecutive_failures
        ),
        bar_reconnect_attempts=broker_options.reconnect_attempts,
        bar_reconnect_base_delay_s=broker_options.reconnect_base_delay_s,
        bar_data_restore_timeout_s=broker_options.data_restore_timeout_s,
    )


def _capture_capabilities(store: Store) -> CapabilitySnapshot:
    try:
        raw_schema = store.get_meta("schema_version")
    except Exception as exc:
        raise StartupConfigRefusal(
            [
                ConfigIssue(
                    RefusalKind.STOP,
                    subject="schema_capabilities",
                    reason="not_evaluated",
                    action="repair_store_evaluation_and_retry",
                )
            ]
        ) from exc
    if (
        not isinstance(raw_schema, str)
        or not raw_schema.isascii()
        or not raw_schema.isdigit()
    ):
        raise StartupConfigRefusal(
            [
                ConfigIssue(
                    RefusalKind.STOP,
                    subject="schema_capabilities",
                    reason="schema_not_numeric",
                    action="repair_store_evaluation_and_retry",
                )
            ]
        )
    try:
        schema_version = int(raw_schema)
        durable = bool(store.durable_risk_controls_enabled())
        exposure = bool(store.exposure_controls_enabled())
    except Exception as exc:
        raise StartupConfigRefusal(
            [
                ConfigIssue(
                    RefusalKind.STOP,
                    subject="schema_capabilities",
                    reason="not_evaluated",
                    action="repair_store_evaluation_and_retry",
                )
            ]
        ) from exc
    return CapabilitySnapshot(schema_version, durable, exposure)


def _read_config_bytes(config_path: Path) -> bytes:
    try:
        return config_path.read_bytes()
    except OSError as exc:
        raise StartupConfigRefusal(
            [
                ConfigIssue(
                    RefusalKind.STOP,
                    subject="config",
                    reason="file_unreadable",
                    action="repair_config_read_and_retry",
                )
            ]
        ) from exc


def _collect_taken_values(*roots: object) -> dict[str, TakenValue[Any]]:
    collected: dict[str, TakenValue[Any]] = {}

    def visit(obj: object) -> None:
        namespace = getattr(type(obj), "SETTING_NAMESPACE", None)
        for member in fields(obj):
            value = getattr(obj, member.name)
            if namespace is None:
                visit(value)
                continue
            if not isinstance(value, TakenValue):
                raise TypeError("validated bound field is not a TakenValue")
            expected_path = f"{namespace}.{member.name}"
            if value.path != expected_path or expected_path in collected:
                raise TypeError("validated bound field identity is inconsistent")
            collected[expected_path] = value

    for root in roots:
        visit(root)
    return collected


def _unwrap_all(bound: object, target: type[T]) -> T:
    import inspect

    signature = inspect.signature(target)
    target_fields = {
        name
        for name, parameter in signature.parameters.items()
        if parameter.kind
        in (parameter.POSITIONAL_OR_KEYWORD, parameter.KEYWORD_ONLY)
    }
    bound_fields = {member.name for member in fields(bound)}
    if bound_fields != target_fields:
        raise StartupConfigRefusal(
            [
                ConfigIssue(
                    RefusalKind.STOP,
                    subject="config_binding",
                    reason="constructor_field_mismatch",
                    action="repair_source_binding_and_retry",
                )
            ]
        )
    values: dict[str, Any] = {}
    for member in fields(bound):
        taken = getattr(bound, member.name)
        if not isinstance(taken, TakenValue):
            raise StartupConfigRefusal(
                [
                    ConfigIssue(
                        RefusalKind.STOP,
                        subject="config_binding",
                        setting=member.name,
                        reason="constructor_value_not_taken",
                        action="repair_source_binding_and_retry",
                    )
                ]
            )
        if taken.active and taken.valid:
            values[member.name] = taken.value
    try:
        return target(**values)
    except (TypeError, ValueError) as exc:
        raise StartupConfigRefusal(
            [
                ConfigIssue(
                    RefusalKind.STOP,
                    subject="config_binding",
                    reason="constructor_rejected_bound_fields",
                    action="repair_source_binding_and_retry",
                )
            ]
        ) from exc


def prepare_runtime_settings(
    config_path: str | Path,
    store: Store,
    *,
    dry_run: bool,
) -> ValidatedRuntimeSettings:
    """Read once, bind immutable settings, and refuse every unconsumed leaf."""

    path = Path(config_path)
    capabilities = _capture_capabilities(store)
    raw = _read_config_bytes(path)
    leaves = YamlLeafWalker.parse(raw)
    mode = "dry_run" if dry_run else "paper"
    reader = SettingsReader(leaves, capabilities, mode=mode)
    positive_fraction = lambda value: 0 < value <= 1
    positive = lambda value: value > 0
    at_least_one = lambda value: value >= 1
    non_blank = lambda value: bool(value.strip())

    risk = BoundRiskInputs(
        policy_id=reader.take(
            "risk.policy_id",
            str,
            default="ts-p1-007-v1",
            capability=DURABLE_RISK,
            validator=non_blank,
        ),
        risk_pct_per_trade=reader.take(
            "risk.risk_pct_per_trade", float, default=0.005, validator=positive_fraction
        ),
        max_daily_loss_pct=reader.take(
            "risk.max_daily_loss_pct", float, default=0.02, validator=positive_fraction
        ),
        max_intraday_drawdown_pct=reader.take(
            "risk.max_intraday_drawdown_pct",
            float,
            default=0.05,
            capability=DURABLE_RISK,
            validator=positive_fraction,
        ),
        equity_floor_usdc=reader.take(
            "risk.equity_floor_usdc",
            float,
            default=500.0,
            capability=DURABLE_RISK,
            validator=positive,
        ),
        max_position_notional_pct=reader.take(
            "risk.max_position_notional_pct",
            float,
            default=0.20,
            validator=positive_fraction,
            active_modes=frozenset({"paper"}),
            mode_override=0.5,
        ),
        min_stop_distance_pct=reader.take(
            "risk.min_stop_distance_pct", float, default=0.001, validator=positive_fraction
        ),
        min_order_usd=reader.take(
            "risk.min_order_usd", float, default=10.0, validator=positive
        ),
        max_leverage=reader.take(
            "risk.max_leverage", int, default=1, validator=at_least_one
        ),
        max_consecutive_losses=reader.take(
            "risk.max_consecutive_losses", int, default=3, validator=at_least_one
        ),
        coin_enabled=reader.take("risk.coin_enabled", bool, default=True),
        feed_stale=reader.take("risk.feed_stale", bool, default=False),
        app_armed=reader.take("risk.app_armed", bool, default=True),
        direction=reader.take(
            "risk.direction",
            str,
            default="BOTH",
            validator=lambda value: value
            in {"BOTH", "LONG_ONLY", "SHORT_ONLY", "NO_TRADE"},
        ),
        size_decimals=reader.take(
            "risk.size_decimals", int, default=6, validator=lambda value: value >= 0
        ),
        exposure_policy_id=reader.take(
            "risk.exposure_policy_id",
            str,
            default="ts-p1-008-v1",
            capability=EXPOSURE_CONTROLS,
            validator=non_blank,
        ),
        max_symbol_gross_pct=reader.take(
            "risk.max_symbol_gross_pct",
            float,
            default=0.20,
            capability=EXPOSURE_CONTROLS,
            validator=positive_fraction,
        ),
        max_portfolio_gross_pct=reader.take(
            "risk.max_portfolio_gross_pct",
            float,
            default=0.40,
            capability=EXPOSURE_CONTROLS,
            validator=positive_fraction,
        ),
        max_wallet_margin_util_pct=reader.take(
            "risk.max_wallet_margin_util_pct",
            float,
            default=0.25,
            capability=EXPOSURE_CONTROLS,
            validator=positive_fraction,
        ),
        max_effective_leverage=reader.take(
            "risk.max_effective_leverage",
            float,
            default=1.0,
            capability=EXPOSURE_CONTROLS,
            validator=positive,
        ),
        min_liquidation_distance_pct=reader.take(
            "risk.min_liquidation_distance_pct",
            float,
            default=0.15,
            capability=EXPOSURE_CONTROLS,
            validator=positive_fraction,
        ),
    )
    engine_start = BoundEngineStartInputs(
        broker=BoundBrokerInputs(
            reconnect_attempts=reader.take(
                "broker.reconnect_attempts", int, default=9, validator=at_least_one
            ),
            reconnect_base_delay_s=reader.take(
                "broker.reconnect_base_delay_s", float, default=5.0, validator=positive
            ),
            data_restore_timeout_s=reader.take(
                "broker.data_restore_timeout_s",
                float,
                default=300.0,
                validator=lambda value: value >= 30,
            ),
        ),
        risk=BoundRiskEngineStartInputs(
            reconcile_max_consecutive_failures=reader.take(
                "risk.reconcile_max_consecutive_failures",
                int,
                default=3,
                validator=at_least_one,
            )
        ),
    )
    bound, binding_issues = BoundFieldWalker.walk(risk, engine_start)
    if binding_issues:
        raise StartupConfigRefusal(binding_issues)

    issues = list(reader.issues)
    required_explicit_paths = REQUIRED_V2_EXPLICIT_LEAF_PATHS
    if dry_run:
        required_explicit_paths -= _DRY_RUN_INTERNAL_OVERRIDE_PATHS
    for missing_path in sorted(required_explicit_paths - set(leaves)):
        issues.append(
            ConfigIssue(
                RefusalKind.FAIL,
                classification="MISSING_REQUIRED",
                setting=missing_path,
                reason="required_explicit_leaf_absent",
                action="restore_required_candidate_leaf",
            )
        )
    refused_paths = {issue.setting for issue in issues if issue.setting is not None}
    for declared_path in sorted(set(leaves) - set(bound) - refused_paths):
        suggestion = _suggest_path(declared_path, tuple(bound))
        issues.append(
            ConfigIssue(
                RefusalKind.FAIL,
                classification="UNKNOWN_KEY",
                setting=declared_path,
                reason="no_bound_runtime_field",
                suggestion=suggestion,
                action="remove_or_implement_under_separate_approval",
            )
        )
    if issues:
        raise StartupConfigRefusal(issues)

    explicit_bound = {
        path_name: setting
        for path_name, setting in bound.items()
        if setting.provenance is Provenance.EXPLICIT or path_name not in leaves
    }
    modeled_settings = _collect_taken_values(risk, engine_start)
    return ValidatedRuntimeSettings(
        config_path=path,
        config_sha256=hashlib.sha256(raw).hexdigest(),
        schema_version=capabilities.schema_version,
        mode=mode,
        risk=risk,
        engine_start=engine_start,
        configured_rows=tuple(
            ConfiguredLeaf("YamlLeafWalker", leaf_path, leaves[leaf_path])
            for leaf_path in sorted(leaves)
        ),
        declared_leaf_paths=tuple(sorted(leaves)),
        bound_setting_paths=tuple(sorted(explicit_bound)),
        settings=MappingProxyType(dict(explicit_bound)),
        modeled_settings=MappingProxyType(dict(modeled_settings)),
    )


@dataclass(frozen=True)
class SourceCensusRow:
    producer: str
    bound_class: str
    target_field: str
    setting_path: str
    expected_path: str
    read_site_capability: str
    consumer_capability: str
    source_path: str
    source_line: int
    field_source_path: str
    field_source_line: int
    take_source_path: str
    take_source_line: int


@dataclass(frozen=True)
class SourceCensusFinding:
    disposition: str
    code: str
    source_path: str
    source_line: int


@dataclass(frozen=True)
class SourceCensusResult:
    status: str
    rows: tuple[SourceCensusRow, ...]
    findings: tuple[SourceCensusFinding, ...]
    source_sha256: str
    source_identities: Mapping[str, str]
    candidate_sha256: str
    candidate_bytes: int
    package_sha256: str


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _attribute_chain(node: ast.AST) -> tuple[str, ...] | None:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return tuple(reversed(parts))
    return None


class ConfigContractAstCensus:
    """Independent source-byte package gate for setting-to-consumer binding."""

    REQUIRED_SOURCES = (
        "bridge/config_contract.py",
        "bridge/app.py",
        "bridge/engine/risk.py",
        "bridge/engine/engine.py",
        "bridge/engine/reconcile.py",
        "bridge/store/db.py",
    )

    @classmethod
    def run(
        cls,
        package_root: str | Path,
        *,
        source_overrides: Mapping[str, str] | None = None,
        candidate_bytes: bytes | None = None,
    ) -> SourceCensusResult:
        root = Path(package_root)
        overrides = {
            key.replace("\\", "/"): value
            for key, value in (source_overrides or {}).items()
        }
        findings: list[SourceCensusFinding] = []
        sources: dict[str, str] = {}
        source_paths = {
            path.relative_to(root).as_posix()
            for path in (root / "bridge").rglob("*.py")
        } | set(overrides)
        for relative in sorted(source_paths):
            if relative in overrides:
                sources[relative] = overrides[relative]
                continue
            try:
                sources[relative] = (root / relative).read_bytes().decode(
                    "utf-8", errors="strict"
                )
            except (OSError, UnicodeDecodeError):
                findings.append(
                    SourceCensusFinding("STOP", "SOURCE_READ_FAILED", relative, 1)
                )
        for relative in cls.REQUIRED_SOURCES:
            if relative not in sources:
                findings.append(
                    SourceCensusFinding("STOP", "REQUIRED_SOURCE_MISSING", relative, 1)
                )

        trees: dict[str, ast.Module] = {}
        for relative, source in sources.items():
            try:
                trees[relative] = ast.parse(source, filename=relative)
            except SyntaxError as exc:
                findings.append(
                    SourceCensusFinding(
                        "STOP", "SOURCE_UNPARSABLE", relative, exc.lineno or 1
                    )
                )

        identities = {
            relative: hashlib.sha256(source.encode("utf-8")).hexdigest()
            for relative, source in sorted(sources.items())
        }
        identity_preimage = "".join(
            f"{relative}\0{digest}\n" for relative, digest in identities.items()
        ).encode("utf-8")
        aggregate_identity = hashlib.sha256(identity_preimage).hexdigest()
        if candidate_bytes is None:
            try:
                candidate_bytes = (root / "config" / "bridge.yaml").read_bytes()
            except OSError:
                candidate_bytes = b""
                findings.append(
                    SourceCensusFinding(
                        "STOP", "CANDIDATE_READ_FAILED", "config/bridge.yaml", 1
                    )
                )
        candidate_identity = hashlib.sha256(candidate_bytes).hexdigest()
        if (
            len(candidate_bytes) != APPROVED_CONFIG_BYTES
            or candidate_identity != APPROVED_CONFIG_SHA256
        ):
            findings.append(
                SourceCensusFinding(
                    "DETECTED", "CANDIDATE_HASH_MISMATCH", "config/bridge.yaml", 1
                )
            )
        package_identity = hashlib.sha256(
            f"{aggregate_identity}\0{candidate_identity}\0{len(candidate_bytes)}".encode(
                "ascii"
            )
        ).hexdigest()
        if any(finding.disposition == "STOP" for finding in findings):
            return SourceCensusResult(
                "SOURCE_CENSUS_STOP",
                (),
                tuple(cls._sort_findings(findings)),
                aggregate_identity,
                MappingProxyType(dict(identities)),
                candidate_identity,
                len(candidate_bytes),
                package_identity,
            )

        cls._scan_unmodeled_execution(trees, findings)
        cls._scan_raw_yaml_access(trees, findings)
        cls._scan_app_construction(trees["bridge/app.py"], findings)
        rows = cls._binding_rows(trees, findings)
        if not rows:
            findings.append(
                SourceCensusFinding(
                    "STOP", "EMPTY_BINDING_CENSUS", "bridge/config_contract.py", 1
                )
            )
        if any(finding.disposition == "STOP" for finding in findings):
            status = "SOURCE_CENSUS_STOP"
        elif findings:
            status = "DETECTED"
        else:
            status = "PASS"
        return SourceCensusResult(
            status,
            tuple(
                sorted(
                    rows,
                    key=lambda row: (row.setting_path, row.bound_class, row.target_field),
                )
            ),
            tuple(cls._sort_findings(findings)),
            aggregate_identity,
            MappingProxyType(dict(identities)),
            candidate_identity,
            len(candidate_bytes),
            package_identity,
        )

    @staticmethod
    def _sort_findings(
        findings: list[SourceCensusFinding],
    ) -> list[SourceCensusFinding]:
        return sorted(
            findings,
            key=lambda finding: (
                finding.disposition,
                finding.source_path,
                finding.source_line,
                finding.code,
            ),
        )

    @staticmethod
    def _scan_unmodeled_execution(
        trees: Mapping[str, ast.Module], findings: list[SourceCensusFinding]
    ) -> None:
        for relative, tree in trees.items():
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id
                    in {
                    "eval",
                    "exec",
                    "compile",
                    "__import__",
                    }
                ):
                    findings.append(
                        SourceCensusFinding(
                            "STOP", "UNMODELED_DYNAMIC_EXECUTION", relative, node.lineno
                        )
                    )

    @staticmethod
    def _scan_raw_yaml_access(
        trees: Mapping[str, ast.Module], findings: list[SourceCensusFinding]
    ) -> None:
        for relative, tree in trees.items():
            if relative == "bridge/config_contract.py":
                continue
            for node in ast.walk(tree):
                raw_access = False
                if isinstance(node, ast.Import):
                    raw_access = any(alias.name == "yaml" for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    raw_access = node.module == "yaml"
                    if node.module == "bridge.config_contract":
                        raw_access = raw_access or any(
                            alias.name
                            in {"YamlLeafWalker", "SettingsReader", "_UniqueKeyLoader"}
                            for alias in node.names
                        )
                elif isinstance(node, ast.Call):
                    call_name = _call_name(node.func)
                    raw_access = call_name in {
                        "safe_load",
                        "full_load",
                        "unsafe_load",
                    }
                    if call_name == "getattr" and len(node.args) >= 2:
                        raw_access = (
                            isinstance(node.args[1], ast.Constant)
                            and node.args[1].value
                            in {"load", "safe_load", "full_load", "unsafe_load"}
                        )
                    if isinstance(node.func, ast.Attribute) and node.func.attr in {
                        "parse",
                        "read_bytes",
                        "read_text",
                        "open",
                    }:
                        receiver = _attribute_chain(node.func.value)
                        raw_access = raw_access or bool(
                            receiver
                            and (
                                receiver[-1]
                                in {"config_path", "resolved_config_path", "YamlLeafWalker"}
                            )
                        )
                    if call_name == "open" and node.args:
                        argument = _attribute_chain(node.args[0])
                        raw_access = raw_access or bool(
                            argument
                            and argument[-1] in {"config_path", "resolved_config_path"}
                        )
                if raw_access:
                    findings.append(
                        SourceCensusFinding(
                            "DETECTED", "RAW_YAML_ACCESS", relative, node.lineno
                        )
                    )

    @staticmethod
    def _scan_app_construction(
        app_tree: ast.Module, findings: list[SourceCensusFinding]
    ) -> None:
        prepare_calls: list[ast.Call] = []
        construct_calls: list[ast.Call] = []
        for node in ast.walk(app_tree):
            if not isinstance(node, ast.Call):
                continue
            name = _call_name(node.func)
            if name in {"RiskConfig", "RiskEngine", "BridgeEngine"}:
                findings.append(
                    SourceCensusFinding(
                        "DETECTED", "MANUAL_SETTINGS_CONSTRUCTION", "bridge/app.py", node.lineno
                    )
                )
            elif name == "prepare_runtime_settings":
                prepare_calls.append(node)
            elif name == "construct_bridge_engine":
                construct_calls.append(node)
        if len(prepare_calls) != 1:
            findings.append(
                SourceCensusFinding(
                    "DETECTED",
                    "PRODUCTION_PREPARE_CALL_COUNT",
                    "bridge/app.py",
                    prepare_calls[0].lineno if prepare_calls else 1,
                )
            )
        if len(construct_calls) != 1:
            findings.append(
                SourceCensusFinding(
                    "DETECTED",
                    "PRODUCTION_CONSTRUCT_CALL_COUNT",
                    "bridge/app.py",
                    construct_calls[0].lineno if construct_calls else 1,
                )
            )
        if prepare_calls and construct_calls and prepare_calls[0].lineno >= construct_calls[0].lineno:
            findings.append(
                SourceCensusFinding(
                    "DETECTED",
                    "CONSTRUCT_PRECEDES_VALIDATION",
                    "bridge/app.py",
                    construct_calls[0].lineno,
                )
            )

    @classmethod
    def _binding_rows(
        cls,
        trees: Mapping[str, ast.Module],
        findings: list[SourceCensusFinding],
    ) -> list[SourceCensusRow]:
        contract_path = "bridge/config_contract.py"
        contract_tree = trees[contract_path]
        capability_constants = cls._capability_constants(contract_tree)
        bound_fields = cls._bound_class_fields(contract_tree)
        constructor_calls: dict[str, list[ast.Call]] = {
            class_name: [] for class_name in bound_fields
        }
        all_take_calls: list[ast.Call] = []
        modeled_take_ids: set[int] = set()
        preliminary: list[dict[str, Any]] = []

        for node in ast.walk(contract_tree):
            if isinstance(node, ast.Call) and _call_name(node.func) == "take":
                all_take_calls.append(node)
            if isinstance(node, ast.Call):
                class_name = _call_name(node.func)
                if class_name in constructor_calls:
                    constructor_calls[class_name].append(node)

        for class_name, definition in bound_fields.items():
            calls = constructor_calls[class_name]
            if len(calls) != 1:
                findings.append(
                    SourceCensusFinding(
                        "DETECTED",
                        "BOUND_OBJECT_CONSTRUCTION_COUNT",
                        contract_path,
                        calls[0].lineno if calls else definition["line"],
                    )
                )
                continue
            call = calls[0]
            keywords = {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg}
            expected_fields = definition["fields"]
            if set(keywords) != set(expected_fields):
                findings.append(
                    SourceCensusFinding(
                        "DETECTED", "BOUND_FIELD_SET_MISMATCH", contract_path, call.lineno
                    )
                )
            for field_name, field_line in expected_fields.items():
                value = keywords.get(field_name)
                if not isinstance(value, ast.Call) or _call_name(value.func) != "take":
                    findings.append(
                        SourceCensusFinding(
                            "DETECTED",
                            "BOUND_FIELD_NOT_DIRECT_TAKE",
                            contract_path,
                            getattr(value, "lineno", call.lineno),
                        )
                    )
                    continue
                modeled_take_ids.add(id(value))
                if not value.args or not isinstance(value.args[0], ast.Constant) or not isinstance(
                    value.args[0].value, str
                ):
                    findings.append(
                        SourceCensusFinding(
                            "STOP", "UNMODELED_TAKE_PATH", contract_path, value.lineno
                        )
                    )
                    continue
                observed_path = value.args[0].value
                expected_path = f"{definition['namespace']}.{field_name}"
                capability_name = "ALWAYS"
                for keyword in value.keywords:
                    if keyword.arg == "capability":
                        if not isinstance(keyword.value, ast.Name):
                            findings.append(
                                SourceCensusFinding(
                                    "STOP",
                                    "UNMODELED_TAKE_CAPABILITY",
                                    contract_path,
                                    keyword.value.lineno,
                                )
                            )
                            capability_name = "<unmodeled>"
                        else:
                            capability_name = keyword.value.id
                capability = capability_constants.get(capability_name)
                if capability is None:
                    findings.append(
                        SourceCensusFinding(
                            "STOP", "UNKNOWN_TAKE_CAPABILITY", contract_path, value.lineno
                        )
                    )
                    continue
                if observed_path != expected_path:
                    findings.append(
                        SourceCensusFinding(
                            "DETECTED", "FIELD_PATH_MISMATCH", contract_path, value.lineno
                        )
                    )
                preliminary.append(
                    {
                        "bound_class": class_name,
                        "field": field_name,
                        "field_line": field_line,
                        "path": observed_path,
                        "expected_path": expected_path,
                        "read_capability": capability["identity"],
                        "read_gate": capability["gate"],
                        "line": value.lineno,
                    }
                )

        for take_call in all_take_calls:
            if id(take_call) not in modeled_take_ids:
                findings.append(
                    SourceCensusFinding(
                        "DETECTED", "DECORATIVE_TAKE", contract_path, take_call.lineno
                    )
                )
        paths = [row["path"] for row in preliminary]
        for duplicate_path in sorted({path for path in paths if paths.count(path) > 1}):
            first = next(row for row in preliminary if row["path"] == duplicate_path)
            findings.append(
                SourceCensusFinding(
                    "DETECTED", "DUPLICATE_TAKE_PATH", contract_path, first["line"]
                )
            )

        risk_consumers = cls._derive_risk_consumers(trees, findings)
        cls._verify_risk_constructor(contract_tree, findings)
        engine_targets = cls._derive_engine_targets(trees, findings)
        rows: list[SourceCensusRow] = []
        for row in preliminary:
            if row["bound_class"] == "BoundRiskInputs":
                consumer = risk_consumers.get(row["field"])
                target_field = row["field"]
            else:
                target_field = engine_targets.get(
                    (row["bound_class"], row["field"]), "<missing>"
                )
                consumer = ("always", None) if target_field != "<missing>" else None
            if consumer is None:
                findings.append(
                    SourceCensusFinding(
                        "DETECTED", "BOUND_FIELD_NO_CONSUMER", contract_path, row["line"]
                    )
                )
                consumer_identity, consumer_gate = "<missing>", "<missing>"
            else:
                consumer_identity, consumer_gate = consumer
            if row["read_capability"] != consumer_identity:
                findings.append(
                    SourceCensusFinding(
                        "DETECTED",
                        "CAPABILITY_IDENTITY_MISMATCH",
                        contract_path,
                        row["line"],
                    )
                )
            if row["read_gate"] != consumer_gate:
                findings.append(
                    SourceCensusFinding(
                        "DETECTED", "CAPABILITY_GATE_MISMATCH", contract_path, row["line"]
                    )
                )
            rows.append(
                SourceCensusRow(
                    producer="ConfigContractAstCensus",
                    bound_class=row["bound_class"],
                    target_field=target_field,
                    setting_path=row["path"],
                    expected_path=row["expected_path"],
                    read_site_capability=row["read_capability"],
                    consumer_capability=consumer_identity,
                    source_path=contract_path,
                    source_line=row["line"],
                    field_source_path=contract_path,
                    field_source_line=row["field_line"],
                    take_source_path=contract_path,
                    take_source_line=row["line"],
                )
            )
        return rows

    @staticmethod
    def _capability_constants(tree: ast.Module) -> dict[str, dict[str, str | None]]:
        constants: dict[str, dict[str, str | None]] = {}
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            if not isinstance(node.targets[0], ast.Name) or not isinstance(node.value, ast.Call):
                continue
            if _call_name(node.value.func) != "Capability" or not node.value.args:
                continue
            identity_node = node.value.args[0]
            gate_node = node.value.args[1] if len(node.value.args) > 1 else None
            if not isinstance(identity_node, ast.Constant) or not isinstance(
                identity_node.value, str
            ):
                continue
            gate = gate_node.value if isinstance(gate_node, ast.Constant) else None
            constants[node.targets[0].id] = {
                "identity": identity_node.value,
                "gate": gate,
            }
        return constants

    @staticmethod
    def _bound_class_fields(tree: ast.Module) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            namespace = None
            bound_members: dict[str, int] = {}
            for child in node.body:
                if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                    if child.target.id == "SETTING_NAMESPACE" and isinstance(
                        child.value, ast.Constant
                    ):
                        namespace = child.value.value
                    elif (
                        isinstance(child.annotation, ast.Subscript)
                        and _call_name(child.annotation.value) == "TakenValue"
                    ):
                        bound_members[child.target.id] = child.lineno
            if namespace is not None:
                result[node.name] = {
                    "namespace": namespace,
                    "fields": bound_members,
                    "line": node.lineno,
                }
        return result

    @classmethod
    def _derive_risk_consumers(
        cls,
        trees: Mapping[str, ast.Module],
        findings: list[SourceCensusFinding],
    ) -> dict[str, tuple[str, str | None]]:
        risk_tree = trees["bridge/engine/risk.py"]
        engine_tree = trees["bridge/engine/engine.py"]
        reconcile_tree = trees["bridge/engine/reconcile.py"]
        durable_fields: set[str] = set()
        exposure_fields: set[str] = set()
        direct_fields: set[str] = set()
        risk_class = next(
            (node for node in risk_tree.body if isinstance(node, ast.ClassDef) and node.name == "RiskEngine"),
            None,
        )
        if risk_class is None:
            findings.append(
                SourceCensusFinding("STOP", "RISK_ENGINE_CLASS_MISSING", "bridge/engine/risk.py", 1)
            )
            return {}
        init = next(
            (node for node in risk_class.body if isinstance(node, ast.FunctionDef) and node.name == "__init__"),
            None,
        )
        if init is None:
            findings.append(
                SourceCensusFinding("STOP", "RISK_INIT_MISSING", "bridge/engine/risk.py", risk_class.lineno)
            )
            return {}
        for node in ast.walk(init):
            if not isinstance(node, ast.Call):
                continue
            owner = _call_name(node.func.value) if isinstance(node.func, ast.Attribute) else None
            if owner not in {"DurableRiskPolicy", "ExposureRiskPolicy"}:
                continue
            target = durable_fields if owner == "DurableRiskPolicy" else exposure_fields
            for keyword in node.keywords:
                chain = _attribute_chain(keyword.value)
                if chain and len(chain) == 3 and chain[:2] == ("self", "config"):
                    target.add(chain[2])
        for function in risk_class.body:
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)) or function.name == "__init__":
                continue
            for node in ast.walk(function):
                chain = _attribute_chain(node)
                if chain and len(chain) == 3 and chain[:2] == ("self", "config"):
                    direct_fields.add(chain[2])

        durable_gate = cls._keyword_gate_method(
            engine_tree, "require_daily_state", "bridge/engine/engine.py", findings
        )
        exposure_gate = cls._snapshot_gate_method(reconcile_tree, findings)
        consumers: dict[str, tuple[str, str | None]] = {}
        for field_name in direct_fields:
            consumers[field_name] = ("always", None)
        for field_name in durable_fields - direct_fields:
            consumers[field_name] = ("durable_risk", durable_gate)
        for field_name in exposure_fields - direct_fields:
            consumers[field_name] = ("exposure_controls", exposure_gate)
        return consumers

    @staticmethod
    def _verify_risk_constructor(
        contract_tree: ast.Module, findings: list[SourceCensusFinding]
    ) -> None:
        construct = next(
            (
                node
                for node in contract_tree.body
                if isinstance(node, ast.FunctionDef)
                and node.name == "construct_bridge_engine"
            ),
            None,
        )
        matched = 0
        if construct is not None:
            for node in ast.walk(construct):
                if not isinstance(node, ast.Call) or _call_name(node.func) != "unwrap_all":
                    continue
                if not isinstance(node.func, ast.Attribute):
                    continue
                if _attribute_chain(node.func.value) != ("validated", "risk"):
                    continue
                if any(
                    isinstance(argument, ast.Name) and argument.id == "RiskConfig"
                    for argument in node.args
                ):
                    matched += 1
        if matched != 1:
            findings.append(
                SourceCensusFinding(
                    "DETECTED",
                    "RISK_BOUND_NOT_EXACT_CONSTRUCTOR_INPUT",
                    "bridge/config_contract.py",
                    construct.lineno if construct is not None else 1,
                )
            )

    @staticmethod
    def _keyword_gate_method(
        tree: ast.Module,
        keyword_name: str,
        source_path: str,
        findings: list[SourceCensusFinding],
    ) -> str | None:
        gates: set[str] = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            for keyword in node.keywords:
                if keyword.arg != keyword_name:
                    continue
                for child in ast.walk(keyword.value):
                    if isinstance(child, ast.Attribute) and child.attr.endswith("_enabled"):
                        gates.add(child.attr)
        if len(gates) != 1:
            findings.append(
                SourceCensusFinding(
                    "STOP", "UNMODELED_CONSUMER_GATE", source_path, 1
                )
            )
            return "<unmodeled>"
        return next(iter(gates))

    @staticmethod
    def _snapshot_gate_method(
        tree: ast.Module, findings: list[SourceCensusFinding]
    ) -> str | None:
        methods: set[str] = set()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name != "_snapshot_version":
                continue
            for child in ast.walk(node):
                if isinstance(child, ast.Constant) and isinstance(child.value, str) and child.value.endswith(
                    "_controls_enabled"
                ):
                    methods.add(child.value)
                elif isinstance(child, ast.Attribute) and child.attr.endswith("_controls_enabled"):
                    methods.add(child.attr)
        if len(methods) != 1:
            findings.append(
                SourceCensusFinding(
                    "STOP", "UNMODELED_EXPOSURE_GATE", "bridge/engine/reconcile.py", 1
                )
            )
            return "<unmodeled>"
        return next(iter(methods))

    @staticmethod
    def _derive_engine_targets(
        trees: Mapping[str, ast.Module],
        findings: list[SourceCensusFinding],
    ) -> dict[tuple[str, str], str]:
        contract_tree = trees["bridge/config_contract.py"]
        engine_tree = trees["bridge/engine/engine.py"]
        construct = next(
            (
                node
                for node in contract_tree.body
                if isinstance(node, ast.FunctionDef) and node.name == "construct_bridge_engine"
            ),
            None,
        )
        if construct is None:
            findings.append(
                SourceCensusFinding(
                    "STOP", "CONSTRUCT_INTERFACE_MISSING", "bridge/config_contract.py", 1
                )
            )
            return {}
        engine_call = next(
            (
                node
                for node in ast.walk(construct)
                if isinstance(node, ast.Call) and _call_name(node.func) == "BridgeEngine"
            ),
            None,
        )
        if engine_call is None:
            findings.append(
                SourceCensusFinding(
                    "STOP", "BRIDGE_ENGINE_CALL_MISSING", "bridge/config_contract.py", construct.lineno
                )
            )
            return {}
        engine_fields = {
            child.target.id
            for node in engine_tree.body
            if isinstance(node, ast.ClassDef) and node.name == "BridgeEngine"
            for child in node.body
            if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name)
        }
        targets: dict[tuple[str, str], str] = {}
        prefixes = {
            "broker_options": "BoundBrokerInputs",
            "risk_start_options": "BoundRiskEngineStartInputs",
        }
        expected_bindings = {
            "broker_options": (
                ("validated", "engine_start", "broker"),
                "BrokerEngineStartOptions",
            ),
            "risk_start_options": (
                ("validated", "engine_start", "risk"),
                "RiskEngineStartOptions",
            ),
        }
        observed_bindings: set[str] = set()
        for child in ast.walk(construct):
            if not isinstance(child, ast.Assign) or len(child.targets) != 1:
                continue
            if not isinstance(child.targets[0], ast.Name) or child.targets[0].id not in expected_bindings:
                continue
            variable = child.targets[0].id
            expected_chain, expected_target = expected_bindings[variable]
            value = child.value
            if (
                isinstance(value, ast.Call)
                and _call_name(value.func) == "unwrap_all"
                and isinstance(value.func, ast.Attribute)
                and _attribute_chain(value.func.value) == expected_chain
                and any(
                    isinstance(argument, ast.Name) and argument.id == expected_target
                    for argument in value.args
                )
            ):
                observed_bindings.add(variable)
        for variable in sorted(set(expected_bindings) - observed_bindings):
            findings.append(
                SourceCensusFinding(
                    "DETECTED",
                    "ENGINE_OPTIONS_NOT_BOUND_OBJECT_INPUT",
                    "bridge/config_contract.py",
                    construct.lineno,
                )
            )
        for keyword in engine_call.keywords:
            if keyword.arg is None:
                findings.append(
                    SourceCensusFinding(
                        "STOP", "UNMODELED_ENGINE_KWARGS", "bridge/config_contract.py", keyword.value.lineno
                    )
                )
                continue
            for child in ast.walk(keyword.value):
                chain = _attribute_chain(child)
                if chain and len(chain) == 2 and chain[0] in prefixes:
                    key = (prefixes[chain[0]], chain[1])
                    if key in targets:
                        findings.append(
                            SourceCensusFinding(
                                "DETECTED", "ENGINE_FIELD_DUPLICATE_USE", "bridge/config_contract.py", child.lineno
                            )
                        )
                    targets[key] = keyword.arg
                    if keyword.arg not in engine_fields:
                        findings.append(
                            SourceCensusFinding(
                                "DETECTED", "ENGINE_TARGET_FIELD_MISSING", "bridge/config_contract.py", child.lineno
                            )
                        )
        return targets
