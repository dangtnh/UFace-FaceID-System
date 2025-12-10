# Sử dụng Node.js phiên bản nhẹ
FROM node:18-alpine

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file định nghĩa thư viện trước (để tối ưu cache)
COPY package*.json ./

# Cài đặt các thư viện (Express, Prisma, Multer...)
RUN npm install

# Copy toàn bộ code còn lại vào container
COPY . .

# Tạo Prisma Client (Bước này cực quan trọng vì bạn dùng Prisma)
# RUN npx prisma generate

# Mở cổng 3000 (Express của bạn chạy cổng này)
EXPOSE 3000

# Chạy server
CMD ["npm", "start"]