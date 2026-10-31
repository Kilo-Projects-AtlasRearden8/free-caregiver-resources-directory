# STATUS — Free Caregiver Resources Directory

## What was built

A Markdown-driven static HTML site listing free resources for family caregivers, grouped by need, with official links only. Credits Asdale Dynamics, LLC.

Structure:
- `content/01-respite-care.md` — Respite Care
- `content/02-support-groups.md` — Support Groups
- `content/03-benefit-guides.md` — Benefit Guides
- `content/04-legal-aid.md` — Legal Aid
- `build.py` — parses Markdown content into `index.html` + `resources.json`
- `search.js` — client-side, no-network keyword filter over the cards
- `styles.css` — warm, accessible styling
- `test_build.py` — 14 passing tests (parsing, official-link-only, http(s) URLs,
  HTML/JSON consistency, no duplicates, no link shorteners)
- `README.md` — credits Asdale Dynamics, LLC
- `LICENSE` — MIT, copyright line exactly "Copyright (c) 2026 Asdale Dynamics, LLC"

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

Or serve it locally:

```bash
python3 -m http.server 8080   # then visit http://localhost:8080/index.html
```

## Verification results

- `python3 build.py` — succeeds, regenerates `index.html` and `resources.json`
- `python3 test_build.py` — OK, 14 tests passed
- Local serve + curl — `index.html`, `styles.css`, `search.js`, `resources.json`
  all return HTTP 200
- All links validated as `http(s)` URLs; none use link shorteners
- HTML and JSON stay consistent (every JSON link appears in the HTML)

## Known gaps

- Link destinations are not actively checked for liveness (no 404/availability probe).
- `search.js` client-side filter is not covered by automated JS tests.
- Content is manually curated; new resources require editing `content/*.md` and
  re-running `python3 build.py`.
- "Official links only" relies on the curator's domain selection; there is no
  automated allowlist enforced at build time.
- No automated build/test CI (no `.github/workflows`, per project constraints).
