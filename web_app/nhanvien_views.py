from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from data_app.models import NhanVien
from web_app.forms import NhanVienForm


def nhanvien_list(request):
    nhanvien_list = NhanVien.objects.all()
    return render(request, 'nhanvien/nhanvien_list.html', {'nhanvien_list': nhanvien_list})


def nhanvien_detail(request, pk):
    nhanvien = get_object_or_404(NhanVien, pk=pk)
    return render(request, 'nhanvien/nhanvien_detail.html', {'nhanvien': nhanvien})


def nhanvien_edit(request, pk):
    nhanvien = get_object_or_404(NhanVien, pk=pk)
    if request.method == 'POST':
        form = NhanVienForm(request.POST, instance=nhanvien)
        if form.is_valid():
            form.save()
            return redirect('nhanvien_detail', pk=nhanvien.pk)
    else:
        form = NhanVienForm(instance=nhanvien)
    return render(request, 'nhanvien/nhanvien_edit.html', {'form': form, 'nhanvien': nhanvien})


def nhanvien_delete(request, pk):
    mau = get_object_or_404(NhanVien, pk=pk)
    if request.method == 'POST':
        mau.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
