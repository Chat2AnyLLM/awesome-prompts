# Prompt Collection Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a curated prompt collection repo with YAML source files, JSON Schema validation, and automated build pipeline that generates `prompts.json` and `prompts.csv` for programmatic consumption.

**Architecture:** Individual YAML files per prompt are the source of truth. A Python build script compiles them into `dist/prompts.json` and `dist/prompts.csv`. JSON Schema validates contributions. CI enforces validation and freshness of generated artifacts.

**Tech Stack:** Python 3.10+, PyYAML, jsonschema, GitHub Actions

---

## File Structure

| File | Responsibility |
|------|---------------|
| `schema/prompt.schema.json` | JSON Schema defining the contract for a single prompt |
| `scripts/validate.py` | Loads all YAML files and validates each against the schema |
| `scripts/build.py` | Reads all YAML, validates, outputs `dist/prompts.json` + `dist/prompts.csv` |
| `Makefile` | Convenience targets: `validate`, `build`, `ci` |
| `prompts/linux-terminal.yaml` | Sample prompt #1 |
| `prompts/english-translator.yaml` | Sample prompt #2 |
| `prompts/code-reviewer.yaml` | Sample prompt #3 |
| `dist/prompts.json` | Generated: all prompts as structured JSON |
| `dist/prompts.csv` | Generated: all prompts as flat CSV |
| `.github/workflows/ci.yml` | CI: validate + build + freshness check |
| `README.md` | Project overview and consumer instructions |
| `CONTRIBUTING.md` | How to add a prompt |
| `LICENSE` | MIT license |
| `.gitignore` | Python bytecode, venv, OS files |
| `requirements.txt` | Python dependencies |

---

### Task 1: Project Scaffolding

**Files:**
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `requirements.txt`

- [ ] **Step 1: Create `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
venv/
.venv/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

- [ ] **Step 2: Create `LICENSE` (MIT)**

```text
MIT License

Copyright (c) 2026 Jian Zhu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Create `requirements.txt`**

```text
pyyaml>=6.0
jsonschema>=4.20
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore LICENSE requirements.txt
git commit -m "chore: add project scaffolding (license, gitignore, requirements)"
```

---

### Task 2: JSON Schema

**Files:**
- Create: `schema/prompt.schema.json`

- [ ] **Step 1: Create `schema/prompt.schema.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/zhujian0805/awesome-prompts/schema/prompt.schema.json",
  "title": "Prompt",
  "description": "Schema for a single curated prompt",
  "type": "object",
  "required": ["slug", "title", "description", "prompt", "tags", "category", "author"],
  "additionalProperties": false,
  "properties": {
    "slug": {
      "type": "string",
      "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
      "description": "URL-safe identifier, must match the filename"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "description": {
      "type": "string",
      "minLength": 1,
      "maxLength": 300
    },
    "prompt": {
      "type": "string",
      "minLength": 10
    },
    "tags": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "minItems": 1,
      "uniqueItems": true
    },
    "category": {
      "type": "string",
      "enum": [
        "developer-tools",
        "writing",
        "education",
        "creative",
        "business",
        "language",
        "lifestyle",
        "analysis"
      ]
    },
    "author": {
      "type": "string",
      "minLength": 1
    },
    "variables": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name"],
        "properties": {
          "name": { "type": "string" },
          "default": { "type": "string" }
        },
        "additionalProperties": false
      }
    }
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add schema/prompt.schema.json
git commit -m "feat: add JSON Schema for prompt validation"
```

---

### Task 3: Validation Script

**Files:**
- Create: `scripts/validate.py`

- [ ] **Step 1: Create `scripts/validate.py`**

```python
#!/usr/bin/env python3
"""Validate all prompt YAML files against the JSON Schema."""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError

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
```

- [ ] **Step 2: Make script executable**

```bash
chmod +x scripts/validate.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/validate.py
git commit -m "feat: add validation script for prompt YAML files"
```

---

### Task 4: Build Script

**Files:**
- Create: `scripts/build.py`

- [ ] **Step 1: Create `scripts/build.py`**

```python
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
```

- [ ] **Step 2: Make script executable**

```bash
chmod +x scripts/build.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/build.py
git commit -m "feat: add build script to generate dist/prompts.json and dist/prompts.csv"
```

---

### Task 5: Makefile

**Files:**
- Create: `Makefile`

- [ ] **Step 1: Create `Makefile`**

```makefile
.PHONY: validate build ci clean install

install:
	pip install -r requirements.txt

validate:
	python scripts/validate.py

build:
	python scripts/build.py

ci: validate build

clean:
	rm -rf dist/
```

- [ ] **Step 2: Commit**

```bash
git add Makefile
git commit -m "feat: add Makefile with validate, build, ci targets"
```

---

### Task 6: Sample Prompts

**Files:**
- Create: `prompts/linux-terminal.yaml`
- Create: `prompts/english-translator.yaml`
- Create: `prompts/code-reviewer.yaml`

- [ ] **Step 1: Create `prompts/linux-terminal.yaml`**

```yaml
slug: linux-terminal
title: Linux Terminal
description: Simulates a Linux terminal, responding only with terminal output.
prompt: |
  I want you to act as a linux terminal. I will type commands and you will
  reply with what the terminal should show. I want you to only reply with
  the terminal output inside one unique code block, and nothing else. Do not
  write explanations. Do not type commands unless I instruct you to do so.
  When I need to tell you something in english, I will do so by putting text
  inside curly brackets {like this}. My first command is pwd
tags:
  - developer
  - terminal
  - simulation
category: developer-tools
author: f
```

- [ ] **Step 2: Create `prompts/english-translator.yaml`**

```yaml
slug: english-translator
title: English Translator and Improver
description: Translates and improves text into elegant English while preserving meaning.
prompt: |
  I want you to act as an English translator, spelling corrector and improver.
  I will speak to you in any language and you will detect the language, translate
  it and answer in the corrected and improved version of my text, in English.
  I want you to replace my simplified A0-level words and sentences with more
  beautiful and elegant, upper level English words and sentences. Keep the meaning
  same, but make them more literary. I want you to only reply the correction, the
  improvements and nothing else, do not write explanations.
tags:
  - language
  - translation
  - writing
category: language
author: f
```

- [ ] **Step 3: Create `prompts/code-reviewer.yaml`**

```yaml
slug: code-reviewer
title: Code Reviewer
description: Reviews code for bugs, security issues, and improvements with structured feedback.
prompt: |
  I want you to act as a code reviewer. I will paste code snippets and you will
  review them for: bugs and logic errors, security vulnerabilities, performance
  issues, code style and readability, and potential improvements. Structure your
  review as a list of findings, each with a severity (critical/warning/suggestion),
  the relevant line(s), and a brief explanation. End with an overall assessment.
tags:
  - developer
  - code-review
  - quality
category: developer-tools
author: zhujian0805
```

- [ ] **Step 4: Run validation to test**

```bash
make install && make validate
```

Expected output:
```
  OK: code-reviewer.yaml
  OK: english-translator.yaml
  OK: linux-terminal.yaml

All 3 prompt(s) valid.
```

- [ ] **Step 5: Run build**

```bash
make build
```

Expected output:
```
Building prompt collection...
  Written: dist/prompts.json (3 prompts)
  Written: dist/prompts.csv (3 prompts)
Done.
```

- [ ] **Step 6: Commit**

```bash
git add prompts/ dist/
git commit -m "feat: add sample prompts and generated dist/ artifacts"
```

---

### Task 7: CI Workflow

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Validate prompts
        run: make validate

      - name: Build dist
        run: make build

      - name: Check dist is up to date
        run: |
          if ! git diff --quiet dist/; then
            echo "ERROR: dist/ is out of date. Run 'make build' and commit the changes."
            git diff dist/
            exit 1
          fi
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow for validation and build"
```

---

### Task 8: Documentation

**Files:**
- Create: `README.md`
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Create `README.md`**

```markdown
# Awesome Prompts

A curated collection of high-quality prompts for AI assistants, stored in a machine-readable format for programmatic consumption.

## For Consumers

Fetch the full prompt collection as JSON:

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/prompts.json
```

Or clone and read locally:

```bash
git clone https://github.com/zhujian0805/awesome-prompts.git
cat awesome-prompts/dist/prompts.json
```

### JSON Format

```json
{
  "version": "1.0.0",
  "generated_at": "2026-06-22T10:00:00Z",
  "count": 3,
  "prompts": [
    {
      "slug": "linux-terminal",
      "title": "Linux Terminal",
      "description": "Simulates a Linux terminal...",
      "prompt": "I want you to act as a linux terminal...",
      "tags": ["developer", "terminal", "simulation"],
      "category": "developer-tools",
      "author": "f",
      "variables": []
    }
  ]
}
```

A CSV export is also available at `dist/prompts.csv`.

## For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a prompt.

## Categories

| Category | Description |
|----------|-------------|
| `developer-tools` | Programming, debugging, code review |
| `writing` | Content creation, editing, copywriting |
| `education` | Teaching, tutoring, explaining |
| `creative` | Art, music, storytelling |
| `business` | Strategy, marketing, management |
| `language` | Translation, grammar, language learning |
| `lifestyle` | Travel, health, personal advice |
| `analysis` | Data, research, critical thinking |

## License

MIT
```

- [ ] **Step 2: Create `CONTRIBUTING.md`**

```markdown
# Contributing

## Adding a Prompt

1. Create a new file `prompts/<slug>.yaml` where `<slug>` is a URL-safe identifier (lowercase, hyphens only).

2. Use this template:

```yaml
slug: my-prompt-name
title: My Prompt Name
description: A one-line summary of what this prompt does.
prompt: |
  The full prompt text goes here. Use the pipe character (|) for
  multi-line prompts to preserve formatting.
tags:
  - relevant
  - tags
category: developer-tools
author: your-github-username
```

3. Validate locally:

```bash
pip install -r requirements.txt
make validate
```

4. Build the dist files:

```bash
make build
```

5. Commit all changes (including `dist/`) and open a PR.

## Schema

The full schema is at `schema/prompt.schema.json`. Key rules:

- `slug` must match the filename (without `.yaml`)
- `slug` must be lowercase with hyphens only: `^[a-z0-9]+(-[a-z0-9]+)*$`
- `category` must be one of: `developer-tools`, `writing`, `education`, `creative`, `business`, `language`, `lifestyle`, `analysis`
- `tags` must have at least one entry, no duplicates
- `prompt` must be at least 10 characters

## Template Variables

If your prompt uses template variables (like `${Position}`), declare them:

```yaml
variables:
  - name: Position
    default: Software Developer
```

## Guidelines

- Write clear, specific prompts that produce consistent results
- Include context about expected behavior in the prompt itself
- One prompt per file
- Test your prompt with an AI assistant before submitting
```

- [ ] **Step 3: Commit**

```bash
git add README.md CONTRIBUTING.md
git commit -m "docs: add README and CONTRIBUTING guide"
```

---

### Task 9: Final Verification

- [ ] **Step 1: Run full CI pipeline locally**

```bash
make ci
```

Expected:
```
  OK: code-reviewer.yaml
  OK: english-translator.yaml
  OK: linux-terminal.yaml

All 3 prompt(s) valid.
Building prompt collection...
  Written: dist/prompts.json (3 prompts)
  Written: dist/prompts.csv (3 prompts)
Done.
```

- [ ] **Step 2: Verify dist/prompts.json is valid JSON**

```bash
python -c "import json; d = json.load(open('dist/prompts.json')); print(f'{d[\"count\"]} prompts, version {d[\"version\"]}')"
```

Expected: `3 prompts, version 1.0.0`

- [ ] **Step 3: Verify repo structure**

```bash
find . -not -path './.git/*' -not -path './.git' | sort
```

Expected to show all planned files in the correct locations.
