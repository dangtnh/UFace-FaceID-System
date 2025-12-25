# 🎭 UFace - FaceID System

Automated Attendance and Face Recognition System built on **FastAPI**, **PostgreSQL** and **Docker**.

# 🚀 Key Features
- Real-time Face Recognition.
- API for managing employee/user lists.
- Automatically encode faces into Vectors and store in the Database.
- Fully packaged system with Docker & Docker Compose.

# 🛠 Yêu cầu hệ thống (Prerequisites)
To run the project, your machine needs to have the following installed:
- **Git**
- **Docker** & **Docker Compose** (latest version)

---

# ⚙️ System Installation and Usage Guide (Quick Start)
## 1. Clone from git repository
```
git clone [https://github.com/dangtnh/UFace-FaceID-System.git]
cd UFace-FaceID-System
```

## 2. Create enviroment and data files
```
cp .env.example .env

mkdir -p data/images
mkdir -p data/vectors
```

## 3. Docker commands
- Build from scratch
```
docker compose up --build -d
```

- Create and draw tables in Database
```
docker compose run --rm prisma_studio npx prisma migrate dev --name init

docker compose run --rm prisma_studio npx prisma migrate dev --name init --skip-generate
```

- Restart container backend 
```
docker compose restart backend
```
- Turn on all containers and turn off all  containers
```
docker compose up -d

docker compose down
```

- Delete all data in container
```
docker compose down -v
```

