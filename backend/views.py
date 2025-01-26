from django.shortcuts import render, get_object_or_404, redirect
from .models import Produk, GambarProduk
from .forms import ProdukForm 
from django.db import transaction
from decimal import Decimal
import os
from django.conf import settings
from django.contrib import messages
from login.models import CustomUser
from django.contrib.auth.decorators import login_required

# CRUD Produk
@login_required
def list_produk(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    produk_list = Produk.objects.all()
    return render(request, 'pages/produk/list_produk.html', {
        'produk_list': produk_list,
        'user': request.user    
    })

def create_produk(request):
    if request.method == 'POST':
        produk_form = ProdukForm(request.POST)
        files = request.FILES.getlist('gambar[]')  

        if produk_form.is_valid():
            produk = produk_form.save()

           
            for file in files:
                GambarProduk.objects.create(path_gambar=file, no_produk=produk)
            
            messages.success(request, "Produk berhasil ditambahkan!")
            return redirect('list_produk')
        else:
            messages.error(request, "Terjadi kesalahan. Silakan cek input Anda.")
    else:
        produk_form = ProdukForm()

    context = {
        'produk_form': produk_form,
        'form_mode': 'create',
    }
    return render(request, 'pages/produk/produk_form.html', context)


def update_produk(request, produk_id):  
    produk = get_object_or_404(Produk, pk=produk_id)

    if request.method == 'POST':
        produk_form = ProdukForm(request.POST, instance=produk)
        files = request.FILES.getlist('gambar[]')  

        if produk_form.is_valid():
            produk = produk_form.save(commit=False)

           
            raw_harga = request.POST.get('harga', '0').replace('.', '').replace(',', '')
            produk.harga = int(raw_harga)  
            produk.save()

           
            for file in files:
                GambarProduk.objects.create(path_gambar=file, no_produk=produk)

            messages.success(request, "Produk berhasil diperbarui!")
            return redirect('list_produk')
        else:
            messages.error(request, "Terjadi kesalahan. Silakan cek input Anda.")
    else:
        produk_form = ProdukForm(instance=produk)

    gambar_produk = GambarProduk.objects.filter(no_produk=produk)

    context = {
        'produk_form': produk_form,
        'form_mode': 'edit',
        'produk': produk,
        'gambar_produk': gambar_produk,
    }
    return render(request, 'pages/produk/produk_form.html', context)


def delete_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    produk.delete()
    messages.success(request, 'Produk berhasil dihapus.')
    return redirect('list_produk')   

 
def tampilkan_gambar_produk(request, no_produk):
    produk = get_object_or_404(Produk, no_produk=no_produk)
    gambar_produk = GambarProduk.objects.filter(no_produk=produk)
    context = {
        'gambar_produk': gambar_produk,
        'produk': produk
    }
    return render(request, 'pages/produk/update.html', context)

 