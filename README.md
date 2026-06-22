# Awesome Prompts

A curated collection of high-quality prompts for AI assistants, stored in a machine-readable format for programmatic consumption. Includes an automated scraper that fetches prompts from configured external sources hourly.

## Two Ways to Contribute

| Method | What you do | Where it lives |
|--------|------------|----------------|
| **Add a prompt directly** | Write a YAML file with the full prompt text | `prompts/<slug>.yaml` |
| **Add a source link** | Add a GitHub link to `awesome_prompts.json` | `awesome_prompts.json` |

## How It Works

```
awesome_prompts.json          prompts/*.yaml
  (configured links)           (direct prompts)
        │                            │
        ▼                            ▼
  scripts/scrape.py           scripts/build.py
        │                            │
        ▼                            ▼
  scraped/<source>/            dist/prompts.json
   (fetched prompts)           dist/prompts.csv
                               dist/sources.json
                               dist/index.json
```

A GitHub Actions workflow runs **every hour** to:
1. Read `awesome_prompts.json` for configured source links
2. Scrape prompts from each source (supports CSV, YAML, Markdown, JSON)
3. Save scraped prompts to `scraped/<source-name>/`
4. Rebuild `dist/` artifacts
5. Update this README with latest stats
6. Commit and push if anything changed

## For Consumers

**Entry point** — fetch `dist/index.json` to discover all available data:

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/index.json
```

**Direct prompts:**

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/prompts.json
```

**Scraped prompts** — stored per-source under `scraped/`:

```bash
# List what's been scraped
ls scraped/
# awesome-chatgpt-prompts/  leaked-system-prompts/
```

## Configuring Sources (`awesome_prompts.json`)

To add a new source to scrape from, edit `awesome_prompts.json`:

```json
{
  "sources": [
    {
      "name": "My Prompt Collection",
      "url": "https://github.com/username/repo",
      "type": "collection",
      "format": "yaml",
      "file_path": "prompts/",
      "description": "What this source contains"
    }
  ]
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Human-readable name for this source |
| `url` | yes | GitHub URL (repo or specific file) |
| `type` | yes | `collection` (repo with many prompts) or `single-prompt` |
| `format` | yes | Format of prompt files: `csv`, `yaml`, `md`, `json` |
| `file_path` | no | Path within the repo (e.g. `prompts.csv`, `prompts/`). Empty = repo root |
| `description` | no | What this source contains |

### Supported Formats

| Format | How it's scraped |
|--------|-----------------|
| `csv` | Reads the CSV file, looks for `act`/`title` + `prompt` columns |
| `yaml` | Reads `.yaml`/`.yml` files, expects a `prompt` field in each |
| `md` | Each `.md` file is treated as a complete prompt |
| `json` | Reads JSON array or `{"prompts": [...]}`, expects `title` + `prompt` fields |

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
make validate      # Check all prompts and sources against schemas
make build         # Generate dist/ artifacts
make scrape        # Fetch prompts from configured sources
make update-readme # Update README stats
make all           # Run everything
```

## Stats

| Metric | Count |
|--------|-------|
| Direct prompts (in `prompts/`) | 3 |
| Configured sources | 4 |
| Scraped prompts (total) | 100 |

### Configured Sources

| Source | URL | Format | Scraped |
|--------|-----|--------|---------|
| Awesome ChatGPT Prompts | [https://github.com/f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | csv | 0 |
| Leaked System Prompts | [https://github.com/jujumilk3/leaked-system-prompts](https://github.com/jujumilk3/leaked-system-prompts) | md | 100 |
| Prompts Chat | [https://github.com/f/prompts.chat](https://github.com/f/prompts.chat) | csv | 0 |
| AI Boost Awesome Prompts | [https://github.com/ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) | md | 0 |
## License

MIT
