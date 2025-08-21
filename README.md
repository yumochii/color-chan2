# color-chan2 — M5StickC Plus / UIFlow (Python)

**「色を聴く」**

**色（RGB）を“音”に変換して鳴らす** M5StickC Plus 用の UIFlow（MicroPython）プロジェクトです。  
カラーセンサーのRGBから和音を生成し、Unit SYNTHで再生します。
お楽しみ要素として、画面には読み取った色とともに、ｽﾀｯｸﾁｬﾝ（★）のような顔を表示し、ボタンのオンオフで口が動くようにしました。
（AIの助けを借りて整えたコードです）
★ｽﾀｯｸﾁｬﾝとは、ししかわさんが開発しオープンソースとして公開されている、M5Stackで動く手乗りサイズのｽｰﾊﾟｰｶﾜｲｲﾛﾎﾞｯﾄです。

---

## 動作環境

- デバイス: **M5StickC Plus**（※Plus2 ではありません）
- 開発環境: **UIFlow**（Web 版 V1.14.8）
- ファームウェア: **UIFlow Firmware for M5StickC Plus**
- 接続: USB-C（データ通信対応のケーブル）

> **注意:** 「M5StickC Plus」と「M5StickC Plus2」は別モデルです。  
> ファームウェアは必ず **Plus 用** を選んでください。

---

## セットアップ（初回）

1. **ドライバの準備（必要な場合）**  
   USB-シリアルドライバ（CP210x / CH9102）が必要なOSがあります。  
   既に M5Burner / UIFlow で接続できていればスキップ可。

2. **UIFlow ファームウェアを書き込み**（M5Burner 使用）  
   - デバイス: **M5StickC Plus** を選択  
   - **UIFlow** の安定版を選び「Burn」  
   - 初回設定で **Wi-Fi** 情報を入れておくと便利（後からでもOK）  
   - **起動モード（Start Mode）** を **App / main.py**（フラッシュのアプリを起動）にしておくと、電源ONで自動起動しやすいです

3. **UIFlow（Web/デスクトップ）を準備**  
   - Web 版 or Desktop 版を起動  
   - **USB Mode**（COMポート）で接続

---

## 使い方（コード書き込み）

> このリポジトリは **Python（MicroPython）** のソースを含みます。UIFlow の **Python タブ**で開いてください。

1. UIFlow を起動し **Python** タブに切り替え  
2. リポジトリ内の **color_chan3_hold_gradual.py**を貼り付け/読み込み  
3. 右上の **Run**（お試し実行）または **Download**（本体へ保存）をクリック  
   - **Run**: PC接続中だけ動作  
   - **Download**: 本体フラッシュに保存され、**電源再投入後も単独で起動**します

> **おすすめ:** 普段使いは **Download**。PC/ネットに繋がずに動きます。

---

## 必要なもの

- M5StickC Plus 本体  
- M5Stack用カラーセンサユニット
-M5Stack Unit Synth
-ExtPort for StickC（M5StickC (Plus/Plus2)の上部コネクタに接続して、2つのGroveポートを増設）  
---

## カスタマイズの目安

コード内で以下を探して調整します:

- **音量**: `volume = 100`（0–100 の範囲で調整）
- **ボタン動作**: `btnA.wasPressed(...)`, `btnB.wasPressed(...)`  
  - 例: Aで再生/停止、Bで音量ダウン 等
- **RGB→音の対応**: `rgb_to_notes(r, g, b)` のような関数があれば、ここでスケールや和音を変更

```python
# 例: ボタンハンドラ
def on_btnA_pressed():
    # 再生/停止など
    pass

def on_btnB_pressed():
    # 音量ダウンやモード切替など
    pass

btnA.wasPressed(on_btnA_pressed)
btnB.wasPressed(on_btnB_pressed)
```
