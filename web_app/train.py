import os

import django

# Đặt biến môi trường cho tệp settings của bạn
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_attendance.settings')

# Khởi tạo Django
django.setup()

import pickle
import cv2
import face_recognition
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from data_app.models import MoHinh
from face_attendance import settings


def train(mohinh_id):
    mohinh = MoHinh.objects.get(pk=mohinh_id)
    if not mohinh:
        return False, "Không tìm tấy mô hình"
    X = []
    y = []
    i = 0
    for mau in mohinh.ds_mau.all():
        label = mau.nhanvien.id
        img_path = os.path.join(
            settings.MEDIA_ROOT,
            mau.link.name
        )  # Đường dẫn ảnh trong DB hoặc có thể là một ImageField
        print(f"Processing {mau.nhanvien.hoten}: {img_path}")

        try:
            image = cv2.imread(img_path)
            face_encodings = face_recognition.face_encodings(image)
            if not face_encodings:
                print(f"No face found in {img_path}")
                continue
            face_encoding = face_encodings[0]
            X.append(face_encoding.tolist())
            y.append(label)
            i += 1
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            # Nếu cần, có thể thêm xử lý xóa mẫu bị lỗi hoặc thông báo

    # Chuyển đổi nhãn và dữ liệu huấn luyện
    targets = np.array(y)
    encoder = LabelEncoder()
    encoder.fit(y)
    y = encoder.transform(y)
    X1 = np.array(X)
    print("shape: " + str(X1.shape))

    save_path = os.path.join(settings.MODEL_ROOT, str(mohinh_id))
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Lưu các lớp (labels) vào file
    np.save(os.path.join(save_path, 'classes.npy'), encoder.classes_)

    # Huấn luyện mô hình SVM
    svc = SVC(kernel='linear', probability=True)
    svc.fit(X1, y)

    # Lưu mô hình đã huấn luyện
    svc_save_path = os.path.join(save_path, 'svc.sav')
    with open(svc_save_path, 'wb') as f:
        pickle.dump(svc, f)

    return True, "Success"
