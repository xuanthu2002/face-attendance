from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from data_app.models import NhanVien, Mau
from web_app.forms import MauForm


def mau_list(request):
    nhanvien_id = request.GET.get('nhanvien_id')
    if not nhanvien_id:
        return redirect('nhanvien_list')
    nhanvien = get_object_or_404(NhanVien, id=nhanvien_id)
    mau_list = Mau.objects.filter(nhanvien=nhanvien).order_by('ngay_them').all()
    return render(request, 'mau/mau_list.html', {'mau_list': mau_list, 'nhanvien': nhanvien})


def mau_create(request, nhanvien_id):
    nhanvien = get_object_or_404(NhanVien, id=nhanvien_id)
    if request.method == 'POST':
        form = MauForm(request.POST, request.FILES)
        if form.is_valid():
            mau = form.save(commit=False)
            mau.nhanvien = nhanvien
            mau.save()
            return redirect(f'{reverse("mau_list")}?nhanvien_id={nhanvien.id}')
    else:
        form = MauForm()
    return render(request, 'mau/mau_form.html', {'form': form, 'nhanvien': nhanvien})


def mau_delete(request, pk):
    mau = get_object_or_404(Mau, pk=pk)
    if request.method == 'POST':
        mau.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
