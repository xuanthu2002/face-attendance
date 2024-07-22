from rest_framework import serializers
from .models import *


class NhanVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhanVien
        fields = '__all__'


class DangKyLichSerializer(serializers.ModelSerializer):
    class Meta:
        model = DangKyLich
        fields = '__all__'


class LichLamViecSerializer(serializers.ModelSerializer):
    class Meta:
        model = LichLamViec
        fields = '__all__'


class KipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kip
        fields = '__all__'


class NgaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ngay
        fields = '__all__'


class DiemDanhSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiemDanh
        fields = '__all__'


class MauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mau
        fields = '__all__'


class MoHinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoHinh
        fields = '__all__'


class MauMoHinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = MauMoHinh
        fields = '__all__'


class MucLuongSerializer(serializers.ModelSerializer):
    class Meta:
        model = MucLuong
        fields = '__all__'


class MucLuongNhanVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = MucLuongNhanVien
        fields = '__all__'
