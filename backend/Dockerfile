FROM python:3.10-slim

WORKDIR /app

# 1. Cài đặt dependencies hệ thống
# Lưu ý: Chỉ giữ libgl1 và libglib2.0-0 nếu bạn dùng OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Cài đặt Python Dependencies (Làm bước này trước để cache pip install)
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# 3. Copy Prisma Schema và Generate Client
# Đặt ở đây để nếu chỉ sửa code backend mà không sửa schema thì không cần chạy lại bước này
COPY prisma ./prisma
RUN python3 -m prisma generate

# 4. Copy source code backend
COPY backend/ .

EXPOSE 8000

# Development CMD (giữ nguyên nếu bạn đang dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production CMD (Dùng cái này khi deploy thật)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]