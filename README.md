# **図書館DX**


図書館DX プロジェクトでは、物体検出を用いて蔵書管理を効率化するためのシステムを構築しています。  
現時点では物体検出で本の検出し文字認識をするということはできていますがデータベースとの連携機能がありません。  
カメラ画像⇒物体検出で切り出し⇒文字認識⇒データベースと連携して蔵書管理をするということが目標

---

## 🔍 取り組み内容

### （1）物体検出
- Roboflow を使用して、本の背表紙のアノテーションを実施
- Ultralytics の YOLO を用いて物体検出モデルを作成
- 本棚画像から本の位置を検出し、1冊ずつ切り出し可能

  物体検出モデルの作成方法
　本棚の画像を作成したらroboflow (https://roboflow.com/) でモデルの作成を行う
  ラベル名などを設定しアノテーションをする際は右のツール欄からsmart selectを使用すると簡単にアノテーションをすることが出来る
<img width="1777" height="686" alt="スクリーンショット (271)" src="https://github.com/user-attachments/assets/5134f6d5-2a97-4e41-808e-9ec4cac9b793" />

  


### （2）OCR（YomitokuOCR）
- 物体検出で切り出した本の画像を対象に処理
- Python から YomitokuOCR を使用し、背表紙の文字認識を実施
- 書名などの文字情報を取得可能
- 

---

## 📌 現在の課題と次のステップ

1. 物体検出モデルの精度改善  
2. OCR 文字認識の実装  
3. 検出結果とデータベースの連携
4. 本の不足など蔵書管理に役立てる

---

## 🔧 実装方法（概要）

1. 本棚の写真を撮る
2. 物体検出をして本を切り出し  
3. 文字認識で本の情報を取得しデータベースと参照

---

## 🖥️　使用したライブラリ

- [Python](https://www.python.org/)
- [Roboflow](https://roboflow.com/)
- [Ultralytics YOLO](https://www.ultralytics.com/)
- [YomitokuOCR](https://github.com/yomitoku/yomitoku)
- [OpenCV](https://opencv.org/)

---

## 🚀 セットアップ手順

```bash
## 🚀 セットアップ手順

```bash
git clone https://github.com/oot11/tosyokanDX.git
cd tosyokanDX

# 必要なライブラリのインストール
pip install -r requirements.txt

# 物体検出 + OCR の実行
python src/main.py


---

##  参考サイト
https://github.com/kotaro-kinoshita/yomitoku
https://qiita.com/ShingoMatsuura/items/1a078681c6e370faeeb9
https://qiita.com/hayato0522/items/57fb179cf2847beeafd5
https://note.com/diy_smile/n/n63086e9c960a?magazine_key=m6a61077e1220
