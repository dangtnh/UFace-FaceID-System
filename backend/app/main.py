from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.router import api_router
from prisma import Prisma
from app.core.database import prisma


# --- THAY ĐỔI 2: Dùng lifespan để quản lý kết nối DB ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await prisma.connect()
        print("✅ Connected to Database via Prisma")
    except Exception as e:
        print(f"❌ Could not connect to Database: {e}")

    yield

    if prisma.is_connected():
        await prisma.disconnect()
        print("🛑 Disconnected from Database")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
# --------------------------------

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    # LƯU Ý: Khi deploy production, hãy thay ["*"] bằng domain cụ thể của frontend
    # Ví dụ: allow_origins=["https://my-frontend.com", "http://localhost:3000"]
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
