import os
import cv2
from detector import BookDetector
from ocr_engine import OCREngine

"""
図書館DX
本棚画像から本の背表紙を検出し、
切り出し画像に対してOCRを実行する
"""

# --- パス設定（相対パス） ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # src/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                # プロジェクトルート

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "best.pt")
IMG_PATH = os.path.join(PROJECT_ROOT, "inputs", "hon_tate.jpg")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")


def setup_folder(base_dir):
    os.makedirs(base_dir, exist_ok=True)

    existing = [d for d in os.listdir(base_dir) if d.startswith("hon_")]
    nums = [int(d.split("_")[1]) for d in existing if d.split("_")[1].isdigit()]
    counter = max(nums) + 1 if nums else 1

    path = os.path.join(base_dir, f"hon_{counter}")
    os.makedirs(path, exist_ok=True)
    return path


def main():
    # 1. 準備
    save_dir = setup_folder(OUTPUT_DIR)
    detector = BookDetector(MODEL_PATH)
    ocr = OCREngine(languages=['ja', 'en'])

    print(f"Working in: {save_dir}")

    # 2. 検出と切り出し
    results, crops = detector.get_crops(IMG_PATH)

    if not crops:
        print("No objects detected.")
        return

    # 3. OCR & 保存
    with open(os.path.join(save_dir, "results.txt"), "w", encoding="utf-8") as f:
        for i, item in enumerate(crops):
            crop_img = item["image"]
            text = ocr.extract_text(crop_img)

            img_name = f"hon{i+1}.jpg"
            cv2.imwrite(os.path.join(save_dir, img_name), crop_img)

            f.write(
                f"File: {img_name} | Conf: {item['conf']:.2f} | Text: {text}\n"
            )
            print(f"Processed: {img_name} -> {text}")

    # 4. 全体アノテーション画像保存
    annotated_img = results[0].plot()
    cv2.imwrite(os.path.join(save_dir, "annotated_full.jpg"), annotated_img)

    print("\nFinish! All results saved.")


if __name__ == "__main__":
    main()
