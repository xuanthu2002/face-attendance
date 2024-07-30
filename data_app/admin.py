from django.contrib import admin

from .models import (
    NhanVien, Mau, MoHinh, DangKyLich, LichLamViec, Kip, Ngay, DiemDanh, LuongNhanVien
)


@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ('hoten', 'ngay_sinh', 'dia_chi', 'so_dt', 'email')
    search_fields = ('hoten', 'email')


@admin.register(Mau)
class MauAdmin(admin.ModelAdmin):
    list_display = ('nhanvien', 'link', 'ngay_them')
    search_fields = ('nhanvien__hoten',)
    list_filter = ('ngay_them',)
    readonly_fields = ('ngay_them',)


@admin.register(MoHinh)
class MoHinhAdmin(admin.ModelAdmin):
    list_display = ('ten', 'link', 'ngay_train', 'active')
    search_fields = ('ten',)
    list_filter = ('active', 'ngay_train')
    filter_horizontal = ('ds_mau',)


@admin.register(DangKyLich)
class DangKyLichAdmin(admin.ModelAdmin):
    list_display = ('nhanvien', 'lich_lam_viec', 'ngay_co_hieu_luc', 'ngay_het_han')
    search_fields = ('nhanvien__hoten', 'lich_lam_viec__ten')
    list_filter = ('ngay_co_hieu_luc', 'ngay_het_han')


@admin.register(LichLamViec)
class LichLamViecAdmin(admin.ModelAdmin):
    list_display = ('ten', 'mota', 'thuong', 'kip', 'ngay')
    search_fields = ('ten', 'mota')
    list_filter = ('kip', 'ngay')


@admin.register(Kip)
class KipAdmin(admin.ModelAdmin):
    list_display = ('ten', 'gio_vao', 'gio_ra', 'mota')
    search_fields = ('ten', 'mota')


@admin.register(Ngay)
class NgayAdmin(admin.ModelAdmin):
    list_display = ('ten', 'mota')
    search_fields = ('ten', 'mota')


@admin.register(DiemDanh)
class DiemDanhAdmin(admin.ModelAdmin):
    list_display = ('ca_lam_viec', 'ngay', 'gio_vao', 'gio_ra')
    search_fields = ('ca_lam_viec__nhanvien__hoten', 'ngay')
    list_filter = ('ngay', 'ca_lam_viec__lich_lam_viec')


@admin.register(LuongNhanVien)
class LuongNhanVienAdmin(admin.ModelAdmin):
    list_display = ('nhanvien', 'muc_luong', 'ngay_co_hieu_luc')
    search_fields = ('nhanvien__hoten',)
    list_filter = ('ngay_co_hieu_luc',)
