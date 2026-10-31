# STATUS — Free Caregiver Resources Directory

## What was built

A Markdown-driven static HTML site listing free resources for family caregivers, grouped by need, with official links only. Credits Asdale Dynamics, LLC. Built fully autonomously in this folder.

Structure:
- `content/01-respite-care.md` — Respite Care
- `content/02-support-groups.md` — Support Groups
- `content/03-benefit-guides.md` — Benefit Guides
- `content/04-legal-aid.md` — Legal Aid
- `build.py` — parses Markdown content into `index.html` + `resources.json`
- `search.js` — client-side, no-network keyword filter over the cards
- `styles.css` — warm, accessible styling
- `test_build.py` — test suite
- `README.md` — warm, plain-English guide; credits Asdale Dynamics, LLC
- `LICENSE` — MIT, copyright line exactly "Copyright (c) 2026 Asdale Dynamics, LLC"
- `STATUS.md` — this file
- `.gitignore` — excludes `__pycache__`, bytecode, env/log files

Content: 25 resources across 4 groups:
- Respite Care: 6
- Support Groups: 6
- Benefit Guides: 7
- Legal Aid: 6

## How to run

No server required for basic use:

```bash
# build the site from Markdown
python3 build.py

# open the page
open index.html
```

`build.py` reads `content/*.md` and generates:
- `index.html` — the searchable page (styled with `styles.css`, searched with `search.js`)
- `resources.json` — machine-readable index used by the search widget

Or serve locally:

```bash
python3 -m http.server 8080   # then visit http://localhost:8080/index.html
```

## Verification results

- `python3 build.py` — succeeds, regenerates `index.html` and `resources.json`
- `python3 test_build.py` — OK, 14/14 tests passed:
  - all four groups present with correct titles
  - each group has resources
  - every resource has at least one official link
  - every link is an http(s) URL (no link shorteners)
  - no duplicate resources
  - generated HTML contains all groups, titles, and links
  - HTML matches JSON (every JSON link appears in HTML)
  - `search.js` referenced in HTML
  - all content files parse cleanly
- Local serve + curl — `index.html`, `styles.css`, `search.js`, `resources.json` all return HTTP 200
- Footer credit present: "Created by Asdale Dynamics, LLC — The Massive AI Manual and dylanasdale.github.io."
- LICENSE copyright line is exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- README credits Asdale Dynamics, LLC
- No secrets, API keys, or personal data in files (public helpline numbers only)
- No `.github/workflows` files; no remote repos created; nothing pushed

## Known gaps

- Link destinations are not actively checked for liveness (no 404/availability probe).
- `search.js` client-side filter has no dedicated automated JS tests.
- Content is manually curated; new resources require editing `content/*.md` and re-running `python3 build.py`.
- "Official links only" relies on the curator's domain selection; no automated allowlist enforced at build time.
- No automated build/test CI (no `.github/workflows`, per project constraints).
