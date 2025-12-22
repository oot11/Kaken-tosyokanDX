import os
import cv2
import numpy as np
import subprocess
from ultralytics import YOLO

# =============================
# 設定
# =============================
MODEL_PATH = "/home/sougou/yolo8/runs/train/obb_exp6/weights/best.pt"
IMG_PATH = "/home/sougou/hon_15.jpg"
OUTPUT_DIR = "/home/sougou/books"
CONF_TH = 0.5

# =============================
# 出力フォルダ連番作成
# =============================
os.makedirs(OUTPUT_DIR, exist_ok=True)
existing = [d for d in os.listdir(OUTPUT_DIR) if d.startswith("hon_")]
nums = [int(d.split("_")[1]) for d in existing if d.split("_")[1].isdigit()]
idx = max(nums) + 1 if nums else 1
SAVE_DIR = os.path.join(OUTPUT_DIR, f"hon_{idx}")
os.makedirs(SAVE_DIR, exist_ok=True)

print(f"📁 保存先: {SAVE_DIR}")

# =============================
# ユーティリティ
# =============================
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # 左上
    rect[2] = pts[np.argmax(s)]   # 右下
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # 右上
    rect[3] = pts[np.argmax(diff)]  # 左下
    return rect

def run_yomitoku(img):
    import tempfile

    # グレースケール
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape

    # 縦書き対策
    if h > w:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # 小さすぎる画像を拡大
    if w < 150:
        scale = 150 / w
        img = cv2.resize(img, None, fx=scale, fy=scale,
                         interpolation=cv2.INTER_CUBIC)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        path = tmp.name
        cv2.imwrite(path, img)

    try:
        res = subprocess.run(
            ["yomitoku", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        text = res.stdout.strip()
        return text if text else "[NO TEXT]"
    finally:
        os.remove(path)

# =============================
# モデルロード
# =============================
model = YOLO(MODEL_PATH)
img = cv2.imread(IMG_PATH)
if img is None:
    raise FileNotFoundError("画像が読み込めません")

# =============================
# 推論
# =============================
results = model.predict(
    source=IMG_PATH,
    imgsz=640,
    conf=CONF_TH,
    device="cpu",
    save=False
)

# =============================
# 検出処理
# =============================
txt_path = os.path.join(SAVE_DIR, "results.txt")
file_id = 1
total = 0

with open(txt_path, "w", encoding="utf-8") as f:
    for result in results:
        if result.obb is None:
            continue

        corners_list = result.obb.xyxyxyxy.cpu().numpy()
        confs = result.obb.conf.cpu().numpy()

        for corners, conf in zip(corners_list, confs):
            if conf < CONF_TH:
                continue

            rect = order_points(corners.astype("float32"))
            (tl, tr, br, bl) = rect

            w1 = np.linalg.norm(br - bl)
            w2 = np.linalg.norm(tr - tl)
            h1 = np.linalg.norm(tr - br)
            h2 = np.linalg.norm(tl - bl)

            W = int(max(w1, w2))
            H = int(max(h1, h2))

            if W < 10 or H < 10:
                continue

            dst = np.array([
                [0, 0],
                [W - 1, 0],
                [W - 1, H - 1],
                [0, H - 1]
            ], dtype="float32")

            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(img, M, (W, H))

            # OCR
            text = run_yomitoku(warped)

            # 保存
            img_name = f"hon{file_id}.jpg"
            cv2.imwrite(os.path.join(SAVE_DIR, img_name), warped)

            f.write(f"{img_name} | conf={conf:.2f} | {text}\n")
            print(f"📖 {img_name} → {text}")

            file_id += 1
            total += 1

# =============================
# 全体アノテーション保存
# =============================
annotated = results[0].plot()
cv2.imwrite(os.path.join(SAVE_DIR, "annotated_full.jpg"), annotated)

print(f"\n✅ 完了：{total} 冊の背表紙を解析しました")
print(f"📝 OCR結果: {txt_path}")
