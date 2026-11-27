---
name: look-like-ai-no-more
description: Pull real design references from a curated, tagged catalog of 200 inspiration galleries, component libraries, prompt libraries (MotionSites-style), templates, design systems, fonts, colours, icons and motion tools for websites, web apps and mobile apps, filterable by occupation/industry, style, platform, price and tech. Use before designing or building any landing page, website, web app, dashboard or mobile app UI, when the user wants something that does not look AI-generated, asks for design inspiration, references, components, or "sites like motionsites.ai", or names an industry (restaurant, SaaS, law firm, portfolio...) or a style (brutalist, editorial, minimal, 3D, motion...).
---

# Look Like AI No More

Generic AI UI is easy to spot: a centred hero with a purple-to-blue gradient, Inter everywhere,
three identical feature cards with emoji icons, glass cards on a dark mesh background, unDraw
people, "Get started" + "Learn more" buttons. This skill fixes that by grounding every design in
real references chosen for the user's **platform**, **industry** and **style**.

The catalog is `sites.json` next to this file, and `search.py` queries it. `catalog.html` is the
same data as a searchable, filterable page for people (open it in a browser, or serve the folder
with `python3 -m http.server`).

## Workflow

1. **Pin down the brief.** From the request (ask only if truly unknown):
   - platform: `website`, `web-app`, `mobile`
   - occupation / industry, e.g. `restaurant`, `saas`, `legal`, `portfolio`
   - style, e.g. `editorial`, `brutalist`, `minimal`, `motion`, `3d`, `luxury`, `retro`
   - tech, e.g. `react`, `tailwind`, `shadcn`, `react-native`, `flutter`, `swiftui`, `framer`, `webflow`
2. **Search the catalog.** See every valid value with:
   ```bash
   python3 ~/.claude/skills/look-like-ai-no-more/search.py --facets
   ```
   Then combine filters (values in one flag are ORed, different flags are ANDed; general-purpose
   entries, meaning occupation `all` or style `mixed`, still match and rank below specific ones
   unless you pass `--specific-only`):
   ```bash
   python3 ~/.claude/skills/look-like-ai-no-more/search.py --platform website --occupation restaurant --style editorial --limit 15
   python3 ~/.claude/skills/look-like-ai-no-more/search.py hero --type inspiration,prompt-library --pricing free
   python3 ~/.claude/skills/look-like-ai-no-more/search.py --platform mobile --type components --tech react-native
   ```
   If the skill folder lives elsewhere, run `search.py` from this file's directory.
3. **Pick a small, varied set**: 2–3 inspiration galleries (industry-specific ones first), 1–2
   component or animation libraries that match the tech, and 1 font + 1 colour source.
4. **Study before building.** Open the most relevant galleries (WebFetch or the browser) and note
   concrete moves from 3–5 real sites: layout grid, type pairing, colour ratio, image treatment,
   motion, section order. Never copy one site wholesale.
5. **Write a short design brief** before code: typefaces (avoid defaulting to Inter/Roboto; check
   Typewolf, Fonts In Use, Fontshare), a palette with one confident accent, layout rhythm, the one
   signature detail, motion rules, and which components come from where.
6. **Build**, then check it against the "AI tells" list below and fix any you hit.

## AI tells to avoid

- Purple/indigo/blue gradients and glowing blobs with no reason to exist
- Everything centred; every section the same width and padding
- Three or four identical cards with icon + title + two lines
- Emoji or generic line icons as the main visual
- Inter/system font only, uniform weights, no typographic contrast
- Stock illustration packs used unedited; fake dashboards with lorem metrics
- Glassmorphism and gradient borders on everything
- Vague copy ("Unlock the power of...", "Seamless", "Revolutionize")

Instead use real photography or product shots, an asymmetric grid, a distinctive type pairing,
industry-specific content, and one deliberate motion idea.

## Catalog fields

Each entry has `id`, `name`, `url`, `type`, `platforms[]`, `occupations[]` (`all` means general),
`styles[]` (`mixed` means varied), `pricing` (`free` | `freemium` | `paid`), `tech[]` and
`description`.

Types: `prompt-library`, `ai-builder`, `inspiration`, `ux-patterns`, `components`, `templates`,
`design-system`, `animation`, `backgrounds`, `ui-kit`, `fonts`, `colors`, `icons`,
`illustrations`, `photos`, `mockups`.

## Adding sites

The source of truth is `data/sites.json` in the LookLikeAiNoMore project. Add an entry there with
the fields above, using existing tag values where possible, check the URL loads, then run
`python3 scripts/build.py` to refresh the browsable `index.html` and this skill's copy.
