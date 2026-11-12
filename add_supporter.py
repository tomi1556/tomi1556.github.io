#!/usr/bin/env python3
"""支え手を、サイトの「支え手の壁」に足す・外す。

  python3 add_supporter.py <MCID> [--since 2026-11-12] [--hide]   足す（すでにいれば何もしない）
  python3 add_supporter.py <MCID> --remove                        外す
  python3 add_supporter.py --list                                 一覧

壁に載せない人は data/supporters.json に入れない約束。--hide は「入れない」ことを確かめて終わる。
足したあとは、python3 build.py → commit → push（Tomi の OK のうえで）。
ゲームの中の ❤ は別：運営が /akashi admin supporter add <MCID> を打つ。
"""
import argparse
import json
import pathlib
import re
import sys
from datetime import date

F = pathlib.Path(__file__).parent / "data" / "supporters.json"


def load():
    try:
        return json.loads(F.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []


def save(rows):
    F.write_text("[\n" + ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mcid", nargs="?")
    ap.add_argument("--since", default=date.today().isoformat())
    ap.add_argument("--hide", action="store_true")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    rows = load()
    if a.list or not a.mcid:
        for r in rows:
            print(r.get("mcid"), r.get("since", ""))
        print(f"{len(rows)} 人")
        return
    m = a.mcid.strip()
    if not re.fullmatch(r"\.?[A-Za-z0-9_ ]{3,20}", m):
        sys.exit(f"MCID の形がおかしいです: {m!r}（統合版は先頭に . が付きます）")
    same = [r for r in rows if str(r.get("mcid", "")).lower() == m.lower()]
    if a.remove:
        if not same:
            sys.exit("その人は壁にいません。")
        save([r for r in rows if r not in same])
        print(f"外しました: {m}")
        return
    if a.hide:
        print("壁に載せない人は、データに入れません。何もしませんでした。（ゲーム側の ❤ は /akashi admin supporter add <MCID> hide）")
        return
    if same:
        print(f"もう壁にいます: {same[0].get('mcid')}（{same[0].get('since')} から）。変更なし。")
        return
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.since):
        sys.exit("--since は 2026-11-12 の形で")
    rows.append({"mcid": m, "since": a.since})
    save(rows)
    print(f"足しました: {m}（{a.since} から）。次は python3 build.py → commit → push。")


main()
