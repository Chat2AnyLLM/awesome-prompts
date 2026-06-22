#!/usr/bin/env python3
"""Build dist/ artifacts from prompts/*.yaml and sources/*.yaml."""

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_SCHEMA_PATH = REPO_ROOT / "schema" / "prompt.schema.json"
SOURCE_SCHEMA_PATH = REPO_ROOT / "schema" / "source.schema.json"
PROMPTS_DIR = REPO_ROOT / "prompts"
SOURCES_DIR = REPO_ROOT / "sources"
DIST_DIR = REPO_ROOT / "dist"

VERSION = "1.0.0"


def load_schema(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_and_validate(directory: Path, schema: dict) -> list[dict]:
    """Load all YAML files from directory, validate, return sorted list."""
    validator = Draft202012Validator(schema)
    items = []
    yaml_files = sorted(directory.glob("*.yaml"))

    if not yaml_files:
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

        if data.get("slug") != file_path.stem:
            print(f"FAIL: {file_path.name} - slug does not match filename")
            sys.exit(1)

        items.append(data)

    return items


def write_prompts_json(prompts: list[dict]) -> None:
    """Write dist/prompts.json."""
    # Normalize: ensure variables key exists
    for p in prompts:
        p.setdefault("variables", [])

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


def write_prompts_csv(prompts: list[dict]) -> None:
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


def write_sources_json(sources: list[dict]) -> None:
    """Write dist/sources.json."""
    output = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(sources),
        "sources": sources,
    }
    DIST_DIR.mkdir(exist_ok=True)
    output_path = DIST_DIR / "sources.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Written: {output_path} ({len(sources)} sources)")


def write_index_json(prompts: list[dict], sources: list[dict]) -> None:
    """Write dist/index.json — a single entry point for consumers."""
    output = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompts": {
            "count": len(prompts),
            "file": "prompts.json",
        },
        "sources": {
            "count": len(sources),
            "file": "sources.json",
        },
    }
    DIST_DIR.mkdir(exist_ok=True)
    output_path = DIST_DIR / "index.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Written: {output_path}")


def main() -> int:
    print("Building prompt collection...")

    prompt_schema = load_schema(PROMPT_SCHEMA_PATH)
    source_schema = load_schema(SOURCE_SCHEMA_PATH)

    prompts = load_and_validate(PROMPTS_DIR, prompt_schema)
    sources = load_and_validate(SOURCES_DIR, source_schema)

    write_prompts_json(prompts)
    write_prompts_csv(prompts)
    write_sources_json(sources)
    write_index_json(prompts, sources)

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
