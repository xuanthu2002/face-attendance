from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from face_attendance_app import views

router = DefaultRouter()
router.register(r'nhan-vien', views.NhanVienViewSet)
router.register(r'dang-ky-lich', views.DangKyLichViewSet)
router.register(r'lich-lam-viec', views.LichLamViecViewSet)
router.register(r'kip', views.KipViewSet)
router.register(r'ngay', views.NgayViewSet)
router.register(r'diem-danh', views.DiemDanhViewSet)
router.register(r'mau', views.MauViewSet)
router.register(r'mo-hinh', views.MoHinhViewSet)
router.register(r'mau-mo-hinh', views.MauMoHinhViewSet)
router.register(r'muc-luong', views.MucLuongViewSet)
router.register(r'muc-luong-nhan-vien', views.MucLuongNhanVienViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
