from django.db import models


class NhanVien(models.Model):
    hoTen = models.CharField(max_length=255)
    ngaySinh = models.DateField()
    diaChi = models.CharField(max_length=255)
    soDT = models.CharField(max_length=11)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.hoTen


class DangKyLich(models.Model):
    nhanVien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    lichLamViec = models.ForeignKey('LichLamViec', on_delete=models.CASCADE)
    ngayCoHieuLuc = models.DateTimeField()

    def __str__(self):
        return f"{self.nhanVien} - {self.lichLamViec}"


class LichLamViec(models.Model):
    ten = models.CharField(max_length=255)
    moTa = models.CharField(max_length=255, null=True, blank=True)
    thuong = models.IntegerField()
    kip = models.ForeignKey('Kip', on_delete=models.CASCADE)
    ngay = models.ForeignKey('Ngay', on_delete=models.CASCADE)

    def __str__(self):
        return self.ten


class Kip(models.Model):
    ten = models.CharField(max_length=50)
    gioVao = models.TimeField()
    gioRa = models.TimeField()
    moTa = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ten


class Ngay(models.Model):
    ten = models.CharField(max_length=20)
    moTa = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ten


class DiemDanh(models.Model):
    ngay = models.DateField()
    gioVao = models.TimeField()
    gioRa = models.TimeField()
    dangKyLich = models.ForeignKey(DangKyLich, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dangKyLich} - {self.ngay}"


class Mau(models.Model):
    nhanVien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    ngayThem = models.DateTimeField()

    def __str__(self):
        return f"{self.nhanVien} - {self.link}"


class MoHinh(models.Model):
    ten = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    ngayTrain = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.ten


class MauMoHinh(models.Model):
    mau = models.ForeignKey(Mau, on_delete=models.CASCADE)
    moHinh = models.ForeignKey(MoHinh, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mau} - {self.moHinh}"


class MucLuong(models.Model):
    luong = models.IntegerField()

    def __str__(self):
        return str(self.luong)


class MucLuongNhanVien(models.Model):
    nhanVien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    mucLuong = models.ForeignKey(MucLuong, on_delete=models.CASCADE)
    ngayCoHieuLuc = models.DateField()

    def __str__(self):
        return f"{self.nhanVien} - {self.mucLuong}"
