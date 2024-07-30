import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from data_app.models import MoHinh, Mau, NhanVien
from .forms import MoHinhForm


def mohinh_list(request):
    mohinh_list = MoHinh.objects.all()
    return render(request, 'mohinh/mohinh_list.html', {'mohinh_list': mohinh_list})


def mohinh_create(request):
    if request.method == 'POST':
        form = MoHinhForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mohinh_list')
    else:
        form = MoHinhForm()
    return render(request, 'mohinh/mohinh_form.html', {'form': form})


def mohinh_detail(request, pk):
    mohinh = get_object_or_404(MoHinh, pk=pk)
    nhanvien_list = NhanVien.objects.all()

    context = {
        'mohinh': mohinh,
        'nhanvien_list': nhanvien_list,
    }
    return render(request, 'mohinh/mohinh_detail.html', context)


def mohinh_edit(request, pk):
    mohinh = get_object_or_404(MoHinh, pk=pk)
    if request.method == 'POST':
        form = MoHinhForm(request.POST, instance=mohinh)
        if form.is_valid():
            form.save()
            return redirect('mohinh_list')
    else:
        form = MoHinhForm(instance=mohinh)
    return render(request, 'mohinh/mohinh_form.html', {'form': form})


def mohinh_delete(request, pk):
    mohinh = get_object_or_404(MoHinh, pk=pk)
    if request.method == 'POST':
        mohinh.delete()
        return redirect('mohinh_list')
    return render(request, 'mohinh/mohinh_confirm_delete.html', {'mohinh': mohinh})


def them_mau(request, mohinh_id, mau_id):
    mohinh = get_object_or_404(MoHinh, pk=mohinh_id)
    mau = get_object_or_404(Mau, pk=mau_id)
    mohinh.ds_mau.add(mau)
    return redirect('nhanvien_mau_list', mohinh_id=mohinh_id, nhanvien_id=mau.nhanvien.id)


def xoa_mau(request, mohinh_id, mau_id):
    mohinh = get_object_or_404(MoHinh, pk=mohinh_id)
    mau = get_object_or_404(Mau, pk=mau_id)
    mohinh.ds_mau.remove(mau)
    return redirect('nhanvien_mau_list', mohinh_id=mohinh_id, nhanvien_id=mau.nhanvien.id)


@require_POST
def mohinh_update_status(request):
    try:
        data = json.loads(request.body)
        active_id = data.get('active_id')
        if active_id:
            MoHinh.objects.update(active=False)
            mohinh = MoHinh.objects.get(pk=active_id)
            mohinh.active = True
            mohinh.save()
            return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def nhanvien_mau_list(request, mohinh_id, nhanvien_id):
    mohinh = get_object_or_404(MoHinh, pk=mohinh_id)
    nhanvien = get_object_or_404(NhanVien, pk=nhanvien_id)
    all_mau = nhanvien.mau_set.all()
    mau_in_mohinh = all_mau.filter(ds_mohinh=mohinh)

    context = {
        'mohinh': mohinh,
        'nhanvien': nhanvien,
        'all_mau': all_mau,
        'mau_in_mohinh': mau_in_mohinh,
    }
    return render(request, 'mohinh/nhanvien_mau_list.html', context)
