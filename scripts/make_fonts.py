#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""标题衬线字体子集化(构建期工具,产物已入库,不在部署时运行)

来源(均 SIL OFL 1.1,允许自托管与子集化):
  Noto Serif SC SemiBold — github.com/notofonts/noto-cjk (Serif/OTF/SimplifiedChinese)
  Cormorant Garamond(可变字体,实例化 wght=560)— github.com/google/fonts (ofl/cormorantgaramond)

流程:
  1) 从 scripts/content.py 收集衬线范围用字(标题/地名/品牌/数字,约 180 字符)
  2) Cormorant 先 instancer 到 wght=560
  3) pyftsubset --flavor=woff2 → assets/fonts/{notoserif-sub,cormorant-sub}.woff2
     (实测 76KB / 37KB,均远低于 400KB 上限)
依赖:pip install fonttools brotli
字符清单快照:assets/fonts/charset.txt(改标题文案后需重跑本流程)
"""
print(open(__file__, encoding="utf-8").read().split('"""')[1])
