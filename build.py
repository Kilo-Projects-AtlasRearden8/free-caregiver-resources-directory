#!/usr/bin/env python3
"""Build the Free Caregiver Resources Directory static site.

Parses Markdown content files in content/ and generates:
  - index.html  (client-side search page)
  - resources.json (machine-readable index for the search)

Usage:
    python build.py
"""
import json
import os
import re
import sys
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUT_HTML = os.path.join(BASE_DIR, "index.html")
OUT_JSON = os.path.join(BASE_DIR, "resources.json")

# Order of groups as they should appear on the page.
GROUP_ORDER = [
    "respite",
    "support",
    "benefits",
    "legal",
]

GROUP_TITLES = {
    "respite": "Respite Care",
    "support": "Support Groups",
    "benefits": "Benefit Guides",
    "legal": "Legal Aid",
}

# Filename -> group key
FILENAME_GROUP = {
    "01-respite-care.md": "respite",
    "02-support-groups.md": "support",
    "03-benefit-guides.md": "benefits",
    "04-legal-aid.md": "legal",
}

# Matches a resource block:
#   ## Title
#   - **What it is:** ...
#   - **Official link:** URL
#   - **Use for:** ...
# Each block may have one or more **Official link:** lines.
RESOURCE_RE = re.compile(
    r"##\s+(?P<title>.+?)\s*\n"
    r"(?P<body>(?:\s*-\s+.+\n)+)",
    re.MULTILINE,
)

LINK_RE = re.compile(r"\*\*Official link:\*\*\s*(?P<url>\S+)")
WHAT_RE = re.compile(r"\*\*What it is:\*\*\s*(?P<desc>.+)")
USE_RE = re.compile(r"\*\*Use for:\*\*\s*(?P<use>.+)")


def parse_markdown(path):
    """Parse a content markdown file into a list of resource dicts."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    resources = []
    for match in RESOURCE_RE.finditer(text):
        title = match.group("title").strip()
        body = match.group("body")

        links = LINK_RE.findall(body)
        what = WHAT_RE.search(body)
        use = USE_RE.search(body)

        if not links:
            continue  # skip malformed entries

        resources.append(
            {
                "title": title,
                "description": what.group("desc").strip() if what else "",
                "use": use.group("use").strip() if use else "",
                "links": links,
            }
        )
    return resources


def load_all_resources():
    """Load resources from all content files, grouped by group key."""
    grouped = {key: [] for key in GROUP_ORDER}
    for filename, group in FILENAME_GROUP.items():
        path = os.path.join(CONTENT_DIR, filename)
        if not os.path.isfile(path):
            print(f"WARNING: missing content file {filename}", file=sys.stderr)
            continue
        resources = parse_markdown(path)
        grouped[group].extend(resources)
    return grouped


def render_html(grouped):
    """Render the full index.html page."""
    # Build group sections
    sections = []
    for group in GROUP_ORDER:
        items = grouped.get(group, [])
        cards = []
        for r in items:
            links_html = "".join(
                f'<a class="link" href="{escape(url)}" target="_blank" rel="noopener">{escape(url)}</a>'
                for url in r["links"]
            )
            desc = f'<p class="desc">{escape(r["description"])}</p>' if r["description"] else ""
            use = f'<p class="use">{escape(r["use"])}</p>' if r["use"] else ""
            cards.append(
                f'      <article class="card" data-group="{group}">\n'
                f'        <h3>{escape(r["title"])}</h3>\n'
                f'        {desc}\n'
                f'        <div>{links_html}</div>\n'
                f'        {use}\n'
                f'      </article>'
            )
        sections.append(
            f'    <section class="group" id="group-{group}">\n'
            f'      <h2>{escape(GROUP_TITLES[group])}</h2>\n'
            + "\n".join(cards)
            + "\n    </section>"
        )

    sections_html = "\n".join(sections)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Free Caregiver Resources Directory</title>
  <meta name="description" content="Free resources for family caregivers: respite care, support groups, benefit guides, and legal aid. Official links only.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site">
    <h1>Free Caregiver Resources Directory</h1>
    <p class="lead">Free resources for family caregivers — respite care, support groups, benefit guides, and legal aid. Grouped by need, official links only.</p>
    <div class="search-row">
      <input id="search" type="search" placeholder="Search resources (e.g. respite, Medicare, legal)…" aria-label="Search resources">
      <span id="count"></span>
    </div>
  </header>
  <main>
{sections_html}
  </main>
  <footer class="site">
    <p>Free Caregiver Resources Directory &mdash; by Asdale Dynamics, LLC. Official links only. No personal data is collected.</p>
    <p>Created by Asdale Dynamics, LLC &mdash; The Massive AI Manual and dylanasdale.github.io.</p>
  </footer>
  <script src="search.js"></script>
</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {OUT_HTML}")


def render_json(grouped, out_path):
    """Write resources.json for the client-side search."""
    data = {
        "groups": [
            {"key": g, "title": GROUP_TITLES[g], "items": grouped.get(g, [])}
            for g in GROUP_ORDER
        ]
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"Wrote {out_path}")


def main():
    grouped = load_all_resources()
    total = sum(len(v) for v in grouped.values())
    if total == 0:
        print("ERROR: no resources found in content/", file=sys.stderr)
        return 1
    render_html(grouped)
    render_json(grouped, OUT_JSON)
    return 0


if __name__ == "__main__":
    sys.exit(main())