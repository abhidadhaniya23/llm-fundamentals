"""
A small JSON-Schema subset validator.

The same schema is sent to the LLM as the tool's parameters and used by the
gateway to validate the arguments the LLM produced (and each agent's final JSON).
Supported: type (incl. lists like ["string","null"]), properties, required,
additionalProperties=false, enum, items, maxLength, pattern, minimum/maximum.
"""

import re

_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "integer": int, "number": (int, float), "null": type(None),
}


def _is_type(value, name: str) -> bool:
    if name in ("integer", "number") and isinstance(value, bool):
        return False
    return isinstance(value, _TYPES[name])


def validate(value, schema: dict, path: str = "$") -> list[str]:
    errors: list[str] = []
    types = schema.get("type")
    if types:
        allowed = types if isinstance(types, list) else [types]
        if not any(_is_type(value, t) for t in allowed):
            return [f"{path}: expected {'/'.join(allowed)}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not one of {schema['enum']}")
    if isinstance(value, str):
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than {schema['maxLength']} chars")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above {schema['maximum']}")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{path}: missing required '{name}'")
        for name, item in value.items():
            if name in properties:
                errors += validate(item, properties[name], f"{path}.{name}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property '{name}'")
    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            errors += validate(item, schema["items"], f"{path}[{index}]")
    return errors


def obj(required: list[str] | None = None, **properties) -> dict:
    """Shorthand: obj(['a'], a=STR, b=BOOL) -> strict object schema."""
    return {"type": "object", "properties": properties, "required": required or list(properties),
            "additionalProperties": False}


STR = {"type": "string", "maxLength": 500}
BOOL = {"type": "boolean"}
DOC_ID = {"type": "string", "pattern": r"\d{4}"}
DATE = {"type": "string", "pattern": r"\d{4}-\d{2}-\d{2}"}
WORKSPACE = {"type": "string", "enum": ["Finance", "Compliance", "HR"]}
PERMISSION = {"type": "string", "enum": ["read", "upload"]}
REQUEST_ID = {"type": "string", "pattern": r"REQ-\d+"}
BATCH_ID = {"type": "string", "pattern": r"BATCH-\d{4}-\d{2}-\d{2}-\d{3}"}
REASON_CODE = {"type": "string", "pattern": r"[A-Z]{3}-[A-Z-]+"}
