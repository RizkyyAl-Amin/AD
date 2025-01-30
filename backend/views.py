from django.shortcuts import render, get_object_or_404, redirect
from .models import Produk, GambarProduk
from .forms import ProdukForm, KategoriForm, CreateAkunForm
from django.contrib import messages
from login.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Kategori
 
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

    kategori_list = Kategori.objects.all()   

    context = {
        'produk_form': produk_form,
        'kategori_list': kategori_list,  
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
            produk.harga = int(raw_harga) / 100  
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
    kategori_list = Kategori.objects.all()

    context = {
        'produk_form': produk_form,
        'form_mode': 'edit',
        'produk': produk,
        'gambar_produk': gambar_produk,
        'kategori_list': kategori_list,
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

def list_kategori(request):
    kategori = Kategori.objects.all()
    return render(request, 'pages/kategori/list_kategori.html', {"kategori": kategori})

def create_kategori(request):
    if request.method == "POST":
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_kategori")
    else:
        form = KategoriForm()
    
    return render(request, "pages/kategori/kategori_form.html", {
        "form": form,
        "form_mode": "create"
    })

def update_kategori(request, kategori_id):
    kategori = get_object_or_404(Kategori, id=kategori_id)
    if request.method == "POST":
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            return redirect("list_kategori")
    else:
        form = KategoriForm(instance=kategori)
    
    return render(request, "pages/kategori/kategori_form.html", {
        "form": form,
        "form_mode": "update",
        "kategori": kategori
    })

def delete_kategori(request, kategori_id):
    kategori = get_object_or_404(Kategori, id=kategori_id)
    kategori.delete()
    return redirect("list_kategori")

@login_required
def list_akun(request):
    users = CustomUser.objects.all()
    return render(request, "pages/akun/list_akun.html", {"users": users})

@login_required
def create_akun(request):
    if request.method == "POST":
        form = CreateAkunForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun berhasil dibuat!")
            return redirect("list_akun")
    else:
        form = CreateAkunForm()
    
    return render(request, "pages/akun/create_akun.html", {"form": form})

@login_required
def delete_akun(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, "Akun berhasil dihapus!")
    return redirect("list_akun")