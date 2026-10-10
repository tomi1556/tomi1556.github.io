# 灯原サイトの組み立て（ヘッダーとフッターを各ページに入れて、静的な HTML を書き出す）
import datetime, pathlib

ADDR = "tomoshibara.life"
DISCORD = "https://discord.gg/wAKGQBHmPS"
SITE = "https://tomoshibara.life"
NAV = [("index.html", "トップ"), ("start.html", "はじめる"), ("guide.html", "遊び方"), ("events.html", "夜祭"), ("rules.html", "きまり")]

LOGO = '<svg width="30" height="36" viewBox="0 0 10 12" aria-hidden="true" style="display:block;shape-rendering:crispEdges"><rect x="2" y="0" width="6" height="1" fill="currentColor"/><rect x="1" y="1" width="8" height="1" fill="currentColor"/><rect x="1" y="2" width="1" height="6" fill="currentColor"/><rect x="8" y="2" width="1" height="6" fill="currentColor"/><rect x="2" y="2" width="6" height="6" fill="#F2B544"/><rect x="4" y="4" width="2" height="2" fill="#FFF1C4"/><rect x="1" y="8" width="8" height="1" fill="currentColor"/><rect x="4" y="9" width="2" height="3" fill="currentColor"/></svg>'


def addr_box(extra=""):
    return f'''<div class="addr"{extra}>
  <span class="addr-t"><small>サーバーアドレス（Java版・統合版 共通）</small><b>{ADDR}</b></span>
  <button type="button" class="pbtn" data-copy="{ADDR}">アドレスをコピー</button>
</div>
<p class="addr-note" data-note role="status">統合版のポートは 19132（最初から入っている数字のまま）です。</p>'''


# ナビのアイコン（16×16 のドット絵。# は線、o は灯りの色）
ICONS = {
    "index.html": ["......####......", ".....######.....", ".....#....#.....", ".....#oooo#.....", ".....#oooo#.....", ".....#oooo#.....", ".....#oooo#.....", ".....######.....", ".......##.......", ".......##.......", ".......##.......", ".......##.......", ".......##.......", "......####......", ".....######.....", "................"],
    "start.html": ["................", "...##########...", "...#........#...", "...#........#...", "...#....#...#...", "...#....##..#...", "...#.######.#...", "...#.#######o...", "...#.######.#...", "...#....##..#...", "...#....#...#...", "...#........#...", "...#........#...", "...##########...", "................", "................"],
    "guide.html": ["................", "................", ".######..######.", ".#....#..#....#.", ".#.oo.#..#.oo.#.", ".#....#..#....#.", ".#.oo.#..#.oo.#.", ".#....#..#....#.", ".#.oo.#..#.oo.#.", ".#....#..#....#.", ".#....####....#.", ".##############.", "................", "................", "................", "................"],
    "events.html": ["................", "......####......", ".......##.......", ".....######.....", "....#oooooo#....", "...#oooooooo#...", "...##########...", "...#oooooooo#...", "...#oooooooo#...", "...##########...", "...#oooooooo#...", "....#oooooo#....", ".....######.....", ".......##.......", "......####......", "................"],
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
  <a href="{DISCORD}" class="pbtn dbtn sm" target="_blank" rel="noopener">Discord に参加</a>
</div></header>'''


def footer():
    links = "".join(f'<a href="{h}" class="fl">{t}</a>' for h, t in NAV[1:])
    return f'''<footer class="foot s-rock"><div class="edge"></div><div class="wrap">
  <h2 class="disp" style="font-size:clamp(30px,4.6vw,56px);line-height:1.3;margin-bottom:24px">夜は、ひとりより大勢で。</h2>
  {addr_box()}
  <div class="btns" style="margin-top:8px"><a href="start.html" class="gbtn">入り方を見る</a><a href="{DISCORD}" class="pbtn dbtn" target="_blank" rel="noopener">Discord に参加</a></div>
  <div class="foot-links">
    <nav aria-label="フッター" style="display:flex;flex-wrap:wrap;gap:2px 8px">{links}<a href="{DISCORD}" class="fl" target="_blank" rel="noopener">Discord</a></nav>
    <p class="legal">灯原は非公式のファンサーバーです。Mojang Studios および Microsoft とは関係ありません。Minecraft は Mojang Synergies AB の商標です。</p>
  </div>
</div></footer>
<div class="gauge" aria-hidden="true"><i></i></div>'''


def page(file, title, desc, body, hero_min=""):
    cur = file if file in dict(NAV) else ("guide.html" if file.startswith("guide-") else "")
    url = SITE + ("/" if file == "index.html" else "/" + file)
    return f'''<!doctype html>
<html lang="ja">
<head>
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
    <nav class="toc" aria-label="このページの内容">{t}</nav>
  </div>
</div>'''


def cd(kind, label):
    return f'''<div class="cd" role="timer" aria-label="{label}" data-{kind}-cd>
  <div class="cd-u"><b data-u="d">–</b><span>日</span></div><div class="cd-u"><b data-u="h">––</b><span>時間</span></div><div class="cd-u"><b data-u="m">––</b><span>分</span></div><div class="cd-u"><b data-u="s">––</b><span>秒</span></div>
</div>'''


# ───────────────────────── トップ ─────────────────────────
index = f'''<div class="hero" style="min-height:min(900px,100svh)">
  <div class="sky"></div><div class="stars" aria-hidden="true"></div><div class="moon" aria-hidden="true"></div><div class="dusk" aria-hidden="true"></div>
  <div class="wrap hero-body" id="content">
    <a href="#season" class="chip fadein"><i></i><span>シーズン1「灯ノ海」</span><b data-season-short>11月7日（土）21:00 開幕</b></a>
    <span class="online" data-online><i></i>いま <b>0</b> 人が参加中</span>
    <h1 class="disp h1 reveal">灯りをつないで、<br>夜の果てまで。</h1>
    <p class="lead lead-hero fadein">灯原は、夜が24分つづくサバイバルサーバーです。灯籠を置いた場所だけが安全で、灯籠どうしがつながると道になります。Java版でも統合版（スマホ・Switch・PC）でも、同じ世界に入れます。参加は無料です。</p>
    <div class="fadein" style="margin-top:32px">
      {addr_box()}
      <div class="btns" style="margin-top:6px"><a href="start.html" class="gbtn">はじめての方へ</a><a href="#film" class="gbtn">予告編を見る</a></div>
    </div>
  </div>
  <div class="scene" data-scene aria-hidden="true"></div>
</div>

<section class="stratum tex s-soil">
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

<section class="s-stone" style="position:relative">
  <div class="edge"></div>
  <div class="wrap" style="padding-top:96px;padding-bottom:36px">
    <p class="depth">Y=0</p>
    <h2 class="disp h2">つづきは、こちらから。</h2>
  </div>
  <a href="start.html" class="band" style="background:#50555C"><div class="wrap band-in"><span class="band-y">Y=−12</span><div class="band-body"><h3 class="disp h3">はじめる</h3><p class="lead">機種ごとの入り方と、最初の夜の過ごし方。3分で入れます。</p><span class="band-go"><i></i>入り方を見る</span></div></div></a>
  <a href="guide.html" class="band" style="background:#474C53"><div class="wrap band-in"><span class="band-y">Y=−24</span><div class="band-body"><h3 class="disp h3">遊び方</h3><p class="lead">灯籠と灯路、長い夜、灯喰い、欠片で解放する加護、263の「灯の証」、130の技と106種の灯魚「灯技」。</p><span class="band-go"><i></i>しくみを読む</span></div></div></a>
  <a href="events.html" class="band" style="background:#3E4249"><div class="wrap band-in"><span class="band-y">Y=−36</span><div class="band-body"><h3 class="disp h3">夜祭</h3><p class="lead">毎週土曜21時。人数がそろうと、週替わりのゲームが自動で始まります。</p><span class="band-go"><i></i>今週のゲームを見る</span></div></div></a>
  <a href="rules.html" class="band" style="background:#34383E;padding-bottom:40px"><div class="wrap band-in"><span class="band-y">Y=−48</span><div class="band-body"><h3 class="disp h3">きまり</h3><p class="lead">してはいけないこと、守られていること、困ったときの連絡先。</p><span class="band-go"><i></i>きまりを読む</span></div></div></a>
</section>

<section class="stratum s-rock" id="film">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">Y=−60</p>
    <h2 class="disp h2">予告編</h2>
    <p class="lead">64秒。音が出ます。</p>
    <div class="film"><video controls preload="none" playsinline poster="assets/trailer-poster.jpg"><source src="assets/trailer.mp4" type="video/mp4">お使いのブラウザでは動画を再生できません。</video></div>
  </div>
</section>

<section class="stratum s-dusk" id="fest" style="padding-top:72px">
  <div class="edge"></div>
  <div class="garland" data-garland aria-hidden="true"></div>
  <div class="wrap" style="display:flex;flex-wrap:wrap;gap:40px 64px;align-items:flex-end">
    <div style="flex:1 1 440px;min-width:0">
      <p class="depth">次の夜祭</p>
      <h2 class="disp h2" style="margin-bottom:8px" data-fest-date>毎週土曜 21:00</h2>
      <p class="mu" style="margin-bottom:22px" data-fest-lead>21時になると、120秒の募集が始まります。何もしなければ参加です。</p>
      {cd("fest", "次の夜祭まで")}
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
        <li><div><h3>3つの欄を入れる</h3><p>サーバー名：<span class="kbd">灯原</span>　サーバーアドレス：<span class="kbd">{ADDR}</span>　ポート：<span class="kbd">19132</span></p></div></li>
        <li><div><h3>「保存」を押し、一覧から「灯原」を選ぶ</h3><p>統合版の人には、押しやすい専用のメニューが出ます。</p></div></li>
      </ol>
    </div>
    <div class="tabpanel" role="tabpanel" id="p-win" aria-labelledby="t-win" hidden>
      <ol class="steps">
        <li><div><h3>Minecraft（統合版）を開いて「遊ぶ」を押す</h3><p>Minecraft Launcher では「Minecraft for Windows」を選びます。Java版とは別のものです。</p></div></li>
        <li><div><h3>「サーバー」のタブを開き、いちばん下の「サーバーを追加」を押す</h3><p>一覧を下までスクロールすると出てきます。</p></div></li>
        <li><div><h3>3つの欄を入れる</h3><p>サーバー名：<span class="kbd">灯原</span>　サーバーアドレス：<span class="kbd">{ADDR}</span>　ポート：<span class="kbd">19132</span></p></div></li>
        <li><div><h3>「保存」を押し、一覧から「灯原」を選ぶ</h3><p>Java版を持っているなら、Java版から入ってもかまいません。同じ世界です。</p></div></li>
      </ol>
    </div>
    <div class="tabpanel" role="tabpanel" id="p-con" aria-labelledby="t-con" hidden>
      <p class="note warn"><b>ゲーム機は、ひと手間かかります。</b>Switch・PlayStation・Xbox のマインクラフトには「サーバーを追加」のボタンがありません。本体のネットワーク設定（DNS）を変える方法で入れますが、手順が機種ごとにちがいます。</p>
      <ol class="steps" style="margin-top:20px">
        <li><div><h3>Discord に参加する</h3><p>「はじめての方」に、機種ごとの手順を画像つきで置いています。わからないところは、その場で聞けます。</p></div></li>
        <li><div><h3>手順どおりに本体の設定を変える</h3><p>設定は、いつでも元に戻せます。保護者の方といっしょに行ってください。</p></div></li>
        <li><div><h3>マインクラフトの「サーバー」から灯原を選ぶ</h3><p>アドレスは <span class="kbd">{ADDR}</span>、ポートは <span class="kbd">19132</span> です。</p></div></li>
      </ol>
      <div class="btns" style="margin-top:20px"><a href="{DISCORD}" class="pbtn dbtn" target="_blank" rel="noopener">Discord で手順を見る</a></div>
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
      <li><time>5分</time><div><h3>メニューを開く</h3><p>チャットに <span class="kbd">/tomoshibi</span> と打つか、何も持たずに灯籠を右クリック（統合版は長押し）します。「はじめの一歩」が6つあり、1つ達成するたびに灯籠を2基もらえます。</p></div></li>
      <li><time>夜</time><div><h3>灯りの中で過ごす</h3><p>画面の下に「灯りの中」と出ていれば安全です。灯りの外に出ると「闇の中」と出て、いちばん近い灯りの方角を教えてくれます。</p></div></li>
      <li><time>いつでも</time><div><h3>灯の証を見る</h3><p><span class="kbd">/akashi</span> で、灯原だけの進捗「灯の証」が開きます。全部で263個。すぐ届くものから、季節をまたぐものまであります。</p></div></li>
      <li><time>いつでも</time><div><h3>技を育てる</h3><p><span class="kbd">/waza</span> で「灯技」が開きます。掘る・切る・釣る・旅をする…遊んだ道の Lv が上がり、技点で技を覚えます。毎日3つの「今日の務め」もあります。</p></div></li>
      <li><time>慣れたら</time><div><h3>人の灯りと、つなぐ</h3><p>だれの灯籠とでも灯路はつながります。5基つながると「二ノ灯」になり、守られる範囲が広がって、灯標どうしを行き来できるようになります。</p></div></li>
    </ol>
    <p class="note cold"><b>来たばかりの人は守られています。</b>はじめて入ってから24時間は、あなたのまわりに灯喰いは来ません。灯籠が3基より少ない拠点も狙われません。</p>
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
      <details><summary>ひとりでも遊べますか</summary><p>遊べます。ただ、この世界は灯りをつなぐほど楽になるように作ってあります。だれかの灯路のそばに灯籠を置くだけで、もう「いっしょに遊んでいる」ことになります。</p></details>
      <details><summary>いない間に、こわされませんか</summary><p>ほかの人の灯籠は壊せません。灯喰いが狙うのは、近くに人がいる灯籠だけなので、留守の間に灯りが消されることもありません。建物をこわされたときは、きまりのページの手順で知らせてください。</p></details>
      <details><summary>ランタンを置いたのに、灯りになりません</summary><p>灯路網につながるのは、光る「灯籠」だけです。ふつうのランタンは飾りになります。灯籠は作業台で、真ん中にランタン、上下にアメジストの欠片、左右に金インゴットを置くと作れます（<span class="kbd">/tomoshibi recipe</span>）。灯籠を壊すと、灯籠のまま戻ります。</p></details>
      <details><summary>夜の敵が強すぎます</summary><p>そのとおりで、最初は勝てないように作ってあります。灯りの中にいれば襲われません。敵は灯りに入れず、外から狙うこともできません。敵や灯喰いが落とす「欠片」を集めて加護を解放していくと、少しずつ戦えるようになります。</p></details>
      <details><summary>動きが重いです</summary><p><span class="kbd">/tomoshibi particles low</span> で光の粒が半分になり、<span class="kbd">off</span> で消えます。統合版の人は、最初から少なめになっています。</p></details>
      <details><summary>動画や配信にしてもいいですか</summary><p>かまいません。許可はいりません。ほかの人の名前が映るので、いやがる人がいたら映さないようにしてください。</p></details>
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
    "more": ["................", ".......##.......", "..##########....", "..#oooooooo##...", "..#oooooooo###..", "..#oooooooo##...", "..##########....", ".......##.......", "....##########..", "...##oooooooo#..", "..###oooooooo#..", "...##oooooooo#..", "....##########..", ".......##.......", ".......##.......", "......####......"],
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
     "sum": "遊ぶほど育つ10の道。技点で130の技を覚える。", "facts": ["10の道", "130の技", "今日の務め"],
     "desc": "灯技（ひわざ）。10の道・130の技、技の木の見方、灯力、主技と副技、今日の務めと極み。"},
    {"id": "fish", "t": "灯魚", "c": "#4FD8C8", "layer": 1, "sec": [],
     "sum": "時と場所と月でかわる、106種の魚。珍しいほど逃げる。", "facts": ["106種", "5つの珍しさ", "ヌシ"],
     "desc": "灯魚（ひうお）106種。珍しさ、かかる条件（水辺・時刻・天気・月・季節・朱月・灯り）、図鑑と灯原一。"},
    {"id": "akashi", "t": "灯の証", "c": "#F29BB8", "layer": 2, "sec": ["akashi"],
     "sum": "この世界で過ごしたことが、そのまま証になる。", "facts": ["263の証", "位階10段", "称号69種"],
     "desc": "灯原だけの進捗「灯の証」263個。難度、段と秘められた証、報酬、証点と位階。"},
    {"id": "more", "t": "灯標・色・招待", "c": "#C9D0DC", "layer": 2, "sec": ["more"],
     "sum": "名前をつけて行き来し、灯りの色を変え、友を呼ぶ。", "facts": ["灯渡り 3秒", "灯りの色 17色", "招待コード"],
     "desc": "灯標と灯渡り、仲間、17の灯りの色の手に入れ方、友達の招待のしかた。"},
]
LAYERS = [("第一層", "はじめに知ること", "ここまで読めば、最初の夜を越えられます。"),
          ("第二層", "強くなる", "慣れてきたら。育てるほど、暮らしが楽になります。"),
          ("第三層", "残す・つなぐ", "長く遊ぶほど、残るものがふえます。")]

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
    <p class="note cold"><b>放置した釣り場では、灯魚はかかりません。</b>視点が5分動かないあいだは、灯魚も経験値も出ません。</p>
  </div>
</section>
'''


def _body(k):
    c = CH[k]
    if c["id"] == "hiwaza":
        return _hiwaza_sec()
    if c["id"] == "fish":
        return _fish_sec()
    return "\n".join(_clean(_SEC[s]) for s in c["sec"])


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
            return f'<a href="guide.html" class="pg {cls}" style="--c:var(--amber)"><small class="dot">{label}</small><b>目次にもどる</b><span class="mu">8つの章の一覧へ</span></a>'
        return f'<a href="guide-{x["id"]}.html" class="pg {cls}" style="--c:{x["c"]}"><small class="dot">{label} {i + 1:02d}</small><b>{x["t"]}</b><span class="mu">{x["sum"]}</span></a>'

    pager = f'''<section class="stratum s-rock pager-s">
  <div class="edge"></div>
  <div class="wrap">
    <nav class="pager" aria-label="前後の章">{pg(prev, k - 1, "prev", "← 前の章")}{pg(nxt, k + 1, "next", "次の章 →")}</nav>
    <p class="pager-toc"><a href="guide.html" class="gbtn sm">≡ 遊び方の目次</a></p>
  </div>
</section>'''
    return hero + "\n" + _body(k) + "\n" + pager


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
    <p class="lead">灯りを置き、つなぎ、夜から守り、育てて、残す。灯原のしくみを8つの章にまとめました。気になる章から開いてください。</p>
    {_rail(-1)}
  </div>
</div>
<section class="stratum s-deep gi">
  <div class="edge"></div>
  <div class="wrap">
    <div class="gi-start">{pix(CH_ICONS["lantern"], "ch-ic lit")}<p><b>はじめての人は、第一層の3章だけで大丈夫です。</b>灯籠を置き、夜を知り、灯喰いから守れれば、最初の夜は越えられます。ほかの章は、遊びながらでどうぞ。</p><a href="guide-lantern.html" class="pbtn">第1章から読む</a></div>
    {layers}
  </div>
</section>'''


guide = _guide_index()

# ───────────────────────── 夜祭 ─────────────────────────
events = f'''<div class="hero">
  <div class="sky" style="background:linear-gradient(180deg,#0B0C24 0%,#211A46 55%,#4A2F66 100%)"></div><div class="stars" aria-hidden="true"></div>
  <div class="garland" data-garland aria-hidden="true" style="margin-top:8px"></div>
  <div class="wrap phead" id="content" style="padding-top:8px">
    <h1 class="disp h1-sub">毎週土曜21時は、夜祭。</h1>
    <p class="lead">この時間にログインすれば、かならずだれかがいます。人数がそろうと、週替わりのゲームが自動で始まります。</p>
    <div style="display:flex;flex-wrap:wrap;gap:32px 56px;align-items:flex-end;margin-top:32px">
      <div><p class="depth">次の夜祭</p><p class="disp" style="font-size:clamp(26px,3.4vw,40px);line-height:1.3;margin:6px 0 14px" data-fest-date>毎週土曜 21:00</p>{cd("fest", "次の夜祭まで")}</div>
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

# ───────────────────────── きまり ─────────────────────────
rules = sub_hero("rules.html", "きまり", "むずかしいことはありません。人のものをこわさない。人をいやな気持ちにさせない。この二つです。",
                 [("dont", "してはいけないこと"), ("safe", "守られていること"), ("penalty", "やぶったとき"), ("help", "困ったとき"), ("parents", "保護者の方へ")]) + f'''
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

<section class="stratum s-deep" id="penalty">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">対応の流れ</p>
    <h2 class="disp h2">きまりをやぶったとき</h2>
    <p class="lead">まちがいは、だれにでもあります。はじめは注意から始めます。ただし、わざと人のものをこわす、ずるをする、人を傷つけることばを使う、といった場合は、すぐに参加を止めることがあります。</p>
    <div class="ladder">
      <div><b>注意</b><span>何がいけなかったかを伝えます。</span></div>
      <div><b>一時的に止める</b><span>数日のあいだ、入れなくなります。</span></div>
      <div><b>長く止める</b><span>くり返した場合、期間がのびます。</span></div>
      <div><b>無期限に止める</b><span>悪質な場合、または何度もくり返した場合。</span></div>
    </div>
    <p class="note">止められた理由に納得がいかないときは、Discord で運営に伝えてください。記録を見直して、返事をします。</p>
  </div>
</section>

<section class="stratum s-dusk" id="help">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">連絡先</p>
    <h2 class="disp h2">困ったとき</h2>
    <p class="lead">こわされた、とられた、いやなことを言われた、ずるをしている人を見た。どれも Discord で運営に知らせてください。やり返さないことが、いちばん早く解決します。</p>
    <ol class="steps" style="margin-top:28px">
      <li><div><h3>その場をはなれる</h3><p>言い返したり、こわし返したりしないでください。あなたまで注意されてしまいます。</p></div></li>
      <li><div><h3>4つのことをメモする</h3><p>いつ（日にちと、だいたいの時間）。どこで（F3 キーや設定で出る座標）。だれが（相手の名前）。何をされたか。画面の写真があれば、なお助かります。</p></div></li>
      <li><div><h3>Discord で運営に送る</h3><p>ほかの人に見られたくない内容は、運営あての個別の連絡で送れます。</p></div></li>
    </ol>
    <div class="btns" style="margin-top:24px"><a href="{DISCORD}" class="pbtn dbtn" target="_blank" rel="noopener">Discord を開く</a></div>
  </div>
</section>

<section class="stratum s-rock" id="parents">
  <div class="edge"></div>
  <div class="wrap narrow">
    <p class="depth">保護者の方へ</p>
    <h2 class="disp h2">お子さまが遊ぶ前に</h2>
    <div class="faq">
      <details open><summary>費用はかかりますか</summary><p>かかりません。サーバーへの参加は無料で、ゲーム内に課金の仕組みはありません。マインクラフト本体と、機種によってはオンラインプレイの加入が別に必要です。</p></details>
      <details><summary>知らない人と話すことになりますか</summary><p>ほかの参加者と文字で会話できます。本名や住所、学校などを書いたり聞いたりすることは禁止しており、見つけた場合は運営が対応します。マインクラフトの設定で、チャットを表示しないようにもできます。</p></details>
      <details><summary>Discord は必要ですか</summary><p>遊ぶだけなら必要ありません。お知らせと問い合わせに使っています。Discord は利用規約で13歳以上が対象です。13歳未満のお子さまの場合は、保護者の方が代わりにご連絡ください。</p></details>
      <details><summary>どんな情報が保存されますか</summary><p>ゲーム内の名前、接続の記録（IPアドレスを含みます）、ゲーム内での行動の記録です。運営と不正への対応のためだけに使い、外部に提供しません。</p></details>
      <details><summary>ゲーム機から入るときの設定変更は安全ですか</summary><p>本体のネットワーク設定のうち、DNS という項目を変更します。いつでも元に戻せますが、かならず保護者の方が内容を確かめたうえで行ってください。</p></details>
      <details><summary>このサーバーは公式のものですか</summary><p>いいえ。灯原は有志が運営する非公式のサーバーで、Mojang Studios および Microsoft とは関係ありません。</p></details>
    </div>
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

PAGES = [
    ("index.html", "灯原｜夜が24分つづく、灯りをつなぐマインクラフトサーバー", "灯籠を置いた場所だけが安全。灯りをつないで道をつくり、灯りを喰いに来る夜から守る。Java版・統合版対応、参加無料のサバイバルサーバー「灯原」。シーズン1は2026年11月7日21時開幕。", index),
    ("start.html", "はじめる｜灯原", "灯原への入り方を機種別に。Java版、スマホ、Windows、Switch・PS・Xbox。最初の夜の過ごし方と、よくある質問。", start),
    ("guide.html", "遊び方｜灯原", "灯原のしくみを8つの章で。灯籠と灯路、昼4分・夜24分の長い夜、灯りを消しに来る灯喰い、8つの加護、10の道・130の技「灯技」、106種の灯魚、263の進捗「灯の証」、灯標と灯りの色。", guide),
] + [(f"guide-{c['id']}.html", f"{c['t']}｜遊び方｜灯原", c['desc'], chapter_page(k)) for k, c in enumerate(CH)] + [
    ("events.html", "夜祭｜灯原", "毎週土曜21時。120秒の募集で人数がそろえば自動で始まる、週替わり4種のゲーム。灯籠リレー、闇かくれんぼ、建築早押し、夜明けまで。", events),
    ("rules.html", "きまり｜灯原", "灯原のきまり。してはいけないこと、しくみで守られていること、困ったときの連絡先、保護者の方へ。", rules),
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
today = datetime.date.today().isoformat()
(out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{'' if f == 'index.html' else f}</loc><lastmod>{today}</lastmod></url>\n" for f, *_ in PAGES if f != "404.html") + "</urlset>\n", encoding="utf-8")
(out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
# 独自ドメインを使うときは、GitHub の Settings → Pages の Custom domain に入れる（CNAME はそこで自動で作られる）
print("built", len(PAGES))
