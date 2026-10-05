# 灯原（ともしばら）サーバー公式サイト

灯籠をつないで夜の世界を広げる、Java版・統合版対応のMinecraftサバイバルサーバーのWebサイトです。
ビルド不要の静的サイトなので、GitHub Pages などにそのまま置けば公開できます。

## ページ

| ファイル | 内容 |
|---|---|
| `index.html` | トップ（ルール体験、開幕カウントダウン、次の夜祭） |
| `join.html` | はじめる（機種別の参加手順、最初の夜、きまり、FAQ） |
| `season.html` | シーズン（開幕カウントダウン、進行状況、過去シーズンの地図） |
| `events.html` | 夜祭（1週間の予定、ゲームの順番、ごほうび） |
| `community.html` | 仲間と遊ぶ（招待、投票、配信） |

## 公開前に書き換える箇所

`[ ]` で囲まれた仮の文字と、仮のアドレスを実際の内容に置き換えてください。

- サーバーアドレス `tomoshibara.example`（全ページ）
- `[対応バージョン]` `[参加用アカウント名]` `[保護者向けの連絡先]`（join.html）
- `[期間]` `[アーカイブ地図のURL]`（season.html）
- `[投票ページのURL]` `[コミュニティの招待URL]`（community.html）
- `[支援の仕組みがあればここに記載]`（join.html のFAQ）

シーズンの開幕日時は、`index.html` と `season.html` の末尾にある
`"seasonStart":{"editor":"text","default":"2026-11-07T21:00:00+09:00"}` を書き換えます。

## しくみ

- `assets/tomo.css` … 全ページ共通のスタイル
- `assets/dc-lite.js` … 各ページの `<template id="dc">` と `<script type="text/x-dc">` から画面を描画する小さなエンジン
- `assets/morphdom.min.js` … 画面の差分更新ライブラリ（MITライセンス、`assets/morphdom-LICENSE.txt`）
- フォントは Google Fonts（Dela Gothic One、DotGothic16、Zen Kaku Gothic New）を読み込みます

## 注意

灯原は非公式のファンサーバーで、Mojang Studios および Microsoft とは関係ありません。
