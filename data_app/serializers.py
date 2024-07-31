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


class MauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mau
        fields = '__all__'


class MoHinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoHinh
        fields = ['id', 'ten', 'ngay_train', 'active', 'ds_mau']


class LuongNhanVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuongNhanVien
        fields = '__all__'


class DiemDanhSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiemDanh
        fields = '__all__'
