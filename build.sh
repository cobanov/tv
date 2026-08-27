#!/bin/sh
# Kaynak: index.template.html + prompt.txt + assets/
# Cikti:  public/  (Cloudflare Pages bunu yayinliyor)
set -e
rm -rf public
mkdir -p public/assets
python3 - <<'PY'
import html
tpl = open('index.template.html', encoding='utf-8').read()
prompt = open('prompt.txt', encoding='utf-8').read().rstrip('\n')
open('public/index.html', 'w', encoding='utf-8').write(tpl.replace('__PROMPT__', html.escape(prompt, quote=False)))
PY
cp prompt.txt public/prompt.txt
cp assets/site.css assets/og.png public/assets/
echo "public/ hazir:"
find public -type f | sort
