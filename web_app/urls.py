from django.urls import path

from . import mau_views, nhanvien_views, mohinh_views
from .diemdanh_views import diemdanh
from .home_views import home
from .nhandien_views import nhandien

urlpatterns = [
    path('', home, name='home'),

    path('nhan-vien/', nhanvien_views.nhanvien_list, name='nhanvien_list'),
    path('nhan-vien/<int:pk>/', nhanvien_views.nhanvien_detail, name='nhanvien_detail'),
    path('nhan-vien/edit/<int:pk>/', nhanvien_views.nhanvien_edit, name='nhanvien_edit'),
    path('nhan-vien/delete/<int:pk>/', nhanvien_views.nhanvien_delete, name='nhanvien_delete'),

    path('mau/', mau_views.mau_list, name='mau_list'),
    path('mau/create/<int:nhanvien_id>/', mau_views.mau_create, name='mau_create'),
    path('mau/delete/<int:pk>/', mau_views.mau_delete, name='mau_delete'),

    path('nhan-dien/', nhandien, name='nhan_dien'),
    path('diem-danh/', diemdanh, name='diem_danh'),

    path('mohinh/', mohinh_views.mohinh_list, name='mohinh_list'),
    path('mohinh/create/', mohinh_views.mohinh_create, name='mohinh_create'),
    path('mohinh/<int:pk>/', mohinh_views.mohinh_detail, name='mohinh_detail'),
    path('mohinh/<int:pk>/edit/', mohinh_views.mohinh_edit, name='mohinh_edit'),
    path('mohinh/<int:pk>/delete/', mohinh_views.mohinh_delete, name='mohinh_delete'),
    path('mohinh/update-status/', mohinh_views.mohinh_update_status, name='mohinh_update_status'),
    path('mohinh/<int:mohinh_id>/nhanvien/<int:nhanvien_id>/mau_list/', mohinh_views.nhanvien_mau_list,
         name='nhanvien_mau_list'),
    path('mohinh/<int:mohinh_id>/them_mau/<int:mau_id>/', mohinh_views.them_mau, name='mohinh_them_mau'),
    path('mohinh/<int:mohinh_id>/xoa_mau/<int:mau_id>/', mohinh_views.xoa_mau, name='mohinh_xoa_mau'),
    path('mohinh/train/', mohinh_views.train_mohinh, name='train_mohinh')
]
