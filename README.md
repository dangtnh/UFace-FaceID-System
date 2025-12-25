# 🎭 UFace - FaceID System

Automated Attendance and Face Recognition System built on **FastAPI**, **PostgreSQL** and **Docker**.

# 🚀 Key Features
- Real-time Face Recognition.
- API for managing employee/user lists.
- Automatically encode faces into Vectors and store in the Database.
- Fully packaged system with Docker & Docker Compose.

# 🛠 System Requirements (Prerequisites)
To run the project, your machine needs to have the following installed:
- **Git**.
- **Docker** & **Docker Compose** (latest version).



# ⚡ Performance Optimization (Optional: GPU Support)
By default, the system runs on CPU to keep the installation size small (~1GB). If you have a supported NVIDIA GPU and want faster face recognition (10x-20x speedup), follow these steps:
1. Open **requirements.txt**.
2. Remove the first line: **--extra-index-url https://download.pytorch.org/whl/cpu**.
3. Edit the torch versions to remove +cpu:
```
torch>=2.2.0
torchvision>=0.17.0
```
4. Add the GPU index URL to the top of the file:
```
--extra-index-url [https://download.pytorch.org/whl/cu118](https://download.pytorch.org/whl/cu118)
```
5. Rebuild the container and follow the next step to build system on your computer: 
```
docker compose up --build -d
```
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

