import easyocr
import numpy as np

class OCREngine:
    def __init__(self, languages=['ja', 'en']):
        # モデルのロード（初回実行時にダウンロードが始まります）
        self.reader = easyocr.Reader(languages)

    def extract_text(self, image_np):
        # image_np: OpenCV形式の画像
        results = self.reader.readtext(image_np)
        # 認識したテキストを結合して返す
        texts = [res[1] for res in results]
        return " ".join(texts)
