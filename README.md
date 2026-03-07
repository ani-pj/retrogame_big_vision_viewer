# Retrogame Big Vision Viewer (RBV2)

# ダウンロード
[ダウンロードはこちら！](https://github.com/ani-pj/retrogame_big_vision_viewer/raw/refs/heads/main/retrogame_big_vision_viewer.zip)

# 使い方
## 概要
1. 「RBV2.exe」本体と「config.txt」を同じフォルダにおいてください
2. 「config.txt」を適切に設定してください
3. 「RBV2.exe」本体を起動してください
  - ただしく設定されていると、ゲーム画面が表示されます

## OBS Studioと接続する場合
- ウィンドウキャプチャで、RBV2の画面を取り込んでください
- 音声は「音声入力キャプチャ」より、キャプチャボードを指定してください

## config.txtパラメータ
- DEVICE 1
  - キャプチャボードのデバイス番号を指定します。分からなければ、0から順番に試してください。ただしこのとき、OBS Studio等の他のソフトで、ゲームの画面取り込みをしないでください
- BILATERAL_FILTER_D 15
- BILATERAL_FILTER_SIGMA_COLOR 50
- BILATERAL_FILTER_SIGMA_SPACE 50
  - 上記3つはBilateral Filterのパラメタです。それぞれ数字を小さくすると処理が軽くなりますが、画面を綺麗にする効果が落ちます
- COMPARE_MODE 0
  - 0は通常のモードです。1にすると、画面左半分が処理前の映像、右半部が処理後の映像となり、この処理の効果を確認できます

# デモ
- [PDF資料](./demo.pdf)
- [動画（カービィのエアライド）](https://youtu.be/-kInQGOimIQ)
- [動画（ポケモンコロシアム）](https://youtu.be/QgVUtphf6XE)

