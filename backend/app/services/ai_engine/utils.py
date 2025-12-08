from PIL import Image, ImageOps
import io
import numpy as np


def normalize_pil(img: Image.Image) -> Image.Image:
    """Xoay ảnh theo EXIF (fix lỗi ảnh chụp điện thoại bị ngược)"""
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    return img.convert("RGB")


def read_image_file(file_bytes: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(file_bytes))
    return normalize_pil(img)


def l2_normalize(embedding: np.ndarray) -> np.ndarray:
    """Chuẩn hóa vector (Quan trọng để tính Cosine Similarity)"""
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm
