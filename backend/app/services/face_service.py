from typing import List
from fastapi import UploadFile
import numpy as np
from app.services.ai_engine.pipeline import ai_engine
from app.services.store.vector_db import vector_db
from app.core.config import settings


class FaceService:
    async def register_student(self, mssv: str, name: str, files: List[UploadFile]):
        vectors = []
        for file in files:
            content = await file.read()
            vec = ai_engine.predict(content)
            if vec is not None:
                vectors.append(vec)

        if not vectors:
            raise ValueError("Không tìm thấy khuôn mặt rõ nét nào.")

        # Tính trung bình cộng và chuẩn hóa lại
        avg_vec = np.mean(vectors, axis=0)
        avg_vec = avg_vec / np.linalg.norm(avg_vec)

        # Lưu: label format "MSSV|Tên"
        label = f"{mssv}|{name}"
        vector_db.add_vector(avg_vec, label)

        return {"mssv": mssv, "name": name, "status": "Training Completed"}

    async def recognize_image(self, file: UploadFile):
        content = await file.read()
        vec = ai_engine.predict(content)

        if vec is None:
            return {"status": "No face detected", "similarity": 0}

        # 1. Tìm người giống nhất (Luôn có kết quả nếu DB không rỗng)
        result = vector_db.search(vec)

        # 2. Giải mã thông tin người giống nhất (Candidate)
        candidate = None
        if result:
            parts = result["label"].split("|")
            candidate = {
                "mssv": parts[0] if len(parts) > 0 else "",
                "name": parts[1] if len(parts) > 1 else result["label"],
            }

        # 3. So sánh ngưỡng để ra quyết định
        # Nếu giống >= ngưỡng (0.80 hoặc 0.65 tùy config) -> MATCH
        if result and result["similarity"] >= settings.RECOGNITION_THRESH:
            return {
                "status": "Match",
                "mssv": candidate["mssv"],
                "name": candidate["name"],
                "similarity": result["similarity"],
            }

        # 4. Nếu giống thấp hơn ngưỡng -> UNKNOWN
        # Nhưng vẫn trả về "best_match" để bạn biết nó đang nhầm với ai (Debug)
        return {
            "status": "Unknown",
            "similarity": result["similarity"] if result else 0,
            "best_match": candidate,  # Trả về thông tin người giống nhất (hoặc None)
        }


face_service = FaceService()
