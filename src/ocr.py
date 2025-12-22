# 
import numpy as np
# Yomitokuのインポート（環境のインストール状況に応じて調整してください）
from yomitoku import Yomitoku

class OCREngine:
    def __init__(self):
        """
        Yomitoku OCRエンジンの初期化
        ※ 内部でモデルのロードが行われます
        """
        self.reader = Yomitoku()

    def extract_text(self, image_np):
        """
        image_np: OpenCV形式(numpy)の画像（背表紙の切り出し画像）
        """
        # Yomitokuで解析実行
        results = self.reader.read(image_np)
        
        # 認識された各行のテキストを抽出して結合
        # 背表紙には「タイトル」「著者名」「出版社」などが別行として認識されるため
        # それらをスペース区切りで1つの文字列にします
        texts = [line.text for line in results.lines]
        
        return " ".join(texts).strip()
