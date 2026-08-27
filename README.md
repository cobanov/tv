# tv.cobanov.dev

Android TV'yi ADB üzerinden temizlemek için tek sayfalık Türkçe rehber ve
Claude Code / Codex'e yapıştırılacak hazır prompt.

Canlı: https://tv.cobanov.dev

## Yapı

| Dosya | Ne |
|---|---|
| `index.template.html` | Sayfanın kaynağı. `__PROMPT__` yer tutucusuna prompt gömülür. |
| `prompt.txt` | Prompt'un tek kaynağı. Değiştirince `./build.sh` çalıştır. |
| `assets/site.css` | Tüm stil. |
| `assets/og.html` | OG görselinin kaynağı (headless Chrome ile PNG'ye çevriliyor). |
| `assets/og.png` | 1200x630 sosyal medya önizlemesi. |
| `build.sh` | `public/` klasörünü üretir. |

## Geliştirme

```sh
./build.sh
open public/index.html
```

OG görselini yeniden üretmek için:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --hide-scrollbars --window-size=1200,630 \
  --screenshot=assets/og.png assets/og.html
```

## Yayınlama

Cloudflare Pages projesi: `tv`

```sh
./build.sh
wrangler pages deploy public --project-name tv --branch main
```
