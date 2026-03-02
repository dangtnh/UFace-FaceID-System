from datetime import datetime, timedelta
from app.core.config import settings


class AttendanceService:
    def check_attendance_status(self):
        """
        Tính toán trạng thái điểm danh: ON TIME (Đúng giờ), LATE (Muộn), ABSENT (Vắng mặt)
        Trả về: (time_string, status, is_late_bool)
        """
        now = datetime.now()
        check_in_time = now.strftime("%H:%M:%S")

        # 1. Khởi tạo mốc thời gian bắt đầu và kết thúc của tiết học hôm nay
        start_time = now.replace(
            hour=settings.START_TIME_HOUR,
            minute=settings.START_TIME_MINUTE,
            second=0,
            microsecond=0,
        )

        end_time = now.replace(
            hour=settings.END_TIME_HOUR,
            minute=settings.END_TIME_MINUTE,
            second=0,
            microsecond=0,
        )

        # 2. Tính toán thời lượng tiết học và các cột mốc (Threshold)
        # Tổng thời gian tiết học (Ví dụ từ 14:45 đến 17:00 là 2h15p)
        class_duration = end_time - start_time

        # Mốc giới hạn đi học muộn (Start time + 15 phút)
        late_deadline = start_time + timedelta(minutes=settings.LATE_THRESHOLD_MINUTES)

        # Mốc giới hạn vắng mặt (Start time + 1 nửa tổng thời gian tiết học)
        absent_deadline = start_time + (class_duration / 2)

        # 3. Logic phân loại trạng thái
        is_late = False
        status = "ON TIME"

        if now > end_time:
            # Điểm danh khi lớp đã kết thúc -> Chắc chắn vắng mặt
            status = "ABSENT"
            is_late = True

        elif now > absent_deadline:
            # Vượt quá 1 nửa thời gian tiết học -> Vắng mặt
            status = "ABSENT"
            is_late = True

        elif now > late_deadline:
            # Sau 15 phút nhưng chưa quá nửa tiết học -> Đi muộn
            status = "LATE"
            is_late = True

        else:
            # Nằm trong khoảng an toàn 15 phút đầu -> Đúng giờ
            status = "ON TIME"
            is_late = False

        return check_in_time, status, is_late


attendance_service = AttendanceService()
