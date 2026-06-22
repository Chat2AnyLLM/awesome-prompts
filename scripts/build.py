#!/usr/bin/env python3
"""Build dist/prompts.json and dist/prompts.csv from prompts/*.yaml."""

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "prompt.schema.json"
PROMPTS_DIR = REPO_ROOT / "prompts"
DIST_DIR = REPO_ROOT / "dist"

VERSION = "1.0.0"


def load_schema() -> dict:
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def load_and_validate_prompts(schema: dict) -> list[dict]:
    """Load all YAML files, validate, return sorted list of prompt dicts."""
    validator = Draft202012Validator(schema)
    prompts = []
    yaml_files = sorted(PROMPTS_DIR.glob("*.yaml"))

    if not yaml_files:
        print("WARNING: No prompt files found in prompts/")
        return []

    for file_path in yaml_files:
        with open(file_path) as f:
            data = yaml.safe_load(f)

        errors = list(validator.iter_errors(data))
        if errors:
            print(f"FAIL: {file_path.name}")
            for err in errors:
                print(f"  {err.json_path}: {err.message}")
            sys.exit(1)

        # Ensure slug matches filename
        if data.get("slug") != file_path.stem:
            print(f"FAIL: {file_path.name} - slug does not match filename")
            sys.exit(1)

        # Normalize: ensure variables key exists
        data.setdefault("variables", [])
        prompts.append(data)

    return prompts


def write_json(prompts: list[dict]) -> None:
    """Write dist/prompts.json."""
    output = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(prompts),
        "prompts": prompts,
    }
    DIST_DIR.mkdir(exist_ok=True)
    output_path = DIST_DIR / "prompts.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Written: {output_path} ({len(prompts)} prompts)")


def write_csv(prompts: list[dict]) -> None:
    """Write dist/prompts.csv."""
    DIST_DIR.mkdir(exist_ok=True)
    output_path = DIST_DIR / "prompts.csv"
    fieldnames = ["slug", "title", "description", "prompt", "tags", "category", "author"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for prompt in prompts:
            row = {k: prompt[k] for k in fieldnames if k != "tags"}
            row["tags"] = ";".join(prompt["tags"])
            writer.writerow(row)
    print(f"  Written: {output_path} ({len(prompts)} prompts)")


def main() -> int:
    print("Building prompt collection...")
    schema = load_schema()
    prompts = load_and_validate_prompts(schema)
    write_json(prompts)
    write_csv(prompts)
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
