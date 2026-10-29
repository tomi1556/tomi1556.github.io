# 灯原サイトの「見てわかる」部品：ドット絵のアイコン・カード・手順・棒グラフ・目盛り・図。
# 文字は短く。くわしい説明は more()（押すと開く）へ。
import html as _h

# 12×12 のドット絵。# は線（明るい色）、o は灯りの色（--c）。
I = {
    "lantern": ["....####....", "...######...", "...#oooo#...", "...#oooo#...", "...#oooo#...", "...######...", ".....##.....", ".....##.....", ".....##.....", ".....##.....", "....####....", "............"],
    "moon": ["....oooo....", "..ooo.......", ".oo.........", ".oo.........", "oo..........", "oo..........", "oo..........", "oo.......o..", ".oo.....oo..", ".ooo..ooo...", "..oooooo....", "....oo......"],
    "sun": [".....oo.....", ".o...oo...o.", "..o......o..", "....####....", "...#oooo#...", "oo.#oooo#.oo", "oo.#oooo#.oo", "...#oooo#...", "....####....", "..o......o..", ".o...oo...o.", ".....oo....."],
    "clock": ["...######...", "..#oooooo#..", ".#oooo#ooo#.", "#ooooo#oooo#", "#ooooo#oooo#", "#ooooo###oo#", "#oooooooooo#", "#oooooooooo#", ".#oooooooo#.", "..#oooooo#..", "...######...", "............"],
    "shield": ["############", "#oooooooooo#", "#oooooooooo#", "#ooooo#oooo#", "#oooo###ooo#", ".#ooo#.#oo#.", ".#oooooooo#.", "..#oooooo#..", "..#oooooo#..", "...#oooo#...", "....#oo#....", ".....##....."],
    "x": ["oo........oo", "ooo......ooo", ".ooo....ooo.", "..ooo..ooo..", "...oooooo...", "....oooo....", "....oooo....", "...oooooo...", "..ooo..ooo..", ".ooo....ooo.", "ooo......ooo", "oo........oo"],
    "ok": ["............", "..........oo", ".........ooo", "........ooo.", ".......ooo..", "oo....ooo...", "ooo..ooo....", ".oooooo.....", "..oooo......", "...oo.......", "............", "............"],
    "heart": ["............", ".###....###.", "#ooo#..#ooo#", "#oooo##oooo#", "#oooooooooo#", "#oooooooooo#", ".#oooooooo#.", "..#oooooo#..", "...#oooo#...", "....#oo#....", ".....##.....", "............"],
    "people": ["............", "..##....##..", ".#oo#..#oo#.", ".#oo#..#oo#.", "..##....##..", "............", ".####..####.", "#oooo##oooo#", "#oooo##oooo#", "#oooo##oooo#", "#oooo##oooo#", "############"],
    "one": ["............", ".....##.....", "....#oo#....", "....#oo#....", ".....##.....", "............", "....####....", "...#oooo#...", "...#oooo#...", "...#oooo#...", "...#oooo#...", "...######..."],
    "house": [".....##.....", "....#oo#....", "...#oooo#...", "..#oooooo#..", ".#oooooooo#.", "############", ".#oooooooo#.", ".#o##ooooo#.", ".#o##o##oo#.", ".#ooooo##o#.", ".#ooooo##o#.", ".##########."],
    "chat": ["............", ".##########.", "#oooooooooo#", "#oooooooooo#", "#oo#oo#oo#o#", "#oooooooooo#", "#oooooooooo#", ".###.######.", "...#.#......", "...##.......", "............", "............"],
    "warn": [".....##.....", "....#oo#....", "....#oo#....", "...#o##o#...", "...#o##o#...", "..#oo##oo#..", "..#oo##oo#..", ".#oooooooo#.", ".#ooo##ooo#.", "#oooo##oooo#", "#oooooooooo#", "############"],
    "star": [".....oo.....", ".....oo.....", "....oooo....", "oooooooooooo", ".oooooooooo.", "..oooooooo..", "...oooooo...", "...oooooo...", "..ooo..ooo..", "..oo....oo..", ".oo......oo.", "............"],
    "chest": ["............", ".##########.", "#oooooooooo#", "#oooooooooo#", "#####oo#####", "#oooo##oooo#", "#oooooooooo#", "#oooooooooo#", "#oooooooooo#", "############", "............", "............"],
    "pick": ["..oooooooo..", ".oooooooooo.", "oo...##...oo", "o....##....o", ".....##.....", ".....##.....", ".....##.....", ".....##.....", ".....##.....", ".....##.....", ".....##.....", "............"],
    "fish": ["............", "............", "....####....", "..##oooo#..#", ".#oooooooo##", "#o#ooooooo#.", "#oooooooooo.", ".#oooooooo##", "..##oooo#..#", "....####....", "............", "............"],
    "book": ["............", "############", "#oooo##oooo#", "#o##o##o##o#", "#oooo##oooo#", "#o##o##o##o#", "#oooo##oooo#", "#oooo##oooo#", "############", "............", "............", "............"],
    "phone": ["...######...", "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", "..#ooo#oo#..", "...######...", "............"],
    "pc": ["############", "#oooooooooo#", "#oooooooooo#", "#oooooooooo#", "#oooooooooo#", "#oooooooooo#", "############", ".....##.....", ".....##.....", "...######...", "............", "............"],
    "pad": ["............", "............", ".##########.", "#oooooooooo#", "#o#ooooo#oo#", "###oooo#o#o#", "#o#ooooo#oo#", "#oooooooooo#", "#ooo####ooo#", ".###....###.", "............", "............"],
    "bolt": [".......ooo..", "......ooo...", ".....ooo....", "....ooo.....", "...oooooooo.", "..oooooooo..", ".......ooo..", "......ooo...", ".....ooo....", "....oo......", "...o........", "............"],
    "fire": [".....#......", "....#o#.....", "....#oo#....", "...#ooo#.#..", "..#oooo##o#.", "..#ooooooo#.", ".#oooooooo#.", ".#ooo##ooo#.", ".#oo####oo#.", ".#oo####oo#.", "..#oooooo#..", "...######..."],
    "eye": ["............", "............", "...######...", ".##oooooo##.", "#ooo####ooo#", "#oo##oo##oo#", "#ooo####ooo#", ".##oooooo##.", "...######...", "............", "............", "............"],
    "lock": ["...######...", "..#......#..", "..#......#..", "..#......#..", "############", "#oooooooooo#", "#oooo##oooo#", "#oooo##oooo#", "#ooooo#oooo#", "#oooooooooo#", "############", "............"],
    "gift": ["..##....##..", "...#o..o#...", "############", "#ooooo#oooo#", "############", ".#oooo#ooo#.", ".#oooo#ooo#.", ".#oooo#ooo#.", ".#oooo#ooo#.", ".##########.", "............", "............"],
    "coin": ["...######...", "..#oooooo#..", ".#oo#oo#oo#.", "#ooo#oo#ooo#", "#oooo##oooo#", "#oo######oo#", "#ooooo#oooo#", "#oo######oo#", "#ooooo#oooo#", ".#oooo#ooo#.", "..#oooooo#..", "...######..."],
    "flag": [".#..........", ".#oooooooo..", ".#ooooooooo.", ".#oooooooo..", ".#ooooooo...", ".#..........", ".#..........", ".#..........", ".#..........", ".#..........", "###.........", "............"],
    "pin": ["...######...", "..#oooooo#..", ".#ooo##ooo#.", ".#oo#..#oo#.", ".#ooo##ooo#.", "..#oooooo#..", "..#oooooo#..", "...#oooo#...", "....#oo#....", ".....##.....", "............", "............"],
    "sword": ["..........##", ".........#o#", "........#o#.", ".......#o#..", "......#o#...", ".#...#o#....", "..#.#o#.....", "...#o#......", "..#.#.......", ".#...#......", "#...........", "............"],
    "hammer": [".#######....", ".#ooooo##...", ".#ooooo###..", ".#######....", "....##......", "....##......", "....##......", "....##......", "....##......", "....##......", "...####.....", "............"],
    "link": ["............", ".#####......", "#ooooo#.....", "#o...o#.....", "#o...#####..", "#o..#oooo#..", ".###o...o#..", "....#o...o#.", "....#o...o#.", "....#ooooo#.", ".....#####..", "............"],
    "path": ["............", "oo..........", "oo..........", "..o.........", "...o........", "....oo....oo", "......o..o..", ".......oo...", "............", "............", "............", "............"],
    "camera": ["............", "............", "########....", "#oooooo#..##", "#oooooo#.#o#", "#oooooo##oo#", "#oooooo##oo#", "#oooooo#.#o#", "#oooooo#..##", "########....", "............", "............"],
    "bell": [".....##.....", "....####....", "...#oooo#...", "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", ".#oooooooo#.", ".#oooooooo#.", "############", ".....##.....", "............", "............"],
    "seed": [".....o......", "....ooo.....", "...oo.oo....", ".....o......", ".....o......", ".....o......", "..########..", ".#oooooooo#.", "..#oooooo#..", "..#oooooo#..", "...######...", "............"],
    "trophy": ["############", "#oooooooooo#", "#oooooooooo#", ".#oooooooo#.", "..#oooooo#..", "...#oooo#...", "....#oo#....", ".....##.....", ".....##.....", "...######...", "..########..", "............"],
    "map": ["............", "##..####..##", "#o##oooo##o#", "#oo#oooo#oo#", "#oo#oooo#oo#", "#oo#oooo#oo#", "#oo#oooo#oo#", "#oo#oooo#oo#", "#o##oooo##o#", "##..####..##", "............", "............"],
    "q": ["...######...", "..#oooooo#..", ".#ooo##ooo#.", ".#oo#..#oo#.", ".....#.#oo#.", "....#oo#....", "....#oo#....", "....#oo#....", "............", "....#oo#....", "....#oo#....", "............"],
}


def ic(name, color="var(--amber)", size=None, cls=""):
    rows = I[name]
    n = len(rows)
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
            r.append(f'<rect x="{x}" y="{y}" width="{w}" height="1"{" class=\"o\"" if ch == "o" else ""}/>')
            x += w
    st = f' style="--c:{color}' + (f';width:{size}px;height:{size}px' if size else "") + '"'
    return f'<svg class="vi {cls}"{st} viewBox="0 0 {n} {n}" aria-hidden="true">' + "".join(r) + "</svg>"


def more(summary, inner, open_=False):
    """押すと開く「くわしく」。"""
    return f'<details class="vmore"{" open" if open_ else ""}><summary><span>{summary}</span></summary><div class="vmore-b">{inner}</div></details>'


def cards(items, cols=3, cls=""):
    """items: (アイコン, 色, 見出し, ひとこと[, リンク]) の並び。"""
    out = []
    for it in items:
        name, color, title, text = it[:4]
        href = it[4] if len(it) > 4 else None
        body = f'<span class="vc-i">{ic(name, color) if name in I else name}</span><span class="vc-x"><span class="vc-t">{title}</span>' + (f'<span class="vc-p">{text}</span>' if text else "") + "</span>"
        tag = f'<a class="vc" href="{href}" style="--c:{color}">' + body + '<i class="vc-go" aria-hidden="true"></i></a>' if href else f'<div class="vc" style="--c:{color}">{body}</div>'
        out.append(f"<li>{tag}</li>")
    return f'<ul class="vcs c{cols} {cls}">' + "".join(out) + "</ul>"


def steps(items, cls=""):
    """横に並ぶ手順。items: (アイコン, 色, 見出し, ひとこと)。"""
    out = []
    for i, (name, color, title, text) in enumerate(items):
        out.append(f'<li style="--c:{color}"><span class="vs-n dot">{i + 1}</span><span class="vs-i">{ic(name, color)}</span><b class="vs-t">{title}</b>' + (f'<span class="vs-p">{text}</span>' if text else "") + "</li>")
    return f'<ol class="vsteps {cls}">' + "".join(out) + "</ol>"


def stats(items):
    """大きな数字。items: (アイコン, 色, 数, 単位, 説明)。"""
    out = [f'<li style="--c:{c}">{ic(n, c)}<b class="disp">{v}<small>{u}</small></b><span>{t}</span></li>' for n, c, v, u, t in items]
    return '<ul class="vstats">' + "".join(out) + "</ul>"


def bars(rows, unit="", maxv=None, cls=""):
    """横の棒グラフ。rows: (名前, 値, 色[, 横の説明])。"""
    m = maxv or max(r[1] for r in rows) or 1
    out = []
    for r in rows:
        label, v, color = r[:3]
        note = r[3] if len(r) > 3 else ""
        vt = r[4] if len(r) > 4 else f"{v:g}{unit}"
        out.append(f'<li style="--c:{color};--w:{max(3, v / m * 100):.1f}%"><span class="vb-l">{label}</span><span class="vb-t"><i></i></span><b class="vb-v dot">{vt}</b>' + (f'<span class="vb-n">{note}</span>' if note else "") + "</li>")
    return f'<ul class="vbars {cls}">' + "".join(out) + "</ul>"


def scale(segs, cls=""):
    """色の目盛り（軽い→重い など）。segs: (上の字, 下の字, 色, 幅)。"""
    out = "".join(f'<li style="--c:{c};flex:{w}"><b>{t}</b><span>{s}</span></li>' for t, s, c, w in segs)
    return f'<ol class="vscale {cls}">{out}</ol>'


def dodont(dos, donts, do_t="してよいこと", dont_t="してはいけないこと"):
    def col(items, kind):
        name, color = ("ok", "#6FD39A") if kind == "do" else ("x", "#E0453A")
        return "".join(f'<li>{ic(name, color)}<span><b>{t}</b>' + (f"<small>{s}</small>" if s else "") + "</span></li>" for t, s in items)
    return f'''<div class="vdd"><div class="vdd-c do"><h3 class="dot">{do_t}</h3><ul>{col(dos, "do")}</ul></div><div class="vdd-c dont"><h3 class="dot">{dont_t}</h3><ul>{col(donts, "dont")}</ul></div></div>'''


def timeline(items):
    """時間の流れ。items: (いつ, アイコン, 色, 見出し, ひとこと)。"""
    out = "".join(f'<li style="--c:{c}"><time class="dot">{w}</time><span class="vt-i">{ic(n, c)}</span><b>{t}</b><span>{p}</span></li>' for w, n, c, t, p in items)
    return f'<ol class="vtl">{out}</ol>'


# ───────── 図 ─────────
def daynight(day=4, night=24):
    """昼と夜の長さの輪。"""
    tot = day + night
    import math
    r, cx, cy = 80, 100, 100
    a = day / tot * 2 * math.pi
    x1, y1 = cx + r * math.sin(a), cy - r * math.cos(a)
    large = 1 if a > math.pi else 0
    return f'''<figure class="vfig vdn"><svg viewBox="0 0 200 200" role="img" aria-label="昼{day}分・夜{night}分">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#2A2F6B" stroke-width="30"/>
  <path d="M{cx} {cy - r} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="#F2B544" stroke-width="30"/>
  <text x="{cx}" y="{cy - 6}" text-anchor="middle" class="t1">{night}分</text><text x="{cx}" y="{cy + 22}" text-anchor="middle" class="t2">が夜</text>
</svg><figcaption><span><i style="background:#F2B544"></i>昼 {day}分</span><span><i style="background:#2A2F6B"></i>夜 {night}分</span></figcaption></figure>'''


def lantern_map():
    """灯籠2基と、守りの円・灯路。"""
    def lan(x, y):
        return f'<g transform="translate({x - 6},{y - 11})"><rect x="3" y="0" width="6" height="2" fill="#2A1A08"/><rect x="2" y="2" width="8" height="8" fill="#2A1A08"/><rect x="3" y="3" width="6" height="6" fill="#FFD98A"/><rect x="5" y="10" width="2" height="8" fill="#2A1A08"/></g>'
    return f'''<figure class="vfig vlm"><svg viewBox="0 0 360 200" role="img" aria-label="灯籠のまわり半径10ブロックが安全。16ブロック以内の灯籠は灯路でつながる">
  <defs><radialGradient id="vg"><stop offset="0" stop-color="#F2B544" stop-opacity=".45"/><stop offset="1" stop-color="#F2B544" stop-opacity=".06"/></radialGradient></defs>
  <rect width="360" height="200" fill="#0E1730"/>
  <circle cx="110" cy="105" r="70" fill="url(#vg)" stroke="#F2B544" stroke-dasharray="4 4"/>
  <circle cx="250" cy="105" r="70" fill="url(#vg)" stroke="#F2B544" stroke-dasharray="4 4"/>
  <line x1="110" y1="112" x2="250" y2="112" stroke="#FFD98A" stroke-width="3" stroke-dasharray="3 5"/>
  {lan(110, 112)}{lan(250, 112)}
  <line x1="110" y1="150" x2="180" y2="150" stroke="#E9EEF6"/><text x="145" y="172" text-anchor="middle" class="t3">半径10</text>
  <text x="180" y="100" text-anchor="middle" class="t4">灯路</text>
  <g fill="#FF3B30"><rect x="16" y="40" width="5" height="3"/><rect x="26" y="40" width="5" height="3"/><rect x="330" y="168" width="5" height="3"/><rect x="340" y="168" width="5" height="3"/></g>
  <text x="24" y="62" text-anchor="middle" class="t5">敵</text>
</svg><figcaption><span><i style="background:#F2B544"></i>灯りの中＝安全</span><span><i style="background:#FFD98A"></i>灯路＝足が速い</span><span><i style="background:#FF3B30"></i>敵は入れない</span></figcaption></figure>'''


def esc(s):
    return _h.escape(s)


def craft(grid):
    """作業台の 3×3。grid: 9個の (名前, 色) か None。"""
    cells = "".join(f'<span class="vcr-s"><i style="background:{c}"></i><small>{n}</small></span>' if g else '<span class="vcr-s"></span>' for g in grid for n, c in ([g] if g else [("", "")]))
    return f'<div class="vcr">{cells}</div>'


def chain(items, color="var(--amber)"):
    """順に上がっていくもの（位階など）。"""
    return '<ol class="vchain" style="--c:' + color + '">' + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


def swatches(items):
    """色の見本。items: (色, 名前, 手に入れ方)。"""
    return '<ul class="vsw">' + "".join(f'<li style="--c:{c}"><i></i><b>{n}</b><small>{h}</small></li>' for c, n, h in items) + "</ul>"


def eq(parts):
    """式を箱で。parts: (文字, 色) か "+"。"""
    out = []
    for p in parts:
        out.append('<span class="veq-op">＋</span>' if p == "+" else f'<span class="veq-b" style="--c:{p[1]}">{p[0]}</span>')
    return '<div class="veq">' + "".join(out) + "</div>"
