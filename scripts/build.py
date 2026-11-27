#!/usr/bin/env python3
"""Embed data/sites.json into index.html and copy it into the skill folder.

Run after editing data/sites.json:  python3 scripts/build.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "sites.json"
PAGE = ROOT / "index.html"
SKILL_DATA = ROOT / "skill" / "look-like-ai-no-more" / "sites.json"

REQUIRED = {"id", "name", "url", "type", "platforms", "occupations", "styles", "pricing", "tech", "description"}

sites = json.loads(DATA.read_text())
ids, urls = set(), set()
for s in sites:
    missing = REQUIRED - s.keys()
    if missing:
        raise SystemExit(f"{s.get('name', '?')}: missing {sorted(missing)}")
    if s["id"] in ids or s["url"] in urls:
        raise SystemExit(f"duplicate: {s['name']}")
    ids.add(s["id"])
    urls.add(s["url"])

blob = json.dumps(sites, separators=(",", ":")).replace("</", "<\\/")
html = PAGE.read_text()
html, n = re.subn(
    r'(<script id="data" type="application/json">)/\*DATA\*/.*?/\*END\*/(</script>)',
    lambda m: f"{m.group(1)}/*DATA*/{blob}/*END*/{m.group(2)}",
    html,
    flags=re.S,
)
if n != 1:
    raise SystemExit("index.html: data markers not found")
PAGE.write_text(html)

SKILL_DATA.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(DATA, SKILL_DATA)
shutil.copyfile(PAGE, SKILL_DATA.parent / "catalog.html")
print(f"{len(sites)} sites -> {PAGE.name}, skill/.../sites.json and skill/.../catalog.html")
