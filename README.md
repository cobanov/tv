# tv.cobanov.dev

Android TV'yi ADB üzerinden temizlemek için tek sayfalık rehber ve yapay zekâ
ajanına yapıştırılacak hazır prompt. On dilde.

Canlı: https://tv.cobanov.dev

## Diller

Varsayılan dil İngilizce ve kökte duruyor. Diğerleri `/<kod>/` altında.

| Dil | Yol | Dil | Yol |
|---|---|---|---|
| English | `/` | Italiano | `/it/` |
| Türkçe | `/tr/` | Русский | `/ru/` |
| Français | `/fr/` | 日本語 | `/ja/` |
| Español | `/es/` | العربية | `/ar/` |
| Deutsch | `/de/` | 简体中文 | `/zh/` |

İngilizce eskiden `/en/` altındaydı. `public/_redirects` o adresleri köke 301
ile taşıyor, eski bağlantılar kırılmıyor.

## Yapı

| Dosya | Ne |
|---|---|
| `index.template.html` | Tek sayfa şablonu. `{{anahtar}}` yer tutucuları doldurulur. |
| `i18n/<kod>.json` | O dilin bütün metinleri. Değerler HTML parçası içerebilir. |
| `prompts/<kod>.txt` | O dilin prompt'u. Sayfaya gömülür, ayrıca `prompt.txt` olarak yayınlanır. |
| `assets/site.css` | Tüm stil. Arapça için mantıksal özellikler, CJK ve Arapça için dile göre yazı tipi. |
| `assets/og.template.html` | Sosyal medya görselinin kaynağı. |
| `assets/og-<kod>.png` | 1200x630 sosyal medya önizlemesi, dil başına bir tane. |
| `build.py` | `public/` klasörünü üretir. |
| `build.sh` | `build.py` + dosya kopyalama. |
| `og.sh` | Sosyal medya görsellerini headless Chrome ile yeniden üretir. |

## Yeni dil ekleme

1. `i18n/<kod>.json` yaz. Mevcut bir dili kopyalayıp çevirmek en hızlısı;
   `path`, `name`, `og_locale` ve `dir` alanlarını unutma.
2. `prompts/<kod>.txt` yaz.
3. `build.py` içindeki `ORDER` listesine kodu ekle, `OG` sözlüğüne de bir satır
   (yazı tipi, başlık puntosu, başlık genişliği, harf aralığı).
4. `./build.sh && ./og.sh`

Sağdan sola yazılan bir dil eklerken JSON'da `"dir": "rtl"` yeter; stil zaten
mantıksal özelliklerle yazıldı.

## Geliştirme

```sh
./build.sh
cd public && python3 -m http.server 8899
```

Sayfalar arası bağlantılar göreli, yani `public/index.html` dosyadan da açılır;
ama `_redirects` yalnızca Cloudflare'de çalışır.

Sosyal medya görsellerini yeniden üretmek için (macOS, Chrome gerekir):

```sh
./build.sh && ./og.sh
```

## Yayınlama

Cloudflare Pages projesi: `tv`

```sh
./build.sh
wrangler pages deploy public --project-name tv --branch main
```
