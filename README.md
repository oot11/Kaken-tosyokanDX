# tosyokanDX

図書館DX プロジェクトでは、物体検出を用いて蔵書管理を効率化するためのシステムを構築しています。  
現時点では物体検出で本の位置がわかりますが、題名や著者名の OCR 認識はまだ未実装です。  
Google Books API による本情報自動識別のシステム構築を目指しています。

---

## 📌 現在の課題と次のステップ

1. 物体検出モデルの精度改善  
2. OCR 文字認識の実装  
3. 検出結果と Google Books API 連携  
4. タイトル・著者名表示の実装

---

## 🔧 実装方法（概要）

1. 本の検出位置を取得  
2. 画像切り取り + OCR 実行  
3. 抽出文字データで書籍照合  
4. 結果を画像上に表示

---

## 🚀 セットアップ手順

```bash
git clone https://github.com/<あなたのユーザー名>/tosyokanDX.git
cd tosyokanDX
# 必要なライブラリのインストール
pip install -r requirements.txt
# モデル学習 / 推論コード 実行
python detect.py
