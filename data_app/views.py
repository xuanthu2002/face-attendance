from rest_framework import viewsets

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


class MauViewSet(viewsets.ModelViewSet):
    queryset = Mau.objects.all()
    serializer_class = MauSerializer


class MoHinhViewSet(viewsets.ModelViewSet):
    queryset = MoHinh.objects.all()
    serializer_class = MoHinhSerializer


class LuongNhanVienViewSet(viewsets.ModelViewSet):
    queryset = LuongNhanVien.objects.all()
    serializer_class = LuongNhanVienSerializer
