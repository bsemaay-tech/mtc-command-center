from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


def validate_json_schema(instance: Any, schema: dict[str, Any]) -> list[ValidationIssue]:
    try:
        from jsonschema import Draft202012Validator
    except Exception:
        return _fallback_validate(instance, schema, "$")

    validator = Draft202012Validator(schema)
    issues: list[ValidationIssue] = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        path = "$"
        if error.absolute_path:
            path += "." + ".".join(str(part) for part in error.absolute_path)
        issues.append(ValidationIssue(path=path, message=error.message))
    return issues


def _fallback_validate(instance: Any, schema: dict[str, Any], path: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    expected_type = schema.get("type")
    if expected_type is not None and not _matches_type(instance, expected_type):
        issues.append(ValidationIssue(path, f"expected type {expected_type}"))
        return issues

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                issues.append(ValidationIssue(f"{path}.{key}", "required property is missing"))

        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                issues.extend(_fallback_validate(value, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                issues.append(ValidationIssue(f"{path}.{key}", "additional property is not allowed"))

    if isinstance(instance, list) and "items" in schema:
        item_schema = schema["items"]
        for index, value in enumerate(instance):
            issues.extend(_fallback_validate(value, item_schema, f"{path}[{index}]"))

    if "enum" in schema and instance not in schema["enum"]:
        issues.append(ValidationIssue(path, f"value is not in enum {schema['enum']}"))

    return issues


def _matches_type(value: Any, expected_type: str | list[str]) -> bool:
    expected = expected_type if isinstance(expected_type, list) else [expected_type]
    for type_name in expected:
        if type_name == "object" and isinstance(value, dict):
            return True
        if type_name == "array" and isinstance(value, list):
            return True
        if type_name == "string" and isinstance(value, str):
            return True
        if type_name == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if type_name == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if type_name == "boolean" and isinstance(value, bool):
            return True
        if type_name == "null" and value is None:
            return True
    return False

