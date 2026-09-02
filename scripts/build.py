#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""流涟旅拍官网 · 静态生成器(L2,幂等)
中英两套页面 + 图片来源页,由 scripts/content.py 的同一份内容模型渲染。
画廊与十地面板来自 photos/index.json(scripts/ingest.py / fetch_placeholders.py 写入);
没有照片的图位渲染为统一占位,入库后零改结构。
地图:Natural Earth 1:10m Admin-1(公有领域)经 mapshaper 简化,见 scripts/mapdata.json。
"""
import json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from content import CITIES, TYPES, T, EMAIL, LABELS  # noqa: E402

HILITE = sorted({p for _, _, _, prefs, *_ in CITIES for p in prefs})


def load_photos():
    p = os.path.join(ROOT, "photos", "index.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def obfuscate(addr):
    """邮箱轻度实体混淆,防最粗的采集。"""
    return "".join("&#%d;" % ord(c) for c in addr)


def svg_map(loc):
    md = json.load(open(os.path.join(ROOT, "scripts", "mapdata.json")))
    lands, hits = [], []
    for name, d in md["prefs"].items():
        cls = "pref hl" if name in HILITE else "pref"
        lands.append('<path class="%s" d="%s"/>' % (cls, d))
    for slug, zh, en, prefs, *_ in CITIES:
        x, y = md["cities"][slug]
        lx, ly, anchor = LABELS[slug]
        name = zh if loc == "zh" else en
        # 引线:标点 → 标签锚点(近处不画)
        need_line = abs(lx - x) > 18 or abs(ly - y) > 18
        line = ('<line class="lead" x1="%s" y1="%s" x2="%s" y2="%s"/>'
                % (x, y, lx, ly)) if need_line else ""
        hits.append(
            '<a href="#pn-%s" class="mappin" aria-label="%s">'
            '<title>%s</title>%s'
            '<circle class="pin-hit" cx="%s" cy="%s" r="34"/>'
            '<circle class="pin" cx="%s" cy="%s" r="6"/>'
            '<text class="plabel" x="%s" y="%s" text-anchor="%s">%s</text></a>'
            % (slug, name, name, line, x, y, x, y, lx, ly, anchor, name))
    aria = "日本拍摄地区分布图" if loc == "zh" else "Map of locations across Japan"
    return ('<svg class="jpmap" viewBox="0 0 %s %s" role="img" aria-label="%s" '
            'xmlns="http://www.w3.org/2000/svg">%s%s</svg>'
            % (md["w"], md["h"], aria, "".join(lands), "".join(hits)))


def has_placeholder(photos):
    return any(it.get("placeholder") for v in photos.values() for it in v)


def picture(loc, folder, it, size, alt, eager=False, sizes_attr=None):
    d = T[loc]["dir"]
    lz = '' if eager else ' loading="lazy"'
    dims = {"2000": (it["fw"], it["fh"]), "800": (it["tw"], it["th"]),
            "400": (it.get("gw", it["tw"]), it.get("gh", it["th"]))}
    w, h = dims[size]
    base = "%sphotos/%s/%s" % (d, folder, it["id"])
    if sizes_attr:
        # 响应式:窄屏取 800,宽屏取 2000
        return ('<picture>'
                '<source type="image/webp" srcset="%s-800.webp %dw, %s-2000.webp %dw" sizes="%s">'
                '<img src="%s-2000.jpg" srcset="%s-800.jpg %dw, %s-2000.jpg %dw" sizes="%s" '
                'alt="%s"%s decoding="async" width="%d" height="%d" fetchpriority="high"></picture>'
                % (base, it["tw"], base, it["fw"], sizes_attr,
                   base, base, it["tw"], base, it["fw"], sizes_attr,
                   html.escape(alt), lz, w, h))
    return ('<picture><source srcset="%s-%s.webp" type="image/webp">'
            '<img src="%s-%s.jpg" alt="%s"%s decoding="async" '
            'width="%d" height="%d"></picture>'
            % (base, size, base, size, html.escape(alt), lz, w, h))


def slot(loc, folder, photos, cls="", alt="", size="800", eager=False, sizes_attr=None):
    items = photos.get(folder, [])
    if items:
        return '<div class="slot %s">%s</div>' % (cls, picture(loc, folder, items[0], size, alt, eager, sizes_attr))
    return ('<div class="slot slot-ph %s" role="img" aria-label="%s">%s</div>'
            % (cls, T[loc]["ph_photo"], T[loc]["ph_photo"]))


def gallery(loc, photos):
    """作品网格:每地取前 2 张;灯箱页收全部入库照片。"""
    flat = []
    for slug, zh, en, *_ in CITIES:
        for it in photos.get(slug, []):
            flat.append((slug, zh if loc == "zh" else en, it))
    if not flat:
        cells = "".join('<div class="slot slot-ph" role="img" aria-label="%s">%s</div>'
                        % (T[loc]["ph_photo"], T[loc]["ph_photo"]) for _ in range(8))
        return '<div class="grid">%s</div>' % cells, ""
    per, seen = {}, []
    for slug, place, it in flat:
        per.setdefault(slug, 0)
        if per[slug] < 2:
            per[slug] += 1
            seen.append((slug, place, it))
    cells = []
    for slug, place, it in seen:
        pid = "p-%s" % it["id"]
        cells.append('<a class="slot" href="#%s" aria-label="%s">%s</a>'
                     % (pid, place, picture(loc, slug, it, "400", place)))
    boxes = lightboxes(loc, flat)
    return '<div class="grid">%s</div>' % "".join(cells), boxes


def lightboxes(loc, flat):
    n = len(flat)
    out = []
    for i, (folder, place, it) in enumerate(flat):
        pid = "p-%s" % it["id"]
        prv = "p-%s" % flat[(i - 1) % n][2]["id"]
        nxt = "p-%s" % flat[(i + 1) % n][2]["id"]
        out.append('<figure class="lb" id="%s"><a class="lb-x" href="#gallery" aria-label="%s">✕</a>'
                   '%s<figcaption>%s</figcaption>'
                   '<div class="lb-nav"><a class="lb-prev" href="#%s" aria-label="%s">←</a>'
                   '<a class="lb-next" href="#%s" aria-label="%s">→</a></div></figure>'
                   % (pid, T[loc]["lb_close"], picture(loc, folder, it, "2000", place),
                      place, prv, T[loc]["lb_prev"], nxt, T[loc]["lb_next"]))
    return "".join(out)


def panels(loc, photos):
    """十地面板::target 打开(禁 JS 可用),JS 增强为模态。"""
    t = T[loc]
    out = []
    for slug, zh, en, prefs, czh, szh, cen, sen in CITIES:
        name = zh if loc == "zh" else en
        cul = czh if loc == "zh" else cen
        sho = szh if loc == "zh" else sen
        items = photos.get(slug, [])
        if items:
            shots = "".join('<a class="pslot" href="#p-%s" aria-label="%s">%s</a>'
                            % (it["id"], name, picture(loc, slug, it, "800", name))
                            for it in items)
            strip = '<div class="pstrip">%s</div>' % shots
        else:
            strip = ('<div class="pstrip"><div class="slot slot-ph pslot" role="img" '
                     'aria-label="%s">%s</div></div>' % (t["ph_photo"], t["ph_photo"]))
        note = ('<p class="phnote">%s</p>' % t["ph_note"]) \
            if any(it.get("placeholder") for it in items) else ""
        out.append(
          '<section class="panel" id="pn-%s" role="dialog" aria-modal="false" aria-label="%s">'
          '<div class="pbox">'
          '<header class="phead"><h3>%s</h3>'
          '<a class="pclose" href="#areas" aria-label="%s">✕</a></header>'
          '%s%s'
          '<div class="pbody">'
          '<h4>%s</h4><p>%s</p>'
          '<h4>%s</h4><p>%s</p>'
          '<p class="pbook"><a href="#contact">%s</a></p>'
          '</div></div>'
          '<a class="pmask" href="#areas" aria-hidden="true"></a>'
          '</section>'
          % (slug, name, name, t["panel_close"], strip, note,
             t["panel_h_cul"], cul, t["panel_h_shoot"], sho, t["panel_book"]))
    return "".join(out)


def render(loc):
    t = T[loc]
    d = t["dir"]
    photos = load_photos()
    nav = '<span class="secnav">%s</span>' % "".join(
        '<a href="%s">%s</a>' % (h, x) for h, x in t["nav"])
    grid, boxes = gallery(loc, photos)
    gnote = ('<p class="phnote">%s</p>' % t["ph_note"]) if has_placeholder(photos) else ""

    chips = "".join('<a class="chip" href="#pn-%s">%s</a>'
                    % (slug, (zh if loc == "zh" else en))
                    for slug, zh, en, *_ in CITIES)

    types_html = "".join(
        '<div class="type">%s<b>%s</b><p>%s</p></div>'
        % (slot(loc, slug, photos, alt=(zh if loc == "zh" else en), size="400"),
           zh if loc == "zh" else en, dzh if loc == "zh" else den)
        for slug, zh, en, dzh, den in TYPES)

    about_stats = "".join('<li><b>%s</b>%s</li>' % (a, b) for a, b in t["about"])

    em = obfuscate(EMAIL)
    ccs = ["".join(('<a class="cc cc-mail link-live" href="mailto:%s"><b>%s</b><span>%s</span>'
                    '<span class="mail">%s</span></a>') % (em, t["email_label"], t["email_sub"], em))]
    for key, label, sub in t["contacts"]:
        ccs.append('<div class="cc link-ph"><b>%s</b><span>%s</span></div>' % (label, sub))

    return """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="format-detection" content="telephone=no">
<meta name="theme-color" content="#FAF8F5">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="alternate" hreflang="{alt_lang}" href="{other}">
<link rel="stylesheet" href="{d}assets/css/site.css">
</head>
<body>
<nav class="top"><div class="wrap topwrap">
  <a class="brand" href="{d}index.html">{brand}</a>
  <div class="topnav">{nav}
    <span class="langsw"><a href="{other}" data-lang="{other_lang}">{other_label}</a></span>
  </div>
</div></nav>
<main>

<section class="hero" id="top"><div class="wrap">
  {hero_shot}
  <h1 class="hero-t">{hero_t}</h1>
  <p class="hero-s">{hero_s}</p>
  <div class="cta">
    <a class="btn btn-1 link-ph" role="link" aria-disabled="true">{cta1}</a>
    <a class="btn btn-2 link-live" href="mailto:{em}">{cta2}</a>
  </div>
</div></section>

<section id="gallery"><div class="wrap">
  <div class="sec-h"><h2>{s2_h}</h2><p>{s2_p}</p></div>
  {grid}{gnote}
</div></section>

<section id="areas"><div class="wrap">
  <div class="sec-h"><h2>{s3_h}</h2><p>{s3_p}</p></div>
  <div class="mapbox">{map}<p class="maplg">{map_lg}</p></div>
  <div class="chips">{chips}</div>
</div></section>

<section id="types"><div class="wrap">
  <div class="sec-h"><h2>{s4_h}</h2><p>{s4_p}</p></div>
  <div class="types">{types}</div>
</div></section>

<section id="about"><div class="wrap">
  <div class="sec-h"><h2>{s5_h}</h2></div>
  <p class="about-p">{about_p}</p>
  <div class="about"><ul>{about_stats}</ul></div>
</div></section>

<section id="contact"><div class="wrap">
  <div class="sec-h"><h2>{s6_h}</h2><p>{s6_p}</p></div>
  <div class="contact">{ccs}</div>
</div></section>

</main>
<footer><div class="wrap foot">
  <div class="langrow"><a href="{d}index.html" data-lang="zh"{cur_zh}>中文</a> · <a href="{d}en/index.html" data-lang="en"{cur_en}>EN</a> · <a href="{d}credits.html">{credits_link}</a></div>
  <div>{foot_c}</div>
  <div>{foot_n}</div>
</div></footer>
{panels}
{boxes}
<script src="{d}assets/js/site.js" defer></script>
</body>
</html>
""".format(lang=t["lang"], desc=html.escape(t["desc"]), title=html.escape(t["title"]),
           other=t["other"], other_label=t["other_label"],
           other_lang=("en" if loc == "zh" else "zh"),
           alt_lang=("en" if loc == "zh" else "zh-Hans"),
           d=d, brand=t["brand"], nav=nav,
           hero_shot=slot(loc, "shouping", photos, cls="hero-shot", alt=t["hero_t"],
                          size="2000", eager=True,
                          sizes_attr="(max-width: 700px) 100vw, min(1080px, 100vw)"),
           hero_t=t["hero_t"], hero_s=t["hero_s"], cta1=t["cta1"], cta2=t["cta2"], em=em,
           s2_h=t["s2_h"], s2_p=t["s2_p"], grid=grid, gnote=gnote,
           s3_h=t["s3_h"], s3_p=t["s3_p"], map=svg_map(loc), map_lg=t["map_lg"], chips=chips,
           s4_h=t["s4_h"], s4_p=t["s4_p"], types=types_html,
           s5_h=t["s5_h"], about_p=t["about_p"], about_stats=about_stats,
           s6_h=t["s6_h"], s6_p=t["s6_p"], ccs="".join(ccs),
           credits_link=t["credits_link"],
           foot_c=t["foot_c"], foot_n=t["foot_n"],
           panels=panels(loc, photos), boxes=boxes,
           cur_zh=(' aria-current="page"' if loc == "zh" else ""),
           cur_en=(' aria-current="page"' if loc == "en" else ""))


def render_credits():
    photos = load_photos()
    rows = []
    name_of = {slug: zh for slug, zh, *_ in CITIES}
    name_of.update({slug: zh for slug, zh, *_ in TYPES})
    name_of["shouping"] = "首屏"
    for folder in sorted(photos):
        for it in photos[folder]:
            c = it.get("credit")
            if not c:
                continue
            rows.append('<tr><td>%s</td><td><a href="%s" rel="external">%s</a></td>'
                        '<td>%s</td><td>%s</td></tr>'
                        % (name_of.get(folder, folder), html.escape(c["url"]),
                           html.escape(c.get("title", c["url"])[:60]),
                           html.escape(c.get("author", "—")), html.escape(c["license"])))
    body = ('<table><thead><tr><th>板块</th><th>来源</th><th>作者</th><th>许可证</th></tr></thead>'
            '<tbody>%s</tbody></table>' % "".join(rows)) if rows else "<p>当前无示意图片。</p>"
    return """<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>图片来源 · 流涟旅拍</title>
<link rel="stylesheet" href="assets/css/site.css">
<style>
.credits{{max-width:900px;margin:0 auto;padding:32px 20px 64px}}
.credits table{{width:100%%;border-collapse:collapse;font-size:13px}}
.credits th,.credits td{{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
.credits td a{{word-break:break-all}}
</style>
</head>
<body>
<nav class="top"><div class="wrap topwrap">
  <a class="brand" href="index.html">流涟旅拍</a>
  <div class="topnav"><span class="secnav"><a href="index.html">← 返回</a></span></div>
</div></nav>
<div class="credits">
<h1>图片来源 · Image credits</h1>
<p style="color:var(--muted);font-size:14px;margin:10px 0 24px">
站内示意图片来自 Wikimedia Commons 等开放许可来源,逐张登记如下;
真实客片入库后逐步替换。地图数据:Natural Earth 1:10m(公有领域,无需署名)。<br>
Sample images are drawn from openly licensed sources and listed below.
Map data: Natural Earth 1:10m (public domain).</p>
%s
</div>
</body></html>
""" % body


def main():
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(render("zh"))
    os.makedirs(os.path.join(ROOT, "en"), exist_ok=True)
    with open(os.path.join(ROOT, "en", "index.html"), "w", encoding="utf-8") as f:
        f.write(render("en"))
    with open(os.path.join(ROOT, "credits.html"), "w", encoding="utf-8") as f:
        f.write(render_credits())
    ph = load_photos()
    n = sum(len(v) for v in ph.values())
    npl = sum(1 for v in ph.values() for it in v if it.get("placeholder"))
    print("built: index.html + en/index.html + credits.html  照片 %d(示意 %d)" % (n, npl))


if __name__ == "__main__":
    main()
