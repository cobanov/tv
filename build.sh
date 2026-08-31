#!/bin/sh
# Kaynak: index.template.html   tek sayfa sablonu, {{...}} yer tutuculu
#         i18n/<kod>.json       o dilin butun metinleri
#         prompts/<kod>.txt     o dilin prompt'u, sayfaya gomuluyor
#         assets/               stil ve sosyal medya gorselleri
# Cikti:  public/               Cloudflare Pages bunu yayinliyor
#
# Ingilizce kokte (/), diger diller /<kod>/ altinda.
# Sosyal medya gorsellerini uretmek icin ayri script: ./og.sh
set -e
rm -rf public
mkdir -p public/assets
python3 build.py
cp assets/site.css public/assets/
cp assets/og-*.png public/assets/
# Ingilizce koke tasinmadan once paylasilan kartlar bu adrese bakiyor.
cp assets/og-en.png public/assets/og.png
echo "public/ hazir:"
find public -type f | sort
