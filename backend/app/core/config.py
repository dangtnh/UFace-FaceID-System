import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 1. Load file .env ngay lập tức để code bên dưới đọc được
load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FaceID System"

    # --- CẤU HÌNH DATABASE (Cách của bạn) ---
    # Lấy từng món từ biến môi trường
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "faceid_db")

    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"
    )

    # --- CẤU HÌNH AI ---
    VECTOR_DB_PATH: str = "/app/data/vectors"
    VECTOR_DIM: int = 512
    DETECTION_CONF_THRESH: float = 0.80
    RECOGNITION_THRESH: float = 0.7

    class Config:
        env_file = ".env"


settings = Settings()
