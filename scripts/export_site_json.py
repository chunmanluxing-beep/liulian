#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 content.py 里★业主可能想改的文案★导出成 content/site.json(后台可编辑的真源)。

用法:python3 scripts/export_site_json.py [输出路径]
不带参数时写到 <仓库根>/content/site.json。

只导出「文字」;以下三类**故意不外置**,避免后台误改:
  · 品牌名、导航词、按钮词等结构性字符串(改动会牵动版式与防误译标记)
  · 关于区的三个数字(2018 / 200 余 / 10)—— 站上数字必须有出处,不允许随手改
  · 地图高亮的都府县对应关系(属于数据,不属于文案)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from content import CITIES, TYPES, T  # noqa: E402

# 字段名 → 中文用途说明(写进 JSON 的 _说明 里,后台与人工编辑时都能看懂)
FIELD_DOC = {
    "hero_s": "首屏定位句 —— 网站第一屏大字下面那一句话。",
    "s2_p": "「作品」区标题下的一句说明。",
    "s3_p": "「拍摄地区」区标题下的一句说明。",
    "s4_p": "「业务范围」区标题下的一句说明。",
    "about_p": "「关于流涟」整段介绍(数字 2018 / 200 余 / 10 由系统固定,不在这里改)。",
    "s6_h": "「预订与联系」区的标题。",
    "s6_p": "「预订与联系」区标题下的一句说明。",
    "foot_n": "页脚最下面那一句(例如照片授权说明)。",
    "title": "浏览器标签页标题,也用于搜索结果标题。",
    "desc": "搜索结果里显示的一段站点简介(约 70–120 字)。",
    "types": "四类业务:每类的名称与介绍段落。",
    "cities": "十个拍摄地:每地的名称、地区文化介绍、拍摄介绍。",
    "cities.culture": "该地的地区与人文介绍,显示在弹窗「地区」小标题下。",
    "cities.shoot": "该地的拍摄安排介绍,显示在弹窗「拍摄」小标题下。",
}

SCALARS = ["hero_s", "s2_p", "s3_p", "s4_p", "about_p",
           "s6_h", "s6_p", "foot_n", "title", "desc"]


def build():
    # 不写 _说明 进 JSON:后台(Decap)保存时只保留已声明字段,注释会被抹掉。
    # 中文用途说明改放在两处业主真正会看到的地方:后台每个字段下的提示、以及私有仓 README。
    out = {}
    for loc, i_name, i_cul, i_sho, i_desc in (
            ("zh", 1, 4, 5, 3), ("en", 2, 6, 7, 4)):
        d = {k: T[loc][k] for k in SCALARS}
        d["types"] = {slug: {"name": tp[i_name], "desc": tp[i_desc]}
                      for tp in TYPES for slug in (tp[0],)}
        d["cities"] = {c[0]: {"name": c[i_name], "culture": c[i_cul], "shoot": c[i_sho]}
                       for c in CITIES}
        out[loc] = d
    return out


if __name__ == "__main__":
    dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "content", "site.json")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("已写出 %s(%d 字节)" % (dst, os.path.getsize(dst)))
