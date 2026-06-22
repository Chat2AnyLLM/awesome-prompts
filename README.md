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

## Development

```bash
pip install -r requirements.txt
make validate   # Check all prompts against schema
make build      # Generate dist/prompts.json and dist/prompts.csv
make ci         # Run both
```

## License

MIT
