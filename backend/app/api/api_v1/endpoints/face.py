from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.face_service import face_service

router = APIRouter()

# Giả sử giờ vào lớp cố định là 8h sáng (Demo)
START_TIME_HOUR = 8
START_TIME_MINUTE = 0
LATE_THRESHOLD_MINUTES = 15  # Cho phép đi muộn 15p


@router.post("/recognize")
async def check_in(file: UploadFile = File(...)):
    # 1. Gọi AI nhận diện xem là ai
    result = await face_service.recognize_image(file)

    if result["status"] != "Match":

        detail_msg = (
            "Unknown student" if result["status"] == "Unknown" else "No face detected"
        )

        # Trả về lỗi 404 nếu là Unknown, hoặc 400 nếu là lỗi xử lý ảnh
        if result["status"] == "Unknown":
            raise HTTPException(status_code=404, detail=detail_msg)
        else:
            raise HTTPException(status_code=400, detail=detail_msg)

    # 2. Logic kiểm tra thời gian (Time Check)
    now = datetime.now()
    check_in_time = now.strftime("%H:%M:%S")

    # Tính thời gian muộn (Nếu hiện tại quá 8h15 thì là Muộn)
    is_late = False

    # Kiểm tra nếu giờ hiện tại lớn hơn giờ bắt đầu
    if now.hour > START_TIME_HOUR:
        is_late = True

    # Kiểm tra nếu cùng giờ bắt đầu nhưng phút vượt quá ngưỡng muộn
    elif now.hour == START_TIME_HOUR and now.minute > LATE_THRESHOLD_MINUTES:
        is_late = True

    attendance_status = "LATE" if is_late else "ON TIME"

    # 3. Trả về kết quả cuối cùng cho Frontend hiển thị
    return {
        "mssv": result["mssv"],
        "name": result["name"],
        "similarity": result["similarity"],
        "check_in_time": check_in_time,
        "status": attendance_status,  # "ON TIME" hoặc "LATE"
        "message": f"Xin chào {result['name']}, bạn đi {'muộn' if is_late else 'đúng giờ'}!",
    }
