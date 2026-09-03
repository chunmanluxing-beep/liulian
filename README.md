# 流涟旅拍 · 官网(L1 骨架)

对外业务介绍站。纯展示,不做在线询价、下单与价目;转化出口是
GetYourGuide / Viator 店铺与微信、小红书。托管在 GitHub Pages。

- 中文:`/`  ·  English:`/en/`
- 内容核心:**客片展示 + 业务地区范围**,文字极简。

## 目录结构

```
index.html            中文页(由 scripts/build.py 生成,勿手改)
en/index.html         英文页(同上)
assets/css/site.css   全部样式(自托管)
assets/js/site.js     渐进增强脚本:语言记忆 / 灯箱键盘 / 滑动提示
assets/img/           站点自有图形(logo、二维码等,尚未提供)
photos/<城市拼音>/     入库客片(2000 与 800 两档 × WebP 与 JPG)
photos/index.json     画廊索引(ingest 写入,build 读取)
scripts/ingest.py     客片投放管道
scripts/build.py      静态生成器(中英两套页面由同一份内容模型渲染)
```

城市拼音目录:`jingdu 京都 / dongjing 东京 / daban 大阪 / nailiang 奈良 /
fuguang 福冈 / liancang 镰仓 / fushishan 富士山 / zhahuang 札幌 / xiaozun 小樽`,
另有 `shouping 首屏` 与 `xingtai-hefu | xingtai-shenghuo | xingtai-qinglv | xingtai-jiating`。

## 设计令牌

| 令牌 | 值 | 说明 |
|---|---|---|
| `--bg` | `#FAF8F5` | 近白暖灰底。照片是主角,底色退到后面 |
| `--ink` | `#22201D` | 墨色正文 |
| `--muted` | `#6B6560` | 次级说明 |
| `--line` | `#E4DFD7` | 分隔线 |
| `--accent` | `#2A4C63` | **单一强调色「深縹」** |
| 字体 | 系统字体栈 | `-apple-system / Hiragino Sans / Noto Sans CJK SC / PingFang SC …`,**不外联任何字体** |
| 圆角 | 8 / 12 / 16 / 999px | 卡片 12,大块 16,按钮胶囊 |
| 间距 | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 | 全站只用这一套 |

**为什么选深縹**:和服客片以红、金、朱为主。冷调的日本传统织物蓝会退到照片后面,
不与画面抢色;在 `#FAF8F5` 上对比度 8.4:1(WCAG AAA),做按钮与链接都够用。

## 板块

| # | 板块 | 状态 |
|---|---|---|
| ① | 首屏:整幅客片 + 品牌 + 一句定位 + 两个按钮 | 图位与按钮均为**占位** |
| ② | 客片精选:响应式网格(手机 2 列 / 桌面 3–4 列)+ 灯箱 | 8 个**占位**图位 |
| ③ | 拍摄地区:内联 SVG 日本地图 + 9 地卡片 | 地图**已就绪**;9 个代表图位为**占位** |
| ④ | 拍摄形态:和服 / 生活方式 / 情侣 / 家庭 | 4 个**占位**图位 |
| ⑤ | 关于流涟:2021 年起 / 30+ 摄影师 / 9 地 | **已就绪** |
| ⑥ | 预订与联系:GetYourGuide / Viator / 小红书 / 微信 / 邮箱 | 5 项均为**占位** |
| ⑦ | 页脚:语言切换 / © / 授权说明 | **已就绪** |

### 占位清单(共 30 处)

- **图位 23 个**,class `slot slot-ph`:首屏 1、客片精选 8、地区 9、形态 4、微信二维码 1。
- **链接 7 个**,class `link-ph`:首屏两个按钮、联系区五项。
  尚未拿到真实店铺链接与账号,本轮不编造。替换时把 `link-ph` 换成 `link-live`
  并补 `href` 即可,结构不动。

真图与真链接分别是 `slot`(无 `slot-ph`)与 `link-live`,与占位用不同 class 标记。

## 地图数据来源

`assets` 里没有任何地图文件——日本轮廓是 **`scripts/build.py` 里自绘的简化海岸线**:
用一组公开的海岸转折点经纬度手工简化(本州 25 点、北海道 9 点、九州 8 点、四国 6 点),
等距圆柱投影 `x=(lon-128)×20, y=(46.5-lat)×22`,内联成 SVG。
**不含任何第三方地图数据、瓦片或 API**,不需要署名。

9 个标点按各地真实经纬度投影后,对关西(京都/大阪/奈良)与关东(东京/镰仓/富士山)
两组做了小幅**示意性错位**(见 `NUDGE`)——真实间距只有几公里,不错开会叠成一团。
它是导航用的示意图,不是测绘图。

## 客片投放与入库

投放夹:`~/Desktop/流涟客片/`(见夹内 `说明.txt`)。

```bash
python3 scripts/ingest.py --list     # 扫描 + 解冻 iCloud 占位 + 导出人审副本
python3 scripts/ingest.py --ingest   # 人审通过后入库(幂等,内容哈希去重)
python3 scripts/ingest.py --ingest --reject 某张.jpg   # 人审拦下某张
```

每张照片:**剥离全部元数据(EXIF / GPS / IPTC / ICC)** → 长边 2000 展示版 +
长边 800 缩略版 → WebP 与 JPG 双格式 → 写入 `photos/<城市拼音>/` →
更新 `photos/index.json` → 重跑 `build.py` 把画廊**静态注入 HTML**(没有 JS 也能看)。

桌面原图**只读**:不改名、不移动、不覆盖。
入库前逐张开图人审,以下情况拦下并在报告里列出:他家水印或 logo、
证件/车牌/门牌等可定位信息、未成年人正面特写、未打码的个人信息。

## 技术约束

- **零第三方资源**:不接字体 CDN、统计脚本、地图 API。全部资源自托管,大陆访客可直接打开。
- **禁用 JS 全站可浏览**:灯箱用 `:target`(纯 CSS)、滑动用 `scroll-snap`(纯 CSS)、
  语言用两套静态页面互链。`assets/js/site.js` 只做三件锦上添花的事,关掉不影响任何内容。
- **触控**:可点元素命中区 ≥44×44,一律用透明伪元素扩展,视觉尺寸不放大。
- **站上数字只用有出处的三个**:9 个拍摄地、30+ 合作摄影师、2021 年起。

## 本地预览

```bash
cd ~/Projects/liulian-site && python3 -m http.server 8971
# 打开 http://127.0.0.1:8971/  与  http://127.0.0.1:8971/en/
```


## L2(2026-09-02):正式文案 + 精致地图 + 十地弹窗 + 授权示意图

- **文案**:全站改为正式的服务介绍语体(第三人称、陈述句、零 PR 腔),中英各一套、
  逐板块对应;站上数字仅 2018 / 200 余 / 10 三个业主口径。
- **地图**:Natural Earth 1:10m Admin-1(公有领域,无需署名)经 mapshaper 简化 12% +
  墨卡托投影生成,46 个都道府县细线描边、业务所在都府县浅色填充,10 地标点 + 引线错开;
  数据文件 `scripts/mapdata.json`,渲染逻辑在 `scripts/build.py`。
- **十地**:京都 / 东京 / 大阪 / 奈良 / 富士山 / 伊豆半岛 / 镰仓 / 福冈 / 札幌 / 小樽。
  点地图、地名或 chip → 弹出该地面板(横滑画廊 + 地区文化 + 拍摄介绍 + 预订出口);
  JS 增强为模态(Esc / 遮罩 / 焦点圈定),禁用 JS 时经 :target 同样可开可看。
- **业务四类**:和服旅拍 / 家庭常服 / 婚纱 / 会议活动摄影(业主口径)。
- **示意图**:36 张,全部来自 Wikimedia Commons 的 CC0 / 公有领域 / CC-BY 素材,
  逐张登记于 `CREDITS.md` 与站内 `credits.html`(页脚「图片来源」);
  相关板块标注「示意图片 · 客片持续更新」,真客片入库(无 placeholder 标记)后该标注自动消失。
  入库沿 L1 管道:剥全部元数据 → 2000/800/400 三档 × WebP/JPG 双格式 → 哈希去重。
- **联系**:邮箱 mailto(HTML 实体混淆);微信板块移除;GYG / Viator / 小红书仍为 link-ph 占位。
- 桌面投放夹同步为 10 地 + 4 业务子夹。


## L4(2026-09-03):华丽化重做 + 高清和服影像扩充 + 出口收口

- **视觉**:深色沉浸重做 —— 墨黑暖底(#131110)衬和服的朱金白;单一金铜强调
  (#C9A05F,仅用于细线/标题下划/按钮描边,不做大面积金渐变);标题衬线自托管子集
  (SIL OFL:Noto Serif SC SemiBold 76KB + Cormorant Garamond wght560 37KB),
  正文仍系统字体栈,**零外链**。子集流程见 `scripts/make_fonts.py` 与
  `assets/fonts/charset.txt`(改标题文案后需重跑)。
- **首屏**:全屏和服人像轮播 3 帧(纯 CSS 淡切,8s/帧;`prefers-reduced-motion`
  下停在首帧)+ 衬线字标 + 金线 + 邮件 / Instagram 两枚描边按钮。
- **作品精选**:编辑感错位网格(和服人像优先,每第 5 格横跨两列)。
- **拍摄地区**:地图改深色版式、金色标点;十地面板改大图横滑 + 桌面文案分栏。
- **业务四类**:大图卡片(主图 + 副图,容器定纵横比以免图片塌高),和服旅拍居首。
- **性能**:离屏格子用 `content-visibility:auto` + `contain-intrinsic-size`,
  首屏首载 727KB(390);整页首载 ≤1.6MB。
- **动效**:滚动进场只动 `transform`,不动 `opacity` —— 任何浏览器/任何滚动位置
  都不会把内容留在不可见状态。
- **出口收口**:GetYourGuide / Viator / 小红书全部占位与文案删除;
  联系仅 邮箱(HTML 实体混淆 mailto)+ Instagram(无跟踪参数,`rel=noopener`
  新窗口);中英「关于」段改为「咨询与预订通过邮箱与 Instagram 进行」。
- **影像高清硬门**(L4 新增,逐张执行):①**本地实际**长边 ≥2400px(不看源站
  标称值 —— Openverse 的 rawpixel / StockSnap 端点只给 ≤1440px 渲染件,
  探测无更大端点,故该渠道本轮零入站);②清晰度实测(拉普拉斯方差,灰度缩至
  长边 1200 统一口径)+ 体积/像素比,数值偏低者开图复核,糊的拒收;
  ③取检索结果里最大可用规格(Commons `iiurlwidth=3840`),不用缩略图端点;
  ④2000 档一律由清晰原图缩放而来。逐张台账见 `CREDITS.md`。


## L5(2026-09-03):上传后门(照片 + 视频) + 首屏视频位 + 品牌防误译

### 首屏视频位
- `scripts/build.py` 的 `hero_media()`:`assets/video/hero-1280.mp4` **存在则渲染视频**,
  否则**原样保持三帧和服人像轮播**(不开天窗、不改一字)。
- 规格:`<video autoplay muted loop playsinline preload="metadata" poster=…>` +
  WebM(VP9)与 MP4(H.264)双源;覆盖层字标/定位句/两枚按钮位置与轮播版完全一致;
  `prefers-reduced-motion: reduce` 时 CSS 隐藏 video、显示 poster 静帧;
  自动播放靠原生属性,**禁用 JS 同样生效**;容器由 `.hero{min-height:92svh}` 撑住,
  视频未加载不塌高。
- 体积硬门(收件仓 ffmpeg 侧执行):MP4 ≤4MB、WebM ≤3.5MB、poster ≤200KB,
  CRF 递降 + 码率兜底,超 20 秒按前 20 秒截取(首屏是循环背景)。

### 上传后门
- **私有收件仓** `chunmanluxing-beep/liulian-inbox`:业主把照片/视频丢进 `inbox/<板块>/`,
  Action 自动剥元数据、转档、去重、写回本仓 `photos/` 与 `assets/video/`、跑 build、提交推送。
  ★原始文件只留在私有仓,永不进本仓及本仓 git 历史。★
- **隐藏上传页** `admin-i6dx95cb/index.html`:`noindex`,不在任何导航/sitemap 里;
  纯前端零外部资源、不含任何密钥;令牌只存 `localStorage` 并提供「清除令牌」;
  含令牌生成三步图文说明、板块下拉(含「首屏视频」)、多选/拖拽上传 + 进度条 +
  失败重试一次、按板块看现有照片并删除。
- **示意图退场**:`load_photos()` 里实现 —— 某板块只要出现 `placeholder` 非真的条目,
  该板块示意图整批不渲染,「示意图片 · 客片持续更新」标注随之消失。
  索引条目仍保留,可逆。`credits.html` 用同一份过滤视图,与站上所见一致。

### 品牌防误译
- 浏览器自动翻译会把「流涟旅拍 / Liulian」译成「六莲 / 刘莲摄影」。
  给品牌字标、首屏大标题、「关于流涟」标题、页脚版权行、十地 chip、十地面板标题、
  地图标点与地名文字加 `translate="no"` 与 `class="notranslate"`(中英两页同改)。
- `hreflang`:两页各自列全 `zh-Hans` / `en` / `x-default`;EN 页 `<html lang="en">`。
