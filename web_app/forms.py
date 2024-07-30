from django import forms

from data_app.models import Mau, NhanVien, MoHinh


class MauForm(forms.ModelForm):
    class Meta:
        model = Mau
        fields = ['link']


class NhanVienForm(forms.ModelForm):
    class Meta:
        model = NhanVien
        fields = ['hoten', 'ngay_sinh', 'dia_chi', 'so_dt', 'email']


class MoHinhForm(forms.ModelForm):
    class Meta:
        model = MoHinh
        fields = ['ten', 'active']
