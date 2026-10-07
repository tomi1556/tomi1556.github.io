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


def header(cur):
    links = "".join(f'<a href="{h}" class="nl"{" aria-current=\"page\"" if h == cur else ""}><i></i>{t}</a>' for h, t in NAV)
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
  {header(cur)}
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
  {header("index.html")}
  <div class="wrap hero-body" id="content">
    <a href="#season" class="chip fadein"><i></i><span>シーズン1「灯ノ海」</span><b data-season-short>11月7日（土）21:00 開幕</b></a>
    <span class="online" data-online><i></i>いま <b>0</b> 人が参加中</span>
    <h1 class="disp h1 reveal">灯りをつないで、<br>夜の果てまで。</h1>
    <p class="lead fadein" style="margin-top:26px;font-size:18px">灯原は、夜が24分つづくサバイバルサーバーです。灯籠を置いた場所だけが安全で、灯籠どうしがつながると道になります。Java版でも統合版（スマホ・Switch・PC）でも、同じ世界に入れます。参加は無料です。</p>
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
      <div class="fact"><div class="fact-n">10<small>ブロック</small></div><div><h3 class="h3 disp">灯りの中は安全。</h3><p>灯籠（ランタン）を置くと、まわり半径10ブロックには敵が湧きません。爆発で壊れず、倒れても持ち物を失いません。近くの灯籠どうしは灯路でつながり、その上は足が速くなります。</p></div></div>
      <div class="fact"><div class="fact-n" style="color:var(--violet)">灯喰い</div><div><h3 class="h3 disp">夜は、灯りを消しに来る。</h3><p>夜になると「灯喰い」が灯籠を狙います。喰われた灯籠は青い冷たい火になり、道も途切れます。倒して守るか、あとで灯し直すか。つながりの多い灯籠ほど、喰われにくくなります。</p></div></div>
    </div>
  </div>
</section>

<section class="stratum s-deep" id="try">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">Y=24</p>
    <h2 class="disp h2">30秒で、ためしてみる。</h2>
    <p class="lead">マスを押して灯籠を置き、「夜にする」を押してください。灯喰いが来たら、押して倒します。<span class="sp"> 地図は横に動かせます。</span></p>
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
  <a href="guide.html" class="band" style="background:#474C53"><div class="wrap band-in"><span class="band-y">Y=−24</span><div class="band-body"><h3 class="disp h3">遊び方</h3><p class="lead">灯籠と灯路、長い夜、灯喰い、敵が落とす欠片で解放する加護。</p><span class="band-go"><i></i>しくみを読む</span></div></div></a>
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
      <li><time>0分</time><div><h3>灯籠を3基受け取る</h3><p>はじめて入ると、持ち物に灯籠（ランタン）が3基入ります。</p></div></li>
      <li><time>1分</time><div><h3>1基目を置く</h3><p>置いた場所のまわり半径10ブロックが「灯りの中」になります。敵が湧かず、爆発で壊れず、倒れても持ち物を失いません。最初の1基は無料です。</p></div></li>
      <li><time>3分</time><div><h3>2基目を、16ブロック以内に置く</h3><p>2基が「灯路」でつながります。灯路の上は足が速くなり、つなげて置くと経験値ももらえます。</p></div></li>
      <li><time>5分</time><div><h3>メニューを開く</h3><p>チャットに <span class="kbd">/tomoshibi</span> と打つか、何も持たずに灯籠を右クリック（統合版は長押し）します。「はじめの一歩」が6つあり、1つ達成するたびに灯籠を2基もらえます。</p></div></li>
      <li><time>夜</time><div><h3>灯りの中で過ごす</h3><p>画面の下に「灯りの中」と出ていれば安全です。灯りの外に出ると「闇の中」と出て、いちばん近い灯りの方角を教えてくれます。</p></div></li>
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
    <div class="tbl-wrap"><table>
      <thead><tr><th>打つもの</th><th>できること</th></tr></thead>
      <tbody>
        <tr><td class="n">/tomoshibi</td><td>メニューを開く（<span class="kbd">/tomo</span> でも同じ）</td></tr>
        <tr><td class="n">/tomoshibi buffs</td><td>加護を見る、欠片で解放する</td></tr>
        <tr><td class="n">/tomoshibi go 名前</td><td>名前のついた灯籠（灯標）へ移動する</td></tr>
        <tr><td class="n">/tomoshibi home</td><td>「帰る場所」に決めた灯標へ戻る</td></tr>
        <tr><td class="n">/tomoshibi invite</td><td>自分の招待コードを見る</td></tr>
        <tr><td class="n">/tomoshibi particles low</td><td>光の粒を減らす（動きが重いとき）</td></tr>
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
      <details><summary>夜の敵が強すぎます</summary><p>そのとおりで、最初は勝てないように作ってあります。灯りの中にいれば襲われません。敵や灯喰いが落とす「欠片」を集めて加護を解放していくと、少しずつ戦えるようになります。</p></details>
      <details><summary>動きが重いです</summary><p><span class="kbd">/tomoshibi particles low</span> で光の粒が半分になり、<span class="kbd">off</span> で消えます。統合版の人は、最初から少なめになっています。</p></details>
      <details><summary>動画や配信にしてもいいですか</summary><p>かまいません。許可はいりません。ほかの人の名前が映るので、いやがる人がいたら映さないようにしてください。</p></details>
      <details><summary>困ったときは、どこに聞けばいいですか</summary><p>Discord で聞いてください。入り方、遊び方、こわされた・いやなことをされた、どれでも受けつけています。</p></details>
    </div>
  </div>
</section>
'''

# ───────────────────────── 遊び方 ─────────────────────────
guide = sub_hero("guide.html", "遊び方", "灯りを置き、つなぎ、夜から守り、欠片を集めて強くなる。この世界のしくみを、順番に。",
                 [("lantern", "灯籠と灯路"), ("night", "長い夜"), ("higui", "灯喰い"), ("buff", "加護と欠片"), ("more", "灯標・色・招待")]) + f'''
<section class="stratum tex s-soil" id="lantern">
  <div class="wrap">
    <p class="depth">1</p>
    <h2 class="disp h2">灯籠を置くと、そこが安全になる。</h2>
    <p class="lead">ランタンを置くと「灯籠」として登録されます。ソウルランタンや銅のランタンでもかまいません。</p>
    <div class="two">
      <div><h3 class="h3 disp">灯りの中で起きること</h3><p class="mu">敵が自然に湧かない。爆発でブロックが壊れない。倒れても持ち物と経験値を失わない。画面の下に、いま灯りの中か外かが出ます。</p></div>
      <div><h3 class="h3 disp">灯路</h3><p class="mu">16ブロック以内の灯籠どうしは、自動で灯路につながります（1基につき4本まで）。灯路の上は足が速くなります。だれの灯籠とでもつながります。</p></div>
    </div>
    <h3 class="h3 disp" style="margin-top:56px">つながるほど、格が上がる。</h3>
    <p class="lead">灯路でつながった灯籠のまとまりを「灯路網」と呼びます。基数がふえると格が上がり、守られる範囲が広がって、まわりが本当に明るくなります。</p>
    <div class="tbl-wrap"><table>
      <thead><tr><th>格</th><th>つながった基数</th><th>守られる半径</th><th>できるようになること</th></tr></thead>
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
        <tr><th>同じチャンクに3基目</th><td>灯籠にならず、ふつうのランタンとして置かれる（1チャンク2基まで）</td></tr>
      </tbody>
    </table></div>
    <p class="note">ぎゅうぎゅうに置くより、少しはなして外へのばすほうが得になるようにしてあります。</p>
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
    <p class="lead">黒い体に白い面。人には目もくれず、灯籠へまっすぐ歩いてきます。</p>
    <ol class="steps" style="margin-top:36px">
      <li><div><h3>狙われる</h3><p>夜、人の近く（48ブロック以内）にある灯籠のうち、灯路がいちばん少ない「端」の1基が狙われます。</p></div></li>
      <li><div><h3>知らせが出る</h3><p>画面の下に「北東の灯が狙われている（32m）」と、方角と距離が出ます。</p></div></li>
      <li><div><h3>喰いはじめる</h3><p>灯籠に取りつくと紫に光り、灯籠から光を吸いはじめます。喰い終わるまでの時間は、下の式のとおりです。</p></div></li>
      <li><div><h3>守る</h3><p>たたくと喰うのが2秒ぶん戻り、しばらくこちらへ向かってきます。倒せば守りきりです。3回に1回ほど、欠片を落とします。</p></div></li>
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

<section class="stratum s-stone" id="more">
  <div class="edge"></div>
  <div class="wrap">
    <p class="depth">5</p>
    <h2 class="disp h2">灯標、灯りの色、招待。</h2>
    <div class="two">
      <div><h3 class="h3 disp">灯標と灯渡り</h3><p class="mu">灯籠に名前をつけると「灯標（とうひょう）」になります。二ノ灯より上の灯路網では、同じ灯路網の灯標へ、3秒じっとしているだけで移動できます（つぎに使えるまで30秒）。灯標は灯喰いに喰われません。ひとつを「帰る場所」に決めておけます。</p></div>
      <div><h3 class="h3 disp">仲間</h3><p class="mu">メニューの「仲間」に加えた人は、あなたの灯籠に名前をつけたり、取り除いたりできます。ほかの人は、あなたの灯籠を壊せません。</p></div>
    </div>
    <h3 class="h3 disp" style="margin-top:56px">灯りの色は、12色。</h3>
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

# ───────────────────────── 夜祭 ─────────────────────────
events = f'''<div class="hero">
  <div class="sky" style="background:linear-gradient(180deg,#0B0C24 0%,#211A46 55%,#4A2F66 100%)"></div><div class="stars" aria-hidden="true"></div>
  {header("events.html")}
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
        <tr data-g="0"><th>灯籠リレー</th><td>紅組と藍組に分かれ、出発点から終点まで、自分の組の灯籠だけで先に灯路を通した組の勝ち。ランタンは16個ずつ配られます。置いた灯籠は、終わったあともそのまま道として残ります。</td><td class="n">12分</td><td class="n">4人</td></tr>
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
      <div><h3 class="h3 disp">勝った人には、印</h3><p class="mu">勝者は次の夜祭まで、プレイヤー一覧の名前の横に ✦ がつきます。次の夜祭でだれかが勝つと、印はその人に移ります。</p></div>
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
  {header("")}
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
    ("guide.html", "遊び方｜灯原", "灯籠と灯路、昼4分・夜24分の長い夜、灯りを消しに来る灯喰い、敵が落とす欠片で解放する8つの加護。灯原のしくみ。", guide),
    ("events.html", "夜祭｜灯原", "毎週土曜21時。120秒の募集で人数がそろえば自動で始まる、週替わり4種のゲーム。灯籠リレー、闇かくれんぼ、建築早押し、夜明けまで。", events),
    ("rules.html", "きまり｜灯原", "灯原のきまり。してはいけないこと、しくみで守られていること、困ったときの連絡先、保護者の方へ。", rules),
    ("404.html", "ページが見つかりません｜灯原", "お探しのページは見つかりませんでした。", notfound),
]
out = pathlib.Path(__file__).parent
for f, t, d, b in PAGES:
    (out / f).write_text(page(f, t, d, b), encoding="utf-8")
today = datetime.date.today().isoformat()
(out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{'' if f == 'index.html' else f}</loc><lastmod>{today}</lastmod></url>\n" for f, *_ in PAGES[:5]) + "</urlset>\n", encoding="utf-8")
(out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
(out / "CNAME").write_text("tomoshibara.life\n", encoding="utf-8")
print("built", len(PAGES))
