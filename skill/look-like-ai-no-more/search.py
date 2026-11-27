#!/usr/bin/env python3
"""Search the Look Like AI No More catalog.

Examples:
  search.py --facets
  search.py --platform website --occupation restaurant --style editorial
  search.py hero sections --type inspiration --pricing free --limit 10
  search.py --platform mobile --type components --tech react-native --json
"""
import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "sites.json"
FIELDS = {
    "platform": "platforms",
    "occupation": "occupations",
    "style": "styles",
    "type": "type",
    "pricing": "pricing",
    "tech": "tech",
}


def values(entry, key):
    v = entry[key]
    return v if isinstance(v, list) else [v]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*", help="free-text words; all must match")
    for flag in FIELDS:
        ap.add_argument(f"--{flag}", action="append", default=[], help="repeat or comma-separate to OR values")
    ap.add_argument("--specific-only", action="store_true", help="drop general-purpose entries (occupation 'all', style 'mixed') when filtering by occupation or style")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--facets", action="store_true", help="list every filter value with counts")
    a = ap.parse_args()

    sites = json.loads(DATA.read_text())

    if a.facets:
        for flag, key in FIELDS.items():
            counts = {}
            for s in sites:
                for v in values(s, key):
                    counts[v] = counts.get(v, 0) + 1
            print(f"{flag}: " + ", ".join(f"{k} ({n})" for k, n in sorted(counts.items(), key=lambda x: -x[1])))
        return

    want = {key: {v.strip() for raw in getattr(a, flag) for v in raw.split(",") if v.strip()} for flag, key in FIELDS.items()}
    terms = [t.lower() for t in a.query]
    results = []
    for s in sites:
        score = 1
        ok = True
        for key, sel in want.items():
            if not sel:
                continue
            v = values(s, key)
            if any(x in sel for x in v):
                if key in ("occupations", "styles"):
                    score += 10
            elif not a.specific_only and ((key == "occupations" and "all" in v) or (key == "styles" and "mixed" in v)):
                pass
            else:
                ok = False
                break
        if not ok:
            continue
        hay = " ".join([s["name"], s["description"], s["url"], s["type"], *s["platforms"], *s["occupations"], *s["styles"], *s["tech"]]).lower()
        if any(t not in hay for t in terms):
            continue
        score += sum(5 if t in s["name"].lower() else 1 for t in terms)
        results.append((score, s))

    results.sort(key=lambda r: (-r[0], r[1]["name"].lower()))
    picked = [s for _, s in results[: a.limit]]
    if a.json:
        print(json.dumps(picked, indent=1))
        return
    print(f"{len(results)} matches (showing {len(picked)})")
    for s in picked:
        occ = "general" if "all" in s["occupations"] else ",".join(s["occupations"][:4])
        print(f"- {s['name']} <{s['url']}> [{s['type']}; {s['pricing']}; {','.join(s['platforms'])}; {occ}; {','.join(s['styles'])}]\n    {s['description']}")


if __name__ == "__main__":
    main()
