from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.face_service import face_service

router = APIRouter()

# Cấu hình giờ vào lớp (Demo: 8h00, cho phép muộn 15p)
START_TIME_HOUR = 8
START_TIME_MINUTE = 0
LATE_THRESHOLD_MINUTES = 15


@router.post("/recognize")
async def check_in(file: UploadFile = File(...)):
    # 1. Gọi AI nhận diện xem là ai
    result = await face_service.recognize_image(file)

    # 2. Xử lý kết quả trả về từ AI
    if result["status"] != "Match":

        # TRƯỜNG HỢP 1: UNKNOWN (Có mặt nhưng không khớp ai trong DB)
        # -> Trả về JSON bình thường để Frontend hiện popup cảnh báo (thay vì lỗi đỏ 404)
        if result["status"] == "Unknown":
            return {
                "status": "unknown",
                "message": "Không tìm thấy dữ liệu sinh viên này trong hệ thống.",
                "data": None,
            }

        # TRƯỜNG HỢP 2: LỖI ẢNH (Không thấy mặt, ảnh mờ...)
        # -> Trả về lỗi 400 Bad Request
        else:
            detail_msg = (
                "No face detected"
                if result["status"] == "NoFace"
                else "Image processing error"
            )
            raise HTTPException(status_code=400, detail=detail_msg)

    # 3. Logic kiểm tra thời gian (Time Check) - Chỉ chạy khi đã Match
    now = datetime.now()
    check_in_time = now.strftime("%H:%M:%S")

    # Tính thời gian muộn
    is_late = False
    if now.hour > START_TIME_HOUR:
        is_late = True
    elif now.hour == START_TIME_HOUR and now.minute > LATE_THRESHOLD_MINUTES:
        is_late = True

    attendance_status = "LATE" if is_late else "ON TIME"

    # 4. Trả về kết quả thành công cho Frontend
    return {
        "status": "success",  # Frontend check: if (status == 'success') ...
        "mssv": result["mssv"],
        "name": result["name"],
        "similarity": result["similarity"],
        "check_in_time": check_in_time,
        "attendance_status": attendance_status,
        "message": f"Xin chào {result['name']}, bạn đi {'muộn' if is_late else 'đúng giờ'}!",
    }
