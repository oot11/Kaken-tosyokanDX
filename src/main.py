import os
import cv2
from detector import BookDetector
from ocr_engine import OCREngine

# --- 設定 ---
MODEL_PATH = '/home/sougou/yolo8/runs/train/obb_exp6/weights/best.pt'
IMG_PATH = '/home/sougou/hon_15.jpg'
OUTPUT_DIR = '/home/sougou/books'

def setup_folder(base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
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

    # 3. 各クロップ画像に対してOCR実行と保存
    with open(os.path.join(save_dir, "results.txt"), "w", encoding="utf-8") as f:
        for i, item in enumerate(crops):
            crop_img = item["image"]
            
            # OCR実行
            text = ocr.extract_text(crop_img)
            
            # 画像保存
            img_name = f"hon{i+1}.jpg"
            cv2.imwrite(os.path.join(save_dir, img_name), crop_img)
            
            # 結果をファイルに書き出し
            f.write(f"File: {img_name} | Conf: {item['conf']:.2f} | Text: {text}\n")
            print(f"Processed: {img_name} -> {text}")

    # 4. 全体アノテーション画像の保存
    for r_idx, result in enumerate(results):
        annotated_img = result.plot()
        cv2.imwrite(os.path.join(save_dir, f"annotated_full.jpg"), annotated_img)

    print("\nFinish! All results saved.")

if __name__ == "__main__":
    main()
