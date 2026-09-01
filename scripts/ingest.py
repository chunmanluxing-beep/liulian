#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""流涟旅拍 · 客片投放管道(幂等)

用法:
  python3 scripts/ingest.py --list     # 扫描投放夹:解冻 iCloud 占位、列出候选、导出人审副本
  python3 scripts/ingest.py --ingest   # 人审通过后入库(可反复跑,内容哈希去重)
  python3 scripts/ingest.py --ingest --reject a.jpg --reject b.jpg   # 拦下指定文件

每张照片的处理:
  剥离全部元数据(EXIF/GPS/IPTC/ICC)→ 长边 2000 压缩版 + 长边 800 缩略 →
  WebP 与 JPG 双格式 → 写入 photos/<城市拼音>/ → 更新 photos/index.json → 重跑 build.py

铁律:
  · 桌面原图只读,脚本不改名、不移动、不写回
  · 入库前必须逐张开图人审(见 --list 导出的 /tmp/liulian-review/)
  · 只处理已获客人同意展示的照片(投放夹说明.txt 已写明)
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, time

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("需要 Pillow:python3 -m pip install --user Pillow")

ROOT = os.environ.get("LIULIAN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.environ.get("LIULIAN_DROP") or os.path.expanduser("~/Desktop/流涟客片")
REVIEW = "/tmp/liulian-review"
PHOTOS = os.path.join(ROOT, "photos")
INDEX = os.path.join(PHOTOS, "index.json")

# 投放夹中文名 → 仓库拼音目录
FOLDERS = {
    "首屏":"shouping",
    "京都":"jingdu", "东京":"dongjing", "大阪":"daban", "奈良":"nailiang",
    "福冈":"fuguang", "镰仓":"liancang", "富士山":"fushishan",
    "札幌":"zhahuang", "小樽":"xiaozun",
    "形态-和服":"xingtai-hefu", "形态-生活":"xingtai-shenghuo",
    "形态-情侣":"xingtai-qinglv", "形态-家庭":"xingtai-jiating",
}
EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".tif", ".tiff"}


def is_dataless(p):
    """iCloud「优化存储」会把文件抽成占位符,读它会长时间阻塞。"""
    try:
        out = subprocess.run(["/bin/ls", "-lO", p], capture_output=True, text=True, timeout=8).stdout
        return "dataless" in out or "compressed" in out
    except Exception:
        return False


def thaw(p):
    """先请 brctl 下载,再用限时小块读探测是否真的落地。"""
    if os.path.exists("/usr/bin/brctl"):
        try:
            subprocess.run(["/usr/bin/brctl", "download", p], capture_output=True, timeout=120)
        except Exception:
            pass
    for _ in range(12):
        try:
            with open(p, "rb") as f:
                f.read(65536)
            return True
        except Exception:
            time.sleep(1)
    return False


def scan():
    """返回 [(投放夹中文名, 拼音目录, 原图绝对路径)],并顺手解冻。"""
    found, frozen = [], []
    for zh, key in FOLDERS.items():
        d = os.path.join(DROP, zh)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.startswith("."):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in EXTS:
                continue
            p = os.path.join(d, name)
            if is_dataless(p) and not thaw(p):
                frozen.append(p)
                continue
            found.append((zh, key, p))
    return found, frozen


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_index():
    if os.path.exists(INDEX):
        with open(INDEX, encoding="utf-8") as f:
            return json.load(f)
    return {}


def strip_and_resize(src, out_dir, pid):
    """剥元数据 + 出四个文件(2000/800 × webp/jpg)。返回尺寸。"""
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)          # 先按 EXIF 摆正,再把 EXIF 全丢掉
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    im.info = {}                               # 丢掉 icc_profile / exif / 注释等所有附带块
    sizes = {}
    os.makedirs(out_dir, exist_ok=True)
    for tag, edge in (("2000", 2000), ("800", 800)):
        w, h = im.size
        s = min(1.0, float(edge) / max(w, h))
        nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
        r = im.resize((nw, nh), Image.LANCZOS) if s < 1.0 else im.copy()
        r.info = {}
        r.save(os.path.join(out_dir, "%s-%s.jpg" % (pid, tag)),
               "JPEG", quality=82, optimize=True, progressive=True, exif=b"")
        r.save(os.path.join(out_dir, "%s-%s.webp" % (pid, tag)),
               "WEBP", quality=80, method=5)
        sizes[tag] = (nw, nh)
    return sizes


def verify_clean(p):
    """抽检:入库件不应带任何元数据。"""
    im = Image.open(p)
    ex = getattr(im, "_getexif", lambda: None)()
    bad = []
    if ex:
        bad.append("exif")
    for k in ("icc_profile", "exif", "comment", "XML:com.adobe.xmp"):
        if im.info.get(k):
            bad.append(k)
    return bad


def cmd_list():
    found, frozen = scan()
    os.makedirs(REVIEW, exist_ok=True)
    print("投放夹:%s" % DROP)
    if not os.path.isdir(DROP):
        print("  ✗ 投放夹不存在")
        return
    if frozen:
        print("  ⚠ 仍冻结(iCloud 未落地)%d 张:" % len(frozen))
        for p in frozen:
            print("     " + p)
    if not found:
        print("  当前 0 张待入库照片 —— 骨架以占位上线。")
        return
    print("  候选 %d 张,已导出到 %s 供逐张开图人审:" % (len(found), REVIEW))
    idx = load_index()
    known = {it["sha"] for v in idx.values() for it in v}
    for zh, key, p in found:
        s = sha(p)
        flag = "（已入库,将跳过）" if s in known else ""
        dst = os.path.join(REVIEW, "%s__%s" % (key, os.path.basename(p)))
        if not os.path.exists(dst):
            shutil.copy2(p, dst)              # 只读拷贝,原件不动
        print("   %-14s %-40s %s %s" % (zh, os.path.basename(p), s[:10], flag))
    print("\n人审要点:他家水印/logo、证件/车牌/门牌、未成年人正面特写、未打码个人信息 → 拦下不入库。")


def cmd_ingest(reject):
    found, frozen = scan()
    if frozen:
        print("⚠ 有 %d 张仍冻结,本次跳过。" % len(frozen))
    idx = load_index()
    known = {it["sha"] for v in idx.values() for it in v}
    added = skipped = blocked = 0
    for zh, key, p in found:
        base = os.path.basename(p)
        if base in reject:
            blocked += 1
            print("  ✗ 人审拦下:%s / %s" % (zh, base))
            continue
        s = sha(p)
        if s in known:
            skipped += 1
            continue
        pid = s[:12]
        sizes = strip_and_resize(p, os.path.join(PHOTOS, key), pid)
        rec = {"id": pid, "sha": s, "src": base,
               "fw": sizes["2000"][0], "fh": sizes["2000"][1],
               "tw": sizes["800"][0], "th": sizes["800"][1]}
        idx.setdefault(key, []).append(rec)
        known.add(s)
        added += 1
        print("  ✓ 入库 %s / %s → %s(%dx%d)" % (zh, base, pid, rec["fw"], rec["fh"]))
    for k in idx:
        idx[k].sort(key=lambda r: r["id"])
    with open(INDEX, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    # 元数据抽检
    dirty = []
    for k, v in idx.items():
        for it in v:
            for tag in ("2000", "800"):
                jp = os.path.join(PHOTOS, k, "%s-%s.jpg" % (it["id"], tag))
                if os.path.exists(jp):
                    b = verify_clean(jp)
                    if b:
                        dirty.append((jp, b))
    print("入库 %d、跳过(已在库)%d、人审拦下 %d;元数据抽检不干净 %d 处。"
          % (added, skipped, blocked, len(dirty)))
    for p, b in dirty:
        print("   ⚠ %s 仍带 %s" % (p, ",".join(b)))
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py")], check=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--ingest", action="store_true")
    ap.add_argument("--reject", action="append", default=[])
    a = ap.parse_args()
    if a.ingest:
        cmd_ingest(set(a.reject))
    else:
        cmd_list()
