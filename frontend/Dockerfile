# 1. Dùng Node Alpine cho nhẹ
FROM node:18-alpine

WORKDIR /app

# 2. Copy file config và cài thư viện
COPY package*.json ./

# Lưu ý: Nếu mạng chậm, có thể dùng 'npm ci' thay vì 'npm install' để cài nhanh hơn
RUN npm install

# 3. Copy source code
COPY . .

# 4. Mở cổng 3000 (Mặc định của Vite)
EXPOSE 3000

# 5. Chạy server ở chế độ Dev
# Lưu ý: Cần thêm '--host' để truy cập được từ bên ngoài Docker (từ máy thật của bạn)
CMD ["npm", "run", "dev"]