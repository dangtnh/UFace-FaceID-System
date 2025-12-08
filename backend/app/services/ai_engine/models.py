import torch
from facenet_pytorch import MTCNN, InceptionResnetV1


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def build_detector(device):
    """
    Cấu hình MTCNN chuẩn từ dự án cũ:
    image_size=160, margin=20, thresholds=[0.5, 0.6, 0.6]
    """
    return MTCNN(
        image_size=160,
        margin=40,
        min_face_size=40,
        thresholds=[0.5, 0.6, 0.6],
        factor=0.709,
        keep_all=False,
        post_process=True,
        device=device,
    )


def build_recognizer(device):
    """FaceNet pretrained vggface2"""
    return InceptionResnetV1(pretrained="vggface2").eval().to(device)
