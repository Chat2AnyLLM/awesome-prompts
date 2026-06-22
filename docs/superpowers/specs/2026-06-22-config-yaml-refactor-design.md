# Design: Refactor awesome-prompts to use config.yaml

**Date:** 2026-06-22  
**Status:** Approved  
**Scope:** Refactor the existing awesome-prompts repo to replace `awesome_prompts.json` with `config.yaml`, support multi-type sources (local, GitHub, JSON URL), and produce a unified `dist/` output.

## Summary

Replace the current dual-script architecture (`scrape.py` + `build.py` reading from `awesome_prompts.json`) with a single unified `build.py` that reads `config.yaml` and produces merged `dist/` artifacts from all configured sources.

## Source Types

### 1. `local` — Local YAML prompt files
- Reads `prompts/*.yaml` files from the repo
- Validates against `schema/prompt.schema.json`
- These are hand-curated, first-class prompts

### 2. `github` — GitHub repo scraping
- Fetches prompts from external GitHub repos
- Supports formats: `csv`, `md`, `txt`, `yaml`, `json`
- Uses GitHub raw content URLs (same as current `scrape.py`)
- Caches fetched content in `scraped/<source-slug>/`

### 3. `json_url` — Remote JSON endpoint
- Fetches a pre-built prompts JSON file from any URL
- Expects either an array of prompt objects or `{"prompts": [...]}` structure
- Each prompt object must have at minimum `title` and `prompt` fields

## Config Format: `config.yaml`

```yaml
version: "2.0.0"
description: "Aggregates prompts from local files, GitHub repos, and remote JSON endpoints"

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
    description: "Large community-curated collection of ChatGPT prompts"

  - name: "Leaked System Prompts"
    type: github
    url: https://github.com/jujumilk3/leaked-system-prompts
    format: md
    file_path: ""
    description: "System prompts from various AI products"

  - name: "AI Boost Awesome Prompts"
    type: github
    url: https://github.com/ai-boost/awesome-prompts
    format: txt
    file_path: prompts/
    description: "300+ curated role-based prompts as plain text files"
```

## Build Pipeline (Single `build.py`)

```
config.yaml
    │
    ├─ type: local    → read prompts/*.yaml, validate against schema
    ├─ type: github   → fetch from GitHub, parse by format, cache in scraped/
    └─ type: json_url → fetch JSON, extract prompts array
    │
    ▼
  Merge all prompts (deduplicate by slug)
    │
    ▼
  dist/prompts.json   — unified collection with source attribution
  dist/prompts.csv    — flat CSV export
  dist/sources.json   — metadata about configured sources
  dist/index.json     — entry point for consumers
```

## Unified Prompt Schema in dist/prompts.json

Each prompt in the merged output includes a `source` field for attribution:

```json
{
  "slug": "code-reviewer",
  "title": "Code Reviewer",
  "prompt": "...",
  "source": "Local Prompts",
  "tags": ["developer"],
  "category": "developer-tools"
}
```

- Local prompts retain all schema fields (tags, category, author, description, variables).
- Scraped/fetched prompts get minimal fields: `slug`, `title`, `prompt`, `source`.

## Deduplication

- Prompts are keyed by `slug`.
- Sources listed earlier in `config.yaml` take priority (first wins).
- This means local prompts override scraped ones with the same slug.

## Files Changed

| Action | File | Notes |
|--------|------|-------|
| Create | `config.yaml` | Replaces `awesome_prompts.json` |
| Rewrite | `scripts/build.py` | Unified build: reads config, fetches, merges, outputs |
| Delete | `scripts/scrape.py` | Logic folded into `build.py` |
| Keep | `scripts/validate.py` | Still validates local `prompts/*.yaml` |
| Keep | `scripts/update_readme.py` | May need minor update to read config.yaml |
| Delete | `awesome_prompts.json` | Replaced by config.yaml |
| Keep | `prompts/*.yaml` | Unchanged |
| Keep | `sources/*.yaml` | Unchanged (informational metadata) |
| Keep | `schema/` | Unchanged |
| Update | `Makefile` | Simplify targets (remove `scrape`, `build` does everything) |
| Update | `README.md` | Document new config.yaml format |

## Makefile (Updated)

```makefile
.PHONY: validate build ci clean install update-readme

install:
	pip install -r requirements.txt

validate:
	python scripts/validate.py

build:
	python scripts/build.py

update-readme:
	python scripts/update_readme.py

ci: validate build

clean:
	rm -rf dist/ scraped/
```

## Error Handling

- If a remote source fails to fetch, log warning and continue (don't fail the whole build).
- If a local prompt fails validation, fail the build (these are first-class).
- If `config.yaml` is malformed, fail immediately with a clear error.

## Dependencies

No new dependencies beyond what's already in `requirements.txt`:
- `pyyaml` (already used)
- `jsonschema` (already used)

## Testing

- `scripts/validate.py` continues to validate local prompts against schema.
- Add a `--dry-run` flag to `build.py` that parses config and reports what it would fetch without actually fetching (useful for CI validation of config changes).
