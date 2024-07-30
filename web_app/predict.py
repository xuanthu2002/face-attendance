import pickle

import face_recognition
import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder

from face_attendance import settings
from web_app.recongnition import get_nhanvien_from_id


def predict(image_file, model_id):
    # Đọc hình ảnh đã được mở từ request
    img = image_file  # Đối tượng đã mở sẵn, không cần dùng Image.open

    img = np.array(img)  # Chuyển đổi PIL image thành NumPy array

    # Đảm bảo hình ảnh có định dạng RGB
    if img.ndim == 2 or img.shape[2] != 3:
        img = np.stack([img] * 3, axis=-1)  # Chuyển đổi hình ảnh xám thành RGB nếu cần

    # Tải mô hình và ánh xạ nhãn
    svc_save_path = f'{settings.MODEL_ROOT}/{model_id}/svc.sav'
    classes_path = f'{settings.MODEL_ROOT}/{model_id}/classes.npy'

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

    if confidence < 0.7:  # Điều chỉnh ngưỡng theo nhu cầu
        return None, "Face not recognized with high enough confidence."

    # Lấy nhãn từ encoder
    label = encoder.inverse_transform(result)[0]
    return label, "Success"


# Testing the function
with Image.open("C:\\Users\\DELL\\Desktop\\z5661705022804_feaf6363c4892aa6a7a42a2497b3c52f.jpg") as img:
    model_id = 1  # Thay thế bằng model_id thực tế bạn muốn sử dụng
    predicted_label, error_message = predict(img, model_id)
    if predicted_label:
        nhanvien = get_nhanvien_from_id(predicted_label)  # Thay đổi để lấy nhanvien từ nhãn
        print(f"Predicted nhanvien: {nhanvien}")
    else:
        print("Face not recognized with high enough confidence.")
