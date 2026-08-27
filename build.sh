#!/bin/sh
# Kaynak: index.template.html + prompt.txt (TR)
#         index.en.template.html + prompt.en.txt (EN)
#         assets/
# Cikti:  public/  (Cloudflare Pages bunu yayinliyor)
set -e
rm -rf public
mkdir -p public/assets public/en
python3 - <<'PY'
import html

def render(tpl_path, prompt_path, out_path):
    tpl = open(tpl_path, encoding='utf-8').read()
    prompt = open(prompt_path, encoding='utf-8').read().rstrip('\n')
    open(out_path, 'w', encoding='utf-8').write(
        tpl.replace('__PROMPT__', html.escape(prompt, quote=False)))

render('index.template.html',    'prompt.txt',    'public/index.html')
render('index.en.template.html', 'prompt.en.txt', 'public/en/index.html')
PY
cp prompt.txt    public/prompt.txt
cp prompt.en.txt public/en/prompt.txt
cp assets/site.css assets/og.png assets/og-en.png public/assets/
echo "public/ hazir:"
find public -type f | sort
