from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import data_app.views as data_app_views
from face_attendance import settings

router = DefaultRouter()
router.register(r'nhan-vien', data_app_views.NhanVienViewSet)
router.register(r'dang-ky-lich', data_app_views.DangKyLichViewSet)
router.register(r'lich-lam-viec', data_app_views.LichLamViecViewSet)
router.register(r'kip', data_app_views.KipViewSet)
router.register(r'ngay', data_app_views.NgayViewSet)
router.register(r'diem-danh', data_app_views.DiemDanhViewSet)
router.register(r'mau', data_app_views.MauViewSet)
router.register(r'mo-hinh', data_app_views.MoHinhViewSet)
router.register(r'muc-luong-nhan-vien', data_app_views.LuongNhanVienViewSet)


def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})


handler404 = custom_page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('web_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
