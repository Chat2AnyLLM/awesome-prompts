# Config YAML Unified Sources Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `awesome_prompts.json` with `config.yaml` and make `scripts/build.py` aggregate local, GitHub, and remote JSON prompt sources into one unified `dist/` collection.

**Architecture:** `config.yaml` is the single source of truth. `scripts/build.py` loads config, dispatches each source to a focused loader (`local`, `github`, `json_url`), normalizes prompts, deduplicates by slug with first source winning, caches scraped GitHub prompts under `scraped/`, and writes unified `dist/` artifacts.

**Tech Stack:** Python 3, PyYAML, jsonschema, urllib, csv/json standard libraries, Makefile.

---

## File Structure

- Create `config.yaml`: YAML config migrated from `awesome_prompts.json`, plus local prompt source.
- Modify `scripts/build.py`: replace the old local-only builder with unified source loading and artifact generation.
- Modify `scripts/update_readme.py`: read `config.yaml` / generated `dist/` instead of legacy config assumptions if needed.
- Modify `Makefile`: make `build` do all aggregation and remove `scrape` from the normal flow.
- Modify `README.md`: document config.yaml and unified outputs.
- Delete `awesome_prompts.json`: replaced by `config.yaml`.
- Delete `scripts/scrape.py`: GitHub scraping is folded into `build.py`.

## Task 1: Add config.yaml

**Files:**
- Create: `config.yaml`

- [ ] **Step 1: Create YAML config migrated from current sources**

```yaml
version: "2.0.0"
description: "Aggregates prompts from local files, GitHub repos, and remote JSON endpoints into a unified collection."

output:
  dir: dist
  formats: [json, csv]

sources:
  - name: "Local Prompts"
    type: local
    path: prompts/
    description: "Hand-curated prompts maintained in this repo"

  - name: "Prompts Chat"
    type: github
    url: https://github.com/f/prompts.chat
    format: csv
    file_path: prompts.csv
    description: "Large community-curated collection of ChatGPT prompts (prompts.chat)"

  - name: "Leaked System Prompts"
    type: github
    url: https://github.com/jujumilk3/leaked-system-prompts
    format: md
    file_path: ""
    description: "System prompts from various AI products, stored as markdown files"

  - name: "AI Boost Awesome Prompts"
    type: github
    url: https://github.com/ai-boost/awesome-prompts
    format: txt
    file_path: prompts/
    description: "300+ curated role-based prompts as plain text files"
```

- [ ] **Step 2: Verify YAML parses**

Run: `python - <<'PY'\nimport yaml\nfrom pathlib import Path\nprint(yaml.safe_load(Path('config.yaml').read_text())['version'])\nPY`

Expected: `2.0.0`

## Task 2: Rewrite unified builder

**Files:**
- Modify: `scripts/build.py`

- [ ] **Step 1: Replace `scripts/build.py` with unified implementation**

The implementation must include these functions:

```python
load_config() -> dict
slugify(text: str) -> str
fetch_url(url: str) -> str
parse_github_url(url: str) -> tuple[str, str]
get_default_branch(user: str, repo: str) -> str
normalize_prompt(prompt: dict, source_name: str, defaults: dict | None = None) -> dict | None
load_local_source(source: dict, prompt_schema: dict) -> list[dict]
load_github_source(source: dict) -> list[dict]
load_json_url_source(source: dict) -> list[dict]
load_source(source: dict, prompt_schema: dict) -> list[dict]
dedupe_prompts(prompts: list[dict]) -> list[dict]
write_prompts_json(prompts: list[dict], output_dir: Path) -> None
write_prompts_csv(prompts: list[dict], output_dir: Path) -> None
write_sources_json(sources: list[dict], output_dir: Path) -> None
write_index_json(prompts: list[dict], sources: list[dict], output_dir: Path) -> None
main() -> int
```

- [ ] **Step 2: Ensure behavior is exact**

Implementation rules:
- `local` reads `*.yaml` from the configured path, validates against `schema/prompt.schema.json`, and preserves all fields.
- `github` reuses existing CSV/MD/TXT/YAML/JSON scraping behavior and writes normalized prompt YAML to `scraped/<source-slug>/`.
- `json_url` fetches either a JSON list or object with `prompts` list.
- Every emitted prompt has `source`.
- Missing scraped metadata defaults to `description: "Imported from <source>"`, `tags: ["imported"]`, `category: "general"` is invalid, so use `category: "analysis"`, and `author` from source or source name.
- Deduplication is first source wins.

- [ ] **Step 3: Run builder**

Run: `python scripts/build.py`

Expected: command exits 0 and writes `dist/prompts.json`, `dist/prompts.csv`, `dist/sources.json`, `dist/index.json`.

## Task 3: Update legacy files

**Files:**
- Modify: `Makefile`
- Delete: `awesome_prompts.json`
- Delete: `scripts/scrape.py`

- [ ] **Step 1: Update Makefile targets**

Use:

```makefile
.PHONY: validate build ci clean install update-readme all

install:
	pip install -r requirements.txt

validate:
	python scripts/validate.py

build:
	python scripts/build.py

update-readme:
	python scripts/update_readme.py

ci: validate build

all: validate build update-readme

clean:
	rm -rf dist/ scraped/
```

- [ ] **Step 2: Remove legacy config and scraper**

Run: `rm awesome_prompts.json scripts/scrape.py`

Expected: files are deleted.

## Task 4: Update docs/readme

**Files:**
- Modify: `README.md`
- Modify: `scripts/update_readme.py` if it references old source/config details

- [ ] **Step 1: Replace README sections that describe `awesome_prompts.json`**

Document:
- `config.yaml` is the entry point.
- Supported source types: `local`, `github`, `json_url`.
- `make build` reads all sources and writes unified dist artifacts.

- [ ] **Step 2: Search for legacy references**

Run: `grep -R "awesome_prompts.json\|scripts/scrape.py\|make scrape" -n README.md scripts Makefile .github 2>/dev/null || true`

Expected: no stale references except historical notes if intentionally retained.

## Task 5: Verification

**Files:**
- Generated: `dist/*.json`, `dist/*.csv`, `scraped/**`

- [ ] **Step 1: Validate local prompts**

Run: `python scripts/validate.py`

Expected: exits 0.

- [ ] **Step 2: Build unified collection**

Run: `python scripts/build.py`

Expected: exits 0, reports all configured source counts.

- [ ] **Step 3: Inspect generated index shape**

Run: `python - <<'PY'\nimport json\nfrom pathlib import Path\nidx=json.loads(Path('dist/index.json').read_text())\nprompts=json.loads(Path('dist/prompts.json').read_text())\nprint(idx['prompts']['count'])\nprint(prompts['count'])\nprint(prompts['prompts'][0]['source'])\nPY`

Expected: two matching positive counts and a non-empty source name.

- [ ] **Step 4: Run Makefile CI target**

Run: `make ci`

Expected: exits 0.

## Self-Review

- Spec coverage: config migration, local/GitHub/json_url source types, unified dist artifacts, dedupe, cleanup, and docs are each covered by a task.
- Placeholder scan: no TBD/TODO placeholders remain.
- Type consistency: source type names and function names are consistent across tasks.
