import pickle
from io import BytesIO

import face_recognition
import numpy as np
from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render
from sklearn.preprocessing import LabelEncoder

from data_app.serializers import NhanVienSerializer
from face_attendance import settings
from web_app.recongnition import get_nhanvien_from_id


def diem_danh(request):
    if request.method == 'GET':
        return render(request, 'diemdanh/diemdanh.html')

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            nhanvien, error_message = nhan_dien(image)
            serializer = NhanVienSerializer(nhanvien)
            if nhanvien:
                return JsonResponse({'success': True, 'nhanvien': serializer.data})
            else:
                return JsonResponse({'success': False, 'error_message': error_message})
        else:
            return JsonResponse({'success': False, 'error_message': 'No image uploaded'})


def nhan_dien(image_file):
    # Load the image from the uploaded file
    img = Image.open(BytesIO(image_file.read()))
    img = np.array(img)  # Convert PIL image to NumPy array

    # Load model and label mapping
    model_id = 1  # Replace with the actual model_id you want to use
    svc_save_path = f'{settings.MODEL_ROOT}/{model_id}/svc.sav'
    classes_path = f'{settings.MODEL_ROOT}/{model_id}/classes.npy'

    with open(svc_save_path, 'rb') as f:
        svc = pickle.load(f)
    encoder = LabelEncoder()
    encoder.classes_ = np.load(classes_path)

    # Preprocess image
    face_encodings = face_recognition.face_encodings(img)
    if not face_encodings:
        return None, "No faces found in the image."

    face_encoding = face_encodings[0]  # Assume one face per image
    face_encoding = face_encoding.reshape(1, -1)  # Reshape for model input

    # Predict
    prob = svc.predict_proba(face_encoding)
    result = np.argmax(prob, axis=1)
    confidence = np.max(prob)

    if confidence < 0.7:  # Adjust threshold as needed
        return None, "Face not recognized with high enough confidence."

    predicted_class_id = result[0]
    nhanvien = get_nhanvien_from_id(predicted_class_id)
    return nhanvien, None
