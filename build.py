#!/usr/bin/env python3
"""index.template.html + i18n/<kod>.json + prompts/<kod>.txt -> public/

Diller tek sablondan uretiliyor. Sablondaki {{anahtar}} yer tutuculari once
hesaplanan alanlarla (canonical, hreflang listesi, dil menusu, adimlar), sonra
JSON'daki duz metinlerle doluyor.
"""

import html
import json
import pathlib
import shutil

SITE = "https://tv.cobanov.dev"
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "public"

# Menudeki sira. Ingilizce ilk: varsayilan dil o. Gerisi kullanicinin istedigi
# sirada; her ad kendi dilinde yazildigi icin alfabetik siralamanin karsiligi
# yok.
ORDER = ["en", "tr", "fr", "es", "de", "it", "ru", "ja", "ar", "zh"]

# Sosyal medya gorseli icin sunum ayarlari. Metnin uzunlugu ve yazinin genisligi
# dilden dile degistigi icin baslik puntosu sabit olamiyor.
OG_FONT_DEFAULT = '-apple-system, "SF Pro Display", system-ui, sans-serif'

# (yazi tipi, baslik puntosu, baslik genisligi, harf araligi). ch birimi Latin
# "0" genisligine dayaniyor, o yuzden CJK basliga dar geliyor; sikistirilmis
# aralik da yalnizca Latin harfte dogru duruyor.
OG = {
    "en": (OG_FONT_DEFAULT, "82px", "17ch", "-0.035em"),
    "tr": (OG_FONT_DEFAULT, "82px", "17ch", "-0.035em"),
    "fr": (OG_FONT_DEFAULT, "72px", "17ch", "-0.035em"),
    "es": (OG_FONT_DEFAULT, "78px", "17ch", "-0.035em"),
    "de": (OG_FONT_DEFAULT, "70px", "17ch", "-0.035em"),
    "it": (OG_FONT_DEFAULT, "74px", "17ch", "-0.035em"),
    "ru": (OG_FONT_DEFAULT, "70px", "17ch", "-0.02em"),
    "ja": ('"Hiragino Sans", "Yu Gothic", ' + OG_FONT_DEFAULT, "66px", "24ch", "normal"),
    "ar": ('"SF Arabic", "Geeza Pro", ' + OG_FONT_DEFAULT, "76px", "20ch", "normal"),
    "zh": ('"PingFang SC", "Hiragino Sans GB", ' + OG_FONT_DEFAULT, "80px", "20ch", "normal"),
}


def load(code):
    d = json.loads((ROOT / "i18n" / f"{code}.json").read_text(encoding="utf-8"))
    # zh gibi yazi varyanti olan dillerde <html lang> ve hreflang, URL'deki
    # kisa koddan ayrilir.
    d.setdefault("lang", d["code"])
    return d


LANGS = [load(c) for c in ORDER]


def fill(tpl, values):
    for key, value in values.items():
        tpl = tpl.replace("{{" + key + "}}", value)
    return tpl


def render(cur, tpl):
    # Kokteki sayfa icin "", alt dizinler icin "../". Mutlak yol yerine bunu
    # kullanmak, public/ klasorunu sunucusuz, dosyadan acmayi da calisir
    # tutuyor.
    base = "" if cur["path"] == "/" else "../"

    hreflangs = [
        f'    <link rel="alternate" hreflang="{l["lang"]}" href="{SITE}{l["path"]}" />'
        for l in LANGS
    ]
    hreflangs.append(f'    <link rel="alternate" hreflang="x-default" href="{SITE}/" />')

    items = []
    for l in LANGS:
        href = base + l["path"].lstrip("/") or "./"
        current = ' aria-current="true"' if l["code"] == cur["code"] else ""
        items.append(
            f'              <li><a href="{href}" lang="{l["lang"]}" '
            f'hreflang="{l["lang"]}"{current}>{l["name"]}</a></li>'
        )

    steps = [
        f"""            <li class="step">
              <h3>{s["h3"]}</h3>
              <p>{s["p"]}</p>
            </li>"""
        for s in cur["steps"]
    ]

    warnings = [
        f"""          <div class="note">
            <p>
              <strong>{w["strong"]}</strong>
              {w["p"]}
            </p>
          </div>"""
        for w in cur["warnings"]
    ]

    prompt = (ROOT / "prompts" / f"{cur['code']}.txt").read_text(encoding="utf-8")

    computed = {
        "code": cur["lang"],
        "base": base,
        "canonical": SITE + cur["path"],
        "og_image": f"{SITE}/assets/og-{cur['code']}.png",
        "hreflangs": "\n".join(hreflangs),
        "lang_items": "\n".join(items),
        "steps": "\n".join(steps),
        "warnings": "\n".join(warnings),
        "prompt": html.escape(prompt.rstrip("\n"), quote=False),
    }

    # Once hesaplananlar, sonra JSON'daki duz metinler. JSON degerleri HTML
    # parcasi icerebiliyor (<strong>, <code>) ve kacisa ugramiyor; prompt ise
    # tek kacisi gereken alan ve yukarida escape edildi.
    page = fill(tpl, computed)
    page = fill(page, {k: v for k, v in cur.items() if isinstance(v, str)})

    out_dir = OUT / cur["path"].strip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    shutil.copy(ROOT / "prompts" / f"{cur['code']}.txt", out_dir / "prompt.txt")

    leftover = [m for m in ("{{",) if m in page]
    if leftover:
        raise SystemExit(f"{cur['code']}: sablonda doldurulmamis yer tutucu kaldi")


def main():
    tpl = (ROOT / "index.template.html").read_text(encoding="utf-8")
    for cur in LANGS:
        render(cur, tpl)

    # Ingilizce /en/ altindaydi ve o adresler paylasildi. Kalici yonlendirme
    # onlari yeni koke tasiyor; /en/prompt.txt de /prompt.txt oluyor.
    (OUT / "_redirects").write_text(
        "# Ingilizce /en/ iken paylasilan adresler artik kokte.\n"
        "/en /  301\n"
        "/en/* /:splat  301\n",
        encoding="utf-8",
    )

    # OG sablonu Chrome'a verilecek; ciktinin kendisi public/ disinda kaliyor.
    og_tpl = (ROOT / "assets" / "og.template.html").read_text(encoding="utf-8")
    og_dir = ROOT / ".og"
    og_dir.mkdir(exist_ok=True)
    for cur in LANGS:
        font, size, width, tracking = OG[cur["code"]]
        values = {k: v for k, v in cur.items() if isinstance(v, str)}
        values.update({
            "code": cur["lang"],
            "og_font": font,
            "og_h1_size": size,
            "og_h1_width": width,
            "og_h1_tracking": tracking,
        })
        (og_dir / f"{cur['code']}.html").write_text(fill(og_tpl, values), encoding="utf-8")


if __name__ == "__main__":
    main()
