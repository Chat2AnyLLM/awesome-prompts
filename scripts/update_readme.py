#!/usr/bin/env python3
"""Update README.md with current prompt stats and scraped prompt listing."""

import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
CONFIG_PATH = REPO_ROOT / "awesome_prompts.json"
DIST_DIR = REPO_ROOT / "dist"
SCRAPED_DIR = REPO_ROOT / "scraped"

# Max prompts to show per source in the table
MAX_PER_SOURCE = 30


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:80]


def count_scraped() -> dict[str, int]:
    """Count scraped prompts per source."""
    counts = {}
    if not SCRAPED_DIR.exists():
        return counts
    for source_dir in sorted(SCRAPED_DIR.iterdir()):
        if source_dir.is_dir():
            count = len(list(source_dir.glob("*.yaml")))
            if count > 0:
                counts[source_dir.name] = count
    return counts


def load_config_sources() -> list[dict]:
    """Load sources from awesome_prompts.json."""
    if not CONFIG_PATH.exists():
        return []
    with open(CONFIG_PATH) as f:
        return json.load(f).get("sources", [])


def abbreviate(text: str, max_len: int = 60) -> str:
    """Truncate text and add ellipsis."""
    text = text.replace("\n", " ").replace("|", "/").strip()
    if len(text) > max_len:
        return text[:max_len - 1] + "…"
    return text


def generate_stats_section() -> str:
    """Generate the Stats section with source tables."""
    prompts_json = DIST_DIR / "prompts.json"
    prompts_count = 0
    if prompts_json.exists():
        with open(prompts_json) as f:
            prompts_count = json.load(f).get("count", 0)

    sources = load_config_sources()
    scraped = count_scraped()
    total_scraped = sum(scraped.values())

    lines = [
        "## Stats",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Direct prompts (in `prompts/`) | {prompts_count} |",
        f"| Configured sources | {len(sources)} |",
        f"| Scraped prompts (total) | {total_scraped} |",
        "",
    ]

    if sources:
        lines.append("### Configured Sources")
        lines.append("")
        lines.append("| Source | URL | Format | Scraped |")
        lines.append("|--------|-----|--------|---------|")
        for s in sources:
            name = s.get("name", "?")
            url = s.get("url", "")
            fmt = s.get("format", "?")
            slug = slugify(name)
            count = scraped.get(slug, 0)
            lines.append(f"| {name} | [{url}]({url}) | {fmt} | {count} |")
        lines.append("")

    # Generate per-source prompt tables
    if SCRAPED_DIR.exists():
        lines.append("### Scraped Prompts")
        lines.append("")
        for source_dir in sorted(SCRAPED_DIR.iterdir()):
            if not source_dir.is_dir():
                continue
            yaml_files = sorted(source_dir.glob("*.yaml"))
            if not yaml_files:
                continue

            source_name = source_dir.name.replace("-", " ").title()
            lines.append(f"<details>")
            lines.append(f"<summary><strong>{source_name}</strong> ({len(yaml_files)} prompts)</summary>")
            lines.append("")
            lines.append("| # | Title | Preview |")
            lines.append("|---|-------|---------|")

            for i, yf in enumerate(yaml_files[:MAX_PER_SOURCE], 1):
                try:
                    data = yaml.safe_load(yf.read_text())
                    title = abbreviate(data.get("title", yf.stem), 40)
                    preview = abbreviate(data.get("prompt", ""), 60)
                    lines.append(f"| {i} | {title} | {preview} |")
                except Exception:
                    continue

            if len(yaml_files) > MAX_PER_SOURCE:
                lines.append(f"| … | *+{len(yaml_files) - MAX_PER_SOURCE} more* | See `scraped/{source_dir.name}/` |")

            lines.append("")
            lines.append("</details>")
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    stats_section = generate_stats_section()

    readme_content = README_PATH.read_text()

    # Replace existing Stats section or insert before License
    stats_pattern = r'## Stats\n.*?(?=\n## [^SC]|\Z)'
    if re.search(stats_pattern, readme_content, re.DOTALL):
        readme_content = re.sub(stats_pattern, stats_section.rstrip(), readme_content, flags=re.DOTALL)
    else:
        license_match = re.search(r'\n## License', readme_content)
        if license_match:
            insert_pos = license_match.start()
            readme_content = readme_content[:insert_pos] + "\n" + stats_section + "\n" + readme_content[insert_pos:]
        else:
            readme_content += "\n" + stats_section

    README_PATH.write_text(readme_content)
    print("README.md updated with current stats.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
