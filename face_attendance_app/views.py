from rest_framework import viewsets
from .models import *
from .serializers import *


class NhanVienViewSet(viewsets.ModelViewSet):
    queryset = NhanVien.objects.all()
    serializer_class = NhanVienSerializer


class DangKyLichViewSet(viewsets.ModelViewSet):
    queryset = DangKyLich.objects.all()
    serializer_class = DangKyLichSerializer


class LichLamViecViewSet(viewsets.ModelViewSet):
    queryset = LichLamViec.objects.all()
    serializer_class = LichLamViecSerializer


class KipViewSet(viewsets.ModelViewSet):
    queryset = Kip.objects.all()
    serializer_class = KipSerializer


class NgayViewSet(viewsets.ModelViewSet):
    queryset = Ngay.objects.all()
    serializer_class = NgaySerializer


class DiemDanhViewSet(viewsets.ModelViewSet):
    queryset = DiemDanh.objects.all()
    serializer_class = DiemDanhSerializer


class MauViewSet(viewsets.ModelViewSet):
    queryset = Mau.objects.all()
    serializer_class = MauSerializer


class MoHinhViewSet(viewsets.ModelViewSet):
    queryset = MoHinh.objects.all()
    serializer_class = MoHinhSerializer


class MauMoHinhViewSet(viewsets.ModelViewSet):
    queryset = MauMoHinh.objects.all()
    serializer_class = MauMoHinhSerializer


class MucLuongViewSet(viewsets.ModelViewSet):
    queryset = MucLuong.objects.all()
    serializer_class = MucLuongSerializer


class MucLuongNhanVienViewSet(viewsets.ModelViewSet):
    queryset = MucLuongNhanVien.objects.all()
    serializer_class = MucLuongNhanVienSerializer
