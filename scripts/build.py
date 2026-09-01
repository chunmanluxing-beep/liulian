#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""流涟旅拍官网 · 静态生成器(幂等)
中英两套页面由同一份内容模型渲染,保证逐板块结构对应。
画廊来自 photos/index.json(由 scripts/ingest.py 写入);没有照片时全部渲染为占位。
"""
import json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────── 内容模型 ───────────────────────────
CITIES = [
    # key,        zh,      en,          lon,     lat,   zh 特色(≤15字),        en 特色
    ("jingdu",   "京都",   "Kyoto",    135.77, 35.01, "老街与神社,和服上镜。", "Old streets and shrines."),
    ("dongjing", "东京",   "Tokyo",    139.69, 35.68, "街头与夜景,城市感强。", "Street corners and night light."),
    ("daban",    "大阪",   "Osaka",    135.50, 34.69, "市井烟火,适合日常穿搭。", "Everyday city texture."),
    ("nailiang", "奈良",   "Nara",     135.83, 34.69, "鹿与古寺,画面安静。",   "Deer and quiet temples."),
    ("fuguang",  "福冈",   "Fukuoka",  130.40, 33.59, "海边与屋台,南国气息。", "Seaside and food stalls."),
    ("liancang", "镰仓",   "Kamakura", 139.55, 35.32, "海与电车,一天拍完。",   "The sea and the old tram line."),
    ("fushishan","富士山", "Mt. Fuji", 138.73, 35.36, "山与湖,晴天出片。",     "Mountain, lake, clear days."),
    ("zhahuang", "札幌",   "Sapporo",  141.35, 43.06, "雪季长,冬装好看。",     "A long snow season."),
    ("xiaozun",  "小樽",   "Otaru",    141.00, 43.19, "运河与旧仓库,复古。",   "Canal and old warehouses."),
]

TYPES = [
    ("xingtai-hefu",     "和服旅拍",   "Kimono session",    "换装、盘发、外拍一次完成。", "Dressing, hair and the shoot in one visit."),
    ("xingtai-shenghuo", "生活方式旅拍","Lifestyle session", "日常穿搭,街头随走随拍。",   "Your own clothes, walking and shooting."),
    ("xingtai-qinglv",   "情侣",       "Couples",           "两个人的节奏,不摆固定姿势。","Your pace, no fixed poses."),
    ("xingtai-jiating",  "家庭",       "Family",            "带孩子也拍得完,节奏放慢。", "Slower, and it works with kids."),
]

CONTACTS = [
    ("gyg",       "GetYourGuide", "GetYourGuide", "预订与档期",   "Booking and dates"),
    ("viator",    "Viator",       "Viator",       "预订与档期",   "Booking and dates"),
    ("xhs",       "小红书",       "Xiaohongshu",  "客片与日常",   "Work and updates"),
    ("wechat",    "微信",         "WeChat",       "扫码咨询",     "Scan to chat"),
    ("email",     "邮箱",         "Email",        "合作与咨询",   "Partnerships and questions"),
]

T = {
 "zh": {
   "lang":"zh-Hans","dir":"","other":"en/index.html","other_label":"EN","self_label":"中文",
   "title":"流涟旅拍 · 日本和服与生活方式旅拍",
   "desc":"流涟旅拍:在日本 9 个城市与地区拍摄和服与生活方式客片,2021 年起接单,合作摄影师 30+ 位。",
   "brand":"流涟旅拍",
   "hero_t":"流涟旅拍","hero_s":"在日本 9 个地方,拍和服与日常。",
   "cta1":"在 GetYourGuide 预订","cta2":"微信咨询",
   "s2_h":"客片精选","s2_p":"近期交付的照片,均经客人同意展示。",
   "s3_h":"拍摄地区","s3_p":"9 个城市与地区,各有各的取景。",
   "map_lg":"点地图上的圆点,跳到该地客片。",
   "s4_h":"拍摄形态","s4_p":"四种常见拍法,按人数与场景选。",
   "s5_h":"关于流涟",
   "about":[("2021","年起接单"),("30+","位合作摄影师"),("9","个城市与地区")],
   "s6_h":"预订与联系","s6_p":"下单与咨询走店铺或社交账号。",
   "foot_c":"© 流涟旅拍","foot_n":"客片均已获客人授权展示。",
   "ph_photo":"客片位","ph_qr":"二维码位","swipe":"◀ 左右滑动 ▶",
   "nav":[("#gallery","客片"),("#areas","地区"),("#types","形态"),("#about","关于"),("#contact","联系")],
   "lb_close":"关闭","lb_prev":"上一张","lb_next":"下一张",
 },
 "en": {
   "lang":"en","dir":"../","other":"../index.html","other_label":"中文","self_label":"EN",
   "title":"Liulian Photography · Kimono and lifestyle sessions in Japan",
   "desc":"Liulian Photography: kimono and lifestyle sessions in nine cities and regions across Japan. Taking bookings since 2021, with 30+ partner photographers.",
   "brand":"Liulian",
   "hero_t":"Liulian Photography","hero_s":"Kimono and everyday portraits, in nine places across Japan.",
   "cta1":"Book on GetYourGuide","cta2":"Chat on WeChat",
   "s2_h":"Selected work","s2_p":"Recent deliveries, shared with client permission.",
   "s3_h":"Where we shoot","s3_p":"Nine cities and regions, each with its own light.",
   "map_lg":"Tap a dot to jump to that place.",
   "s4_h":"Session types","s4_p":"Four common formats, by group and setting.",
   "s5_h":"About Liulian",
   "about":[("2021","taking bookings since"),("30+","partner photographers"),("9","cities and regions")],
   "s6_h":"Book and contact","s6_p":"Bookings and questions go through the shops or social accounts.",
   "foot_c":"© Liulian Photography","foot_n":"All photos shown with client permission.",
   "ph_photo":"PHOTO SLOT","ph_qr":"QR SLOT","swipe":"◀ swipe ▶",
   "nav":[("#gallery","Work"),("#areas","Places"),("#types","Types"),("#about","About"),("#contact","Contact")],
   "lb_close":"Close","lb_prev":"Previous","lb_next":"Next",
 },
}

# ─────────────────── 日本轮廓 SVG(自绘简化海岸线) ───────────────────
# 来源:本仓库自绘。用一组公开的海岸转折点经纬度手工简化而成,
# 等距圆柱投影 x=(lon-128)*20, y=(46.5-lat)*22。不含任何第三方地图数据或瓦片。
COAST = {
 "honshu": [(140.9,41.5),(141.5,39.7),(141.0,38.3),(140.9,37.0),(140.8,36.0),(140.1,35.6),
            (139.8,35.0),(138.9,34.7),(137.0,34.6),(136.9,34.2),(135.9,33.5),(135.1,33.6),
            (135.0,34.45),(134.0,34.55),(132.6,34.35),(131.2,34.3),(130.95,34.6),(132.0,35.4),
            (134.0,35.6),(135.9,35.6),(136.7,36.8),(137.8,37.3),(139.0,38.0),(139.9,39.9),(140.3,41.2)],
 "hokkaido":[(140.0,41.8),(141.5,42.6),(143.0,42.3),(144.5,43.0),(145.3,44.3),(144.0,44.3),
             (142.0,45.5),(141.5,45.4),(140.5,43.3)],
 "kyushu": [(130.70,33.75),(131.60,33.45),(131.90,32.75),(131.40,31.35),(130.60,31.05),
            (130.10,31.85),(129.65,32.90),(130.15,33.45)],
 "shikoku":[(132.20,33.65),(134.30,34.00),(134.70,33.70),(134.00,33.25),(132.90,32.75),(132.35,33.15)],
}
def proj(lon, lat): return round((lon-128)*20, 1), round((46.5-lat)*22, 1)

# 标点示意性错位(投影后像素):关西与关东三点实际相距仅数公里,
# 按真实坐标会叠成一团,这里做小幅拉开,只为可点可读,不代表精确位置。
NUDGE = {
 "jingdu":(-2,-8), "daban":(-11,3), "nailiang":(12,4),
 "dongjing":(6,-4), "liancang":(2,10), "fushishan":(-14,-6),
 "zhahuang":(4,4),  "xiaozun":(-8,-6), "fuguang":(0,0),
}
def path(pts):
    d = "M " + " L ".join("%s %s" % proj(a, b) for a, b in pts) + " Z"
    return d

def svg_map(loc):
    lands = "".join('<path class="land" d="%s"/>' % path(v) for v in COAST.values())
    pins = []
    for key, zh, en, lon, lat, _, _ in CITIES:
        x, y = proj(lon, lat)
        dx, dy = NUDGE.get(key, (0, 0)); x, y = round(x+dx,1), round(y+dy,1)
        name = zh if loc == "zh" else en
        pins.append(
          '<a href="#city-%s" aria-label="%s"><title>%s</title>'
          '<circle class="pin-hit" cx="%s" cy="%s" r="28"/>'
          '<circle class="pin" cx="%s" cy="%s" r="4.5"/></a>' % (key, name, name, x, y, x, y))
    return ('<svg class="jpmap" viewBox="20 10 350 350" role="img" '
            'aria-label="%s" xmlns="http://www.w3.org/2000/svg">%s%s</svg>'
            % ("日本拍摄地区分布图" if loc=="zh" else "Map of shooting locations in Japan",
               lands, "".join(pins)))

# ─────────────────────────── 渲染 ───────────────────────────
def load_photos():
    p = os.path.join(ROOT, "photos", "index.json")
    if not os.path.exists(p): return {}
    with open(p, encoding="utf-8") as f: return json.load(f)

def slot(loc, folder, photos, cls="", alt=""):
    """有图渲染真图,无图渲染统一占位。两种状态结构一致。"""
    items = photos.get(folder, [])
    if items:
        it = items[0]
        return ('<div class="slot %s"><picture>'
                '<source srcset="%sphotos/%s/%s-800.webp" type="image/webp">'
                '<img src="%sphotos/%s/%s-800.jpg" alt="%s" loading="lazy" decoding="async" '
                'width="%d" height="%d"></picture></div>'
                % (cls, T[loc]["dir"], folder, it["id"], T[loc]["dir"], folder, it["id"],
                   html.escape(alt), it["tw"], it["th"]))
    return ('<div class="slot slot-ph %s" role="img" aria-label="%s">%s</div>'
            % (cls, T[loc]["ph_photo"], T[loc]["ph_photo"]))

def gallery(loc, photos):
    flat = []
    for key, zh, en, *_ in CITIES:
        for it in photos.get(key, []):
            flat.append((key, zh if loc=="zh" else en, it))
    if not flat:
        cells = "".join('<div class="slot slot-ph" role="img" aria-label="%s">%s</div>'
                        % (T[loc]["ph_photo"], T[loc]["ph_photo"]) for _ in range(8))
        return '<div class="grid">%s</div>' % cells, ""
    cells, boxes = [], []
    n = len(flat)
    d = T[loc]["dir"]
    for i, (folder, place, it) in enumerate(flat):
        pid = "p-%s" % it["id"]
        cells.append('<a class="slot" href="#%s" aria-label="%s"><picture>'
                     '<source srcset="%sphotos/%s/%s-800.webp" type="image/webp">'
                     '<img src="%sphotos/%s/%s-800.jpg" alt="%s" loading="lazy" decoding="async" '
                     'width="%d" height="%d"></picture></a>'
                     % (pid, place, d, folder, it["id"], d, folder, it["id"], place, it["tw"], it["th"]))
        prv = "p-%s" % flat[(i-1) % n][2]["id"]
        nxt = "p-%s" % flat[(i+1) % n][2]["id"]
        boxes.append('<figure class="lb" id="%s"><a class="lb-x" href="#gallery" '
                     'aria-label="%s">✕</a><picture>'
                     '<source srcset="%sphotos/%s/%s-2000.webp" type="image/webp">'
                     '<img src="%sphotos/%s/%s-2000.jpg" alt="%s" width="%d" height="%d"></picture>'
                     '<figcaption>%s</figcaption>'
                     '<div class="lb-nav"><a class="lb-prev" href="#%s" aria-label="%s">←</a>'
                     '<a class="lb-next" href="#%s" aria-label="%s">→</a></div></figure>'
                     % (pid, T[loc]["lb_close"], d, folder, it["id"], d, folder, it["id"],
                        place, it["fw"], it["fh"], place,
                        prv, T[loc]["lb_prev"], nxt, T[loc]["lb_next"]))
    return '<div class="grid">%s</div>' % "".join(cells), "".join(boxes)

def render(loc):
    t = T[loc]; d = t["dir"]; photos = load_photos()
    nav = '<span class="secnav">%s</span>' % "".join('<a href="%s">%s</a>' % (h, x) for h, x in t["nav"])
    grid, boxes = gallery(loc, photos)
    cities = "".join(
        '<div class="city" id="city-%s">%s<b>%s</b><span>%s</span></div>'
        % (k, slot(loc, k, photos, alt=(zh if loc=="zh" else en)),
           zh if loc=="zh" else en, dzh if loc=="zh" else den)
        for k, zh, en, lon, lat, dzh, den in CITIES)
    types = "".join(
        '<div class="type">%s<b>%s</b><span>%s</span></div>'
        % (slot(loc, k, photos, alt=(zh if loc=="zh" else en)),
           zh if loc=="zh" else en, dzh if loc=="zh" else den)
        for k, zh, en, dzh, den in TYPES)
    about = "".join('<li><b>%s</b>%s</li>' % (n, (zh if loc=="zh" else en))
                    for n, zh in [(a, b) for a, b in t["about"]]) if False else \
            "".join('<li><b>%s</b>%s</li>' % (a, b) for a, b in t["about"])
    ccs = []
    for key, zh, en, szh, sen in CONTACTS:
        label = zh if loc=="zh" else en
        sub   = szh if loc=="zh" else sen
        if key == "wechat":
            ccs.append('<div class="cc link-ph"><b>%s</b><span>%s</span>'
                       '<div class="slot slot-ph qr" role="img" aria-label="%s">%s</div></div>'
                       % (label, sub, t["ph_qr"], t["ph_qr"]))
        else:
            ccs.append('<div class="cc link-ph"><b>%s</b><span>%s</span></div>' % (label, sub))
    swipe_hint = '<span class="swipe-hint">%s</span>' % t["swipe"]

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
    <a class="btn btn-2 link-ph" role="link" aria-disabled="true">{cta2}</a>
  </div>
</div></section>

<section id="gallery"><div class="wrap">
  <div class="sec-h"><h2>{s2_h}</h2><p>{s2_p}</p></div>
  {grid}
</div></section>

<section id="areas"><div class="wrap">
  <div class="sec-h"><h2>{s3_h}</h2><p>{s3_p}</p></div>
  <div class="mapbox">{map}<p class="maplg">{map_lg}</p></div>
  <div class="cities swipe">{cities}</div>{swipe_hint}
</div></section>

<section id="types"><div class="wrap">
  <div class="sec-h"><h2>{s4_h}</h2><p>{s4_p}</p></div>
  <div class="types">{types}</div>
</div></section>

<section id="about"><div class="wrap">
  <div class="sec-h"><h2>{s5_h}</h2></div>
  <div class="about"><ul>{about}</ul></div>
</div></section>

<section id="contact"><div class="wrap">
  <div class="sec-h"><h2>{s6_h}</h2><p>{s6_p}</p></div>
  <div class="contact">{ccs}</div>
</div></section>

</main>
<footer><div class="wrap foot">
  <div class="langrow"><a href="{d}index.html" data-lang="zh"{cur_zh}>中文</a> · <a href="{d}en/index.html" data-lang="en"{cur_en}>EN</a></div>
  <div>{foot_c}</div>
  <div>{foot_n}</div>
</div></footer>
{boxes}
<script src="{d}assets/js/site.js" defer></script>
</body>
</html>
""".format(lang=t["lang"], desc=html.escape(t["desc"]), title=html.escape(t["title"]),
           other=t["other"], other_label=t["other_label"], other_lang=("en" if loc=="zh" else "zh"),
           alt_lang=("en" if loc=="zh" else "zh-Hans"),
           d=d, brand=t["brand"], nav=nav,
           hero_shot=slot(loc, "shouping", photos, cls="hero-shot", alt=t["hero_t"]),
           hero_t=t["hero_t"], hero_s=t["hero_s"], cta1=t["cta1"], cta2=t["cta2"],
           s2_h=t["s2_h"], s2_p=t["s2_p"], grid=grid,
           s3_h=t["s3_h"], s3_p=t["s3_p"], map=svg_map(loc), map_lg=t["map_lg"],
           cities=cities, swipe_hint=swipe_hint,
           s4_h=t["s4_h"], s4_p=t["s4_p"], types=types,
           s5_h=t["s5_h"], about=about,
           s6_h=t["s6_h"], s6_p=t["s6_p"], ccs="".join(ccs),
           foot_c=t["foot_c"], foot_n=t["foot_n"], boxes=boxes,
           cur_zh=(' aria-current="page"' if loc=="zh" else ""),
           cur_en=(' aria-current="page"' if loc=="en" else ""))

def main():
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(render("zh"))
    os.makedirs(os.path.join(ROOT, "en"), exist_ok=True)
    with open(os.path.join(ROOT, "en", "index.html"), "w", encoding="utf-8") as f:
        f.write(render("en"))
    ph = load_photos()
    n = sum(len(v) for v in ph.values())
    print("built: index.html + en/index.html   已入库照片 %d 张" % n)

if __name__ == "__main__":
    main()
