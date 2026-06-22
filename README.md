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
| Configured sources | 3 |
| Scraped prompts (total) | 2332 |

### Configured Sources

| Source | URL | Format | Scraped |
|--------|-----|--------|---------|
| Prompts Chat | [https://github.com/f/prompts.chat](https://github.com/f/prompts.chat) | csv | 1873 |
| Leaked System Prompts | [https://github.com/jujumilk3/leaked-system-prompts](https://github.com/jujumilk3/leaked-system-prompts) | md | 163 |
| AI Boost Awesome Prompts | [https://github.com/ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) | txt | 296 |

### Scraped Prompts

<details>
<summary><strong>Ai Boost Awesome Prompts</strong> (296 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | 3D Generative Artist | Role You are a world-class 3D Generative Artist and Technic… |
| 2 | A2A Agent Protocol Architect | A2A Agent Protocol Architect Sources: A2A Protocol specific… |
| 3 | A2Ui Agent To User Interface Architect | A2UI Agent-to-User Interface Architect Sources: A2UI Protoc… |
| 4 | Academic Paper Architect | # Academic Paper Architect — Full-Spectrum Manuscript Orche… |
| 5 | Academic Peer Reviewer | Role You are a Distinguished Academic Peer Reviewer with 20… |
| 6 | Accessibility Auditor | # Accessibility Auditor # Source: msitarzewski/agency-agent… |
| 7 | Adaptive Learning Designer | Role You are a Senior Adaptive Learning Designer with 15+ y… |
| 8 | Adhd Parallel Ideation Skill | --- name: adhd description: Parallel divergent ideation for… |
| 9 | Adk Skilltoolset Designer | ADK SkillToolset Designer Sources: Google Developer's Guide… |
| 10 | Ag Ui Frontend Architect | AG-UI Frontend Integration Architect Sources: AG-UI Protoco… |
| 11 | Agent Context Efficiency Engineer | Agent Context Efficiency Engineer Source: mksglu/context-mo… |
| 12 | Agent Cooperation Designer | Agent Cooperation Designer Sources: Competition and Coopera… |
| 13 | Agent Cost Observability Architect | Agent Cost Observability Architect Source: getagentseal/cod… |
| 14 | Agent Eval Designer | Agent Eval Designer Sources: Anthropic Demystifying Evals f… |
| 15 | Agent First Language Architect | Agent-First Language Architect Source: vercel-labs/zerolang… |
| 16 | Agent Governance Orchestrator | Agent Governance Orchestrator Sources: The Orchestration of… |
| 17 | Agent Harness Designer | Agent Harness Designer Sources: OpenAI Harness Engineering … |
| 18 | Agent Harness Performance Engineer | Agent Harness Performance Engineer Source: affaan-m/everyth… |
| 19 | Agent Memory Architect | Agent Memory Architect Sources: AgeMem: Unified Long- and S… |
| 20 | Agent Permission Auto Mode Architect | Agent Permission Auto-Mode Architect Sources: Anthropic — C… |
| 21 | Agent Powered Vulnerability Scanner Arc… | Agent-Powered Vulnerability Scanner Architect Sources: verc… |
| 22 | Agent Protocol Advisor | Agent Protocol Advisor Sources: Google Developer's Guide to… |
| 23 | Agent Red Team Architect | Agent Red Team Architect Sources: The Promptware Kill Chain… |
| 24 | Agent Reliability Engineer | Agent Reliability Engineer Sources: Towards a Science of AI… |
| 25 | Agent Skill Designer | Agent Skill Designer Sources: Anthropic Agent Skills Docs (… |
| 26 | Agent Skill Optimizer Architect | Agent Skill Optimizer Architect Source: microsoft/SkillOpt … |
| 27 | Agent Skill Supply Chain Auditor | Agent Skill Supply-Chain Security Auditor Sources: Supply-C… |
| 28 | Agent State Hygiene Architect | Agent State Hygiene Architect Source: vibeforge1111/keep-co… |
| 29 | Agent Style Enforcer | Agent Style Enforcer — Literature-Backed Technical-Prose Ru… |
| 30 | Agent Tool Engineer | Agent Tool Engineer Sources: Anthropic — Writing effective … |
| … | *+266 more* | See `scraped/ai-boost-awesome-prompts/` |

</details>

<details>
<summary><strong>Leaked System Prompts</strong> (163 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | Anthropic Claude 2.0 20240306 | # anthropic-claude_2.0_20240306  source: <https://twitter.c… |
| 2 | Anthropic Claude 2.1 20240306 | # anthropic-claude_2.1_20240306  source: <https://twitter.c… |
| 3 | Anthropic Claude 4.1 20250806 | # anthropic-claude-4.1_20250806  source: <https://github.co… |
| 4 | Anthropic Claude 4 20250522 | # anthropic-claude-4_20250522  source: <https://github.com/… |
| 5 | Anthropic Claude Api Tool Use 20250119 | # anthropic-claude-api-tool-use_20250119  ## claude-3-5-son… |
| 6 | Anthropic Claude Code 20250304 | # anthropic-claude-code_20250304  source: <https://github.c… |
| 7 | Anthropic Claude Design 20260417 | # anthropic-claude-design_20260417  source: <https://github… |
| 8 | Anthropic Claude Fable 5 20260609 | # anthropic-claude-fable-5_20260609  source: <https://githu… |
| 9 | Anthropic Claude Haiku 3 20240712 | # anthropic-claude-haiku-3_20240712  source: <https://docs.… |
| 10 | Anthropic Claude Haiku 4.5 20251015 | # anthropic-claude-haiku-4.5_20251015  source: <https://pla… |
| 11 | Anthropic Claude Haiku 4.5 20251119 | # anthropic-claude-haiku-4.5_20251119  source: <https://pla… |
| 12 | Anthropic Claude Opus 20240306 | # anthropic-claude-opus_20240306  source: <https://twitter.… |
| 13 | Anthropic Claude Opus 3 20240712 | # anthropic-claude-opus-3_20240712  source: <https://docs.a… |
| 14 | Anthropic Claude Opus 4.1 20250805 | # anthropic-claude-opus-4.1_20250805  source: <https://plat… |
| 15 | Anthropic Claude Opus 4 20250522 | # anthropic-claude-opus-4_20250522  source: <https://docs.a… |
| 16 | Anthropic Claude Opus 4 20250731 | # anthropic-claude-opus-4_20250731  source: <https://docs.a… |
| 17 | Anthropic Claude Opus 4 20250805 | # anthropic-claude-opus-4_20250805  source: <https://platfo… |
| 18 | Anthropic Claude Opus 4.5 20251124 | # anthropic-claude-opus-4.5_20251124  source: <https://plat… |
| 19 | Anthropic Claude Opus 4.5 Full 20251124 | # anthropic-claude-opus-4.5-full_20251124  source: <https:/… |
| 20 | Anthropic Claude Opus 4.6 20260206 | # anthropic-claude-opus-4.6_20260206  source: <https://gith… |
| 21 | Anthropic Claude Opus 4.7 20260416 | # anthropic-claude-opus-4.7_20260416  source: <https://gith… |
| 22 | Anthropic Claude Sonnet 3 20240306 | # anthropic-claude-sonnet-3_20240306  source: <https://twit… |
| 23 | Anthropic Claude Sonnet 3 20240311 | # anthropic-claude-sonnet-3_20240311  source: <https://gith… |
| 24 | Anthropic Claude Sonnet 3.5 20240712 | # anthropic-claude-sonnet-3.5_20240712  source: <https://do… |
| 25 | Anthropic Claude Sonnet 3.5 20240909 | # anthropic-claude-sonnet-3.5_20240909  source: <https://do… |
| 26 | Anthropic Claude Sonnet 3.5 20241022 | # anthropic-claude-sonnet-3.5_20241022  source: <https://do… |
| 27 | Anthropic Claude Sonnet 3.5 20241122 | # anthropic-claude-sonnet-3.5_20241122  source: <https://do… |
| 28 | Anthropic Claude Sonnet 3.7 20250224 | # anthropic-claude-sonnet-3.7_20250224  source: <https://x.… |
| 29 | Anthropic Claude Sonnet 3.7 20250516 | # anthropic-claude-sonnet-3.7_20250516  source: <https://gi… |
| 30 | Anthropic Claude Sonnet 4 20250522 | # anthropic-claude-sonnet-4_20250522  source: <https://docs… |
| … | *+133 more* | See `scraped/leaked-system-prompts/` |

</details>

<details>
<summary><strong>Prompts Chat</strong> (1873 prompts)</summary>

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
| … | *+1843 more* | See `scraped/prompts-chat/` |

</details>
## License

MIT
