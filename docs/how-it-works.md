# How Look Like AI No More works

## Layout

| Path | What it is |
|---|---|
| `data/sites.json` | Source of truth: every entry and its tags |
| `index.html` | The catalog page, with the data embedded (GitHub Pages serves it as-is) |
| `scripts/build.py` | Validates the data, embeds it in `index.html`, copies it into the skill |
| `skill/look-like-ai-no-more/` | The Claude Code skill: `SKILL.md`, `search.py`, `sites.json`, `catalog.html` |
| `scripts/render-assets.sh`, `scripts/art/` | README images (headless Chrome) |

## An entry

```json
{
  "id": "typewolf",
  "name": "Typewolf",
  "url": "https://www.typewolf.com",
  "type": "inspiration",
  "platforms": ["website"],
  "occupations": ["all"],
  "styles": ["editorial"],
  "pricing": "freemium",
  "tech": [],
  "description": "Sites of the day chosen for typography, with the fonts named. Key for not looking generic."
}
```

- `type` is one of 16: `prompt-library`, `ai-builder`, `inspiration`, `ux-patterns`, `components`, `templates`,
  `design-system`, `animation`, `backgrounds`, `ui-kit`, `fonts`, `colors`, `icons`, `illustrations`, `photos`,
  `mockups`.
- `occupations: ["all"]` marks a general resource; `styles: ["mixed"]` marks one with varied styles.
- `pricing` is `free`, `freemium` or `paid`.

## The build

`scripts/build.py` checks that every entry has all the required fields and that ids and URLs are unique, then
replaces the JSON between `/*DATA*/` and `/*END*/` in `index.html` and writes the skill's `sites.json` and
`catalog.html`. There's no bundler and nothing to install.

## The page

Everything runs in one inline script:

- **State in the URL.** Search text, sort, the "include general" switch and every filter are kept in the hash
  (`#platforms=website&occupations=restaurant&styles=editorial`), so a link reproduces the view exactly.
- **Matching.** OR inside a filter group, AND across groups. General entries (`all` / `mixed`) match occupation
  and style filters unless that switch is off.
- **Search.** Every word must appear in the name, description, URL or tags. Ranking: +5 for a word in the name,
  +1 otherwise, +3 when a word is exactly an occupation, style or type.
- **Counts.** Each filter chip shows how many results it would give with the other filters applied.
- **Copy as AI brief** writes the current filters and results as a plain-text prompt to the clipboard.
- **Theme.** Follows the system setting; the button cycles auto, light and dark.

## The skill

`SKILL.md` tells Claude, before building any UI, to:

1. Pin down platform, industry, style and tech.
2. Search with `search.py` (same matching rules as the page; `--specific-only` drops general entries).
3. Pick a small, varied set: 2–3 galleries, 1–2 component or animation libraries for the tech, one font and one
   colour source.
4. Study 3–5 real sites for concrete moves, without copying any one.
5. Write a short design brief before code.
6. Build, then check the result against the list of **AI tells** and fix any it hits.

## README images

`scripts/render-assets.sh` opens `index.html` in headless Chrome with a filter in the URL hash and takes 1440×900
screenshots in light and dark mode, then six frames with filters being added for `demo.gif` (`scripts/make-gif.py`,
Pillow). The icon and hero are HTML pages in `scripts/art/`, rendered by the same browser in the page's own fonts
and colours.
