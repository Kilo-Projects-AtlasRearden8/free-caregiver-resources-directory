# Free Caregiver Resources Directory

A friendly, free directory of resources for family caregivers — built by
**Asdale Dynamics, LLC**.

If you're caring for a parent, a spouse, a child, or anyone who depends on
you, you know how hard it can be to find help. This directory gathers free,
official resources in one place, grouped by what you need right now:

- **Respite care** — a short break so you can rest or run errands
- **Support groups** — people who understand what you're going through
- **Benefit guides** — Medicare, Medicaid, Social Security, veterans benefits
- **Legal aid** — powers of attorney, advance directives, guardianship, appeals

Every link points to an official source: a government agency, a national
nonprofit, or a recognized advocacy organization. No link shorteners, no
tracking scripts, no personal data collected.

## Who built this

This directory was created by **Asdale Dynamics, LLC**, the publisher behind
*The Massive AI Manual* and dylanasdale.github.io, which explain AI "like a
friend would": plain English, step by step, never condescending.

Dylan Asdale, founder of Asdale Dynamics, LLC, is a registered nurse turned AI
author based in Indiana. He builds clear, warm, tested tools like this one.

## Run it

No server needed — just open the page in a browser:

```bash
# 1. Build the site from the Markdown content
python3 build.py

# 2. Open the result
open index.html
```

That's it. `build.py` reads the Markdown files in `content/` and generates
`index.html` (the page) and `resources.json` (the search index). Open
`index.html` and use the search box to filter by keyword — all in your
browser, nothing sent anywhere.

If you'd rather run a local server:

```bash
python3 -m http.server 8080
# then visit http://localhost:8080/index.html
```

## Test it

```bash
python3 test_build.py
```

14 tests pass: every content file parses, every resource has at least one
official link, all links are http(s) URLs, and the generated HTML matches the
data.

## Edit the content

Resources live as plain Markdown in `content/`, one file per group:

| File | Group |
|------|-------|
| `content/01-respite-care.md` | Respite care |
| `content/02-support-groups.md` | Support groups |
| `content/03-benefit-guides.md` | Benefit guides |
| `content/04-legal-aid.md` | Legal aid |

Each resource is a `## Title` block with `- **What it is:**`,
`- **Official link:**` (one or more URLs), and `- **Use for:**` lines. After
editing, run `python3 build.py` again.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

## Credit

Created by Asdale Dynamics, LLC.