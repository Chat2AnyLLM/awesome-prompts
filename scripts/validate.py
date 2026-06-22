#!/usr/bin/env python3
"""Validate all prompt YAML files against the JSON Schema."""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "prompt.schema.json"
PROMPTS_DIR = REPO_ROOT / "prompts"


def load_schema() -> dict:
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def validate_prompt(file_path: Path, schema: dict) -> list[str]:
    """Validate a single YAML file. Returns list of error messages."""
    errors = []
    try:
        with open(file_path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    if data is None:
        return ["File is empty"]

    # Validate against schema
    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(data):
        errors.append(f"  {error.json_path}: {error.message}")

    # Check slug matches filename
    expected_slug = file_path.stem
    if data.get("slug") != expected_slug:
        errors.append(
            f"  slug '{data.get('slug')}' does not match filename '{expected_slug}'"
        )

    return errors


def main() -> int:
    schema = load_schema()
    yaml_files = sorted(PROMPTS_DIR.glob("*.yaml"))

    if not yaml_files:
        print("WARNING: No prompt files found in prompts/")
        return 0

    total_errors = 0
    for file_path in yaml_files:
        errors = validate_prompt(file_path, schema)
        if errors:
            print(f"FAIL: {file_path.name}")
            for err in errors:
                print(err)
            total_errors += len(errors)
        else:
            print(f"  OK: {file_path.name}")

    if total_errors:
        print(f"\n{total_errors} error(s) found.")
        return 1

    print(f"\nAll {len(yaml_files)} prompt(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
