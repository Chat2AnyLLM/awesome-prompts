#!/usr/bin/env python3
"""Scrape prompts from sources configured in awesome_prompts.json.

Reads the config file, fetches prompt files from each configured GitHub link,
parses them, and saves into scraped/<source-name>/ as normalized YAML files.
"""

import csv
import io
import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "awesome_prompts.json"
SCRAPED_DIR = REPO_ROOT / "scraped"


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text[:80]


def fetch_url(url: str) -> str:
    """Fetch URL content as text."""
    req = Request(url, headers={"User-Agent": "awesome-prompts-scraper/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except (URLError, OSError, TimeoutError) as e:
        print(f"    ERROR fetching {url}: {e}")
        return ""


def load_config() -> dict:
    """Load awesome_prompts.json config."""
    with open(CONFIG_PATH) as f:
        return json.load(f)


def parse_github_url(url: str) -> tuple[str, str]:
    """Extract (user, repo) from a GitHub URL."""
    match = re.match(r'https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$', url)
    if match:
        return match.groups()
    return ("", "")


def get_default_branch(user: str, repo: str) -> str:
    """Get default branch via GitHub API."""
    api_url = f"https://api.github.com/repos/{user}/{repo}"
    content = fetch_url(api_url)
    if content:
        try:
            return json.loads(content).get("default_branch", "main")
        except json.JSONDecodeError:
            pass
    return "main"


def scrape_csv(user: str, repo: str, branch: str, file_path: str) -> list[dict]:
    """Scrape prompts from a CSV file in a GitHub repo."""
    raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"
    content = fetch_url(raw_url)
    if not content:
        return []

    prompts = []
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        # Support common CSV column names
        title = row.get("act") or row.get("title") or row.get("name") or ""
        prompt_text = row.get("prompt") or row.get("text") or row.get("content") or ""
        title = title.strip()
        prompt_text = prompt_text.strip()

        if not title or not prompt_text or len(prompt_text) < 10:
            continue

        prompts.append({
            "slug": slugify(title),
            "title": title,
            "prompt": prompt_text,
        })

    return prompts


def scrape_md_files(user: str, repo: str, branch: str, file_path: str) -> list[dict]:
    """Scrape prompts from markdown files in a GitHub repo."""
    # If file_path points to a specific file, fetch just that
    if file_path and file_path.endswith(".md"):
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"
        content = fetch_url(raw_url)
        if not content or len(content) < 20:
            return []
        name = Path(file_path).stem
        return [{
            "slug": slugify(name),
            "title": name.replace("-", " ").replace("_", " ").title(),
            "prompt": content.strip(),
        }]

    # Otherwise list directory and fetch .md files
    dir_path = file_path or ""
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{dir_path}"
    content = fetch_url(api_url)
    if not content:
        return []

    try:
        items = json.loads(content)
    except json.JSONDecodeError:
        return []

    if not isinstance(items, list):
        return []

    skip_files = {"readme.md", "license.md", "contributing.md", "changelog.md", "code_of_conduct.md"}
    md_files = [
        item for item in items
        if isinstance(item, dict)
        and item.get("name", "").lower().endswith(".md")
        and item.get("name", "").lower() not in skip_files
    ]

    prompts = []
    for md_file in md_files[:100]:  # Cap per source
        download_url = md_file.get("download_url", "")
        if not download_url:
            continue

        file_content = fetch_url(download_url)
        if not file_content or len(file_content) < 20:
            continue

        name = md_file["name"].replace(".md", "")
        prompts.append({
            "slug": slugify(name),
            "title": name.replace("-", " ").replace("_", " ").title(),
            "prompt": file_content.strip(),
        })

    return prompts


def scrape_yaml_files(user: str, repo: str, branch: str, file_path: str) -> list[dict]:
    """Scrape prompts from YAML files in a GitHub repo."""
    # Single file
    if file_path and (file_path.endswith(".yaml") or file_path.endswith(".yml")):
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"
        content = fetch_url(raw_url)
        if not content:
            return []
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            return []
        if isinstance(data, dict) and data.get("prompt"):
            return [{
                "slug": slugify(data.get("title", Path(file_path).stem)),
                "title": data.get("title", Path(file_path).stem),
                "prompt": data["prompt"],
            }]
        return []

    # Directory listing
    dir_path = file_path or ""
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{dir_path}"
    content = fetch_url(api_url)
    if not content:
        return []

    try:
        items = json.loads(content)
    except json.JSONDecodeError:
        return []

    if not isinstance(items, list):
        return []

    yaml_files = [
        item for item in items
        if isinstance(item, dict)
        and (item.get("name", "").endswith(".yaml") or item.get("name", "").endswith(".yml"))
    ]

    prompts = []
    for yf in yaml_files[:100]:
        download_url = yf.get("download_url", "")
        if not download_url:
            continue

        file_content = fetch_url(download_url)
        if not file_content:
            continue

        try:
            data = yaml.safe_load(file_content)
        except yaml.YAMLError:
            continue

        if isinstance(data, dict) and data.get("prompt"):
            name = yf["name"].rsplit(".", 1)[0]
            prompts.append({
                "slug": slugify(data.get("title", name)),
                "title": data.get("title", name),
                "prompt": data["prompt"],
            })

    return prompts


def scrape_json_file(user: str, repo: str, branch: str, file_path: str) -> list[dict]:
    """Scrape prompts from a JSON file."""
    if not file_path:
        return []

    raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"
    content = fetch_url(raw_url)
    if not content:
        return []

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return []

    prompts = []
    # Handle array of prompts or object with prompts key
    items = data if isinstance(data, list) else data.get("prompts", [])
    for item in items:
        if not isinstance(item, dict):
            continue
        title = item.get("title") or item.get("act") or item.get("name") or ""
        prompt_text = item.get("prompt") or item.get("content") or item.get("text") or ""
        if title and prompt_text and len(prompt_text) >= 10:
            prompts.append({
                "slug": slugify(title),
                "title": title,
                "prompt": prompt_text,
            })

    return prompts


def scrape_source(source: dict) -> list[dict]:
    """Scrape prompts from a configured source."""
    url = source["url"]
    fmt = source.get("format", "")
    file_path = source.get("file_path", "")

    user, repo = parse_github_url(url)
    if not user or not repo:
        print(f"    ERROR: Cannot parse GitHub URL: {url}")
        return []

    branch = get_default_branch(user, repo)
    print(f"    Repo: {user}/{repo} (branch: {branch}, format: {fmt})")

    try:
        if fmt == "csv":
            return scrape_csv(user, repo, branch, file_path or "prompts.csv")
        elif fmt == "md":
            return scrape_md_files(user, repo, branch, file_path)
        elif fmt in ("yaml", "yml"):
            return scrape_yaml_files(user, repo, branch, file_path)
        elif fmt == "json":
            return scrape_json_file(user, repo, branch, file_path)
        else:
            print(f"    Skipping unsupported format: {fmt}")
            return []
    except Exception as e:
        print(f"    ERROR: {e}")
        return []


def save_scraped_prompts(source_name: str, prompts: list[dict]) -> int:
    """Save scraped prompts to scraped/<source-slug>/ as YAML files."""
    source_slug = slugify(source_name)
    output_dir = SCRAPED_DIR / source_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean existing files
    for f in output_dir.glob("*.yaml"):
        f.unlink()

    saved = 0
    seen_slugs = set()
    for prompt in prompts:
        slug = prompt["slug"]
        if not slug or slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        out_file = output_dir / f"{slug}.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            yaml.dump(prompt, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        saved += 1

    return saved


def main() -> int:
    print("=== Prompt Scraper ===")
    print(f"Config: {CONFIG_PATH}")

    config = load_config()
    sources = config.get("sources", [])

    if not sources:
        print("No sources configured in awesome_prompts.json")
        return 0

    print(f"Found {len(sources)} source(s) to scrape.\n")

    total_scraped = 0
    for source in sources:
        name = source.get("name", "unknown")
        print(f"  [{name}]")
        prompts = scrape_source(source)
        if prompts:
            count = save_scraped_prompts(name, prompts)
            print(f"    Saved: {count} prompts\n")
            total_scraped += count
        else:
            print(f"    No prompts found.\n")

    print(f"Total: {total_scraped} prompts scraped from {len(sources)} sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
