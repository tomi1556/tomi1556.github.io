# 灯原サイトの組み立て（ヘッダーとフッターを各ページに入れて、静的な HTML を書き出す）
import datetime, math, pathlib, re as _re0
from cast import CAST, BY, SCARF, CLOAK, fig, eater, reds, ridge, say_box

ADDR = "tomoshibara.life"
DISCORD = "https://discord.gg/wAKGQBHmPS"
SITE = "https://tomoshibara.life"
NAV = [("index.html", "トップ"), ("start.html", "はじめる"), ("guide.html", "遊び方"), ("events.html", "夜祭"), ("rules.html", "きまり"), ("support.html", "支える")]

LOGO = '<svg width="30" height="36" viewBox="0 0 10 12" aria-hidden="true" style="display:block;shape-rendering:crispEdges"><rect x="2" y="0" width="6" height="1" fill="currentColor"/><rect x="1" y="1" width="8" height="1" fill="currentColor"/><rect x="1" y="2" width="1" height="6" fill="currentColor"/><rect x="8" y="2" width="1" height="6" fill="currentColor"/><rect x="2" y="2" width="6" height="6" fill="#F2B544"/><rect x="4" y="4" width="2" height="2" fill="#FFF1C4"/><rect x="1" y="8" width="8" height="1" fill="currentColor"/><rect x="4" y="9" width="2" height="3" fill="currentColor"/></svg>'


def addr_box(extra=""):
    return f'''<div class="addr"{extra}>
  <span class="addr-t"><small>アドレス（Java版・統合版 共通）</small><b>{ADDR}</b></span>
  <span class="addr-p"><small>統合版のポート</small><b>5156</b></span>
  <button type="button" class="pbtn" data-copy="{ADDR}">アドレスをコピー</button>
</div>
<p class="addr-note" data-note role="status">統合版は、ポートの 19132 を <b class="port">5156</b> に書きかえてください。Java版はアドレスだけで入れます。</p>'''


# ナビのアイコン（16×16 のドット絵。# は線、o は灯りの色）
ICONS = {
    "index.html": ["......####......", ".....######.....", ".....#....#.....", ".....#oooo#.....", ".....#oooo#.....", ".....#oooo#.....", ".....#oooo#.....", ".....######.....", ".......##.......", ".......##.......", ".......##.......", ".......##.......", ".......##.......", "......####......", ".....######.....", "................"],
    "start.html": ["................", "...##########...", "...#........#...", "...#........#...", "...#....#...#...", "...#....##..#...", "...#.######.#...", "...#.#######o...", "...#.######.#...", "...#....##..#...", "...#....#...#...", "...#........#...", "...#........#...", "...##########...", "................", "................"],
    "guide.html": ["................", "................", ".######..######.", ".#....#..#....#.", ".#.oo.#..#.oo.#.", ".#....#..#....#.", ".#.oo.#..#.oo.#.", ".#....#..#....#.", ".#.oo.#..#.oo.#.", ".#....#..#....#.", ".#....####....#.", ".##############.", "................", "................", "................", "................"],
    "events.html": ["................", "......####......", ".......##.......", ".....######.....", "....#oooooo#....", "...#oooooooo#...", "...##########...", "...#oooooooo#...", "...#oooooooo#...", "...##########...", "...#oooooooo#...", "....#oooooo#....", ".....######.....", ".......##.......", "......####......", "................"],
    "support.html": ["................", "................", "..####....####..", ".#oooo#..#oooo#.", "#oooooo##oooooo#", "#oooooooooooooo#", "#oooooooooooooo#", ".#oooooooooooo#.", "..#oooooooooo#..", "...#oooooooo#...", "....#oooooo#....", ".....#oooo#.....", "......#oo#......", ".......##.......", "................", "................"],
    "rules.html": ["................", "..###########...", "..#.........#...", "..#.oooooo..#...", "..#.........#...", "..#.oooooooo#...", "..#.........#...", "..#.oooooo..#...", "..#.........#...", "..#.oooo....#...", "..#.........#...", "..#......####...", "..#......#.#....", "..#......##.....", "..#########.....", "................"],
}


def icon(h):
    rects = []
    for y, row in enumerate(ICONS[h]):
        for x, ch in enumerate(row):
            if ch != ".":
                rects.append(f'<rect x="{x}" y="{y}" width="1" height="1" class="{"ic-l" if ch == "o" else "ic-s"}"/>')
    return '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true">' + "".join(rects) + "</svg>"


def header(cur):
    links = "".join(f'<a href="{h}" class="nl"{" aria-current=\"page\"" if h == cur else ""}>{icon(h)}<span>{t}</span></a>' for h, t in NAV)
    return f'''<a href="#content" class="skip">本文へ進む</a>
<header class="hdr"><div class="wrap hdr-in">
  <a href="index.html" class="logo">{LOGO}<span>灯原</span></a>
  <nav class="nav" aria-label="メイン">{links}</nav>
  <button type="button" class="qs-btn" data-qs aria-label="サイト内を探す（Ctrl+K）"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="2" width="6" height="2"/><rect x="2" y="3" width="2" height="6"/><rect x="8" y="3" width="2" height="6"/><rect x="3" y="8" width="6" height="2"/><rect x="9" y="9" width="2" height="2"/><rect x="11" y="11" width="2" height="2"/><rect x="12" y="12" width="2" height="2"/></svg><span>探す</span><kbd class="dot">Ctrl K</kbd></button>
  <a href="{DISCORD}" class="pbtn dbtn sm" target="_blank" rel="noopener">Discord に参加</a>
</div></header>'''


def footer():
    ch = "".join(f'<li><a href="guide-{c["id"]}.html">{c["t"]}</a></li>' for c in CH)
    cols = [
        ("はじめる", [("start.html#join", "入り方"), ("start.html#first", "最初の夜"), ("playstyle.html", "遊び方を選ぶ"), ("commands.html", "コマンド一覧"), ("start.html#faq", "よくある質問")]),
        ("遊び方", None),
        ("Wiki", [("wiki.html", "Wiki のはじめ"), ("wiki.html#all", "すべての技を探す"), ("wiki.html#trials", "奥義の試練"), ("wiki.html#tasks", "今日の務め"), ("wiki-hiuo.html", "灯魚図鑑"), ("wiki-build.html", "技の組み立て"), ("akashi.html", "灯の証 Wiki"), ("himon.html", "灯紋 Wiki"), ("hisato.html", "灯里 Wiki")]),
        ("灯原", [("events.html", "夜祭"), ("characters.html", "ひとびと"), ("rules.html", "きまり"), ("support.html", "支える"), (DISCORD, "Discord")]),
    ]
    cm = ""
    for h, items in cols:
        lis = ch if items is None else "".join(f'<li><a href="{u}"{" target=\"_blank\" rel=\"noopener\"" if u.startswith("http") else ""}>{t}</a></li>' for u, t in items)
        cm += f'<div class="fm"><h3>{h}</h3><ul>{lis}</ul></div>'
    # 灯りの輪：6人と灯籠、闇の端に灯喰い
    xs = [14, 25, 38, 55, 68, 80]
    camp = "".join(f'<span class="cm" style="left:{x}%">{fig(c["id"], i % 2 == 0)}</span>' for i, (x, c) in enumerate(zip(xs, CAST)))
    camp += "".join(f'<span class="lp" style="left:{x}%"><i class="rl" style="--d:0s"><i class="rl-g"></i><i class="rl-c"></i><i class="rl-h" style="background:var(--amber);box-shadow:0 0 18px 4px rgba(242,181,68,.75)"></i><i class="rl-p"></i></i></span>' for x in (6, 46, 89))
    camp += f'<span class="cm foe" style="left:97%">{eater()}</span>'
    return f'''<footer class="foot s-rock"><div class="edge"></div>
  <div class="wrap foot-cta">
    <div><h2 class="disp" style="font-size:clamp(30px,4.6vw,56px);line-height:1.3;margin-bottom:24px">夜は、ひとりより大勢で。</h2>
    {addr_box()}</div>
    <div class="btns"><a href="start.html" class="gbtn">入り方を見る</a><a href="{DISCORD}" class="pbtn dbtn" target="_blank" rel="noopener">Discord に参加</a></div>
  </div>
  <div class="camp" aria-hidden="true"><div class="camp-in">{camp}</div><div class="camp-g"></div></div>
  <div style="background:#101215">
  <nav class="wrap foot-map" aria-label="サイトの地図">{cm}</nav>
  <div class="wrap foot-end"><a href="index.html" class="logo">{LOGO}<span>灯原</span></a><p class="legal">灯原は非公式のファンサーバーです。Mojang Studios および Microsoft とは関係ありません。Minecraft は Mojang Synergies AB の商標です。</p></div>
  </div>
</footer>
<div class="gauge" aria-hidden="true"><i></i></div>'''


# 夜空の下に敷く景色の縁（ページごとに、立っている人とひとことが変わる）
RIDGE = {
    "start.html": dict(seed=2, cast=[("hino", 9, True)], say=("hino", "最初の1基は、ここに置こう。")),
    "guide.html": dict(seed=3, cast=[("hino", 7, True), ("yuki", 37, False)], say=("yuki", "12の章に、ぜんぶ書いたよ。")),
    "events.html": dict(seed=4, cast=[("momo", 10, True), ("hino", 13, False), ("sora", 34, True)], say=("momo", "土曜の21時、広場でね！")),
    "rules.html": dict(seed=5, cast=[("shino", 9, True)], say=("shino", "人の灯りは、守るもの。")),
    "support.html": dict(seed=6, cast=[("yuki", 9, True), ("hino", 12, False)], say=("yuki", "名前は、ちゃんと残すからね。")),
    "404.html": dict(seed=7, cast=[("hino", 12, True)], say=("hino", "あれ……こっちは闇の中だ。"), eaters=(40,)),
    "characters.html": dict(seed=8, cast=[("hino", 6, True), ("momo", 13, False), ("sora", 20, True), ("waka", 27, False), ("shino", 34, True), ("yuki", 41, False)], lamps=4),
    "commands.html": dict(seed=9, cast=[("hino", 9, True)], say=("hino", "/tomoshibi だけ覚えれば大丈夫。")),
    "wiki.html": dict(seed=10, cast=[("yuki", 9, True), ("waka", 36, False)], say=("yuki", "130の技、ぜんぶ書きとめたよ。")),
    "wiki-hiuo.html": dict(seed=11, cast=[("sora", 10, True)], say=("sora", "「秘」の魚は、まだ見つからない……")),
}
_CH_WHO = {"lantern": "hino", "night": "shino", "higui": "shino", "buff": "momo", "hiwaza": "waka", "fish": "sora", "himon": "yuki", "akashi": "yuki", "more": "sora", "sato": "hino", "shoku": "waka", "musubi": "momo"}
_PATH_WHO = {"light": "hino", "night": "shino", "mine": "momo", "wood": "waka", "farm": "waka", "fish": "sora", "craft": "yuki", "travel": "sora", "ranch": "momo", "arcane": "hino"}


def _ridge_for(file):
    if file in RIDGE:
        return ridge(**RIDGE[file])
    m = _re0.match(r"guide-(\w+)\.html", file)
    if m:
        k = [c["id"] for c in CH].index(m.group(1))
        who = _CH_WHO[m.group(1)]
        return ridge(seed=20 + k, cast=[(who, 9, True)], eaters=(41,) if m.group(1) == "higui" else ())
    if file.startswith("akashi"):
        return ridge(seed=60 + len(file), cast=[("yuki", 9, True)], say=("yuki", "ぜんぶ、書きとめておいたよ。") if file == "akashi.html" else None)
    m = _re0.match(r"wiki-(\w+)\.html", file)
    if m and m.group(1) in _PATH_WHO:
        return ridge(seed=40 + len(m.group(1)), cast=[(_PATH_WHO[m.group(1)], 9, True)])
    return ridge(seed=1)


def _with_ridge(file, body):
    """先頭の夜空（.hero）の終わりに景色の縁を入れ、次のセクションに縁（ギザギザ）がなければつける。"""
    if not body.startswith('<div class="hero') or "data-scene" in body[:2000]:
        return body
    i = body.find("<section")
    head, rest = (body[:i], body[i:]) if i >= 0 else (body, "")
    j = head.rstrip().rfind("</div>")
    head = head[:j] + "  " + _ridge_for(file) + "\n" + head[j:]
    if rest:
        k = rest.index(">") + 1
        if '<div class="edge">' not in rest[k:k + 40]:
            rest = rest[:k] + '\n  <div class="edge"></div>' + rest[k:]
    return head + rest


def page(file, title, desc, body, hero_min=""):
    cur = file if file in dict(NAV) else ("guide.html" if file.startswith(("guide-", "wiki", "akashi")) else "start.html" if file in ("commands.html", "playstyle.html") else "")
    body = _with_ridge(file, body)
    url = SITE + ("/" if file == "index.html" else "/" + file)
    is_top = file == "index.html"
    return f'''<!doctype html>
<html lang="ja" class="nojs">
<head>
<script>document.documentElement.className="js";if(matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.className+=" rm"</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#070E20">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="灯原">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=DotGothic16&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
{header(cur)}
<main>
{body}
</main>
{footer()}
<script src="assets/site.js" defer></script>
<script src="assets/fx.js" defer></script>{"<script src=\"assets/hero.js\" defer></script>" if is_top else ""}
</body>
</html>
'''


def sub_hero(cur, h1, lead, toc):
    t = "".join(f'<a href="#{i}">{n}</a>' for i, n in toc)
    return f'''<div class="hero">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div><div class="moon" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    <h1 class="disp h1-sub">{h1}</h1>
    <p class="lead">{lead}</p>
    {f'<nav class="toc" aria-label="このページの内容">{t}</nav>' if t else ''}
  </div>
</div>'''


def cd(kind, label):
    return f'''<div class="cd" role="timer" aria-label="{label}" data-{kind}-cd>
  <div class="cd-u"><b data-u="d">–</b><span>日</span></div><div class="cd-u"><b data-u="h">––</b><span>時間</span></div><div class="cd-u"><b data-u="m">––</b><span>分</span></div><div class="cd-u"><b data-u="s">––</b><span>秒</span></div>
</div>'''


_CMD_N = [0]
_CMDS = [
    ("導", "#FFE3A3", "灯原のメニュー", "Hishirube", "はじめて来たときに渡す「灯しるべ」を右クリックしても、同じメニューが開きます。", [
        ("/menu", "", "灯原のメニューを開く。<b>迷ったらこれ</b>。灯籠・灯技・灯紋・灯の証・里・灯結のすべてへ（<span class=\"kbd\">/tomoshibara</span> でも同じ）"),
        ("/menu item", "", "灯しるべ（右クリックでメニューが開く品）をもう一度もらう"),
        ("/link", "", "Discord とつなぐ。出た6けたの数字を、Discord の「はじめての方へ」→「Discord と連携」か <span class=\"kbd\">/link 数字</span> に入れる。はじめてつなぐと灯籠5基"),
        ("/link status", "", "いまつながっている Discord を見る"),
        ("/link off", "", "Discord との連携を外す"),
        ("/hud", "", "上のバー（ボスバー）・下の文字（アクションバー）・効果音を切りかえる。<span class=\"kbd\">/hud bar off</span>・<span class=\"kbd\">/hud action off</span>・<span class=\"kbd\">/hud sound off</span>・<span class=\"kbd\">/hud on</span>。メニューのいちばん上、自分の名前の右の3つの札でも切りかえられる"),
    ]),
    ("灯", "#F2B544", "灯籠と灯路", "Tomoshibi", "灯籠を素手で右クリックしても、同じメニューが開きます。", [
        ("/tomoshibi", "", "メニューを開く。<b>これだけ覚えれば大丈夫</b>（<span class=\"kbd\">/tomo</span> でも同じ）"),
        ("/tomoshibi info", "", "いま立っている灯路網と、灯籠の数"),
        ("/tomoshibi recipe", "", "灯籠の作り方"),
        ("/tomoshibi buffs", "", "加護を見る・欠片で解放する"),
        ("/tomoshibi name", "<名前>", "近くの自分の灯籠を灯標にする（16文字まで）"),
        ("/tomoshibi unname", "", "灯標の名前を取り消す"),
        ("/tomoshibi list", "", "行ける灯標の一覧"),
        ("/tomoshibi go", "<名前>", "灯標へ灯渡り"),
        ("/tomoshibi home", "", "「帰る場所」に決めた灯標へ灯渡り"),
        ("/tomoshibi trust", "<名前>", "仲間にする（もう一度で外す）。いまサーバーにいる人だけ"),
        ("/tomoshibi colors", "", "灯りの色の一覧"),
        ("/tomoshibi color", "<色>", "灯りの色を変える"),
        ("/tomoshibi invite", "", "自分の招待コードを見る"),
        ("/tomoshibi code", "<コード>", "友達の招待コードを使う"),
        ("/tomoshibi particles", "<off|low|normal>", "自分に見える光の粒の量（重いときは low）"),
        ("/tomoshibi top", "", "灯籠の多い人"),
    ]),
    ("里", "#E9824A", "灯里", "Hisato", "<span class=\"kbd\">/sato</span> は <span class=\"kbd\">/hisato</span> でも同じ。里の灯帳を手に持って右クリックするか、里灯を素手で右クリックしても、同じホームが開きます。", [
        ("/sato", "", "里のホームを開く。<b>これだけ覚えれば大丈夫</b>（里のない人は、里を探す・開く画面）"),
        ("/sato job", "", "職の画面（位・バフ・匠の試し・転職の試し・弟子）"),
        ("/sato board", "", "掲示板（日課・週課・里の頼み・大事業）"),
        ("/sato kura", "", "蔵（棚・納める・出し入れの記録）"),
        ("/sato map", "", "里の地図（土地・屋敷・建築中の区画・喰われた灯籠）"),
        ("/sato musubi", "", "灯結（縁・一団・合流・手紙・合図・配信中・離れる）"),
        ("/sato mail", "", "受信箱（手紙・小包・里の知らせ・里の便り）"),
        ("/sato home", "", "帰里：里灯へ帰る（待ち時間あり）"),
        ("/sato party", "[言葉]", "一団の画面を開く。言葉をつけると、一団にだけ話す"),
        ("/sato c", "<言葉>", "里の民にだけ話す"),
        ("/sato accept", "", "誘い・申し込み・合流の頼みを受ける（チャットの［受ける］を押しても同じ）"),
        ("/sato deny", "", "断る"),
        ("/sato book", "", "里の灯帳をもう一度もらう"),
    ]),
    ("証", "#F29BB8", "灯の証", "Akashi", "報酬の受け取り、称号・足跡の選択は、画面からもできます。", [
        ("/akashi", "", "証の一覧を開く"),
        ("/akashi claim", "", "報酬をまとめて受け取る"),
        ("/akashi top", "", "証の番付"),
        ("/akashi stats", "[名前]", "記録を見る"),
        ("/akashi track", "<id|off>", "証を追跡する（画面の上に進み具合が出る）"),
        ("/akashi title", "<id|off>", "称号を選ぶ"),
        ("/akashi trail", "<id|off>", "足跡を選ぶ"),
        ("/akashi supporter", "[hide|show]", "支え手の ❤ と、サイトの「支え手の壁」に載せるかどうか"),
    ]),
    ("技", "#5AAAFF", "灯技", "Hiwaza", "<span class=\"kbd\">/waza</span> は <span class=\"kbd\">/hiwaza</span> でも同じ。便利な技は、覚えたあとで使えます。", [
        ("/waza", "", "技の画面を開く（技の木・使う技・今日の務め・灯魚図鑑）"),
        ("/waza use", "[技]", "使う技の一覧／その技を使う"),
        ("/waza main", "<技>", "主技を決める（しゃがみ2回で使う）"),
        ("/waza sub", "<技>", "副技を決める（しゃがんで F で使う）"),
        ("/waza tasks", "", "今日の務め"),
        ("/waza fish", "", "灯魚図鑑"),
        ("/waza top", "", "番付"),
        ("/waza craft", "", "携帯作業台", "匠"),
        ("/waza ender", "", "携帯エンダーチェスト", "匠"),
        ("/waza bag", "", "背負い籠（自分だけの入れ物）", "匠"),
        ("/waza sort", "", "持ち物を整頓", "匠"),
        ("/waza stash", "", "まとめ入れ（同じ物が入った近くの箱へ）", "匠"),
        ("/waza bottle", "", "経験の瓶詰め", "術"),
        ("/waza mark", "", "しるべ（印への方角と距離）", "旅"),
        ("/waza mark clear", "", "しるべを消す", "旅"),
    ]),
    ("紋", "#F2B544", "灯紋", "Himon", "<span class=\"kbd\">/mon</span> は <span class=\"kbd\">/himon</span> でも同じ。", [
        ("/himon", "", "紋書を引く画面を開く（5つの段から、経験値で引く）"),
        ("/himon engrave", "", "道具に紋を刻む・外す画面を開く"),
        ("/himon book", "", "紋帳（見つけた紋と回数）"),
    ]),
    ("祭", "#C79BFF", "夜祭", "Yomatsuri", "何もしなければ参加です。", [
        ("/yomatsuri", "", "次の夜祭と、自分の参加回数（<span class=\"kbd\">/matsuri</span> でも同じ）"),
        ("/yomatsuri out", "", "今回は参加しない"),
        ("/yomatsuri in", "", "やっぱり参加する"),
        ("/yomatsuri vote", "<名前>", "建築早押しで、いちばん良い建物に投票（自分には入れられません）"),
    ]),
    ("夜", "#9C8CFF", "長い夜", "Tokoyo", "", [
        ("/tokoyo", "", "いまが昼か夜か、夜明けまでの時間、夜の敵の強さ（<span class=\"kbd\">/yoru</span> でも同じ）"),
    ]),
]


# ───────────────────────── トップ ─────────────────────────
index = f'''<div class="hero hero-top" style="min-height:min(900px,100svh)">
  <div class="bars" aria-hidden="true"><i></i><i></i></div>
  <div class="sky"></div><div class="stars" aria-hidden="true"></div><div class="moon" aria-hidden="true"></div><div class="dusk" aria-hidden="true"></div>
  <div class="wrap hero-body" id="content">
    <a href="#season" class="chip fadein"><i></i><span>シーズン1「灯ノ海」</span><b data-season-short>11月7日（土）21:00 開幕</b></a>
    <span class="online" data-online><i></i>いま <b>0</b> 人が参加中</span>
    <h1 class="disp h1 reveal">灯りをつないで、<br>夜の果てまで。</h1>
    <p class="lead lead-hero fadein">夜が24分つづくサバイバルサーバー。灯籠を置いた場所だけが安全で、つなぐと道になります。Java版でも統合版でも、無料で同じ世界に入れます。</p>
    <div class="fadein" style="margin-top:32px">
      {addr_box()}
      <div class="btns" style="margin-top:6px"><a href="start.html" class="gbtn">はじめての方へ</a><a href="#film" class="gbtn">予告編を見る</a></div>
    </div>
  </div>
  <div class="scene" data-scene aria-hidden="true"></div>
  <template id="tpl-cast"><span class="who">{fig("hino", True)}</span><span class="who foe">{eater()}</span></template>
</div>

<section class="stratum tex s-soil" id="facts">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">Y=48</p>
    <h2 class="disp h2">この世界の、三つのこと。</h2>
    <p class="lead">灯原がふつうのサバイバルとちがうのは、この三つだけです。</p>
    <div class="facts">
      <div class="fact"><div class="fact-n">24<small>分</small></div><div><h3 class="h3 disp">夜が長い。</h3><p>昼は4分、夜は24分。夜の敵は体力が2.5倍、攻撃が2倍で、夜を重ねるほど強くなります。来たばかりでは、まず勝てません。</p></div></div>
      <div class="fact"><div class="fact-n">10<small>ブロック</small></div><div><h3 class="h3 disp">灯りの中は安全。</h3><p>灯籠を置くと、まわり半径10ブロックには敵が入れず、灯りの中の人は狙われません。爆発で壊れず、倒れても持ち物を失いません。近くの灯籠どうしは灯路でつながり、その上は足が速くなります。</p></div></div>
      <div class="fact"><div class="fact-n" style="color:var(--violet)">灯喰い</div><div><h3 class="h3 disp">夜は、灯りを消しに来る。</h3><p>灯りの守りを破れるのは「灯喰い」だけ。夜になると灯籠を狙い、喰われた灯籠は青い冷たい火になって、守りも道も途切れます。倒して守るか、あとで灯し直すか。つながりの多い灯籠ほど、喰われにくくなります。</p></div></div>
    </div>
  </div>
</section>

<section class="stratum s-rock" id="film">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">Y=−72</p>
    <h2 class="disp h2">予告編</h2>
    <p class="lead">62秒。音が出ます。長い夜、灯喰い、加護、灯技と灯魚と灯の証。</p>
    <div class="film" data-film><video preload="none" playsinline poster="assets/trailer-poster.jpg"><source src="assets/trailer.mp4" type="video/mp4">お使いのブラウザでは動画を再生できません。</video>
      <button type="button" class="film-play" aria-label="予告編を再生する"><i aria-hidden="true"></i><span class="dot">PLAY</span></button></div>
    <p class="film-note mu">再生すると、まわりが暗くなります。Esc か画面の外を押すと戻ります。</p>
  </div>
</section>

<section class="stratum s-deep" id="try">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">Y=24</p>
    <h2 class="disp h2">30秒で、ためしてみる。</h2>
    <p class="lead">マスを押して灯籠を置き、「夜にする」を押してください。灯喰いが来たら、押して倒します。</p>
    <div class="demo" data-demo>
      <div class="pn demo-main">
        <div class="btns" style="margin-bottom:14px"><button type="button" class="pbtn sm" data-night aria-pressed="false">夜にする</button><button type="button" class="gbtn sm" data-reset>最初の配置に戻す</button></div>
        <div class="grid-scroll"><div class="grid"></div></div>
        <div class="legend">
          <span><i style="background:#6FA347"></i>灯りの中</span>
          <span><i style="background:#16241A;border:1px solid #6F7D6A"></i>灯りの外</span>
          <span><i style="background:#F2B544"></i>灯籠</span>
          <span><i style="background:#5AAAFF"></i>喰われた灯籠（押すと灯し直す）</span>
          <span><i style="background:#0B0714;box-shadow:0 0 0 2px #B46CFF"></i>灯喰い（押すと倒す）</span>
        </div>
      </div>
      <div class="demo-side">
        <div class="stat"><span>置いた灯籠</span><b><i data-s="lan" style="font-style:normal">3</i><small> / 10</small></b></div>
        <div class="stat"><span>つながった灯路</span><b><i data-s="road" style="font-style:normal">0</i><small> 本</small></b></div>
        <div class="stat"><span>守った回数</span><b data-s="saved">0</b></div>
        <div class="stat"><span>手に入れた欠片</span><b data-s="shard">0</b></div>
        <p class="demo-msg" data-msg role="status">灯籠が3基置いてあります。マスを押して増やすか、「夜にする」を押してください。</p>
      </div>
    </div>
  </div>
</section>


<section class="stratum s-dusk" id="fest" style="padding-top:72px">
  <div class="edge"></div>
  <div class="garland" data-garland aria-hidden="true"></div>
  <div class="wrap" style="display:flex;flex-wrap:wrap;gap:40px 64px;align-items:flex-end">
    <div style="flex:1 1 440px;min-width:0">
      <p class="depth">次の夜祭</p>
      <h2 class="disp h2" style="margin-bottom:8px" data-fest-date>夜祭は毎週土曜 21:00</h2>
      <p class="mu" style="margin-bottom:22px" data-fest-lead>21時になると、120秒の募集が始まります。何もしなければ参加です。</p>
      <div data-twin-hide>{cd("fest", "次の夜祭まで")}</div>
    </div>
    <div class="pn" style="flex:1 1 360px;min-width:0">
      <p class="mu" style="font-size:14px;font-weight:700">この日のゲーム</p>
      <h3 class="disp" style="margin:6px 0 10px;font-size:32px;line-height:1.3;color:#F6B8CE" data-fest-game>週替わりで4種類</h3>
      <p style="margin-bottom:22px;font-size:16px" data-fest-desc>灯籠リレー、闇かくれんぼ、建築早押し、夜明けまで。</p>
      <a href="events.html" class="pbtn sm">夜祭について</a>
    </div>
  </div>
</section>

<section class="stratum s-soil tex" id="season">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">シーズン1</p>
    <h2 class="disp h2">「灯ノ海」は、<span style="white-space:nowrap">11月7日</span>の夜に始まる。</h2>
    <p class="lead">2026年11月7日（土）21時。まっさらな世界に、全員が同じ場所から入ります。最初の夜祭も、この夜です。</p>
    <div style="margin-top:28px" data-season-cd>{cd("season", "開幕まで").replace(' data-season-cd', '')}</div>
    <p class="note" data-season-live hidden><b>シーズン1は開催中です。</b>いまから入っても、小さな拠点は灯喰いに狙われないので、落ち着いて始められます。</p>
    <div class="three">
      <div><h3 class="h3 disp">開幕の夜の色</h3><p class="mu">開幕の夜に参加した全員に、この夜だけの灯りの色「はじまりの灯」を配ります。</p></div>
      <div><h3 class="h3 disp">3か月でひと区切り</h3><p class="mu">シーズンは約3か月。終わると世界を新しく作り直し、また全員が同じ場所から始めます。</p></div>
      <div><h3 class="h3 disp">引き継がれるもの</h3><p class="mu">灯りの色と、夜祭・招待の記録は次のシーズンへ持ち越す予定です。建物と持ち物は持ち越しません。</p></div>
    </div>
  </div>
</section>
<section class="s-stone" style="position:relative">
  <div class="edge"></div>
  <div class="wrap" style="padding-top:96px;padding-bottom:36px">
    <p class="depth">Y=0</p>
    <h2 class="disp h2">つづきは、こちらから。</h2>
  </div>
  <a href="start.html" class="band" style="background:#50555C"><div class="wrap band-in"><span class="band-y">Y=−12</span><div class="band-body"><h3 class="disp h3">はじめる</h3><p class="lead">機種ごとの入り方と、最初の夜の過ごし方。3分で入れます。</p><span class="band-go"><i></i>入り方を見る</span></div></div></a>
  <a href="guide.html" class="band" style="background:#474C53"><div class="wrap band-in"><span class="band-y">Y=−24</span><div class="band-body"><h3 class="disp h3">遊び方</h3><p class="lead">灯籠と灯路、長い夜、灯喰い、欠片で解放する加護、263の「灯の証」、130の技と106種の灯魚「灯技」、仲間と開く里と5つの職「灯里」。</p><span class="band-go"><i></i>しくみを読む</span></div></div></a>
  <a href="events.html" class="band" style="background:#3E4249"><div class="wrap band-in"><span class="band-y">Y=−36</span><div class="band-body"><h3 class="disp h3">夜祭</h3><p class="lead">毎週土曜21時。人数がそろうと、週替わりのゲームが自動で始まります。</p><span class="band-go"><i></i>今週のゲームを見る</span></div></div></a>
  <a href="rules.html" class="band" style="background:#34383E"><div class="wrap band-in"><span class="band-y">Y=−48</span><div class="band-body"><h3 class="disp h3">きまり</h3><p class="lead">してはいけないこと、守られていること、困ったときの連絡先。</p><span class="band-go"><i></i>きまりを読む</span></div></div></a>
  <a href="support.html" class="band" style="background:#2E3137;padding-bottom:40px"><div class="wrap band-in"><span class="band-y">Y=−60</span><div class="band-body"><h3 class="disp h3">支える</h3><p class="lead">灯原を続けるための寄付。PayPay で、金額は自由。お礼は名前の ❤ と、支え手の壁。</p><span class="band-go"><i></i>支え方を見る</span></div></div></a>
</section>

'''

# ───────────────────────── はじめる ─────────────────────────
start = sub_hero("start.html", "はじめる", "マインクラフトを持っていれば、3分で入れます。登録もお金もいりません。",
                 [("join", "入り方"), ("first", "最初の夜"), ("cmd", "コマンド"), ("faq", "よくある質問")]) + f'''
<section class="stratum tex s-soil" id="join">
  <div class="wrap">
    <p class="depth">手順 1</p>
    <h2 class="disp h2">機種をえらんで、入る。</h2>
    {addr_box()}
    <div class="tabs" role="tablist" aria-label="機種">
      <button type="button" class="tab" role="tab" id="t-java" aria-controls="p-java" aria-selected="true">Java版（PC）</button>
      <button type="button" class="tab" role="tab" id="t-mob" aria-controls="p-mob" aria-selected="false" tabindex="-1">スマホ・タブレット</button>
      <button type="button" class="tab" role="tab" id="t-win" aria-controls="p-win" aria-selected="false" tabindex="-1">Windows（統合版）</button>
      <button type="button" class="tab" role="tab" id="t-con" aria-controls="p-con" aria-selected="false" tabindex="-1">Switch・PS・Xbox</button>
    </div>
    <p class="mu dev-note" data-device-note hidden>お使いの端末に合わせて、タブを選んでおきました。</p>
    <div class="tabpanel" role="tabpanel" id="p-java" aria-labelledby="t-java">
      <ol class="steps">
        <li><div><h3>マインクラフトを起動して「マルチプレイ」を選ぶ</h3><p>バージョンは最新版（26.2）にしてください。</p></div></li>
        <li><div><h3>「サーバーを追加」を押す</h3><p>サーバー名は「灯原」など、わかりやすい名前でかまいません。</p></div></li>
        <li><div><h3>サーバーアドレスに <span class="kbd">{ADDR}</span> を入れる</h3><p>上の「アドレスをコピー」を押してから貼り付けると、まちがえません。</p></div></li>
        <li><div><h3>「完了」を押し、一覧から選んで「サーバーに接続」</h3><p>入ると、灯籠を3基受け取れます。</p></div></li>
      </ol>
    </div>
    <div class="tabpanel" role="tabpanel" id="p-mob" aria-labelledby="t-mob" hidden>
      <ol class="steps">
        <li><div><h3>マインクラフトを開いて「遊ぶ」を押す</h3><p>Microsoft アカウントでサインインしておいてください。</p></div></li>
        <li><div><h3>「サーバー」のタブを開き、いちばん下の「サーバーを追加」を押す</h3><p>一覧を下までスクロールすると出てきます。</p></div></li>
        <li><div><h3>3つの欄を入れる</h3><p>サーバー名：<span class="kbd">灯原</span>　サーバーアドレス：<span class="kbd">{ADDR}</span>　ポート：<span class="kbd">5156</span>（最初の 19132 から書きかえる）</p></div></li>
        <li><div><h3>「保存」を押し、一覧から「灯原」を選ぶ</h3><p>統合版の人には、押しやすい専用のメニューが出ます。</p></div></li>
      </ol>
    </div>
    <div class="tabpanel" role="tabpanel" id="p-win" aria-labelledby="t-win" hidden>
      <ol class="steps">
        <li><div><h3>Minecraft（統合版）を開いて「遊ぶ」を押す</h3><p>Minecraft Launcher では「Minecraft for Windows」を選びます。Java版とは別のものです。</p></div></li>
        <li><div><h3>「サーバー」のタブを開き、いちばん下の「サーバーを追加」を押す</h3><p>一覧を下までスクロールすると出てきます。</p></div></li>
        <li><div><h3>3つの欄を入れる</h3><p>サーバー名：<span class="kbd">灯原</span>　サーバーアドレス：<span class="kbd">{ADDR}</span>　ポート：<span class="kbd">5156</span>（最初の 19132 から書きかえる）</p></div></li>
        <li><div><h3>「保存」を押し、一覧から「灯原」を選ぶ</h3><p>Java版を持っているなら、Java版から入ってもかまいません。同じ世界です。</p></div></li>
      </ol>
    </div>
    <div class="tabpanel" role="tabpanel" id="p-con" aria-labelledby="t-con" hidden>
      <p class="note warn"><b>ゲーム機は、ひと手間かかります。</b>Switch・PlayStation・Xbox のマインクラフトには「サーバーを追加」がありません。本体の「DNS」という設定を変えて、入り口のサーバー（BedrockConnect）をとおして入ります。設定はいつでも元に戻せます。保護者の方といっしょに行ってください。</p>
      <ol class="steps" style="margin-top:20px">
        <li><div><h3>本体の DNS を「手動」にして、2つの数字を入れる</h3><p><b>Switch・Xbox</b>：優先（プライマリ）<span class="kbd">104.238.130.180</span>　代替（セカンダリ）<span class="kbd">8.8.8.8</span><br><b>PlayStation</b>：プライマリー <span class="kbd">45.55.68.52</span>　セカンダリー <span class="kbd">8.8.8.8</span><br><small class="mu">Switch：設定 → インターネット → インターネット設定 → 使っているネットワーク → 設定の変更 → DNS設定。PS5：設定 → ネットワーク → 設定 → インターネット接続を設定する → 詳細設定。Xbox：設定 → 全般 → ネットワーク設定 → 詳細設定 → DNS 設定。</small></p></div></li>
        <li><div><h3>マインクラフトの「サーバー」で、特集サーバーをどれか1つ選ぶ</h3><p>The Hive などに入ろうとすると、代わりに <b>BedrockConnect の画面</b> が開きます。開かないときは、本体を再起動してもう一度。</p></div></li>
        <li><div><h3>「Connect to a Server」で灯原を入れる</h3><p>Server Address：<span class="kbd">{ADDR}</span>　Port：<span class="kbd">5156</span>。「Add to server list」にチェックを入れておくと、次からは一覧から選ぶだけです。</p></div></li>
      </ol>
      <p class="mu" style="margin-top:12px">オンラインで遊ぶには、Switch は Nintendo Switch Online、PlayStation は PlayStation Plus、Xbox はオンラインつきの Game Pass が要ります。</p>
      <div class="btns" style="margin-top:20px"><a href="{DISCORD}" class="pbtn dbtn" target="_blank" rel="noopener">Discord で1つずつ見る</a></div>
    </div>
    <p class="note"><b>入れないときは。</b>アドレスの打ちまちがい、バージョンが古い、の2つがほとんどです。それでも入れなければ、Discord で機種と表示された文を教えてください。</p>
  </div>
</section>

<section class="stratum s-stone" id="first">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">手順 2</p>
    <h2 class="disp h2">最初の夜を、越える。</h2>
    <p class="lead">夜は24分つづき、夜の敵には、来たばかりでは勝てません。だから最初にやることは、たたかうことではなく、灯りをともすことです。</p>
    <ol class="night">
      <li><time>0分</time><div><h3>灯籠を3基受け取る</h3><p>はじめて入ると、持ち物に光る「灯籠」が3基入ります。ふつうのランタンとは別のもので、ふつうのランタンは飾りにしかなりません。灯籠は作業台で作れます（アメジストの欠片2・金インゴット2・ランタン1）。</p></div></li>
      <li><time>1分</time><div><h3>1基目を置く</h3><p>置いた場所のまわり半径10ブロックが「灯りの中」になります。敵は入ってこられず、中にいる人を狙えません。爆発で壊れず、倒れても持ち物を失いません。最初の1基は無料です。</p></div></li>
      <li><time>3分</time><div><h3>2基目を、16ブロック以内に置く</h3><p>2基が「灯路」でつながります。灯路の上は足が速くなり、つなげて置くと経験値ももらえます。</p></div></li>
      <li><time>5分</time><div><h3>メニューを開く</h3><p>持ち物の「灯しるべ」を右クリックするか、チャットに <span class="kbd">/menu</span> と打つと、灯原のメニューが開きます。灯籠・灯技・灯紋・灯の証・里・灯結の、すべての画面へここから行けます。灯籠の画面（<span class="kbd">/tomoshibi</span>）には「はじめの一歩」が6つあり、1つ達成するたびに灯籠を2基もらえます。</p></div></li>
      <li><time>夜</time><div><h3>灯りの中で過ごす</h3><p>画面の下に「灯りの中」と出ていれば安全です。灯りの外に出ると「闇の中」と出て、いちばん近い灯りの方角を教えてくれます。</p></div></li>
      <li><time>いつでも</time><div><h3>灯の証を見る</h3><p><span class="kbd">/akashi</span> で、灯原だけの進捗「灯の証」が開きます。全部で263個。すぐ届くものから、季節をまたぐものまであります。</p></div></li>
      <li><time>いつでも</time><div><h3>技を育てる</h3><p><span class="kbd">/waza</span> で「灯技」が開きます。掘る・切る・釣る・旅をする…遊んだ道の Lv が上がり、技点で技を覚えます。毎日3つの「今日の務め」もあります。</p></div></li>
      <li><time>いつでも</time><div><h3>Discord とつなぐ</h3><p>ゲームで <span class="kbd">/link</span> と打つと6けたの数字が出ます。Discord の「はじめての方へ」→「Discord と連携」に入れるとつながり、はじめての人はお礼に灯籠を5基もらえます。手紙や夜祭の知らせも、Discord で受け取れるようになります。</p></div></li>
      <li><time>慣れたら</time><div><h3>人の灯りと、つなぐ</h3><p>だれの灯籠とでも灯路はつながります。5基つながると「二ノ灯」になり、守られる範囲が広がって、灯標どうしを行き来できるようになります。</p></div></li>
    </ol>
    <p class="note cold"><b>来たばかりの人は守られています。</b>はじめて入ってから24時間は、あなたのまわりに灯喰いは来ません。灯籠が3基より少ない拠点も狙われません。</p>
    <p style="margin-top:24px"><a href="playstyle.html" class="gbtn">だれと遊ぶかで選ぶ：みんなで・身内で・ひとりで</a></p>
  </div>
</section>

<section class="stratum s-deep" id="cmd">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">早見表</p>
    <h2 class="disp h2">おぼえるコマンドは、ひとつ。</h2>
    <p class="lead"><span class="kbd">/tomoshibi</span> でメニューが開き、あとは押すだけです。下の表は、直接打ちたい人むけです。</p>
    <div class="tbl-wrap"><table class="cmd">
      <thead><tr><th>打つもの</th><th>できること</th></tr></thead>
      <tbody>
        <tr><td class="n">/tomoshibi</td><td>メニューを開く（<span class="kbd">/tomo</span> でも同じ）</td></tr>
        <tr><td class="n">/tomoshibi buffs</td><td>加護を見る、欠片で解放する</td></tr>
        <tr><td class="n">/tomoshibi recipe</td><td>灯籠の作り方</td></tr>
        <tr><td class="n">/tomoshibi go 名前</td><td>名前のついた灯籠（灯標）へ移動する</td></tr>
        <tr><td class="n">/tomoshibi home</td><td>「帰る場所」に決めた灯標へ戻る</td></tr>
        <tr><td class="n">/tomoshibi invite</td><td>自分の招待コードを見る</td></tr>
        <tr><td class="n">/tomoshibi particles low</td><td>光の粒を減らす（動きが重いとき）</td></tr>
        <tr><td class="n">/akashi</td><td>灯の証（進捗）を開く。報酬の受け取り、称号・足跡の選択も</td></tr>
        <tr><td class="n">/akashi claim</td><td>証の報酬をまとめて受け取る</td></tr>
        <tr><td class="n">/akashi top</td><td>証の番付</td></tr>
        <tr><td class="n">/waza</td><td>灯技（技の木・使う技・今日の務め・灯魚図鑑）を開く</td></tr>
        <tr><td class="n">/waza use</td><td>使う技の一覧（しゃがみ2回で主技、しゃがんで F で副技）</td></tr>
        <tr><td class="n">/waza tasks</td><td>今日の務め</td></tr>
        <tr><td class="n">/waza fish</td><td>灯魚図鑑</td></tr>
        <tr><td class="n">/tokoyo</td><td>いまが昼か夜か、夜明けまでの時間、敵の強さ</td></tr>
        <tr><td class="n">/yomatsuri</td><td>次の夜祭と、自分の参加回数</td></tr>
        <tr><td class="n">/yomatsuri out</td><td>募集中の夜祭に、今回は参加しない</td></tr>
      </tbody>
    </table></div>
    <p style="margin-top:24px"><a href="commands.html" class="gbtn">すべてのコマンドを見る（{sum(len(g[5]) for g in _CMDS)}）</a></p>
  </div>
</section>

<section class="stratum s-rock" id="faq">
  <div class="edge"></div>
  <div class="wrap narrow">
    <p class="depth">よくある質問</p>
    <h2 class="disp h2">入る前に、気になること。</h2>
    <div class="faq">
      <details><summary>お金はかかりますか</summary><p>かかりません。参加は無料で、強さを買う仕組みもありません。灯りの色や名前の横の印は、遊んで手に入れる見た目だけのものです。</p></details>
      <details><summary>Java版と統合版で、いっしょに遊べますか</summary><p>遊べます。PCの人も、スマホやSwitchの人も、同じ世界に入ります。</p></details>
      <details><summary>ひとりでも遊べますか</summary><p>遊べます。ただ、この世界は灯りをつなぐほど楽になるように作ってあります。だれかの灯路のそばに灯籠を置くだけで、もう「いっしょに遊んでいる」ことになります。ひとりで遊ぶコツは<a href="playstyle.html#solo">遊び方を選ぶ</a>にまとめています。</p></details>
      <details><summary>いない間に、こわされませんか</summary><p>ほかの人の灯籠は壊せません。灯喰いが狙うのは、近くに人がいる灯籠だけなので、留守の間に灯りが消されることもありません。建物をこわされたときは、きまりのページの手順で知らせてください。</p></details>
      <details><summary>ランタンを置いたのに、灯りになりません</summary><p>灯路網につながるのは、光る「灯籠」だけです。ふつうのランタンは飾りになります。灯籠は作業台で、真ん中にランタン、上下にアメジストの欠片、左右に金インゴットを置くと作れます（<span class="kbd">/tomoshibi recipe</span>）。灯籠を壊すと、灯籠のまま戻ります。</p></details>
      <details><summary>夜の敵が強すぎます</summary><p>そのとおりで、最初は勝てないように作ってあります。灯りの中にいれば襲われません。敵は灯りに入れず、外から狙うこともできません。敵や灯喰いが落とす「欠片」を集めて加護を解放していくと、少しずつ戦えるようになります。</p></details>
      <details><summary>動きが重いです</summary><p><span class="kbd">/tomoshibi particles low</span> で光の粒が半分になり、<span class="kbd">off</span> で消えます。統合版の人は、最初から少なめになっています。</p></details>
      <details><summary>動画や配信にしてもいいですか</summary><p>かまいません。許可はいりません。ほかの人の名前が映るので、いやがる人がいたら映さないようにしてください。</p></details>
      <details><summary>Discord と連携すると、何ができますか</summary><p>ゲームで <span class="kbd">/link</span> と打って出た数字を、Discord の「はじめての方へ」に入れるとつながります。はじめての人には灯籠5基。処罰の知らせや異議を本人として受け取れ、手紙・夜祭・ログインの知らせも順に Discord へ届くようになります。外すときは <span class="kbd">/link off</span>。</p></details>
      <details><summary>困ったときは、どこに聞けばいいですか</summary><p>Discord で聞いてください。入り方、遊び方、こわされた・いやなことをされた、どれでも受けつけています。</p></details>
    </div>
  </div>
</section>
'''

# ───────────────────────── 遊び方 ─────────────────────────
_guide_src = f'''
<section class="stratum tex s-soil" id="lantern">
  <div class="wrap">
    <p class="depth">1</p>
    <h2 class="disp h2">灯籠を置くと、そこが安全になる。</h2>
    <p class="lead">光る「灯籠」を置くと、灯路網に登録されます。ふつうのランタンは飾りで、灯りにはなりません。</p>
    <div class="pn" style="margin-top:28px">
      <p class="mu" style="font-size:14px;font-weight:700">灯籠の作り方（作業台）</p>
      <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;max-width:380px;margin:12px 0 14px">
        <span></span><span class="kbd" style="display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:13px;line-height:1.4;padding:8px 4px;min-height:48px">アメジストの欠片</span><span></span>
        <span class="kbd" style="display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:13px;line-height:1.4;padding:8px 4px;min-height:48px">金インゴット</span><span class="kbd" style="display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:13px;line-height:1.4;padding:8px 4px;min-height:48px;color:var(--amber)">ランタン</span><span class="kbd" style="display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:13px;line-height:1.4;padding:8px 4px;min-height:48px">金インゴット</span>
        <span></span><span class="kbd" style="display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:13px;line-height:1.4;padding:8px 4px;min-height:48px">アメジストの欠片</span><span></span>
      </div>
      <p class="mu" style="font-size:16px">はじめて入ったときに3基もらえます。「はじめの一歩」や毎日の灯守り、灯の証の報酬でも手に入ります。壊すと灯籠のまま戻るので、置き直してもむだになりません。</p>
    </div>
    <div class="two">
      <div><h3 class="h3 disp">灯りの中で起きること</h3><p class="mu">敵は入ってこられない。入りこんだ敵は外へ押し返され、居座ると灯りに焼かれる。灯りの中の人は狙われないので、外からの矢や爆発も来ない。敵が湧かない。爆発でブロックが壊れない。倒れても持ち物と経験値を失わない。画面の下に、いま灯りの中か外かが出ます。</p></div>
      <div><h3 class="h3 disp">灯路</h3><p class="mu">16ブロック以内の灯籠どうしは、自動で灯路につながります（1基につき4本まで）。灯路の上は足が速くなります。だれの灯籠とでもつながります。</p></div>
    </div>
    <h3 class="h3 disp" style="margin-top:56px">つながるほど、格が上がる。</h3>
    <p class="lead">灯路でつながった灯籠のまとまりを「灯路網」と呼びます。基数がふえると格が上がり、守られる範囲が広がって、まわりが本当に明るくなります。</p>
    <div class="tbl-wrap"><table>
      <thead><tr><th>格</th><th>つながった基数</th><th>守られる半径</th><th>できること</th></tr></thead>
      <tbody>
        <tr><th>一ノ灯</th><td class="n">1〜4基</td><td class="n">10</td><td>基本の守り。加護は Lv1 まで働く</td></tr>
        <tr><th>二ノ灯</th><td class="n">5〜14基</td><td class="n">12</td><td>灯標どうしを行き来できる。加護は Lv2 まで</td></tr>
        <tr><th>三ノ灯</th><td class="n">15〜39基</td><td class="n">14</td><td>灯路の上がさらに速くなる。加護は Lv3 まで</td></tr>
        <tr><th>四ノ灯</th><td class="n">40基〜</td><td class="n">16</td><td>いちばん広く守られる</td></tr>
      </tbody>
    </table></div>
    <h3 class="h3 disp" style="margin-top:56px">置くときのきまり</h3>
    <div class="tbl-wrap"><table>
      <thead><tr><th>置き方</th><th>かかるもの・もらえるもの</th></tr></thead>
      <tbody>
        <tr><th>最初の1基</th><td>無料</td></tr>
        <tr><th>いまある灯籠から16ブロック以内</th><td>無料。灯路1本につき経験値がもらえる（3本まで）</td></tr>
        <tr><th>どの灯籠ともつながらない場所</th><td>経験値レベル 2 がかかる</td></tr>
        <tr><th>同じチャンクに3基目</th><td>置けない（1チャンク2基まで）。灯籠は手もとに残る</td></tr>
        <tr><th>ふつうのランタン</th><td>飾りとして置かれる。灯路網にはつながらない</td></tr>
      </tbody>
    </table></div>
    <p class="note">ぎゅうぎゅうに置くより、少しはなして外へのばすほうが得になるようにしてあります。</p>
    <p class="note warn"><b>灯りの守りが効かないもの。</b>灯喰いと、ウィザー・エンダードラゴン・ウォーデン・エルダーガーディアン。灯喰いに喰われた灯籠のまわりも、守りが消えます。</p>
  </div>
</section>

<section class="stratum s-dusk" id="night">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">2</p>
    <h2 class="disp h2">昼は4分、夜は24分。</h2>
    <p class="lead">灯原では、ほとんどの時間が夜です。ベッドで寝ても夜は飛ばせません（リスポーン地点は決められます）。日没と夜明けには、画面の真ん中に知らせが出ます。</p>
    <h3 class="h3 disp" style="margin-top:44px">夜に湧く敵</h3>
    <div class="tbl-wrap"><table>
      <thead><tr><th>ふつうのマインクラフトとくらべて</th><th>倍率</th></tr></thead>
      <tbody>
        <tr><th>体力</th><td class="n">×2.5</td></tr>
        <tr><th>攻撃</th><td class="n">×2.0</td></tr>
        <tr><th>矢・爆発</th><td class="n">×1.8</td></tr>
        <tr><th>足の速さ</th><td class="n">×1.15</td></tr>
        <tr><th>気づく距離</th><td class="n">×1.5</td></tr>
      </tbody>
    </table></div>
    <div class="two">
      <div><h3 class="h3 disp">さらに強くなるとき</h3><p class="mu">夜を1つ重ねるごとに+4%（最大で2倍）。真夜中は+25%。そして、あなたの防具が固いほど敵も強くなります。育っても、夜は楽になりません。</p></div>
      <div><h3 class="h3 disp">精鋭と群れ</h3><p class="mu">10体に1体は、名前のついた「精鋭」です。体力も攻撃もさらに高いかわりに、経験値は4倍、欠片も6割の確率で落とします。3回に1回は、もう1体いっしょに湧きます。</p></div>
    </div>
    <p class="note warn"><b>朱月（しゅげつ）の夜。</b>7夜に一度、月が赤くなります。敵は1.4倍強く、群れと精鋭がふえます。ひとりで外にいる夜ではありません。</p>
    <p class="note">昼に湧いた敵と、スポナーから出た敵は、ふつうの強さのままです。いまの時刻と敵の強さは <span class="kbd">/tokoyo</span> で見られます。</p>
  </div>
</section>

<section class="stratum s-blood" id="higui">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">3</p>
    <h2 class="disp h2">灯喰いは、灯りを消しに来る。</h2>
    <p class="lead">黒い体に白い面。灯りの守りを破れる、ただひとつの敵です。人には目もくれず、灯籠へまっすぐ向かってきます。道をふさいでも、闇を渡って灯籠のそばに現れます。</p>
    <ol class="steps" style="margin-top:36px">
      <li><div><h3>狙われる</h3><p>夜、人の近く（48ブロック以内）にある灯籠のうち、灯路がいちばん少ない「端」の1基が狙われます。</p></div></li>
      <li><div><h3>知らせが出る</h3><p>灯喰いがいるあいだ、画面の下に「灯喰いが灯を狙っている｜北東 32m・灯まであと 12m」と出つづけます。灯喰いの体は光っていて、暗がりでも見えます。</p></div></li>
      <li><div><h3>喰いはじめる</h3><p>灯籠に取りつくと、灯籠から光を吸いはじめます。画面の下に、どこまで喰われたかが ■■■■□□ のように出ます。喰い終わるまでの時間は、下の式のとおりです。</p></div></li>
      <li><div><h3>守る</h3><p>たたくと喰うのが2秒ぶん戻り、たたいた人にだけ、しばらくやり返してきます。倒せば守りきりです。3回に1回ほど、欠片を落とします。</p></div></li>
      <li><div><h3>喰われたら</h3><p>灯籠は青い冷たい火になり、守りも灯路も止まります。途中の1基が消えると、灯路網が2つに分かれて格が下がることもあります。</p></div></li>
      <li><div><h3>灯し直す</h3><p>青い灯籠を、何も持たずに右クリックすると、だれでも灯し直せます。ほかの人の灯籠を灯し直すと、経験値がもらえます。</p></div></li>
    </ol>
    <div class="pn" style="margin-top:32px">
      <p class="mu" style="font-size:14px;font-weight:700">喰い終わるまでの時間</p>
      <p class="dot" style="font-size:clamp(19px,2.6vw,28px);line-height:1.6;color:#FFE3A3;margin-top:6px">5秒 ＋ 灯路1本ごとに5秒 ＋ 灯りの中の人ひとりごとに3秒</p>
      <p class="mu" style="margin-top:10px;font-size:16px">ぽつんと1基だけの灯籠は5秒。灯路が3本つながり、そばに2人いれば26秒。つなぐほど、集まるほど、守れます。</p>
    </div>
    <div class="two">
      <div><h3 class="h3 disp">夜明けに起きること</h3><p class="mu">まだ灯っている灯籠とつながっている灯籠には、火が移って自然に戻ります。つながりのない灯籠は、だれかが行くまで消えたままです。ひとつも消させなかった夜は「無欠の夜」として、経験値がもらえます。</p></div>
      <div><h3 class="h3 disp">狙われないもの</h3><p class="mu">3基より少ない灯路網。名前をつけた灯標。最初の広場のまわり。来てから24時間以内の人のまわり。地下や高い塔の灯籠。そして、近くにだれもいない灯籠。</p></div>
    </div>
  </div>
</section>

<section class="stratum s-deep" id="buff">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">4</p>
    <h2 class="disp h2">倒して、集めて、強くなる。</h2>
    <p class="lead">敵はときどき「欠片」を落とします。右クリックで取り込み（しゃがむと全部）、<span class="kbd">/tomoshibi buffs</span> で加護を解放します。加護は、灯りの中にいるあいだだけ働きます。</p>
    <div class="two">
      <div>
        <h3 class="h3 disp">欠片が落ちる確率</h3>
        <div class="tbl-wrap" style="margin-top:8px"><table style="min-width:0">
          <tbody>
            <tr><th>ふつうの敵</th><td class="n">5%</td></tr>
            <tr><th>夜に強くなった敵</th><td class="n">12%</td></tr>
            <tr><th>灯喰い</th><td class="n">35%</td></tr>
            <tr><th>精鋭</th><td class="n">60%</td></tr>
          </tbody>
        </table></div>
      </div>
      <div>
        <h3 class="h3 disp">解放に要る欠片</h3>
        <div class="tbl-wrap" style="margin-top:8px"><table style="min-width:0">
          <tbody>
            <tr><th>Lv1</th><td class="n">4個</td></tr>
            <tr><th>Lv2</th><td class="n">さらに10個</td></tr>
            <tr><th>Lv3</th><td class="n">さらに20個</td></tr>
          </tbody>
        </table></div>
        <p class="mu" style="font-size:15px;margin-top:10px">欠片は加護の種類ごとに別です。再生の欠片は、再生の加護にだけ使えます。</p>
      </div>
    </div>
    <h3 class="h3 disp" style="margin-top:56px">8つの加護</h3>
    <div class="tbl-wrap"><table>
      <thead><tr><th>加護</th><th>働く場所</th><th>Lv1</th><th>Lv2</th><th>Lv3</th></tr></thead>
      <tbody>
        <tr><th><span class="sw" style="background:#F29BB8"></span>再生</th><td>灯りの中</td><td colspan="3">体力が少しずつ戻る。Lv が上がるほど速い</td></tr>
        <tr><th><span class="sw" style="background:#F2D544"></span>採掘速度</th><td>灯りの中</td><td colspan="3">掘るのが速くなる</td></tr>
        <tr><th><span class="sw" style="background:#C9D0DC"></span>耐性</th><td>灯りの中</td><td colspan="3">受けるダメージが減る</td></tr>
        <tr><th><span class="sw" style="background:#E0453A"></span>攻撃力</th><td>灯りの中</td><td colspan="3">攻撃が強くなる</td></tr>
        <tr><th><span class="sw" style="background:#8BD18F"></span>幸運</th><td>灯りの中</td><td colspan="3">戦利品や釣りの運が上がる</td></tr>
        <tr><th><span class="sw" style="background:#8FC3E8"></span>跳躍</th><td>灯路の上</td><td colspan="3">高く跳べる</td></tr>
        <tr><th><span class="sw" style="background:#F2B544"></span>満腹</th><td>灯りの中</td><td class="n">空腹 −50%</td><td class="n">−75%</td><td>腹が減らない</td></tr>
        <tr><th><span class="sw" style="background:#6FD39A"></span>経験</th><td>灯りの中</td><td class="n">経験値 +15%</td><td class="n">+30%</td><td class="n">+50%</td></tr>
      </tbody>
    </table></div>
    <p class="note"><b>格とのかけ算。</b>働くのは「いまいる灯路網の格まで」の Lv です。Lv3 を解放していても、一ノ灯の灯りの中では Lv1 しか働きません。自分が強くなることと、みんなで灯路網を育てることの、両方が要ります。</p>
  </div>
</section>

<section class="stratum s-dusk" id="akashi">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">5</p>
    <h2 class="disp h2">灯の証。263の、灯原だけの進捗。</h2>
    <p class="lead"><span class="kbd">/akashi</span> で開きます。灯籠、夜、狩り、旅、ものづくり、暮らし、夜祭、灯技。この世界で過ごしたことが、そのまま証になります。すべて集めるには、季節をまたぐほどの時間がかかります。</p>
    <div class="tbl-wrap"><table>
      <thead><tr><th>難度</th><th>数</th><th>目安</th><th>例</th></tr></thead>
      <tbody>
        <tr><th style="color:#55FF55">◆ 易</th><td class="n">43</td><td>その日のうちに</td><td>灯籠をひとつ灯す、最初の夜を越える</td></tr>
        <tr><th style="color:#55FFFF">◆◆ 並</th><td class="n">77</td><td>何日か続ければ</td><td>15基の灯路網に加わる、朱月の夜を越える</td></tr>
        <tr><th style="color:#FF55FF">◆◆◆ 難</th><td class="n">81</td><td>腰を据えて</td><td>100回の夜を越える、ウィザーを倒す</td></tr>
        <tr><th style="color:#FFAA00">◆◆◆◆ 極</th><td class="n">43</td><td>何週間も</td><td>灯籠を300基持つ、ウォーデンを倒す</td></tr>
        <tr><th style="color:#FF5555">◆◆◆◆◆ 伝</th><td class="n">19</td><td>季節をまたいで</td><td>500回の夜を越える、8つの加護をすべて Lv3 にする</td></tr>
      </tbody>
    </table></div>
    <div class="three">
      <div><h3 class="h3 disp">段になっている</h3><p class="mu">同じ種類の証は段になっていて、前の段を得ると次が現れます。ひとつ選んで「追跡」すると、画面の上のバーで進み具合を見られます。</p></div>
      <div><h3 class="h3 disp">秘められた証</h3><p class="mu">条件が隠されていて、ヒントだけが読める証が12個あります。だれかが見つけると、その証の札に「初達成」の名前が残ります。</p></div>
      <div><h3 class="h3 disp">報酬は、強さの差がつかない量</h3><p class="mu">経験値、加護の欠片、名前の前に出る称号（69種）、歩くと光が残る足跡（12種）、証でしか手に入らない灯りの色（5色）。</p></div>
    </div>
    <h3 class="h3 disp" style="margin-top:56px">証点と位階</h3>
    <p class="lead">証を得るたびに、難度に応じて証点がたまります（易10・並25・難50・極100・伝250）。証点で位階が上がり、称号や足跡がもらえます。</p>
    <p class="dot" style="font-size:clamp(16px,2.2vw,22px);line-height:2;color:#FFE3A3;margin-top:10px">灯見習い → 灯守 → 灯師 → 灯匠 → 灯司 → 夜番 → 夜渡り → 宵の主 → 暁の灯 → 灯原の伝説</p>
    <p class="note">放置している時間（5分間、視点が動かない）と、クリエイティブでの行動は数えません。「夜を越える」は、夜のはじめから夜明けまで、地上の世界で倒れずに過ごすことです。</p>
  </div>
</section>


<section class="stratum s-stone" id="more">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">7</p>
    <h2 class="disp h2">灯標、灯りの色、招待。</h2>
    <div class="two">
      <div><h3 class="h3 disp">灯標と灯渡り</h3><p class="mu">灯籠に名前をつけると「灯標（とうひょう）」になります。二ノ灯より上の灯路網では、同じ灯路網の灯標へ、3秒じっとしているだけで移動できます（つぎに使えるまで30秒）。灯標は灯喰いに喰われません。ひとつを「帰る場所」に決めておけます。</p></div>
      <div><h3 class="h3 disp">仲間</h3><p class="mu">メニューの「仲間」に加えた人は、あなたの灯籠に名前をつけたり、取り除いたりできます。ほかの人は、あなたの灯籠を壊せません。</p></div>
    </div>
    <h3 class="h3 disp" style="margin-top:56px">灯りの色は、17色。</h3>
    <p class="lead">灯籠の光と灯路の色を変えられます。強さは変わりません。手に入れ方は、遊ぶことだけです。</p>
    <div class="tbl-wrap"><table>
      <thead><tr><th>色</th><th>手に入れ方</th></tr></thead>
      <tbody>
        <tr><th><span class="sw" style="background:#F2B544"></span>山吹</th><td>最初から</td></tr>
        <tr><th><span class="sw" style="background:#F29BB8"></span>桜</th><td>夜祭に5回参加する</td></tr>
        <tr><th><span class="sw" style="background:#8FC3E8"></span>水縹（みはなだ）</th><td>夜祭に10回参加する</td></tr>
        <tr><th><span class="sw" style="background:#8BD18F"></span>若竹</th><td>夜祭に20回参加する</td></tr>
        <tr><th><span class="sw" style="background:#C9D0DC"></span>白銀</th><td>友達を1人招待する</td></tr>
        <tr><th><span class="sw" style="background:#B79CF2"></span>藤</th><td>友達を3人招待する</td></tr>
        <tr><th><span class="sw" style="background:#F2A07A"></span>曙</th><td>友達を5人招待する</td></tr>
        <tr><th><span class="sw" style="background:#FFF1C4"></span>はじまりの灯</th><td>シーズン1の開幕の夜（11月7日）に参加する</td></tr>
        <tr><th><span class="sw" style="background:#FF7624"></span>篝火</th><td>証「夜を貫く灯路」（300基の灯路網に加わる）</td></tr>
        <tr><th><span class="sw" style="background:#40D6A0"></span>翡翠</th><td>証「八徳の灯」（8つの加護をすべて Lv3）</td></tr>
        <tr><th><span class="sw" style="background:#D62448"></span>紅</th><td>証「一年の灯守」（灯守りを365日続ける）</td></tr>
        <tr><th><span class="sw" style="background:#FF6ED2"></span>花火</th><td>証「祭神」（夜祭で50回勝つ）</td></tr>
        <tr><th><span class="sw" style="background:#BAAAFF"></span>天の川</th><td>位階「灯原の伝説」に届く</td></tr>
      </tbody>
    </table></div>
    <p class="mu" style="font-size:15px;margin-top:12px">ほかの色は、メニューの「灯りの色」に手に入れ方が書いてあります。</p>
    <h3 class="h3 disp" style="margin-top:56px">友達を呼ぶ</h3>
    <ol class="steps" style="margin-top:16px">
      <li><div><h3><span class="kbd">/tomoshibi invite</span> で、自分の招待コードを見る</h3><p>メニューの「招待」からも見られます。</p></div></li>
      <li><div><h3>友達に、サーバーのアドレスとコードを伝える</h3><p>アドレスは <span class="kbd">{ADDR}</span> です。</p></div></li>
      <li><div><h3>友達が、入ってから7日以内に <span class="kbd">/tomoshibi code コード</span> と打つ</h3><p>呼んだ人の招待が1人ふえます。10人呼ぶと、番付の「灯友の碑」に名前が載ります。</p></div></li>
    </ol>
  </div>
</section>
'''

import re as _re

# ───────────────────────── 遊び方：章立て ─────────────────────────
# 遊び方は「目次（guide.html）」と、章ごとのページ（guide-○○.html）に分ける。

# 章のドット絵（16×16。# は線、o は章の色でともる部分）
CH_ICONS = {
    "lantern": ICONS["index.html"],
    "night": ["................", "..........o.....", ".........ooo....", "....###...o.....", "...#ooo#........", "..#oo##.........", "..#o#...........", ".#oo#...........", ".#oo#.......o...", ".#oo#...........", "..#o#...........", "..#oo##.........", "...#ooo##.......", "....#####.......", "................", "................"],
    "higui": ["................", "....########....", "...#oooooooo#...", "...#o##oo##o#...", "...#o##oo##o#...", "...#oooooooo#...", "...#ooo##ooo#...", "....#oooooo#....", ".....######.....", "....########....", "...##########...", "...##########...", "...##.####.##...", "...##.####.##...", "...##......##...", "................"],
    "buff": ["................", ".......##.......", "......#oo#......", ".....#oooo#.....", "....#oooooo#....", "...#oooooooo#...", "..#oooooooooo#..", "..############..", "...#oooooooo#...", "....#oooooo#....", ".....#oooo#.....", "......#oo#......", ".......##.......", "................", "................", "................"],
    "hiwaza": ["................", "..####....####..", "..#oo#....#oo#..", "..#oo#....#oo#..", "..####....####..", "....#......#....", "....#......#....", "....########....", ".......#........", ".......#........", "......####......", "......#oo#......", "......#oo#......", "......####......", "................", "................"],
    "fish": ["................", "................", "................", "......#####.....", "....##ooooo##...", "...#ooooooooo#.#", "..#o#oooooooo###", "..#ooooooooooo##", "..#ooooooooooo##", "...#ooooooooo#.#", "....##ooooo##...", "......#####.....", "................", "................", "................", "................"],
    "akashi": ["................", "...##......##...", "....##....##....", ".....##..##.....", "......####......", ".....######.....", "....#oooooo#....", "...#oooooooo#...", "...#ooo##ooo#...", "...#oo####oo#...", "...#ooo##ooo#...", "...#oooooooo#...", "....#oooooo#....", ".....######.....", "................", "................"],
    "himon": ["................", ".......##.......", "......#oo#......", ".....#o##o#.....", "....#o#..#o#....", "...#o#.##.#o#...", "..#o#.#oo#.#o#..", ".#o#.#o##o#.#o#.", ".#o#.#o##o#.#o#.", "..#o#.#oo#.#o#..", "...#o#.##.#o#...", "....#o#..#o#....", ".....#o##o#.....", "......#oo#......", ".......##.......", "................"],
    "more": ["................", ".......##.......", "..##########....", "..#oooooooo##...", "..#oooooooo###..", "..#oooooooo##...", "..##########....", ".......##.......", "....##########..", "...##oooooooo#..", "..###oooooooo#..", "...##oooooooo#..", "....##########..", ".......##.......", ".......##.......", "......####......"],
    "sato": ["................", ".......##.......", ".....##oo##.....", "...##oooooo##...", ".##oooooooooo##.", "################", "..#oo#....#oo#..", "..#oo#.##.#oo#..", "..####.##.####..", "..#....##....#..", "..#..######..#..", "..#..#oooo#..#..", "..#..#oooo#..#..", "################", "................", "................"],
    "shoku": ["................", "..##########....", ".#oooooooooo#...", ".#oooooooooo#...", "..####oo####....", ".....#oo#.......", ".....#oo#....##.", ".....#oo#...#oo#", ".....#oo#..#oo#.", ".....#oo#.#oo#..", ".....#oo##oo#...", ".....#oo#oo#....", "....#oooooo#....", "....########....", "................", "................"],
    "musubi": ["................", "...###....###...", "..#ooo#..#ooo#..", "..#ooo#..#ooo#..", "...###....###...", "................", "..#####..#####..", ".#ooooo##ooooo#.", ".#oooooooooooo#.", ".#oo#oooooo#oo#.", ".#oo#oooooo#oo#.", "..##.######.##..", "....#oo##oo#....", "....#oo##oo#....", "....###..###....", "................"],
}


def pix(rows, cls="ch-ic"):
    r = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            ch = row[x]
            if ch == ".":
                x += 1
                continue
            w = 1
            while x + w < len(row) and row[x + w] == ch:
                w += 1
            r.append(f'<rect x="{x}" y="{y}" width="{w}" height="1" class="{"l" if ch == "o" else "s"}"/>')
            x += w
    return f'<svg class="{cls}" viewBox="0 0 16 16" aria-hidden="true">' + "".join(r) + "</svg>"


# 章の一覧（読む順）。layer は目次での区切り。
CH = [
    {"id": "lantern", "t": "灯籠と灯路", "c": "#F2B544", "layer": 0, "sec": ["lantern"],
     "sum": "置いた場所だけが安全になる。つなぐほど、格が上がる。", "facts": ["守り 半径10〜16", "16ブロックでつながる", "格は4段"],
     "desc": "灯籠を置くとそこが安全になる。灯路でつなぎ、灯路網の格を上げる。作り方と置くときのきまり。"},
    {"id": "night", "t": "長い夜", "c": "#9C8CFF", "layer": 0, "sec": ["night"],
     "sum": "昼は4分、夜は24分。夜を重ねるほど、敵は強くなる。", "facts": ["夜 24分", "敵の体力 ×2.5", "7夜に一度の朱月"],
     "desc": "昼4分・夜24分の灯原の夜。夜に湧く敵の強さ、精鋭と群れ、朱月の夜。"},
    {"id": "higui", "t": "灯喰い", "c": "#E0453A", "layer": 0, "sec": ["higui"],
     "sum": "灯りの守りを破る、ただひとつの敵。人ではなく灯籠を狙う。", "facts": ["灯籠だけを狙う", "喰い終わるまで 5秒〜", "夜明けに火が戻る"],
     "desc": "灯籠を喰いに来る灯喰い。狙われる灯籠、喰い終わるまでの時間、守り方と灯し直し方。"},
    {"id": "buff", "t": "加護と欠片", "c": "#6FD39A", "layer": 1, "sec": ["buff"],
     "sum": "敵が落とす欠片で、灯りの中だけで働く加護を解放する。", "facts": ["8つの加護", "Lv3 まで", "格とのかけ算"],
     "desc": "欠片が落ちる確率、解放に要る数、8つの加護。灯路網の格とのかけ算。"},
    {"id": "hiwaza", "t": "灯技", "c": "#5AAAFF", "layer": 1, "sec": [],
     "sum": "遊ぶほど育つ10の道。技点で130の技を覚える。", "facts": ["10の道", "130の技", "奥義まで約1か月"],
     "desc": "灯技（ひわざ）。10の道・130の技、技の木の見方、灯力、主技と副技、今日の務めと極み。"},
    {"id": "himon", "t": "灯紋", "c": "#E9C46A", "layer": 1, "sec": [],
     "sum": "遊んだ時間でたまる灯札で紋書を引き、道具に刻む。ふつうの付呪にはない力。", "facts": ["92の紋", "灯札は遊んだ時間で", "秘は無銘の紋書だけ"],
     "desc": "灯紋（ひもん）。経験値と灯札で紋書を引く4つの段と無銘の紋書、道具への刻み方・重ね方・外し方、暮らし・戦い・移動・守りのおすすめの紋。"},
    {"id": "fish", "t": "灯魚", "c": "#4FD8C8", "layer": 2, "sec": [],
     "sum": "時と場所と月でかわる、106種の魚。珍しいほど逃げる。", "facts": ["106種", "5つの珍しさ", "ヌシ"],
     "desc": "灯魚（ひうお）106種。珍しさ、かかる条件（水辺・時刻・天気・月・季節・朱月・灯り）、図鑑と灯原一。"},
    {"id": "akashi", "t": "灯の証", "c": "#F29BB8", "layer": 2, "sec": ["akashi"],
     "sum": "この世界で過ごしたことが、そのまま証になる。", "facts": ["263の証", "位階10段", "称号69種"],
     "desc": "灯原だけの進捗「灯の証」263個。難度、段と秘められた証、報酬、証点と位階。"},
    {"id": "more", "t": "灯標・色・招待", "c": "#C9D0DC", "layer": 2, "sec": ["more"],
     "sum": "名前をつけて行き来し、灯りの色を変え、友を呼ぶ。", "facts": ["灯渡り 3秒", "灯りの色 17色", "招待コード"],
     "desc": "灯標と灯渡り、仲間、17の灯りの色の手に入れ方、友達の招待のしかた。"},
    {"id": "sato", "t": "灯里", "c": "#E9824A", "layer": 3, "sec": [],
     "sum": "3人で開き、灯りで土地を広げ、集落から都へ。仲間と育てる、小さな国。", "facts": ["4つの格", "土地は灯路網", "屋敷は持ち主だけ"],
     "desc": "灯里（ひさと）の里。開く条件と礎、仮の里の7日、里灯と土地、屋敷と掟、蔵、4つの格と毎週の灯油。"},
    {"id": "shoku", "t": "職と依頼", "c": "#EE9A4A", "layer": 3, "sec": [],
     "sum": "5つの職から1つ。里に足りないものが依頼で届き、働くほど位が上がる。", "facts": ["5つの職", "見習い→匠", "鑑定は見た目だけ"],
     "desc": "大工・灯守・衛士・商人・旅人の5つの職とバフ、見習いから匠までの位、日課・週課・大事業、建築の依頼と鑑定、転職の試し。"},
    {"id": "musubi", "t": "灯結と暮らし", "c": "#F29BB8", "layer": 3, "sec": [],
     "sum": "縁・一団・合流・手紙・合図。名所めぐりと市の日で、里の外ともつながる。", "facts": ["一団 12人", "名所めぐり", "すべて画面で"],
     "desc": "灯結（ひむすび）の縁・一団・合流・手紙と小包・合図・配信中・離れる。名所めぐり、旅の依頼、屋台と市、里の便り、感謝の灯、画面のきまり。"},
]
LAYERS = [("第一層", "はじめに知ること", "ここまで読めば、最初の夜を越えられます。"),
          ("第二層", "強くなる", "慣れてきたら。育てるほど、暮らしが楽になります。"),
          ("第三層", "残す・つなぐ", "長く遊ぶほど、残るものがふえます。"),
          ("第四層", "里で暮らす", "仲間ができたら。里を開き、職について、街を育てます。")]

_SEC = {m.group(1): m.group(0) for m in _re.finditer(r'<section class="stratum[^"]*" id="(\w+)">.*?\n</section>', _guide_src, _re.S)}


def _clean(sec):
    sec = _re.sub(r'\n\s*<p class="depth">\d+</p>', "", sec)
    if '<div class="edge">' not in sec[:200]:
        sec = sec.replace(">\n  <div class=\"wrap\">", ">\n  <div class=\"edge\"></div>\n  <div class=\"wrap\">", 1)
    return sec


# ── 灯技の章 ──
_PATHS = [
    ("灯", "灯の道", "#FFAA00", "灯籠を置く・守る・灯し直す、灯喰いを倒す", ["手灯り", "仮灯（闇に一時の結界）", "灯路の足", "見回り"], "灯の化身"),
    ("夜", "夜の道", "#B46CFF", "夜を越える、闇で過ごす", ["夜目", "梟の耳（背後の敵）", "影渡り", "帰り火（家へ帰る）"], "静夜"),
    ("掘", "掘の道", "#55FFFF", "石・鉱石を掘る", ["灯脈掘り（まとめ掘り）", "鉱石の灯視", "灯の熱（その場で精錬）", "3×3 掘り"], "地脈の声"),
    ("樵", "樵の道", "#55FF55", "木を切る", ["一本切り", "巨木切り", "苗木植え", "まとめ剥ぎ"], "森の主"),
    ("耕", "耕の道", "#FFFF55", "実った作物を収穫する", ["7×7 の一斉収穫", "種まき 5×5", "自動植え直し", "上物が採れる"], "灯の恵み"),
    ("釣", "釣の道", "#3CC8C8", "魚を釣る", ["早釣り", "魚読み（釣れる灯魚の数）", "撒き餌（みんなに効く）", "魚拓"], "主の竿"),
    ("匠", "匠の道", "#FF55FF", "作る、かまど、灯籠を作る", ["整頓", "近くの箱へまとめ入れ", "携帯作業台", "背負い籠"], "灯の手入れ"),
    ("旅", "旅の道", "#FFFFFF", "遠くへ行く、新しい土地を訪れる", ["健脚", "段差越え", "受け身（落下 −75%）", "灯の翼（滑空の加速）"], "疾風"),
    ("牧", "牧の道", "#FF5555", "殖やす、手なずける、毛を刈る", ["双子", "群れ刈り", "まとめ餌やり", "呼び笛"], "牧の主"),
    ("術", "術の道", "#7C7CFF", "付呪、醸造、経験値を集める", ["経験の灯（+30%）", "魂の残り火", "金床の名人", "灯矢（光の矢）"], "灯の賢者"),
]


def _tree_demo():
    # 技の木の見方：4つの枝 × 3つの段 ＋ 奥義。状態の印を実物どおりに並べる
    st = [["ok", "ok", "go", "no"], ["ok", "go", "lock", "lock"], ["go", "lock", "lock", "lock"]]
    mark = {"ok": "✔", "go": "▶", "no": "・", "lock": "✖"}
    rows = ""
    for t in range(3):
        cells = "".join(f'<span class="tc {st[t][b]}"><i>{mark[st[t][b]]}</i></span>' for b in range(4))
        rows += f'<div class="tr"><span class="tl dot">{["一の段", "二の段", "三の段"][t]}</span>{cells}</div>'
    head = '<div class="tr th"><span class="tl"></span>' + "".join(f'<span class="tb dot">枝{n}</span>' for n in "一二三四") + "</div>"
    return f'''<div class="tree" role="img" aria-label="技の木の見本。4つの枝と3つの段、その下に奥義。">
      {head}{rows}
      <div class="tr cap"><span class="tl dot">奥義</span><span class="tc lock wide"><i>✖</i><em>三の段を2つ覚えると開く</em></span></div>
    </div>'''


def _hiwaza_sec():
    cards = "".join(f'''<div class="path" style="--c:{c}">
        <h3><span class="k">{k}</span><span class="disp">{name}</span></h3>
        <p class="grow">育つこと：{grow}</p>
        <ul>{"".join(f"<li>{x}</li>" for x in ex)}</ul>
        <p class="cap">奥義 <b>{cap}</b></p>
      </div>''' for k, name, c, grow, ex, cap in _PATHS)
    return f'''<section class="stratum s-deep" id="hiwaza">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">遊ぶほど、技が身につく。</h2>
    <p class="lead"><span class="kbd">/waza</span> で開きます。掘る、切る、耕す、釣る、作る、旅をする、動物と暮らす、付呪する、灯籠を守る、夜を越える。遊んだ道の Lv が上がり（最大50）、Lv が1上がるごとに技点が1。技点で技を覚えます。戦うための技は少しだけで、ほとんどは暮らしと夜を越えるための技です。</p>
    <div class="paths">{cards}</div>
    <a href="wiki.html" class="wiki-band"><span class="wb-k dot">WIKI</span><span class="wb-b"><b class="disp">130の技を、ひとつずつ</b><span>効き目・要る Lv・技点・灯力・待ち時間。技の名前で探せます。</span></span><span class="wb-go">灯技 Wiki へ<i></i></span></a>
  </div>
</section>

<section class="stratum s-dusk" id="tree">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">技の木の見方。</h2>
    <p class="lead">どの道も同じ形です。4つの「枝」に3つの「段」、いちばん下に「奥義」。上の段を覚えると、その下の段が開きます。下の段ほど強く、覚えたときの演出も派手になります。</p>
    <div class="demo-tree">
      {_tree_demo()}
      <dl class="marks">
        <div><dt class="ok">✔</dt><dd><b>覚えた</b>技は光っています。段の強さは Ⅰ〜Ⅲ。</dd></div>
        <div><dt class="go">▶</dt><dd><b>いま覚えられる</b>左クリックで覚えます。</dd></div>
        <div><dt class="no">・</dt><dd><b>Lv か技点が足りない</b>道を育てると覚えられます。</dd></div>
        <div><dt class="lock">✖</dt><dd><b>前の技が先</b>灰色で表示されます。</dd></div>
      </dl>
    </div>
    <div class="three">
      <div><h3 class="h3 disp"><span class="tag t1">〔常時〕</span></h3><p class="mu">覚えれば、いつも働く技。速く歩ける、経験値が増える、など。</p></div>
      <div><h3 class="h3 disp"><span class="tag t2">〔切替〕</span></h3><p class="mu">右クリックでオン／オフできる技。まとめ掘りや一本切りなど、いらないときは止められます。</p></div>
      <div><h3 class="h3 disp"><span class="tag t3">〔発動〕</span></h3><p class="mu">自分で使う技。主技・副技に決めて、<b>しゃがみ2回</b>／<b>しゃがんで F</b> で呼び出します。17あります。</p></div>
    </div>
  </div>
</section>

<section class="stratum s-stone" id="gauge">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">灯りで蓄えて、闇へ持ち出す。</h2>
    <div class="facts">
      <div class="fact"><p class="fact-n">灯力</p><p>使う技の力です。灯籠の灯りの中でたまり、灯路網の格が高いほど早くたまります。灯りの外ではほとんどたまりません。画面の上のバーに出ます。</p></div>
      <div class="fact"><p class="fact-n">3<small>つ／日</small></p><p>毎日0時に「今日の務め」が3つ出ます。果たすと経験値と灯力、3つすべて果たすと加護の欠片がもらえます。</p></div>
      <div class="fact"><p class="fact-n">★10</p><p>Lv50 を超えた経験値は「極み」の★になります。道ごとに★10まで。番付にも出ます。</p></div>
      <div class="fact"><p class="fact-n">4,000<small>／日</small></p><p>「今日の伸び」。道ごとに1日 4,000 まではふつうに育ち、その先は1割になります。遊べなかった日の分は3日ぶんまで貯まるので、毎日入れなくても置いていかれません。まとめ掘りや一本切りで技がいっしょに壊した分は、経験値が半分です。</p></div>
      <div class="fact"><p class="fact-n">約1<small>か月</small></p><p>ひとつの奥義までの目安です（毎日遊んで）。奥義には Lv と三の段2つに加えて「奥義の試練」が要ります。たとえば掘の道は鉱石3,000個、釣の道は灯魚60種、旅の道は40種の土地。</p></div>
      <div class="fact"><p class="fact-n">1<small>回目は無料</small></p><p>技は振り直せます。はじめの1回は無料、そのあとは経験値 Lv10 と24時間の待ちがかかります。</p></div>
    </div>
    <p class="note cold"><b>ずるはできないようにしてあります。</b>放置（視点が5分動かない）中は育ちません。自分で置いたブロック、石の製造機、同じ場所を回る・瞬間移動では経験値が入りません。保護された場所では技も働きません。</p>
  </div>
</section>
'''


# ── 灯魚の章 ──
_RAR = [("並", 1, "#E9EEF6", 24, 0, "手がかりがすべて図鑑に出る"),
        ("珍", 2, "#55FF55", 38, 10, "手がかりがすべて出る。1割ほど逃げる"),
        ("稀", 3, "#55FFFF", 28, 25, "手がかりは一部だけ。4回に1回は逃げる"),
        ("秘", 4, "#FF55FF", 10, 40, "手がかりなし。逃げると、姿と手がかりが図鑑に残る"),
        ("幻", 5, "#FFAA00", 6, 55, "半分以上が逃げる。条件がいくつも重なったときだけ")]
_CONDS = [("水辺", ["川", "海", "暖かい海", "冷たい海", "深い海", "沼", "マングローブ", "鍾乳洞", "繁茂した洞窟", "ディープダーク", "密林", "桜の林", "雪の地", "砂漠", "果ての地", "ほか"]),
          ("時刻", ["昼", "夜", "夜明け", "夕暮れ", "真夜中", "真昼"]),
          ("天気", ["晴れ", "雨", "雷雨"]),
          ("月", ["満月", "十三夜", "半月", "三日月", "新月"]),
          ("季節", ["春（3〜5月）", "夏（6〜8月）", "秋（9〜11月）", "冬（12〜2月）"]),
          ("灯原だけ", ["朱月", "灯りの中", "格2〜4の灯り", "灯りの外", "深い水"])]


def _fish_sec():
    mx = max(r[3] for r in _RAR)
    rows = "".join(f'''<div class="rar" style="--c:{c}">
        <span class="rar-n"><b class="dot">{"◆" * n}<s>{"◇" * (5 - n)}</s></b><span class="disp">{name}</span></span>
        <span class="rar-count"><span class="bar"><i style="width:{cnt / mx * 100:.0f}%"></i></span><b class="dot">{cnt}<small>種</small></b></span>
        <span class="rar-esc"><small>逃げる</small><span class="esc">{"".join(f'<i class="{"on" if k < esc // 10 else ""}"></i>' for k in range(6))}</span><b class="dot">{esc}%</b></span>
        <p>{txt}</p>
      </div>''' for name, n, c, cnt, esc, txt in _RAR)
    conds = "".join(f'<div class="cond"><dt class="dot">{k}</dt><dd>{"".join(f"<span>{x}</span>" for x in v)}</dd></div>' for k, v in _CONDS)
    return f'''<section class="stratum s-deep" id="fish">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">同じ場所でも、時がちがえば別の魚。</h2>
    <p class="lead">釣りをしていると、ふつうの魚の代わりに「灯魚（ひうお）」がかかります。全部で106種。どこで、いつ、どんな空の下で釣るかで、かかる顔ぶれが変わります。</p>
    <div class="rars">{rows}</div>
    <p class="mu" style="font-size:14px;margin-top:12px">逃げる確率は、釣の道「糸さばき」でさげられます。大きな灯りの中で釣ると、少し逃げにくくなります。</p>
  </div>
</section>

<section class="stratum s-dusk" id="conds">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">かかる魚を決めるもの。</h2>
    <p class="lead">灯魚にはそれぞれ条件があります。珍しい魚ほど、いくつもの条件が重なったときにしか現れません。季節は、現実の日本の暦です。</p>
    <dl class="conds">{conds}</dl>
    <div class="three">
      <div><h3 class="h3 disp">図鑑と灯原一</h3><p class="mu"><span class="kbd">/waza fish</span> で図鑑が開きます。川・海・沼・地底・野山・特別のつまみで分かれ、釣った・影だけ見た・まだ、の3つの状態で並びます。大きさ（cm）が記録され、種類ごとのいちばん大きな記録が「灯原一」として残ります。</p></div>
      <div><h3 class="h3 disp">魚読み</h3><p class="mu">釣の道の「魚読み」を覚えると、竿を投げたとき、その場・その時に釣れる灯魚が何種いて、まだ図鑑にないものがいくつあるかがわかります。</p></div>
      <div><h3 class="h3 disp">ヌシ</h3><p class="mu">釣の道の奥義「主の竿」を覚えると、倍ほどの大きさの「ヌシ」がかかります。秘と幻、そしてヌシを釣り上げると、全体に知らされます。</p></div>
    </div>
    <a href="wiki-hiuo.html" class="wiki-band" style="margin-top:28px"><span class="wb-k dot">WIKI</span><span class="wb-b"><b class="disp">灯魚図鑑</b><span>106種の珍しさ・大きさ・水辺・手がかり（珍しい魚は伏せてあります）。</span></span><span class="wb-go">図鑑を見る<i></i></span></a>
    <p class="note cold"><b>放置した釣り場では、灯魚はかかりません。</b>視点が5分動かないあいだは、灯魚も経験値も出ません。</p>
  </div>
</section>
'''


def _body(k):
    c = CH[k]
    if c["id"] == "akashi":
        b = "\n".join(_clean(_SEC[s]) for s in c["sec"])
        i = b.rfind("\n  </div>\n</section>")
        return b[:i] + '\n    <a href="akashi.html" class="wiki-band ak-band" style="margin-top:44px"><span class="wb-k dot">WIKI</span><span class="wb-b"><b class="disp">263の証を、ひとつずつ</b><span>目標・報酬・段の道・秘められた証の手がかり。名前や報酬で探せます。</span></span><span class="wb-go">灯の証 Wiki へ<i></i></span></a>' + b[i:]
    if c["id"] == "hiwaza":
        return _hiwaza_sec()
    if c["id"] == "fish":
        return _fish_sec()
    if c["id"] == "himon":
        return _himon_sec()
    if c["id"] == "sato":
        return _sato_sec() + '\n<script src="assets/sato.js" defer></script>'
    if c["id"] == "shoku":
        return _shoku_sec()
    if c["id"] == "musubi":
        return _musubi_sec()
    return "\n".join(_clean(_SEC[s]) for s in c["sec"])


_CH_SAY = {
    "lantern": "まずは1基。次の1基を16ブロック以内に置けば、灯路でつながるよ。",
    "night": "夜は24分。来たばかりなら、灯りの外へは出るな。",
    "higui": "灯喰いは、人を見ない。灯籠だけを見る。端の灯籠から守れ。",
    "buff": "欠片が集まったら、加護をひらこう！ 灯りの中だけで効くからね。",
    "hiwaza": "急がなくていいよ。1日ちょっとずつ、毎日育てるのがいちばん。",
    "fish": "同じ水辺でも、時刻と月で、かかる魚が変わるんだ。",
    "himon": "段が上がるほど、くじは高い。でも1冊で、遊び方が変わることもあるよ。",
    "akashi": "やったことは、ぜんぶ証になるよ。秘められた証もあるからね。",
    "more": "灯標に名前をつけたら、灯渡りでひとっ飛び。",
    "sato": "里の土地は、灯りでできてる。灯籠をつなぐほど、里は広がるよ。",
    "shoku": "職のいちばん上の力は、自分じゃなくて、仲間のために使う力なんだ。",
    "musubi": "里がちがっても、縁は結べる。手紙は、いない人にも届くよ。",
}


def _rail(cur):
    return '<nav class="rail" aria-label="章">' + "".join(
        f'<a href="guide-{c["id"]}.html" style="--rc:{c["c"]}" title="{i + 1:02d} {c["t"]}"{" aria-current=\"page\"" if i == cur else ""}><span class="dot">{i + 1:02d}</span><span class="rail-t">{c["t"]}</span></a>'
        for i, c in enumerate(CH)) + "</nav>"


def chapter_page(k):
    c = CH[k]
    prev = CH[k - 1] if k > 0 else None
    nxt = CH[k + 1] if k + 1 < len(CH) else None
    hero = f'''<div class="hero ch-hero" style="--c:{c["c"]}">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    <nav class="crumb" aria-label="現在地"><a href="guide.html">遊び方</a><span aria-hidden="true">›</span><span>第{k + 1}章</span></nav>
    <div class="ch-head">{pix(CH_ICONS[c["id"]], "ch-ic big")}<div><p class="ch-big dot">CHAPTER {k + 1:02d} ／ {len(CH):02d}</p><h1 class="disp h1-sub">{c["t"]}</h1></div></div>
    <p class="lead">{c["sum"]}</p>
    {_rail(k)}
  </div>
</div>'''

    def pg(x, i, cls, label):
        if x is None:
            return f'<a href="guide.html" class="pg {cls}" style="--c:var(--amber)"><small class="dot">{label}</small><b>目次にもどる</b><span class="mu">{len(CH)}の章の一覧へ</span></a>'
        return f'<a href="guide-{x["id"]}.html" class="pg {cls}" style="--c:{x["c"]}"><small class="dot">{label} {i + 1:02d}</small><b>{x["t"]}</b><span class="mu">{x["sum"]}</span></a>'

    pager = f'''<section class="stratum s-rock pager-s">
  <div class="edge"></div>
  <div class="wrap">
    <nav class="pager" aria-label="前後の章">{pg(prev, k - 1, "prev", "← 前の章")}{pg(nxt, k + 1, "next", "次の章 →")}</nav>
    <p class="pager-toc"><a href="guide.html" class="gbtn sm">≡ 遊び方の目次</a></p>
  </div>
</section>'''
    body = _body(k)
    w = body.find('<div class="wrap">') + len('<div class="wrap">')
    body = body[:w] + "\n    " + say_box(_CH_WHO[c["id"]], _CH_SAY[c["id"]]) + body[w:]
    return hero + "\n" + body + "\n" + pager


def _guide_index():
    layers = ""
    for li, (no, name, note) in enumerate(LAYERS):
        cards = ""
        for k, c in enumerate(CH):
            if c["layer"] != li:
                continue
            cards += f'''<a href="guide-{c["id"]}.html" class="ch" style="--c:{c["c"]}">
        <span class="ch-top"><span class="ch-no">{k + 1:02d}</span>{pix(CH_ICONS[c["id"]])}</span>
        <h3 class="disp">{c["t"]}</h3>
        <p>{c["sum"]}</p>
        <ul>{"".join(f"<li>{x}</li>" for x in c["facts"])}</ul>
        <span class="ch-go">読む<i></i></span>
      </a>'''
        layers += f'''<div class="glayer">
      <div class="layer-h"><span class="dot">{no}</span><h2 class="disp">{name}</h2><p>{note}</p></div>
      <div class="chs">{cards}</div>
    </div>'''
    return f'''<div class="hero">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div><div class="moon" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    <h1 class="disp h1-sub">遊び方</h1>
    <p class="lead">灯りを置き、つなぎ、夜から守り、育てて、残す。灯原のしくみを{len(CH)}の章にまとめました。気になる章から開いてください。</p>
    {_rail(-1)}
  </div>
</div>
<section class="stratum s-deep gi">
  <div class="edge"></div>
  <div class="wrap">
    <div class="gi-start">{pix(CH_ICONS["lantern"], "ch-ic lit")}<p><b>はじめての人は、第一層の3章だけで大丈夫です。</b>灯籠を置き、夜を知り、灯喰いから守れれば、最初の夜は越えられます。ほかの章は、遊びながらでどうぞ。</p><a href="guide-lantern.html" class="pbtn">第1章から読む</a></div>
    {layers}
    <div class="wk-bands">
    <a href="wiki.html" class="wiki-band"><span class="wb-k dot">WIKI</span><span class="wb-b"><b class="disp">灯技 Wiki</b><span>130の技の効き目・要る Lv・技点・待ち時間、技の木、奥義の試練、務め、灯魚図鑑、技の組み立て。</span></span><span class="wb-go">開く<i></i></span></a>
    <a href="akashi.html" class="wiki-band ak-band"><span class="wb-k dot">WIKI</span><span class="wb-b"><b class="disp">灯の証 Wiki</b><span>263の証の目標と報酬、段の道、10の位階、称号・灯りの色・足跡の手に入れ方。</span></span><span class="wb-go">開く<i></i></span></a>
    <a href="himon.html" class="wiki-band hm-band"><span class="wb-k dot">WIKI</span><span class="wb-b"><b class="disp">灯紋 Wiki</b><span>{len(HM["defs"])}の紋の段・効き目・刻めるもの、紋書の引き方、刻み方と重ね方。</span></span><span class="wb-go">開く<i></i></span></a>
    <a href="hisato.html" class="wiki-band hs-band"><span class="wb-k dot">WIKI</span><span class="wb-b"><b class="disp">灯里 Wiki</b><span>4つの格、5つの職のバフと日課・週課、位と匠の試し、施設の素材、礎、ずるの防ぎ方。</span></span><span class="wb-go">開く<i></i></span></a>
    </div>
    <a href="commands.html" class="wiki-band cmd-band"><span class="wb-k dot">CMD</span><span class="wb-b"><b class="disp">コマンド一覧</b><span>/menu・/tomoshibi・/sato・/akashi・/waza・/himon・/yomatsuri・/tokoyo のすべて。探して、すぐ見つかる。</span></span><span class="wb-go">開く<i></i></span></a>
  </div>
</section>'''



# ───────────────────────── 夜祭 ─────────────────────────
events = f'''<div class="hero">
  <div class="sky" style="background:linear-gradient(180deg,#0B0C24 0%,#211A46 55%,#4A2F66 100%)"></div><div class="stars" aria-hidden="true"></div>
  <div class="garland" data-garland aria-hidden="true" style="margin-top:8px"></div>
  <div class="wrap phead" id="content" style="padding-top:8px">
    <h1 class="disp h1-sub">毎週土曜21時は、夜祭。</h1>
    <p class="lead">この時間にログインすれば、かならずだれかがいます。人数がそろうと、週替わりのゲームが自動で始まります。</p>
    <div style="display:flex;flex-wrap:wrap;gap:32px 56px;align-items:flex-end;margin-top:32px">
      <div><p class="depth">次の夜祭</p><p class="disp" style="font-size:clamp(26px,3.4vw,40px);line-height:1.3;margin:6px 0 14px" data-fest-date>夜祭は毎週土曜 21:00</p>{cd("fest", "次の夜祭まで")}</div>
      <div class="pn" style="flex:1 1 320px;min-width:0;background:rgba(10,8,30,.6)"><p class="mu" style="font-size:14px;font-weight:700">この日のゲーム</p><h2 class="disp" style="margin:6px 0 8px;font-size:30px;line-height:1.3;color:#F6B8CE" data-fest-game>週替わりで4種類</h2><p style="font-size:16px" data-fest-desc>灯籠リレー、闇かくれんぼ、建築早押し、夜明けまで。</p></div>
    </div>
  </div>
</div>

<section class="stratum tex s-soil" id="how">
  <div class="wrap">
    <p class="depth">始まり方</p>
    <h2 class="disp h2">何もしなければ、参加です。</h2>
    <ol class="steps" style="margin-top:28px">
      <li><div><h3>21時に、120秒の募集が始まる</h3><p>画面の上に、残り時間と参加人数のバーが出ます。</p></div></li>
      <li><div><h3>参加する人は、そのまま待つ</h3><p>何も打たなくてかまいません。今回は見送りたい人だけ <span class="kbd">/yomatsuri out</span> と打ちます。気が変わったら <span class="kbd">/yomatsuri in</span>。</p></div></li>
      <li><div><h3>人数がそろっていれば、自動で始まる</h3><p>必要な人数は、そのときサーバーにいる人数の4割（上限8人）です。届かなければ、その回は見送りになります。</p></div></li>
      <li><div><h3>会場へ移動して、終わったら元の場所へ戻る</h3><p>灯籠リレーと闇かくれんぼは、参加者を会場へ運びます。終わると、もといた場所に戻ります。</p></div></li>
    </ol>
    <div class="tbl-wrap"><table>
      <thead><tr><th>サーバーにいる人数</th><th>始まるのに必要な人数</th></tr></thead>
      <tbody>
        <tr><td class="n">5人</td><td class="n">2〜4人（ゲームによる）</td></tr>
        <tr><td class="n">10人</td><td class="n">4人</td></tr>
        <tr><td class="n">15人</td><td class="n">6人</td></tr>
        <tr><td class="n">20人〜</td><td class="n">8人</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="stratum s-dusk" id="games">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">4週でひとまわり</p>
    <h2 class="disp h2">ゲームは、毎週かわる。</h2>
    <p class="lead">苦手なゲームの週があっても、次の週は別の遊びです。</p>
    <div class="tbl-wrap" data-rot><table>
      <thead><tr><th>ゲーム</th><th>どんな遊び</th><th>長さ</th><th>最少人数</th></tr></thead>
      <tbody>
        <tr data-g="0"><th>灯籠リレー</th><td>紅組と藍組に分かれ、出発点から終点まで、自分の組の灯籠だけで先に灯路を通した組の勝ち。「祭の灯籠」が16個ずつ配られます。祭の灯籠は、祭が終わると置いたものも手もとのものも消えます。</td><td class="n">12分</td><td class="n">4人</td></tr>
        <tr data-g="1"><th>闇かくれんぼ</th><td>5人に1人が鬼。鬼は最初の30秒、動けません。触れられたら負けで、範囲の外に出ても負け。灯籠を置くと10秒間、体が光ります。朝まで隠れきれば勝ち。</td><td class="n">8分</td><td class="n">4人</td></tr>
        <tr data-g="2"><th>建築早押し</th><td>お題（灯台、橋、屋台など）の建物を15分で建てます。最後に <span class="kbd">/yomatsuri vote 名前</span> で、いちばん良いと思う人に投票します。途中参加できます。</td><td class="n">15分</td><td class="n">3人</td></tr>
        <tr data-g="3"><th>夜明けまで</th><td>朱月の夜を呼びます。倒れたら脱落。朝まで生き延びた人の勝ち。全員で灯りを守りきる夜です。途中参加できます。</td><td class="n">10分</td><td class="n">2人</td></tr>
      </tbody>
    </table></div>
    <style>[data-rot] tr.cur{{background:rgba(242,181,68,.12)}}[data-rot] tr.cur th::after{{content:'次回';display:inline-block;margin-left:10px;padding:0 8px;background:var(--amber);color:#24180A;font-size:12px;line-height:1.8}}</style>
  </div>
</section>

<section class="stratum s-deep" id="reward">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">ごほうび</p>
    <h2 class="disp h2">強くはならない。だから、だれでも同じ条件。</h2>
    <p class="lead">夜祭でもらえるのは、灯りの色と、名前の横の印だけです。はじめての人も、ずっといる人も、同じ条件で遊べます。</p>
    <div class="two">
      <div>
        <h3 class="h3 disp">参加した回数で、色がふえる</h3>
        <div class="tbl-wrap" style="margin-top:8px"><table style="min-width:0"><tbody>
          <tr><th><span class="sw" style="background:#F29BB8"></span>桜</th><td class="n">5回</td></tr>
          <tr><th><span class="sw" style="background:#8FC3E8"></span>水縹</th><td class="n">10回</td></tr>
          <tr><th><span class="sw" style="background:#8BD18F"></span>若竹</th><td class="n">20回</td></tr>
        </tbody></table></div>
        <p class="mu" style="font-size:15px;margin-top:10px">勝ち負けは関係ありません。参加した回数だけで数えます。</p>
      </div>
      <div><h3 class="h3 disp">勝った人には、印</h3><p class="mu">勝者は次の夜祭まで、プレイヤー一覧の名前の横に ✦ がつきます。次の夜祭でだれかが勝つと、印はその人に移ります。</p><h3 class="h3 disp" style="margin-top:28px">灯の証「祭の章」</h3><p class="mu">参加と勝利は、灯の証にも記録されます。4つの遊びすべてで勝つ、50回勝つ、といった証があります。</p></div>
    </div>
  </div>
</section>

<section class="stratum s-blood" id="calendar">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">シーズン1の予定</p>
    <h2 class="disp h2">おぼえておく夜。</h2>
    <ol class="night">
      <li><time>11月7日</time><div><h3>開幕の夜</h3><p>21時、まっさらな世界に全員が同じ場所から入ります。参加した全員に、灯りの色「はじまりの灯」。最初の夜祭もこの夜です。</p></div></li>
      <li><time>毎週土曜</time><div><h3>夜祭</h3><p>21時から。4つのゲームが週替わりで回ります。</p></div></li>
      <li><time>7夜ごと</time><div><h3>朱月の夜</h3><p>ゲームの中の7夜に一度（現実ではおよそ3時間ごと）、月が赤くなります。敵は強く、群れと精鋭がふえます。</p></div></li>
      <li><time>6週目</time><div><h3>大夜祭</h3><p>12月12日（土）の予定。全員でひとつの灯路をのばす、シーズンの山場です。くわしい内容は Discord で知らせます。</p></div></li>
    </ol>
  </div>
</section>
'''


# ───────── きまり：違反の表（data/ritsu.json ＝ 灯律の rules.yaml から作る。数字は手で書かない） ─────────
import json as _rj, html as _rh

RITSU = _rj.loads((pathlib.Path(__file__).parent / "data" / "ritsu.json").read_text(encoding="utf-8"))


def _ritsu_html():
    R = RITSU
    e = _rh.escape
    steps = "".join(f'<div><b>{e(x["label"])}</b><span>レベル {x["min"]}{"〜" + str(x["max"]) if x["max"] else " 以上"}</span></div>' for x in R["steps"])
    tiers = [("重度", "16〜20", "s16"), ("中度", "9〜15", "s9"), ("軽度", "4〜8", "s4"), ("注意", "1〜3", "s1")]
    tb = ""
    for t, rng, cls in tiers:
        rows = "".join(f'<tr><th class="n">{e(v["code"])}</th><td data-label="行為"><b>{e(v["name"])}</b></td><td data-label="ここから">{e(v["from"])}</td>'
                       f'<td data-label="レベル" class="n">{v["level"]}</td></tr>' for v in R["violations"] if v["tier"] == t)
        n = sum(1 for v in R["violations"] if v["tier"] == t)
        tb += (f'<details class="rt-tier {cls}"><summary><b>{t}</b><span>レベル {rng}・{n}項目</span></summary>'
               f'<div class="tbl-wrap"><table class="stack rt-tbl"><thead><tr><th>番号</th><th>行為</th><th>ここから</th><th>レベル</th></tr></thead><tbody>{rows}</tbody></table></div></details>')
    mods = "".join(f'<tr><th class="n">{e(m["code"])}</th><td data-label="内容">{e(m["name"])}</td><td data-label="補正" class="n">{"+" if m["add"] > 0 else "−"}{abs(m["add"])}</td></tr>' for m in R["modifiers"])
    notv = "".join(f"<li>{e(x)}</li>" for x in R["not_violations"])
    sp = "".join(f"<li>{e(x)}</li>" for x in R["special"])
    kinds = "".join(f'<li><b>{e(r["label"])}</b><span>{e("・".join(r["need"]))}</span></li>' for r in R["report_types"])
    monthly = ""
    md = sorted((pathlib.Path(__file__).parent / "data").glob("ritsu-monthly-*.json"))
    if md:
        m = _rj.loads(md[-1].read_text(encoding="utf-8"))
        items = "".join(f'<tr><th class="n">{e(x["code"])}</th><td>{e(x["name"])}</td><td class="n">{x["n"]}</td></tr>' for x in m["by_code"][:12])
        monthly = (f'<h3 class="h3 disp" style="margin-top:56px">{e(m["month"])} のまとめ</h3><p class="mu">通報 {m["reports"]} 件・罰 {m["punished"]} 件・違反なし {m["no_violation"]} 件・取り消し {m["revoked"]} 件（名前は出しません）</p>'
                   f'<div class="tbl-wrap"><table><thead><tr><th>番号</th><th>違反</th><th>件数</th></tr></thead><tbody>{items}</tbody></table></div>')
    return f"""<section class="stratum s-deep" id="penalty">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">対応の流れ</p>
    <h2 class="disp h2">きまりをやぶったとき</h2>
    <p class="lead">してしまったことを、下の表で「レベル」にして、その合計で罰が決まります。だれに対しても同じ表を使います。まちがいはだれにでもあるので、軽いものは注意から。わざと人を傷つけたり、人のものを大きくこわしたりしたときは、すぐに止めます。</p>
    <div class="ladder rt-ladder">{steps}</div>
    <div class="two rt-two">
      <div><h3 class="h3 disp">制限のあいだ</h3><p class="mu">ことばの違反（暴言・連投・煽りなど）は、チャット・里と一団のチャット・手紙・看板・本・合図と Discord の発言が止まります。それ以外の違反は、他人の土地で建てる・壊す、他人の箱を開ける、取引・屋台・小包・旅の依頼、PvP、合流・呼ぶが止まります。<b>自分の土地で遊ぶこと・灯渡り・帰里は止まりません。</b></p></div>
      <div><h3 class="h3 disp">入ったときに分かる</h3><p class="mu">罰を受けた人には、画面のまん中とチャットに、理由・件の番号・いつまでか・異議の出し方が出ます。制限中は画面の上に残り時間が出ます。BAN のときは、入ろうとした画面に同じことが出ます。注意は「わかった」を押すまで、入るたびに出ます。</p></div>
    </div>
    <div class="two rt-two">
      <div><h3 class="h3 disp">こわされた物は戻す</h3><p class="mu">罰とは別に、こわされた建物はゲームの記録から元に戻し、持ち去られた物と、こわされた灯籠は持ち主に返します。</p></div>
      <div><h3 class="h3 disp">名前を出すのは、永久BANだけ</h3><p class="mu">運営が確かめて永久BANに決まった人だけを、Discord の #処罰の記録 に名前と番号で載せます。それ以外は、本人と通報した人にだけ知らせます。毎月、名前なしの件数をこのページと Discord で公開します。</p></div>
    </div>
  </div>
</section>

<section class="stratum s-rock" id="levels">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">違反の表</p>
    <h2 class="disp h2">どこからが、どのレベルか</h2>
    <p class="lead">迷わないように、数で決めてあります。表にないことは、いちばん近いものに当てはめて、かならず運営が確かめます。</p>
    {tb}
    <h3 class="h3 disp" style="margin-top:56px">足す・引く</h3>
    <div class="tbl-wrap"><table class="stack"><thead><tr><th>番号</th><th>内容</th><th>補正</th></tr></thead><tbody>{mods}</tbody></table></div>
    <p class="note">いくつも重なったときは、いちばん重いものに、ほか1つごとに +2。合計は1より下がりません。16以上には引く補正をかけません。同じ違反の3回目は、罰を1段上げます。軽い違反だけで永久BANにはなりません。違反の回数は90日で数え直します（BAN の歴は残ります）。</p>
    <div class="two rt-two">
      <div><h3 class="h3 disp">違反にならないこと</h3><ul class="rt-list">{notv}</ul></div>
      <div><h3 class="h3 disp">特別なきまり</h3><ul class="rt-list">{sp}</ul></div>
    </div>
    {monthly}
  </div>
</section>

<section class="stratum s-dusk" id="help">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">連絡先</p>
    <h2 class="disp h2">困ったとき：通報と異議</h2>
    <p class="lead">こわされた、とられた、いやなことを言われた、ずるをしている人を見た。どれも Discord の <b>/通報</b> で知らせてください。やり返さないことが、いちばん早く解決します。</p>
    <ol class="steps" style="margin-top:28px">
      <li><div><h3>その場をはなれて、画面を写す</h3><p>言い返したり、こわし返したりしないでください。相手の名前・言葉・場所が分かるように、画面を写しておきます（F3 で座標が出ます）。</p></div></li>
      <li><div><h3>Discord で /通報</h3><p>必ず入れるのは3つ：<b>相手の MCID</b>（候補から選ぶ）・<b>証拠の画像</b>（1〜5枚）・<b>何をされたか</b>（いつ・どこ・何を）。送る前に確認が出ます。</p></div></li>
      <li><div><h3>専用のスレッドで待つ</h3><p>あなたとボット・運営だけが見えるスレッドができます。ゲームの記録と照らして調べ、結果をそこで知らせます。足りないものがあれば聞くので、すべて載せてから「足し終えたので判断する」を押してください。</p></div></li>
    </ol>
    <h3 class="h3 disp" style="margin-top:56px">種類ごとに、あるとよいもの</h3>
    <ul class="rt-kinds">{kinds}</ul>
    <div class="two rt-two">
      <div><h3 class="h3 disp">罰が違うと思ったら</h3><p class="mu">Discord の <b>#異議</b> で「異議を出す」を押し、ゲームの画面に出た<b>件の番号</b>（#0123）と<b>異議の印</b>（6文字）を入れてください。異議は1つの罰に1回、運営が72時間を目安にお返事します。異議のあいだも罰は続きます。取り消しになったときは、記録からも消します。</p></div>
      <div><h3 class="h3 disp">うその通報は違反です</h3><p class="mu">作った画像やうその説明で人を罰させようとすることは、それ自体が重い違反（16-C）です。画像だけでは罰を出さず、かならずゲームの記録と照らします。通報は1人1日5件までです。</p></div>
    </div>
    <div class="btns" style="margin-top:24px"><a href="{DISCORD}" class="pbtn dbtn" target="_blank" rel="noopener">Discord を開く</a></div>
  </div>
</section>"""

# ───────────────────────── きまり ─────────────────────────
rules = sub_hero("rules.html", "きまり", "むずかしいことはありません。人のものをこわさない。人をいやな気持ちにさせない。この二つです。",
                 [("dont", "してはいけないこと"), ("safe", "守られていること"), ("penalty", "やぶったとき"), ("levels", "違反の表"), ("help", "通報と異議"), ("parents", "保護者の方へ")]) + f'''
<section class="stratum tex s-soil" id="dont">
  <div class="wrap narrow">
    <p class="depth">6つのきまり</p>
    <h2 class="disp h2">してはいけないこと</h2>
    <ul class="rules">
      <li><div><h3>人の建物やものを、こわさない・とらない</h3><p>ほかの人が建てたもの、チェストの中身、畑や動物に、ことわりなく手を出さないでください。「だれのものかわからない」ときは、さわらないのが正解です。</p></div></li>
      <li><div><h3>ずるをしない</h3><p>地面が透けて見える、自動で動く、ふつうより速く動くなどの改造や道具は使えません。不具合を見つけたら、使わずに Discord で知らせてください。見た目を変えるだけのものや、動きを軽くするものはかまいません。</p></div></li>
      <li><div><h3>人をいやな気持ちにさせない</h3><p>悪口、からかい、仲間はずれ、しつこくつきまとうこと、差別的なことばは禁止です。チャットでも、Discord でも同じです。</p></div></li>
      <li><div><h3>自分や人のことを、くわしく書かない・聞かない</h3><p>本名、住所、学校、電話番号、SNSのアカウントなどを、チャットに書いたり聞いたりしないでください。</p></div></li>
      <li><div><h3>宣伝や勧誘をしない</h3><p>ほかのサーバーや商品の宣伝、お金や物のやりとりの持ちかけは禁止です。</p></div></li>
      <li><div><h3>招待を水増ししない</h3><p>自分で別のアカウントを作って自分を招待するなど、招待の数をごまかすことは禁止です。見つかった場合、色と記録を取り消します。</p></div></li>
    </ul>
    <p class="note">ここに書いていないことでも、「これをされたら自分はいやだな」と思うことは、しないでください。迷ったら Discord で聞いてください。</p>
  </div>
</section>

<section class="stratum s-stone" id="safe">
  <div class="edge"></div>
  <div class="wrap narrow">
    <p class="depth">しくみで守られていること</p>
    <h2 class="disp h2">守られていること</h2>
    <ul class="rules ok">
      <li><div><h3>ほかの人は、あなたの灯籠を壊せない</h3><p>壊せるのは、置いた本人と、本人が「仲間」に加えた人だけです。</p></div></li>
      <li><div><h3>灯りの中では、敵に襲われない</h3><p>敵は灯りに入れず、灯りの中の人を狙えません（灯喰いとボスをのぞく）。</p></div></li>
      <li><div><h3>灯りの中は、爆発で壊れない</h3><p>クリーパーやTNTの爆発で、灯りの中のブロックは壊れません。</p></div></li>
      <li><div><h3>灯りの中で倒れても、持ち物を失わない</h3><p>持ち物も経験値も、そのまま残ります。</p></div></li>
      <li><div><h3>いない間に、灯りは消されない</h3><p>灯喰いが狙うのは、近くに人がいる灯籠だけです。</p></div></li>
      <li><div><h3>来たばかりの人は、狙われない</h3><p>はじめて入ってから24時間と、灯籠が3基より少ない拠点には、灯喰いは来ません。</p></div></li>
      <li><div><h3>強さは、売っていない</h3><p>お金で強くなる仕組みはありません。色や印は、見た目だけです。</p></div></li>
    </ul>
    <p class="note cold"><b>建物は、灯籠とちがって「壊せない」ようにはなっていません。</b>こわされたときは、運営が記録を調べて、できるかぎり元に戻します。下の「困ったとき」の手順で知らせてください。</p>
  </div>
</section>

{_ritsu_html()}

<section class="stratum s-rock" id="parents">
  <div class="edge"></div>
  <div class="wrap narrow">
    <p class="depth">保護者の方へ</p>
    <h2 class="disp h2">お子さまが遊ぶ前に</h2>
    <div class="faq">
      <details open><summary>費用はかかりますか</summary><p>かかりません。サーバーへの参加は無料で、ゲーム内に課金の仕組みはありません。マインクラフト本体と、機種によってはオンラインプレイの加入が別に必要です。</p></details>
      <details><summary>知らない人と話すことになりますか</summary><p>ほかの参加者と文字で会話できます。本名や住所、学校などを書いたり聞いたりすることは禁止しており、見つけた場合は運営が対応します。マインクラフトの設定で、チャットを表示しないようにもできます。</p></details>
      <details><summary>Discord は必要ですか</summary><p>遊ぶだけなら必要ありません。お知らせと問い合わせに使っています。Discord は利用規約で13歳以上が対象です。13歳未満のお子さまの場合は、保護者の方が代わりにご連絡ください。</p></details>
      <details><summary>どんな情報が保存されますか</summary><p>ゲーム内の名前、接続の記録（IPアドレスを含みます）、ゲーム内での行動の記録（チャット・看板・本・箱の出し入れ・ブロックなど）です。細かい記録は30日で消え、処罰に使った記録だけを残します。運営と不正への対応のためだけに使い、外部に提供しません。</p></details>
      <details><summary>通報は AI が判断するのですか</summary><p>通報された件では、関係するゲーム内の記録（その時間・その場所・関係する人の分だけ）と通報の文章・画像を、AI（Anthropic 社の Claude）に送って、きまりの表に当てはめます。IP アドレスや、関係のない人の記録は送りません。数を数える・罰の重さを決めるのはプログラムで、重い件や迷う件は運営が確かめます。永久BANは、かならず運営が決めます。</p></details>
      <details><summary>ゲーム機から入るときの設定変更は安全ですか</summary><p>本体のネットワーク設定のうち、DNS という項目を変更します。いつでも元に戻せますが、かならず保護者の方が内容を確かめたうえで行ってください。</p></details>
      <details><summary>このサーバーは公式のものですか</summary><p>いいえ。灯原は有志が運営する非公式のサーバーで、Mojang Studios および Microsoft とは関係ありません。</p></details>
    </div>
  </div>
</section>
'''

# ───────────────────────── 灯技 Wiki ─────────────────────────
# data/hiwaza.json（プラグインの定義から書き出したもの）から作る。数字は手で書かない。
import json as _wj, html as _wh

HW = _wj.loads((pathlib.Path(__file__).parent / "data" / "hiwaza.json").read_text(encoding="utf-8"))
_KIND = ["常時", "切替", "発動"]
_KIND_C = ["#C9CFDA", "#55FFFF", "#FF7AE6"]
_KIND_HELP = ["覚えれば、いつも働く", "右クリックでオン／オフ", "主技・副技にして使う"]
_TIER = ["", "一の段", "二の段", "三の段", "奥義"]
_ROMAN = ["", "Ⅰ", "Ⅱ", "Ⅲ"]
_PCOL = ["#FFAA00", "#B46CFF", "#55FFFF", "#55FF55", "#FFFF55", "#3CC8C8", "#FF55FF", "#FFFFFF", "#FF5555", "#7C7CFF"]
_E = _wh.escape


def _sec(s):
    if s >= 60 and s % 60 == 0:
        return f"{s // 60}分"
    if s >= 60:
        return f"{s // 60}分{s % 60}秒"
    return f"{s}秒"


def _desc(n):
    return "".join(n["desc"])


def _num(v):
    return f"{v:,}"


# 道ごとの「育つこと」（経験値の入り口）。プラグインの数え方と同じ。
def _xp_rows(i):
    mx, wx, cx = HW["mineXp"], HW["woodXp"], HW["cropXp"]
    if i == 2:
        groups = {}
        for k, v in mx.items():
            groups.setdefault(v, []).append(k)
        names = {1: "石・深層岩・花崗岩・ネザーラックなど", 2: "黒曜石・アメジストの塊", 4: "石炭・銅・石英・ネザー金", 5: "レッドストーン", 6: "鉄", 7: "ラピスラズリ", 10: "金",
                 25: "ダイヤモンド・エメラルド", 50: "古代の残骸"}
        return [(names.get(v, "ほか"), f"+{v}") for v in sorted(groups)]
    if i == 3:
        return [("原木・幹（オーク・トウヒ・桜・ペールオークなど、すべて）", f"+{max(wx.values())}"), ("巨大キノコのかさ", "+2")]
    if i == 4:
        return [("小麦・ニンジン・ジャガイモ・ビートルート・ネザーウォート・カカオ（実ったもの）", "+3"), ("スイカ・カボチャ", "+4"), ("トーチフラワー・ウツボカズラ", "+6")]
    return {
        0: [("灯籠を置く", "+25"), ("灯喰いから灯籠を守りきる", "+60"), ("消えた灯籠を灯し直す", "+30"), ("灯喰いを倒す", "+60"), ("夜、灯りの中で過ごす", "+2 ／分")],
        1: [("夜を越えて夜明けを迎える", "+40"), ("朱月の夜を越える", "+150"), ("夜、灯りの外で過ごす", "+3 ／分"), ("夜哭きの精鋭を倒す", "+20")],
        5: [("魚を釣る（なんでも）", "+15"), ("灯魚：並 ／ 珍 ／ 稀", f"+{HW['rarityXp'][1]} ／ +{HW['rarityXp'][2]} ／ +{HW['rarityXp'][3]}"),
            ("灯魚：秘 ／ 幻", f"+{HW['rarityXp'][4]} ／ +{HW['rarityXp'][5]}")],
        6: [("ものを作る", "+2"), ("灯籠を作る", "+15"), ("かまどから取り出す", "1個 +1"), ("（作る・かまどは合わせて1分に60まで）", "")],
        7: [("遠くへ進む（10秒ごと、まっすぐ進んだ距離 6ブロックにつき）", "+1"), ("はじめての土地（バイオーム）を訪れる", "+40"), ("（10秒で数えるのは120ブロックまで）", "")],
        8: [("動物を殖やす", "+15"), ("動物を手なずける", "+60"), ("羊の毛を刈る", "+3"), ("卵集めで卵を拾う", "+1"), ("（1分に150まで）", "")],
        9: [("付呪する", "+15×段 ＋ 使ったLv"), ("薬を醸造する", "1本 +8（1分に120まで）"), ("経験値オーブを拾う", "半分（1分に40まで）")],
    }[i]


_WIKIS = [("waza", "技", "灯技", "wiki.html", "#5AAAFF", "guide-hiwaza.html"), ("akashi", "証", "灯の証", "akashi.html", "#F29BB8", "guide-akashi.html"),
          ("himon", "紋", "灯紋", "himon.html", "#F2B544", "guide-himon.html"), ("hisato", "里", "灯里", "hisato.html", "#E9824A", "guide-sato.html")]


def _wiki_switch(cur):
    """どの Wiki にも、同じ場所に同じ切り替えを出す。"""
    tabs = "".join(f'<a href="{u}" style="--c:{c}"{" aria-current=\"page\"" if k == cur else ""}><span class="ws-k">{ch}</span>{t}<small>Wiki</small></a>' for k, ch, t, u, c, _ in _WIKIS)
    tabs += f'<a href="commands.html" class="wsw-cmd" style="--c:#C9D0DC"{" aria-current=\"page\"" if cur == "cmd" else ""}><span class="ws-k">令</span>コマンド</a>'
    return f'<nav class="wsw" aria-label="Wiki の切り替え">{tabs}</nav>'


def _wiki_crumb(cur, tail=""):
    w = next(x for x in _WIKIS if x[0] == cur)
    return f'<nav class="crumb" aria-label="現在地"><a href="guide.html">遊び方</a><span aria-hidden="true">›</span><a href="{w[3]}">{w[2]} Wiki</a>{tail}</nav>'


def _wiki_others(cur):
    w = next(x for x in _WIKIS if x[0] == cur)
    out = f'<p class="dot wside-h wside-x">ほかの Wiki</p>'
    out += "".join(f'<a href="{u}" class="ws-o" style="--c:{c}"><span class="ws-k">{ch}</span>{t} Wiki</a>' for k, ch, t, u, c, _ in _WIKIS if k != cur)
    out += f'<a href="{w[5]}" class="ws-o" style="--c:{w[4]}"><span class="ws-k">章</span>遊び方の「{w[2]}」の章</a>'
    return out


def _wiki_side(cur):
    items = f'<a href="wiki.html"{" aria-current=\"page\"" if cur == "top" else ""}><span class="ws-k" style="--c:var(--amber)">≡</span>Wiki のはじめ</a>'
    for i, p in enumerate(HW["paths"]):
        items += f'<a href="wiki-{p["id"]}.html" style="--c:{_PCOL[i]}"{" aria-current=\"page\"" if cur == p["id"] else ""}><span class="ws-k">{p["k"]}</span>{p["name"]}</a>'
    items += f'<a href="wiki-hiuo.html" style="--c:#4FD8C8"{" aria-current=\"page\"" if cur == "hiuo" else ""}><span class="ws-k">魚</span>灯魚図鑑</a>'
    items += f'<a href="wiki-build.html" style="--c:var(--amber)"{" aria-current=\"page\"" if cur == "build" else ""}><span class="ws-k">組</span>技の組み立て</a>'
    items += _wiki_others("waza")
    return f'<nav class="wside" aria-label="Wiki の目次"><p class="dot wside-h">灯技 Wiki</p>{items}</nav>'


def _wiki_hero(title, lead, color, crumb, icon_rows=None, sub=""):
    ic = pix(icon_rows, "ch-ic big") if icon_rows else ""
    return f'''<div class="hero ch-hero wk-hero" style="--c:{color}">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    {_wiki_switch("waza")}
    {_wiki_crumb("waza", crumb)}
    <div class="ch-head">{ic}<div><p class="ch-big dot">{sub}</p><h1 class="disp h1-sub">{title}</h1></div></div>
    <p class="lead">{lead}</p>
  </div>
</div>'''


def _tile(n, color):
    k = n["kind"]
    ranks = "".join("<i></i>" for _ in range(len(n["req"])))
    return f'''<a href="#{n["id"]}" class="tn k{k}" style="--c:{color}" title="{_E(n["name"])}"><span class="tn-k">{_KIND[k]}</span><b>{_E(n["name"])}</b><span class="tn-r">{ranks}</span><small class="dot">Lv{n["req"][0]}〜</small></a>'''


def _tree(p, color):
    nodes = p["nodes"]
    head = '<div class="tg-h"></div>' + "".join(f'<div class="tg-b"><span class="dot">枝{"一二三四"[b]}</span><b>{_E(p["branches"][b])}</b></div>' for b in range(4))
    rows = ""
    for t in (1, 2, 3):
        rows += f'<div class="tg-t dot">{_TIER[t]}</div>'
        for b in range(4):
            n = next((x for x in nodes if x["branch"] == b and x["tier"] == t), None)
            rows += f'<div class="tg-c">{_tile(n, color) if n else ""}</div>'
    cap = next(x for x in nodes if x["tier"] == 4)
    rows += f'<div class="tg-t dot cap">奥義</div><div class="tg-cap">{_tile(cap, color)}<p class="mu">三の段を {HW["capNeeds"]} つ覚え、Lv{cap["req"][0]} と「奥義の試練」を果たすと開く</p></div>'
    return f'<div class="tg" role="group" aria-label="技の木">{head}{rows}</div>'


def _node_card(p, n, color):
    k = n["kind"]
    parent = next((x for x in p["nodes"] if x["id"] == n["parent"]), None) if n["parent"] else None
    if n["tier"] == 4:
        need = f'三の段の技を {HW["capNeeds"]} つ ＋ 奥義の試練「{_E(p["trial"])}」' + ("（灯籠プラグインがなければ試練なし）" if p["trialTomo"] else "")
    elif parent:
        need = f'同じ枝の「<a href="#{parent["id"]}">{_E(parent["name"])}</a>」を先に覚える'
    else:
        need = "なし（一の段）"
    rows = ""
    for r in range(len(n["req"])):
        cd = f'<td class="n">{_sec(n["cooldown"][min(r, len(n["cooldown"]) - 1)])}</td>' if k == 2 else ""
        rows += f'<tr><th class="n">{_ROMAN[r + 1] if len(n["req"]) > 1 else "—"}</th><td>{_E(n["effect"][r])}</td><td class="n">Lv{n["req"][r]}</td><td class="n">{n["cost"][r]}</td>{cd}</tr>'
    act = f'<p class="nc-act"><span>灯力</span><b class="dot">{n["gauge"]}</b><span>待ち時間</span><b class="dot">{" → ".join(_sec(c) for c in n["cooldown"])}</b></p>' if k == 2 else ""
    total = sum(n["cost"])
    place = "奥義" if n["tier"] == 4 else f'{_E(p["branches"][n["branch"]])}の枝 ・ {_TIER[n["tier"]]}'
    return f'''<article class="nc t{n["tier"]}" id="{n["id"]}" style="--c:{color}" data-name="{_E(n["name"])}">
      <header><span class="nc-tag k{k}">〔{_KIND[k]}〕</span><h3 class="disp">{_E(n["name"])}</h3><span class="nc-place dot">{place}</span></header>
      <p class="nc-desc">{_E(_desc(n))}</p>
      {act}
      <div class="tbl-wrap"><table class="nc-t"><thead><tr><th>段</th><th>効き目</th><th>要る Lv</th><th>技点</th>{"<th>待ち</th>" if k == 2 else ""}</tr></thead><tbody>{rows}</tbody></table></div>
      <p class="nc-need"><span>覚える条件</span>{need}</p>
      <p class="nc-foot mu"><span>{_KIND_HELP[k]}</span><span>すべての段で技点 {total}</span><span class="dot">id: {n["id"]}</span></p>
    </article>'''


def wiki_path(i):
    p = HW["paths"][i]
    color = _PCOL[i]
    nodes = p["nodes"]
    xp = "".join(f'<tr><th>{_E(a)}</th><td class="n">{_E(b)}</td></tr>' for a, b in _xp_rows(i))
    acts = sum(1 for n in nodes if n["kind"] == 2)
    order = sorted(nodes, key=lambda n: (n["tier"] == 4, n["branch"], n["tier"]))
    cards = ""
    for b in range(4):
        cards += f'<h2 class="disp h3 br-h" style="--c:{color}"><span class="dot">枝{"一二三四"[b]}</span>{_E(p["branches"][b])}の枝</h2>'
        cards += "".join(_node_card(p, n, color) for n in order if n["branch"] == b)
    cards += f'<h2 class="disp h3 br-h cap" style="--c:{color}"><span class="dot">奥義</span>この道の極み</h2>' + "".join(_node_card(p, n, color) for n in order if n["tier"] == 4)
    nb = HW["paths"]
    prev, nxt = nb[i - 1] if i > 0 else None, nb[i + 1] if i + 1 < len(nb) else None
    pg = lambda x, j, cls, lab: (f'<a href="wiki-{x["id"]}.html" class="pg {cls}" style="--c:{_PCOL[j]}"><small class="dot">{lab}</small><b>{x["name"]}</b><span class="mu">{_E(x["desc"][0])}</span></a>' if x else
                                 f'<a href="wiki-hiuo.html" class="pg {cls}" style="--c:#4FD8C8"><small class="dot">{lab}</small><b>灯魚図鑑</b><span class="mu">106種の灯魚と、かかる条件。</span></a>' if cls == "next" else
                                 f'<a href="wiki.html" class="pg {cls}" style="--c:var(--amber)"><small class="dot">{lab}</small><b>Wiki のはじめ</b><span class="mu">すべての技の一覧と、育て方。</span></a>')
    hero = _wiki_hero(p["name"], _E(p["desc"][0] + p["desc"][1]), color, f'<span aria-hidden="true">›</span><span>{p["name"]}</span>', None, f'PATH {i + 1:02d} ／ 10')
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    {_wiki_side(p["id"])}
    <div class="wk-main">
      <div class="wk-stats" style="--c:{color}">
        <div><b class="dot">13</b><span>技</span></div><div><b class="dot">{acts}</b><span>使う技（発動）</span></div><div><b class="dot">{p["cost"]}</b><span>すべて覚える技点</span></div><div><b class="dot">50</b><span>最大 Lv</span></div>
      </div>
      <h2 class="disp h2 wk-h">技の木</h2>
      <p class="mu wk-p">上から順に開きます。技をおすと、その技の説明へ飛びます。</p>
      {_tree(p, color)}
      <div class="two wk-two">
        <div><h2 class="disp h3">育つこと</h2><div class="tbl-wrap"><table class="xpt"><tbody>{xp}</tbody></table></div>
          <p class="mu wk-small">技がいっしょに壊したブロック（まとめ掘り・一本切り・一斉収穫など）は半分。1日 {_num(HW["dailyXp"])} を超えた分は {int(HW["overflow"] * 100)}%。放置中は育ちません。</p></div>
        <div><h2 class="disp h3">奥義の試練</h2><p class="trial" style="--c:{color}"><b>{_E(p["trial"])}</b><span>奥義を覚えるには、Lv と三の段2つに加えてこの積み重ねが要ります。務めと同じ数え方です。{"灯籠プラグインがないサーバーでは試練なし。" if p["trialTomo"] else ""}</span></p></div>
      </div>
      <h2 class="disp h2 wk-h">技のすべて</h2>
      <div class="ncs">{cards}</div>
      <nav class="pager wk-pager" aria-label="前後の道">{pg(prev, i - 1, "prev", "← 前の道")}{pg(nxt, i + 1, "next", "次の道 →")}</nav>
    </div>
  </div>
</section>
<script src="assets/wiki.js" defer></script>'''


def _curve_svg():
    tot = HW["total"]
    W, H, L, B, T, R = 640, 270, 54, 34, 30, 14
    mx = tot[-1]
    pts = []
    for lv in range(1, 51):
        x = L + (W - L - R) * (lv - 1) / 49
        y = T + (H - T - B) * (1 - tot[lv] / mx)
        pts.append(f"{x:.1f},{y:.1f}")
    grid = ""
    for v in (50000, 100000, 150000, 200000):
        if v > mx:
            continue
        y = T + (H - T - B) * (1 - v / mx)
        grid += f'<line x1="{L}" x2="{W - R}" y1="{y:.1f}" y2="{y:.1f}" class="cg"/><text x="{L - 8}" y="{y + 4:.1f}" class="ct" text-anchor="end">{v // 10000}万</text>'
    marks = ""
    for lv in (10, 20, 30, 40, 50):
        x = L + (W - L - R) * (lv - 1) / 49
        y = T + (H - T - B) * (1 - tot[lv] / mx)
        marks += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="cm"/><text x="{x:.1f}" y="{H - 12}" class="ct" text-anchor="middle">Lv{lv}</text>'
        marks += f'<text x="{x - 6:.1f}" y="{y - 10:.1f}" class="cv" text-anchor="end">{_num(tot[lv])}</text>'
    return f'''<svg class="curve" viewBox="0 0 {W} {H}" role="img" aria-label="Lv ごとの、そこまでに要る経験値の合計。Lv10 で {_num(tot[10])}、Lv40 で {_num(tot[40])}、Lv50 で {_num(tot[50])}。">
      {grid}<line x1="{L}" x2="{W - R}" y1="{H - B}" y2="{H - B}" class="ca"/><polyline points="{" ".join(pts)}" class="cl"/>{marks}</svg>'''


def wiki_index():
    allnodes = [(i, p, n) for i, p in enumerate(HW["paths"]) for n in p["nodes"]]
    cards = ""
    for i, p in enumerate(HW["paths"]):
        mini = ""
        for t in (1, 2, 3):
            for b in range(4):
                n = next(x for x in p["nodes"] if x["branch"] == b and x["tier"] == t)
                mini += f'<i class="k{n["kind"]}"></i>'
        cap = next(x for x in p["nodes"] if x["tier"] == 4)
        cards += f'''<a href="wiki-{p["id"]}.html" class="wpc" style="--c:{_PCOL[i]}">
        <span class="wpc-k">{p["k"]}</span>
        <span class="wpc-b"><b class="disp">{p["name"]}</b><span>{_E(p["desc"][0])}</span><small>奥義「{_E(cap["name"])}」</small></span>
        <span class="wpc-mini" aria-hidden="true">{mini}<i class="cap"></i></span>
      </a>'''
    rows = ""
    for i, p, n in allnodes:
        k = n["kind"]
        tier = "奥義" if n["tier"] == 4 else _TIER[n["tier"]]
        rows += f'''<a href="wiki-{p["id"]}.html#{n["id"]}" class="sk" style="--c:{_PCOL[i]}" data-path="{p["id"]}" data-kind="{k}" data-tier="{n["tier"]}" data-q="{_E(n["name"] + " " + _desc(n) + " " + " ".join(n["effect"]) + " " + p["name"] + " " + n["id"])}">
        <span class="sk-p">{p["k"]}</span><span class="sk-n"><b>{_E(n["name"])}</b><small>{_E(_desc(n))}</small></span><span class="sk-k k{k}">{_KIND[k]}</span><span class="sk-t dot">{tier}</span><span class="sk-l dot">Lv{n["req"][0]}{"〜" + str(n["req"][-1]) if len(n["req"]) > 1 else ""}</span>
      </a>'''
    pchips = "".join(f'<button type="button" class="chip-f" data-f="path" data-v="{p["id"]}" style="--c:{_PCOL[i]}">{p["k"]}</button>' for i, p in enumerate(HW["paths"]))
    kchips = "".join(f'<button type="button" class="chip-f" data-f="kind" data-v="{k}" style="--c:{_KIND_C[k]}">{_KIND[k]}</button>' for k in range(3))
    tchips = "".join(f'<button type="button" class="chip-f" data-f="tier" data-v="{t}" style="--c:var(--amber)">{_TIER[t]}</button>' for t in (1, 2, 3, 4))
    acts = [(i, p, n) for i, p, n in allnodes if n["kind"] == 2]
    arows = "".join(f'<tr><th><a href="wiki-{p["id"]}.html#{n["id"]}" style="color:{_PCOL[i]}">{_E(n["name"])}</a></th><td>{p["name"]}</td><td class="n">{n["gauge"]}</td><td class="n">{" → ".join(_sec(c) for c in n["cooldown"])}</td><td>{_E(n["effect"][-1])}</td></tr>' for i, p, n in acts)
    trows = "".join(f'<tr><th style="color:{_PCOL[i]}">{p["name"]}</th><td>{_E(p["trial"])}</td><td>{_E(next(x for x in p["nodes"] if x["tier"] == 4)["name"])}</td></tr>' for i, p in enumerate(HW["paths"]))
    taskrows = "".join(f'<tr><th style="color:{_PCOL[t["path"]]}">{HW["paths"][t["path"]]["k"]}</th><td>{_E(t["text"])}</td><td class="n">+{t["xp"]}</td></tr>' for t in HW["tasks"])
    tot = HW["total"]
    hero = _wiki_hero("灯技 完全解説", "10の道、130の技、106種の灯魚。プラグインの定義からそのまま作った、灯技のすべてです。数字はゲームと同じです。", "#5AAAFF", "", CH_ICONS["hiwaza"], "HIWAZA WIKI")
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    {_wiki_side("top")}
    <div class="wk-main">
      <div class="wk-stats big">
        <div><b class="dot">10</b><span>道</span></div><div><b class="dot">{len(allnodes)}</b><span>技</span></div><div><b class="dot">{len(acts)}</b><span>使う技（発動）</span></div><div><b class="dot">{len(HW["fish"])}</b><span>灯魚</span></div><div><b class="dot">{len(HW["tasks"])}</b><span>務め</span></div>
      </div>

      <h2 class="disp h2 wk-h" id="paths">10の道</h2>
      <div class="wpcs">{cards}</div>

      <a href="wiki-build.html" class="wiki-band cmd-band" style="margin-top:28px"><span class="wb-k dot">BUILD</span><span class="wb-b"><b class="disp">技の組み立て</b><span>道の Lv を決めて技を選ぶと、技点と条件をその場で計算。組み立てはリンクで共有できます。</span></span><span class="wb-go">組み立てる<i></i></span></a>

      <h2 class="disp h2 wk-h" id="all">すべての技を探す</h2>
      <div class="finder">
        <label class="find"><span class="sr">技を探す</span><input type="search" id="wq" placeholder="名前・効き目で探す（例：まとめ、灯力、落下）" autocomplete="off"><kbd class="dot">/</kbd></label>
        <div class="filters"><div class="fg"><span class="fl-l">道</span>{pchips}</div><div class="fg"><span class="fl-l">種類</span>{kchips}</div><div class="fg"><span class="fl-l">段</span>{tchips}</div></div>
        <p class="find-n mu" aria-live="polite"><b class="dot" id="wn">{len(allnodes)}</b> の技 <button type="button" class="clear" id="wclear" hidden>しぼりこみを消す</button></p>
        <div class="sks" id="wl">{rows}</div>
        <p class="wk-empty" id="wempty" hidden>見つかりませんでした。ことばを短くしてみてください。</p>
      </div>

      <h2 class="disp h2 wk-h" id="grow">育て方</h2>
      <div class="grow2">
        <div><h3 class="disp h3">Lv と経験値</h3><p class="mu">Lv が1上がるごとに、その道の技点が1。Lv50 で、その道の技はすべて覚えられます（余る道もあります）。Lv50 の先は「極み」の★（{_num(HW["starNeed"])} ごとに1つ、★{HW["maxStar"]} まで）。</p>{_curve_svg()}
          <div class="lvsteps">{"".join(f'<div><small>Lv{l} まで</small><b>{_num(tot[l])}</b></div>' for l in (10, 20, 40, 50))}</div></div>
        <div><h3 class="disp h3" id="daily">今日の伸び</h3>
          <div class="gtiles">
            <div class="gt wide"><b>{_num(HW["dailyXp"])}<small>／日・道ごと</small></b><strong>ふつうに育つ量</strong><span>道ごとに数えます。掘る日と釣る日を分けても、損はありません。</span></div>
            <div class="gt" style="--c:#E0453A"><b>{int(HW["overflow"] * 100)}<small>%</small></b><strong>超えた分</strong><span>伸びを使い切ったあとも、少しは育ちます。</span></div>
            <div class="gt" style="--c:#6FD39A"><b>{HW["bankDays"]}<small>日ぶん</small></b><strong>貯まる</strong><span>遊べなかった日の伸びは、あとで使えます。</span></div>
            <div class="gt" style="--c:#9AA3B5"><b>{int(HW["chainXp"] * 100)}<small>%</small></b><strong>技がいっしょに壊した分</strong><span>まとめ掘り・一本切りなど。</span></div>
            <div class="gt" style="--c:#5AAAFF"><b>別<small>勘定</small></b><strong>務めのごほうび</strong><span>今日の伸びを使いません。</span></div>
          </div>
          <p class="mu wk-small">放置（視点が5分動かない）中、クリエイティブ、自分で置いたブロック、石の製造機では育ちません。</p></div>
      </div>

      <h2 class="disp h2 wk-h" id="trials">奥義の試練</h2>
      <div class="tbl-wrap"><table><thead><tr><th>道</th><th>試練</th><th>奥義</th></tr></thead><tbody>{trows}</tbody></table></div>

      <h2 class="disp h2 wk-h" id="actives">使う技（発動）の一覧</h2>
      <p class="mu wk-p">主技は <b>しゃがみ2回</b>、副技は <b>しゃがんで F</b>。<span class="kbd">/waza use</span> で一覧から使うこともできます。灯力は灯籠の灯りの中でたまります。</p>
      <div class="tbl-wrap"><table><thead><tr><th>技</th><th>道</th><th>灯力</th><th>待ち時間（段ごと）</th><th>いちばん上の段</th></tr></thead><tbody>{arows}</tbody></table></div>

      <h2 class="disp h2 wk-h" id="tasks">今日の務め（{len(HW["tasks"])}種から毎日3つ）</h2>
      <div class="tbl-wrap"><table><thead><tr><th>道</th><th>務め</th><th>経験値</th></tr></thead><tbody>{taskrows}</tbody></table></div>
      <p class="mu wk-small">果たすと経験値と灯力 +20。3つすべて果たすと加護の欠片。毎日0時（日本時間）に入れ替わります。</p>
    </div>
  </div>
</section>
<script src="assets/wiki.js" defer></script>'''


def wiki_fish():
    groups = HW["groups"]
    rar = HW["rarity"]
    rc = ["", "#E9EEF6", "#55FF55", "#55FFFF", "#FF55FF", "#FFAA00"]
    cards = ""
    for f in HW["fish"]:
        r = f["rarity"]
        secret = f["name"] is None
        cond = "・".join(f["cond"]) if f["cond"] else ("手がかりなし" if secret else "どこでも")
        name = "？？？" if secret else _E(f["name"])
        cards += f'''<li class="fc{" secret" if secret else ""}"{"" if secret else f' id="f-{f["id"]}"'} style="--c:{rc[r]}" data-g="{f["group"]}" data-r="{r}">
        <span class="fc-r dot">{"◆" * r}<s>{"◇" * (5 - r)}</s> {rar[r]}</span>
        <b class="fc-n">{name}</b>
        <span class="fc-g">{_E(groups[f["group"]])}</span>
        <p class="fc-c"><span>手がかり</span>{_E(cond)}</p>
        {"" if secret else f'<p class="fc-f mu">{_E(f["flavor"])}</p>'}
        <p class="fc-s dot">{("？" if secret else f'{f["min"]:g}〜{f["max"]:g}cm')}</p>
      </li>'''
    gchips = "".join(f'<button type="button" class="chip-f" data-f="g" data-v="{i}" style="--c:#4FD8C8">{_E(g)}</button>' for i, g in enumerate(groups))
    rchips = "".join(f'<button type="button" class="chip-f" data-f="r" data-v="{i}" style="--c:{rc[i]}">{rar[i]}</button>' for i in range(1, 6))
    counts = " ・ ".join(f'{rar[i]} {sum(1 for f in HW["fish"] if f["rarity"] == i)}' for i in range(1, 6))
    hero = _wiki_hero("灯魚図鑑", f"全{len(HW['fish'])}種（{counts}）。手がかりはゲームの図鑑と同じだけ載せています。珍しい魚ほど、自分で見つけてください。", "#4FD8C8",
                      '<span aria-hidden="true">›</span><span>灯魚図鑑</span>', CH_ICONS["fish"], "HIUO")
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    {_wiki_side("hiuo")}
    <div class="wk-main">
      <div class="finder fishf">
        <div class="filters"><div class="fg"><span class="fl-l">水辺</span>{gchips}</div><div class="fg"><span class="fl-l">珍しさ</span>{rchips}</div></div>
        <p class="find-n mu" aria-live="polite"><b class="dot" id="fn">{len(HW["fish"])}</b> 種 <button type="button" class="clear" id="fclear" hidden>しぼりこみを消す</button></p>
        <ul class="fcs" id="fl">{cards}</ul>
      </div>
      <h2 class="sr">灯魚のしくみ</h2>
      <div class="three">
        <div><h3 class="h3 disp">逃げる確率</h3><p class="mu">並 0% ・ 珍 {int(HW["escape"][2] * 100)}% ・ 稀 {int(HW["escape"][3] * 100)}% ・ 秘 {int(HW["escape"][4] * 100)}% ・ 幻 {int(HW["escape"][5] * 100)}%。釣の道「糸さばき」で、段ごとに2割ずつ下がります。逃げられた魚は、図鑑に姿と手がかりが残ります。</p></div>
        <div><h3 class="h3 disp">釣れる見込み</h3><p class="mu">釣りをしたとき、灯魚がかかるかどうかは「灯釣り」・夜・灯りの中で上がります。釣の道「魚読み」を覚えると、その場で釣れる灯魚の数がわかります。</p></div>
        <div><h3 class="h3 disp">季節は現実の暦</h3><p class="mu">春は3〜5月、夏は6〜8月、秋は9〜11月、冬は12〜2月（日本時間）。月の満ち欠けは、ゲームの中の月です。</p></div>
      </div>
    </div>
  </div>
</section>
<script src="assets/wiki.js" defer></script>'''


WIKI_PAGES = [("wiki.html", "灯技 完全解説｜灯原", "灯技（ひわざ）のすべて。10の道・130の技の効き目と要るLv・技点・灯力・待ち時間、奥義の試練、今日の務め、灯魚図鑑。", wiki_index())]
WIKI_PAGES += [(f"wiki-{p['id']}.html", f"{p['name']}｜灯技 Wiki｜灯原", f"{p['name']}の13の技（{'・'.join(n['name'] for n in p['nodes'][:5])}…）の効き目、要るLv・技点、技の木、育つこと、奥義の試練。", wiki_path(i))
               for i, p in enumerate(HW["paths"])]
WIKI_PAGES += [("wiki-hiuo.html", "灯魚図鑑｜灯技 Wiki｜灯原", f"灯魚（ひうお）{len(HW['fish'])}種の珍しさ・大きさ・水辺・手がかり。", wiki_fish())]


# ───────────────────────── 灯の証 Wiki ─────────────────────────
AK = _wj.loads((pathlib.Path(__file__).parent / "data" / "akashi.json").read_text(encoding="utf-8"))
_MC = {"0": "#3A3F55", "1": "#5A5AFF", "2": "#3CC83C", "3": "#3CC8C8", "4": "#E04848", "5": "#C77DFF", "6": "#FFAA00", "7": "#AAB0BD", "8": "#7A8295", "9": "#7C7CFF",
       "a": "#55FF55", "b": "#55FFFF", "c": "#FF5555", "d": "#FF55FF", "e": "#FFFF55", "f": "#FFFFFF"}
_AK_SLUG = ["light", "night", "hunt", "travel", "craft", "life", "fest", "secret"]
_AK_COL = [_MC[c["mc"][0]] for c in AK["cats"]]
_TCOL = ["", "#55FF55", "#55FFFF", "#FF55FF", "#FFAA00", "#FF5555"]
_TNAME = ["", "易", "並", "難", "極", "伝"]
_TFEEL = ["", "すぐ届く", "少し続ければ", "腰を据えて", "何週間も", "季節をまたいで"]
_AK_ICON = {0: CH_ICONS["lantern"], 1: CH_ICONS["night"], 2: CH_ICONS["higui"], 3: CH_ICONS["more"], 4: CH_ICONS["hiwaza"], 5: CH_ICONS["buff"], 6: ICONS["events.html"], 7: CH_ICONS["akashi"]}


def _dia(t):
    return f'<span class="dia" style="--t:{_TCOL[t]}" aria-label="難度 {_TNAME[t]}">{"◆" * t}<s>{"◇" * (5 - t)}</s></span>'


def _ak_medal(t, hidden=False):
    c = "#5A6070" if hidden else _TCOL[t]
    return pix(CH_ICONS["akashi"], "md").replace('<svg class="md"', f'<svg class="md" style="--t:{c}"')


def _rewards(x, full=True):
    t = AK["tiers"][x["tier"] - 1]
    out = []
    if full:
        out.append(f'<li class="rw-p"><b class="dot">+{t["points"]}</b>証点</li>')
        out.append(f'<li class="rw-x"><b class="dot">+{t["xp"]}</b>経験値</li>')
        if t["frag"]:
            out.append(f'<li class="rw-f"><b class="dot">×{t["frag"]}</b>加護の欠片</li>')
    if x.get("title"):
        out.append(f'<li class="rw-t">称号<b>{_E(x["title"])}</b></li>')
    if x.get("tint"):
        r, g, b = x["tint"]["rgb"]
        out.append(f'<li class="rw-c" style="--rgb:rgb({r},{g},{b})">灯りの色<b>{_E(x["tint"]["name"])}</b></li>')
    if x.get("trail"):
        out.append(f'<li class="rw-s">足跡<b>{_E(x["trail"])}</b></li>')
    if x.get("item"):
        out.append(f'<li class="rw-i">品物<b>{_E(x["item"])}</b></li>')
    return "".join(out)


def _rw_keys(x):
    return " ".join(k for k in ("title", "tint", "trail", "item") if x.get(k))


def _ak_defs(c):
    return [x for x in AK["defs"] if x["cat"] == c]


def _ak_series(c):
    """段でつながった証をひとまとめにする（[最初の段, …]）。ひとつきりのものは長さ1。"""
    ds = _ak_defs(c)
    byid = {x["id"]: x for x in ds if x["id"]}
    nxt = {x["prev"]: x for x in ds if x.get("prev")}
    out = []
    for x in ds:
        if x["hidden"] or x.get("prev"):
            continue
        chain = [x]
        while chain[-1]["id"] in nxt:
            chain.append(nxt[chain[-1]["id"]])
        out.append(chain)
    return out


def _ak_hid_ix(c):
    return [i for i, x in enumerate(_ak_defs(c)) if x["hidden"]]


def _ak_side(cur):
    items = f'<a href="akashi.html"{" aria-current=\"page\"" if cur == "top" else ""}><span class="ws-k" style="--c:var(--pink)">≡</span>証 Wiki のはじめ</a>'
    for i, c in enumerate(AK["cats"]):
        items += f'<a href="akashi-{_AK_SLUG[i]}.html" style="--c:{_AK_COL[i]}"{" aria-current=\"page\"" if cur == i else ""}><span class="ws-k">{c["k"]}</span>{c["name"]}<small class="dot">{len(_ak_defs(i))}</small></a>'
    items += _wiki_others("akashi")
    return f'<nav class="wside" aria-label="証 Wiki の目次"><p class="dot wside-h">灯の証 Wiki</p>{items}</nav>'


def _ak_hero(title, lead, color, crumb, icon_rows, sub):
    ic = pix(icon_rows, "ch-ic big") if icon_rows else ""
    return f'''<div class="hero ch-hero wk-hero" style="--c:{color}">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    {_wiki_switch("akashi")}
    {_wiki_crumb("akashi", crumb)}
    <div class="ch-head">{ic}<div><p class="ch-big dot">{sub}</p><h1 class="disp h1-sub">{title}</h1></div></div>
    <p class="lead">{lead}</p>
  </div>
</div>'''


def _ak_card(x, c):
    """証の札（章のページ）。"""
    if x["hidden"]:
        n = _ak_hid_ix(c).index(_ak_defs(c).index(x)) + 1
        return f'''<article class="ac hid" id="h{n}" style="--t:#5A6070">
      <div class="ac-m">{_ak_medal(x["tier"], True)}</div>
      <div class="ac-b"><header><h3 class="disp">？？？</h3>{_dia(x["tier"])}</header>
      <p class="ac-hint">「{_E(x["hint"])}」</p>
      <p class="ac-foot mu"><span>秘められた証</span><span>得ると、名前と条件が明かされます</span></p></div>
    </article>'''
    stage = f'<span class="ac-st dot">第{x["stage"]}段 / 全{x["stages"]}段</span>' if x["stages"] > 1 else ""
    prev = next((y for y in _ak_defs(c) if y["id"] == x["prev"]), None) if x.get("prev") else None
    need = f'<p class="ac-need"><span>現れる条件</span>前の段「<a href="#{prev["id"]}">{_E(prev["name"])}</a>」を得る</p>' if prev else ""
    return f'''<article class="ac" id="{x["id"]}" style="--t:{_TCOL[x["tier"]]}">
      <div class="ac-m">{_ak_medal(x["tier"])}</div>
      <div class="ac-b"><header><h3 class="disp">{_E(x["name"])}</h3>{_dia(x["tier"])}{stage}</header>
      <p class="ac-d">{"<br>".join(_E(s) for s in x["desc"])}</p>
      <p class="ac-goal"><span>目標</span><b class="dot">{_E(x["goal"])}</b></p>
      <ul class="rw">{_rewards(x)}</ul>
      {need}</div>
    </article>'''


def _ak_track(chain, c):
    nodes = ""
    for x in chain:
        nodes += f'''<a href="#{x["id"]}" class="tk-n" style="--t:{_TCOL[x["tier"]]}"><i class="tk-l"></i><b>{_E(x["name"])}</b><span class="dot">{_E(x["goal"])}</span>{"<em>" + ("称号" if x.get("title") else "色" if x.get("tint") else "足跡" if x.get("trail") else "品物") + "</em>" if _rw_keys(x) else ""}</a>'''
    head = chain[0]["desc"][0]
    return f'<div class="tk" style="--n:{len(chain)}"><p class="tk-h"><span class="dot">{len(chain)}段</span>{_E(head)}</p><div class="tk-r">{nodes}</div></div>'


def akashi_cat(c):
    cat = AK["cats"][c]
    color = _AK_COL[c]
    ds = _ak_defs(c)
    series = _ak_series(c)
    chains = [s for s in series if len(s) > 1]
    singles = [s[0] for s in series if len(s) == 1]
    hid = [x for x in ds if x["hidden"]]
    pts = sum(AK["tiers"][x["tier"] - 1]["points"] for x in ds)
    tracks = "".join(_ak_track(s, c) for s in chains)
    order = [x for s in chains for x in s] + singles
    cards = "".join(_ak_card(x, c) for x in order)
    hcards = "".join(_ak_card(x, c) for x in hid)
    tiers = [sum(1 for x in ds if x["tier"] == t) for t in range(1, 6)]
    tbar = "".join(f'<i style="--t:{_TCOL[t + 1]};flex:{n}" title="{_TNAME[t + 1]} {n}"></i>' for t, n in enumerate(tiers) if n)
    prv, nx = (c - 1, c + 1)
    pg = lambda j, cls, lab: (f'<a href="akashi-{_AK_SLUG[j]}.html" class="pg {cls}" style="--c:{_AK_COL[j]}"><small class="dot">{lab}</small><b>{AK["cats"][j]["name"]}</b><span class="mu">{_E(AK["cats"][j]["desc"][0])}</span></a>' if 0 <= j < 8 else
                              f'<a href="akashi.html" class="pg {cls}" style="--c:var(--pink)"><small class="dot">{lab}</small><b>証 Wiki のはじめ</b><span class="mu">すべての証の一覧と、位階・報酬。</span></a>')
    hero = _ak_hero(cat["name"], _E(cat["desc"][0] + cat["desc"][1]), color, f'<span aria-hidden="true">›</span><span>{cat["name"]}</span>', _AK_ICON[c], f'CHAPTER {c + 1:02d} ／ 08')
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    {_ak_side(c)}
    <div class="wk-main">
      <div class="wk-stats" style="--c:{color}">
        <div><b class="dot">{len(ds)}</b><span>証</span></div><div><b class="dot">{len(chains)}</b><span>段の道</span></div><div><b class="dot">{_num(pts)}</b><span>章の証点</span></div><div><b class="dot">{len(hid)}</b><span>秘められた証</span></div>
      </div>
      <div class="tbar" aria-label="難度の内わけ">{tbar}</div>
      <p class="tlg mu">{"".join(f'<span style="--t:{_TCOL[t + 1]}">{_TNAME[t + 1]} {n}</span>' for t, n in enumerate(tiers))}</p>
      {f'<h2 class="disp h2 wk-h">段の道</h2><p class="mu wk-p">同じ記録の証は段になっていて、前の段を得ると次の段が現れます。押すと、その証の札へ。</p><div class="tks">{tracks}</div>' if chains else ""}
      <h2 class="disp h2 wk-h">証のすべて</h2>
      <div class="acs">{cards}</div>
      {f'<h2 class="disp h2 wk-h">秘められた証</h2><p class="mu wk-p">名前も条件も伏せられた証。手がかりはひとことだけ。得ると、ゲームの中で明かされます。</p><div class="acs">{hcards}</div>' if hid else ""}
      <nav class="pager wk-pager" aria-label="前後の章">{pg(prv, "prev", "← 前の章")}{pg(nx, "next", "次の章 →")}</nav>
    </div>
  </div>
</section>
<script src="assets/wiki.js" defer></script>'''


def akashi_index():
    ds = AK["defs"]
    cards = ""
    for i, c in enumerate(AK["cats"]):
        d = _ak_defs(i)
        tiers = [sum(1 for x in d if x["tier"] == t) for t in range(1, 6)]
        tb = "".join(f'<i style="--t:{_TCOL[t + 1]};flex:{n}"></i>' for t, n in enumerate(tiers) if n)
        cards += f'''<a href="akashi-{_AK_SLUG[i]}.html" class="akc" style="--c:{_AK_COL[i]}">
        <span class="akc-k">{c["k"]}</span>
        <span class="akc-b"><b class="disp">{c["name"]}</b><span>{_E(c["desc"][0])}</span></span>
        <span class="akc-n dot">{len(d)}</span>
        <span class="tbar sm" aria-hidden="true">{tb}</span>
      </a>'''
    rows = ""
    hidn = {i: 0 for i in range(8)}
    for x in ds:
        c = x["cat"]
        if x["hidden"]:
            hidn[c] += 1
            href = f'akashi-{_AK_SLUG[c]}.html#h{hidn[c]}'
            q = f'秘 ？？？ {x["hint"]} {AK["cats"][c]["name"]}'
            nm, sm = "？？？", "「" + _E(x["hint"]) + "」"
        else:
            href = f'akashi-{_AK_SLUG[c]}.html#{x["id"]}'
            q = " ".join(filter(None, [x["name"], " ".join(x["desc"]), x["goal"], x.get("title"), (x.get("tint") or {}).get("name"), x.get("trail"), x.get("item"), AK["cats"][c]["name"]]))
            nm, sm = _E(x["name"]), _E(x["desc"][0])
        marks = "".join(f'<i class="m-{k}" title="{t}">{t[0]}</i>' for k, t in (("title", "称号"), ("tint", "色"), ("trail", "足跡"), ("item", "品物")) if x.get(k))
        rows += f'''<a href="{href}" class="ak{" hid" if x["hidden"] else ""}" style="--c:{_AK_COL[c]};--t:{_TCOL[x["tier"]]}" data-cat="{c}" data-tier="{x["tier"]}" data-rw="{_rw_keys(x) or "none"}" data-q="{_E(q)}">
        <span class="sk-p">{AK["cats"][c]["k"]}</span><span class="sk-n"><b>{nm}</b><small>{sm}</small></span><span class="ak-r">{marks}</span>{_dia(x["tier"])}<span class="sk-l dot">{_E(x["goal"] or "—")}</span>
      </a>'''
    cchips = "".join(f'<button type="button" class="chip-f" data-f="cat" data-v="{i}" style="--c:{_AK_COL[i]}">{c["k"]}</button>' for i, c in enumerate(AK["cats"]))
    tchips = "".join(f'<button type="button" class="chip-f" data-f="tier" data-v="{t}" style="--c:{_TCOL[t]}">{_TNAME[t]}</button>' for t in range(1, 6))
    rchips = "".join(f'<button type="button" class="chip-f" data-f="rw" data-v="{k}" style="--c:var(--amber)">{t}</button>' for k, t in (("title", "称号"), ("tint", "灯りの色"), ("trail", "足跡"), ("item", "品物")))
    tiles = ""
    for t in range(1, 6):
        ti = AK["tiers"][t - 1]
        n = sum(1 for x in ds if x["tier"] == t)
        tiles += f'''<div class="tt" style="--t:{_TCOL[t]}"><p>{_dia(t)}</p><b class="disp">{_TNAME[t]}</b><span class="tt-f">{_TFEEL[t]}</span>
          <dl><div><dt>証点</dt><dd class="dot">{ti["points"]}</dd></div><div><dt>経験値</dt><dd class="dot">{ti["xp"]}</dd></div><div><dt>欠片</dt><dd class="dot">{ti["frag"] or "—"}</dd></div></dl><span class="tt-n dot">{n} 個</span></div>'''
    mx = AK["ranks"][-1]["need"]
    ladder = ""
    for i, r in enumerate(AK["ranks"]):
        rc = _MC[r["mc"][0]]
        rw = []
        if i > 0:
            rw.append(f'称号「{_E(r["name"])}」')
        if r.get("trail"):
            rw.append(f'足跡「{_E(r["trail"])}」')
        if r.get("tint"):
            rw.append(f'灯りの色「{_E(r["tint"]["name"])}」')
        ladder += f'''<li style="--r:{rc};--w:{max(1.2, r["need"] / mx * 100):.1f}%"><span class="rk-i dot">{i + 1:02d}</span><b class="disp">{_E(r["name"])}</b><span class="rk-b"><i></i></span><span class="rk-n dot">{_num(r["need"])}</span><span class="rk-w">{" ・ ".join(rw) or "はじまりの位"}</span></li>'''
    titles = "".join(f'<li{" class=hid" if t["id"] is None else ""}><b>{_E(t["t"]) if t["t"] else "？？？"}</b><span>{_E(t["how"])}</span></li>' for t in AK["titles"])
    trails = "".join(f'<li><b>{_E(t["name"])}</b><span>{_E(t["how"])}</span></li>' for t in AK["trails"])
    tints = [(x["tint"]["name"], x["tint"]["rgb"], x["name"]) for x in ds if x.get("tint")] + [(r["tint"]["name"], r["tint"]["rgb"], "位階「" + r["name"] + "」") for r in AK["ranks"] if r.get("tint")]
    tintl = "".join(f'<li style="--rgb:rgb({c[0]},{c[1]},{c[2]})"><i></i><b>{_E(n)}</b><span>{_E(h)}</span></li>' for n, c, h in tints)
    hero = _ak_hero("灯の証 完全解説", f"灯原だけの進捗、{len(ds)}の証。8つの章・5つの難度・10の位階と、称号・灯りの色・足跡の手に入れ方。プラグインの定義からそのまま作りました。", "#F29BB8", "", CH_ICONS["akashi"], "AKASHI WIKI")
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    {_ak_side("top")}
    <div class="wk-main">
      <div class="wk-stats big" style="--c:var(--pink)">
        <div><b class="dot">{len(ds)}</b><span>証</span></div><div><b class="dot">8</b><span>章</span></div><div><b class="dot">{_num(AK["total"])}</b><span>証点の合計</span></div><div><b class="dot">{len(AK["ranks"])}</b><span>位階</span></div><div><b class="dot">{len(AK["titles"])}</b><span>称号</span></div><div><b class="dot">{len(AK["trails"])}</b><span>足跡</span></div>
      </div>

      <h2 class="disp h2 wk-h" id="cats">8つの章</h2>
      <div class="akcs">{cards}</div>

      <h2 class="disp h2 wk-h" id="all">すべての証を探す</h2>
      <div class="finder">
        <label class="find"><span class="sr">証を探す</span><input type="search" id="aq" placeholder="名前・条件・報酬で探す（例：灯籠、朱月、称号）" autocomplete="off"><kbd class="dot">/</kbd></label>
        <div class="filters"><div class="fg"><span class="fl-l">章</span>{cchips}</div><div class="fg"><span class="fl-l">難度</span>{tchips}</div><div class="fg"><span class="fl-l">報酬</span>{rchips}</div></div>
        <p class="find-n mu" aria-live="polite"><b class="dot" id="an">{len(ds)}</b> の証 <button type="button" class="clear" id="aclear" hidden>しぼりこみを消す</button></p>
        <div class="sks aks" id="al">{rows}</div>
        <p class="wk-empty" id="aempty" hidden>見つかりませんでした。ことばを短くしてみてください。</p>
      </div>

      <h2 class="disp h2 wk-h" id="tiers">5つの難度</h2>
      <p class="mu wk-p">報酬の証点・経験値・加護の欠片は難度で決まります。称号・灯りの色・足跡・品物は、証ごとに追加でつきます。</p>
      <div class="tts">{tiles}</div>

      <h2 class="disp h2 wk-h" id="ranks">10の位階</h2>
      <p class="mu wk-p">証点がたまると位階が上がります。バーは、いちばん上の位階までの道のり。</p>
      <ol class="rks">{ladder}</ol>

      <h2 class="disp h2 wk-h" id="rewards">見た目の報酬</h2>
      <div class="rwg">
        <div><h3 class="disp h3">灯りの色 <small class="dot">{len(tints)}</small></h3><ul class="tintl">{tintl}</ul>
             <h3 class="disp h3" style="margin-top:28px">足跡 <small class="dot">{len(AK["trails"])}</small></h3><ul class="nml">{trails}</ul></div>
        <div><h3 class="disp h3">称号 <small class="dot">{len(AK["titles"])}</small></h3><ul class="nml ttl">{titles}</ul></div>
      </div>
      <p class="mu wk-small">報酬はすべて、見た目か少しの手助けだけ。強さの差は開きません。秘められた証の報酬は伏せてあります。</p>
      <nav class="pager wk-pager" aria-label="ほかの Wiki">{f'<a href="akashi-light.html" class="pg next" style="--c:{_AK_COL[0]}"><small class="dot">はじめの章 →</small><b>灯の章</b><span class="mu">{_E(AK["cats"][0]["desc"][0])}</span></a>'}<a href="wiki.html" class="pg prev" style="--c:#5AAAFF"><small class="dot">← もうひとつの Wiki</small><b>灯技 Wiki</b><span class="mu">10の道・130の技と、灯魚図鑑。</span></a></nav>
    </div>
  </div>
</section>
<script src="assets/wiki.js" defer></script>'''


AK_PAGES = [("akashi.html", "灯の証 完全解説｜灯原", f"灯の証（あかし）{len(AK['defs'])}個のすべて。8つの章、難度と報酬（証点・経験値・欠片・称号・灯りの色・足跡）、段の道、10の位階。秘められた証は手がかりだけ。", akashi_index())]
AK_PAGES += [(f"akashi-{_AK_SLUG[i]}.html", f"{c['name']}｜灯の証 Wiki｜灯原", f"{c['name']}の{len(_ak_defs(i))}の証。{c['desc'][0]}段の道、目標、報酬、秘められた証の手がかり。", akashi_cat(i)) for i, c in enumerate(AK["cats"])]


# ───────────────────────── 灯紋 ─────────────────────────
# data/himon.json（プラグインの定義から書き出したもの）から作る。
HM = _wj.loads((pathlib.Path(__file__).parent / "data" / "himon.json").read_text(encoding="utf-8"))
HM_ICON = CH_ICONS["himon"]
_HM_G = [("w", "武器", {"SWORD", "AXE", "MACE"}), ("b", "弓・クロスボウ", {"BOW", "XBOW"}), ("t", "三叉槍", {"TRIDENT"}), ("s", "盾", {"SHIELD"}),
         ("a", "防具", {"HEAD", "CHEST", "LEGS", "FEET"}), ("e", "エリトラ", {"ELYTRA"}), ("g", "掘る・切る", {"PICK", "SHOVEL", "AXE"}), ("r", "釣り竿", {"ROD"})]
_re_n = _re.compile(r"(\d+(?:\.\d+)?)")


def _hm_desc(ds):
    """Lv ごとの説明を1行に。数字だけがちがうなら「10／20／30」とまとめる。"""
    if len(ds) == 1:
        return _E(ds[0])
    parts = [_re_n.split(d) for d in ds]
    if any(len(p) != len(parts[0]) for p in parts) or any(p[i] != parts[0][i] for p in parts for i in range(0, len(p), 2)):
        return "<br>".join(f"Lv{i + 1}：{_E(d)}" for i, d in enumerate(ds))
    out = ""
    for i, seg in enumerate(parts[0]):
        if i % 2 == 0:
            out += _E(seg)
        else:
            vals = [p[i] for p in parts]
            out += vals[0] if len(set(vals)) == 1 else '<b class="hm-v">' + "／".join(vals) + "</b>"
    return out


def _hm_tiers():
    R = HM["rarity"]
    M = HM["mumei"]
    up = int(round(HM["upgrade"] * 100))
    out = ""
    shelf = [r for r in R if r["shelf"]]
    for i, r in enumerate(shelf):
        nxt = f'{up}%で「{shelf[i + 1]["jp"]}」が出る' if i + 1 < len(shelf) else "秘へは上がらない"
        out += f'''<div class="hm-tier" style="--c:{r["hex"]}"><span class="hm-r disp">{r["jp"]}</span><b class="dot">{r["book"]}<small>Lv</small></b><span>＋ 灯札 {r["fuda"]} 枚</span><ul><li><b class="dot">{r["n"]}</b> 種</li><li>刻むとき <b class="dot">{r["engrave"]}</b> Lv</li><li>{nxt}</li></ul></div>'''
    tot = sum(M["weight"])
    hi = R[-1]
    odds = "・".join(f'{x["jp"]} {round(w / tot * 100)}%' for x, w in zip(R, M["weight"]))
    out += f'''<div class="hm-tier mumei" style="--c:{hi["hex"]}"><span class="hm-r disp">無銘</span><b class="dot">{M["lv"]}<small>Lv</small></b><span>＋ 灯札 {M["fuda"]} 枚</span><ul><li>すべての段から出る</li><li><b class="dot">秘 {M["weight"][-1]}%</b>（{hi["n"]}種）</li><li>{M["pity"]}冊で必ず秘</li></ul></div>'''
    return f'<div class="hm-tiers">{out}</div><p class="mu hm-odds">無銘の紋書の出かた：{odds}。秘が出ないまま {M["pity"]} 冊引くと、次の1冊は必ず秘になります。</p>'


def _hm_fuda():
    M = HM["mumei"]
    return f'''<div class="three hm-rules">
        <div><h3 class="h3 disp">灯札は、遊んだ時間でたまる</h3><p class="mu">紋書を引くには、経験値に加えて「灯札」が要ります。動いて遊んだ {HM["fudaMin"]} 分で1枚、{HM["fudaMax"]} 枚まで持てます。はじめて来たときに {HM["fudaStart"]} 枚もらえます。</p></div>
        <div><h3 class="h3 disp">放置ではたまらない</h3><p class="mu">数えるのは、視点が動き、そのうえで歩くか、ブロックを掘る・置くかした1分だけ。経験値トラップの前で立っているだけ、乗り物や水流で運ばれているだけでは、たまりません。</p></div>
        <div><h3 class="h3 disp">秘は、無銘の紋書からだけ</h3><p class="mu">段の紋書から秘は出ません。無銘の紋書を引いて、5%を引き当てるか、{M["pity"]} 冊目の天井まで。秘を引き当てると、サーバーのみんなに知らされます。</p></div>
      </div>'''


def _hm_rules():
    return f'''<ol class="hm-steps">
        <li><b>「刻む」を開く</b><span>画面の「刻む」か <span class="kbd">/himon engrave</span>。</span></li>
        <li><b>道具と紋書を置く</b><span>持ち物をクリックすると、道具と紋書がそれぞれの場所に入ります。刻めるかどうかは、その場で表示。</span></li>
        <li><b>刻む</b><span>段に応じた経験値（{HM["rarity"][0]["engrave"]}〜{HM["rarity"][-1]["engrave"]} Lv）を払います。重ねて Lv2 にするときは1.5倍、Lv3 は2倍。紋書はなくなります。</span></li>
      </ol>
      <div class="three hm-rules">
        <div><h3 class="h3 disp">重ねて強く</h3><p class="mu">同じ紋を同じ Lv で重ねると、1つ上がります（Lv1＋Lv1 → Lv2）。Lv がちがうときは、高い方が残ります。</p></div>
        <div><h3 class="h3 disp">1つの道具に{HM["slots"]}つまで</h3><p class="mu">秘の紋は1つだけ。閃光と陣立て、不屈と不死鳥は、同じ道具に刻めません。ふつうの付呪とはいっしょに使えます。</p></div>
        <div><h3 class="h3 disp">外すこともできる</h3><p class="mu">刻む画面で、紋をしゃがみクリック。段に応じた経験値（2〜9 Lv）で外せます（紋書は戻りません）。</p></div>
      </div>'''


# 遊び方の章で見せる、場面ごとのおすすめ
_HM_PICKS = [("暮らし", "#8BD18F", ["yorite", "suiyose", "miteate", "sunanuki", "itabiki"]),
             ("戦い", "#E0453A", ["kaishaku", "kamaitachi", "fuiuchi", "ikkitousen", "yaame"]),
             ("移動", "#8FC3E8", ["nidantobi", "kamikaze", "kaginawa", "hanegasa", "koorizuri"]),
             ("守り", "#F2B544", ["hokora", "kizuna", "makimodoshi", "tetsuheki", "inugami"])]


def _himon_sec():
    by = {d["id"]: d for d in HM["defs"]}
    R = HM["rarity"]
    picks = ""
    for t, col, ids in _HM_PICKS:
        lis = "".join(f'<li><a href="himon.html#m-{i}"><span class="hm-r disp" style="--c:{R[by[i]["r"]]["hex"]}">{R[by[i]["r"]]["jp"]}</span><span><b>{_E(by[i]["name"])}</b><small>{_E(by[i]["desc"][-1])}</small></span></a></li>' for i in ids)
        picks += f'<div class="hm-pick" style="--c:{col}"><h3 class="h3 disp">{t}</h3><ul>{lis}</ul></div>'
    n = len(HM["defs"])
    return f'''<section class="stratum s-deep" id="himon">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">経験値で引いて、道具に刻む。</h2>
    <p class="lead"><span class="kbd">/himon</span> で開きます。経験値と「灯札」を払って紋書を引き、道具や防具に刻むと、ふつうの付呪にはない力が宿ります。全部で{n}種。ふつうの付呪とも、灯技とも重なりません。</p>
    {_hm_tiers()}
    {_hm_fuda()}
    <p class="mu" style="font-size:14px;margin-top:20px">どの紋が出るかは、段の中でくじ引きです。最大 Lv2 の紋は 85% で Lv1、最大 Lv3 の紋は 75%・20%・5%。見つけた紋は <span class="kbd">/himon book</span> の紋帳に残ります。紋書は渡したり交換したりできます。</p>
  </div>
</section>

<section class="stratum s-dusk" id="engrave">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">刻む・重ねる・外す。</h2>
    {_hm_rules()}
  </div>
</section>

<section class="stratum s-stone" id="picks">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">まず、どれを狙うか。</h2>
    <p class="lead">場面ごとに、効き目のわかりやすい紋を選びました。安い段の紋も、毎日の手間をはっきり減らします。</p>
    <div class="hm-picks">{picks}</div>
    <a href="himon.html" class="wiki-band" style="margin-top:28px"><span class="wb-k dot">LIST</span><span class="wb-b"><b class="disp">{n}の紋を、ひとつずつ</b><span>段・効き目・刻めるもの。名前や効き目で探せて、段と道具でしぼりこめます。</span></span><span class="wb-go">灯紋の一覧へ<i></i></span></a>
  </div>
</section>
'''


def himon_page():
    R = HM["rarity"]
    rows = ""
    for d in HM["defs"]:
        r = R[d["r"]]
        gs = " ".join(k for k, _, s in _HM_G if s & set(d["cats"]))
        mx = f'<span class="hm-mx dot">最大 Lv{d["max"]}</span>' if d["max"] > 1 else ""
        pair = ""
        if d["group"]:
            o = [x["name"] for x in HM["defs"] if x["group"] == d["group"] and x["id"] != d["id"]]
            pair = f'<span class="hm-x">「{"・".join(o)}」と同じ道具には刻めない</span>'
        rows += f'''<li class="hm" id="m-{d["id"]}" style="--c:{r["hex"]}" data-r="{d["r"]}" data-g="{gs}" data-q="{_E(d["name"] + " " + " ".join(d["desc"]) + " " + d["on"] + " " + r["jp"] + " " + d["id"])}">
        <span class="hm-r disp">{r["jp"]}</span>
        <div class="hm-b"><b class="hm-n">{_E(d["name"])}</b>{mx}<p>{_hm_desc(d["desc"])}</p><span class="hm-on">{_E(d["on"])}</span>{pair}</div>
      </li>'''
    rchips = "".join(f'<button type="button" class="chip-f" data-f="r" data-v="{i}" style="--c:{r["hex"]}">{r["jp"]}</button>' for i, r in enumerate(R))
    gchips = "".join(f'<button type="button" class="chip-f" data-f="g" data-v="{k}" style="--c:#E9EEF6">{t}</button>' for k, t, _ in _HM_G)
    side = "".join(f'<a href="#{a}" style="--c:{c}"><span class="ws-k">{k}</span>{t}</a>' for a, k, t, c in [
        ("draw", "引", "紋書を引く", "#F2B544"), ("engrave", "刻", "道具に刻む", "#8FC3E8"), ("all", "紋", f"{len(HM['defs'])}の紋", "#B79CF2"), ("cmd", "令", "コマンド", "#C9D0DC")])
    side += _wiki_others("himon")
    hero = f'''<div class="hero ch-hero wk-hero" style="--c:#F2B544">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    {_wiki_switch("himon")}
    {_wiki_crumb("himon", f'<span aria-hidden="true">›</span><span>{len(HM["defs"])}の紋</span>')}
    <div class="ch-head">{pix(HM_ICON, "ch-ic big")}<div><h1 class="disp h1-sub">灯紋</h1></div></div>
    <p class="lead">経験値で紋書を引き、道具に刻む、{len(HM["defs"])}の特別な付呪。ふつうの付呪とも灯技とも重ならない、灯原だけの力です。</p>
  </div>
</div>'''
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    <nav class="wside" aria-label="灯紋の目次"><p class="dot wside-h">灯紋 Wiki</p>{side}</nav>
    <div class="wk-main">
      <div class="wk-stats big">
        <div><b class="dot">{len(HM["defs"])}</b><span>紋</span></div><div><b class="dot">{len(R)}</b><span>段</span></div><div><b class="dot">{HM["slots"]}</b><span>1つの道具に刻める数</span></div><div><b class="dot">{HM["fudaMin"]}<small>分</small></b><span>灯札1枚に要る、遊んだ時間</span></div>
      </div>

      <h2 class="disp h2 wk-h" id="draw">紋書を引く</h2>
      <p class="mu wk-p"><span class="kbd">/himon</span> で画面を開き、紋書を選んで経験値と灯札を払うと、1冊出ます。どの紋が出るかは、段の中でくじ引きです。</p>
      {_hm_tiers()}
      {_hm_fuda()}
      <p class="mu wk-small">紋の Lv：最大 Lv2 の紋は 85% で Lv1・15% で Lv2。最大 Lv3 の紋は 75%・20%・5%。見つけた紋は <span class="kbd">/himon book</span>（紋帳）に残ります。</p>

      <h2 class="disp h2 wk-h" id="engrave">道具に刻む</h2>
      {_hm_rules()}

      <h2 class="disp h2 wk-h" id="all">{len(HM["defs"])}の紋</h2>
      <div class="finder">
        <label class="find"><span class="sr">紋を探す</span><input type="search" id="hq" placeholder="名前・効き目で探す（例：夜、矢、滑空）" autocomplete="off"><kbd class="dot">/</kbd></label>
        <div class="filters"><div class="fg"><span class="fl-l">段</span>{rchips}</div><div class="fg"><span class="fl-l">道具</span>{gchips}</div></div>
        <p class="find-n mu" aria-live="polite"><b class="dot" id="hn">{len(HM["defs"])}</b> の紋 <button type="button" class="clear" id="hclear" hidden>しぼりこみを消す</button></p>
        <ul class="hms" id="hl">{rows}</ul>
        <p class="wk-empty" id="hempty" hidden>見つかりませんでした。ことばを短くしてみてください。</p>
      </div>
      <p class="mu wk-small">「灯りの外」は灯籠の灯りが届かない場所。「帰る場所」は灯標で決めた場所です。宝玉は、胸当てに刻むと、身につけたほかの紋をすべて1段強くします。</p>

      <h2 class="disp h2 wk-h" id="cmd">コマンド</h2>
      <div class="tbl-wrap"><table><thead><tr><th>コマンド</th><th>すること</th></tr></thead><tbody>
        <tr><th class="n">/himon</th><td>紋書を引く画面を開く（<span class="kbd">/mon</span> でも同じ）</td></tr>
        <tr><th class="n">/himon engrave</th><td>道具に刻む画面を開く</td></tr>
        <tr><th class="n">/himon book</th><td>紋帳（見つけた紋と回数）</td></tr>
      </tbody></table></div>
    </div>
  </div>
</section>
<script src="assets/wiki.js" defer></script>'''


HM_PAGES = [("himon.html", "灯紋 Wiki｜灯原", f"灯紋（ひもん）{len(HM['defs'])}種のすべて。経験値で紋書を引く5つの段（並・良・珍・稀・秘）、道具への刻み方、重ね方、効き目と刻めるもの。", himon_page())]


# ───────────────────────── 灯里（里・職・灯結） ─────────────────────────
HS = _wj.loads((pathlib.Path(__file__).parent / "data" / "hisato.json").read_text(encoding="utf-8"))
HSN = HS["num"]
_HS_JC = {"daiku": "#EE9A4A", "himori": "#F2CB4E", "eji": "#E8574A", "shonin": "#72D69C", "tabibito": "#6AA8FF"}
_HS_JK = {"daiku": "大", "himori": "灯", "eji": "衛", "shonin": "商", "tabibito": "旅"}
_HS_JG = {"daiku": "土地にブロックを置く。数えるのは新しい場所だけで、土や丸石を積むだけ、壊して置き直すだけは数えない。",
          "himori": "喰われた里の灯籠を灯し直す。新しい灯籠をつないで土地を広げる。夜に里の灯籠を見回る。",
          "eji": "夜、土地の中で、自然に湧いた敵を倒す。灯喰いを退ける。スポナーや敵トラップの敵は数えない。",
          "shonin": "屋台で取引が成り立つ。同じ相手ほど少なく、ほかの里の人との取引は多めに数える。",
          "tabibito": "里の外で集めた建材を蔵へ。まだ誰も歩いていない土地を自分の足で歩く（滑空・船・乗り物は数えない）。遺跡を見聞録に記す。"}
_HS_GC = ["#C9B48A", "#8FCB6A", "#6AB8E8", "#E9824A"]
# 格のドット絵（16×16）：集落・村・町・都
_HS_GI = [
    ["................", "................", "................", "................", "................", "................", ".......##.......", "......#oo#......", ".....#oooo#.....", "....#oooooo#....", "...##########...", "....#o####o#....", "....#o#oo#o#....", "....#o#oo#o#....", "...##########...", "................"],
    ["................", "................", "................", "...##...........", "..#oo#..........", ".#oooo#....##...", "########..#oo#..", ".#o##o#..#oooo#.", ".#o##o#.########", ".#o##o#..#o##o#.", ".######..#o##o#.", "#########o##o##.", "................", "................", "................", "................"],
    ["................", ".......##.......", "......#oo#......", ".....######.....", "......#oo#......", ".##...#oo#...##.", "#oo#..#oo#..#oo#", "####.######.####", "#o##.#o##o#.#o##", "#o##.#o##o#.#o##", "#o##.#o##o#.#o##", "################", "................", "................", "................", "................"],
    [".......##.......", "......#oo#......", "....########....", ".....#oooo#.....", "...##########...", "....#oo##oo#....", "..############..", "...#oo#oo#oo#...", ".##############.", "..#oo#oooo#oo#..", "..#oo#o##o#oo#..", "..#oo#o##o#oo#..", "################", "................", "................", "................"],
]


def _hs_merge(vals):
    """段ごとの文を1行に。数字だけがちがうなら「+1／+2／+3」とまとめる。"""
    return _hm_desc(vals)


def _hs_mat(d):
    return "".join(f'<span class="hs-mat"><b class="dot">{v:,}</b>{_E(k)}</span>' for k, v in d.items())


def _hs_land_demo():
    return '''<div class="demo hs-demo" data-sato>
      <div class="pn demo-main hs-demo-main">
        <div class="btns" style="margin-bottom:14px"><button type="button" class="pbtn sm" data-eat>灯喰いの夜</button><button type="button" class="gbtn sm" data-far>遠灯し（灯守の匠）</button><button type="button" class="gbtn sm" data-reset>最初の形に戻す</button></div>
        <div class="grid-scroll"><div class="grid hs-grid"></div></div>
        <div class="legend">
          <span><i style="background:#8A6A3A"></i>里の土地</span>
          <span><i style="background:#3D5E2C"></i>灯りの中（里の土地ではない）</span>
          <span><i style="background:#16241A;border:1px solid #6F7D6A"></i>灯りの外</span>
          <span><i style="background:#F2B544"></i>民の灯籠</span>
          <span><i style="background:#5AAAFF"></i>喰われた灯籠</span>
          <span><i style="background:#E9824A;box-shadow:0 0 0 2px #FFE3A3"></i>里灯</span>
          <span><i style="background:transparent;outline:2px dashed #FFE3A3;outline-offset:-2px"></i>屋敷</span>
        </div>
      </div>
      <div class="demo-side">
        <div class="stat"><span>土地に数える灯籠</span><b><i data-s="lan" style="font-style:normal">0</i><small> / 40</small></b></div>
        <div class="stat"><span>里の土地</span><b><i data-s="land" style="font-style:normal">0</i><small> マス</small></b></div>
        <div class="stat"><span>欠けた土地</span><b data-s="lost">0</b></div>
        <p class="demo-msg" data-msg role="status">マスを押すと灯籠を置けます。灯籠を押すと喰わせられます。里灯から灯路でつながっている灯籠の守りだけが、里の土地です。</p>
      </div>
    </div>'''


def _hs_found_steps():
    f = HS["foundation"]
    steps = [
        ("創設者", f'動いて遊んだ時間 <b class="dot">{HSN["founderHours"]}</b> 時間以上、灯の証の位階 <b class="dot">{HSN["founderRank"]}</b> 以上、どの里にも属していないこと。'),
        ("発起人", f'創設者を含めて <b class="dot">{HSN["founders"]}</b> 人。それぞれ <b class="dot">{HSN["cofounderHours"]}</b> 時間以上遊んでいて、14日以内に里を抜けていないこと。誘いは画面から送ります。'),
        ("礎を納める", f'礎の祭壇に、発起人それぞれが<b>2割以上</b>を自分で納めます。誰がどれだけ納めたかは画面に出ます。<span class="hs-mats">{_hs_mat(f)}</span>'),
        ("里灯を立てる", f'灯路網の格2以上で、発起人の灯籠10基以上につながっている場所。ほかの里の土地から <b class="dot">{HSN["gap"]}</b> ブロック以上離れていること。'),
        ("仮の里の7日", f'{HSN["provisionalDays"]}日のうちに礎を納めきり、最初の大事業「里開き」を果たします。発起人3人がそれぞれ日課を3つ、蔵へ木材256・食料128。'),
    ]
    lis = "".join(f'<li><span class="hs-st-n dot">{i + 1}</span><b class="disp">{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(steps))
    return f'''<ol class="hs-steps">{lis}<li class="end"><span class="hs-st-n dot">✦</span><b class="disp">集落になる</b><p>里の名がサーバー全体に知らされ、掲示板・蔵・日課が動き出します。</p></li></ol>'''


def _hs_grades():
    G = HS["grades"]
    mx = G[-1]["lanterns"]
    cols = ""
    for i, g in enumerate(G):
        up = "・".join(f"{k} {v}" for k, v in g["upkeep"].items())
        cols += f'''<div class="hs-g" style="--c:{_HS_GC[i]};--i:{len(G) - 1 - i}">
        <div class="hs-g-top">{pix(_HS_GI[i], "ch-ic hs-g-ic")}<span class="hs-g-no dot">格 {i + 1}</span><h3 class="disp">{g["jp"]}</h3><p class="hs-g-pw"><b class="dot">{g["power"]:,}</b><small>里の力</small></p></div>
        <dl>
          <div><dt>民</dt><dd class="dot">{g["people"]}<small>人</small></dd></div>
          <div><dt>土地の灯籠</dt><dd class="dot">{g["lanterns"]}<small>基</small></dd></div>
          <div><dt>補佐</dt><dd class="dot">{g["aides"]}<small>人</small></dd></div>
          <div><dt>施設</dt><dd class="dot">{g["facilities"]}</dd></div>
          <div><dt>名所</dt><dd class="dot">{g["landmarks"]}</dd></div>
          <div><dt>里の力の上限</dt><dd class="dot">{g["weekCap"]:,}<small>／週</small></dd></div>
        </dl>
        <p class="hs-g-open"><span>開くもの</span>{_E(g["opens"])}</p>
        <p class="hs-g-up"><span>毎週の灯油</span>{_E(up)}</p>
        <div class="hs-g-bar" aria-hidden="true"><i style="width:{g["lanterns"] / mx * 100:.0f}%"></i></div>
      </div>'''
    return f'<div class="hs-grades">{cols}</div>'


def _sato_sec():
    return f'''<section class="stratum s-deep" id="sato">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">灯りが、そのまま里の土地になる。</h2>
    <p class="lead"><span class="kbd">/sato</span> で開きます。里は、仲間と開く小さな国です。里の中心に立てる大きな灯籠「里灯（さとび）」から、灯路でつながっている民の灯籠。その守りの範囲が、里の<b>土地</b>です。囲いの道具はありません。灯りを広げれば、土地が広がります。</p>
    {_hs_land_demo()}
    <div class="three">
      <div><h3 class="h3 disp">里灯は喰われない</h3><p class="mu">里灯は灯喰いに喰われず、壊せるのは里長だけ。動かすときは「移築」で、3日かけて移ります。右クリックで里のホームが開きます。</p></div>
      <div><h3 class="h3 disp">喰われると、土地が欠ける</h3><p class="mu">灯籠が喰われると、そこから先の土地が欠けます。欠けているあいだも、屋敷と認められた建物の守りは持ち主に残ります。灯し直せば、土地は戻ります。</p></div>
      <div><h3 class="h3 disp">外の人は、通れるが建てられない</h3><p class="mu">土地の中で建てる・壊す・箱を開けるのは民だけ。ほかの里の人や里のない人は、歩いて通り抜けられますが、土地には手を出せません。</p></div>
    </div>
  </div>
</section>

<section class="stratum s-dusk" id="found">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">3人と、重い礎と、7日。</h2>
    <p class="lead">里は、ひとりでもサブのアカウントでも開けないようにしてあります。来たばかりの人が開いて、すぐ消える里が並ばないように。開くまでの道のりそのものが、最初の共同作業です。</p>
    {_hs_found_steps()}
    <p class="note warn"><b>7日のうちに果たせなかったときは、解散します。</b>納めた礎は、納めた人それぞれに半分ずつ手紙で戻ります。正式な里を解散したときは、礎は戻りません。開いて消してをくり返しても、得をしないようにしてあります。</p>
  </div>
</section>

<section class="stratum s-stone" id="grade">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">集落から、都へ。</h2>
    <p class="lead">依頼を果たすと「里の力」が貯まり、格が上がります。里の力は使っても減りません。格を上げるには、里の力に加えて、大事業「格上げの普請」を果たします。点数だけでは上がりません。</p>
    {_hs_grades()}
    <p class="mu hs-small">よく遊ぶ10人ほどの里で、村まで約2週、町まで約6週、都まで約3か月が目安です。里の力には、格ごとに1週間の上限があります。</p>
  </div>
</section>

<section class="stratum s-rock" id="yashiki">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">屋敷は持ち主のもの。共有地は、掟で決める。</h2>
    <div class="hs-roles">
      <div class="hs-role" style="--c:#F2B544"><span class="hs-role-k disp">長</span><h3 class="disp">里長 <small class="dot">1人</small></h3><p>建物の鑑定、蔵、施設の普請、民の出入り、補佐の任命、里の設定。</p></div>
      <div class="hs-role" style="--c:#C9D0DC"><span class="hs-role-k disp">補</span><h3 class="disp">補佐 <small class="dot">0〜3人</small></h3><p>鑑定（自分の依頼はのぞく）、民を迎える、蔵。人数は格で決まります。</p></div>
      <div class="hs-role" style="--c:#8FCB6A"><span class="hs-role-k disp">民</span><h3 class="disp">民 <small class="dot">格の上限まで</small></h3><p>職につく、依頼を受ける、土地で建てる。里は1人1つまで。</p></div>
    </div>
    <div class="three">
      <div><h3 class="h3 disp">屋敷（家の区画）</h3><p class="mu">里長が民ごとに区画を割り当てます。屋敷の中で建てる・壊す・箱を開けるのは、持ち主と、持ち主が許した人だけ。<b>里長も入れません。</b></p></div>
      <div><h3 class="h3 disp">掟（共有地のきまり）</h3><p class="mu">屋敷の外の土地で、誰が何をできるかを、立場と職ごとにオン・オフします。はじめは、大工と里長・補佐だけが共有地で建てられ、民は共有の箱を開けられます。</p></div>
      <div><h3 class="h3 disp">入る・抜ける</h3><p class="mu">招待か、申し込みの承認で入ります。入って{HSN["newcomerDays"]}日は「新入り」で報酬が半分。抜けるのはいつでもでき、抜けたあと{HSN["leaveLock"]}日はほかの里に入れません。申し込む前に{HSN["guestDays"]}日だけ「客人」として入ってみることもできます。</p></div>
    </div>
    <div class="facts">
      <div class="fact"><p class="fact-n">蔵</p><p>里の共有の倉庫。建材・食料・鉱物・珍品・雑貨の5つの棚に分かれ、棚ごとに出せる人を決めます。出し入れはすべて記録に残り、補佐が1日に持ち出せる量には上限があります。</p></div>
      <div class="fact"><p class="fact-n">灯油</p><p>毎週月曜、格ごとに決まった維持費を蔵から自動で払います。2週続けて払えないと里全体のバフが止まり、4週続くと格が1つ下がります。</p></div>
      <div class="fact"><p class="fact-n">30<small>日</small></p><p>民が誰も来ない里は「眠る里」になり、依頼とバフが止まります。90日で里灯が消え、蔵の中身は里長に手紙で届きます。</p></div>
      <div class="fact"><p class="fact-n">21<small>日</small></p><p>里長が来ないときは、いちばんよく来ている補佐に、いなければ職の位がいちばん高い民に、自動で引き継ぎます。運営が里を片付ける必要はありません。</p></div>
    </div>
  </div>
</section>
'''


def _hs_job_card(j):
    c = _HS_JC[j["key"]]
    rows = ""
    for i in range(len(j["buffs"][0])):
        vals = [b[i] for b in j["buffs"]]
        rows += f"<li>{_hs_merge(vals)}</li>"
    return f'''<article class="hs-job" style="--c:{c}" id="j-{j["key"]}">
        <header><span class="hs-job-k disp">{_HS_JK[j["key"]]}</span><div><h3 class="disp">{j["jp"]}</h3><p>{_E(j["role"])}</p></div></header>
        <p class="hs-job-g"><span>育つこと</span>{_E(_HS_JG[j["key"]])}</p>
        <ul class="hs-job-b">{rows}</ul>
        <p class="hs-job-s"><span class="dot">匠の奉仕</span><b>{_E(j["service"])}</b>{_E(j["serviceText"])}</p>
      </article>'''


def _hs_ranks():
    R = HS["ranks"]
    mx = math.sqrt(R[-1]["xp"])
    hrs = ["―", "約5時間", "約20時間", "約50時間", "約100時間"]
    nodes = ""
    for i, r in enumerate(R):
        x = math.sqrt(r["xp"]) / mx * 100
        nodes += f'''<li style="--x:{x:.1f}%"><i></i><b class="disp">{r["jp"]}</b><span class="dot">{r["xp"]:,}</span><small>{hrs[i]}</small><em>{_E(r["opens"])}</em></li>'''
    return f'<ol class="hs-ranks">{nodes}</ol>'


def _hs_hud():
    return '''<div class="hs-hud" role="img" aria-label="建築の依頼のとき、画面の上に出るバーの例">
      <p class="hs-hud-t">民の家 <span>|</span> <b>✔ブロック 300/300</b> ・ <b>✔種類 10/5</b> ・ <b>✔高さ 7/6</b> ・ 時間 48分/1時間</p>
      <div class="hs-hud-bar"><i style="width:88%"></i></div>
    </div>'''


def _shoku_sec():
    jobs = "".join(_hs_job_card(j) for j in HS["jobs"])
    trials = "".join(f'<li style="--c:{_HS_JC[j["key"]]}"><b>{j["jp"]}</b>{_E(j["trial"])}</li>' for j in HS["jobs"])
    return f'''<section class="stratum s-deep" id="jobs">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">5つの職で、里が回る。</h2>
    <p class="lead">建てる・守る・広げる・つなぐ・運ぶ。里に要る役目を、5つの職で分けました。灯技の「道」が自分の腕を育てるのに対して、職は「里での役目」を育てます。バフは里の土地の中で働き（旅人は外で）、いちばん上の力は仲間のために使う「奉仕」です。</p>
    <div class="hs-jobs">{jobs}</div>
    <p class="mu hs-small">数字は段ごとの値です（見習い・一人前 ／ 熟練 ／ 名人・匠）。職は里に入ったときに選び、新入りの{HSN["newcomerDays"]}日のあいだに限り、1回だけ無料で選び直せます。</p>
  </div>
</section>

<section class="stratum s-dusk" id="rank">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">見習いから、匠へ。</h2>
    <p class="lead">職の経験は、依頼からおよそ7割、職の行動から3割。行動から入るのは1日 {HSN["actionCap"]} までで、放置や稼ぎ場では伸びません。毎日2時間ほど遊んで、匠まで約2か月です。</p>
    {_hs_ranks()}
    <div class="hs-two">
      <div><h3 class="h3 disp">匠の試し</h3><p class="mu">匠になるには、経験に加えて職ごとの試しを1つ果たします。匠になると、サーバー全体に知らされ、サイトの匠の名簿に載ります。</p><ul class="hs-trials">{trials}</ul></div>
      <div><h3 class="h3 disp">弟子</h3><p class="mu">名人と匠は、同じ職の見習い・一人前を弟子にできます（2人まで）。弟子の依頼の報酬が +20%、師匠にもその1割が入ります。</p>
        <h3 class="h3 disp" style="margin-top:28px">五職そろい</h3><p class="mu">5つの職にそれぞれ1人以上、最近7日に来た民がいると、土地の中で民全員の灯力（灯技）がたまりやすくなります。同じ職が民の半分を超えると、その職の報酬は下がり、少ない職には「人手不足」の印と +25% がつきます。</p></div>
    </div>
  </div>
</section>

<section class="stratum s-stone" id="quest">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">依頼は、里に足りないものから届く。</h2>
    <p class="lead">依頼は里の様子を見て、自動で出る仕事です。喰われた灯籠が多ければ灯守の灯し直し、建材の棚がさみしければ旅人の運び、という具合。量や数はプラグインが数え、里長が見るのは建物の見た目だけです。</p>
    <div class="hs-kinds">
      <div style="--c:#F2B544"><span class="dot">毎日0時</span><h3 class="disp">日課</h3><p>民ごとに職の依頼が{3}つ。30分ほど。</p><b class="dot">経験 {HSN["dailyXp"]}・里の力 10</b></div>
      <div style="--c:#8FCB6A"><span class="dot">毎週月曜</span><h3 class="disp">週課</h3><p>民ごとに2つ。一人前から。2〜4時間。</p><b class="dot">経験 {HSN["weeklyXp"]}・里の力 80・欠片 2</b></div>
      <div style="--c:#6AB8E8"><span class="dot">里長・補佐が出す</span><h3 class="disp">里の頼み</h3><p>形を選んで数を決めるだけ。報酬は蔵から先に預けます。</p><b class="dot">蔵の品＋職の経験</b></div>
      <div style="--c:#E9824A"><span class="dot">格上げ・施設のたびに</span><h3 class="disp">大事業</h3><p>ひとつの目標を職ごとの分担に分けて、みんなで果たします。</p><b class="dot">里の力・格・施設</b></div>
    </div>
    <h3 class="h3 disp hs-sub">建築の依頼</h3>
    <p class="mu hs-p">「ここを角にする」で区画を決めると、光の線で枠が見え、画面の上のバーに条件の進み具合が出続けます。</p>
    {_hs_hud()}
    <div class="hs-judge">
      <div class="hs-checks"><p class="dot">プラグインが数えること</p><ul>
        <li>置いたブロックの数（土・砂・丸石など埋め立て用は数えない。その里で30日以内に置いたことのない場所だけ）</li>
        <li>使ったブロックの種類（5種以上）</li>
        <li>建てた時間（動いて遊んだ時間で数える）</li>
        <li>形：高さ、屋根、扉、ベッド、灯り、床の広さ</li>
      </ul></div>
      <div class="hs-verdicts"><p class="dot">里長が見ること（見た目だけ）</p>
        <div class="hs-v" style="--c:#F2B544"><b class="disp">見事</b><span>報酬 1.5倍</span></div>
        <div class="hs-v" style="--c:#8FCB6A"><b class="disp">良し</b><span>報酬 1倍</span></div>
        <div class="hs-v" style="--c:#E8574A"><b class="disp">やり直し</b><span>理由をひとこと</span></div>
        <p class="mu">{HSN["autoHours"]}時間たっても鑑定されないときは、条件を満たしていれば自動で「良し」。認めた建物は{HSN["watchDays"]}日見守り、3割以上壊されると報酬が取り消されます。</p>
      </div>
    </div>
  </div>
</section>

<section class="stratum s-rock" id="change">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">職は、試しを越えて変える。</h2>
    <p class="lead">職は簡単には変えられません。職をなくすこともできません。里を移っても、職と位はそのまま持っていきます。</p>
    <ol class="hm-steps hs-five">
      <li><b>申し出る</b><span>職の画面の「転職の試し」で、なりたい職を選ぶ。里長に知らせが届く。</span></li>
      <li><b>引き継ぐ</b><span>いまの職の依頼を終えるか手放す。弟子がいれば解く。</span></li>
      <li><b>奉公する</b><span>{HSN["hokoDays"]}日のうちに、新しい職の「奉公の依頼」を{HSN["hokoNeed"]}つ果たす（週に3つ届く）。</span></li>
      <li><b>師の許し</b><span>新しい職の熟練以上か里長が許す。{72}時間返事がなければ自動で許される。</span></li>
      <li><b>転職する</b><span>新しい職の見習いから。前の職の経験と位は残り、{HSN["lockDays"]}日は変えられない。</span></li>
    </ol>
    <p class="mu hs-small">前の職に戻るときは、奉公が7日と3つで済みます。人手不足の職へ移るときは、奉公の依頼が4つで済みます。</p>
    <a href="hisato.html" class="wiki-band hs-band"><span class="wb-k dot">LIST</span><span class="wb-b"><b class="disp">灯里 Wiki</b><span>職ごとの日課と週課、バフの段、位、格、施設の素材、礎、ずるの防ぎ方。ゲームと同じ数字で。</span></span><span class="wb-go">灯里の一覧へ<i></i></span></a>
  </div>
</section>
'''


_HS_MUSUBI = [
    ("縁", "#F29BB8", f"{HSN['friendsMax']}人まで", "フレンド。来ている・いないが一覧で見え、同じ里の民は「里の縁」として別の段に並びます。"),
    ("一団", "#F2B544", f"{HSN['partyMax']}人まで", "パーティ。仲間の方角と体力が見え、一団だけのチャットと一団の箱が使えます。里の中でも外でも組めます。"),
    ("合流・呼ぶ", "#8FCB6A", "3秒", "相手が承認すると、相手の近くの灯りへ移ります。民は里灯へ帰る「帰里」も使えます（待ち時間あり）。"),
    ("手紙と小包", "#6AB8E8", f"{HSN['mailDays']}日で戻る", "いない人にも届く置き手紙。品を添えた小包は、受け取られないと送り主に戻ります。里の知らせ・便りもここへ。"),
    ("合図", "#E9824A", "8つまで", "空中に言葉の札を立てます。見せる相手は自分・一団・里・みんな。里長は「普請の予定地」を立てられます。"),
    ("配信中", "#B46CFF", "3つの強さ", "配信や録画のときに。座標・名前・チャットを伏せる範囲を、ゆるく／しっかり／完全から選びます。"),
    ("離れる", "#C9D0DC", "お互いに", "合わない相手と、お互いに見えず、言葉も届かなくなります。同じ里の民にも使え、その人の依頼の鑑定は回ってきません。"),
    ("おかえり", "#FFE3A3", "留守のあいだ", "入ったとき、留守のあいだの手紙・鑑定の結果・喰われた里の灯籠・大事業の進み具合をまとめて見せます。"),
]
_HS_LIFE = [
    ("名所めぐり", "#F2B544", "「見事」になった建物を、里長が名所に登録します。誰でも名所の前へ灯渡りで見学でき、訪れるとはんこが押されます。10か所・30か所で灯の証。月に一度、みんなの投票で「今月の名所」を選びます。"),
    ("旅の依頼", "#6AB8E8", "里長が掲示板に「鉄インゴット128を求む」のように出す依頼。報酬は蔵から先に預け、里のない人やほかの里の人が受けられます。ひとりで遊ぶ人にも出番ができます。"),
    ("屋台と市の日", "#72D69C", "商人はエメラルドと品を交換する屋台を出せます。持ち主がいなくても売り買いでき、売り上げは手紙で届きます。週に一度の市の日は、ほかの里の人も灯渡りで来られます。"),
    ("里の便り", "#F29BB8", "毎週月曜、里ごとに1冊の本が届きます。果たした依頼の数、職ごとにいちばん働いた人、新しい建物、灯し直してくれた人、格の進み。"),
    ("感謝の灯", "#FFE3A3", f"鑑定・灯し直し・取引など、人の役に立つことが起きると「ありがとうを送る」が出ます。1日{HSN['thanks']}回まで、同じ相手には1日1回。週にいちばん感謝された人は、称号「里の灯」。"),
    ("朝の灯と里の顔", "#E9824A", "その日はじめて土地に入ると、里灯が強く灯り、灯路を渡って里中に光が走ります。里の旗、名前の色、入口のあいさつ、広場に住み着く里人。強さではなく、名前と見た目を配ります。"),
]


def _hs_gui():
    # 6段のチェスト画面の見本（ホーム）
    S = {0: ("職", "#EE9A4A", "大工 一人前"), 2: ("板", "#F2B544", "掲示板 日課 2/3"), 3: ("蔵", "#C9B48A", "蔵"), 4: ("里", "#E9824A", "灯の里（村）"), 5: ("図", "#8FCB6A", "里の地図"), 6: ("結", "#F29BB8", "灯結"), 8: ("✉", "#6AB8E8", "受信箱 3通"),
         20: ("普", "#E9824A", "普請"), 21: ("鑑", "#F2B544", "鑑定の箱"), 22: ("民", "#8FCB6A", "民"), 23: ("掟", "#C9D0DC", "掟"), 24: ("名", "#F2B544", "名所めぐり"), 30: ("市", "#72D69C", "市と屋台"), 31: ("旅", "#6AB8E8", "旅の依頼"), 32: ("暦", "#B46CFF", "季節の大事業"),
         45: ("←", "#BFC9DB", "戻る"), 46: ("◀", "#BFC9DB", "前のページ"), 49: ("⌂", "#F2B544", "ホーム"), 52: ("▶", "#BFC9DB", "次のページ"), 53: ("✕", "#E8574A", "閉じる")}
    cells = ""
    for i in range(54):
        if i in S:
            k, c, t = S[i]
            cells += f'<span class="hs-slot on" style="--c:{c}" title="{t}"><i class="disp">{k}</i></span>'
        else:
            cells += '<span class="hs-slot"></span>'
    return f'''<div class="hs-gui">
      <div class="hs-chest" role="img" aria-label="里のホームの画面の見本。上の段が見出し、下の段が固定の操作。"><p class="hs-chest-t">里のホーム ― 灯の里</p><div class="hs-slots">{cells}</div></div>
      <dl class="hs-gui-rules">
        <div><dt class="dot">上の段</dt><dd>見出し。いまの画面、自分の職と位、未読の手紙。</dd></div>
        <div><dt class="dot">下の段</dt><dd>どの画面でも同じ位置に、戻る・前・ホーム・次・閉じる。</dd></div>
        <div><dt class="dot">押し方</dt><dd>左クリックが主な操作、シフト＋クリックが2つ目。右クリックだけの隠れた操作はありません。</dd></div>
        <div><dt class="dot">取り消せないこと</dt><dd>解散・追放・転職などは、1回目で札が赤くなり、もう一度押すと実行します。</dd></div>
        <div><dt class="dot">生きている画面</dt><dd>進み具合・残り時間・人数は、開いたまま1秒ごとに変わります。</dd></div>
        <div><dt class="dot">統合版</dt><dd>同じ中身を、押しやすいフォームで。文字は金床（Java）かフォームで入れます。</dd></div>
      </dl>
    </div>'''


def _musubi_sec():
    tiles = "".join(f'<div class="hs-tile" style="--c:{c}"><span class="dot">{n}</span><h3 class="disp">{t}</h3><p>{d}</p></div>' for t, c, n, d in _HS_MUSUBI)
    life = "".join(f'<div class="hs-life" style="--c:{c}"><h3 class="disp">{t}</h3><p>{d}</p></div>' for t, c, d in _HS_LIFE)
    return f'''<section class="stratum s-deep" id="musubi">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">仲間と、ほどよくつながる。</h2>
    <p class="lead">灯結（ひむすび）は、里の暮らしの道具です。<span class="kbd">/sato musubi</span> か、里のホームの「灯結」から。里がなくても使えます。近づく人を押し戻す結界はありません。里の土地には、すでに建てる・壊すの守りがあるからです。</p>
    <div class="hs-tiles">{tiles}</div>
  </div>
</section>

<section class="stratum s-dusk" id="life">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">来るたびに、小さな楽しみを。</h2>
    <p class="lead">里は、働く場所だけでは使われません。作ったものが人に見られ、里の外の人ともつながるように。どれも強さは配らず、名前と見た目と話題を配ります。</p>
    <div class="hs-lifes">{life}</div>
    <p class="note"><b>季節の大事業。</b>シーズンに1回、サーバー全体でひとつのものを作ります。すべての里が分担を受け、進み具合は全員に見えます。完成すると全員に記念の品、いちばん力を尽くした里に称号。</p>
  </div>
</section>

<section class="stratum s-stone" id="gui">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">コマンドを覚えなくていい。</h2>
    <p class="lead">はじめて来たときに「里の灯帳」を渡します。手に持って右クリックするか、里灯を素手で右クリック。どちらも同じホームに着き、すべての操作が画面で終わります。</p>
    {_hs_gui()}
  </div>
</section>
'''


# ── 灯里の一覧（数字のすべて） ──
def _hs_quest_rows(j):
    out = ""
    for q in j["quests"]:
        out += f'<tr><th class="n">{q["kind"]}</th><td>{_E(q["text"])}</td><td class="dot">{q["xp"]}</td></tr>'
    return out


def hisato_page():
    G, J, R, F = HS["grades"], HS["jobs"], HS["ranks"], HS["facilities"]
    side = "".join(f'<a href="#{a}" style="--c:{c}"><span class="ws-k">{k}</span>{t}</a>' for a, k, t, c in [
        ("open", "開", "里を開く", "#E9824A"), ("grades", "格", "4つの格", "#8FCB6A"), ("jobs", "職", "5つの職", "#EE9A4A"), ("ranks", "位", "位", "#F2B544"),
        ("quests", "依", "依頼", "#6AB8E8"), ("facilities", "施", "施設", "#C9B48A"), ("fair", "守", "ずるの防ぎ方", "#E8574A"), ("musubi", "結", "灯結", "#F29BB8"), ("cmd", "令", "コマンド", "#C9D0DC")])
    side += _wiki_others("hisato")
    hero = f'''<div class="hero ch-hero wk-hero" style="--c:#E9824A">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    {_wiki_switch("hisato")}
    {_wiki_crumb("hisato", '<span aria-hidden="true">›</span><span>すべての数字</span>')}
    <div class="ch-head">{pix(CH_ICONS["sato"], "ch-ic big")}<div><h1 class="disp h1-sub">灯里</h1></div></div>
    <p class="lead">里・職・依頼・灯結。灯里（ひさと）のすべての数字を、ゲームと同じ値で。</p>
  </div>
</div>'''
    grow = "".join(f'<tr><th class="n">{g["jp"]}</th><td class="dot">{g["power"]:,}</td><td class="dot">{g["people"]}</td><td class="dot">{g["lanterns"]}</td><td class="dot">{g["aides"]}</td><td class="dot">{g["facilities"]}</td><td class="dot">{g["weekCap"]:,}</td><td class="dot">{g["kura"]:,}</td></tr>' for g in G)
    upk = "".join(f'<tr><th class="n">{g["jp"]}</th><td>{_E("・".join(f"{k} {v}" for k, v in g["upkeep"].items()))}</td><td>{_E(g["opens"])}</td></tr>' for g in G)
    jobs = ""
    for j in J:
        c = _HS_JC[j["key"]]
        buffs = "".join(f"<li>{_hs_merge([b[i] for b in j['buffs']])}</li>" for i in range(len(j["buffs"][0])))
        jobs += f'''<div class="hs-wj" style="--c:{c}" id="w-{j["key"]}">
        <h3 class="disp"><span class="hs-job-k disp">{_HS_JK[j["key"]]}</span>{j["jp"]}<small>{_E(j["role"])}</small></h3>
        <div class="hs-wj-in">
          <div><p class="dot hs-wj-h">バフ（見習い・一人前 ／ 熟練 ／ 名人・匠）</p><ul class="hs-job-b">{buffs}</ul>
          <p class="dot hs-wj-h">匠の奉仕</p><p><b>{_E(j["service"])}</b>：{_E(j["serviceText"])}</p>
          <p class="dot hs-wj-h">匠の試し</p><p>{_E(j["trial"])}</p></div>
          <div class="tbl-wrap"><table><thead><tr><th>種類</th><th>依頼</th><th>経験</th></tr></thead><tbody>{_hs_quest_rows(j)}</tbody></table></div>
        </div>
      </div>'''
    ranks = "".join(f'<tr><th class="n">{r["jp"]}</th><td class="dot">{r["xp"]:,}</td><td>{_E(r["opens"])}</td></tr>' for r in R)
    fac = ""
    for f in F:
        cost = "・".join(f"{k} {v:,}" for k, v in f["cost"].items()) or "（格上げの普請で建てる）"
        fac += f'<tr><th class="n">{f["jp"]}</th><td>{f["grade"]}</td><td>{_E(f["text"])}</td><td>{_E("・".join(f["need"]))}</td><td>{_E(cost)}</td></tr>'
    fair = [("身内どうしで、手抜きの建物を「見事」にする", "量・種類・時間・形はプラグインが数えるので、鑑定で変わるのは倍率（最大1.5倍）だけ。建てたブロックは本人の持ち物から減る。里の力には1週間の上限がある"),
            ("建てて、壊して、また建てる", "数えるのは、その里で30日以内に置いたことのない場所だけ。認めた建物は7日見守り、3割以上壊れたら報酬を取り消す"),
            ("サブのアカウントで人数を水増しする", f"人数・五職そろい・人手不足に数えるのは、最近7日に2時間以上動いて遊んだ民だけ。入って{HSN['newcomerDays']}日は報酬が半分"),
            ("ひとりの資本とサブのアカウントで里を開く", f"発起人それぞれに {HSN['founderHours']}時間・{HSN['cofounderHours']}時間の遊んだ時間が要り、礎の2割以上を自分で納める"),
            ("転職をくり返して、おいしい日課だけを受ける", f"転職には{HSN['hokoDays']}日の奉公が要り、変えたあとは{HSN['lockDays']}日変えられない"),
            ("里を渡り歩いて、日課を何度も受ける", f"日課と週課は人ごとに出るので、里を変えても同じ日に2回は出ない。抜けたら{HSN['leaveLock']}日はほかの里に入れない"),
            ("敵トラップ・品の往復・乗り物で職を育てる", f"衛士は自然に湧いた敵だけ、商人は同じ相手ほど少なく、旅人は自分の足で新しく歩いた場所だけ。行動から入る経験は1日 {HSN['actionCap']} まで"),
            ("蔵の持ち逃げ", "出し入れはすべて記録に残る。補佐が1日に持ち出せる量には上限があり、多く持ち出すと里長に知らせる"),
            ("里長の意地悪な鑑定", f"やり直しには理由が要る。同じ人を3回続けてやり直しにすると、次の鑑定は補佐に回る。{HSN['autoHours']}時間たつと自動で「良し」"),
            ("里を開いて消して、資本を回す", "仮の里の解散では礎が半分戻るだけ。正式な里の解散では礎は戻らない")]
    fair_rows = "".join(f"<tr><th>{_E(a)}</th><td>{_E(b)}</td></tr>" for a, b in fair)
    mus = "".join(f'<tr><th class="n">{t}</th><td>{_E(n)}</td><td>{_E(d)}</td></tr>' for t, c, n, d in _HS_MUSUBI)
    cmd = next(g for g in _CMDS if g[3] == "Hisato")
    cmd_rows = "".join(f'<tr><th class="n">{_E((r[0] + " " + r[1]).strip())}</th><td>{r[2]}</td></tr>' for r in cmd[5])
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    <nav class="wside" aria-label="灯里の目次"><p class="dot wside-h">灯里 Wiki</p>{side}</nav>
    <div class="wk-main">
      <div class="wk-stats big">
        <div><b class="dot">4</b><span>格</span></div><div><b class="dot">5</b><span>職</span></div><div><b class="dot">5</b><span>位（見習い〜匠）</span></div><div><b class="dot">{len(F)}</b><span>施設</span></div><div><b class="dot">{sum(len(j["quests"]) for j in J)}</b><span>依頼の型</span></div>
      </div>

      <h2 class="disp h2 wk-h" id="open">里を開く</h2>
      {_hs_found_steps()}

      <h2 class="disp h2 wk-h" id="grades">4つの格</h2>
      <div class="tbl-wrap"><table><thead><tr><th>格</th><th>要る里の力</th><th>民の上限</th><th>土地の灯籠</th><th>補佐</th><th>施設</th><th>里の力の上限／週</th><th>蔵の容量</th></tr></thead><tbody>{grow}</tbody></table></div>
      <div class="tbl-wrap" style="margin-top:16px"><table><thead><tr><th>格</th><th>毎週の灯油</th><th>開くもの</th></tr></thead><tbody>{upk}</tbody></table></div>
      <p class="mu wk-small">格を上げるには、要る里の力に加えて大事業「格上げの普請」を果たします。村へは集会所、町へは蔵屋敷、都へは大門を建てます。</p>

      <h2 class="disp h2 wk-h" id="jobs">5つの職</h2>
      {jobs}

      <h2 class="disp h2 wk-h" id="ranks">位</h2>
      <div class="tbl-wrap"><table><thead><tr><th>位</th><th>要る職の経験</th><th>開くもの</th></tr></thead><tbody>{ranks}</tbody></table></div>
      <p class="mu wk-small">日課1つで経験 {HSN["dailyXp"]}、週課1つで {HSN["weeklyXp"]}。行動から入る経験は1日 {HSN["actionCap"]} まで。人手不足の職は報酬 +25%、民の半分を超える職は −30%、弟子は +20%、学び舎のある里の見習い・一人前は +20%。</p>

      <h2 class="disp h2 wk-h" id="quests">依頼のきまり</h2>
      <div class="tbl-wrap"><table><thead><tr><th>種類</th><th>出かた</th><th>報酬</th></tr></thead><tbody>
        <tr><th class="n">日課</th><td>毎日0時、民ごとに3つ。里に足りないものから選ばれる</td><td>経験 {HSN["dailyXp"]}・里の力 10</td></tr>
        <tr><th class="n">週課</th><td>毎週月曜、民ごとに2つ（一人前から）</td><td>経験 {HSN["weeklyXp"]}・里の力 80・加護の欠片 2</td></tr>
        <tr><th class="n">里の頼み</th><td>里長・補佐が掲示板に出す</td><td>蔵から預けた品＋経験</td></tr>
        <tr><th class="n">旅の依頼</th><td>里長が出し、里の外の人も受けられる</td><td>蔵から預けた品</td></tr>
        <tr><th class="n">大事業</th><td>格上げ・施設の普請のたび。職ごとの分担。いない職の分は「手伝い」で埋められる（報酬は半分）</td><td>里の力・格・施設</td></tr>
        <tr><th class="n">建築の依頼</th><td>区画を決めて建て、鑑定に出す。見事 1.5倍・良し 1倍・やり直し</td><td>{HSN["autoHours"]}時間で自動の「良し」、{HSN["watchDays"]}日の見守り</td></tr>
      </tbody></table></div>

      <h2 class="disp h2 wk-h" id="facilities">施設</h2>
      <div class="tbl-wrap"><table><thead><tr><th>施設</th><th>要る格</th><th>効き目</th><th>中に置くもの</th><th>普請の素材</th></tr></thead><tbody>{fac}</tbody></table></div>
      <p class="mu wk-small">施設も建物なので、大工が建てて里長が鑑定します。中に置くもの（鐘・書見台など）は自動で数えます。大工がいる里は、普請の素材が 10〜20% 減ります。</p>

      <h2 class="disp h2 wk-h" id="fair">ずるの防ぎ方</h2>
      <p class="mu wk-p">身内の八百長は「止める」のではなく「しても得をしない」形にしてあります。量は機械が数え、素材は本当に減り、報酬の多くは本人の職の経験と里の力です。怪しい動きは週に一度、自動で運営に知らされます。</p>
      <div class="tbl-wrap"><table><thead><tr><th>起きそうなこと</th><th>防ぎ方</th></tr></thead><tbody>{fair_rows}</tbody></table></div>

      <h2 class="disp h2 wk-h" id="musubi">灯結</h2>
      <div class="tbl-wrap"><table><thead><tr><th>道具</th><th>数</th><th>できること</th></tr></thead><tbody>{mus}</tbody></table></div>

      <h2 class="disp h2 wk-h" id="cmd">コマンド</h2>
      <div class="tbl-wrap"><table><thead><tr><th>コマンド</th><th>すること</th></tr></thead><tbody>{cmd_rows}</tbody></table></div>
    </div>
  </div>
</section>'''


HS_PAGES = [("hisato.html", "灯里 Wiki｜灯原", "灯里（ひさと）のすべての数字。里を開く条件と礎、4つの格、5つの職のバフと依頼、位と匠の試し、施設、ずるの防ぎ方、灯結、コマンド。", hisato_page())]


# ───────────────────────── 技の組み立て ─────────────────────────
def wiki_build():
    data = {"capNeeds": HW["capNeeds"], "kind": _KIND, "paths": [
        {"id": p["id"], "k": p["k"], "name": p["name"], "c": _PCOL[i], "branches": p["branches"], "trial": p["trial"],
         "nodes": [{"id": n["id"], "name": n["name"], "b": n["branch"], "t": n["tier"], "kind": n["kind"], "req": n["req"], "cost": n["cost"], "eff": n["effect"], "parent": n["parent"]} for n in p["nodes"]]}
        for i, p in enumerate(HW["paths"])]}
    js = _wj.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tabs = "".join(f'<button type="button" class="bd-tab" data-p="{i}" style="--c:{_PCOL[i]}"><span class="ws-k">{p["k"]}</span><span class="bd-tn">{p["name"]}</span><small class="dot" data-sum="{i}">Lv25</small></button>' for i, p in enumerate(HW["paths"]))
    hero = _wiki_hero("技の組み立て", "道の Lv を決めて技を選ぶと、使う技点と覚える条件をその場で計算します。組み立てはリンクにして、そのまま Discord に貼れます。", "#F2B544", '<span aria-hidden="true">›</span><span>技の組み立て</span>', CH_ICONS["hiwaza"], "SKILL BUILDER")
    return hero + f'''
<section class="stratum s-deep wk">
  <div class="edge"></div>
  <div class="wrap wk-in">
    {_wiki_side("build")}
    <div class="wk-main bd" data-builder>
      <noscript><p class="note">この道具は JavaScript を使います。</p></noscript>
      <div class="bd-tabs" role="tablist" aria-label="道">{tabs}</div>
      <div class="bd-top">
        <label class="bd-lv"><span>Lv</span><input type="range" min="1" max="50" value="25" data-lv aria-label="道の Lv"><b class="dot" data-lvn>25</b></label>
        <div class="bd-pts"><span>技点</span><b class="dot" data-used>0</b><span>/</span><b class="dot" data-have>25</b><em data-left>残り 25</em></div>
        <label class="bd-trial"><input type="checkbox" data-trial checked> 奥義の試練を終えた</label>
      </div>
      <div class="bd-bar"><i data-barfill></i></div>
      <div class="bd-grid">
        <div class="tg bd-tree" data-tree></div>
        <aside class="bd-info" data-info aria-live="polite"><p class="mu">技を押すと、ここに説明と「覚える／外す」が出ます。</p></aside>
      </div>
      <div class="bd-acts">
        <button type="button" class="pbtn sm" data-share>組み立てのリンクをコピー</button>
        <button type="button" class="gbtn sm" data-resetp>この道をはじめから</button>
        <button type="button" class="gbtn sm" data-resetall>すべての道をはじめから</button>
        <span class="bd-msg mu" data-msg role="status"></span>
      </div>
      <h2 class="disp h2 wk-h">選んだ技</h2>
      <div class="bd-sum" data-summary></div>
      <p class="mu wk-small">数字はゲームと同じです。奥義は、三の段の技を {HW["capNeeds"]} つ覚え、奥義の試練を果たすと覚えられます（試練の進み具合は、ここでは数えません）。</p>
    </div>
  </div>
</section>
<script type="application/json" id="bd-data">{js}</script>
<script src="assets/build.js" defer></script>'''


WIKI_PAGES += [("wiki-build.html", "技の組み立て｜灯技 Wiki｜灯原", "灯技の組み立てシミュレーター。道の Lv と技を選ぶと、技点と覚える条件を計算。組み立てはリンクで共有できます。", wiki_build())]


# ───────────────────────── 支える（寄付） ─────────────────────────
import json as _json, html as _html

# PayPay の受け取り。どちらか（両方でも）を入れると、ボタン・QR・コピーが出る。空のあいだは「準備中」。
PAYPAY_LINK = ""   # PayPay アプリの「受け取りリンク」（https://… で始まるもの）
PAYPAY_ID = ""     # PayPay ID（アプリの「送る」→ ID で検索してもらう）
SUPPORT_CH = "#支援"  # 送ったあとに知らせてもらう Discord のチャンネル名

try:
    SUPPORTERS = _json.loads((pathlib.Path(__file__).parent / "data" / "supporters.json").read_text(encoding="utf-8"))
except (OSError, ValueError):
    SUPPORTERS = []


def _qr_svg(text):
    try:
        import segno
    except ImportError:
        return ""
    q = segno.make(text, error="m")
    rows = list(q.matrix_iter(scale=1, border=2))
    n = len(rows)
    r = []
    for y, row in enumerate(rows):
        x = 0
        while x < n:
            if not row[x]:
                x += 1
                continue
            w = 1
            while x + w < n and row[x + w]:
                w += 1
            r.append(f'<rect x="{x}" y="{y}" width="{w}" height="1"/>')
            x += w
    return f'<svg class="qr" viewBox="0 0 {n} {n}" role="img" aria-label="PayPay の受け取りQRコード"><rect width="{n}" height="{n}" fill="#fff"/><g fill="#14161B">{"".join(r)}</g></svg>'


_HEART = ["................", "................", "..####....####..", ".#oooo#..#oooo#.", "#oooooo##oooooo#", "#oooooooooooooo#", "#oooooooooooooo#", ".#oooooooooooo#.",
          "..#oooooooooo#..", "...#oooooooo#...", "....#oooooo#....", ".....#oooo#.....", "......#oo#......", ".......##.......", "................", "................"]

# 顔の画像が出ないとき（統合版の名前など）の代わりの顔（8×8 のドット絵）
_FACE = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8' shape-rendering='crispEdges'%3E%3Crect width='8' height='8' fill='%233B4466'/%3E"
         "%3Crect y='0' width='8' height='2' fill='%23262C45'/%3E%3Crect x='1' y='3' width='2' height='1' fill='%23F2B544'/%3E%3Crect x='5' y='3' width='2' height='1' fill='%23F2B544'/%3E"
         "%3Crect x='3' y='5' width='2' height='1' fill='%23262C45'/%3E%3C/svg%3E")


def _face(mcid, size=64):
    m = _html.escape(mcid, quote=True)
    src = f"https://mc-heads.net/avatar/{m}/{size}" if not mcid.startswith(".") else _FACE
    return f'<img class="face" src="{src}" alt="" width="{size}" height="{size}" loading="lazy" decoding="async" onerror="this.onerror=null;this.src=&quot;{_FACE}&quot;">'


def _wall():
    if not SUPPORTERS:
        ghosts = "".join('<li class="sup ghost" aria-hidden="true"><span class="face"></span><b class="dot">？？？</b><small>&nbsp;</small></li>' for _ in range(6))
        return f'''<div class="wall-empty">
      <ul class="wall">{ghosts}</ul>
      <p class="wall-msg"><b>あなたの灯が、最初のひとつになります。</b>まだ、この壁にはだれもいません。</p>
    </div>'''
    items = ""
    for s in SUPPORTERS:
        mcid = str(s.get("mcid", "")).strip()
        if not mcid:
            continue
        since = str(s.get("since", ""))[:7].replace("-", ".")
        items += f'<li class="sup">{_face(mcid)}<b class="dot">{_html.escape(mcid)}</b><small>{since} から</small></li>'
    return f'<ul class="wall">{items}</ul>'


def _pay_panel():
    ready = bool(PAYPAY_LINK or PAYPAY_ID)
    if not ready:
        return '''<div class="pay soon">
        <div class="pay-qr"><span class="qr-ph" aria-hidden="true"></span></div>
        <div class="pay-body">
          <p class="pay-k dot">PayPay</p>
          <h3 class="disp">ただいま準備中です</h3>
          <p class="mu">受け取りの用意ができしだい、ここにボタンとQRコードが出ます。Discord でもお知らせします。</p>
          <span class="pbtn paypay is-off" aria-disabled="true">準備中</span>
        </div>
      </div>'''
    qr = _qr_svg(PAYPAY_LINK) if PAYPAY_LINK else ""
    btn = f'<a href="{_html.escape(PAYPAY_LINK, quote=True)}" class="pbtn paypay" target="_blank" rel="noopener">PayPay で送る</a>' if PAYPAY_LINK else ""
    idrow = f'''<div class="addr pay-id"><span class="addr-t"><small>PayPay ID（アプリの「送る」→「ID」で検索）</small><b>{_html.escape(PAYPAY_ID)}</b></span><button type="button" class="gbtn sm" data-copy="{_html.escape(PAYPAY_ID, quote=True)}">IDをコピー</button></div>''' if PAYPAY_ID else ""
    return f'''<div class="pay">
        <div class="pay-qr">{qr or '<span class="qr-ph" aria-hidden="true"></span>'}<small class="mu">{"スマホのカメラか PayPay で読みとる" if qr else ""}</small></div>
        <div class="pay-body">
          <p class="pay-k dot">PayPay</p>
          <h3 class="disp">PayPay で、ひとことと一緒に。</h3>
          <p class="mu">金額は自由です（100円から）。<b>メッセージ欄に、あなたの MCID（マインクラフトの名前）</b>を書いてください。統合版の人は、名前の前の「.」もそのまま。</p>
          <div class="btns">{btn}</div>
          {idrow}
        </div>
      </div>'''


support = f'''<div class="hero sp-hero">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div><div class="moon" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    <div class="sp-head">{pix(_HEART, "ch-ic big heart")}<div><p class="ch-big dot">SUPPORT</p><h1 class="disp h1-sub">灯原を、支える。</h1></div></div>
    <p class="lead">灯原は、運営がひとりで、自分のお金で動かしています。もし「この夜が続いてほしい」と思ってもらえたら、少しだけ手を貸してください。寄付はまったくの自由です。しなくても、遊び方は何ひとつ変わりません。</p>
    <div class="btns" style="margin-top:26px"><a href="#how" class="pbtn">PayPay で支える</a><a href="#wall" class="gbtn">支え手の壁を見る</a></div>
  </div>
</div>

<section class="stratum s-deep" id="thanks">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">お礼は、見た目だけ。</h2>
    <p class="lead">支えてくれた人には、ふたつの「ありがとう」を。どちらも強さには関わりません。アイテムも経験値も加護も、ほかの人と同じです。</p>
    <div class="perks">
      <div class="perk">
        <div class="tagscene" aria-hidden="true">
          <div class="nametag"><i>❤</i> Tomi</div>
          <div class="pc"><span class="pc-h"></span><span class="pc-b"></span><span class="pc-l"></span><span class="pc-lan"></span></div>
          <div class="ground"></div>
        </div>
        <div class="perk-body">
          <p class="perk-k dot">01</p>
          <h3 class="disp h3">名前に <span class="hrt">❤</span> がつく</h3>
          <p class="mu">頭の上の名前、タブの一覧、チャットに、灯色の ❤ がつきます。灯籠のそばに立つあなたが、遠くからでもわかります。</p>
          <div class="mock">
            <p class="mock-row tab"><span class="mk-l">タブ</span><span><i class="hrt">❤</i> <s>[灯の大家]</s> Tomi</span></p>
            <p class="mock-row chat"><span class="mk-l">チャット</span><span><i class="hrt">❤</i> <s>[灯の大家]</s> &lt;Tomi&gt; こんばんは、今夜も灯しにきた</span></p>
          </div>
        </div>
      </div>
      <div class="perk">
        <div class="wallscene" aria-hidden="true">
          <span class="ws"></span><span class="ws on"></span><span class="ws"></span><span class="ws on"></span><span class="ws"></span><span class="ws"></span><span class="ws on"></span><span class="ws"></span>
        </div>
        <div class="perk-body">
          <p class="perk-k dot">02</p>
          <h3 class="disp h3">支え手の壁に、顔と名前が載る</h3>
          <p class="mu">このページのいちばん下の「支え手の壁」に、スキンの顔と MCID が並びます。載りたくなければ、ゲームの中で <span class="kbd">/akashi supporter hide</span> と打つだけ。名前の ❤ はそのまま残ります。</p>
        </div>
      </div>
    </div>
    <p class="note cold"><b>買えるものは、ありません。</b>灯原では、お金で強くなることはできません。マインクラフトの利用規約（EULA）とガイドラインに沿って、お礼は見た目だけにしています。</p>
  </div>
</section>

<section class="stratum s-stone" id="how">
  <div class="edge"></div>
  <div class="wrap">
    <h2 class="disp h2">支え方は、3つの手順。</h2>
    <ol class="flow">
      <li><span class="fl-n dot">1</span><div><h3>PayPay で送る</h3><p>下のボタンかQRコードから。金額は自由。メッセージ欄に <b>MCID</b> を書いてください。</p></div></li>
      <li><span class="fl-n dot">2</span><div><h3>Discord で知らせる</h3><p>灯原の Discord の <span class="kbd">{SUPPORT_CH}</span> に「送りました」と、MCID をひとこと。送ったときの画面の写しがあると、確かめるのが早くなります。</p></div></li>
      <li><span class="fl-n dot">3</span><div><h3>名前に ❤ がつく</h3><p>運営が確かめて、たいてい24時間以内に ❤ がつきます。ついたときは、画面にお礼が出ます。支え手の壁には、サイトの次の更新で載ります。</p></div></li>
    </ol>
    {_pay_panel()}
    <div class="btns" style="margin-top:20px"><a href="{DISCORD}" class="pbtn dbtn" target="_blank" rel="noopener">Discord を開く</a></div>
  </div>
</section>

<section class="stratum s-dusk" id="wall">
  <div class="edge"></div>
  <div class="wrap">
    <div class="wall-h"><h2 class="disp h2">支え手の壁</h2><p class="wall-n"><b class="dot">{len([s for s in SUPPORTERS if str(s.get("mcid", "")).strip()])}</b><span>人の灯が、この夜を照らしています</span></p></div>
    <p class="lead">灯原を支えてくれた人たちです。ここに並ぶ灯のひとつひとつが、サーバーの明日をつくっています。</p>
    {_wall()}
  </div>
</section>

<section class="stratum s-rock" id="faq">
  <div class="edge"></div>
  <div class="wrap narrow">
    <h2 class="disp h2">よくある質問</h2>
    <div class="faq">
      <details><summary>いくらから送れますか？</summary><p>100円からです。上限はありません。お礼はどの金額でも同じです。</p></details>
      <details><summary>❤ はいつまでつきますか？</summary><p>ずっとです。シーズンが変わっても残ります。</p></details>
      <details><summary>名前を変えたら、❤ は消えますか？</summary><p>消えません。一度入ったあとは、マインクラフトのアカウントでつながっているので、名前を変えてもそのままです。支え手の壁の名前も、次の更新で新しい名前になります。</p></details>
      <details><summary>統合版（スマホ・Switch など）でもつきますか？</summary><p>つきます。MCID は、名前の前の「.」も含めて書いてください。統合版の人は、支え手の壁ではスキンの代わりに灯原の顔が出ることがあります。</p></details>
      <details><summary>名前を出さずに支えたいです。</summary><p>できます。ゲームの中で <span class="kbd">/akashi supporter hide</span> と打つと、支え手の壁に載りません。Discord で知らせるときに「壁には載せないで」と書いてもらっても大丈夫です。</p></details>
      <details><summary>返金はできますか？</summary><p>寄付なので、お返しはできません。送る前に、金額をよく確かめてください。まちがえて送ったときは、Discord で運営に相談してください。</p></details>
      <details><summary>子どもでも送れますか？</summary><p>18歳より下の人は、かならずおうちの人に相談して、いいよと言ってもらってから送ってください。おうちの人の PayPay で送るときも同じです。</p></details>
      <details><summary>送ったお金は、何に使われますか？</summary><p>灯原を続けるための費用（サーバーの借り代・ドメイン・バックアップなど）に使います。</p></details>
    </div>
    <p class="mu legal-n">寄付は見返りを目的としない、任意のものです。お礼の ❤ と支え手の壁は、感謝のしるしとしてお渡しするもので、ゲームの中の有利さはありません。PayPay は PayPay株式会社の商標です。灯原は Mojang Studios・Microsoft とは関係ありません。</p>
  </div>
</section>
'''


notfound = f'''<div class="hero" style="min-height:70svh">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div><div class="moon" aria-hidden="true"></div>
  <div class="wrap phead" id="content">
    <p class="dot" style="color:var(--amber);font-size:20px">404　闇の中</p>
    <h1 class="disp h1-sub" style="margin-top:8px">ここには、灯りがありません。</h1>
    <p class="lead">お探しのページは見つかりませんでした。いちばん近い灯りは、こちらです。</p>
    <div class="btns" style="margin-top:28px"><a href="index.html" class="pbtn">トップへ戻る</a><a href="start.html" class="gbtn">入り方を見る</a></div>
  </div>
</div>'''


# ───────────────────────── ひとびと ─────────────────────────
_SCARF_NAME = ["琥珀", "桃", "空色", "若葉", "藤", "雪"]


def _appears(cid):
    out = []
    names = {"start.html": "はじめる", "guide.html": "遊び方", "events.html": "夜祭", "rules.html": "きまり", "support.html": "支える", "404.html": "迷子のページ", "commands.html": "コマンド", "wiki.html": "灯技 Wiki", "wiki-hiuo.html": "灯魚図鑑"}
    for f, r in RIDGE.items():
        if f in names and any(w == cid for w, *_ in r["cast"]):
            out.append((f, names[f]))
    for k, c in enumerate(CH):
        if _CH_WHO[c["id"]] == cid:
            out.append((f"guide-{c['id']}.html", f"第{k + 1}章 {c['t']}"))
    return out


def _pf(c):
    paths = "".join(f'<a href="wiki-{p["id"]}.html" style="--c:{_PCOL[i]}"><i>{p["k"]}</i>{p["name"]}</a>' for i, p in enumerate(HW["paths"]) if p["id"] in c["paths"])
    ap = "".join(f'<a href="{f}">{t}</a>' for f, t in _appears(c["id"])[:6])
    return f'''<article class="pf" id="{c["id"]}" style="--sc:{SCARF[c["k"] % 6]}">
      <div class="pf-st">{fig(c["id"], True)}</div>
      <div class="pf-b">
        <div class="pf-h"><h3>{c["n"]}</h3><span>{c["kj"]}　／　えりまき：{_SCARF_NAME[c["k"] % 6]}</span></div>
        <span class="pf-role">{c["role"]}</span>
        <p class="pf-q">{c["line"]}</p>
        <p class="pf-bio">{c["bio"]}</p>
        <dl class="pf-dl"><div><dt>好きなもの</dt><dd>{c["like"]}</dd></div><div><dt>得意な道</dt><dd>{paths}</dd></div><div><dt>出てくるところ</dt><dd>{ap}</dd></div></dl>
      </div>
    </article>'''


characters = sub_hero("characters.html", "灯原の、ひとびと。", "予告編に出てくる6人の旅人と、灯りを喰う影。このサイトのあちこちで、案内をしてくれます。",
                      [("cast", "6人の旅人"), ("foe", "灯喰いと夜の敵"), ("about", "この人たちのこと")]) + f'''
<section class="stratum tex s-soil" id="cast">
  <div class="wrap">
    <p class="depth">6人</p>
    <h2 class="disp h2">えりまきの色で、見分ける。</h2>
    <p class="lead">6人とも、同じフードのマントを着ています。ちがうのは、えりまきと、マントの色。名前はみんな、ふた文字です。</p>
    <div class="lineup" aria-hidden="true">{"".join(fig(c["id"], True) for c in CAST)}</div>
    {"".join(_pf(c) for c in CAST)}
  </div>
</section>

<section class="stratum s-blood" id="foe">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">闇の中</p>
    <h2 class="disp h2">灯りを、喰うもの。</h2>
    <p class="lead">6人が守っているのは、灯りです。灯りを狙うものと、闇から見ているもの。</p>
    <article class="pf foe" id="higui">
      <div class="pf-st">{eater()}</div>
      <div class="pf-b">
        <div class="pf-h"><h3>灯喰い</h3><span>ひぐい　／　すみれ色の目</span></div>
        <span class="pf-role">灯りの守りを破る、ただひとつの敵</span>
        <p class="pf-q">（なにも言わない）</p>
        <p class="pf-bio">黒い体に、白い面。夜になると、灯路のいちばん少ない「端」の灯籠へまっすぐ向かい、喰いはじめます。人には目もくれません。喰われた灯籠は青い冷たい火になり、守りも灯路も途切れます。倒せば欠片を落とし、夜明けには、つながっている灯籠へ火が戻ります。</p>
        <dl class="pf-dl"><div><dt>くわしく</dt><dd><a href="guide-higui.html">第3章 灯喰い</a></dd></div><div><dt>守りかた</dt><dd><a href="guide-lantern.html">灯籠どうしを、つなぐ</a></dd></div></dl>
      </div>
    </article>
    <article class="pf foe" id="reds" style="--sc:#FF3B30">
      <div class="pf-st" style="background:linear-gradient(180deg,#020205,#0B0710 80%)">{reds("pf-reds")}{reds("pf-reds")}</div>
      <div class="pf-b">
        <div class="pf-h"><h3>闇の目</h3><span>夜の敵　／　赤い目</span></div>
        <span class="pf-role" style="color:#fff">灯りの外にいるもの</span>
        <p class="pf-q">灯りの外へ出たら、見られている。</p>
        <p class="pf-bio">24分の夜に湧く敵たち。体力は2.5倍、攻撃は2倍で、夜を重ねるほど強くなります。灯りの中には入れず、中にいる人を狙えません。7夜に一度の朱月の夜には、さらに強く、群れと精鋭がふえます。</p>
        <dl class="pf-dl"><div><dt>くわしく</dt><dd><a href="guide-night.html">第2章 長い夜</a></dd></div><div><dt>朱月の夜</dt><dd><a href="events.html">夜祭「夜明けまで」</a></dd></div></dl>
      </div>
    </article>
  </div>
</section>

<section class="stratum s-rock" id="about">
  <div class="edge"></div>
  <div class="wrap narrow">
    <p class="depth">このページについて</p>
    <h2 class="disp h2">ゲームの中では、あなたが旅人。</h2>
    <p class="lead">6人は、予告編とこのサイトの案内役です。サーバーの中に、この6人が人物として出てくることはありません。灯原で灯籠を置き、夜を越えるのは、あなたです。</p>
    <div class="btns" style="margin-top:28px"><a href="start.html" class="pbtn">旅人になる（入り方）</a><a href="index.html#film" class="gbtn">予告編を見る</a></div>
  </div>
</section>
'''

# ───────────────────────── コマンド ─────────────────────────
def _cmd_rows(rows):
    out = ""
    for r in rows:
        _CMD_N[0] += 1
        c, a, d = r[0], r[1], r[2]
        need = f'<span class="need" title="この道の技を覚えると使えます">{r[3]}の技</span>' if len(r) > 3 else ""
        q = _E(c + " " + a + " " + _re0.sub("<[^>]+>", "", d))
        out += f'<div class="cr" id="k{_CMD_N[0]}" data-q="{q}"><code>{_E(c)}{" <i>" + _E(a) + "</i>" if a else ""}</code><span>{d}{need}</span></div>'
    return out


commands = sub_hero("commands.html", "コマンド一覧", "ふだんはメニューを押すだけで遊べます。直接打ちたい人のための、すべてのコマンドです。",
                    [(f"c{i}", g[2]) for i, g in enumerate(_CMDS)]) + f'''
<section class="stratum s-deep" id="cmds">
  <div class="wrap">
    {say_box("hino", "迷ったら <span class=\"kbd\">/menu</span>。統合版なら、押しやすいメニューが出るよ。")}
    <div class="finder">
      <label class="find"><span class="sr">コマンドを探す</span><input type="search" id="cq" placeholder="コマンド・できることで探す（例：灯渡り、色、番付）" autocomplete="off"><kbd class="dot">/</kbd></label>
      <p class="find-n mu" aria-live="polite"><b class="dot" id="cn">{sum(len(g[5]) for g in _CMDS)}</b> のコマンド <button type="button" class="clear" id="cclear" hidden>探すのをやめる</button></p>
      <div id="cl">{"".join(f'''<div class="cmdg" id="c{i}"><div class="cmdg-h" style="--c:{g[1]}"><span class="k">{g[0]}</span><h2 class="disp">{g[2]}</h2><p>{g[4]}</p></div>{_cmd_rows(g[5])}</div>''' for i, g in enumerate(_CMDS))}</div>
      <p class="wk-empty" id="cempty" hidden>見つかりませんでした。ことばを短くしてみてください。</p>
    </div>
    <p class="note" style="margin-top:44px"><b>統合版（スマホ・Switch など）の人へ。</b>コマンドを打たなくても、<span class="kbd">/tomoshibi</span>・<span class="kbd">/sato</span>・<span class="kbd">/akashi</span>・<span class="kbd">/waza</span> で押しやすい専用のメニューが開きます。</p>
  </div>
</section>
<script src="assets/wiki.js" defer></script>'''
commands = commands.replace('<div class="wrap phead" id="content">', '<div class="wrap phead" id="content">\n    ' + _wiki_switch("cmd"), 1)


# ───────────────────── 遊び方を選ぶ（みんなで・身内で・ひとりで） ─────────────────────
_K = lambda c: f'<span class="kbd">{c}</span>'

_PS = [
    {"id": "all", "who": "momo", "c": "#F29BB8", "t": "みんなで", "sub": "知らない人とも、広く",
     "lead": "人の灯路につなぐほど楽になる世界です。話しかけなくても、だれかの灯路のそばに置けば、もういっしょに遊んでいます。",
     "steps": [
         ("最初の広場のまわりで始める", "広場のまわりは、灯喰いに狙われません。"),
         ("だれかの灯路の16ブロック以内に置く", "灯路はだれの灯籠とでもつながり、5基で「二ノ灯」、15基で「三ノ灯」に上がります。"),
         ("灯標で行き来する", "二ノ灯より上なら、名前のついた灯籠へ3秒で移動できます。"),
         ("土曜21時の夜祭に出る", "何もしなければ参加です。ゲームは毎週かわります。"),
         ("友達を呼ぶ", "招待1人で「白銀」、3人で「藤」、5人で「曙」の色がもらえます。"),
     ],
     "cmds": [("/tomoshibi list", "行ける灯標"), ("/tomoshibi go 名前", "灯標へ移動"), ("/yomatsuri", "次の夜祭"), ("/tomoshibi invite", "招待コード")],
     "note": "人の建物には手を出さないでください。灯籠は守られていますが、建物は守られていません。"},
    {"id": "crew", "who": "waka", "c": "#8BD18F", "t": "身内で", "sub": "友達や家族と、自分たちの場所を",
     "lead": "友達や家族と、ひとつの拠点を育てる遊び方です。Java版と統合版がまざっていても、同じ世界に入れます。",
     "steps": [
         ("全員が同じアドレスで入る", f"{_K(ADDR)}。統合版はポートを {_K('5156')} に。"),
         ("呼んだ人の招待コードを入れる", f"入ってから7日以内に {_K('/tomoshibi code コード')}。"),
         ("おたがいを「仲間」にする", f"{_K('/tomoshibi trust 名前')}。仲間は、あなたの灯籠に名前をつけたり、取り除いたりできます。"),
         ("拠点をひとつの灯路網にする", "16ブロック以内に置けばつながります。みんなで置けば、すぐ二ノ灯です。"),
         ("集合場所の灯標をつくる", f"{_K('/tomoshibi name 集合')} で名前をつければ、全員 {_K('/tomoshibi go 集合')} で集まれます。"),
     ],
     "cmds": [("/tomoshibi trust 名前", "仲間にする・外す"), ("/tomoshibi name 名前", "灯標にする"), ("/tomoshibi home", "帰る場所へ"), ("/tomoshibi color 色", "灯りの色")],
     "note": "「仲間」は灯籠を取り除ける権利です。本当に信頼できる人だけにしてください。ほかの人とつなげたくなければ、人の灯路から16ブロック以上離れて建てます。"},
    {"id": "solo", "who": "sora", "c": "#8FC3E8", "t": "ひとりで", "sub": "自分のペースで、黙々と",
     "lead": "ひとりでも、最後まで遊べます。小さな拠点は守られていて、技と図鑑と証は自分のペースで埋められます。",
     "steps": [
         ("最初の24時間で拠点をつくる", "来てから24時間は、まわりに灯喰いが来ません。"),
         ("小さな拠点は狙われない", "灯籠が3基より少ない灯路網と、地下や高い塔の灯籠は狙われません。"),
         ("自分の灯籠を5基つなぐ", "ひとりでも二ノ灯になり、灯標どうしを行き来できます。"),
         ("灯技を育てる", f"{_K('/waza')}。遊んだ道の Lv が上がり、毎日3つの「今日の務め」もあります。"),
         ("図鑑と証を埋める", "灯魚は106種、灯の証は263個あります。"),
     ],
     "cmds": [("/waza", "灯技"), ("/waza fish", "灯魚図鑑"), ("/akashi", "灯の証"), ("/yomatsuri out", "夜祭を見送る")],
     "note": "迷ったら画面の下を見てください。灯りの外では、いちばん近い灯りの方角が出ます。"},
]


def playstyle():
    tabs = "".join(f'''<button type="button" class="tab ps-tab" role="tab" id="t-{m["id"]}" aria-controls="{m["id"]}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else ' tabindex="-1"'} style="--c:{m["c"]}"><span class="ps-fig">{fig(m["who"], True, "", "")}</span><span class="ps-tt"><b>{m["t"]}</b><small>{m["sub"]}</small></span></button>''' for i, m in enumerate(_PS))
    panels = ""
    for i, m in enumerate(_PS):
        steps = "".join(f'<li><div><h3>{a}</h3><p>{b}</p></div></li>' for a, b in m["steps"])
        cmds = "".join(f'<div><dt>{_K(a)}</dt><dd>{b}</dd></div>' for a, b in m["cmds"])
        panels += f'''<div class="ps-panel" role="tabpanel" id="{m["id"]}" aria-labelledby="t-{m["id"]}" style="--c:{m["c"]}"{"" if i == 0 else " hidden"}>
      <h2 class="disp h2">{m["t"]}遊ぶ。</h2>
      <p class="lead">{m["lead"]}</p>
      <ol class="steps">{steps}</ol>
      <dl class="ps-cmds">{cmds}</dl>
      <p class="ps-note">{m["note"]}</p>
    </div>'''
    hero = sub_hero("playstyle.html", "だれと、遊ぶ？", "遊び方に合わせて、最初にやることを5つにまとめました。", [])
    return hero + f'''
<section class="stratum s-deep ps">
  <div class="edge"></div>
  <div class="wrap narrow">
    <div class="ps-tabs" role="tablist" aria-label="遊び方">{tabs}</div>
    {panels}
    <p class="ps-more">コマンドを打たなくても、{_K("/tomoshibi")} のメニューから同じことができます。<a href="commands.html">すべてのコマンド</a></p>
  </div>
</section>'''


guide = _guide_index()
PAGES = [
    ("index.html", "灯原｜夜が24分つづく、灯りをつなぐマインクラフトサーバー", "灯籠を置いた場所だけが安全。灯りをつないで道をつくり、灯りを喰いに来る夜から守る。Java版・統合版対応、参加無料のサバイバルサーバー「灯原」。シーズン1は2026年11月7日21時開幕。", index),
    ("start.html", "はじめる｜灯原", "灯原への入り方を機種別に。Java版、スマホ、Windows、Switch・PS・Xbox。最初の夜の過ごし方と、よくある質問。", start),
    ("guide.html", "遊び方｜灯原", f"灯原のしくみを{len(CH)}の章で。灯籠と灯路、昼4分・夜24分の長い夜、灯りを消しに来る灯喰い、8つの加護、10の道・130の技「灯技」、106種の灯魚、{len(HM['defs'])}の特別な付呪「灯紋」、263の進捗「灯の証」、灯標と灯りの色、仲間と開く里と5つの職「灯里」、灯結。", guide),
] + [(f"guide-{c['id']}.html", f"{c['t']}｜遊び方｜灯原", c['desc'], chapter_page(k)) for k, c in enumerate(CH)] + [
    ("events.html", "夜祭｜灯原", "毎週土曜21時。120秒の募集で人数がそろえば自動で始まる、週替わり4種のゲーム。灯籠リレー、闇かくれんぼ、建築早押し、夜明けまで。", events),
    ("playstyle.html", "遊び方を選ぶ｜灯原", "みんなで・身内で・ひとりで。3つの遊び方ごとのマニュアル。はじめの5つ、よく使うコマンド、コツ、気をつけること。", playstyle()),
    ("rules.html", "きまり｜灯原", "灯原のきまり。してはいけないこと、しくみで守られていること、困ったときの連絡先、保護者の方へ。", rules),
] + WIKI_PAGES + AK_PAGES + HM_PAGES + HS_PAGES + [
    ("support.html", "支える｜灯原", "灯原を支える（寄付）。PayPay で金額は自由、100円から。お礼は名前につく ❤ と「支え手の壁」への掲載だけで、強さには関わりません。", support),
    ("characters.html", "ひとびと｜灯原", "灯原の案内役、6人の旅人（ヒノ・モモ・ソラ・ワカ・シノ・ユキ）と、灯りを喰う灯喰い、夜の敵。予告編に出てくるドット絵の登場人物たち。", characters),
    ("commands.html", "コマンド一覧｜灯原", "灯原のすべてのコマンド。灯原のメニュー（/menu）、灯籠と灯路（/tomoshibi）、灯里（/sato）、灯の証（/akashi）、灯技（/waza）、夜祭（/yomatsuri）、長い夜（/tokoyo）。", commands),
    ("404.html", "ページが見つかりません｜灯原", "お探しのページは見つかりませんでした。", notfound),
]
out = pathlib.Path(__file__).parent

import budoux
from bs4 import BeautifulSoup, NavigableString

PARSER = budoux.load_default_japanese_parser()
PHRASE = "h1,h2,h3,p,li,summary,th,td,a,button,span.addr-t small,.stat span,.legend span,b"
SKIP = {"script", "style", "code", "svg", "title"}


def finish(html):
    """日本語を文節の切れ目でだけ改行させる（<wbr> を入れ、CSS で keep-all にする）。幅の狭い画面では表を縦に積む。"""
    soup = BeautifulSoup(html, "html.parser")
    for el in soup.select(".depth, .band-y, .ch-big, .wb-k, .ch > ul, .say"):
        el.decompose()
    for el in soup.select(PHRASE):
        for node in list(el.descendants):
            if not isinstance(node, NavigableString) or node.parent is None:
                continue
            if any(p.name in SKIP or "kbd" in (p.get("class") or []) for p in node.parents if p.name):
                continue
            text = str(node)
            if len(text.strip()) < 6 or "<wbr>" in text:
                continue
            parts = PARSER.parse(text)
            merged = []
            for p in parts:
                if merged and (len(merged[-1].strip()) < 2 or len(p.strip()) < 2):
                    merged[-1] += p
                else:
                    merged.append(p)
            parts = merged
            if len(parts) < 2:
                continue
            frag = BeautifulSoup("<wbr>".join(p.replace("&", "&amp;").replace("<", "&lt;") for p in parts), "html.parser")
            node.replace_with(frag)
    for table in soup.find_all("table"):
        head = table.find("thead")
        if not head:
            continue
        labels = [th.get_text(strip=True) for th in head.find_all("th")]
        body = table.find("tbody")
        first_is_th = all(tr.find(["th", "td"], recursive=False).name == "th" for tr in body.find_all("tr"))
        longest = max((len(td.get_text(strip=True)) for td in body.find_all("td")), default=0)
        if len(labels) >= 3:
            table["class"] = (table.get("class") or []) + ["stack"]
        elif first_is_th and longest > 14:
            table["class"] = (table.get("class") or []) + ["stack2"]
        if "stack" in (table.get("class") or []):
            for td in body.find_all("td"):
                inner = soup.new_tag("span")
                for ch in list(td.contents):
                    inner.append(ch.extract())
                td.append(inner)
        for tr in table.find("tbody").find_all("tr"):
            i = 0
            for cell in tr.find_all(["th", "td"], recursive=False):
                span = int(cell.get("colspan", 1))
                if cell.name == "td":
                    cell["data-label"] = "効果" if span > 1 else (labels[i] if i < len(labels) else "")
                i += span
    return str(soup)


for f, t, d, b in PAGES:
    (out / f).write_text(finish(page(f, t, d, b)), encoding="utf-8")
# サイト内検索の索引（Ctrl+K）
_idx = []
for f, t, d, b in PAGES:
    if f == "404.html":
        continue
    _idx.append({"k": "ページ", "t": t.split("｜")[0], "s": d[:60], "u": f})
for i, p in enumerate(HW["paths"]):
    for n in p["nodes"]:
        _idx.append({"k": "技", "t": n["name"], "s": p["name"] + "・" + _desc(n)[:40], "u": f"wiki-{p['id']}.html#{n['id']}", "c": _PCOL[i]})
_RN = ["", "並", "良", "珍", "稀", "秘"]
for fsh in HW["fish"]:
    if fsh.get("name") and fsh["rarity"] <= 4:
        _idx.append({"k": "灯魚", "t": fsh["name"], "s": _RN[fsh["rarity"]] + "・" + "・".join(fsh["cond"][:1 if fsh["rarity"] == 4 else 3]), "u": f"wiki-hiuo.html#f-{fsh['id']}", "c": "#4FD8C8"})
for x in AK["defs"]:
    if not x["hidden"]:
        _idx.append({"k": "証", "t": x["name"], "s": AK["cats"][x["cat"]]["name"] + "・" + x["desc"][0], "u": f"akashi-{_AK_SLUG[x['cat']]}.html#{x['id']}", "c": _TCOL[x["tier"]]})
_kn = 0
for g in _CMDS:
    for r in g[5]:
        _kn += 1
        _idx.append({"k": "コマンド", "t": (r[0] + " " + r[1]).strip(), "s": _re0.sub("<[^>]+>", "", r[2])[:50], "u": f"commands.html#k{_kn}", "c": g[1]})
for x in HM["defs"]:
    _idx.append({"k": "紋", "t": x["name"], "s": HM["rarity"][x["r"]]["jp"] + "・" + x["on"] + "・" + x["desc"][0][:36], "u": f"himon.html#m-{x['id']}", "c": HM["rarity"][x["r"]]["hex"]})
for j in HS["jobs"]:
    _idx.append({"k": "職", "t": j["jp"], "s": j["role"] + "・匠の奉仕「" + j["service"] + "」", "u": f"guide-shoku.html#j-{j['key']}", "c": _HS_JC[j["key"]]})
for f in HS["facilities"]:
    _idx.append({"k": "施設", "t": f["jp"], "s": f["grade"] + "・" + f["text"][:40], "u": "hisato.html#facilities", "c": "#E9824A"})
(out / "assets" / "search.json").write_text(_wj.dumps(_idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
today = datetime.date.today().isoformat()
(out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{'' if f == 'index.html' else f}</loc><lastmod>{today}</lastmod></url>\n" for f, *_ in PAGES if f != "404.html") + "</urlset>\n", encoding="utf-8")
(out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
# 独自ドメインを使うときは、GitHub の Settings → Pages の Custom domain に入れる（CNAME はそこで自動で作られる）
print("built", len(PAGES))
