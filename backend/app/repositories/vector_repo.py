import os
import faiss
import numpy as np
import pickle
from app.core.config import settings


class VectorRepository:
    def __init__(self):
        os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
        self.index_path = os.path.join(settings.VECTOR_DB_PATH, "face.index")
        self.labels_path = os.path.join(settings.VECTOR_DB_PATH, "labels.pkl")
        self.index = None
        self.labels = []
        self._load()

    def _load(self):
        """Tải dữ liệu từ ổ cứng"""
        if os.path.exists(self.index_path) and os.path.exists(self.labels_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.labels_path, "rb") as f:
                self.labels = pickle.load(f)
            print(f"📦 Vector Repo: Loaded {len(self.labels)} vectors.")
        else:
            self.index = faiss.IndexFlatIP(settings.VECTOR_DIM)
            self.labels = []

    def _save(self):
        """Lưu xuống ổ cứng (Private method)"""
        faiss.write_index(self.index, self.index_path)
        with open(self.labels_path, "wb") as f:
            pickle.dump(self.labels, f)

    def add(self, vector: np.ndarray, label: str):
        """Thêm dữ liệu vào kho"""
        vec_reshaped = np.expand_dims(vector.astype(np.float32), axis=0)
        self.index.add(vec_reshaped)
        self.labels.append(label)
        self._save()

    def search_similar(self, vector: np.ndarray, k=1):
        """Tìm kiếm trong kho"""
        if self.index.ntotal == 0:
            return None

        vec_reshaped = np.expand_dims(vector.astype(np.float32), axis=0)
        sims, idxs = self.index.search(vec_reshaped, k)

        best_idx = idxs[0][0]
        if best_idx == -1:
            return None

        return {"label": self.labels[best_idx], "similarity": float(sims[0][0])}


vector_repo = VectorRepository()
