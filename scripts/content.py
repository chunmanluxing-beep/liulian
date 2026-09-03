# -*- coding: utf-8 -*-
"""流涟旅拍 · 内容模型(L2)
中英两套文案集中在此;build.py 只做渲染。
站上数字仅限三个有出处的:2018(创立)、200 余(合作摄影师)、10(城市与地区)。
"""

# slug, 中文名, 英文名, 高亮都府县(地图), 文化(zh), 拍摄(zh), 文化(en), 拍摄(en)
CITIES = [
 ("jingdu", "京都", "Kyoto", ["Kyōto"],
  "京都自平安时代起长期作为日本都城,清水寺、伏见稻荷大社与岚山是最具代表性的去处。东山一带保留成片的传统町屋街区,石板路与木造建筑延续至今;春季樱花、秋季红叶为全年景色最盛的两个时节。",
  "和服拍摄多安排在东山与祇园的传统街区,清晨人少、光线柔和。伏见稻荷的连排鸟居与岚山竹林适合纵深构图,行程按步行路线安排。",
  "Kyoto served as Japan's capital for over a millennium. Kiyomizu-dera, Fushimi Inari and Arashiyama are its best-known sights, and the Higashiyama district keeps whole streets of wooden townhouses. Cherry blossom in spring and maple leaves in autumn mark the two peak seasons.",
  "Kimono sessions are usually planned around Higashiyama and Gion, early in the morning when the streets are quiet. The torii rows of Fushimi Inari and the Arashiyama bamboo grove suit deep, layered compositions."),

 ("dongjing", "东京", "Tokyo", ["Tokyo"],
  "东京是日本的首都与最大城市。浅草寺与雷门保留江户风貌,涩谷、新宿代表当代都市景观;皇居外苑与明治神宫在市中心保留大片绿地,新旧街区并存是这座城市的基本面貌。",
  "都市题材以涩谷、银座与新宿的街景为主,浅草一带适合和服拍摄。傍晚至入夜的时段可拍霓虹与街道光影,室内外衔接的行程按区域集中安排。",
  "Tokyo is Japan's capital and largest city. Senso-ji and the Kaminarimon gate keep the flavour of old Edo, while Shibuya and Shinjuku stand for the contemporary city; the Imperial Palace gardens and Meiji Shrine hold broad green space in the very centre.",
  "City sessions focus on the streets of Shibuya, Ginza and Shinjuku; the Asakusa area works well for kimono. From dusk into the evening, neon and street light become the main subject."),

 ("daban", "大阪", "Osaka", ["Ōsaka"],
  "大阪自江户时代起就是商业城市,道顿堀的招牌与运河、通天阁周边的下町街区最具辨识度。大阪城天守阁与护城河一带是春季赏樱名所,城市气质市井而热闹。",
  "道顿堀与心斋桥适合夜景与街头题材,大阪城公园适合白天的开阔场景。下町街区的招牌与铺面是常用背景,拍摄节奏随街区人流调整。",
  "Osaka has been a merchant city since the Edo period. The signboards and canal of Dotonbori and the shitamachi streets around Tsutenkaku are its most recognisable scenery; the moat of Osaka Castle is a famous spot for spring blossom.",
  "Dotonbori and Shinsaibashi suit night and street work, while Osaka Castle Park offers open daytime scenes. The signage and shopfronts of the old quarters serve as familiar backdrops."),

 ("nailiang", "奈良", "Nara", ["Nara"],
  "奈良曾为古代日本的都城,东大寺与春日大社列入世界遗产,奈良公园内成群的鹿在步道间自由活动。历史建筑集中、主要景点之间步行可达,秋季红叶与开阔的草坡是它的另一重景色。",
  "与鹿同框是奈良最常见的拍法,清晨游客少、鹿群安静。东大寺参道与春日大社的石灯笼群适合和服题材,行程可在半日内走完。",
  "Nara was the capital of ancient Japan. Todai-ji and Kasuga Taisha are World Heritage sites, and the deer of Nara Park wander freely among the paths. The historic quarter is compact and walkable, with maple colour and open lawns in autumn.",
  "Photographs with the deer are the classic Nara shot; early mornings are calm and uncrowded. The approach to Todai-ji and the stone lanterns of Kasuga Taisha suit kimono sessions well."),

 ("fushishan", "富士山", "Mt. Fuji", ["Shizuoka", "Yamanashi"],
  "富士山是日本最高峰,山体横跨静冈、山梨两县,已列入世界文化遗产。河口湖、山中湖一带视野开阔,冬春两季山顶积雪,晴天时轮廓完整,是日本最具代表性的自然景观。",
  "拍摄多安排在河口湖周边与忠灵塔一带,清晨云量少、山体清晰的概率更高。秋季红叶与冬季雪景是一年中最受欢迎的时段。",
  "Mt. Fuji is Japan's highest mountain, straddling Shizuoka and Yamanashi and inscribed as World Cultural Heritage. The Kawaguchiko and Yamanakako lakesides open onto wide views; from winter into spring the summit holds snow and the outline stands sharp on clear days.",
  "Sessions are usually planned around Lake Kawaguchi and the Chureito pagoda. Early mornings give the best chance of a cloud-free mountain; autumn colour and winter snow are the favourite seasons."),

 ("yidou", "伊豆半岛", "Izu Peninsula", ["Shizuoka"],
  "伊豆半岛位于静冈县东部,以海岸线与温泉著称。城崎海岸的火山岩礁、下田的旧港街区与河津的早樱各具特色;半岛内温泉旅馆密集,是关东近郊的传统度假地。",
  "海岸题材以城崎海岸与西伊豆的落日为主,春季河津樱花期适合花景人像。区域之间车程较长,拍摄按半岛东西两侧分区安排。",
  "The Izu Peninsula, in eastern Shizuoka, is known for its coastline and hot springs. The volcanic rock shore of Jogasaki, the old port streets of Shimoda and the early cherry blossom of Kawazu each have their own character.",
  "Coastal work centres on Jogasaki and the sunsets of western Izu; the Kawazu blossom season suits portraits among the trees. Distances are long, so sessions are grouped by one side of the peninsula or the other."),

 ("liancang", "镰仓", "Kamakura", ["Kanagawa"],
  "镰仓曾是武家政权的所在地,高德院大佛与鹤冈八幡宫为代表古迹。江之电沿海岸行驶,镰仓高校前一带的海景平交道广为人知;老街小巷与海岸在半日内均可走到。",
  "大佛、江之电与海岸是三类常用场景,午后逆光下的海面层次丰富。长谷一带的小巷安静,适合放慢节奏的拍摄。",
  "Kamakura was once the seat of Japan's first warrior government. The Great Buddha of Kotoku-in and Tsurugaoka Hachimangu are its landmark sites, and the Enoden line runs along the shore past the well-known seaside crossing at Kamakura-Kokomae.",
  "The Buddha, the Enoden line and the shore make three staple settings; in afternoon backlight the sea gains depth. The lanes around Hase are quiet and suit an unhurried pace."),

 ("fuguang", "福冈", "Fukuoka", ["Fukuoka"],
  "福冈面向博多湾,是九州最大的城市。太宰府天满宫供奉学问之神,参道保留传统铺面;中洲的屋台在夜间沿河排开,大濠公园与海滨地带是市民的日常去处,城市节奏舒缓。",
  "太宰府参道与大濠公园适合白天拍摄,中洲屋台的灯光适合夜景人像。海滨百道一带的现代建筑可作对比场景。",
  "Fukuoka faces Hakata Bay and is the largest city on Kyushu. Dazaifu Tenmangu is dedicated to the deity of learning, its approach lined with traditional shopfronts; at night the yatai food stalls of Nakasu open along the river.",
  "The Dazaifu approach and Ohori Park suit daytime sessions, while the lamplight of the yatai suits evening portraits. The modern seaside district of Momochi offers a contrasting backdrop."),

 ("zhahuang", "札幌", "Sapporo", ["Hokkaidō"],
  "札幌是北海道的中心城市,大通公园贯穿市中心,旧道厅的红砖建筑保留开拓时期的风貌。冬季降雪量大,雪祭期间大通公园设有大型雪雕;夏季凉爽,两季各有景色。",
  "冬季雪景是主要题材,大通公园与旧道厅一带以雪后清晨为佳。夏季以街区与近郊花田为主,光线通透。",
  "Sapporo is the principal city of Hokkaido. Odori Park runs through the centre, and the red-brick Former Government Office keeps the look of the pioneering era. Winters bring heavy snow and the famous snow festival; summers stay cool and clear.",
  "Snow scenes are the main winter subject, best on clear mornings after fresh snowfall around Odori Park. In summer the city streets and nearby flower fields take over, in bright, clean light."),

 ("xiaozun", "小樽", "Otaru", ["Hokkaidō"],
  "小樽因港口与运河而兴,运河沿岸的石造仓库群保留明治、大正时期的风貌,如今多为工房与餐馆。堺町通的玻璃工艺与音乐盒馆延续着手工业传统;冬雪中的运河夜景最为知名。",
  "运河沿岸适合黄昏与夜间拍摄,雪季煤气灯亮起后氛围最好。堺町通的老建筑立面是白天的主要背景。",
  "Otaru grew around its port and canal. The stone warehouses along the water keep the look of the Meiji and Taisho eras and now house workshops and restaurants; Sakaimachi street carries on the town's glasswork tradition.",
  "The canal bank suits dusk and evening sessions, at its best in the snow season once the gas lamps are lit. By day, the old facades of Sakaimachi street serve as the main backdrop."),
]

# slug, 中文名, 英文名, 介绍(zh), 介绍(en)
TYPES = [
 ("xingtai-hefu", "和服旅拍", "Kimono sessions",
  "以传统街区与神社寺院为主要场景。拍摄当日先完成着装与发型整理,再按所选地区的步行路线外景拍摄。适合初次到访日本、希望以传统装束留影的客人。",
  "Set in historic districts and temple grounds. On the day, dressing and hair styling come first; the session then moves outdoors along a planned walking route. A natural choice for first-time visitors who want portraits in traditional dress."),
 ("xingtai-jiating", "家庭常服", "Family sessions",
  "不更换服装,以公园、街区与海岸等开放场景为主。过程以记录为主、不摆固定姿势,儿童与长辈均可参与,适合家庭旅行途中的纪念拍摄。",
  "Shot in everyday clothes, in parks, streets and along the shore. The approach is documentary rather than posed, and works for children and grandparents alike — a record of the family trip as it happened."),
 ("xingtai-hunsha", "婚纱", "Wedding portraits",
  "提供婚纱与和装两个方向,场景可选庭园、海岸、街区或山景。拍摄前确认服装、场景与时段,当日按既定路线进行,适合婚前拍摄与结婚纪念。",
  "Available in both Western dress and traditional Japanese wasō, set in gardens, along the coast, in old streets or against the mountains. Dress, location and timing are settled beforehand; the day itself follows the agreed route."),
 ("xingtai-huiyi", "会议活动摄影", "Event photography",
  "覆盖企业会议、展会与庆典等场合,内容包括会场、流程与人物记录,成片按活动进程整理交付。适合在日举办活动的企业与团体。",
  "Coverage for corporate meetings, trade shows and ceremonies: the venue, the programme and the people, delivered in the order the event unfolded. For companies and groups holding events in Japan."),
]

T = {
 "zh": {
   "lang": "zh-Hans", "dir": "", "other": "en/index.html", "other_label": "EN",
   "title": "流涟旅拍 · 日本旅拍与活动摄影",
   "desc": "流涟旅拍创立于 2018 年,合作摄影师 200 余名,遍布全日本。在 10 个城市与地区提供和服旅拍、家庭常服、婚纱与会议活动摄影服务。",
   "brand": "流涟旅拍",
   "hero_t": "流涟旅拍",
   "hero_s": "在日本 10 个城市与地区提供旅拍与活动摄影服务。",
   "cta1": "邮件咨询", "cta2": "Instagram",
   "s2_h": "作品", "s2_p": "按拍摄地整理,点击查看大图。",
   "ph_note": "示意图片 · 客片持续更新",
   "s3_h": "拍摄地区", "s3_p": "覆盖 10 个城市与地区,点击查看当地介绍与作品。",
   "map_lg": "地图数据:Natural Earth(公有领域)。点击地名或区域查看该地详情。",
   "s4_h": "业务范围", "s4_p": "四类拍摄服务,均由当地摄影师执行。",
   "s5_h": "关于流涟",
   "about_p": "流涟旅拍创立于 2018 年,合作摄影师 200 余名,遍布全日本。业务涵盖和服旅拍、家庭常服、婚纱与会议活动摄影,拍摄地覆盖京都、东京、大阪等 10 个城市与地区。咨询与预订通过邮箱与 Instagram 进行。",
   "about": [("2018", "年创立"), ("200 余", "名合作摄影师,遍布全日本"), ("10", "个城市与地区")],
   "s6_h": "预订与联系", "s6_p": "咨询与预订通过邮箱或 Instagram 私信进行。",
   "email_label": "邮箱", "email_sub": "咨询与合作", "ig_label": "Instagram", "ig_sub": "作品与私信",
   "foot_c": "© 流涟旅拍", "foot_n": "作品照片均经客人授权后展示。",
   "credits_link": "图片来源",
   "ph_photo": "图片位", "swipe": "◀ 左右滑动 ▶", "alt_sample": "示意图片",
   "nav": [("#gallery", "作品"), ("#areas", "地区"), ("#types", "业务"), ("#about", "关于"), ("#contact", "联系")],
   "lb_close": "关闭", "lb_prev": "上一张", "lb_next": "下一张",
   "panel_close": "关闭", "panel_book": "预订咨询 →",
   "panel_h_cul": "地区", "panel_h_shoot": "拍摄",
   "contacts": [],
 },
 "en": {
   "lang": "en", "dir": "../", "other": "../index.html", "other_label": "中文",
   "title": "Liulian Photography · Portrait and event photography across Japan",
   "desc": "Founded in 2018, Liulian Photography works with over two hundred photographers across Japan, offering kimono, family, wedding and event photography in ten cities and regions.",
   "brand": "Liulian",
   "hero_t": "Liulian Photography",
   "hero_s": "Portrait and event photography in ten cities and regions across Japan.",
   "cta1": "Email us", "cta2": "Instagram",
   "s2_h": "Work", "s2_p": "Arranged by location — select any photograph to see it larger.",
   "ph_note": "Sample images · client work being added",
   "s3_h": "Where we shoot", "s3_p": "Ten cities and regions — select a place to read about it and see the work made there.",
   "map_lg": "Map data: Natural Earth (public domain). Click a name or region for details.",
   "s4_h": "Services", "s4_p": "Four kinds of session, each handled by photographers based in the area.",
   "s5_h": "About Liulian",
   "about_p": "Liulian Photography was founded in 2018 and works with over two hundred partner photographers across Japan. Its services cover kimono, family, wedding and event photography, in ten cities and regions including Kyoto, Tokyo and Osaka. Enquiries and bookings are handled by email and through Instagram.",
   "about": [("2018", "founded"), ("200+", "partner photographers across Japan"), ("10", "cities and regions")],
   "s6_h": "Booking and contact", "s6_p": "For enquiries and bookings, write to us by email or send a message on Instagram.",
   "email_label": "Email", "email_sub": "Enquiries and partnerships", "ig_label": "Instagram", "ig_sub": "Work and messages",
   "foot_c": "© Liulian Photography", "foot_n": "Client photographs are shown with permission.",
   "credits_link": "Image credits",
   "ph_photo": "IMAGE SLOT", "swipe": "◀ swipe ▶", "alt_sample": "Sample image",
   "nav": [("#gallery", "Work"), ("#areas", "Places"), ("#types", "Services"), ("#about", "About"), ("#contact", "Contact")],
   "lb_close": "Close", "lb_prev": "Previous", "lb_next": "Next",
   "panel_close": "Close", "panel_book": "Book or enquire →",
   "panel_h_cul": "The place", "panel_h_shoot": "The shoot",
   "contacts": [],
 },
}

EMAIL = "1297435105@qq.com"
INSTAGRAM = "https://www.instagram.com/liulian_travel/"
INSTAGRAM_LABEL = "@liulian_travel"

# 地图标签排布:slug → (标签锚点 x, y, 对齐 start|end|middle)
LABELS = {
 "jingdu":   (300, 630, "end"),
 "daban":    (282, 700, "end"),
 "nailiang": (392, 726, "start"),
 "dongjing": (588, 606, "start"),
 "liancang": (588, 668, "start"),
 "fushishan":(446, 610, "end"),
 "yidou":    (505, 716, "middle"),
 "fuguang":  (80, 792, "start"),
 "zhahuang": (664, 172, "start"),
 "xiaozun":  (560, 122, "end"),
}
