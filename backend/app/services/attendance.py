from datetime import datetime
from app.core.config import settings


class AttendanceService:
    def check_attendance_status(self):
        """
        Hàm này tính toán xem thời điểm hiện tại là Muộn hay Đúng giờ.
        Trả về: (time_string, status, is_late_bool)
        """
        now = datetime.now()
        check_in_time = now.strftime("%H:%M:%S")

        is_late = False

        # 1. Nếu giờ hiện tại lớn hơn giờ quy định (Ví dụ: 9h > 8h)
        if now.hour > settings.START_TIME_HOUR:
            is_late = True

        # 2. Nếu bằng giờ (8h) nhưng phút vượt quá giới hạn ( > 15p)
        elif (
            now.hour == settings.START_TIME_HOUR
            and now.minute > settings.LATE_THRESHOLD_MINUTES
        ):
            is_late = True

        status = "LATE" if is_late else "ON TIME"

        # TODO: Sau này sẽ thêm logic gọi Repository để lưu bản ghi điểm danh vào DB ở đây.

        return check_in_time, status, is_late


attendance_service = AttendanceService()
