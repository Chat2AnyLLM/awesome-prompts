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
