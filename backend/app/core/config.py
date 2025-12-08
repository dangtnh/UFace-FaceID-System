import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FaceID System"

    # --- Config Database (Giữ nguyên của AchiStay) ---
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # --- Config AI (Lấy từ config.py dự án cũ) ---
    VECTOR_DB_PATH: str = "/app/data/vectors"  # Đường dẫn trong Docker
    VECTOR_DIM: int = 512
    DETECTION_CONF_THRESH: float = 0.80  # Ngưỡng tin cậy tìm mặt
    RECOGNITION_THRESH: float = 0.65  # Ngưỡng nhận diện (Cosine Similarity)

    class Config:
        env_file = ".env"


settings = Settings()
