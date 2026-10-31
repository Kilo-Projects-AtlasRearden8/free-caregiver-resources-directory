# Free Caregiver Resources Directory

A Markdown-driven, static HTML directory of **free resources for family caregivers**, grouped by need:

- **Respite Care** — short-term breaks so caregivers can rest or run errands
- **Support Groups** — peer connection, helplines, and online communities
- **Benefit Guides** — Medicare, Medicaid, Social Security, veterans benefits, and local aid
- **Legal Aid** — powers of attorney, advance directives, guardianship, and appeals

**Official links only.** Every entry points to a government agency, national nonprofit, or recognized advocacy organization. No personal data is collected, no tracking scripts, fully client-side search.

## Who built this

Created by **Asdale Dynamics, LLC** — the publisher behind *The Massive AI Manual* and [dylanasdale.github.io](https://github.com/dylanasdale), which explain AI "like a friend would": plain English, step by step, never condescending.

## Run it

This is a plain static site — no server required.

```bash
# 1. Build the site from the Markdown content
python build.py

# 2. Open the result
open index.html
```

`build.py` reads the Markdown files in `content/` and generates:

- `index.html` — the searchable page (styled with `styles.css`, searched with `search.js`)
- `resources.json` — a machine-readable index used by the search widget

## Test it

```bash
python test_build.py
```

Tests verify that every content file parses, every resource has at least one official link, all links are `http(s)` URLs, the build regenerates the HTML and JSON consistently, and all four groups are present.

## Edit content

Resources live as Markdown in `content/`, one file per group:

| File | Group |
|------|-------|
| `content/01-respite-care.md` | Respite Care |
| `content/02-support-groups.md` | Support Groups |
| `content/03-benefit-guides.md` | Benefit Guides |
| `content/04-legal-aid.md` | Legal Aid |

Each resource is a `## Title` block with `- **What it is:**`, `- **Official link:**` (one or more URLs), and `- **Use for:**` lines. Re-run `python build.py` after editing.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.