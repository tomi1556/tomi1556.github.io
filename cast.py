# 灯原の「ひとびと」：予告編に出てくる旅人と灯喰いを、そのままドット絵（SVG）にする。
# 形は予告編（Film7.tsx の Figure / Eater）と同じ寸法。1 マス = 0.1u。

CLOAK = ["#3B4A6B", "#5A3F52", "#3F5A4E", "#5A4A3A"]
SCARF = ["#F2B544", "#F29BB8", "#8FC3E8", "#8BD18F", "#B79CF2", "#F2F3F5"]

# k は予告編の番号（マントは k%4、えりまきは k%6）
CAST = [
    {"id": "hino", "n": "ヒノ", "kj": "灯乃", "k": 0, "role": "道しるべ", "paths": ["light", "arcane"],
     "line": "灯りは、つながって道になる。",
     "bio": "灯原にいちばん早く着いて、最初の灯籠を置いた旅人。迷っている人を見つけると、だまって隣に灯りを置く。このサイトの案内役。",
     "like": "灯籠の火を見ていること"},
    {"id": "momo", "n": "モモ", "kj": "桃", "k": 1, "role": "夜祭の太鼓番", "paths": ["mine", "ranch"],
     "line": "土曜の21時、待ってるからね！",
     "bio": "にぎやかなことが好きで、夜祭ではいつも最初に広場にいる。力持ちで、掘るのも速い。動物にやたら好かれる。",
     "like": "夜祭と、羊の毛刈り"},
    {"id": "sora", "n": "ソラ", "kj": "空", "k": 2, "role": "灯路を渡る旅人", "paths": ["travel", "fish"],
     "line": "灯標があれば、どこへでも。",
     "bio": "ひとつの場所にいられない。灯標から灯標へ渡り歩き、見たことのない水辺で糸を垂らす。灯魚図鑑の「秘」を探している。",
     "like": "地図にない場所"},
    {"id": "waka", "n": "ワカ", "kj": "若葉", "k": 3, "role": "畑と森の人", "paths": ["wood", "farm"],
     "line": "切ったら、植えなおす。",
     "bio": "のんびりしていて、朝がくるのをいちばん楽しみにしている。木を切り、畑を耕し、余った作物をだれかの箱にそっと入れていく。",
     "like": "朝の4分間"},
    {"id": "shino", "n": "シノ", "kj": "忍", "k": 4, "role": "夜番", "paths": ["night"],
     "line": "守れ。",
     "bio": "長い夜のあいだ、灯りの外を見回っている。灯喰いの足音を聞きわけられる、らしい。口数は少ないが、喰われた灯籠はかならず灯し直す。",
     "like": "朱月の夜（なぜか）"},
    {"id": "yuki", "n": "ユキ", "kj": "雪", "k": 5, "role": "記録係", "paths": ["craft"],
     "line": "ぜんぶ、書きとめておくね。",
     "bio": "灯の証をつけている。だれが何をしたか、どの夜に何が起きたかを、几帳面に書き残す。手先が器用で、道具の手入れも得意。",
     "like": "まっさらな帳面"},
]
BY = {c["id"]: c for c in CAST}


def _hex(c):
    c = c.lstrip("#")
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def shade(c, f):
    r, g, b = _hex(c)
    if f < 1:
        r, g, b = (round(v * f) for v in (r, g, b))
    else:
        r, g, b = (round(v + (255 - v) * (f - 1)) for v in (r, g, b))
    return "#%02X%02X%02X" % (r, g, b)


def _r(l, b, w, h, c, top, cls=""):
    # 予告編の座標（左・下・幅・高さ、u 単位）を SVG の座標（10 倍、上が 0）にする
    x, y = round(l * 10), round((top - b - h) * 10)
    return f'<rect x="{x}" y="{y}" width="{round(w * 10)}" height="{round(h * 10)}" fill="{c}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}/>'


def fig(who, lamp=False, cls="", label=None):
    """旅人ひとり。who は CAST の id か番号。"""
    c = BY[who] if isinstance(who, str) else CAST[who]
    k = c["k"]
    cloak, scarf = CLOAK[k % 4], SCARF[k % 6]
    dk, lt = shade(cloak, .72), shade(cloak, 1.18)
    T = 11.6
    p = [
        _r(-1.6, 0, 1.2, 2, "#1B1420", T), _r(0.4, 0, 1.2, 2, "#1B1420", T),
        _r(-2.5, 2, 5, 1.2, cloak, T), _r(1.5, 2, 1, 1.2, dk, T),
        _r(-2, 3.2, 4, 4.2, cloak, T), _r(1.2, 3.2, 0.8, 4.2, dk, T), _r(-2, 3.2, 0.5, 4.2, lt, T),
        # えりまき（うしろへなびく端は動かす）
        '<g class="tail">' + _r(-3.3, 6.0, 1.1, 0.9, scarf, T) + _r(-3.9, 5.5, 0.6, 0.6, shade(scarf, .8), T) + "</g>",
        _r(-2.2, 7, 4.4, 1, scarf, T), _r(-2.2, 7, 4.4, 0.3, shade(scarf, .78), T),
        _r(-2, 8, 4, 3.6, cloak, T), _r(-1.6, 11.6 - 0.5, 3.2, 0.5, lt, T), _r(1.4, 8, 0.6, 3.1, dk, T),
        _r(-1.2, 8.4, 2.4, 1.7, "#E8C9A0", T), _r(-1.2, 8.4, 2.4, 0.4, "#D4B288", T),
        '<g class="eyes">' + _r(-0.8, 9.1, 0.5, 0.5, "#2A1E16", T) + _r(0.4, 9.1, 0.5, 0.5, "#2A1E16", T) + "</g>",
    ]
    if lamp:
        p.append('<g class="lamp">' + _r(2.2, 6.0, 0.3, 0.9, "#2A1E16", T) + _r(2.5, 4.2, 1.5, 1.9, "#2A1E16", T) + _r(2.8, 4.5, 0.9, 1.3, scarf, T)
                 + _r(2.95, 4.95, 0.35, 0.45, shade(scarf, 1.6), T) + "</g>")
    name = label if label is not None else c["n"]
    a = f'role="img" aria-label="{name}"' if name else 'aria-hidden="true"'
    return f'<svg class="fig {cls}" viewBox="-40 0 82 116" style="--sc:{scarf};--dl:-{k * .47:.2f}s" {a}>' + "".join(p) + "</svg>"


def eater(cls="", label="灯喰い"):
    """灯喰い（黒い体、白い面、すみれ色の目）。"""
    T = 13.1
    B, D = "#0B0714", "#07050D"
    p = [
        _r(-1.4, 0, 1, 3, D, T), _r(0.4, 0, 1, 3, D, T),
        _r(-2.2, 3, 4.4, 6.5, B, T), _r(-2.8, 3, 0.8, 4.5, B, T), _r(2, 3, 0.8, 4.5, B, T),
        '<g class="arm">' + _r(-4.6, 7.2, 2.6, 0.9, B, T) + _r(-5.2, 6.6, 0.8, 0.8, B, T) + "</g>",
        _r(-1.9, 9.5, 3.8, 3.6, "#D9D4C4", T), _r(-1.9, 9.5, 3.8, 0.8, "#A9A493", T),
        _r(-1.3, 11, 1, 1.1, D, T), _r(0.3, 11, 1, 1.1, D, T),
        '<g class="eye">' + _r(-1.05, 11.3, 0.5, 0.5, "#B46CFF", T) + _r(0.55, 11.3, 0.5, 0.5, "#B46CFF", T) + "</g>",
    ]
    return f'<svg class="eat {cls}" viewBox="-56 0 88 131" role="img" aria-label="{label}">' + "".join(p) + "</svg>"


def reds(cls=""):
    """闇の中の赤い目（夜の敵）。"""
    return f'<svg class="reds {cls}" viewBox="0 0 32 6" aria-hidden="true"><rect width="10" height="6" fill="#FF3B30"/><rect x="22" width="10" height="6" fill="#FF3B30"/></svg>'


# ───── 景色の縁（各ページの夜空の下に敷く、草と土と灯籠の稜線） ─────
def _noise(seed):
    s = [seed * 7919 + 13]

    def r():
        s[0] = (s[0] * 9301 + 49297) % 233280
        return s[0] / 233280
    return r


def _hills(w, h, step, base, amp, f1, f2, ph):
    import math
    pts = [f"0,{h}"]
    for x in range(0, w, step):
        y = max(4, round((h - (base + amp * math.sin(x / f1 + ph) + amp * .55 * math.sin(x / f2 + 1.3 + ph))) / 6) * 6)
        pts += [f"{x},{y}", f"{x + step},{y}"]
    return " ".join(pts + [f"{w},{h}"])


def ridge(seed=1, cast=(), lamps=5, say=None, eaters=()):
    """cast: (id, 列, 灯籠を持つか) の並び。say: (id, ことば)。eaters: 列の並び。"""
    import math
    N, H = 48, 15
    rnd = _noise(seed)
    hs = []
    for i in range(N):
        v = 4.2 + 1.5 * math.sin(i * .41 + seed) + 1.1 * math.sin(i * .17 + 2 + seed * .7) + (1 if rnd() > .8 else 0)
        hs.append(max(3, min(7, round(v))) + 2)
    taken = {c for _, c, _ in cast} | set(eaters)
    lc = []
    for j in range(lamps):
        c = round((j + .5) * N / lamps + (rnd() - .5) * 3)
        while c in taken or c in lc:
            c = (c + 1) % N
        lc.append(c)
    lc.sort()
    cols = ""
    for i, hh in enumerate(hs):
        inner = ""
        if i in lc:
            d = .5 + lc.index(i) * .28
            inner = f'<i class="rl" style="--d:{d:.2f}s"><i class="rl-g"></i><i class="rl-c"></i><i class="rl-h"></i><i class="rl-p"></i></i>'
        for who, c, lamp in cast:
            if c == i:
                bub = ""
                if say and say[0] == who:
                    bub = f'<span class="bub dot{" l" if c > N * .55 else ""}">{say[1]}</span>'
                inner += f'<span class="who">{bub}{fig(who, lamp)}</span>'
        if i in eaters:
            inner += f'<span class="who foe">{eater()}</span>'
        cols += f'<i class="rc" style="--h:{hh}">{inner}</i>'
    road = " ".join(f"{(c + .5) * 10:.0f},{(H - hs[c] - 2.8) * 10:.1f}" for c in lc)
    ph = seed * .9
    return f'''<div class="ridge" aria-hidden="true">
    <svg class="rg-far" viewBox="0 0 960 130" preserveAspectRatio="none"><polygon points="{_hills(960, 130, 30, 74, 16, 110, 47, ph)}" fill="#17274E"/></svg>
    <svg class="rg-mid" viewBox="0 0 960 130" preserveAspectRatio="none"><polygon points="{_hills(960, 130, 18, 50, 12, 70, 33, ph + 2)}" fill="#1F3460"/></svg>
    <div class="rg-cols">{cols}</div>
    <svg class="rg-road" viewBox="0 0 {N * 10} {H * 10}" preserveAspectRatio="none"><polyline class="rb" points="{road}" pathLength="100" vector-effect="non-scaling-stroke"/><polyline class="rf" points="{road}" pathLength="100" vector-effect="non-scaling-stroke"/></svg>
  </div>'''


def say_box(who, text, cls=""):
    c = BY[who]
    return f'''<aside class="say {cls}" style="--sc:{SCARF[c["k"] % 6]}" aria-label="{c["n"]}のひとこと"><span class="say-who"><span class="say-st">{fig(who, True, "", "")}</span><b class="dot">{c["n"]}</b></span><p class="say-b">{text}</p></aside>'''
