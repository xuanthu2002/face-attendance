from django.http import JsonResponse
from django.shortcuts import render

from data_app.models import NhanVien
from data_app.serializers import NhanVienSerializer
from web_app.predict import predict


def nhandien(request):
    if request.method == 'GET':
        return render(request, 'diemdanh/diemdanh.html')

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            nhanvien_id, error_message = predict(image)
            if not nhanvien_id:
                return JsonResponse({'success': False, 'error_message': error_message})
            nhanvien = NhanVien.objects.get(pk=nhanvien_id)
            serializer = NhanVienSerializer(nhanvien)
            if nhanvien:
                return JsonResponse({'success': True, 'nhanvien': serializer.data})
            else:
                return JsonResponse({'success': False, 'error_message': error_message})
        else:
            return JsonResponse({'success': False, 'error_message': 'No image uploaded'})
