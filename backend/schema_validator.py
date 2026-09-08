"""JSON Schema validation for threat reports"""

import json
import os
from jsonschema import validate, ValidationError

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "schemas")

def load_schema(framework: str) -> dict:
    """Load schema for a framework"""
    schema_file = os.path.join(SCHEMAS_DIR, f"{framework.lower()}.schema.json")

    if not os.path.exists(schema_file):
        raise ValueError(f"Schema not found for framework: {framework}")

    with open(schema_file, 'r') as f:
        return json.load(f)

def validate_threat_report(report: dict, framework: str) -> tuple[bool, list]:
    """Validate threat report against schema. Returns (is_valid, errors)"""
    try:
        schema = load_schema(framework)
        validate(instance=report, schema=schema)
        return True, []
    except ValidationError as e:
        errors = [str(e) for e in e.context] if e.context else [str(e)]
        return False, errors
    except Exception as e:
        return False, [str(e)]

def get_schema_requirements(framework: str) -> dict:
    """Get human-readable schema requirements"""
    schema = load_schema(framework)

    return {
        "required_fields": schema.get("required", []),
        "properties": {
            name: prop.get("description", "")
            for name, prop in schema.get("properties", {}).items()
        }
    }
