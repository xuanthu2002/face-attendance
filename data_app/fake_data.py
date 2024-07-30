import os

import django

# Đặt biến môi trường cho tệp settings của bạn
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_attendance.settings')

# Khởi tạo Django
django.setup()

from django.core.files import File
from data_app.models import NhanVien, Mau


def load_images_to_mau(nhanvien_id, images_folder_path):
    # Lấy đối tượng nhân viên từ ID
    try:
        nhanvien = NhanVien.objects.get(id=nhanvien_id)
    except NhanVien.DoesNotExist:
        print(f"Nhân viên với ID {nhanvien_id} không tồn tại.")
        return

    # Lấy danh sách tất cả các file ảnh trong thư mục
    image_files = [f for f in os.listdir(images_folder_path) if os.path.isfile(os.path.join(images_folder_path, f))]

    for image_file in image_files:
        image_path = os.path.join(images_folder_path, image_file)
        with open(image_path, 'rb') as f:
            # Tạo đối tượng Mau mới và lưu vào database
            django_file = File(f, name=image_file)
            mau = Mau(nhanvien=nhanvien, link=django_file)
            mau.save()
            print(f"Đã lưu ảnh {image_file} cho nhân viên {nhanvien}")


# Gọi hàm với ID của nhân viên và đường dẫn đến thư mục chứa ảnh
load_images_to_mau(3, 'D:\\Learn\\PTHTTM\\face_attendance\\dataset\\test\\sontung')
