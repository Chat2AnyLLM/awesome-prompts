import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = REPO_ROOT / "scripts" / "build.py"


def load_build_module():
    spec = importlib.util.spec_from_file_location("build", BUILD_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["build"] = module
    spec.loader.exec_module(module)
    return module


class BuildConfigTests(unittest.TestCase):
    def setUp(self):
        self.build = load_build_module()

    def test_load_config_reads_yaml_config(self):
        config = self.build.load_config()

        self.assertEqual(config["version"], "2.0.0")
        self.assertEqual(config["sources"][0]["type"], "local")


class BuildNormalizationTests(unittest.TestCase):
    def setUp(self):
        self.build = load_build_module()

    def test_normalize_prompt_adds_defaults_and_source(self):
        prompt = self.build.normalize_prompt(
            {"title": "My Prompt", "prompt": "Use this prompt for useful work."},
            "Example Source",
        )

        self.assertEqual(prompt["slug"], "my-prompt")
        self.assertEqual(prompt["source"], "Example Source")
        self.assertEqual(prompt["description"], "Imported from Example Source")
        self.assertEqual(prompt["tags"], ["imported"])
        self.assertEqual(prompt["category"], "analysis")
        self.assertEqual(prompt["author"], "Example Source")

    def test_dedupe_prompts_keeps_first_slug(self):
        prompts = [
            {"slug": "same", "title": "First", "prompt": "first prompt", "source": "A"},
            {"slug": "same", "title": "Second", "prompt": "second prompt", "source": "B"},
            {"slug": "other", "title": "Other", "prompt": "other prompt", "source": "C"},
        ]

        deduped = self.build.dedupe_prompts(prompts)

        self.assertEqual([p["title"] for p in deduped], ["First", "Other"])


class BuildJsonUrlTests(unittest.TestCase):
    def setUp(self):
        self.build = load_build_module()

    def test_load_json_url_source_accepts_prompts_object(self):
        payload = {
            "prompts": [
                {"title": "Remote Prompt", "prompt": "Remote prompt content goes here."}
            ]
        }

        original_fetch_url = self.build.fetch_url
        self.build.fetch_url = lambda url: json.dumps(payload)
        try:
            prompts = self.build.load_json_url_source(
                {"name": "Remote", "type": "json_url", "url": "https://example.test/prompts.json"}
            )
        finally:
            self.build.fetch_url = original_fetch_url

        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0]["source"], "Remote")
        self.assertEqual(prompts[0]["slug"], "remote-prompt")


class BuildLocalSourceTests(unittest.TestCase):
    def setUp(self):
        self.build = load_build_module()

    def test_load_local_source_validates_and_adds_source(self):
        schema = {
            "type": "object",
            "required": ["slug", "title", "description", "prompt", "tags", "category", "author"],
            "additionalProperties": False,
            "properties": {
                "slug": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "prompt": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "category": {"type": "string"},
                "author": {"type": "string"},
            },
        }

        with tempfile.TemporaryDirectory() as tmp:
            prompt_dir = Path(tmp) / "prompts"
            prompt_dir.mkdir()
            (prompt_dir / "local-prompt.yaml").write_text(
                yaml.safe_dump(
                    {
                        "slug": "local-prompt",
                        "title": "Local Prompt",
                        "description": "A local test prompt",
                        "prompt": "Local prompt content goes here.",
                        "tags": ["test"],
                        "category": "analysis",
                        "author": "tester",
                    },
                    sort_keys=False,
                )
            )

            prompts = self.build.load_local_source(
                {"name": "Local", "type": "local", "path": str(prompt_dir)}, schema
            )

        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0]["source"], "Local")
        self.assertEqual(prompts[0]["title"], "Local Prompt")


if __name__ == "__main__":
    unittest.main()
