import cv2
import numpy as np
from ultralytics import YOLO

class BookDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]   # 左上
        rect[2] = pts[np.argmax(s)]   # 右下
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)] # 右上
        rect[3] = pts[np.argmax(diff)] # 左下
        return rect

    def get_crops(self, img_path, conf=0.5):
        img = cv2.imread(img_path)
        if img is None:
            return None, []

        results = self.model.predict(source=img_path, imgsz=640, conf=conf, device='cpu', save=False)
        
        crops = []
        for result in results:
            if result.obb is None or len(result.obb.xyxyxyxy) == 0:
                continue

            corners_list = result.obb.xyxyxyxy.cpu().numpy()
            confidences = result.obb.conf.cpu().numpy()

            for corners, c_conf in zip(corners_list, confidences):
                rect = self.order_points(np.array(corners, dtype="float32"))
                (tl, tr, br, bl) = rect
                
                width = int(max(np.linalg.norm(br-bl), np.linalg.norm(tr-tl)))
                height = int(max(np.linalg.norm(tr-br), np.linalg.norm(tl-bl)))

                if width < 2 or height < 2: continue

                dst = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype="float32")
                M = cv2.getPerspectiveTransform(rect, dst)
                warped = cv2.warpPerspective(img, M, (width, height))
                
                crops.append({"image": warped, "conf": c_conf})
        
        return results, crops
