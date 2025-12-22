import subprocess
import tempfile
import cv2
import os

class OCREngine:
    def extract_text(self, img):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
            text = result.stdout.strip()
            return text if text else "[NO TEXT]"

        finally:
            os.remove(path)
