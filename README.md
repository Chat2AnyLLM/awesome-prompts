# Awesome Prompts

A curated collection of high-quality prompts for AI assistants, stored in a machine-readable format for programmatic consumption. The collection is built from sources configured in `config.yaml`, including local YAML prompts, external GitHub repositories, and remote JSON prompt collections.

## Two Ways to Contribute

| Method | What you do | Where it lives |
|--------|------------|----------------|
| **Add a prompt directly** | Write a YAML file with the full prompt text | `prompts/<slug>.yaml` |
| **Add a source** | Add a `local`, `github`, or `json_url` source | `config.yaml` |

## How It Works

```
config.yaml
  (local, GitHub, JSON URL sources)
        │
        ▼
  scripts/build.py
        │
        ├─ reads prompts/*.yaml
        ├─ fetches configured GitHub sources
        ├─ fetches configured JSON URL sources
        └─ caches fetched GitHub prompts in scraped/<source>/
        │
        ▼
  dist/prompts.json   (unified prompt collection)
  dist/prompts.csv
  dist/sources.json
  dist/index.json
```

A GitHub Actions workflow runs **every hour** to:
1. Read `config.yaml` for configured sources
2. Load local prompts and fetch remote sources (supports CSV, YAML, Markdown, TXT, and JSON)
3. Cache fetched GitHub prompts in `scraped/<source-name>/`
4. Build unified `dist/` artifacts
5. Update this README with latest stats
6. Commit and push if anything changed

## For Consumers

**Entry point** — fetch `dist/index.json` to discover all available data:

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/index.json
```

**Unified prompts:**

```bash
curl -s https://raw.githubusercontent.com/zhujian0805/awesome-prompts/main/dist/prompts.json
```

**Scraped prompts** — stored per-source under `scraped/`:

```bash
# List what's been scraped
ls scraped/
# awesome-chatgpt-prompts/  leaked-system-prompts/
```

## Configuring Sources (`config.yaml`)

To add a new source, edit `config.yaml`:

```yaml
sources:
  - name: "Local Prompts"
    type: local
    path: prompts/
    description: "Hand-curated prompts maintained in this repo"

  - name: "My GitHub Prompt Collection"
    type: github
    url: https://github.com/username/repo
    format: yaml
    file_path: prompts/
    description: "Prompt YAML files from a GitHub repo"

  - name: "My JSON Prompt Collection"
    type: json_url
    url: https://raw.githubusercontent.com/username/repo/main/dist/prompts.json
    description: "Pre-built JSON prompt collection"
```

### Source Types

| Type | Required fields | Description |
|------|-----------------|-------------|
| `local` | `name`, `type`, `path` | Reads local `*.yaml` prompt files and validates them against `schema/prompt.schema.json` |
| `github` | `name`, `type`, `url`, `format` | Fetches prompts from a GitHub repo. Optional `file_path` points to a file or directory inside the repo |
| `json_url` | `name`, `type`, `url` | Fetches a pre-built JSON prompt collection from any URL |

### GitHub Supported Formats

| Format | How it's scraped |
|--------|-----------------|
| `csv` | Reads the CSV file, looks for `act`/`title` + `prompt` columns |
| `yaml` | Reads `.yaml`/`.yml` files, expects a `prompt` field in each |
| `md` | Each `.md` file is treated as a complete prompt |
| `txt` | Each `.txt` file is treated as a complete prompt |
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
make validate      # Check local prompts and source metadata against schemas
make test          # Run unit tests
make build         # Load all config.yaml sources and generate unified dist/ artifacts
make update-readme # Update README stats
make all           # Run validation, tests, build, and README update
```

## Stats

| Metric | Count |
|--------|-------|
| Unified prompts (in `dist/prompts.json`) | 1906 |
| Direct prompts (from `prompts/`) | 3 |
| Configured sources | 4 |
| Scraped prompts cached in `scraped/` | 1905 |

### Configured Sources

| Source | Type | Location | Format | Loaded |
|--------|------|----------|--------|--------|
| Local Prompts | local | `prompts/` | - | 3 |
| Prompts Chat | github | [https://github.com/f/prompts.chat](https://github.com/f/prompts.chat) | csv | 1905 |
| Leaked System Prompts | github | [https://github.com/jujumilk3/leaked-system-prompts](https://github.com/jujumilk3/leaked-system-prompts) | md | 0 |
| AI Boost Awesome Prompts | github | [https://github.com/ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) | txt | 0 |

### Scraped Prompts

<details>
<summary><strong>Prompts Chat</strong> (1905 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | 12-Month AI and Computer Vision Roadmap… | {   "role": "AI and Computer Vision Specialist Coach",   "c… |
| 2 | 1950s Diner Photo Transformation | {   "prompt": "You will perform an image edit using the per… |
| 3 | 2026 Mobile Poster Creator | Act as a graphic design assistant. Your task is to create a… |
| 4 | 2026 Size Neler getirecek | {   "task": "Photorealistic premium mystical 2026 astrology… |
| 5 | 2046 Puzzle Game Challenge | Act as a game developer. You are tasked with creating a tex… |
| 6 | 21st.dev component prompt | You are given a task to integrate an existing React compone… |
| 7 | 30-Day Skill Mastery Challenge Prompt T… | # 30-Day Skill Mastery Challenge Prompt Template ## Goal St… |
| 8 | 30 tweet Project | Act as a Senior Crypto Narrative Strategist & Rally.fun Alg… |
| 9 | 3D Avatar Prompt | Use a user-uploaded image as the source and convert the per… |
| 10 | 3D Cartoon Animation: Baby Bunny Advent… | Vertical 9:16, 3D cartoon-style animation of a cute baby bu… |
| 11 | 3D Character Render In High-End Disney … | 3D character render in high-end Pixar Disney animation styl… |
| 12 | 3D City Prompt | Hyper-realistic 3D square diorama of ${city_name:Istanbul},… |
| 13 | 3D FACTORY | I NEED THIS FULLY INTEGRATED, IMPLEMENTED, ENFORCED, HARDEN… |
| 14 | 3D FPS Game | Develop a first-person shooter game using Three.js and Java… |
| 15 | 3D Isometric Miniature City View with W… | Present a clear, 45° top-down view of a vertical (9:16) iso… |
| 16 | 3D Isometric Miniature Diorama | "When I give you a movie quote, never reply with text or a … |
| 17 | 3D Kinetic Ball Simulation | I want you to act as an expert front-end game engineer spec… |
| 18 | 3D Mechanical Part Image to Technical D… | {   "task": "image_to_image",   "input_image": "3d_render_o… |
| 19 | 3D Medical Anatomy Model Render Prompt | {   "fixed_prompt_components": {     "composition": "Wide a… |
| 20 | 3D Physics Sandbox Architect | I want you to act as a Senior WebGL Game Architect speciali… |
| 21 | 3D Racing Game | Create an exciting 3D racing game using Three.js and JavaSc… |
| 22 | 3D Space Explorer | Build an immersive 3D space exploration game using Three.js… |
| 23 | 3D to 2D Floor Plan Converter | {   "task": "image_to_image",   "description": "Convert a f… |
| 24 | 3x3 Grid Storyboarding from Photo | Act as a storyboard artist. You are skilled in visual story… |
| 25 | 4 Optimized Versions of A Prompt (in Ar… | Act as a certified and expert AI prompt engineer  Analyze a… |
| 26 | $500/Hour AI Consultant Prompt | You are Lyra, a master-level Al prompt optimization special… |
| 27 | 5x2 Reverse Construction Process - Vill… | Act as an architectural visualization expert specialized in… |
| 28 | 6-Panel Storyboard Mastery | Act as a storyboard artist. You are skilled in creating pre… |
| 29 | 7v7 Football Team Generator App | Act as an Application Designer. You are tasked with creatin… |
| 30 | A blonde woman in a dreamy | A blonde woman in a dreamy, ethereal photographic scene wit… |
| … | *+1875 more* | See `scraped/prompts-chat/` |

</details>
## License

MIT
