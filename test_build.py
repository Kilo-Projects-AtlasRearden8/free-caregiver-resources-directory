#!/usr/bin/env python3
"""Tests for the Free Caregiver Resources Directory build.

Validates:
  - content/ markdown files parse into resources
  - every resource has at least one official link
  - every link is an http(s) URL
  - build.py regenerates index.html and resources.json
  - resources.json is valid JSON and matches the HTML
  - index.html contains all expected groups

Usage:
    python test_build.py
"""
import json
import os
import re
import subprocess
import sys
import unittest
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUT_HTML = os.path.join(BASE_DIR, "index.html")
OUT_JSON = os.path.join(BASE_DIR, "resources.json")

EXPECTED_GROUPS = ["respite", "support", "benefits", "legal"]
GROUP_TITLES = {
    "respite": "Respite Care",
    "support": "Support Groups",
    "benefits": "Benefit Guides",
    "legal": "Legal Aid",
}

URL_RE = re.compile(r"^https?://\S+$")


def run_build():
    """Run build.py and return (returncode, stdout, stderr)."""
    proc = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "build.py")],
        capture_output=True,
        text=True,
        cwd=BASE_DIR,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.returncode, cls.stdout, cls.stderr = run_build()
        if cls.returncode != 0:
            raise AssertionError(f"build.py failed: {cls.stderr}")
        with open(OUT_JSON, "r", encoding="utf-8") as fh:
            cls.data = json.load(fh)
        with open(OUT_HTML, "r", encoding="utf-8") as fh:
            cls.html = fh.read()

    # ---- content parsing ----

    def test_build_succeeds(self):
        self.assertEqual(self.returncode, 0)

    def test_all_groups_present(self):
        groups = [g["key"] for g in self.data["groups"]]
        self.assertEqual(groups, EXPECTED_GROUPS)

    def test_group_titles_correct(self):
        for g in self.data["groups"]:
            self.assertEqual(g["title"], GROUP_TITLES[g["key"]])

    def test_each_group_has_resources(self):
        for g in self.data["groups"]:
            self.assertGreater(len(g["items"]), 0, f"group {g['key']} is empty")

    def test_every_resource_has_official_link(self):
        for g in self.data["groups"]:
            for item in g["items"]:
                self.assertTrue(item.get("links"), f"{item['title']} has no links")

    def test_every_link_is_http_url(self):
        for g in self.data["groups"]:
            for item in g["items"]:
                for url in item["links"]:
                    self.assertTrue(URL_RE.match(url), f"bad url: {url}")

    def test_no_resource_links_to_non_official_domains(self):
        # Official links only: disallow common non-official link shorteners.
        for g in self.data["groups"]:
            for item in g["items"]:
                for url in item["links"]:
                    self.assertNotIn("bit.ly", url)
                    self.assertNotIn("tinyurl", url)
                    self.assertNotIn("goo.gl", url)

    def test_no_duplicates(self):
        seen = set()
        for g in self.data["groups"]:
            for item in g["items"]:
                key = (g["key"], item["title"])
                self.assertNotIn(key, seen, f"duplicate resource: {key}")
                seen.add(key)

    # ---- html/json consistency ----

    def test_html_contains_all_groups(self):
        for group in EXPECTED_GROUPS:
            self.assertIn(f'id="group-{group}"', self.html)

    def test_html_contains_all_resource_titles(self):
        for g in self.data["groups"]:
            for item in g["items"]:
                self.assertIn(escape(item["title"]), self.html)

    def test_html_contains_all_links(self):
        for g in self.data["groups"]:
            for item in g["items"]:
                for url in item["links"]:
                    self.assertIn(url, self.html)

    def test_html_has_search_script(self):
        self.assertIn("search.js", self.html)

    def test_json_matches_html_links(self):
        # Every link in JSON must appear in the HTML.
        for g in self.data["groups"]:
            for item in g["items"]:
                for url in item["links"]:
                    self.assertIn(url, self.html)


class TestContentFiles(unittest.TestCase):
    def test_content_files_parse(self):
        from build import parse_markdown  # type: ignore
        for filename in ["01-respite-care.md", "02-support-groups.md",
                         "03-benefit-guides.md", "04-legal-aid.md"]:
            path = os.path.join(CONTENT_DIR, filename)
            self.assertTrue(os.path.isfile(path), f"missing {filename}")
            resources = parse_markdown(path)
            self.assertGreater(len(resources), 0, f"{filename} parsed no resources")
            for r in resources:
                self.assertTrue(r["links"], f"{filename}: {r['title']} has no links")


if __name__ == "__main__":
    unittest.main()