import torch
import numpy as np
from app.core.config import settings
from .models import build_detector, build_recognizer, get_device
from .utils import read_image_file, l2_normalize


class FaceNetPipeline:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceNetPipeline, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        print("⏳ AI Engine: Đang tải models...")
        self.device = get_device()
        self.mtcnn = build_detector(self.device)
        self.resnet = build_recognizer(self.device)
        print(f"✅ AI Engine: Sẵn sàng ({self.device})")

    def predict(self, image_bytes: bytes):
        try:
            img = read_image_file(image_bytes)

            # 1. Detect lấy tọa độ
            boxes, probs = self.mtcnn.detect(img)

            if boxes is None or probs is None:
                return None, None, None

            # 2. Lấy box tốt nhất
            best_box = boxes[0]
            best_prob = probs[0]

            if best_prob < settings.DETECTION_CONF_THRESH:
                return None, None, None

            # 3. Extract (Cắt ảnh)
            face_tensor = self.mtcnn.extract(img, np.array([best_box]), save_path=None)

            if face_tensor is not None:

                if face_tensor.ndim == 3:
                    face_tensor = face_tensor.unsqueeze(0)

                face_tensor = face_tensor.to(self.device)

                with torch.no_grad():
                    emb = self.resnet(face_tensor)

                vec_norm = l2_normalize(emb[0].cpu().numpy())

                return vec_norm, best_box, best_prob

            return None, None, None

        except Exception as e:
            print(f"❌ AI Error: {e}")
            return None, None, None


ai_engine = FaceNetPipeline()
