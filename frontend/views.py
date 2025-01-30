from django.shortcuts import render
from backend.models import Produk, GambarProduk, Kategori
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
    produk_list = Produk.objects.prefetch_related('gambar_produk').all()
    kategori_list = Kategori.objects.all()
    nomor_wa = "6289527310809"   
    return render(request, 'index.html', {
        'produk_list': produk_list,
        'kategori_list': kategori_list,
        'nomor_wa': nomor_wa,
    })

def product_details(request, no_produk):
    produk = get_object_or_404(Produk, no_produk=no_produk)
    gambar_produk = GambarProduk.objects.filter(no_produk=produk)
    context = {
        'produk': produk,
        'gambar_produk': gambar_produk,
    }
    return render(request, 'product-details.html', context)
