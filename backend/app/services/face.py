from typing import List
from fastapi import UploadFile
import numpy as np
from app.services.ai_engine.pipeline import ai_engine
from app.repositories.face import vector_repo
from app.core.config import settings


class FaceService:
    async def register_student(self, mssv: str, name: str, files: List[UploadFile]):
        """
        Hàm đăng ký:
        - Input: Danh sách ảnh.
        - Process: Tính vector trung bình.
        - Output: Lưu vào Vector DB.
        """
        vectors = []
        for file in files:
            content = await file.read()
            await file.seek(0)

            # --- XỬ LÝ 1: Hứng 3 giá trị từ Pipeline ---
            # Tại bước đăng ký, ta KHÔNG cần vẽ khung (box) hay xem xác suất (prob).
            # Chỉ cần lấy vector (vec) để lưu.
            # Dùng dấu "_" để bỏ qua dữ liệu không cần thiết.
            vec, _, _ = ai_engine.predict(content)

            if vec is not None:
                vectors.append(vec)

        if not vectors:
            raise ValueError(
                "Không tìm thấy khuôn mặt rõ nét nào trong các ảnh gửi lên."
            )

        # Tính trung bình cộng và chuẩn hóa lại vector (L2 Norm)
        avg_vec = np.mean(vectors, axis=0)
        avg_vec = avg_vec / np.linalg.norm(avg_vec)

        # Tạo nhãn lưu trữ format: "MSSV|Tên"
        label = f"{mssv}|{name}"
        vector_repo.add(avg_vec, label)

        return {"mssv": mssv, "name": name, "status": "Training Completed"}

    async def recognize_image(self, file: UploadFile):
        """
        Hàm nhận diện:
        - Input: 1 ảnh từ Camera.
        - Process: Nhận diện + Lấy tọa độ Box.
        - Output: Trả về JSON chứa cả thông tin người và tọa độ để vẽ.
        """
        content = await file.read()

        # --- XỬ LÝ 2: Hứng đủ 3 giá trị để dùng cho Frontend ---
        # vec: Để tìm kiếm người.
        # box: Để vẽ khung đỏ.
        # prob: Xác suất là mặt người (dùng làm giá trị mặc định cho score).
        vec, box, prob = ai_engine.predict(content)

        # Trường hợp 1: Không thấy mặt hoặc không đạt ngưỡng detection
        if vec is None:
            return {
                "status": "No face detected",
                "similarity": 0,
                "box": None,  # Trả về None -> Frontend sẽ xóa khung vẽ
                "score": 0,
                "mssv": "Unknown",
                "name": "Unknown",
            }

        # --- XỬ LÝ 3: Chuyển đổi dữ liệu Box ---
        # Box từ AI là Numpy array, cần chuyển về int của Python để đóng gói JSON không bị lỗi.
        face_box = {
            "x1": int(box[0]),
            "y1": int(box[1]),
            "x2": int(box[2]),
            "y2": int(box[3]),
        }

        # 1. Tìm kiếm trong Vector DB (Lấy người giống nhất)
        result = vector_repo.search_similar(vec)

        # --- XỬ LÝ Logic hiển thị (Score & Identity) ---

        status = "Unknown"
        final_similarity = 0.0

        # Mặc định danh tính là Unknown
        identity = {"mssv": "Unknown", "name": "Unknown"}

        # Nếu tìm thấy kết quả tương đồng trong DB
        if result:
            # Lấy độ giống thực tế để hiển thị (Đây là cái thầy cô muốn xem)
            final_similarity = result["similarity"]

            # Kiểm tra ngưỡng (Threshold)
            if final_similarity >= settings.RECOGNITION_THRESH:
                status = "Match"
                # Chỉ khi Match mới giải mã lấy tên thật
                parts = result["label"].split("|")
                identity["mssv"] = parts[0] if len(parts) > 0 else ""
                identity["name"] = parts[1] if len(parts) > 1 else result["label"]
            else:
                pass

        # 2. Trả về kết quả đầy đủ
        return {
            "status": status,  # Match / Unknown
            "mssv": identity["mssv"],
            "name": identity["name"],
            "similarity": final_similarity,
            "box": face_box,  # Tọa độ {x1, y1, x2, y2}
            "score": final_similarity,  # Điểm số hiển thị (Luôn là độ giống)
        }


face_service = FaceService()
