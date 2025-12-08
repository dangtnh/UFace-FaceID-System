from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.router import api_router

app = FastAPI(title=settings.PROJECT_NAME)

# Cấu hình CORS (Cho phép Web Frontend gọi vào)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. KẾT NỐI ROUTER VÀO APP
# Dòng này cực quan trọng, nếu thiếu nó Swagger sẽ trống trơn
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
