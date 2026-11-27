#!/bin/bash
# Renders every README image into docs/images/ from the real catalog page, with headless Chrome:
#   catalog-light.png / catalog-dark.png   the page with a filter applied through its shareable URL
#   demo.gif                               filters being added one at a time
#   icon.png, hero.png                     drawn from scripts/art/*.html
# Run from anywhere: scripts/render-assets.sh   (needs Google Chrome or Chromium, Python 3 with Pillow, internet
# for the Google Fonts the page uses)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=docs/images; mkdir -p "$OUT"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
CHROME=${CHROME:-$(command -v chromium || command -v google-chrome || echo "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")}
PAGE="file://$PWD/index.html"

shot() {  # shot OUT.png WIDTHxHEIGHT URL [extra chrome flags...]
  local out=$1 size=$2 url=$3; shift 3
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run --user-data-dir="$TMP/profile" \
    --window-size="${size/x/,}" --virtual-time-budget=6000 --default-background-color=00000000 \
    --screenshot="$out" "$@" "$url" > /dev/null 2>&1
  [ -s "$out" ] || { echo "failed: $out" >&2; exit 1; }
  echo "rendered $(basename "$out")"
}

FILTER="#platforms=website&occupations=restaurant&styles=editorial"
shot "$OUT/catalog-light.png" 1440x900 "$PAGE$FILTER" --blink-settings=preferredColorScheme=1
shot "$OUT/catalog-dark.png"  1440x900 "$PAGE$FILTER" --force-dark-mode --blink-settings=preferredColorScheme=0

i=0
for h in "" "#platforms=website" "#platforms=website&occupations=restaurant" "$FILTER" "$FILTER&type=fonts,colors" "#platforms=mobile"; do
  shot "$TMP/f$i.png" 1440x900 "$PAGE$h" --blink-settings=preferredColorScheme=1; i=$((i + 1))
done
python3 -I scripts/make-gif.py "$OUT/demo.gif" 900 1.4 "$TMP"/f{0,1,2,3,4,5}.png

shot "$OUT/icon.png" 1024x1024 "file://$PWD/scripts/art/icon.html"
cp "$OUT/icon.png" "$OUT/catalog-light.png" "$TMP/" && cp scripts/art/hero.html "$TMP/" && mv "$TMP/catalog-light.png" "$TMP/shot.png"
shot "$OUT/hero.png" 1920x1080 "file://$TMP/hero.html"
ls -la "$OUT"
