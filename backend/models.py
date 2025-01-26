from django.db import models
import os
from django.conf import settings

class Produk(models.Model):
    no_produk = models.CharField(max_length=20, unique=True, editable=False)
    nama = models.CharField(max_length=100)
    kategori = models.CharField(max_length=50)
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.no_produk:
            total_produk = Produk.objects.count() + 1
            self.no_produk = f'PRD-{total_produk:05}'  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class GambarProduk(models.Model):
    def upload_to_products(instance, filename):
        return f'products/{filename}'

    path_gambar = models.ImageField(upload_to=upload_to_products)
    no_produk = models.ForeignKey('Produk', on_delete=models.CASCADE, related_name='gambar_produk')

    def __str__(self):
        return f"Gambar untuk {self.no_produk.nama}"