import subprocess
import tempfile
import cv2
import os


class OCREngine:
    def extract_text(self, img):
        if img is None:
            return "[NO IMAGE]"

        # グレースケール
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h, w = img.shape

        # 🔴 縦長 → 横向きへ
        if h > w:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            h, w = img.shape

        # 🔴 幅が細すぎる場合は拡大
        if w < 150:
            scale = 150 / w
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # コントラスト強調
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

        # デバッグ保存（最初は必ず見る）
        cv2.imwrite("debug_ocr_input.jpg", img)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            path = tmp.name
            cv2.imwrite(path, img)

        try:
            result = subprocess.run(
                ["yomitoku", path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                return "[OCR ERROR]"

            return result.stdout.strip() or "[NO TEXT]"

        finally:
            os.remove(path)
