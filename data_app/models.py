import os
import uuid

from django.db import models


class NhanVien(models.Model):
    hoten = models.CharField(max_length=255)
    ngay_sinh = models.DateField()
    dia_chi = models.CharField(max_length=255)
    so_dt = models.CharField(max_length=11)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.hoten


def get_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('dataset', str(instance.nhanvien.id), f'{uuid.uuid4()}.{ext}')


class Mau(models.Model):
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    link = models.ImageField(upload_to=get_upload_to)
    ngay_them = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nhanvien} - {self.link}"


class MoHinh(models.Model):
    ten = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    ngay_train = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    ds_mau = models.ManyToManyField(Mau, related_name='ds_mohinh')

    def __str__(self):
        return self.ten


class DangKyLich(models.Model):
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    lich_lam_viec = models.ForeignKey('LichLamViec', on_delete=models.CASCADE)
    ngay_co_hieu_luc = models.DateTimeField()
    ngay_het_han = models.DateTimeField()

    def __str__(self):
        return f"{self.nhanvien} - {self.lich_lam_viec}"


class LichLamViec(models.Model):
    ten = models.CharField(max_length=255)
    mota = models.CharField(max_length=255, null=True, blank=True)
    thuong = models.IntegerField(default=0)
    kip = models.ForeignKey('Kip', on_delete=models.CASCADE)
    ngay = models.ForeignKey('Ngay', on_delete=models.CASCADE)

    def __str__(self):
        return self.ten


class Kip(models.Model):
    ten = models.CharField(max_length=50)
    gio_vao = models.TimeField()
    gio_ra = models.TimeField()
    mota = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ten


class Ngay(models.Model):
    ten = models.CharField(max_length=20)
    mota = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ten


class DiemDanh(models.Model):
    ngay = models.DateField()
    gio_vao = models.TimeField()
    gio_ra = models.TimeField(null=True)
    ca_lam_viec = models.ForeignKey(DangKyLich, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ca_lam_viec} - {self.ngay}"


class LuongNhanVien(models.Model):
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    muc_luong = models.IntegerField()
    ngay_co_hieu_luc = models.DateField()

    def __str__(self):
        return f"{self.nhanvien} - {self.muc_luong}"
