# Contributing

There are two ways to contribute prompts to this collection:

## Option 1: Add a Prompt Directly

Best for: prompts you wrote or have permission to include in full.

1. Create `prompts/<slug>.yaml` (lowercase, hyphens only):

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

2. Validate and build:

```bash
pip install -r requirements.txt
make ci
```

3. Commit all changes (including `dist/`) and open a PR.

### Prompt Schema Rules

- `slug` must match the filename (without `.yaml`)
- `slug` format: `^[a-z0-9]+(-[a-z0-9]+)*$`
- `category` must be one of: `developer-tools`, `writing`, `education`, `creative`, `business`, `language`, `lifestyle`, `analysis`
- `tags` must have at least one entry, no duplicates
- `prompt` must be at least 10 characters

### Template Variables

If your prompt uses template variables (like `${Position}`), declare them:

```yaml
variables:
  - name: Position
    default: Software Developer
```

---

## Option 2: Link an External Source

Best for: pointing to a GitHub repo or file that contains prompts (YAML, Markdown, CSV, JSON).

1. Create `sources/<slug>.yaml`:

```yaml
slug: my-source-name
title: My Source Name
description: A one-line summary of what this source contains.
url: https://github.com/username/repo-with-prompts
format: yaml
type: collection
tags:
  - relevant
  - tags
category: developer-tools
author: your-github-username
notes: |
  Optional notes about how the prompts are organized in this repo,
  which files to look at, or how a consumer should use them.
```

2. Validate and build:

```bash
make ci
```

3. Commit and open a PR.

### Source Schema Rules

- `slug` must match the filename (without `.yaml`)
- `url` must be a GitHub URL (`https://github.com/...`)
- `format`: what format the prompt files are in — `yaml`, `md`, `csv`, `json`, or `mixed`
- `type`: `single-prompt` (link to one prompt file) or `collection` (link to a repo with many)
- `notes` is optional but encouraged — helps consumers know how to parse the source

### What Makes a Good Source Link

- The linked repo should contain actual prompt content (not just a README listing)
- Prompts should be in a parseable format (YAML, Markdown, CSV, or JSON)
- The repo should be actively maintained or at least stable
- Include `notes` explaining the file structure so a consumer tool can fetch and parse it

---

## Guidelines

- Write clear, specific prompts that produce consistent results
- Include context about expected behavior in the prompt itself
- One prompt per file (for direct prompts)
- Test your prompt with an AI assistant before submitting
- For external sources, verify the link works and the repo is accessible
