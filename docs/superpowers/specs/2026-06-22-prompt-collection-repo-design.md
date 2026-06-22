# Prompt Collection Repository Design

## Purpose

A curated repository of high-quality prompts stored in a simple, machine-readable format so that another tool (CLI, MCP server, or agent) can fetch and serve them programmatically.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary format | **JSON** (`prompts.json`) | Structured, typed, zero-parsing ambiguity for consumers; CSV provided as secondary export |
| Secondary format | **CSV** (`prompts.csv`) | Human-friendly, easy to edit in spreadsheets, compatible with the `f/awesome-chatgpt-prompts` ecosystem |
| Source of truth | Individual **YAML files** in `prompts/` | Easy to edit, review in PRs, merge without conflicts; JSON/CSV are generated artifacts |
| Schema | **JSON Schema** (`schema/prompt.schema.json`) | Validates contributions, documents the contract for consumers |
| Generation | **Makefile + script** | `make build` compiles YAML sources into `prompts.json` and `prompts.csv` |

## Repository Structure

```
awesome-prompts/
├── README.md
├── LICENSE                      # MIT
├── Makefile
├── schema/
│   └── prompt.schema.json       # JSON Schema for a single prompt
├── prompts/                     # Source of truth — one YAML file per prompt
│   ├── linux-terminal.yaml
│   ├── english-translator.yaml
│   └── ...
├── dist/                        # Generated artifacts (gitignored OR committed for easy consumption)
│   ├── prompts.json             # Array of all prompts
│   └── prompts.csv              # Flat CSV export
├── scripts/
│   ├── build.py                 # Compiles YAML → JSON + CSV
│   └── validate.py              # Validates all YAML against schema
├── .github/
│   └── workflows/
│       └── ci.yml               # Validates + builds on every PR
└── CONTRIBUTING.md
```

## Prompt Schema

Each prompt YAML file (`prompts/<slug>.yaml`):

```yaml
# prompts/linux-terminal.yaml
slug: linux-terminal
title: Linux Terminal
description: Simulates a Linux terminal, responding only with terminal output.
prompt: |
  I want you to act as a linux terminal. I will type commands and you will
  reply with what the terminal should show. I want you to only reply with
  the terminal output inside one unique code block, and nothing else...
tags:
  - developer
  - terminal
  - simulation
category: developer-tools
author: f
variables: []                    # Optional template variables like ${Position}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slug` | string | yes | URL-safe identifier, matches filename |
| `title` | string | yes | Human-readable name |
| `description` | string | yes | One-line summary of what the prompt does |
| `prompt` | string | yes | The full prompt text |
| `tags` | string[] | yes | Categorization tags |
| `category` | string | yes | Primary category (enum: see below) |
| `author` | string | yes | Contributor handle |
| `variables` | object[] | no | Template variables with name + default |

### Categories (enum)

- `developer-tools`
- `writing`
- `education`
- `creative`
- `business`
- `language`
- `lifestyle`
- `analysis`

## Generated `prompts.json` Format

```json
{
  "version": "1.0.0",
  "generated_at": "2026-06-22T10:00:00Z",
  "count": 42,
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

## Consumer Contract

A consuming tool can:

1. **Fetch raw JSON from GitHub:**
   ```
   https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/prompts.json
   ```
2. **Clone and read locally** — the `dist/` folder is always up to date on `main`.
3. **Use the schema** to validate its own prompt additions before submitting a PR.

## Build Pipeline

```makefile
build:
	python scripts/build.py

validate:
	python scripts/validate.py

ci: validate build
```

- `scripts/build.py`: reads all `prompts/*.yaml`, validates against schema, outputs `dist/prompts.json` and `dist/prompts.csv`.
- `scripts/validate.py`: runs JSON Schema validation on each YAML file; exits non-zero on failure.
- CI runs `make ci` on every PR; `dist/` is committed so consumers always have fresh artifacts on `main`.

## CI Workflow

On PR:
1. Validate all YAML files against schema
2. Build `dist/prompts.json` and `dist/prompts.csv`
3. Fail if generated files differ from committed (ensures contributors ran `make build`)

## Contribution Flow

1. Author creates `prompts/<slug>.yaml`
2. Runs `make validate` locally
3. Runs `make build` to regenerate `dist/`
4. Opens PR — CI verifies

## Non-Goals

- No web UI (that's the consumer's job)
- No API server in this repo
- No prompt versioning (prompts are immutable once merged; edits are new commits)
- No rating/voting system
