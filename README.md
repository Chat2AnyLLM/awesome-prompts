# Awesome Prompts

A curated collection of high-quality prompts for AI assistants, stored in a machine-readable format for programmatic consumption.

## Two Ways to Contribute

| Method | What you do | Where it lives |
|--------|------------|----------------|
| **Add a prompt directly** | Write a YAML file with the full prompt text | `prompts/<slug>.yaml` |
| **Link an external source** | Point to a GitHub repo/file containing prompts | `sources/<slug>.yaml` |

## For Consumers

**Entry point** — fetch `dist/index.json` to discover all available data:

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/index.json
```

**Direct prompts:**

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/prompts.json
```

**External sources (links to other repos):**

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/sources.json
```

A CSV export of direct prompts is also available at `dist/prompts.csv`.

### prompts.json Format

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

### sources.json Format

```json
{
  "version": "1.0.0",
  "generated_at": "2026-06-22T10:00:00Z",
  "count": 2,
  "sources": [
    {
      "slug": "awesome-chatgpt-prompts",
      "title": "Awesome ChatGPT Prompts",
      "description": "A large collection of curated ChatGPT prompts...",
      "url": "https://github.com/f/awesome-chatgpt-prompts",
      "format": "csv",
      "type": "collection",
      "tags": ["general", "chatgpt", "roles"],
      "category": "creative",
      "author": "f"
    }
  ]
}
```

## For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on both contribution methods.

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

## Development

```bash
pip install -r requirements.txt
make validate   # Check all prompts and sources against schemas
make build      # Generate dist/ artifacts
make ci         # Run both
```

## License

MIT
