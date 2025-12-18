from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.router import api_router
from prisma import Prisma

app = FastAPI(title=settings.PROJECT_NAME)

prisma = Prisma()


# --- BỔ SUNG LOGIC KẾT NỐI DB ---
@app.on_event("startup")
async def startup():
    try:
        await prisma.connect()
        print("✅ Connected to Database via Prisma")
    except Exception as e:
        print(f"❌ Could not connect to Database: {e}")


@app.on_event("shutdown")
async def shutdown():
    if prisma.is_connected():
        await prisma.disconnect()
        print("🛑 Disconnected from Database")


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
