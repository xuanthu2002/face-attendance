import os

import django

# Đặt biến môi trường cho tệp settings của bạn
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_attendance.settings')

# Khởi tạo Django
django.setup()

import numpy as np
import tensorflow as tf
import torch
from PIL import Image
from facenet_pytorch import InceptionResnetV1
from sklearn.utils import class_weight
from face_attendance import settings
from data_app.models import MoHinh, Mau

# Load pre-trained FaceNet model
device = 'cpu'
face_model = InceptionResnetV1(pretrained='vggface2').eval().to(device)


def load_images_from_db(model_id):
    images = []
    labels = []
    # Get samples related to the specific model
    mohinh = MoHinh.objects.filter(id=model_id).get()
    mau_mohinh_ids = mohinh.ds_mau.all()
    for mau in Mau.objects.filter(id__in=mau_mohinh_ids):
        img_path = os.path.join(settings.MEDIA_ROOT, mau.link.name)
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((160, 160))  # Resize image
            img_array = np.array(img)
            if img_array.shape[-1] == 4:  # Handle RGBA images
                img_array = img_array[..., :3]
            images.append(img_array)
            labels.append(mau.nhanvien.id)
    return np.array(images), np.array(labels)


import json
from sklearn.preprocessing import LabelEncoder


def save_label_mapping(labels, model_dir):
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    label_mapping = dict(zip(label_encoder.transform(label_encoder.classes_), label_encoder.classes_))
    label_mapping = {int(k): str(v) for k, v in label_mapping.items()}
    mapping_path = os.path.join(model_dir, 'label_mapping.json')
    with open(mapping_path, 'w') as f:
        json.dump(label_mapping, f)


def extract_features(images):
    features = []
    for img in images:
        img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0).permute(0, 3, 1, 2).to(
            device)  # Convert to tensor and rearrange dimensions
        with torch.no_grad():
            feature = face_model(img_tensor).cpu().numpy()
        features.append(feature)
    return np.array(features).reshape(len(features), -1)


def train_model(model_id):
    images, labels = load_images_from_db(model_id)
    images = (images / 255.0).astype(np.float32)  # Normalize images

    features = extract_features(images)

    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(labels_encoded), y=labels_encoded)
    class_weights_dict = dict(enumerate(class_weights))

    # Define a simple neural network model using TensorFlow
    num_classes = len(np.unique(labels_encoded))
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(features.shape[1],)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')  # Ensure correct number of output classes
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Create TensorFlow dataset
    dataset = tf.data.Dataset.from_tensor_slices((features, labels_encoded))
    dataset = dataset.shuffle(buffer_size=100).batch(32)

    # Train the model
    model.fit(dataset, epochs=10, class_weight=class_weights_dict)

    # Create a directory for the model
    model_dir = os.path.join(settings.MODEL_ROOT, str(model_id))
    os.makedirs(model_dir, exist_ok=True)

    # Save the model
    model.save(os.path.join(model_dir, 'facenet_model.keras'))
    save_label_mapping(labels, model_dir)


if __name__ == '__main__':
    train_model(1)  # Replace with the actual model_id you want to train
