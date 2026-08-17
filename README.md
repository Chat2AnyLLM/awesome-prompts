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
| Unified prompts (in `dist/prompts.json`) | 2574 |
| Direct prompts (from `prompts/`) | 3 |
| Configured sources | 4 |
| Scraped prompts cached in `scraped/` | 2579 |

### Configured Sources

| Source | Type | Location | Format | Loaded |
|--------|------|----------|--------|--------|
| Local Prompts | local | `prompts/` | - | 3 |
| Prompts Chat | github | [https://github.com/f/prompts.chat](https://github.com/f/prompts.chat) | csv | 2090 |
| Leaked System Prompts | github | [https://github.com/jujumilk3/leaked-system-prompts](https://github.com/jujumilk3/leaked-system-prompts) | md | 145 |
| AI Boost Awesome Prompts | github | [https://github.com/ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) | txt | 344 |

### Scraped Prompts

<details>
<summary><strong>Ai Boost Awesome Prompts</strong> (344 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | 3D Generative Artist | Role You are a world-class 3D Generative Artist and Technic… |
| 2 | 5W3H Intent Architect | You are a 5W3H Structured Intent Architect. Your job is to … |
| 3 | A2A Agent Protocol Architect | A2A Agent Protocol Architect Sources: A2A Protocol specific… |
| 4 | A2Ui Agent To User Interface Architect | A2UI Agent-to-User Interface Architect Sources: A2UI Protoc… |
| 5 | Abstract Chain Of Thought Architect | Abstract Chain-of-Thought Architect Sources: "Thinking With… |
| 6 | Academic Paper Architect | # Academic Paper Architect — Full-Spectrum Manuscript Orche… |
| 7 | Academic Peer Reviewer | Role You are a Distinguished Academic Peer Reviewer with 20… |
| 8 | Accessibility Auditor | # Accessibility Auditor # Source: msitarzewski/agency-agent… |
| 9 | Adaptive Learning Designer | Role You are a Senior Adaptive Learning Designer with 15+ y… |
| 10 | Adk Skilltoolset Designer | ADK SkillToolset Designer Sources: Google Developer's Guide… |
| 11 | Ag Ui Frontend Architect | AG-UI Frontend Integration Architect Sources: AG-UI Protoco… |
| 12 | Agent Atlas Trajectory Auditor | AgentAtlas Trajectory Auditor Source: "AgentAtlas: Beyond O… |
| 13 | Agent Context Efficiency Engineer | Agent Context Efficiency Engineer Source: mksglu/context-mo… |
| 14 | Agent Cost Observability Architect | Agent Cost Observability Architect Source: getagentseal/cod… |
| 15 | Agent Data Injection Attack Auditor | Agent Data Injection Attack Auditor Source: "Agent Data Inj… |
| 16 | Agent Environment Engineering Architect | Agent Environment Engineering Architect Sources: "EurekAgen… |
| 17 | Agent Eval Designer | Agent Eval Designer Sources: Anthropic Demystifying Evals f… |
| 18 | Agent First Language Architect | Agent-First Language Architect Source: vercel-labs/zerolang… |
| 19 | Agent Governance Orchestrator | Agent Governance Orchestrator Sources: The Orchestration of… |
| 20 | Agent Harness Designer | Agent Harness Designer Sources: OpenAI Harness Engineering … |
| 21 | Agent Harness Performance Engineer | Agent Harness Performance Engineer Source: affaan-m/everyth… |
| 22 | Agent Memory Architect | Agent Memory Architect Sources: AgeMem: Unified Long- and S… |
| 23 | Agent Permission Auto Mode Architect | Agent Permission Auto-Mode Architect Sources: Anthropic — C… |
| 24 | Agent Powered Vulnerability Scanner Arc… | Agent-Powered Vulnerability Scanner Architect Sources: verc… |
| 25 | Agent Protocol Advisor | Agent Protocol Advisor Sources: Google Developer's Guide to… |
| 26 | Agent Red Team Architect | Agent Red Team Architect Sources: The Promptware Kill Chain… |
| 27 | Agent Reliability Engineer | Agent Reliability Engineer Sources: Towards a Science of AI… |
| 28 | Agent Safety Testing At Scale Architect | Agent Safety Testing at Scale Architect Source: "Safety Tes… |
| 29 | Agent Skill Compositional Risk Auditor | Agent Skill Compositional Risk Auditor Sources: When Safe S… |
| 30 | Agent Skill Designer | Agent Skill Designer Sources: Anthropic Agent Skills Docs (… |
| … | *+314 more* | See `scraped/ai-boost-awesome-prompts/` |

</details>

<details>
<summary><strong>Leaked System Prompts</strong> (145 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | Anthropic Claude 2.0 20240306 | # anthropic-claude_2.0_20240306  source: <https://twitter.c… |
| 2 | Anthropic Claude 2.1 20240306 | # anthropic-claude_2.1_20240306  source: <https://twitter.c… |
| 3 | Anthropic Claude 4.1 20250806 | # anthropic-claude-4.1_20250806  source: <https://github.co… |
| 4 | Anthropic Claude Design 20260417 | # anthropic-claude-design_20260417  source: <https://github… |
| 5 | Anthropic Claude Opus 20240306 | # anthropic-claude-opus_20240306  source: <https://twitter.… |
| 6 | Anthropic Claude Opus 3 20240712 | # anthropic-claude-opus-3_20240712  source: <https://docs.a… |
| 7 | Anthropic Claude Opus 4 20250522 | # anthropic-claude-opus-4_20250522  source: <https://docs.a… |
| 8 | Anthropic Claude Opus 4 20250731 | # anthropic-claude-opus-4_20250731  source: <https://docs.a… |
| 9 | Anthropic Claude Opus 4.5 20251124 | # anthropic-claude-opus-4.5_20251124  source: <https://plat… |
| 10 | Anthropic Claude Opus 4.5 Full 20251124 | # anthropic-claude-opus-4.5-full_20251124  source: <https:/… |
| 11 | Anthropic Claude Opus 4.7 20260416 | # anthropic-claude-opus-4.7_20260416  source: <https://gith… |
| 12 | Anthropic Claude Sonnet 3 20240306 | # anthropic-claude-sonnet-3_20240306  source: <https://twit… |
| 13 | Anthropic Claude Sonnet 3 20240311 | # anthropic-claude-sonnet-3_20240311  source: <https://gith… |
| 14 | Anthropic Claude Sonnet 3.5 20240712 | # anthropic-claude-sonnet-3.5_20240712  source: <https://do… |
| 15 | Anthropic Claude Sonnet 3.5 20240909 | # anthropic-claude-sonnet-3.5_20240909  source: <https://do… |
| 16 | Anthropic Claude Sonnet 3.5 20241122 | # anthropic-claude-sonnet-3.5_20241122  source: <https://do… |
| 17 | Anthropic Claude Sonnet 3.7 20250224 | # anthropic-claude-sonnet-3.7_20250224  source: <https://x.… |
| 18 | Anthropic Claude Sonnet 3.7 20250516 | # anthropic-claude-sonnet-3.7_20250516  source: <https://gi… |
| 19 | Anthropic Claude Sonnet 4 20250731 | # anthropic-claude-sonnet-4_20250731  source: <https://plat… |
| 20 | Anthropic Claude Sonnet 4 20250805 | # anthropic-claude-sonnet-4_20250805  source: <https://plat… |
| 21 | Anthropic Claude Sonnet 4.5 20250929 | # anthropic-claude-sonnet-4.5_20250929  source: <https://pl… |
| 22 | Anthropic Claude Sonnet 4.5 20251119 | # anthropic-claude-sonnet-4.5_20251119  source: <https://pl… |
| 23 | Anthropic Claude Sonnet 4.5 20260128 | # anthropic-claude-sonnet-4.5_20260128  ## Q (User)  wrap t… |
| 24 | Anthropic Claude User Styles 20250420 | # anthropic-claude-user-styles_20250420  source: <https://g… |
| 25 | Bolt.New 20241009 | # bolt.new_20241009  source: <https://github.com/stackblitz… |
| 26 | Bolt.New 20250425 | # bolt.new_20250425  source: <https://github.com/elder-plin… |
| 27 | Canva Code 20250519 | # canva-code_20250519  ## Q(user)  make a simple plain html… |
| 28 | Claude Artifacts 20240620 | # claude-artifacts_20240620  source : <https://x.com/elder_… |
| 29 | Claude Code Output Style Explanatory 20… | # claude-code-output-style-explanatory_20251007  source: Ex… |
| 30 | Claude Code Output Style Learning 20251… | # claude-code-output-style-learning_20251007  source: Extra… |
| … | *+115 more* | See `scraped/leaked-system-prompts/` |

</details>

<details>
<summary><strong>Prompts Chat</strong> (2090 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | 12-Month AI and Computer Vision Roadmap… | {   "role": "AI and Computer Vision Specialist Coach",   "c… |
| 2 | 1337 | "Create a detailed efficiency guide for ${game_name}.  The … |
| 3 | 1950s Diner Photo Transformation | {   "prompt": "You will perform an image edit using the per… |
| 4 | 2026 Mobile Poster Creator | Act as a graphic design assistant. Your task is to create a… |
| 5 | 2026 Size Neler getirecek | {   "task": "Photorealistic premium mystical 2026 astrology… |
| 6 | 2046 Puzzle Game Challenge | Act as a game developer. You are tasked with creating a tex… |
| 7 | 21st.dev component prompt | You are given a task to integrate an existing React compone… |
| 8 | 30-Day Skill Mastery Challenge Prompt T… | # 30-Day Skill Mastery Challenge Prompt Template ## Goal St… |
| 9 | 30 tweet Project | Act as a Senior Crypto Narrative Strategist & Rally.fun Alg… |
| 10 | 3D Avatar Prompt | Use a user-uploaded image as the source and convert the per… |
| 11 | 3D Cartoon Animation: Baby Bunny Advent… | Vertical 9:16, 3D cartoon-style animation of a cute baby bu… |
| 12 | 3D Character Render In High-End Disney … | 3D character render in high-end Pixar Disney animation styl… |
| 13 | 3D City Prompt | Hyper-realistic 3D square diorama of ${city_name:Istanbul},… |
| 14 | 3D FACTORY | I NEED THIS FULLY INTEGRATED, IMPLEMENTED, ENFORCED, HARDEN… |
| 15 | 3D FPS Game | Develop a first-person shooter game using Three.js and Java… |
| 16 | 3D Isometric Miniature City View with W… | Present a clear, 45° top-down view of a vertical (9:16) iso… |
| 17 | 3D Isometric Miniature Diorama | "When I give you a movie quote, never reply with text or a … |
| 18 | 3D Kinetic Ball Simulation | I want you to act as an expert front-end game engineer spec… |
| 19 | 3D Mechanical Part Image to Technical D… | {   "task": "image_to_image",   "input_image": "3d_render_o… |
| 20 | 3D Medical Anatomy Model Render Prompt | {   "fixed_prompt_components": {     "composition": "Wide a… |
| 21 | 3D Physics Sandbox Architect | I want you to act as a Senior WebGL Game Architect speciali… |
| 22 | 3D Racing Game | Create an exciting 3D racing game using Three.js and JavaSc… |
| 23 | 3D Space Explorer | Build an immersive 3D space exploration game using Three.js… |
| 24 | 3D to 2D Floor Plan Converter | {   "task": "image_to_image",   "description": "Convert a f… |
| 25 | 3x3 Grid Storyboarding from Photo | Act as a storyboard artist. You are skilled in visual story… |
| 26 | 4 Optimized Versions of A Prompt (in Ar… | Act as a certified and expert AI prompt engineer  Analyze a… |
| 27 | $500/Hour AI Consultant Prompt | You are Lyra, a master-level Al prompt optimization special… |
| 28 | 5x2 Reverse Construction Process - Vill… | Act as an architectural visualization expert specialized in… |
| 29 | 6-Panel Storyboard Mastery | Act as a storyboard artist. You are skilled in creating pre… |
| 30 | 7v7 Football Team Generator App | Act as an Application Designer. You are tasked with creatin… |
| … | *+2060 more* | See `scraped/prompts-chat/` |

</details>
## License

MIT
