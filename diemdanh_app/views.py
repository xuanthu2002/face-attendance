from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from diemdanh_app.serializers import DiemDanhSerializer
from data_app.models import DiemDanh, NhanVien, DangKyLich


class DiemDanhViewSet(viewsets.ModelViewSet):
    queryset = DiemDanh.objects.all()
    serializer_class = DiemDanhSerializer

    def create(self, request, *args, **kwargs):
        nhanvien_id = request.data.get('nhanvien_id')
        if not nhanvien_id:
            return Response({"error": "nhanvien_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nhanvien = NhanVien.objects.get(id=nhanvien_id)
        except NhanVien.DoesNotExist:
            return Response({"error": "NhanVien not found"}, status=status.HTTP_404_NOT_FOUND)

        dang_ky_lich = self.get_lich_diem_danh(nhanvien_id)
        if not dang_ky_lich:
            return Response({"error": "No shift found for today"}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        today = now.date()

        # Kiểm tra nếu đã có bản ghi điểm danh trong ngày
        diem_danh = DiemDanh.objects.filter(ca_lam_viec=dang_ky_lich, ngay=today).first()
        if diem_danh:  # Nếu đã có gio_vao, cập nhật gio_ra
            if diem_danh.gio_vao:
                diem_danh.gio_ra = now.time()
                diem_danh.save()
                return Response({"message": "Check-out time recorded", "gio_ra": diem_danh.gio_ra},
                                status=status.HTTP_200_OK)
        else:  # Nếu chưa có, tạo bản ghi mới với gio_vao
            DiemDanh.objects.create(ca_lam_viec=dang_ky_lich, ngay=today, gio_vao=now.time())
            return Response({"message": "Check-in time recorded", "gio_vao": now.time()}, status=status.HTTP_200_OK)

    def get_lich_diem_danh(self, nhanvien_id):
        def time_diff(time1, time2):
            t1 = timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
            t2 = timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second)
            return abs(t1 - t2)

        now = timezone.now()
        today = now.date()
        ds_dang_ky_lich = DangKyLich.objects.filter(
            nhanvien__id=nhanvien_id,
            ngay_co_hieu_luc__date__lte=today,
            ngay_het_han__date__gte=today,
            lich_lam_viec__ngay__id=(today.weekday() + 1),
        ).all()
        if not ds_dang_ky_lich:
            return None

        lich_lam_viec_gan_nhat = None
        min_diff = timedelta.max
        for dang_ky_lich in ds_dang_ky_lich:
            kip = dang_ky_lich.lich_lam_viec.kip
            diff_in = time_diff(kip.gio_vao, now)
            diff_out = time_diff(kip.gio_ra, now)

            # Lấy khoảng cách thời gian nhỏ nhất
            if diff_in < min_diff:
                min_diff = diff_in
                lich_lam_viec_gan_nhat = dang_ky_lich
            if diff_out < min_diff:
                min_diff = diff_out
                lich_lam_viec_gan_nhat = dang_ky_lich
        return lich_lam_viec_gan_nhat
