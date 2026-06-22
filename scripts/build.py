#!/usr/bin/env python3
"""Build unified dist/ artifacts from sources configured in config.yaml."""

import csv
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

import yaml
from jsonschema import Draft202012Validator

# Increase CSV field size limit for large prompt texts.
csv.field_size_limit(10 * 1024 * 1024)

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config.yaml"
PROMPT_SCHEMA_PATH = REPO_ROOT / "schema" / "prompt.schema.json"
DIST_DIR = REPO_ROOT / "dist"
SCRAPED_DIR = REPO_ROOT / "scraped"

VERSION = "2.0.0"
DEFAULT_CATEGORY = "analysis"


def load_schema(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_config() -> dict:
    """Load config.yaml."""
    if not CONFIG_PATH.exists():
        print(f"FAIL: missing config file: {CONFIG_PATH}")
        sys.exit(1)

    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"FAIL: invalid config.yaml: {e}")
        sys.exit(1)

    if not isinstance(config, dict):
        print("FAIL: config.yaml must contain a mapping")
        sys.exit(1)
    if not isinstance(config.get("sources"), list):
        print("FAIL: config.yaml must contain a sources list")
        sys.exit(1)

    return config


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:80]


def fetch_url(url: str) -> str:
    """Fetch URL content as text. Returns an empty string on fetch errors."""
    req = Request(url, headers={"User-Agent": "awesome-prompts-builder/2.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except (URLError, OSError, TimeoutError) as e:
        print(f"    WARNING fetching {url}: {e}")
        return ""


def parse_github_url(url: str) -> tuple[str, str]:
    """Extract (user, repo) from a GitHub URL."""
    match = re.match(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url)
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


def normalize_prompt(
    prompt: dict,
    source_name: str,
    defaults: dict | None = None,
) -> dict | None:
    """Normalize a prompt from any source into the unified dist shape."""
    if not isinstance(prompt, dict):
        return None

    defaults = defaults or {}
    title = str(
        prompt.get("title")
        or prompt.get("act")
        or prompt.get("name")
        or defaults.get("title")
        or ""
    ).strip()
    prompt_text = str(
        prompt.get("prompt")
        or prompt.get("content")
        or prompt.get("text")
        or ""
    ).strip()

    if not title or not prompt_text or len(prompt_text) < 10:
        return None

    slug = slugify(prompt.get("slug") or title)
    if not slug:
        return None

    tags = prompt.get("tags", defaults.get("tags", ["imported"]))
    if isinstance(tags, str):
        tags = [tag.strip() for tag in re.split(r"[,;]", tags) if tag.strip()]
    if not tags:
        tags = ["imported"]

    normalized = {
        "slug": slug,
        "title": title,
        "description": str(
            prompt.get("description")
            or defaults.get("description")
            or f"Imported from {source_name}"
        ).strip(),
        "prompt": prompt_text,
        "tags": tags,
        "category": str(
            prompt.get("category") or defaults.get("category") or DEFAULT_CATEGORY
        ).strip(),
        "author": str(
            prompt.get("author") or defaults.get("author") or source_name
        ).strip(),
        "source": source_name,
    }

    if "variables" in prompt:
        normalized["variables"] = prompt["variables"]

    return normalized


def validate_prompt_file(file_path: Path, data: dict, schema: dict) -> None:
    """Validate a local prompt YAML file and fail the build if invalid."""
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    if errors:
        print(f"FAIL: {file_path.name}")
        for err in errors:
            print(f"  {err.json_path}: {err.message}")
        sys.exit(1)

    if data.get("slug") != file_path.stem:
        print(f"FAIL: {file_path.name} - slug does not match filename")
        sys.exit(1)


def load_local_source(source: dict, prompt_schema: dict) -> list[dict]:
    """Load and validate prompts from a local directory of YAML files."""
    source_name = source.get("name", "Local")
    path = Path(source.get("path", "prompts/"))
    source_dir = path if path.is_absolute() else REPO_ROOT / path

    if not source_dir.exists():
        print(f"    WARNING: local path does not exist: {source_dir}")
        return []

    prompts = []
    for file_path in sorted(source_dir.glob("*.yaml")):
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            print(f"FAIL: {file_path.name} is empty")
            sys.exit(1)

        validate_prompt_file(file_path, data, prompt_schema)
        normalized = dict(data)
        normalized.setdefault("variables", [])
        normalized["source"] = source_name
        prompts.append(normalized)

    return prompts


def prompts_from_csv(content: str, source_name: str) -> list[dict]:
    prompts = []
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        normalized = normalize_prompt(row, source_name)
        if normalized:
            prompts.append(normalized)
    return prompts


def prompts_from_text_file(file_name: str, content: str, source_name: str) -> list[dict]:
    if not content or len(content.strip()) < 20:
        return []
    name = Path(file_name).stem
    normalized = normalize_prompt(
        {
            "slug": slugify(name),
            "title": name.replace("-", " ").replace("_", " ").title(),
            "prompt": content.strip(),
        },
        source_name,
    )
    return [normalized] if normalized else []


def prompts_from_yaml(content: str, file_name: str, source_name: str) -> list[dict]:
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        return []

    items = data if isinstance(data, list) else [data]
    prompts = []
    for item in items:
        defaults = {"title": Path(file_name).stem.replace("-", " ").title()}
        normalized = normalize_prompt(item, source_name, defaults)
        if normalized:
            prompts.append(normalized)
    return prompts


def prompts_from_json(content: str, source_name: str) -> list[dict]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return []

    items = data if isinstance(data, list) else data.get("prompts", [])
    prompts = []
    for item in items:
        normalized = normalize_prompt(item, source_name)
        if normalized:
            prompts.append(normalized)
    return prompts


def list_github_directory(user: str, repo: str, dir_path: str) -> list[dict]:
    encoded_dir = quote(dir_path or "", safe="/")
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{encoded_dir}"
    content = fetch_url(api_url)
    if not content:
        return []
    try:
        items = json.loads(content)
    except json.JSONDecodeError:
        return []
    return items if isinstance(items, list) else []


def fetch_github_file(user: str, repo: str, branch: str, file_path: str) -> str:
    encoded_path = quote(file_path, safe="/")
    raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{encoded_path}"
    return fetch_url(raw_url)


def scrape_github_text_files(
    user: str,
    repo: str,
    branch: str,
    file_path: str,
    fmt: str,
    source_name: str,
) -> list[dict]:
    extensions = (".txt",) if fmt == "txt" else (".md",)

    if file_path and any(file_path.lower().endswith(ext) for ext in extensions):
        content = fetch_github_file(user, repo, branch, file_path)
        return prompts_from_text_file(file_path, content, source_name)

    skip_files = {
        "readme.md",
        "readme.txt",
        "license.md",
        "contributing.md",
        "changelog.md",
        "code_of_conduct.md",
    }
    items = list_github_directory(user, repo, file_path or "")
    matching_files = [
        item
        for item in items
        if isinstance(item, dict)
        and any(item.get("name", "").lower().endswith(ext) for ext in extensions)
        and item.get("name", "").lower() not in skip_files
    ]

    prompts = []
    for item in matching_files[:500]:
        path = item.get("path", item.get("name", ""))
        content = fetch_github_file(user, repo, branch, path)
        prompts.extend(prompts_from_text_file(path, content, source_name))
    return prompts


def scrape_github_yaml_files(
    user: str,
    repo: str,
    branch: str,
    file_path: str,
    source_name: str,
) -> list[dict]:
    if file_path and file_path.lower().endswith((".yaml", ".yml")):
        content = fetch_github_file(user, repo, branch, file_path)
        return prompts_from_yaml(content, file_path, source_name)

    items = list_github_directory(user, repo, file_path or "")
    yaml_files = [
        item
        for item in items
        if isinstance(item, dict)
        and item.get("name", "").lower().endswith((".yaml", ".yml"))
    ]

    prompts = []
    for item in yaml_files[:100]:
        path = item.get("path", item.get("name", ""))
        content = fetch_github_file(user, repo, branch, path)
        prompts.extend(prompts_from_yaml(content, path, source_name))
    return prompts


def scrape_github_json_file(
    user: str,
    repo: str,
    branch: str,
    file_path: str,
    source_name: str,
) -> list[dict]:
    if not file_path:
        return []
    content = fetch_github_file(user, repo, branch, file_path)
    return prompts_from_json(content, source_name)


def save_scraped_prompts(source_name: str, prompts: list[dict]) -> int:
    """Cache scraped prompts in scraped/<source-slug>/ as YAML files."""
    source_slug = slugify(source_name)
    output_dir = SCRAPED_DIR / source_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_path in output_dir.glob("*.yaml"):
        file_path.unlink()

    saved = 0
    seen_slugs = set()
    for prompt in prompts:
        slug = prompt.get("slug", "")
        if not slug or slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        out_file = output_dir / f"{slug}.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            yaml.dump(prompt, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        saved += 1

    return saved


def load_github_source(source: dict) -> list[dict]:
    """Load prompts by scraping a configured GitHub repo source."""
    source_name = source.get("name", "GitHub Source")
    url = source.get("url", "")
    fmt = source.get("format", "")
    file_path = source.get("file_path", "") or ""

    user, repo = parse_github_url(url)
    if not user or not repo:
        print(f"    WARNING: cannot parse GitHub URL: {url}")
        return []

    branch = get_default_branch(user, repo)
    print(f"    Repo: {user}/{repo} (branch: {branch}, format: {fmt})")

    if fmt == "csv":
        content = fetch_github_file(user, repo, branch, file_path or "prompts.csv")
        prompts = prompts_from_csv(content, source_name)
    elif fmt in ("md", "txt"):
        prompts = scrape_github_text_files(user, repo, branch, file_path, fmt, source_name)
    elif fmt in ("yaml", "yml"):
        prompts = scrape_github_yaml_files(user, repo, branch, file_path, source_name)
    elif fmt == "json":
        prompts = scrape_github_json_file(user, repo, branch, file_path, source_name)
    else:
        print(f"    WARNING: unsupported GitHub source format: {fmt}")
        return []

    saved = save_scraped_prompts(source_name, prompts)
    print(f"    Cached: {saved} prompts")
    return prompts


def load_json_url_source(source: dict) -> list[dict]:
    """Load prompts from a remote JSON URL."""
    source_name = source.get("name", "JSON URL Source")
    url = source.get("url", "")
    if not url:
        print("    WARNING: json_url source missing url")
        return []

    content = fetch_url(url)
    if not content:
        return []
    return prompts_from_json(content, source_name)


def load_source(source: dict, prompt_schema: dict) -> list[dict]:
    """Dispatch a configured source to its loader."""
    source_type = source.get("type")
    if source_type == "local":
        return load_local_source(source, prompt_schema)
    if source_type == "github":
        return load_github_source(source)
    if source_type == "json_url":
        return load_json_url_source(source)

    print(f"    WARNING: unsupported source type: {source_type}")
    return []


def dedupe_prompts(prompts: list[dict]) -> list[dict]:
    """Deduplicate prompts by slug. First source in config wins."""
    deduped = []
    seen_slugs = set()
    for prompt in prompts:
        slug = prompt.get("slug")
        if not slug or slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        deduped.append(prompt)
    return deduped


def write_prompts_json(prompts: list[dict], output_dir: Path) -> None:
    """Write unified dist/prompts.json."""
    for prompt in prompts:
        prompt.setdefault("variables", [])

    output = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(prompts),
        "prompts": prompts,
    }
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "prompts.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Written: {output_path} ({len(prompts)} prompts)")


def write_prompts_csv(prompts: list[dict], output_dir: Path) -> None:
    """Write unified dist/prompts.csv."""
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "prompts.csv"
    fieldnames = [
        "slug",
        "title",
        "description",
        "prompt",
        "tags",
        "category",
        "author",
        "source",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for prompt in prompts:
            row = {k: prompt.get(k, "") for k in fieldnames if k != "tags"}
            row["tags"] = ";".join(prompt.get("tags", []))
            writer.writerow(row)
    print(f"  Written: {output_path} ({len(prompts)} prompts)")


def write_sources_json(sources: list[dict], output_dir: Path) -> None:
    """Write dist/sources.json."""
    output = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(sources),
        "sources": sources,
    }
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "sources.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Written: {output_path} ({len(sources)} sources)")


def write_index_json(prompts: list[dict], sources: list[dict], output_dir: Path) -> None:
    """Write dist/index.json — a single entry point for consumers."""
    output = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompts": {
            "count": len(prompts),
            "file": "prompts.json",
        },
        "sources": {
            "count": len(sources),
            "file": "sources.json",
        },
    }
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "index.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Written: {output_path}")


def main() -> int:
    print("Building unified prompt collection...")

    config = load_config()
    prompt_schema = load_schema(PROMPT_SCHEMA_PATH)
    sources = config.get("sources", [])
    output_dir = REPO_ROOT / config.get("output", {}).get("dir", "dist")

    all_prompts = []
    source_summaries = []
    for source in sources:
        name = source.get("name", "unknown")
        print(f"  [{name}]")
        prompts = load_source(source, prompt_schema)
        print(f"    Loaded: {len(prompts)} prompts\n")
        all_prompts.extend(prompts)
        source_summary = dict(source)
        source_summary["count"] = len(prompts)
        source_summaries.append(source_summary)

    prompts = dedupe_prompts(all_prompts)
    skipped = len(all_prompts) - len(prompts)
    if skipped:
        print(f"Deduplicated: skipped {skipped} duplicate prompt(s)")

    write_prompts_json(prompts, output_dir)
    write_prompts_csv(prompts, output_dir)
    write_sources_json(source_summaries, output_dir)
    write_index_json(prompts, source_summaries, output_dir)

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
