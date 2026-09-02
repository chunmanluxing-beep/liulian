#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""流涟旅拍 · 授权示意图获取(Wikimedia Commons 开放 API,无需密钥)

--search  按内置检索词逐板块搜图,只收白名单许可证(CC0/公有领域/CC-BY)
          且宽度 ≥1600 的图,下载 2200px 审阅版到 /tmp/liulian-L2/review/,
          并写 candidates.json(来源 URL/作者/许可证)供逐张人审。
--ingest  读 accepted.json(人审后手工挑选的 review 文件名列表),
          经 L1 管道(剥元数据/双尺寸/双格式/哈希去重)入库,
          记 placeholder:true 与 credit,并重建站点与 CREDITS.md。

许可证白名单:CC0、Public domain(及各类 PD-*)、CC BY 1.0/2.0/2.5/3.0/4.0。
拒收:含 SA / NC / ND / GFDL-only / 未标注。
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = "/tmp/liulian-L2/review"
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "liulian-site-builder/1.0 (static site; contact: repo owner)"}

OK_LICENSE = re.compile(r"^(cc0|public domain|pd[- ]|no restrictions|cc[ -]by[ -]\d)", re.I)
BAD = re.compile(r"(sa|nc|nd|gfdl)", re.I)

# slug → (每板块目标张数, [检索词])
PLAN = {
  "shouping":        (2, ["Chureito Pagoda Mount Fuji", "Arashiyama bamboo grove"]),
  "jingdu":          (4, ["Fushimi Inari torii path", "Kiyomizu-dera autumn", "Gion Hanamikoji street", "Arashiyama bamboo forest"]),
  "dongjing":        (3, ["Sensoji temple Asakusa", "Shibuya crossing night", "Tokyo Tower dusk"]),
  "daban":           (3, ["Dotonbori canal night", "Osaka Castle cherry blossom", "Shinsekai Tsutenkaku"]),
  "nailiang":        (3, ["Nara deer park", "Todai-ji Great Buddha Hall", "Kasuga Taisha lanterns"]),
  "fushishan":       (3, ["Mount Fuji Lake Kawaguchi", "Chureito Pagoda Fuji spring", "Mount Fuji winter"]),
  "yidou":           (3, ["Jogasaki coast Izu", "Kawazu cherry blossoms", "Izu peninsula coast"]),
  "liancang":        (3, ["Kamakura Great Buddha Kotoku-in", "Enoden Kamakura", "Yuigahama beach Kamakura"]),
  "fuguang":         (3, ["Dazaifu Tenmangu", "Ohori Park Fukuoka", "Fukuoka yatai night"]),
  "zhahuang":        (3, ["Odori Park Sapporo", "Former Hokkaido Government Office", "Sapporo snow street"]),
  "xiaozun":         (3, ["Otaru canal winter", "Otaru canal evening", "Sakaimachi Otaru"]),
  "xingtai-hefu":    (2, ["kimono woman back street Kyoto", "kimono geta walking"]),
  "xingtai-jiating": (2, ["family walking beach silhouette", "family park autumn walking"]),
  "xingtai-hunsha":  (2, ["wedding couple shrine Japan", "shiromuku wedding"]),
  "xingtai-huiyi":   (2, ["conference hall audience", "trade show exhibition hall Japan"]),
}


def api(params):
    q = dict(params); q["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def lic_ok(short):
    if not short: return False
    if BAD.search(short): return False
    return bool(OK_LICENSE.search(short.strip()))


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def search(term, n=14):
    d = api({"action": "query", "generator": "search",
             "gsrsearch": 'filetype:bitmap ' + term, "gsrnamespace": 6, "gsrlimit": n,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
             "iiurlwidth": 2200})
    pages = (d.get("query") or {}).get("pages") or {}
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        if not ii: continue
        if ii.get("mime") not in ("image/jpeg", "image/png"): continue
        if (ii.get("width") or 0) < 1600: continue
        md = ii.get("extmetadata") or {}
        lic = strip_tags((md.get("LicenseShortName") or {}).get("value"))
        if not lic_ok(lic): continue
        out.append({
            "title": p.get("title", ""),
            "pageurl": ii.get("descriptionurl", ""),
            "thumb": ii.get("thumburl") or ii.get("url"),
            "width": ii.get("width"), "height": ii.get("height"),
            "author": strip_tags((md.get("Artist") or {}).get("value"))[:80] or "unknown",
            "license": lic,
        })
    return out


def cmd_search():
    os.makedirs(REVIEW, exist_ok=True)
    cands = {}
    for slug, (want, terms) in PLAN.items():
        got = []
        seen = set()
        for term in terms:
            try:
                rs = search(term)
            except Exception as e:
                print("  ! %s 「%s」检索失败:%s" % (slug, term, e)); continue
            for r in rs:
                if r["title"] in seen: continue
                seen.add(r["title"]); got.append(r)
            time.sleep(0.4)
        got = got[: want * 4]
        cands[slug] = got
        print("%-16s 候选 %d" % (slug, len(got)))
        for i, r in enumerate(got):
            ext = ".png" if r["thumb"].lower().endswith("png") else ".jpg"
            fn = "%s__%02d%s" % (slug, i, ext)
            dst = os.path.join(REVIEW, fn)
            r["file"] = fn
            if os.path.exists(dst) and os.path.getsize(dst) > 10000: continue
            try:
                req = urllib.request.Request(r["thumb"], headers=UA)
                with urllib.request.urlopen(req, timeout=90) as resp, open(dst, "wb") as f:
                    f.write(resp.read())
            except Exception as e:
                print("    下载失败 %s: %s" % (fn, e)); r["file"] = None
            time.sleep(0.3)
    with open(os.path.join(REVIEW, "candidates.json"), "w", encoding="utf-8") as f:
        json.dump(cands, f, ensure_ascii=False, indent=1)
    print("候选清单与审阅图已写入", REVIEW)


def cmd_ingest():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from ingest import strip_and_resize, load_index, INDEX, PHOTOS, sha  # noqa
    import subprocess
    with open(os.path.join(REVIEW, "candidates.json"), encoding="utf-8") as f:
        cands = json.load(f)
    with open(os.path.join(REVIEW, "accepted.json"), encoding="utf-8") as f:
        accepted = json.load(f)          # {file 名: true} 或 [file 名,...]
    if isinstance(accepted, list):
        accepted = {k: True for k in accepted}
    byfile = {}
    for slug, rs in cands.items():
        for r in rs:
            if r.get("file"): byfile[r["file"]] = (slug, r)
    idx = load_index()
    known = {it["sha"] for v in idx.values() for it in v}
    added = 0
    for fn in sorted(accepted):
        if fn not in byfile:
            print("  ? 未知文件", fn); continue
        slug, r = byfile[fn]
        src = os.path.join(REVIEW, fn)
        s = sha(src)
        if s in known:
            print("  = 已在库", fn); continue
        pid = s[:12]
        sizes = strip_and_resize(src, os.path.join(PHOTOS, slug), pid)
        rec = {"id": pid, "sha": s, "src": fn,
               "fw": sizes["2000"][0], "fh": sizes["2000"][1],
               "tw": sizes["800"][0], "th": sizes["800"][1],
               "gw": sizes["400"][0], "gh": sizes["400"][1],
               "placeholder": True,
               "credit": {"url": r["pageurl"], "title": r["title"].replace("File:", ""),
                          "author": r["author"], "license": r["license"]}}
        idx.setdefault(slug, []).append(rec)
        known.add(s); added += 1
        print("  ✓ %s ← %s(%s)" % (slug, fn, r["license"]))
    for k in idx: idx[k].sort(key=lambda x: x["id"])
    os.makedirs(PHOTOS, exist_ok=True)
    with open(INDEX, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    # CREDITS.md
    lines = ["# 图片来源 · Image credits", "",
             "站内示意图片(placeholder)逐张登记;真实客片入库后逐步替换。",
             "地图数据:Natural Earth 1:10m Admin-1(公有领域,无需署名)。", ""]
    for slug in sorted(idx):
        for it in idx[slug]:
            c = it.get("credit")
            if not c: continue
            lines.append("- **%s** · [%s](%s) · %s · **%s**"
                         % (slug, c["title"], c["url"], c["author"], c["license"]))
    with open(os.path.join(ROOT, "CREDITS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("入库 %d 张;CREDITS.md 已更新" % added)
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py")], check=True)


if __name__ == "__main__":
    if "--ingest" in sys.argv: cmd_ingest()
    else: cmd_search()
