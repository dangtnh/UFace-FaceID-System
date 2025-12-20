from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.face_service import face_service
from app.services.attendance import attendance_service

router = APIRouter()


@router.post("/recognize")
async def check_in(file: UploadFile = File(...)):
    # 1. Gọi AI nhận diện
    result = await face_service.recognize_image(file)

    # 2. Xử lý các trường hợp lỗi/unknown
    if result["status"] != "Match":
        if result["status"] == "Unknown":
            return {
                "status": "unknown",
                "message": "Không tìm thấy sinh viên.",
                "box": result.get("box"),
                "score": result.get("score"),
                "similarity": result.get("similarity"),
                "name": "Unknown",
            }
        # else:
        #     raise HTTPException(status_code=400, detail="No face detected or Error")

    # 3. Gọi Service tính toán giờ giấc (Thay vì if/else tại đây)
    check_in_time, status, is_late = attendance_service.check_attendance_status()

    # 4. Trả kết quả
    return {
        "status": "success",
        "mssv": result["mssv"],
        "name": result["name"],
        "similarity": result["similarity"],
        "check_in_time": check_in_time,
        "attendance_status": status,
        "message": f"Xin chào {result['name']}, bạn đi {'muộn' if is_late else 'đúng giờ'}!",
        "box": result.get("box"),
        "score": result.get("score"),
    }
