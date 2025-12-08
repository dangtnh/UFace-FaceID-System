import torch
import numpy as np
from app.core.config import settings
from .models import build_detector, build_recognizer, get_device
from .utils import read_image_file, l2_normalize


class FaceNetPipeline:
    _instance = None

    def __new__(cls):
        # Singleton: Chỉ load model 1 lần duy nhất
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

    def predict(self, image_bytes: bytes) -> np.ndarray:
        try:
            img = read_image_file(image_bytes)

            # Detect (lấy cả xác suất prob)
            face, prob = self.mtcnn(img, return_prob=True)

            if face is None or prob is None:
                return None

            # Kiểm tra ngưỡng tin cậy (Logic từ project cũ)
            prob_score = (
                float(np.array(prob).max())
                if isinstance(prob, (list, np.ndarray))
                else float(prob)
            )
            if prob_score < settings.DETECTION_CONF_THRESH:
                return None

            # Embed
            if face.ndim == 3:
                face = face.unsqueeze(0)
            face = face.to(self.device)

            with torch.no_grad():
                emb = self.resnet(face)

            # Chuẩn hóa L2
            return l2_normalize(emb[0].cpu().numpy())

        except Exception as e:
            print(f"❌ AI Error: {e}")
            return None


ai_engine = FaceNetPipeline()
