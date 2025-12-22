import os
import cv2
from detector import BookDetector
from ocr_engine import OCREngine

"""
図書館DX: 背表紙検出 & Yomitoku OCR 統合メインスクリプト
1. YOLOv8 OBBで背表紙を検出し、歪みを補正して切り出し
2. Yomitoku OCRで縦書き・横書きを解析してテキスト化
3. 抽出結果と画像を連番フォルダに保存
"""

# --- パス設定 ---
# 実行ファイル(src/main.py)の場所を基準にパスを解決
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# モデルや入出力のパス
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "best.pt")
IMG_PATH = os.path.join(PROJECT_ROOT, "inputs", "hon_tate.jpg")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

def setup_folder(base_dir):
    """
    outputs/hon_1, hon_2... のように重複しない連番フォルダを作成する
    """
    os.makedirs(base_dir, exist_ok=True)

    existing = [d for d in os.listdir(base_dir) if d.startswith("hon_")]
    nums = [int(d.split("_")[1]) for d in existing if d.split("_")[1].isdigit()]
    counter = max(nums) + 1 if nums else 1

    path = os.path.join(base_dir, f"hon_{counter}")
    os.makedirs(path, exist_ok=True)
    return path

def main():
    # 1. クラスの初期化
    save_dir = setup_folder(OUTPUT_DIR)
    
    # 検出器（YOLOv8 OBB）
    detector = BookDetector(MODEL_PATH)
    
    # OCRエンジン（Yomitoku）
    # ※ocr_engine.py側でYomitokuを呼び出すように実装されている前提
    ocr = OCREngine()

    print(f"--- 処理開始 ---")
    print(f"使用画像: {IMG_PATH}")
    print(f"保存先: {save_dir}")

    # 2. 背表紙の検出と切り出し (歪み補正済み画像リストを取得)
    results, crops = detector.get_crops(IMG_PATH, conf=0.5)

    if not crops:
        print("認識対象が見つかりませんでした。")
        return

    # 3. OCR実行 & 結果保存
    results_txt_path = os.path.join(save_dir, "results.txt")
    
    with open(results_txt_path, "w", encoding="utf-8") as f:
        for i, item in enumerate(crops):
            crop_img = item["image"]
            conf_val = item["conf"]

            # OCR実行（Yomitokuによる解析）
            text = ocr.extract_text(crop_img)

            # 画像の保存
            img_name = f"hon{i+1}.jpg"
            cv2.imwrite(os.path.join(save_dir, img_name), crop_img)

            # テキスト結果の書き込み
            line = f"File: {img_name} | Conf: {conf_val:.2f} | Text: {text}\n"
            f.write(line)
            
            print(f"[{i+1}/{len(crops)}] {img_name} 解析完了: {text}")

    # 4. 全体アノテーション画像の保存（どこを検出したか視覚的に確認用）
    if results:
        annotated_img = results[0].plot()
        cv2.imwrite(os.path.join(save_dir, "annotated_full.jpg"), annotated_img)

    print(f"--- 完了 ---")
    print(f"全 {len(crops)} 冊の解析結果を {save_dir} に保存しました。")

if __name__ == "__main__":
    main()
