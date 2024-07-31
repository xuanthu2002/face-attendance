import pickle

import face_recognition
import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder

from data_app.models import MoHinh
from face_attendance import settings


def predict(image_file):
    mohinh = MoHinh.objects.filter(active=True).first()
    img = Image.open(image_file)

    # Đảm bảo ảnh có định dạng RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')

    img = np.array(img)  # Chuyển đổi PIL image thành NumPy array

    # Tải mô hình và ánh xạ nhãn
    svc_save_path = f'{settings.MODEL_ROOT}/{mohinh.id}/svc.sav'
    classes_path = f'{settings.MODEL_ROOT}/{mohinh.id}/classes.npy'

    with open(svc_save_path, 'rb') as f:
        svc = pickle.load(f)
    encoder = LabelEncoder()
    encoder.classes_ = np.load(classes_path)

    # Tiền xử lý hình ảnh
    face_encodings = face_recognition.face_encodings(img)
    if not face_encodings:
        return None, "No faces found in the image."

    face_encoding = face_encodings[0]  # Giả sử có một khuôn mặt trên mỗi hình ảnh
    face_encoding = face_encoding.reshape(1, -1)  # Chuyển đổi định dạng để phù hợp với đầu vào của mô hình

    # Dự đoán
    prob = svc.predict_proba(face_encoding)
    result = np.argmax(prob, axis=1)
    confidence = np.max(prob)
    print(prob)
    if confidence < 0.7:  # Điều chỉnh ngưỡng theo nhu cầu
        return None, "Face not recognized with high enough confidence."

    # Lấy nhãn từ encoder
    label = encoder.inverse_transform(result)[0]
    return label, "Success"
