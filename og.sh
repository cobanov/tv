#!/bin/sh
# Sosyal medya gorsellerini yeniden uretir: her dil icin assets/og-<kod>.png.
# Once ./build.sh calistir, .og/ altindaki HTML'leri o hazirliyor.
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -d .og ] || { echo "once ./build.sh calistir"; exit 1; }
for f in .og/*.html; do
  code=$(basename "$f" .html)
  "$CHROME" --headless --disable-gpu --hide-scrollbars \
    --window-size=1200,630 --default-background-color=00000000 \
    --screenshot="assets/og-$code.png" "$f" 2>/dev/null
  echo "assets/og-$code.png"
done
