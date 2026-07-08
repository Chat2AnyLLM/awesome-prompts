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
| Unified prompts (in `dist/prompts.json`) | 2318 |
| Direct prompts (from `prompts/`) | 3 |
| Configured sources | 4 |
| Scraped prompts cached in `scraped/` | 2320 |

### Configured Sources

| Source | Type | Location | Format | Loaded |
|--------|------|----------|--------|--------|
| Local Prompts | local | `prompts/` | - | 3 |
| Prompts Chat | github | [https://github.com/f/prompts.chat](https://github.com/f/prompts.chat) | csv | 1974 |
| Leaked System Prompts | github | [https://github.com/jujumilk3/leaked-system-prompts](https://github.com/jujumilk3/leaked-system-prompts) | md | 108 |
| AI Boost Awesome Prompts | github | [https://github.com/ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) | txt | 238 |

### Scraped Prompts

<details>
<summary><strong>Ai Boost Awesome Prompts</strong> (238 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | 3D Generative Artist | Role You are a world-class 3D Generative Artist and Technic… |
| 2 | A2A Agent Protocol Architect | A2A Agent Protocol Architect Sources: A2A Protocol specific… |
| 3 | A2Ui Agent To User Interface Architect | A2UI Agent-to-User Interface Architect Sources: A2UI Protoc… |
| 4 | Abstract Chain Of Thought Architect | Abstract Chain-of-Thought Architect Sources: "Thinking With… |
| 5 | Academic Peer Reviewer | Role You are a Distinguished Academic Peer Reviewer with 20… |
| 6 | Adaptive Learning Designer | Role You are a Senior Adaptive Learning Designer with 15+ y… |
| 7 | Adhd Parallel Ideation Skill | --- name: adhd description: Parallel divergent ideation for… |
| 8 | Adk Skilltoolset Designer | ADK SkillToolset Designer Sources: Google Developer's Guide… |
| 9 | Agent Atlas Trajectory Auditor | AgentAtlas Trajectory Auditor Source: "AgentAtlas: Beyond O… |
| 10 | Agent Context Efficiency Engineer | Agent Context Efficiency Engineer Source: mksglu/context-mo… |
| 11 | Agent Cooperation Designer | Agent Cooperation Designer Sources: Competition and Coopera… |
| 12 | Agent Environment Engineering Architect | Agent Environment Engineering Architect Sources: "EurekAgen… |
| 13 | Agent First Language Architect | Agent-First Language Architect Source: vercel-labs/zerolang… |
| 14 | Agent Governance Orchestrator | Agent Governance Orchestrator Sources: The Orchestration of… |
| 15 | Agent Harness Performance Engineer | Agent Harness Performance Engineer Source: affaan-m/everyth… |
| 16 | Agent Memory Architect | Agent Memory Architect Sources: AgeMem: Unified Long- and S… |
| 17 | Agent Permission Auto Mode Architect | Agent Permission Auto-Mode Architect Sources: Anthropic — C… |
| 18 | Agent Protocol Advisor | Agent Protocol Advisor Sources: Google Developer's Guide to… |
| 19 | Agent Red Team Architect | Agent Red Team Architect Sources: The Promptware Kill Chain… |
| 20 | Agent Reliability Engineer | Agent Reliability Engineer Sources: Towards a Science of AI… |
| 21 | Agent Skill Compositional Risk Auditor | Agent Skill Compositional Risk Auditor Sources: When Safe S… |
| 22 | Agent Skill Designer | Agent Skill Designer Sources: Anthropic Agent Skills Docs (… |
| 23 | Agent Skill Effectiveness Auditor | Agent Skill Effectiveness Auditor Source: SWE-Skills-Bench:… |
| 24 | Agent Skill Optimizer Architect | Agent Skill Optimizer Architect Source: microsoft/SkillOpt … |
| 25 | Agent Skill Supply Chain Auditor | Agent Skill Supply-Chain Security Auditor Sources: Supply-C… |
| 26 | Agent Style Enforcer | Agent Style Enforcer — Literature-Backed Technical-Prose Ru… |
| 27 | Agent Tool Engineer | Agent Tool Engineer Sources: Anthropic — Writing effective … |
| 28 | Agent Trajectory Triage Specialist | Agent Trajectory Triage Specialist Sources: Signals: Trajec… |
| 29 | Agent Virtual Filesystem Architect | Agent Virtual Filesystem Architect Sources: strukto-ai/mira… |
| 30 | Agent World Model Architect | Agent World Model Architect Sources: VLA-World: Vision-Lang… |
| … | *+208 more* | See `scraped/ai-boost-awesome-prompts/` |

</details>

<details>
<summary><strong>Leaked System Prompts</strong> (108 prompts)</summary>

| # | Title | Preview |
|---|-------|---------|
| 1 | Anthropic Claude 2.1 20240306 | # anthropic-claude_2.1_20240306  source: <https://twitter.c… |
| 2 | Anthropic Claude Fable 5 20260609 | # anthropic-claude-fable-5_20260609  source: <https://githu… |
| 3 | Anthropic Claude Haiku 3 20240712 | # anthropic-claude-haiku-3_20240712  source: <https://docs.… |
| 4 | Anthropic Claude Haiku 4.5 20251015 | # anthropic-claude-haiku-4.5_20251015  source: <https://pla… |
| 5 | Anthropic Claude Haiku 4.5 20251119 | # anthropic-claude-haiku-4.5_20251119  source: <https://pla… |
| 6 | Anthropic Claude Opus 20240306 | # anthropic-claude-opus_20240306  source: <https://twitter.… |
| 7 | Anthropic Claude Opus 3 20240712 | # anthropic-claude-opus-3_20240712  source: <https://docs.a… |
| 8 | Anthropic Claude Opus 4.1 20250805 | # anthropic-claude-opus-4.1_20250805  source: <https://plat… |
| 9 | Anthropic Claude Opus 4 20250522 | # anthropic-claude-opus-4_20250522  source: <https://docs.a… |
| 10 | Anthropic Claude Opus 4 20250731 | # anthropic-claude-opus-4_20250731  source: <https://docs.a… |
| 11 | Anthropic Claude Opus 4 20250805 | # anthropic-claude-opus-4_20250805  source: <https://platfo… |
| 12 | Anthropic Claude Opus 4.5 Full 20251124 | # anthropic-claude-opus-4.5-full_20251124  source: <https:/… |
| 13 | Anthropic Claude Opus 4.6 20260206 | # anthropic-claude-opus-4.6_20260206  source: <https://gith… |
| 14 | Anthropic Claude Opus 4.7 20260416 | # anthropic-claude-opus-4.7_20260416  source: <https://gith… |
| 15 | Anthropic Claude Sonnet 3 20240311 | # anthropic-claude-sonnet-3_20240311  source: <https://gith… |
| 16 | Anthropic Claude Sonnet 3.5 20240712 | # anthropic-claude-sonnet-3.5_20240712  source: <https://do… |
| 17 | Anthropic Claude Sonnet 3.5 20241022 | # anthropic-claude-sonnet-3.5_20241022  source: <https://do… |
| 18 | Anthropic Claude Sonnet 3.7 20250224 | # anthropic-claude-sonnet-3.7_20250224  source: <https://x.… |
| 19 | Anthropic Claude Sonnet 3.7 20250516 | # anthropic-claude-sonnet-3.7_20250516  source: <https://gi… |
| 20 | Anthropic Claude Sonnet 4 20250522 | # anthropic-claude-sonnet-4_20250522  source: <https://docs… |
| 21 | Anthropic Claude Sonnet 4 20250731 | # anthropic-claude-sonnet-4_20250731  source: <https://plat… |
| 22 | Anthropic Claude Sonnet 4.5 20250929 | # anthropic-claude-sonnet-4.5_20250929  source: <https://pl… |
| 23 | Anthropic Claude Sonnet 4.5 20251119 | # anthropic-claude-sonnet-4.5_20251119  source: <https://pl… |
| 24 | Anthropic Claude Sonnet 4.5 20260128 | # anthropic-claude-sonnet-4.5_20260128  ## Q (User)  wrap t… |
| 25 | Anthropic Claude Sonnet 4.5 Full 202509… | # anthropic-claude-sonnet-4.5-full_20250929  source: <https… |
| 26 | Anthropic Claude User Styles 20250420 | # anthropic-claude-user-styles_20250420  source: <https://g… |
| 27 | Brave Leo Ai 20250903 | # brave-leo-ai_20250903  source:  ![Image](https://github.c… |
| 28 | Claude Code Output Style Explanatory 20… | # claude-code-output-style-explanatory_20251007  source: Ex… |
| 29 | Claude Code Output Style Learning 20251… | # claude-code-output-style-learning_20251007  source: Extra… |
| 30 | Claude In Chrome 20260328 | # claude-in-chrome_20260328  This content was obtained via … |
| … | *+78 more* | See `scraped/leaked-system-prompts/` |

</details>

<details>
<summary><strong>Prompts Chat</strong> (1974 prompts)</summary>

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
| … | *+1944 more* | See `scraped/prompts-chat/` |

</details>
## License

MIT
