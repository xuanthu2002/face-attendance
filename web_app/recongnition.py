import json
import os

import django
from PIL import Image

# Đặt biến môi trường cho tệp settings của bạn
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_attendance.settings')

# Khởi tạo Django
django.setup()

import numpy as np
import tensorflow as tf
import torch
from facenet_pytorch import InceptionResnetV1

from face_attendance import settings
from data_app.models import MoHinh, NhanVien

# Load Facenet model
base_model = InceptionResnetV1(pretrained='vggface2').eval()


def get_model_and_mapping(model_id):
    try:
        # Lấy đường dẫn của mô hình từ cơ sở dữ liệu
        mohinh = MoHinh.objects.get(id=model_id)
        model_dir = os.path.join(settings.MODEL_ROOT, str(mohinh.id))

        # Tải mô hình
        model_path = os.path.join(model_dir, 'facenet_model.keras')
        model = tf.keras.models.load_model(model_path)

        # Tải label mapping
        mapping_path = os.path.join(model_dir, 'label_mapping.json')
        with open(mapping_path, 'r') as f:
            label_mapping = json.load(f)

        return model, label_mapping
    except MoHinh.DoesNotExist:
        raise FileNotFoundError(f"Model with id {model_id} not found in database.")
    except Exception as e:
        raise RuntimeError(f"Error loading model or mapping: {e}")


def preprocess_image(img):
    if img.mode != 'RGB':
        img = img.convert('RGB')  # Convert image to RGB if not already
    img = img.resize((160, 160))  # Resize to the input size required by the model
    img_array = np.array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array


def extract_features(image):
    # Convert images to PyTorch tensors and preprocess
    image_tensor = (torch.tensor(image)
                    .permute(0, 3, 1, 2).float())  # Change order to (batch_size, channels, height, width)

    # Extract features
    with torch.no_grad():
        features = base_model(image_tensor)

    return features.numpy()


def recognize_face(image, model_id):
    # Preprocess the image
    image = preprocess_image(image)

    # Extract features
    features = extract_features(image)

    # Load model and label mapping
    model, label_mapping = get_model_and_mapping(model_id)

    # Predict using the trained model
    predictions = model.predict(features)

    # Xác suất dự đoán cho từng lớp
    probabilities = tf.nn.softmax(predictions).numpy()

    predicted_class = np.argmax(predictions, axis=1)
    predicted_probability = np.max(probabilities, axis=1)
    print(predicted_class, predicted_probability)

    # Return predicted label if confidence is high enough
    # if predicted_probability[0] < 0.7:
    #     return None
    return label_mapping.get(str(predicted_class[0]), "Unknown")


def get_nhanvien_from_id(nhanvien_id):
    try:
        nhanvien = NhanVien.objects.get(id=nhanvien_id)
        return nhanvien
    except NhanVien.DoesNotExist:
        return "Unknown"


# Example usage
if __name__ == '__main__':
    with Image.open("../dataset/test/sontung/006.jpg") as img:
        model_id = 1  # Replace with the actual model_id you want to use
        predicted_class_id = recognize_face(img, model_id)
        if predicted_class_id:
            nhanvien = get_nhanvien_from_id(predicted_class_id)
            print(f"Predicted nhanvien: {nhanvien}")
        else:
            print("Face not recognized with high enough confidence.")
